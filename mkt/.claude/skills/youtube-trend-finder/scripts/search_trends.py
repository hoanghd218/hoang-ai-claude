#!/usr/bin/env python3
"""
YouTube Channel Video Finder
Fetch latest videos from subscribed channels AND search trending topics.
Uses YouTube Data API v3. Config loaded from channels.json.

Usage:
    python3 search_trends.py                                    # Channels + topics, today
    python3 search_trends.py --date week                        # Last 7 days
    python3 search_trends.py --channels "@BenAI92,@ColeMedin"   # Custom channels
    python3 search_trends.py --topics "claude code,ai agents"   # Custom topics
    python3 search_trends.py --no-topics                        # Channels only
    python3 search_trends.py --no-channels                      # Topics only
    python3 search_trends.py --format json --output results.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is not installed.", file=sys.stderr)
    print("Install it with: pip3 install python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests is not installed.", file=sys.stderr)
    print("Install it with: pip3 install requests", file=sys.stderr)
    sys.exit(1)

YOUTUBE_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
YOUTUBE_PLAYLIST_ITEMS_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

CONFIG_FILE = Path(__file__).resolve().parent.parent / "channels.json"

# How many playlist items to fetch per channel based on date filter
FETCH_COUNTS = {
    "today": 5,
    "week": 15,
    "month": 50,
}

# Max search results per topic
SEARCH_MAX_PER_TOPIC = 10


def load_config() -> dict:
    """Load channels and topics from channels.json."""
    if not CONFIG_FILE.exists():
        print(f"Warning: Config file not found at {CONFIG_FILE}", file=sys.stderr)
        return {"channels": [], "topics": []}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Support both old format (list) and new format (dict)
    if isinstance(data, list):
        return {"channels": data, "topics": []}
    return data


def load_api_key() -> str:
    """Load YouTube API key from .env file."""
    script_dir = Path(__file__).resolve().parent
    env_paths = [
        script_dir / ".env",
        script_dir.parent / ".env",
        script_dir.parent.parent / ".env",
        script_dir.parent.parent.parent / ".env",
        Path.cwd() / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "YOUTUBE_API_KEY":
        print("Error: YOUTUBE_API_KEY not found or not set in .env file.", file=sys.stderr)
        sys.exit(1)
    return api_key


def get_date_cutoff(date_filter: str) -> datetime:
    """Get the cutoff datetime for the given date filter."""
    now = datetime.now(timezone.utc)
    delta = {
        "today": timedelta(hours=24),
        "week": timedelta(days=7),
        "month": timedelta(days=30),
    }.get(date_filter, timedelta(hours=24))
    return now - delta


def resolve_handles(api_key: str, handles: list[str]) -> list[dict]:
    """Resolve @handles to channel info (ID, title, uploads playlist)."""
    channels = []
    for handle in handles:
        clean = handle.lstrip("@")
        resp = requests.get(YOUTUBE_CHANNELS_URL, params={
            "part": "snippet,contentDetails",
            "forHandle": clean,
            "key": api_key,
        }, timeout=30)

        if resp.status_code != 200:
            print(f"  Warning: Could not resolve @{clean} (HTTP {resp.status_code})", file=sys.stderr)
            continue

        items = resp.json().get("items", [])
        if not items:
            print(f"  Warning: Channel @{clean} not found", file=sys.stderr)
            continue

        ch = items[0]
        uploads_id = ch.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        if not uploads_id:
            print(f"  Warning: No uploads playlist for @{clean}", file=sys.stderr)
            continue

        channels.append({
            "handle": f"@{clean}",
            "id": ch["id"],
            "title": ch["snippet"]["title"],
            "uploads_playlist": uploads_id,
        })
        print(f"  Resolved @{clean} -> {ch['snippet']['title']}", file=sys.stderr)

    return channels


def fetch_playlist_videos(api_key: str, playlist_id: str, max_items: int) -> list[dict]:
    """Fetch recent videos from a playlist (uploads). Returns basic video info."""
    videos = []
    page_token = None

    while len(videos) < max_items:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": min(max_items - len(videos), 50),
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(YOUTUBE_PLAYLIST_ITEMS_URL, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"  Error fetching playlist {playlist_id}: {resp.status_code}", file=sys.stderr)
            break

        data = resp.json()
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            title = snippet.get("title", "")

            # Skip private/deleted videos
            if title in ("Private video", "Deleted video"):
                continue

            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = (
                thumbnails.get("maxres", {}).get("url")
                or thumbnails.get("standard", {}).get("url")
                or thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url")
                or ""
            )

            videos.append({
                "video_id": snippet.get("resourceId", {}).get("videoId", ""),
                "title": title,
                "channel": snippet.get("channelTitle", ""),
                "thumbnail_url": thumbnail_url,
                "published_at": snippet.get("publishedAt", ""),
                "source": "channel",
            })

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return videos


def search_videos_by_topic(api_key: str, topic: str, published_after: str, max_results: int = SEARCH_MAX_PER_TOPIC) -> list[dict]:
    """Search YouTube for videos matching a topic, published after a given date.

    Uses YouTube Search API (100 quota units per call).
    """
    videos = []
    resp = requests.get(YOUTUBE_SEARCH_URL, params={
        "part": "snippet",
        "q": topic,
        "type": "video",
        "order": "date",
        "publishedAfter": published_after,
        "maxResults": max_results,
        "key": api_key,
    }, timeout=30)

    if resp.status_code != 200:
        print(f"  Error searching topic '{topic}': HTTP {resp.status_code}", file=sys.stderr)
        return videos

    data = resp.json()
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")
        if not video_id:
            continue

        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("high", {}).get("url")
            or thumbnails.get("medium", {}).get("url")
            or thumbnails.get("default", {}).get("url")
            or ""
        )

        videos.append({
            "video_id": video_id,
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", ""),
            "thumbnail_url": thumbnail_url,
            "published_at": snippet.get("publishedAt", ""),
            "source": f"topic:{topic}",
        })

    print(f"  Topic '{topic}': {len(videos)} video(s) found", file=sys.stderr)
    return videos


def filter_by_date(videos: list[dict], cutoff: datetime) -> list[dict]:
    """Keep only videos published after the cutoff date."""
    filtered = []
    for v in videos:
        try:
            pub = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00"))
            if pub >= cutoff:
                filtered.append(v)
        except (ValueError, KeyError):
            continue
    return filtered


def deduplicate(videos: list[dict]) -> list[dict]:
    """Remove duplicate videos by video_id. Keep first occurrence (channel > topic)."""
    seen = set()
    unique = []
    for v in videos:
        vid = v["video_id"]
        if vid not in seen:
            seen.add(vid)
            unique.append(v)
    return unique


def parse_duration_seconds(iso_duration: str) -> int:
    """Parse ISO 8601 duration (PT1H2M30S) to seconds."""
    import re
    if not iso_duration:
        return 0
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def get_video_details(api_key: str, video_ids: list[str]) -> dict[str, dict]:
    """Fetch view counts and duration for a list of video IDs.
    Returns {video_id: {"view_count": int, "duration_seconds": int}}."""
    if not video_ids:
        return {}

    details = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        resp = requests.get(YOUTUBE_VIDEOS_URL, params={
            "part": "statistics,contentDetails",
            "id": ",".join(batch),
            "key": api_key,
        }, timeout=30)
        if resp.status_code != 200:
            print(f"  Error fetching video stats: {resp.status_code}", file=sys.stderr)
            continue
        for item in resp.json().get("items", []):
            view_count = int(item.get("statistics", {}).get("viewCount", 0))
            duration_iso = item.get("contentDetails", {}).get("duration", "")
            duration_seconds = parse_duration_seconds(duration_iso)
            details[item["id"]] = {
                "view_count": view_count,
                "duration_seconds": duration_seconds,
            }

    return details


def format_markdown(videos: list[dict], date_filter: str, channels_info: list[dict], topics: list[str]) -> str:
    """Format results as markdown."""
    date_label = {
        "today": "hôm nay (24h)",
        "week": "tuần này (7 ngày)",
        "month": "tháng này (30 ngày)",
    }.get(date_filter, date_filter)

    channel_names = ", ".join(ch["title"] for ch in channels_info) if channels_info else "N/A"
    topics_str = ", ".join(f'"{t}"' for t in topics) if topics else "N/A"

    lines = [
        f"# Video mới từ kênh & topics",
        f"**Kênh:** {channel_names}",
        f"**Topics:** {topics_str}",
        f"**Thời gian:** {date_label}",
        f"**Tìm thấy:** {len(videos)} video (đã khử trùng lặp)",
        f"**Cập nhật:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
    ]

    for i, video in enumerate(videos, 1):
        view_fmt = f"{video['view_count']:,}"
        pub_date = video["published_at"][:10] if video["published_at"] else "N/A"
        source = video.get("source", "")

        lines += [
            f"## {i}. {video['title']}",
            f"- **URL:** {video['url']}",
            f"- **Kênh:** {video['channel']}",
            f"- **Views:** {view_fmt}",
            f"- **Ngày đăng:** {pub_date}",
            f"- **Nguồn:** {source}",
            f"- **Thumbnail:** {video['thumbnail_url']}",
            "",
        ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch latest videos from YouTube channels and search trending topics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                          # Channels + topics, today
  %(prog)s --date week                              # Last 7 days
  %(prog)s --channels "@BenAI92,@ColeMedin"         # Custom channels
  %(prog)s --topics "claude code,ai agents"         # Custom topics
  %(prog)s --no-topics                              # Channels only
  %(prog)s --no-channels                            # Topics only
  %(prog)s --format json --output results.json      # JSON output to file
        """,
    )
    parser.add_argument(
        "--channels",
        help="Comma-separated @handles. Default: from channels.json",
    )
    parser.add_argument(
        "--topics",
        help="Comma-separated search topics. Default: from channels.json",
    )
    parser.add_argument(
        "--no-channels",
        action="store_true",
        help="Skip channel-based fetching (topics only)",
    )
    parser.add_argument(
        "--no-topics",
        action="store_true",
        help="Skip topic-based search (channels only)",
    )
    parser.add_argument(
        "--date", "-d",
        choices=["today", "week", "month"],
        default="today",
        help="Date filter: today (24h), week (7d), month (30d). Default: today",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format. Default: markdown",
    )
    parser.add_argument(
        "--output", "-o",
        help="Save results to file (.json or .md)",
    )

    args = parser.parse_args()
    api_key = load_api_key()
    config = load_config()

    # Parse channels
    if args.channels:
        handles = [h.strip() for h in args.channels.split(",") if h.strip()]
    else:
        handles = [ch["handle"] for ch in config.get("channels", [])]

    # Parse topics
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    else:
        topics = config.get("topics", [])

    all_videos = []
    channels_info = []
    active_topics = []

    # --- Flow 1: Channel-based fetch ---
    if not args.no_channels and handles:
        print(f"Resolving {len(handles)} channel(s)...", file=sys.stderr)
        channels_info = resolve_handles(api_key, handles)

        if channels_info:
            cutoff = get_date_cutoff(args.date)
            fetch_count = FETCH_COUNTS.get(args.date, 5)

            print(f"Fetching channel videos ({args.date})...", file=sys.stderr)
            for ch in channels_info:
                raw_videos = fetch_playlist_videos(api_key, ch["uploads_playlist"], fetch_count)
                filtered = filter_by_date(raw_videos, cutoff)
                print(f"  {ch['title']}: {len(filtered)} video(s) in range", file=sys.stderr)
                all_videos.extend(filtered)

    # --- Flow 2: Topic-based search ---
    if not args.no_topics and topics:
        cutoff = get_date_cutoff(args.date)
        published_after = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"Searching {len(topics)} topic(s) ({args.date})...", file=sys.stderr)
        for topic in topics:
            topic_videos = search_videos_by_topic(api_key, topic, published_after)
            all_videos.extend(topic_videos)
            active_topics.append(topic)

    if not all_videos:
        print("No videos found in the specified time range.", file=sys.stderr)
        empty = {
            "channels": [ch["title"] for ch in channels_info],
            "topics": active_topics,
            "date_filter": args.date,
            "total": 0,
            "results": [],
        }
        print(json.dumps(empty, ensure_ascii=False))
        return

    # Deduplicate (channel videos first, then topic videos)
    before_dedup = len(all_videos)
    all_videos = deduplicate(all_videos)
    dedup_count = before_dedup - len(all_videos)
    if dedup_count > 0:
        print(f"Deduplicated: removed {dedup_count} duplicate(s)", file=sys.stderr)

    # Get view counts and durations
    video_ids = [v["video_id"] for v in all_videos]
    print(f"Fetching video details for {len(video_ids)} video(s)...", file=sys.stderr)
    video_details = get_video_details(api_key, video_ids)

    # Build final results (filter out short videos: < 5 minutes)
    MIN_DURATION_SECONDS = 300
    results = []
    short_count = 0
    for v in all_videos:
        details = video_details.get(v["video_id"], {})
        duration = details.get("duration_seconds", 0)

        # Skip videos under 5 minutes
        if duration < MIN_DURATION_SECONDS:
            short_count += 1
            continue

        published_at = v["published_at"]
        video_date = published_at[:10] if published_at else ""
        results.append({
            "title": v["title"],
            "url": f"https://www.youtube.com/watch?v={v['video_id']}",
            "channel": v["channel"],
            "thumbnail_url": v["thumbnail_url"],
            "published_at": published_at,
            "video_date": video_date,
            "view_count": details.get("view_count", 0),
            "source": v.get("source", "channel"),
        })

    if short_count > 0:
        print(f"  Filtered out {short_count} video(s) shorter than 5 minutes", file=sys.stderr)

    # Sort by publish date (newest first)
    results.sort(key=lambda x: x["published_at"], reverse=True)

    print(f"Found {len(results)} video(s).", file=sys.stderr)

    # Format output
    if args.format == "json":
        output_str = json.dumps({
            "channels": [ch["title"] for ch in channels_info],
            "topics": active_topics,
            "date_filter": args.date,
            "total": len(results),
            "deduplicated": dedup_count,
            "results": results,
        }, ensure_ascii=False, indent=2)
    else:
        output_str = format_markdown(results, args.date, channels_info, active_topics)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_str, encoding="utf-8")
        print(f"Results saved to: {args.output}", file=sys.stderr)
    else:
        print(output_str)


if __name__ == "__main__":
    main()
