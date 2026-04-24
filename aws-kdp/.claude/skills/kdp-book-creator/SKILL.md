---
name: kdp-book-creator
description: Create a KDP coloring book end-to-end by orchestrating sub-agents for planning, image generation & review, and book assembly. USE WHEN the user says 'tao sach', 'create coloring book', 'kdp create book', 'build coloring book end to end', 'make a coloring book', 'tao sach to mau', or otherwise asks to produce a complete KDP coloring book from a concept. Trigger even when the user only gives a concept (e.g. "a book about cozy cats") without explicitly naming the pipeline.
---

# KDP Book Creator — End-to-End Orchestrator

You are the **orchestrator**. You own the interview, plan review, and delivery. All heavy work is delegated to three named sub-agents — each a separate file in `.claude/agents/` that owns a complete chunk of the pipeline:

| Phase | Sub-agent | Job |
|---|---|---|
| 2 | `kdp-plan-writer` | Write all page prompts + cover prompt + SEO metadata → `plan.json` |
| 4 | `kdp-image-worker` | Generate images, review each, auto-regenerate bad ones |
| 5 | `kdp-assembly-worker` | Build interior PDF + cover, run KDP preflight, fix simple issues |

---

## Execution Protocol — READ FIRST

- Run ALL phases **in sequence without stopping**, except Phase 1 (interview) and Phase 3 (plan review) which require user input.
- Do **NOT** ask for confirmation between phases. The user invoked the skill — that is the green light.
- After a sub-agent returns, **immediately proceed to the next phase in the same turn**. No "ready to continue?", no summary-and-stop.
- Between phases, emit ONE short progress sentence (e.g. "Plan done, generating images now"), then continue.
- **Delegate heavy work to sub-agents.** One Agent call = one action from your view; the sub-agent runs autonomously in its own 200K context and only returns when done. This is the key to avoiding mid-run stalls.
- Stop only when: (a) Phase 5 delivered, (b) a blocking error you cannot recover from, or (c) Phase 1 / Phase 3 needs user input.

---

## Pipeline

```
Phase 1: Interview                     (you — pause for user)
Phase 2: Plan Writing                  (Agent: kdp-plan-writer)
Phase 3: Plan Review                   (you — pause for user)
Phase 4: Images — generate + review    (Agent: kdp-image-worker)
Phase 5: Assembly + Preflight          (Agent: kdp-assembly-worker)
   + Deliver                           (you — present to user)
```

---

## Phase 1: Interview (pause for user)

Use **AskUserQuestion** to collect:

1. **Concept** — e.g. "cozy cats in a cafe". Skip if passed as invocation args.
2. **Audience** — Adults (cozy/cute) or Kids (6–12).
3. **Book size** — 8.5x11 (portrait, default) or 8.5x8.5 (square).
4. **Page count** — recommend 25–30.
5. **Theme key** — snake_case slug; suggest one based on concept.
6. **Author** — first name + last name.

**→ Once answered, IMMEDIATELY proceed to Phase 2. Do not re-confirm the answers.**

---

## Phase 2: Plan Writing

Spawn the `kdp-plan-writer` agent:

```
Agent(
  subagent_type: "kdp-plan-writer",
  description: "Write plan for {theme_key}",
  prompt: "
Write the complete plan for this KDP coloring book.

- concept: {concept}
- audience: {audience}
- page_size: {page_size}
- page_count: {page_count}
- theme_key: {theme_key}
- author_first_name: {author_first_name}
- author_last_name: {author_last_name}

Follow your agent spec: read the prompt guide, write cover prompt + {page_count} page prompts, invoke kdp-book-detail skill for SEO metadata, save plan.json + prompts.txt, register the theme in config.py. Return Title, Subtitle, keywords, categories, cover prompt, and 3 sample page prompts.
  "
)
```

**→ When the agent returns, IMMEDIATELY Read `output/{theme_key}/plan.json` and go to Phase 3.**

---

## Phase 3: Plan Review (pause for user)

Read `output/{theme_key}/plan.json` and present to the user:

- Title + Subtitle
- Description (HTML, show raw — it's short)
- 7 Keywords, 2 Categories, Reading Age
- 3–5 sample page prompts

Ask: *"Duyệt để tiếp tục generate images, hoặc cần sửa gì?"*

If changes: edit `plan.json` directly with the Edit tool, re-present the delta, loop until approved.

**→ Once approved, IMMEDIATELY proceed to Phase 4.**

---

## Phase 4: Images

Spawn the `kdp-image-worker` agent:

```
Agent(
  subagent_type: "kdp-image-worker",
  description: "Generate + review images for {theme_key}",
  prompt: "
Generate and review all coloring images for this book.

- theme_key: {theme_key}
- audience: {audience}
- page_count: {page_count}

Follow your agent spec: run generate_images.py, verify every page exists, review each image for KDP quality, auto-regenerate REDOs up to 2 attempts each. Return PASS / WARN / REDO-resolved / REDO-unresolved counts and list any unresolved pages with reasons.
  "
)
```

**→ When the agent returns, keep the unresolved-pages list (you'll surface it at delivery) and IMMEDIATELY proceed to Phase 5.**

If > 30% of pages are unresolved REDOs, pause and ask the user: ship as-is, or regenerate the whole set with a stronger prompt?

---

## Phase 5: Assembly + Preflight + Deliver

Spawn the `kdp-assembly-worker` agent:

```
Agent(
  subagent_type: "kdp-assembly-worker",
  description: "Build PDF + cover for {theme_key}",
  prompt: "
Assemble the final deliverables for this book.

- theme_key: {theme_key}
- author_name: {author_first_name} {author_last_name}
- page_size: {page_size}

Follow your agent spec: verify theme in config.py, build interior PDF with --author, generate cover via kdp-cover-creator skill, run kdp-cover-checker + manual KDP preflight, fix simple issues. Return file paths + sizes + preflight status.
  "
)
```

**→ When the agent returns, deliver to the user:**

```
BOOK COMPLETE!

Interior PDF: output/{theme_key}/interior.pdf
Cover:        output/{theme_key}/cover.pdf   (+ cover.png)
Plan:         output/{theme_key}/plan.json
  - Title:    {title}
  - Keywords: {keywords}

KDP PRE-FLIGHT: {pass summary from kdp-assembly-worker}
{Unresolved-pages list from Phase 4, if any — label "manual review recommended"}

NEXT STEPS
1. kdp.amazon.com → New Paperback
2. Upload interior.pdf + cover.pdf (not PNG)
3. Trim: {page_size}, No bleed
4. Copy title / description / 7 keywords / 2 categories / reading age from plan.json

NOTE: KDP limits 10 titles / format / week.
```

---

## Error Handling

| Failure | Recovery |
|---|---|
| kdp-plan-writer fails on prompts | The agent falls back to writing metadata itself if kdp-book-detail fails. If the agent itself fails twice, retry once with the same inputs. |
| Image generation API fails | kdp-image-worker retries internally. If the report says > 30% unresolved, pause and ask user. |
| build_pdf.py fails | Usually theme missing in config.py; kdp-assembly-worker fixes and retries. |
| Cover fails | Check `GOOGLE_API_KEY` / renderer key; retry once. |

Don't stop the chain on soft failures — retries happen inside each agent. Only surface blockers that genuinely need user input.

---

## Rules

- **Never** call any external LLM API for *writing* prompts or metadata — Claude (you + all three sub-agents) writes everything. This rule is repeated in each agent spec.
- After any sub-agent returns, continue in the same turn. Do not end your turn waiting for a nudge.
- Only 2 user pauses in the whole pipeline: Phase 1 (interview) and Phase 3 (plan review).
- The three sub-agents are **reusable** — `kdp-batch-planner` uses `kdp-plan-writer`, `kdp-batch-assembler` uses `kdp-image-worker` + `kdp-assembly-worker`. Keep agent behavior generic; orchestrator-specific logic stays here.
