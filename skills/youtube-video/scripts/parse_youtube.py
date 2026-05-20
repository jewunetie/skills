#!/usr/bin/env python3
"""
YouTube video transcript extraction and processing.

Handles:
- Sliding-window deduplication for YouTube auto-captions
- HTML entity decoding
- Speaker diarization from >> markers
- Sentence-level chunking with configurable interval
- Metadata extraction
- Whisper fallback transcription

Usage:
    # Full pipeline: download subs + parse
    python3 parse_youtube.py "VIDEO_URL"

    # Parse an existing VTT file
    python3 parse_youtube.py --vtt /tmp/yt_subs.en.vtt

    # Full pipeline with custom options
    python3 parse_youtube.py "VIDEO_URL" --lang es --chunk-seconds 60 --output /tmp/transcript.txt

    # Metadata only
    python3 parse_youtube.py "VIDEO_URL" --metadata-only

    # Whisper fallback (when no subtitles available)
    python3 parse_youtube.py "VIDEO_URL" --whisper --whisper-model base
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# VTT Parsing
# ---------------------------------------------------------------------------

def parse_vtt_raw(filepath):
    """Parse a VTT file into raw (timestamp, text) entries."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    entries = []
    current_start = None
    current_text = []

    for line in content.split("\n"):
        line = line.strip()
        ts_match = re.match(
            r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})", line
        )
        if ts_match:
            if current_start and current_text:
                text = " ".join(current_text).strip()
                text = re.sub(r"<[^>]+>", "", text)  # strip VTT formatting tags
                text = html.unescape(text)  # decode &gt; &amp; etc.
                if text:
                    entries.append((current_start, text))
            current_start = ts_match.group(1)
            current_text = []
        elif (
            line
            and not line.startswith("WEBVTT")
            and not line.startswith("Kind:")
            and not line.startswith("Language:")
            and not re.match(r"^\d+$", line)
        ):
            current_text.append(line)

    # flush last entry
    if current_start and current_text:
        text = " ".join(current_text).strip()
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
        if text:
            entries.append((current_start, text))

    return entries


def dedup_sliding_window(entries):
    """Extract only new text from YouTube's sliding-window auto-captions.

    YouTube auto-captions repeat previous text in each new entry. For example:
        Entry 1: "Hello world"
        Entry 2: "Hello world how are you"
        Entry 3: "how are you I am fine"

    This function extracts only the new portion from each entry.
    """
    if not entries:
        return []

    result = []
    prev_text = ""

    for timestamp, text in entries:
        if not prev_text:
            result.append((timestamp, text))
            prev_text = text
            continue

        # Find the longest suffix of prev_text that is a prefix of text
        new_part = text
        for i in range(min(len(prev_text), len(text)), 0, -1):
            if text.startswith(prev_text[-i:]):
                new_part = text[i:].strip()
                break

        if new_part and new_part != prev_text:
            result.append((timestamp, new_part))
        prev_text = text

    return result


def is_auto_caption(entries):
    """Detect if entries are auto-generated (heavy duplication pattern)."""
    if len(entries) < 10:
        return False
    # Sample consecutive pairs and check for substring overlap
    overlap_count = 0
    sample_size = min(50, len(entries) - 1)
    for i in range(sample_size):
        a = entries[i][1]
        b = entries[i + 1][1]
        if a in b or b in a:
            overlap_count += 1
    return overlap_count / sample_size > 0.3


# ---------------------------------------------------------------------------
# Timestamp Utilities
# ---------------------------------------------------------------------------

def ts_to_seconds(ts):
    """Convert HH:MM:SS.mmm to float seconds."""
    h, m, rest = ts.split(":")
    s = float(rest)
    return int(h) * 3600 + int(m) * 60 + s


def seconds_to_display(sec):
    """Convert float seconds to human-readable timestamp."""
    sec = int(sec)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------------------
# Chunking and Speaker Detection
# ---------------------------------------------------------------------------

def chunk_entries(entries, chunk_seconds=30):
    """Merge entries into sentence-level chunks at roughly chunk_seconds intervals.

    Breaks on sentence boundaries (. ? ! ") when the chunk is at least
    chunk_seconds long, or forces a break at 1.5x chunk_seconds.
    """
    if not entries:
        return []

    chunks = []
    current_parts = []
    chunk_start_sec = None

    for timestamp, text in entries:
        sec = ts_to_seconds(timestamp)
        if chunk_start_sec is None:
            chunk_start_sec = sec
        current_parts.append(text)

        combined = " ".join(current_parts)
        elapsed = sec - chunk_start_sec
        at_sentence = combined.rstrip().endswith((".", "?", "!", '"'))
        force_break = elapsed >= chunk_seconds * 1.5

        if (elapsed >= chunk_seconds * 0.8 and at_sentence) or force_break:
            chunks.append((seconds_to_display(chunk_start_sec), combined))
            current_parts = []
            chunk_start_sec = None

    # flush remainder
    if current_parts and chunk_start_sec is not None:
        chunks.append((seconds_to_display(chunk_start_sec), " ".join(current_parts)))

    return chunks


def detect_speakers(chunks):
    """Detect speaker changes from >> markers in auto-captions.

    NOTE: This is a utility function available for manual use. The main pipeline
    preserves >> markers in the output text rather than replacing them with labels,
    since auto-caption speaker detection is unreliable. Call this explicitly if you
    want to strip >> markers and count speaker turns.

    Returns chunks with >> markers removed and text cleaned.
    """
    labeled = []
    for timestamp, text in chunks:
        parts = re.split(r"\s*>>\s*", text)
        cleaned_parts = [p.strip() for p in parts if p.strip()]
        labeled.append((timestamp, " ".join(cleaned_parts)))
    return labeled


def count_speakers(text):
    """Count approximate number of speaker changes in full text."""
    return text.count(">>")


# ---------------------------------------------------------------------------
# yt-dlp Wrappers
# ---------------------------------------------------------------------------

YT_DLP_BASE = ["yt-dlp", "--no-check-certificates"]


def get_metadata(url):
    """Fetch video metadata without downloading."""
    cmd = YT_DLP_BASE + [
        "--extractor-args", "youtube:player_client=android",
        "--dump-json", "--skip-download", url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"ERROR: metadata fetch failed:\n{result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: failed to parse metadata JSON: {e}", file=sys.stderr)
        return None


def download_subtitles(url, lang="en", output_prefix="/tmp/yt_subs"):
    """Download subtitles (manual preferred, auto-generated as fallback).

    Returns the path to the downloaded VTT file, or None on failure.
    """
    cmd = YT_DLP_BASE + [
        "--extractor-args", "youtube:player_client=android",
        "--write-subs", "--write-auto-sub",
        "--sub-lang", lang,
        "--skip-download", "--sub-format", "vtt",
        "-o", output_prefix,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    # Check for the output file (could be .en.vtt or .<lang>.vtt)
    expected_path = f"{output_prefix}.{lang}.vtt"
    if os.path.isfile(expected_path):
        return expected_path

    # Try glob for any VTT that was produced
    parent = Path(output_prefix).parent
    prefix = Path(output_prefix).name
    for f in parent.glob(f"{prefix}*.vtt"):
        return str(f)

    print(f"ERROR: no subtitle file produced.", file=sys.stderr)
    if result.stderr:
        # Surface the most useful error lines
        for line in result.stderr.split("\n"):
            if "ERROR" in line or "WARNING" in line:
                print(f"  {line.strip()}", file=sys.stderr)
    if result.stdout:
        for line in result.stdout.split("\n"):
            if "ERROR" in line:
                print(f"  {line.strip()}", file=sys.stderr)

    return None


def download_audio(url, output_path="/tmp/yt_audio.wav"):
    """Download audio for Whisper transcription."""
    cmd = YT_DLP_BASE + [
        "--extractor-args", "youtube:player_client=android",
        "--extract-audio", "--audio-format", "wav",
        "--audio-quality", "5",
        "-o", output_path.replace(".wav", ".%(ext)s"),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if os.path.isfile(output_path):
        return output_path

    # yt-dlp may have produced a different extension
    base = output_path.rsplit(".", 1)[0]
    for ext in ["wav", "webm", "m4a", "opus"]:
        p = f"{base}.{ext}"
        if os.path.isfile(p):
            # Convert to wav with ffmpeg
            subprocess.run(
                ["ffmpeg", "-y", "-i", p, "-ar", "16000", "-ac", "1", output_path],
                capture_output=True, timeout=300,
            )
            os.remove(p)
            if os.path.isfile(output_path):
                return output_path

    print(f"ERROR: audio download failed.", file=sys.stderr)
    return None


def whisper_transcribe(audio_path, model_name="base"):
    """Transcribe audio with faster-whisper. Returns list of (timestamp, text)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR: faster-whisper not installed. Run: pip install faster-whisper --break-system-packages", file=sys.stderr)
        return []

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5)

    print(f"Whisper detected language: {info.language} (probability: {info.language_probability:.2f})", file=sys.stderr)
    print(f"Audio duration: {info.duration:.1f}s", file=sys.stderr)

    entries = []
    for seg in segments:
        entries.append((
            f"{int(seg.start)//3600:02d}:{(int(seg.start)%3600)//60:02d}:{seg.start%60:06.3f}",
            seg.text.strip(),
        ))

    return entries


# ---------------------------------------------------------------------------
# Output Formatting
# ---------------------------------------------------------------------------

def format_transcript(chunks, metadata=None, source="youtube_subtitles"):
    """Format chunks into a readable transcript string."""
    lines = []

    if metadata:
        lines.append(f"# {metadata.get('title', 'Unknown Title')}")
        lines.append(f"**Channel:** {metadata.get('channel', 'Unknown')}")
        duration = metadata.get("duration", 0)
        lines.append(f"**Duration:** {duration // 60}m {duration % 60}s")
        lines.append(f"**Source:** {source}")
        speaker_count = count_speakers(" ".join(t for _, t in chunks))
        if speaker_count > 5:
            lines.append(f"**Speaker changes detected:** ~{speaker_count}")
        lines.append("")

    for timestamp, text in chunks:
        lines.append(f"[{timestamp}] {text}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def process_video(url, lang="en", chunk_seconds=30, output_path=None,
                  metadata_only=False, use_whisper=False, whisper_model="base",
                  vtt_path=None):
    """Full pipeline: metadata -> subtitles/whisper -> parse -> chunk -> output."""

    # Step 1: Metadata (skip if just parsing a VTT)
    metadata = None
    if not vtt_path:
        print("Fetching metadata...", file=sys.stderr)
        metadata = get_metadata(url)
        if metadata:
            print(f"Title: {metadata.get('title')}", file=sys.stderr)
            print(f"Channel: {metadata.get('channel')}", file=sys.stderr)
            duration = metadata.get("duration", 0)
            print(f"Duration: {duration // 60}m {duration % 60}s", file=sys.stderr)
            has_manual = bool(metadata.get("subtitles", {}).get(lang))
            has_auto = bool(metadata.get("automatic_captions"))
            print(f"Manual subs ({lang}): {'yes' if has_manual else 'no'}", file=sys.stderr)
            print(f"Auto-captions: {'yes' if has_auto else 'no'}", file=sys.stderr)

        if metadata_only:
            if metadata:
                desc = (metadata.get("description") or "")[:1000]
                print(f"\nDescription:\n{desc}", file=sys.stderr)
            else:
                print("ERROR: could not fetch metadata.", file=sys.stderr)
            return

    # Step 2: Get raw transcript
    source = "youtube_subtitles"

    if vtt_path:
        # Parse provided VTT file directly
        if not os.path.isfile(vtt_path):
            print(f"ERROR: VTT file not found: {vtt_path}", file=sys.stderr)
            sys.exit(1)
        raw_entries = parse_vtt_raw(vtt_path)
        print(f"Parsed {len(raw_entries)} raw entries from {vtt_path}", file=sys.stderr)

    elif use_whisper:
        # Whisper path
        source = f"whisper_{whisper_model}"
        print(f"Downloading audio...", file=sys.stderr)
        audio = download_audio(url)
        if not audio:
            sys.exit(1)
        print(f"Transcribing with Whisper ({whisper_model})...", file=sys.stderr)
        raw_entries = whisper_transcribe(audio, whisper_model)
        os.remove(audio)
        print(f"Whisper produced {len(raw_entries)} segments", file=sys.stderr)

    else:
        # Subtitle path (default)
        print(f"Downloading subtitles ({lang})...", file=sys.stderr)
        vtt = download_subtitles(url, lang)
        if not vtt:
            print("No subtitles available. Falling back to Whisper...", file=sys.stderr)
            source = f"whisper_{whisper_model}"
            audio = download_audio(url)
            if not audio:
                print("ERROR: Both subtitle and audio download failed.", file=sys.stderr)
                sys.exit(1)
            print(f"Transcribing with Whisper ({whisper_model})...", file=sys.stderr)
            raw_entries = whisper_transcribe(audio, whisper_model)
            os.remove(audio)
        else:
            raw_entries = parse_vtt_raw(vtt)
            print(f"Parsed {len(raw_entries)} raw entries", file=sys.stderr)
            os.remove(vtt)

    if not raw_entries:
        print("ERROR: No transcript entries produced.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Dedup if auto-captions
    if is_auto_caption(raw_entries):
        print("Auto-caption sliding window detected. Deduplicating...", file=sys.stderr)
        deduped = dedup_sliding_window(raw_entries)
        print(f"Deduped: {len(raw_entries)} -> {len(deduped)} entries", file=sys.stderr)
    else:
        deduped = raw_entries
        print("Manual subtitles detected. Skipping dedup.", file=sys.stderr)

    # Step 4: Chunk
    chunks = chunk_entries(deduped, chunk_seconds)
    print(f"Chunked into {len(chunks)} segments (~{chunk_seconds}s each)", file=sys.stderr)

    # Step 5: Format and output
    transcript = format_transcript(chunks, metadata, source)
    word_count = len(transcript.split())

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"\nTranscript written to {output_path} ({word_count} words)", file=sys.stderr)
    else:
        print(transcript)
        print(f"\n--- {word_count} words ---", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="YouTube video transcript extraction")
    parser.add_argument("url", nargs="?", help="YouTube video URL")
    parser.add_argument("--vtt", help="Parse an existing VTT file instead of downloading")
    parser.add_argument("--lang", default="en", help="Subtitle language code (default: en)")
    parser.add_argument("--chunk-seconds", type=int, default=30,
                        help="Target chunk duration in seconds (default: 30)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--metadata-only", action="store_true",
                        help="Only fetch and display metadata")
    parser.add_argument("--whisper", action="store_true",
                        help="Force Whisper transcription instead of subtitles")
    parser.add_argument("--whisper-model", default="base",
                        choices=["tiny", "base", "small"],
                        help="Whisper model size (default: base)")

    args = parser.parse_args()

    if not args.url and not args.vtt:
        parser.error("Either a YouTube URL or --vtt path is required")

    process_video(
        url=args.url,
        lang=args.lang,
        chunk_seconds=args.chunk_seconds,
        output_path=args.output,
        metadata_only=args.metadata_only,
        use_whisper=args.whisper,
        whisper_model=args.whisper_model,
        vtt_path=args.vtt,
    )


if __name__ == "__main__":
    main()
