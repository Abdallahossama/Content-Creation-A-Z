"""File 26: CENTCOM FOIA PDFs (case 05-0109) + DoD reward memo -> page images media/<rid>p<n>_page.png + text-layer line boxes build/ocr/<rid>p<n>.json.
A4 = interrogation report, A5 = FRAGO 1217, A6 = FRAGO 1239, A7 = CAG info paper, A10 = reward memo. 2.4x zoom.
  uv run --no-project --with pymupdf python docs_to_pages.py"""
import json, os, fitz
ROOT = "D:/why habibi/_newchannel/26_saddam_capture/"
Z = ROOT + "media/_zip/Saddam Hussein%27s Capture/"
SRC = {"A4": Z + "Saddam Capture and Interrogation-Redacted.pdf", "A5": Z + "FRAGO 1217-Redacted.pdf", "A6": Z + "FRAGO 1239-Redacted.pdf",
       "A7": Z + "CAG Info Paper-Redacted.pdf", "A10": [f for f in [ROOT + "media/" + x for x in os.listdir(ROOT + "media")] if os.path.basename(f).startswith("A10_")][0]}
for rid, pdf in SRC.items():
    doc = fitz.open(pdf); z = 2.4
    for n, page in enumerate(doc):
        if n > 5: break
        out = f"{ROOT}media/{rid}p{n + 1}_page.png"
        page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False).save(out)
        rows = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip()
                if t: x0, y0, x1, y1 = l["bbox"]; rows.append({"text": t, "box": [x0 * z, y0 * z, x1 * z, y1 * z]})
        rows.sort(key=lambda r: (round(r["box"][1] / 6), r["box"][0]))
        json.dump(rows, open(f"{ROOT}build/ocr/{rid}p{n + 1}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(rid, n + 1, len(rows), "rows", os.path.basename(out), flush=True)
