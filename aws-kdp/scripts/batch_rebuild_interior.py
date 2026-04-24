#!/usr/bin/env python3
"""Batch rebuild interior PDFs for all books in output/ folder."""
import os
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from build_pdf import build_pdf


def main():
    output_dir = config.OUTPUT_DIR
    themes = []

    for d in sorted(os.listdir(output_dir)):
        theme_dir = os.path.join(output_dir, d)
        if not os.path.isdir(theme_dir):
            continue
        plan_path = os.path.join(theme_dir, "plan.json")
        images_dir = os.path.join(theme_dir, "images")
        if not os.path.exists(plan_path):
            continue
        if not os.path.isdir(images_dir):
            continue
        pngs = [f for f in os.listdir(images_dir) if f.endswith(".png")]
        if not pngs:
            continue
        themes.append(d)

    total = len(themes)
    print(f"Found {total} books to rebuild.\n")

    success = 0
    failed = []

    for i, theme in enumerate(themes, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{total}] Building interior PDF: {theme}")
        print(f"{'='*60}")
        try:
            build_pdf(theme)
            success += 1
            print(f"  -> OK")
        except Exception as e:
            print(f"  -> FAILED: {e}")
            failed.append((theme, str(e)))

    print(f"\n{'='*60}")
    print(f"DONE: {success}/{total} succeeded, {len(failed)} failed")
    if failed:
        print("\nFailed books:")
        for theme, err in failed:
            print(f"  - {theme}: {err}")


if __name__ == "__main__":
    main()
