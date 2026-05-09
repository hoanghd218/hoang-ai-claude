#!/usr/bin/env python3
"""
AI Artist Generate — Multi-provider image generation.

Supports: Nano Banana Pro (Gemini), AI33.

Usage:
    python generate.py "<prompt>" --output <path.png> [options]
    python generate.py "<prompt>" -o out.png --provider ai33 -ar 1:1
"""

import argparse
import io
import json
import sys
import os
import time
from pathlib import Path

# Environment setup
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

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# --- Nano Banana Pro (Gemini) ---

GEMINI_MODEL_ID = "gemini-3.1-flash-image-preview"
ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]

# --- AI33 ---

AI33_API_URL = "https://api.ai33.pro/v1i/task/generate-image"
AI33_STATUS_URL = "https://api.ai33.pro/v1/task"
AI33_MODEL_ID = "gemini-3.1-flash-image-preview"
AI33_RESOLUTION = "2K"
AI33_POLL_INTERVAL = 5
AI33_POLL_TIMEOUT = 300
AI33_MAX_RETRIES = 3

# Resolution mapping for AI33
AI33_RESOLUTIONS = {
    ("1:1", "1K"): "1024x1024",
    ("1:1", "2K"): "1024x1024",
    ("9:16", "1K"): "768x1344",
    ("9:16", "2K"): "768x1344",
    ("16:9", "1K"): "1344x768",
    ("16:9", "2K"): "1344x768",
    ("3:4", "1K"): "768x1024",
    ("3:4", "2K"): "768x1024",
    ("4:3", "1K"): "1024x768",
    ("4:3", "2K"): "1024x768",
}

PROVIDERS = ["nano", "ai33"]


def _get_env(key: str, skill: str = 'ai-multimodal') -> str:
    if CENTRALIZED_RESOLVER:
        return resolve_env(key, skill=skill)
    return os.getenv(key)


def generate_image_nano(prompt: str, output_path: str, aspect_ratio: str = "1:1",
                        size: str = "2K", verbose: bool = False) -> dict:
    """Generate image using Nano Banana Pro (Gemini Pro image model)."""
    if not GENAI_AVAILABLE:
        return {"status": "error", "error": "google-genai not installed. Run: pip install google-genai"}

    api_key = _get_env('GEMINI_API_KEY')
    if not api_key:
        return {"status": "error", "error": "GEMINI_API_KEY not found"}

    if verbose:
        print(f"\n[Nano Banana Pro]")
        print(f"  Model: {GEMINI_MODEL_ID}")
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
            model=GEMINI_MODEL_ID,
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
                    return {"status": "success", "output": str(output_file), "model": GEMINI_MODEL_ID}

        return {"status": "error", "error": "No image in response"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def generate_image_ai33(prompt: str, output_path: str, aspect_ratio: str = "1:1",
                        size: str = "2K", verbose: bool = False) -> dict:
    """Generate image using AI33 API (Grok-2 image model)."""
    if not REQUESTS_AVAILABLE:
        return {"status": "error", "error": "requests not installed. Run: pip install requests"}

    api_key = _get_env('AI33_KEY')
    if not api_key:
        return {"status": "error", "error": "AI33_KEY not found in env"}

    resolution = size if size in ("1K", "2K") else AI33_RESOLUTION

    if verbose:
        print(f"\n[AI33]")
        print(f"  Model: {AI33_MODEL_ID}")
        print(f"  Aspect: {aspect_ratio}")
        print(f"  Resolution: {resolution}")
        print(f"  Prompt: {prompt[:150]}...")

    headers = {"xi-api-key": api_key}
    model_params = json.dumps({
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    })

    for attempt in range(AI33_MAX_RETRIES):
        try:
            resp = requests.post(
                AI33_API_URL,
                headers=headers,
                data={
                    "prompt": prompt,
                    "model_id": AI33_MODEL_ID,
                    "generations_count": "1",
                    "model_parameters": model_params,
                },
                verify=False,
            )
            resp.raise_for_status()
            result = resp.json()

            if not result.get("success"):
                if verbose:
                    print(f"  Submit failed (attempt {attempt + 1}): {result}")
                continue

            task_id = result["task_id"]
            credits_remaining = result.get("ec_remain_credits", "?")
            if verbose:
                print(f"  Task submitted: {task_id} (credits: {credits_remaining})")

            elapsed = 0
            while elapsed < AI33_POLL_TIMEOUT:
                time.sleep(AI33_POLL_INTERVAL)
                elapsed += AI33_POLL_INTERVAL

                status_resp = requests.get(
                    f"{AI33_STATUS_URL}/{task_id}",
                    headers={"Content-Type": "application/json", "xi-api-key": api_key},
                    verify=False,
                )
                status_resp.raise_for_status()
                status = status_resp.json()

                if status.get("status") == "done":
                    images = status.get("metadata", {}).get("result_images", [])
                    if not images:
                        return {"status": "error", "error": "Task done but no images returned"}
                    image_url = images[0].get("imageUrl")
                    if not image_url:
                        return {"status": "error", "error": "No imageUrl in result"}

                    img_resp = requests.get(image_url, verify=False)
                    img_resp.raise_for_status()

                    output_file = Path(output_path)
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_file, 'wb') as f:
                        f.write(img_resp.content)
                    if verbose:
                        print(f"  Generated: {output_file}")
                    return {"status": "success", "output": str(output_file), "model": AI33_MODEL_ID}

                elif status.get("status") == "error":
                    error_msg = status.get("error_message", "Unknown error")
                    return {"status": "error", "error": f"AI33 task error: {error_msg}"}

                else:
                    if verbose and elapsed % 15 == 0:
                        progress = status.get("progress", 0)
                        print(f"  Polling... status={status.get('status')} progress={progress}%")

            return {"status": "error", "error": f"Timeout ({AI33_POLL_TIMEOUT}s) waiting for AI33 task {task_id}"}

        except Exception as e:
            if verbose:
                print(f"  Error (attempt {attempt + 1}/{AI33_MAX_RETRIES}): {e}")
            if attempt < AI33_MAX_RETRIES - 1:
                time.sleep(2)

    return {"status": "error", "error": f"AI33 failed after {AI33_MAX_RETRIES} attempts"}


# --- Dispatcher ---

_GENERATORS = {
    "nano": generate_image_nano,
    "ai33": generate_image_ai33,
}


def generate_image(prompt: str, output_path: str, aspect_ratio: str = "1:1",
                   size: str = "2K", verbose: bool = False, provider: str = "nano") -> dict:
    """Generate image using the specified provider."""
    fn = _GENERATORS.get(provider)
    if not fn:
        return {"status": "error", "error": f"Unknown provider '{provider}'. Choose from: {PROVIDERS}"}
    return fn(prompt, output_path, aspect_ratio=aspect_ratio, size=size, verbose=verbose)


def main():
    parser = argparse.ArgumentParser(description="AI Artist — Multi-provider image generation")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("--output", "-o", required=True, help="Output image path")
    parser.add_argument("--aspect-ratio", "-ar", choices=ASPECT_RATIOS, default="1:1")
    parser.add_argument("--size", choices=["1K", "2K", "4K"], default="2K")
    parser.add_argument("--provider", "-p", choices=PROVIDERS, default="nano",
                        help="Image provider: nano (Gemini), ai33 (Grok-2)")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Show prompt without generating")

    args = parser.parse_args()

    if args.dry_run:
        print(f"[Provider: {args.provider}]\n[Prompt]\n{args.prompt}\n\n[Dry run — no generation]")
        return

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect_ratio,
        size=args.size,
        verbose=args.verbose,
        provider=args.provider,
    )

    if result["status"] == "success":
        print(f"✓ Generated: {result['output']} (provider: {args.provider})")
    else:
        print(f"✗ Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
