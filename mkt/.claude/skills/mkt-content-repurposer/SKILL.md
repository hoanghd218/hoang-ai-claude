---
name: mkt-content-repurposer
description: Transform one long-form content piece (video transcript, book chapter, article) into 6-8 multi-format content pieces across 5 platforms — Facebook, X.com, LinkedIn, Instagram carousel, TikTok carousel. USE WHEN user says 'repurpose content', 'tách content', 'chuyển video thành nhiều content', 'repurpose transcript', '1 video thành nhiều bài', 'content repurpose', 'nhân bản content', 'đăng đa nền tảng', 'multi-platform content'.
---

# Content Repurposer — Multi-Platform

## Purpose
Force multiplier: take 1 long-form piece and produce 6-8 content pieces across 5 platforms. Each piece is standalone and optimized for its target platform.

## Supported Platforms

| Platform | Skill Reference | Format Types |
|----------|----------------|--------------|
| **Facebook** | `video-to-facebook-posts`, `mkt-book-to-wisdom-posts` | Actionable, Comparison, Listicle, Deep-dive, Wisdom image |
| **X.com** | `mkt-xcom-post-creator` | Insight Thread, Step-by-step Thread, Hot Take Thread, Tool Thread, Standalone |
| **LinkedIn** | `mkt-linkedin-post-creator` | Insight Post, Case Study, Contrarian Take, Carousel Text |
| **Instagram** | `mkt-carousel-creator` (IG mode) | Listicle, Step-by-step, Before/After, Myth-busting, Story carousel |
| **TikTok** | `mkt-carousel-creator` (TikTok mode) + `mkt-create-script-short-video` | Carousel slides, Short video script |

## Input
- Video transcript (from `youtube-transcript` skill)
- Book excerpt or chapter
- Article text
- Expert content / podcast transcript

## Process

### Step 1: Extract standalone insights
Read the full source content and extract 5-8 standalone insights. Each insight must:
- Be understandable WITHOUT the full context
- Have a clear takeaway or action item
- Be interesting enough to stand alone as a post

### Step 2: Classify each insight & map to platforms
For each insight, determine the best platforms and formats:

| Insight Type | Best Platforms | Format per Platform |
|-------------|---------------|---------------------|
| **Quotable wisdom, pithy truth** | Facebook + X.com + LinkedIn | Wisdom image (`mkt-book-to-wisdom-posts`) + Quote Card (`mkt-xcom-post-creator`) + Insight Post (`mkt-linkedin-post-creator`) |
| **Actionable how-to, step-by-step** | Facebook + X.com + IG Carousel | Actionable Post (`video-to-facebook-posts`) + Step-by-step Thread (`mkt-xcom-post-creator`) + Step-by-step Carousel (`mkt-carousel-creator`) |
| **Data/comparison, analysis** | LinkedIn + X.com + Facebook | Case Study (`mkt-linkedin-post-creator`) + Insight Thread (`mkt-xcom-post-creator`) + Comparison Post (`video-to-facebook-posts`) |
| **Counter-intuitive, bold opinion** | X.com + LinkedIn + Facebook | Hot Take Thread (`mkt-xcom-post-creator`) + Contrarian Take (`mkt-linkedin-post-creator`) + Deep-dive Post (`video-to-facebook-posts`) |
| **Visual concept, list of items** | IG Carousel + TikTok Carousel + X.com | Listicle Carousel (`mkt-carousel-creator`) + Tool Thread (`mkt-xcom-post-creator`) |
| **Transformation story, before/after** | LinkedIn + IG Carousel + Facebook | Case Study (`mkt-linkedin-post-creator`) + Before/After Carousel (`mkt-carousel-creator`) + Actionable Post (`video-to-facebook-posts`) |
| **Short, punchy insight** | X.com + TikTok | Standalone Post (`mkt-xcom-post-creator`) + Short video script (`mkt-create-script-short-video`) |

**QUAN TRỌNG:** Chọn 2-3 best platforms per insight — KHÔNG ép tất cả 5 platforms cho mỗi insight.

### Step 3: Generate all outputs
For each insight, generate content following the format rules of the target skill:

**For Facebook Posts** (video-to-facebook-posts format):
- 300-600 words, no emoji, line breaks for mobile
- Hook > Value > CTA + Last Dab
- Brand voice applied

**For Facebook Wisdom Posts** (mkt-book-to-wisdom-posts format):
- 6 formats: Progressive Reduction, Never Too Late List, Contrast Pairs, Numbered Skills, Intangible Assets, Bold Statement
- Caption + image text layout

**For X.com Threads/Posts** (mkt-xcom-post-creator format):
- Max 280 chars/tweet, thread 3-10 tweets
- Hook tweet standalone, hashtags max 3 ở tweet cuối
- Tone sắc bén, data-driven, authority

**For LinkedIn Posts** (mkt-linkedin-post-creator format):
- 1300-2000 ký tự, professional tone
- Credential signals sớm, soft CTA
- Hashtags 3-5 cuối bài

**For IG/TikTok Carousels** (mkt-carousel-creator format):
- 5-10 slides, headline + body + visual direction per slide
- IG: 1:1, 20-30 hashtags, professional caption
- TikTok: 9:16, 3-5 hashtags, casual caption

**For Short Video Scripts** (mkt-create-script-short-video format):
- 60s max, Vietnamese conversational tone
- Before-After / Three Acts / Action structure

### Step 4: Compile content pack
Bundle all generated pieces into a single file, grouped by platform.

## Output
Master file at `workspace/content/[YYYY-MM-DD]/repurposed/[slug]-content-pack.md`:

```markdown
# Content Pack: [Source Title]
**Source**: [URL or book name]
**Date**: [YYYY-MM-DD]
**Total pieces generated**: [N]
**Platforms**: [list of platforms covered]

---

## FACEBOOK

### Piece 1: [Format] — [Insight Title]
[Generated content — copy-paste ready]

---

### Piece 2: [Format] — [Insight Title]
[Generated content]

---

## X.COM

### Piece 3: [Format] — [Insight Title]
[Thread or standalone post — copy-paste ready]

---

## LINKEDIN

### Piece 4: [Format] — [Insight Title]
[LinkedIn post — copy-paste ready]

---

## INSTAGRAM CAROUSEL

### Piece 5: [Format] — [Insight Title]
[Slide-by-slide content + caption + hashtags]

---

## TIKTOK

### Piece 6: [Format] — [Insight Title]
[Carousel slides or short video script]

---
```

## Rules
1. **Each piece must stand alone** — no references to "the video" or "as I mentioned"
2. **Apply brand voice per platform** — read `MY RESOURCES/BRANDVOICE.MD` then adjust tone per platform:
   - Facebook: 7/10 energy, conversational expert
   - X.com: 8/10 energy, sharp authority
   - LinkedIn: 6.5/10 energy, professional thoughtful
   - IG/TikTok carousel: 7.5/10 energy, bold visual
3. **Tiếng Việt có dấu đầy đủ** — giữ English tech terms
4. **No emoji** — in body text across all platforms
5. **Minimum 6 pieces across minimum 3 platforms** — if fewer than 5 insights extractable, source may not be suitable
6. **Diverse platforms** — aim for at least 3 different platforms per pack
7. **Quality over quantity** — chọn 2-3 best platforms per insight, không ép tất cả 5
8. **Platform-specific rules** — follow each platform skill's mandatory rules (char limits, hashtag counts, CTA styles)
