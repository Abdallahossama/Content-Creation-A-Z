"""Real-photo thumbnails (1280x720), 'famous YouTube' style: emotional real subject, 2-3 huge
condensed words, night grade, LED 3:00 clock, tiny Batata as the only brand hint."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H = 1280, 720
S = "D:/why habibi/1st video/claude_package/stock/"
PK = "D:/why habibi/WhyHabibi_Pack1_characters_rig_brand (1)/"
OUT = "D:/why habibi/1st video/claude_package/thumbnails/"
IMPACT = "C:/Windows/Fonts/impact.ttf"
YEL, RED, WHITE, BLACK = (255, 214, 0), (255, 38, 38), (255, 255, 255), (0, 0, 0)

def F(sz): return ImageFont.truetype(IMPACT, sz)

def word(txt, size, fill, stroke=12, shadow=10, glow=None):
    f = F(size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = d.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    pad = stroke + shadow + 30
    w, h = int(bb[2] - bb[0]) + pad * 2, int(bb[3] - bb[1]) + pad * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    ox, oy = pad - bb[0], pad - bb[1]
    if glow:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((ox, oy), txt, font=f, fill=glow + (255,), stroke_width=stroke + 6, stroke_fill=glow + (255,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    if shadow:
        dr.text((ox + shadow * 0.6, oy + shadow), txt, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    dr.text((ox, oy), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    return im.crop(im.getbbox())

def put(c, spr, x, y, anchor="lt", rot=0, scale=1.0):
    if scale != 1: spr = spr.resize((int(spr.width * scale), int(spr.height * scale)), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if anchor == "c": x, y = x - spr.width / 2, y - spr.height / 2
    elif anchor == "lc": y = y - spr.height / 2
    elif anchor == "rt": x = x - spr.width
    elif anchor == "cb": x, y = x - spr.width / 2, y - spr.height
    elif anchor == "lb": y = y - spr.height
    c.alpha_composite(spr, (int(x), int(y))) if x >= 0 and y >= 0 and x + spr.width <= W and y + spr.height <= H else paste_clip(c, spr, int(x), int(y))

def paste_clip(c, spr, x, y):
    sx0, sy0 = max(0, -x), max(0, -y); sx1, sy1 = min(spr.width, W - x), min(spr.height, H - y)
    if sx1 > sx0 and sy1 > sy0:
        c.alpha_composite(spr.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))

def glow_behind(spr, col, r=30, strength=1.6):
    a = spr.getchannel("A").filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * strength)))
    pad = r * 2
    out = Image.new("RGBA", (spr.width + pad * 2, spr.height + pad * 2), (0, 0, 0, 0))
    g = Image.new("RGBA", spr.size, col + (0,)); g.putalpha(a)
    out.alpha_composite(g.resize(spr.size), (pad, pad)); out = out.filter(ImageFilter.GaussianBlur(r / 2))
    out.alpha_composite(spr, (pad, pad))
    return out

def radial(c, cx, cy, r, col, a=200):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(1 - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r, 0, 1) ** 1.8
    arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = col; arr[..., 3] = (d * a).astype(np.uint8)
    c.alpha_composite(Image.fromarray(arr, "RGBA"))

def vignette(c, s=0.65):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    a = (np.clip(d - 0.55, 0, 1) ** 1.3 * 255 * s).clip(0, 255).astype(np.uint8)
    arr = np.zeros((H, W, 4), np.uint8); arr[..., 3] = a; c.alpha_composite(Image.fromarray(arr, "RGBA"))

def left_fade(c, x0=0, x1=620, a=245):
    g = np.zeros((H, W, 4), np.uint8)
    ramp = np.clip((x1 - np.arange(W)) / (x1 - x0), 0, 1) ** 1.2
    g[..., 3] = (ramp[None, :] * a).astype(np.uint8); c.alpha_composite(Image.fromarray(g, "RGBA"))

def night_grade(im, bright=0.62, blue=1.12, red=0.82, contrast=1.25):
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im.convert("RGB")).enhance(bright)).enhance(contrast)
    a = np.asarray(im).astype(np.float32); a[..., 0] *= red; a[..., 2] *= blue
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def stars(c, n=60, seed=2):
    r = np.random.default_rng(seed); d = ImageDraw.Draw(c)
    for _ in range(n):
        x, y, s = r.uniform(0, W), r.uniform(0, H), r.choice([1.5, 2, 3])
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, int(r.uniform(90, 220))))

SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd"}
def led(text="3:00", h=180, col=(255, 40, 30), housing=True):
    dw, t = int(h * 0.55), int(h * 0.13)
    w = sum(int(h * 0.18) if ch == ":" else dw + int(h * 0.12) for ch in text)
    pad = 60
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    lit = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lit); off = Image.new("RGBA", im.size, (0, 0, 0, 0)); do = ImageDraw.Draw(off)
    x = pad
    for ch in text:
        if ch == ":":
            r = t * 0.55
            for yy in (pad + h * 0.32, pad + h * 0.68): dl.ellipse((x + 4, yy - r, x + 4 + 2 * r, yy + r), fill=col + (255,))
            x += int(h * 0.18); continue
        y0, y1, ym = pad, pad + h, pad + h / 2
        segs = {"a": (x + t, y0, x + dw - t, y0 + t), "d": (x + t, y1 - t, x + dw - t, y1), "g": (x + t, ym - t / 2, x + dw - t, ym + t / 2),
                "f": (x, y0 + t, x + t, ym - t / 2), "b": (x + dw - t, y0 + t, x + dw, ym - t / 2),
                "e": (x, ym + t / 2, x + t, y1 - t), "c": (x + dw - t, ym + t / 2, x + dw, y1 - t)}
        for k, box in segs.items():
            (dl if k in SEG[ch] else do).rounded_rectangle(box, t // 2, fill=(col + (255,)) if k in SEG[ch] else (60, 10, 10, 120))
        x += dw + int(h * 0.12)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if housing:
        ImageDraw.Draw(out).rounded_rectangle((pad - 40, pad - 34, x + 26, pad + h + 34), 26, fill=(14, 10, 12, 245), outline=(40, 40, 46, 255), width=5)
    out.alpha_composite(off)
    out.alpha_composite(lit.filter(ImageFilter.GaussianBlur(16))); out.alpha_composite(lit.filter(ImageFilter.GaussianBlur(5))); out.alpha_composite(lit)
    return out.crop(out.getbbox())

def batata_peek(c, x=26, size=120):
    b = Image.open(PK + "01_Characters_Plain/Batata/Batata_shocked.png").convert("RGBA")
    b = b.crop(b.getbbox()); b = b.resize((size, int(b.height * size / b.width)), Image.LANCZOS)
    b = b.crop((0, 0, b.width, int(b.height * 0.62)))      # only the head peeks in
    put(c, b, x, H - b.height, rot=0)

def save(c, name):
    os.makedirs(OUT, exist_ok=True)
    p = OUT + name + ".png"; c.convert("RGB").save(p, optimize=True); print(p); return p

def photo_fill(path, crop, dx=0, grade=True, **kw):
    im = Image.open(path).convert("RGB").crop(crop).resize((W, H), Image.LANCZOS)
    im = night_grade(im, **kw) if grade else im.convert("RGBA")
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255)); c.alpha_composite(im, (dx, 0)) if dx >= 0 else paste_clip(c, im, dx, 0)
    return c

# 1) NOT AGAIN — hands over mouth, eyes wide, night grade
c = photo_fill(S + "pexels-8276884.jpg", (0, 230, 1920, 1310), dx=330, bright=0.55, blue=1.18, red=0.86)
radial(c, 1000, 260, 420, (60, 120, 255), 70)
left_fade(c, 380, 780, 255); vignette(c)
put(c, word("NOT", 150, WHITE), 40, 40)
put(c, word("AGAIN", 250, YEL, stroke=14, glow=(255, 160, 0)), 30, 175)
put(c, led("3:00", 120), 60, 500, rot=0)
batata_peek(c, x=960); save(c, "real_1_NOT_AGAIN")

# 2) BRAIN, STOP. — man staring at his phone, black background
c = photo_fill(S + "pexels-11645171.jpg", (100, 80, 1920, 1104), grade=False)
radial(c, 640, 330, 300, (120, 170, 255), 90)
card = Image.new("RGBA", (470, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
d.rounded_rectangle((0, 0, 469, 169), 26, fill=(24, 24, 30, 235), outline=(255, 255, 255, 60), width=2)
d.rounded_rectangle((22, 26, 122, 126), 18, fill=(229, 9, 20))
d.polygon([(58, 50), (58, 102), (100, 76)], fill=WHITE)
fs = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26); fr = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 21)
d.text((140, 24), "NOW REPLAYING", font=fr, fill=(255, 80, 80))
d.text((140, 52), "That time you waved", font=fs, fill=WHITE); d.text((140, 84), "back at a stranger", font=fs, fill=WHITE)
d.rounded_rectangle((140, 132, 440, 140), 4, fill=(80, 80, 90)); d.rounded_rectangle((140, 132, 380, 140), 4, fill=(229, 9, 20))
put(c, glow_behind(card, (120, 170, 255), 22, 0.9), 70, 470, rot=3)
put(c, word("BRAIN,", 165, WHITE), 40, 30)
put(c, word("STOP.", 245, RED, stroke=14, glow=(255, 0, 0)), 34, 185)
batata_peek(c, x=960); save(c, "real_2_BRAIN_STOP")

# 3) CRINGE O'CLOCK — shocked man + giant LED clock
c = Image.new("RGBA", (W, H), (8, 6, 14, 255)); stars(c, 50)
radial(c, 380, 470, 520, (200, 20, 20), 150); radial(c, 1000, 380, 500, (40, 60, 180), 110)
put(c, led("3:00", 170), 46, 455)
man = Image.open(S + "cut_shocked.png").convert("RGBA"); man = man.resize((int(man.width * 790 / man.height), 790), Image.LANCZOS)
mg = glow_behind(man, (255, 90, 70), 24, 1.2); paste_clip(c, mg, W - mg.width + 120, H - mg.height + 150)
put(c, word("CRINGE", 140, WHITE), 40, 22)
put(c, word("O'CLOCK", 170, YEL, stroke=14, glow=(255, 150, 0)), 36, 158)
vignette(c, 0.5); batata_peek(c, x=960)
save(c, "real_3_CRINGE_OCLOCK")

# 4) CRINGE ATTACK — real brain + screaming seagull (like the D-G references)
c = Image.new("RGBA", (W, H), (4, 4, 8, 255)); stars(c, 70, 5)
radial(c, 330, 520, 480, (255, 70, 120), 70)
gull = Image.open(S + "cut_seagull.png").convert("RGBA"); gull = gull.resize((int(gull.width * 1.15), int(gull.height * 1.15)), Image.LANCZOS)
put(c, gull, 20, 20, rot=-8)
brain = Image.open(S + "cut_brain.png").convert("RGBA"); brain = brain.resize((620, int(brain.height * 620 / brain.width)), Image.LANCZOS)
bg_ = glow_behind(brain, (255, 120, 150), 28, 1.0); paste_clip(c, bg_, -40, H - bg_.height + 70)
put(c, word("CRINGE", 190, WHITE), W - 40, 90, anchor="rt")
put(c, word("ATTACK", 230, RED, stroke=14, glow=(255, 0, 0)), W - 30, 300, anchor="rt")
batata_peek(c, x=960); save(c, "real_4_CRINGE_ATTACK")

# 5) THEY BARELY NOTICED — lone man in a spotlight, gold/blue duotone
im = Image.open(S + "pexels-460918.jpg").convert("L").crop((0, 90, 1920, 1170)).resize((W, H), Image.LANCZOS)
im = ImageEnhance.Contrast(im).enhance(1.3)
duo = ImageOps.colorize(im, black=(4, 6, 22), mid=(70, 60, 90), white=(255, 226, 160)).convert("RGBA")
c = Image.new("RGBA", (W, H), (0, 0, 0, 255)); paste_clip(c, duo, -40, 0)
cone = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(cone).polygon([(150, -10), (300, -10), (420, 720), (40, 720)], fill=(255, 230, 170, 45))
c.alpha_composite(cone.filter(ImageFilter.GaussianBlur(20)))
put(c, word("THEY BARELY", 128, WHITE), W - 40, 120, anchor="rt")
put(c, word("NOTICED", 235, YEL, stroke=14, glow=(255, 170, 0)), W - 30, 255, anchor="rt")
vignette(c, 0.5); batata_peek(c, x=960); save(c, "real_5_THEY_BARELY_NOTICED")
