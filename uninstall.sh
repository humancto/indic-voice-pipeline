#!/usr/bin/env bash
#
# Indic Voice Pipeline — Uninstaller
#
# Removes both skills from Claude Code's global skills directory.
# Does NOT remove Python packages or cached models.
#

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

SKILLS_DIR="$HOME/.claude/skills"

echo ""
echo -e "${BOLD}Indic Voice Pipeline — Uninstaller${NC}"
echo ""

# Remove skills
if [[ -d "$SKILLS_DIR/video-downloader" ]]; then
    rm -rf "$SKILLS_DIR/video-downloader"
    echo -e "${GREEN}[OK]${NC}  Removed video-downloader"
else
    echo -e "${YELLOW}[SKIP]${NC} video-downloader not found"
fi

if [[ -d "$SKILLS_DIR/whisper-transcribe" ]]; then
    rm -rf "$SKILLS_DIR/whisper-transcribe"
    echo -e "${GREEN}[OK]${NC}  Removed whisper-transcribe"
else
    echo -e "${YELLOW}[SKIP]${NC} whisper-transcribe not found"
fi

echo ""
echo "Skills removed. Python packages and cached models were NOT removed."
echo ""
echo "To also remove cached IndicWhisper models:"
echo "  rm -rf ~/.cache/indicwhisper/"
echo ""
echo "To remove Python packages:"
echo "  pip uninstall openai-whisper yt-dlp transformers accelerate"
echo ""
