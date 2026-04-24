#!/usr/bin/env python3
"""
Batch generate missing coloring book images across ALL books in output/.

Scans every subdirectory in output/, finds plan.json, checks which
page images are missing from the images/ folder, and generates them
using both nanopic and ai33 providers running 6 threads each (12 total).
"""
from __future__ import annotations

import argparse
import io
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime

from dotenv import load_dotenv
from PIL import Image, ImageEnhance, ImageOps

import config
from image_providers import generate_image_nanopic, generate_image_ai33, get_nanopic_pool

load_dotenv()

# ── Logging ──────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATE_FORMAT = "%H:%M:%S"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
log = logging.getLogger("batch")

# ── Auto-detect nanopic token count for default worker scaling ───────
_NANOPIC_TOKEN_COUNT = get_nanopic_pool().size or 1


# ── Data structures ──────────────────────────────────────────────────
@dataclass
class PageTask:
    """A single missing page to generate."""
    book_dir: str          # e.g. output/french_bulldog_lovers
    theme_key: str         # e.g. french_bulldog_lovers
    page_num: int          # 1-based
    prompt: str
    page_size: str         # e.g. "8.5x8.5"
    output_path: str       # full path to page_XX.png


@dataclass
class BookScanResult:
    """Result of scanning a single book directory."""
    theme_key: str
    total_pages: int
    existing_pages: int
    missing_tasks: list[PageTask] = field(default_factory=list)


# ── Post-processing (same as generate_images.py) ────────────────────
def post_process(image: Image.Image, size_key: str = config.DEFAULT_PAGE_SIZE) -> Image.Image:
    """Post-process generated image for coloring book quality."""
    dims = config.get_page_dims(size_key)
    image = ImageOps.grayscale(image)
    image = ImageOps.contain(
        image,
        (dims["safe_width_px"], dims["safe_height_px"]),
        Image.Resampling.LANCZOS,
    )
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.3)

    full_page = Image.new("L", (dims["width_px"], dims["height_px"]), 255)
    paste_x = (dims["width_px"] - image.size[0]) // 2
    paste_y = (dims["height_px"] - image.size[1]) // 2
    full_page.paste(image, (paste_x, paste_y))
    return full_page


# ── Scanning ─────────────────────────────────────────────────────────
def scan_book(book_dir: str) -> BookScanResult | None:
    """Scan a single book directory for missing pages."""
    plan_path = os.path.join(book_dir, "plan.json")
    if not os.path.isfile(plan_path):
        return None

    try:
        with open(plan_path, "r") as f:
            plan = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log.warning("Skipping %s: cannot read plan.json (%s)", book_dir, e)
        return None

    theme_key = plan.get("theme_key", os.path.basename(book_dir))
    page_prompts = plan.get("page_prompts", [])
    if not page_prompts:
        return None

    page_size = plan.get("page_size", config.DEFAULT_PAGE_SIZE)
    if page_size not in config.PAGE_SIZES:
        page_size = config.DEFAULT_PAGE_SIZE

    images_dir = os.path.join(book_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    result = BookScanResult(
        theme_key=theme_key,
        total_pages=len(page_prompts),
        existing_pages=0,
    )

    for idx, raw_prompt in enumerate(page_prompts):
        # Normalize: some plan.json files store page_prompts as list of dicts
        # (e.g. {"page": 1, "prompt": "..."}) instead of plain strings.
        if isinstance(raw_prompt, dict):
            prompt = raw_prompt.get("prompt") or raw_prompt.get("text") or ""
        else:
            prompt = str(raw_prompt)

        if not prompt.strip():
            log.warning("Skipping %s page %d: empty prompt", theme_key, idx + 1)
            continue

        page_num = idx + 1
        filename = f"page_{page_num:02d}.png"
        filepath = os.path.join(images_dir, filename)

        if os.path.exists(filepath):
            result.existing_pages += 1
        else:
            result.missing_tasks.append(PageTask(
                book_dir=book_dir,
                theme_key=theme_key,
                page_num=page_num,
                prompt=prompt,
                page_size=page_size,
                output_path=filepath,
            ))

    return result


def scan_all_books(output_dir: str) -> list[PageTask]:
    """Scan all book directories and return a flat list of missing page tasks."""
    all_tasks: list[PageTask] = []
    books_with_missing = 0
    books_total = 0

    for entry in sorted(os.listdir(output_dir)):
        book_dir = os.path.join(output_dir, entry)
        if not os.path.isdir(book_dir):
            continue

        result = scan_book(book_dir)
        if result is None:
            continue

        books_total += 1
        if result.missing_tasks:
            books_with_missing += 1
            all_tasks.extend(result.missing_tasks)
            log.info(
                "📖 %-40s  %d/%d pages missing",
                result.theme_key,
                len(result.missing_tasks),
                result.total_pages,
            )
        else:
            log.debug(
                "✅ %-40s  complete (%d pages)",
                result.theme_key,
                result.total_pages,
            )

    log.info("")
    log.info(
        "Scan complete: %d books scanned, %d books with missing pages, %d total missing pages",
        books_total, books_with_missing, len(all_tasks),
    )
    return all_tasks


# ── Generation workers ───────────────────────────────────────────────
def generate_one(task: PageTask, provider: str) -> tuple[bool, str]:
    """Generate a single page image.

    Returns (success, message).
    """
    dims = config.get_page_dims(task.page_size)

    # Already generated by the other provider (race condition check)
    if os.path.exists(task.output_path):
        return True, f"[SKIP] {task.theme_key}/page_{task.page_num:02d} — already exists"

    ar = dims.get("ai33_aspect_ratio", "1:1") if provider == "ai33" else "1:1"

    try:
        if provider == "nanopic":
            image = generate_image_nanopic(task.prompt, aspect_ratio=ar)
        elif provider == "ai33":
            image = generate_image_ai33(task.prompt, aspect_ratio=ar)
        else:
            return False, f"[ERROR] Unknown provider: {provider}"

        if image is None:
            return False, f"[FAIL] {task.theme_key}/page_{task.page_num:02d} ({provider}) — no image returned"

        # Double-check another worker didn't write this file
        if os.path.exists(task.output_path):
            return True, f"[SKIP] {task.theme_key}/page_{task.page_num:02d} — written by other provider"

        processed = post_process(image, size_key=task.page_size)
        processed.save(task.output_path, "PNG", dpi=(config.DPI, config.DPI))
        return True, f"[OK] {task.theme_key}/page_{task.page_num:02d} ({provider}) ✅"

    except Exception as e:
        return False, f"[ERROR] {task.theme_key}/page_{task.page_num:02d} ({provider}): {e}"


# ── Main ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Batch generate missing coloring book images across all books"
    )
    parser.add_argument(
        "--output-dir", type=str,
        default=os.path.join(os.path.dirname(__file__), "output"),
        help="Root output directory to scan (default: ./output)",
    )
    nanopic_default = _NANOPIC_TOKEN_COUNT * 3  # 3 workers per token
    parser.add_argument(
        "--nanopic-workers", type=int, default=nanopic_default,
        help=f"Number of parallel nanopic workers (default: {nanopic_default}, based on {_NANOPIC_TOKEN_COUNT} token(s) × 3)",
    )
    parser.add_argument(
        "--ai33-workers", type=int, default=6,
        help="Number of parallel ai33 workers (default: 6)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Only scan and report missing pages, don't generate",
    )
    parser.add_argument(
        "--book", type=str, default=None,
        help="Only process a specific book (theme_key folder name)",
    )
    parser.add_argument(
        "--ai33-only", action="store_true",
        help="Only use ai33 provider, skip nanopic",
    )
    parser.add_argument(
        "--nanopic-only", action="store_true",
        help="Only use nanopic provider, skip ai33",
    )
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    if not os.path.isdir(output_dir):
        log.error("Output directory not found: %s", output_dir)
        sys.exit(1)

    log.info("=" * 70)
    log.info("BATCH IMAGE GENERATOR")
    log.info("=" * 70)
    log.info("Output dir : %s", output_dir)
    
    if args.ai33_only:
        log.info("Providers  : ai33 only (%d workers)", args.ai33_workers)
    elif args.nanopic_only:
        log.info("Providers  : nanopic only (%d workers)", args.nanopic_workers)
    else:
        log.info("Providers  : nanopic (%d workers) + ai33 (%d workers)", args.nanopic_workers, args.ai33_workers)
        
    log.info("Started at : %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("")

    # ── Scan ──
    if args.book:
        book_dir = os.path.join(output_dir, args.book)
        if not os.path.isdir(book_dir):
            log.error("Book directory not found: %s", book_dir)
            sys.exit(1)
        result = scan_book(book_dir)
        if result is None or not result.missing_tasks:
            log.info("✅ Book '%s' has no missing pages.", args.book)
            return
        all_tasks = result.missing_tasks
        log.info("📖 %s: %d/%d pages missing", result.theme_key, len(result.missing_tasks), result.total_pages)
    else:
        all_tasks = scan_all_books(output_dir)

    if not all_tasks:
        log.info("🎉 All books are complete! No missing pages found.")
        return


    # ── Split tasks between providers ──
    nanopic_tasks: list[PageTask] = []
    ai33_tasks: list[PageTask] = []

    if args.ai33_only:
        ai33_tasks = all_tasks
    elif args.nanopic_only:
        nanopic_tasks = all_tasks
    else:
        # Alternate tasks between nanopic and ai33 for even distribution
        for i, task in enumerate(all_tasks):
            if i % 2 == 0:
                nanopic_tasks.append(task)
            else:
                ai33_tasks.append(task)

    log.info("")
    log.info("📋 Task distribution:")
    log.info("   nanopic: %d pages (%d workers)", len(nanopic_tasks), args.nanopic_workers)
    log.info("   ai33   : %d pages (%d workers)", len(ai33_tasks), args.ai33_workers)
    log.info("")

    if args.dry_run:
        log.info("DRY RUN — listing all missing pages:")
        if nanopic_tasks:
            log.info("  [nanopic]")
            for t in nanopic_tasks:
                log.info("    %s/page_%02d.png", t.theme_key, t.page_num)
        if ai33_tasks:
            log.info("  [ai33]")
            for t in ai33_tasks:
                log.info("    %s/page_%02d.png", t.theme_key, t.page_num)
        return

    # ── Run both pools in parallel ──
    success_count = 0
    fail_count = 0
    total = len(all_tasks)
    completed = 0
    start_time = time.time()

    futures = {}

    nanopic_pool = ThreadPoolExecutor(max_workers=args.nanopic_workers, thread_name_prefix="nanopic")
    ai33_pool = ThreadPoolExecutor(max_workers=args.ai33_workers, thread_name_prefix="ai33")

    try:
        # Submit nanopic tasks
        for task in nanopic_tasks:
            future = nanopic_pool.submit(generate_one, task, "nanopic")
            futures[future] = task

        # Submit ai33 tasks
        for task in ai33_tasks:
            future = ai33_pool.submit(generate_one, task, "ai33")
            futures[future] = task

        # Process results as they complete
        for future in as_completed(futures):
            completed += 1
            task = futures[future]
            try:
                success, message = future.result()
                if success:
                    success_count += 1
                    log.info("✅ [%d/%d success | %d/%d done] %s",
                             success_count, total, completed, total, message)
                else:
                    fail_count += 1
                    log.warning("❌ [%d/%d success | %d/%d done] %s",
                                success_count, total, completed, total, message)
            except Exception as e:
                fail_count += 1
                log.error(
                    "❌ [%d/%d success | %d/%d done] [EXCEPTION] %s/page_%02d: %s",
                    success_count, total, completed, total, task.theme_key, task.page_num, e,
                )

    finally:
        nanopic_pool.shutdown(wait=True)
        ai33_pool.shutdown(wait=True)

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    log.info("")
    log.info("=" * 70)
    log.info("BATCH COMPLETE")
    log.info("=" * 70)
    log.info("Total pages  : %d", total)
    log.info("Success      : %d ✅", success_count)
    log.info("Failed       : %d ❌", fail_count)
    log.info("Time elapsed : %dm %ds", minutes, seconds)
    log.info("=" * 70)


if __name__ == "__main__":
    main()
