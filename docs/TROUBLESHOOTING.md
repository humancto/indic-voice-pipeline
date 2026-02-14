# Troubleshooting Guide

Common issues and their solutions when using Indic Voice Pipeline.

## Installation Issues

### Python version too old

```
Error: Python 3.10+ required
```

**Fix**: Install Python 3.10 or newer from https://python.org or via:

```bash
brew install python@3.11  # macOS
sudo apt install python3.11  # Ubuntu
```

### ffmpeg not found

```
Error: ffmpeg not found
```

**Fix**:

```bash
brew install ffmpeg      # macOS
sudo apt install ffmpeg  # Ubuntu/Debian
choco install ffmpeg     # Windows
```

### pip install fails for openai-whisper

```
Error: llvmlite build failed
```

**Fix**: Install numba with binary-only, then whisper:

```bash
pip install numba --only-binary=:all:
pip install openai-whisper
```

## Transcription Issues

### `transformers requires torch >= 2.6`

```
ValueError: Due to a serious vulnerability issue in torch.load...
```

**Cause**: transformers 5.x requires torch 2.6+, but your system may have an older torch.

**Fix**: Pin transformers to a compatible version:

```bash
pip install transformers==4.46.3
```

### `numpy >= 2.0 incompatible with torch`

```
AttributeError: _ARRAY_API not found
```

**Cause**: NumPy 2.x is incompatible with older PyTorch versions.

**Fix**:

```bash
pip install "numpy<2"
```

### `suppress_tokens index error`

```
IndexError: index -2 is out of bounds for dimension 0 with size 0
```

**Cause**: Fine-tuned model has empty `suppress_tokens` in generation config.

**Fix**: Already fixed in the latest version of the script. Update to the latest:

```bash
cd indic-voice-pipeline && git pull && bash install.sh
```

### `no_timestamps_token_id not set`

```
ValueError: no_timestamps_token_id is not set
```

**Cause**: Fine-tuned model missing timestamp configuration.

**Fix**: Already patched in the script. Ensure you're on the latest version.

### `max_new_tokens exceeds max_target_positions`

```
ValueError: max_new_tokens + decoder_input_ids exceeds max_target_positions
```

**Cause**: forced_decoder_ids consume part of the 448-token budget.

**Fix**: Already handled in the script — `safe_max_tokens` is computed dynamically.

### Missing words at chunk boundaries

**Cause**: Audio longer than 30 seconds is split into chunks. Older versions used hard boundaries.

**Fix**: The current version uses 25s chunks with 5s overlap and intelligent merge. Update to latest.

### Transcription is empty or garbled

**Possible causes**:

1. Audio is too noisy — try `--model medium` or `--model large`
2. Wrong language specified — let it auto-detect, or use `detect` command first
3. Audio codec not supported — convert to WAV first: `ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav`

## Download Issues

### yt-dlp fails to download

```
ERROR: Unable to extract video data
```

**Fix**: Update yt-dlp (sites change their APIs frequently):

```bash
pip install -U yt-dlp
```

### Video is age-restricted or private

**Fix**: yt-dlp can use browser cookies for authentication:

```bash
python3 video_downloader.py download "URL" --cookies-from-browser chrome
```

Note: Cookie-based auth is not currently built into the skill but can be added.

### Download is slow

**Possible fixes**:

- Use `--quality 720` instead of default 1080p
- Check your internet connection
- Some sites throttle downloads

## Model / Memory Issues

### MPS out of memory (Apple Silicon)

```
RuntimeError: MPS backend out of memory
```

**Fix**: Use a smaller model:

```bash
python3 whisper_transcribe.py transcribe file.mp4 --model small
# or
python3 whisper_transcribe.py transcribe file.mp4 --model base
```

### CUDA out of memory (NVIDIA GPU)

**Fix**: Same as above — use a smaller model, or set `CUDA_VISIBLE_DEVICES=""` to force CPU.

### IndicWhisper download fails

```
Failed to download: <urlopen error ...>
```

**Possible causes**:

1. No internet connection
2. E2E Networks server is down
3. Firewall blocking the download

**Fix**: Download manually and extract:

```bash
# Download the ZIP
curl -O https://indicwhisper.objectstore.e2enetworks.net/telugu_models.zip

# Extract to cache directory
mkdir -p ~/.cache/indicwhisper/telugu
unzip telugu_models.zip -d ~/.cache/indicwhisper/telugu/
touch ~/.cache/indicwhisper/telugu/.download_complete
```

### Model download stuck / slow

First downloads can take several minutes for large models. The vasista22 large-v2 models are ~3 GB. IndicWhisper models are ~600 MB each.

**Fix**: Be patient on first run. Models are cached after download — subsequent runs are instant.

## Platform-Specific Notes

### macOS (Apple Silicon)

- Uses MPS (Metal Performance Shaders) for GPU acceleration
- PyTorch MPS support is good but not as mature as CUDA
- If you hit MPS issues, set `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` to reduce memory fragmentation

### macOS (Intel)

- Falls back to CPU inference
- Transcription will be slower but still works
- Use `--model tiny` or `--model base` for reasonable speed

### Linux (with NVIDIA GPU)

- Uses CUDA automatically if available
- Install PyTorch with CUDA support: https://pytorch.org/get-started/locally/
- Best performance of all platforms

### Linux (CPU only)

- Works but slow for large models
- Recommend `--model base` or `--model small`

## Getting Help

If none of the above solutions work:

1. Run the dependency checker:

   ```bash
   python3 ~/.claude/skills/whisper-transcribe/scripts/check_deps.py
   python3 ~/.claude/skills/video-downloader/scripts/check_deps.py
   ```

2. Check Python and package versions:

   ```bash
   python3 --version
   pip show torch transformers openai-whisper yt-dlp
   ```

3. Open an issue on GitHub with the error output and your system info.
