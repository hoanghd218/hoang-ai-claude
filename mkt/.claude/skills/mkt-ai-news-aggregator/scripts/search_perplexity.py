# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Search AI news using Perplexity Sonar via OpenRouter API."""

import argparse
import json
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "perplexity/sonar-pro"


def search_perplexity(query: str, period: str = "24h", model: str = DEFAULT_MODEL) -> dict:
    """Search for AI news using Perplexity Sonar via OpenRouter."""
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY not set in .env", file=sys.stderr)
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
                "You are an AI news researcher. Return results as a JSON array. "
                "Each item must have: title, summary (2-3 sentences), url, tags (array of keywords). "
                "Focus on: new AI models, AI tools, AI agent frameworks, automation tools, "
                "coding AI, business AI applications. Return ONLY valid JSON array, no markdown."
            ),
        },
        {
            "role": "user",
            "content": f"What are the most important AI news and announcements {time_filter}? "
            f"Focus on: {query}. Return top 10 items as JSON array.",
        },
    ]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 4000,
        "temperature": 0.1,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    # Try to parse JSON from response
    try:
        # Handle markdown code blocks
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        items = json.loads(content.strip())
    except json.JSONDecodeError:
        items = [{"title": "Raw response", "summary": content, "url": "", "tags": []}]

    citations = data.get("citations", [])

    return {
        "source": "perplexity",
        "query": query,
        "period": period,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "items": items,
        "citations": citations,
    }


def main():
    parser = argparse.ArgumentParser(description="Search AI news via Perplexity")
    parser.add_argument("--query", default="AI news", help="Search query")
    parser.add_argument(
        "--period", default="24h", choices=["24h", "week", "month"], help="Time period"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help="OpenRouter model ID (default: perplexity/sonar-pro)"
    )
    parser.add_argument(
        "--format", default="json", choices=["json", "text"], help="Output format"
    )
    args = parser.parse_args()

    result = search_perplexity(args.query, args.period, args.model)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== Perplexity AI News ({result['date']}) ===\n")
        for i, item in enumerate(result.get("items", []), 1):
            title = item.get("title", "Untitled")
            summary = item.get("summary", "")
            url = item.get("url", "")
            tags = ", ".join(item.get("tags", []))
            print(f"{i}. {title}")
            print(f"   {summary}")
            if url:
                print(f"   URL: {url}")
            if tags:
                print(f"   Tags: {tags}")
            print()


if __name__ == "__main__":
    main()
