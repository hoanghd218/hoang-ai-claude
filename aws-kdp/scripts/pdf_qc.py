#!/usr/bin/env python3
"""KDP pre-flight PDF checker.

Validates interior or cover PDFs against KDP's manual-review requirements
before upload. Exits non-zero if any CRITICAL check fails.

Dependencies: pypdf (pure Python, already common). Falls back gracefully
if pypdf isn't installed — reports skipped checks instead of crashing.

Usage:
  python3 pdf_qc.py --pdf path.pdf --trim 8.5x11
  python3 pdf_qc.py --pdf cover.pdf --cover --expected-width 17.37 --expected-height 11.25 --expected-bleed 0.125
  python3 pdf_qc.py --pdf interior.pdf --trim 8.5x11 --require-even-pages --min-line-weight 0.75pt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from pypdf import PdfReader  # type: ignore
    HAS_PYPDF = True
except Exception:
    HAS_PYPDF = False

POINTS_PER_INCH = 72.0
TOLERANCE_IN = 0.01

TRIM_SIZES_IN = {
    "8.5x11":  (8.5, 11.0),
    "8.5x8.5": (8.5, 8.5),
    "6x9":     (6.0, 9.0),
    "7x10":    (7.0, 10.0),
    "8x10":    (8.0, 10.0),
}


class Report:
    def __init__(self) -> None:
        self.critical: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.skipped: list[str] = []

    def crit(self, msg: str) -> None:
        self.critical.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def skip(self, msg: str) -> None:
        self.skipped.append(msg)

    @property
    def verdict(self) -> str:
        return "NO_GO" if self.critical else "GO"

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "critical_issues": self.critical,
            "warnings": self.warnings,
            "notes": self.notes,
            "skipped": self.skipped,
        }


def _page_dims_inches(reader: "PdfReader", page_index: int) -> tuple[float, float]:
    page = reader.pages[page_index]
    box = page.mediabox
    width_pt = float(box.width)
    height_pt = float(box.height)
    return (width_pt / POINTS_PER_INCH, height_pt / POINTS_PER_INCH)


def check_interior(args, report: Report) -> None:
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        report.crit(f"PDF not found: {pdf_path}")
        return
    if not HAS_PYPDF:
        report.skip("pypdf not installed — dimensional checks skipped (`pip install pypdf`)")
        return

    reader = PdfReader(str(pdf_path))
    n_pages = len(reader.pages)
    report.note(f"Page count: {n_pages}")

    if args.require_even_pages and n_pages % 2 != 0:
        report.crit(f"Page count {n_pages} is ODD — KDP requires even page count")

    if args.trim:
        if args.trim not in TRIM_SIZES_IN:
            report.crit(f"Unknown trim: {args.trim}")
        else:
            expected_w, expected_h = TRIM_SIZES_IN[args.trim]
            for i in range(n_pages):
                w, h = _page_dims_inches(reader, i)
                if abs(w - expected_w) > TOLERANCE_IN or abs(h - expected_h) > TOLERANCE_IN:
                    report.crit(
                        f"Page {i + 1} is {w:.3f}×{h:.3f}\" — expected {expected_w}×{expected_h}\""
                    )
                    break
            else:
                report.note(f"All {n_pages} pages match trim {args.trim}")

    mb = pdf_path.stat().st_size / (1024 * 1024)
    report.note(f"File size: {mb:.1f} MB")
    if mb > 650:
        report.crit(f"File size {mb:.1f} MB exceeds KDP limit 650 MB")
    elif mb > 400:
        report.warn(f"File size {mb:.1f} MB is large — consider optimizing")

    if args.min_line_weight:
        report.skip(f"Line-weight check ({args.min_line_weight}) — delegate to kdp-image-reviewer")


def check_cover(args, report: Report) -> None:
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        report.crit(f"PDF not found: {pdf_path}")
        return
    if not HAS_PYPDF:
        report.skip("pypdf not installed — dimensional checks skipped (`pip install pypdf`)")
        return

    reader = PdfReader(str(pdf_path))
    n_pages = len(reader.pages)
    if n_pages != 1:
        report.crit(f"Cover PDF must be exactly 1 page, got {n_pages}")
        return

    w, h = _page_dims_inches(reader, 0)
    report.note(f"Cover dimensions: {w:.3f}\" × {h:.3f}\"")

    if args.expected_width and abs(w - args.expected_width) > TOLERANCE_IN:
        report.crit(
            f"Cover width {w:.3f}\" ≠ expected {args.expected_width}\" (Δ {w - args.expected_width:+.3f}\")"
        )
    if args.expected_height and abs(h - args.expected_height) > TOLERANCE_IN:
        report.crit(
            f"Cover height {h:.3f}\" ≠ expected {args.expected_height}\" (Δ {h - args.expected_height:+.3f}\")"
        )

    mb = pdf_path.stat().st_size / (1024 * 1024)
    report.note(f"File size: {mb:.1f} MB")

    report.skip("Barcode safe-zone check — visual inspection required")
    report.skip("300 DPI raster check — use image-specific tooling")


def main() -> int:
    parser = argparse.ArgumentParser(description="KDP pre-flight PDF checker")
    parser.add_argument("--pdf", required=True, help="Path to PDF")
    parser.add_argument("--trim", help="Expected trim size (e.g. 8.5x11)")
    parser.add_argument("--require-even-pages", action="store_true")
    parser.add_argument("--min-line-weight", help="Minimum line weight (e.g. 0.75pt)")
    parser.add_argument("--cover", action="store_true", help="Treat as cover PDF")
    parser.add_argument("--expected-width", type=float)
    parser.add_argument("--expected-height", type=float)
    parser.add_argument("--expected-bleed", type=float, default=0.125)
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args()

    report = Report()
    if args.cover:
        check_cover(args, report)
    else:
        check_interior(args, report)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"📋 PDF QC — {args.pdf}")
        print(f"   Verdict: {'✅ GO' if report.verdict == 'GO' else '🛑 NO_GO'}")
        if report.critical:
            print("\n🛑 CRITICAL:")
            for m in report.critical:
                print(f"  • {m}")
        if report.warnings:
            print("\n⚠  WARNINGS:")
            for m in report.warnings:
                print(f"  • {m}")
        if report.notes:
            print("\n• NOTES:")
            for m in report.notes:
                print(f"  • {m}")
        if report.skipped:
            print("\n… SKIPPED:")
            for m in report.skipped:
                print(f"  • {m}")

    return 1 if report.verdict == "NO_GO" else 0


if __name__ == "__main__":
    sys.exit(main())
