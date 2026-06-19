# YouTube Emotion Analyzer

Analyze emotions in any YouTube video or short, fully locally — no API key, no
cost. It downloads the video, then runs up to three independent models:

| Modality   | What it measures                          | Default model                                                       |
|------------|-------------------------------------------|---------------------------------------------------------------------|
| `language` | emotion in the spoken words (7 emotions)  | Whisper transcription + `j-hartmann/emotion-english-distilroberta-base` |
| `prosody`  | emotion in voice tone (4 emotions)        | `superb/wav2vec2-base-superb-er`                                    |
| `face`     | facial expressions on sampled frames      | OpenCV detection + `dima806/facial_emotions_image_detection`        |
| `burst`    | non-verbal sounds (laughs/sighs)          | not included (prints a notice — see Limitations)                    |

**Background:** this replaces an older tool that used Hume.ai's batch Expression
Measurement API, which was retired on 2026-06-14. Everything here runs on
**PyTorch** — there is **no TensorFlow** and **no Hume dependency**, which is what
lets it work on Python 3.14.

---

## 1. Requirements

- **Python 3.10 - 3.14** (tested on 3.14, 64-bit).
- ~3 GB free disk for model weights (downloaded once, then cached).
- Internet for the first run (to fetch model weights from Hugging Face).
- **ffmpeg is NOT required** — audio is decoded by the `av` package, which bundles
  its own. (You may install ffmpeg as an optional fallback; see Troubleshooting.)

You do **not** need a GPU. CPU works; a run takes a few minutes per short.

---

## 2. Install

These commands are PowerShell (Windows). macOS/Linux are identical except where
noted. Run them from the folder that contains `youtube_emotion_analyzer.py`.

**Recommended: install everything at once.**

```powershell
pip install -r requirements.txt
```

This resolves cleanly on Python 3.14. If you prefer to install in stages (so you
only pull what each modality needs), this is the order:

```powershell
# language (lightest - start here)
pip install yt-dlp faster-whisper transformers torch numpy av

# + prosody (voice tone)
pip install librosa soundfile

# + face (facial expressions; PyTorch, no TensorFlow)
pip install opencv-python pillow
```

> **Do NOT `pip install deepface` or `tf-keras`.** They require TensorFlow, which
> has no Python 3.14 wheel and will abort the whole install with
> `ResolutionImpossible`. This tool deliberately avoids them.

> **Smaller torch download (optional):**
> `pip install torch --index-url https://download.pytorch.org/whl/cpu`

> **Linux only:** if pip says `externally-managed-environment`, append
> `--break-system-packages` to the pip command. Windows and macOS don't need it.

---

## 3. Quick start

Start with the lightest modality to confirm everything works end to end:

```powershell
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/QNQQATMQT5M" --models language --save-json
```

Then run all three:

```powershell
python youtube_emotion_analyzer.py "https://www.youtube.com/shorts/QNQQATMQT5M" --models language,prosody,face --save-json
```

The first run downloads model weights (one-time, cached afterward). You'll see a
`config.json` / `model.safetensors` download bar, then the results table and a
saved JSON path.

**Tip:** pick a video with a person clearly **talking on camera**. Music-only or
text-overlay shorts produce empty transcripts and weak face detection.

---

## 4. Usage

```powershell
# Simplest
python youtube_emotion_analyzer.py "YOUR_URL"

# Full options
python youtube_emotion_analyzer.py "YOUR_URL" `
    --output-dir "./results" `
    --models "language,prosody,face" `
    --whisper-model small `
    --fps-sample 2 `
    --save-json

# Analyze a local file instead of downloading
python youtube_emotion_analyzer.py "x" --video-path ./my_clip.mp4 --models face
```

(In PowerShell the line-continuation character is a backtick `` ` ``. In
macOS/Linux shells use a backslash `\`.)

### Options

| Option            | Description                                   | Default                  |
|-------------------|-----------------------------------------------|--------------------------|
| `youtube_url`     | YouTube video/short URL (required)            | —                        |
| `--output-dir`    | where the video + results are saved           | `./emotion_analysis`     |
| `--models`        | comma list: `language,prosody,face,burst`     | `language,prosody,face`  |
| `--whisper-model` | `tiny\|base\|small\|medium\|large`            | `base`                   |
| `--prosody-model` | HF audio-classification model id              | `superb/wav2vec2-base-superb-er` |
| `--text-model`    | HF text-classification model id               | distilroberta (above)    |
| `--face-model`    | HF image-classification model id (PyTorch)    | dima806 ViT (above)      |
| `--device`        | `cpu` or `cuda`                               | `cpu`                    |
| `--fps-sample`    | frames/sec sampled for face analysis          | `1.0`                    |
| `--save-json`     | also write detailed JSON results              | off                      |
| `--video-path`    | analyze a local file instead of downloading   | —                        |

---

## 5. How to read the results

Scores are **0-100% likelihoods**, not literal feelings. Each model has its own
label set, so names won't line up across modalities — that's expected. Two real
quirks to keep in mind:

- **Prosody often labels energetic/emphatic speech as "angry."** The voice model
  is trained on a dataset where the high-energy class is "anger," so a loud,
  forceful speaker scores high on `ang` without being angry. Read it as arousal.
- **Face scores are averaged over many frames** of a moving face, so the spread is
  usually soft. Look at the distribution, not a single top label.

Treat the three modalities as three lenses on the same moment, each with its own
bias — the combination is more informative than any one number.

---

## 6. Troubleshooting

### `ERROR: ResolutionImpossible` / `tensorflow ... no matching distribution`
You (or an old requirements file) tried to install `deepface` / `tf-keras`, which
need TensorFlow. **TensorFlow has no wheel for Python 3.14**, so pip can't resolve
it and installs **nothing** from that run. Fix: make sure `deepface` and
`tf-keras` are not in your requirements, then `pip install -r requirements.txt`.
Face emotion here uses PyTorch (`opencv-python` + `pillow`), no TensorFlow.

### `[!] Error: [WinError 2] The system cannot find the file specified`
Seen at the audio-extraction step. It means a system `ffmpeg` couldn't be found.
With the current script this should not happen, because audio is decoded by `av`.
If you see it anyway:
1. Confirm `av` is installed: `pip install av`
2. Or install ffmpeg and **restart your terminal** (winget prints
   *"restart your shell to use the new value"* — existing windows don't see the
   new PATH until reopened). On machines where Python lives under a different user
   profile, even a restart may not expose it; the `av` decoder avoids the issue
   entirely.

To put ffmpeg on PATH permanently (run once, then open a fresh terminal):

```powershell
$ff = Get-ChildItem -Path C:\Users\*\AppData\Local\Microsoft\WinGet\Packages -Recurse -Filter ffmpeg.exe -ErrorAction SilentlyContinue | Select-Object -First 1
if ($ff) {
  $u = [Environment]::GetEnvironmentVariable("Path","User")
  if ($u -notlike "*$($ff.DirectoryName)*") {
    [Environment]::SetEnvironmentVariable("Path", $u + ";" + $ff.DirectoryName, "User")
    "Added to user PATH: " + $ff.DirectoryName
  } else { "Already on user PATH." }
}
```

### Voice scores are all ~equal (e.g. every emotion ~12-13%)
The voice model's classifier head was randomly initialized — you'll see lines like
`classifier.weight | MISSING` / `projector.weight | MISSING` in the load report.
That happens with models built for older `transformers` versions (e.g.
`ehcalabres/...`). Use the default `superb/wav2vec2-base-superb-er`, whose head
loads cleanly. A correct load shows **no `MISSING` head weights** and an **uneven**
score distribution.

### Transcript is empty or just `Oh`, language scores look meaningless
The clip has little or no clear speech (music / on-screen text). Use a talking-head
video. For **non-English** speech, the language modality is weak (Whisper `base` +
an English-only emotion model) — try `--whisper-model small` and treat language
scores cautiously. Voice and face are language-agnostic.

### `Warning: You are sending unauthenticated requests to the HF Hub ...`
Harmless. It's just a download rate-limit notice. Weights are cached after the
first run, so later runs skip downloading and start fast. (To silence it, set a
free token: `setx HF_TOKEN "hf_xxx"`, then reopen the terminal.)

### `WARNING: The script yt-dlp.exe is installed in '...' which is not on PATH`
Harmless. You call the tool through `python youtube_emotion_analyzer.py`, not the
`.exe`, so PATH doesn't matter here.

### PowerShell: pasting a multi-line block fails
Paste blocks wrapped in a literal here-string `@' ... '@` so quotes and newlines
are preserved exactly. The closing `'@` must be at the very start of its own line.

### Editing / replacing the script and "it didn't change"
If you download a new copy and it seems to do nothing different, you're probably
running an old copy in a different folder. Find every copy with:

```powershell
Get-ChildItem -Path C:\Users -Recurse -Filter "youtube_emotion_analyzer*.py" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object FullName, LastWriteTime
```

Then make sure you run the one in your working folder.

---

## 7. Programmatic use

```python
from youtube_emotion_analyzer import YouTubeEmotionAnalyzer

analyzer = YouTubeEmotionAnalyzer(output_dir="./results", models=["language", "face"])
video = analyzer.download_youtube_video("YOUR_URL")
predictions = analyzer.analyze(video["path"])
summary = analyzer.process_predictions(predictions, title=video["title"])
analyzer.print_summary(summary)
analyzer.save_results(summary, "my_analysis.json")
```

---

## 8. Limitations

- Scores are model **estimates** of how a human might label an expression — not
  ground truth, and not clinical or diagnostic signals.
- **`burst`** (laughs/sighs) relied on a proprietary model and is not included;
  requesting it prints a notice rather than inventing numbers. To add it, plug a
  laughter/vocalization detector into `analyze_burst()`.
- Only analyze content you have the right to process, and respect YouTube's terms.