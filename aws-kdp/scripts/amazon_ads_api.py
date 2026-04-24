#!/usr/bin/env python3
"""Amazon Ads API wrapper for KDP OS — stub.

Real integration requires Amazon Advertising API OAuth flow and scope approval.
This stub does two things out of the box:

1. `bulk-export` — generate a CSV ready to upload via advertising.amazon.com →
   Bulk operations. Uses the official bulk sheet schema (Record Type, Campaign,
   Ad Group, Keyword, Match Type, Bid, State, …).
2. `report` — if ads-API credentials are present in config/.env, fetch recent
   performance data; otherwise print a helpful placeholder.

Extend this file when credentials are wired up. Helpers from `env_loader` and
`db.py` are imported lazily so the CLI works even before dependencies exist.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

BULK_HEADERS = [
    "Product",
    "Entity",
    "Operation",
    "Campaign Id",
    "Ad Group Id",
    "Portfolio Id",
    "Ad Id",
    "Keyword Id",
    "Product Targeting Id",
    "Campaign Name",
    "Ad Group Name",
    "Start Date",
    "End Date",
    "Targeting Type",
    "State",
    "Daily Budget",
    "SKU",
    "ASIN",
    "Ad Group Default Bid",
    "Bid",
    "Keyword Text",
    "Match Type",
    "Bidding Strategy",
    "Placement",
    "Percentage",
    "Product Targeting Expression",
]


def build_launch_plan(
    asin: str, title: str, keywords_tier1: list[str], keywords_tier2: list[str],
    default_bid: float, daily_budget_auto: float = 5.0,
    daily_budget_exact: float = 10.0, daily_budget_phrase: float = 5.0,
) -> list[dict]:
    """Return a list of bulk-sheet rows implementing the launch playbook."""
    plan: list[dict] = []
    campaigns = [
        ("Launch Auto — " + title[:40], "auto", daily_budget_auto, default_bid * 0.9),
        ("Launch Exact — " + title[:40], "manual", daily_budget_exact, default_bid),
        ("Launch Phrase — " + title[:40], "manual", daily_budget_phrase, default_bid * 0.9),
    ]
    for camp_name, camp_type, budget, bid in campaigns:
        plan.append({
            "Product": "Sponsored Products",
            "Entity": "Campaign",
            "Operation": "Create",
            "Campaign Name": camp_name,
            "Start Date": "",
            "Targeting Type": "Auto" if camp_type == "auto" else "Manual",
            "State": "enabled",
            "Daily Budget": f"{budget:.2f}",
            "Bidding Strategy": "Dynamic bids - down only",
        })
        plan.append({
            "Product": "Sponsored Products",
            "Entity": "Ad Group",
            "Operation": "Create",
            "Campaign Name": camp_name,
            "Ad Group Name": "AG1",
            "State": "enabled",
            "Ad Group Default Bid": f"{bid:.2f}",
        })
        plan.append({
            "Product": "Sponsored Products",
            "Entity": "Product Ad",
            "Operation": "Create",
            "Campaign Name": camp_name,
            "Ad Group Name": "AG1",
            "State": "enabled",
            "ASIN": asin,
        })

        if camp_type == "auto":
            continue

        kws = keywords_tier1 if "Exact" in camp_name else keywords_tier2
        match = "exact" if "Exact" in camp_name else "phrase"
        for kw in kws:
            plan.append({
                "Product": "Sponsored Products",
                "Entity": "Keyword",
                "Operation": "Create",
                "Campaign Name": camp_name,
                "Ad Group Name": "AG1",
                "State": "enabled",
                "Bid": f"{bid:.2f}",
                "Keyword Text": kw,
                "Match Type": match,
            })

    # default negatives
    for neg in ("free", "download", "pdf", "kindle"):
        for camp_name, *_ in campaigns:
            plan.append({
                "Product": "Sponsored Products",
                "Entity": "Campaign Negative Keyword",
                "Operation": "Create",
                "Campaign Name": camp_name,
                "State": "enabled",
                "Keyword Text": neg,
                "Match Type": "negativeExact",
            })

    return plan


def write_bulk_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=BULK_HEADERS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def cmd_bulk_export(args) -> int:
    keywords_tier1 = json.loads(args.keywords_exact) if args.keywords_exact else []
    keywords_tier2 = json.loads(args.keywords_phrase) if args.keywords_phrase else []
    plan = build_launch_plan(
        asin=args.asin,
        title=args.title,
        keywords_tier1=keywords_tier1,
        keywords_tier2=keywords_tier2,
        default_bid=args.bid,
        daily_budget_auto=args.budget_auto,
        daily_budget_exact=args.budget_exact,
        daily_budget_phrase=args.budget_phrase,
    )
    out = Path(args.out)
    write_bulk_csv(plan, out)
    print(f"✅ Wrote {len(plan)} bulk-sheet rows to {out}")
    print("   Upload at advertising.amazon.com → Bulk operations")
    return 0


def cmd_report(args) -> int:
    try:
        from env_loader import env  # type: ignore
    except Exception:
        sys.path.insert(0, str(HERE))
        from env_loader import env  # type: ignore

    if not env("ADS_API_CLIENT_ID"):
        print("ℹ Ads API not configured in config/.env — nothing to fetch.")
        print("   Fill ADS_API_* credentials to enable automated reports.")
        return 0
    print("TODO: implement Amazon Ads API OAuth + report pull.")
    print("   Currently a stub. See github.com/amzn/ads-advanced-tools-docs for reference.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bulk-export", help="Generate Amazon Ads bulk-upload CSV for a launch")
    b.add_argument("--asin", required=True)
    b.add_argument("--title", required=True)
    b.add_argument("--bid", type=float, default=0.10)
    b.add_argument("--budget-auto", type=float, default=5.0)
    b.add_argument("--budget-exact", type=float, default=10.0)
    b.add_argument("--budget-phrase", type=float, default=5.0)
    b.add_argument("--keywords-exact", help="JSON array of exact-match keywords")
    b.add_argument("--keywords-phrase", help="JSON array of phrase-match keywords")
    b.add_argument("--out", required=True)

    r = sub.add_parser("report", help="Fetch recent ads performance (requires credentials)")
    r.add_argument("--days", type=int, default=7)
    r.add_argument("--all", action="store_true")
    r.add_argument("--book-id", type=int)

    args = parser.parse_args()

    if args.cmd == "bulk-export":
        return cmd_bulk_export(args)
    if args.cmd == "report":
        return cmd_report(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
