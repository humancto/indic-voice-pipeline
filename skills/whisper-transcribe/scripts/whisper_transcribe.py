#!/usr/bin/env python3
"""
Whisper Transcribe — Local audio transcription, translation, and analysis.

Supports standard OpenAI Whisper models, HuggingFace fine-tuned models
(e.g., vasista22/whisper-telugu-large-v2 for Telugu), and Qwen3-ASR.

Features:
    - 12 Indian languages with fine-tuned models (vasista22, AI4Bharat IndicWhisper)
    - Speaker diarization via pyannote-audio (who spoke when)
    - Qwen3-ASR-1.7B as alternative ASR engine for comparison
    - Smart chunking with 25s windows and 5s overlap

Commands:
    transcribe  — Transcribe audio/video to text (auto-detects language)
    translate   — Transcribe and translate to English
    detect      — Detect the language of an audio file
    info        — Show audio file metadata without transcribing

Usage:
    whisper_transcribe.py transcribe <file> [options]
    whisper_transcribe.py translate <file> [options]
    whisper_transcribe.py detect <file>
    whisper_transcribe.py info <file>
"""

import argparse
import json
import os
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from urllib.request import urlretrieve


# Well-known HuggingFace fine-tuned Whisper models for specific languages.
# When --language is specified and no explicit --hf-model is given, these are
# used automatically for better accuracy.
HF_LANGUAGE_MODELS = {
    "te": "vasista22/whisper-telugu-large-v2",
    "hi": "vasista22/whisper-hindi-large-v2",
    "kn": "vasista22/whisper-kannada-medium",
    "gu": "vasista22/whisper-gujarati-medium",
    "ta": "vasista22/whisper-tamil-medium",
}

# AI4Bharat IndicWhisper models — distributed as ZIP archives (not on HuggingFace).
# Fine-tuned on Whisper-medium (769M params) using the Vistaar training dataset.
# Covers languages where vasista22 models may not be available.
# Models are downloaded once, extracted, and cached locally.
INDICWHISPER_BASE_URL = "https://indicwhisper.objectstore.e2enetworks.net"
INDICWHISPER_CACHE_DIR = Path.home() / ".cache" / "indicwhisper"

INDICWHISPER_MODELS = {
    "bn": {"name": "Bengali",    "zip": "bengali_models.zip"},
    "ml": {"name": "Malayalam",  "zip": "malayalam_models.zip"},
    "mr": {"name": "Marathi",    "zip": "marathi_models.zip"},
    "or": {"name": "Odia",       "zip": "odia_models.zip"},
    "pa": {"name": "Punjabi",    "zip": "punjabi_models.zip"},
    "sa": {"name": "Sanskrit",   "zip": "sanskrit_models.zip"},
    "ur": {"name": "Urdu",       "zip": "urdu_models.zip"},
}

LANG_NAMES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "nl": "Dutch", "ru": "Russian",
    "zh": "Chinese", "ja": "Japanese", "ko": "Korean", "ar": "Arabic",
    "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "bn": "Bengali",
    "tr": "Turkish", "pl": "Polish", "uk": "Ukrainian", "vi": "Vietnamese",
    "th": "Thai", "id": "Indonesian", "ms": "Malay", "sv": "Swedish",
    "da": "Danish", "no": "Norwegian", "fi": "Finnish", "cs": "Czech",
    "ro": "Romanian", "hu": "Hungarian", "el": "Greek", "he": "Hebrew",
    "ur": "Urdu", "fa": "Persian", "mr": "Marathi", "gu": "Gujarati",
    "kn": "Kannada", "ml": "Malayalam", "pa": "Punjabi", "or": "Odia",
    "sa": "Sanskrit",
}

# Qwen3-ASR-1.7B supported languages (subset — model supports ~30 languages + 22 Chinese dialects)
QWEN_SUPPORTED_LANGUAGES = {
    "en", "hi", "ar", "de", "es", "fr", "it", "ja", "ko", "nl", "pt", "ru",
    "th", "tr", "uk", "vi", "id", "ms", "fa", "pl", "ro", "sv", "cs", "da",
    "fi", "el", "hu", "no", "zh",
}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_audio_info(file_path):
    """Get audio metadata using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", str(file_path)
            ],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception:
        return None


def format_duration(seconds):
    """Format seconds into HH:MM:SS."""
    seconds = int(float(seconds))
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_timestamp(seconds):
    """Format seconds into SRT-style timestamp."""
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    ms = int((s - int(s)) * 1000)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{ms:03d}"


def extract_audio_if_video(file_path, output_dir):
    """If the input is a video file, extract audio to a temp WAV. Returns path to audio."""
    probe = get_audio_info(file_path)
    if not probe:
        return str(file_path)

    streams = probe.get("streams", [])
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)

    if has_video and has_audio:
        eprint("Extracting audio from video...")
        audio_path = Path(output_dir) / f"_whisper_temp_{Path(file_path).stem}.wav"
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(file_path),
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                str(audio_path)
            ],
            capture_output=True, timeout=300,
        )
        if audio_path.exists():
            return str(audio_path)

    return str(file_path)


def _download_progress(block_num, block_size, total_size):
    """Print download progress."""
    if total_size > 0:
        downloaded = block_num * block_size
        pct = min(100, downloaded * 100 / total_size)
        mb_done = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        eprint(f"\r  Downloaded {mb_done:.1f} / {mb_total:.1f} MB ({pct:.0f}%)", end="")
    else:
        downloaded = block_num * block_size
        eprint(f"\r  Downloaded {downloaded / (1024*1024):.1f} MB...", end="")


def download_and_cache_indicwhisper(lang_code):
    """Download and extract an IndicWhisper model ZIP if not already cached.
    Returns the local directory path to the extracted model."""
    info = INDICWHISPER_MODELS[lang_code]
    zip_name = info["zip"]
    lang_name = info["name"].lower()
    url = f"{INDICWHISPER_BASE_URL}/{zip_name}"

    # Cache directory for this language
    lang_cache = INDICWHISPER_CACHE_DIR / lang_name
    marker = lang_cache / ".download_complete"

    if marker.exists():
        # Already downloaded and extracted — find the model directory
        model_dir = _find_indicwhisper_model_dir(lang_cache)
        if model_dir:
            eprint(f"IndicWhisper {info['name']} model already cached at {model_dir}")
            return str(model_dir)

    # Download
    INDICWHISPER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = INDICWHISPER_CACHE_DIR / zip_name

    eprint(f"Downloading IndicWhisper {info['name']} model...")
    eprint(f"  URL: {url}")
    eprint(f"  (This is a one-time download — ~500-800 MB)")

    try:
        urlretrieve(url, str(zip_path), reporthook=_download_progress)
        eprint()  # newline after progress
    except Exception as e:
        eprint(f"\nFailed to download: {e}")
        if zip_path.exists():
            zip_path.unlink()
        return None

    # Extract
    eprint(f"Extracting to {lang_cache}...")
    lang_cache.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(str(zip_path), "r") as zf:
            zf.extractall(str(lang_cache))
    except Exception as e:
        eprint(f"Failed to extract: {e}")
        return None
    finally:
        # Clean up zip
        if zip_path.exists():
            zip_path.unlink()

    # Mark as complete
    marker.touch()

    model_dir = _find_indicwhisper_model_dir(lang_cache)
    if model_dir:
        eprint(f"IndicWhisper {info['name']} model ready at {model_dir}")
        return str(model_dir)

    eprint(f"Warning: Could not locate model files in {lang_cache}")
    return str(lang_cache)


def _find_indicwhisper_model_dir(cache_dir):
    """Find the actual model directory inside extracted IndicWhisper files.
    The ZIPs may contain a nested folder structure. We look for a directory
    containing config.json (standard HF model marker)."""
    cache_path = Path(cache_dir)

    # Check if config.json is directly in the cache dir
    if (cache_path / "config.json").exists():
        return cache_path

    # Search one or two levels deep
    for depth_pattern in ["*/config.json", "*/*/config.json"]:
        matches = list(cache_path.glob(depth_pattern))
        if matches:
            return matches[0].parent

    # Fallback: return the first subdirectory
    subdirs = [d for d in cache_path.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if subdirs:
        return subdirs[0]

    return None


def resolve_hf_model(language, hf_model_arg):
    """Resolve which HuggingFace model to use, if any.
    Returns model ID/path string or None (use standard whisper).
    Checks vasista22 HF models first, then IndicWhisper (AI4Bharat)."""
    if hf_model_arg:
        return hf_model_arg
    if language and language in HF_LANGUAGE_MODELS:
        return HF_LANGUAGE_MODELS[language]
    if language and language in INDICWHISPER_MODELS:
        # Download/cache and return local path
        local_path = download_and_cache_indicwhisper(language)
        if local_path:
            return local_path
    return None


def load_whisper_model(model_name):
    """Load a standard OpenAI Whisper model."""
    eprint(f"Loading Whisper model '{model_name}'...")
    import whisper
    model = whisper.load_model(model_name)
    eprint(f"Model '{model_name}' loaded.")
    return model


def load_hf_model_and_processor(hf_model_id):
    """Load a HuggingFace Whisper model and processor directly (not via pipeline).
    hf_model_id can be a HuggingFace repo ID (e.g. 'vasista22/whisper-telugu-large-v2')
    or a local directory path (for IndicWhisper cached models)."""
    is_local = os.path.isdir(hf_model_id)
    label = hf_model_id if not is_local else f"local:{Path(hf_model_id).name}"
    eprint(f"Loading {'local' if is_local else 'HuggingFace'} model '{label}'...")
    if not is_local:
        eprint("(First run will download the model — this may take a few minutes)")
    import torch
    from transformers import WhisperForConditionalGeneration, WhisperProcessor

    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    torch_dtype = torch.float16 if device != "cpu" else torch.float32

    processor = WhisperProcessor.from_pretrained(hf_model_id)
    model = WhisperForConditionalGeneration.from_pretrained(
        hf_model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
    )
    model.to(device)

    # Fix generation config for fine-tuned models with missing/empty suppress_tokens
    if model.generation_config.suppress_tokens is not None and len(model.generation_config.suppress_tokens) == 0:
        model.generation_config.suppress_tokens = None
    if not hasattr(model.generation_config, "no_timestamps_token_id") or model.generation_config.no_timestamps_token_id is None:
        model.generation_config.no_timestamps_token_id = processor.tokenizer.convert_tokens_to_ids("<|notimestamps|>")

    eprint(f"Model '{label}' loaded on {device}.")
    return model, processor, device, torch_dtype


def transcribe_with_hf(hf_model_id, audio_path, task="transcribe"):
    """Transcribe using a HuggingFace model directly. Returns dict with text and segments.

    Strategy:
    - Short audio (<= 30s): single pass for best accuracy.
    - Longer audio: sliding window with overlap + intelligent word-level merge
      to ensure no words are lost at chunk boundaries.
    """
    import torch

    model, processor, device, torch_dtype = load_hf_model_and_processor(hf_model_id)

    # Load audio
    eprint("Loading audio...")
    try:
        import librosa
        audio_array, _sr = librosa.load(audio_path, sr=16000)
    except ImportError:
        import whisper
        audio_array = whisper.load_audio(audio_path)

    SAMPLE_RATE = 16000
    total_samples = len(audio_array)
    total_duration = total_samples / SAMPLE_RATE
    eprint(f"Audio duration: {total_duration:.1f}s")

    # Detect language for forced decoder IDs from model name/path
    HF_MODEL_TO_LANG = {
        "telugu": "te", "hindi": "hi", "kannada": "kn",
        "gujarati": "gu", "tamil": "ta",
        "bengali": "bn", "malayalam": "ml", "marathi": "mr",
        "odia": "or", "punjabi": "pa", "sanskrit": "sa", "urdu": "ur",
    }
    lang_code = None
    model_lower = hf_model_id.lower()
    for lang_name, code in HF_MODEL_TO_LANG.items():
        if lang_name in model_lower:
            lang_code = code
            break

    def _generate_text(chunk):
        """Run inference on a single audio chunk. Returns decoded text."""
        input_features = processor(
            chunk, sampling_rate=SAMPLE_RATE, return_tensors="pt"
        ).input_features.to(device, dtype=torch_dtype)

        # Odia ("or") is not in Whisper's built-in language list — pass None
        effective_lang = None if lang_code == "or" else lang_code
        forced_decoder_ids = processor.get_decoder_prompt_ids(
            language=effective_lang,
            task=task,
        )

        # Compute safe max_new_tokens: Whisper max is 448 total sequence length.
        # forced_decoder_ids adds prompt tokens; we need to leave room.
        prompt_len = len(forced_decoder_ids) + 1 if forced_decoder_ids else 1
        safe_max_tokens = 448 - prompt_len

        with torch.no_grad():
            predicted_ids = model.generate(
                input_features,
                forced_decoder_ids=forced_decoder_ids,
                max_new_tokens=safe_max_tokens,
            )

        return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()

    # ── Single pass for short audio (up to 30s) ──
    if total_duration <= 30.0:
        eprint("Short audio — single pass...")
        text = _generate_text(audio_array)
        segments = [{
            "id": 0,
            "start": 0.0,
            "end": round(total_duration, 2),
            "text": text,
        }] if text else []
        return {"text": text, "segments": segments}

    # ── Sliding window for longer audio ──
    CHUNK_SEC = 25          # each chunk is 25s of audio
    OVERLAP_SEC = 5         # 5s overlap between consecutive chunks
    CHUNK_LEN = CHUNK_SEC * SAMPLE_RATE
    OVERLAP_LEN = OVERLAP_SEC * SAMPLE_RATE
    STRIDE = CHUNK_LEN - OVERLAP_LEN

    eprint(f"Chunked mode: {CHUNK_SEC}s windows, {OVERLAP_SEC}s overlap, {STRIDE/SAMPLE_RATE:.0f}s stride")

    raw_chunks = []
    start_sample = 0
    idx = 0

    while start_sample < total_samples:
        end_sample = min(start_sample + CHUNK_LEN, total_samples)
        chunk = audio_array[start_sample:end_sample]

        # Skip very short trailing fragments
        if len(chunk) / SAMPLE_RATE < 2.0:
            break

        idx += 1
        t0 = start_sample / SAMPLE_RATE
        t1 = end_sample / SAMPLE_RATE
        eprint(f"  Chunk {idx}: {t0:.1f}s – {t1:.1f}s ({len(chunk)/SAMPLE_RATE:.1f}s)")

        text = _generate_text(chunk)
        if text:
            raw_chunks.append({"start": t0, "end": t1, "text": text})

        start_sample += STRIDE

    # ── Merge overlapping chunks ──
    if not raw_chunks:
        return {"text": "", "segments": []}

    if len(raw_chunks) == 1:
        c = raw_chunks[0]
        return {
            "text": c["text"],
            "segments": [{"id": 0, "start": round(c["start"], 2),
                          "end": round(c["end"], 2), "text": c["text"]}],
        }

    def _find_best_overlap(prev_words, curr_words):
        """Find longest suffix of prev_words matching a prefix of curr_words.
        Also tries fuzzy matching: if exact match fails, look for the longest
        matching subsequence at the boundary."""
        max_search = min(len(prev_words), len(curr_words), 20)

        # Exact suffix-prefix match (greedy: find longest)
        best = 0
        for length in range(1, max_search + 1):
            if prev_words[-length:] == curr_words[:length]:
                best = length

        if best > 0:
            return best

        # Fuzzy: find any single word from end of prev that appears near
        # start of curr — use it as anchor to skip overlap region
        search_end = min(len(curr_words), 8)
        for pw_idx in range(min(len(prev_words), 10) - 1, -1, -1):
            word = prev_words[pw_idx]
            if len(word) < 3:
                continue  # skip short words, too ambiguous
            for cw_idx in range(search_end):
                if curr_words[cw_idx] == word:
                    return cw_idx + 1

        return 0

    merged_parts = []
    segments = []

    for i, chunk in enumerate(raw_chunks):
        if i == 0:
            merged_parts.append(chunk["text"])
            segments.append({
                "id": 0,
                "start": round(chunk["start"], 2),
                "end": round(chunk["end"], 2),
                "text": chunk["text"],
            })
            continue

        prev_words = raw_chunks[i - 1]["text"].split()
        curr_words = chunk["text"].split()

        overlap_words = _find_best_overlap(prev_words, curr_words)

        if overlap_words > 0:
            unique = " ".join(curr_words[overlap_words:])
        else:
            # Heuristic fallback: skip ~first OVERLAP/CHUNK fraction of words
            skip = max(1, int(len(curr_words) * (OVERLAP_SEC / CHUNK_SEC) * 0.5))
            unique = " ".join(curr_words[skip:])

        if unique:
            merged_parts.append(unique)
            seg_start = chunk["start"] + OVERLAP_SEC if overlap_words == 0 else chunk["start"] + (overlap_words / max(len(curr_words), 1)) * (chunk["end"] - chunk["start"])
            segments.append({
                "id": i,
                "start": round(seg_start, 2),
                "end": round(chunk["end"], 2),
                "text": unique,
            })

    full_text = " ".join(merged_parts)
    return {"text": full_text, "segments": segments}


# ─── Speaker Diarization (pyannote-audio) ───────────────────────────────────

def resolve_hf_token(args):
    """Resolve HuggingFace token from CLI arg, environment variable, or HF cache.
    Returns token string or None."""
    # Priority 1: explicit --hf-token argument
    token = getattr(args, "hf_token", None)
    if token:
        return token

    # Priority 2: HF_TOKEN environment variable
    token = os.environ.get("HF_TOKEN")
    if token:
        return token

    # Priority 3: HUGGING_FACE_HUB_TOKEN (legacy env var)
    token = os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if token:
        return token

    # Priority 4: huggingface-cli cached token
    for token_path in [
        Path.home() / ".huggingface" / "token",
        Path.home() / ".cache" / "huggingface" / "token",
    ]:
        if token_path.exists():
            cached = token_path.read_text().strip()
            if cached:
                return cached

    return None


def load_diarization_pipeline(hf_token):
    """Load the pyannote speaker diarization pipeline.
    Uses CPU on Apple Silicon (MPS has known issues with pyannote).

    Args:
        hf_token: HuggingFace token string (required for first download).

    Returns:
        pyannote.audio Pipeline instance.
    """
    try:
        from pyannote.audio import Pipeline as PyannotePipeline
    except ImportError:
        raise ImportError(
            "Speaker diarization requires pyannote.audio.\n"
            "Install with: pip install pyannote.audio\n"
            "Then accept the license at: https://huggingface.co/pyannote/speaker-diarization-3.1"
        )

    import torch

    MODEL_ID = "pyannote/speaker-diarization-3.1"
    eprint(f"Loading diarization model '{MODEL_ID}'...")

    # Force CPU on Apple Silicon (MPS not fully supported by pyannote)
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
        if torch.backends.mps.is_available():
            eprint("  (Using CPU — MPS not yet supported by pyannote)")

    try:
        pipeline = PyannotePipeline.from_pretrained(
            MODEL_ID,
            use_auth_token=hf_token,
        )
        pipeline.to(device)
    except Exception as e:
        error_msg = str(e)
        if ("401" in error_msg or "auth" in error_msg.lower()
                or "token" in error_msg.lower() or "NoneType" in error_msg
                or "user conditions" in error_msg.lower()):
            raise RuntimeError(
                f"Authentication required for '{MODEL_ID}'.\n"
                "Steps to fix:\n"
                "  1. Create a free token at https://huggingface.co/settings/tokens\n"
                "  2. Accept the license at https://huggingface.co/pyannote/speaker-diarization-3.1\n"
                "  3. Pass token via: --hf-token <TOKEN>  or  export HF_TOKEN=<TOKEN>"
            )
        raise

    eprint("Diarization model loaded.")
    return pipeline


def run_diarization(pipeline, audio_path, num_speakers=None, min_speakers=None, max_speakers=None):
    """Run speaker diarization on an audio file.

    Args:
        pipeline: loaded pyannote Pipeline instance.
        audio_path: path to audio file (WAV preferred, 16kHz mono).
        num_speakers: exact number of speakers (optional).
        min_speakers: minimum number of speakers (optional).
        max_speakers: maximum number of speakers (optional).

    Returns:
        List of dicts: [{"start": float, "end": float, "speaker": str}, ...]
        Speaker labels are normalized to "Speaker 1", "Speaker 2", etc.
    """
    eprint("Running speaker diarization...")

    kwargs = {}
    if num_speakers is not None:
        kwargs["num_speakers"] = num_speakers
    elif min_speakers is not None or max_speakers is not None:
        if min_speakers is not None:
            kwargs["min_speakers"] = min_speakers
        if max_speakers is not None:
            kwargs["max_speakers"] = max_speakers

    diarization = pipeline(audio_path, **kwargs)

    # Convert pyannote output to simple list of turns
    turns = []
    speaker_map = {}
    speaker_counter = 0

    for turn, _, speaker_label in diarization.itertracks(yield_label=True):
        if speaker_label not in speaker_map:
            speaker_counter += 1
            speaker_map[speaker_label] = f"Speaker {speaker_counter}"

        turns.append({
            "start": round(turn.start, 3),
            "end": round(turn.end, 3),
            "speaker": speaker_map[speaker_label],
        })

    eprint(f"Diarization complete: {speaker_counter} speaker(s), {len(turns)} turn(s).")
    return turns


def merge_speakers_with_segments(segment_data, diarization_turns):
    """Merge speaker diarization labels into transcription segments.

    For each transcription segment, finds the diarization speaker with the
    greatest temporal overlap and assigns that speaker label.

    Args:
        segment_data: list of segment dicts with "start", "end", "text" keys.
        diarization_turns: list of dicts from run_diarization().

    Returns:
        segment_data (modified in place) with "speaker" key added.
    """
    if not diarization_turns:
        for seg in segment_data:
            seg["speaker"] = "Speaker 1"
        return segment_data

    for seg in segment_data:
        seg_start = seg["start"]
        seg_end = seg["end"]

        # Calculate overlap duration with each speaker
        speaker_overlap = {}
        for turn in diarization_turns:
            overlap_start = max(seg_start, turn["start"])
            overlap_end = min(seg_end, turn["end"])
            overlap_duration = max(0.0, overlap_end - overlap_start)

            if overlap_duration > 0:
                speaker = turn["speaker"]
                speaker_overlap[speaker] = speaker_overlap.get(speaker, 0.0) + overlap_duration

        if speaker_overlap:
            seg["speaker"] = max(speaker_overlap, key=speaker_overlap.get)
        else:
            # Nearest-speaker fallback for gaps
            seg_mid = (seg_start + seg_end) / 2.0
            nearest = min(
                diarization_turns,
                key=lambda t: min(abs(t["start"] - seg_mid), abs(t["end"] - seg_mid))
            )
            seg["speaker"] = nearest["speaker"]

    return segment_data


# ─── Qwen3-ASR Engine ───────────────────────────────────────────────────────

def load_qwen_asr_model():
    """Load Qwen3-ASR-1.7B model and processor from HuggingFace.

    Returns:
        (model, processor, device) tuple.
    """
    try:
        import torch
        from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
    except ImportError:
        raise ImportError(
            "Qwen3-ASR requires transformers and torch.\n"
            "Install with: pip install transformers torch accelerate"
        )

    eprint("Loading Qwen3-ASR-1.7B model...")
    eprint("(First run will download the model — ~3.5 GB)")

    MODEL_ID = "Qwen/Qwen3-ASR-1.7B"

    if torch.cuda.is_available():
        device = "cuda"
        torch_dtype = torch.float16
    elif torch.backends.mps.is_available():
        device = "mps"
        torch_dtype = torch.float16
    else:
        device = "cpu"
        torch_dtype = torch.float32

    processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        MODEL_ID,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    model.to(device)

    eprint(f"Qwen3-ASR-1.7B loaded on {device}.")
    return model, processor, device


def transcribe_with_qwen(audio_path, language=None, task="transcribe"):
    """Transcribe using Qwen3-ASR-1.7B. Returns dict with text and segments.

    Uses the same chunking strategy as the Whisper HF path for consistency.
    """
    import torch

    model, processor, device = load_qwen_asr_model()

    # Load audio
    eprint("Loading audio...")
    try:
        import librosa
        audio_array, _sr = librosa.load(audio_path, sr=16000)
    except ImportError:
        import whisper
        audio_array = whisper.load_audio(audio_path)

    SAMPLE_RATE = 16000
    total_samples = len(audio_array)
    total_duration = total_samples / SAMPLE_RATE
    eprint(f"Audio duration: {total_duration:.1f}s")

    def _generate_text(chunk):
        """Run Qwen3-ASR inference on a single audio chunk."""
        inputs = processor(
            chunk, sampling_rate=SAMPLE_RATE, return_tensors="pt"
        )
        input_features = inputs.input_features.to(device, dtype=model.dtype)

        generate_kwargs = {}
        if language:
            generate_kwargs["language"] = language
        if task == "translate":
            generate_kwargs["task"] = "translate"

        with torch.no_grad():
            predicted_ids = model.generate(
                input_features,
                max_new_tokens=448,
                **generate_kwargs,
            )

        text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()
        return text

    # ── Single pass for short audio (up to 30s) ──
    if total_duration <= 30.0:
        eprint("Short audio — single pass...")
        text = _generate_text(audio_array)
        segments = [{
            "id": 0,
            "start": 0.0,
            "end": round(total_duration, 2),
            "text": text,
        }] if text else []
        return {"text": text, "segments": segments}

    # ── Sliding window for longer audio (same strategy as Whisper HF path) ──
    CHUNK_SEC = 25
    OVERLAP_SEC = 5
    CHUNK_LEN = CHUNK_SEC * SAMPLE_RATE
    STRIDE = CHUNK_LEN - (OVERLAP_SEC * SAMPLE_RATE)

    eprint(f"Chunked mode: {CHUNK_SEC}s windows, {OVERLAP_SEC}s overlap")

    raw_chunks = []
    start_sample = 0
    idx = 0

    while start_sample < total_samples:
        end_sample = min(start_sample + CHUNK_LEN, total_samples)
        chunk = audio_array[start_sample:end_sample]

        if len(chunk) / SAMPLE_RATE < 2.0:
            break

        idx += 1
        t0 = start_sample / SAMPLE_RATE
        t1 = end_sample / SAMPLE_RATE
        eprint(f"  Chunk {idx}: {t0:.1f}s – {t1:.1f}s")

        text = _generate_text(chunk)
        if text:
            raw_chunks.append({"start": t0, "end": t1, "text": text})

        start_sample += STRIDE

    if not raw_chunks:
        return {"text": "", "segments": []}

    if len(raw_chunks) == 1:
        c = raw_chunks[0]
        return {
            "text": c["text"],
            "segments": [{"id": 0, "start": round(c["start"], 2),
                          "end": round(c["end"], 2), "text": c["text"]}],
        }

    # Reuse the same merge algorithm
    def _find_best_overlap(prev_words, curr_words):
        max_search = min(len(prev_words), len(curr_words), 20)
        best = 0
        for length in range(1, max_search + 1):
            if prev_words[-length:] == curr_words[:length]:
                best = length
        if best > 0:
            return best
        search_end = min(len(curr_words), 8)
        for pw_idx in range(min(len(prev_words), 10) - 1, -1, -1):
            word = prev_words[pw_idx]
            if len(word) < 3:
                continue
            for cw_idx in range(search_end):
                if curr_words[cw_idx] == word:
                    return cw_idx + 1
        return 0

    merged_parts = []
    segments = []

    for i, chunk in enumerate(raw_chunks):
        if i == 0:
            merged_parts.append(chunk["text"])
            segments.append({
                "id": 0,
                "start": round(chunk["start"], 2),
                "end": round(chunk["end"], 2),
                "text": chunk["text"],
            })
            continue

        prev_words = raw_chunks[i - 1]["text"].split()
        curr_words = chunk["text"].split()
        overlap_words = _find_best_overlap(prev_words, curr_words)

        if overlap_words > 0:
            unique = " ".join(curr_words[overlap_words:])
        else:
            skip = max(1, int(len(curr_words) * (OVERLAP_SEC / CHUNK_SEC) * 0.5))
            unique = " ".join(curr_words[skip:])

        if unique:
            merged_parts.append(unique)
            seg_start = chunk["start"] + OVERLAP_SEC if overlap_words == 0 else chunk["start"] + (overlap_words / max(len(curr_words), 1)) * (chunk["end"] - chunk["start"])
            segments.append({
                "id": i,
                "start": round(seg_start, 2),
                "end": round(chunk["end"], 2),
                "text": unique,
            })

    full_text = " ".join(merged_parts)
    return {"text": full_text, "segments": segments}


def cmd_info(args):
    """Show audio file metadata."""
    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        print(json.dumps({"status": "error", "error": f"File not found: {file_path}"}))
        return 1

    probe = get_audio_info(file_path)
    if not probe:
        print(json.dumps({"status": "error", "error": "Could not read file metadata. Is ffprobe installed?"}))
        return 1

    fmt = probe.get("format", {})
    streams = probe.get("streams", [])

    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    video_streams = [s for s in streams if s.get("codec_type") == "video"]

    duration = float(fmt.get("duration", 0))
    size_bytes = int(fmt.get("size", 0))

    info = {
        "status": "ok",
        "file": str(file_path),
        "filename": file_path.name,
        "format": fmt.get("format_long_name", fmt.get("format_name", "unknown")),
        "duration": format_duration(duration),
        "duration_seconds": round(duration, 2),
        "file_size": f"{size_bytes / (1024*1024):.1f} MB" if size_bytes > 1024*1024 else f"{size_bytes / 1024:.1f} KB",
        "file_size_bytes": size_bytes,
        "bitrate": f"{int(fmt.get('bit_rate', 0)) // 1000} kbps" if fmt.get("bit_rate") else "unknown",
        "has_video": len(video_streams) > 0,
        "has_audio": len(audio_streams) > 0,
    }

    if audio_streams:
        a = audio_streams[0]
        info["audio"] = {
            "codec": a.get("codec_long_name", a.get("codec_name", "unknown")),
            "sample_rate": f"{a.get('sample_rate', 'unknown')} Hz",
            "channels": a.get("channels", "unknown"),
            "channel_layout": a.get("channel_layout", "unknown"),
        }

    if video_streams:
        v = video_streams[0]
        info["video"] = {
            "codec": v.get("codec_long_name", v.get("codec_name", "unknown")),
            "resolution": f"{v.get('width', '?')}x{v.get('height', '?')}",
        }

    print(json.dumps(info, indent=2, ensure_ascii=False))
    return 0


def cmd_detect(args):
    """Detect language of audio file."""
    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        print(json.dumps({"status": "error", "error": f"File not found: {file_path}"}))
        return 1

    import whisper

    model = load_whisper_model(args.model)

    temp_audio = extract_audio_if_video(file_path, file_path.parent)

    eprint("Detecting language...")
    audio = whisper.load_audio(temp_audio)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    # Clean up temp file
    if temp_audio != str(file_path) and Path(temp_audio).exists():
        Path(temp_audio).unlink()

    top_langs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:5]

    result = {
        "status": "ok",
        "file": str(file_path),
        "detected_language": top_langs[0][0],
        "detected_language_name": LANG_NAMES.get(top_langs[0][0], top_langs[0][0]),
        "confidence": round(top_langs[0][1], 4),
        "top_languages": [
            {
                "code": code,
                "name": LANG_NAMES.get(code, code),
                "probability": round(prob, 4),
            }
            for code, prob in top_langs
        ],
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_transcribe(args):
    """Transcribe audio to text using Whisper (standard/HF fine-tuned) or Qwen3-ASR."""
    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        print(json.dumps({"status": "error", "error": f"File not found: {file_path}"}))
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_audio = extract_audio_if_video(file_path, output_dir)

    engine = getattr(args, "engine", "whisper")
    hf_model_id = None
    use_qwen = False

    # ── Engine routing ──
    if engine == "qwen":
        lang = args.language or "en"
        if lang not in QWEN_SUPPORTED_LANGUAGES:
            eprint(f"Warning: Qwen3-ASR doesn't support '{lang}'. Falling back to Whisper.")
            engine = "whisper"
        else:
            use_qwen = True

    if not use_qwen:
        hf_model_id = resolve_hf_model(args.language, getattr(args, "hf_model", None))

    eprint(f"Transcribing with {'Qwen3-ASR' if use_qwen else 'Whisper'}...")
    start_time = time.time()

    if use_qwen:
        # --- Qwen3-ASR-1.7B engine ---
        model_label = "Qwen/Qwen3-ASR-1.7B"
        qwen_result = transcribe_with_qwen(temp_audio, language=args.language, task=args.task)

        full_text = qwen_result["text"]
        segments = qwen_result["segments"]
        language = args.language or "auto"

        segment_data = []
        for seg in segments:
            segment_data.append({
                "id": seg["id"],
                "start": seg["start"],
                "end": seg["end"],
                "start_ts": format_timestamp(seg["start"]),
                "end_ts": format_timestamp(seg["end"]),
                "text": seg["text"],
            })

    elif hf_model_id:
        # --- HuggingFace fine-tuned model path ---
        model_label = hf_model_id
        hf_result = transcribe_with_hf(hf_model_id, temp_audio, task=args.task)

        full_text = hf_result["text"]
        segments = hf_result["segments"]
        language = args.language or "auto"

        segment_data = []
        for seg in segments:
            segment_data.append({
                "id": seg["id"],
                "start": seg["start"],
                "end": seg["end"],
                "start_ts": format_timestamp(seg["start"]),
                "end_ts": format_timestamp(seg["end"]),
                "text": seg["text"],
            })
    else:
        # --- Standard OpenAI Whisper path ---
        model_label = args.model
        model = load_whisper_model(args.model)

        transcribe_opts = {"verbose": False}

        if args.language:
            transcribe_opts["language"] = args.language

        if args.task == "translate":
            transcribe_opts["task"] = "translate"

        result = model.transcribe(temp_audio, **transcribe_opts)

        full_text = result.get("text", "").strip()
        language = result.get("language", "unknown")
        raw_segments = result.get("segments", [])

        segment_data = []
        for seg in raw_segments:
            segment_data.append({
                "id": seg.get("id", 0),
                "start": round(seg.get("start", 0), 2),
                "end": round(seg.get("end", 0), 2),
                "start_ts": format_timestamp(seg.get("start", 0)),
                "end_ts": format_timestamp(seg.get("end", 0)),
                "text": seg.get("text", "").strip(),
            })

    elapsed = time.time() - start_time

    # ── Speaker Diarization (optional) ──
    diarization_active = False
    diar_elapsed = 0.0
    if getattr(args, "diarize", False):
        try:
            hf_token = resolve_hf_token(args)
            if not hf_token:
                eprint("Warning: No HuggingFace token found. Diarization requires a token.")
                eprint("  Set HF_TOKEN in your environment:  export HF_TOKEN=\"hf_...\"")
                eprint("  Or pass --hf-token hf_...  on the command line.")
                eprint("  Get a free token at: https://huggingface.co/settings/tokens")
                eprint("Skipping diarization — transcription will continue without speaker labels.")
                raise RuntimeError("HF_TOKEN not set")
            diar_pipeline = load_diarization_pipeline(hf_token)

            diar_start = time.time()
            diarization_turns = run_diarization(
                diar_pipeline,
                temp_audio,
                num_speakers=getattr(args, "num_speakers", None),
                min_speakers=getattr(args, "min_speakers", None),
                max_speakers=getattr(args, "max_speakers", None),
            )
            segment_data = merge_speakers_with_segments(segment_data, diarization_turns)
            diarization_active = True
            diar_elapsed = time.time() - diar_start
            eprint(f"Diarization completed in {diar_elapsed:.1f}s")
        except ImportError as e:
            eprint(f"Warning: {e}")
            eprint("Continuing without speaker diarization.")
        except RuntimeError as e:
            eprint(f"Warning: Diarization failed: {e}")
            eprint("Continuing without speaker diarization.")
        except Exception as e:
            eprint(f"Warning: Unexpected diarization error: {e}")
            eprint("Continuing without speaker diarization.")

    # Clean up temp file
    if temp_audio != str(file_path) and Path(temp_audio).exists():
        Path(temp_audio).unlink()

    # Save text file
    stem = file_path.stem
    task_suffix = "_translated" if args.task == "translate" else ""
    txt_path = output_dir / f"{stem}{task_suffix}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        if diarization_active:
            current_speaker = None
            for seg in segment_data:
                speaker = seg.get("speaker", "")
                if speaker != current_speaker:
                    if current_speaker is not None:
                        f.write("\n")
                    f.write(f"[{speaker}]\n")
                    current_speaker = speaker
                f.write(seg["text"].strip() + "\n")
        else:
            f.write(full_text + "\n")

    # Save SRT file
    srt_path = output_dir / f"{stem}{task_suffix}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segment_data, 1):
            f.write(f"{i}\n")
            f.write(f"{seg['start_ts'].replace('.', ',')} --> {seg['end_ts'].replace('.', ',')}\n")
            if diarization_active and seg.get("speaker"):
                f.write(f"[{seg['speaker']}] {seg['text']}\n\n")
            else:
                f.write(f"{seg['text']}\n\n")

    # Save JSON transcript
    json_path = output_dir / f"{stem}{task_suffix}.json"
    transcript_json = {
        "file": str(file_path),
        "language": language,
        "task": args.task,
        "model": model_label,
        "engine": "qwen" if use_qwen else "whisper",
        "diarization": diarization_active,
        "text": full_text,
        "segments": segment_data,
    }
    if diarization_active:
        speakers = sorted(set(seg.get("speaker", "") for seg in segment_data if seg.get("speaker")))
        transcript_json["speakers"] = speakers
        transcript_json["num_speakers"] = len(speakers)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(transcript_json, f, indent=2, ensure_ascii=False)

    # Build output
    output = {
        "status": "ok",
        "task": args.task,
        "file": str(file_path),
        "model": model_label,
        "engine": "qwen" if use_qwen else "whisper",
        "language": language,
        "language_name": LANG_NAMES.get(language, language),
        "diarization": diarization_active,
        "duration_seconds": round(segment_data[-1]["end"], 2) if segment_data else 0,
        "duration": format_duration(segment_data[-1]["end"]) if segment_data else "00:00",
        "processing_time": f"{elapsed:.1f}s",
        "text": full_text,
        "segment_count": len(segment_data),
        "segments": segment_data,
        "output_files": {
            "text": str(txt_path),
            "srt": str(srt_path),
            "json": str(json_path),
        },
    }

    if diarization_active:
        speakers = sorted(set(seg.get("speaker", "") for seg in segment_data if seg.get("speaker")))
        output["num_speakers"] = len(speakers)
        output["speakers"] = speakers
        output["diarization_time"] = f"{diar_elapsed:.1f}s"

    if hf_model_id:
        output["hf_model"] = hf_model_id

    print(json.dumps(output, indent=2, ensure_ascii=False))

    eprint(f"\nTranscription complete in {elapsed:.1f}s")
    if diarization_active:
        eprint(f"  Diarization: {diar_elapsed:.1f}s ({len(speakers)} speakers)")
    eprint(f"  Text: {txt_path}")
    eprint(f"  SRT:  {srt_path}")
    eprint(f"  JSON: {json_path}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Whisper Transcribe — Local audio transcription and translation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common args for transcribe/translate
    def add_common_args(p):
        p.add_argument("file", help="Path to audio or video file")
        p.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base). Ignored when using a HuggingFace model.")
        p.add_argument("--language", default=None,
                        help="Source language code (e.g. 'en', 'te', 'hi'). Auto-detected if not set. "
                             "For Telugu ('te'), automatically uses vasista22/whisper-telugu-large-v2.")
        p.add_argument("--hf-model", default=None,
                        help="HuggingFace model ID to use instead of standard Whisper "
                             "(e.g. 'vasista22/whisper-telugu-large-v2').")
        p.add_argument("--output-dir", default="~/Downloads",
                        help="Output directory (default: ~/Downloads)")
        # Engine selection
        p.add_argument("--engine", default="whisper", choices=["whisper", "qwen"],
                        help="ASR engine: 'whisper' (default) or 'qwen' (Qwen3-ASR-1.7B)")
        # Speaker diarization
        p.add_argument("--diarize", action="store_true", default=False,
                        help="Enable speaker diarization (who spoke when). Requires pyannote.audio.")
        p.add_argument("--num-speakers", type=int, default=None,
                        help="Expected number of speakers (improves diarization accuracy).")
        p.add_argument("--min-speakers", type=int, default=None,
                        help="Minimum number of speakers.")
        p.add_argument("--max-speakers", type=int, default=None,
                        help="Maximum number of speakers.")
        p.add_argument("--hf-token", default=None,
                        help="HuggingFace token for pyannote model access. "
                             "Can also set via HF_TOKEN env var.")

    # --- transcribe ---
    p_transcribe = subparsers.add_parser("transcribe", help="Transcribe audio/video to text")
    add_common_args(p_transcribe)

    # --- translate ---
    p_translate = subparsers.add_parser("translate", help="Transcribe and translate to English")
    add_common_args(p_translate)

    # --- detect ---
    p_detect = subparsers.add_parser("detect", help="Detect language of audio")
    p_detect.add_argument("file", help="Path to audio or video file")
    p_detect.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                          help="Whisper model size (default: base)")

    # --- info ---
    p_info = subparsers.add_parser("info", help="Show audio file metadata")
    p_info.add_argument("file", help="Path to audio or video file")

    args = parser.parse_args()

    if args.command == "info":
        return cmd_info(args)
    elif args.command == "detect":
        return cmd_detect(args)
    elif args.command in ("transcribe", "translate"):
        args.task = "translate" if args.command == "translate" else "transcribe"
        return cmd_transcribe(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
