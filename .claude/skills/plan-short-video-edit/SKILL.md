---
name: plan-short-video-edit
description: "Plan short video production from MP3 voiceover + script + PRE-EXTRACTED SRT. Analyzes content to classify segments (heygen/grok/custom/prompt-typing), plans effects, captions, BGM, Grok video prompts, and outputs a complete production plan folder. SRT transcription is handled upstream by mkt-ai-video-extract-srt-segment. This is the planning phase — downstream skills (heygen-short-video, heygen-remotion-short-video-editor) consume this output. USE WHEN user says 'plan video edit', 'lên kế hoạch video', 'plan short video', 'phân tích script video', 'tạo plan video từ mp3', 'plan video ngắn', 'chuẩn bị video edit'."
---

# Plan Short Video Edit

Analyze MP3 voiceover + script to produce a complete production plan folder that downstream skills consume.

```
MP3 + Script + SRT (pre-extracted) → Ask custom b-roll? → Classify segments
  → Plan effects, captions, BGM, Grok prompts → Output plan folder
```

## Input

1. **MP3 file path** (required) — voiceover audio
2. **Script text or file** (required) — full script content for context
3. **SRT file** (required) — pre-extracted upstream by `mkt-ai-video-extract-srt-segment`
4. **Segments JSON** (required) — word-level timestamps, pre-extracted upstream
5. **Custom b-roll manifest** (optional — see references in heygen-short-video skill)

## Step 1: Verify SRT + Segments Exist

**SRT transcription and script-based correction are handled upstream** (by `mkt-ai-video-extract-srt-segment` skill). This skill does NOT transcribe audio.

Verify the following files exist:
- `<mp3_parent>/voiceover.srt` — or a provided SRT path
- `<mp3_parent>/voiceover_segments.json` — word-level timestamps

If either is missing, STOP and tell the user to run `mkt-ai-video-extract-srt-segment` first.

After verification, ask about custom b-roll:
> Bạn có ảnh hoặc video nào muốn dùng làm cảnh trám không?
> (Ví dụ: screenshot bài báo, giao diện GitHub, demo app...)
> Nếu có, tạo 1 file text: `/path/to/file.png | Mô tả nội dung`

## Step 2: Analyze SRT & Classify Segments

Read SRT transcript and classify each segment:

| Type | When to use | Source |
|------|-------------|--------|
| `heygen` | Direct speaking, opinions, CTA, hooks, explanations | HeyGen avatar clip |
| `grok` | Concepts, demos, scenarios, metaphors, processes | Grok AI video (6s) |
| `custom` | User-provided b-roll matching content | User image/video |
| `prompt-typing` | Speaker reads a prompt, command, text input | Remotion PromptTyping |

### Duration Constraints

- **HeyGen ≤ 50%** of total duration. If exceeded, convert middle heygen segments to grok.
- **≤ 30s total**: Max 2 heygen segments (≤ 15s heygen time)
- **31-40s total**: Max 3 heygen segments (≤ 20s heygen time)
- Prioritize keeping heygen for **hook** (first) and **CTA** (last)
- Show budget: `HeyGen: X.Xs / Y.Ys budget (Z%)`

## Step 3: Plan Production Elements

For each segment, determine in one pass:

1. **style** — `hook`, `pain`, `normal`, `solution`, `cta`
2. **highlights** — key words to highlight (max 2-3)
3. **visual overlay** — emoji/GIF/logo, avatar segments only. Reference: `heygen-short-video/references/visual-overlays.md`
4. **textEffect** — mix across segments: `word-by-word`, `typewriter`, `slam`, `wave`, `deep-glow`, `flicker`, `none`. Reference: `heygen-short-video/references/text-effects.md`
5. **soundEffect** — max 3-5 total. Reference: `heygen-short-video/references/meme-sounds.md`, `heygen-short-video/references/sound-design-patterns.md`
   **VALIDATION BẮT BUỘC**: Sau khi chọn sound effect, PHẢI chạy lệnh kiểm tra file tồn tại:
   ```bash
   for sfx in "file1.mp3" "file2.mp3"; do
     [ -f "workspace/video-projects/remotion-studio/public/reels/audio/sfx/$sfx" ] && echo "OK: $sfx" || echo "MISSING: $sfx"
   done
   ```
   Nếu file MISSING, chọn sound effect khác từ danh sách có sẵn. KHÔNG được dùng tên file không tồn tại.
6. **Hook optimization (first 10s)** — `hookBoostSec: 10`, aggressive `zoomPulses`, camera-flash SFX at 0.0s
7. **Background Music** — Reference: `heygen-short-video/references/bgm-selection.md`
   **VALIDATION BẮT BUỘC**: Sau khi chọn BGM, PHẢI kiểm tra file tồn tại:
   ```bash
   ls workspace/video-projects/remotion-studio/public/reels/audio/bgm/
   ```
   Chỉ dùng tên file có trong thư mục này.
8. **Grok Video Prompts** — For each `grok` segment. Reference: `heygen-short-video/references/grok-prompts.md`

## Step 4: Output Plan Folder

Save everything to:
```
workspace/content/{YYYY-MM-DD}/video-short/{slug}/plan/
├── script.txt              # Original script
├── voiceover.srt           # Transcribed SRT
├── voiceover_segments.json  # Word-level timestamps (from upstream extract skill)
├── production-plan.json    # Complete plan (see schema below)
└── grok-prompts.md         # Grok prompts for user to generate videos
```

### production-plan.json schema

```json
{
  "totalDuration": 64.5,
  "avatarBudget": { "used": 30.2, "max": 32.25, "percent": 46.8 },
  "bgm": [
    { "track": "Fortitude", "startSec": 0, "endSec": 10, "volume": 0.15 }
  ],
  "segments": [
    {
      "index": 1,
      "startSec": 0.0,
      "endSec": 3.5,
      "type": "heygen",
      "srtText": "Bạn có biết rằng...",
      "style": "hook",
      "highlights": ["biết"],
      "textEffect": "word-by-word",
      "visualOverlay": { "type": "emoji", "value": "mind-blown" },
      "soundEffect": { "name": "camera-flash", "atSec": 0.0 },
      "grokPrompt": null,
      "avatarNote": "Energetic, front view",
      "words": [{"word": "Bạn", "start": 0.0, "end": 0.3}]
    },
    {
      "index": 2,
      "startSec": 3.5,
      "endSec": 9.0,
      "type": "grok",
      "srtText": "AI tự động chạy lúc bạn ngủ",
      "style": "normal",
      "highlights": ["AI"],
      "textEffect": "none",
      "visualOverlay": null,
      "soundEffect": null,
      "grokPrompt": "Cinematic wide shot of a glowing neural network...",
      "avatarNote": null,
      "words": []
    }
  ]
}
```

## Step 5: Present Plan & Next Steps

Show the production plan table:
```
| # | Time | Type | SRT summary | Style | TextEffect | SFX |
```

Then instruct user:
> Đây là production plan. Grok visual videos sẽ được **tạo tự động** qua 79ai API trong bước production.
>
> Bước tiếp theo: dùng skill `heygen-short-video` để tạo avatar clips.
> Grok visuals sẽ auto-generate bởi `generate_grok_visuals.py` khi chạy `heygen-remotion-short-video-editor`.
> Cuối cùng dùng skill `heygen-remotion-short-video-editor` để ghép video.
