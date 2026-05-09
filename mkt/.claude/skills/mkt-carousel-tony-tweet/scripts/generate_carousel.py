#!/usr/bin/env python3
"""
Generate tweet-style carousel images with Tony Hoang branding via Nano Banana Pro (ai33.pro).

Supports:
- Text-only prompts (pure TTI)
- Reference avatar image passed as input (image-to-image) for face consistency

Usage:
    python generate_carousel.py --prompt "..." -o out.png [--avatar /path/avatar.png]
    python generate_carousel.py --plan plan.json --out-dir ./out/ [--avatar /path/avatar.png]
"""

import argparse
import json
import mimetypes
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip install requests", file=sys.stderr)
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parents[4]
try:
    from dotenv import load_dotenv
    for p in [PROJECT_ROOT / '.env', Path.home() / '.claude' / '.env']:
        if p.exists():
            load_dotenv(p)
except ImportError:
    pass

AI33_SUBMIT = "https://api.ai33.pro/v1i/task/generate-image"
AI33_STATUS = "https://api.ai33.pro/v1/task"
MODEL_ID = "gemini-3.1-flash-image-preview"
POLL_INTERVAL = 5
POLL_TIMEOUT = 300


def submit_task(prompt, aspect_ratio, resolution, asset_paths=None, model_id=MODEL_ID, verbose=False):
    """Submit AI33 generation task. asset_paths = list of reference image file paths.

    Reference images are attached via multipart 'assets' field (one per image).
    In the prompt, reference them as @img1, @img2, etc. (1-indexed).
    """
    api_key = os.getenv("AI33_KEY") or os.getenv("AI33_API_KEY")
    if not api_key:
        return {"status": "error", "error": "AI33_KEY not found in env"}

    headers = {"xi-api-key": api_key}
    model_params = json.dumps({"aspect_ratio": aspect_ratio, "resolution": resolution})
    data = {
        "prompt": prompt,
        "model_id": model_id,
        "generations_count": "1",
        "model_parameters": model_params,
    }

    files = []
    file_handles = []
    if asset_paths:
        for path in asset_paths:
            p = Path(path)
            if not p.exists():
                return {"status": "error", "error": f"Asset not found: {path}"}
            mime = mimetypes.guess_type(str(p))[0] or "image/png"
            fh = open(p, "rb")
            file_handles.append(fh)
            files.append(("assets", (p.name, fh, mime)))
        if verbose:
            print(f"  [ref] Attaching {len(asset_paths)} asset(s): {', '.join(str(p) for p in asset_paths)}")

    try:
        for attempt in range(3):
            try:
                resp = requests.post(
                    AI33_SUBMIT,
                    headers=headers,
                    data=data,
                    files=files if files else None,
                    verify=False,
                    timeout=180,
                )
                resp.raise_for_status()
                r = resp.json()
                if r.get("success"):
                    return {"status": "ok", "task_id": r["task_id"], "credits": r.get("ec_remain_credits")}
                if verbose:
                    print(f"  submit failed attempt {attempt+1}: {r}")
            except Exception as e:
                if verbose:
                    print(f"  submit error attempt {attempt+1}: {e}")
                time.sleep(2)
            # Re-seek file handles for retry
            for fh in file_handles:
                fh.seek(0)
        return {"status": "error", "error": "Failed to submit task"}
    finally:
        for fh in file_handles:
            fh.close()


def poll_task(task_id, verbose=False):
    api_key = os.getenv("AI33_KEY") or os.getenv("AI33_API_KEY")
    headers = {"Content-Type": "application/json", "xi-api-key": api_key}
    elapsed = 0
    while elapsed < POLL_TIMEOUT:
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
        try:
            r = requests.get(f"{AI33_STATUS}/{task_id}", headers=headers, verify=False, timeout=30).json()
            st = r.get("status")
            if st == "done":
                images = r.get("metadata", {}).get("result_images", [])
                if not images:
                    return {"status": "error", "error": "done but no images"}
                return {"status": "ok", "image_url": images[0].get("imageUrl")}
            if st == "error":
                return {"status": "error", "error": r.get("error_message", "unknown")}
            if verbose and elapsed % 15 == 0:
                print(f"  poll {elapsed}s status={st} progress={r.get('progress', 0)}%")
        except Exception as e:
            if verbose:
                print(f"  poll error: {e}")
    return {"status": "error", "error": f"timeout {POLL_TIMEOUT}s"}


def download(url, path):
    r = requests.get(url, verify=False, timeout=120)
    r.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(r.content)


def generate_one(prompt, out, aspect_ratio="4:5", resolution="2K", assets=None,
                 model_id=MODEL_ID, verbose=False):
    if verbose:
        print(f"\n[{model_id} via AI33]")
        print(f"  Aspect: {aspect_ratio}, Resolution: {resolution}")
        print(f"  Output: {out}")
        print(f"  Prompt ({len(prompt)} chars): {prompt[:180]}...")

    sub = submit_task(prompt, aspect_ratio, resolution, assets, model_id, verbose)
    if sub["status"] != "ok":
        return sub
    if verbose:
        print(f"  Task: {sub['task_id']} (credits: {sub.get('credits')})")

    poll = poll_task(sub["task_id"], verbose)
    if poll["status"] != "ok":
        return poll

    out_path = Path(out)
    download(poll["image_url"], out_path)
    if verbose:
        print(f"  ✓ Saved: {out_path}")
    return {"status": "ok", "output": str(out_path), "task_id": sub["task_id"]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", help="Single image prompt")
    p.add_argument("-o", "--output", help="Output path")
    p.add_argument("--plan", help="JSON plan: {slides: [{prompt, output, assets?}, ...]}")
    p.add_argument("--out-dir", help="Output dir when using --plan")
    p.add_argument("--assets", nargs="+", default=[],
                   help="Reference image paths (1-indexed as @img1, @img2 in prompt). First one should be avatar.")
    p.add_argument("--avatar", help="Shortcut for single avatar reference (equivalent to --assets AVATAR)")
    p.add_argument("--model", default=MODEL_ID,
                   help=f"AI33 model_id (default: {MODEL_ID}). Use 'bytedance-seedream-4.5' for image-to-image.")
    p.add_argument("--aspect-ratio", "-ar", default="4:5",
                   choices=["1:1", "4:5", "9:16", "16:9", "3:4", "4:3"])
    p.add_argument("--resolution", default="2K", choices=["1K", "2K"])
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    # Merge --avatar into --assets (avatar becomes @img1)
    assets = list(args.assets)
    if args.avatar:
        assets.insert(0, args.avatar)

    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except Exception:
        pass

    if args.plan:
        plan = json.loads(Path(args.plan).read_text())
        out_dir = Path(args.out_dir or ".")
        out_dir.mkdir(parents=True, exist_ok=True)
        results = []
        for i, slide in enumerate(plan.get("slides", []), start=1):
            out = slide.get("output") or str(out_dir / f"slide_{i:02d}.png")
            slide_assets = slide.get("assets", assets)  # per-slide override, fall back to global
            slide_model = slide.get("model", args.model)
            res = generate_one(slide["prompt"], out, args.aspect_ratio, args.resolution,
                               slide_assets, slide_model, args.verbose)
            results.append({"slide": i, **res})
            print(json.dumps({"slide": i, **res}, ensure_ascii=False))
        ok = sum(1 for r in results if r["status"] == "ok")
        print(f"\n[Batch] {ok}/{len(results)} succeeded")
        sys.exit(0 if ok == len(results) else 1)

    if not args.prompt or not args.output:
        p.error("Need --prompt + -o, or --plan + --out-dir")

    r = generate_one(args.prompt, args.output, args.aspect_ratio, args.resolution,
                     assets, args.model, args.verbose)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(0 if r["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
