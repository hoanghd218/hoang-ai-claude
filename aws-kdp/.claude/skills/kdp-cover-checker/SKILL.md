---
name: kdp-cover-checker
description: >
  Validate KDP book cover PDFs against Amazon's dimension, bleed, and DPI specifications.
  Checks cover width/height based on page count and spine calculation, verifies 0.125" bleed
  on all sides, and ensures minimum 300 DPI. Supports both 8.5x11 (portrait) and 8.5x8.5
  (square) trim sizes. Can check a single book or scan all books in output/ folder.
  USE WHEN user says 'check cover', 'verify cover', 'validate cover', 'kiem tra bia',
  'cover dimensions', 'cover size check', 'kdp cover check', 'cover compliance',
  'check all covers', 'are my covers correct', 'cover specs', 'kiem tra kich thuoc bia'.
---

# KDP Cover Checker

Validate KDP book cover PDFs against Amazon's exact dimension and quality specifications.

---

## When to Run

- After generating covers with `/kdp-cover-creator` or `generate_cover.py`
- Before uploading to KDP to catch dimension errors
- When KDP rejects a cover for wrong dimensions
- To audit all books in the output/ folder at once

## How to Run

Execute the checker script:

```bash
# Check ALL books in output/
python .claude/skills/kdp-cover-checker/scripts/check_covers.py

# Check a single book
python .claude/skills/kdp-cover-checker/scripts/check_covers.py --theme cozy_cats_daily_life

# Verbose mode (show all details even for passing books)
python .claude/skills/kdp-cover-checker/scripts/check_covers.py --verbose
```

## KDP Cover Specifications

These are the exact rules the checker validates:

### Bleed (mandatory for covers)
- All covers MUST include 0.125" bleed on all 4 sides
- This is non-negotiable — KDP rejects covers without bleed

### Spine Width Formula
```
spine_width = total_pages * 0.002252"
```
Where `total_pages` = the interior PDF page count (white paper, black ink).

### Full Cover Dimensions
```
width  = 8.5" (back) + spine + 8.5" (front) + 0.125" (bleed left) + 0.125" (bleed right)
height = trim_height + 0.125" (bleed top) + 0.125" (bleed bottom)
```

### Example for 8.5x8.5 square, 104 pages
- Spine: 104 * 0.002252 = 0.234"
- Width: 8.5 + 0.234 + 8.5 + 0.125 + 0.125 = **17.484"**
- Height: 8.5 + 0.125 + 0.125 = **8.750"**
- At 300 DPI: 5245 x 2625 px

### Example for 8.5x11 portrait, 56 pages
- Spine: 56 * 0.002252 = 0.126"
- Width: 8.5 + 0.126 + 8.5 + 0.125 + 0.125 = **17.376"**
- Height: 11 + 0.125 + 0.125 = **11.250"**
- At 300 DPI: 5213 x 3375 px

### DPI
- Minimum 300 DPI required

### Tolerance
- Dimension tolerance: +/- 0.01" (3 pixels at 300 DPI)
- This accounts for rounding in pixel-to-inch conversion

## Understanding the Output

The checker reports for each book:

```
[PASS] cozy_cats_daily_life
  Pages: 104 | Size: 8.5x8.5 | Spine: 0.234"
  Expected: 17.484" x 8.750" | Actual: 17.484" x 8.750"

[FAIL] farm_animals_bold — WIDTH MISMATCH
  Pages: 56 | Size: 8.5x11 | Spine: 0.126"
  Expected: 17.376" x 11.250" | Actual: 17.250" x 11.250"
  Delta: width off by -0.126" (missing spine width?)

[SKIP] dragons_cute_friendly — no cover.pdf found
```

## What to Do with Failures

- **Width too small**: Usually means spine width wasn't included or page count changed after cover was generated. Regenerate the cover.
- **Height wrong**: Check if the correct page size (8.5x11 vs 8.5x8.5) was used.
- **DPI too low**: The cover image was saved at less than 300 DPI. Regenerate with `--dpi 300` or check the source image resolution.
- **Missing cover.pdf**: Run `/kdp-cover-creator` for that theme.

## Page Count Detection

The script determines page count by:
1. Counting PNG images in `output/{theme}/images/` directory
2. Calculating total pages: `2 (title + copyright) + (num_images * 2) + 1 (thank you)`, rounded up to even

This matches the logic in `generate_cover.py` and `build_pdf.py`.
