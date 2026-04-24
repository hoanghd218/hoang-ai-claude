---
name: kdp-image-reviewer
description: Review coloring book images for quality and KDP compliance. USE WHEN user says 'review coloring pages', 'check image quality', 'review generated images', 'kdp image review', 'check coloring book images', 'which pages need regeneration', 'quality check images'.
---

# KDP Image Reviewer

Claude visually reviews each coloring page image to assess quality, style consistency, and KDP compliance. Uses Claude's multimodal vision to inspect every page directly.

---

## When to Use

- After images are generated (by `kdp-image-generator` skill)
- User wants to check quality before building PDF
- The `/project:kdp-create-book` command reaches the review phase

---

## Process

### Step 1: Identify Theme & Audience

Ask the user or detect from context:
- **Theme key** (folder name in `output/images/`)
- **Audience**: adults or kids (determines quality criteria)

Check the plan file if available:
```bash
cat output/{theme_key}/plan.json | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('audience','unknown'))"
```

### Step 2: Inventory & Technical Check

First, detect the expected page size from the plan:
```bash
python -c "
import json, os
plan = json.load(open('output/{theme_key}/plan.json')) if os.path.exists('output/{theme_key}/plan.json') else {}
size = plan.get('page_size', '8.5x11')
print(f'Page size: {size}')
"
```

Then run a quick technical scan (adjust expected dimensions based on page_size):
```bash
python -c "
from PIL import Image
import os, glob, json

theme = '{theme_key}'
img_dir = f'output/{theme}/images/'

# Detect expected size from plan
plan_path = f'plans/{theme}_plan.json'
expected_w, expected_h = 2550, 3300  # default 8.5x11
if os.path.exists(plan_path):
    plan = json.load(open(plan_path))
    if plan.get('page_size') == '8.5x8.5':
        expected_w, expected_h = 2550, 2550

issues = []
for f in sorted(glob.glob(os.path.join(img_dir, '*.png'))):
    img = Image.open(f)
    name = os.path.basename(f)
    w, h = img.size
    mode = img.mode
    fsize = os.path.getsize(f) / 1024

    if w != expected_w or h != expected_h:
        issues.append(f'{name}: Wrong size {w}x{h} (expected {expected_w}x{expected_h})')
    if mode not in ('L', 'LA'):
        issues.append(f'{name}: Not grayscale (mode={mode})')
    if fsize < 50:
        issues.append(f'{name}: Suspiciously small ({fsize:.0f}KB)')

    print(f'{name}: {w}x{h} {mode} {fsize:.0f}KB')

print()
print(f'Expected: {expected_w}x{expected_h}')
if issues:
    print('ISSUES FOUND:')
    for i in issues:
        print(f'  - {i}')
else:
    print('All images pass technical checks.')
"
```

### Step 3: Claude Visual Review (Core Step)

**Use the Read tool to open and visually inspect EVERY image file.** Claude can see PNG images directly.

For each image at `output/{theme_key}/images/page_XX.png`:

1. **Read the image** using the Read tool
2. **Evaluate** against the criteria below based on audience type
3. **Score**: PASS, WARN (minor issues but usable), or REDO (must regenerate)
4. **Note specific issues** if any

#### Review Criteria for Adults (cozy/cute style):
- Scene composition: foreground + midground + background layers present?
- Detail level: colorable without being overwhelming? No dense micro-patterns?
- Line quality: clean, consistent thickness, no broken lines?
- Style: kawaii/cozy aesthetic maintained? Large stylized shapes?
- Content: matches the prompt intent? Scene feels complete, not empty?
- Artifacts: any distortion, blurring, unwanted text, or color remnants?

#### Review Criteria for Kids (6-12):
- Single clear subject centered and filling the page?
- Bold, thick outlines suitable for crayons/markers?
- NO shading, gradients, gray fills, or half-tones?
- Simple enough for the target age?
- No unwanted text, borders, frames, or decorative elements?
- Clean lines without artifacts?

#### Anatomy & Character Issues (CRITICAL — always check):
- **Mirror/reflection creating duplicate character**: If a mirror or reflective surface shows a full character, it looks like 2 people on the page. Prompts for single-character pages should use "NO mirrors, NO reflections". Mark as REDO and fix the prompt to remove the mirror
- **Multiple characters when only one intended**: Count all visible human figures including reflections, silhouettes, and partially visible people. If the prompt says "single character" but the image shows 2+ people, mark as REDO
- **Partially visible second person**: A second character cut off at the edge, or only torso/limbs visible without a head — mark as REDO
- **Multiple characters merging**: Two or more characters overlapping, sharing body parts, or blending into each other. AI often renders multi-character scenes with bodies fused together — mark as REDO
- **Missing limbs**: Characters missing arms, legs, hands, or feet when they should be visible
- **Missing or malformed heads**: Characters without a clear head, or with distorted facial features
- **Extra fingers/limbs**: Characters with too many fingers, extra arms, or duplicate body parts
- **Clothing without a person**: Empty clothing (shirt, dress) rendered without a body inside — mark as REDO
- **Body horror**: Any grotesque, unnatural, or disturbing body proportions or anatomy
- **Ghost characters**: Faint or partial second character appearing in the background when only one was intended

**IMPORTANT**: Single-character prompts are safest. If a prompt mentions mirrors, vanity tables, or reflective surfaces, the AI will often render a full reflection that looks like a second person. When reviewing, always count the number of visible human figures (including reflections). When fixing prompts, add "NO mirrors, NO reflections" and change the scene to avoid reflective surfaces.

#### KDP Technical Compliance (CRITICAL):
- **Line thickness**: Lines must be at minimum 0.75pt (0.01" / 0.3mm). Lines thinner than this may not print correctly. If lines appear hairline-thin, mark as REDO.
- **Gray fill minimum**: Any gray-filled areas must be at least 10% fill. Very light gray (<10%) won't reproduce in print. If image has barely-visible gray shading, mark as WARN.
- **No color remnants**: Must be pure grayscale. Any RGB color traces = REDO.

#### Other Common Issues to Flag:
- Text or letters appearing in the image
- Color or gray shading (should be pure line art)
- Too cluttered / too sparse
- Broken or inconsistent line weight
- Unwanted borders or frames
- Subject doesn't match prompt
- Blurry or distorted areas
- Overly complex areas that would be frustrating to color

### Step 4: Report Findings

Present results as a summary table:

| Page | Score | Issues |
|------|-------|--------|
| page_01.png | PASS | Clean scene, good detail level |
| page_02.png | WARN | Slightly dense foliage in corner, but usable |
| page_03.png | REDO | Contains unwanted text, lines too thin |
| ... | ... | ... |

Then summarize:
- **Total pages**: X
- **PASS**: X pages
- **WARN**: X pages (list briefly)
- **REDO**: X pages (list with reasons)

### Step 5: Regenerate Problem Pages

For pages marked REDO, ask the user if they want to regenerate. For each:

1. Delete the bad image:
```bash
rm output/{theme_key}/images/page_XX.png
```

2. Optionally adjust the prompt in `output/{theme_key}/plan.json`

3. Regenerate (0-indexed start):
```bash
python generate_images.py --plan output/{theme_key}/plan.json --start {XX-1} --count 1
```

4. **Re-review the regenerated page** by reading it again with the Read tool

---

## Output

- Visual review report with PASS/WARN/REDO per page
- Specific issues described from Claude's visual inspection
- Regenerated images for REDO pages (after user approval)

---

## Important Notes

- **Always read every image** — do not skip visual review even if technical checks pass
- **Read images in batches** of 5-8 for efficiency (multiple parallel Read calls)
- Compare pages against each other for **style consistency** across the book
- If many pages have the same issue, note it as a systemic problem (likely a prompt issue)
- After regeneration, always re-review the new image before marking it as done
