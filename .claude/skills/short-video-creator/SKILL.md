---
name: short-video-creator
description: Create short videos (7-15s) for TikTok, Reels, Facebook using Remotion. Supports 2 modes - (1) Text Overlay on b-roll video backgrounds with auto-matching and 3 templates (Dark Minimal, Bold Highlight, Epic Fullscreen), (2) Image Ken Burns from static images. Auto-selects background music from library by filename. USE WHEN user says 'tạo video short', 'short video', 'tạo video reel', 'video text overlay', 'video từ ảnh', 'render video', 'tạo video facebook', 'tạo video tiktok', 'video ngắn', 'render short', 'tạo video ngắn'.
---

# Short Video Creator

Create short videos for social media using a **single shared Remotion project**.

## Shared Remotion Studio

All videos use one pre-installed project — no per-video project creation needed.

```
workspace/video-projects/remotion-studio/
├── package.json              ← Remotion 4.0.435, already installed
├── public/media/             ← symlink → workspace/assets/reels/
├── props/                    ← per-video JSON props files
├── src/
│   ├── index.ts
│   ├── Root.tsx              ← all 5 Compositions registered
│   ├── types.ts              ← shared prop types
│   └── templates/
│       ├── DarkMinimal.tsx
│       ├── BoldHighlight.tsx
│       ├── EpicFullscreen.tsx
│       ├── ImageKenBurns.tsx
│       └── ProgressiveReduction.tsx
└── out/                      ← render output
```

## Two Video Modes

### Mode 1: Text Overlay on B-roll
- Input: text content (Vietnamese) + b-roll video files in `workspace/assets/reels/videos/`
- Auto-match b-roll clips to text mood/topic by analyzing filenames
- 4 templates: DarkMinimal, BoldHighlight, EpicFullscreen, ProgressiveReduction

### Mode 2: Image Ken Burns
- Input: static image (PNG/JPG)
- Slow zoom (1.0→1.15) + drift animation
- Fade in/out 0.5s, background color matched to image

## Composition IDs & Templates

| CompositionId | Best For | Aspect |
|---------------|----------|--------|
| `DarkMinimal` | Numbered lists, step-by-step wisdom | 1080x1920 |
| `BoldHighlight` | Tips with bold keywords, mindset | 1080x1920 |
| `EpicFullscreen` | Shock statements, bold claims, viral hooks | 1080x1920 |
| `ProgressiveReduction` | Multi-section progressive text, quotes | 1080x1920 |
| `ImageKenBurns` | Wisdom posts, infographics, quote cards | 1080x1080 |

## Media Library

```
workspace/assets/reels/
├── music/    ← background music (name descriptively: motivational-piano.mp3, dark-cinematic.mp3)
└── videos/   ← b-roll clips (name descriptively: working-laptop.mp4, city-night.mp4)
```

Media is accessible in templates via `staticFile()` as `media/videos/filename.mp4` and `media/music/filename.mp3`.

### Music Auto-Selection

Scan `workspace/assets/reels/music/` filenames, match mood to text:
- Motivational → motivational, uplifting, inspiring, piano, epic
- Dark/serious → dark, cinematic, dramatic, intense
- Calm/wisdom → calm, peaceful, ambient, lo-fi, chill
- Tech/AI → tech, electronic, digital, futuristic

No match → first available mp3. No mp3 → render without music.

### B-roll Auto-Selection

Scan `workspace/assets/reels/videos/` filenames, match to text:
- Work/productivity → work, laptop, office, desk, typing, coding
- Nature/philosophy → nature, mountain, ocean, sky, sunset
- City/modern → city, street, night, urban, traffic

Multiple matches → use as sequence clips. No match → first available mp4.

## Workflow

1. Parse text — extract lines, identify mood/topic
2. Select template (user-specified or auto-detect from content type)
3. Scan media folders for matching b-roll + music
4. Create props JSON file in `workspace/video-projects/remotion-studio/props/{slug}.json`
5. Render: `cd workspace/video-projects/remotion-studio && npx remotion render src/index.ts {CompositionId} out/{slug}.mp4 --props=props/{slug}.json`
6. Copy output to `workspace/content/{YYYY-MM-DD}/video/{slug}-{template}.mp4`

## Props JSON Format

Each template accepts a JSON props file. Reference media as `media/videos/filename.mp4` and `media/music/filename.mp3`.

### DarkMinimal

```json
{
  "title": "Bạn không cần nỗ lực, thứ bạn cần là:",
  "items": ["Một mục tiêu đủ lớn", "Hành động nhỏ lặp lại hàng ngày"],
  "watermark": "@tranvanhoang.com",
  "bgVideo": "media/videos/Hoang ngoi lam viec laptop ban dem.mp4",
  "bgMusic": "media/music/nhac truyen cam hung.mp3",
  "durationSeconds": 8
}
```

### BoldHighlight

```json
{
  "title": "Cách mình vượt qua giai đoạn khó khăn",
  "bodyLines": [
    { "text": "Tập trung vào hệ thống, không phải mục tiêu", "highlights": ["hệ thống"] },
    { "text": "Mỗi ngày làm 1 việc nhỏ, kiên trì", "highlights": ["kiên trì"] }
  ],
  "quote": "\"Greatness is built in silence\" - Naval",
  "accentColor": "#FFD700",
  "watermark": "@tranvanhoang.com",
  "bgVideo": "media/videos/Hoang ngoi lam viec voi may tinh.mp4",
  "bgMusic": "media/music/nhac truyen cam hung.mp3",
  "durationSeconds": 10
}
```

### EpicFullscreen

```json
{
  "lines": [
    { "text": "AI sẽ thay thế" },
    { "text": "90% công việc", "isHighlight": true },
    { "text": "trong 5 năm tới" }
  ],
  "accentColor": "#FFD700",
  "bgVideo": "media/videos/Hoang giang day dao tao ai.mp4",
  "bgMusic": "media/music/nhac truyen cam hung.mp3",
  "durationSeconds": 8
}
```

### ProgressiveReduction

```json
{
  "durationSeconds": 18,
  "watermark": "@tranvanhoang.com",
  "bgVideo": "media/videos/Hoang ngoi lam viec laptop ban dem.mp4",
  "bgMusic": "media/music/nhac truyen cam hung.mp3",
  "sections": [
    {
      "lines": ["Hãy đặt mục tiêu", "— ngay bây giờ."],
      "startSec": 0.3,
      "durationSec": 3.5,
      "fontSize": 56,
      "fontWeight": 700,
      "color": "#FFFFFF",
      "lineHeight": 1.3
    }
  ]
}
```

### ImageKenBurns

```json
{
  "imagePath": "media/images/quote-card.png",
  "bgColor": "#f5f0e8",
  "bgMusic": "media/music/nhac truyen cam hung.mp3",
  "durationSeconds": 8
}
```

## Render Command

```bash
cd workspace/video-projects/remotion-studio
npx remotion render src/index.ts {CompositionId} out/{slug}.mp4 --props=props/{slug}.json
```

## Output

`workspace/content/{YYYY-MM-DD}/video/{slug}-{template}.mp4`

## Critical Remotion Rules

- ALL animations via `useCurrentFrame()` + `interpolate()` — NO CSS animations/transitions
- `<Video>` and `<Audio>` from `@remotion/media`
- `<Img>` from `remotion` — never native `<img>`
- `staticFile()` for files in `public/`
- Loop b-roll: `<Video src={...} loop muted />`
- Music: `<Audio src={...} volume={0.3} loop />` with fade-out last 0.5s
- FPS: 30
- Use `calculateMetadata` for dynamic duration from `durationSeconds` prop

## Adding New Templates

1. Create `src/templates/NewTemplate.tsx`
2. Add prop type to `src/types.ts`
3. Register `<Composition>` in `src/Root.tsx` with `calculateMetadata`
4. Document props JSON format in this file

## Template Reference

See [references/templates.md](references/templates.md) for full template component code.
