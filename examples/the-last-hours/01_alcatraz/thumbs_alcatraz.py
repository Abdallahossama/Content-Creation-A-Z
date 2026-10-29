"""3 thumbnails (1280x720), Case File look: real archive photos in B&W bone, red marks, Franklin Gothic Cond words (<=3)."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
import lastkit as L
from lastkit import INK, BONE, RED, STEEL, COND, TYPE, SER
M = "D:/why habibi/_newchannel/01_alcatraz/media/"; OUT = "D:/why habibi/_newchannel/01_alcatraz/export/thumbs/"
import os; os.makedirs(OUT, exist_ok=True)
TW, TH = 1280, 720
ELL = (330, 270, 820, 520)

def cover(im, w, h, cx=0.5, cy=0.5, z=1.0):
    s = max(w / im.width, h / im.height) * z; cw, ch = w / s, h / s
    x0 = min(max(cx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(cy * im.height - ch / 2, 0), im.height - ch)
    return im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
def vign(im, k=0.55):
    a = np.asarray(im.convert("RGB"), np.float32); yy, xx = np.mgrid[0:im.height, 0:im.width]
    r = np.sqrt(((xx - im.width / 2) / (im.width / 2)) ** 2 + ((yy - im.height / 2) / (im.height / 2)) ** 2)
    a *= np.clip(1 - k * np.clip(r - 0.5, 0, None) ** 1.5, 0, 1)[..., None]; return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
def word(c, s, x, y, size, fill=BONE, anchor="mm", stroke=10):
    d = ImageDraw.Draw(c); f = L.font(COND, size)
    d.text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(8, 8, 8))
def ellipse(c, box, width=12):
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = [(cx + rx * (1 + 0.035 * math.sin(i / 9)) * math.cos(-2.3 + 2 * math.pi * 1.1 * i / 120), cy + ry * (1 + 0.035 * math.cos(i / 7)) * math.sin(-2.3 + 2 * math.pi * 1.1 * i / 120)) for i in range(121)]
    ImageDraw.Draw(c).line(pts, fill=RED + (255,), width=width, joint="curve")
def stamp(c, s, cx, cy, size, rot=-7):
    f = L.font(COND, size); bb = f.getbbox(s); w, h = bb[2] - bb[0] + 70, bb[3] - bb[1] + 60
    lay = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((10, 10, w + 10, h + 10), outline=RED + (255,), width=10); d.rectangle((26, 26, w - 6, h - 6), outline=RED + (255,), width=4)
    d.text(((w + 20) / 2, (h + 20) / 2 - 4), s, font=f, fill=RED + (255,), anchor="mm"); lay = lay.rotate(rot, Image.BICUBIC, expand=True)
    c.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

# A: STILL WANTED: 1962 mugshot -> 2022 age-progressed, the same man
def A():
    c = Image.new("RGBA", (TW, TH), INK + (255,))
    mug = L.print_card(L.bw(M + "A1_fbi_morris.jpg"), 330, rot=-3); old = L.print_card(L.bw(M + "A10_usms_age_morris.jpg", (0, 0, 1, 0.82)), 330, rot=2.5)
    c.alpha_composite(mug, (30, 110)); c.alpha_composite(old, (420, 95))
    d = ImageDraw.Draw(c); d.line([(385, 330), (425, 330)], fill=RED, width=10); d.polygon([(440, 330), (412, 311), (412, 349)], fill=RED)
    L.text(c, "1962", 205, 640, 50, STEEL, TYPE); L.text(c, "2022", 605, 640, 50, STEEL, TYPE)
    word(c, "STILL", 1020, 250, 165, stroke=0); word(c, "WANTED", 1020, 410, 132, fill=RED, stroke=0)
    L.text(c, "US MARSHALS", 1020, 530, 38, STEEL, TYPE)
    return c

# B: IT WAS A DUMMY: the FBI photo of the head in the bed
def B():
    c = vign(cover(L.bw(M + "B2_fbi_dummy_in_bed.jpg"), TW, TH, cx=0.62, cy=0.3, z=1.55).convert("RGBA"), 0.6)
    ellipse(c, ELL)
    lay = Image.new("RGBA", (TW, 260), (0, 0, 0, 0)); g = np.linspace(0, 1, 260)[:, None] ** 1.2 * 230
    lay.putalpha(Image.fromarray(np.repeat(g, TW, 1).astype(np.uint8))); c.alpha_composite(lay, (0, TH - 260))
    word(c, "IT WAS A DUMMY", TW / 2, TH - 110, 150, stroke=0)
    L.text(c, "7:20 AM", 1110, 70, 58, BONE, TYPE)
    return c

# C: NEVER FOUND: the island + the three men
def C():
    c = vign(cover(L.bw(M + "F3_nps_aerial_1950a.jpg", (0, 0, 1, 0.955)), TW, TH, cx=0.5, cy=0.5, z=1.15).convert("RGBA"), 0.7)
    c.alpha_composite(Image.new("RGBA", (TW, TH), (0, 0, 0, 90)))
    for k, (p, cr) in enumerate([("A1_fbi_morris.jpg", None), ("mug_john_anglin.jpg", (0, 0, 1, 0.78)), ("mug_clarence_anglin.jpg", None)]):
        pc = L.print_card(L.bw(M + p, cr), 250, border=12, rot=(-4, 2, -2)[k]); c.alpha_composite(pc, (60 + k * 230, 40 + (k % 2) * 30))
    stamp(c, "NEVER FOUND", 900, 520, 120)
    L.text(c, "3 MEN  ·  1962", 330, 650, 46, BONE, TYPE)
    return c

for name, fn in [("A_STILL_WANTED", A), ("B_IT_WAS_A_DUMMY", B), ("C_NEVER_FOUND", C)]:
    im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
sheet = Image.new("RGB", (TW, TH * 3 // 2 + 20), (30, 30, 30))
for i, n in enumerate(["A_STILL_WANTED", "B_IT_WAS_A_DUMMY", "C_NEVER_FOUND"]):
    sheet.paste(Image.open(OUT + n + ".png").resize((TW // 2 - 10, TH // 2 - 6)), ((i % 2) * (TW // 2 + 10), (i // 2) * (TH // 2 + 10)))
sheet.save(OUT + "_sheet.png"); print("ok")
