# Remotion Video Production cho Storytelling Video

Hướng dẫn dùng Remotion để biến script storytelling thành video hoàn chỉnh.

---

## Khi nào dùng Remotion?

| Trường hợp | Dùng Remotion |
|------------|--------------|
| Video có text overlay, title card, animations | ✅ |
| Video chỉ ghép clip đơn giản | ❌ (dùng FFmpeg) |
| Video cần captions TikTok-style | ✅ |
| Video cần transitions đẹp giữa sections | ✅ |
| Video cần branded elements (logo, màu, font) | ✅ |

---

## Project Setup

### Khởi tạo project mới (nếu chưa có)

```bash
mkdir -p workspace/content/[video-slug]/remotion/src/compositions
mkdir -p workspace/content/[video-slug]/remotion/public
cd workspace/content/[video-slug]/remotion
```

### package.json

```json
{
  "name": "storytelling-video",
  "version": "1.0.0",
  "scripts": {
    "dev": "remotion studio",
    "render": "remotion render"
  },
  "dependencies": {
    "@remotion/bundler": "^4.0.242",
    "@remotion/captions": "^4.0.242",
    "@remotion/cli": "^4.0.242",
    "@remotion/transitions": "^4.0.242",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "remotion": "^4.0.242"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "typescript": "^5.0.0"
  }
}
```

**QUAN TRỌNG:**
- React PHẢI là `^18.x` (Remotion 4.x KHÔNG hỗ trợ React 19)
- `@remotion/media` KHÔNG tồn tại — dùng `OffthreadVideo` từ core `remotion`

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

### remotion.config.ts

```ts
import {Config} from '@remotion/cli/config';
Config.setVideoImageFormat('jpeg');
```

### src/index.ts

```tsx
import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';

registerRoot(RemotionRoot);
```

---

## Cấu trúc Video Storytelling

Video YouTube storytelling gồm các section tương ứng script:

```
┌─────────────┐
│   HOOK      │  5 giây đầu — text overlay + visual hook
├─────────────┤
│   INTRO     │  20-30 giây — establish credibility, curiosity gap
├─────────────┤
│   BODY      │  Thân bài — các main points với conflict loops
│   Point 1   │  Setup → Teaching → Proof
│   Point 2   │  Setup → Teaching → Proof
│   Point 3   │  Setup → Teaching → Proof
├─────────────┤
│  LAST DAB   │  Câu kết — memorable, quotable
├─────────────┤
│    CTA      │  Link → Curiosity → Promise
└─────────────┘
```

---

## Root.tsx Template

```tsx
import {Composition, Folder} from 'remotion';
import {StorytellingVideo} from './compositions/StorytellingVideo';

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;

// Tính duration dựa trên script (ước tính 150 từ/phút khi nói)
// Ví dụ: script 1500 từ ≈ 10 phút ≈ 18000 frames
const DURATION_FRAMES = 18000;

export const RemotionRoot: React.FC = () => {
  return (
    <Folder name="Storytelling">
      <Composition
        id="StorytellingVideo"
        component={StorytellingVideo}
        durationInFrames={DURATION_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </Folder>
  );
};
```

---

## Component Patterns cho Storytelling

### 1. Title Card (Hook & Section Headers)

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';

interface TitleCardProps {
  title: string;
  subtitle?: string;
  bgColor?: string;
}

export const TitleCard: React.FC<TitleCardProps> = ({
  title,
  subtitle,
  bgColor = '#1a1a2e',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const titleScale = spring({frame, fps, config: {damping: 200}});
  const subtitleOpacity = interpolate(frame, [15, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bgColor,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          transform: `scale(${titleScale})`,
          fontSize: 72,
          fontWeight: 900,
          color: '#FFFFFF',
          fontFamily: 'Roboto, Arial, sans-serif',
          textAlign: 'center',
          maxWidth: '80%',
          textShadow: '0 4px 20px rgba(0,0,0,0.5)',
        }}
      >
        {title}
      </div>
      {subtitle && (
        <div
          style={{
            opacity: subtitleOpacity,
            fontSize: 36,
            color: '#FFD700',
            fontFamily: 'Roboto, Arial, sans-serif',
            marginTop: 20,
          }}
        >
          {subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};
```

### 2. Text Overlay (Key Points, Conflict Markers)

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';

interface TextOverlayProps {
  text: string;
  position?: 'top' | 'center' | 'bottom';
  highlightWord?: string;
  bgOpacity?: number;
}

export const TextOverlay: React.FC<TextOverlayProps> = ({
  text,
  position = 'bottom',
  highlightWord,
  bgOpacity = 0.7,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const fadeIn = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 10, durationInFrames],
    [1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const opacity = Math.min(fadeIn, fadeOut);

  const positionStyle = {
    top: {justifyContent: 'flex-start', paddingTop: 120} as const,
    center: {justifyContent: 'center'} as const,
    bottom: {justifyContent: 'flex-end', paddingBottom: 120} as const,
  };

  const words = text.split(' ');

  return (
    <AbsoluteFill
      style={{
        ...positionStyle[position],
        alignItems: 'center',
        opacity,
      }}
    >
      <div
        style={{
          backgroundColor: `rgba(0, 0, 0, ${bgOpacity})`,
          padding: '20px 40px',
          borderRadius: 12,
          maxWidth: '80%',
        }}
      >
        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            fontFamily: 'Roboto, Arial, sans-serif',
            textAlign: 'center',
            lineHeight: 1.4,
          }}
        >
          {words.map((word, i) => (
            <span
              key={i}
              style={{
                color:
                  highlightWord && word.includes(highlightWord)
                    ? '#FFD700'
                    : '#FFFFFF',
              }}
            >
              {word}{' '}
            </span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### 3. Section Transition

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';

interface SectionTransitionProps {
  sectionNumber: number;
  sectionTitle: string;
}

export const SectionTransition: React.FC<SectionTransitionProps> = ({
  sectionNumber,
  sectionTitle,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const slideIn = interpolate(frame, [0, 15], [-100, 0], {
    extrapolateRight: 'clamp',
  });
  const numberScale = interpolate(frame, [5, 20], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0f0f23',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div style={{textAlign: 'center'}}>
        <div
          style={{
            fontSize: 120,
            fontWeight: 900,
            color: '#FFD700',
            transform: `scale(${numberScale})`,
            fontFamily: 'Roboto, Arial, sans-serif',
          }}
        >
          {sectionNumber}
        </div>
        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: '#FFFFFF',
            transform: `translateY(${slideIn}px)`,
            fontFamily: 'Roboto, Arial, sans-serif',
            marginTop: 10,
          }}
        >
          {sectionTitle}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### 4. Conflict Loop Marker (BUT / THEREFORE)

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring} from 'remotion';

interface ConflictMarkerProps {
  type: 'BUT' | 'THEREFORE';
}

export const ConflictMarker: React.FC<ConflictMarkerProps> = ({type}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const scale = spring({frame, fps, config: {damping: 12, stiffness: 200}});

  const colors = {
    BUT: {bg: '#FF4444', text: 'NHƯNG'},
    THEREFORE: {bg: '#44BB44', text: 'VÌ THẾ'},
  };

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          transform: `scale(${scale})`,
          backgroundColor: colors[type].bg,
          padding: '15px 40px',
          borderRadius: 8,
          fontSize: 36,
          fontWeight: 900,
          color: '#FFFFFF',
          fontFamily: 'Roboto, Arial, sans-serif',
          textTransform: 'uppercase',
          letterSpacing: '0.1em',
        }}
      >
        {colors[type].text}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Composition Assembly

### StorytellingVideo.tsx (Main Composition)

```tsx
import {AbsoluteFill, Sequence, Series, OffthreadVideo, Audio, staticFile} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {TitleCard} from '../components/TitleCard';
import {TextOverlay} from '../components/TextOverlay';
import {SectionTransition} from '../components/SectionTransition';

const FPS = 30;

// Tính frames từ giây
const sec = (s: number) => Math.round(s * FPS);

export const StorytellingVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>

      {/* === HOOK (0-5s) === */}
      <Sequence from={0} durationInFrames={sec(5)}>
        <TitleCard
          title="[HOOK TEXT TỪ SCRIPT]"
          subtitle="[Subtitle nếu có]"
        />
      </Sequence>

      {/* === INTRO (5-35s) === */}
      <Sequence from={sec(5)} durationInFrames={sec(30)}>
        <AbsoluteFill>
          {/* Background video hoặc B-roll */}
          <OffthreadVideo src={staticFile('intro-bg.mp4')} />
          {/* Text overlay cho credibility */}
          <Sequence from={sec(3)} durationInFrames={sec(5)}>
            <TextOverlay
              text="[Credibility statement]"
              position="bottom"
            />
          </Sequence>
        </AbsoluteFill>
      </Sequence>

      {/* === BODY SECTIONS === */}
      {/* Point 1 */}
      <Sequence from={sec(35)} durationInFrames={sec(2)}>
        <SectionTransition sectionNumber={1} sectionTitle="[Tên point 1]" />
      </Sequence>
      <Sequence from={sec(37)} durationInFrames={sec(60)}>
        <AbsoluteFill>
          <OffthreadVideo src={staticFile('section1.mp4')} />
          {/* Key point overlays */}
          <Sequence from={sec(10)} durationInFrames={sec(5)}>
            <TextOverlay text="[Key point]" highlightWord="[từ quan trọng]" />
          </Sequence>
        </AbsoluteFill>
      </Sequence>

      {/* Thêm các points khác tương tự... */}

      {/* === LAST DAB === */}
      <Sequence from={sec(500)} durationInFrames={sec(10)}>
        <TitleCard
          title="[LAST DAB TEXT]"
          bgColor="#1a1a2e"
        />
      </Sequence>

      {/* === CTA === */}
      <Sequence from={sec(510)} durationInFrames={sec(15)}>
        <AbsoluteFill>
          <OffthreadVideo src={staticFile('cta-bg.mp4')} />
          <TextOverlay
            text="[CTA: Link → Curiosity → Promise]"
            position="center"
          />
        </AbsoluteFill>
      </Sequence>

      {/* === BACKGROUND MUSIC === */}
      <Audio
        src={staticFile('bgm.mp3')}
        volume={0.15}
      />
    </AbsoluteFill>
  );
};
```

---

## Assets cần chuẩn bị

Đặt trong thư mục `public/`:

| File | Mục đích | Yêu cầu |
|------|---------|---------|
| `intro-bg.mp4` | Background video cho intro | 1920x1080, codec H.264 |
| `section1.mp4` | Video/B-roll cho mỗi section | 1920x1080 |
| `cta-bg.mp4` | Background cho CTA | 1920x1080 |
| `bgm.mp3` | Background music | Nhạc không bản quyền |
| `logo.png` | Logo (nếu cần) | PNG transparent |

**Lưu ý:**
- Tên file KHÔNG có khoảng trắng
- Copy file vào `public/` trước khi chạy preview
- Dùng `ffprobe` kiểm tra duration/codec trước khi dùng

---

## Workflow Preview & Render

### 1. Preview (BẮT BUỘC trước khi render)

```bash
cd workspace/content/[video-slug]/remotion
npm install
npm run dev
```

Mở Remotion Studio → kiểm tra từng section → verify timing.

### 2. Render (CHỈ khi user đồng ý)

```bash
npx remotion render StorytellingVideo out/video.mp4 --codec h264 --crf 18
```

### Quality options

```bash
# Preview nhanh (thấp chất lượng)
npx remotion render StorytellingVideo out/preview.mp4 --crf 28 --frames 0-300

# Production (chất lượng cao)
npx remotion render StorytellingVideo out/final.mp4 --codec h264 --crf 18 --audio-codec aac
```

---

## Kết hợp với Captions

Nếu video có voiceover/talking head, thêm captions theo pattern từ video skill:

1. **Transcribe** audio bằng whisper.cpp
2. **Load** captions JSON vào composition
3. **Render** với TikTok-style word highlighting

Tham khảo chi tiết: `.claude/skills/video/references/captions.md`

---

## Gotchas

1. **KHÔNG dùng CSS transitions/animations** — chỉ dùng `useCurrentFrame()` + `interpolate()`
2. **KHÔNG dùng React 19** — Remotion 4.x chỉ hỗ trợ React 18
3. **KHÔNG dùng `@remotion/media`** — package này không tồn tại
4. **LUÔN preview trước render** — không tự động render
5. **Folder name không có space** — dùng hyphen thay thế
6. **Dùng `staticFile()`** cho mọi asset trong `public/`
7. **Duration transitions** — khi dùng TransitionSeries, tổng duration giảm đi bằng tổng các transitions
