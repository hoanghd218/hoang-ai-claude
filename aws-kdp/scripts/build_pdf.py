#!/usr/bin/env python3
"""
Build a KDP-ready PDF coloring book from generated images.
Layout: title page, copyright, coloring pages on odd pages with blank backs.
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import config


def get_sorted_images(theme: str) -> list[str]:
    """Get sorted list of generated image files for a theme."""
    image_dir = config.get_images_dir(theme)
    if not os.path.exists(image_dir):
        print(f"Error: Image directory not found: {image_dir}")
        print(f"Run 'python generate_images.py --theme {theme}' first")
        sys.exit(1)

    images = sorted(
        [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if f.endswith(".png")
        ]
    )

    if not images:
        print(f"Error: No PNG images found in {image_dir}")
        sys.exit(1)

    return images


def _load_plan_meta(theme: str) -> dict:
    """Load audience and page_size from plan file."""
    import json
    plan_path = config.get_plan_path(theme)
    meta = {"audience": "kids", "page_size": None}
    if os.path.exists(plan_path):
        with open(plan_path) as f:
            plan = json.load(f)
            meta["audience"] = plan.get("audience", "kids")
            meta["page_size"] = plan.get("page_size")
    return meta


def build_pdf(theme: str, title: str | None = None, subtitle: str | None = None, author: str = "", size: str = config.DEFAULT_PAGE_SIZE):
    """Build KDP-ready PDF coloring book."""
    theme_config = config.THEMES.get(theme)
    if not theme_config:
        print(f"Error: Unknown theme '{theme}'")
        sys.exit(1)

    # Auto-detect page size from plan/theme config if not explicitly set
    plan_meta = _load_plan_meta(theme)
    audience = plan_meta["audience"]
    if size == config.DEFAULT_PAGE_SIZE:
        # Check plan first, then theme config
        if plan_meta["page_size"] and plan_meta["page_size"] in config.PAGE_SIZES:
            size = plan_meta["page_size"]
        elif "page_size" in theme_config and theme_config["page_size"] in config.PAGE_SIZES:
            size = theme_config["page_size"]

    if title is None:
        title = theme_config["book_title"]
    if subtitle is None:
        if audience == "adults":
            subtitle = "A Relaxing Coloring Book for Adults"
        else:
            subtitle = f"Coloring Book for Kids Ages {config.TARGET_AGE}"

    # Load author: CLI > plan.json > .env default
    if not author:
        import json
        plan_path = config.get_plan_path(theme)
        if os.path.exists(plan_path):
            with open(plan_path) as f:
                plan_data = json.load(f)
                author_obj = plan_data.get("author", {})
                if isinstance(author_obj, dict):
                    first = author_obj.get("first_name", "")
                    last = author_obj.get("last_name", "")
                    author = f"{first} {last}".strip()
                elif isinstance(author_obj, str):
                    author = author_obj
    if not author:
        author = config.DEFAULT_AUTHOR

    images = get_sorted_images(theme)
    print(f"Found {len(images)} coloring pages")

    # Calculate total page count first (for gutter margin)
    total_pages = 2 + (len(images) * 2) + 1  # title + copyright + pages + thank you
    if total_pages % 2 != 0:
        total_pages += 1  # padding page

    # Page size with gutter margin based on page count
    dims = config.get_page_dims(size, page_count=total_pages)
    page_w = dims["width_inches"] * inch
    page_h = dims["height_inches"] * inch
    margin = dims["margin_inches"] * inch       # outside, top, bottom
    gutter = dims["gutter_margin_inches"] * inch  # inside (spine side)

    gutter_in = dims["gutter_margin_inches"]
    print(f"Total pages: {total_pages} -> gutter margin: {gutter_in}\" (outside: {dims['margin_inches']}\")")

    # Output path
    book_dir = config.get_book_dir(theme)
    os.makedirs(book_dir, exist_ok=True)
    output_path = config.get_interior_pdf_path(theme)

    # Register embeddable TTF fonts (KDP requires all fonts fully embedded)
    pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Italic', '/System/Library/Fonts/Supplemental/Arial Italic.ttf'))
    # Override Helvetica so ReportLab's default font is also embedded
    pdfmetrics.registerFont(TTFont('Helvetica', '/System/Library/Fonts/Supplemental/Arial.ttf'))

    c = canvas.Canvas(output_path, pagesize=(page_w, page_h))
    c.setFont("Arial", 12)  # Override default Helvetica

    # Helper: get content area for a given page number (1-based)
    # Odd pages (right-hand): gutter on LEFT, outside on RIGHT
    # Even pages (left-hand): gutter on RIGHT, outside on LEFT
    def _content_area(page_num: int):
        """Return (x, y, w, h) for the safe content area on this page."""
        if page_num % 2 == 1:  # odd = right-hand page, gutter on left
            left = gutter
            right = margin
        else:  # even = left-hand page, gutter on right
            left = margin
            right = gutter
        x = left
        y = margin  # bottom margin
        w = page_w - left - right
        h = page_h - 2 * margin  # top + bottom margin
        return x, y, w, h

    page_num = 0  # tracks current page number

    # --- Page 1: Title Page ---
    page_num += 1
    cx, cy, cw, ch = _content_area(page_num)
    center_x = cx + cw / 2

    # Auto-scale title font until it fits in max 4 lines
    title_font_size = 36
    title_max_chars = 25
    title_lines = _wrap_text(title, max_chars=title_max_chars)
    while len(title_lines) > 4 and title_font_size > 18:
        title_font_size -= 2
        title_max_chars += 5
        title_lines = _wrap_text(title, max_chars=title_max_chars)
    title_line_spacing = title_font_size * 1.3

    # Draw title block centered vertically in upper half of page
    c.setFont("Arial-Bold", title_font_size)
    title_block_height = (len(title_lines) - 1) * title_line_spacing
    title_top = page_h * 0.72  # start from upper area
    title_bottom = title_top - title_block_height  # actual bottom of title block
    for i, line in enumerate(title_lines):
        c.drawCentredString(center_x, title_top - (i * title_line_spacing), line)

    # Subtitle: always placed below title block with fixed gap
    GAP = 28
    y_sub = title_bottom - GAP
    c.setFont("Arial", 16)
    subtitle_lines = _wrap_text(subtitle, max_chars=48)
    for i, line in enumerate(subtitle_lines):
        c.drawCentredString(center_x, y_sub - (i * 22), line)
    y_after_sub = y_sub - (len(subtitle_lines) - 1) * 22

    # Design label
    y_label = y_after_sub - GAP
    c.setFont("Arial-Italic", 13)
    if audience == "adults":
        c.drawCentredString(center_x, y_label, "Cozy & Relaxing Designs")
    else:
        c.drawCentredString(center_x, y_label, "Bold & Easy Designs")

    # Author name — always below label with fixed gap
    if author:
        y_author = y_label - GAP
        c.setFont("Arial", 13)
        c.drawCentredString(center_x, y_author, f"by {author}")
    c.showPage()

    # --- Page 2: Copyright / Info Page ---
    page_num += 1
    cx, cy, cw, ch = _content_area(page_num)
    center_x = cx + cw / 2

    current_year = datetime.datetime.now().year
    c.setFont("Arial", 11)
    author_line = f"Copyright (c) {current_year} {author}. All rights reserved." if author else f"Copyright (c) {current_year}. All rights reserved."
    if audience == "adults":
        copyright_lines = [
            author_line,
            "",
            "No part of this book may be reproduced or used in any manner",
            "without written permission of the copyright owner.",
            "",
            "This coloring book is designed for adults who enjoy relaxing,",
            "creative coloring sessions.",
            "",
            "For personal use only. Not for resale.",
            "",
            "We hope you enjoy every page!",
        ]
    else:
        copyright_lines = [
            author_line,
            "",
            "No part of this book may be reproduced or used in any manner",
            "without written permission of the copyright owner.",
            "",
            f"This coloring book is designed for children ages {config.TARGET_AGE}.",
            "",
            "For personal use only. Not for resale.",
            "",
            "Made with love for creative kids everywhere!",
        ]
    y = page_h * 0.6
    for line in copyright_lines:
        c.drawCentredString(center_x, y, line)
        y -= 18
    c.showPage()

    # --- Coloring Pages (odd pages) with blank backs (even pages) ---
    for i, image_path in enumerate(images):
        # Odd page: coloring image
        page_num += 1
        cx, cy, cw, ch = _content_area(page_num)

        # Draw image within the safe content area (respecting gutter + margins)
        c.drawImage(
            image_path,
            cx,
            cy,
            width=cw,
            height=ch,
            preserveAspectRatio=True,
            anchor="c",
        )
        c.showPage()

        # Even page: blank (prevents bleed-through when coloring)
        page_num += 1
        c.showPage()

    # Ensure even total page count (KDP requirement)
    # Add blank page BEFORE Thank You if needed, so Thank You is always the last page
    remaining = page_num  # pages so far
    # Thank You will be page_num+1. Total = page_num+1. Need even total.
    if (remaining + 1) % 2 != 0:
        # Add a blank page so Thank You lands on an even total
        page_num += 1
        c.showPage()

    # --- Last Page: Thank You ---
    page_num += 1
    cx, cy, cw, ch = _content_area(page_num)
    center_x = cx + cw / 2

    c.setFont("Arial-Bold", 28)
    c.drawCentredString(center_x, page_h * 0.55, "Thank You!")
    c.setFont("Arial", 16)
    c.drawCentredString(center_x, page_h * 0.45, "We hope you enjoyed coloring!")
    c.setFont("Arial", 14)
    c.drawCentredString(
        center_x, page_h * 0.38, "If you liked this book, please leave a review."
    )
    c.showPage()

    c.save()

    print(f"PDF created: {output_path}")
    print(f"Total pages: {page_num}")
    print(f"  - Title page: 1")
    print(f"  - Copyright: 1")
    print(f"  - Coloring pages: {len(images)} (with {len(images)} blank backs)")
    print(f"  - Thank you: 1")
    print(f"Page size: {dims['width_inches']}\" x {dims['height_inches']}\"")
    print(f"Gutter margin: {gutter_in}\" | Outside/Top/Bottom: {dims['margin_inches']}\"")


def _wrap_text(text: str, max_chars: int = 25) -> list[str]:
    """Simple word-wrap for title text."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > max_chars and current_line:
            lines.append(current_line.strip())
            current_line = word
        else:
            current_line += " " + word
    if current_line.strip():
        lines.append(current_line.strip())
    return lines


def main():
    parser = argparse.ArgumentParser(description="Build KDP-ready coloring book PDF")
    parser.add_argument(
        "--theme",
        required=True,
        choices=config.THEMES.keys(),
        help="Coloring book theme",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Custom book title (default: from config)",
    )
    parser.add_argument(
        "--subtitle",
        type=str,
        default=None,
        help="Custom subtitle",
    )
    parser.add_argument(
        "--author",
        type=str,
        default="",
        help="Author name (for title page and copyright)",
    )
    parser.add_argument(
        "--size",
        choices=config.PAGE_SIZES.keys(),
        default=config.DEFAULT_PAGE_SIZE,
        help=f"Page size (default: {config.DEFAULT_PAGE_SIZE})",
    )
    args = parser.parse_args()

    build_pdf(args.theme, args.title, args.subtitle, args.author, args.size)


if __name__ == "__main__":
    main()
