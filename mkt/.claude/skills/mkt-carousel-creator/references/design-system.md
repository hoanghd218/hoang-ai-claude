# Design System — Carousel

Reuse design system từ `image-post-creator` skill để brand consistency.

## Color Palette

| Element | Hex | Usage |
|---------|-----|-------|
| Background | `#F5F0E8` | Primary slide background — cream/off-white |
| Text | `#1A1A1A` | Headline và body text — near-black |
| Highlight | `#FFE066` | Yellow marker highlight — cho keywords, titles |
| Underline | `#C0392B` | Red double underline — cho CTA, key phrases |
| Accent | `#6B9E7A` | Sage green — cho icons, borders, infographic elements |
| Footer | `#666666` | Gray — cho watermark @tranvanhoang.com |
| Alt Background | `#1A1A1A` | Dark slides (cover hoặc accent slides) |
| Alt Text | `#F5F0E8` | Light text trên dark background |

## Typography

| Element | Style | Size (IG 1:1) | Size (TikTok 9:16) |
|---------|-------|---------------|---------------------|
| Headline | Bold sans-serif (Montserrat/Inter) | 48-64px | 64-80px |
| Body | Regular/Medium sans-serif | 28-36px | 36-48px |
| Number/Label | Bold, slightly larger | 56-72px | 72-96px |
| Footer | Regular, centered | 16-20px | 20-24px |

## Visual Emphasis Techniques

### 1. Yellow Highlight Marker
- Dùng cho: Titles, keywords chính, terms quan trọng
- Effect: Highlight marker tay — không perfect rectangle
- Khi nào: Cover slide title, key terms trong body

### 2. Red Double Underline
- Dùng cho: CTA text, conclusions, warnings
- Effect: Double underline đỏ dưới text
- Khi nào: CTA slide, final takeaway

### 3. Number Emphasis
- Dùng cho: Step numbers, list numbers
- Effect: Số lớn bold, khác màu hoặc highlight
- Khi nào: Listicle và step-by-step slides

### 4. Strikethrough
- Dùng cho: Myths, sai lầm, "before" items
- Effect: Gạch ngang qua text
- Khi nào: Myth-busting slides, before/after

## Layout Templates

### IG 1:1 (1080x1080)
```
┌─────────────────────────┐
│     [80px padding]      │
│                         │
│   HEADLINE              │
│   (yellow highlight)    │
│                         │
│   Body text here        │
│   Line 2 if needed      │
│                         │
│                         │
│                         │
│   @tranvanhoang.com     │
│     [80px padding]      │
└─────────────────────────┘
```

### TikTok 9:16 (1080x1920)
```
┌─────────────────────────┐
│     [120px top safe]    │
│                         │
│                         │
│   HEADLINE              │
│   (yellow highlight)    │
│                         │
│                         │
│   Body text here        │
│   Line 2 if needed      │
│                         │
│                         │
│                         │
│   @tranvanhoang.com     │
│                         │
│     [200px bottom safe] │
│     (TikTok UI zone)    │
└─────────────────────────┘
```

## Slide Consistency Rules

1. **Same palette** across all slides — không random đổi màu
2. **Same font** across all slides — chỉ thay size/weight
3. **Footer** trên mọi slide — @tranvanhoang.com
4. **Cover slide** có thể dùng dark background (#1A1A1A) để nổi bật
5. **CTA slide** dùng yellow highlight + red underline combo
6. **NO photos, NO complex illustrations** — typography-based design
7. **NO emoji trong slides** — chỉ text + simple icons nếu cần
