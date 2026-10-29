"""Thumbnail kit (1280x720): real emotional photo, <=3 huge Impact words, night grade, LED clock, marker circle,
Batata v2 peeking small. Same recipe as Ep 1's thumbs_real.py, without the glow, importable by any episode."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import marker as MK

W, H = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"
YEL, RED, WHITE, BLACK = (255, 194, 26), (240, 64, 47), (255, 255, 255), (0, 0, 0)

def word(txt, size, fill, stroke=12, shadow=10):
    f = ImageFont.truetype(IMPACT, size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = d.textbbox((0, 0), txt, font=f, stroke_width=stroke); pad = stroke + shadow + 20
    im = Image.new("RGBA", (int(bb[2] - bb[0]) + pad * 2, int(bb[3] - bb[1]) + pad * 2), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    ox, oy = pad - bb[0], pad - bb[1]
    if shadow: dr.text((ox + shadow * 0.6, oy + shadow), txt, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    dr.text((ox, oy), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    return im.crop(im.getbbox())

def paste_clip(c, spr, x, y):
    sx0, sy0 = max(0, -x), max(0, -y); sx1, sy1 = min(spr.width, W - x), min(spr.height, H - y)
    if sx1 > sx0 and sy1 > sy0: c.alpha_composite(spr.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))

def put(c, spr, x, y, anchor="lt", rot=0, scale=1.0):
    if scale != 1: spr = spr.resize((int(spr.width * scale), int(spr.height * scale)), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if anchor == "c": x, y = x - spr.width / 2, y - spr.height / 2
    elif anchor == "rt": x -= spr.width
    elif anchor == "lb": y -= spr.height
    paste_clip(c, spr, int(x), int(y))

def shade(c, cx, cy, r, col, a=200):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.clip(1 - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r, 0, 1) ** 1.8
    arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = col; arr[..., 3] = (d * a).astype(np.uint8); c.alpha_composite(Image.fromarray(arr, "RGBA"))

def vignette(c, s=0.6):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    arr = np.zeros((H, W, 4), np.uint8); arr[..., 3] = (np.clip(d - 0.55, 0, 1) ** 1.3 * 255 * s).clip(0, 255).astype(np.uint8)
    c.alpha_composite(Image.fromarray(arr, "RGBA"))

def side_fade(c, x0, x1, a=235, right=False):
    ramp = np.clip((np.arange(W) - x0) / (x1 - x0), 0, 1) if right else np.clip((x1 - np.arange(W)) / (x1 - x0), 0, 1)
    g = np.zeros((H, W, 4), np.uint8); g[..., 3] = (ramp[None, :] ** 1.2 * a).astype(np.uint8); c.alpha_composite(Image.fromarray(g, "RGBA"))

def night(im, bright=0.62, blue=1.12, red=0.82, contrast=1.25):
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im.convert("RGB")).enhance(bright)).enhance(contrast)
    a = np.asarray(im).astype(np.float32); a[..., 0] *= red; a[..., 2] *= blue
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def photo(path, focus=(0.5, 0.5), zoom=1.0, dx=0, grade=True, **kw):
    im = Image.open(path).convert("RGB"); iw, ih = im.size; ar = W / H
    cw, ch = (iw, iw / ar) if iw / ih < ar else (ih * ar, ih); cw /= zoom; ch /= zoom
    cx = min(max(focus[0] * iw, cw / 2), iw - cw / 2); cy = min(max(focus[1] * ih, ch / 2), ih - ch / 2)
    im = im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.LANCZOS)
    im = night(im, **kw) if grade else im.convert("RGBA")
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255)); paste_clip(c, im, dx, 0); return c

SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd"}
def led(text="1:07", h=180, col=(255, 40, 30)):
    dw, t = int(h * 0.55), int(h * 0.13); pad = 60
    w = sum(int(h * 0.18) if ch == ":" else dw + int(h * 0.12) for ch in text)
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
    ImageDraw.Draw(out).rounded_rectangle((pad - 40, pad - 34, x + 26, pad + h + 34), 26, fill=(14, 10, 12, 245), outline=(40, 40, 46, 255), width=5)
    out.alpha_composite(off); out.alpha_composite(lit.filter(ImageFilter.GaussianBlur(5))); out.alpha_composite(lit)
    return out.crop(out.getbbox())

def circle(c, cx, cy, rx, ry, color=RED, width=9, seed=5):
    MK.strokes(c, MK.circle_path(cx, cy, rx, ry, seed=seed), color, width)

def batata_peek(c, x=980, size=120, expr="shocked"):
    b = MK.sticker(MK.BATATA + f"Batata_{expr}.png", int(size * 1.41), border=6, rot=0)
    put(c, b.crop((0, 0, b.width, int(b.height * 0.74))), x, H - int(b.height * 0.74))
