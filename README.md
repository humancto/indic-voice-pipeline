<p align="center">
  <img src="https://img.shields.io/badge/languages-12_Indian-orange?style=for-the-badge" alt="12 Indian Languages" />
  <img src="https://img.shields.io/badge/engines-Whisper_+_Qwen3--ASR-teal?style=for-the-badge" alt="Whisper + Qwen3-ASR" />
  <img src="https://img.shields.io/badge/speaker_diarization-pyannote-red?style=for-the-badge" alt="Speaker Diarization" />
  <img src="https://img.shields.io/badge/runs-100%25_local-green?style=for-the-badge" alt="100% Local" />
  <img src="https://img.shields.io/badge/API_keys-none_needed-blue?style=for-the-badge" alt="No API Keys" />
  <img src="https://img.shields.io/badge/license-MIT-purple?style=for-the-badge" alt="MIT License" />
</p>

# Indic Voice Pipeline

**Download, transcribe, diarize, and translate audio/video in 12 Indian languages — entirely on your machine.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill set that gives your AI assistant the ability to download videos from 1000+ sites, transcribe speech to text using state-of-the-art fine-tuned Whisper models (or Alibaba's Qwen3-ASR), identify speakers with pyannote diarization, and translate between languages. No cloud APIs, no data leaving your machine, no API keys.

---

## What's New

- **Speaker Diarization** — Identify _who spoke when_ using pyannote-audio. Add `--diarize` and get `[Speaker 1]`, `[Speaker 2]` labels in every output file.
- **Qwen3-ASR Engine** — Switch to Alibaba's Qwen3-ASR-1.7B as an alternative ASR engine with `--engine qwen`. Supports Hindi + ~30 languages. Drop-in comparison with Whisper, same output formats.
- **Multi-engine Architecture** — Choose the best engine per task. Whisper for Indian languages, Qwen for broader multilingual coverage. Diarization works with both.

---

## Why This Exists

Indian language content is **exploding** — YouTube alone has 500M+ Indian language users. But tooling for working with this content programmatically is fragmented:

- Standard Whisper works well for English but struggles with Telugu, Kannada, or Odia
- Fine-tuned models exist but are scattered across HuggingFace repos and obscure ZIP downloads
- Downloading videos, extracting audio, transcribing, and translating requires stitching together 5+ different tools
- Multi-speaker content (interviews, podcasts, meetings) loses all attribution without diarization

**Indic Voice Pipeline solves this.** One install, one natural language command, and Claude handles the entire pipeline — from URL to speaker-attributed translated text.

```
You:    "Download this Telugu interview and transcribe it with speaker labels"
Claude: [downloads] → [extracts audio] → [loads fine-tuned Telugu model] → [transcribes] → [diarizes speakers] → [saves .txt + .srt + .json]
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

Transcribe and translate audio/video using OpenAI Whisper + fine-tuned Indian language models, with optional speaker diarization.

| Feature     | Details                                                                           |
| ----------- | --------------------------------------------------------------------------------- |
| Languages   | 99+ languages, with fine-tuned models for 12 Indian languages                     |
| Models      | Standard Whisper (tiny → large) + HuggingFace fine-tuned + AI4Bharat IndicWhisper |
| Output      | Plain text (.txt), Subtitles (.srt), Structured JSON (.json)                      |
| Hardware    | Apple Silicon (MPS), NVIDIA GPU (CUDA), or CPU                                    |
| Accuracy    | Intelligent 25s chunking with 5s overlap — no words lost at boundaries            |
| Diarization | Optional speaker identification via pyannote-audio (`--diarize`)                  |

### Skill 3: Qwen3-ASR Engine

Alternative ASR engine using Alibaba's Qwen3-ASR-1.7B for broader multilingual coverage.

| Feature     | Details                                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------------------------- |
| Languages   | Hindi + ~30 languages (Arabic, French, German, Japanese, Korean, Russian, Spanish, Thai, Turkish, Vietnamese, and more) |
| Model       | `Qwen/Qwen3-ASR-1.7B` from HuggingFace (~3.5 GB, downloaded and cached once)                                            |
| Output      | Same .txt, .srt, .json formats — drop-in comparison with Whisper                                                        |
| Fallback    | Auto-falls back to Whisper for unsupported languages (Telugu, Kannada, etc.)                                            |
| Diarization | Full speaker diarization support (`--diarize` works with Qwen too)                                                      |
| License     | Apache 2.0                                                                                                              |

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
- **HuggingFace Token** _(optional, only for speaker diarization)_ — Free read-only token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### Install

**One-line install:**

```bash
git clone https://github.com/humancto/indic-voice-pipeline.git
cd indic-voice-pipeline && bash install.sh
```

**Manual install:**

```bash
# Install Python dependencies
pip install -r requirements.txt

# (Optional) Install speaker diarization support
pip install pyannote.audio

# Copy skills to Claude Code
cp -r skills/video-downloader ~/.claude/skills/
cp -r skills/whisper-transcribe ~/.claude/skills/
```

> **Note:** If you skip `pip install pyannote.audio`, everything else works normally. Diarization is the only feature that requires it. The pipeline degrades gracefully — transcription always works regardless.

### Uninstall

```bash
bash uninstall.sh
```

---

## Usage

Once installed, just talk to Claude naturally. The skills are triggered automatically based on your intent.

### Quick Reference — Top Flags

| Flag             | What it does                                                   | Default             | Example                                        |
| ---------------- | -------------------------------------------------------------- | ------------------- | ---------------------------------------------- |
| `--language`     | Set source language (skips auto-detection, loads best model)   | Auto-detect         | `--language te`                                |
| `--model`        | Whisper model size: `tiny`, `base`, `small`, `medium`, `large` | `large`             | `--model base`                                 |
| `--engine`       | ASR engine: `whisper` or `qwen`                                | `whisper`           | `--engine qwen`                                |
| `--diarize`      | Enable speaker diarization (who spoke when)                    | Off                 | `--diarize`                                    |
| `--num-speakers` | Exact speaker count (improves diarization accuracy)            | Auto                | `--num-speakers 2`                             |
| `--hf-token`     | HuggingFace token for diarization                              | `$HF_TOKEN` env var | `--hf-token hf_...`                            |
| `--output-dir`   | Where to save output files                                     | `~/Downloads`       | `--output-dir ./out`                           |
| `--hf-model`     | Override with any HuggingFace Whisper model                    | Auto-selected       | `--hf-model vasista22/whisper-telugu-large-v2` |

> **Diarization note:** `--diarize` is off by default. When enabled, it requires a HuggingFace token (via `--hf-token` or `$HF_TOKEN`). If no token is found, the pipeline prints a helpful message and continues transcription without speaker labels — it never fails.

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

### Transcribe with Speaker Diarization

```
"Transcribe ~/Downloads/interview.mp4 --diarize"
"Transcribe this Hindi podcast with speaker labels --language hi --diarize"
"Transcribe meeting.wav --diarize --num-speakers 3"
```

### Transcribe with Qwen3-ASR Engine

```
"Transcribe ~/Downloads/speech.mp3 --engine qwen"
"Transcribe this Hindi video --engine qwen --language hi"
"Transcribe meeting.wav --engine qwen --diarize"
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
"Download this podcast and transcribe with speaker labels --diarize"
```

---

## Speaker Diarization

Speaker diarization answers the question: **"Who spoke when?"** It labels each segment of the transcript with a speaker identity — `[Speaker 1]`, `[Speaker 2]`, etc.

### How It Works

The pipeline uses [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1), the gold standard for neural speaker diarization. Diarization runs as a post-processing step after transcription, so it works with **both** the Whisper and Qwen3-ASR engines.

### Setup (One-Time)

**Step 1:** Install pyannote.audio

```bash
pip install pyannote.audio
```

**Step 2:** Create a free HuggingFace token (read-only access is sufficient)

Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and create a token.

**Step 3:** Accept the pyannote model licenses

You must accept **both** gated model licenses on HuggingFace (free, instant approval):

1. **Speaker Diarization 3.1** — [huggingface.co/pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) → Click "Agree and access repository"
2. **Segmentation 3.0** — [huggingface.co/pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) → Click "Agree and access repository"

> **Important:** Both licenses are required. The diarization pipeline internally depends on the segmentation model. If you only accept the first one, you'll get a `403 Forbidden` error.

**Step 4:** Provide your token (choose one method)

```bash
# Option A: Pass directly as a flag
--hf-token hf_...

# Option B: Set as an environment variable
export HF_TOKEN="hf_..."
```

> **Token is required every run**, not just for the initial model download. pyannote uses it for authentication on each load. The recommended approach is to set it permanently in your shell profile:
>
> ```bash
> echo 'export HF_TOKEN="hf_your_token_here"' >> ~/.zshrc
> source ~/.zshrc
> ```
>
> The pyannote models (~300 MB total) are downloaded once on first use and cached permanently at `~/.cache/torch/pyannote/`.

### Diarization Flags

| Flag             | Description                                 | Example                |
| ---------------- | ------------------------------------------- | ---------------------- |
| `--diarize`      | Enable speaker diarization                  | `--diarize`            |
| `--hf-token`     | HuggingFace token for pyannote model access | `--hf-token hf_abc123` |
| `--num-speakers` | Exact number of speakers (if known)         | `--num-speakers 2`     |
| `--min-speakers` | Minimum expected speakers                   | `--min-speakers 2`     |
| `--max-speakers` | Maximum expected speakers                   | `--max-speakers 5`     |

### Diarized Output Examples

**Plain Text (`.txt`) with speaker labels:**

```
[Speaker 1] నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.
[Speaker 2] అవును, చాలా మంచి విషయం. ప్రారంభిద్దాం.
[Speaker 1] శ్రీరాముడు అయోధ్యకు తిరిగి వచ్చిన రోజు...
```

**SRT Subtitles (`.srt`) with speaker labels:**

```
1
00:00:00,000 --> 00:00:05,320
[Speaker 1] నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.

2
00:00:05,320 --> 00:00:08,100
[Speaker 2] అవును, చాలా మంచి విషయం. ప్రారంభిద్దాం.
```

**Structured JSON (`.json`) with speaker metadata:**

```json
{
  "file": "/Users/you/Downloads/interview.mp4",
  "language": "te",
  "task": "transcribe",
  "model": "vasista22/whisper-telugu-large-v2",
  "diarization": true,
  "speakers_found": 2,
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.32,
      "speaker": "Speaker 1",
      "text": "నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం."
    }
  ]
}
```

### Hardware Notes for Diarization

| Platform      | Diarization Device | Notes                                                       |
| ------------- | ------------------ | ----------------------------------------------------------- |
| Apple Silicon | CPU                | MPS is not supported by pyannote; CPU is used automatically |
| NVIDIA GPU    | CUDA               | Full GPU acceleration                                       |
| CPU-only      | CPU                | Works, but slower on long audio files                       |

### Graceful Degradation

If `pyannote.audio` is not installed and you pass `--diarize`, the pipeline will print a warning and proceed with transcription only — no crash, no error. Speaker labels will simply be absent from the output. Install pyannote whenever you need diarization; uninstall it if you never do.

---

## Qwen3-ASR Engine

[Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) is Alibaba's open-source automatic speech recognition model, offering strong multilingual performance as an alternative to Whisper.

### When to Use Qwen3-ASR

| Scenario                                                                              | Recommended Engine                        |
| ------------------------------------------------------------------------------------- | ----------------------------------------- |
| Telugu, Kannada, Odia, or other Indian languages with fine-tuned Whisper models       | **Whisper** (`--engine whisper`, default) |
| Hindi with desire for a second opinion or comparison                                  | **Either** — try both                     |
| Arabic, French, German, Japanese, Korean, Russian, Spanish, Thai, Turkish, Vietnamese | **Qwen** (`--engine qwen`)                |
| Benchmarking ASR engines against each other                                           | **Both** — run once with each engine      |

### Supported Languages (Qwen3-ASR)

Hindi, Arabic, Cantonese, Dutch, English, French, German, Indonesian, Italian, Japanese, Korean, Malay, Portuguese, Russian, Spanish, Swedish, Thai, Turkish, Ukrainian, Vietnamese, and more (~30 total).

> **Auto-fallback:** If you request a language that Qwen3-ASR does not support (e.g., Telugu, Kannada), the pipeline automatically falls back to Whisper. No manual intervention needed.

### Usage

```bash
# Transcribe with Qwen3-ASR
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe audio.mp3 --engine qwen

# Qwen + diarization
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe interview.mp4 --engine qwen --diarize --hf-token hf_...

# Qwen with specific language
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe audio.mp3 --engine qwen --language hi
```

### Model Details

| Property     | Value                                                     |
| ------------ | --------------------------------------------------------- |
| Model        | `Qwen/Qwen3-ASR-1.7B`                                     |
| Parameters   | 1.7 billion                                               |
| Size on disk | ~3.5 GB (downloaded once, cached permanently)             |
| License      | Apache 2.0                                                |
| Source       | [HuggingFace](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) |

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

### Interviews & Podcasts

- **Interview transcription** — Transcribe interviews with `--diarize` to get speaker-attributed text. Know exactly who said what.
- **Podcast transcription** — Multi-speaker podcasts with automatic speaker attribution. Each host and guest is labeled.
- **Meeting notes** — Transcribe team meetings with speaker identification. Instantly generate attributed minutes.

### Journalism & Documentation

- **Interview processing** — Download and transcribe interviews from any platform with full speaker attribution
- **Evidence documentation** — Transcribe audio/video evidence with timestamps and speaker labels
- **Accessibility** — Generate subtitles for hearing-impaired audiences

### Personal & Productivity

- **Voice notes** — Convert voice memos in your native language to searchable text
- **Religious content** — Transcribe pravachans, kirtans, and spiritual discourses
- **Family archives** — Digitize family recordings in regional languages

### Developers & AI Engineers

- **Training data generation** — Create parallel corpora (audio + text) for ML models
- **ASR benchmarking** — Compare transcription quality across Whisper and Qwen3-ASR engines
- **Pipeline automation** — Build downstream NLP workflows on top of transcriptions

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Claude Code (CLI)                             │
│                                                                      │
│  "Download and transcribe this Telugu interview with speaker labels"  │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐     ┌──────────────────────────────────────┐   │
│  │ video-downloader │     │         whisper-transcribe            │   │
│  │                  │     │                                       │   │
│  │  yt-dlp engine   │────▶│  Audio Extraction (ffmpeg, 16kHz)    │   │
│  │  1000+ sites     │     │         │                            │   │
│  │  Any quality     │     │         ▼                            │   │
│  │  Audio extract   │     │  Engine Selection                    │   │
│  └─────────────────┘     │  ┌───────┴────────┐                  │   │
│                           │  │                │                  │   │
│                           │  ▼                ▼                  │   │
│                           │ Whisper          Qwen3-ASR           │   │
│                           │ (default)        (--engine qwen)     │   │
│                           │  │                │                  │   │
│                           │  ▼                ▼                  │   │
│                           │  Language Detection                  │   │
│                           │         │                            │   │
│                           │         ▼                            │   │
│                           │  Model Router                        │   │
│                           │  ┌──────┴──────┐                    │   │
│                           │  │             │                    │   │
│                           │  ▼             ▼                    │   │
│                           │ vasista22    IndicWhisper / Qwen    │   │
│                           │ (HuggingFace) (ZIP / HF cache)     │   │
│                           │  │             │                    │   │
│                           │  └──────┬──────┘                    │   │
│                           │         │                            │   │
│                           │         ▼                            │   │
│                           │  Chunked Inference                   │   │
│                           │  25s windows, 5s overlap             │   │
│                           │         │                            │   │
│                           │         ▼                            │   │
│                           │  Smart Merge                         │   │
│                           │  (no words lost)                     │   │
│                           │         │                            │   │
│                           │         ▼                            │   │
│                           │  ┌─────────────────────────┐        │   │
│                           │  │  Speaker Diarization     │        │   │
│                           │  │  (pyannote, optional)    │        │   │
│                           │  │  --diarize flag          │        │   │
│                           │  └─────────────────────────┘        │   │
│                           │         │                            │   │
│                           │         ▼                            │   │
│                           │  .txt  .srt  .json                   │   │
│                           │  (with speaker labels if diarized)   │   │
│                           └──────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Pipeline Flow (Simplified)

```
URL → yt-dlp Download → Audio Extraction (ffmpeg) → Engine Selection (Whisper / Qwen)
  → Language Detection → Model Router → Chunked Inference → Smart Merge
  → [Optional: Speaker Diarization (pyannote)] → .txt  .srt  .json
```

### How Transcription Works

1. **Audio extraction** — Video files have audio extracted via ffmpeg (16kHz mono WAV)
2. **Engine selection** — Whisper (default) or Qwen3-ASR (`--engine qwen`)
3. **Model selection** — Language code maps to the best available fine-tuned model
4. **Chunked inference** — Long audio is split into 25-second chunks with 5-second overlaps
5. **Smart merge** — Overlapping regions are deduplicated using a 3-tier algorithm:
   - Exact suffix-prefix word matching
   - Fuzzy anchor word matching
   - Heuristic proportional skip
6. **Speaker diarization** _(optional)_ — If `--diarize` is set, pyannote identifies speakers and labels each segment
7. **Multi-format output** — Results saved as plain text, SRT subtitles, and structured JSON

### Model Priority

```
User specifies --engine qwen?  → Use Qwen3-ASR-1.7B
                                  → Auto-fallback to Whisper if language unsupported

User specifies --hf-model?     → Use that exact Whisper model
User specifies --language?     → Check vasista22 (HuggingFace) first
                                → Fall back to IndicWhisper (ZIP download)
Neither specified?             → Use standard Whisper with auto-detection
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

**Transcribe with speaker diarization:**

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe ~/Downloads/interview.mp4 \
    --language te --diarize --hf-token hf_... --output-dir ~/Downloads
```

**Transcribe with Qwen3-ASR engine:**

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe ~/Downloads/audio.mp3 \
    --engine qwen --language hi --output-dir ~/Downloads
```

**Transcribe with Qwen3-ASR + diarization:**

```bash
python3 skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe ~/Downloads/meeting.mp4 \
    --engine qwen --diarize --num-speakers 3 --hf-token hf_... --output-dir ~/Downloads
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

### Engine Comparison

| Property               | Whisper                                  | Qwen3-ASR-1.7B                    |
| ---------------------- | ---------------------------------------- | --------------------------------- |
| Indian language models | 12 fine-tuned (vasista22 + IndicWhisper) | Hindi only (others auto-fallback) |
| Global languages       | 99+                                      | ~30                               |
| Model sizes            | tiny (39M) to large (1.5B)               | 1.7B (single model)               |
| Disk space             | Varies by model size                     | ~3.5 GB                           |
| License                | MIT (Whisper) / varies (fine-tuned)      | Apache 2.0                        |
| Diarization support    | Yes                                      | Yes                               |

---

## Output Formats

Every transcription produces three files:

### Plain Text (`.txt`)

```
నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.
```

With `--diarize`:

```
[Speaker 1] నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.
[Speaker 2] అవును, చాలా మంచి విషయం.
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

With `--diarize`:

```
1
00:00:00,000 --> 00:00:05,320
[Speaker 1] నమస్కారం. ఈ రోజు మనం రామాయణం గురించి మాట్లాడుకుందాం.

2
00:00:05,320 --> 00:00:08,100
[Speaker 2] అవును, చాలా మంచి విషయం. ప్రారంభిద్దాం.
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

With `--diarize`:

```json
{
  "file": "/Users/you/Downloads/interview.mp4",
  "language": "te",
  "task": "transcribe",
  "model": "vasista22/whisper-telugu-large-v2",
  "diarization": true,
  "speakers_found": 2,
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.32,
      "speaker": "Speaker 1",
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
│           └── whisper_transcribe.py      # Transcription engine (Whisper + Qwen + Diarization)
├── docs/
│   ├── MODELS.md                          # Detailed model documentation
│   └── TROUBLESHOOTING.md                 # Common issues and fixes
└── examples/
    └── pipeline_example.sh                # Example end-to-end pipeline
```

---

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions. Quick fixes:

| Problem                                           | Solution                                                                                                                                                                              |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `torch_dtype is deprecated`                       | Ignore — cosmetic warning, doesn't affect output                                                                                                                                      |
| `transformers requires torch >= 2.6`              | Pin transformers: `pip install transformers==4.46.3`                                                                                                                                  |
| `numpy >= 2.0 incompatible`                       | Downgrade: `pip install "numpy<2"`                                                                                                                                                    |
| `suppress_tokens index error`                     | Already fixed in the script — update to latest version                                                                                                                                |
| `IndicWhisper download fails`                     | Check internet connection, retry, or download ZIP manually                                                                                                                            |
| `MPS out of memory`                               | Use a smaller model: `--model small` or `--model base`                                                                                                                                |
| `pyannote not installed` warning                  | `pip install pyannote.audio` — only needed for `--diarize`                                                                                                                            |
| `pyannote license not accepted` / `403 Forbidden` | Accept **both** licenses: [speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) AND [segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) |
| `HF_TOKEN not set` for diarization                | `export HF_TOKEN="hf_..."` or pass `--hf-token hf_...`                                                                                                                                |
| Qwen unsupported language fallback                | Expected behavior — pipeline auto-switches to Whisper                                                                                                                                 |

---

## Credits & Acknowledgments

This project stands on the shoulders of remarkable open-source work:

- **[OpenAI Whisper](https://github.com/openai/whisper)** — The foundation model for speech recognition
- **[Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B)** — Alibaba's multilingual ASR model (Apache 2.0)
- **[pyannote-audio](https://github.com/pyannote/pyannote-audio)** — State-of-the-art neural speaker diarization
- **[vasista22 / IIT Madras Speech Lab](https://huggingface.co/vasista22)** — Fine-tuned Whisper models for Telugu, Hindi, Kannada, Gujarati, Tamil. Funded by Bhashini / MeitY (Government of India)
- **[AI4Bharat / IIT Madras](https://ai4bharat.iitm.ac.in/)** — IndicWhisper models for 12 Indian languages, trained on the [Vistaar](https://github.com/AI4Bharat/vistaar) dataset (10,700+ hours)
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — The backbone for video downloading from 1000+ sites
- **[HuggingFace Transformers](https://github.com/huggingface/transformers)** — Model loading and inference infrastructure
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — The AI assistant that orchestrates the entire pipeline

---

## Contributing

Contributions welcome! Areas where help is needed:

- **Real-time streaming** — Support live audio transcription
- **Batch processing** — Process entire folders of audio/video files
- **Quality benchmarks** — WER comparisons across models, languages, and engines
- **New language models** — Add fine-tuned Whisper models for more Indian languages
- **Translation pipeline** — Integrate translation with diarized output

---

## License

MIT License. See [LICENSE](LICENSE) for details.

The fine-tuned models and dependencies have their own licenses:

- vasista22 models: Check individual model cards on HuggingFace
- AI4Bharat IndicWhisper: MIT License
- Qwen3-ASR-1.7B: Apache 2.0 License
- pyannote-audio: MIT License (model weights require license acceptance on HuggingFace)

---

<p align="center">
  <strong>Built with care for Indian languages.</strong><br/>
  <sub>By <a href="https://github.com/humancto">HumanCTO</a></sub>
</p>
