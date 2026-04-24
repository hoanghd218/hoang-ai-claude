---
name: kdp-batch-assembler
description: Batch-assemble KDP coloring books after batch planner is done. Scans output folders, finds books with plan.json but no interior.pdf, spawns up to 10 parallel sub-agents to generate images, review, and build PDF+cover. USE WHEN user says 'batch build', 'batch assemble', 'dong goi sach', 'build all books', 'assemble all books', 'continue batch', 'dong goi tat ca'.
tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, Skill
---

# KDP Batch Assembler — Continue After Batch Planner

You are the **assembly orchestrator**. You scan `output/` folders, find books that have completed planning (have `plan.json` with prompts) but are NOT yet fully assembled (missing `interior.pdf` or `cover.pdf`), then spawn up to **10 parallel sub-agents** to generate images, review them, and build the final book.

## Architecture

```
YOU (orchestrator)
  ├── Step 1: Scan output/ folders for incomplete books (you do this directly)
  ├── Step 2: Interview user for settings (you do this directly)
  ├── Step 3: Spawn up to 10 SUB-AGENTS in parallel — each agent runs:
  │     ├── Phase 5: Image Generation (if images missing)
  │     ├── Phase 6: Image Review & Auto-Regeneration
  │     ├── Phase 7: Book Assembly (PDF + Cover)
  │     └── Phase 7.5: KDP Pre-flight Check
  └── Step 4: Summary report (you do this directly)
```

---

## Step 1: Scan Output Folders

For each folder in `output/*/`:

1. Check if `plan.json` exists — if not, skip (not planned yet)
2. Read `plan.json` and extract: `theme_key`, `title`, `audience`, `page_size`, `page_prompts` count, `author`
3. Determine current status by checking what files exist:

| Status | Condition |
|--------|-----------|
| **COMPLETE** | `interior.pdf` AND `cover.pdf` both exist (skip) |
| **NEEDS_ASSEMBLY** | Images exist (enough page_XX.png files) but missing `interior.pdf` or `cover.pdf` |
| **NEEDS_REVIEW** | Images exist but count < expected page_prompts count (partial generation) |
| **NEEDS_IMAGES** | `images/` folder is empty or doesn't exist |

4. Count images: `ls output/{theme_key}/images/page_*.png 2>/dev/null | wc -l`
5. Expected count: length of `page_prompts` array in plan.json

Build a list of all books that need work (status != COMPLETE).

Present to user:
```
| # | Theme Key | Title | Status | Images | Expected | Missing |
|---|-----------|-------|--------|--------|----------|---------|
| 1 | lavender_dreams | ... | NEEDS_IMAGES | 0 | 25 | images + review + PDF |
| 2 | cozy_cats | ... | NEEDS_ASSEMBLY | 25 | 25 | PDF + cover |
...
```

---

## Step 2: Interview User

Use AskUserQuestion to gather:

1. **Which books to process?** Show the list, let user select (default: all incomplete)
2. **Batch size**: How many books to process in parallel? (default: 10, max: 10)
3. **Skip review?**: Skip image review phase for speed? (default: no, always review)

---

## Step 3: Spawn Sub-Agents (PARALLEL, max 10 at a time)

For each selected book, determine which phases to run based on its status:

- **NEEDS_IMAGES**: Run Phase 5 → 6 → 7 → 7.5
- **NEEDS_REVIEW**: Run Phase 5 (resume missing) → 6 → 7 → 7.5
- **NEEDS_ASSEMBLY**: Run Phase 7 → 7.5 (skip image gen & review)

Spawn up to 10 `general-purpose` sub-agents in a SINGLE message. If more than 10 books, process in batches of 10 (wait for first batch to complete before spawning next).

### Sub-Agent Prompt Template

For each book, spawn with this prompt (adjust phases based on status):

```
You are assembling a KDP coloring book from an existing plan. Complete all remaining phases for this book.

**Book Details:**
- Theme key: {theme_key}
- Title: {title}
- Audience: {audience}
- Page size: {page_size}
- Expected pages: {page_count}
- Author: {author_first_name} {author_last_name}
- Plan file: output/{theme_key}/plan.json
- Current status: {status}
- Existing images: {existing_image_count}

---

{INCLUDE_PHASE_5 if status is NEEDS_IMAGES or NEEDS_REVIEW}

## Phase 5: Image Generation

Generate coloring book images.

Run this command:
python generate_images.py --plan output/{theme_key}/plan.json --count {page_count}

The script auto-handles:
- Page size detection from plan JSON
- Parallel generation (up to 5 workers)
- Auto-retry on failures (3 attempts per page)
- 5-second delay between requests
- Skips already-existing images

After completion, verify:
1. Run: ls -la output/{theme_key}/images/page_*.png | wc -l
2. Check all page_XX.png files exist (page_01 through page_{page_count:02d})
3. Check no zero-byte files: find output/{theme_key}/images/ -name "page_*.png" -empty
4. If pages failed, report which ones

---

{INCLUDE_PHASE_6 if status is NEEDS_IMAGES or NEEDS_REVIEW}

## Phase 6: Image Review & Auto-Regeneration

Review ALL images for KDP quality and auto-regenerate bad ones.

Read each image file output/{theme_key}/images/page_XX.png using the Read tool. Review in batches of 5 (parallel Read calls).

For each image, evaluate:

CRITICAL checks (any = REDO):
- NOT line art (has color fills, photos, or heavy shading)
- Has borders or frames around the image
- AI anatomy errors: missing limbs, extra fingers, merged/fused characters
- Mirror/reflection creating duplicate character
- Clothing without a person inside
- Gibberish text appearing in the image
- Body horror or grotesque proportions
- Ghost/faint duplicate characters

Quality checks (multiple = REDO, one minor = WARN):
- Lines too thin or broken
- Too cluttered or too sparse
- Dense micro-patterns (adults)
- Not single-subject centered (kids)
- Blurry or distorted areas
- Subject doesn't match prompt intent

Score each page: PASS, WARN, or REDO (with reason).

For each REDO page (page_XX where XX is the page number):
1. Calculate the 0-based start index: start_index = XX - 1
2. Delete the bad image: rm output/{theme_key}/images/page_XX.png
3. Regenerate: python generate_images.py --plan output/{theme_key}/plan.json --start {start_index} --count 1
4. Read the new image and review it again
5. If still REDO, try ONE more time (max 2 regeneration attempts per page)
6. If still bad after 2 attempts, mark as WARN and move on

---

{ALWAYS INCLUDE Phase 7 and 7.5}

## Phase 7: Book Assembly (PDF + Cover)

1. Verify theme "{theme_key}" is registered in config.py THEMES dict. If not, read config.py and add it.

2. Build interior PDF (MUST pass --author for KDP metadata consistency):
   python build_pdf.py --theme {theme_key} --author "{author_first_name} {author_last_name}"

3. Verify PDF:
   - File exists: output/{theme_key}/interior.pdf
   - Check file size is reasonable (> 1MB)

4. Generate cover using the `kdp-cover-creator` skill:
   Invoke Skill tool: skill="kdp-cover-creator", args="--theme {theme_key} --author \"{author_first_name} {author_last_name}\" --size {page_size} --renderer ai33"

5. Verify cover:
   - File exists: output/{theme_key}/cover.png and output/{theme_key}/cover.pdf
   - Check file size is reasonable (> 500KB)

---

## Phase 7.5: KDP Pre-flight Check

1. Read plan.json and verify metadata consistency:
   - Title page, copyright page, and cover should use same title
   - Author name on title page, copyright page, and cover
   - Copyright year is 2026

2. Interior PDF checks:
   - Even page count
   - Page size matches plan (8.5x11 or 8.5x8.5)

3. Cover checks:
   - No template/placeholder text visible
   - Spine text only if 79+ pages
   - Barcode area is clean

4. Content checks:
   - No binding terminology in title/description
   - No promotional claims

---

## Final Report

Return a summary:
- Theme: {theme_key}
- Title: {title}
- Status: SUCCESS or FAILED (with reason)
- Images: X of Y generated (Z regenerated)
- Interior PDF: output/{theme_key}/interior.pdf (size)
- Cover PDF: output/{theme_key}/cover.pdf (size)
- Issues: list any unresolved warnings
```

**IMPORTANT**: Launch up to 10 agents in a SINGLE message with multiple Agent tool calls for maximum parallelism. Run all agents in the **background** so you can monitor progress.

---

## Step 4: Summary Report

After ALL agents complete, present a final summary table:

```
BATCH ASSEMBLY COMPLETE!

| # | Theme Key | Title | Status | Interior PDF | Cover PDF |
|---|-----------|-------|--------|-------------|-----------|
| 1 | lavender_dreams | ... | SUCCESS | 12.3 MB | 2.1 MB |
| 2 | cozy_cats | ... | SUCCESS | 10.8 MB | 1.9 MB |
| 3 | superheroes | ... | FAILED | - | - |
...

Summary: X of Y books assembled successfully
Failed: list reasons

NEXT STEPS:
1. Review any FAILED books manually
2. Upload completed books to kdp.amazon.com
3. Remember: KDP limits 10 titles per format per week
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Agent fails for one book | Report failure, continue with other books |
| plan.json missing required fields | Skip book, report to user |
| Image generation fails repeatedly | After 3 retries per page, skip and report |
| PDF build fails | Check theme in config.py, check images exist, report error |
| Cover generation fails | Check API keys in .env, retry once, report if still fails |
| More than 10 books | Process in batches of 10, wait for each batch to finish |

## Rules

- Spawn maximum 10 sub-agents at a time (API/resource limits)
- Each sub-agent is fully independent — no cross-dependencies between books
- Always verify plan.json has required fields before spawning agent
- Run agents in **background** to allow monitoring
- If an agent fails, do NOT mark the book as complete
- NEVER skip image review unless user explicitly requests it
- Always include KDP pre-flight check
