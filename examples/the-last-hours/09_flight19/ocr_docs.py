"""OCR every Board / log page (A1-A33) once: line boxes -> build/ocr/<rid>.json, so DOC spotlights land on the right words."""
import glob, json, os, sys
from rapidocr_onnxruntime import RapidOCR
M = "D:/why habibi/_newchannel/09_flight19/media/"; O = "D:/why habibi/_newchannel/09_flight19/build/ocr/"
eng = RapidOCR()
for n in range(1, 34):
    if os.path.exists(O + f"A{n}.json"): continue
    g = glob.glob(M + f"A{n}_*")
    if not g: continue
    res, _ = eng(g[0])
    rows = [{"box": [min(p[0] for p in b), min(p[1] for p in b), max(p[0] for p in b), max(p[1] for p in b)], "text": t, "conf": round(float(c), 3)} for b, t, c in (res or [])]
    json.dump(rows, open(O + f"A{n}.json", "w", encoding="utf-8"), indent=0); print(f"A{n}", len(rows), flush=True)
