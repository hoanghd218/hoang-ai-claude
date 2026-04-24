#!/usr/bin/env python3
"""
Generate a complete coloring book plan using Gemini API (text only).
Outputs SEO title, subtitle, description, keywords, cover prompt,
and interior page prompts — all saved as JSON + compatible prompt file.
"""

import argparse
import json
import os
import re
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

import config

load_dotenv()


def get_client():
    """Initialize Gemini API client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        print("Copy .env.example to .env and add your API key")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def build_prompt(concept: str, audience: str, pages: int) -> str:
    """Build the super prompt for Gemini based on audience type."""
    if audience == "adults":
        return f"""Generate a complete adult-friendly coloring book package based on the concept below, but do not generate any images; output text only.
Concept: {concept}
Number of coloring pages: {pages}

All prompts must be written specifically for image generation and must later create final illustrations, but for now only text should be produced.
Every coloring page prompt must follow a refined "cute cozy medium-detail" adult aesthetic with complete, layered scenes that never feel empty, but all details must remain clean, bold, and easy to color.
Absolutely avoid dense clusters of small shapes; all vegetation, plants, flowers must be drawn using large, simple, stylized shapes with wide line spacing.
Characters must maintain consistent kawaii proportions and expressive poses.
CRITICAL: Every prompt MUST include this instruction: "The illustration must NOT have any border, frame, or rectangular outline around the edges. The artwork extends naturally with NO enclosing box or boundary line."

Output format (respond ONLY with this JSON, no other text):
{{
  "title": "catchy SEO-friendly title",
  "subtitle": "descriptive subtitle",
  "description": "3-5 sentence commercial description for Amazon KDP emphasizing cozy charm and relaxation",
  "keywords": ["keyword1", "keyword2", ... 7 keywords],
  "cover_prompt": "full-color cover illustration prompt that includes title/subtitle text, warm premium cozy aesthetic, states 'Coloring Book for Adults'",
  "page_prompts": ["prompt1", "prompt2", ... {pages} prompts, each describing a finished black-and-white coloring page with medium detail, large clear decorative shapes, cozy fully developed scenes]
}}"""
    else:
        return f"""Generate a complete children's coloring book package based on the concept below, but do not generate any images; output text only.
Concept: {concept}
Target age: 6-12
Number of coloring pages: {pages}

All prompts must be written specifically for image generation. Each coloring page must be a black-and-white line art page with:
- Bold, thick, clean outlines suitable for children ages 6-12
- Simple enough for kids to color with crayons or markers
- Single subject centered on page, filling most of the space
- NO shading, NO gradients, NO gray tones
- White background, no borders or frames
- Cute, friendly, appealing style

Output format (respond ONLY with this JSON, no other text):
{{
  "title": "catchy SEO-friendly title with 'for Kids Ages 6-12'",
  "subtitle": "descriptive subtitle",
  "description": "3-5 sentence commercial description for Amazon KDP emphasizing fun and creativity for children",
  "keywords": ["keyword1", "keyword2", ... 7 keywords],
  "cover_prompt": "full-color vibrant cover illustration prompt, cartoon style, eye-catching, NO text in image, states 'Coloring Book for Kids Ages 6-12'",
  "page_prompts": ["prompt1", "prompt2", ... {pages} prompts, each describing a single cute subject for a children's coloring page]
}}"""


def parse_json_response(text: str) -> dict:
    """Parse JSON from Gemini response, handling possible markdown code fences."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response:\n{text[:500]}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a complete coloring book plan using Gemini API"
    )
    parser.add_argument(
        "--concept",
        required=True,
        help="Free text describing the book concept (e.g. 'cozy cats in a cafe setting')",
    )
    parser.add_argument(
        "--audience",
        default="kids",
        choices=["kids", "adults"],
        help="Target audience (default: kids)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=30,
        help="Number of interior coloring pages (default: 30)",
    )
    parser.add_argument(
        "--theme-key",
        required=True,
        help="Short snake_case key for this theme (e.g. cozy_cat_cafe)",
    )
    args = parser.parse_args()

    # Validate theme key format
    if not re.match(r"^[a-z][a-z0-9_]*$", args.theme_key):
        print("Error: --theme-key must be snake_case (lowercase letters, digits, underscores)")
        sys.exit(1)

    print(f"Planning coloring book...")
    print(f"  Concept:  {args.concept}")
    print(f"  Audience: {args.audience}")
    print(f"  Pages:    {args.pages}")
    print(f"  Theme key: {args.theme_key}")
    print()

    # Build prompt and call Gemini
    client = get_client()
    prompt = build_prompt(args.concept, args.audience, args.pages)

    print("Calling Gemini API for book plan (text only)...")
    try:
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT"],
            ),
        )
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

    # Extract text from response
    response_text = ""
    for part in response.parts:
        if part.text is not None:
            response_text += part.text

    if not response_text.strip():
        print("Error: Empty response from Gemini API")
        sys.exit(1)

    # Parse JSON
    plan_data = parse_json_response(response_text)

    # Validate required fields
    required_fields = ["title", "subtitle", "description", "keywords", "cover_prompt", "page_prompts"]
    for field in required_fields:
        if field not in plan_data:
            print(f"Error: Missing required field '{field}' in Gemini response")
            sys.exit(1)

    # Add metadata
    plan_data["theme_key"] = args.theme_key
    plan_data["audience"] = args.audience

    # Reorder so theme_key and audience come first
    ordered = {
        "theme_key": plan_data["theme_key"],
        "audience": plan_data["audience"],
        "title": plan_data["title"],
        "subtitle": plan_data["subtitle"],
        "description": plan_data["description"],
        "keywords": plan_data["keywords"],
        "cover_prompt": plan_data["cover_prompt"],
        "page_prompts": plan_data["page_prompts"],
    }

    # Save JSON plan
    book_dir = config.get_book_dir(args.theme_key)
    os.makedirs(book_dir, exist_ok=True)
    json_path = config.get_plan_path(args.theme_key)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)
    print(f"Saved plan JSON: {json_path}")

    # Save prompts text file (compatible with generate_images.py)
    prompts_path = config.get_prompts_path(args.theme_key)
    with open(prompts_path, "w", encoding="utf-8") as f:
        for prompt_line in ordered["page_prompts"]:
            f.write(prompt_line.strip() + "\n")
    print(f"Saved prompts file: {prompts_path}")

    # Print summary
    print()
    print("=" * 60)
    print("BOOK PLAN SUMMARY")
    print("=" * 60)
    print(f"Title:    {ordered['title']}")
    print(f"Subtitle: {ordered['subtitle']}")
    print()
    print(f"Description:")
    print(f"  {ordered['description']}")
    print()
    print(f"Keywords: {', '.join(ordered['keywords'])}")
    print()
    print(f"Cover prompt:")
    print(f"  {ordered['cover_prompt'][:150]}...")
    print()
    print(f"Page prompts: {len(ordered['page_prompts'])} prompts generated")
    for i, p in enumerate(ordered["page_prompts"][:5], 1):
        print(f"  {i}. {p[:80]}...")
    if len(ordered["page_prompts"]) > 5:
        print(f"  ... and {len(ordered['page_prompts']) - 5} more")
    print()

    # Print instructions for registering theme in config
    print("=" * 60)
    print("TO REGISTER THIS THEME, add to config.py THEMES dict:")
    print("=" * 60)
    print(f"""
    "{args.theme_key}": {{
        "name": "{ordered['title']}",
        "book_title": "{ordered['title']}",
        "prompt_file": "prompts/{args.theme_key}.txt",
    }},
""")
    print("Then generate images with:")
    print(f"  python generate_images.py --theme {args.theme_key} --count {len(ordered['page_prompts'])}")


if __name__ == "__main__":
    main()
