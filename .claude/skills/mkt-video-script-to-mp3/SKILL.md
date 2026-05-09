---
name: mkt-video-script-to-mp3
description: Convert video scripts (Vietnamese/English) to MP3 voiceover audio using MiniMax TTS API (speech-2.8-hd model). Use when user wants to generate voiceover audio from a script, convert text to speech for video production, create MP3 from script text, or needs TTS for video pipeline. USE WHEN user says 'tạo audio từ script', 'script to mp3', 'text to speech', 'tạo voiceover', 'convert script to audio', 'tạo mp3 từ kịch bản', 'generate voiceover', 'TTS from script', 'đọc script thành audio'.
---

# Video Script to MP3

Convert video scripts to MP3 voiceover using MiniMax TTS API.

## Defaults

- **Model**: `speech-2.8-hd`
- **Voice**: `moss_audio_c56d6120-ef9c-11f0-9649-8ee40147f116`
- **Speed**: `1.08`
- **Language**: Vietnamese
- **Format**: MP3 (32kHz, 128kbps, mono)

## Quick Usage

### Via Python script (recommended for long scripts)

```bash
uv run .claude/skills/mkt-video-script-to-mp3/scripts/text_to_mp3.py \
  --file path/to/script.txt \
  -o workspace/content/YYYY-MM-DD/voiceover.mp3
```

### Via script with custom options

```bash
uv run .claude/skills/mkt-video-script-to-mp3/scripts/text_to_mp3.py \
  "Xin chào các bạn" \
  -o output.mp3 \
  --speed 1.1 \
  --language_boost Vietnamese
```

### Via MiniMax MCP tool (short text only)

```
mcp__minimax__text_to_audio(
  text="...",
  voice_id="moss_audio_c56d6120-ef9c-11f0-9649-8ee40147f116",
  model="speech-2.8-hd",
  speed=1.08,
  language_boost="Vietnamese",
  output_directory="workspace/assets/minimax/"
)
```

Note: MCP tool uses different API version. Prefer the Python script for production voiceovers as it calls `t2a_v2` with full parameter support.

## Workflow

1. Read or receive video script text
2. Save script to a `.txt` file if needed
3. Run `text_to_mp3.py` with appropriate output path
4. Script returns: duration, file size, character count
5. Use output MP3 in video production pipeline (Remotion, HeyGen, etc.)

## Output Convention

Save MP3 files to: `workspace/content/YYYY-MM-DD/video-short/<project>/voiceover.mp3`

## API Details

See [references/minimax-tts-api.md](references/minimax-tts-api.md) for full API parameters including `pronunciation_dict`, `voice_modify` (echo effects), and response format.

## Requirements

- `MINIMAX_API_KEY` in project `.env` file
- Python dependencies managed via PEP 723 inline metadata (auto-installed by `uv run`)
