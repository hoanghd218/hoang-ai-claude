#!/usr/bin/env python3
"""
Shared image generation providers for KDP coloring book pipeline.
Supports: AI33, Bimai, NanoPic, Kie.ai.
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import threading

import requests
from PIL import Image

import config


# ── NanoPic Token Pool ───────────────────────────────────────────────
class NanoPickTokenPool:
    """Thread-safe round-robin pool for multiple NANOPIC_ACCESS_TOKENs."""

    def __init__(self):
        raw = os.getenv("NANOPIC_ACCESS_TOKEN", "")
        self._tokens = [t.strip() for t in raw.split(",") if t.strip()]
        self._index = 0
        self._lock = threading.Lock()
        if self._tokens:
            print(f"  NanoPic token pool initialised with {len(self._tokens)} token(s)")
        else:
            print("  Warning: No NANOPIC_ACCESS_TOKEN found in .env")

    @property
    def size(self) -> int:
        return len(self._tokens)

    def next(self) -> str:
        """Return the next token in round-robin order (thread-safe)."""
        with self._lock:
            if not self._tokens:
                raise RuntimeError("No NANOPIC_ACCESS_TOKEN available")
            token = self._tokens[self._index % len(self._tokens)]
            self._index += 1
            return token


# Singleton — created once at module import time
_nanopic_pool: NanoPickTokenPool | None = None


def get_nanopic_pool() -> NanoPickTokenPool:
    global _nanopic_pool
    if _nanopic_pool is None:
        _nanopic_pool = NanoPickTokenPool()
    return _nanopic_pool


def generate_image_ai33(prompt: str, aspect_ratio: str = "1:1") -> Image.Image | None:
    """Generate an image using AI33 API."""
    api_key = os.getenv("AI33_KEY")
    if not api_key:
        print("Error: AI33_KEY not found in .env")
        sys.exit(1)

    headers = {"xi-api-key": api_key}
    model_params = json.dumps({
        "aspect_ratio": aspect_ratio,
        "resolution": config.AI33_RESOLUTION,
    })

    for attempt in range(config.MAX_RETRIES):
        try:
            resp = requests.post(
                config.AI33_API_URL,
                headers=headers,
                data={
                    "prompt": prompt,
                    "model_id": config.AI33_MODEL_ID,
                    "generations_count": "1",
                    "model_parameters": model_params,
                },
            )
            resp.raise_for_status()
            result = resp.json()

            if not result.get("success"):
                print(f"  AI33 submit failed (attempt {attempt + 1}): {result}")
                continue

            task_id = result["task_id"]
            credits_remaining = result.get("ec_remain_credits", "?")
            print(f"  Task submitted: {task_id} (credits remaining: {credits_remaining})")

            elapsed = 0
            while elapsed < config.AI33_POLL_TIMEOUT:
                time.sleep(config.AI33_POLL_INTERVAL)
                elapsed += config.AI33_POLL_INTERVAL

                status_resp = requests.get(
                    f"{config.AI33_STATUS_URL}/{task_id}",
                    headers={"Content-Type": "application/json", "xi-api-key": api_key},
                )
                status_resp.raise_for_status()
                status = status_resp.json()

                if status.get("status") == "done":
                    images = status.get("metadata", {}).get("result_images", [])
                    if not images:
                        print("  Warning: Task done but no images returned")
                        break
                    image_url = images[0].get("imageUrl")
                    if not image_url:
                        print("  Warning: No imageUrl in result")
                        break
                    img_resp = requests.get(image_url)
                    img_resp.raise_for_status()
                    return Image.open(io.BytesIO(img_resp.content))

                elif status.get("status") == "error":
                    print(f"  AI33 error: {status.get('error_message', 'Unknown error')}")
                    break
                else:
                    progress = status.get("progress", 0)
                    if elapsed % 15 == 0:
                        print(f"  Polling... status={status.get('status')} progress={progress}%")

            if elapsed >= config.AI33_POLL_TIMEOUT:
                print(f"  Timeout waiting for AI33 task {task_id}")

        except Exception as e:
            print(f"  Error (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(config.REQUEST_DELAY_SECONDS)

    return None


def generate_image_bimai(prompt: str, aspect_ratio: str = "9:16", resolution: str = "1k") -> Image.Image | None:
    """Generate an image using Bimai API (app.bimai.vn)."""
    api_key = os.getenv("BIMAI_API_KEY")
    if not api_key:
        print("Error: BIMAI_API_KEY not found in .env")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "display_name": config.BIMAI_DISPLAY_NAME,
        "provider": config.BIMAI_PROVIDER,
        "model": config.BIMAI_MODEL,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }

    for attempt in range(config.MAX_RETRIES):
        try:
            resp = requests.post(config.BIMAI_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            result = resp.json()

            if not result.get("succeeded"):
                print(f"  Bimai submit failed (attempt {attempt + 1}): {result}")
                continue

            task_id = result["data"]["task_id"]
            print(f"  Bimai task submitted: {task_id}")

            elapsed = 0
            while elapsed < config.BIMAI_POLL_TIMEOUT:
                time.sleep(config.BIMAI_POLL_INTERVAL)
                elapsed += config.BIMAI_POLL_INTERVAL

                status_resp = requests.get(
                    f"{config.BIMAI_STATUS_URL}/{task_id}",
                    headers=headers,
                )
                status_resp.raise_for_status()
                status = status_resp.json()
                task_data = status.get("data", {})
                task_status = task_data.get("status")

                if task_status == "completed":
                    image_url = task_data.get("image_url")
                    if not image_url:
                        print("  Warning: Task completed but no image_url returned")
                        break
                    img_resp = requests.get(image_url)
                    img_resp.raise_for_status()
                    return Image.open(io.BytesIO(img_resp.content))

                elif task_status == "failed":
                    error_msg = task_data.get("error", "Unknown error")
                    print(f"  Bimai error: {error_msg}")
                    break
                else:
                    if elapsed % 15 == 0:
                        print(f"  Polling... status={task_status}")

            if elapsed >= config.BIMAI_POLL_TIMEOUT:
                print(f"  Timeout waiting for Bimai task {task_id}")

        except Exception as e:
            print(f"  Error (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(config.REQUEST_DELAY_SECONDS)

    return None


def generate_image_nanopic(prompt: str, aspect_ratio: str = "1:1") -> Image.Image | None:
    """Generate an image using NanoPic API (nanoai.pics)."""
    api_key = os.getenv("NANOPIC_API_KEY")
    pool = get_nanopic_pool()
    if not api_key or pool.size == 0:
        print("Error: NANOPIC_API_KEY or NANOPIC_ACCESS_TOKEN not found in .env")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    nanopic_ar = config.NANOPIC_ASPECT_RATIOS.get(aspect_ratio, "IMAGE_ASPECT_RATIO_SQUARE")

    for attempt in range(config.MAX_RETRIES):
        # Rotate token on each attempt so a bad/expired token gets skipped
        access_token = pool.next()
        token_tail = access_token[-10:] if len(access_token) >= 10 else access_token
        try:
            payload = {
                "accessToken": access_token,
                "promptText": prompt,
                "imageUrls": [],
                "aspectRatio": nanopic_ar,
                "imageModel": config.NANOPIC_MODEL,
            }
            resp = requests.post(config.NANOPIC_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            result = resp.json()

            if not result.get("success"):
                print(f"  NanoPic submit failed (token ...{token_tail}): {result}")
                continue

            task_id = result.get("taskId") or result.get("data", {}).get("taskId")
            if not task_id:
                for key in result:
                    if "task" in key.lower() and isinstance(result[key], str):
                        task_id = result[key]
                        break
            if not task_id:
                print(f"  NanoPic submit failed (attempt {attempt + 1}): no taskId in {result}")
                continue

            print(f"  NanoPic task submitted: {task_id}")

            elapsed = 0
            while elapsed < config.NANOPIC_POLL_TIMEOUT:
                time.sleep(config.NANOPIC_POLL_INTERVAL)
                elapsed += config.NANOPIC_POLL_INTERVAL

                status_resp = requests.get(
                    f"{config.NANOPIC_STATUS_URL}?taskId={task_id}",
                    headers=headers,
                )
                status_resp.raise_for_status()
                status = status_resp.json()

                code = status.get("code", "")
                data = status.get("data") or {}

                # Success: code=="success" and data.fifeUrl present
                if code == "success" and data.get("fifeUrl"):
                    image_url = data["fifeUrl"]
                    img_resp = requests.get(image_url)
                    img_resp.raise_for_status()
                    return Image.open(io.BytesIO(img_resp.content))

                # Failure states
                if code in ("error", "failed", "fail"):
                    error_msg = status.get("message", "Unknown error")
                    detail = data.get("error") or {}
                    if detail:
                        error_msg = f"{error_msg} ({detail.get('status', '')}: {detail.get('message', '')})"
                    print(f"  NanoPic error (token ...{token_tail}): {error_msg}")
                    break

                # code="processing" / "pending" / empty — keep polling
                if elapsed % 15 == 0:
                    print(f"  Polling... status={code or 'pending'}")

            if elapsed >= config.NANOPIC_POLL_TIMEOUT:
                print(f"  Timeout waiting for NanoPic task {task_id}")

        except Exception as e:
            print(f"  Error (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(config.REQUEST_DELAY_SECONDS)

    return None


def generate_image_kie(prompt: str, aspect_ratio: str = "3:4") -> Image.Image | None:
    """Generate an image using Kie.ai API."""
    api_key = os.getenv("KIE_API_KEY")
    if not api_key:
        print("Error: KIE_API_KEY not found in .env")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.KIE_MODEL,
        "input": {
            "prompt": prompt,
            "image_input": [],
            "aspect_ratio": aspect_ratio,
            "resolution": config.KIE_RESOLUTION,
            "output_format": "png",
        },
    }

    for attempt in range(config.MAX_RETRIES):
        try:
            resp = requests.post(config.KIE_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            result = resp.json()

            if result.get("code") != 200:
                print(f"  Kie.ai submit failed (attempt {attempt + 1}): {result.get('msg', result)}")
                continue

            task_id = result.get("data", {}).get("taskId")
            if not task_id:
                print(f"  Kie.ai submit failed (attempt {attempt + 1}): no taskId in {result}")
                continue

            print(f"  Kie.ai task submitted: {task_id}")

            elapsed = 0
            while elapsed < config.KIE_POLL_TIMEOUT:
                time.sleep(config.KIE_POLL_INTERVAL)
                elapsed += config.KIE_POLL_INTERVAL

                status_resp = requests.get(
                    f"{config.KIE_STATUS_URL}?taskId={task_id}",
                    headers=headers,
                )
                status_resp.raise_for_status()
                status = status_resp.json()
                task_data = status.get("data", {})
                task_state = task_data.get("state", "")

                if task_state == "success":
                    result_json_str = task_data.get("resultJson", "")
                    if result_json_str:
                        result_json = json.loads(result_json_str)
                        urls = result_json.get("resultUrls", [])
                        if urls:
                            img_resp = requests.get(urls[0])
                            img_resp.raise_for_status()
                            return Image.open(io.BytesIO(img_resp.content))
                    print("  Warning: Kie.ai task succeeded but no result URLs")
                    break

                elif task_state == "failed":
                    fail_msg = task_data.get("failMsg", "Unknown error")
                    print(f"  Kie.ai error: {fail_msg}")
                    break
                else:
                    if elapsed % 15 == 0:
                        print(f"  Polling... state={task_state}")

            if elapsed >= config.KIE_POLL_TIMEOUT:
                print(f"  Timeout waiting for Kie.ai task {task_id}")

        except Exception as e:
            print(f"  Error (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(config.REQUEST_DELAY_SECONDS)

    return None


# --- Dispatcher ---

RENDERERS = {
    "ai33": generate_image_ai33,
    "bimai": generate_image_bimai,
    "nanopic": generate_image_nanopic,
    "kie": generate_image_kie,
}

RENDERER_CHOICES = list(RENDERERS.keys())

DEFAULT_RENDERER = os.getenv("IMAGE_RENDERER", "bimai").lower()
if DEFAULT_RENDERER not in RENDERERS:
    print(f"Warning: IMAGE_RENDERER='{DEFAULT_RENDERER}' in .env is not valid. Using 'bimai'.")
    DEFAULT_RENDERER = "bimai"


def generate_image(
    prompt: str,
    renderer: str | None = None,
    aspect_ratio: str = "1:1",
    resolution: str = "1k",
) -> Image.Image | None:
    """Generate an image using the specified renderer.

    Args:
        prompt: The text prompt for image generation.
        renderer: One of 'ai33', 'bimai', 'nanopic'.
        aspect_ratio: Aspect ratio string (e.g. '1:1', '3:4', '9:16').
        resolution: Resolution hint (only used by bimai).

    Returns:
        PIL Image or None on failure.
    """
    if renderer is None:
        renderer = DEFAULT_RENDERER
    fn = RENDERERS.get(renderer)
    if not fn:
        print(f"Error: Unknown renderer '{renderer}'. Choose from: {RENDERER_CHOICES}")
        sys.exit(1)

    if renderer == "bimai":
        return fn(prompt, aspect_ratio=aspect_ratio, resolution=resolution)
    return fn(prompt, aspect_ratio=aspect_ratio)
