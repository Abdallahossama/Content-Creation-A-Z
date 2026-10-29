"""Batata v2: a REAL potato (Pexels 33948200, Nikolaos Kofidis) with a face drawn on in black marker.
Writes D:/why habibi/_style_kit/mascot/batata/Batata_<expression>.png (transparent, full res; marker.sticker() adds the
white sticker edge when used on screen).   python batata2.py   |   python batata2.py sheet"""
import sys, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from marker import strokes, circle_path, _noise, sticker, place, hand, night, fill, W, H, NAVY, YEL, WHITE

SRC = "D:/why habibi/_style_kit/mascot/source/potato_cut.png"
OUT = "D:/why habibi/_style_kit/mascot/batata/"; os.makedirs(OUT, exist_ok=True)
INK = (28, 24, 22)
POT = Image.open(SRC).convert("RGBA")                       # 1068 x 1508
LX, RX, EY, MY = 375, 665, 610, 900                          # eye x (left/right), eye y, mouth y
SW = 24                                                      # marker width at full res

def line(p0, p1, seed=0, wob=4):
    p0, p1 = np.array(p0, float), np.array(p1, float); n = 40
    pts = np.linspace(p0, p1, n); d = p1 - p0; nr = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-6)
    return pts + nr * _noise(n, seed, wob)[:, None]

def arc(cx, cy, rx, ry, a0, a1, seed=0, n=50):
    a = np.radians(np.linspace(a0, a1, n)); k = 1 + _noise(n, seed, 0.04)
    return np.stack([cx + rx * k * np.cos(a), cy + ry * k * np.sin(a)], 1)

def dot(cx, cy, r, seed=0, ry=None):                         # a filled marker dot = tight spiral
    t = np.linspace(0, 5 * np.pi, 160); k = (1 - t / (5 * np.pi)) * (1 + _noise(160, seed, 0.06))
    return np.stack([cx + r * k * np.cos(t), cy + (ry or r) * k * np.sin(t)], 1)

def eye_ring(cx, cy, r, seed): return circle_path(cx, cy, r, r * 1.08, seed=seed, turns=1.06, tilt=0, n=160)[0]

def face(expr):
    """returns list of (paths, width) for one expression"""
    P = []
    E = lambda x, s: eye_ring(x, EY, 92, s)
    if expr == "shocked":
        P += [([E(LX, 1), E(RX, 2)], SW), ([dot(LX, EY + 6, 26, 3), dot(RX, EY + 6, 26, 4)], 14),
              ([line((LX - 80, EY - 160), (LX + 60, EY - 185), 5), line((RX - 60, EY - 185), (RX + 80, EY - 160), 6)], SW),
              ([circle_path(520, MY + 30, 52, 70, seed=7, turns=1.05, tilt=0)[0]], SW)]
    elif expr == "deadpan":
        P += [([E(LX, 1), E(RX, 2)], SW),
              ([line((LX - 95, EY - 12), (LX + 95, EY - 8), 8, 3), line((RX - 95, EY - 8), (RX + 95, EY - 12), 9, 3)], SW),
              ([dot(LX, EY + 40, 24, 3), dot(RX, EY + 40, 24, 4)], 14),
              ([line((430, MY), (620, MY + 4), 10, 3)], SW)]
    elif expr == "sleepy":
        P += [([arc(LX, EY - 10, 80, 50, 15, 165, 1), arc(RX, EY - 10, 80, 50, 15, 165, 2)], SW),
              ([circle_path(540, MY + 10, 34, 40, seed=3, turns=1.05, tilt=0)[0]], SW - 4)]
    elif expr == "sideeye":
        P += [([E(LX, 1), E(RX, 2)], SW), ([dot(LX + 50, EY + 10, 28, 3), dot(RX + 50, EY + 10, 28, 4)], 14),
              ([line((LX - 90, EY - 130), (LX + 90, EY - 105), 5), line((RX - 90, EY - 110), (RX + 90, EY - 125), 6)], SW),
              ([line((440, MY + 8), (600, MY - 6), 10, 3)], SW)]
    elif expr == "smug":
        P += [([arc(LX, EY + 5, 85, 60, 190, 350, 1), arc(RX, EY + 5, 85, 60, 190, 350, 2)], SW),
              ([line((LX - 70, EY + 8), (LX + 80, EY + 8), 3, 2), line((RX - 80, EY + 8), (RX + 70, EY + 8), 4, 2)], SW - 4),
              ([dot(LX + 20, EY + 30, 20, 5), dot(RX + 20, EY + 30, 20, 6)], 12),
              ([line((LX - 80, EY - 120), (LX + 70, EY - 115), 7), arc(RX, EY - 95, 90, 45, 200, 340, 8)], SW),
              ([arc(570, MY - 80, 150, 90, 25, 125, 9)], SW)]
    elif expr == "sad":
        P += [([E(LX, 1), E(RX, 2)], SW), ([dot(LX - 10, EY + 45, 26, 3), dot(RX - 10, EY + 45, 26, 4)], 14),
              ([line((LX - 80, EY - 120), (LX + 70, EY - 165), 5), line((RX - 70, EY - 165), (RX + 80, EY - 120), 6)], SW),
              ([arc(520, MY + 70, 110, 60, 205, 335, 7)], SW)]
    elif expr == "panic":
        P += [([E(LX, 1), E(RX, 2)], SW), ([dot(LX, EY, 14, 3), dot(RX, EY, 14, 4)], 12),
              ([line((LX - 70, EY - 150), (LX + 70, EY - 200), 5), line((RX - 70, EY - 200), (RX + 70, EY - 150), 6)], SW),
              ([circle_path(520, MY + 60, 80, 105, seed=7, turns=1.05, tilt=0)[0]], SW), ([dot(520, MY + 60, 70, 9, ry=95)], 46)]
    elif expr == "fine":                                      # "this is fine" smile
        P += [([arc(LX, EY + 20, 75, 55, 200, 340, 1), arc(RX, EY + 20, 75, 55, 200, 340, 2)], SW),
              ([arc(520, MY - 70, 170, 110, 20, 160, 7), line((350, MY - 40), (370, MY - 5), 8, 2), line((690, MY - 40), (670, MY - 5), 9, 2)], SW)]
    elif expr == "cool":                                      # the brand face: marker sunglasses + smirk (= old Batata's look)
        L1, L2 = lens(LX - 5, EY + 15, 1), lens(RX + 5, EY + 15, 2)
        P += [([L1, L2], "fill"), ([L1, L2], SW),
              ([line((LX + 100, EY - 5), (RX - 100, EY - 5), 3, 3)], SW),
              ([line((LX - 112, EY - 20), (LX - 170, EY - 40), 4, 2), line((RX + 112, EY - 20), (RX + 170, EY - 40), 5, 2)], SW - 4),
              ([line((LX - 70, EY - 10), (LX - 30, EY - 32), 6, 1), line((RX - 70, EY - 10), (RX - 30, EY - 32), 7, 1)], ("erase", 12)),
              ([arc(545, MY - 85, 145, 85, 22, 140, 9)], SW)]
    return P

def lens(cx, cy, seed, a=108, b=72, n=3.2):
    """a wayfarer-ish lens outline (superellipse, flatter top) with a hand wobble"""
    t = np.linspace(0, 2 * np.pi, 120); k = 1 + _noise(120, seed, 0.03)
    x = a * np.sign(np.cos(t)) * np.abs(np.cos(t)) ** (2 / n); y = b * np.sign(np.sin(t)) * np.abs(np.sin(t)) ** (2 / n)
    y = np.where(y < 0, y * 0.8, y)
    return np.stack([cx + x * k, cy + y * k], 1)

def draw(expr):
    lay = Image.new("RGBA", POT.size, (0, 0, 0, 0))
    C = np.array([520.0, 700.0])                             # features drawn 20% bigger around the face centre
    for k, (paths, w) in enumerate(face(expr)):
        paths = [C + (p - C) * 1.2 for p in paths]
        if w == "fill":                                       # solid marker fill (sunglasses lenses)
            for p in paths: ImageDraw.Draw(lay).polygon([tuple(q) for q in p], fill=INK + (255,))
        elif isinstance(w, tuple):                            # ("erase", width): skin left unpainted = a glint
            for p in paths: ImageDraw.Draw(lay).line([tuple(q) for q in p], fill=(0, 0, 0, 0), width=w[1], joint="curve")
        else:
            strokes(lay, paths, INK, w * 1.22, seed=k * 7 + 1)
    a = np.asarray(lay.getchannel("A"), np.float32) / 255
    pot = np.asarray(POT, np.float32)
    lum = pot[..., :3].mean(-1); tex = lum - np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32)
    a = np.clip(a * (0.93 + tex / 60.0), 0, 1) * (pot[..., 3] / 255)        # ink skips a little on the skin's bumps
    ink = np.array(INK, np.float32) / 255
    pot[..., :3] *= (1 - a[..., None]) + a[..., None] * ink                    # multiply: the skin shows through
    im = Image.fromarray(np.clip(pot, 0, 255).astype(np.uint8), "RGBA"); im.save(OUT + f"Batata_{expr}.png"); return im

EXPR = ["cool", "shocked", "deadpan", "sleepy", "sideeye", "smug", "sad", "panic", "fine"]

def sheet():
    c = Image.new("RGBA", (W, H), (14, 17, 46, 255))
    for i, e in enumerate(EXPR):
        x, y = 200 + (i % 5) * 380, 280 + (i // 5) * 520
        place(c, sticker(OUT + f"Batata_{e}.png", 330, rot=[0, 6, -5, 4, -7, 5, -4, 8, -6][i]), x, y)
        place(c, hand(e + (" (brand)" if e == "cool" else ""), 44, YEL, rot=-3), x, y + 210)
    c.convert("RGB").save("D:/why habibi/_style_kit/mascot/batata_sheet.png"); print("sheet")

if __name__ == "__main__":
    for e in EXPR: draw(e); print(e)
    sheet()
