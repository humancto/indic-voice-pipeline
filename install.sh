#!/usr/bin/env bash
#
# Indic Voice Pipeline — One-Command Installer
#
# Installs both skills (video-downloader + whisper-transcribe) into
# Claude Code's global skills directory (~/.claude/skills/).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/humancto/indic-voice-pipeline/main/install.sh | bash
#   — or —
#   git clone https://github.com/humancto/indic-voice-pipeline.git
#   cd indic-voice-pipeline && bash install.sh
#

set -euo pipefail

# ─── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }

# ─── Banner ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}"
echo "  ╔═══════════════════════════════════════════════════════════╗"
echo "  ║                                                           ║"
echo "  ║          Indic Voice Pipeline — Installer                 ║"
echo "  ║                                                           ║"
echo "  ║    Download + Transcribe + Translate Indian Languages     ║"
echo "  ║    100% Local  |  12 Indian Languages  |  No API Keys    ║"
echo "  ║                                                           ║"
echo "  ╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ─── Detect script location (works for both git clone and curl) ──────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

# Check if we have the skill files locally (git clone path)
if [[ -d "$SCRIPT_DIR/skills/video-downloader" && -d "$SCRIPT_DIR/skills/whisper-transcribe" ]]; then
    SOURCE_DIR="$SCRIPT_DIR/skills"
    info "Installing from local directory: $SCRIPT_DIR"
else
    # Curl/remote install — clone to temp dir
    TEMP_DIR="$(mktemp -d)"
    trap "rm -rf $TEMP_DIR" EXIT
    info "Cloning repository..."
    git clone --quiet https://github.com/humancto/indic-voice-pipeline.git "$TEMP_DIR/repo"
    SOURCE_DIR="$TEMP_DIR/repo/skills"
fi

# ─── Install Skills ──────────────────────────────────────────────────────────
echo ""
info "Installing skills to $SKILLS_DIR..."

# Video Downloader
mkdir -p "$SKILLS_DIR/video-downloader/scripts"
cp "$SOURCE_DIR/video-downloader/SKILL.md" "$SKILLS_DIR/video-downloader/"
cp "$SOURCE_DIR/video-downloader/scripts/"*.py "$SKILLS_DIR/video-downloader/scripts/"
success "video-downloader skill installed"

# Whisper Transcribe
mkdir -p "$SKILLS_DIR/whisper-transcribe/scripts"
cp "$SOURCE_DIR/whisper-transcribe/SKILL.md" "$SKILLS_DIR/whisper-transcribe/"
cp "$SOURCE_DIR/whisper-transcribe/scripts/"*.py "$SKILLS_DIR/whisper-transcribe/scripts/"
success "whisper-transcribe skill installed"

# ─── Check System Dependencies ───────────────────────────────────────────────
echo ""
info "Checking system dependencies..."

ALL_OK=true

# Python
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1 | awk '{print $2}')
    success "Python $PY_VER"
else
    error "Python 3 not found — install from https://python.org"
    ALL_OK=false
fi

# ffmpeg
if command -v ffmpeg &>/dev/null; then
    FF_VER=$(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')
    success "ffmpeg $FF_VER"
else
    warn "ffmpeg not found — install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
    ALL_OK=false
fi

# yt-dlp
if command -v yt-dlp &>/dev/null || python3 -c "import yt_dlp" &>/dev/null 2>&1; then
    success "yt-dlp"
else
    warn "yt-dlp not found — will install with pip"
fi

# ─── Install Python Dependencies ─────────────────────────────────────────────
echo ""
info "Installing Python dependencies..."

pip_install() {
    python3 -m pip install --quiet "$@" 2>/dev/null || pip3 install --quiet "$@" 2>/dev/null
}

# Core
pip_install yt-dlp && success "yt-dlp" || warn "yt-dlp install failed — try: pip install yt-dlp"
pip_install openai-whisper && success "openai-whisper" || warn "openai-whisper install failed — try: pip install openai-whisper"
pip_install "transformers==4.46.3" accelerate && success "transformers + accelerate" || warn "transformers install failed"

# ─── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}"
echo "  ════════════════════════════════════════════════════════════"
echo "    Installation complete!"
echo "  ════════════════════════════════════════════════════════════"
echo -e "${NC}"
echo ""
echo "  Skills installed at:"
echo "    $SKILLS_DIR/video-downloader/"
echo "    $SKILLS_DIR/whisper-transcribe/"
echo ""
echo -e "  ${BOLD}Usage with Claude Code:${NC}"
echo '    "Download this video: https://youtube.com/watch?v=..."'
echo '    "Transcribe ~/Downloads/video.mp4 --language te"'
echo '    "Translate this Telugu audio to English"'
echo ""
echo -e "  ${BOLD}Supported Indian Languages:${NC}"
echo "    Telugu (te)  Hindi (hi)  Kannada (kn)  Gujarati (gu)  Tamil (ta)"
echo "    Bengali (bn) Malayalam (ml) Marathi (mr) Odia (or)"
echo "    Punjabi (pa) Sanskrit (sa) Urdu (ur)"
echo ""
echo -e "  ${CYAN}Run dependency check:${NC}"
echo "    python3 ~/.claude/skills/whisper-transcribe/scripts/check_deps.py"
echo "    python3 ~/.claude/skills/video-downloader/scripts/check_deps.py"
echo ""

if [[ "$ALL_OK" = false ]]; then
    warn "Some dependencies are missing — see warnings above."
fi
