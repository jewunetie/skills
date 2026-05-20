---
name: youtube-video
description: >
  Extract and analyze content from YouTube videos via transcription, subtitles, and visual frame analysis.
  Use this skill whenever the user shares a YouTube URL or asks to watch, listen to, summarize, analyze,
  transcribe, or extract information from a YouTube video. Also trigger on phrases like "what does this
  video say", "summarize this video", "watch this for me", "what happens in this video", or any request
  involving a youtube.com or youtu.be link. Trigger proactively even if the user just pastes a YouTube
  URL without explicit instructions -- assume they want the content analyzed.
---

# YouTube Video Skill

Extract and analyze YouTube video content through transcription and visual frame analysis.

## Strategy

Use a tiered approach for maximum quality with minimum resource usage:

1. **Subtitles first**: YouTube's own subtitles (manual or auto-generated) are almost always higher quality than local transcription. Prefer these.
2. **Whisper fallback**: When no subtitles are available, download audio and transcribe locally with `faster-whisper`.
3. **Visual analysis** (optional): Extract keyframes with `ffmpeg` and analyze them with vision when the user asks about visual content, or when the video is instructional/visual in nature (tutorials, presentations, diagrams).

## Setup

Before processing, install dependencies if not already present:

```bash
pip install yt-dlp faster-whisper --break-system-packages -q 2>/dev/null
```

**Important sandbox notes:**
- All `yt-dlp` commands require `--no-check-certificates` due to the proxy SSL configuration.
- All `yt-dlp` commands require `--extractor-args "youtube:player_client=android"` to avoid YouTube bot detection (429 errors and "sign in to confirm you're not a bot" failures). The bundled script handles both of these automatically.
- `faster-whisper` downloads the model on first use (30-60 seconds for `base`). This is a one-time cost per session.

## Bundled Script

The primary tool is `scripts/parse_youtube.py`, which handles the full pipeline: metadata, subtitle download, sliding-window deduplication, HTML entity decoding, sentence chunking, and automatic Whisper fallback.

Copy it to a working directory before use since the skill directory is read-only:

```bash
cp -r /mnt/skills/user/youtube-video/scripts /tmp/yt_scripts
```

### Basic usage

```bash
# Full pipeline: metadata + subtitles + parse + chunk (writes to stdout)
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL"

# Save to file
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL" -o /tmp/transcript.txt

# Metadata only (quick check before committing to full download)
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL" --metadata-only

# Non-English video
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL" --lang ja

# Force Whisper (skip subtitle attempt)
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL" --whisper --whisper-model base

# Parse an existing VTT file
python3 /tmp/yt_scripts/parse_youtube.py --vtt /tmp/existing_subs.en.vtt

# Longer chunks for long videos (60s instead of default 30s)
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL" --chunk-seconds 60
```

### What the script handles automatically

- **Sliding-window deduplication**: YouTube auto-captions repeat previous text in each entry (a sliding window). The script detects this pattern and extracts only the new text from each entry, eliminating the 2-3x duplication.
- **Auto-caption detection**: Samples consecutive entries for substring overlap to decide whether to apply sliding-window dedup or treat as clean manual subtitles.
- **HTML entity decoding**: Converts `&gt;`, `&amp;`, `&lt;`, etc. to their readable forms.
- **Sentence-level chunking**: Merges small entries into readable paragraphs, breaking on sentence boundaries at roughly the configured interval (default 30 seconds).
- **Speaker change markers**: Preserves `>>` markers from auto-captions that indicate speaker changes in multi-speaker content (podcasts, interviews).
- **Automatic Whisper fallback**: If subtitle download fails, automatically downloads audio and transcribes with faster-whisper.
- **File existence verification**: Checks that output files were actually produced after each download step, surfacing the real error on failure.
- **Cleanup**: Removes intermediate files (VTT, audio) after parsing.

### Output format

The script writes a timestamped transcript to stdout (or to a file with `-o`):

```
# Video Title
**Channel:** Channel Name
**Duration:** 45m 30s
**Source:** youtube_subtitles
**Speaker changes detected:** ~47

[0:00] First chunk of text from the video, merged to roughly 30 seconds of content per chunk with breaks at sentence boundaries.

[0:28] Second chunk continues here. >> Speaker changes are preserved with the >> marker from YouTube auto-captions.

[1:02] And so on...
```

Status messages go to stderr, so piping stdout gives clean transcript text.

## Workflow

### Step 1: Get metadata and transcript

For most videos, a single command does everything:

```bash
cp -r /mnt/skills/user/youtube-video/scripts /tmp/yt_scripts
pip install yt-dlp faster-whisper --break-system-packages -q 2>/dev/null
python3 /tmp/yt_scripts/parse_youtube.py "VIDEO_URL" -o /tmp/transcript.txt
```

Then read the transcript:

```bash
cat /tmp/transcript.txt
```

For videos over 30 minutes, the transcript will be large. Use `--chunk-seconds 60` to produce fewer, longer chunks.

**Duration guidelines:**
- Under 30 minutes: default settings work well
- 30-90 minutes: use `--chunk-seconds 60`; transcript fits in context but is long
- Over 90 minutes: use `--chunk-seconds 90`; consider reading in sections (see "Long transcript strategy" below)

### Step 2: Visual analysis (when needed)

Extract keyframes when the video has meaningful visual content (presentations, tutorials, demos, charts). This requires downloading the video, so only do it when visual context adds value.

```bash
# Download lowest quality video (frame content is preserved at any quality)
yt-dlp --no-check-certificates --extractor-args "youtube:player_client=android" \
  -f "worst[ext=mp4]/worst" -o "/tmp/yt_video.%(ext)s" "VIDEO_URL"

# Verify download succeeded and find the actual filename
VIDEO_FILE=$(ls /tmp/yt_video.* 2>/dev/null | head -1)
if [ -z "$VIDEO_FILE" ]; then echo "ERROR: video download failed"; exit 1; fi
echo "Downloaded: $VIDEO_FILE"

# Extract keyframes (adjust INTERVAL based on video length)
# Short (<5 min): INTERVAL=10
# Medium (5-30 min): INTERVAL=30
# Long (30+ min): INTERVAL=60
INTERVAL=30
mkdir -p /tmp/yt_frames
ffmpeg -y -i "$VIDEO_FILE" -vf "fps=1/$INTERVAL" -q:v 2 /tmp/yt_frames/frame_%04d.jpg 2>/dev/null

echo "Extracted $(ls /tmp/yt_frames/*.jpg 2>/dev/null | wc -l) frames"

# Clean up video file to free disk space
rm -f "$VIDEO_FILE"
```

Then use the `view` tool on extracted frames to analyze visual content. Cross-reference frame numbers with timestamps: frame N corresponds to approximately (N-1) * INTERVAL seconds into the video (frame_0001 = 0s, frame_0002 = INTERVAL seconds, etc.).

### Step 3: Synthesize and respond

Combine transcript and visual analysis to address the user's request. Common patterns:

- **Summarize**: Provide a structured summary with key points, organized by topic or chronologically
- **Answer a question**: Search the transcript for relevant sections, cite timestamps
- **Extract information**: Pull specific data points, quotes, or claims from the content
- **Analyze**: Evaluate arguments, identify themes, assess quality of information

Always include:
- Video title and channel for attribution
- Timestamps for key points so the user can jump to relevant sections
- A note about transcript source (YouTube subtitles vs. Whisper) since Whisper may have errors

## Long Transcript Strategy

For videos over 60 minutes, the transcript may exceed what fits comfortably in a single context pass. Strategies:

**For summarization**: Read the transcript in sections using `view` with line ranges. Process each section, build topic-level notes, then synthesize a final summary. A 90-minute video at 30-second chunks produces roughly 180 chunks. Read in batches of 50-60 chunks.

**For specific questions**: Use `grep` to find relevant sections of the transcript before reading the full context:

```bash
grep -n -i "keyword" /tmp/transcript.txt
```

Then use `view` with targeted line ranges around the matches.

**For topic segmentation**: The `>>` speaker markers and natural paragraph breaks in the chunked output make it possible to identify topic transitions. Look for clusters of related keywords to find topic boundaries.

## Cleanup

After processing, remove temporary files to free disk space:

```bash
rm -f /tmp/yt_audio.wav /tmp/yt_video.mp4 /tmp/yt_subs*
rm -f /tmp/transcript.txt
rm -rf /tmp/yt_frames /tmp/yt_scripts
```

## Manual Fallback

If the bundled script is unavailable or encounters issues, here are the raw yt-dlp commands with the required flags:

```bash
# Metadata
yt-dlp --no-check-certificates --extractor-args "youtube:player_client=android" \
  --dump-json --skip-download "VIDEO_URL"

# Subtitles
yt-dlp --no-check-certificates --extractor-args "youtube:player_client=android" \
  --write-subs --write-auto-sub --sub-lang en \
  --skip-download --sub-format vtt -o "/tmp/yt_subs" "VIDEO_URL"
# IMPORTANT: verify file exists after download
ls /tmp/yt_subs*.vtt || echo "Download failed"

# Audio (for Whisper)
yt-dlp --no-check-certificates --extractor-args "youtube:player_client=android" \
  --extract-audio --audio-format wav --audio-quality 5 \
  -o "/tmp/yt_audio.%(ext)s" "VIDEO_URL"
ls /tmp/yt_audio.wav || echo "Download failed"
```

If using manual subtitle download, be aware that auto-generated captions have heavy duplication from YouTube's sliding-window format. Each entry contains the previous entry's text plus new text. You must deduplicate by extracting only the new suffix from each entry. The bundled script handles this; doing it manually requires the sliding-window diff algorithm.

## Limitations

- Whisper `tiny`/`base` models may produce errors with heavy accents, technical jargon, or music
- Videos over 90 minutes may take significant time with Whisper; subtitles are strongly preferred
- YouTube may rate-limit requests (429 errors); the android player client workaround helps but is not foolproof
- Some videos have geo-restrictions or age-gates that yt-dlp cannot bypass in this environment
- Frame extraction requires downloading video, which uses disk space (use lowest quality)
- Private or unlisted videos may not be accessible
- Auto-caption speaker detection relies on `>>` markers, which are not always present or accurate
