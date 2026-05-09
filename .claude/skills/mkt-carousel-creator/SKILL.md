---
name: mkt-carousel-creator
description: Create carousel slides for Instagram and TikTok from transcript, insight, or topic. Dual-mode (IG 1:1 / TikTok 9:16). Instagram content in ENGLISH, TikTok in Vietnamese. Output text + visual direction per slide, ready for image rendering. USE WHEN user says 'tạo carousel', 'carousel instagram', 'carousel tiktok', 'tạo slides ig', 'carousel post', 'slide ig', 'slide tiktok', 'ig carousel', 'tiktok carousel'.
---

# Carousel Creator — Instagram & TikTok

Create carousel slide content for Instagram and TikTok. Output: text + visual direction per slide, ready for image rendering.

## Content Language Rule

**Instagram content MUST be written in English** (global audience). **TikTok content uses Vietnamese** (local audience). Only Facebook and YouTube use Vietnamese. LinkedIn, X.com, and Instagram all use English.

## Brand Voice Reference

- [BRANDVOICE.MD](../../../MY RESOURCES/BRANDVOICE.MD) - DNA Brand Voice Hoàng

**Brand voice for Carousel:**
- Slide text: Short, bold, scannable — one idea per slide (knowledge statement style, no direct addressing)
- Caption (IG): English, "I"/"Hoang" voice
- Caption (TikTok): Vietnamese, "mình"/"Hoàng" voice
- Energy: 7.5/10 — bold, visual-driven, attention-grabbing
- Power words: System, Automation, AI, Framework, Workflow, Template

## Platform Modes

| Setting | Instagram Mode | TikTok Mode |
|---------|---------------|-------------|
| **Aspect ratio** | 1:1 (1080x1080) | 9:16 (1080x1920) |
| **Slides** | 5-10 slides | 5-10 slides |
| **Caption length** | 150-300 chars | 100-200 chars |
| **Hashtags** | 20-30 tags | 3-5 tags |
| **Tone** | Professional-clean | Casual, trending |
| **Watermark** | @tranvanhoang.com | @tranvanhoang.com |
| **Font style** | Clean sans-serif | Bold, more playful |

## Workflow

### Phase 1: Thu thập thông tin

Khi user gọi skill, cần:

1. **Content source** (bắt buộc): Transcript, insight, topic, hoặc bài viết
2. **Platform** (hỏi nếu thiếu): "instagram" hoặc "tiktok"
3. **Carousel type** (auto-detect hoặc user chọn): Listicle, Step-by-step, Before/After, Myth-busting, Story

Nếu thiếu platform, hỏi user:
```json
{"questions": [
  {"question": "Tạo carousel cho nền tảng nào?", "header": "Platform", "multiSelect": false, "options": [
    {"label": "Instagram", "description": "Slides 1:1, caption dài, 20-30 hashtags"},
    {"label": "TikTok", "description": "Slides 9:16, caption ngắn, 3-5 hashtags"},
    {"label": "Cả hai", "description": "Tạo 2 versions cho IG và TikTok"}
  ]}
]}
```

### Phase 2: Phân tích & chọn structure

Đọc input và auto-detect carousel type:

| Dấu hiệu nội dung | Carousel Type |
|--------------------|---------------|
| Danh sách tips, tools, features | **Listicle** |
| Hướng dẫn step-by-step, tutorial | **Step-by-step** |
| So sánh trước/sau, transformation | **Before/After** |
| Phản bác quan niệm sai, myth-busting | **Myth-busting** |
| Kể chuyện, narrative, journey | **Story** |

Xem chi tiết templates tại [Slide Templates](references/slide-templates.md).

### Phase 3: Tạo slides

Cho mỗi slide, tạo:
1. **Headline** (2-5 từ, bold)
2. **Body** (1-2 câu ngắn)
3. **Visual direction** (màu nền, icon, layout)
4. **Design note** (highlight, underline, special emphasis)
5. **Image prompt** — Prompt tạo ảnh theo design system, sẵn sàng dùng với Nano Banana Pro hoặc image generator

Áp dụng [Design System](references/design-system.md) cho visual direction và prompt generation.

### Phase 4: Tạo caption

Tạo caption theo platform rules:
- Instagram: [IG Rules](references/ig-rules.md)
- TikTok: [TikTok Rules](references/tiktok-rules.md)

### Phase 5: Output

**Quy tắc slide content bắt buộc:**
1. Slide 1 (Cover) PHẢI hook — quyết định swipe hay skip
2. Mỗi slide 1 ý duy nhất — KHÔNG nhồi nhét
3. Text ngắn gọn — đọc được trong 3 giây
4. Slide cuối PHẢI có CTA rõ ràng
5. KHÔNG dùng emoji trong slide text
6. Tiếng Việt có dấu, giữ English tech terms

## Output Format

```
═══════════════════════════════════════
PHAN TICH
═══════════════════════════════════════

Source: [Tiêu đề / chủ đề]
Platform: [Instagram / TikTok / Cả hai]
Carousel type: [Listicle / Step-by-step / Before-After / Myth-busting / Story]
Số slides: [N]

═══════════════════════════════════════
CAROUSEL: [Tiêu đề carousel]
Platform: [Instagram 1:1 / TikTok 9:16]
Type: [Carousel type]
Slides: [N]
═══════════════════════════════════════

## Slide 1 — Cover
**Headline:** [2-5 từ, bold — hook chính]
**Body:** [1 câu sub-headline hoặc để trống]
**Visual:** [Màu nền, layout]
**Design:** [Yellow highlight trên headline]
**Prompt:**
```
[Full image generation prompt — Nano Banana Pro / Gemini compatible]
```

---

## Slide 2
**Headline:** [2-5 từ]
**Body:** [1-2 câu]
**Visual:** [Màu nền, icon gợi ý]
**Design:** [Notes]
**Prompt:**
```
[Full image generation prompt]
```

---

...

## Slide N — CTA
**Headline:** [CTA text]
**Body:** [Follow / Save / Link in bio]
**Visual:** [Brand colors, @tranvanhoang.com]
**Design:** [Red underline trên CTA keyword]
**Prompt:**
```
[Full image generation prompt]
```

═══════════════════════════════════════
CAPTION
═══════════════════════════════════════

[Caption text — copy-paste ready]

[Hashtags]
```

## Mandatory Rules

### Slides
- Cover slide = hook — PHẢI gây tò mò
- 1 ý / 1 slide — đọc được trong 3 giây
- Text ngắn: headline 2-5 từ, body 1-2 câu MAX
- Visual direction phải consistent across slides
- CTA slide cuối — không bao giờ bỏ qua

### Caption
- Platform-specific length và hashtag count
- Vietnamese có dấu đầy đủ
- Brand voice applied
- CTA phù hợp platform

### Output
- Content phải copy-paste ready
- Lưu output vào `workspace/content/carousel/` nếu user yêu cầu save
- Tên file: `[slug]-carousel-[ig|tiktok].md`
