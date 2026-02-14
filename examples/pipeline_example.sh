#!/usr/bin/env bash
#
# Indic Voice Pipeline — Example: Full Download + Transcribe Pipeline
#
# This example demonstrates the complete workflow:
#   1. Download a video from YouTube
#   2. Transcribe the audio to text
#   3. Translate to English
#
# Usage:
#   bash examples/pipeline_example.sh <YOUTUBE_URL> <LANGUAGE_CODE>
#
# Example:
#   bash examples/pipeline_example.sh "https://youtube.com/shorts/abc123" te
#

set -euo pipefail

SCRIPTS_DIR="$HOME/.claude/skills"
PYTHON="python3"
OUTPUT_DIR="$HOME/Downloads"

# ─── Parse Args ──────────────────────────────────────────────────────────────
URL="${1:-}"
LANG="${2:-}"

if [[ -z "$URL" ]]; then
    echo "Usage: bash pipeline_example.sh <URL> [language_code]"
    echo ""
    echo "Examples:"
    echo "  bash pipeline_example.sh 'https://youtube.com/shorts/abc' te    # Telugu"
    echo "  bash pipeline_example.sh 'https://youtube.com/watch?v=xyz' hi   # Hindi"
    echo "  bash pipeline_example.sh 'https://youtube.com/watch?v=xyz'      # Auto-detect"
    echo ""
    echo "Language codes: te hi kn gu ta bn ml mr or pa sa ur en es fr de ..."
    exit 1
fi

echo "════════════════════════════════════════════════════════════"
echo "  Indic Voice Pipeline — Full Example"
echo "════════════════════════════════════════════════════════════"
echo ""

# ─── Step 1: Download ────────────────────────────────────────────────────────
echo "Step 1: Downloading video..."
echo "  URL: $URL"
echo ""

DOWNLOAD_JSON=$($PYTHON "$SCRIPTS_DIR/video-downloader/scripts/video_downloader.py" download "$URL" --output-dir "$OUTPUT_DIR" 2>/dev/null)
VIDEO_PATH=$(echo "$DOWNLOAD_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['file'])" 2>/dev/null || echo "")

if [[ -z "$VIDEO_PATH" || ! -f "$VIDEO_PATH" ]]; then
    echo "ERROR: Download failed. Raw output:"
    echo "$DOWNLOAD_JSON"
    exit 1
fi

echo "  Downloaded: $VIDEO_PATH"
echo ""

# ─── Step 2: Transcribe ──────────────────────────────────────────────────────
echo "Step 2: Transcribing..."

LANG_FLAG=""
if [[ -n "$LANG" ]]; then
    LANG_FLAG="--language $LANG"
    echo "  Language: $LANG"
fi
echo ""

TRANSCRIBE_JSON=$($PYTHON "$SCRIPTS_DIR/whisper-transcribe/scripts/whisper_transcribe.py" transcribe "$VIDEO_PATH" $LANG_FLAG --output-dir "$OUTPUT_DIR" 2>&1 | tee /dev/stderr | grep -v '^\[stderr\]' || true)

echo ""
echo "  Transcription complete!"
echo ""

# ─── Step 3: Translate (if not English) ──────────────────────────────────────
if [[ -n "$LANG" && "$LANG" != "en" ]]; then
    echo "Step 3: Translating to English..."
    echo ""

    $PYTHON "$SCRIPTS_DIR/whisper-transcribe/scripts/whisper_transcribe.py" translate "$VIDEO_PATH" $LANG_FLAG --output-dir "$OUTPUT_DIR" 2>&1 | tee /dev/stderr | grep -v '^\[stderr\]' || true

    echo ""
    echo "  Translation complete!"
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Done! Output files in: $OUTPUT_DIR"
echo "════════════════════════════════════════════════════════════"
echo ""

STEM=$(basename "${VIDEO_PATH%.*}")
echo "  Video:        $VIDEO_PATH"
echo "  Transcript:   $OUTPUT_DIR/${STEM}.txt"
echo "  Subtitles:    $OUTPUT_DIR/${STEM}.srt"
echo "  JSON:         $OUTPUT_DIR/${STEM}.json"
if [[ -n "$LANG" && "$LANG" != "en" ]]; then
    echo "  Translation:  $OUTPUT_DIR/${STEM}_translated.txt"
    echo "  Trans. SRT:   $OUTPUT_DIR/${STEM}_translated.srt"
fi
echo ""
