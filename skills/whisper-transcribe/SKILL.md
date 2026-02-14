---
name: whisper-transcribe
description: |
  Transcribe and translate audio/video files locally using OpenAI Whisper.
  Use when the user mentions: transcribe, transcription, speech to text,
  audio to text, translate audio, what does this say, convert speech,
  subtitle, caption, detect language, whisper, dictation,
  translate this video, translate this audio, what language is this.
  Works with any audio (mp3, wav, m4a, ogg, flac) or video (mp4, mkv, webm, mov) file.
  Supports 99 languages. Runs 100% locally — no API keys needed.
---

# Whisper Transcribe

Transcribe and translate audio/video files locally using OpenAI Whisper. Supports 99 languages, runs entirely on your machine.

## Prerequisites

Run once to install dependencies:

```bash
pip install openai-whisper --quiet
pip install transformers accelerate --quiet  # For HuggingFace fine-tuned models
```

ffmpeg is required for audio processing:

```bash
brew install ffmpeg  # macOS
```

## Step-by-Step Workflow

**For ANY transcription/translation request, follow these steps:**

### Step 1: Check dependencies

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/check_deps.py
```

### Step 2: Determine intent and run the appropriate command

**User wants to transcribe audio/video to text:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE_PATH>" --output-dir ~/Downloads
```

**User wants to translate audio/video to English:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py translate "<FILE_PATH>" --output-dir ~/Downloads
```

**User wants to detect the language:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py detect "<FILE_PATH>"
```

**User wants file info without transcribing:**

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py info "<FILE_PATH>"
```

### Step 3: Report results

Tell the user:

- Detected language and confidence
- The full transcription text
- Where output files were saved (text, SRT subtitles, JSON)
- Processing time
- If translated: both original language and English translation

## All Commands

```bash
# Transcribe audio/video (auto-detects language, saves .txt + .srt + .json)
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE>" --output-dir ~/Downloads

# Transcribe with a specific source language (faster, skips detection)
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE>" --language te

# Transcribe with a larger model for better accuracy
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE>" --model medium

# Transcribe with a specific HuggingFace fine-tuned model
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE>" --hf-model "vasista22/whisper-telugu-large-v2"

# Translate any language to English
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py translate "<FILE>" --output-dir ~/Downloads

# Translate with known source language
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py translate "<FILE>" --language te

# Detect language of audio
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py detect "<FILE>"

# Show audio file metadata
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py info "<FILE>"
```

## Indian Language Fine-Tuned Models

The skill supports **12 Indian languages** with fine-tuned Whisper models from two sources:

- **vasista22** (IIT Madras Speech Lab) — HuggingFace hosted, plug-and-play
- **AI4Bharat IndicWhisper** — Downloaded as ZIP, cached locally at `~/.cache/indicwhisper/`

**Auto-routing:** Just pass `--language <code>` — the best model is selected automatically:

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE>" --language te
```

**Manual override:** Use `--hf-model` to specify any HuggingFace Whisper model:

```bash
/usr/local/opt/python@3.11/bin/python3.11 ~/.claude/skills/whisper-transcribe/scripts/whisper_transcribe.py transcribe "<FILE>" --hf-model "vasista22/whisper-telugu-large-v2"
```

### vasista22 Models (HuggingFace — auto-downloaded)

| Language | Code | Model                               |
| -------- | ---- | ----------------------------------- |
| Telugu   | `te` | `vasista22/whisper-telugu-large-v2` |
| Hindi    | `hi` | `vasista22/whisper-hindi-large-v2`  |
| Kannada  | `kn` | `vasista22/whisper-kannada-medium`  |
| Gujarati | `gu` | `vasista22/whisper-gujarati-medium` |
| Tamil    | `ta` | `vasista22/whisper-tamil-medium`    |

Models by [vasista22 (IIT Madras Speech Lab)](https://huggingface.co/vasista22), funded by Bhashini / MeitY.

### AI4Bharat IndicWhisper Models (ZIP download — cached locally)

These models are fine-tuned on Whisper-medium using the [Vistaar](https://github.com/AI4Bharat/vistaar) dataset.
First use downloads the model ZIP (~500-800 MB) and caches it at `~/.cache/indicwhisper/<language>/`.

| Language  | Code | Source                   |
| --------- | ---- | ------------------------ |
| Bengali   | `bn` | IndicWhisper (AI4Bharat) |
| Malayalam | `ml` | IndicWhisper (AI4Bharat) |
| Marathi   | `mr` | IndicWhisper (AI4Bharat) |
| Odia      | `or` | IndicWhisper (AI4Bharat) |
| Punjabi   | `pa` | IndicWhisper (AI4Bharat) |
| Sanskrit  | `sa` | IndicWhisper (AI4Bharat) |
| Urdu      | `ur` | IndicWhisper (AI4Bharat) |

Models by [AI4Bharat (IIT Madras)](https://ai4bharat.iitm.ac.in/), MIT licensed.

### Priority

When a language has models from both sources (e.g. Hindi, Gujarati, Kannada, Tamil), the vasista22 HuggingFace model is preferred. IndicWhisper is used for languages not covered by vasista22.

## Model Sizes

| Model    | Size   | Speed    | Accuracy | Best for                         |
| -------- | ------ | -------- | -------- | -------------------------------- |
| `tiny`   | 39 MB  | Fastest  | Low      | Quick drafts, clear speech       |
| `base`   | 74 MB  | Fast     | Good     | Default — good balance           |
| `small`  | 244 MB | Moderate | Better   | Noisy audio, accented speech     |
| `medium` | 769 MB | Slow     | Great    | Non-English, complex audio       |
| `large`  | 1.5 GB | Slowest  | Best     | Maximum accuracy, rare languages |

## Supported Languages (selection)

English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Telugu, Tamil, Bengali, Turkish, Ukrainian, Vietnamese, Thai, Indonesian, Swedish, and 70+ more.

## Important Notes

- Default output location is `~/Downloads`
- All output is JSON to stdout, status messages go to stderr
- Three output files per transcription: `.txt` (plain text), `.srt` (subtitles), `.json` (structured)
- Works with both audio files (mp3, wav, m4a, ogg, flac) and video files (mp4, mkv, webm, mov)
- Video files have audio automatically extracted before transcription
- Translation always outputs English (this is a Whisper limitation)
- First run downloads the model (~74 MB for base) — subsequent runs use cache
- Runs 100% locally — no internet needed after model download, no API keys
- Use `--model medium` or `--model large` for better accuracy on non-English or noisy audio
