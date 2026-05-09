---
name: mkt-news-to-content-brief
description: Filter and rank AI news digest into content briefs with audience relevance scoring, hooks, and format recommendations. USE WHEN user says 'news to content', 'tạo content brief từ tin', 'content brief from news', 'chuyển tin thành content', 'rank news for content'.
---

# News to Content Brief

## Purpose
Take raw news digest from `mkt-ai-news-aggregator` and produce ranked content briefs ready for script creation.

## Input
- Digest JSON from `mkt-ai-news-aggregator` (at `research/ai-news/[date]/digest.json`)
- OR inline news items

## Process

### Step 1: Score audience relevance
For each news item, score 1-10 based on:
- **Direct applicability (8-10)**: Can Vietnamese SME owners use this immediately? (e.g., new free AI tool, Claude update)
- **Trend awareness (5-7)**: Important to know but not immediately actionable (e.g., new AI model benchmark)
- **Niche/technical (1-4)**: Only relevant to developers or researchers

### Step 2: Filter
Keep only items scoring 7+/10 on audience relevance.

### Step 3: Generate content brief for each item

```
## [News Title]
**Relevance Score**: X/10
**Why it matters for our audience**: [1-2 sentences in Vietnamese — why Vietnamese SME owners should care]

**Suggested angle**: [How to frame this for Hoang's audience — not just "AI news" but "how this changes YOUR business"]

**Hook draft (Vietnamese)**:
"[Hook following brand voice — data/shock, one person power, or bold statement pattern]"

**Suggested format**:
- [ ] Facebook post (if opinion/commentary)
- [ ] Short video (if demo-able or visual)
- [ ] YouTube deep-dive (if complex topic needing explanation)

**Key talking points**:
1. [Point 1]
2. [Point 2]
3. [Point 3]

**Source**: [URL]
```

### Step 4: Rank and save
Sort by relevance score descending. Save to `workspace/content/news-briefs/[YYYY-MM-DD]-ai-news-briefs.md`.

## Output
Markdown file with 3-5 content briefs, ranked by relevance. Each brief is ready to feed into `mkt-create-script-short-video` or `video-to-facebook-posts`.

## Brand Voice Rules
- All hooks and angles must follow brand voice from `MY RESOURCES/BRANDVOICE.MD`
- Target persona from `MY RESOURCES/WHO10X TECH.MD`
- Language: Vietnamese with power words in English (System, Automation, AI, Framework, etc.)
- Energy: 7/10 — confident, actionable, not hype
