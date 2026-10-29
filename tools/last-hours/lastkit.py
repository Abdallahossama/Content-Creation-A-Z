"""lastkit: The Last Hours editing kit (16:9 documentary). Black / bone / evidence-red, typewriter timestamps,
real archive photos in black and white with slow push-ins, case-file prints, red evidence marks, hard cuts.
No grain, no glow, no light leaks, no duotone, no pills/badges (see Ask Habibi no-AI-slop rule)."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

W, H, FPS = 1920, 1080, 30
F = "C:/Windows/Fonts/"
COND, TYPE, SER = F + "FRAMDCN.TTF", F + "courbd.ttf", F + "georgiai.ttf"
INK, BONE, RED, STEEL = (13, 13, 14), (236, 230, 214), (178, 34, 34), (150, 156, 162)
_FONTS = {}
def font(p, s):
    k = (p, int(s))
    if k not in _FONTS: _FONTS[k] = ImageFont.truetype(p, int(s))
    return _FONTS[k]
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def clamp01(x): return min(max(x, 0.0), 1.0)

_IMG = {}
def bw(path, crop=None, tone=(1.0, 0.985, 0.95)):
    """archive look: grayscale, gentle contrast, bone-white highlights (not a duotone: one warm white point)"""
    k = (path, crop)
    if k not in _IMG:
        im = Image.open(path).convert("RGB")
        if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=0.5)
        a = np.asarray(g, np.float32)[..., None] / 255.0 * np.array([236, 230, 214], np.float32) * np.array(tone, np.float32)
        _IMG[k] = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    return _IMG[k]

def kenburns(src, t, t0, t1, z0=1.04, z1=1.14, c0=(0.5, 0.5), c1=(0.5, 0.5)):
    """full-frame slow push/pan of an image over [t0, t1] (cover-fit); c = focus centre in image fractions"""
    u = clamp01((t - t0) / max(t1 - t0, 1e-6)); z = z0 + (z1 - z0) * u
    cx = c0[0] + (c1[0] - c0[0]) * u; cy = c0[1] + (c1[1] - c0[1]) * u
    s = max(W / src.width, H / src.height) * z; w, h = W / s, H / s
    x0 = min(max(cx * src.width - w / 2, 0), src.width - w); y0 = min(max(cy * src.height - h / 2, 0), src.height - h)
    return src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert("RGBA")

def vignette(img, k=0.38):
    if not hasattr(vignette, "m"):
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        vignette.m = np.clip(1 - k * np.clip(r - 0.55, 0, None) ** 1.6, 0, 1).astype(np.float32)[..., None]
    a = np.asarray(img.convert("RGB"), np.float32) * vignette.m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def typewriter(c, text, t, t0, x, y, size=64, fill=BONE, cps=22, anchor="lm", fnt=TYPE, cursor=True):
    """text typed letter by letter from t0 (cps chars per second); returns number of visible chars"""
    if t < t0: return 0
    n = min(len(text), int((t - t0) * cps) + 1); d = ImageDraw.Draw(c); f = font(fnt, size)
    shown = text[:n]
    if cursor and n < len(text) or (cursor and int(t * 2) % 2 == 0 and n == len(text) and t - t0 < len(text) / cps + 1.2):
        shown += "_"
    d.text((x, y), shown, font=f, fill=fill, anchor=anchor); return n

def text(c, s, x, y, size, fill=BONE, fnt=COND, anchor="mm", alpha=1.0):
    if alpha <= 0: return
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), s, font=font(fnt, size), fill=tuple(fill) + (int(255 * alpha),), anchor=anchor); c.alpha_composite(lay)

def rule(c, x0, x1, y, t, t0, dur=0.5, width=6, col=RED):
    if t < t0: return
    u = ease((t - t0) / dur); ImageDraw.Draw(c).rectangle((x0, y, x0 + (x1 - x0) * u, y + width), fill=col)

def hour_card(c, t, t0, big, sub, cps=16):
    """black chapter card: the signature 'time' title, typed, with a red rule"""
    ImageDraw.Draw(c).rectangle((0, 0, W, H), fill=INK)
    n = typewriter(c, big, t, t0, W / 2 - len(big) * 0.3 * 230 / 2 * 1.0, H / 2 - 40, size=230, cps=cps, anchor="lm", cursor=False)
    if n >= len(big):
        t1 = t0 + len(big) / cps
        text(c, sub, W / 2, H / 2 + 140, 62, STEEL, SER, alpha=ease((t - t1) / 0.4))
        rule(c, W / 2 - 300, W / 2 + 300, H / 2 + 205, t, t1 + 0.2)

def print_card(img, w, border=16, rot=0.0):
    """a photo print: bone border, slight rotation, soft drop shadow"""
    im = img.copy(); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    card = Image.new("RGBA", (im.width + 2 * border, im.height + 2 * border), BONE + (255,)); card.paste(im, (border, border))
    sh = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", card.size, (0, 0, 0, 150)), (30, 38)); sh = sh.filter(ImageFilter.GaussianBlur(14))
    sh.alpha_composite(card, (30, 30)); return sh.rotate(rot, Image.BICUBIC, expand=True)

def drop(c, spr, cx, cy, t, t0, dur=0.35, dy=60):
    """slide-and-settle in (no bounce)"""
    if t < t0: return
    u = ease((t - t0) / dur); y = cy + dy * (1 - u)
    s = spr.copy()
    if u < 1: s.putalpha(s.split()[3].point(lambda v: int(v * u)))
    c.alpha_composite(s, (int(cx - s.width / 2), int(y - s.height / 2)))

def red_ellipse(c, box, t, t0, dur=0.5, width=8):
    """hand-drawn-ish red ellipse that draws itself on (one stroke, slight overshoot)"""
    if t < t0: return
    u = ease((t - t0) / dur); x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    n = int(80 * u) + 2; a0 = -2.2
    pts = [(cx + rx * (1 + 0.04 * math.sin(3 * i / 13)) * math.cos(a0 + 2 * math.pi * 1.08 * i / 80),
            cy + ry * (1 + 0.04 * math.cos(2 * i / 11)) * math.sin(a0 + 2 * math.pi * 1.08 * i / 80)) for i in range(n)]
    ImageDraw.Draw(c).line(pts, fill=RED + (255,), width=width, joint="curve")

def stamp(c, s, cx, cy, t, t0, size=120, rot=-8):
    """rubber-stamp text slammed on (scale 1.25 -> 1.0); red ink, double rule frame"""
    if t < t0: return
    u = ease((t - t0) / 0.18); k = 1.25 - 0.25 * u
    f = font(COND, size); bb = f.getbbox(s); w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 50
    lay = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((10, 10, w + 10, h + 10), outline=RED + (235,), width=7); d.rectangle((22, 22, w - 2, h - 2), outline=RED + (235,), width=3)
    d.text(((w + 20) / 2, (h + 20) / 2), s, font=f, fill=RED + (235,), anchor="mm")
    lay = lay.rotate(rot, Image.BICUBIC, expand=True); lay = lay.resize((int(lay.width * k), int(lay.height * k)), Image.LANCZOS)
    c.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def fade_black(c, a):
    if a <= 0: return c
    return Image.blend(c, Image.new("RGBA", c.size, INK + (255,)), min(a, 1.0))
