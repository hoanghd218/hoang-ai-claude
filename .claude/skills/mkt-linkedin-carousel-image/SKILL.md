---
description: "Generate LinkedIn carousel images in ENGLISH from carousel markdown. Dark tech professional style, PNG slides via Nano Banana Pro."
trigger_phrases:
  - "tạo ảnh carousel linkedin"
  - "linkedin carousel images"
  - "render linkedin slides"
  - "generate linkedin carousel"
  - "ảnh slide linkedin"
input: "LinkedIn carousel markdown file (from mkt-carousel-creator or mkt-repurpose-to-social) OR carousel text content"
output: "PNG images per slide in workspace/content/YYYY-MM-DD/social-posts/images/"
tools:
  - Bash (for generate.py)
  - Read
  - Write
  - Glob
---

# LinkedIn Carousel Image Generator

Generate professional images for LinkedIn carousel PDF from carousel markdown content. Professional dark tech style for LinkedIn audience (executives, founders, tech professionals).

## Content Language Rule

**LinkedIn content MUST be in English.** All slide text, headlines, body text in image prompts must be English. Only Facebook and YouTube use Vietnamese.

## Design System

Đọc `references/design-system.md` cho full spec. Key points:
- **Dark navy background** (`#0F172A`) — professional, tech feel
- **Blue-purple gradient accents** (`#3B82F6` → `#8B5CF6`)
- **Monospace for data/metrics** — code/tech credibility
- **NO photos, NO emoji** — typography + data only
- **Footer**: `@tranvanhoang.com` every slide

## Image Generation

Sử dụng Nano Banana Pro (Gemini 3.1 Flash Image) via existing script:

```bash
~/.claude/skills/.venv/bin/python3 .claude/skills/image-post-creator/scripts/generate.py "<prompt>" \
  --output <path.png> \
  --aspect-ratio 1:1 \
  --size 2K \
  --verbose
```

## Workflow

### Phase 1: Read Input

1. Đọc carousel markdown file (chứa slides with headline, body, visual direction)
2. Đọc `references/design-system.md` cho design specs
3. Xác định output directory: `workspace/content/YYYY-MM-DD/social-posts/images/`
4. Create output directory if not exists

### Phase 2: Generate Prompts

Cho mỗi slide, tạo image generation prompt theo template:

```
A professional LinkedIn carousel slide image, 1080x1080 pixels.
Background: deep navy (#0F172A) solid color.
Typography-only design, NO photographs, NO illustrations, NO emoji.
Clean minimal tech aesthetic with subtle grid dot pattern at 3% opacity.

[SLIDE-SPECIFIC CONTENT BELOW]

Slide number: [##] displayed in accent blue (#3B82F6) bold text, top-left corner.

Headline: "[HEADLINE TEXT]" in bold white (#F1F5F9) sans-serif font (Inter/Geist style), 56-64px, left-aligned.

Body: "[BODY TEXT]" in regular white (#F1F5F9) sans-serif, 28-32px, left-aligned. Key phrases highlighted with blue (#3B82F6) color.

[ADDITIONAL ELEMENTS based on slide type — gradient bar, data display, comparison layout, etc.]

Footer: "@tranvanhoang.com" in muted gray (#64748B), 18px, bottom-center.
Padding: 80px all sides.
```

#### Slide Type Prompts

**Cover Slide:**
- Add gradient accent bar (blue→purple) at top, 6px height
- Label text in uppercase muted above headline
- Headline 64-72px, 2-3 lines max
- No slide number

**Content Slide (numbered):**
- Slide number `#0X` in accent blue, top-left
- Headline bold 56px
- Body 28-32px, max 4 lines
- Key term in accent blue

**Data/Benchmark Slide:**
- Numbers in monospace bold (JetBrains Mono style), 48-64px, accent blue
- Comparison numbers in muted gray
- Metric labels uppercase 18px above numbers

**Turning Point / Contrarian Slide:**
- Amber (#F59E0B) accent instead of blue for warning tone
- Headline slightly smaller, italic tagline below

**Summary/Last Dab Slide:**
- Short bullet points with checkmarks in green (#10B981)
- Closing statement in larger bold text
- Subtle gradient overlay

**CTA Slide:**
- Blue→purple gradient background overlay (20% opacity)
- Community name in accent blue bold
- URL in cyan (#06B6D4) underlined
- Tagline in italic muted text
- Gradient accent bar at bottom

### Phase 3: Generate Images

Loop qua từng slide prompt:

```bash
~/.claude/skills/.venv/bin/python3 .claude/skills/image-post-creator/scripts/generate.py \
  "<prompt>" \
  --output workspace/content/YYYY-MM-DD/social-posts/images/<slug>-slide-01.png \
  --aspect-ratio 1:1 \
  --size 2K \
  --verbose
```

- Generate sequentially (1 at a time to avoid rate limits)
- Show user each generated image path as it completes
- If generation fails, retry once then skip with warning

### Phase 4: Review & Output

After all slides generated:

1. List all generated images with paths
2. Show total slide count
3. Suggest: "Combine these PNGs into a PDF for LinkedIn upload"
4. Provide ImageMagick command for PDF assembly:

```bash
convert workspace/content/YYYY-MM-DD/social-posts/images/<slug>-slide-*.png \
  workspace/content/YYYY-MM-DD/social-posts/<slug>-linkedin-carousel.pdf
```

## Rules

- **MUST** read design-system.md before generating any prompts
- **MUST** generate 1:1 aspect ratio (LinkedIn carousel standard)
- **MUST** include `@tranvanhoang.com` footer in every slide prompt
- **MUST** use Vietnamese text with full diacritics in prompts
- **MUST** keep English for technical terms (AI, System, Workflow, MCP, etc.)
- **NO photos, NO complex illustrations** — typography + data visualization only
- **NO emoji** in slide content
- Sequential generation — one slide at a time
- Show progress to user after each slide
