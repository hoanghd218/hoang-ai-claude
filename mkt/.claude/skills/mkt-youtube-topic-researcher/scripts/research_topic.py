# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31",
#     "python-dotenv>=1.0",
# ]
# ///
"""
YouTube Topic Researcher
Search YouTube videos by keyword, filter by views and breakout ratio (views/subscribers).

Usage:
    uv run research_topic.py "claude code"
    uv run research_topic.py "ai agents" --min-views 50000 --date week
    uv run research_topic.py "mcp server" --sort ratio --max-results 30
    uv run research_topic.py "vibe coding" --lang en --no-save
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"


def load_api_key() -> str:
    """Load YouTube API key from .env file, searching up from script dir."""
    script_dir = Path(__file__).resolve().parent
    for ancestor in [script_dir, *script_dir.parents]:
        env_path = ancestor / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            break

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key.startswith("your_"):
        print("Error: YOUTUBE_API_KEY not found in .env", file=sys.stderr)
        sys.exit(1)
    return api_key


def get_published_after(date_filter: str) -> str:
    """Get ISO 8601 cutoff date for the given filter."""
    now = datetime.now(timezone.utc)
    delta = {
        "today": timedelta(hours=24),
        "week": timedelta(days=7),
        "month": timedelta(days=30),
        "year": timedelta(days=365),
    }.get(date_filter, timedelta(days=30))
    cutoff = now - delta
    return cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:60]


def search_videos(api_key: str, query: str, published_after: str,
                  max_results: int, order: str, lang: str | None) -> list[dict]:
    """Search YouTube for videos matching query."""
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": order,
        "publishedAfter": published_after,
        "maxResults": min(max_results, 50),
        "key": api_key,
    }
    if lang:
        params["relevanceLanguage"] = lang

    all_items = []
    page_token = None
    fetched = 0

    while fetched < max_results:
        if page_token:
            params["pageToken"] = page_token
        params["maxResults"] = min(max_results - fetched, 50)

        resp = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=30)
        if resp.status_code != 200:
            error_msg = resp.json().get("error", {}).get("message", resp.text[:200])
            print(f"Error searching YouTube: {resp.status_code} - {error_msg}", file=sys.stderr)
            if resp.status_code == 403:
                print("Hint: Check your API key and quota at console.cloud.google.com", file=sys.stderr)
            break

        data = resp.json()
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            video_id = item.get("id", {}).get("videoId")
            if not video_id:
                continue
            snippet = item["snippet"]
            thumbnails = snippet.get("thumbnails", {})
            thumb_url = (
                thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url")
                or ""
            )
            all_items.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "channel_id": snippet.get("channelId", ""),
                "published_at": snippet.get("publishedAt", ""),
                "thumbnail_url": thumb_url,
            })

        fetched += len(items)
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return all_items


def get_video_stats(api_key: str, video_ids: list[str]) -> dict[str, dict]:
    """Fetch statistics and content details for videos."""
    stats = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        resp = requests.get(YOUTUBE_VIDEOS_URL, params={
            "part": "statistics,contentDetails",
            "id": ",".join(batch),
            "key": api_key,
        }, timeout=30)
        if resp.status_code != 200:
            print(f"Error fetching video stats: {resp.status_code}", file=sys.stderr)
            continue
        for item in resp.json().get("items", []):
            s = item.get("statistics", {})
            stats[item["id"]] = {
                "view_count": int(s.get("viewCount", 0)),
                "like_count": int(s.get("likeCount", 0)),
                "comment_count": int(s.get("commentCount", 0)),
                "duration": item.get("contentDetails", {}).get("duration", ""),
            }
    return stats


def get_channel_subscribers(api_key: str, channel_ids: list[str]) -> dict[str, int]:
    """Fetch subscriber counts for channels."""
    subs = {}
    unique_ids = list(set(channel_ids))
    for i in range(0, len(unique_ids), 50):
        batch = unique_ids[i:i + 50]
        resp = requests.get(YOUTUBE_CHANNELS_URL, params={
            "part": "statistics",
            "id": ",".join(batch),
            "key": api_key,
        }, timeout=30)
        if resp.status_code != 200:
            print(f"Error fetching channel stats: {resp.status_code}", file=sys.stderr)
            continue
        for item in resp.json().get("items", []):
            sub_count = int(item.get("statistics", {}).get("subscriberCount", 0))
            subs[item["id"]] = sub_count
    return subs


def format_number(n: int) -> str:
    """Format number with commas."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def print_table(videos: list[dict], query: str, date_filter: str,
                min_views: int, sort_by: str, lang: str | None):
    """Print formatted summary table."""
    lang_str = f" | lang={lang}" if lang else ""
    header = f'YouTube Topic Research: "{query}"'
    filters = f"Filters: min {format_number(min_views)} views | {date_filter} | sorted by {sort_by}{lang_str}"
    found = f"Found: {len(videos)} videos"

    width = max(len(header), len(filters), len(found)) + 6
    print(f"\n{'═' * width}")
    print(f"  {header}")
    print(f"  {filters}")
    print(f"  {found}")
    print(f"{'═' * width}\n")

    if not videos:
        print("  No videos match the criteria.\n")
        return

    # Table header
    print(f" {'#':>3} | {'Title':<40} | {'Channel':<18} | {'Views':>9} | {'Subs':>9} | {'Ratio':>6} | URL")
    print(f" {'-'*3}-+-{'-'*40}-+-{'-'*18}-+-{'-'*9}-+-{'-'*9}-+-{'-'*6}-+{'-'*30}")

    for v in videos:
        title = v["title"][:38] + ".." if len(v["title"]) > 40 else v["title"]
        channel = v["channel"][:16] + ".." if len(v["channel"]) > 18 else v["channel"]
        ratio_str = f"{v['breakout_ratio']:.1f}x" if v["breakout_ratio"] > 0 else "N/A"
        short_url = f"youtu.be/{v['video_id']}"

        print(f" {v['rank']:>3} | {title:<40} | {channel:<18} | {format_number(v['view_count']):>9} | {format_number(v['subscriber_count']):>9} | {ratio_str:>6} | {short_url}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Research YouTube videos by topic — filter by views & breakout ratio",
    )
    parser.add_argument("query", help="Search keyword/topic")
    parser.add_argument("--min-views", type=int, default=10000,
                        help="Minimum view count (default: 10000)")
    parser.add_argument("--date", "-d", choices=["today", "week", "month", "year"],
                        default="month", help="Date range (default: month)")
    parser.add_argument("--max-results", type=int, default=20,
                        help="Max results to fetch (default: 20)")
    parser.add_argument("--sort", choices=["views", "ratio", "date", "relevance"],
                        default="views", help="Sort results by (default: views)")
    parser.add_argument("--lang", help="Language filter (e.g. vi, en)")
    parser.add_argument("--output", "-o", help="Custom output file path")
    parser.add_argument("--no-save", action="store_true",
                        help="Print only, don't save to file")

    args = parser.parse_args()
    api_key = load_api_key()

    # Map sort option to YouTube API order parameter
    yt_order = {
        "views": "viewCount",
        "date": "date",
        "relevance": "relevance",
        "ratio": "viewCount",  # fetch by views, re-sort by ratio later
    }.get(args.sort, "viewCount")

    # Search
    published_after = get_published_after(args.date)
    print(f"Searching YouTube for \"{args.query}\" ({args.date})...", file=sys.stderr)
    raw_videos = search_videos(api_key, args.query, published_after,
                               args.max_results, yt_order, args.lang)

    if not raw_videos:
        print("No videos found.", file=sys.stderr)
        print_table([], args.query, args.date, args.min_views, args.sort, args.lang)
        return

    print(f"Found {len(raw_videos)} raw results. Fetching stats...", file=sys.stderr)

    # Fetch video stats
    video_ids = [v["video_id"] for v in raw_videos]
    video_stats = get_video_stats(api_key, video_ids)

    # Fetch channel subscriber counts
    channel_ids = [v["channel_id"] for v in raw_videos]
    channel_subs = get_channel_subscribers(api_key, channel_ids)

    # Build enriched results
    enriched = []
    for v in raw_videos:
        stats = video_stats.get(v["video_id"], {})
        view_count = stats.get("view_count", 0)

        # Apply minimum views filter
        if view_count < args.min_views:
            continue

        sub_count = channel_subs.get(v["channel_id"], 0)
        ratio = round(view_count / sub_count, 2) if sub_count > 0 else 0.0

        enriched.append({
            "title": v["title"],
            "video_id": v["video_id"],
            "url": f"https://www.youtube.com/watch?v={v['video_id']}",
            "channel": v["channel"],
            "channel_id": v["channel_id"],
            "subscriber_count": sub_count,
            "view_count": view_count,
            "like_count": stats.get("like_count", 0),
            "comment_count": stats.get("comment_count", 0),
            "breakout_ratio": ratio,
            "published_at": v["published_at"],
            "duration": stats.get("duration", ""),
            "thumbnail_url": v["thumbnail_url"],
        })

    # Sort
    if args.sort == "ratio":
        enriched.sort(key=lambda x: x["breakout_ratio"], reverse=True)
    elif args.sort == "views":
        enriched.sort(key=lambda x: x["view_count"], reverse=True)
    elif args.sort == "date":
        enriched.sort(key=lambda x: x["published_at"], reverse=True)
    # relevance: keep YouTube's default order

    # Add rank
    for i, v in enumerate(enriched, 1):
        v["rank"] = i

    # Print summary table
    print_table(enriched, args.query, args.date, args.min_views, args.sort, args.lang)

    filtered_count = len(raw_videos) - len(enriched)
    if filtered_count > 0:
        print(f"  Filtered out {filtered_count} video(s) with < {format_number(args.min_views)} views\n", file=sys.stderr)

    # Save to file
    if not args.no_save:
        if args.output:
            output_path = Path(args.output)
        else:
            slug = slugify(args.query)
            output_path = Path("research/youtube/topics") / slug / "videos.json"

        output_data = {
            "metadata": {
                "query": args.query,
                "date_filter": args.date,
                "min_views": args.min_views,
                "sort_by": args.sort,
                "language": args.lang,
                "max_results": args.max_results,
                "searched_at": datetime.now(timezone.utc).isoformat(),
                "total_results": len(enriched),
                "filtered_out": filtered_count,
            },
            "videos": enriched,
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved to: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
