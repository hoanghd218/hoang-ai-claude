#!/usr/bin/env python3
"""
B-Roll Screenshot & Video Capture — iPhone 15 Pro mobile responsive.
Uses Playwright Chromium with mobile emulation.

Usage:
  python3 capture.py screenshot --urls "URL1,URL2" --names "name1,name2" --output-dir ./assets
  python3 capture.py multiscreenshot --urls "URL1" --names "name1" --output-dir ./assets --count 5 --total-scroll 3000
  python3 capture.py video --urls "URL1" --names "name1" --output-dir ./assets --scroll-px 1500 --duration 8
"""

import argparse
import os
import sys
from playwright.sync_api import sync_playwright

IPHONE_CONFIG = {
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.5 Mobile/15E148 Safari/604.1"
    ),
    "viewport": {"width": 393, "height": 852},
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
}


def capture_screenshot(p, url, name, output_dir, wait_sec):
    """Capture a single mobile screenshot."""
    browser = p.chromium.launch()
    context = browser.new_context(**IPHONE_CONFIG)
    page = context.new_page()

    print(f"  Loading {url}")
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        # Fallback: some sites never reach networkidle, just wait for load
        try:
            page.goto(url, wait_until="load", timeout=30000)
        except Exception:
            pass
    page.wait_for_timeout(int(wait_sec * 1000))

    dest = os.path.join(output_dir, f"{name}.png")
    page.screenshot(path=dest)
    print(f"  -> {dest}")

    context.close()
    browser.close()
    return dest


def capture_multiscreenshot(p, url, name, output_dir, count, total_scroll, wait_sec):
    """Load page once and capture multiple screenshots at evenly-spaced scroll positions."""
    browser = p.chromium.launch()
    context = browser.new_context(**IPHONE_CONFIG)
    page = context.new_page()

    print(f"  Loading {url}")
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        try:
            page.goto(url, wait_until="load", timeout=30000)
        except Exception:
            pass
    page.wait_for_timeout(int(wait_sec * 1000))

    results = []
    step = total_scroll // (count - 1) if count > 1 else 0
    for i in range(count):
        offset = step * i
        page.evaluate(f"window.scrollTo(0, {offset})")
        page.wait_for_timeout(300)
        dest = os.path.join(output_dir, f"{name}-{i+1:02d}.png")
        page.screenshot(path=dest)
        print(f"  -> {dest} (scroll {offset}px)")
        results.append(dest)

    context.close()
    browser.close()
    return results


def capture_video(p, url, name, output_dir, scroll_px, duration, wait_sec):
    """Record a smooth-scroll b-roll video."""
    duration = min(duration, 10)  # cap at 10s
    # Use 360x640 viewport (9:16 at CSS level) so 3x scale = 1080x1920 exact
    video_config = {**IPHONE_CONFIG, "viewport": {"width": 360, "height": 640}}
    browser = p.chromium.launch()
    context = browser.new_context(
        **video_config,
        record_video_dir=output_dir,
        record_video_size={"width": 1080, "height": 1920},
    )
    page = context.new_page()

    print(f"  Loading {url}")
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        try:
            page.goto(url, wait_until="load", timeout=30000)
        except Exception:
            pass
    page.wait_for_timeout(int(wait_sec * 1000))

    # Smooth scroll: divide into small steps over `duration` seconds
    # Reserve 1.5s at start and 1.5s at end for static view
    scroll_time = max(duration - 3, 2)
    steps = int(scroll_time * 10)  # 10 steps per second
    step_px = scroll_px / steps

    for _ in range(steps):
        page.evaluate(f"window.scrollBy(0, {step_px})")
        page.wait_for_timeout(100)

    page.wait_for_timeout(int(wait_sec * 1000))

    video_path = page.video.path()
    context.close()
    browser.close()

    dest = os.path.join(output_dir, f"{name}-broll.webm")
    if os.path.exists(video_path) and os.path.abspath(video_path) != os.path.abspath(dest):
        os.rename(video_path, dest)
    print(f"  -> {dest}")
    return dest


def main():
    parser = argparse.ArgumentParser(description="Mobile b-roll capture")
    parser.add_argument("mode", choices=["screenshot", "multiscreenshot", "video"], help="Capture mode")
    parser.add_argument("--urls", required=True, help="Comma-separated URLs")
    parser.add_argument("--names", required=True, help="Comma-separated output names")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--scroll-px", type=int, default=1500, help="Pixels to scroll (video mode)")
    parser.add_argument("--duration", type=int, default=8, help="Video duration in seconds (max 10)")
    parser.add_argument("--wait", type=float, default=1.5, help="Seconds to wait after page load")
    parser.add_argument("--count", type=int, default=5, help="Number of screenshots (multiscreenshot mode)")
    parser.add_argument("--total-scroll", type=int, default=3000, help="Total scroll distance in px (multiscreenshot mode)")

    args = parser.parse_args()
    urls = [u.strip() for u in args.urls.split(",")]
    names = [n.strip() for n in args.names.split(",")]

    if len(urls) != len(names):
        print(f"Error: {len(urls)} URLs but {len(names)} names — must match", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    with sync_playwright() as p:
        results = []
        for url, name in zip(urls, names):
            print(f"[{args.mode}] {name}")
            if args.mode == "screenshot":
                r = capture_screenshot(p, url, name, args.output_dir, args.wait)
                results.append(r)
            elif args.mode == "multiscreenshot":
                r = capture_multiscreenshot(p, url, name, args.output_dir, args.count, args.total_scroll, args.wait)
                results.extend(r)
            else:
                r = capture_video(p, url, name, args.output_dir, args.scroll_px, args.duration, args.wait)
                results.append(r)

    print(f"\nDone! {len(results)} file(s) saved to {args.output_dir}")


if __name__ == "__main__":
    main()
