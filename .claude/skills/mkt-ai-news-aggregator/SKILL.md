---
name: mkt-ai-news-aggregator
description: Aggregate AI news from Perplexity, GitHub Trending, and X.com (via xAI Grok) into a unified digest. USE WHEN user says 'ai news today', 'tin AI hôm nay', 'research AI news', 'tìm tin AI', 'aggregate AI news', 'github trending AI', 'ai news digest'.
---

# AI News Aggregator

## Purpose
Scan 3 sources in parallel for the latest AI news and compile into a single digest for content creation.

## Sources
1. **Perplexity Sonar Pro via OpenRouter** — structured AI news with citations
2. **GitHub Trending** — trending AI/ML repositories
3. **xAI Grok** — trending AI discussions on X.com

## Process

### Step 1: Run all 3 scripts in parallel
```bash
# Perplexity AI news
uv run .claude/skills/mkt-ai-news-aggregator/scripts/search_perplexity.py --query "AI news" --period 24h --format json

# GitHub trending AI repos
uv run .claude/skills/mkt-ai-news-aggregator/scripts/github_trending.py --language python --since daily --topic ai

# X.com trending via Grok
uv run .claude/skills/mkt-ai-news-aggregator/scripts/search_x_posts.py --topic "AI" --period 24h --limit 10
```

### Step 2: Merge results
Combine all outputs into a unified digest. For each item:
- Title/headline
- Source (Perplexity/GitHub/X.com)
- Summary (2-3 sentences)
- URL/link
- Relevance score (1-10) for Vietnamese SME audience

### Step 3: Rank and filter
- Score each item for audience relevance (target: Vietnamese SME owners, managers 28-45)
- Filter: keep items scoring 7+/10
- Sort by relevance score descending

### Step 4: Save digest
Output to `research/ai-news/[YYYY-MM-DD]/digest.json`

## Output Format
```json
{
  "date": "YYYY-MM-DD",
  "total_items": N,
  "filtered_items": N,
  "sources": {
    "perplexity": N,
    "github": N,
    "xcom": N
  },
  "items": [
    {
      "title": "...",
      "source": "perplexity|github|xcom",
      "summary": "...",
      "url": "...",
      "relevance_score": 8,
      "tags": ["claude", "ai-agent", "automation"]
    }
  ]
}
```

## Environment Variables Required
- `OPENROUTER_API_KEY` — OpenRouter API (routes to Perplexity Sonar Pro)
- `XAI_API_KEY` — xAI Grok API (already configured)
