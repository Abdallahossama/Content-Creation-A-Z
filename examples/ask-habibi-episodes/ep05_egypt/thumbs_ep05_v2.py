"""Ep 5 thumbnails v2 (user, 18 Oct 2026: every option a genuinely different composition, real people + real photos).
  A  MAP      night map of Egypt, boss Batata, "95% EMPTY"            (kept from v1: thumbnails/A_95_EMPTY.png)
  B  SPLIT    real Cairo rooftops | real empty desert, torn paper seam, shocked man (Pexels) between, "PACKED" / "EMPTY"
  C  PROOF    the real NASA photo of Egypt at night, red marker loop on the dark desert, surprised woman (Pexels), "NOBODY HERE?"
-> 5th video/export/thumbnails/  (B_PACKED_EMPTY.png, C_NOBODY_HERE_v2.png, _sheet_v2.png)"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import cinekit as CK, marker as MK
from thumbkit import W, H
OUT = "D:/why habibi/5th video/export/thumbnails/"; PH = "D:/why habibi/_media/photos_2026-10-18/"; CUT = "D:/why habibi/_media/cutouts/"

def fill(path, w, h, focus=(0.5, 0.5), sat=1.15, con=1.1, bright=1.0):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); im = im.crop((x, y, x + w, y + h))
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con); im = ImageEnhance.Brightness(im).enhance(bright)
    return im.convert("RGBA")

def person(path, h, rot=0):
    return MK.sticker(path, h, border=10, rot=rot)

def torn_seam(c, x, seed=4):
    r = np.random.default_rng(seed); pts = [(x + r.uniform(-14, 14), y) for y in range(-10, H + 20, 22)]
    d = ImageDraw.Draw(c); left = [(p[0] - 9, p[1]) for p in pts]; right = [(p[0] + 9, p[1]) for p in pts[::-1]]
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(a + 8, b) for a, b in left + right], fill=(0, 0, 0, 140)); c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.polygon(left + right, fill=(248, 244, 232, 255))

def make_B():
    c = Image.new("RGBA", (W, H)); c.alpha_composite(fill(PH + "eg_cairo_aerial.jpg", W // 2, H, (0.55, 0.7), bright=1.05), (0, 0))
    desert = fill(PH + "eg_sand_sea_iss.jpg", W // 2, H, (0.5, 0.5), sat=1.6, con=1.25, bright=1.45); desert.alpha_composite(Image.new("RGBA", desert.size, (255, 186, 90, 60))); c.alpha_composite(desert, (W // 2, 0))
    torn_seam(c, W // 2)
    for txt, x in (("PACKED", 40), ("EMPTY", W // 2 + 70)): CK.words(c, [txt], size=150, x=x, y=20, rot=-3)
    m = person(CUT + "person_shocked_man.png", 470, rot=2); MK.place(c, m, W // 2 - 10, H - m.height // 2 + 40)
    MK.strokes(c, MK.circle_path(980, 470, 150, 95, seed=3), MK.RED, 12, seed=3)            # the empty desert, circled
    CK.corner_vignette(c); return c

def make_C():
    c = fill(PH + "eg_nile_night_iss.jpg", W, H, (0.42, 0.62), sat=1.25, con=1.2, bright=1.15)
    MK.strokes(c, MK.circle_path(430, 390, 140, 90, seed=7), MK.RED, 13, seed=7)
    MK.strokes(c, MK.arrow_path((600, 200), (500, 310), bend=0.25, head=36, seed=2), MK.RED, 12, seed=2)
    CK.words(c, ["NOBODY", "HERE?"], size=140, x=30, y=10)
    w = person(CUT + "person_surprised_woman.png", 600, rot=-3); MK.place(c, w, W - w.width // 2 - 20, H - w.height // 2 + 70)
    CK.corner_vignette(c); return c

if __name__ == "__main__":
    ims = {"A_95_EMPTY": Image.open(OUT + "A_95_EMPTY.png").convert("RGBA"), "B_PACKED_EMPTY": make_B(), "C_NOBODY_HERE_v2": make_C()}
    for n, im in ims.items():
        if n != "A_95_EMPTY": im.convert("RGB").save(OUT + n + ".png"); print(OUT + n + ".png")
    sheet = Image.new("RGB", (W * 3 // 2 + 20, H // 2), (20, 20, 20))
    for k, im in enumerate(ims.values()): sheet.paste(im.convert("RGB").resize((W // 2, H // 2)), (k * (W // 2 + 10), 0))
    sheet.save(OUT + "_sheet_v2.png"); print(OUT + "_sheet_v2.png")
