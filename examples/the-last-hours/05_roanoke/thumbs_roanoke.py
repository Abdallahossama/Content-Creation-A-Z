"""3 thumbnails (1280x720) for The Last Hours #4 Roanoke, in the Hakawi (@7akawi-AA) style the owner asked for:
one FULL-COLOUR cinematic real scene, a real period image ghosted in, huge question/number words on solid black/yellow blocks.
Real images only (Pexels photos, a 1667 painting, an 1876 engraving, the 1600 printed page); no women; <= 4 words.
A: WHERE DID / THEY GO?   B: 115 PEOPLE / GONE   C: ONE WORD / NO CROSS"""
import sys, os, glob, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_newchannel")
import lastkit as L
from lastkit import INK, BONE, RED, STEEL, COND, TYPE
M = "D:/why habibi/_newchannel/05_roanoke/media/"; OUT = "D:/why habibi/_newchannel/05_roanoke/export/thumbnails/"
os.makedirs(OUT, exist_ok=True)
TW, TH = 1280, 720
def P(rid): return glob.glob(M + rid + "_*")[0]

def cover(im, w, h, cx=0.5, cy=0.5, z=1.0):
    s = max(w / im.width, h / im.height) * z; cw, ch = w / s, h / s
    x0 = min(max(cx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(cy * im.height - ch / 2, 0), im.height - ch)
    return im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
def vign(im, k=0.55):
    a = np.asarray(im.convert("RGB"), np.float32); yy, xx = np.mgrid[0:im.height, 0:im.width]
    r = np.sqrt(((xx - im.width / 2) / (im.width / 2)) ** 2 + ((yy - im.height / 2) / (im.height / 2)) ** 2)
    a *= np.clip(1 - k * np.clip(r - 0.5, 0, None) ** 1.5, 0, 1)[..., None]; return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
def word(c, s, x, y, size, fill=BONE, anchor="mm", stroke=0):
    ImageDraw.Draw(c).text((x, y), s, font=L.font(COND, size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(8, 8, 8))
YEL = (255, 204, 0)
def block(c, s, x, y, size, fill=(255, 255, 255), anchor="l", pad=(22, 12)):
    """one huge word line on a solid black block; x = left edge (anchor l) or centre (anchor m); y = block centre"""
    f = L.font(COND, size); bb = f.getbbox(s); w, h = bb[2] - bb[0], bb[3] - bb[1]
    x0 = x if anchor == "l" else x - w / 2 - pad[0]
    d = ImageDraw.Draw(c); d.rectangle((x0, y - h / 2 - pad[1], x0 + w + 2 * pad[0], y + h / 2 + pad[1]), fill=(0, 0, 0, 255))
    d.text((x0 + pad[0] - bb[0], y - h / 2 - bb[1]), s, font=f, fill=fill)
    return x0 + w + 2 * pad[0]
def ellipse(c, box, width=12):
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = [(cx + rx * (1 + 0.035 * math.sin(i / 9)) * math.cos(-2.3 + 2 * math.pi * 1.1 * i / 120), cy + ry * (1 + 0.035 * math.cos(i / 7)) * math.sin(-2.3 + 2 * math.pi * 1.1 * i / 120)) for i in range(121)]
    ImageDraw.Draw(c).line(pts, fill=RED + (255,), width=width, joint="curve")
def stamp(c, s, cx, cy, size, rot=-7):
    f = L.font(COND, size); bb = f.getbbox(s); w, h = bb[2] - bb[0] + 70, bb[3] - bb[1] + 60
    lay = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((10, 10, w + 10, h + 10), fill=(10, 10, 10, 150), outline=RED + (255,), width=10); d.rectangle((26, 26, w - 6, h - 6), outline=RED + (255,), width=4)
    d.text(((w + 20) / 2, (h + 20) / 2 - 4), s, font=f, fill=RED + (255,), anchor="mm"); lay = lay.rotate(rot, Image.BICUBIC, expand=True)
    c.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))
def hgrad(w, h, x0f, x1f, a0, a1):
    g = np.clip((np.linspace(0, 1, w) - x0f) / (x1f - x0f), 0, 1); g = (a0 + (a1 - a0) * g)[None, :] * np.ones((h, 1))
    lay = Image.new("RGBA", (w, h), (8, 8, 9, 0)); lay.putalpha(Image.fromarray(g.astype(np.uint8))); return lay

IMPACT = "C:/Windows/Fonts/impact.ttf"
def blockI(c, s, x, y, size, fill=(255, 255, 255), bg=(0, 0, 0, 255), anchor="l", pad=(24, 10)):
    """Hakawi-style heavy word block (Impact)"""
    f = L.font(IMPACT, size); bb = f.getbbox(s); w, h = bb[2] - bb[0], bb[3] - bb[1]
    x0 = x if anchor == "l" else (x - w / 2 - pad[0] if anchor == "m" else x - w - 2 * pad[0])
    d = ImageDraw.Draw(c); d.rectangle((x0, y - h / 2 - pad[1], x0 + w + 2 * pad[0], y + h / 2 + pad[1]), fill=bg)
    d.text((x0 + pad[0] - bb[0], y - h / 2 - bb[1]), s, font=f, fill=fill)
    return x0 + w + 2 * pad[0]
def grade(im, sat=1.15, contrast=1.12, teal=0.10, warm=0.08):
    """cinematic grade: teal shadows, warm highlights, a little contrast (a real photo, only colour-corrected)"""
    a = np.asarray(im.convert("RGB"), np.float32) / 255; a = np.clip((a - 0.5) * contrast + 0.5, 0, 1)
    g = a.mean(2, keepdims=True); a = np.clip(g + (a - g) * sat, 0, 1); lum = g
    a = a + (1 - lum) * teal * np.array([-0.6, 0.15, 0.35]) + lum * warm * np.array([0.5, 0.15, -0.4])
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
def ghost(img, w, h, alpha, feather=120):
    """a real B&W engraving faded into the scene (Hakawi's ghosted-portrait trick)"""
    g = img.convert("L").resize((w, h), Image.LANCZOS); a = np.asarray(g, np.float32)
    ink = np.clip((235 - a) / 200, 0, 1)                      # engraving lines -> alpha
    yy, xx = np.mgrid[0:h, 0:w]; edge = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / feather
    al = np.clip(ink * np.clip(edge, 0, 1) * alpha * 255, 0, 255).astype(np.uint8)
    lay = Image.new("RGBA", (w, h), (230, 220, 200, 0)); lay.putalpha(Image.fromarray(al)); return lay
YEL = (255, 204, 0)

def CP(rid): return Image.open(P(rid)).convert("RGB")

# A: WHERE DID THEY GO?  misty forest (colour) + the 1876 CROATOAN engraving ghosted on the right
def A():
    c = grade(cover(CP("E4"), TW, TH, cx=0.55, cy=0.5), sat=1.25, teal=0.16, warm=0.10)
    eng = Image.open(P("A14")).convert("RGB"); eng = eng.crop((0, 0, int(eng.width * 0.62), eng.height))
    c.alpha_composite(ghost(eng, 640, int(640 * eng.height / eng.width), 0.55), (TW - 660, 90))
    c = vign(c, 0.5)
    blockI(c, "WHERE DID", 40, 210, 150)
    blockI(c, "THEY GO?", 40, 400, 150, fill=(0, 0, 0), bg=YEL + (255,))
    return c

# B: 115 PEOPLE / GONE  foggy marsh at dawn (colour)
def B():
    c = grade(cover(CP("E3"), TW, TH, cx=0.5, cy=0.6), sat=1.2, teal=0.12, warm=0.06)
    names = Image.open(P("A8")).convert("RGB"); names = names.crop((200, 900, 2420, 3200))
    c.alpha_composite(ghost(names, 520, int(520 * names.height / names.width), 0.35), (TW - 560, 120))
    c = vign(c, 0.45)
    blockI(c, "115 PEOPLE", 40, 470, 160, fill=YEL)
    blockI(c, "GONE", 40, 640, 130, fill=(255, 255, 255), bg=(178, 34, 34, 255))
    return c

# C: ONE WORD / NO CROSS  the 1667 storm painting (colour) + the real 1600 printed line, CROATOAN circled
def C():
    c = grade(cover(CP("C5"), TW, TH, cx=0.55, cy=0.45), sat=1.15, teal=0.10, warm=0.10)
    c = vign(c, 0.45)
    pg = Image.open(P("A12")).convert("L"); import json
    rows = json.load(open("D:/why habibi/_newchannel/05_roanoke/build/lines_A12.json")); ya, yb = rows[6][0] - 70, rows[6][1] + 60
    strip = pg.crop((420, ya, 2420, yb)); a = np.asarray(strip, np.float32); lo, hi = np.percentile(a, 5), np.percentile(a, 99)
    a = np.clip((a - lo) / (hi - lo), 0, 1); strip = Image.fromarray((a[..., None] * np.array([240, 230, 205])).astype(np.uint8))
    sw = 1180; k = sw / strip.width; strip = strip.resize((sw, int(strip.height * k)), Image.LANCZOS).convert("RGBA")
    ty0, ty1 = (rows[6][0] - ya) * k, (rows[6][1] - ya) * k; tx0, tx1 = (1650 - 420) * k, (2105 - 420) * k
    ellipse(strip, (tx0 - 26, ty0 - 26, tx1 + 26, ty1 + 22), width=9)
    card = L.print_card(strip.convert("RGB"), sw, border=10, rot=-2); c.alpha_composite(card, ((TW - card.width) // 2, 420))
    blockI(c, "ONE WORD.", 40, 150, 140)
    blockI(c, "NO CROSS.", 40, 315, 140, fill=(0, 0, 0), bg=YEL + (255,))
    return c

if __name__ == "__main__":
    names = [("A_WHERE_DID_THEY_GO", A), ("B_115_PEOPLE_GONE", B), ("C_ONE_WORD_NO_CROSS", C)]
    for name, fn in names:
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
    sheet = Image.new("RGB", (TW, TH * 3 // 2 + 20), (30, 30, 30))
    for i, (n, _) in enumerate(names):
        sheet.paste(Image.open(OUT + n + ".png").resize((TW // 2 - 10, TH // 2 - 6)), ((i % 2) * (TW // 2 + 10), (i // 2) * (TH // 2 + 10)))
    small = [Image.open(OUT + n + ".png").resize((246, 138)) for n, _ in names]
    for i, s_ in enumerate(small): sheet.paste(s_, (TW // 2 + 20 + i * 205 if i < 2 else TW // 2 + 20, TH // 2 + 30 + (0 if i < 2 else 160)))
    sheet.save(OUT + "_sheet.png"); print("ok")
