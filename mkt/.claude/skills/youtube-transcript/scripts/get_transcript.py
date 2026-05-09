#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.28.0", "python-dotenv>=1.0.0"]
# ///
"""
Extract transcript from a YouTube video.

Uses DownSub API (api.downsub.com) to fetch transcripts.
Requires DOWNSUB_API_KEY in .env file.

Usage:
    uv run scripts/get_transcript.py <video_id_or_url> [--timestamps]
"""

import sys
import re
import os
import argparse
import json
import requests
from dotenv import load_dotenv


def find_and_load_env():
    """Find and load .env file from project root."""
    # Walk up from script directory to find .env
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):  # search up to 5 levels
        env_path = os.path.join(current, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            return True
        current = os.path.dirname(current)
    # Also try load_dotenv default behavior
    load_dotenv()
    return False


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or return as-is if already an ID."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def build_youtube_url(video_id: str) -> str:
    """Build a full YouTube URL from a video ID."""
    return f"https://www.youtube.com/watch?v={video_id}"


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_srt_timestamp(ts: str) -> float:
    """Parse SRT timestamp (HH:MM:SS,mmm) to seconds."""
    ts = ts.strip().replace(',', '.')
    parts = ts.split(':')
    if len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    return float(ts)


def parse_srt_content(srt_text: str, with_timestamps: bool = False) -> str:
    """Parse SRT format text into plain text or timestamped text."""
    lines = srt_text.strip().split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Skip sequence numbers (just digits)
        if line.isdigit():
            i += 1
            continue
        # Check for timestamp line (contains -->)
        if '-->' in line:
            start_ts = line.split('-->')[0].strip()
            start_seconds = parse_srt_timestamp(start_ts)
            # Collect text lines until empty line or next sequence number
            i += 1
            text_parts = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().isdigit():
                # Skip if it's actually a timestamp line for next entry
                if '-->' in lines[i]:
                    break
                text_parts.append(lines[i].strip())
                i += 1
            text = ' '.join(text_parts)
            if text:
                if with_timestamps:
                    result.append(f"[{format_timestamp(start_seconds)}] {text}")
                else:
                    result.append(text)
            continue
        i += 1
    return '\n'.join(result)


def get_transcript_downsub(video_url: str, api_key: str, with_timestamps: bool = False) -> str:
    """Fetch transcript via DownSub API."""
    url = 'https://api.downsub.com/download'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {'url': video_url, 'lang': 'en'}

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    # Try to get subtitle content from the response
    # DownSub API may return different formats, handle common ones
    if isinstance(data, dict):
        # Check for direct text content
        if 'text' in data:
            text = data['text']
            if with_timestamps:
                return text  # Return as-is if it has timestamps
            # Strip timestamps if present
            return re.sub(r'\[\d{2}:\d{2}(:\d{2})?\]\s*', '', text)

        # Check for SRT-style subtitles in common response fields
        for key in ['srt', 'subtitle', 'subtitles', 'content', 'data']:
            if key in data and isinstance(data[key], str) and data[key].strip():
                content = data[key]
                # If it looks like SRT format, parse it
                if '-->' in content:
                    return parse_srt_content(content, with_timestamps)
                if with_timestamps:
                    return content
                return re.sub(r'\[\d{2}:\d{2}(:\d{2})?\]\s*', '', content)

        # Check for list of subtitle entries
        for key in ['subtitles', 'captions', 'data', 'segments']:
            if key in data and isinstance(data[key], list):
                entries = data[key]
                lines = []
                for entry in entries:
                    text = entry.get('text', entry.get('t', entry.get('content', '')))
                    if with_timestamps:
                        start = entry.get('start', entry.get('s', entry.get('startTime', 0)))
                        lines.append(f"[{format_timestamp(float(start))}] {text}")
                    else:
                        lines.append(str(text))
                if lines:
                    return '\n'.join(lines)

        # If we have download URLs, try to download the first subtitle file
        for key in ['download_urls', 'downloads', 'files']:
            if key in data and isinstance(data[key], list) and data[key]:
                first_url = data[key][0]
                if isinstance(first_url, dict):
                    first_url = first_url.get('url', first_url.get('download_url', ''))
                if first_url:
                    sub_response = requests.get(first_url, timeout=30)
                    sub_response.raise_for_status()
                    content = sub_response.text
                    if '-->' in content:
                        return parse_srt_content(content, with_timestamps)
                    return content

    # If response is a string directly
    if isinstance(data, str):
        if '-->' in data:
            return parse_srt_content(data, with_timestamps)
        return data

    # Fallback: dump the full response for debugging
    raise ValueError(f"Could not extract transcript from DownSub response. Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")


def get_transcript(video_id: str, with_timestamps: bool = False) -> str:
    """Fetch transcript using DownSub API."""
    find_and_load_env()

    api_key = os.environ.get('DOWNSUB_API_KEY')
    if not api_key:
        print("Error: DOWNSUB_API_KEY not found in .env file.", file=sys.stderr)
        print("Please add DOWNSUB_API_KEY=your_key to your .env file.", file=sys.stderr)
        sys.exit(1)

    video_url = build_youtube_url(video_id)
    return get_transcript_downsub(video_url, api_key, with_timestamps)


def main():
    parser = argparse.ArgumentParser(description='Get YouTube video transcript')
    parser.add_argument('video', help='YouTube video URL or video ID')
    parser.add_argument('--timestamps', '-t', action='store_true',
                        help='Include timestamps in output')
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.video)
        transcript = get_transcript(video_id, with_timestamps=args.timestamps)
        print(transcript)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
