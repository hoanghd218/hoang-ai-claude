#!/usr/bin/env python3
"""
AI Artist Generate — Nano Banana Pro image generation.

Takes a prompt and generates an image using Gemini Pro image model.

Usage:
    python generate.py "<prompt>" --output <path.png> [options]
"""

import argparse
import sys
import os
from pathlib import Path

# Gemini API setup
CLAUDE_ROOT = Path.home() / '.claude'
sys.path.insert(0, str(CLAUDE_ROOT / 'scripts'))
PROJECT_CLAUDE = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_CLAUDE / 'scripts'))
try:
    from resolve_env import resolve_env
    CENTRALIZED_RESOLVER = True
except ImportError:
    CENTRALIZED_RESOLVER = False
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_CLAUDE.parent / '.env')
        load_dotenv(Path.home() / '.claude' / '.env')
        load_dotenv(Path.home() / '.claude' / 'skills' / '.env')
    except ImportError:
        pass

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

MODEL_ID = "gemini-3.1-flash-image-preview"
ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]


def get_api_key() -> str:
    if CENTRALIZED_RESOLVER:
        return resolve_env('GEMINI_API_KEY', skill='ai-multimodal')
    return os.getenv('GEMINI_API_KEY')


def generate_image(prompt: str, output_path: str, aspect_ratio: str = "1:1",
                   size: str = "2K", verbose: bool = False) -> dict:
    """Generate image using Nano Banana Pro (Gemini Pro image model)."""
    if not GENAI_AVAILABLE:
        return {"status": "error", "error": "google-genai not installed. Run: pip install google-genai"}

    api_key = get_api_key()
    if not api_key:
        return {"status": "error", "error": "GEMINI_API_KEY not found"}

    if verbose:
        print(f"\n[Nano Banana Pro]")
        print(f"  Model: {MODEL_ID}")
        print(f"  Aspect: {aspect_ratio}")
        print(f"  Size: {size}")
        print(f"  Prompt: {prompt[:150]}...")

    try:
        client = genai.Client(api_key=api_key)

        config = types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=size,
            )
        )

        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt],
            config=config
        )

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if hasattr(response, 'candidates') and response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    with open(output_file, 'wb') as f:
                        f.write(part.inline_data.data)
                    if verbose:
                        print(f"  Generated: {output_file}")
                    return {"status": "success", "output": str(output_file), "model": MODEL_ID}

        return {"status": "error", "error": "No image in response"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="AI Artist — Nano Banana Pro image generation")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("--output", "-o", required=True, help="Output image path")
    parser.add_argument("--aspect-ratio", "-ar", choices=ASPECT_RATIOS, default="1:1")
    parser.add_argument("--size", choices=["1K", "2K", "4K"], default="2K")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Show prompt without generating")

    args = parser.parse_args()

    if args.dry_run:
        print(f"[Prompt]\n{args.prompt}\n\n[Dry run — no generation]")
        return

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect_ratio,
        size=args.size,
        verbose=args.verbose
    )

    if result["status"] == "success":
        print(f"✓ Generated: {result['output']}")
    else:
        print(f"✗ Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
