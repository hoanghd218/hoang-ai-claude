#!/usr/bin/env python3
"""
Process raw video clips for short video editing.
Analyzes clips, detects and removes silence gaps (jump cuts),
trims segments, extracts audio, and transcribes with Whisper.

Usage:
    python3 process_raw_clips.py \
        --clips clip1.mp4 clip2.mp4 clip3.mp4 \
        --output-dir ./output/ \
        --silence-threshold -30 \
        --silence-min-duration 0.5 \
        --language vi
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, check=True, capture=True):
    """Run a subprocess command and return result."""
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        print(f"  [WARN] Command failed: {' '.join(str(c) for c in cmd)}", file=sys.stderr)
        if result.stderr:
            print(f"  stderr: {result.stderr[:500]}", file=sys.stderr)
    return result


def ffprobe_info(video_path):
    """Get video metadata using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", str(video_path),
    ]
    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def get_duration(file_path):
    """Get duration of audio/video file in seconds."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0", str(file_path),
    ]
    result = run_cmd(cmd, check=False)
    try:
        return float(result.stdout.strip())
    except (ValueError, AttributeError):
        return 0.0


def detect_silence(audio_path, threshold_db=-30, min_duration=0.5):
    """Detect silence regions using ffmpeg silencedetect filter."""
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={threshold_db}dB:d={min_duration}",
        "-f", "null", "-",
    ]
    result = run_cmd(cmd, check=False)
    stderr = result.stderr or ""

    silences = []
    starts = re.findall(r"silence_start:\s*([\d.]+)", stderr)
    ends = re.findall(r"silence_end:\s*([\d.]+)", stderr)

    for i, start in enumerate(starts):
        end = ends[i] if i < len(ends) else None
        silences.append({
            "start": float(start),
            "end": float(end) if end else None,
            "duration": round(float(end) - float(start), 3) if end else None,
        })

    return silences


def extract_audio(video_path, output_path):
    """Extract audio from video as 16kHz mono WAV (Whisper-compatible)."""
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(output_path),
    ]
    return run_cmd(cmd, check=False)


def trim_video(input_path, output_path, start, end):
    """Trim video segment. Tries stream copy first, falls back to re-encode."""
    duration = end - start
    # Try stream copy (fast, no quality loss)
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start:.3f}",
        "-i", str(input_path),
        "-t", f"{duration:.3f}",
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        str(output_path),
    ]
    result = run_cmd(cmd, check=False)

    if result.returncode != 0:
        # Fallback: re-encode
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start:.3f}",
            "-i", str(input_path),
            "-t", f"{duration:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-avoid_negative_ts", "make_zero",
            str(output_path),
        ]
        run_cmd(cmd, check=True)


def concat_audio_files(audio_paths, output_path):
    """Concatenate multiple audio files using ffmpeg concat demuxer."""
    concat_list = output_path.parent / "_concat_list.txt"
    with open(concat_list, "w") as f:
        for ap in audio_paths:
            f.write(f"file '{ap}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(output_path),
    ]
    run_cmd(cmd, check=True)
    concat_list.unlink(missing_ok=True)


def transcribe_whisper(audio_path, language="vi", model="base"):
    """Transcribe audio using local Whisper CLI with word-level timestamps."""
    output_dir = str(Path(audio_path).parent)
    cmd = [
        "whisper", str(audio_path),
        "--model", model,
        "--language", language,
        "--output_format", "all",
        "--word_timestamps", "True",
        "--output_dir", output_dir,
    ]

    print(f"  Running: whisper --model {model} --language {language} --word_timestamps True")
    result = run_cmd(cmd, check=False, capture=False)

    if result.returncode != 0:
        print("  [ERROR] Whisper transcription failed!", file=sys.stderr)
        return {}

    stem = Path(audio_path).stem
    return {
        "srt": os.path.join(output_dir, f"{stem}.srt"),
        "json": os.path.join(output_dir, f"{stem}.json"),
        "txt": os.path.join(output_dir, f"{stem}.txt"),
    }


def parse_whisper_json(json_path):
    """Parse Whisper JSON output to extract word-level timestamps."""
    if not json_path or not os.path.exists(json_path):
        return []

    with open(json_path) as f:
        data = json.load(f)

    segments = []
    for seg in data.get("segments", []):
        entry = {
            "text": seg.get("text", "").strip(),
            "start": round(seg.get("start", 0), 3),
            "end": round(seg.get("end", 0), 3),
            "words": [],
        }
        for word in seg.get("words", []):
            entry["words"].append({
                "word": word.get("word", "").strip(),
                "start": round(word.get("start", 0), 3),
                "end": round(word.get("end", 0), 3),
            })
        if entry["text"]:
            segments.append(entry)

    return segments


def main():
    parser = argparse.ArgumentParser(
        description="Process raw video clips: analyze, detect silence, trim, transcribe"
    )
    parser.add_argument(
        "--clips", nargs="+", required=True,
        help="Video files in playback order",
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Output directory for processed files",
    )
    parser.add_argument(
        "--silence-threshold", type=float, default=-30,
        help="Silence detection threshold in dB (default: -30)",
    )
    parser.add_argument(
        "--silence-min-duration", type=float, default=0.5,
        help="Minimum silence duration in seconds to cut (default: 0.5)",
    )
    parser.add_argument(
        "--language", default="vi",
        help="Transcription language (default: vi)",
    )
    parser.add_argument(
        "--whisper-model", default="base",
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--keep-edge-padding", type=float, default=0.05,
        help="Seconds of padding to keep at silence boundaries (default: 0.05)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    trimmed_dir = output_dir / "trimmed"
    trimmed_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("  RAW CLIP PROCESSOR")
    print("=" * 60)

    # ── Step 1: Analyze clips ──
    print("\n[Step 1] Analyzing clips...")
    clip_info = []
    for clip_path in args.clips:
        if not os.path.exists(clip_path):
            print(f"  [ERROR] File not found: {clip_path}", file=sys.stderr)
            sys.exit(1)

        info = ffprobe_info(clip_path)
        if not info:
            print(f"  [ERROR] Cannot probe: {clip_path}", file=sys.stderr)
            sys.exit(1)

        duration = float(info.get("format", {}).get("duration", 0))
        video_stream = next(
            (s for s in info.get("streams", []) if s.get("codec_type") == "video"), None
        )
        audio_stream = next(
            (s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None
        )

        clip_data = {
            "path": os.path.abspath(clip_path),
            "filename": os.path.basename(clip_path),
            "duration": round(duration, 3),
            "width": int(video_stream.get("width", 0)) if video_stream else 0,
            "height": int(video_stream.get("height", 0)) if video_stream else 0,
            "has_audio": audio_stream is not None,
            "fps": eval(video_stream.get("r_frame_rate", "30/1")) if video_stream else 30,
            "codec": video_stream.get("codec_name", "unknown") if video_stream else "none",
        }
        clip_info.append(clip_data)
        print(f"  [{clip_data['filename']}] {duration:.1f}s  {clip_data['width']}x{clip_data['height']}  audio={'yes' if clip_data['has_audio'] else 'no'}")

    total_original = sum(c["duration"] for c in clip_info)
    print(f"\n  Total original: {total_original:.1f}s across {len(clip_info)} clips")

    # Save clip info
    with open(output_dir / "clip_info.json", "w") as f:
        json.dump(clip_info, f, indent=2, ensure_ascii=False)

    # ── Step 2: Detect silence per clip ──
    print(f"\n[Step 2] Detecting silence (threshold={args.silence_threshold}dB, min={args.silence_min_duration}s)...")
    all_silence_data = []
    all_keep_segments = []
    pad = args.keep_edge_padding

    for i, clip in enumerate(clip_info):
        if not clip["has_audio"]:
            # No audio — keep entire clip as one segment
            all_keep_segments.append({
                "source_clip": i,
                "source_file": clip["path"],
                "clip_start": 0,
                "clip_end": clip["duration"],
            })
            print(f"  Clip {i+1}: No audio track, keeping full {clip['duration']:.1f}s")
            continue

        # Extract audio for silence detection
        temp_audio = output_dir / f"_temp_audio_{i}.wav"
        extract_audio(clip["path"], temp_audio)

        silences = detect_silence(
            temp_audio,
            threshold_db=args.silence_threshold,
            min_duration=args.silence_min_duration,
        )

        all_silence_data.append({
            "clip_index": i,
            "filename": clip["filename"],
            "silences": silences,
        })

        if not silences:
            all_keep_segments.append({
                "source_clip": i,
                "source_file": clip["path"],
                "clip_start": 0,
                "clip_end": clip["duration"],
            })
            print(f"  Clip {i+1}: No silence found, keeping full {clip['duration']:.1f}s")
        else:
            # Invert silence regions to get keep-regions
            keep_regions = []
            prev_end = 0.0

            for silence in silences:
                seg_end = silence["start"] + pad  # keep a tiny pad before silence
                if seg_end > prev_end + 0.1:  # minimum 0.1s segment
                    keep_regions.append((prev_end, min(seg_end, clip["duration"])))
                prev_end = max((silence["end"] or clip["duration"]) - pad, 0)

            # Final segment after last silence
            if prev_end < clip["duration"] - 0.1:
                keep_regions.append((prev_end, clip["duration"]))

            removed = sum(s["duration"] for s in silences if s["duration"])
            print(f"  Clip {i+1}: {len(silences)} gaps ({removed:.1f}s silence) -> {len(keep_regions)} segments")

            for start, end in keep_regions:
                all_keep_segments.append({
                    "source_clip": i,
                    "source_file": clip["path"],
                    "clip_start": round(start, 3),
                    "clip_end": round(end, 3),
                })

        # Cleanup temp audio
        temp_audio.unlink(missing_ok=True)

    # Save silence data
    with open(output_dir / "silence_gaps.json", "w") as f:
        json.dump(all_silence_data, f, indent=2, ensure_ascii=False)

    print(f"\n  Total segments to keep: {len(all_keep_segments)}")

    # ── Step 3: Trim clips ──
    print(f"\n[Step 3] Trimming {len(all_keep_segments)} segments...")
    trimmed_clips = []
    trimmed_total = 0.0

    for idx, seg in enumerate(all_keep_segments):
        seg_filename = f"seg_{idx:03d}.mp4"
        seg_path = trimmed_dir / seg_filename
        expected_dur = seg["clip_end"] - seg["clip_start"]

        trim_video(seg["source_file"], seg_path, seg["clip_start"], seg["clip_end"])

        # Verify trimmed file
        if not seg_path.exists() or seg_path.stat().st_size < 1000:
            print(f"  [WARN] Segment {seg_filename} too small or missing, skipping")
            continue

        actual_dur = get_duration(seg_path)
        trimmed_total += actual_dur

        trimmed_clips.append({
            "index": idx,
            "path": str(seg_path),
            "filename": seg_filename,
            "duration": round(actual_dur, 3),
            "source_clip": seg["source_clip"],
            "source_start": seg["clip_start"],
            "source_end": seg["clip_end"],
        })
        print(f"  {seg_filename}: {actual_dur:.1f}s (clip {seg['source_clip']+1} @ {seg['clip_start']:.1f}-{seg['clip_end']:.1f}s)")

    saved = total_original - trimmed_total
    print(f"\n  Trimmed: {trimmed_total:.1f}s (removed {saved:.1f}s = {saved/total_original*100:.0f}% silence)")

    # Save timeline
    timeline = {
        "original_duration": round(total_original, 3),
        "trimmed_duration": round(trimmed_total, 3),
        "removed_duration": round(saved, 3),
        "removed_percent": round(saved / total_original * 100, 1) if total_original > 0 else 0,
        "segment_count": len(trimmed_clips),
        "segments": trimmed_clips,
    }
    with open(output_dir / "timeline.json", "w") as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)

    # ── Step 4: Extract & concatenate trimmed audio ──
    print("\n[Step 4] Extracting audio from trimmed segments...")
    audio_parts = []
    for tc in trimmed_clips:
        audio_part = output_dir / f"_audio_{tc['index']:03d}.wav"
        extract_audio(tc["path"], audio_part)
        if audio_part.exists() and audio_part.stat().st_size > 100:
            audio_parts.append(audio_part)

    trimmed_audio = output_dir / "trimmed_audio.wav"
    if len(audio_parts) == 1:
        shutil.copy2(audio_parts[0], trimmed_audio)
    elif len(audio_parts) > 1:
        concat_audio_files(audio_parts, trimmed_audio)
    else:
        print("  [ERROR] No audio extracted!", file=sys.stderr)
        sys.exit(1)

    # Cleanup temp audio parts
    for ap in audio_parts:
        ap.unlink(missing_ok=True)

    print(f"  Combined audio: {get_duration(trimmed_audio):.1f}s")

    # ── Step 5: Transcribe with Whisper ──
    print(f"\n[Step 5] Transcribing with Whisper (model={args.whisper_model}, lang={args.language})...")
    whisper_output = transcribe_whisper(
        trimmed_audio,
        language=args.language,
        model=args.whisper_model,
    )

    # Parse word-level timestamps
    segments_data = parse_whisper_json(whisper_output.get("json"))
    if segments_data:
        with open(output_dir / "segments.json", "w") as f:
            json.dump(segments_data, f, indent=2, ensure_ascii=False)
        print(f"  Transcribed: {len(segments_data)} segments with word-level timing")
    else:
        print("  [WARN] No segments parsed from Whisper output")

    # Copy SRT to output
    srt_src = whisper_output.get("srt")
    srt_dst = output_dir / "transcript.srt"
    if srt_src and os.path.exists(srt_src):
        shutil.copy2(srt_src, srt_dst)
        print(f"  SRT saved: {srt_dst}")

    # ── Summary ──
    print("\n" + "=" * 60)
    print("  PROCESSING COMPLETE")
    print("=" * 60)
    print(f"  Original:  {total_original:.1f}s ({len(clip_info)} clips)")
    print(f"  Trimmed:   {trimmed_total:.1f}s ({len(trimmed_clips)} segments)")
    print(f"  Removed:   {saved:.1f}s ({saved/total_original*100:.0f}% silence)")
    print(f"  Output:    {output_dir}")
    print()
    print("  Files:")
    print(f"    clip_info.json      - Original clip metadata")
    print(f"    silence_gaps.json   - Detected silence regions")
    print(f"    timeline.json       - Trimmed segment timeline")
    print(f"    trimmed/            - Trimmed video segments")
    print(f"    trimmed_audio.wav   - Combined audio")
    print(f"    transcript.srt      - Whisper SRT")
    print(f"    segments.json       - Word-level timestamps")
    print("=" * 60)


if __name__ == "__main__":
    main()
