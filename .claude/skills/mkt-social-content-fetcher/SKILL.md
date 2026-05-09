---
name: mkt-social-content-fetcher
description: Fetch viral AI content from TikTok and Facebook using Apify scrapers. USE WHEN you need to scrape TikTok creator videos or Facebook page posts about AI topics.
---

# mkt-social-content-fetcher

## Purpose

Fetch viral AI content from TikTok and Facebook pages/creators using Apify REST API.
Used by the `mkt-ai-content-researcher` agent as data collection sub-agents.

## Prerequisites

- `APIFY_API_TOKEN` in `.env`
- `uv` installed

## Scripts

### fetch_tiktok.py — Fetch TikTok videos from AI creators

```bash
uv run .claude/skills/mkt-social-content-fetcher/scripts/fetch_tiktok.py \
  --handles "handle1,handle2" \
  --min-views 10000 \
  --period week \
  --output research/ai-content/YYYY-MM-DD/tiktok.json
```

**Args:**
- `--handles` — comma-separated TikTok handles (from sources.json or override)
- `--min-views` — minimum view count filter (default: 10000)
- `--period` — `day`, `week`, `month` (default: week)
- `--output` — output file path (optional, default: stdout)
- `--sources-file` — path to sources.json (default: auto-detect)

**Output:**
```json
{
  "source": "tiktok",
  "date": "YYYY-MM-DD",
  "period": "week",
  "items": [
    {
      "title": "video description",
      "url": "https://tiktok.com/@handle/video/...",
      "author": "@handle",
      "views": 123456,
      "likes": 5000,
      "shares": 200,
      "published_at": "YYYY-MM-DD",
      "tags": ["ai", "automation"],
      "thumbnail_url": "..."
    }
  ]
}
```

### fetch_facebook.py — Fetch Facebook page posts from AI pages

```bash
uv run .claude/skills/mkt-social-content-fetcher/scripts/fetch_facebook.py \
  --pages "PageName1,PageName2" \
  --date-from YYYY-MM-DD \
  --min-likes 100 \
  --output research/ai-content/YYYY-MM-DD/facebook.json
```

**Args:**
- `--pages` — comma-separated Facebook page names/URLs
- `--date-from` — fetch posts from this date (default: 7 days ago)
- `--min-likes` — minimum likes filter (default: 100)
- `--output` — output file path (optional, default: stdout)
- `--sources-file` — path to sources.json (default: auto-detect)

**Output:** Same format as TikTok but source = "facebook".

## Sources Config

Edit `.claude/skills/mkt-social-content-fetcher/sources.json` to configure which channels to monitor per platform.

## Apify Actors Used

- TikTok: `clockworks/tiktok-scraper`
- Facebook: `apify/facebook-posts-scraper`
