---
name: kdp-prompt-writer
description: Analyze concepts and write SEO-optimized prompts for KDP coloring books. Claude writes ALL prompts — no AI generation. USE WHEN user says 'write coloring book prompts', 'create book plan', 'plan coloring book', 'write page prompts', 'kdp prompts', 'coloring book plan', 'write book metadata', 'create kdp plan'.
---

# KDP Prompt Writer

Claude analyzes the book concept and writes everything: SEO metadata, cover prompt, and all interior page prompts. NO AI/Gemini is used for this step — Claude is the expert prompt writer.

---

## When to Use

- User wants to plan a new coloring book
- The `/project:kdp-create-book` command reaches the planning phase
- User wants to write or rewrite prompts for an existing theme

---

## Process

### Step 1: Determine Audience, Page Size & Load Guidelines

Determine the **page_size** (from user or calling command):
- `"8.5x11"` — Portrait (default). Images are 3:4 aspect ratio.
- `"8.5x8.5"` — Square. Images are 1:1 aspect ratio. All prompts must describe SQUARE compositions.

Read the appropriate reference guide:
- **Adults**: Read `references/adult-prompt-guide.md` in this skill directory
- **Kids**: Read `references/kids-prompt-guide.md` in this skill directory

### Step 2: Write SEO Metadata

Generate based on the concept:

**Title** — Catchy, keyword-rich, includes audience indicator
- Adults: e.g., "Whiskers & Warmth: A Cozy Cat Café Coloring Book for Adults"
- Kids: e.g., "Amazing Dinosaurs Coloring Book for Kids Ages 6-12"

**Subtitle** — Descriptive, complementary
- Adults: e.g., "Relaxing Kawaii Scenes with Cute Cats, Warm Drinks & Cozy Interiors"
- Kids: e.g., "Bold & Easy Designs for Creative Kids"

**Description** — 3-5 sentences for Amazon KDP listing. Emphasize:
- Adults: cozy charm, relaxation, stress relief, beautiful scenes
- Kids: fun, creativity, learning, hours of entertainment

**Keywords** — 7 SEO-relevant keywords for Amazon search

### Step 3: Write Cover Prompt

**Adults cover prompt must include:**
- Full-color illustration (NOT black-and-white)
- Warm, premium cozy aesthetic
- Multiple large readable props and decorative elements
- Title and subtitle text reference
- State "Coloring Book for Adults"

**Kids cover prompt must include:**
- Full-color, vibrant cartoon style
- Eye-catching, professional children's book cover art
- DO NOT include any text/letters/words in the generated image
- Bright colors, cheerful composition
- Mention "Coloring Book for Kids Ages 6-12"

### Step 4: Write Page Prompts (20-30)

**For Adults (Cozy & Cute):**
Each prompt describes a complete black-and-white coloring page with:
- "Cute cozy medium-detail" adult aesthetic
- **KDP line thickness**: All outlines must be bold enough to meet KDP's minimum 0.75pt (0.01") line weight. Add "bold thick outlines suitable for coloring" to every prompt.
- Complete layered scene: foreground + midground + background
- Large, clear decorative shapes — NO dense micro-patterns
- Simplified vegetation (large stylized shapes, wide spacing, no micro-veins)
- Spaced-out background motifs (wallpapers, textiles use big shapes)
- Kawaii character proportions (consistent across pages)
- Cozy environment props: shelves, lamps, cushions, windows, curtains, tables, art, rugs
- Mix of solo scenes and occasional secondary character interactions
- **If page_size is 8.5x8.5**: Add "SQUARE format (1:1 aspect ratio)" to every prompt. Compose scenes that work well in a square frame — balanced, not too tall.
- **If page_size is 8.5x11**: Add "PORTRAIT orientation (taller than wide)" to every prompt.

**For Kids (Bold & Easy):**
Each prompt describes a single-subject coloring page with:
- Black-and-white line art only
- Bold, thick, clean outlines for ages 6-12 (must meet KDP minimum 0.75pt / 0.01" line weight)
- Single subject centered, fills most of page
- NO shading, gradients, borders, or frames
- White background
- Cute, friendly, appealing style
- Simple enough for crayons/markers
- **If page_size is 8.5x8.5**: Add "SQUARE format (1:1 aspect ratio)" to every prompt. Subject should fill the square frame evenly.
- **If page_size is 8.5x11**: Add "PORTRAIT orientation (taller than wide)" to every prompt.

### Step 5: Ensure Variety

Page prompts must cover diverse scenes/activities:
- Different settings (indoor, outdoor, seasonal)
- Different activities (cooking, reading, playing, sleeping, crafting)
- Different moods (playful, peaceful, cozy, adventurous)
- Main character in different poses/situations

**IMPORTANT — Avoid AI Body-Part Errors**: AI image generation (Gemini) frequently renders multiple characters with merged/fused bodies, missing limbs, extra arms, or overlapping anatomy — making them look deformed. To prevent this:
- **Minimize the number of characters per scene** — fewer characters = fewer rendering errors
- When multiple characters appear, they must be **clearly separated** with space between them (no touching, overlapping, or intertwined poses)
- Prefer a **pet companion** (cat, dog, bunny) over a second human character — animals are simpler to render correctly
- Avoid prompts with physically close interactions (hugging, holding hands, dancing together) — these cause body-part fusion errors
- Add "IMPORTANT: Each character must have clearly defined, complete body with no overlapping or merged body parts" to every prompt that includes more than one character
- Background characters (e.g., vendors at a market) are acceptable only if they are small, distant, and clearly separated from the main character

### Step 6: Save Plan

Create the plan JSON file at `output/{theme_key}/plan.json`:
```json
{
  "theme_key": "the_theme_key",
  "audience": "adults|kids",
  "page_size": "8.5x11|8.5x8.5",
  "title": "...",
  "subtitle": "...",
  "description": "...",
  "keywords": ["kw1", "kw2", "kw3", "kw4", "kw5", "kw6", "kw7"],
  "cover_prompt": "...",
  "page_prompts": ["prompt1", "prompt2", ...]
}
```

**`page_size`** defaults to `"8.5x11"` if not specified. This field is read by `generate_images.py`, `build_pdf.py`, and `generate_cover.py` to set the correct dimensions and aspect ratio.

Also save `output/{theme_key}/prompts.txt` (one prompt per line).

### Step 7: Register Theme

Add to `config.py` THEMES dict:
```python
"{theme_key}": {
    "name": "{Title}",
    "book_title": "{Full Title}",
    "prompt_file": "output/{theme_key}/prompts.txt",
},
```

---

## Output

- `output/{theme_key}/plan.json` — Full plan with metadata + all prompts
- `output/{theme_key}/prompts.txt` — One prompt per line

---

## Quality Criteria

- Title is SEO-friendly and audience-appropriate
- Description is compelling and marketplace-ready
- 7 diverse, relevant keywords
- Cover prompt matches audience style guidelines
- Every page prompt follows the correct audience guide strictly
- Page prompts are varied (different scenes, activities, settings)
- Characters described consistently across all prompts
- No dense micro-detail instructions in adult prompts
- No shading/gradient instructions in kids prompts

---

## References

- `references/adult-prompt-guide.md` — Cozy & cute adult style (from Hoja 1)
- `references/kids-prompt-guide.md` — Bold & easy kids style
