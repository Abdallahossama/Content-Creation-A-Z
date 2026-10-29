"""Benghazi stadium (file 11) thumbnails, round 2: four more styles taken from the niche's viral hits (research/thumb_styles, 25 Oct):
D  VHS "on TV" (The Dark Archive, 2.1-2.4M): a face through a CRT/VHS finish, red condensed words, a red REC dot, a camcorder date.
   "HANGED / ON LIBYAN TV" is Amnesty's account (1985: shown being hanged on Libyan television).
E  one red word (Penguin History "PURGE", 7.1M): a face fading into a deep red field, one huge red word with a white edge.
F  flag field (Penguin History "GADDAFI", 1.1M): Libya's plain green 1977-2011 flag colour, the face, one huge spaced word.
G  eyes + stamp (Real Crime, 1.5M): an eyes-only crop, our own red TOP SECRET stamp (no agency seal), 3 words.
   "THE CIA KNEW" is true of the record: FBIS, which translated every hanging bulletin within a day, was part of the CIA.
Faces: U.S. Navy 2009 (B2, PD), European Commission 2004 (B5, CC BY 4.0), Kremlin.ru 2008 (B7, CC BY 4.0). No broadcast frames, no rope.
  uv run --no-project --with pillow --with numpy python thumbs_gaddafi_v2.py"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, vign, block, paste_faded, TW, TH, YEL, WHITE, RED, IMPACT
EP = "12_gaddafi_stadium"; OUT = "D:/why habibi/_newchannel/12_gaddafi_stadium/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None
DATE = "5 JUNE 1984"

def crop(prefix, box):
    m = src(EP, prefix); return m.crop(tuple(int(v * s) for v, s in zip(box, (m.width, m.height, m.width, m.height))))
def fit_h(m, h): return m.resize((int(m.width * h / m.height), h), Image.LANCZOS)
def vhs(im, red=0.22):
    """CRT / VHS finish: colour bleed, scanlines, noise, a red-teal cast"""
    a = np.asarray(im.convert("RGB"), np.float32)
    r = np.roll(a[..., 0], 5, axis=1); b = np.roll(a[..., 2], -5, axis=1); a = np.stack([r, a[..., 1], b], -1)
    a[::3] *= 0.78                                                         # scanlines
    a += np.random.default_rng(3).normal(0, 9, a.shape[:2])[..., None]     # tape noise
    a = a * np.array([1 + red, 1 - red * 0.35, 1 - red * 0.2], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
def red_text(c, s, x, y, size, fill=(225, 30, 30), edge=None, glow=True, spacing=0):
    f = ImageFont.truetype(IMPACT, size); lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if spacing:
        for ch in s: d.text((x, y), ch, font=f, fill=fill + (255,)); x += f.getlength(ch) + spacing
    else: d.text((x, y), s, font=f, fill=fill + (255,), stroke_width=edge[1] if edge else 0, stroke_fill=(edge[0] + (255,)) if edge else None)
    if glow:
        g = lay.filter(ImageFilter.GaussianBlur(14)); c.alpha_composite(Image.composite(Image.new("RGBA", c.size, (0, 0, 0, 200)), Image.new("RGBA", c.size, (0, 0, 0, 0)), g.split()[3]))
    c.alpha_composite(lay)
def grain(c, k=10):
    a = np.asarray(c.convert("RGB"), np.float32) + np.random.default_rng(9).normal(0, k, (c.height, c.width))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def D():   # VHS: HANGED / (REC) ON LIBYAN TV  + camcorder date
    f = crop("B5_", (0.0, 0.02, 1.0, 0.95)); bg = Image.new("RGB", (TW, TH), (14, 10, 10))
    f = fit_h(grade(f, sat=1.0, contrast=1.25, teal=0.04, warm=0.05), TH); bg = bg.convert("RGBA"); paste_faded(bg, f, TW - f.width + 40, 0, left=180)
    c = vign(vhs(bg.convert("RGB"), red=0.32), 0.55).convert("RGBA")
    red_text(c, "HANGED", 54, 70, 176)
    d = ImageDraw.Draw(c); d.ellipse((62, 336, 112, 386), fill=(225, 30, 30))
    red_text(c, "ON LIBYAN TV", 130, 300, 104)
    mono = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 64)
    d.text((60, 600), "JUN 5 1984", font=mono, fill=(245, 245, 235), stroke_width=4, stroke_fill=(0, 0, 0))
    return c
def E():   # one red word on a deep red field: HANGED.  (B2, U.S. Navy 2009)
    c = Image.new("RGB", (TW, TH)); a = np.zeros((TH, TW, 3), np.float32)
    xx = np.linspace(0, 1, TW)[None, :, None]; a[:] = np.array([70, 6, 8]) * (0.55 + 0.45 * xx) + np.array([20, 0, 0])
    c = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    f = crop("B2_", (0.12, 0.06, 0.92, 0.62)); f = fit_h(grade(f, sat=1.15, contrast=1.2, teal=0.0, warm=0.12), TH)
    paste_faded(c, f.convert("RGB"), -40, 0, right=320)
    c = grain(c, 8)
    red_text(c, "HANGED.", 540, 170, 186, fill=(230, 28, 28), edge=((250, 245, 235), 6))
    block(c, "8 MEN  ·  8 DAYS", 580, 450, 54, fill=WHITE, bg=(0, 0, 0, 230))
    block(c, DATE, 580, 600, 58, fill=WHITE, bg=RED + (255,))
    return c
def F():   # Libya's plain green flag field + face (B7) + one huge spaced word: BENGHAZI
    a = np.zeros((TH, TW, 3), np.float32); yy = np.linspace(0, 1, TH)[:, None, None]
    a[:] = np.array([0, 122, 51]) * (1.05 - 0.35 * yy); c = grain(Image.fromarray(a.astype(np.uint8)), 7)
    f = crop("B7_", (0.0, 0.0, 0.62, 1.0)); f = fit_h(grade(f, sat=1.1, contrast=1.2, teal=0.0, warm=0.08), 640)
    paste_faded(c, f.convert("RGB"), TW - f.width - 10, TH - f.height, left=200, top=40)
    red_text(c, "BENGHAZI", 40, 18, 150, fill=(10, 20, 12), glow=False, spacing=14)
    block(c, "HANGED IN", 44, 300, 96, fill=WHITE, bg=(0, 0, 0, 235))
    block(c, "PUBLIC.", 44, 430, 96, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, DATE, 44, 610, 58, fill=WHITE, bg=RED + (255,))
    return c
def G():   # eyes only (B5) + our own TOP SECRET stamp: THE CIA KNEW.
    f = crop("B5_", (0.04, 0.22, 0.96, 0.58)); c = cover(grade(f, sat=1.05, contrast=1.3, teal=0.05, warm=0.06), TW, TH, cx=0.5, cy=0.5, z=1.0)
    c = vign(ImageEnhance.Brightness(c).enhance(0.8), 0.6).convert("RGBA")
    st = Image.new("RGBA", (760, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    d.rectangle((6, 6, 754, 184), outline=(214, 30, 30, 255), width=12)
    d.text((380, 95), "TOP SECRET", font=ImageFont.truetype(IMPACT, 150), fill=(214, 30, 30, 255), anchor="mm")
    st = st.resize((570, 143), Image.LANCZOS).rotate(8, expand=True, resample=Image.BICUBIC); c.alpha_composite(st, (40, 26))
    block(c, "THE CIA", 44, 400, 120)
    block(c, "KNEW.", 44, 540, 120, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, DATE, 880, 640, 52, fill=WHITE, bg=RED + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name in ("A_8_MEN", "B_AGENT_OF_AMERICA", "C_SHOW_TRIAL"):
        tiles.append((name, Image.open(OUT + name + ".png").convert("RGB")))
    for name, fn in (("D_ON_LIBYAN_TV", D), ("E_HANGED_RED", E), ("F_BENGHAZI_GREEN", F), ("G_THE_CIA_KNEW", G)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append((name, im))
    w, h = TW // 2, TH // 2; S = Image.new("RGB", (w * 4 + 50, (h + 40) * 2 + 10), (25, 25, 25)); d = ImageDraw.Draw(S)
    lab = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    for i, (name, im) in enumerate(tiles):
        x, y = 10 + (i % 4) * (w + 10), 10 + (i // 4) * (h + 40); S.paste(im.resize((w, h), Image.LANCZOS), (x, y + 34)); d.text((x, y), name.replace("_", " "), font=lab, fill=(255, 220, 0))
    S.save(OUT + "_sheet_v2.png"); print(OUT + "_sheet_v2.png")
