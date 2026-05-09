# Layout Specifications

16 layout types for chalkboard developer explainer slides. All layouts designed for **16:9 landscape** (PowerPoint ratio) — maximize horizontal space.

## 1. Split Comparison

**Use for**: A vs B, before/after, pros/cons, old vs new

```
LAYOUT: split layout with a vertical dashed chalk divider
LEFT SIDE
  Title: [Left Label]
  [Panel color] panel with white chalk outline
  Inside: [icon drawing]
  Text: [short label]
  Caption: [description]
RIGHT SIDE
  Title: [Right Label]
  [Panel color] panel with white chalk outline
  Inside: [icon drawing]
  Text: [short label]
  Caption: [description]
```

Multiple panels per side allowed (stacked vertically with curved chalk arrows).

## 2. Circular Loop

**Use for**: Self-healing systems, feedback loops, recurring cycles, CI/CD

```
LAYOUT: circular loop with 4 chalk-drawn nodes arranged in a circle
  Connected by curved chalk arrows forming a continuous loop
  Top node ([color] panel): [icon] text: [label]
  Right node ([color] panel): [icon] text: [label]
  Bottom node ([color] panel): [icon] text: [label]
  Left node ([color] panel): [icon] text: [label]
  Center: [optional central concept label]
```

## 3. Layered Stack

**Use for**: Architecture layers, tech stacks, OSI model, abstraction levels

```
LAYOUT: layered stack of [N] horizontal panels stacked vertically
  Top-to-bottom ordering (highest abstraction at top)
  Top layer ([color] panel): [icon] text: [label]
  Middle layer ([color] panel): [icon] text: [label]
  Bottom layer ([color] panel): [icon] text: [label]
  Vertical dashed chalk arrows between layers
  Labels on left side: [layer names]
```

## 4. Linear Flow

**Use for**: Step-by-step processes, pipelines, data flow, request lifecycle

```
LAYOUT: linear horizontal flow with [N] panels connected by curved chalk arrows
  Left-to-right direction
  Panel 1 ([color]): [icon] text: [label]
  Arrow →
  Panel 2 ([color]): [icon] text: [label]
  Arrow →
  Panel 3 ([color]): [icon] text: [label]
  Each panel: rounded soft [color] panel with white chalk outline
```

## 5. Vertical Step Ladder

**Use for**: Sequential tutorial steps, numbered instructions, setup guides

```
LAYOUT: vertical step ladder with [N] numbered steps
  Each step: numbered chalk circle on left, panel on right
  Step 1 ([color] panel): [icon] text: [label]
    Curved chalk arrow down ↓
  Step 2 ([color] panel): [icon] text: [label]
    Curved chalk arrow down ↓
  Step 3 ([color] panel): [icon] text: [label]
  Numbers: large chalk-drawn numerals (1, 2, 3...)
```

## 6. Hub-and-Spoke

**Use for**: Central concept with related features, microservices, plugin architecture

```
LAYOUT: hub-and-spoke diagram
  CENTER: large [color] circle with [icon] text: [central concept]
  Surrounding spokes (evenly distributed):
    Spoke 1 ([color] panel): [icon] text: [label]
    Spoke 2 ([color] panel): [icon] text: [label]
    Spoke 3 ([color] panel): [icon] text: [label]
    Spoke 4 ([color] panel): [icon] text: [label]
  Connected by chalk lines from center to each spoke
```

## 7. Input → Transform → Output

**Use for**: Data processing, API transforms, ETL, function behavior, compiler stages

```
LAYOUT: three-section horizontal flow
  LEFT (Input): [color] panel with [icon] text: [input label]
  CENTER (Transform): larger [color] panel with gear/cog icon
    text: [process name]
    Small sub-labels below: [detail 1], [detail 2]
  RIGHT (Output): [color] panel with [icon] text: [output label]
  Thick curved chalk arrows: Input → Transform → Output
```

## 8. Timeline

**Use for**: History, evolution, roadmap, version progression, project phases

```
LAYOUT: horizontal timeline with chalk-drawn horizontal line
  [N] milestone markers evenly spaced on the line
  Each milestone: vertical tick mark with panel above or below (alternating)
    Milestone 1 (above, [color] panel): [icon] text: [label] date: [time]
    Milestone 2 (below, [color] panel): [icon] text: [label] date: [time]
    Milestone 3 (above, [color] panel): [icon] text: [label] date: [time]
  Arrow at right end of timeline indicating continuation
```

## 9. Decision Branch

**Use for**: If/else logic, routing decisions, error handling paths, feature flags

```
LAYOUT: decision tree branching from top
  TOP: [color] diamond shape with question text: [condition?]
  LEFT BRANCH (labeled "Yes" or condition met):
    Curved chalk arrow down-left
    [color] panel: [icon] text: [outcome A]
  RIGHT BRANCH (labeled "No" or condition not met):
    Curved chalk arrow down-right
    [color] panel: [icon] text: [outcome B]
  Optional: sub-branches from outcomes
```

## 10. Grid / Matrix

**Use for**: Feature comparison tables, capability matrices, tool comparisons

```
LAYOUT: [rows]x[cols] grid matrix
  Column headers (top row): [Header 1] | [Header 2] | [Header 3]
  Row headers (left column): [Row 1] | [Row 2] | [Row 3]
  Each cell: small [color] panel with [icon or checkmark/X]
  Grid lines: dashed chalk lines
  Header cells: slightly larger, bold chalk text
```

## 11. Funnel / Pyramid

**Use for**: Sales funnel, learning progression, filtering stages, priority hierarchy

```
LAYOUT: wide horizontal funnel narrowing left-to-right (or inverted pyramid top-to-bottom centered in 16:9 frame)
  Top/Wide layer ([color] panel): [icon] text: [label] — widest
  Middle layer ([color] panel): [icon] text: [label] — medium
  Bottom/Narrow layer ([color] panel): [icon] text: [label] — smallest
  Each layer: trapezoid shape with white chalk outline
  Dashed chalk arrows pointing inward between layers
  Labels on right side: [counts or percentages]
```

## 12. Before → Problem → Solution (Three-Act)

**Use for**: Pain-point storytelling, product pitch, "why this matters" explanations

```
LAYOUT: three horizontal panels side-by-side spanning full 16:9 width
  LEFT panel (red, ~30% width): sad face or broken icon
    Title: Before / Problem
    text: [pain point description]
  CENTER panel (gold, ~30% width): lightning bolt or warning icon
    Title: The Issue
    text: [root cause]
  RIGHT panel (green, ~30% width): checkmark or rocket icon
    Title: Solution
    text: [solution description]
  Curved chalk arrows connecting left → center → right
  Small chalk sparkle effects around the solution panel
```

## 13. Zoom-In / Exploded View

**Use for**: Deep dive into one component, anatomy of a system, code block breakdown

```
LAYOUT: left side shows a small overview diagram, right side shows zoomed-in detail
  LEFT (~35% width): small complete system diagram with one section highlighted
    Dashed chalk circle or bracket around the highlighted section
    Chalk magnifying glass icon near the highlight
  RIGHT (~60% width): enlarged detail of the highlighted section
    Multiple labeled sub-panels with chalk annotations
    Chalk arrows pointing to specific parts with labels
  Connecting: dashed chalk lines from left highlight to right detail area
```

## 14. Scoreboard / Metrics Dashboard

**Use for**: Performance comparison, benchmark results, KPI overview, tool ratings

```
LAYOUT: horizontal row of 3-5 metric cards evenly spaced across 16:9 width
  Each card: tall rounded [color] panel with white chalk outline
    Top: large chalk-drawn number or percentage
    Middle: small icon
    Bottom: metric label text
  Below cards: horizontal dashed chalk baseline
  Optional: small up/down chalk arrows next to numbers indicating trend
  Optional: one card highlighted larger as "hero metric"
```

## 15. Sandwich / Wrapper Pattern

**Use for**: Middleware, decorators, HOC, security layers, request-response wrapping

```
LAYOUT: concentric rounded rectangles (3 layers) centered in 16:9 frame
  OUTER layer ([color] panel, largest): text: [outer wrapper label]
  MIDDLE layer ([color] panel): text: [middle layer label]
  INNER layer ([color] panel, smallest): text: [core/payload label]
  Chalk arrows on left side entering from outside → in
  Chalk arrows on right side exiting from inside → out
  Labels on sides: "Request →" on left, "← Response" on right
```

## 16. Cause-and-Effect / Fishbone

**Use for**: Root cause analysis, debugging, "why does X happen", troubleshooting

```
LAYOUT: horizontal fishbone (Ishikawa) diagram spanning full 16:9 width
  Main horizontal chalk arrow pointing right to: [effect/problem] in red panel
  Diagonal chalk branches above and below the main line (3 above, 3 below)
    Branch 1 (above, blue panel): [cause category 1] with sub-causes
    Branch 2 (below, gold panel): [cause category 2] with sub-causes
    Branch 3 (above, purple panel): [cause category 3] with sub-causes
    Branch 4 (below, green panel): [cause category 4] with sub-causes
  Each branch: angled chalk line with small panel at the end
  Sub-causes: smaller chalk text along each branch line
```
