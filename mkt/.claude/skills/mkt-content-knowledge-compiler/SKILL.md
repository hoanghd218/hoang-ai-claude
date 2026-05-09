---
name: mkt-content-knowledge-compiler
description: Compile learnings from video analysis into a persistent knowledge base — hooks, title formulas, video structures, insights library. USE WHEN user says 'compile knowledge', 'tổng hợp kiến thức', 'update knowledge base', 'cập nhật knowledge base', 'add to knowledge base'.
---

# Content Knowledge Compiler

## Purpose
Aggregate and deduplicate learnings from multiple analysis reports into structured knowledge base files. This creates a growing library of proven patterns that inform future content creation.

## Input
One or more analysis reports from:
- `mkt-competitor-video-strategy-analyzer` — strategy reports
- `mkt-insight-extractor` — extracted insights
- `script-storytelling-analyzer` — storytelling scores
- `mkt-content-format-analyzer` — format classifications
- Or any research output in `research/youtube/`

## Process

### Step 1: Read existing knowledge base
Read all files in `workspace/foundations/knowledge-base/` to understand what's already captured.
If the directory or files don't exist yet, create them.

### Step 2: Extract new learnings
From each input report, extract:
- **Hooks**: Any hook formula, pattern, or example that scored well
- **Titles**: Title formulas and patterns that drove high views
- **Structures**: Video structure patterns that retained viewers
- **Insights**: Key frameworks, paradigm shifts, principles worth referencing

### Step 3: Deduplicate
Compare new learnings against existing knowledge base entries. Skip duplicates. If a pattern is seen again, increment its `frequency` count.

### Step 4: Append to knowledge base
Add new entries to the appropriate file with metadata:
- Source video URL
- Date captured
- Performance metrics (views, if available)
- Frequency count (how many times this pattern has been seen)

## Output

Append to files in `workspace/foundations/knowledge-base/`:

### `hooks-that-work.md`
```
## [Hook Type] — [Source Channel]
- **Pattern**: [Hook formula]
- **Example**: "[Actual hook text]"
- **Source**: [Video URL]
- **Views**: [X]
- **Date**: [YYYY-MM-DD]
- **Frequency**: [N times seen]
```

### `title-formulas.md`
```
## [Formula Name]
- **Pattern**: [e.g., "Number + Adjective + Noun + Promise"]
- **Examples**:
  - "[Title 1]" (Xk views)
  - "[Title 2]" (Xk views)
- **When to use**: [Context]
- **Frequency**: [N]
```

### `video-structures.md`
```
## [Structure Type] — [Source Channel]
- **Pattern**: [e.g., Hook > Problem > 3 Solutions > CTA]
- **Duration**: [X minutes]
- **Section breakdown**: [list]
- **Source**: [Video URL]
- **Frequency**: [N]
```

### `insights-library.md`
```
## [Insight Title] — [Type: Framework/Paradigm Shift/Warning/Diagnosis/Principle]
- **Summary**: [1-2 sentences]
- **Source**: [Video URL / Book]
- **Date**: [YYYY-MM-DD]
- **Relevance**: [How this applies to Hoang's content]
```

## Rules
1. **APPEND, never overwrite** — always add to existing files, never replace them
2. **Deduplicate** — check for similar patterns before adding
3. **Include source** — every entry must have a source URL or reference
4. **Sort by frequency** — most-seen patterns should be at the top
5. **Create files if they don't exist** — on first run, create the knowledge-base directory and files
