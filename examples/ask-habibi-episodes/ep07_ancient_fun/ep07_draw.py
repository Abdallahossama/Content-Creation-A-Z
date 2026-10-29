"""Ep 7 drawings (all drawn by us, no downloads): cave art, flutes, dice, the Royal Game of Ur, senet, tablet, toys, icons."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
RUBIK = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; HAND = "C:/Windows/Fonts/Inkfree.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"
OCHRE = (176, 62, 34); INK = (24, 18, 14)

def _noise(w, h, base, amp=14, seed=1):
    a = np.array(base, np.float32)[None, None, :] + np.random.default_rng(seed).normal(0, amp, (h, w, 1))
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)); return im
def rock(w, h, base=(196, 168, 128), seed=1, r=36):
    im = _noise(w, h, base, 16, seed).convert("RGBA"); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    im.putalpha(m); d = ImageDraw.Draw(im)
    rr = np.random.default_rng(seed + 7)
    for _ in range(14):
        x, y = rr.uniform(0, w), rr.uniform(0, h); d.line((x, y, x + rr.uniform(-80, 80), y + rr.uniform(-40, 40)), fill=(150, 124, 92, 120), width=2)
    return im

def hand_stencil(size=520, claw=True, seed=3):
    im = rock(size, size, seed=seed); spray = Image.new("L", (size, size), 0); d = ImageDraw.Draw(spray); cx, cy = size / 2, size * 0.6
    hand = Image.new("L", (size, size), 0); h = ImageDraw.Draw(hand)
    h.rounded_rectangle((cx - 78, cy - 70, cx + 78, cy + 110), 50, fill=255)                       # palm + wrist
    h.rectangle((cx - 60, cy + 90, cx + 60, size), fill=255)
    for ang, ln, x0 in ((-14, 150, -54), (-4, 175, -18), (5, 168, 18), (15, 135, 52)):          # four fingers
        a = math.radians(ang - 90); bx, by = cx + x0, cy - 60; ex, ey = bx + math.cos(a) * ln, by + math.sin(a) * ln
        w = 15 if not claw else 12
        h.line((bx, by, ex, ey), fill=255, width=w * 2); h.ellipse((ex - w, ey - w, ex + w, ey + w), fill=255)
        if claw: h.polygon([(ex - w, ey), (ex + w, ey), (ex + math.cos(a + 0.5) * 34, ey + math.sin(a + 0.5) * 34)], fill=255)
    a = math.radians(-145); bx, by = cx - 70, cy + 20; ex, ey = bx + math.cos(a) * 120, by + math.sin(a) * 120     # thumb
    h.line((bx, by, ex, ey), fill=255, width=34); h.ellipse((ex - 17, ey - 17, ex + 17, ey + 17), fill=255)
    rr = np.random.default_rng(seed)
    for _ in range(9000):
        x, y = rr.normal(cx, size * 0.24), rr.normal(cy - 30, size * 0.24); r = rr.uniform(1, 3.5); d.ellipse((x - r, y - r, x + r, y + r), fill=int(rr.uniform(120, 255)))
    spray = spray.filter(ImageFilter.GaussianBlur(2.2))
    sp = np.asarray(spray, np.float32) * (1 - np.asarray(hand.filter(ImageFilter.GaussianBlur(2)), np.float32) / 255)
    col = Image.new("RGBA", (size, size), OCHRE + (0,)); col.putalpha(Image.fromarray((sp * 0.85).astype(np.uint8))); im.alpha_composite(col)
    return im

def pig_scene(w=640, h=420):
    im = rock(w, h, (200, 172, 130), seed=5); lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = OCHRE + (230,)
    d.ellipse((220, 150, 470, 290), fill=c); d.polygon([(460, 190), (540, 205), (545, 240), (465, 260)], fill=c)            # body + snout
    for x in (250, 290, 400, 440): d.line((x, 270, x - 6, 340), fill=c, width=14)
    d.polygon([(250, 160), (230, 120), (275, 150)], fill=c); d.line((222, 200, 190, 180), fill=c, width=6)                # ear + tail
    for (x, y, s) in ((110, 200, 1), (590, 150, 1), (560, 330, -1)):                                                         # three small figures
        d.ellipse((x - 12, y - 70, x + 12, y - 46), fill=c); d.line((x, y - 46, x, y), fill=c, width=8)
        d.line((x, y - 34, x + 34 * s, y - 50), fill=c, width=6); d.line((x, y - 34, x - 26 * s, y - 20), fill=c, width=6)
        d.line((x, y, x - 14, y + 40), fill=c, width=7); d.line((x, y, x + 14, y + 40), fill=c, width=7)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.5))); return im

def flutings(w=640, h=360, t=0.0):
    im = rock(w, h, (214, 196, 160), seed=9); d = ImageDraw.Draw(im)
    for k in range(9):
        y0 = 40 + k * 34; pts = [(x, y0 + 18 * math.sin(x / 55 + k * 0.7)) for x in range(20, w - 20, 8)]
        for f in range(3): d.line([(x, y + f * 9) for x, y in pts], fill=(150, 120, 86, 200), width=5)
    return im

def flute(length=640, holes=5, col=(236, 226, 200), ivory=False):
    im = Image.new("RGBA", (length + 20, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = (238, 232, 214) if ivory else col
    d.rounded_rectangle((10, 30, length, 80), 25, fill=c + (255,), outline=(120, 100, 70, 255), width=4)
    d.ellipse((length - 40, 22, length + 8, 88), fill=c + (255,), outline=(120, 100, 70, 255), width=4)
    for k in range(holes): x = 140 + k * (length - 260) / max(1, holes - 1); d.ellipse((x - 11, 44, x + 11, 66), fill=(70, 52, 36, 255))
    for k in range(6): d.line((60 + k * 90, 36, 80 + k * 90, 74), fill=(180, 160, 128, 160), width=2)
    return im

def dice_sticks():
    im = Image.new("RGBA", (520, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(3):
        x = 40 + k * 160; side = k % 2
        d.rounded_rectangle((x, 40, x + 110, 220), 50, fill=(232, 214, 176, 255) if side else (150, 110, 70, 255), outline=(90, 66, 40, 255), width=5)
        if side:
            for j in range(4): d.line((x + 25, 80 + j * 30, x + 85, 80 + j * 30), fill=(90, 60, 36, 255), width=6)
    return im

UR_SQ = [(r, c) for r in range(3) for c in range(8) if not (r != 1 and c in (4, 5))]
UR_ROSE = {(0, 0), (2, 0), (1, 3), (0, 6), (2, 6)}
def ur_board(sq=78, lit=()):
    W_, H_ = sq * 8 + 40, sq * 3 + 40; im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for r, c in UR_SQ:
        x, y = 20 + c * sq, 20 + r * sq
        d.rectangle((x, y, x + sq - 4, y + sq - 4), fill=(28, 52, 120, 255), outline=(10, 16, 40, 255), width=3)
        d.rectangle((x + 7, y + 7, x + sq - 11, y + sq - 11), fill=(236, 226, 200, 255))
        if (r, c) in UR_ROSE:
            cx, cy = x + sq / 2 - 2, y + sq / 2 - 2
            for k in range(8):
                a = k * math.pi / 4; d.ellipse((cx + math.cos(a) * 16 - 9, cy + math.sin(a) * 16 - 9, cx + math.cos(a) * 16 + 9, cy + math.sin(a) * 16 + 9), fill=(196, 40, 40, 255))
            d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=(28, 52, 120, 255))
            if (r, c) in lit: d.rectangle((x, y, x + sq - 4, y + sq - 4), outline=(255, 206, 60, 255), width=7)
        else:
            for dx, dy in ((0.3, 0.3), (0.7, 0.3), (0.5, 0.5), (0.3, 0.7), (0.7, 0.7)):
                px, py = x + dx * (sq - 4), y + dy * (sq - 4); d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(28, 52, 120, 255))
    return im
def ur_piece(white=True, r=26):
    im = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(246, 240, 226, 255) if white else (30, 26, 24, 255), outline=(200, 160, 60, 255), width=4)
    for k in range(5):
        a = k * 2 * math.pi / 5; d.ellipse((r + 4 + math.cos(a) * 12 - 3, r + 4 + math.sin(a) * 12 - 3, r + 4 + math.cos(a) * 12 + 3, r + 4 + math.sin(a) * 12 + 3), fill=(200, 160, 60, 255))
    return im
def ur_cell_xy(r, c, sq=78): return 20 + c * sq + sq / 2 - 2, 20 + r * sq + sq / 2 - 2

def senet_board(sq=58):
    W_, H_ = sq * 10 + 60, sq * 3 + 60; im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W_ - 1, H_ - 1), 14, fill=(150, 98, 52, 255), outline=(70, 44, 22, 255), width=5)
    for r in range(3):
        for c in range(10):
            x, y = 30 + c * sq, 30 + r * sq; d.rectangle((x, y, x + sq - 4, y + sq - 4), fill=(222, 190, 132, 255), outline=(110, 72, 36, 255), width=2)
    for c, ch in ((5, "ankh"), (6, "x"), (7, "iii"), (8, "ii"), (9, "o")):
        x, y = 30 + c * sq + sq / 2 - 2, 30 + 2 * sq + sq / 2 - 2; d.text((x, y), {"ankh": "☥", "x": "X", "iii": "III", "ii": "II", "o": "O"}[ch], font=ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", 30), fill=(90, 50, 20, 255), anchor="mm")
    for k in range(5):
        x, y = 30 + k * 2 * sq + sq / 2 - 2, 30 + sq / 2 - 2; d.polygon([(x, y - 18), (x - 14, y + 16), (x + 14, y + 16)], fill=(30, 26, 24, 255))
        x2 = 30 + (k * 2 + 1) * sq + sq / 2 - 2; d.ellipse((x2 - 15, y - 15, x2 + 15, y + 15), fill=(246, 240, 226, 255), outline=(60, 40, 20, 255), width=3)
    return im

def clay_tablet(w=520, h=380, seed=4):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 60, fill=255)
    base = _noise(w, h, (198, 160, 112), 10, seed).convert("RGBA"); base.putalpha(m); im.alpha_composite(base); d = ImageDraw.Draw(im); rr = np.random.default_rng(seed)
    for row in range(8):
        y = 40 + row * 40; x = 36
        while x < w - 50:
            s = rr.uniform(8, 14); d.polygon([(x, y), (x + s, y + s * 0.4), (x, y + s * 0.8)], fill=(110, 80, 50, 255)); d.line((x + s * 0.4, y + s * 0.4, x + s * 1.8, y + s * 0.4), fill=(110, 80, 50, 255), width=3)
            x += s * 2.6 + rr.uniform(0, 10)
    return im

def plaster_wall(text, w=900, h=300, size=40):
    im = rock(w, h, (232, 220, 196), seed=11, r=10); d = ImageDraw.Draw(im); f = ImageFont.truetype(HAND, size)
    lines = text.split("\n")
    for k, l in enumerate(lines): d.text((w / 2, h / 2 + (k - (len(lines) - 1) / 2) * size * 1.15), l, font=f, fill=(120, 36, 30, 255), anchor="mm", stroke_width=1, stroke_fill=(120, 36, 30, 255))
    return im

def rattle(t=0.0):
    im = Image.new("RGBA", (380, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = (176, 120, 72, 255); o = (90, 56, 30, 255)
    for ex in (100, 280): d.ellipse((ex - 38, 40, ex + 38, 116), fill=c, outline=o, width=5)
    d.ellipse((50, 70, 330, 330), fill=c, outline=o, width=6); d.ellipse((140, 210, 240, 300), fill=(196, 146, 96, 255), outline=o, width=4)
    d.ellipse((172, 222, 208, 248), fill=o); d.ellipse((120, 150, 150, 180), fill=o); d.ellipse((230, 150, 260, 180), fill=o)
    rr = np.random.default_rng(int(t * 30))
    for _ in range(14): x, y = 190 + rr.uniform(-130, 130), 190 + rr.uniform(-100, 100); d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(120, 80, 46, 255))
    return im

def owl_plaque():
    im = Image.new("RGBA", (300, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(40, 20), (260, 20), (285, 400), (15, 400)], fill=(96, 104, 112, 255), outline=(50, 54, 60, 255))
    for ex in (100, 200):
        for r in (44, 30, 16): d.ellipse((ex - r, 110 - r, ex + r, 110 + r), outline=(220, 224, 228, 255), width=4)
    d.polygon([(150, 130), (138, 170), (162, 170)], fill=(220, 224, 228, 255))
    for k in range(6): d.line((40, 210 + k * 30, 260, 225 + k * 30), fill=(200, 205, 210, 255), width=4)
    return im

def doll():
    im = Image.new("RGBA", (220, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = (240, 228, 200, 255); o = (150, 120, 80, 255)
    d.ellipse((70, 10, 150, 100), fill=c, outline=o, width=4); d.rounded_rectangle((70, 100, 150, 260), 30, fill=c, outline=o, width=4)
    for x0 in (30, 160): d.rounded_rectangle((x0, 110, x0 + 30, 190), 14, fill=c, outline=o, width=3); d.rounded_rectangle((x0, 196, x0 + 30, 270), 14, fill=c, outline=o, width=3)
    for x0 in (75, 115): d.rounded_rectangle((x0, 262, x0 + 30, 360), 14, fill=c, outline=o, width=3); d.rounded_rectangle((x0, 366, x0 + 30, 460), 14, fill=c, outline=o, width=3)
    for x, y in ((45, 193), (175, 193), (90, 363), (130, 363)): d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=o)
    return im

def ballcourt():
    im = Image.new("RGBA", (620, 340), (0, 0, 0, 0)); d = ImageDraw.Draw(im); g = (196, 170, 120, 255); o = (110, 84, 50, 255)
    d.polygon([(40, 40), (580, 40), (580, 110), (470, 110), (470, 230), (580, 230), (580, 300), (40, 300), (40, 230), (150, 230), (150, 110), (40, 110)], fill=g, outline=o)
    d.rectangle((150, 130, 470, 210), fill=(222, 204, 160, 255), outline=o, width=3); d.ellipse((295, 155, 325, 185), fill=(30, 26, 24, 255))
    return im

def crossed(kind, size=200):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = (30, 30, 30, 255); s = size
    if kind == "phone": d.rounded_rectangle((s * 0.3, s * 0.1, s * 0.7, s * 0.9), 18, fill=(60, 60, 70, 255), outline=o, width=5); d.rectangle((s * 0.35, s * 0.18, s * 0.65, s * 0.78), fill=(120, 190, 255, 255))
    if kind == "book": d.polygon([(s * 0.1, s * 0.25), (s * 0.5, s * 0.32), (s * 0.9, s * 0.25), (s * 0.9, s * 0.8), (s * 0.5, s * 0.87), (s * 0.1, s * 0.8)], fill=(200, 60, 50, 255), outline=o); d.line((s * 0.5, s * 0.32, s * 0.5, s * 0.87), fill=o, width=4)
    if kind == "writing": im.alpha_composite(clay_tablet(int(s * 0.8), int(s * 0.6)).resize((int(s * 0.8), int(s * 0.6))), (int(s * 0.1), int(s * 0.2)))
    d.line((s * 0.1, s * 0.1, s * 0.9, s * 0.9), fill=(220, 40, 40, 255), width=16); d.line((s * 0.9, s * 0.1, s * 0.1, s * 0.9), fill=(220, 40, 40, 255), width=16)
    return im

def stamp(text, size=80, col=(210, 40, 40)):
    f = ImageFont.truetype(IMPACT, size); w = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=f)) + 60
    im = Image.new("RGBA", (w, size + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rectangle((6, 6, w - 6, size + 44), outline=col + (255,), width=8)
    d.text((w / 2, (size + 50) / 2), text, font=f, fill=col + (255,), anchor="mm"); return im.rotate(-10, Image.BICUBIC, expand=True)

def shock_button(pressed=False):
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((30, 150, 270, 260), fill=(60, 60, 60, 255)); dy = 20 if pressed else 0
    d.ellipse((50, 100 + dy, 250, 220 + dy), fill=(220, 30, 30, 255), outline=(120, 10, 10, 255), width=6)
    if pressed: d.polygon([(150, 0), (110, 70), (145, 70), (120, 130), (190, 50), (155, 50), (175, 0)], fill=(255, 220, 40, 255), outline=(120, 90, 0, 255))
    return im
