---
name: mkt-ideas-to-script-notion
description: Convert a list of short-video ideas (with reference links for images/videos) into full Vietnamese scripts using the Before-After / Three Acts / Action framework, then push each script to the Notion short-video script database — preserving ALL reference links both as inline [REF] markers inside the script and as a dedicated Reference Links field so the video editor can fetch the assets. USE WHEN user says 'ý tưởng thành script notion', 'ideas to script notion', 'viết script từ ý tưởng và đẩy notion', 'tạo script ngắn từ list ý tưởng', 'batch script notion', 'script short video to notion', 'ideas to notion'.
---

# Ideas → Short Video Script → Notion

Batch pipeline: takes N video ideas (each with optional reference links to images / videos / articles), writes a full Vietnamese short-video script for each using the v1 storytelling framework (Before-After / Three Acts / Action), then creates one Notion page per script in the target database.

**Key requirement:** Every reference link supplied with an idea MUST end up in the Notion page in two places:
1. **Inline in the script body** as `[REF: url]` markers positioned where the editor should insert that image/video.
2. **A dedicated Reference Links section** (field or page block) listing every link, so the editor has a single place to copy them all.

---

## Prerequisites

1. **Notion API key** — `NOTION_API_KEY` must be set in `.env` at repo root.
2. **Target database ID** — URL provided by user: `https://www.notion.so/hoangtranbs/c683a4e952634536be963054944bbdf3` → database ID `c683a4e952634536be963054944bbdf3` (formatted: `c683a4e9-5263-4536-be96-3054944bbdf3`).
   - Store in `.env` as `NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID=c683a4e9-5263-4536-be96-3054944bbdf3`.
3. **Integration must be shared with the database** — in Notion, open the DB → `...` → `Connections` → add your integration.

---

## Workflow

### Step 1 — Parse input

Input can arrive in **two ways** (always accept both):

**A. File path** — user passes a `.md` or `.txt` file:
```bash
/mkt-ideas-to-script-notion path/to/ideas.md
```

**B. Inline text** — user pastes ideas directly in the prompt.

Parse the input into a list of idea blocks. Each idea block should have:
- `title` (short name)
- `angle` / `key_points` (what the video is about)
- `references[]` — list of `{url, note}` pairs (may be empty)

Use the input format in [references/input-format.md](references/input-format.md). If the user's input is loose prose, infer the fields — do NOT reject; just parse best-effort and confirm once before writing scripts if ambiguous.

### Step 2 — Fetch Notion database schema

Before writing anything to Notion, fetch the actual schema so property names and types match:

```bash
python3 .claude/skills/mkt-ideas-to-script-notion/scripts/push_to_notion.py --fetch-schema
```

This prints the DB's property names and types. Map fields accordingly. Expected/likely properties (confirm at runtime):
- `Name` (title) — script title
- `Script` (rich text) OR page body — full script with inline `[REF]` markers
- `Reference Links` (rich text or url) — newline-separated list of all links
- `Structure` (select) — `Before-After` | `Three Acts` | `Action`
- `Status` (select) — default to the first available status (e.g. `Draft`, `Ngân hàng`)
- `Date` (date) — today

If a property in the list above does not exist in the schema, **skip it silently**. Never create new properties. If `Name` is not found, abort and report.

### Step 3 — Write one script per idea

For each idea, pick structure by content type using the rules in [references/script-structures.md](references/script-structures.md):

| Content type | Structure |
|--------------|-----------|
| Tips / tool review / hacks / transformations / before-after | **Before-After** |
| Personal story / journey / conflict-driven experience | **Three Acts** |
| Challenge / reaction / tense situation / unexpected | **Action** |

Follow the hard rules in this repo's brand voice:
- First person = **`mình`** (NEVER `tui`, NEVER `tôi`). Address audience as **`bạn`** / **`các bạn`**.
- Hook in first 3 seconds — specific numbers, not generic ("200 view" not "view thấp").
- Short spoken sentences. No lecturing. No English jargon (except brand names: ChatGPT, Claude, AI, Anthropic, …).
- End with a CTA tied to the **AI Freedom Builders** community.
- Length: target 30s–90s spoken (≈ 75–225 words). Adjust if user specifies.
- Write **Last Dab first**, then hook, then fill middle (per brand voice rules).

**Inline reference placement — this is the differentiator of this skill:**

As you write, insert `[REF: <url>]` on its own line immediately after the line where that visual should appear. One marker per visual cue. If an idea has 3 reference links, the script body should contain 3 `[REF: …]` markers placed where each asset best supports the narration. Example:

```
[HOOK]
Hôm qua mình vừa thử Claude Code 2.5 — nó tự fix bug trong 30 giây.
[REF: https://youtu.be/abc123?t=45]

[TRƯỚC]
Bình thường debug cái lỗi này mình mất 20 phút, đọc stack trace muốn nổ đầu.
[REF: https://i.imgur.com/oldway.png]
```

If the idea has reference links the narration doesn't naturally "point to", still place them at the most relevant beat — the editor needs a hint of WHERE to put each asset, not just a flat list.

### Step 4 — Build the script output format

For each idea, produce an object ready for Notion:

```json
{
  "title": "Claude Code 2.5 tự fix bug trong 30 giây",
  "structure": "Before-After",
  "script_body": "[HOOK]\n...\n[REF: url1]\n\n[TRƯỚC]\n...\n[REF: url2]\n\n...",
  "references": [
    {"url": "https://youtu.be/abc123?t=45", "note": "clip demo từ Anthropic"},
    {"url": "https://i.imgur.com/oldway.png", "note": "screenshot stack trace cũ"}
  ],
  "duration_sec": 60,
  "word_count": 180
}
```

### Step 5 — User checkpoint (REQUIRED)

Before pushing to Notion, print a **compact summary** to the user:
- How many scripts produced
- Title + structure + word count for each
- Total reference links preserved

Then ask: *"Đồng ý push [N] script lên Notion DB không? (yes / chỉ push script #1,#3 / sửa trước)"*

Only proceed after explicit approval. If user asks to edit, edit in place before pushing.

### Step 6 — Push to Notion

Write the parsed scripts array to a temp JSON file at `/tmp/scripts_to_push.json`, then call the helper:

```bash
python3 .claude/skills/mkt-ideas-to-script-notion/scripts/push_to_notion.py --input /tmp/scripts_to_push.json
```

The helper:
- Reads `NOTION_API_KEY` and `NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID` from `.env`
- Fetches the live schema and maps fields dynamically
- Creates one page per script
- Body content (page blocks):
  - `## Script` heading
  - The full script with `[REF: url]` markers preserved as inline text
  - `## Reference Links` heading
  - Bulleted list of every reference (`- [note](url)` or just `- url` if no note)
- Prints the URL of each created page

### Step 7 — Report back

After the Python helper finishes, report to the user:
- ✅ N scripts pushed
- Direct links to each new Notion page
- Any failures (with reason)

---

## Usage Examples

### Example A — File input

User says:
> Đẩy cái file `plans/video-ideas-2026-04.md` lên — viết script rồi bắn vô Notion

Steps:
1. Read `plans/video-ideas-2026-04.md`.
2. Parse each `## Idea:` block.
3. Write scripts.
4. Show summary → ask for approval.
5. Push.

### Example B — Inline input

User says:
> Viết script rồi đẩy notion. 3 ý tưởng:
> 1) Claude Code 2.5 tự fix bug. Ref: https://youtu.be/abc (demo), https://i.imgur.com/before.png (screenshot cũ)
> 2) One Person Business — 1 người chạy 5 bot. Ref: https://x.com/xyz/status/123
> 3) AI Agent thay VA. Ref: https://tiktok.com/@aaa/video/111

Steps:
1. Parse 3 ideas inline.
2. Write 3 scripts (likely Before-After for #1, Three Acts for #2, Action for #3 — but use judgment per rules above).
3. Preserve all 4 links inline + in Reference Links field.
4. Checkpoint → push.

---

## Edge Cases

| Case | Handling |
|------|----------|
| No references on an idea | Write script normally, `references: []`, skip Reference Links block in body, leave the field empty |
| Duplicate URLs in references | Deduplicate before inserting |
| Very long reference URLs (>2000 chars) | Keep as-is — Notion rich text supports long URLs, just don't inline-embed twice |
| User provides > 10 ideas at once | Process all, but confirm at checkpoint — mention rate limits |
| DB schema mismatch (missing `Script` field) | Fall back to putting the script in the **page body** only; report which properties were skipped |
| Notion API returns 404 | Integration not shared with DB — instruct user to add connection in Notion UI |
| Notion API returns 401 | `NOTION_API_KEY` missing/invalid — instruct user to check `.env` |

---

## Files

- [scripts/push_to_notion.py](scripts/push_to_notion.py) — Notion API helper (fetch schema + create pages)
- [references/input-format.md](references/input-format.md) — how to structure idea input files
- [references/script-structures.md](references/script-structures.md) — Before-After / Three Acts / Action templates (adapted for this skill)
