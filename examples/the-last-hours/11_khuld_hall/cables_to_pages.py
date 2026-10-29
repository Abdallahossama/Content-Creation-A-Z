"""AAD cable PDFs (State Department telegrams as typed by NARA's AAD) -> page images media/<rid>_p<n>.png + line boxes
build/ocr/<rid>_p<n>.json (from the PDF's own text layer: exact, no OCR). 2.4x zoom (about 1470 px wide).
  uv run --no-project --with pymupdf python cables_to_pages.py"""
import glob, json, os, fitz
ROOT = "D:/why habibi/_newchannel/11_khuld_hall/"
for pdf in sorted(glob.glob(ROOT + "media/A*.pdf")):
    rid = os.path.basename(pdf).split("_")[0]; doc = fitz.open(pdf); z = 2.4
    for n, page in enumerate(doc):
        out = f"{ROOT}media/{rid}p{n + 1}_page.png"
        page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False).save(out)
        rows = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip()
                if t: x0, y0, x1, y1 = l["bbox"]; rows.append({"text": t, "box": [x0 * z, y0 * z, x1 * z, y1 * z]})
        rows.sort(key=lambda r: (round(r["box"][1] / 6), r["box"][0]))
        json.dump(rows, open(f"{ROOT}build/ocr/{rid}p{n + 1}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(rid, n + 1, len(rows), "rows", os.path.basename(out))
