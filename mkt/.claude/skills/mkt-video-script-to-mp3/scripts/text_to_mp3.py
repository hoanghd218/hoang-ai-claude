# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
"""Convert text to MP3 using MiniMax TTS API (speech-2.8-hd).

Usage:
    uv run scripts/text_to_mp3.py "Your text here" -o output.mp3
    uv run scripts/text_to_mp3.py --file script.txt -o output.mp3
    uv run scripts/text_to_mp3.py "Text" --voice_id custom_voice_id -o output.mp3
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).resolve().parents[4]  # .claude/skills/skill-name/scripts -> project root
load_dotenv(_project_root / ".env")

API_URL = "https://api.minimax.io/v1/t2a_v2"
DEFAULT_VOICE_ID = "moss_audio_c56d6120-ef9c-11f0-9649-8ee40147f116"
DEFAULT_MODEL = "speech-2.8-hd"
DEFAULT_SPEED = 1.08


def text_to_mp3(
    text: str,
    output_path: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    speed: float = DEFAULT_SPEED,
    vol: float = 1.0,
    pitch: int = 0,
    language_boost: str = "Vietnamese",
) -> dict:
    """Call MiniMax TTS API and save MP3 to output_path."""
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        print("Error: MINIMAX_API_KEY not found in .env", file=sys.stderr)
        sys.exit(1)

    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
        "language_boost": language_boost,
        "output_format": "hex",
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"Sending {len(text)} chars to MiniMax TTS ({model})...")
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    # Check for API errors
    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        print(f"API Error: {base_resp.get('status_msg', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    # Decode hex audio and write to file
    audio_hex = data["data"]["audio"]
    audio_bytes = bytes.fromhex(audio_hex)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(audio_bytes)

    extra = data.get("extra_info", {})
    duration_ms = extra.get("audio_length", 0)
    size_bytes = extra.get("audio_size", len(audio_bytes))
    chars_used = extra.get("usage_characters", len(text))

    print(f"Saved: {out}")
    print(f"Duration: {duration_ms / 1000:.1f}s | Size: {size_bytes / 1024:.1f}KB | Chars: {chars_used}")

    return {
        "output_path": str(out),
        "duration_ms": duration_ms,
        "size_bytes": size_bytes,
        "chars_used": chars_used,
        "trace_id": data.get("trace_id"),
    }


def main():
    parser = argparse.ArgumentParser(description="MiniMax TTS: text to MP3")
    parser.add_argument("text", nargs="?", help="Text to convert")
    parser.add_argument("--file", "-f", help="Read text from file instead")
    parser.add_argument("--output", "-o", required=True, help="Output MP3 path")
    parser.add_argument("--voice_id", default=DEFAULT_VOICE_ID, help=f"Voice ID (default: {DEFAULT_VOICE_ID})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model (default: {DEFAULT_MODEL})")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED, help=f"Speed (default: {DEFAULT_SPEED})")
    parser.add_argument("--vol", type=float, default=1.0, help="Volume 0-10 (default: 1.0)")
    parser.add_argument("--pitch", type=int, default=0, help="Pitch -12 to 12 (default: 0)")
    parser.add_argument("--language_boost", default="Vietnamese", help="Language boost (default: Vietnamese)")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8").strip()
    elif args.text:
        text = args.text
    else:
        parser.error("Provide text as argument or --file")

    if not text:
        parser.error("Text is empty")

    result = text_to_mp3(
        text=text,
        output_path=args.output,
        voice_id=args.voice_id,
        model=args.model,
        speed=args.speed,
        vol=args.vol,
        pitch=args.pitch,
        language_boost=args.language_boost,
    )

    # Print JSON result for programmatic use
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
