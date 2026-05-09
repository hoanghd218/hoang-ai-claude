# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Search trending AI posts on X.com using xAI Grok API."""

import argparse
import json
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("XAI_API_KEY")
API_URL = "https://api.x.ai/v1/chat/completions"


def search_x_posts(
    topic: str = "AI", period: str = "24h", limit: int = 10
) -> dict:
    """Search for trending AI posts on X.com using Grok."""
    if not API_KEY:
        print("Error: XAI_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    time_filter = {
        "24h": "in the last 24 hours",
        "week": "in the last 7 days",
        "month": "in the last 30 days",
    }.get(period, "in the last 24 hours")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a social media researcher. Search X.com (Twitter) for the most discussed "
                "posts about the given topic. Return results as a JSON array. "
                "Each item must have: author (X handle), summary (what the post says, 2-3 sentences), "
                "url (if available), engagement (high/medium/low), tags (array of keywords). "
                "Return ONLY valid JSON array, no markdown."
            ),
        },
        {
            "role": "user",
            "content": f"Find the top {limit} most discussed posts about {topic} on X.com {time_filter}. "
            "Focus on: new AI tools, AI models, AI agent frameworks, coding with AI, AI business applications. "
            "Return as JSON array.",
        },
    ]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-3",
        "messages": messages,
        "max_tokens": 4000,
        "temperature": 0.1,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    try:
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        items = json.loads(content.strip())
    except json.JSONDecodeError:
        items = [
            {
                "author": "unknown",
                "summary": content,
                "url": "",
                "engagement": "unknown",
                "tags": [],
            }
        ]

    return {
        "source": "xcom",
        "topic": topic,
        "period": period,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Search trending AI posts on X.com"
    )
    parser.add_argument("--topic", default="AI", help="Topic to search")
    parser.add_argument(
        "--period",
        default="24h",
        choices=["24h", "week", "month"],
        help="Time period",
    )
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument(
        "--format", default="json", choices=["json", "text"], help="Output format"
    )
    args = parser.parse_args()

    result = search_x_posts(args.topic, args.period, args.limit)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== X.com Trending AI Posts ({result['date']}) ===\n")
        for i, item in enumerate(result.get("items", []), 1):
            author = item.get("author", "unknown")
            summary = item.get("summary", "")
            engagement = item.get("engagement", "")
            print(f"{i}. @{author} [{engagement}]")
            print(f"   {summary}")
            if item.get("url"):
                print(f"   {item['url']}")
            print()


if __name__ == "__main__":
    main()
