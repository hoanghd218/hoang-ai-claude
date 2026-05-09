---
name: mkt-competitor-video-strategy-analyzer
description: Analyze competitor YouTube video strategy — title patterns, hook structure, video pacing, thumbnail style, and cross-video patterns. Focuses on HOW competitors make videos, not just what they cover. USE WHEN user says 'phân tích chiến lược video', 'analyze competitor videos', 'video strategy analysis', 'phân tích đối thủ', 'competitor analysis'.
---

# Competitor Video Strategy Analyzer

## Input

Video metadata (title, views, publish date, thumbnail URL) + transcript text. Can be a single video or a batch from the same channel.

Accepted input formats:
- Direct video URL(s) — metadata fetched via `youtube-trend-finder` or YouTube API
- Pre-extracted metadata + transcript text
- Channel URL — fetch recent videos for batch analysis

## Process

1. **Parse video metadata and transcript** — Extract title, view count, publish date, thumbnail URL, and full transcript. Use `youtube-transcript` skill for transcript extraction if not provided.

2. **Analyze title pattern** — Detect formula type (e.g., "How to...", "X Ways...", "I [verb]..."), identify power words, measure character length, count emotional triggers. Score as Strong / Medium / Weak.

3. **Analyze hook (first ~200 words of transcript)** — Classify hook type (question, shocking stat, story, demo, bold claim, myth bust). Measure time-to-value: how quickly the viewer receives the first concrete insight. Identify retention signals (pattern interrupts, visual vs. audio hooks, promise specificity).

4. **Analyze video structure** — Break transcript into logical sections. Identify structure type (linear, problem-solution, listicle, tutorial, story-driven, hybrid). Map CTA placement (early, middle, end, multiple). Note mid-roll hooks, segment transitions, and cliffhangers.

5. **Analyze thumbnail via MiniMax understand_image MCP** — If thumbnail URL is provided, use MiniMax `understand_image` MCP tool to detect: face presence, text overlay patterns, color scheme, composition style, emotion conveyed, and brand consistency.

6. **Cross-video pattern analysis (batch mode)** — When analyzing multiple videos from one channel: identify repeating formats, correlate performance (views) with format type, calculate posting cadence, cluster related topics, and surface what overperforms relative to channel average.

7. **Generate strategy report** — Compile all findings into a structured markdown report with scoring, pattern summaries, and actionable takeaways.

## Output

- **Location**: `research/youtube/strategy/[channel-slug]/strategy-report.md`
- **Format**: Markdown report with the following sections:

```
## Channel Overview
## Title Pattern Analysis
## Hook Structure Analysis
## Video Structure Analysis
## Thumbnail Style Analysis
## Cross-Video Patterns (if batch)
## Key Takeaways & Actionable Insights
```

Each section includes:
- Data findings with specific examples
- Scoring indicators: ✅ Strong / ⚠️ Moderate / ❌ Weak
- Comparison to best practices
- Actionable recommendations for our channel

## Dependencies

- **youtube-transcript** skill — for transcript extraction
- **youtube-trend-finder** skill — for video metadata retrieval
- **MiniMax understand_image MCP** — for thumbnail visual analysis
- No Python scripts needed — pure LLM analysis + MCP tools

## Example Usage

```
Phân tích chiến lược video của kênh @ChannelName — lấy 10 video gần nhất,
phân tích title, hook, structure, thumbnail.
```

```
Analyze competitor videos: [video_url_1], [video_url_2], [video_url_3].
Focus on hook patterns and what makes their titles click-worthy.
```

## References

- `references/strategy-analysis-framework.md` — Full scoring framework for each analysis dimension
