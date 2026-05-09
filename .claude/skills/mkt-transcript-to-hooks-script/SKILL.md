---
name: mkt-transcript-to-hooks-script
description: Transform a source video transcript into a full Vietnamese short-video script — 4 distinct hook variations (Bold Statement, Data/Shock, Counter-intuition, Myth Busting) plus a Before-After / Three Acts / Action body with inline [REF] markers. Output is structured JSON ready for review + Notion push. Sub-skill invoked by the `mkt-video-url-to-script-notion` orchestrator (and its `mkt-script-hook-writer` sub-agent). USE WHEN user says 'transcript to 4 hooks', 'viết 4 hook từ transcript', 'transcript to script với 4 hook', or a parent workflow hands you a transcript and needs a Vietnamese short-video script.
---

# Transcript → 4 Hooks + Script

Single-purpose sub-skill: distill one video's transcript into a finished Vietnamese short-video script with 4 hook variations the editor can A/B test. Does NOT download videos, does NOT push Notion.

---

## Input

Either inline arguments in the invoking prompt, or a JSON blob:

```json
{
  "transcript_text": "full plaintext transcript of source video…",
  "source_title": "original uploader's title",
  "source_url": "https://www.youtube.com/shorts/XYZ",
  "duration_sec": 80,
  "angle": "optional: what angle the user wants",
  "avoid": "optional: anything not to mention (e.g. 'don't say day 21')"
}
```

---

## Workflow

### Step 1 — Distill the core idea

Read the transcript. Identify:
- 1-line topic
- Main claim / payoff
- Key supporting points (bullet list, max 6)
- Content type: listicle / demo / personal story / news / comparison
- Best structure (see [references/v1-structures.md](references/v1-structures.md)):
  - Before-After (default, most versatile)
  - Three Acts (if personal story with conflict)
  - Action (if demo/reaction/tension)

### Step 2 — Draft Last Dab + CTA first

Per brand voice: write the closing punchline FIRST, then hook, then middle.

Default CTA (use verbatim unless user overrides):
> *Comment "Agent" mình gửi bạn link nhóm học Agents miễn phí nhé.*

### Step 3 — Write 4 hooks — one per type

Use [references/hook-patterns.md](references/hook-patterns.md). Each hook is 1–2 short spoken sentences, max 3 seconds aloud:

- **Hook A — Bold Statement / Comparison Shock** — compare brands, declare a paradigm shift, drop a strong claim.
- **Hook B — Data / Specific Numbers** — lead with concrete figures (6 update, 60 giây, 90+ công cụ, v.v.).
- **Hook C — Counter-intuition / Personal Contrarian** — "mình vừa làm X, nghe điên nhưng…", unusual personal move.
- **Hook D — Myth Busting / Behavior Disruption** — call out what the audience is currently doing wrong; invert a common assumption.

Every hook must:
- Use `mình` (never `tui`, never `tôi`), address `bạn` / `các bạn`.
- Put the concrete payoff in the first sentence — no warm-up.
- Contain at least one specific detail (number, tool name, action) — no generic hooks.
- Respect the `avoid` list if the caller supplied one.

### Step 4 — Write the body in chosen structure

Follow the template in v1-structures.md. Body = TRƯỚC → CẦU NỐI → SAU → LAST DAB + CTA. Keep:
- Short spoken sentences, conversational.
- Brand names allowed (Claude, ChatGPT, OpenAI, Anthropic, Cursor, Slack, Notion, Jira, Google Docs, Figma, Midjourney, TikTok, Reels, etc.). No other English jargon.
- One `[REF: url]` marker after the line that visually matches each reference URL the caller gave. If only the source URL is available, place `[REF: source_url]` right after the hook.

### Step 5 — Write the editor notes

One short block with:
- Aspect ratio
- Visual recommendations per hook (1 line each)
- Demo / screen recording guidance
- Nhạc (BPM)

### Step 6 — Emit JSON output

Exactly this shape (for the parent orchestrator to collect):

```json
{
  "title": "Script title in Vietnamese",
  "structure": "Before-After|Three Acts|Action",
  "duration_sec": 75,
  "hooks": {
    "A": "Hook A text…",
    "B": "Hook B text…",
    "C": "Hook C text…",
    "D": "Hook D text…"
  },
  "body": "Full body text with inline [REF: url] markers — TRƯỚC → CẦU NỐI → SAU → LAST DAB + CTA",
  "editor_notes": "Short editor notes…",
  "references": [
    {"url": "https://…", "note": "nguồn gốc / cảnh nào"}
  ],
  "source_url": "https://…",
  "source_title": "original title"
}
```

Also produce a human-readable markdown preview (title, 4 hooks, body, editor notes) so the user review step is easy to read. The JSON is the machine output; the markdown is for the human.

---

## Hard Rules — enforced before returning

- [ ] First person = **`mình`** (never `tui`, never `tôi`).
- [ ] 4 distinct hooks, one per type, all reference a concrete detail.
- [ ] Body ends with the CTA (or caller-overridden CTA).
- [ ] Every caller-supplied reference URL appears at least once as `[REF: …]` in body.
- [ ] No English jargon outside allowed brand names.
- [ ] Respect `avoid` list (check final text).
- [ ] Target word count = `duration_sec × 2.8` (Vietnamese speaking pace ~170 wpm).

If any rule fails, fix in place before emitting output.

---

## Files

- [references/hook-patterns.md](references/hook-patterns.md) — 4 hook types with templates + criteria
- [references/v1-structures.md](references/v1-structures.md) — Before-After / Three Acts / Action templates
