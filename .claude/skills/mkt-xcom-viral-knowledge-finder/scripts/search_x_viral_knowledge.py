# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Search viral knowledge-sharing X.com posts about Claude.ai / AI topics via Grok on OpenRouter."""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "x-ai/grok-4-fast"

SYSTEM_PROMPT = (
    "You are a research analyst specialized in finding KNOWLEDGE-SHARING posts on X.com (Twitter). "
    "Your job is to surface viral posts that teach something — threads, tips, frameworks, tutorials, "
    "workflows, prompt templates, comparisons with analysis, case studies with concrete learnings.\n\n"
    "EXCLUDE strictly: pure news announcements ('X launched Y'), memes, shitposts, hype without substance, "
    "ads, affiliate spam, single-line opinion tweets, pure hot-takes.\n\n"
    "INCLUDE: posts where a reader walks away having LEARNED something actionable.\n\n"
    "Return ONLY a valid JSON array (no markdown fences, no prose). Each item must have exactly these fields: "
    "rank (int), author (X handle with @), post_type ('thread'|'single'|'quote'), "
    "title_or_hook (string — the opening line), summary (3-5 sentence summary of the knowledge shared), "
    "key_takeaways (array of 2-5 short actionable bullets), knowledge_value (int 1-10, how useful is the knowledge), "
    "virality_signal ('high'|'medium'|'low'), url (string, '' if unknown), "
    "tags (array of lowercase keywords)."
)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:40] or "topic"


def extract_json_array(content: str):
    """Robustly extract JSON array from LLM response."""
    content = content.strip()

    if "```" in content:
        parts = content.split("```")
        for part in parts:
            stripped = part.strip()
            if stripped.startswith("json"):
                stripped = stripped[4:].strip()
            if stripped.startswith("["):
                try:
                    return json.loads(stripped)
                except json.JSONDecodeError:
                    continue

    start = content.find("[")
    end = content.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(content[start : end + 1])
        except json.JSONDecodeError:
            pass

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def search_grok(topic: str, period: str, limit: int, model: str) -> dict:
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    time_filter = {
        "24h": "in the last 24 hours",
        "week": "in the last 7 days",
        "month": "in the last 30 days",
    }.get(period, "in the last 7 days")

    user_prompt = (
        f"Find the top {limit} VIRAL KNOWLEDGE-SHARING posts on X.com about '{topic}' {time_filter}.\n\n"
        "Focus on posts that teach something concrete — prompt engineering tips, agent architectures, "
        "Claude Code / Claude.ai workflows, AI tool reviews with analysis, coding with AI, building "
        "AI products, automation frameworks. Prefer THREADS with depth over single hot-takes.\n\n"
        "Rank by combination of knowledge_value (priority) and virality_signal. Ensure diversity — "
        "avoid more than 2 posts from the same author. Return ONLY the JSON array."
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Hoang218/hoang-ai-marketing",
        "X-Title": "mkt-xcom-viral-knowledge-finder",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 6000,
        "temperature": 0.2,
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=90)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    items = extract_json_array(content)
    if items is None:
        items = [
            {
                "rank": 1,
                "author": "@unknown",
                "post_type": "single",
                "title_or_hook": "Raw response (JSON parse failed)",
                "summary": content[:800],
                "key_takeaways": [],
                "knowledge_value": 0,
                "virality_signal": "low",
                "url": "",
                "tags": [],
            }
        ]

    for i, it in enumerate(items, 1):
        it.setdefault("rank", i)

    return {
        "source": "xcom-via-grok-openrouter",
        "topic": topic,
        "period": period,
        "model": model,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "fetched_at": datetime.now().isoformat(),
        "count": len(items),
        "items": items,
    }


def render_markdown(result: dict) -> str:
    lines = [
        f"# X.com Viral Knowledge — {result['topic']} ({result['period']})",
        "",
        f"_Fetched: {result['fetched_at']}_ · model `{result['model']}`",
        "",
        "| # | Author | Type | Knowledge | Virality | Hook |",
        "|---|--------|------|-----------|----------|------|",
    ]
    for it in result["items"]:
        hook = str(it.get("title_or_hook", "")).replace("|", "\\|")[:80]
        lines.append(
            f"| {it.get('rank','')} | {it.get('author','')} | {it.get('post_type','')} | "
            f"{it.get('knowledge_value','')}/10 | {it.get('virality_signal','')} | {hook} |"
        )

    lines += ["", "## Details", ""]
    for it in result["items"]:
        lines.append(f"### {it.get('rank','')}. {it.get('author','')} — {it.get('title_or_hook','')}")
        lines.append(f"- **Type**: {it.get('post_type','')} · **Knowledge**: {it.get('knowledge_value','')}/10 · **Virality**: {it.get('virality_signal','')}")
        if it.get("url"):
            lines.append(f"- **URL**: {it['url']}")
        if it.get("tags"):
            lines.append(f"- **Tags**: {', '.join(it['tags'])}")
        lines.append("")
        lines.append(f"**Summary:** {it.get('summary','')}")
        lines.append("")
        takeaways = it.get("key_takeaways") or []
        if takeaways:
            lines.append("**Key takeaways:**")
            for t in takeaways:
                lines.append(f"- {t}")
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Find viral knowledge-sharing X.com posts via Grok on OpenRouter."
    )
    parser.add_argument("--topic", default="Claude.ai", help="Topic to search")
    parser.add_argument(
        "--period", default="week", choices=["24h", "week", "month"], help="Time window"
    )
    parser.add_argument("--limit", type=int, default=10, help="Max posts")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter model ID")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output dir (default: research/x-viral-knowledge/[YYYY-MM-DD])",
    )
    parser.add_argument(
        "--format", default="json", choices=["json", "text"], help="Stdout format"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Do not write files, only stdout"
    )
    args = parser.parse_args()

    result = search_grok(args.topic, args.period, args.limit, args.model)

    written = []
    if not args.no_save:
        date_str = result["date"]
        out_dir = Path(args.output_dir) if args.output_dir else Path("research/x-viral-knowledge") / date_str
        out_dir.mkdir(parents=True, exist_ok=True)

        slug = slugify(args.topic)
        json_path = out_dir / f"viral-knowledge-{slug}-{args.period}.json"
        md_path = out_dir / f"viral-knowledge-{slug}-{args.period}.md"

        json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(render_markdown(result), encoding="utf-8")
        written = [str(json_path), str(md_path)]

    if args.format == "json":
        summary = {
            "status": "ok",
            "count": result["count"],
            "topic": result["topic"],
            "period": result["period"],
            "model": result["model"],
            "written": written,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"=== X.com Viral Knowledge — {result['topic']} ({result['period']}) ===\n")
        for it in result["items"]:
            print(f"{it.get('rank','')}. {it.get('author','')} "
                  f"[K={it.get('knowledge_value','?')}/10 V={it.get('virality_signal','?')}] "
                  f"— {it.get('title_or_hook','')}")
            print(f"   {it.get('summary','')}")
            for t in (it.get("key_takeaways") or []):
                print(f"   • {t}")
            if it.get("url"):
                print(f"   {it['url']}")
            print()
        if written:
            print(f"Saved: {', '.join(written)}")


if __name__ == "__main__":
    main()
