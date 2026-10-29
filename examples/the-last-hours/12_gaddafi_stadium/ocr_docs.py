"""OCR the scanned document pages once (FBIS, State, LoC, CIA: the A* page images): line boxes -> build/ocr/<rid>.json, so DOC
spotlights land on the right words. The UN record (A90p*) gets exact boxes from un_pages.py instead.
Run alone (never beside Chatterbox or a render).  uv run --no-project --with rapidocr_onnxruntime python ocr_docs.py"""
import glob, json, os, re
from rapidocr_onnxruntime import RapidOCR
M = "D:/why habibi/_newchannel/12_gaddafi_stadium/media/"; O = "D:/why habibi/_newchannel/12_gaddafi_stadium/build/ocr/"; os.makedirs(O, exist_ok=True)
eng = RapidOCR()
for f in sorted(glob.glob(M + "A*")):
    rid = os.path.basename(f).split("_")[0]
    if not re.fullmatch(r"A\d+b?", rid) or not f.lower().endswith((".jpg", ".png")) or os.path.exists(O + f"{rid}.json"): continue
    res, _ = eng(f)
    rows = [{"box": [min(p[0] for p in b), min(p[1] for p in b), max(p[0] for p in b), max(p[1] for p in b)], "text": t, "conf": round(float(c), 3)} for b, t, c in (res or [])]
    json.dump(rows, open(O + f"{rid}.json", "w", encoding="utf-8"), indent=0); print(rid, len(rows), flush=True)
