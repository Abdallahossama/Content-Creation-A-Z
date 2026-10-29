"""Ep 9 drawings (ours): the walk clock timeline, a step counter, glucose curves, bars, x-ray card frames, organ labels."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
RUBIK = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"
def F(s, p=RUBIK): return ImageFont.truetype(p, int(s))
STAGES = ["MINUTE 1", "MINUTE 10", "AFTER A MEAL", "3 DAYS OFF", "WEEKS", "1 YEAR", "YEARS", "THE NUMBER"]

def walk_clock(active, w=1300, h=86):
    """a strip of stages along the walk; the active one is lit, the past ones ticked"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); n = len(STAGES); seg = w / n
    d.rounded_rectangle((0, 0, w - 1, h - 1), 24, fill=(20, 26, 22, 225))
    for k, s in enumerate(STAGES):
        x0 = k * seg; col = (255, 206, 60) if k == active else ((150, 200, 150) if k < active else (150, 150, 140))
        if k == active: d.rounded_rectangle((x0 + 6, 8, x0 + seg - 6, h - 8), 18, fill=(70, 120, 70, 255))
        d.text((x0 + seg / 2, h / 2), s, font=F(22), fill=col, anchor="mm")
    return im

def step_counter(n, w=360, h=150):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(24, 30, 26, 235), outline=(255, 206, 60, 255), width=4)
    d.text((w / 2, 40), "STEPS", font=F(28), fill=(200, 220, 200), anchor="mm"); d.text((w / 2, 100), f"{int(n):,}", font=F(72, IMPACT), fill=(255, 206, 60), anchor="mm")
    return im

def glucose(u=1.0, walk=True, w=900, h=420, label=None):
    """two after-meal blood-sugar curves: sitting (red) vs a short walk (green); u = drawn fraction"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(24, 18, 12, 225))
    x0, x1, yb = 70, w - 40, h - 70; d.line((x0, yb, x1, yb), fill=(200, 190, 175), width=4); d.line((x0, 50, x0, yb), fill=(200, 190, 175), width=4)
    d.text((x1, yb + 24), "time after eating", font=F(24), fill=(200, 190, 175), anchor="rm"); d.text((x0 + 10, 60), "blood sugar", font=F(24), fill=(200, 190, 175))
    for amp, col in ((1.0, (230, 70, 60)), (0.78 if walk else 1.0, (90, 200, 110))):
        pts = [(x, yb - (yb - 80) * amp * math.exp(-((x - x0) / (x1 - x0) - 0.3) ** 2 / 0.03)) for x in range(x0, int(x0 + (x1 - x0) * u), 4)]
        if len(pts) > 1: d.line(pts, fill=col + (255,), width=7)
    d.text((x1 - 10, 70), "sitting", font=F(28), fill=(230, 70, 60), anchor="ra"); d.text((x1 - 10, 108), "short walk", font=F(28), fill=(90, 200, 110), anchor="ra")
    if label: d.text((w / 2, 26), label, font=F(26), fill=(255, 225, 120), anchor="mm")
    return im

def bars(rows, w=1100, u=1.0, title=None):
    h = 90 + 110 * len(rows) + (50 if title else 0); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(24, 18, 12, 225)); y0 = 40 + (50 if title else 0)
    if title: d.text((w / 2, 40), title, font=F(34), fill=(235, 225, 210), anchor="mm")
    for k, (lab, v, mx, col, txt) in enumerate(rows):
        y = y0 + k * 110; d.text((40, y), lab, font=F(34), fill=(255, 255, 255))
        d.rounded_rectangle((40, y + 44, w - 230, y + 90), 12, fill=(70, 60, 52, 255)); ww = (w - 270) * min(1, v / mx) * u
        d.rounded_rectangle((40, y + 44, 40 + max(14, ww), y + 90), 12, fill=col + (255,))
        d.text((w - 30, y + 67), txt, font=F(46, IMPACT), fill=(255, 206, 60), anchor="rm", stroke_width=3, stroke_fill=(10, 10, 10))
    return im

def xray_card(path, w=560, label=None, tint=(120, 200, 255)):
    """a Gray's Anatomy plate (public domain) turned into an 'x-ray' card: inverted on dark blue with a glow"""
    src = Image.open(path).convert("L"); h = int(src.height * w / src.width); src = src.resize((w, h), Image.LANCZOS)
    inv = Image.eval(src, lambda v: 255 - v); a = np.asarray(inv, np.float32) / 255
    rgb = np.stack([10 + a * tint[0], 20 + a * tint[1], 40 + a * tint[2]], 2).clip(0, 255).astype(np.uint8)
    card = Image.new("RGBA", (w + 30, h + 30 + (50 if label else 0)), (8, 14, 30, 255)); card.paste(Image.fromarray(rgb), (15, 15))
    if label: ImageDraw.Draw(card).text(((w + 30) / 2, h + 50), label, font=F(30), fill=(255, 225, 120), anchor="mm")
    m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=255); card.putalpha(m)
    return card

def checkmark_list(items, done, w=820):
    h = 70 * len(items) + 40; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(24, 18, 12, 225))
    for k, it in enumerate(items):
        y = 30 + k * 70; col = (255, 255, 255) if k < done else (110, 100, 90)
        if k < done: d.line([(40, y + 22), (54, y + 38), (80, y + 6)], fill=(120, 220, 120), width=7)
        else: d.ellipse((52, y + 16, 66, y + 30), fill=col)
        d.text((100, y), it, font=F(38), fill=col)
    return im
