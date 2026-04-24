#!/usr/bin/env python3
"""KDP OS — SQLite database CLI.

Single source of truth for all 8 agents. Each agent reads/writes via this CLI.

Usage:
  python3 db.py init
  python3 db.py dashboard
  python3 db.py niches create '{"niche_name": "...", ...}'
  python3 db.py niches list [--rating HOT] [--status APPROVED]
  python3 db.py niches get <id>
  python3 db.py books create '{...}'
  python3 db.py books list [--status LIVE]
  python3 db.py books get <id>
  python3 db.py books update <id> '{...}'
  python3 db.py manuscripts create '{...}'
  python3 db.py covers create '{...}'
  python3 db.py listings create '{...}'
  python3 db.py qa_reports create '{...}'
  python3 db.py ad_campaigns create '{...}'
  python3 db.py royalties ingest --file <csv_path>
  python3 db.py royalties summary --month YYYY-MM
  python3 db.py actions bulk-create '[{...}, {...}]'
  python3 db.py pipelines create '{...}'
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DB_PATH = HERE.parent / "data" / "kdp.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS niches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    niche_name TEXT NOT NULL,
    book_type TEXT NOT NULL CHECK(book_type IN ('coloring','low_content','activity')),
    primary_keyword TEXT,
    secondary_keywords TEXT,    -- JSON array
    long_tail_keywords TEXT,    -- JSON array
    audience TEXT,              -- adults_cozy, kids_6_12, seniors_large_print, etc.
    page_size TEXT DEFAULT '8.5x11',
    target_page_count INTEGER DEFAULT 50,
    score_demand REAL,
    score_competition REAL,
    score_margin REAL,
    score_content_scale REAL,
    score_longevity REAL,
    overall_score REAL,
    rating TEXT CHECK(rating IN ('HOT','WARM','COLD','SKIP')),
    competitor_analysis TEXT,   -- JSON
    content_concepts_count INTEGER,
    content_concepts_sample TEXT,  -- JSON array
    ip_risk_notes TEXT,
    seasonal_relevance TEXT,
    estimated_monthly_royalty_usd TEXT,
    recommended_list_price_usd REAL,
    status TEXT DEFAULT 'PENDING_IP_CHECK',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    niche_id INTEGER REFERENCES niches(id),
    book_type TEXT NOT NULL,
    theme_key TEXT UNIQUE NOT NULL,
    title TEXT,
    subtitle TEXT,
    author TEXT,
    page_size TEXT,
    target_page_count INTEGER,
    actual_page_count INTEGER,
    list_price_usd REAL,
    asin TEXT,
    kdp_title_id TEXT,
    status TEXT DEFAULT 'PLANNING',
    -- PLANNING, MANUSCRIPT_READY, COVER_READY, LISTING_READY,
    -- READY_TO_PUBLISH, LIVE, RETIRED, BLOCKED
    published_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS manuscripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    page_count INTEGER,
    file_path TEXT,
    plan_json_path TEXT,
    build_log TEXT,
    status TEXT DEFAULT 'DRAFT',   -- DRAFT, READY, BLOCKED
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS covers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    trim_size TEXT,
    page_count INTEGER,
    spine_width_in REAL,
    full_width_in REAL,
    full_height_in REAL,
    bleed_in REAL DEFAULT 0.125,
    file_path_pdf TEXT,
    file_path_png_preview TEXT,
    front_art_path TEXT,
    status TEXT DEFAULT 'DIMENSIONS_READY',   -- DIMENSIONS_READY, ART_READY, READY, BLOCKED
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    title TEXT,
    subtitle TEXT,
    description_html TEXT,
    description_plain TEXT,
    keywords TEXT,                      -- JSON array of 7
    primary_category_bisac TEXT,
    secondary_category_bisac TEXT,
    requested_extra_categories TEXT,    -- JSON array
    list_price_usd REAL,
    a_plus_modules TEXT,                -- JSON
    status TEXT DEFAULT 'DRAFT',        -- DRAFT, READY, LIVE
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS qa_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    verdict TEXT CHECK(verdict IN ('GO','NO_GO')),
    critical_issues TEXT,   -- JSON array
    warnings TEXT,          -- JSON array
    notes TEXT,             -- JSON array
    reviewed_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ad_campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    campaign_name TEXT,
    campaign_type TEXT,         -- auto, exact, phrase, category
    amazon_campaign_id TEXT,
    budget_daily_usd REAL,
    default_bid_usd REAL,
    target_acos_pct REAL,
    target_cpc_usd REAL,
    keywords TEXT,              -- JSON array
    negative_keywords TEXT,     -- JSON array
    harvested_keywords TEXT,    -- JSON array
    status TEXT DEFAULT 'DRAFT',
    launched_at TEXT,
    iterated_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS royalties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER REFERENCES books(id),
    asin TEXT,
    date TEXT NOT NULL,
    marketplace TEXT DEFAULT 'US',
    units_sold INTEGER DEFAULT 0,
    kenp_reads INTEGER DEFAULT 0,
    royalty_net_usd REAL DEFAULT 0,
    returns INTEGER DEFAULT 0,
    UNIQUE(asin, date, marketplace)
);

CREATE TABLE IF NOT EXISTS ad_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER REFERENCES books(id),
    campaign_id INTEGER REFERENCES ad_campaigns(id),
    date TEXT NOT NULL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    spend_usd REAL DEFAULT 0,
    sales_usd REAL DEFAULT 0,
    orders INTEGER DEFAULT 0,
    acos_pct REAL,
    ctr_pct REAL,
    cvr_pct REAL,
    UNIQUE(campaign_id, date)
);

CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER REFERENCES books(id),
    action_type TEXT,          -- SCALE_ADS, FIX_LISTING, FIX_COVER, KILL, EXPAND_SERIES, SEASONAL_RAMP, REVIEW_VELOCITY
    priority INTEGER,
    expected_impact_usd REAL,
    command TEXT,
    reason TEXT,
    status TEXT DEFAULT 'PENDING',   -- PENDING, APPROVED, DONE, SKIPPED
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS pipelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_type TEXT,        -- launch, daily, weekly, optimize, scale, kill, seasonal
    niche_id INTEGER REFERENCES niches(id),
    book_id INTEGER REFERENCES books(id),
    current_step INTEGER DEFAULT 1,
    total_steps INTEGER,
    status TEXT DEFAULT 'RUNNING',  -- RUNNING, PAUSED, COMPLETE, FAILED
    step_log TEXT,                   -- JSON array of step events
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_books_status ON books(status);
CREATE INDEX IF NOT EXISTS idx_books_niche ON books(niche_id);
CREATE INDEX IF NOT EXISTS idx_royalties_date ON royalties(date);
CREATE INDEX IF NOT EXISTS idx_royalties_book ON royalties(book_id);
CREATE INDEX IF NOT EXISTS idx_ad_perf_date ON ad_performance(date);
CREATE INDEX IF NOT EXISTS idx_actions_status ON actions(status);
CREATE INDEX IF NOT EXISTS idx_pipelines_status ON pipelines(status);
"""


JSON_FIELDS = {
    "niches": {
        "secondary_keywords",
        "long_tail_keywords",
        "competitor_analysis",
        "content_concepts_sample",
    },
    "listings": {"keywords", "requested_extra_categories", "a_plus_modules"},
    "qa_reports": {"critical_issues", "warnings", "notes"},
    "ad_campaigns": {"keywords", "negative_keywords", "harvested_keywords"},
    "pipelines": {"step_log"},
}


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    print(f"✅ KDP OS database initialized at {DB_PATH}")
    print(f"   Tables: niches, books, manuscripts, covers, listings, qa_reports,")
    print(f"           ad_campaigns, royalties, ad_performance, actions, pipelines")


def _prep_row(table: str, payload: dict) -> dict:
    json_fields = JSON_FIELDS.get(table, set())
    out = {}
    for k, v in payload.items():
        if v is None:
            out[k] = None
        elif k in json_fields and not isinstance(v, str):
            out[k] = json.dumps(v, ensure_ascii=False)
        elif isinstance(v, (dict, list)):
            out[k] = json.dumps(v, ensure_ascii=False)
        else:
            out[k] = v
    return out


def _row_to_dict(row: sqlite3.Row, table: str) -> dict:
    data = dict(row)
    json_fields = JSON_FIELDS.get(table, set())
    for k, v in data.items():
        if k in json_fields and isinstance(v, str) and v:
            try:
                data[k] = json.loads(v)
            except json.JSONDecodeError:
                pass
    return data


def create(table: str, payload: dict) -> int:
    payload = _prep_row(table, payload)
    cols = ", ".join(payload.keys())
    placeholders = ", ".join("?" for _ in payload)
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    conn = get_conn()
    cur = conn.execute(sql, tuple(payload.values()))
    conn.commit()
    return cur.lastrowid


def update(table: str, row_id: int, payload: dict) -> None:
    payload = _prep_row(table, payload)
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    sets = ", ".join(f"{k} = ?" for k in payload)
    sql = f"UPDATE {table} SET {sets} WHERE id = ?"
    conn = get_conn()
    conn.execute(sql, (*payload.values(), row_id))
    conn.commit()


def get(table: str, row_id: int) -> dict | None:
    conn = get_conn()
    row = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()
    return _row_to_dict(row, table) if row else None


def list_rows(table: str, filters: dict | None = None, limit: int = 100) -> list[dict]:
    conn = get_conn()
    where = ""
    params: list[Any] = []
    if filters:
        parts = []
        for k, v in filters.items():
            parts.append(f"{k} = ?")
            params.append(v)
        where = " WHERE " + " AND ".join(parts)
    sql = f"SELECT * FROM {table}{where} ORDER BY id DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, tuple(params)).fetchall()
    return [_row_to_dict(r, table) for r in rows]


def get_by(table: str, field: str, value: Any) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        f"SELECT * FROM {table} WHERE {field} = ? ORDER BY id DESC LIMIT 1", (value,)
    ).fetchone()
    return _row_to_dict(row, table) if row else None


def dashboard() -> None:
    conn = get_conn()
    niches_total = conn.execute("SELECT COUNT(*) FROM niches").fetchone()[0]
    niches_hot = conn.execute("SELECT COUNT(*) FROM niches WHERE rating='HOT'").fetchone()[0]
    niches_warm = conn.execute("SELECT COUNT(*) FROM niches WHERE rating='WARM'").fetchone()[0]
    books_live = conn.execute("SELECT COUNT(*) FROM books WHERE status='LIVE'").fetchone()[0]
    books_in_prod = conn.execute(
        "SELECT COUNT(*) FROM books WHERE status NOT IN ('LIVE','RETIRED','BLOCKED')"
    ).fetchone()[0]
    books_retired = conn.execute("SELECT COUNT(*) FROM books WHERE status='RETIRED'").fetchone()[0]

    royalty_7d = (
        conn.execute(
            "SELECT COALESCE(SUM(royalty_net_usd), 0) FROM royalties "
            "WHERE date >= date('now', '-7 days')"
        ).fetchone()[0]
        or 0
    )
    units_7d = (
        conn.execute(
            "SELECT COALESCE(SUM(units_sold), 0) FROM royalties "
            "WHERE date >= date('now', '-7 days')"
        ).fetchone()[0]
        or 0
    )
    ad_spend_7d = (
        conn.execute(
            "SELECT COALESCE(SUM(spend_usd), 0) FROM ad_performance "
            "WHERE date >= date('now', '-7 days')"
        ).fetchone()[0]
        or 0
    )

    pending_actions = conn.execute(
        "SELECT COUNT(*) FROM actions WHERE status='PENDING'"
    ).fetchone()[0]
    running_pipelines = conn.execute(
        "SELECT COUNT(*) FROM pipelines WHERE status='RUNNING'"
    ).fetchone()[0]

    print("🏢 KDP OS — COMPANY DASHBOARD")
    print(f"   {datetime.now().strftime('%Y-%m-%d %A')}")
    print()
    print("PORTFOLIO")
    print(f"  Niches researched:        {niches_total}   (HOT {niches_hot}, WARM {niches_warm})")
    print(f"  Books in production:      {books_in_prod}")
    print(f"  Books LIVE:               {books_live}")
    print(f"  Books retired:            {books_retired}")
    print()
    print("PAST 7 DAYS")
    print(f"  Units sold:               {units_7d}")
    print(f"  Royalty:                  ${royalty_7d:,.2f}")
    print(f"  Ad spend:                 ${ad_spend_7d:,.2f}")
    print()
    print(f"Pending actions: {pending_actions}")
    print(f"Running pipelines: {running_pipelines}")
    print()
    if niches_total == 0:
        print("👉 Start here: /niche-hunter [topic]")
    elif books_live == 0:
        print("👉 Next: /master-orchestrator launch [niche_id]")
    else:
        print("👉 Next: /master-orchestrator weekly")


def royalties_summary(month: str) -> None:
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT b.title, COALESCE(r.asin, 'n/a') AS asin,
               SUM(r.units_sold) AS units,
               SUM(r.kenp_reads) AS kenp,
               SUM(r.royalty_net_usd) AS royalty
        FROM royalties r
        LEFT JOIN books b ON b.id = r.book_id
        WHERE strftime('%Y-%m', r.date) = ?
        GROUP BY b.id
        ORDER BY royalty DESC
        """,
        (month,),
    ).fetchall()
    total_royalty = sum((r["royalty"] or 0) for r in rows)
    total_units = sum((r["units"] or 0) for r in rows)
    total_kenp = sum((r["kenp"] or 0) for r in rows)
    print(f"📊 ROYALTY SUMMARY — {month}")
    print(f"  Units:   {total_units}")
    print(f"  KENP:    {total_kenp:,}")
    print(f"  Royalty: ${total_royalty:,.2f}")
    print()
    print(f"  {'Title':<40} {'ASIN':<12} {'Units':>6} {'KENP':>8} {'Royalty':>10}")
    for r in rows:
        title = (r["title"] or "(untitled)")[:40]
        print(
            f"  {title:<40} {r['asin']:<12} {r['units'] or 0:>6} "
            f"{r['kenp'] or 0:>8,} ${r['royalty'] or 0:>9,.2f}"
        )


def bulk_create(table: str, payloads: list[dict]) -> list[int]:
    return [create(table, p) for p in payloads]


def cli() -> None:
    parser = argparse.ArgumentParser(prog="kdp-db")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")
    sub.add_parser("dashboard")

    for table in (
        "niches",
        "books",
        "manuscripts",
        "covers",
        "listings",
        "qa_reports",
        "ad_campaigns",
        "actions",
        "pipelines",
    ):
        tbl = sub.add_parser(table)
        tsub = tbl.add_subparsers(dest="op", required=True)

        tsub.add_parser("create").add_argument("payload")
        tsub.add_parser("bulk-create").add_argument("payload")
        get_p = tsub.add_parser("get")
        get_p.add_argument("id_or_kv", nargs="+")
        list_p = tsub.add_parser("list")
        list_p.add_argument("--status")
        list_p.add_argument("--rating")
        list_p.add_argument("--book_id", type=int)
        list_p.add_argument("--limit", type=int, default=100)
        upd = tsub.add_parser("update")
        upd.add_argument("id", type=int)
        upd.add_argument("payload")

    roy = sub.add_parser("royalties")
    rsub = roy.add_subparsers(dest="op", required=True)
    rsub.add_parser("summary").add_argument("--month", required=True)

    args = parser.parse_args()

    if args.cmd == "init":
        init_db()
        return
    if args.cmd == "dashboard":
        dashboard()
        return

    if args.cmd == "royalties":
        if args.op == "summary":
            royalties_summary(args.month)
        return

    table = args.cmd
    if args.op == "create":
        new_id = create(table, json.loads(args.payload))
        print(json.dumps({"ok": True, "table": table, "id": new_id}, indent=2))
    elif args.op == "bulk-create":
        ids = bulk_create(table, json.loads(args.payload))
        print(json.dumps({"ok": True, "table": table, "ids": ids}, indent=2))
    elif args.op == "get":
        # either integer id or "--book_id X" style
        tokens = args.id_or_kv
        if len(tokens) == 1 and tokens[0].isdigit():
            row = get(table, int(tokens[0]))
        elif len(tokens) == 2 and tokens[0].startswith("--"):
            field = tokens[0].lstrip("-")
            row = get_by(table, field, int(tokens[1]) if tokens[1].isdigit() else tokens[1])
        else:
            print("usage: get <id>  OR  get --book_id 14", file=sys.stderr)
            sys.exit(2)
        print(json.dumps(row, indent=2, default=str))
    elif args.op == "list":
        filters = {}
        if args.status:
            filters["status"] = args.status
        if args.rating:
            filters["rating"] = args.rating
        if args.book_id:
            filters["book_id"] = args.book_id
        rows = list_rows(table, filters, args.limit)
        print(json.dumps(rows, indent=2, default=str))
    elif args.op == "update":
        update(table, args.id, json.loads(args.payload))
        print(json.dumps({"ok": True, "table": table, "id": args.id}, indent=2))


if __name__ == "__main__":
    cli()
