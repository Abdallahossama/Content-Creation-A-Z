"""Find phrases in an episode's OCR rows (build/ocr/<rid>.json): prints rid, row index, box and text, to pick DOC pages and marks.
  uv run --no-project python ocr_find.py <episode folder> "phrase" ["phrase" ...]"""
import glob, json, os, re, sys
def nrm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
ROOT = sys.argv[1].rstrip("/") + "/"
for q in sys.argv[2:]:
    n = nrm(q); print("==", q)
    for f in sorted(glob.glob(ROOT + "build/ocr/*.json")):
        rows = json.load(open(f, encoding="utf-8")); rid = os.path.basename(f)[:-5]
        for i, r in enumerate(rows):
            if n in nrm(r["text"]): print(f"  {rid:6} row {i:3d} {[int(v) for v in r['box']]}  {r['text'][:90]}")
