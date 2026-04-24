#!/usr/bin/env python3
"""Apify-based Amazon research — Python fallback when MCP is unavailable.

Primary integration for niche-hunter is the Apify MCP server (see .mcp.json).
When Claude runs the niche-hunter skill from within Claude Code, it calls the
Apify `junglee/Amazon-crawler` actor directly via MCP tools.

This script is a pure-Python fallback for:
  1. Batch/scheduled jobs (cron, GitHub Actions) where MCP is not available
  2. Debugging and local testing without Claude
  3. CI integration tests

Commands:
  search <keyword>             — top 20 organic results for a keyword
  product <ASIN>               — full product details
  bestsellers <category>       — top 100 of a category
  top10 <keyword>              — top 10 formatted for niche-hunter JSON packet
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from env_loader import env  # type: ignore

APIFY_BASE = "https://api.apify.com/v2"
DEFAULT_ACTOR = "junglee~Amazon-crawler"   # Apify uses ~ instead of / in actor IDs


def _get_token() -> str:
    token = env("APIFY_API_TOKEN")
    if not token:
        print("❌ APIFY_API_TOKEN not set in config/.env", file=sys.stderr)
        print("   Get one at https://console.apify.com/settings/integrations", file=sys.stderr)
        sys.exit(2)
    return token


def _actor_run_sync(actor_id: str, payload: dict, timeout: int = 180) -> list[dict]:
    """Run an Apify actor synchronously and return dataset items."""
    token = _get_token()
    url = f"{APIFY_BASE}/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except error.HTTPError as exc:
        print(f"❌ Apify HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(2)
    except error.URLError as exc:
        print(f"❌ Apify network error: {exc}", file=sys.stderr)
        sys.exit(2)


def search(keyword: str, marketplace: str = "com", max_items: int = 20, scrape_details: bool = False) -> list[dict]:
    """Search Amazon for a keyword, return product list."""
    payload = {
        "categoryOrProductUrls": [
            {"url": f"https://www.amazon.{marketplace}/s?k={keyword.replace(' ', '+')}"}
        ],
        "maxItemsPerStartUrl": max_items,
        "scrapeProductVariantPrices": False,
        "scrapeProductDetails": scrape_details,
        "useCaptchaSolver": False,
    }
    return _actor_run_sync(env("APIFY_DEFAULT_ACTOR", DEFAULT_ACTOR).replace("/", "~"), payload)


def product(asin: str, marketplace: str = "com") -> dict | None:
    """Get full product details for a single ASIN."""
    url = f"https://www.amazon.{marketplace}/dp/{asin}"
    payload = {
        "categoryOrProductUrls": [{"url": url}],
        "maxItemsPerStartUrl": 1,
        "scrapeProductDetails": True,
    }
    items = _actor_run_sync(env("APIFY_DEFAULT_ACTOR", DEFAULT_ACTOR).replace("/", "~"), payload)
    return items[0] if items else None


def bestsellers(category_url: str, max_items: int = 100) -> list[dict]:
    """Scrape an Amazon bestsellers category page."""
    payload = {
        "categoryOrProductUrls": [{"url": category_url}],
        "maxItemsPerStartUrl": max_items,
    }
    return _actor_run_sync(env("APIFY_DEFAULT_ACTOR", DEFAULT_ACTOR).replace("/", "~"), payload)


# ────────────────────────────────────────────────────────
# Niche-hunter integration: produce top-10 JSON packet
# ────────────────────────────────────────────────────────

def _extract_bsr(item: dict) -> int | None:
    """BSR can live under different keys depending on actor version.
    Returns the OVERALL 'Books' rank — the one that converts to daily-sales estimate.
    """
    for key in ("bestsellerRanks", "bestsellersRank", "bsr", "bestSellersRank"):
        val = item.get(key)
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            try:
                return int(val.replace(",", "").replace("#", "").strip().split()[0])
            except (ValueError, IndexError):
                pass
        if isinstance(val, list) and val:
            first = val[0]
            if isinstance(first, dict):
                rank = first.get("rank") or first.get("Rank")
                if rank:
                    try:
                        return int(str(rank).replace(",", "").replace("#", ""))
                    except ValueError:
                        pass
    return None


def _days_since(date_str: str | None) -> int | None:
    """Best-effort conversion of publication date string → days since."""
    if not date_str:
        return None
    from datetime import date, datetime

    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y"):
        try:
            dt = datetime.strptime(date_str.strip(), fmt).date()
            return (date.today() - dt).days
        except ValueError:
            continue
    return None


def _attr(item: dict, key_name: str) -> str | None:
    """Look up a key in the Apify `attributes` array (key/value pairs)."""
    for a in item.get("attributes") or []:
        if isinstance(a, dict) and a.get("key", "").strip().lower() == key_name.strip().lower():
            return a.get("value")
    return None


def _extract_pages(item: dict) -> int:
    val = item.get("printLength") or item.get("pages") or _attr(item, "Print length")
    if val is None:
        return 0
    if isinstance(val, int):
        return val
    try:
        return int(str(val).split()[0].replace(",", ""))
    except (ValueError, IndexError):
        return 0


def _extract_publisher(item: dict) -> str:
    return item.get("publisher") or _attr(item, "Publisher") or item.get("brand") or "?"


def _extract_pub_date(item: dict) -> str | None:
    return item.get("publicationDate") or _attr(item, "Publication date") or item.get("date")


def _extract_reviews(item: dict) -> int:
    """reviewsCount may be None for new books."""
    v = item.get("reviewsCount") or item.get("reviews")
    if v is None:
        return 0
    try:
        return int(v)
    except (ValueError, TypeError):
        return 0


def _extract_rating(item: dict) -> float:
    v = item.get("stars") or item.get("rating")
    if v is None:
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0


def _extract_price(item: dict) -> float:
    """Price can be dict {value, currency} or scalar."""
    for key in ("price", "priceValue", "listPrice"):
        val = item.get(key)
        if isinstance(val, dict):
            v = val.get("value") or val.get("amount")
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    continue
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            try:
                return float(val.replace("$", "").replace(",", "").strip())
            except ValueError:
                continue
    return 0.0


def top10_packet(keyword: str, marketplace: str = "com") -> dict:
    """Search and format top-10 for niche-hunter's evaluation script."""
    raw = search(keyword, marketplace=marketplace, max_items=15, scrape_details=True)
    products = raw[:10]

    packet = {
        "primary_keyword": keyword,
        "top10_asins":        [p.get("asin") for p in products],
        "top10_titles":       [p.get("title") for p in products],
        "top10_bsr":          [b for b in (_extract_bsr(p) for p in products) if b is not None],
        "top10_reviews":      [_extract_reviews(p) for p in products],
        "top10_prices":       [_extract_price(p) for p in products],
        "top10_rating":       [_extract_rating(p) for p in products],
        "top10_publishers":   [_extract_publisher(p) for p in products],
        "top10_age_days":     [
            d for d in (_days_since(_extract_pub_date(p)) for p in products)
            if d is not None
        ],
        "top10_pages":        [_extract_pages(p) for p in products],
        "sources":            [p.get("url") for p in products],
        "raw_products":       products,
    }

    # Clean up: if we got zeros (field missing), drop the null-ish entries so the
    # evaluator uses default assumptions rather than treating 0 as real data.
    for key in ("top10_reviews", "top10_prices", "top10_rating", "top10_pages"):
        vals = packet[key]
        if vals and all(v in (0, 0.0) for v in vals):
            packet[key] = []

    return packet


# ────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────

def cmd_search(args):
    items = search(args.keyword, args.marketplace, args.max)
    print(json.dumps(items, indent=2, default=str))


def cmd_product(args):
    data = product(args.asin, args.marketplace)
    print(json.dumps(data, indent=2, default=str))


def cmd_bestsellers(args):
    items = bestsellers(args.url, args.max)
    print(json.dumps(items, indent=2, default=str))


def cmd_top10(args):
    packet = top10_packet(args.keyword, args.marketplace)
    print(json.dumps(packet, indent=2, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(description="Apify-powered Amazon research")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search")
    p.add_argument("keyword")
    p.add_argument("--marketplace", default="com")
    p.add_argument("--max", type=int, default=20)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("product")
    p.add_argument("asin")
    p.add_argument("--marketplace", default="com")
    p.set_defaults(func=cmd_product)

    p = sub.add_parser("bestsellers")
    p.add_argument("url")
    p.add_argument("--max", type=int, default=100)
    p.set_defaults(func=cmd_bestsellers)

    p = sub.add_parser("top10")
    p.add_argument("keyword")
    p.add_argument("--marketplace", default="com")
    p.set_defaults(func=cmd_top10)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
