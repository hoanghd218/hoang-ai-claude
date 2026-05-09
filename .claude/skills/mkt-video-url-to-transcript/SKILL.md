---
name: mkt-video-url-to-transcript
description: Download a short-form video (YouTube Shorts / Instagram Reels / TikTok / any yt-dlp-supported URL) and transcribe it with local Whisper, producing an MP4 + plaintext transcript + SRT + metadata JSON. Auto-detects source language. This is a sub-skill invoked by the `mkt-video-url-to-script-notion` orchestrator (and its `mkt-video-transcript-fetcher` sub-agent). USE WHEN user says 'download + transcribe video', 'tải video + bóc transcript', 'video url to transcript', 'transcribe youtube shorts', 'transcribe instagram reel', 'whisper một video url', or when a parent workflow needs raw transcript text from a video URL.
---

# Video URL → Transcript

Single-purpose sub-skill: **video URL → MP4 + transcript + metadata**. Does NOT write scripts, does NOT push Notion — those are other skills. This one owns the "extract script info trong video gốc" step.

---

## Prerequisites

- `uv` installed (`which uv` → ok)
- `ffmpeg` installed (`which ffmpeg` → ok — `brew install ffmpeg` if missing)

Both were set up earlier today on this machine.

---

## Usage

```bash
python3 .claude/skills/mkt-video-url-to-transcript/scripts/download_and_transcribe.py \
  --url "<video_url>" \
  [--output-dir /tmp/videosrc-<id>] \
  [--model base]
```

**Args:**
- `--url` (required) — any URL yt-dlp supports (YouTube / IG Reel / TikTok / Twitter / Facebook / …)
- `--output-dir` (optional) — default `/tmp/videosrc-<slug>` where slug is derived from the URL
- `--model` (optional) — Whisper model size. Default `base`. Use `small` for better Vietnamese accuracy.

**Side effects** — files written to `output_dir`:
- `video.mp4` — downloaded video
- `video.info.json` — yt-dlp metadata
- `video.txt` — plaintext transcript (one block)
- `video.srt` — segment-level subtitles
- `metadata.json` — unified summary (same as stdout)

**stdout** — one JSON object for the caller to parse:

```json
{
  "url": "https://www.youtube.com/shorts/XYZ",
  "source_title": "Video title from uploader",
  "duration_sec": 80,
  "language": "english",
  "transcript_text": "Full plaintext transcript…",
  "transcript_path": "/tmp/videosrc-XYZ/video.txt",
  "srt_path": "/tmp/videosrc-XYZ/video.srt",
  "mp4_path": "/tmp/videosrc-XYZ/video.mp4",
  "output_dir": "/tmp/videosrc-XYZ"
}
```

---

## How it works

1. Runs `uvx yt-dlp --no-playlist -f "best[ext=mp4]/best" -o video.%(ext)s --write-info-json <url>`.
2. Runs `uvx --from openai-whisper whisper video.mp4 --model <M> --output_format txt --output_format srt` — no `--language` flag, so Whisper auto-detects.
3. Parses `Detected language:` from Whisper stderr.
4. Reads yt-dlp's `.info.json` for title + duration.
5. Writes `metadata.json` and prints it to stdout.

---

## Error handling

| Failure | Behavior |
|---------|----------|
| yt-dlp returns non-zero | Exit 1, last 500 chars of stderr to stderr |
| Whisper returns non-zero | Exit 1, last 500 chars of stderr to stderr |
| `ffmpeg` missing | Whisper errors with `FileNotFoundError: 'ffmpeg'` — user must `brew install ffmpeg` |
| URL returns 404 / private | yt-dlp errors; caller should skip this URL |

---

## Notes

- Script is idempotent on `output_dir` — re-running overwrites previous files.
- For Vietnamese voiceovers you may prefer `--model small` (better accuracy, ~2× slower); English auto-detect works fine with `base`.
- This skill DOES NOT call `mkt-ai-video-extract-srt-segment` because that one forces `--language vi` and emits a different JSON (word-level segments) that's not needed here. The script in this skill is simpler and language-agnostic.
