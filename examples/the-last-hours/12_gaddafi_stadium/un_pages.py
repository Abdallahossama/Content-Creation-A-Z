"""UN General Assembly verbatim record A/64/PV.3 (23 Sep 2009, public domain UN official record) -> page images
media/A90p<n>_page.png + exact line boxes build/ocr/A90p<n>.json, only for the pages the Gaddafi file shows.
  uv run --no-project --with pymupdf python un_pages.py"""
import json, pymupdf
ROOT = "D:/why habibi/_newchannel/12_gaddafi_stadium/"
doc = pymupdf.open(ROOT + "media/A90_un_verbatim_record_A_64_PV3_23sep2009.pdf"); z = 2.4
KEYS = ["King of African Kings", "of which I have a copy", "Terror Council"]
for n, page in enumerate(doc):
    txt = " ".join(page.get_text().split())
    if not any(k in txt.replace("\n", " ") for k in KEYS): continue
    out = f"{ROOT}media/A90p{n + 1}_page.png"; page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False).save(out)
    rows = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t: x0, y0, x1, y1 = l["bbox"]; rows.append({"text": t, "box": [x0 * z, y0 * z, x1 * z, y1 * z]})
    rows.sort(key=lambda r: (round(r["box"][0] / 400), round(r["box"][1] / 6)))
    json.dump(rows, open(f"{ROOT}build/ocr/A90p{n + 1}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("A90", n + 1, len(rows), "rows", [k for k in KEYS if k in txt.replace("\n", " ")])
