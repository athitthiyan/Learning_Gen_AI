#!/usr/bin/env python3
"""
YouTube Emotion Analysis Tool (open-source local edition)
=========================================================

A drop-in rebuild of the tool described in SETUP_AND_USAGE.md.

The original relied on Hume.ai's batch Expression Measurement API, which was
sunset on 2026-06-14. This version keeps the same command-line interface, the
same `YouTubeEmotionAnalyzer` class, and the same output format, but performs
all inference LOCALLY with open-source models. No API key required, no cost.

Modalities (choose with --models, comma separated):
  language : transcribe speech (Whisper) -> 7-emotion text classifier
  prosody  : speech emotion recognition from tone/voice (wav2vec2)
  face     : facial-expression emotion from sampled video frames (DeepFace)
  burst    : non-verbal vocalizations (laughs/sighs) -- see note below

Each modality lazily imports its own dependencies, so you only need to install
what you actually use. Start with `language` (lightest) to see it working.

Run `python youtube_emotion_analyzer.py --help` for options.
"""

import argparse
import json
import shutil
import os
import subprocess
import sys
from datetime import datetime

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

SUPPORTED_MODELS = ["language", "prosody", "face", "burst"]
DEFAULT_TEXT_MODEL = "j-hartmann/emotion-english-distilroberta-base"
DEFAULT_PROSODY_MODEL = "superb/wav2vec2-base-superb-er"
# Facial-emotion model runs on PyTorch via transformers (no TensorFlow needed).
DEFAULT_FACE_MODEL = "dima806/facial_emotions_image_detection"


def log(msg, status="*"):
    """Mirror the [*]/[v]/[!] status style of the original tool."""
    print(f"[{status}] {msg}")


# ----------------------------------------------------------------------------
# Analyzer
# ----------------------------------------------------------------------------

class YouTubeEmotionAnalyzer:
    """Download a YouTube video and analyze emotions across several modalities.

    Heavy ML libraries (torch, transformers, faster-whisper, librosa, opencv)
    are imported lazily inside the methods that need them, so importing or
    running --help never requires them. Facial emotion uses a PyTorch model,
    so TensorFlow is NOT a dependency.
    """

    def __init__(
        self,
        output_dir="./emotion_analysis",
        models=None,
        whisper_model="base",
        prosody_model=DEFAULT_PROSODY_MODEL,
        text_model=DEFAULT_TEXT_MODEL,
        face_model=DEFAULT_FACE_MODEL,
        device="cpu",
        fps_sample=1.0,
    ):
        self.output_dir = output_dir
        self.models = models or ["language", "prosody", "face"]
        self.whisper_model = whisper_model
        self.prosody_model = prosody_model
        self.text_model = text_model
        self.face_model = face_model
        self.device = device
        self.fps_sample = fps_sample
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # 1. Download
    # ------------------------------------------------------------------ #
    def download_youtube_video(self, url):
        """Download a YouTube video/short with yt-dlp. Returns {path, title}."""
        import yt_dlp

        log(f"Downloading YouTube video from:\n    {url}")
        outtmpl = os.path.join(self.output_dir, "%(id)s.%(ext)s")
        ydl_opts = {
            # prefer a single mp4 file with both audio+video
            "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "outtmpl": outtmpl,
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)
            # prepare_filename may report pre-merge extension; fix to mp4
            if not os.path.exists(path):
                base = os.path.splitext(path)[0]
                for ext in (".mp4", ".mkv", ".webm"):
                    if os.path.exists(base + ext):
                        path = base + ext
                        break
        title = info.get("title", "Unknown")
        log(f"Downloaded: {title}", status="v")
        return {"path": path, "title": title}

    # ------------------------------------------------------------------ #
    # 2. Audio extraction (needed by language / prosody / burst)
    #    Primary path uses PyAV, which bundles its own ffmpeg, so a system
    #    ffmpeg on PATH is NOT required. Falls back to a system ffmpeg binary.
    # ------------------------------------------------------------------ #
    def extract_audio(self, video_path):
        """Extract a 16 kHz mono WAV next to the video. Returns the wav path."""
        wav_path = os.path.splitext(video_path)[0] + ".wav"
        if os.path.exists(wav_path):
            return wav_path

        # --- Primary: PyAV (bundled ffmpeg; installed with faster-whisper) ---
        try:
            log("Extracting audio (16 kHz mono WAV) via PyAV...")
            self._extract_audio_pyav(video_path, wav_path)
            return wav_path
        except Exception as e:
            log(f"PyAV path unavailable ({e}); trying a system ffmpeg...", status="!")

        # --- Fallback: system ffmpeg binary ---
        ffmpeg = shutil.which("ffmpeg") or self._find_ffmpeg_binary()
        if not ffmpeg:
            raise RuntimeError(
                "Could not extract audio. PyAV failed and no ffmpeg binary was "
                "found on PATH.\nFix options:\n"
                "  * Close and reopen your terminal (winget just added ffmpeg to "
                "PATH; existing shells don't see it until restarted), or\n"
                "  * pip install av   (provides a bundled decoder, no PATH needed)."
            )
        cmd = [ffmpeg, "-y", "-i", video_path, "-ac", "1", "-ar", "16000", "-vn", wav_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("ffmpeg failed to extract audio:\n" + result.stderr[-500:])
        return wav_path

    @staticmethod
    def _extract_audio_pyav(video_path, wav_path):
        """Decode + resample to 16 kHz mono PCM using PyAV, write with soundfile."""
        import av
        import numpy as np
        import soundfile as sf

        container = av.open(video_path)
        try:
            audio_stream = next(s for s in container.streams if s.type == "audio")
        except StopIteration:
            container.close()
            raise RuntimeError("no audio stream in file")

        resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
        chunks = []

        def collect(frames):
            for fr in frames:
                arr = fr.to_ndarray()  # mono s16 -> shape (1, n)
                chunks.append(np.asarray(arr).reshape(-1))

        for frame in container.decode(audio_stream):
            collect(resampler.resample(frame))
        collect(resampler.resample(None))  # flush buffered samples
        container.close()

        if not chunks:
            raise RuntimeError("no audio frames decoded")
        audio = np.concatenate(chunks).astype("int16")
        sf.write(wav_path, audio, 16000, subtype="PCM_16")

    @staticmethod
    def _find_ffmpeg_binary():
        """Look in common Windows winget install locations as a last resort."""
        local = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(local, "Microsoft", "WinGet", "Links", "ffmpeg.exe"),
        ]
        for c in candidates:
            if c and os.path.exists(c):
                return c
        return None

    # ------------------------------------------------------------------ #
    # 3a. Language emotions  (Whisper transcription -> text classifier)
    # ------------------------------------------------------------------ #
    def analyze_language(self, audio_path):
        log("Analyzing language emotions (transcribe + text classifier)...")
        from faster_whisper import WhisperModel
        from transformers import pipeline

        # transcribe
        wm = WhisperModel(self.whisper_model, device=self.device, compute_type="int8")
        segments, _ = wm.transcribe(audio_path)
        transcript = " ".join(seg.text.strip() for seg in segments).strip()
        if not transcript:
            log("No speech detected; skipping language emotions.", status="!")
            return {"_transcript": "", "emotions": {}}

        clf = pipeline(
            "text-classification",
            model=self.text_model,
            top_k=None,
            device=0 if self.device == "cuda" else -1,
        )
        # classify in <=400-word chunks, average the scores
        words = transcript.split()
        chunks = [" ".join(words[i:i + 400]) for i in range(0, len(words), 400)] or [transcript]
        totals, n = {}, 0
        for chunk in chunks:
            for item in clf(chunk)[0]:
                totals[item["label"]] = totals.get(item["label"], 0.0) + item["score"]
            n += 1
        emotions = {k: v / n for k, v in totals.items()}
        return {"_transcript": transcript, "emotions": emotions}

    # ------------------------------------------------------------------ #
    # 3b. Prosody emotions  (speech emotion recognition from voice tone)
    # ------------------------------------------------------------------ #
    def analyze_prosody(self, audio_path):
        log("Analyzing voice tone & prosody (speech emotion recognition)...")
        import librosa
        import numpy as np
        from transformers import pipeline

        clf = pipeline(
            "audio-classification",
            model=self.prosody_model,
            top_k=None,
            device=0 if self.device == "cuda" else -1,
        )
        # window the audio into 10s segments and average
        y, sr = librosa.load(audio_path, sr=16000, mono=True)
        win = 10 * sr
        windows = [y[i:i + win] for i in range(0, len(y), win)] or [y]
        totals, n = {}, 0
        for w in windows:
            if len(w) < sr:  # skip <1s tails
                continue
            for item in clf({"array": np.asarray(w, dtype=np.float32), "sampling_rate": sr}):
                totals[item["label"]] = totals.get(item["label"], 0.0) + item["score"]
            n += 1
        if n == 0:
            return {"emotions": {}}
        return {"emotions": {k: v / n for k, v in totals.items()}}

    # ------------------------------------------------------------------ #
    # 3c. Face emotions  (OpenCV face detection + PyTorch ViT classifier)
    #     No TensorFlow required.
    # ------------------------------------------------------------------ #
    def analyze_face(self, video_path):
        log("Analyzing facial expressions (OpenCV + PyTorch classifier)...")
        import cv2
        from PIL import Image
        from transformers import pipeline

        clf = pipeline(
            "image-classification",
            model=self.face_model,
            top_k=None,
            device=0 if self.device == "cuda" else -1,
        )
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(cascade_path)

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        step = max(int(fps / max(self.fps_sample, 0.01)), 1)
        totals, n, idx = {}, 0, 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % step == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                # if a face is found, classify the largest crop; else use whole frame
                if len(faces):
                    x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
                    crop = frame[y:y + h, x:x + w]
                else:
                    crop = frame
                try:
                    pil = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                    for item in clf(pil):
                        label = item["label"].lower()
                        totals[label] = totals.get(label, 0.0) + float(item["score"])
                    n += 1
                except Exception:
                    pass
            idx += 1
        cap.release()
        if n == 0:
            log("No frames analyzed; skipping facial emotions.", status="!")
            return {"emotions": {}, "frames_analyzed": 0}
        return {"emotions": {k: v / n for k, v in totals.items()}, "frames_analyzed": n}

    # ------------------------------------------------------------------ #
    # 3d. Burst  (non-verbal vocalizations) -- honest stub
    # ------------------------------------------------------------------ #
    def analyze_burst(self, audio_path):
        log(
            "Non-verbal 'burst' detection (laughs/sighs) used Hume's proprietary "
            "model, which is retired. This open-source build does not fabricate "
            "burst scores. Install a dedicated laughter-detection model to add it.",
            status="!",
        )
        return {"emotions": {}, "note": "burst model not included in open-source build"}

    # ------------------------------------------------------------------ #
    # Orchestration
    # ------------------------------------------------------------------ #
    def analyze(self, video_path):
        """Run all requested modalities. Returns a predictions dict."""
        predictions = {}
        needs_audio = any(m in self.models for m in ("language", "prosody", "burst"))
        audio_path = self.extract_audio(video_path) if needs_audio else None

        if "face" in self.models:
            predictions["face"] = self.analyze_face(video_path)
        if "prosody" in self.models:
            predictions["prosody"] = self.analyze_prosody(audio_path)
        if "language" in self.models:
            predictions["language"] = self.analyze_language(audio_path)
        if "burst" in self.models:
            predictions["burst"] = self.analyze_burst(audio_path)
        return predictions

    # ------------------------------------------------------------------ #
    # Post-processing / formatting
    # ------------------------------------------------------------------ #
    @staticmethod
    def _top(emotions, k=5):
        return dict(sorted(emotions.items(), key=lambda kv: kv[1], reverse=True)[:k])

    def process_predictions(self, predictions, title="Unknown"):
        """Build a structured summary similar to the original JSON output."""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "video_title": title,
            "models_used": self.models,
        }
        if "face" in predictions:
            summary["face_emotions"] = self._top(predictions["face"].get("emotions", {}))
        if "prosody" in predictions:
            summary["voice_emotions"] = self._top(predictions["prosody"].get("emotions", {}))
        if "burst" in predictions:
            summary["burst_emotions"] = self._top(predictions["burst"].get("emotions", {}))
        if "language" in predictions:
            lang = predictions["language"]
            summary["language_emotions"] = self._top(lang.get("emotions", {}))
            summary["transcript"] = lang.get("_transcript", "")
        return summary

    def print_summary(self, summary):
        line = "=" * 60
        print("\n" + line)
        print("EMOTION ANALYSIS RESULTS")
        print(f"  {summary.get('video_title', 'Unknown')}")
        print(line)

        def block(header, emotions):
            if not emotions:
                return
            print(f"\n[{header}]")
            for name, score in emotions.items():
                print(f"  {name:<26} {score * 100:5.1f}%")

        block("FACIAL EXPRESSIONS", summary.get("face_emotions", {}))
        block("VOICE TONE & PROSODY", summary.get("voice_emotions", {}))
        block("VOCALIZATIONS (Laughs, Sighs, etc.)", summary.get("burst_emotions", {}))
        block("LANGUAGE / TEXT SENTIMENT", summary.get("language_emotions", {}))

        if summary.get("transcript"):
            t = summary["transcript"]
            print("\n[TRANSCRIPT]")
            print("  " + (t[:300] + ("..." if len(t) > 300 else "")))
        print("\n" + line + "\n")

    def save_results(self, summary, filename=None):
        if filename is None:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"emotion_analysis_{stamp}.json")
        with open(filename, "w") as f:
            json.dump(summary, f, indent=2)
        log(f"Saved detailed results to: {filename}", status="v")
        return filename


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Analyze emotions in a YouTube video (open-source local edition)."
    )
    p.add_argument("youtube_url", help="YouTube video/short URL (required)")
    p.add_argument("--output-dir", default="./emotion_analysis",
                   help="Directory to save video and results (default: ./emotion_analysis)")
    p.add_argument("--models", default="language,prosody,face",
                   help="Comma-separated: language,prosody,face,burst "
                        "(default: language,prosody,face)")
    p.add_argument("--whisper-model", default="base",
                   help="Whisper size for transcription: tiny|base|small|medium|large "
                        "(default: base)")
    p.add_argument("--prosody-model", default=DEFAULT_PROSODY_MODEL,
                   help="HF audio-classification model for voice emotion")
    p.add_argument("--text-model", default=DEFAULT_TEXT_MODEL,
                   help="HF text-classification model for language emotion")
    p.add_argument("--face-model", default=DEFAULT_FACE_MODEL,
                   help="HF image-classification model for facial emotion (PyTorch)")
    p.add_argument("--device", default="cpu", choices=["cpu", "cuda"],
                   help="Inference device (default: cpu)")
    p.add_argument("--fps-sample", type=float, default=1.0,
                   help="Frames per second to sample for face analysis (default: 1.0)")
    p.add_argument("--save-json", action="store_true",
                   help="Save detailed results to JSON")
    p.add_argument("--video-path",
                   help="Skip download and analyze a local video file instead")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    bad = [m for m in models if m not in SUPPORTED_MODELS]
    if bad:
        log(f"Unknown model(s): {bad}. Supported: {SUPPORTED_MODELS}", status="!")
        return 2

    analyzer = YouTubeEmotionAnalyzer(
        output_dir=args.output_dir,
        models=models,
        whisper_model=args.whisper_model,
        prosody_model=args.prosody_model,
        text_model=args.text_model,
        face_model=args.face_model,
        device=args.device,
        fps_sample=args.fps_sample,
    )

    try:
        if args.video_path:
            video = {"path": args.video_path, "title": os.path.basename(args.video_path)}
        else:
            video = analyzer.download_youtube_video(args.youtube_url)

        log(f"Preparing models: {models}")
        predictions = analyzer.analyze(video["path"])
        log("Processing predictions...")
        summary = analyzer.process_predictions(predictions, title=video["title"])
        analyzer.print_summary(summary)
        if args.save_json:
            analyzer.save_results(summary)
    except Exception as e:
        log(f"Error: {e}", status="!")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())