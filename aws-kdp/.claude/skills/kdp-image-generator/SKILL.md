---
name: kdp-image-generator
description: Generate coloring page images using the configured image renderer (set via IMAGE_RENDERER in .env). USE WHEN user says 'generate coloring pages', 'create coloring images', 'generate images for book', 'run image generation', 'kdp generate images', 'make coloring page images', 'generate pages from plan'.
---

# KDP Image Generator

Generates coloring book page images using the configured image renderer (from `IMAGE_RENDERER` in `.env`). Supported renderers: `ai33`, `bimai`, `nanopic`. This is the ONLY step that calls an external API — for image generation only, not prompt writing.

---

## When to Use

- After prompts are written (by `kdp-prompt-writer` skill)
- User wants to generate or regenerate coloring page images
- The `/project:kdp-create-book` command reaches the generation phase

---

## Process

### Step 1: Verify Prerequisites

Check that:
1. Plan exists: `output/{theme_key}/plan.json`
2. `.env` has `IMAGE_RENDERER` set (e.g. `bimai`, `ai33`, or `nanopic`) and the corresponding API key (`BIMAI_API_KEY`, `AI33_KEY`, or `NANOPIC_API_KEY`)
3. Dependencies installed: `pip install Pillow python-dotenv requests`

```bash
ls output/{theme_key}/plan.json
```

### Step 2: Run Image Generation

**Plan-based (recommended):**
```bash
python generate_images.py --plan output/{theme_key}/plan.json --count {num_pages}
```
The script auto-detects `page_size` from the plan JSON (`"8.5x11"` or `"8.5x8.5"`). For 8.5x8.5, images are generated with 1:1 (square) aspect ratio. You can override with `--size 8.5x8.5`.

**Theme-based (legacy, for existing themes in config.py):**
```bash
python generate_images.py --theme {theme_key} --count {num_pages}
```

**Resume from a specific page:**
```bash
python generate_images.py --plan output/{theme_key}/plan.json --count {num_pages} --start {start_index}
```

### Step 3: Monitor Progress

The script outputs:
- `[page_num/total] Generating: {prompt_preview}...`
- `Saved: page_XX.png` on success
- `FAILED: Could not generate image` on failure

Note failed pages for regeneration.

### Step 4: Handle Failures

If pages fail:
1. The script auto-retries 3 times with delays
2. If still failing, wait and re-run with `--start` at the failed index
3. Rate limit: 5 seconds between requests (built-in)
4. If persistent failures, check API key and quota

### Step 5: Verify Output

```bash
ls -la output/{theme_key}/images/
```

Check:
- Expected number of `page_XX.png` files exist
- File sizes are reasonable (>50KB each)
- No zero-byte files

---

## Technical Details

- **Renderer**: Configured via `IMAGE_RENDERER` in `.env` (supports: `ai33`, `bimai`, `nanopic`)
- **Requires**: Corresponding API key in `.env` (`AI33_KEY`, `BIMAI_API_KEY`, or `NANOPIC_API_KEY`)
- **Override**: Use `--renderer` flag to override the `.env` default
- **Post-processing**: Grayscale conversion, contrast +2.0, brightness +1.3
- **Margins**: 0.25" (75px) — image centered on full page
- **Parallel**: Up to 5 concurrent workers for faster generation

**Page sizes (`--size`):**
| Size | Dimensions | Aspect Ratio | Pixels (300 DPI) |
|------|-----------|--------------|------------------|
| `8.5x11` (default) | 8.5" x 11" portrait | 3:4 | 2550 x 3300 |
| `8.5x8.5` | 8.5" x 8.5" square | 1:1 | 2550 x 2550 |

---

## Output

- `output/{theme_key}/images/page_01.png` through `page_XX.png`
- Each image: grayscale, 300 DPI, PNG format
  - 8.5x11: 2550x3300px (portrait)
  - 8.5x8.5: 2550x2550px (square)

---

## Quality Criteria

- All requested pages generated (no missing files)
- Images are grayscale line art (not photos, not colored)
- Clean white background
- Lines are visible and bold
- No artifacts or distortion
- No zero-byte or corrupted files
