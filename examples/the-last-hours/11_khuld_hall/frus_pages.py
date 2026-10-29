"""FRUS 1977-80 vol. XVIII docs 138 and 139 (US State Department text, public domain) typeset as plain pages, in the AAD
print style (Times on white, like the cable PDFs), with the source line on top: media/A27p1_page.png, A28p1_page.png +
line boxes build/ocr/A27p1.json, A28p1.json. The words are the published text, unchanged; only the paragraphs we quote.
  uv run --no-project --with pillow --with beautifulsoup4 python frus_pages.py"""
import json, re, textwrap, glob
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
ROOT = "D:/why habibi/_newchannel/11_khuld_hall/"
F = ImageFont.truetype("C:/Windows/Fonts/times.ttf", 34); FH = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
DOCS = [("A27", "doc_138", "Foreign Relations of the United States, 1977–1980, Volume XVIII, Document 138",
         ["138. Telegram From the Interests Section in Iraq to the Department of State", "Baghdad, July 17, 1979, 0957Z"], ("2. Summary:",)),
        ("A28", "doc_139", "Foreign Relations of the United States, 1977–1980, Volume XVIII, Document 139",
         ["139. Telegram From the Interests Section in Iraq to the Department of State", "Baghdad, February 4, 1980, 0947Z", "Subj: Saddam Hussein: Part I—The Man."], ("14. Any vestigial",))]
for rid, key, src, head, starts in DOCS:
    f = glob.glob(f"{ROOT}media/{rid}_*{key}*.html")[0]
    s = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
    paras = [re.sub(r"\s+", " ", p.get_text(" ", strip=True)) for p in s.find_all("p")]
    body = [p for p in paras if p.startswith(starts)]
    im = Image.new("RGB", (1470, 1900), "white"); d = ImageDraw.Draw(im); rows = []; y = 60
    d.text((735, y), src, font=FH, fill=(120, 120, 120), anchor="mt"); y += 110
    def put(t, y, font=F):
        x0, y0, x1, y1 = d.textbbox((88, y), t, font=font); d.text((88, y), t, font=font, fill=(0, 0, 0)); rows.append({"text": t, "box": [x0, y0, x1, y1]})
    for h in head: put(h, y); y += 52
    y += 40
    for p in body:
        for ln in textwrap.wrap(p, 70): put(ln, y); y += 50
        y += 40
    im.crop((0, 0, 1470, max(900, y + 80))).save(f"{ROOT}media/{rid}p1_page.png")
    json.dump(rows, open(f"{ROOT}build/ocr/{rid}p1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(rid, len(rows), "rows"); [print(" ", i, r["text"]) for i, r in enumerate(rows)]
