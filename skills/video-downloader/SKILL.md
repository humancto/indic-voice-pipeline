---
name: video-downloader
description: |
  Download videos, audio, and playlists from any URL using yt-dlp.
  Use when the user mentions: download video, download from youtube,
  save this video, get audio from, download playlist, what formats available,
  download music, rip audio, save video from URL, extract audio,
  grab this video, download from twitter, download from tiktok.
  Supports YouTube, Vimeo, Twitter/X, TikTok, Instagram, Reddit, and 1000+ sites.
---

# Video Downloader

Download videos, audio, and playlists from any URL. Supports 1000+ sites via yt-dlp.

## Prerequisites

Run once to install dependencies:

```bash
pip install yt-dlp --quiet
```

ffmpeg is also required for audio extraction and format merging:

```bash
brew install ffmpeg  # macOS
```

## Step-by-Step Workflow

**For ANY video download request, follow these steps:**

### Step 1: Check dependencies

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/check_deps.py
```

### Step 2: Determine intent and run the appropriate command

**User wants to download a video:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py download "<URL>" --output-dir ~/Downloads
```

**User wants audio only (music, podcast, etc.):**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py audio "<URL>" --output-dir ~/Downloads --audio-format mp3
```

**User wants a full playlist:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py playlist "<URL>" --output-dir ~/Downloads
```

**User wants to see available formats/qualities:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py formats "<URL>"
```

**User wants video info without downloading:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py info "<URL>"
```

### Step 3: Report results

Tell the user:

- Where the file was saved (full path)
- File size
- Video title and duration
- Any subtitles that were downloaded

## All Commands

```bash
# Download single video (default: best quality up to 1080p, saved to ~/Downloads)
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py download "<URL>"

# Download with quality cap
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py download "<URL>" --quality 720

# Download with specific format ID (use 'formats' command to find IDs)
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py download "<URL>" --format 137

# Download without subtitles
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py download "<URL>" --no-subs

# Download to custom directory
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py download "<URL>" --output-dir ~/Videos

# Download audio only as MP3
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py audio "<URL>"

# Download audio as M4A or Opus
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py audio "<URL>" --audio-format m4a
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py audio "<URL>" --audio-format opus

# Download entire playlist
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py playlist "<URL>"

# List available formats
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py formats "<URL>"

# Show video info without downloading
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/video-downloader/scripts/video_downloader.py info "<URL>"
```

## Important Notes

- Default download location is `~/Downloads`
- All output is JSON to stdout, status messages go to stderr
- A `download_meta.json` file is saved alongside each download
- Quality options: 360, 480, 720, 1080, 4k (default: 1080)
- Audio format options: mp3, m4a, opus (default: mp3)
- yt-dlp supports 1000+ sites: YouTube, Vimeo, Twitter/X, TikTok, Instagram, Reddit, Twitch, etc.
- Subtitles are downloaded by default (English, SRT format)
- Playlist videos are numbered with zero-padded index prefix
