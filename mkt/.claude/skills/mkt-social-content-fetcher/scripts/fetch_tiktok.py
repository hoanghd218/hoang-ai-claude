# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Fetch viral AI videos from TikTok creators using Apify."""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
APIFY_BASE = "https://api.apify.com/v2"
ACTOR_ID = "clockworks~tiktok-scraper"


def find_sources_file(sources_file: str | None) -> Path | None:
    if sources_file:
        return Path(sources_file)
    candidates = [
        Path(__file__).parent.parent / "sources.json",
        Path(".claude/skills/mkt-social-content-fetcher/sources.json"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def load_handles(sources_file: str | None, handles_arg: str | None) -> list[str]:
    if handles_arg:
        return [h.strip().lstrip("@") for h in handles_arg.split(",")]
    path = find_sources_file(sources_file)
    if path:
        data = json.loads(path.read_text())
        return [entry["handle"].lstrip("@") for entry in data.get("tiktok", [])]
    return []


def run_actor(handles: list[str], min_views: int, period: str) -> list[dict]:
    if not APIFY_TOKEN:
        print("Error: APIFY_API_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    days = {"day": 1, "week": 7, "month": 30}.get(period, 7)
    date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00.000Z")

    input_data = {
        "profiles": [f"https://www.tiktok.com/@{h}" for h in handles],
        "resultsPerPage": 20,
        "publishedAtFrom": date_from,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
    }

    headers = {"Content-Type": "application/json"}
    params = {"token": APIFY_TOKEN}

    # Start actor run
    resp = requests.post(
        f"{APIFY_BASE}/acts/{ACTOR_ID}/runs",
        headers=headers,
        params=params,
        json={"input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    run_id = resp.json()["data"]["id"]

    # Poll until finished (max 5 min)
    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(10)
        status_resp = requests.get(
            f"{APIFY_BASE}/acts/{ACTOR_ID}/runs/{run_id}",
            params=params,
            timeout=15,
        )
        status_resp.raise_for_status()
        status = status_resp.json()["data"]["status"]
        if status == "SUCCEEDED":
            break
        if status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"Error: Apify actor run {status}", file=sys.stderr)
            sys.exit(1)

    # Fetch dataset items
    dataset_resp = requests.get(
        f"{APIFY_BASE}/acts/{ACTOR_ID}/runs/{run_id}/dataset/items",
        params={**params, "format": "json", "limit": 200},
        timeout=30,
    )
    dataset_resp.raise_for_status()
    raw_items = dataset_resp.json()

    # Normalize
    items = []
    for v in raw_items:
        views = v.get("playCount", 0) or 0
        if views < min_views:
            continue
        items.append({
            "title": v.get("text", ""),
            "url": v.get("webVideoUrl", ""),
            "author": f"@{v.get('authorMeta', {}).get('name', '')}",
            "views": views,
            "likes": v.get("diggCount", 0) or 0,
            "shares": v.get("shareCount", 0) or 0,
            "comments": v.get("commentCount", 0) or 0,
            "published_at": datetime.fromtimestamp(
                v.get("createTime", 0)
            ).strftime("%Y-%m-%d") if v.get("createTime") else "",
            "tags": [t.get("name", "") for t in v.get("hashtags", [])],
            "thumbnail_url": v.get("covers", [None])[0] if v.get("covers") else "",
        })

    # Sort by views descending
    items.sort(key=lambda x: x["views"], reverse=True)
    return items


def main():
    parser = argparse.ArgumentParser(description="Fetch viral TikTok AI videos via Apify")
    parser.add_argument("--handles", help="Comma-separated TikTok handles (overrides sources.json)")
    parser.add_argument("--min-views", type=int, default=10000, help="Minimum view count")
    parser.add_argument("--period", default="week", choices=["day", "week", "month"])
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--sources-file", help="Path to sources.json")
    args = parser.parse_args()

    handles = load_handles(args.sources_file, args.handles)
    if not handles:
        print("Error: No TikTok handles found. Provide --handles or configure sources.json", file=sys.stderr)
        sys.exit(1)

    items = run_actor(handles, args.min_views, args.period)

    result = {
        "source": "tiktok",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "period": args.period,
        "handles_fetched": handles,
        "total_items": len(items),
        "items": items,
    }

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Saved {len(items)} TikTok items to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
