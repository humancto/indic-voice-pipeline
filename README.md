<p align="center">
  <img src="https://img.shields.io/badge/languages-12_Indian-orange?style=for-the-badge" alt="12 Indian Languages" />
  <img src="https://img.shields.io/badge/runs-100%25_local-green?style=for-the-badge" alt="100% Local" />
  <img src="https://img.shields.io/badge/API_keys-none_needed-blue?style=for-the-badge" alt="No API Keys" />
  <img src="https://img.shields.io/badge/license-MIT-purple?style=for-the-badge" alt="MIT License" />
</p>

# Indic Voice Pipeline

**Download, transcribe, and translate audio/video in 12 Indian languages — entirely on your machine.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill set that gives your AI assistant the ability to download videos from 1000+ sites, transcribe speech to text using state-of-the-art fine-tuned Whisper models, and translate between languages. No cloud APIs, no data leaving your machine, no API keys.

---

## Why This Exists

Indian language content is **exploding** — YouTube alone has 500M+ Indian language users. But tooling for working with this content programmatically is fragmented:

- Standard Whisper works well for English but struggles with Telugu, Kannada, or Odia
- Fine-tuned models exist but are scattered across HuggingFace repos and obscure ZIP downloads
- Downloading videos, extracting audio, transcribing, and translating requires stitching together 5+ different tools

**Indic Voice Pipeline solves this.** One install, one natural language command, and Claude handles the entire pipeline — from URL to translated text.

```
You:    "Download this Telugu video and transcribe it"
Claude: [downloads] → [extracts audio] → [loads fine-tuned Telugu model] → [transcribes] → [saves .txt + .srt + .json]
```

---

## What's Included

### Skill 1: Video Downloader

Download videos, audio, and playlists from **1000+ websites** using yt-dlp.

| Feature | Details                                                                      |
| ------- | ---------------------------------------------------------------------------- |
| Sites   | YouTube, Vimeo, Twitter/X, TikTok, Instagram, Reddit, Twitch, and 1000+ more |
| Formats | Video (mp4, webm), Audio-only (mp3, m4a, opus)                               |
| Quality | 360p, 480p, 720p, 1080p, 4K                                                  |
| Extras  | Subtitle download, playlist support, format listing                          |

### Skill 2: Whisper Transcribe

Transcribe and translate audio/video using OpenAI Whisper + fine-tuned Indian language models.

| Feature   | Details                                                                           |
| --------- | --------------------------------------------------------------------------------- |
| Languages | 99+ languages, with fine-tuned models for 12 Indian languages                     |
| Models    | Standard Whisper (tiny → large) + HuggingFace fine-tuned + AI4Bharat IndicWhisper |
| Output    | Plain text (.txt), Subtitles (.srt), Structured JSON (.json)                      |
| Hardware  | Apple Silicon (MPS), NVIDIA GPU (CUDA), or CPU                                    |
| Accuracy  | Intelligent 25s chunking with 5s overlap — no words lost at boundaries            |

---

## Supported Indian Languages

<table>
<tr>
<th>Language</th>
<th>Code</th>
<th>Model Source</th>
<th>Base</th>
</tr>
<tr><td><strong>Telugu</strong></td><td><code>te</code></td><td>vasista22/whisper-telugu-large-v2</td><td>Whisper Large-v2 (1.5B)</td></tr>
<tr><td><strong>Hindi</strong></td><td><code>hi</code></td><td>vasista22/whisper-hindi-large-v2</td><td>Whisper Large-v2 (1.5B)</td></tr>
<tr><td><strong>Kannada</strong></td><td><code>kn</code></td><td>vasista22/whisper-kannada-medium</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Gujarati</strong></td><td><code>gu</code></td><td>vasista22/whisper-gujarati-medium</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Tamil</strong></td><td><code>ta</code></td><td>vasista22/whisper-tamil-medium</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Bengali</strong></td><td><code>bn</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Malayalam</strong></td><td><code>ml</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Marathi</strong></td><td><code>mr</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Odia</strong></td><td><code>or</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Punjabi</strong></td><td><code>pa</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Sanskrit</strong></td><td><code>sa</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
<tr><td><strong>Urdu</strong></td><td><code>ur</code></td><td>AI4Bharat IndicWhisper</td><td>Whisper Medium (769M)</td></tr>
</table>

**Model sources:**

- [vasista22](https://huggingface.co/vasista22) — IIT Madras Speech Lab, funded by Bhashini / MeitY
- [AI4Bharat IndicWhisper](https://github.com/AI4Bharat/vistaar) — IIT Madras, trained on 10,700+ hours across 12 languages, MIT licensed

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **ffmpeg** — `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux)
- **Claude Code** — [Install Claude Code](https://docs.anthropic.com/en/docs/claude-code)

### Install

**One-line install:**

```bash
git clone https://github.com/ARC-TECH-LABS/indic-voice-pipeline.git
cd indic-voice-pipeline && bash install.sh
```

**Manual install:**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy skills to Claude Code
cp -r skills/video-downloader ~/.claude/skills/
cp -r skills/whisper-transcribe ~/.claude/skills/
```

### Uninstall

```bash
bash uninstall.sh
```

---

## Usage

Once installed, just talk to Claude naturally. The skills are triggered automatically based on your intent.

### Download a Video

```
"Download this video: https://youtube.com/watch?v=..."
"Download audio only from this URL as MP3"
"Download this entire playlist"
"What formats are available for this video?"
```

### Transcribe Audio / Video

```
"Transcribe ~/Downloads/speech.mp4"
"Transcribe this Telugu video --language te"
"Transcribe ~/Downloads/podcast.mp3 --model medium"
```

### Translate to English

```
"Translate this Hindi audio to English"
"Translate ~/Downloads/telugu_speech.mp4 --language te"
```

### Detect Language

```
"What language is this audio file?"
"Detect the language of ~/Downloads/unknown_speech.wav"
```

### Full Pipeline (Download + Transcribe)

```
"Download this Telugu YouTube video and transcribe it"
"Download https://youtube.com/shorts/abc123 and translate to English"
```

---

## Use Cases

### Content Creators & Media

- **Subtitle generation** — Auto-generate `.srt` subtitle files for YouTube videos in any Indian language
- **Content repurposing** — Download a Telugu podcast, transcribe it, translate to English, create blog posts
- **Multi-language publishing** — Transcribe Hindi content, translate to English for wider reach

### Education & Research

- **Lecture transcription** — Transcribe university lectures in Tamil, Kannada, or Hindi
- **Oral history preservation** — Digitize oral traditions in Sanskrit, Odia, or Punjabi
- **Linguistic research** — Analyze speech patterns across 12 Indian languages locally

### Journalism & Documentation

- **Interview processing** — Download and transcribe interviews from any platform
- **Evidence documentation** — Transcribe audio/video evidence with timestamps
- **Accessibility** — Generate subtitles for hearing-impaired audiences

### Personal & Productivity

- **Voice notes** — Convert voice memos in your native language to searchable text
- **Religious content** — Transcribe pravachans, kirtans, and spiritual discourses
- **Family archives** — Digitize family recordings in regional languages

### Developers & AI Engineers

- **Training data generation** — Create parallel corpora (audio + text) for ML models
- **ASR benchmarking** — Compare transcription quality across Whisper model sizes
- **Pipeline automation** — Build downstream NLP workflows on top of transcriptions

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code (CLI)                      │
│                                                           │
│  "Download and transcribe this Telugu video"              │
│           │                                               │
│           ▼                                               │
│  ┌─────────────────┐     ┌──────────────────────────┐    │
│  │ video-downloader │     │    whisper-transcribe     │    │
│  │                  │     │                           │    │
│  │  yt-dlp engine   │────▶│  Language Detection       │    │
│  │  1000+ sites     │     │         │                 │    │
│  │  Any quality     │     │         ▼                 │    │
│  │  Audio extract   │     │  Model Router             │    │
│  └─────────────────┘     │  ┌──────┴──────┐          │    │
│                           │  │             │          │    │
│                           │  ▼             ▼          │    │
│                           │ vasista22    IndicWhisper  │    │
│                           │ (HuggingFace) (ZIP cache) │    │
│                           │  │             │          │    │
│                           │  └──────┬──────┘          │    │
│                           │         │                 │    │
│                           │         ▼                 │    │
│                           │  Chunked Inference        │    │
│                           │  25s windows, 5s overlap  │    │
│                           │         │                 │    │
│                           │         ▼                 │    │
│                           │  Smart Merge              │    │
│                           │  (no words lost)          │    │
│                           │         │                 │    │
│                           │         ▼                 │    │
│                           │  .txt  .srt  .json        │    │
│                           └──────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### How Transcription Works

1. **Audio extraction** — Video files have audio extracted via ffmpeg (16kHz mono WAV)
2. **Model selection** — Language code maps to the best available fine-tuned model
3. **Chunked inference** — Long audio is split into 25-second chunks with 5-second overlaps
4. **Smart merge** — Overlapping regions are deduplicated using a 3-tier algorithm:
   - Exact suffix-prefix word matching
   - Fuzzy anchor word matching
   - Heuristic proportional skip
5. **Multi-format output** — Results saved as plain text, SRT subtitles, and structured JSON

### Model Priority

```
User specifies --hf-model?  → Use that exact model
User specifies --language?  → Check vasista22 (HuggingFace) first
                             → Fall back to IndicWhisper (ZIP download)
Neither specified?          → Use standard Whisper with auto-detection
```

---

## Advanced Usage

### Standalone Scripts (Without Claude Code)

The scripts work independently — you don't need Claude Code to use them.

**Download a video:**

```bash
python3 skills/video-downloader/scripts/video_downloader.py download "https://youtube.com/watch?v=..." --output-dir ~/Downloads
```

**Transcribe with Telugu model:**

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe ~/Downloads/video.mp4 --language te --output-dir ~/Downloads
```

**Translate to English:**

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py translate ~/Downloads/audio.mp3 --language hi --output-dir ~/Downloads
```

**Detect language:**

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py detect ~/Downloads/audio.mp3
```

**List video formats:**

```bash
python3 skills/video-downloader/scripts/video_downloader.py formats "https://youtube.com/watch?v=..."
```

### Custom HuggingFace Models

Use any Whisper fine-tuned model from HuggingFace:

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe audio.mp3 \
    --hf-model "openai/whisper-large-v3"
```

### Model Sizes

| Model    | VRAM   | Speed    | Accuracy | Best For                         |
| -------- | ------ | -------- | -------- | -------------------------------- |
| `tiny`   | ~1 GB  | Fastest  | Low      | Quick drafts, clear speech       |
| `base`   | ~1 GB  | Fast     | Good     | Default — good balance           |
| `small`  | ~2 GB  | Moderate | Better   | Noisy audio, accented speech     |
| `medium` | ~5 GB  | Slow     | Great    | Non-English, complex audio       |
| `large`  | ~10 GB | Slowest  | Best     | Maximum accuracy, rare languages |

---

## Output Formats

Every transcription produces three files:

### Plain Text (`.txt`)

```
నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.
```

### SRT Subtitles (`.srt`)

```
1
00:00:00,000 --> 00:00:05,320
నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.

2
00:00:05,320 --> 00:00:12,800
శ్రీరాముడు అయోధ్యకు తిరిగి వచ్చిన రోజు...
```

### Structured JSON (`.json`)

```json
{
  "file": "/Users/you/Downloads/video.mp4",
  "language": "te",
  "task": "transcribe",
  "model": "vasista22/whisper-telugu-large-v2",
  "text": "నమస్కారం. ఈ రోజు మనం...",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.32,
      "start_ts": "00:00:00.000",
      "end_ts": "00:00:05.320",
      "text": "నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం."
    }
  ]
}
```

---

## File Structure

```
indic-voice-pipeline/
├── README.md                              # This file
├── LICENSE                                # MIT License
├── install.sh                             # One-command installer
├── uninstall.sh                           # Clean uninstaller
├── requirements.txt                       # Python dependencies
├── skills/
│   ├── video-downloader/
│   │   ├── SKILL.md                       # Claude Code skill definition
│   │   └── scripts/
│   │       ├── check_deps.py              # Dependency checker
│   │       └── video_downloader.py        # Download engine (yt-dlp wrapper)
│   └── whisper-transcribe/
│       ├── SKILL.md                       # Claude Code skill definition
│       └── scripts/
│           ├── check_deps.py              # Dependency checker
│           └── whisper_transcribe.py      # Transcription engine
├── docs/
│   ├── MODELS.md                          # Detailed model documentation
│   └── TROUBLESHOOTING.md                 # Common issues and fixes
└── examples/
    └── pipeline_example.sh                # Example end-to-end pipeline
```

---

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions. Quick fixes:

| Problem                              | Solution                                                   |
| ------------------------------------ | ---------------------------------------------------------- |
| `torch_dtype is deprecated`          | Ignore — cosmetic warning, doesn't affect output           |
| `transformers requires torch >= 2.6` | Pin transformers: `pip install transformers==4.46.3`       |
| `numpy >= 2.0 incompatible`          | Downgrade: `pip install "numpy<2"`                         |
| `suppress_tokens index error`        | Already fixed in the script — update to latest version     |
| `IndicWhisper download fails`        | Check internet connection, retry, or download ZIP manually |
| `MPS out of memory`                  | Use a smaller model: `--model small` or `--model base`     |

---

## Credits & Acknowledgments

This project stands on the shoulders of remarkable open-source work:

- **[OpenAI Whisper](https://github.com/openai/whisper)** — The foundation model for speech recognition
- **[vasista22 / IIT Madras Speech Lab](https://huggingface.co/vasista22)** — Fine-tuned Whisper models for Telugu, Hindi, Kannada, Gujarati, Tamil. Funded by Bhashini / MeitY (Government of India)
- **[AI4Bharat / IIT Madras](https://ai4bharat.iitm.ac.in/)** — IndicWhisper models for 12 Indian languages, trained on the [Vistaar](https://github.com/AI4Bharat/vistaar) dataset (10,700+ hours)
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — The backbone for video downloading from 1000+ sites
- **[HuggingFace Transformers](https://github.com/huggingface/transformers)** — Model loading and inference infrastructure
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — The AI assistant that orchestrates the entire pipeline

---

## Contributing

Contributions welcome! Areas where help is needed:

- **New language models** — Add fine-tuned Whisper models for more Indian languages
- **Speaker diarization** — Identify who's speaking in multi-speaker audio
- **Real-time streaming** — Support live audio transcription
- **Batch processing** — Process entire folders of audio/video files
- **Quality benchmarks** — WER comparisons across models and languages

---

## License

MIT License. See [LICENSE](LICENSE) for details.

The fine-tuned models have their own licenses:

- vasista22 models: Check individual model cards on HuggingFace
- AI4Bharat IndicWhisper: MIT License

---

<p align="center">
  <strong>Built with care for Indian languages.</strong><br/>
  <sub>By <a href="https://github.com/ARC-TECH-LABS">ARC Tech Labs</a></sub>
</p>
