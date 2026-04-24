#!/usr/bin/env python3
"""
KDP Cover Dimension Checker
Validates cover PDFs against Amazon KDP specifications.
"""
import argparse
import json
import os
import sys

# ---------------------------------------------------------------------------
# KDP Constants
# ---------------------------------------------------------------------------
BLEED_INCHES = 0.125
PAPER_THICKNESS = 0.002252  # white paper, black ink — inches per page
MIN_DPI = 300
TOLERANCE_INCHES = 0.01  # ±0.01" tolerance for rounding

PAGE_SIZES = {
    "8.5x11": {"width": 8.5, "height": 11.0},
    "8.5x8.5": {"width": 8.5, "height": 8.5},
}
DEFAULT_SIZE = "8.5x11"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def count_images(theme_dir: str) -> int:
    """Count PNG images in the images/ subfolder."""
    img_dir = os.path.join(theme_dir, "images")
    if not os.path.isdir(img_dir):
        return 0
    return len([f for f in os.listdir(img_dir) if f.lower().endswith(".png")])


def estimate_total_pages(num_images: int) -> int:
    """Estimate interior page count (matches build_pdf.py logic)."""
    if num_images == 0:
        return 0
    total = 2 + (num_images * 2) + 1  # title + copyright + pages*2 + thank-you
    if total % 2 != 0:
        total += 1
    return total


def expected_cover_dims(total_pages: int, trim_w: float, trim_h: float) -> dict:
    """Return expected cover dimensions in inches."""
    spine = round(total_pages * PAPER_THICKNESS, 4)
    width = trim_w * 2 + spine + BLEED_INCHES * 2
    height = trim_h + BLEED_INCHES * 2
    return {
        "spine_inches": spine,
        "width_inches": round(width, 4),
        "height_inches": round(height, 4),
        "width_px": round(width * MIN_DPI),
        "height_px": round(height * MIN_DPI),
    }


def read_pdf_dimensions(pdf_path: str) -> dict | None:
    """Read PDF page size and DPI. Tries pikepdf first, then PyPDF2."""
    try:
        import pikepdf
        pdf = pikepdf.open(pdf_path)
        page = pdf.pages[0]
        mb = page.mediabox
        # pikepdf returns points (1 inch = 72 points)
        w_pts = float(mb[2]) - float(mb[0])
        h_pts = float(mb[3]) - float(mb[1])
        w_inches = round(w_pts / 72, 4)
        h_inches = round(h_pts / 72, 4)
        pdf.close()
        return {"width_inches": w_inches, "height_inches": h_inches, "source": "pikepdf"}
    except ImportError:
        pass
    except Exception as e:
        print(f"  pikepdf error: {e}")

    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        page = reader.pages[0]
        mb = page.mediabox
        w_pts = float(mb.width)
        h_pts = float(mb.height)
        w_inches = round(w_pts / 72, 4)
        h_inches = round(h_pts / 72, 4)
        return {"width_inches": w_inches, "height_inches": h_inches, "source": "PyPDF2"}
    except ImportError:
        pass
    except Exception as e:
        print(f"  PyPDF2 error: {e}")

    # Fallback: use Pillow to read the image embedded in PDF
    try:
        from PIL import Image
        img = Image.open(pdf_path)
        dpi = img.info.get("dpi", (MIN_DPI, MIN_DPI))
        dpi_x = dpi[0] if dpi[0] > 0 else MIN_DPI
        dpi_y = dpi[1] if dpi[1] > 0 else MIN_DPI
        w_inches = round(img.width / dpi_x, 4)
        h_inches = round(img.height / dpi_y, 4)
        img.close()
        return {"width_inches": w_inches, "height_inches": h_inches, "source": "Pillow",
                "dpi_x": dpi_x, "dpi_y": dpi_y, "px_w": img.width, "px_h": img.height}
    except Exception as e:
        print(f"  Pillow fallback error: {e}")

    return None


def check_dpi_from_png(theme_dir: str) -> dict | None:
    """Check DPI from the cover PNG (more reliable than PDF metadata)."""
    png_path = os.path.join(theme_dir, "cover.png")
    if not os.path.isfile(png_path):
        return None
    try:
        from PIL import Image
        img = Image.open(png_path)
        dpi = img.info.get("dpi", (0, 0))
        result = {"dpi_x": dpi[0], "dpi_y": dpi[1], "width_px": img.width, "height_px": img.height}
        img.close()
        return result
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Main checker
# ---------------------------------------------------------------------------

def check_single_book(theme_dir: str, theme_name: str, verbose: bool = False) -> dict:
    """Check a single book's cover. Returns result dict."""
    result = {"theme": theme_name, "status": "UNKNOWN", "details": []}

    # 1. Detect page_size from plan.json
    plan_path = os.path.join(theme_dir, "plan.json")
    page_size_key = DEFAULT_SIZE
    if os.path.isfile(plan_path):
        with open(plan_path) as f:
            plan = json.load(f)
            ps = plan.get("page_size", DEFAULT_SIZE)
            if ps in PAGE_SIZES:
                page_size_key = ps
    result["page_size"] = page_size_key

    trim_w = PAGE_SIZES[page_size_key]["width"]
    trim_h = PAGE_SIZES[page_size_key]["height"]

    # 2. Count pages
    num_images = count_images(theme_dir)
    if num_images == 0:
        # Try to get from plan
        if os.path.isfile(plan_path):
            with open(plan_path) as f:
                plan = json.load(f)
                prompts = plan.get("prompts", plan.get("pages", []))
                num_images = len(prompts) if prompts else 25
        else:
            num_images = 25  # default estimate

    total_pages = estimate_total_pages(num_images)
    result["num_images"] = num_images
    result["total_pages"] = total_pages

    # 3. Calculate expected dimensions
    expected = expected_cover_dims(total_pages, trim_w, trim_h)
    result["expected"] = expected

    # 4. Check if cover.pdf exists
    pdf_path = os.path.join(theme_dir, "cover.pdf")
    if not os.path.isfile(pdf_path):
        result["status"] = "SKIP"
        result["details"].append("No cover.pdf found")
        return result

    # 5. Read actual dimensions
    actual = read_pdf_dimensions(pdf_path)
    if actual is None:
        result["status"] = "ERROR"
        result["details"].append("Could not read PDF dimensions (install pikepdf or PyPDF2)")
        return result

    result["actual"] = actual

    # 6. Compare dimensions
    issues = []

    w_delta = actual["width_inches"] - expected["width_inches"]
    h_delta = actual["height_inches"] - expected["height_inches"]

    if abs(w_delta) > TOLERANCE_INCHES:
        issues.append(f"WIDTH: expected {expected['width_inches']:.3f}\", got {actual['width_inches']:.3f}\" (delta {w_delta:+.3f}\")")
    if abs(h_delta) > TOLERANCE_INCHES:
        issues.append(f"HEIGHT: expected {expected['height_inches']:.3f}\", got {actual['height_inches']:.3f}\" (delta {h_delta:+.3f}\")")

    # 7. Check DPI from PNG
    png_info = check_dpi_from_png(theme_dir)
    if png_info:
        result["png_info"] = png_info
        dpi_tolerance = 0.5  # 299.5+ is effectively 300
        if png_info["dpi_x"] < (MIN_DPI - dpi_tolerance) or png_info["dpi_y"] < (MIN_DPI - dpi_tolerance):
            issues.append(f"DPI: {png_info['dpi_x']:.1f}x{png_info['dpi_y']:.1f} (minimum {MIN_DPI} required)")

    if issues:
        result["status"] = "FAIL"
        result["details"] = issues
    else:
        result["status"] = "PASS"

    return result


def format_result(r: dict, verbose: bool = False) -> str:
    """Format a single result for display."""
    lines = []
    status = r["status"]

    if status == "SKIP":
        lines.append(f"[SKIP] {r['theme']} — {r['details'][0]}")
        return "\n".join(lines)

    if status == "ERROR":
        lines.append(f"[ERROR] {r['theme']} — {r['details'][0]}")
        return "\n".join(lines)

    expected = r.get("expected", {})
    actual = r.get("actual", {})

    tag = "PASS" if status == "PASS" else "FAIL"
    suffix = ""
    if status == "FAIL":
        suffix = " — " + "; ".join(r["details"])

    lines.append(f"[{tag}] {r['theme']}{suffix}")
    lines.append(f"  Pages: {r['total_pages']} ({r['num_images']} images) | Size: {r['page_size']} | Spine: {expected.get('spine_inches', 0):.3f}\"")
    lines.append(f"  Expected: {expected.get('width_inches', 0):.3f}\" x {expected.get('height_inches', 0):.3f}\"")
    lines.append(f"  Actual:   {actual.get('width_inches', 0):.3f}\" x {actual.get('height_inches', 0):.3f}\"")

    if verbose and r.get("png_info"):
        pi = r["png_info"]
        lines.append(f"  PNG: {pi['width_px']}x{pi['height_px']} px, DPI: {pi['dpi_x']}x{pi['dpi_y']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="KDP Cover Dimension Checker")
    parser.add_argument("--theme", type=str, default=None, help="Check a single theme (folder name)")
    parser.add_argument("--output-dir", type=str, default="output", help="Base output directory (default: output)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details for all books including passing ones")
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    if not os.path.isdir(output_dir):
        print(f"Error: output directory not found: {output_dir}")
        sys.exit(1)

    # Collect themes to check
    if args.theme:
        themes = [args.theme]
    else:
        themes = sorted([
            d for d in os.listdir(output_dir)
            if os.path.isdir(os.path.join(output_dir, d))
        ])

    if not themes:
        print("No themes found in output/")
        sys.exit(0)

    results = []
    for theme in themes:
        theme_dir = os.path.join(output_dir, theme)
        if not os.path.isdir(theme_dir):
            print(f"[SKIP] {theme} — directory not found")
            continue
        r = check_single_book(theme_dir, theme, args.verbose)
        results.append(r)

    # Display results
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")
    skip_count = sum(1 for r in results if r["status"] == "SKIP")
    error_count = sum(1 for r in results if r["status"] == "ERROR")

    print("=" * 70)
    print("KDP COVER DIMENSION CHECK")
    print("=" * 70)
    print()

    # Show failures first
    for r in results:
        if r["status"] == "FAIL":
            print(format_result(r, args.verbose))
            print()

    # Then errors
    for r in results:
        if r["status"] == "ERROR":
            print(format_result(r, args.verbose))
            print()

    # Then skips
    for r in results:
        if r["status"] == "SKIP":
            print(format_result(r, args.verbose))

    # Then passes (only if verbose or few results)
    if args.verbose or len(results) <= 10:
        for r in results:
            if r["status"] == "PASS":
                print(format_result(r, args.verbose))
                print()
    else:
        # Compact pass list
        passing = [r["theme"] for r in results if r["status"] == "PASS"]
        if passing:
            print(f"\n[PASS] {len(passing)} books OK: {', '.join(passing[:5])}", end="")
            if len(passing) > 5:
                print(f" ... and {len(passing) - 5} more", end="")
            print()

    # Summary
    print()
    print("-" * 70)
    print(f"SUMMARY: {len(results)} books checked")
    print(f"  PASS: {pass_count}  |  FAIL: {fail_count}  |  SKIP: {skip_count}  |  ERROR: {error_count}")
    print("-" * 70)

    # Exit code: 1 if any failures
    sys.exit(1 if fail_count > 0 else 0)


if __name__ == "__main__":
    main()
