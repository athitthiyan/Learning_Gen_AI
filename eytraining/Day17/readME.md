# YouTube Emotion Analyzer — Working Edition (TensorFlow-free)

A local, open-source rebuild of the tool from `SETUP_AND_USAGE.md`.

**Why this differs from your PDF:** the original used Hume.ai's batch Expression
Measurement API, which was **sunset on 2026-06-14** (last day to create jobs was
2026-05-14). That backend no longer returns results. This edition keeps the same
CLI, the same `YouTubeEmotionAnalyzer` class, and the same output format, but
runs everything locally with open-source models. No API key, no cost.

**Everything runs on PyTorch — no TensorFlow, no DeepFace.** This matters on
Python 3.14, where TensorFlow has no wheel yet (see Troubleshooting).

## What it analyzes

| Modality   | What it measures                          | Model (default)                                                       |
|------------|-------------------------------------------|----------------------------------------------------------------------|
| `language` | emotion in spoken words (7 emotions)      | Whisper + `j-hartmann/emotion-english-distilroberta-base`            |
| `prosody`  | emotion in voice tone                     | `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`         |
| `face`     | facial expressions on sampled frames      | OpenCV detection + `dima806/facial_emotions_image_detection` (torch) |
| `burst`    | non-verbal sounds (laughs/sighs)          | not included — was Hume-proprietary (see notes)                      |

## Setup (step by step)

**1. Install ffmpeg** (system dependency, not pip):
```bash
# Windows
winget install Gyan.FFmpeg
# macOS
brew install ffmpeg
# Ubuntu/Debian
sudo apt install ffmpeg
```

**2. Start with the lightest path — language only.** Fastest way to see it work:
```bash
pip install yt-dlp faster-whisper transformers torch
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/kpQsbOueyFI" --models language --save-json
```

**3. Add voice tone (prosody):**
```bash
pip install librosa soundfile
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/s3sxlNBtCFE" --models language,prosody
```

**4. Add facial expressions (face):**  *(PyTorch — no TensorFlow)*
```bash
pip install opencv-python pillow
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/s3sxlNBtCFE" --models language,prosody,face --save-json
```

Or install everything at once: `pip install -r requirements.txt`

> **CPU-only torch (smaller download):**
> `pip install torch --index-url https://download.pytorch.org/whl/cpu`

The first run of each modality downloads model weights from Hugging Face
(hundreds of MB to ~1 GB depending on Whisper size). They are cached after that.

## Usage

```bash
# Simplest
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/s3sxlNBtCFE"

# Full options
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/s3sxlNBtCFE" \
    --output-dir "./results" \
    --models "language,prosody,face" \
    --whisper-model small \
    --fps-sample 2 \
    --save-json

# Analyze a local file you already have (skip download)
python youtube_emotion_analyzer.py "x" --video-path ./my_clip.mp4 --models face
```

### Options
| Option            | Description                                   | Default                  |
|-------------------|-----------------------------------------------|--------------------------|
| `youtube_url`     | YouTube video/short URL (required)            | —                        |
| `--output-dir`    | where video + results are saved               | `./emotion_analysis`     |
| `--models`        | comma list: language,prosody,face,burst       | `language,prosody,face`  |
| `--whisper-model` | tiny\|base\|small\|medium\|large              | `base`                   |
| `--prosody-model` | HF audio-classification model id              | wav2vec2 SER (above)     |
| `--text-model`    | HF text-classification model id               | distilroberta (above)    |
| `--face-model`    | HF image-classification model id (PyTorch)    | dima806 ViT (above)      |
| `--device`        | `cpu` or `cuda`                               | `cpu`                    |
| `--fps-sample`    | frames/sec sampled for face analysis          | `1.0`                    |
| `--save-json`     | write detailed JSON results                   | off                      |
| `--video-path`    | analyze a local file instead of downloading   | —                        |

## Programmatic use

```python
from youtube_emotion_analyzer import YouTubeEmotionAnalyzer

analyzer = YouTubeEmotionAnalyzer(output_dir="./results", models=["language", "face"])
video = analyzer.download_youtube_video("YOUR_URL")
predictions = analyzer.analyze(video["path"])
summary = analyzer.process_predictions(predictions, title=video["title"])
analyzer.print_summary(summary)
analyzer.save_results(summary, "my_analysis.json")
```

## Troubleshooting

**`ResolutionImpossible` / `tensorflow has no matching distribution`**
You are on Python 3.14, which TensorFlow does not support yet. The old `face`
stack (deepface + tf-keras) needs TensorFlow, so it cannot install. This edition
already removed that dependency — make sure your `requirements.txt` has **no**
`deepface` or `tf-keras` lines, then reinstall. The PyTorch face model needs only
`opencv-python` and `pillow`.

If you would rather keep deepface for some reason, the alternative is to install a
Python 3.12 environment (e.g. `py -3.12 -m venv .venv`) where TensorFlow wheels
exist — but you do not need to; the PyTorch path is recommended.

**`ffmpeg` not found**
Install it (step 1) and reopen your terminal so PATH refreshes.

**`yt-dlp.exe is not on PATH` warning**
Harmless — you are calling it through `python youtube_emotion_analyzer.py`, not
the `.exe`. You can ignore it.

## Notes & honest limitations

- **Scores are not ground-truth emotions.** They are model estimates of how a
  human rater *might* label an expression — signals, not facts.
- **`burst`** (laughs/sighs) relied on Hume's proprietary model. This build does
  **not** fabricate burst numbers; requesting it prints a notice. To add it, plug
  a laughter/vocalization detector into `analyze_burst()`.
- **Emotion label sets differ per model** (face: happy/sad/angry/…, language:
  joy/anger/…), so names won't match across modalities. That's expected.
- **Speed:** on CPU expect a few minutes per short. Use `--whisper-model tiny`
  and `--fps-sample 0.5` to go faster; `--device cuda` if you have a GPU.
- Only analyze videos you have the right to process, and respect YouTube's terms.