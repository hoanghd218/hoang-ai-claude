---
name: mkt-edu-slide-nano
description: "Analyze video scripts and generate Nano Banana Pro image prompts for educational slide illustrations in chalkboard developer explainer style. Input is a video script (Vietnamese). Output is a slide plan with prompts for each key knowledge point. Use for IT/AI knowledge-sharing video slides, tech explainer diagrams, developer education content. Supports 16 layout types. USE WHEN user says 'tạo slide', 'slide cho video', 'ảnh slide', 'edu slide', 'explainer slide', 'chalkboard slide', 'developer diagram', 'tech slide prompt', 'slide giải thích', 'slide kiến thức', 'hình minh họa cho video', 'phân tích script tạo slide'."
---

# Edu Slide Prompt Generator — Chalkboard Dev Explainer

Analyze video scripts → identify knowledge points needing visual explanation → generate Nano Banana Pro prompts in chalkboard dev explainer style.

## Workflow

1. **Read script** — Read the full video script provided by user
2. **Scan & Plan** — Scan for visual moments + output slide plan table in one pass:

| # | Timestamp / Section | Concept | Layout | Title / Subtitle |
|---|---------------------|---------|--------|-----------------|
| 1 | PHẦN 1: Vấn đề | Manual research pain | Before→Problem→Solution | ... |
| 2 | PHẦN 2: Setup | 4-step setup guide | Vertical Step Ladder | ... |

3. **Generate prompts** — For each slide, generate a complete prompt and write to output file


## How to Scan for Visual Moments

Look for these patterns in the script:

| Script Pattern | Slide Needed |
|---------------|-------------|
| `[VISUAL] Diagram ...` or `[VISUAL] So sánh ...` | Explicitly requested diagram |
| "Bước 1... Bước 2... Bước 3..." | Step-by-step layout |
| "A vs B", "cũ vs mới", trước/sau | Split Comparison |
| "Vòng lặp", "cycle", self-healing | Circular Loop |
| Kiến trúc, layers, stack | Layered Stack |
| "Flow", pipeline, request lifecycle | Linear Flow |
| Central concept + nhiều features | Hub-and-Spoke |
| Timeline, "6:00 AM → 6:30 AM" | Timeline |
| "Nếu... thì...", if/else logic | Decision Branch |
| Số liệu, KPI, benchmark | Scoreboard |
| Pain → Cause → Solution narrative | Before→Problem→Solution |
| Zoom into a component | Zoom-In / Exploded View |
| Funnel, filtering, hierarchy | Funnel / Pyramid |

## Fixed Master Style

Every prompt MUST start with this opening + end with this style/negative block:

**Opening:**
```
A developer explainer diagram drawn on a matte black chalkboard background.
```

**Style block (append at end of every prompt):**
```
SIGNATURE: small chalk-style text "@tranvanhoang.com" in the bottom-right corner of the image as a subtle watermark signature. STYLE REQUIREMENTS: hand-drawn chalkboard explainer style white chalk handwritten typography slightly imperfect handwritten strokes chalk marker lettering looks like hand written with a chalk pen on a blackboard NOT a modern sans-serif font NOT typed text NOT digital UI font TEXT STYLE: clean readable chalk handwriting solid white strokes no chalk dust no speckled texture high contrast readable letters VISUAL STYLE: hand drawn developer whiteboard diagram chalkboard presentation slide engineering explainer diagram clean chalk marker lines minimal texture presentation quality readability NEGATIVE PROMPT: modern sans serif font helvetica font arial font clean digital UI typography vector UI infographic photorealistic 3D render glossy UI
```

## Color System

| Color | Use For |
|-------|---------|
| **Red** | Errors, warnings, problems, "before" state |
| **Blue** | Info, processes, neutral steps |
| **Green** | Success, solutions, completion |
| **Gold/Yellow** | Highlights, important notes, attention |
| **Purple** | Advanced concepts, special features |
| **Gray** | Background info, secondary content |

## Icon System

Simple chalk-drawn icons only:
- **Tech**: laptop, monitor, smartphone, server rack, terminal window
- **Status**: checkmark, X mark, warning triangle, question mark
- **Flow**: curved arrows, dashed lines, dotted connectors
- **People**: stick figure, robot doodle, user silhouette
- **Data**: magnifying glass, gear/cog, database cylinder, cloud
- **Time**: clock, calendar, hourglass, stopwatch
- **Communication**: speech bubble, envelope, bell notification

## Layout Quick Selection

Read `references/layouts.md` for full 16 layout specs. Quick guide:

| Content Type | Best Layout |
|-------------|-------------|
| A vs B, before/after, pros/cons | **Split Comparison** |
| Feedback loops, cycles, CI/CD | **Circular Loop** |
| Architecture layers, tech stack | **Layered Stack** |
| Step-by-step process, pipeline | **Linear Flow** |
| Numbered tutorial steps | **Vertical Step Ladder** |
| Central concept + related features | **Hub-and-Spoke** |
| Data processing, API transform | **Input → Transform → Output** |
| History, evolution, roadmap | **Timeline** |
| If/else logic, routing, error handling | **Decision Branch** |
| Feature matrix, tool comparison | **Grid / Matrix** |
| Sales funnel, filtering stages | **Funnel / Pyramid** |
| Pain → cause → fix storytelling | **Before → Problem → Solution** |
| Deep dive into one component | **Zoom-In / Exploded View** |
| KPIs, benchmark results | **Scoreboard / Metrics Dashboard** |
| Middleware, decorators, wrapping | **Sandwich / Wrapper Pattern** |
| Root cause analysis, debugging | **Cause-and-Effect / Fishbone** |

## Prompt Template

```
A developer explainer diagram drawn on a matte black chalkboard background. [STYLE BLOCK] TITLE AT TOP: "[Tiêu Đề Có Dấu]" Subtitle: "[Phụ đề có dấu]" LAYOUT: [layout-specific description with panels, colors, icons, text in "quotes with diacritics", arrows] [STYLE BLOCK]
```

**Vietnamese text rule:** Every Vietnamese word/phrase appearing on the slide MUST be wrapped in `"double quotes"` with full diacritics. English technical terms do NOT need quotes.

## Aspect Ratio

ALWAYS **16:9** landscape (PowerPoint ratio). Command: `--aspect-ratio 16:9 --size 2K`.

Optimize for horizontal space: panels side-by-side, flows left→right, splits left/right.

## Generate Command

```bash
cd .claude/skills/image-post-creator && python3 scripts/generate.py "<prompt>" -o <output.png> -ar 16:9 --size 2K
```

## Output Format

Save output to a **separate .md file** alongside the script:
- Path: same folder as the script, named `[script-name]-slides.md`
- Example: if script is `workspace/content/2026-03-07/contents/my-script.md` → output `workspace/content/2026-03-07/contents/my-script-slides.md`

### Output file structure:

```markdown
# Slide Prompts — [Video Title]

**Script:** [path to original script]
**Total slides:** [N]
**Style:** Chalkboard Dev Explainer
**Aspect ratio:** 16:9

---

## Slide Plan

| # | Section | Concept | Layout | Title |
|---|---------|---------|--------|-------|
| 1 | PHẦN 1: ... | ... | Split Comparison | ... |
| 2 | PHẦN 2: ... | ... | Vertical Step Ladder | ... |

---

## Slide 1: [Concept Name]

**Section:** [PHẦN X: tên phần trong script]
**Script context:** [trích 1-2 câu từ script giải thích tại sao cần slide này]
**Layout:** [layout type]

### Prompt

\```
[complete ready-to-use prompt]
\```

---

## Slide 2: [Concept Name]
...
```

## Prompt Examples

See `references/prompt-examples.md` for 8 complete prompt examples (including 3 script-derived examples).

## Vietnamese Text Formatting

Nano Banana Pro **supports Vietnamese with diacritics**. When writing Vietnamese text in prompts:

1. **Always use full diacritics** — write `"Nghiên Cứu"` NOT `Nghien Cuu`
2. **Wrap every Vietnamese text in double quotes** — this helps the model render it correctly
3. **Technical terms stay in English** — API, AI, Agent, Workflow, CI/CD, Scheduled Tasks, etc.

### Examples

```
❌ BAD:  text: Nghien Cuu Content Thu Cong
❌ BAD:  text: Nghiên Cứu Content Thủ Công
✅ GOOD: text: "Nghiên Cứu Content Thủ Công"

❌ BAD:  Title: Truoc Day
❌ BAD:  Title: Trước Đây
✅ GOOD: Title: "Trước Đây"

❌ BAD:  Caption: AI tu lam moi sang
✅ GOOD: Caption: "AI Tự Làm Mỗi Sáng"

✅ OK:   text: Scheduled Tasks  (English technical term — no quotes needed)
✅ OK:   text: AI Agent  (English technical term — no quotes needed)
```

## Rules

1. **Slide language** — Default: **Vietnamese** (có dấu, trong ngoặc kép `""`). Vietnamese text in prompts MUST have full diacritics and be wrapped in double quotes. Technical terms (API, AI, Agent, Workflow, CI/CD, etc.) stay in English without quotes. If user requests English, use English for all on-image text
2. Keep text SHORT — max 3-5 words per panel label
3. Max 6-8 panels per slide for readability at 16:9
4. Always include TITLE and Subtitle at top
5. Every panel: color + icon + short text
6. Curved chalk arrows for relationships/flow
7. Consistent panel sizes within a layout
8. Never use digital/modern UI elements
9. Skip sections that don't need diagrams (talking head, emotional beats, CTAs)
10. Prioritize moments where the script says `[VISUAL] Diagram` or describes a comparison/process
