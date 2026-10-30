"""OCR document images once (RapidOCR): line boxes -> <episode>/build/ocr/<rid>.json, so DOC spotlights land on the spoken words.
rid = the file name up to the first "_" (media/A3p1_routing.jpg -> A3p1). Run alone (never beside Chatterbox or a render, LESSONS 35).
  uv run --no-project --with rapidocr_onnxruntime python ocr_pages.py <episode folder> <image> [image ...]"""
import json, os, sys
from rapidocr_onnxruntime import RapidOCR
ROOT = sys.argv[1].rstrip("/") + "/"; O = ROOT + "build/ocr/"; os.makedirs(O, exist_ok=True)
eng = RapidOCR()
for f in sys.argv[2:]:
    rid = os.path.basename(f).split("_")[0].split(".")[0]
    if os.path.exists(O + f"{rid}.json"): print("have", rid); continue
    res, _ = eng(f)
    rows = [{"box": [min(p[0] for p in b), min(p[1] for p in b), max(p[0] for p in b), max(p[1] for p in b)], "text": t, "conf": round(float(c), 3)} for b, t, c in (res or [])]
    json.dump(rows, open(O + f"{rid}.json", "w", encoding="utf-8"), indent=0); print(rid, len(rows), flush=True)
