#!/usr/bin/env python3
"""Quick test: render 1 image with AI33 renderer."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from image_providers import generate_image_ai33  # noqa: E402


def main() -> int:
    prompt = (
        "black and white coloring book page for adults, cute cozy cat "
        "sitting in a coffee shop window with plants, medium detail, "
        "clean bold outlines, no shading, no gradients, white background"
    )
    out_path = ROOT / "output" / "ai33_test" / "page_01.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[ai33] Generating test image…")
    print(f"  prompt: {prompt[:80]}…")
    t0 = time.time()
    img = generate_image_ai33(prompt, aspect_ratio="3:4")
    elapsed = time.time() - t0

    if img is None:
        print(f"[FAIL] ai33 returned None after {elapsed:.1f}s")
        return 1

    img.save(out_path)
    print(f"[OK] saved -> {out_path} ({img.size[0]}x{img.size[1]}, {elapsed:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
