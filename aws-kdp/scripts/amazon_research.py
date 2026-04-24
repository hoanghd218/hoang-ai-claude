#!/usr/bin/env python3
"""KDP niche research toolkit.

Utility functions the niche-hunter skill uses to produce deterministic output
from WebSearch-gathered data. Claude runs the WebSearch queries; this script
crunches the numbers.

Commands:
  autocomplete-seeds <keyword>        — print list of Amazon-autocomplete probes
  evaluate <niche.json>               — full blue-ocean evaluation of a niche
  bsr <bsr_int>                       — quick BSR → daily/monthly estimate
  category-urls <slug> [--depth N]    — top-100 bestseller URLs to crawl
  compare <niche1.json> <niche2.json> — side-by-side niche comparison
  blueprint                           — print the research blueprint / worksheet
"""

from __future__ import annotations

import argparse
import json
import string
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kdp_config import (  # type: ignore
    bsr_to_daily_sales,
    estimate_monthly_royalty,
    opportunity_score,
    competition_strength,
    apply_hard_elimination,
    niche_score,
    royalty_per_sale_usd,
)


# ────────────────────────────────────────────────────────
# Amazon autocomplete probes
# ────────────────────────────────────────────────────────

def autocomplete_seeds(keyword: str) -> list[str]:
    """Generate probe strings for Amazon search autocomplete.

    Returns a list of queries to feed to WebSearch / Amazon search box.
    Harvesting Amazon's autocomplete is the single best free source of
    real-user search phrases.

    Strategy: append every letter/digit and common prefixes/suffixes.
    """
    keyword = keyword.strip().lower()
    probes = []

    # Raw + pluralized
    probes.append(keyword)
    if not keyword.endswith("s"):
        probes.append(keyword + "s")

    # keyword + space + a..z (suffix discovery)
    for c in string.ascii_lowercase:
        probes.append(f"{keyword} {c}")

    # keyword + space + digit (e.g., "coloring book 1" → series / volume signal)
    for d in "0123456789":
        probes.append(f"{keyword} {d}")

    # Prefix discovery — a..z + space + keyword (who's asking for this + qualifier)
    for c in string.ascii_lowercase:
        probes.append(f"{c} {keyword}")

    # Audience modifiers (most commercially loaded)
    for mod in (
        "for adults",
        "for kids",
        "for teens",
        "for seniors",
        "for women",
        "for men",
        "for beginners",
        "for kids ages 6-12",
        "for kids ages 4-8",
        "large print",
        "for dementia",
        "for autism",
        "for anxiety",
    ):
        probes.append(f"{keyword} {mod}")

    return probes


# ────────────────────────────────────────────────────────
# Amazon category bestseller URLs
# ────────────────────────────────────────────────────────

CATEGORY_SLUGS = {
    # coloring
    "coloring_adults": "Best-Sellers-Books-Coloring-Books-Grown-Ups/zgbs/books/4991425011",
    "coloring_kids":   "Best-Sellers-Books-Childrens-Activity-Books/zgbs/books/3191",
    "coloring_mandala":"Best-Sellers-Books-Coloring-Books-Grown-Ups/zgbs/books/4991425011",
    # low-content
    "journals":        "Best-Sellers-Books-Journal-Writing/zgbs/books/11090",
    "planners":        "Best-Sellers-Books-Calendars/zgbs/books/4736",
    "notebooks":       "Best-Sellers-Books-Journals-Diaries/zgbs/books/11090",
    # activity
    "sudoku":          "Best-Sellers-Books-Sudoku-Puzzles/zgbs/books/11058",
    "crosswords":      "Best-Sellers-Books-Crossword-Puzzles/zgbs/books/11055",
    "word_search":     "Best-Sellers-Books-Word-Search-Puzzles/zgbs/books/11059",
    "puzzles_general": "Best-Sellers-Books-Puzzles-Games/zgbs/books/11056",
    "brain_games":     "Best-Sellers-Books-Brain-Games/zgbs/books/11062",
}


def category_urls(slug: str, depth: int = 1) -> list[str]:
    """Return Amazon bestseller URLs to crawl for a given category slug.

    depth=1  → first 50 (page 1)
    depth=2  → top 100 (pages 1-2)
    """
    path = CATEGORY_SLUGS.get(slug)
    if not path:
        return []
    urls = [f"https://www.amazon.com/{path}"]
    if depth >= 2:
        urls.append(f"https://www.amazon.com/{path}?_encoding=UTF8&pg=2")
    return urls


def all_categories() -> list[str]:
    return sorted(CATEGORY_SLUGS.keys())


# ────────────────────────────────────────────────────────
# Niche evaluation — end-to-end
# ────────────────────────────────────────────────────────

def evaluate_niche(data: dict) -> dict:
    """Run full blue-ocean evaluation on a niche data packet.

    Required input fields (from WebSearch-gathered data):
      book_type: "coloring"|"low_content"|"activity"
      recommended_list_price_usd: float
      target_page_count: int
      top10_bsr: list[int]          (at least top 3, ideally 10)
      top10_reviews: list[int]
      top10_prices: list[float]
      top10_pages: list[int]        (optional — defaults assumed)
      top10_publishers: list[str]   (optional)
      top10_age_days: list[int]     (days since first listing, optional)
      top10_rating: list[float]     (optional, default 4.3)
      content_concepts_count: int
      is_seasonal: bool
      days_to_peak: int             (if seasonal)
      has_trademark_risk: bool
    """
    # ----- Hard elimination -----
    violations = apply_hard_elimination(
        {
            "top3_bsr": data.get("top10_bsr", []),
            "top10_reviews": data.get("top10_reviews", []),
            "top10_prices": data.get("top10_prices", []),
            "top10_pages": data.get("top10_pages", []),
            "top10_publishers": data.get("top10_publishers", []),
            "is_seasonal": data.get("is_seasonal", False),
            "days_to_peak": data.get("days_to_peak", 999),
            "has_trademark_risk": data.get("has_trademark_risk", False),
        }
    )

    if violations:
        return {
            "verdict": "SKIP",
            "violations": violations,
            "rating": "SKIP",
            "overall_score": 0,
            "reason": "Failed hard-elimination filter",
        }

    # ----- Demand: convert BSR to monthly royalty estimates -----
    top10_bsr = data.get("top10_bsr", [])
    list_price = data["recommended_list_price_usd"]
    page_count = data.get("target_page_count", 50)

    top10_monthly_sales_mid = []
    top10_monthly_royalty_mid = []
    for bsr in top10_bsr[:10]:
        est = estimate_monthly_royalty(bsr, list_price, page_count)
        top10_monthly_sales_mid.append(est["daily_sales_mid"] * 30)
        top10_monthly_royalty_mid.append(est["monthly_mid_usd"])

    avg_monthly_sales = (
        sum(top10_monthly_sales_mid) / len(top10_monthly_sales_mid)
        if top10_monthly_sales_mid
        else 0
    )
    avg_monthly_royalty = (
        sum(top10_monthly_royalty_mid) / len(top10_monthly_royalty_mid)
        if top10_monthly_royalty_mid
        else 0
    )

    # ----- Opportunity: sales / reviews -----
    top10_reviews = data.get("top10_reviews", [])
    avg_reviews = sum(top10_reviews) / len(top10_reviews) if top10_reviews else 0
    opp = opportunity_score(avg_monthly_sales, avg_reviews)

    # Map opportunity tier to 0-10 for scoring
    opp_map = {"BLUE_OCEAN": 10, "MODERATE": 7, "COMPETITIVE": 4, "SATURATED": 2}
    opp_0_10 = opp_map.get(opp["tier"], 5)

    # ----- Competition strength -----
    age_days = data.get("top10_age_days", [])
    avg_age = sum(age_days) / len(age_days) if age_days else 730  # default ~2 years
    ratings = data.get("top10_rating", [])
    avg_rating = sum(ratings) / len(ratings) if ratings else 4.3
    comp = competition_strength(avg_reviews, avg_age, avg_rating)

    # ----- Demand score (0-10) — based on avg monthly royalty of top-10 -----
    if avg_monthly_royalty >= 2000:
        demand_0_10 = 10
    elif avg_monthly_royalty >= 1000:
        demand_0_10 = 8
    elif avg_monthly_royalty >= 500:
        demand_0_10 = 6
    elif avg_monthly_royalty >= 200:
        demand_0_10 = 4
    else:
        demand_0_10 = 2

    # ----- Margin score (0-10) — based on recommended price -----
    if list_price >= 10.99:
        margin_0_10 = 10
    elif list_price >= 8.99:
        margin_0_10 = 8
    elif list_price >= 7.99:
        margin_0_10 = 6
    elif list_price >= 6.99:
        margin_0_10 = 4
    else:
        margin_0_10 = 2

    # ----- Content scale -----
    concepts = data.get("content_concepts_count", 0)
    if concepts >= 50:
        content_0_10 = 10
    elif concepts >= 30:
        content_0_10 = 8
    elif concepts >= 20:
        content_0_10 = 6
    elif concepts >= 10:
        content_0_10 = 4
    else:
        content_0_10 = 2

    # ----- Longevity -----
    longevity_0_10 = 5  # default "moderate"
    if data.get("is_evergreen"):
        longevity_0_10 = 10
    elif data.get("is_seasonal_recurring"):
        longevity_0_10 = 7
    elif data.get("is_trend"):
        longevity_0_10 = 3
    elif data.get("is_fad"):
        longevity_0_10 = 1

    # ----- Composite niche score -----
    score = niche_score(
        demand_0_10=demand_0_10,
        competition_strength_0_10=comp["composite_0_to_10"],
        margin_0_10=margin_0_10,
        content_scale_0_10=content_0_10,
        longevity_0_10=longevity_0_10,
        opportunity_0_10=opp_0_10,
    )

    # ----- Estimated monthly royalty for OUR new book (realistic: bottom-of-top-10) -----
    # Assume new book reaches bottom of top-10 after 60-90 days of ads
    conservative_bsr = top10_bsr[-1] if len(top10_bsr) >= 3 else (top10_bsr[0] if top10_bsr else 150_000)
    our_estimate = estimate_monthly_royalty(conservative_bsr, list_price, page_count)

    # ----- Blue-ocean flags (bonus signals) -----
    flags = []
    if opp["tier"] == "BLUE_OCEAN":
        flags.append("BLUE_OCEAN_OPPORTUNITY")
    if avg_reviews < 50:
        flags.append("LOW_REVIEW_BARRIER")
    if len(set(data.get("top10_publishers", []))) >= 8:
        flags.append("FRAGMENTED_MARKET")  # no dominant player = good
    if avg_age < 365:
        flags.append("EMERGING_MARKET")  # top-10 all < 1 year = fresh
    if avg_monthly_royalty >= 500 and avg_reviews < 100:
        flags.append("GOLDMINE")  # $$$ and easy to rank

    return {
        "verdict": score["rating"],
        "overall_score": score["overall"],
        "rating": score["rating"],
        "blue_ocean_flags": flags,
        "demand": {
            "score_0_10": demand_0_10,
            "avg_monthly_sales_top10": round(avg_monthly_sales),
            "avg_monthly_royalty_top10_usd": round(avg_monthly_royalty, 2),
        },
        "opportunity": opp,
        "competition": comp,
        "margin": {
            "score_0_10": margin_0_10,
            "list_price_usd": list_price,
            "royalty_per_sale_usd": royalty_per_sale_usd(list_price, page_count),
        },
        "content_scale": {"score_0_10": content_0_10, "concepts_count": concepts},
        "longevity": {"score_0_10": longevity_0_10},
        "our_estimated_monthly_royalty": our_estimate,
        "weights": score["weights"],
        "violations": [],
    }


# ────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────

BLUEPRINT = """\
🎯 KDP NICHE HUNTER — RESEARCH BLUEPRINT

The niche-hunter skill executes this 9-step blueprint per keyword.
Each step is a WebSearch-backed data collection, then the output is fed
into `amazon_research.py evaluate` for scoring.

STEP 1  Keyword sanity + book type detection
STEP 2  Autocomplete harvesting
          → python3 amazon_research.py autocomplete-seeds "<kw>"
          Claude runs each probe through WebSearch, collects top phrases
STEP 3  Category bestseller scan
          → python3 amazon_research.py category-urls <slug> --depth 2
STEP 4  Top-10 competitor snapshot (for the primary keyword)
          Data: BSR, reviews, price, page count, publisher, age, rating
STEP 5  "Customers also bought" expansion (from 3 bestsellers)
          → unearths adjacent niches
STEP 6  Leading-indicator scan
          Etsy + Pinterest + Google Trends + TikTok/BookTok
STEP 7  IP risk pre-scan (brand names, characters, real people)
STEP 8  Evaluate via script:
          python3 amazon_research.py evaluate <niche.json>
STEP 9  Save to DB + JSON file; suggest next command

SCORING WEIGHTS
  demand:        20%
  opportunity:   25%  ← heaviest (sales/reviews = break-in ease)
  competition:   15%  (ease, not strength)
  margin:        15%
  content_scale: 10%
  longevity:     15%

HARD ELIMINATION (applied BEFORE scoring)
  ❌ dead_market              — all top-3 BSR > 300,000
  ❌ over_saturated           — all top-10 reviews > 500
  ❌ race_to_bottom           — all top-10 priced ≤ $6.99 and ≤ 50 pages
  ❌ single_publisher_lock    — 6+ top-10 from same publisher
  ❌ seasonal_missed_window   — peak is < 75 days away
  ❌ ip_trap                  — trademark/character/brand name detected

BLUE-OCEAN FLAGS (bonus signals, surfaced in final report)
  🌊 BLUE_OCEAN_OPPORTUNITY   — opportunity score ≥ 5
  🌊 LOW_REVIEW_BARRIER       — avg top-10 reviews < 50
  🌊 FRAGMENTED_MARKET        — no publisher owns > 2 of top-10
  🌊 EMERGING_MARKET          — all top-10 listed within last 12 months
  💰 GOLDMINE                 — top-10 avg royalty > $500/mo AND reviews < 100
"""


def cmd_autocomplete_seeds(args):
    seeds = autocomplete_seeds(args.keyword)
    if args.json:
        print(json.dumps(seeds, indent=2))
    else:
        for s in seeds:
            print(s)


def cmd_evaluate(args):
    data = json.loads(Path(args.path).read_text())
    result = evaluate_niche(data)
    print(json.dumps(result, indent=2))


def cmd_bsr(args):
    bsr = int(args.bsr)
    sales = bsr_to_daily_sales(bsr)
    royalty = estimate_monthly_royalty(bsr, args.price, args.pages)
    print(json.dumps({"daily_sales": sales, "monthly_royalty": royalty}, indent=2))


def cmd_category_urls(args):
    urls = category_urls(args.slug, args.depth)
    if not urls:
        print(f"Unknown category slug. Available: {', '.join(all_categories())}", file=sys.stderr)
        sys.exit(2)
    for u in urls:
        print(u)


def cmd_compare(args):
    out = []
    for p in args.paths:
        data = json.loads(Path(p).read_text())
        ev = evaluate_niche(data)
        out.append({
            "file": p,
            "niche": data.get("niche_name", Path(p).stem),
            "rating": ev["rating"],
            "score": ev["overall_score"],
            "flags": ev.get("blue_ocean_flags", []),
            "our_monthly_mid_usd": ev.get("our_estimated_monthly_royalty", {}).get("monthly_mid_usd"),
            "opportunity": ev.get("opportunity", {}).get("opportunity"),
        })
    out.sort(key=lambda r: -(r.get("score") or 0))
    print(f"{'Niche':<40} {'Rating':<6} {'Score':>6} {'Opp':>6} {'$/mo mid':>10}  Flags")
    for r in out:
        name = (r["niche"] or "")[:40]
        flags = ",".join(r["flags"])[:40]
        print(
            f"{name:<40} {r['rating']:<6} {r['score']:>6} "
            f"{(r['opportunity'] or 0):>6} ${(r['our_monthly_mid_usd'] or 0):>9,.0f}  {flags}"
        )


def cmd_blueprint(_args):
    print(BLUEPRINT)


def main() -> int:
    parser = argparse.ArgumentParser(description="KDP niche research toolkit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("autocomplete-seeds")
    p.add_argument("keyword")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_autocomplete_seeds)

    p = sub.add_parser("evaluate")
    p.add_argument("path")
    p.set_defaults(func=cmd_evaluate)

    p = sub.add_parser("bsr")
    p.add_argument("bsr", type=int)
    p.add_argument("--price", type=float, default=8.99)
    p.add_argument("--pages", type=int, default=50)
    p.set_defaults(func=cmd_bsr)

    p = sub.add_parser("category-urls")
    p.add_argument("slug")
    p.add_argument("--depth", type=int, default=1)
    p.set_defaults(func=cmd_category_urls)

    p = sub.add_parser("compare")
    p.add_argument("paths", nargs="+")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("blueprint")
    p.set_defaults(func=cmd_blueprint)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
