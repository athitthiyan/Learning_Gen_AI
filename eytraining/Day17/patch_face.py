import io
import sys

FILE = "youtube_emotion_analyzer.py"

with io.open(FILE, "r", encoding="utf-8-sig") as f:
    content = f.read().replace("\r\n", "\n")

if "DEFAULT_FACE_MODEL" in content:
    print("Already patched (DEFAULT_FACE_MODEL present). Nothing to do.")
    sys.exit(0)

edits = []

edits.append((
    "face-model constant",
    'DEFAULT_PROSODY_MODEL = "superb/wav2vec2-base-superb-er"\n',
    'DEFAULT_PROSODY_MODEL = "superb/wav2vec2-base-superb-er"\n'
    'DEFAULT_FACE_MODEL = "dima806/facial_emotions_image_detection"\n',
))

edits.append((
    "__init__ signature",
    "        text_model=DEFAULT_TEXT_MODEL,\n        device=\"cpu\",",
    "        text_model=DEFAULT_TEXT_MODEL,\n"
    "        face_model=DEFAULT_FACE_MODEL,\n        device=\"cpu\",",
))

edits.append((
    "__init__ assignment",
    "        self.text_model = text_model\n        self.device = device",
    "        self.text_model = text_model\n"
    "        self.face_model = face_model\n        self.device = device",
))

old_face = '''    # ------------------------------------------------------------------ #
    # 3c. Face emotions  (DeepFace on sampled frames)
    # ------------------------------------------------------------------ #
    def analyze_face(self, video_path):
        log("Analyzing facial expressions (DeepFace on sampled frames)...")
        import cv2
        from deepface import DeepFace

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        step = max(int(fps / max(self.fps_sample, 0.01)), 1)
        totals, n, idx = {}, 0, 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % step == 0:
                try:
                    res = DeepFace.analyze(
                        frame, actions=["emotion"],
                        enforce_detection=False, silent=True,
                    )
                    emo = (res[0] if isinstance(res, list) else res)["emotion"]
                    for k, v in emo.items():
                        totals[k] = totals.get(k, 0.0) + float(v) / 100.0  # 0-100 -> 0-1
                    n += 1
                except Exception:
                    pass
            idx += 1
        cap.release()
        if n == 0:
            log("No faces detected; skipping facial emotions.", status="!")
            return {"emotions": {}, "frames_analyzed": 0}
        return {"emotions": {k: v / n for k, v in totals.items()}, "frames_analyzed": n}'''

new_face = '''    # ------------------------------------------------------------------ #
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
        return {"emotions": {k: v / n for k, v in totals.items()}, "frames_analyzed": n}'''

edits.append(("analyze_face method", old_face, new_face))

edits.append((
    "CLI flag",
    '    p.add_argument("--text-model", default=DEFAULT_TEXT_MODEL,\n'
    '                   help="HF text-classification model for language emotion")',
    '    p.add_argument("--text-model", default=DEFAULT_TEXT_MODEL,\n'
    '                   help="HF text-classification model for language emotion")\n'
    '    p.add_argument("--face-model", default=DEFAULT_FACE_MODEL,\n'
    '                   help="HF image-classification model for facial emotion (PyTorch)")',
))

edits.append((
    "main() construction",
    "        prosody_model=args.prosody_model,\n"
    "        text_model=args.text_model,\n        device=args.device,",
    "        prosody_model=args.prosody_model,\n"
    "        text_model=args.text_model,\n        face_model=args.face_model,\n"
    "        device=args.device,",
))

for label, old, new in edits:
    if old not in content:
        print("FAILED to find the section for: " + label)
        print("No changes written. Paste this message back so it can be fixed.")
        sys.exit(1)
    content = content.replace(old, new, 1)

with io.open(FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("Patched successfully. analyze_face now uses PyTorch (no TensorFlow).")
