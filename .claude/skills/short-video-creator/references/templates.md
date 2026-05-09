# Text Overlay Templates

3 templates based on viral Vietnamese short video styles.

## Table of Contents
- [Template 1: Dark Minimal](#template-1-dark-minimal)
- [Template 2: Bold Highlight](#template-2-bold-highlight)
- [Template 3: Epic Fullscreen](#template-3-epic-fullscreen)
- [Template 4: Image Ken Burns](#template-4-image-ken-burns)
- [Shared Patterns](#shared-patterns)

---

## Template 1: Dark Minimal

**Style**: Dark moody b-roll (person working) + white text block centered in lower half. Clean, minimal.
**Best for**: Numbered lists, step-by-step wisdom, productivity tips.
**Reference**: @daily.cao style — "Bạn không cần nỗ lực, thứ bạn cần là..."

### Visual Spec
- B-roll: dark/moody, fill entire frame, `objectFit: "cover"`, dimmed 40% with black overlay
- Text area: bottom 60% of frame, centered horizontally
- Title: white, 42px, bold, line-height 1.4
- List items: white, 36px, regular weight, numbered
- Font: Be Vietnam Pro (Google Fonts) — supports Vietnamese diacritics
- Watermark: top-right corner, 24px, opacity 0.7
- Text appears with fade-in per line (staggered 0.3s each)

### Props Type

```tsx
type DarkMinimalProps = {
  title: string;           // "Bạn không cần nỗ lực, thứ bạn cần là:"
  items: string[];         // ["Một mục tiêu đủ lớn", "Hành động nhỏ lặp lại hàng ngày"]
  watermark: string;       // "@tranvanhoang.com"
  bgVideo: string;         // filename in public/
  bgMusic?: string;        // filename in public/
  durationSeconds?: number; // default 8
};
```

### Component Code

```tsx
import React from "react";
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing, Sequence, staticFile,
} from "remotion";
import { Video, Audio } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/BeVietnamPro";

const { fontFamily } = loadFont("normal", { weights: ["400", "700"], subsets: ["vietnamese"] });

export const DarkMinimal: React.FC<DarkMinimalProps> = ({
  title, items, watermark, bgVideo, bgMusic, durationSeconds = 8,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Fade out music in last 0.5s
  const musicVolume = (f: number) =>
    interpolate(f, [0, fps * 0.3, durationInFrames - fps * 0.5, durationInFrames], [0, 0.3, 0.3, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* B-roll video */}
      <Video src={staticFile(bgVideo)} loop muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />

      {/* Dark overlay */}
      <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,0.4)" }} />

      {/* Background music */}
      {bgMusic && <Audio src={staticFile(bgMusic)} volume={musicVolume} loop />}

      {/* Watermark */}
      <div style={{
        position: "absolute", top: 40, right: 40,
        color: "white", fontSize: 24, fontFamily, opacity: 0.7,
      }}>
        {watermark}
      </div>

      {/* Text content — bottom 60% */}
      <div style={{
        position: "absolute", bottom: "10%", left: "8%", right: "8%",
        display: "flex", flexDirection: "column", gap: 16, fontFamily,
      }}>
        {/* Title with fade in */}
        <Sequence from={0} layout="none">
          <div style={{
            color: "white", fontSize: 42, fontWeight: 700, lineHeight: 1.4,
            opacity: interpolate(frame, [0, fps * 0.3], [0, 1], { extrapolateRight: "clamp" }),
          }}>
            {title}
          </div>
        </Sequence>

        {/* Items — staggered fade in */}
        {items.map((item, i) => {
          const itemStart = fps * (0.5 + i * 0.4);
          const itemOpacity = interpolate(frame, [itemStart, itemStart + fps * 0.3], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          const itemY = interpolate(frame, [itemStart, itemStart + fps * 0.3], [20, 0], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.ease),
          });
          return (
            <div key={i} style={{
              color: "white", fontSize: 36, fontWeight: 400, lineHeight: 1.5,
              opacity: itemOpacity, transform: `translateY(${itemY}px)`,
            }}>
              {i + 1}. {item}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Template 2: Bold Highlight

**Style**: Dark b-roll + text with **bold colored keywords**. Has quote at bottom in accent color.
**Best for**: Tips with key concepts, mindset advice, methods with terminology.
**Reference**: @daily.cao style — "Cách mình vượt qua những giai đoạn khó khăn..."

### Visual Spec
- B-roll: dark/moody, dimmed 35%
- Text area: center-bottom of frame
- Title: white, 40px bold
- Body text: white, 32px, with keywords wrapped in bold + accent color (#FFD700 gold)
- Quote: accent color italic, 28px, at bottom
- Font: Be Vietnam Pro
- Text fade-in block by block (title → body → quote)

### Props Type

```tsx
type BoldHighlightProps = {
  title: string;
  bodyLines: Array<{
    text: string;
    highlights?: string[];  // words to bold+color
  }>;
  quote?: string;            // "Greatest is built from solitude" - Naval
  accentColor?: string;      // default "#FFD700"
  watermark: string;
  bgVideo: string;
  bgMusic?: string;
  durationSeconds?: number;
};
```

### Component Code

```tsx
import React from "react";
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing, staticFile,
} from "remotion";
import { Video, Audio } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/BeVietnamPro";

const { fontFamily } = loadFont("normal", { weights: ["400", "700"], subsets: ["vietnamese"] });

// Render text with highlighted words
const HighlightedText: React.FC<{ text: string; highlights?: string[]; color: string; fontSize: number }> = ({
  text, highlights = [], color, fontSize,
}) => {
  if (highlights.length === 0) return <span style={{ fontSize }}>{text}</span>;

  const regex = new RegExp(`(${highlights.map(h => h.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'gi');
  const parts = text.split(regex);

  return (
    <span style={{ fontSize }}>
      {parts.map((part, i) =>
        highlights.some(h => h.toLowerCase() === part.toLowerCase()) ? (
          <span key={i} style={{ fontWeight: 700, color }}>{part}</span>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </span>
  );
};

export const BoldHighlight: React.FC<BoldHighlightProps> = ({
  title, bodyLines, quote, accentColor = "#FFD700", watermark, bgVideo, bgMusic, durationSeconds = 10,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const musicVolume = (f: number) =>
    interpolate(f, [0, fps * 0.3, durationInFrames - fps * 0.5, durationInFrames], [0, 0.3, 0.3, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  const titleOpacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: "clamp" });
  const bodyOpacity = interpolate(frame, [fps * 0.6, fps * 1.0], [0, 1], { extrapolateRight: "clamp" });
  const quoteOpacity = interpolate(frame, [fps * 2.0, fps * 2.5], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Video src={staticFile(bgVideo)} loop muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,0.35)" }} />

      {bgMusic && <Audio src={staticFile(bgMusic)} volume={musicVolume} loop />}

      <div style={{ position: "absolute", top: 40, right: 40, color: "white", fontSize: 24, fontFamily, opacity: 0.7 }}>
        {watermark}
      </div>

      <div style={{
        position: "absolute", bottom: "8%", left: "6%", right: "6%",
        display: "flex", flexDirection: "column", gap: 20, fontFamily, color: "white",
      }}>
        <div style={{ fontSize: 40, fontWeight: 700, lineHeight: 1.3, opacity: titleOpacity }}>
          {title}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 10, opacity: bodyOpacity, lineHeight: 1.5 }}>
          {bodyLines.map((line, i) => (
            <div key={i}>
              <HighlightedText text={line.text} highlights={line.highlights} color={accentColor} fontSize={32} />
            </div>
          ))}
        </div>

        {quote && (
          <div style={{ fontSize: 28, fontStyle: "italic", color: accentColor, opacity: quoteOpacity, marginTop: 10 }}>
            {quote}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Template 3: Epic Fullscreen

**Style**: Full-screen dramatic b-roll + LARGE bold centered text with color-highlighted keywords. Can include emoji.
**Best for**: Shock statements, bold claims, viral hooks, short punchy messages.
**Reference**: "Ứng Dụng AI Mỗi Ngày" style — large text over epic landscape.

### Visual Spec
- B-roll: dramatic/epic (landscape, mountains, aerial), fill frame, NO dimming (or very light 15%)
- Text: centered both vertically and horizontally
- Font size: 64-80px, extra bold
- Key phrases in accent color (#FFD700)
- Drop shadow on text for readability: `textShadow: "0 4px 20px rgba(0,0,0,0.8)"`
- Text scales up slightly on appear (spring feel)
- Font: Be Vietnam Pro 800 weight

### Props Type

```tsx
type EpicFullscreenProps = {
  lines: Array<{
    text: string;
    isHighlight?: boolean;  // render in accent color
  }>;
  accentColor?: string;
  bgVideo: string;
  bgMusic?: string;
  durationSeconds?: number;
};
```

### Component Code

```tsx
import React from "react";
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing, spring, staticFile,
} from "remotion";
import { Video, Audio } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/BeVietnamPro";

const { fontFamily } = loadFont("normal", { weights: ["400", "800"], subsets: ["vietnamese"] });

export const EpicFullscreen: React.FC<EpicFullscreenProps> = ({
  lines, accentColor = "#FFD700", bgVideo, bgMusic, durationSeconds = 8,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const musicVolume = (f: number) =>
    interpolate(f, [0, fps * 0.3, durationInFrames - fps * 0.5, durationInFrames], [0, 0.35, 0.35, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  // Text group scale-up entrance
  const textScale = spring({ frame, fps, config: { damping: 12, stiffness: 100 }, durationInFrames: fps });
  const textOpacity = interpolate(frame, [0, fps * 0.3], [0, 1], { extrapolateRight: "clamp" });

  // Fade out
  const fadeOut = interpolate(frame, [durationInFrames - fps * 0.5, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Video src={staticFile(bgVideo)} loop muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,0.15)" }} />

      {bgMusic && <Audio src={staticFile(bgMusic)} volume={musicVolume} loop />}

      <AbsoluteFill style={{
        justifyContent: "center", alignItems: "center",
        opacity: textOpacity * fadeOut,
        transform: `scale(${0.8 + textScale * 0.2})`,
      }}>
        <div style={{
          display: "flex", flexDirection: "column", alignItems: "center",
          padding: "0 60px", textAlign: "center", fontFamily,
        }}>
          {lines.map((line, i) => (
            <div key={i} style={{
              fontSize: 68, fontWeight: 800, lineHeight: 1.2,
              color: line.isHighlight ? accentColor : "white",
              textShadow: "0 4px 20px rgba(0,0,0,0.8), 0 2px 8px rgba(0,0,0,0.6)",
            }}>
              {line.text}
            </div>
          ))}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## Template 4: Image Ken Burns

**Style**: Static image with slow zoom + drift. Fade in/out.
**Best for**: Wisdom posts, infographics, quote cards.

### Visual Spec
- Image: `objectFit: "contain"`, centered
- Ken Burns: scale 1.0→1.15, drift (-15px, -10px) over duration
- Fade in 0.5s, fade out 0.5s
- Background: match image edge color (default #f5f0e8 for light images, #1a1a1a for dark)

### Props Type

```tsx
type ImageKenBurnsProps = {
  imagePath: string;       // filename in public/
  bgColor?: string;        // default "#f5f0e8"
  bgMusic?: string;
  durationSeconds?: number; // default 8
};
```

### Component Code

```tsx
import React from "react";
import {
  AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing,
} from "remotion";
import { Audio } from "@remotion/media";

export const ImageKenBurns: React.FC<ImageKenBurnsProps> = ({
  imagePath, bgColor = "#f5f0e8", bgMusic, durationSeconds = 8,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const scale = interpolate(frame, [0, durationInFrames], [1, 1.15], {
    extrapolateRight: "clamp", easing: Easing.inOut(Easing.ease),
  });
  const translateX = interpolate(frame, [0, durationInFrames], [0, -15], {
    extrapolateRight: "clamp", easing: Easing.inOut(Easing.ease),
  });
  const translateY = interpolate(frame, [0, durationInFrames], [0, -10], {
    extrapolateRight: "clamp", easing: Easing.inOut(Easing.ease),
  });
  const fadeIn = interpolate(frame, [0, fps * 0.5], [0, 1], { extrapolateRight: "clamp" });
  const fadeOut = interpolate(frame, [durationInFrames - fps * 0.5, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  const musicVolume = (f: number) =>
    interpolate(f, [0, fps * 0.3, durationInFrames - fps * 0.5, durationInFrames], [0, 0.3, 0.3, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    });

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, justifyContent: "center", alignItems: "center" }}>
      {bgMusic && <Audio src={staticFile(bgMusic)} volume={musicVolume} loop />}
      <div style={{
        width: "100%", height: "100%", overflow: "hidden",
        display: "flex", justifyContent: "center", alignItems: "center",
        opacity: fadeIn * fadeOut,
      }}>
        <Img
          src={staticFile(imagePath)}
          style={{
            width: "100%", height: "100%", objectFit: "contain",
            transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
```

---

## Shared Patterns

### Root.tsx Pattern

```tsx
import React from "react";
import { Composition } from "remotion";
import { DarkMinimal } from "./DarkMinimal";
// import other templates as needed

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ShortVideo"
      component={DarkMinimal}
      durationInFrames={240}  // 8s * 30fps
      fps={30}
      width={1080}
      height={1920}  // 9:16 portrait
      defaultProps={{
        title: "...",
        items: [],
        watermark: "@tranvanhoang.com",
        bgVideo: "bg.mp4",
      }}
    />
  );
};
```

### Aspect Ratios

| Platform | Ratio | Width | Height |
|----------|-------|-------|--------|
| TikTok / Reels / Shorts | 9:16 | 1080 | 1920 |
| Facebook feed | 1:1 | 1080 | 1080 |
| Facebook feed (portrait) | 4:5 | 1080 | 1350 |

### Duration Formula

```
durationInFrames = durationSeconds * fps
```
Example: 8 seconds at 30fps = 240 frames.
