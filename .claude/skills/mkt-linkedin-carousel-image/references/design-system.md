# Design System — LinkedIn Carousel

Professional tech visual style optimized for LinkedIn's audience: executives, founders, tech professionals.

## Color Palette

| Element | Hex | Usage |
|---------|-----|-------|
| Background Dark | `#0F172A` | Primary slide background — deep navy |
| Background Light | `#F8FAFC` | Alternate slides — near-white |
| Text Light | `#F1F5F9` | Body text on dark background |
| Text Dark | `#0F172A` | Body text on light background |
| Accent Blue | `#3B82F6` | Keywords, highlights, data points |
| Accent Cyan | `#06B6D4` | Secondary accent — charts, icons |
| Accent Purple | `#8B5CF6` | Tertiary — gradient partner with blue |
| Success Green | `#10B981` | Positive metrics, checkmarks |
| Warning Amber | `#F59E0B` | Caution, attention markers |
| Muted | `#64748B` | Secondary text, labels, watermark |
| Border | `#1E293B` | Subtle dividers on dark bg |
| Border Light | `#E2E8F0` | Subtle dividers on light bg |

## Typography

| Element | Style | Size |
|---------|-------|------|
| Headline | Bold sans-serif (Inter/Geist) | 56-72px |
| Subheadline | Semibold | 36-44px |
| Body | Regular/Medium | 28-36px |
| Data/Number | Bold Mono (JetBrains Mono/Fira Code) | 48-64px |
| Label | Medium uppercase, letter-spacing 2px | 18-22px |
| Footer | Regular, small subtle | (do NOT put pixel sizes in prompts — AI renders them as text) |

## Slide Dimensions

- **Format:** 1080x1080px (1:1 square) — LinkedIn carousel PDF standard
- **Padding:** 80px all sides
- **Safe zone:** Keep text within 920x920px center

## Visual Style Rules

### 1. Gradient Accents
- Primary gradient: `#3B82F6` → `#8B5CF6` (blue to purple)
- Use for: Accent bars, number backgrounds, highlight strips
- Direction: left-to-right or top-to-bottom

### 2. Data Emphasis
- Numbers in monospace bold font, 2x body size
- Metric labels in uppercase small text above numbers
- Use accent blue for positive metrics, amber for comparison

### 3. Comparison Layout
- Split slide 50/50 with subtle vertical divider
- Left side: before/competitor (muted colors)
- Right side: after/our solution (accent colors)

### 4. Icon Style
- Minimal line icons only — no filled, no 3D
- Stroke width: 2-3px
- Color: accent blue or cyan on dark bg, dark on light bg
- NO emoji, NO photos, NO complex illustrations

### 5. Code/Tech Feel
- Monospace font for technical terms, metrics, tool names
- Subtle grid or dot pattern overlay (opacity 3-5%)
- Terminal-style brackets or angle brackets for emphasis: `< >`, `[ ]`

## Layout Templates

### Cover Slide (Dark)
```
┌─────────────────────────┐
│  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  │
│  [gradient accent bar]   │
│                          │
│  SMALL LABEL TEXT        │
│                          │
│  BIG BOLD                │
│  HEADLINE                │
│  (2-3 lines max)         │
│                          │
│                          │
│  @tranvanhoang.com       │
│  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁  │
└─────────────────────────┘
```

### Content Slide (Dark)
```
┌─────────────────────────┐
│                          │
│  #01                     │
│  [accent blue number]    │
│                          │
│  HEADLINE                │
│  (bold, 1-2 lines)       │
│                          │
│  Body text line 1        │
│  Body text line 2        │
│  **Key phrase** accent   │
│                          │
│  @tranvanhoang.com       │
└─────────────────────────┘
```

### Data Slide (Dark)
```
┌─────────────────────────┐
│                          │
│  METRIC LABEL            │
│  ┌─────────┐             │
│  │  84%    │ [big mono]  │
│  └─────────┘             │
│                          │
│  vs 54.2%  [muted]       │
│                          │
│  Context explanation      │
│  in regular body text     │
│                          │
│  @tranvanhoang.com       │
└─────────────────────────┘
```

### CTA Slide (Dark + Gradient)
```
┌─────────────────────────┐
│                          │
│  [gradient bg overlay]   │
│                          │
│  HEADLINE                │
│  (invitation text)       │
│                          │
│  Community Name          │
│  [bold, accent blue]     │
│                          │
│  URL / Link              │
│  [underlined, cyan]      │
│                          │
│  Tagline in italic       │
│  @tranvanhoang.com       │
└─────────────────────────┘
```

## Slide Consistency Rules

1. **Alternating dark/light** — cover + odd slides dark, even slides can be light for visual rhythm
2. **Same font family** across all slides — only vary size/weight
3. **Footer** `@tranvanhoang.com` on every slide — muted color, bottom center
4. **Slide number** visible on content slides — accent blue, top-left corner
5. **Gradient accent bar** on cover and CTA slides only
6. **NO photos, NO complex illustrations** — typography + data visualization only
7. **NO emoji** — use line icons sparingly if needed
8. **Vietnamese text** with full diacritics, technical terms in English
