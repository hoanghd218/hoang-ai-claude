# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Fetch trending AI/ML repositories from GitHub."""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def get_trending_repos(
    language: str = "", since: str = "daily", topic: str = "ai", limit: int = 10
) -> dict:
    """Fetch trending repos using GitHub API via gh CLI."""
    # Calculate date range
    days = {"daily": 1, "weekly": 7, "monthly": 30}.get(since, 1)
    date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Build search query
    topic_queries = {
        "ai": "artificial-intelligence OR machine-learning OR llm OR ai-agents OR deep-learning",
        "ml": "machine-learning OR deep-learning OR neural-network",
        "llm": "llm OR large-language-model OR gpt OR claude OR chatbot",
        "agents": "ai-agents OR autonomous-agents OR agent-framework",
    }
    topic_q = topic_queries.get(topic, topic)

    query = f"({topic_q}) created:>{date_from} stars:>10"
    if language:
        query += f" language:{language}"

    # Use gh CLI for reliable API access
    cmd = [
        "gh",
        "api",
        "search/repositories",
        "-X",
        "GET",
        "-f",
        f"q={query}",
        "-f",
        "sort=stars",
        "-f",
        "order=desc",
        "-f",
        f"per_page={limit}",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Error: gh api failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        data = json.loads(result.stdout)
    except FileNotFoundError:
        print(
            "Error: gh CLI not found. Install from https://cli.github.com/",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: GitHub API request timed out", file=sys.stderr)
        sys.exit(1)

    items = []
    for repo in data.get("items", [])[:limit]:
        items.append(
            {
                "title": repo["full_name"],
                "summary": repo.get("description", "No description")
                or "No description",
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "language": repo.get("language", ""),
                "tags": repo.get("topics", [])[:5],
                "created": repo["created_at"][:10],
            }
        )

    return {
        "source": "github",
        "topic": topic,
        "since": since,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": data.get("total_count", 0),
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch trending AI repos from GitHub"
    )
    parser.add_argument(
        "--language", default="", help="Filter by language (e.g., python)"
    )
    parser.add_argument(
        "--since",
        default="daily",
        choices=["daily", "weekly", "monthly"],
        help="Time range",
    )
    parser.add_argument(
        "--topic",
        default="ai",
        choices=["ai", "ml", "llm", "agents"],
        help="Topic filter",
    )
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument(
        "--format", default="json", choices=["json", "text"], help="Output format"
    )
    args = parser.parse_args()

    result = get_trending_repos(args.language, args.since, args.topic, args.limit)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== GitHub Trending AI Repos ({result['date']}) ===\n")
        for i, item in enumerate(result["items"], 1):
            print(f"{i}. {item['stars']} stars — {item['title']}")
            print(f"   {item['summary']}")
            print(f"   {item['url']}")
            if item["tags"]:
                print(f"   Tags: {', '.join(item['tags'])}")
            print()


if __name__ == "__main__":
    main()
