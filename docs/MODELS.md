# Model Documentation

Detailed documentation for all speech recognition models used in Indic Voice Pipeline.

## Model Architecture

All models in this pipeline are based on OpenAI's **Whisper** architecture — a transformer-based encoder-decoder model trained on 680,000 hours of multilingual audio. The fine-tuned variants take Whisper as a starting point and continue training on language-specific datasets for improved accuracy.

```
Audio Input → Mel Spectrogram → Encoder (Transformer) → Decoder (Transformer) → Text Output
                                    ↑                        ↑
                              768M-1.5B params          Language-specific
                              (depends on size)         fine-tuning
```

## Standard Whisper Models

These are the base OpenAI models. Used as fallback when no fine-tuned model is available for a language.

| Model    | Parameters | English WER | Multilingual WER | Disk Size |
| -------- | ---------- | ----------- | ---------------- | --------- |
| tiny     | 39M        | 7.6%        | 14.2%            | 75 MB     |
| base     | 74M        | 5.0%        | 10.7%            | 142 MB    |
| small    | 244M       | 3.4%        | 7.6%             | 466 MB    |
| medium   | 769M       | 2.9%        | 6.1%             | 1.5 GB    |
| large-v2 | 1.55B      | 2.7%        | 5.2%             | 2.9 GB    |

Source: [OpenAI Whisper paper](https://arxiv.org/abs/2212.04356)

## vasista22 Fine-Tuned Models

Created by the IIT Madras Speech Lab, funded by Bhashini / MeitY (Government of India). These models are hosted on HuggingFace and load automatically.

### Telugu — `vasista22/whisper-telugu-large-v2`

- **Base**: Whisper Large-v2 (1.55B parameters)
- **Training data**: Telugu speech corpus
- **HuggingFace**: https://huggingface.co/vasista22/whisper-telugu-large-v2
- **Best for**: Telugu content — news, speeches, pravachans, daily conversation

### Hindi — `vasista22/whisper-hindi-large-v2`

- **Base**: Whisper Large-v2 (1.55B parameters)
- **Training data**: Hindi speech corpus
- **HuggingFace**: https://huggingface.co/vasista22/whisper-hindi-large-v2
- **Best for**: Hindi content — Bollywood, news, education, podcasts

### Kannada — `vasista22/whisper-kannada-medium`

- **Base**: Whisper Medium (769M parameters)
- **HuggingFace**: https://huggingface.co/vasista22/whisper-kannada-medium
- **Best for**: Kannada regional content

### Gujarati — `vasista22/whisper-gujarati-medium`

- **Base**: Whisper Medium (769M parameters)
- **HuggingFace**: https://huggingface.co/vasista22/whisper-gujarati-medium
- **Best for**: Gujarati regional content

### Tamil — `vasista22/whisper-tamil-medium`

- **Base**: Whisper Medium (769M parameters)
- **HuggingFace**: https://huggingface.co/vasista22/whisper-tamil-medium
- **Best for**: Tamil regional content

## AI4Bharat IndicWhisper Models

Created by AI4Bharat at IIT Madras. Fine-tuned on the Vistaar dataset (10,700+ hours across 12 languages). These models are distributed as ZIP archives and cached locally on first use.

**Paper**: [Vistaar: Diverse Benchmarks and Training Sets for Indian Language ASR](https://arxiv.org/abs/2305.15386)

### Architecture

- **Base**: Whisper Medium (769M parameters, 24 encoder + 24 decoder layers)
- **Training**: Fine-tuned on publicly available training datasets from the Vistaar collection
- **Performance**: Lowest WER on 39 out of 59 Vistaar benchmarks

### Available Languages

| Language  | Code | ZIP Size | Cache Location                     |
| --------- | ---- | -------- | ---------------------------------- |
| Bengali   | `bn` | ~600 MB  | `~/.cache/indicwhisper/bengali/`   |
| Malayalam | `ml` | ~600 MB  | `~/.cache/indicwhisper/malayalam/` |
| Marathi   | `mr` | ~600 MB  | `~/.cache/indicwhisper/marathi/`   |
| Odia      | `or` | ~600 MB  | `~/.cache/indicwhisper/odia/`      |
| Punjabi   | `pa` | ~600 MB  | `~/.cache/indicwhisper/punjabi/`   |
| Sanskrit  | `sa` | ~600 MB  | `~/.cache/indicwhisper/sanskrit/`  |
| Urdu      | `ur` | ~600 MB  | `~/.cache/indicwhisper/urdu/`      |

### Special Notes

- **Odia**: Not in Whisper's built-in language list. The script passes `language=None` to the decoder to avoid errors.
- **First download**: Takes 2-10 minutes depending on your connection. Subsequent runs use the local cache.
- **License**: MIT (applies to all IndicWhisper models)

## Adding New Models

To add a new HuggingFace model, edit `HF_LANGUAGE_MODELS` in `whisper_transcribe.py`:

```python
HF_LANGUAGE_MODELS = {
    "te": "vasista22/whisper-telugu-large-v2",
    "hi": "vasista22/whisper-hindi-large-v2",
    # Add your model:
    "xx": "your-org/whisper-language-model",
}
```

To add a new IndicWhisper model, edit `INDICWHISPER_MODELS`:

```python
INDICWHISPER_MODELS = {
    "bn": {"name": "Bengali", "zip": "bengali_models.zip"},
    # Add your model:
    "xx": {"name": "Language", "zip": "language_models.zip"},
}
```

Also update `HF_MODEL_TO_LANG` in the `transcribe_with_hf()` function and `LANG_NAMES` at the top of the file.
