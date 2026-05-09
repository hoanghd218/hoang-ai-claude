---
name: mkt-video-url-to-script-notion
description: End-to-end orchestrator — take one or more short-form video URLs (YouTube Shorts / IG Reels / TikTok / any yt-dlp URL), extract transcripts, generate Vietnamese short-video scripts with 4 hook variations (Bold / Data / Counter-intuition / Myth-bust) per video, show them to the user for review, then push approved scripts to the Notion short-video DB. Delegates transcription to the `mkt-video-transcript-fetcher` sub-agent and script writing to the `mkt-script-hook-writer` sub-agent for context isolation. USE WHEN user says 'viết script từ video url push notion', 'video url to script notion', 'từ video ra script đẩy notion', 'transcript to hooks to notion', 'orchestrate video script pipeline', or pastes a video URL with a request to turn it into a Notion-ready short-video script.
---

# Video URL → 4 Hooks + Script → Notion (orchestrator)

End-to-end pipeline with a **mandatory user review checkpoint** before anything is written to Notion. Delegates heavy work to 2 sub-agents so main context stays light.

```
URL(s) ──► [sub-agent 1] ──► transcript ──► [sub-agent 2] ──► 4 hooks + script
                                                                    │
                                                     USER REVIEW CHECKPOINT
                                                                    │
                                                              push_to_notion.py
```

---

## Prerequisites

- `.env` at repo root with:
  - `NOTION_API_KEY=<valid token>`
  - `NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID=<db id>`
- `uv` + `ffmpeg` installed (for the transcription sub-skill).
- Notion integration shared with the target DB.

The `mkt-ideas-to-script-notion/scripts/push_to_notion.py` helper is **reused as-is** — do not duplicate it.

---

## 5-Phase Workflow

**Start:** `TodoWrite` 5 items — one per phase.

### Phase 1 — Parse input

Accept any of:
- Single URL: `https://www.youtube.com/shorts/xyz`
- Multiple URLs in the same message
- URL + inline instructions (angle, things to avoid)

Extract for each URL:
- `url`
- optional `angle` (what direction the script should take)
- optional `avoid` (things not to mention — e.g. *"không được nói về day 21"*)

Create work dir: `/tmp/video-script-<timestamp>/`. Mark Phase 1 done.

### Phase 2 — Transcripts (sub-agent, parallel)

For each URL, spawn a **`mkt-video-transcript-fetcher`** sub-agent via the Task tool.

- If multiple URLs, spawn them **in parallel** (single message, multiple Task tool calls).
- Each sub-agent returns one `RESULT_JSON:` line with `{url, source_title, duration_sec, transcript_text, transcript_path, mp4_path, language}`.
- Collect all results into an array. Skip any URL whose sub-agent returned `{"error": ...}` and report it to the user.

Mark Phase 2 done.

### Phase 3 — Scripts (sub-agent, parallel)

For each collected transcript, spawn a **`mkt-script-hook-writer`** sub-agent in parallel.

Input blob per sub-agent:
```json
{
  "transcript_text": "...",
  "source_title": "...",
  "source_url": "...",
  "duration_sec": N,
  "angle": "<from phase 1, if any>",
  "avoid": "<from phase 1, if any>"
}
```

Each returns a `RESULT_JSON:` line with `{title, structure, duration_sec, hooks:{A,B,C,D}, body, editor_notes, references, source_url, source_title}`.

Collect into a `drafts[]` array. Mark Phase 3 done.

### Phase 4 — USER REVIEW CHECKPOINT (mandatory — blocking)

Print **all drafts inline** in readable markdown:

```
─── Draft 1/N ──────────────────────────
Title: <title>
Structure: <structure> · ~<duration_sec>s

Hook A: …
Hook B: …
Hook C: …
Hook D: …

[Body preview — full text with [REF: …] markers]

Editor notes: …
```

Then ask exactly:

> *"Đồng ý push hết lên Notion / chỉ push #a,#b / sửa trước (nói rõ chỗ nào sửa)?"*

**Block until user responds.** Handle:
- **Approve all** → go to Phase 5 with all drafts.
- **Approve subset** (e.g. "push #1,#3") → filter drafts, go to Phase 5.
- **Edit request** → edit the draft in place (main skill does the edit, does NOT re-spawn sub-agent for small edits). Re-print, ask again.
- **Reject all** → exit cleanly, no Notion write. Summarize what was dropped.

Do NOT skip this checkpoint. Do NOT push to Notion before explicit approval.

### Phase 5 — Push to Notion

Format approved drafts into the exact schema `push_to_notion.py` expects:

```json
[
  {
    "title": "<draft.title>",
    "structure": "<draft.structure>",
    "status": "Kịch bản",
    "duration_sec": <draft.duration_sec>,
    "script_body": "[HOOK — 4 variations]\nHook A: …\nHook B: …\nHook C: …\nHook D: …\n[REF: source_url]\n\n<draft.body>\n\n[GHI CHÚ EDITOR]\n<draft.editor_notes>",
    "references": [{"url": "<source_url>", "note": "Video nguồn"}, ...<draft.references>]
  }
]
```

Write to `/tmp/scripts_to_push.json`, then:

```bash
python3 .claude/skills/mkt-ideas-to-script-notion/scripts/push_to_notion.py --input /tmp/scripts_to_push.json
```

Report to user:
- ✅ Count of pages created + Notion URLs for each
- ❌ Any failures (title + error message)
- Location of `/tmp/video-script-<timestamp>/` (transcripts + MP4s are still there if they want to save later)

Mark Phase 5 done.

---

## Why 2 sub-agents

- **Context isolation:** each transcript can be 1-3KB; a script pass balloons to 5-8KB with hooks + body + notes. Keeping these out of the main orchestrator context means the checkpoint step doesn't risk compression.
- **Parallelism:** batch runs (3 URLs at once) finish in ~1/3 the wall time vs sequential.
- **Clear contract:** each sub-agent has one job, returns one JSON line — easy to debug, easy to swap.

---

## Hard Rules

- Phase 4 is **mandatory** and **blocking**. Never push Notion before explicit user approval.
- If ANY draft fails a brand rule (`tui`/`tôi` instead of `mình`, English jargon other than brand names, missing CTA), fix in place during Phase 4 before push.
- Default CTA (unless user said otherwise): `Comment "Agent" mình gửi bạn link nhóm học Agents miễn phí nhé.`
- Default status on Notion: `Kịch bản`.
- Do NOT save MP4/transcript to Google Drive by default (user said no to Drive save).

---

## Error Handling

| Failure | Behavior |
|---------|----------|
| URL yt-dlp cannot download | Sub-agent 1 returns `{"error": "..."}`, main skill skips that URL, reports to user, continues with others |
| Whisper fails (ffmpeg missing) | Instruct user to `brew install ffmpeg`, abort |
| Notion 401 | `NOTION_API_KEY` invalid. Report token rejected, suggest regenerating |
| Notion 404 on DB | Integration not shared with DB. Instruct user to add connection |
| User rejects all at checkpoint | Exit cleanly, summarize what was dropped, work dir preserved |

---

## Files this skill touches

- `.claude/skills/mkt-video-url-to-transcript/scripts/download_and_transcribe.py` (via sub-agent 1)
- `.claude/skills/mkt-transcript-to-hooks-script/SKILL.md` (via sub-agent 2)
- `.claude/skills/mkt-ideas-to-script-notion/scripts/push_to_notion.py` (direct reuse)
- `.claude/agents/mkt-video-transcript-fetcher.md` (sub-agent 1)
- `.claude/agents/mkt-script-hook-writer.md` (sub-agent 2)
