---
name: raw-short-video-editor
description: "Edit short videos from raw filmed clips — auto-transcribe with local Whisper, auto-cut silence/gaps (jump cuts), add TikTok-style captions (bold stroke text, word-by-word highlight), zoom effects, transitions, BGM, and sound effects using Remotion. Input is multiple raw video files in order. Output is a viral-ready 9:16 short video. Different visual style from HeyGen pipeline — uses TikTokCreator composition with stroke captions instead of backdrop-blur boxes. USE WHEN user says 'edit video thô', 'ghép video quay', 'auto cut video', 'tạo short từ clip', 'edit raw clips', 'cắt ghép video', 'video editor từ clip thô', 'chỉnh sửa video thô', 'tạo tiktok từ video quay', 'auto cut silence', 'jump cut video', 'ghép clip quay tay', 'edit clip thô thành video', 'raw video editor', 'cắt im lặng video'."
---

# Raw Short Video Editor

Edit multiple raw filmed clips into a polished, viral-ready short video (9:16) with auto-silence-removal, TikTok-style captions, zoom effects, transitions, and music.

## How this differs from HeyGen short video pipeline

This skill is for **real footage you filmed** (phone, screen recording, camera). No AI avatars, no AI-generated visuals. Key differences:

| | HeyGen Pipeline | Raw Clip Editor |
|---|---|---|
| **Source** | AI avatar + AI visuals | Your real filmed clips |
| **Audio** | Separate MP3 voiceover | Audio from the clips themselves |
| **Captions** | Backdrop-blur boxes, 38px | Bold stroke text, 52px, no box |
| **Silence** | N/A (scripted audio) | Auto-detected and removed (jump cuts) |
| **Composition** | `HeyGenShort` | `TikTokCreator` |
| **Feel** | Polished AI presenter | Raw, energetic TikTok creator |

## Prerequisites

- `whisper` CLI — already installed at `/Library/Frameworks/Python.framework/Versions/3.13/bin/whisper`
- `ffmpeg` + `ffprobe` — at `/opt/homebrew/bin/`
- Remotion Studio — `workspace/video-projects/remotion-studio/`

## Workflow

```
User provides ordered raw clips
  ↓
[Step 1] Analyze clips (ffprobe)
  ↓
[Step 2] Detect silence → trim → export segments (auto jump cuts)
  ↓
[Step 3] Transcribe trimmed audio (Whisper local, Vietnamese)
  ↓
[Step 4] Correct transcript against user notes (if provided)
  ↓
[Step 5] Plan effects — captions, zoom, transitions, BGM, SFX
  ↓
[Step 6] Build Remotion props → stage assets → preview
  ↓
[Step 7] User approves → render final MP4
```

## Step 1: Collect Input

Ask user for:
1. **Video files** — paths to raw clips, in playback order
2. **Script/notes** (optional) — to correct Whisper transcription errors
3. **Silence threshold** (optional, default: -30dB, min duration 0.5s)
4. **BGM preference** (optional — auto-select if not specified)

## Step 2: Process Raw Clips

Run the processing script:

```bash
python3 .claude/skills/raw-short-video-editor/scripts/process_raw_clips.py \
  --clips clip1.mp4 clip2.mp4 clip3.mp4 \
  --output-dir workspace/content/YYYY-MM-DD/video-short/SLUG/raw-edit/ \
  --silence-threshold -30 \
  --silence-min-duration 0.5 \
  --language vi
```

The script:
1. Probes each clip (duration, resolution, has_audio)
2. Detects silence gaps using `ffmpeg silencedetect`
3. Builds cut list — keeps non-silent segments
4. Trims clips with ffmpeg (stream copy, re-encode only if needed)
5. Concatenates trimmed audio
6. Runs Whisper with word-level timestamps
7. Outputs structured JSON files

Output structure:
```
output-dir/
├── clip_info.json        # Original clip metadata
├── silence_gaps.json     # Detected silence regions
├── timeline.json         # Trimmed segments with timing
├── trimmed/              # Trimmed video segments
│   ├── seg_000.mp4
│   ├── seg_001.mp4
│   └── ...
├── trimmed_audio.wav     # Combined audio for transcription
├── transcript.srt        # Whisper SRT output
└── segments.json         # Word-level timestamps
```

## Step 3: Correct Transcript

Read `transcript.srt`. Whisper often mangles Vietnamese and English terms. If user provided script/notes:
1. Compare SRT text against original script
2. Replace wrong text with correct text
3. Keep all timestamps unchanged — Whisper timing is accurate, text is not
4. Save corrected SRT back

## Step 4: Plan Effects (TikTok Creator Style)

Analyze the timeline and apply these TikTok creator patterns:

### Caption Style
- **Position**: Center of screen (`captionPosition: 45`)
- **Font**: 52px bold with black text-stroke (no backdrop-blur box)
- **Effect**: Primarily `word-by-word` with bright yellow highlights
- **Hook (first 3-5s)**: `slam` effect, larger text
- **CTA (last segment)**: `typewriter` effect

### Zoom Effects
- `hookBoostSec: 5` — auto zoom boost in first 5 seconds
- Add `punch` zoom pulse at each scene transition
- Add `slow` zoom pulse on key moments (insights, reveals)
- Ken Burns drift is built-in (1.0→1.03)

### Transitions
- Prefer fast, energetic transitions: `whip-pan`, `zoom-blur`, `swipe-left`
- Duration: 8 frames (~0.27s) — faster than default 12
- Every transition gets a zoom pulse

### Sound Effects (max 4-5 total)
Select from `workspace/assets/reels/MEME SOUND/`:
- **Transition**: `Whoosh sound effect` on scene changes
- **Hook**: `Sound Effect - Camera shutter` or `SUDDEN SUSPENSE`
- **Positive moment**: `The Price is Right Ding` or `tada`
- **Dramatic reveal**: `DUN DUN DUNNN`
- **CTA**: `ting`

### Background Music
Auto-select from `workspace/assets/reels/bgm/`:

| Track | Energy | Best for |
|-------|--------|----------|
| `chase-velocity.mp3` | High | Fast demos, exciting reveals |
| `rising-star.mp3` | Medium-high | Success stories, achievements |
| `Fortitude.mp3` | Medium | Tutorials, motivational |
| `miracle.mp3` | Emotional | Storytelling, transformations |
| `aluminum.mp3` | Chill | Casual tips, calm content |

Settings: volume 0.08-0.12, fade in 1s, fade out 2s.

## Step 5: Build Remotion Props

Build props JSON for the `TikTokCreator` composition.

The trimmed clip segments become `clips[]`, captions from SRT become `captions[]`.

```json
{
  "clips": [
    { "videoPath": "media/raw-edit/seg_000.mp4", "durationSeconds": 3.2 },
    { "videoPath": "media/raw-edit/seg_001.mp4", "durationSeconds": 2.8 }
  ],
  "captions": [
    {
      "text": "Bạn có biết rằng AI có thể làm điều này",
      "startSec": 0.0,
      "endSec": 3.2,
      "words": [
        { "word": "Bạn", "start": 0.0, "end": 0.3 },
        { "word": "có", "start": 0.3, "end": 0.5 }
      ],
      "highlights": ["AI"],
      "style": "hook",
      "textEffect": "slam",
      "captionPosition": 45
    }
  ],
  "durationSeconds": 45.0,
  "hookBoostSec": 5,
  "showProgressBar": true,
  "captionFontSize": 52,
  "captionStrokeWidth": 3,
  "captionHighlightColor": "#FFE600",
  "sceneTransition": { "type": "whip-pan", "durationFrames": 8 },
  "zoomPulses": [
    { "timeSec": 3.2, "type": "punch", "scale": 1.12 }
  ],
  "soundEffects": [
    { "audioPath": "media/sfx/whoosh.mp3", "startSec": 3.2, "volume": 0.6 }
  ],
  "backgroundMusic": [
    { "audioPath": "media/bgm/chase-velocity.mp3", "startSec": 0, "volume": 0.10, "fadeInSec": 1, "fadeOutSec": 2 }
  ],
  "footerText": "@tranvanhoang.com",
  "outro": {
    "durationSeconds": 6,
    "title": "Hoang AI",
    "subtitle": "AI Freedom Builders",
    "bgColor": "#000",
    "profileImage": "hoang profile.webp"
  }
}
```

## Step 6: Stage & Preview

1. Copy trimmed clips to `workspace/video-projects/remotion-studio/public/media/raw-edit/`
2. Ensure BGM/SFX files are in `public/media/bgm/` and `public/media/sfx/`
3. Save props to `workspace/video-projects/remotion-studio/props/tiktok-creator.json`
4. Start Remotion Studio:

```bash
cd workspace/video-projects/remotion-studio && npx remotion studio
```

5. Tell user: Preview the `TikTokCreator` composition. Check captions, timing, effects.

## Step 7: Render

After user approves:

```bash
cd workspace/video-projects/remotion-studio && npx remotion render TikTokCreator \
  --props=props/tiktok-creator.json \
  out/raw-clip-final.mp4
```

Output: `workspace/video-projects/remotion-studio/out/raw-clip-final.mp4`

## Quick Reference: Caption Segment Styles

| Style | When | TextEffect | Highlight Color |
|-------|------|------------|-----------------|
| `hook` | First 3-5s | `slam` | `#FF4444` (red) |
| `pain` | Problem/conflict | `flicker` | `#FF6B35` (orange) |
| `normal` | Regular content | `word-by-word` | `#FFE600` (yellow) |
| `solution` | Resolution/insight | `deep-glow` | `#00FF88` (green) |
| `cta` | Last segment | `typewriter` | `#A78BFA` (purple) |
