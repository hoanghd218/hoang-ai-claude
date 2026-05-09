---
name: mkt-ai-video-extract-srt-segment
description: "Transcribe an MP3 voiceover into an SRT subtitle file and a word-level segments JSON using local OpenAI Whisper. Input is a single MP3 path; output is `<stem>.srt` + `<stem>_segments.json` written next to the MP3 (or to a custom output dir). USE WHEN the user says 'extract srt from mp3', 'trích srt từ mp3', 'transcribe voiceover', 'tạo file srt và segments', 'whisper transcribe', 'bóc transcript có timestamp', 'extract voiceover segments', 'tách SRT từ audio', or any time a downstream skill (plan-short-video-edit, heygen-remotion-short-video-editor) needs an SRT + word-level segments JSON from a voiceover MP3 and one does not already exist."
---

# MKT AI Video — Extract SRT + Segments from MP3

Transcribe a voiceover MP3 into two files used throughout the short-video production pipeline:

1. **`<stem>.srt`** — standard SRT subtitles (segment-level timestamps, used for captions)
2. **`<stem>_segments.json`** — word-level timestamps (used for precise SFX placement, word-by-word caption animation, and segment classification downstream)

Both files are written **next to the MP3** by default. Filenames follow the MP3 stem — e.g. `voiceover.mp3` → `voiceover.srt` + `voiceover_segments.json`.

## When to use this skill

- User hands you an MP3 voiceover and asks for SRT / transcript / segments
- A downstream skill (`plan-short-video-edit`, `heygen-remotion-short-video-editor`, caption rendering) needs word-level timestamps and they don't exist yet
- You need to regenerate segments for an existing voiceover (e.g. after re-recording)

If both output files already exist and are newer than the MP3, prefer reusing them instead of re-running Whisper.

## Input

| Arg | Required | Default | Notes |
|-----|----------|---------|-------|
| `mp3_path` | yes | — | Absolute path to the MP3 file |
| `language` | no | `vi` | Whisper language code. Use `vi` for Vietnamese voiceovers, `en` for English |
| `model` | no | `base` | Whisper model size: `tiny` / `base` / `small` / `medium` / `large`. `base` is a good balance for Vietnamese; `small` gives noticeably better Vietnamese accuracy at ~2x the cost |
| `output_dir` | no | MP3's parent folder | Where to write the SRT + JSON |

## Step 1 — Run the transcription script

Reuse the existing Whisper script from the `heygen-short-video` skill — it already implements exactly this behavior, so we don't duplicate code:

```bash
uv run .claude/skills/heygen-short-video/scripts/transcribe_mp3.py "<mp3_path>" --language vi --model base
```

This produces:
- `<mp3_parent>/<stem>.srt`
- `<mp3_parent>/<stem>_segments.json`

To write outputs somewhere else, append `--output-dir <path>`.

**Example** — for `workspace/content/2026-04-09/video-short/learn-claude-code/voiceover.mp3`:

```bash
uv run .claude/skills/heygen-short-video/scripts/transcribe_mp3.py \
  "workspace/content/2026-04-09/video-short/learn-claude-code/voiceover.mp3" \
  --language vi --model base
```

Outputs:
- `workspace/content/2026-04-09/video-short/learn-claude-code/voiceover.srt`
- `workspace/content/2026-04-09/video-short/learn-claude-code/voiceover_segments.json`

## Step 2 — Sanity-check the output

After the script finishes, confirm both files exist and have non-trivial content:

```bash
ls -lh "<output_dir>/<stem>.srt" "<output_dir>/<stem>_segments.json"
head -20 "<output_dir>/<stem>.srt"
```

Expected:
- SRT starts with `1\n00:00:00,000 --> 00:00:0X,XXX\n<text>\n\n`
- JSON is an array of objects, each with `id`, `start`, `end`, `text`, and a `words` array of `{word, start, end}`

If either file is missing or empty, the run failed — re-read stderr from Step 1 and surface the error to the user rather than silently continuing.

## Output format reference

### `voiceover.srt`

```
1
00:00:00,000 --> 00:00:05,139
Đây là tài liệu học Claude Code tốt nhất mình từng thấy…

2
00:00:05,139 --> 00:00:07,299
Nếu bạn mới bắt đầu tìm hiểu Claude Code,
```

### `voiceover_segments.json`

```json
[
  {
    "id": 0,
    "start": 0.0,
    "end": 5.14,
    "text": "Đây là tài liệu học Claude Code tốt nhất…",
    "words": [
      { "word": "Đây", "start": 0.0, "end": 0.34 },
      { "word": "là",  "start": 0.94, "end": 1.12 }
    ]
  }
]
```

Word-level timestamps are what make this JSON valuable — downstream skills use them for word-by-word caption animation, per-word SFX cues, and precise segment boundary detection. Do **not** drop the `words` array when post-processing.

## Step 3 — Script-based text correction (REQUIRED when script is available)

Whisper often mangles Vietnamese mixed with English tech terms (e.g. "Claude Code" → "Clocot", "MCP Servers" → "MCP Service", "prompt" → "PromGtt"). **Always** perform this correction when the original script is available (it almost always is in the video pipeline). Correct the SRT/JSON **text** while preserving all **timestamps**:

1. Read the generated SRT + JSON (keep every `start`/`end` unchanged).
2. Align each SRT entry against the matching chunk of the original script by position.
3. Replace the Whisper text with the script text for that chunk.
4. Mirror the same correction into `voiceover_segments.json` at the segment-level `text` field. Word-level entries can stay as Whisper produced them unless you have a reliable word alignment — it's fine to leave `words[].word` as-is because downstream skills mainly use word timings, not the word strings.
5. Write both files back in place.

**Why**: SRT text is used for rendered captions. Wrong text = wrong captions. Timestamps from Whisper are trustworthy; text is not.

Skip this step ONLY if the user explicitly did not provide a script. In the full video pipeline (`mkt-full-ai-video`), the script is always available — so this correction is always performed.

## Tips & gotchas

- **Model choice**: `base` handles most clean voiceovers fine. For noisy recordings or heavy accent, jump to `small` or `medium`. Costs rise quickly beyond `small` and rarely pay back for short-form content.
- **Language**: Always pass `--language vi` explicitly for Vietnamese. Auto-detect occasionally falls back to other languages on short clips.
- **Reruns**: Whisper is deterministic for the same model + audio, so rerunning only helps if you change the model or fix audio. Don't rerun hoping for better results at the same model size.
- **Path quoting**: Always quote the MP3 path — workspace folders often contain hyphens, dates, and slashes that will break unquoted shell expansion.
- **No duplication**: This skill deliberately does **not** ship its own script. If you find yourself about to write a new transcription script, stop — use `heygen-short-video/scripts/transcribe_mp3.py`. If that script needs changes, edit it there so every consumer benefits.

## Hand-off

After both files are saved and verified, report back with:

```
SRT:      <absolute path>.srt
Segments: <absolute path>_segments.json
Segments count: N
Total duration: X.Xs
```

Then let the user (or the calling skill) decide the next step — typically `plan-short-video-edit` for production planning, or direct consumption by `heygen-remotion-short-video-editor`.
