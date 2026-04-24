#!/usr/bin/env python3
"""
Generate coloring book page images using AI image providers.
Each image is a black-and-white line art suitable for coloring.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from dotenv import load_dotenv
from PIL import Image, ImageEnhance, ImageOps

import config
from image_providers import generate_image, RENDERER_CHOICES, DEFAULT_RENDERER

load_dotenv()


def load_subjects(theme: str) -> list[str]:
    """Load subject list from prompt template file."""
    theme_config = config.THEMES.get(theme)
    if not theme_config:
        print(f"Error: Unknown theme '{theme}'")
        print(f"Available themes: {', '.join(config.THEMES.keys())}")
        sys.exit(1)

    prompt_file = theme_config["prompt_file"]
    if not os.path.exists(prompt_file):
        print(f"Error: Prompt file not found: {prompt_file}")
        sys.exit(1)

    with open(prompt_file, "r") as f:
        subjects = [line.strip() for line in f if line.strip()]
    return subjects


def load_plan_prompts(plan_path: str) -> tuple[str, list[str], str | None]:
    """Load theme key, full prompts, and page_size from a plan JSON file."""
    if not os.path.exists(plan_path):
        print(f"Error: Plan file not found: {plan_path}")
        sys.exit(1)

    with open(plan_path, "r") as f:
        plan = json.load(f)

    theme_key = plan.get("theme_key")
    if not theme_key:
        print("Error: Plan file missing 'theme_key'")
        sys.exit(1)

    page_prompts = plan.get("page_prompts", []) or plan.get("prompts", [])
    if not page_prompts:
        print("Error: Plan file has no 'page_prompts' or 'prompts'")
        sys.exit(1)

    page_size = plan.get("page_size")
    return theme_key, page_prompts, page_size


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


def main():
    parser = argparse.ArgumentParser(description="Generate coloring book images")
    parser.add_argument(
        "--theme",
        choices=config.THEMES.keys(),
        help="Coloring book theme (required unless --plan is used)",
    )
    parser.add_argument(
        "--plan", type=str, default=None,
        help="Path to a plan JSON file (from plan_book.py output)",
    )
    parser.add_argument(
        "--count", type=int, default=config.COLORING_PAGES_PER_BOOK,
        help=f"Number of pages to generate (default: {config.COLORING_PAGES_PER_BOOK})",
    )
    parser.add_argument(
        "--start", type=int, default=0,
        help="Start index in subject list (for resuming)",
    )
    parser.add_argument(
        "--size", choices=config.PAGE_SIZES.keys(),
        default=config.DEFAULT_PAGE_SIZE,
        help=f"Page size (default: {config.DEFAULT_PAGE_SIZE})",
    )
    parser.add_argument(
        "--renderer", choices=RENDERER_CHOICES, default=DEFAULT_RENDERER,
        help=f"Image renderer (default: {DEFAULT_RENDERER} from .env)",
    )
    args = parser.parse_args()

    # Determine mode: plan-based or theme-based
    use_raw_prompt = False
    if args.plan:
        theme_key, prompts, plan_page_size = load_plan_prompts(args.plan)
        use_raw_prompt = True
        theme_name = theme_key
        if plan_page_size and plan_page_size in config.PAGE_SIZES and args.size == config.DEFAULT_PAGE_SIZE:
            args.size = plan_page_size
        if theme_key in config.THEMES:
            theme_name = config.THEMES[theme_key]["name"]
    elif args.theme:
        theme_key = args.theme
        theme_name = config.THEMES[args.theme]["name"]
        prompts = load_subjects(args.theme)
    else:
        parser.error("--theme is required unless --plan is provided")

    end_idx = min(args.start + args.count, len(prompts))
    prompts = prompts[args.start : end_idx]

    output_dir = config.get_images_dir(theme_key)
    os.makedirs(output_dir, exist_ok=True)

    dims = config.get_page_dims(args.size)
    print(f"Theme: {theme_name}")
    if use_raw_prompt:
        print(f"Plan: {args.plan}")
    print(f"Renderer: {args.renderer}")
    print(f"Page size: {config.PAGE_SIZES[args.size]['label']}")
    print(f"Generating {len(prompts)} coloring pages...")
    print(f"Output: {output_dir}/")
    print()

    def _generate_one(i_prompt):
        i, prompt_text = i_prompt
        page_num = args.start + i + 1
        filename = f"page_{page_num:02d}.png"
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            print(f"[{page_num}/{end_idx}] Skipping (exists): {filename}")
            return True

        display_text = prompt_text[:80] + "..." if len(prompt_text) > 80 else prompt_text
        print(f"[{page_num}/{end_idx}] Generating: {display_text}")

        if use_raw_prompt:
            full_prompt = prompt_text
        else:
            full_prompt = config.BASE_PROMPT.format(age=config.TARGET_AGE, subject=prompt_text)

        ar = dims["bimai_aspect_ratio"] if args.renderer == "bimai" else dims["ai33_aspect_ratio"]
        image = generate_image(full_prompt, renderer=args.renderer, aspect_ratio=ar)

        if image:
            processed = post_process(image, size_key=args.size)
            processed.save(filepath, "PNG", dpi=(config.DPI, config.DPI))
            print(f"  Saved: {filename}")
            return True
        else:
            print(f"  FAILED: Could not generate image")
            return False

    tasks = list(enumerate(prompts))

    if len(tasks) > 1:
        from concurrent.futures import ThreadPoolExecutor
        workers = min(config.MAX_PARALLEL_WORKERS, len(tasks))
        print(f"Running {workers} parallel workers...\n")
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(_generate_one, tasks))
        success_count = sum(1 for r in results if r)
    else:
        success_count = 0
        for task in tasks:
            if _generate_one(task):
                success_count += 1

    print()
    print(f"Done! Generated {success_count}/{len(prompts)} pages")
    print(f"Output directory: {output_dir}/")


if __name__ == "__main__":
    main()
