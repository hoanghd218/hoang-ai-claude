#!/usr/bin/env python3
"""Download a video URL (YouTube / IG / TikTok / etc) via yt-dlp and transcribe
with local Whisper, then emit a JSON metadata summary to stdout.

Reuses:
  - yt-dlp (via `uvx yt-dlp`) for download
  - openai-whisper (via `uvx --from openai-whisper whisper`) for transcription
  - ffmpeg (system) — required by Whisper for audio decode

Usage:
    python3 download_and_transcribe.py --url <URL> [--output-dir <DIR>] [--model base]

Output (stdout, one JSON object):
    {
      "url": "...",
      "source_title": "...",
      "duration_sec": 80,
      "language": "en",
      "transcript_text": "full plain text",
      "transcript_path": "/abs/path/video.txt",
      "srt_path": "/abs/path/video.srt",
      "mp4_path": "/abs/path/video.mp4",
      "output_dir": "/abs/path"
    }

Side effects: writes metadata.json + video.mp4 + video.txt + video.srt into output_dir.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def slugify(url: str) -> str:
    m = re.search(r"([A-Za-z0-9_-]{8,})(?:/?\?|/?$|\?)", url)
    return (m.group(1) if m else "video")[:16]


def download(url: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "uvx", "yt-dlp",
        "--no-playlist",
        "-f", "best[ext=mp4]/best",
        "-o", str(out_dir / "video.%(ext)s"),
        "--write-info-json",
        url,
    ]
    proc = run(cmd, check=False)
    if proc.returncode != 0:
        sys.exit(f"yt-dlp failed: {proc.stderr[-500:]}")
    mp4 = next(iter(out_dir.glob("video.*")), None)
    # Prefer .mp4; fall back to whatever yt-dlp saved
    mp4 = out_dir / "video.mp4" if (out_dir / "video.mp4").exists() else mp4
    if not mp4 or not mp4.exists():
        sys.exit(f"download succeeded but no video file in {out_dir}")
    return mp4


def transcribe(video_path: Path, model: str) -> tuple[Path, Path, str]:
    """Run Whisper, return (txt_path, srt_path, detected_language)."""
    cmd = [
        "uvx", "--from", "openai-whisper", "whisper",
        str(video_path),
        "--model", model,
        "--output_dir", str(video_path.parent),
        "--output_format", "txt",
        "--output_format", "srt",
    ]
    proc = run(cmd, check=False)
    if proc.returncode != 0:
        sys.exit(f"whisper failed: {proc.stderr[-500:]}")
    # Whisper prints "Detected language: English" to stderr (or stdout depending on version)
    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    lang_match = re.search(r"Detected language:\s*(\w+)", combined)
    lang = (lang_match.group(1).lower() if lang_match else "unknown")
    stem = video_path.stem
    return (video_path.parent / f"{stem}.txt", video_path.parent / f"{stem}.srt", lang)


def read_info(out_dir: Path) -> dict:
    info_path = out_dir / "video.info.json"
    if not info_path.exists():
        return {}
    try:
        return json.loads(info_path.read_text())
    except Exception:
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--output-dir", help="Default: /tmp/videosrc-<slug>")
    ap.add_argument("--model", default="base", help="Whisper model size (default: base)")
    args = ap.parse_args()

    out_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.gettempdir()) / f"videosrc-{slugify(args.url)}"
    out_dir = out_dir.resolve()

    mp4 = download(args.url, out_dir)
    txt_path, srt_path, lang = transcribe(mp4, args.model)

    transcript_text = txt_path.read_text().strip() if txt_path.exists() else ""
    info = read_info(out_dir)

    summary = {
        "url": args.url,
        "source_title": info.get("title") or info.get("fulltitle") or "",
        "duration_sec": int(info.get("duration") or 0),
        "language": lang,
        "transcript_text": transcript_text,
        "transcript_path": str(txt_path),
        "srt_path": str(srt_path),
        "mp4_path": str(mp4),
        "output_dir": str(out_dir),
    }

    (out_dir / "metadata.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
