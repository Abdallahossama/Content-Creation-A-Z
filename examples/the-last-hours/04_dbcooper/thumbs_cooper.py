"""3 thumbnails (1280x720) for The Last Hours #3 D.B. Cooper, Case File look: real FBI images in B&W bone, red marks, <=3 words.
Layout from the Hakawi lesson: one big real scene + huge words on solid black blocks (white / yellow).
A: NOT HIS NAME   B: $200,000 / NEVER FOUND   C: EVERYTHING IS OK (quoted)"""
import sys, os, glob, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_newchannel")
import lastkit as L
from lastkit import INK, BONE, RED, STEEL, COND, TYPE
M = "D:/why habibi/_newchannel/04_dbcooper/media/"; OUT = "D:/why habibi/_newchannel/04_dbcooper/export/thumbnails/"
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


# A: NOT HIS NAME  the real ticket, 'DAN COOPER' circled, the FBI sketch on the right
def A():
    c = Image.new("RGBA", (TW, TH), INK + (255,))
    t = L.bw(P("A12"), (0.06, 0.15, 0.62, 0.62)).resize((900, 720), Image.LANCZOS).convert("RGBA")
    c.alpha_composite(t, (0, 0)); ellipse(c, (40, 140, 560, 330), width=13)
    sk = cover(L.bw(P("A10"), (0.08, 0.06, 0.92, 0.74)), 520, 720).convert("RGBA")
    m = np.clip(np.arange(520) / 110, 0, 1)[None, :] * np.ones((720, 1)) * 255; sk.putalpha(Image.fromarray(m.astype(np.uint8)))
    c.alpha_composite(sk, (TW - 520, 0)); c = vign(c, 0.35)
    x1 = block(c, "NOT HIS", 40, TH - 215, 150); block(c, "NAME", 40, TH - 85, 150, fill=YEL)
    return c

# B: $200,000 / NEVER FOUND  the sketch, the money from the river
def B():
    c = Image.new("RGBA", (TW, TH), INK + (255,))
    mo = cover(L.bw(P("A2")), 760, 720).convert("RGBA"); c.alpha_composite(mo, (0, 0))
    c.alpha_composite(hgrad(TW, TH, 0.0, 0.6, 150, 245))
    sk = cover(L.bw(P("A10"), (0.05, 0.04, 0.95, 0.8)), 600, 720).convert("RGBA")
    m = np.clip(np.arange(600) / 130, 0, 1)[None, :] * np.ones((720, 1)) * 255; sk.putalpha(Image.fromarray(m.astype(np.uint8)))
    c.alpha_composite(sk, (TW - 600, 0)); c = vign(c, 0.35)
    block(c, "$200,000", 40, 250, 170, fill=YEL)
    block(c, "NEVER FOUND", 40, 450, 140, fill=(255, 255, 255))
    return c

# C: "EVERYTHING IS OK"  the 727 from below (1973), its rear stairs circled; words in the empty sky on the right
def rblock(c, s, xr, y, size, fill):
    f = L.font(COND, size); bb = f.getbbox(s); return block(c, s, xr - (bb[2] - bb[0]) - 44, y, size, fill=fill)
def C():
    c = Image.new("RGBA", (TW, TH), INK + (255,))
    pl = L.bw(P("B2"), (0.0, 0.15, 1.0, 0.525)).resize((TW, TH), Image.LANCZOS).convert("RGBA"); c.alpha_composite(pl, (0, 0))
    c.alpha_composite(hgrad(TW, TH, 0.55, 1.0, 0, 120)); c = vign(c, 0.4)
    ellipse(c, (545, 575, 700, 695), width=12)
    rblock(c, "“EVERYTHING", TW - 30, 200, 118, (255, 255, 255))
    rblock(c, "IS OK”", TW - 30, 350, 118, YEL)
    return c

if __name__ == "__main__":
    names = [("A_NOT_HIS_NAME", A), ("B_NEVER_FOUND", B), ("C_EVERYTHING_OK", C)]
    for name, fn in names:
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
    sheet = Image.new("RGB", (TW, TH * 3 // 2 + 20), (30, 30, 30))
    for i, (n, _) in enumerate(names):
        sheet.paste(Image.open(OUT + n + ".png").resize((TW // 2 - 10, TH // 2 - 6)), ((i % 2) * (TW // 2 + 10), (i // 2) * (TH // 2 + 10)))
    small = [Image.open(OUT + n + ".png").resize((246, 138)) for n, _ in names]      # feed size check
    for i, s_ in enumerate(small): sheet.paste(s_, (TW // 2 + 20 + i * 205 if i < 2 else TW // 2 + 20, TH // 2 + 30 + (0 if i < 2 else 160)))
    sheet.save(OUT + "_sheet.png"); print("ok")
