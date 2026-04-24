#!/usr/bin/env python3
"""Batch rebuild covers for all books in output/ folder.

Runs up to 6 books in parallel using ThreadPoolExecutor.
"""
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from generate_cover import build_cover

MAX_WORKERS = 6
_print_lock = threading.Lock()


def _safe_print(*args, **kwargs):
    """Thread-safe print."""
    with _print_lock:
        print(*args, **kwargs, flush=True)


def _process_one(theme, index, total, renderer, regenerate):
    """Process a single theme – called from a worker thread."""
    _safe_print(f"\n{'='*60}")
    _safe_print(f"[{index}/{total}] Generating cover: {theme}")
    _safe_print(f"{'='*60}")
    try:
        build_cover(theme, renderer=renderer, regenerate_artwork=regenerate)
        _safe_print(f"  [{theme}] -> OK")
        return (theme, True, None)
    except Exception as e:
        _safe_print(f"  [{theme}] -> FAILED: {e}")
        return (theme, False, str(e))


def main():
    renderer = "nanopic"
    regenerate = False

    # Parse args
    args = sys.argv[1:]
    for arg in args:
        if arg == "--regenerate":
            regenerate = True
        else:
            renderer = arg

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
    mode = "REGENERATE artwork" if regenerate else "REUSE saved artwork (use --regenerate to force new)"
    print(f"Found {total} books to generate covers (renderer: {renderer}, mode: {mode}).")
    print(f"Running with {MAX_WORKERS} parallel workers.\n")

    success = 0
    failed = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(_process_one, theme, i, total, renderer, regenerate): theme
            for i, theme in enumerate(themes, 1)
        }

        for future in as_completed(futures):
            theme, ok, err = future.result()
            if ok:
                success += 1
            else:
                failed.append((theme, err))

    print(f"\n{'='*60}")
    print(f"DONE: {success}/{total} succeeded, {len(failed)} failed")
    if failed:
        print("\nFailed books:")
        for theme, err in failed:
            print(f"  - {theme}: {err}")


if __name__ == "__main__":
    main()

