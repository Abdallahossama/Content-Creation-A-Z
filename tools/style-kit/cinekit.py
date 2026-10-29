"""Cinematic Batata thumbnail kit (the default from 2026-10-14; the user picked it over the flat Batata-hero look).
Still the REAL potato with its marker face, no AI images. What changed:
  backdrop  : saturated colour, darker edges, a warm burst + soft light rays hidden behind Batata's head
  batata    : contrast/colour grade, warm key light, warm rim light on the burst side, cool rim on the other side
              (replaces the white sticker edge)
  hold      : marker-drawn arms + white cartoon mitts, so Batata can hold the prop
  prop      : glowing (thumbkit.led timers, card() index cards, any RGBA cut-out)
  words     : 1-2 huge Impact words, yellow-to-orange gradient, thick dark outline, drop shadow
Layout used so far: words top-left, prop centre-left, Batata right with its bottom off-frame."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageChops
from thumbkit import W, H, IMPACT, put
import marker as MK

INK = (14, 10, 8)
BLUE = dict(top=(34, 86, 235), edge=(6, 12, 70), warm=(255, 120, 30), rays=(255, 170, 70))
RED = dict(top=(214, 38, 40), edge=(60, 4, 10), warm=(255, 196, 40), rays=(255, 220, 120))
NIGHT = dict(top=(82, 46, 190), edge=(10, 6, 42), warm=(255, 110, 60), rays=(255, 160, 120))

def backdrop(pal=BLUE, burst=(880, 380), seed=3):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W * 0.55) / W) ** 2 + ((yy - H * 0.42) / H) ** 2)
    t = np.clip(d / 0.75, 0, 1)[..., None]
    a = np.array(pal["top"], np.float32) * (1 - t) + np.array(pal["edge"], np.float32) * t
    bx, by = burst; r = np.sqrt((xx - bx) ** 2 + (yy - by) ** 2); ang = np.arctan2(yy - by, xx - bx)
    rays = (0.5 + 0.5 * np.cos(ang * 9)) ** 6 * np.clip(1 - r / 900, 0, 1)
    warm = np.clip(1 - r / 640, 0, 1) ** 1.3
    a = a * (1 - 0.85 * warm[..., None]) + np.array(pal["warm"], np.float32) * 0.85 * warm[..., None]
    a += np.array(pal["rays"], np.float32) * (rays * 0.22)[..., None]
    a += np.random.default_rng(seed).normal(0, 3, a.shape)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def batata(expr, height, rot=-6):
    """expr = a Batata v2 expression name, or a full path to any Batata PNG (e.g. the boss versions)"""
    src = Image.open(expr if expr.endswith(".png") else MK.BATATA + f"Batata_{expr}.png").convert("RGBA")
    src = src.crop(src.getbbox()); src = src.resize((int(src.width * height / src.height), height), Image.LANCZOS)
    rgb, al = src.convert("RGB"), src.split()[3]
    rgb = ImageEnhance.Contrast(rgb).enhance(1.22); rgb = ImageEnhance.Color(rgb).enhance(1.25)
    arr = np.asarray(rgb, np.float32); w = arr.shape[1]; xs = np.linspace(0, 1, w)[None, :, None]
    arr = arr * (0.80 + 0.30 * xs) * np.array([1.06, 1.0, 0.92])
    a = np.asarray(al, np.float32) / 255; inner = np.asarray(al.filter(ImageFilter.MinFilter(41)), np.float32) / 255
    rim = Image.fromarray((np.clip(a - inner, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    rim = np.asarray(rim, np.float32)[..., None] / 255
    arr = arr + rim * (np.array([255, 175, 70]) * 1.7 * xs ** 1.2 + np.array([90, 170, 255]) * 1.3 * (1 - xs) ** 2.2)
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA"); out.putalpha(al)
    return out.rotate(rot, Image.BICUBIC, expand=True) if rot else out

def grad_word(txt, size, top=(255, 238, 90), bot=(255, 146, 18), stroke=14):
    f = ImageFont.truetype(IMPACT, size); bb = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), txt, font=f, stroke_width=stroke)
    pad = 40; Wt, Ht = bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2; o = (pad - bb[0], pad - bb[1])
    fill_m = Image.new("L", (Wt, Ht), 0); ImageDraw.Draw(fill_m).text(o, txt, font=f, fill=255)
    out_m = Image.new("L", (Wt, Ht), 0); ImageDraw.Draw(out_m).text(o, txt, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    g = np.clip((np.linspace(0, 1, Ht)[:, None, None] * Ht - pad) / (Ht - 2 * pad), 0, 1)
    col = (np.array(top) * (1 - g) + np.array(bot) * g) * np.ones((1, Wt, 1))
    im = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
    sh = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0)); sh.putalpha(out_m.point(lambda v: int(v * 0.75)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5))); im = ImageChops.offset(im, 7, 10)
    ol = Image.new("RGBA", (Wt, Ht), INK + (255,)); ol.putalpha(out_m); im.alpha_composite(ol)
    fl = Image.fromarray(col.astype(np.uint8)).convert("RGBA"); fl.putalpha(fill_m); im.alpha_composite(fl)
    return im.crop(im.getbbox())

def words(c, lines, size=170, x=40, y=18, rot=-4, step=152, indent=30):
    for k, l in enumerate(lines):
        put(c, grad_word(l, size).rotate(rot, Image.BICUBIC, expand=True), x + k * indent, y + k * step)

def glow(c, spr, x, y, col, r=38, a=0.9):
    m = spr.split()[3].filter(ImageFilter.MaxFilter(9)); g = Image.new("RGBA", spr.size, col + (0,)); g.putalpha(m.point(lambda v: int(v * a)))
    pad = r * 3; big = Image.new("RGBA", (spr.width + pad * 2, spr.height + pad * 2), (0, 0, 0, 0)); big.alpha_composite(g, (pad, pad))
    put(c, big.filter(ImageFilter.GaussianBlur(r)), x - pad, y - pad)

def mitt(c, cx, cy, r=34, rot=0):
    """a cartoon hand: white fill, black marker outline"""
    s = r * 4; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); m = s // 2
    d.ellipse((m - r, m - r * 0.8, m + r, m + r * 0.8), fill=(250, 248, 240, 255))
    for k in range(3):
        fy = m - r * 0.55 + k * r * 0.45
        d.ellipse((m + r * 0.35, fy - r * 0.26, m + r * 1.05, fy + r * 0.26), fill=(250, 248, 240, 255))
    im = im.rotate(rot, Image.BICUBIC); put(c, im, cx - s / 2, cy - s / 2)
    e = np.asarray(im.split()[3].filter(ImageFilter.MaxFilter(9)), np.int16) - np.asarray(im.split()[3], np.int16)
    ol = Image.new("RGBA", im.size, INK + (0,)); ol.putalpha(Image.fromarray(e.clip(0, 255).astype(np.uint8))); put(c, ol, cx - s / 2, cy - s / 2)

def card(lines, w=400, h=260, circle_line=0, rot=-6):
    """a real-looking index card: ruled lines, red margin, handwriting, red marker circle round one line"""
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = 30
    d.rectangle((o, o, o + w, o + h), fill=(250, 244, 226, 255))
    for k in range(1, 7): d.line((o, o + 34 + k * 34, o + w, o + 34 + k * 34), fill=(150, 185, 225, 255), width=2)
    d.line((o, o + 40, o + w, o + 40), fill=(225, 80, 80, 255), width=2)
    f = ImageFont.truetype(MK.HAND, 44); y = o + 50; boxes = []
    for l in lines:
        d.text((o + 24, y), l, font=f, fill=(24, 34, 110, 255)); boxes.append(d.textbbox((o + 24, y), l, font=f)); y += 62
    if circle_line is not None:
        x0, y0, x1, y1 = boxes[circle_line]
        MK.strokes(im, MK.circle_path((x0 + x1) / 2, (y0 + y1) / 2 + 4, (x1 - x0) / 2 + 26, (y1 - y0) / 2 + 18, seed=7), MK.RED, 7, seed=7)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.split()[3].point(lambda v: int(v * 0.5)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (8, 12)); out.alpha_composite(im)
    return out.rotate(rot, Image.BICUBIC, expand=True)

OIL = dict(top=(14, 74, 86), edge=(2, 12, 16), warm=(255, 140, 30), rays=(255, 186, 96))

SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd"}
def price_sign(price="4.36", label="REGULAR", h=130, col=(255, 52, 36)):
    """a gas-station price panel: white label on top, red 7-segment digits with a decimal point, a '$' in Impact"""
    dw, t, pad = int(h * 0.55), int(h * 0.13), 50; dol = ImageFont.truetype(IMPACT, int(h * 0.9))
    w = int(h * 0.62) + sum(int(h * 0.22) if ch == "." else dw + int(h * 0.12) for ch in price)
    top = int(h * 0.42); im = Image.new("RGBA", (w + pad * 2, h + top + pad * 2), (0, 0, 0, 0))
    lit = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lit); off = Image.new("RGBA", im.size, (0, 0, 0, 0)); do = ImageDraw.Draw(off)
    y0 = pad + top; x = pad
    dl.text((x, y0 + h / 2), "$", font=dol, fill=col + (255,), anchor="lm"); x += int(h * 0.62)
    for ch in price:
        if ch == ".":
            r = t * 0.6; dl.ellipse((x + 6, y0 + h - 2 * r, x + 6 + 2 * r, y0 + h), fill=col + (255,)); x += int(h * 0.22); continue
        y1, ym = y0 + h, y0 + h / 2
        segs = {"a": (x + t, y0, x + dw - t, y0 + t), "d": (x + t, y1 - t, x + dw - t, y1), "g": (x + t, ym - t / 2, x + dw - t, ym + t / 2),
                "f": (x, y0 + t, x + t, ym - t / 2), "b": (x + dw - t, y0 + t, x + dw, ym - t / 2),
                "e": (x, ym + t / 2, x + t, y1 - t), "c": (x + dw - t, ym + t / 2, x + dw, y1 - t)}
        for k, box in segs.items():
            (dl if k in SEG[ch] else do).rounded_rectangle(box, t // 2, fill=(col + (255,)) if k in SEG[ch] else (60, 10, 10, 120))
        x += dw + int(h * 0.12)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    d.rounded_rectangle((pad - 36, pad - 30, x + 26, y0 + h + 30), 24, fill=(14, 10, 12, 245), outline=(40, 40, 46, 255), width=5)
    d.rounded_rectangle((pad - 20, pad - 16, x + 10, pad + top - 18), 10, fill=(245, 245, 240, 255))
    d.text(((pad - 20 + x + 10) / 2, (pad - 16 + pad + top - 18) / 2), label, font=ImageFont.truetype(IMPACT, int(top * 0.62)), fill=(20, 20, 24, 255), anchor="mm")
    out.alpha_composite(off); out.alpha_composite(lit.filter(ImageFilter.GaussianBlur(5))); out.alpha_composite(lit)
    return out.crop(out.getbbox())

def print_card(img, border=12, rot=-6):
    """a real photo or map as a printed card: white edge, soft shadow, tilt"""
    e = Image.new("RGBA", (img.width + border * 2, img.height + border * 2), (255, 255, 255, 255)); e.alpha_composite(img.convert("RGBA"), (border, border))
    s = Image.new("RGBA", (e.width + 40, e.height + 40), (0, 0, 0, 0)); sh = Image.new("RGBA", e.size, (0, 0, 0, 150))
    s.alpha_composite(sh, (14, 18)); s = s.filter(ImageFilter.GaussianBlur(9)); s.alpha_composite(e, (0, 0))
    return s.rotate(rot, Image.BICUBIC, expand=True)

def oil_barrel(w=330, h=420, body=(196, 34, 30), label="CRUDE"):
    """a painted steel drum: cylinder shading + specular band, two ribs, lid with bung, stencil label, an oil drip"""
    pad, ry = 24, int(w * 0.13); im = Image.new("RGBA", (w + pad * 2, h + ry * 2 + pad * 2), (0, 0, 0, 0))
    x0, y0, x1, y1 = pad, pad + ry, pad + w, pad + ry + h
    m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    d.rectangle((x0, y0, x1, y1), fill=255); d.ellipse((x0, y1 - ry, x1, y1 + ry), fill=255)
    xs = np.clip((np.arange(im.width) - x0) / w, 0, 1)
    shade = 0.32 + 0.85 * np.sin(xs * np.pi) ** 0.8; hl = np.exp(-((xs - 0.3) / 0.07) ** 2) * 0.5
    row = np.array(body, np.float32)[None, :] * shade[:, None] + 255 * hl[:, None]
    arr = np.repeat(row[None], im.height, 0) + np.random.default_rng(2).normal(0, 3, (im.height, im.width, 1))
    b = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA"); b.putalpha(m); im.alpha_composite(b)
    d2 = ImageDraw.Draw(im)
    for f in (0.30, 0.70):
        yy = y0 + h * f
        d2.arc((x0, yy - ry, x1, yy + ry), 0, 180, fill=(70, 8, 8, 255), width=12)
        d2.arc((x0 + 4, yy - ry + 12, x1 - 4, yy + ry + 12), 10, 170, fill=(255, 140, 120, 150), width=5)
    d2.ellipse((x0, y0 - ry, x1, y0 + ry), fill=(122, 18, 16, 255), outline=(66, 8, 8, 255), width=8)
    d2.ellipse((x0 + 20, y0 - ry + 10, x1 - 20, y0 + ry - 10), fill=(150, 26, 22, 255))
    d2.ellipse((x0 + w * 0.62, y0 - ry * 0.4, x0 + w * 0.78, y0 + ry * 0.1), fill=(96, 96, 104, 255), outline=(40, 40, 44, 255), width=4)
    d2.text(((x0 + x1) / 2 - 10, y0 + h * 0.17), label, font=ImageFont.truetype(IMPACT, int(w * 0.17)), fill=(250, 236, 220, 200), anchor="mm")
    xd = x0 + w * 0.86                                                    # a glossy oil drip from the rim
    d2.rounded_rectangle((xd - 13, y0 - 6, xd + 13, y0 + 74), 13, fill=(12, 10, 10, 255)); d2.ellipse((xd - 20, y0 + 56, xd + 20, y0 + 104), fill=(12, 10, 10, 255))
    d2.line((xd - 5, y0 + 10, xd - 5, y0 + 60), fill=(120, 120, 130, 200), width=4); d2.ellipse((xd - 12, y0 + 70, xd - 2, y0 + 82), fill=(150, 150, 160, 220))
    return im

def _link(L, t, face):
    s = Image.new("RGBA", (L + 30, L + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(s); c = (L + 30) / 2
    if face:
        box = (c - L / 2, c - L * 0.31, c + L / 2, c + L * 0.31)
        d.ellipse(box, outline=(28, 30, 36, 255), width=t + 8); d.ellipse(box, outline=(176, 182, 192, 255), width=t)
        d.arc((box[0] + 4, box[1] + 3, box[2] - 4, box[3] - 3), 200, 290, fill=(245, 248, 252, 255), width=max(3, t // 3))
    else:
        d.rounded_rectangle((c - L / 2, c - t * 0.9, c + L / 2, c + t * 0.9), t, fill=(150, 156, 166, 255), outline=(28, 30, 36, 255), width=4)
        d.line((c - L / 2 + t, c - t * 0.3, c + L / 2 - t, c - t * 0.3), fill=(235, 238, 244, 255), width=3)
    return s

def chain(c, p0, p1, L=52, t=12):
    """a steel chain from p0 to p1: alternating face-on and edge-on links"""
    p0, p1 = np.array(p0, float), np.array(p1, float); n = int(np.hypot(*(p1 - p0)) / (L * 0.72))
    ang = np.degrees(np.arctan2(-(p1 - p0)[1], (p1 - p0)[0]))
    for k in range(n + 1):
        q = p0 + (p1 - p0) * k / max(n, 1); s = _link(L, t, k % 2 == 0).rotate(ang, Image.BICUBIC, expand=True)
        c.alpha_composite(s, (int(q[0] - s.width / 2), int(q[1] - s.height / 2)))

def padlock(w=128):
    h = int(w * 0.82); im = Image.new("RGBA", (w + 40, h + int(w * 0.75) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bx0, by0 = 20, 20 + int(w * 0.62)
    d.arc((20 + w * 0.18, 20, 20 + w * 0.82, 20 + w * 1.15), 180, 360, fill=(30, 32, 38, 255), width=int(w * 0.2))
    d.arc((20 + w * 0.18 + 5, 25, 20 + w * 0.82 - 5, 20 + w * 1.15 - 5), 180, 360, fill=(190, 196, 206, 255), width=int(w * 0.12))
    g = np.linspace(0, 1, h)[:, None, None]; col = np.array([255, 222, 96.0]) * (1 - g) + np.array([186, 120, 8.0]) * g
    body = Image.fromarray(np.repeat(col, w, 1).astype(np.uint8)).convert("RGBA"); mk = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mk).rounded_rectangle((0, 0, w - 1, h - 1), int(w * 0.16), fill=255); body.putalpha(mk)
    im.alpha_composite(body, (bx0, by0)); d.rounded_rectangle((bx0, by0, bx0 + w - 1, by0 + h - 1), int(w * 0.16), outline=(110, 66, 0, 255), width=5)
    kx, ky = bx0 + w / 2, by0 + h * 0.45
    d.ellipse((kx - 13, ky - 13, kx + 13, ky + 13), fill=(30, 18, 6, 255)); d.polygon([(kx - 8, ky + 4), (kx + 8, ky + 4), (kx + 12, ky + 34), (kx - 12, ky + 34)], fill=(30, 18, 6, 255))
    d.line((bx0 + 14, by0 + 12, bx0 + 14, by0 + h - 16), fill=(255, 244, 190, 220), width=6)
    return im

def locked_barrel():
    """the oil drum wrapped in two crossing chains with a gold padlock at the crossing"""
    b = oil_barrel(); pad = 60; im = Image.new("RGBA", (b.width + pad * 2, b.height + pad * 2), (0, 0, 0, 0)); im.alpha_composite(b, (pad, pad))
    x0, y0, x1, y1 = pad + 6, pad + 120, pad + b.width - 6, pad + b.height - 90
    chain(im, (x0 - 14, y0), (x1 + 14, y1)); chain(im, (x1 + 14, y0), (x0 - 14, y1))
    lk = padlock(); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    im.alpha_composite(lk, (int(cx - lk.width / 2), int(cy - lk.height * 0.42)))
    return im.crop(im.getbbox())

def photo_bg(path, src_pt, dst_pt, crop_w, blur=2.5, burst=None, warm=(255, 150, 60), tone=(1.0, 1.0, 1.0), dark=0.82):
    """a real photo as a cinematic background: crop so src_pt lands on dst_pt, shallow depth of field, punchy grade,
    an optional warm burst + rays (e.g. on the sun, behind Batata's head) and a darker top-left for the words"""
    im = Image.open(path).convert("RGB"); k = W / crop_w; ch = crop_w * H / W
    x0 = src_pt[0] - dst_pt[0] / k; y0 = src_pt[1] - dst_pt[1] / k
    assert 0 <= x0 and x0 + crop_w <= im.width and 0 <= y0 and y0 + ch <= im.height, f"crop out of bounds {x0, y0}"
    im = im.crop((int(x0), int(y0), int(x0 + crop_w), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(blur)); im = ImageEnhance.Contrast(im).enhance(1.15); im = ImageEnhance.Color(im).enhance(1.2)
    a = np.asarray(im, np.float32) * dark * np.array(tone)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a *= (1 - 0.45 * np.clip(1 - np.hypot(xx / 700, yy / 420), 0, 1))[..., None]      # darker top-left behind the words
    if burst:
        bx, by = burst; r = np.hypot(xx - bx, yy - by); ang = np.arctan2(yy - by, xx - bx)
        glowm = np.clip(1 - r / 520, 0, 1) ** 1.6; rays = (0.5 + 0.5 * np.cos(ang * 9)) ** 6 * np.clip(1 - r / 900, 0, 1)
        a += np.array(warm, np.float32) * (glowm * 0.55 + rays * 0.18)[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def corner_vignette(c, s=0.55):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); d = np.sqrt(((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    v = np.zeros((H, W, 4), np.uint8); v[..., 3] = (np.clip(d - 0.75, 0, 1) * 255 * s).astype(np.uint8); c.alpha_composite(Image.fromarray(v, "RGBA"))

SLEEVE = (30, 42, 104)
def scene(pal, expr, prop, prop_glow, lines, prop_xy=(250, 360), b_cx=905, b_top=175, b_h=700, sleeves=False, hand_y=(0.80, 0.20), bg=None, word_size=170, hold=True):
    """the standard layout: words top-left, glowing prop held by marker hands centre-left, Batata right.
    sleeves=True (the suited boss Batata): navy suit sleeves with white cuffs instead of marker stick arms"""
    c = bg.copy() if bg is not None else backdrop(pal)
    b = batata(expr, b_h); bx = b_cx - b.width // 2
    tx, ty = prop_xy; pw, ph = prop.size
    hands = [(tx + pw - 40, ty + ph * hand_y[0], 15), (tx + pw - 50, ty + ph * hand_y[1], -10)]
    if hold and not sleeves:
        arms = [MK.arrow_path((bx + 120, b_top + 470), hands[0][:2], bend=-0.25, head=0, seed=4)[0],
                MK.arrow_path((bx + 150, b_top + 330), hands[1][:2], bend=0.2, head=0, seed=6)[0]]
        MK.strokes(c, arms, INK, 16, seed=4)
    put(c, b, bx, b_top)
    if hold and sleeves:
        starts = [(bx + 0.10 * b.width, b_top + 0.86 * b_h), (bx + 0.07 * b.width, b_top + 0.76 * b_h)]
        arms = [MK.arrow_path(s_, (h[0] + 18, h[1] + 4), bend=bd, head=0, seed=sd)[0] for s_, h, bd, sd in zip(starts, hands, (-0.12, 0.12), (4, 6))]
        MK.strokes(c, arms, INK, 60, seed=4); MK.strokes(c, arms, SLEEVE, 46, seed=4)
        for h in hands:
            ImageDraw.Draw(c).ellipse((h[0] + 6, h[1] - 22, h[0] + 34, h[1] + 22), fill=(246, 246, 244, 255), outline=INK + (255,), width=4)
    if prop_glow: glow(c, prop, tx, ty, prop_glow, r=46, a=1.0); glow(c, prop, tx, ty, tuple(min(255, v + 50) for v in prop_glow), r=18, a=0.8)
    put(c, prop, tx, ty)
    if hold:
        for hx, hy, rot in hands: mitt(c, hx, hy, 34, rot)
    words(c, lines, size=word_size, step=int(word_size * 0.9)); corner_vignette(c)
    return c
