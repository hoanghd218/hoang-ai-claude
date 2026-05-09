#!/usr/bin/env python3
"""
Fetch top trending repositories from github.com/trending.

GitHub không có API chính thức cho trending — script này scrape HTML từ
https://github.com/trending (có filter language + since).

Output: JSON + Markdown summary.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write(
        "Missing deps. Install:\n"
        "  pip3 install requests beautifulsoup4\n"
    )
    sys.exit(1)


TRENDING_URL = "https://github.com/trending"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
}


def build_url(language: str, since: str) -> str:
    path = TRENDING_URL
    if language and language.lower() != "all":
        path = f"{TRENDING_URL}/{language.lower()}"
    return f"{path}?since={since}"


def parse_trending(html: str, limit: int) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("article.Box-row")
    repos = []

    for rank, art in enumerate(articles[:limit], start=1):
        h2 = art.select_one("h2 a")
        if not h2:
            continue
        full_name = " ".join(h2.get_text().split()).replace(" ", "")
        href = h2.get("href", "").strip()
        if "/" not in full_name:
            continue
        owner, name = full_name.split("/", 1)

        desc_el = art.select_one("p")
        description = desc_el.get_text(strip=True) if desc_el else ""

        lang_el = art.select_one("span[itemprop='programmingLanguage']")
        language = lang_el.get_text(strip=True) if lang_el else ""

        stars_today_text = ""
        for span in art.select("span.d-inline-block.float-sm-right"):
            stars_today_text = span.get_text(strip=True)
            break

        stars_today = _parse_number(stars_today_text)

        links = art.select("a.Link--muted")
        total_stars = 0
        forks = 0
        if len(links) >= 1:
            total_stars = _parse_number(links[0].get_text(strip=True))
        if len(links) >= 2:
            forks = _parse_number(links[1].get_text(strip=True))

        repos.append({
            "rank": rank,
            "owner": owner,
            "name": name,
            "full_name": f"{owner}/{name}",
            "url": f"https://github.com{href}",
            "description": description,
            "language": language,
            "stars_today": stars_today,
            "stars_today_raw": stars_today_text,
            "total_stars": total_stars,
            "forks": forks,
        })

    return repos


def _parse_number(text: str) -> int:
    if not text:
        return 0
    m = re.search(r"([\d,\.]+)\s*(k|m)?", text.lower())
    if not m:
        return 0
    num = float(m.group(1).replace(",", ""))
    suffix = m.group(2)
    if suffix == "k":
        num *= 1_000
    elif suffix == "m":
        num *= 1_000_000
    return int(num)


def to_markdown(repos: list[dict], language: str, since: str, fetched_at: str) -> str:
    lang_label = language if language and language != "all" else "All languages"
    lines = [
        f"# GitHub Trending — {lang_label} ({since})",
        "",
        f"_Fetched: {fetched_at}_",
        "",
        "| # | Repo | Language | ⭐ Today | ⭐ Total | Forks |",
        "|---|------|----------|---------|---------|-------|",
    ]
    for r in repos:
        repo_link = f"[{r['full_name']}]({r['url']})"
        lines.append(
            f"| {r['rank']} | {repo_link} | {r['language'] or '—'} | "
            f"{r['stars_today']:,} | {r['total_stars']:,} | {r['forks']:,} |"
        )

    lines.append("")
    lines.append("## Details")
    lines.append("")
    for r in repos:
        lines.append(f"### {r['rank']}. [{r['full_name']}]({r['url']})")
        if r["language"]:
            lines.append(f"- **Language**: {r['language']}")
        lines.append(
            f"- **Stars today**: {r['stars_today']:,} · "
            f"**Total**: {r['total_stars']:,} · **Forks**: {r['forks']:,}"
        )
        if r["description"]:
            lines.append(f"- **Description**: {r['description']}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub trending repos")
    parser.add_argument("--language", default="all",
                        help="Language filter (e.g. python, typescript, all)")
    parser.add_argument("--since", default="daily",
                        choices=["daily", "weekly", "monthly"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output-dir", default=None,
                        help="Output directory. Default: research/github-trend/[today]/")
    parser.add_argument("--format", default="both",
                        choices=["json", "md", "both", "stdout"])
    args = parser.parse_args()

    url = build_url(args.language, args.since)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    repos = parse_trending(resp.text, args.limit)
    if not repos:
        sys.stderr.write(f"No repos parsed from {url}\n")
        sys.exit(2)

    now = datetime.now(timezone.utc)
    fetched_at = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    today = now.strftime("%Y-%m-%d")

    if args.format == "stdout":
        print(json.dumps({
            "fetched_at": fetched_at,
            "language": args.language,
            "since": args.since,
            "source_url": url,
            "repos": repos,
        }, indent=2, ensure_ascii=False))
        return

    out_dir = Path(args.output_dir) if args.output_dir else Path(f"research/github-trend/{today}")
    out_dir.mkdir(parents=True, exist_ok=True)

    lang_slug = (args.language or "all").lower().replace(" ", "-")
    base_name = f"trending-{lang_slug}-{args.since}"

    payload = {
        "fetched_at": fetched_at,
        "language": args.language,
        "since": args.since,
        "source_url": url,
        "repos": repos,
    }

    written = []
    if args.format in ("json", "both"):
        json_path = out_dir / f"{base_name}.json"
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        written.append(str(json_path))

    if args.format in ("md", "both"):
        md_path = out_dir / f"{base_name}.md"
        md_path.write_text(to_markdown(repos, args.language, args.since, fetched_at))
        written.append(str(md_path))

    print(json.dumps({
        "status": "ok",
        "count": len(repos),
        "source_url": url,
        "written": written,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
