---
name: kdp-cover-creator
description: >
  Generate full-color KDP book cover (front + spine + back) as PDF.
  Handles both 8.5x11 (portrait) and 8.5x8.5 (square) books with correct
  aspect ratios. Uses the configured image renderer (from IMAGE_RENDERER in .env) for artwork.
  Outputs cover PNG + PDF ready for KDP upload. USE WHEN user says 'make cover',
  'generate cover', 'create book cover', 'kdp cover', 'tao bia sach', 'cover pdf',
  'build cover', 'cover for coloring book'.
---

# KDP Cover Creator

Generate a full KDP-compliant book cover (front + spine + back) as both PNG and PDF.

---

## Input

Accept any of these:
1. **Theme key** — looks up plan from `output/{theme_key}/plan.json` and theme from `config.py`
2. **Plan JSON path** — reads book details directly
3. **Manual details** — concept, title, author, page count, page size

Always need:
- **Author name** (for cover text)
- **Theme key** (for file paths and config lookup)

---

## Process

### Step 1: Read Book Details

Read `output/{theme_key}/plan.json` to get:
- `title` — for front cover text
- `subtitle` — for front cover text (optional)
- `audience` — adults or kids (affects style)
- `page_size` — **critical**: "8.5x11" or "8.5x8.5"
- `cover_prompt` — AI prompt for front artwork
- `page_prompts` — count determines spine width

Also check `config.py` THEMES dict for theme registration.

### Step 2: Determine Aspect Ratios

**This is critical for correct cover generation.**

| Book Size | Front Cover Aspect Ratio | Back Cover Image Ratio | Trim Size |
|-----------|--------------------------|------------------------|-----------|
| 8.5x11 (portrait) | `3:4` | `3:4` | 8.5" x 11" |
| 8.5x8.5 (square) | `1:1` | `1:1` | 8.5" x 8.5" |

The aspect ratio affects:
- Front artwork generation (AI33 `aspect_ratio` parameter)
- Back cover sample page thumbnails (must match page shape)
- Overall cover height calculation

### Step 3: Generate Front Cover Artwork

Run `generate_cover.py` with the correct parameters:

```bash
# For 8.5x11 (portrait) books (renderer auto-detected from .env IMAGE_RENDERER):
python generate_cover.py --theme {theme_key} --author "{author}" --size 8.5x11

# For 8.5x8.5 (square) books:
python generate_cover.py --theme {theme_key} --author "{author}" --size 8.5x8.5

# Override renderer if needed:
python generate_cover.py --theme {theme_key} --author "{author}" --size 8.5x11 --renderer ai33
```

**IMPORTANT**: Before running, verify that `generate_cover.py` uses the correct aspect ratio for the book size. The code in `generate_front_artwork()` must pass the right aspect ratio to the renderer:

- For 8.5x11: `aspect_ratio="3:4"`
- For 8.5x8.5: `aspect_ratio="1:1"`

If the code hardcodes `3:4`, fix it first:

```python
# In generate_front_artwork(), replace hardcoded aspect ratio:
# OLD: return _generate_image_ai33(prompt, aspect_ratio="3:4")
# NEW: determine from page size
page_size = size if size else config.DEFAULT_PAGE_SIZE
ar = config.PAGE_SIZES[page_size]["ai33_aspect_ratio"]
return _generate_image_ai33(prompt, aspect_ratio=ar)
```

### Step 4: Fix Back Cover for Square Books

For 8.5x8.5 books, the back cover sample page thumbnails must use 1:1 aspect ratio:

In `generate_cover.py`, the `page_ratio` variable in the sample pages grid section:

```python
# OLD (hardcoded portrait):
# page_ratio = 3300 / 2550  # ~1.294

# NEW (dynamic based on page size):
page_dims = config.get_page_dims(size)
page_ratio = page_dims["height_px"] / page_dims["width_px"]  # 1.294 for portrait, 1.0 for square
```

This ensures square books show square thumbnails on the back cover.

### Step 5: Cover Dimensions

Cover dimensions are auto-calculated:

```
Spine width = total_pages × 0.002252" (white paper)
Full width  = (2 × trim_width) + spine + (2 × 0.125" bleed)
Full height = trim_height + (2 × 0.125" bleed)
```

| Book Size | Approx Cover Width (50 pages) | Cover Height |
|-----------|-------------------------------|-------------|
| 8.5x11 | ~17.36" | 11.25" |
| 8.5x8.5 | ~17.36" | 8.75" |

KDP can also provide exact dimensions — use `--kdp-width` and `--kdp-height` to override.

### Step 6: Verify Output (KDP Pre-flight)

Check:
- `output/{theme_key}/cover.png` exists and > 500KB
- `output/{theme_key}/cover.pdf` exists (this is what KDP needs)
- Front artwork matches theme and has title text
- Back cover shows sample pages with **correct aspect ratio**
- For square books: back thumbnails are square, NOT portrait rectangles
- Author name visible on front
- Barcode area clear on back — **NO template text** in barcode area (triggers rejection)
- **Spine text clearance**: if spine has text, verify 0.0625" clearance on each side
- **Spine text only if 79+ pages** — fewer pages = no spine text allowed
- **Metadata consistency**: title on cover must match title on interior title page

---

## Output

```
COVER GENERATED!

Cover PNG: output/{theme_key}/cover.png
Cover PDF: output/{theme_key}/cover.pdf  ← Upload this to KDP

Dimensions: {width}px × {height}px ({full_width}" × {full_height}")
Spine: {spine_width}" ({total_pages} pages)
Page size: {page_size}
Aspect ratios: front={ar}, back thumbnails={ar}
```

---

## Code Fixes Required

Before running for the first time, apply these fixes to `generate_cover.py`:

### Fix 1: Front artwork aspect ratio (line ~199)

The `generate_front_artwork()` function needs a `size` parameter:

```python
def generate_front_artwork(theme: str, title: str = "", renderer: str = "gemini", size: str = config.DEFAULT_PAGE_SIZE) -> Image.Image | None:
```

And use it for AI33:
```python
if renderer == "ai33":
    ar = config.PAGE_SIZES[size]["ai33_aspect_ratio"]
    return _generate_image_ai33(prompt, aspect_ratio=ar)
```

### Fix 2: Back cover thumbnail ratio (line ~584)

Replace hardcoded ratio:
```python
# OLD:
page_ratio = 3300 / 2550

# NEW:
page_dims_for_ratio = config.get_page_dims(size)
page_ratio = page_dims_for_ratio["height_px"] / page_dims_for_ratio["width_px"]
```

### Fix 3: Pass size to generate_front_artwork (line ~406)

```python
# OLD:
artwork = generate_front_artwork(theme, title, renderer=renderer)

# NEW:
artwork = generate_front_artwork(theme, title, renderer=renderer, size=size)
```

---

## Quality Checklist

- [ ] Cover PDF exists at `output/{theme_key}/cover.pdf`
- [ ] Front artwork uses correct aspect ratio for book size
- [ ] Back cover thumbnails use correct aspect ratio (1:1 for square, 3:4 for portrait)
- [ ] Title text is readable over front artwork
- [ ] Author name displayed on front cover
- [ ] Barcode area clear on back cover
- [ ] 300 DPI resolution
- [ ] Spine width calculated correctly for page count
- [ ] Cover height matches book trim height + bleed
