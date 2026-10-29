"""OCR the scanned document pages once (FBIS A1-A6, FBI A7-A11, CIA A26): line boxes -> build/ocr/<rid>.json, so DOC spotlights land
on the right words. Cables and FRUS pages get exact boxes from cables_to_pages.py / frus_pages.py instead.
Run alone (never beside Chatterbox or a render).  uv run --no-project --with rapidocr_onnxruntime python ocr_docs.py"""
import glob, json, os
from rapidocr_onnxruntime import RapidOCR
M = "D:/why habibi/_newchannel/11_khuld_hall/media/"; O = "D:/why habibi/_newchannel/11_khuld_hall/build/ocr/"
eng = RapidOCR()
for n in list(range(1, 12)) + [26]:
    if os.path.exists(O + f"A{n}.json"): continue
    g = [f for f in glob.glob(M + f"A{n}_*") if f.lower().endswith((".jpg", ".png"))]
    if not g: continue
    res, _ = eng(g[0])
    rows = [{"box": [min(p[0] for p in b), min(p[1] for p in b), max(p[0] for p in b), max(p[1] for p in b)], "text": t, "conf": round(float(c), 3)} for b, t, c in (res or [])]
    json.dump(rows, open(O + f"A{n}.json", "w", encoding="utf-8"), indent=0); print(f"A{n}", len(rows), flush=True)
