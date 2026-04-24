#!/usr/bin/env python3
"""KDP royalty report ingester.

KDP does not have a public read API — royalty data comes as CSV / Excel
exports from the KDP Reports dashboard. The user drops files into
`data/kdp_reports/` and this script parses them into the `royalties` table.

Supported formats (auto-detected by header row):
- "KDP_Royalties_Estimator" CSV (monthly)
- "KDP_Prior_Months_Royalties" CSV
- "KENP_Read_Report" CSV (KDP Select)

Usage:
  python3 amazon_kdp_reports.py ingest --dir data/kdp_reports/
  python3 amazon_kdp_reports.py ingest --file some.csv
  python3 amazon_kdp_reports.py list
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE.parent / "data" / "kdp.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _detect_format(header: list[str]) -> str:
    header_lower = [h.lower() for h in header]
    if any("kenp" in h for h in header_lower):
        return "kenp"
    if any("royalty" in h for h in header_lower) and any(
        "units" in h or "net units" in h for h in header_lower
    ):
        return "royalties"
    return "unknown"


def _find_col(header: list[str], needles: list[str]) -> int | None:
    for idx, h in enumerate(header):
        low = h.lower()
        if all(n in low for n in needles):
            return idx
    return None


def _parse_date(raw: str) -> str | None:
    if not raw:
        return None
    raw = raw.strip().strip('"')
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m", "%b %d %Y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def ingest_file(path: Path) -> int:
    if not path.exists():
        print(f"⚠ Skip (missing): {path}")
        return 0

    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    if not rows:
        return 0

    # find the header row (KDP reports often have a banner line first)
    header_idx = 0
    for i, row in enumerate(rows[:5]):
        if any("ASIN" in cell or "asin" in cell for cell in row):
            header_idx = i
            break
    header = rows[header_idx]
    data_rows = rows[header_idx + 1 :]
    fmt = _detect_format(header)

    if fmt == "unknown":
        print(f"⚠ Unknown format: {path.name}")
        return 0

    asin_col = _find_col(header, ["asin"])
    date_col = _find_col(header, ["date"]) or _find_col(header, ["royalty", "date"])
    marketplace_col = _find_col(header, ["marketplace"])
    units_col = _find_col(header, ["net", "units"]) or _find_col(header, ["units"])
    royalty_col = _find_col(header, ["royalty"])
    kenp_col = _find_col(header, ["kenp"]) or _find_col(header, ["pages", "read"])

    conn = get_conn()
    # Map ASIN → book_id
    asin_to_book = {
        r["asin"]: r["id"] for r in conn.execute("SELECT id, asin FROM books WHERE asin IS NOT NULL")
    }

    inserted = 0
    for row in data_rows:
        if not row or len(row) < 2:
            continue
        asin = row[asin_col].strip() if asin_col is not None and asin_col < len(row) else ""
        if not asin or asin.upper() == "ASIN":
            continue
        date = _parse_date(row[date_col]) if date_col is not None and date_col < len(row) else None
        if not date:
            continue
        marketplace = (
            row[marketplace_col].strip() if marketplace_col is not None and marketplace_col < len(row) else "US"
        )

        def _num(col: int | None) -> float:
            if col is None or col >= len(row):
                return 0.0
            raw = row[col].replace(",", "").replace("$", "").strip()
            try:
                return float(raw)
            except ValueError:
                return 0.0

        units = int(_num(units_col))
        kenp = int(_num(kenp_col))
        royalty = _num(royalty_col)
        book_id = asin_to_book.get(asin)

        try:
            conn.execute(
                """
                INSERT INTO royalties (book_id, asin, date, marketplace, units_sold, kenp_reads, royalty_net_usd)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(asin, date, marketplace) DO UPDATE SET
                    units_sold = excluded.units_sold,
                    kenp_reads = excluded.kenp_reads,
                    royalty_net_usd = excluded.royalty_net_usd,
                    book_id = COALESCE(excluded.book_id, royalties.book_id)
                """,
                (book_id, asin, date, marketplace, units, kenp, royalty),
            )
            inserted += 1
        except sqlite3.IntegrityError as exc:
            print(f"  ⚠ {asin} {date}: {exc}")

    conn.commit()
    print(f"  • {path.name}: ingested {inserted} rows ({fmt})")
    return inserted


def ingest_dir(directory: Path) -> int:
    if not directory.exists():
        print(f"⚠ Directory missing: {directory}")
        return 0
    total = 0
    for f in sorted(directory.glob("*.csv")):
        total += ingest_file(f)
    return total


def list_recent(limit: int = 20) -> None:
    conn = get_conn()
    rows = conn.execute(
        """SELECT date, asin, units_sold, kenp_reads, royalty_net_usd
           FROM royalties ORDER BY date DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    if not rows:
        print("No royalty rows yet. Drop KDP CSV exports into data/kdp_reports/ and run `ingest`.")
        return
    print(f"{'Date':<12} {'ASIN':<12} {'Units':>6} {'KENP':>8} {'Royalty':>10}")
    for r in rows:
        print(
            f"{r['date']:<12} {r['asin']:<12} {r['units_sold']:>6} "
            f"{r['kenp_reads']:>8,} ${r['royalty_net_usd']:>9,.2f}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    ing = sub.add_parser("ingest")
    ing.add_argument("--dir")
    ing.add_argument("--file")

    lst = sub.add_parser("list")
    lst.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    if args.cmd == "ingest":
        if args.dir:
            total = ingest_dir(Path(args.dir))
        elif args.file:
            total = ingest_file(Path(args.file))
        else:
            print("need --dir or --file", file=sys.stderr)
            return 2
        print(f"✅ Ingested {total} rows total")
    elif args.cmd == "list":
        list_recent(args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
