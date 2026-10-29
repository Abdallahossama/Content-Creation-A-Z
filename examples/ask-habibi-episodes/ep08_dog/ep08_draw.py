"""Ep 8 drawings (ours): cone curves, eye chart, field of view, flicker TV, brain icon, nose bars, pools, scent house, sound waves."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
RUBIK = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"; HAND = "C:/Windows/Fonts/Inkfree.ttf"
def F(s, p=RUBIK): return ImageFont.truetype(p, int(s))
INK = (24, 20, 16, 255); PANEL = (24, 18, 12, 225)

def panel(w, h, r=30, fill=PANEL):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill); return im

def cones(dog=False, w=900, h=420, u=1.0):
    """sensitivity curves over a rainbow strip: human 3 cones (blue, green, red) vs dog 2 (blue-violet ~429 nm, yellow-green ~555 nm)"""
    im = panel(w, h); d = ImageDraw.Draw(im); x0, x1, yb = 60, w - 40, h - 90
    for x in range(x0, x1):
        nm = 400 + (x - x0) / (x1 - x0) * 300; d.line((x, yb + 14, x, yb + 44), fill=_wl(nm) + (255,))
    d.text((x0, yb + 50), "400 nm", font=F(22), fill=(200, 190, 175)); d.text((x1, yb + 50), "700 nm", font=F(22), fill=(200, 190, 175), anchor="ra")
    peaks = [(429, (120, 110, 255)), (555, (200, 220, 60))] if dog else [(420, (90, 110, 255)), (534, (60, 200, 90)), (564, (240, 70, 60))]
    for pk, col in peaks:
        pts = []
        for x in range(x0, int(x0 + (x1 - x0) * u)):
            nm = 400 + (x - x0) / (x1 - x0) * 300; pts.append((x, yb - (h - 170) * math.exp(-((nm - pk) / 42) ** 2)))
        if len(pts) > 1: d.line(pts, fill=col + (255,), width=7)
    d.text((w / 2, 34), "YOUR DOG: 2 cone types" if dog else "YOU: 3 cone types", font=F(40), fill=(255, 255, 255), anchor="mm")
    return im
def _wl(nm):
    if nm < 440: r, g, b = -(nm - 440) / 40, 0, 1
    elif nm < 490: r, g, b = 0, (nm - 440) / 50, 1
    elif nm < 510: r, g, b = 0, 1, -(nm - 510) / 20
    elif nm < 580: r, g, b = (nm - 510) / 70, 1, 0
    elif nm < 645: r, g, b = 1, -(nm - 645) / 65, 0
    else: r, g, b = 1, 0, 0
    return int(255 * r), int(255 * g), int(255 * b)

def eye_chart(blur=0.0, w=420, h=520, label="YOU · 20/20"):
    im = Image.new("RGBA", (w, h), (250, 248, 240, 255)); d = ImageDraw.Draw(im); rows = ["E", "F P", "T O Z", "L P E D", "P E C F D", "E D F C Z P"]
    for k, r in enumerate(rows): d.text((w / 2, 50 + k * 64 + k * k * 1.5), r, font=F(80 - k * 11, IMPACT), fill=(20, 20, 20), anchor="mm")
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    d = ImageDraw.Draw(im); d.rectangle((0, h - 70, w, h), fill=(24, 18, 12)); d.text((w / 2, h - 35), label, font=F(34), fill=(255, 206, 60), anchor="mm")
    d.rectangle((0, 0, w - 1, h - 1), outline=(60, 50, 40), width=4); return im

def fov(dog=True, r=300, u=1.0):
    """top-down field of view: a wedge (240 deg dog / 180 deg human) and the overlap where both eyes see (30-60 vs ~140)"""
    w = 2 * r + 80; im = Image.new("RGBA", (w, r + 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx, cy = w / 2, r + 60
    tot = (240 if dog else 180) * u; both = (50 if dog else 140) * u
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90 - tot / 2, -90 + tot / 2, fill=(120, 190, 255, 150))
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90 - both / 2, -90 + both / 2, fill=(255, 206, 60, 200))
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=(150, 100, 60, 255), outline=INK, width=4)
    d.text((cx, cy + 56), f"{'DOG' if dog else 'YOU'}: ~{240 if dog else 180}°", font=F(38), fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))
    return im

def tv(t, hz_seen=True, w=380, h=300):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w - 10, h - 50), 24, fill=(60, 56, 52, 255), outline=INK, width=6)
    on = (int(t * 30) % 2 == 0) or not hz_seen; d.rounded_rectangle((34, 34, w - 34, h - 74), 14, fill=(150, 200, 255, 255) if on else (60, 90, 130, 255))
    d.line((w / 2 - 50, h - 50, w / 2 - 80, h - 10), fill=INK, width=8); d.line((w / 2 + 50, h - 50, w / 2 + 80, h - 10), fill=INK, width=8); return im

def brain(glow=0.0, w=360, h=300, q=False):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if glow > 0:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((w * 0.35, h * 0.4, w * 0.65, h * 0.7), fill=(255, 200, 60, int(220 * glow))); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(26)))
    d.ellipse((20, 30, w - 20, h - 40), outline=(196, 54, 96, 255), width=10)
    for k in range(5): d.arc((40 + k * 50, 60, 140 + k * 50, 200), 200, 340, fill=(196, 54, 96, 255), width=8)
    d.line((w / 2, 40, w / 2, h - 50), fill=(196, 54, 96, 255), width=6)
    if glow > 0: d.ellipse((w * 0.44, h * 0.48, w * 0.56, h * 0.62), fill=(255, 210, 70, 255))
    if q: d.text((w - 50, 70), "?", font=F(120, IMPACT), fill=(255, 206, 60, 255), anchor="mm", stroke_width=6, stroke_fill=(10, 10, 10))
    return im

def pools(n=20, lit=0.0, w=900, h=360):
    im = panel(w, h); d = ImageDraw.Draw(im)
    for k in range(n):
        x, y = 50 + (k % 10) * 82, 60 + (k // 10) * 120; d.rectangle((x, y, x + 70, y + 90), fill=(70, 150, 220, 255), outline=(255, 255, 255, 255), width=3)
        for j in range(3): d.line((x + 6, y + 20 + j * 24, x + 64, y + 20 + j * 24), fill=(200, 230, 255, 160), width=2)
    if lit > 0:
        x, y = 50 + 9 * 82 + 35, 60 + 120 + 45; r = 10 + 6 * lit; d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 206, 60, 255), outline=INK, width=3)
    d.text((w / 2, h - 36), "1 drop  in  20 Olympic pools  ≈  1 part per trillion", font=F(32), fill=(255, 255, 255), anchor="mm"); return im

def scent_house(fade, w=620, h=420):
    """a house with scent waves that get weaker over time (fade 0 = fresh, 1 = faint)"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(w / 2, 40), (w - 90, 170), (90, 170)], fill=(200, 80, 60, 255), outline=INK); d.rectangle((120, 170, w - 120, h - 30), fill=(240, 226, 196, 255), outline=INK, width=5)
    d.rectangle((w / 2 - 40, h - 150, w / 2 + 40, h - 30), fill=(120, 80, 50, 255))
    a = int(230 * (1 - fade))
    for k in range(4):
        y = 210 + k * 34; pts = [(150 + x, y + 10 * math.sin(x / 26 + k)) for x in range(0, w - 300, 6)]; d.line(pts, fill=(120, 170, 80, a), width=7)
    return im

def waves(t, happy=True, w=520, h=200):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); amp = 70 if happy else 14; col = (255, 206, 60, 255) if happy else (170, 170, 170, 255)
    pts = [(x, h / 2 + amp * math.sin(x / (14 if happy else 30) + t * 8) * math.sin(math.pi * x / w)) for x in range(0, w, 3)]; d.line(pts, fill=col, width=7); return im

def bars(rows, w=1100, u=1.0, title=None):
    """rows [(label, value, max, colour, text)]"""
    h = 90 + 110 * len(rows) + (50 if title else 0); im = panel(w, h); d = ImageDraw.Draw(im); y0 = 40 + (50 if title else 0)
    if title: d.text((w / 2, 40), title, font=F(36), fill=(235, 225, 210), anchor="mm")
    for k, (lab, v, mx, col, txt) in enumerate(rows):
        y = y0 + k * 110; d.text((40, y), lab, font=F(34), fill=(255, 255, 255))
        d.rounded_rectangle((40, y + 44, w - 220, y + 90), 12, fill=(70, 60, 52, 255))
        ww = (w - 260) * min(1, v / mx) * u; d.rounded_rectangle((40, y + 44, 40 + max(14, ww), y + 90), 12, fill=col + (255,))
        d.text((w - 30, y + 67), txt, font=F(46, IMPACT), fill=(255, 206, 60), anchor="rm", stroke_width=3, stroke_fill=(10, 10, 10))
    return im

def crossed_word(word, new=None, size=110):
    f = F(size, IMPACT); w = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(word, font=f)) + 60
    im = Image.new("RGBA", (w, size + 200 if new else size + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((w / 2, size / 2 + 20), word, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=6, stroke_fill=(10, 10, 10))
    d.line((10, size / 2 + 30, w - 10, size / 2 + 10), fill=(220, 40, 40), width=14)
    if new: d.text((w / 2, size + 120), new, font=F(size * 0.8, HAND), fill=(255, 206, 60), anchor="mm", stroke_width=3, stroke_fill=(10, 10, 10))
    return im
