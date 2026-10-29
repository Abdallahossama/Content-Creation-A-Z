"""Ask Habibi 'cut & marker' kit (from Ep. 2): the anti-AI-slop look, see _style_kit/STYLE_RULES.md.
Real sources on screen + an editor's hand on top: yellow highlighter, red/yellow marker circles, arrows and notes
(Ink Free), white-bordered cut-out stickers (Batata, cut-out people), the channel's Rubik captions.
No cards, borders, pills, dot wordmarks, tracked micro-labels, glow or light leaks."""
import math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
NAVY = (11, 16, 80); YEL = (255, 194, 26); RED = (240, 64, 47); WHITE = (255, 255, 255); BLACK = (0, 0, 0)
KIT = "D:/why habibi/_style_kit/"
RUBIK = KIT + "fonts/Rubik-Bold.ttf"          # = CapCut font id 7148699606082130433 (the caption font)
BATATA = KIT + "mascot/batata/"                # Batata_<expression>.png, the default mascot
HAND = "C:/Windows/Fonts/Inkfree.ttf"
CAP_Y = 934            # caption centre = CapCut y -0.73
SS = 2                 # supersampling for marker strokes

@functools.lru_cache(maxsize=64)
def font(path, size): return ImageFont.truetype(path, size)

def _noise(n, seed, amp, freqs=(1, 2, 3)):
    """smooth wobble, n samples, +-amp"""
    r = np.random.default_rng(seed); t = np.linspace(0, 1, n); out = np.zeros(n)
    for f in freqs: out += r.uniform(-1, 1) * np.sin(2 * np.pi * f * t + r.uniform(0, 6.28)) / f
    return out * amp

# ---------------------------------------------------------------- hand-drawn paths (frame px)
def circle_path(cx, cy, rx, ry, seed=0, turns=1.18, tilt=-3, n=320):
    """a quick marker loop: starts upper-left, goes round once and overshoots, never a perfect ellipse"""
    r = np.random.default_rng(seed)
    a0 = math.radians(r.uniform(200, 230)); t = np.linspace(0, turns * 2 * np.pi, n); ang = a0 - t
    k = 1 + _noise(n, seed, 0.045) + 0.08 * t / (2 * np.pi) - 0.04
    x, y = rx * k * np.cos(ang), ry * k * np.sin(ang)
    c, s = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    return [np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)]

def arrow_path(p0, p1, bend=0.25, head=42, seed=0):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = np.hypot(*d); nrm = np.array([-d[1], d[0]]) / L
    ctrl = (p0 + p1) / 2 + nrm * L * bend
    t = np.linspace(0, 1, 90)[:, None]
    shaft = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * ctrl + t ** 2 * p1
    shaft = shaft + np.stack([_noise(90, seed, 3), _noise(90, seed + 1, 3)], 1)
    tg = shaft[-1] - shaft[-8]; tg /= np.hypot(*tg); heads = []
    for a in (152, -146):
        a = math.radians(a); q = p1 + np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]) @ tg * head
        heads.append(np.linspace(q, shaft[-1], 14))
    return [shaft] + heads

def underline_path(x0, x1, y, seed=0, flick=True):
    n = 60; xs = np.linspace(x0, x1, n); ys = y + _noise(n, seed, 5) + np.linspace(0, -6, n)
    p = [np.stack([xs, ys], 1)]
    if flick: p.append(np.linspace([x1 - 10, y - 4], [x0 + (x1 - x0) * 0.35, y + 16], 30))
    return p

def strokes(canvas, paths, color=RED, width=11, progress=1.0, seed=0):
    """draw marker strokes in order; progress 0..1 writes them on (pen moving along the path)"""
    lens = [float(np.sum(np.hypot(*np.diff(p, axis=0).T))) for p in paths]; budget = sum(lens) * progress
    if budget <= 0: return canvas
    allp = np.concatenate(paths); m = width * 2
    x0, y0 = (np.floor(allp.min(0) - m)).astype(int); x1, y1 = (np.ceil(allp.max(0) + m)).astype(int)
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(canvas.width, x1), min(canvas.height, y1)
    if x1 <= x0 or y1 <= y0: return canvas
    lay = Image.new("L", ((x1 - x0) * SS, (y1 - y0) * SS), 0); d = ImageDraw.Draw(lay)
    for i, (p, L) in enumerate(zip(paths, lens)):
        if budget <= 0: break
        cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(p, axis=0).T))])
        s = np.arange(0, min(budget, L), 0.8); budget -= L
        if len(s) == 0: continue
        xs, ys = np.interp(s, cum, p[:, 0]), np.interp(s, cum, p[:, 1])
        wob = 1 + _noise(max(len(s), 2), seed + i, 0.16)[:len(s)]
        taper = np.clip(np.minimum((s + 4) / (L * 0.06 + 6), (L - s + 4) / (L * 0.08 + 6)), 0.45, 1)
        for x, y, wk, tp in zip(xs, ys, wob, taper):
            rr = width * wk * tp / 2 * SS; cx, cy = (x - x0) * SS, (y - y0) * SS
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=255)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    col = Image.new("RGBA", lay.size, tuple(color) + (255,)); col.putalpha(lay)
    canvas.alpha_composite(col, (int(x0), int(y0))); return canvas

def highlight(canvas, box, progress=1.0, seed=0, color=YEL, strength=0.78):
    """highlighter swipe over a text box (x0,y0,x1,y1) in canvas px, multiply-blended so the ink stays black"""
    x0, y0, x1, y1 = box; h = y1 - y0
    x0 -= h * 0.25; x1 += h * 0.25; y0 -= h * 0.14; y1 += h * 0.10
    xe = x0 + (x1 - x0) * progress
    if xe <= x0 + 2: return canvas
    r = np.random.default_rng(seed); n = 28; xs = np.linspace(x0, xe, n); slope = r.uniform(-0.01, 0.01)
    top = y0 + (xs - x0) * slope + _noise(n, seed, h * 0.05); bot = y1 + (xs - x0) * slope + _noise(n, seed + 7, h * 0.05)
    poly = list(zip(xs, top)) + [(xe + h * 0.1, (top[-1] + bot[-1]) / 2)] + list(zip(xs[::-1], bot[::-1])) \
        + [(x0 - h * 0.08, (top[0] + bot[0]) / 2)]
    bx0, by0 = int(max(0, x0 - h)), int(max(0, min(top) - 6)); bx1, by1 = int(min(canvas.width, xe + h)), int(min(canvas.height, max(bot) + 6))
    if bx1 <= bx0 or by1 <= by0: return canvas
    m = Image.new("L", (bx1 - bx0, by1 - by0), 0); ImageDraw.Draw(m).polygon([(px - bx0, py - by0) for px, py in poly], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(1.0)), np.float32) / 255 * strength
    a *= (1 + _noise(a.shape[0], seed + 3, 0.07, freqs=(3, 5, 9)))[:, None]          # felt-tip streaks
    reg = np.asarray(canvas.crop((bx0, by0, bx1, by1)), np.float32)
    reg[..., :3] *= (1 - a[..., None]) + a[..., None] * (np.array(color, np.float32) / 255)
    canvas.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8), "RGBA"), (bx0, by0)); return canvas

# ---------------------------------------------------------------- type
SYMBOL = "C:/Windows/Fonts/seguisym.ttf"           # Ink Free has no arrows / ≠ / ✓: those come from Segoe UI Symbol
SYMS = set("→←↑↓↗↘≠✓✗×≈♥")

@functools.lru_cache(maxsize=256)
def _hand_base(s, size, color, thick):
    f, fs = font(HAND, size), font(SYMBOL, int(size * 1.05))
    d = ImageDraw.Draw(Image.new("L", (1, 1))); lh = int(size * 1.08)
    def runs(line):
        out = []
        for ch in line:
            sym = ch in SYMS
            if out and out[-1][1] == sym: out[-1][0] += ch
            else: out.append([ch, sym])
        return out
    lines = s.split("\n")
    wmax = max(sum(d.textlength(t, font=fs if sy else f) for t, sy in runs(l)) for l in lines)
    im = Image.new("RGBA", (int(wmax) + 40 + thick * 2, lh * len(lines) + int(size * 0.6) + 24), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im); y = 12
    xb = f.getbbox("x"); x_mid = (xb[1] + xb[3]) / 2           # centre symbols on the handwriting's x-height
    for l in lines:
        x = 12
        for t, sy in runs(l):
            ff = fs if sy else f; dy = 0
            if sy:
                sb = fs.getbbox(t); dy = x_mid - (sb[1] + sb[3]) / 2
            dr.text((x, y + dy), t, font=ff, fill=color, stroke_width=thick, stroke_fill=color)
            x += d.textlength(t, font=ff)
        y += lh
    bb = im.getbbox() or (0, 0, 1, 1)
    return im.crop((max(0, bb[0] - 10), max(0, bb[1] - 10), min(im.width, bb[2] + 10), min(im.height, bb[3] + 10)))

def hand(s, size=66, color=RED, rot=-4, thick=1, reveal=1.0):
    """handwritten marker note (Ink Free, thickened; symbols from Segoe UI Symbol). reveal 0..1 = written left-to-right"""
    im = _hand_base(s, size, tuple(color), thick).copy()
    if reveal < 1:
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rectangle((0, 0, int(im.width * reveal), im.height), fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", im.size, 0), m))
    return im.rotate(rot, Image.BICUBIC, expand=True)

def bold(s, size, color=WHITE, stroke=0, stroke_col=BLACK):
    f = font(RUBIK, size); d = ImageDraw.Draw(Image.new("L", (1, 1)))
    bb = d.multiline_textbbox((0, 0), s, font=f, stroke_width=stroke, spacing=int(size * 0.02))
    im = Image.new("RGBA", (int(math.ceil(bb[2] - bb[0])) + 8, int(math.ceil(bb[3] - bb[1])) + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).multiline_text((4 - bb[0], 4 - bb[1]), s, font=f, fill=tuple(color), stroke_width=stroke,
                                      stroke_fill=tuple(stroke_col), spacing=int(size * 0.02))
    return im

def outlined(s, size, color=WHITE, stroke=6, track=0.035):
    """Rubik with a black outline drawn under ALL letters first, so outlines never eat the neighbouring letters"""
    f = font(RUBIK, size); d = ImageDraw.Draw(Image.new("L", (1, 1))); gap = size * track
    xs, x = [], 0.0
    for ch in s: xs.append(x); x += d.textlength(ch, font=f) + (size * 0.12 if ch == " " else gap)
    asc, desc = f.getmetrics(); im = Image.new("RGBA", (int(x) + stroke * 2 + 8, asc + desc + stroke * 2 + 8), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    for ch, cx in zip(s, xs): dr.text((cx + stroke + 4, stroke + 4), ch, font=f, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
    for ch, cx in zip(s, xs): dr.text((cx + stroke + 4, stroke + 4), ch, font=f, fill=tuple(color))
    return im.crop(im.getbbox())

def caption(canvas, s, size=66):
    """the channel caption: Rubik Bold, white, lowercase, 1-3 words; black outline now that we sit on real images"""
    place(canvas, outlined(s.lower(), size, WHITE, stroke=max(5, size // 11)), W / 2, CAP_Y); return canvas

# ---------------------------------------------------------------- images
def place(c, spr, x, y, anchor="c"):
    if anchor == "c": x, y = x - spr.width / 2, y - spr.height / 2
    elif anchor == "lt": pass
    elif anchor == "lc": y -= spr.height / 2
    c.alpha_composite(spr, (int(round(x)), int(round(y)))); return c

@functools.lru_cache(maxsize=16)
def _sticker_base(path, height, border):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.getbbox())
    im = im.resize((max(1, int(im.width * height / im.height)), height), Image.LANCZOS)
    pad = border + 12; base = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    base.alpha_composite(im, (pad, pad))
    a = base.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    for _ in range(max(1, border // 2)): a = a.filter(ImageFilter.MaxFilter(5))
    a = a.filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(0.7))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 120)); sh.putalpha(a.point(lambda v: v * 110 // 255))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2.5)), (0, 0))
    out = out.transform(out.size, Image.AFFINE, (1, 0, -5, 0, 1, -8))      # shadow nudged down-right
    wh = Image.new("RGBA", base.size, (255, 255, 255, 255)); wh.putalpha(a)
    out.alpha_composite(wh); out.alpha_composite(base); return out

def sticker(path, height, border=12, rot=6, scale=1.0):
    """cut-out with a white sticker edge and a small hard shadow (meme-editor vocabulary, not a UI card)"""
    s = _sticker_base(path, height, border)
    if scale != 1.0: s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.LANCZOS)
    return s.rotate(rot, Image.BICUBIC, expand=True)

POP = [0.0, 0.55, 1.14, 1.05, 0.98, 1.0]        # sticker scale per frame after it lands (snappy, no ease-in-out)
def pop(frames_since): return POP[frames_since] if 0 <= frames_since < len(POP) else (0.0 if frames_since < 0 else 1.0)

def fill(img, focus=(0.5, 0.5), zoom=1.0):
    """crop a photo to 16:9 around a focus point (0..1) and scale to the frame"""
    img = img.convert("RGB"); iw, ih = img.size; ar = W / H
    cw, ch = (iw, iw / ar) if iw / ih < ar else (ih * ar, ih); cw /= zoom; ch /= zoom
    cx = min(max(focus[0] * iw, cw / 2), iw - cw / 2); cy = min(max(focus[1] * ih, ch / 2), ih - ch / 2)
    return img.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.LANCZOS).convert("RGBA")

def night(img, amt=0.55):
    """night grade: shadows sink into brand navy, highlights stay natural, a little cooler overall"""
    a = np.asarray(img.convert("RGB"), np.float32) / 255; lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    w = ((1 - lum) ** 2 * amt)[..., None]; navy = np.array(NAVY, np.float32) / 255
    out = a * (1 - w) + navy * w * 1.6; out *= np.array([0.94, 0.97, 1.05], np.float32)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGB").convert("RGBA")

_vig = {}
def vignette(canvas, amt=0.38):
    """edges sink toward navy. Precomputed as one RGBA overlay (out = a*v + navy/2*(1-v)), composited in C: fast."""
    if amt not in _vig:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        v = np.clip(1 - amt * np.clip(d - 0.55, 0, 1) / 0.45, 0, 1)
        ov = np.zeros((H, W, 4), np.uint8); ov[..., :3] = (np.array(NAVY) * 0.5).astype(np.uint8); ov[..., 3] = ((1 - v) * 255).astype(np.uint8)
        _vig[amt] = Image.fromarray(ov, "RGBA")
    out = canvas.copy(); out.alpha_composite(_vig[amt]); return out

def page_view(page, c, s, angle=-1.4, marks=(), focus=(), dim=0.0):
    """a real screenshot filling the frame (cropped off the edges, slightly crooked, like it was pasted in).
    page = full-res screenshot, c = page point at frame centre, s = page px -> frame px.
    marks = [(box_in_page_px, progress, seed)] highlighter swipes drawn ON the page (they rotate with it).
    focus = page boxes that stay bright while the rest of the page sinks back (dim 0..1), documentary style.
    returns (frame, to_frame(x, y)) so marker strokes can be drawn on top in frame px."""
    cw, ch = W / s * 1.12, H / s * 1.12
    ix0, iy0 = int(round(c[0] - cw / 2)), int(round(c[1] - ch / 2)); ix1, iy1 = int(round(c[0] + cw / 2)), int(round(c[1] + ch / 2))
    crop = Image.new("RGBA", (ix1 - ix0, iy1 - iy0), (255, 255, 255, 255)); crop.alpha_composite(page.crop((ix0, iy0, ix1, iy1)).convert("RGBA"))
    if focus and dim > 0:
        m = Image.new("L", crop.size, 0); dm = ImageDraw.Draw(m)
        for b in focus: dm.rounded_rectangle((b[0] - ix0 - 40, b[1] - iy0 - 26, b[2] - ix0 + 40, b[3] - iy0 + 26), 20, fill=255)
        m = m.filter(ImageFilter.GaussianBlur(22))
        a = np.asarray(crop, np.float32); k = (np.asarray(m, np.float32) / 255)[..., None]
        sunk = a[..., :3] * (1 - 0.76 * dim) + np.array(NAVY, np.float32) * 0.18 * dim
        a[..., :3] = a[..., :3] * k + sunk * (1 - k); crop = Image.fromarray(a.astype(np.uint8), "RGBA")
    for box, prog, seed in marks:
        highlight(crop, (box[0] - ix0, box[1] - iy0, box[2] - ix0, box[3] - iy0), prog, seed)
    # one affine resample, page crop -> frame (scale + tilt + crop together; ~3x faster than resize-then-rotate)
    th = math.radians(angle); co, si = math.cos(th), math.sin(th); cx, cy = c
    data = (co / s, -si / s, cx - ix0 - (co * W / 2 - si * H / 2) / s,
            si / s, co / s, cy - iy0 - (si * W / 2 + co * H / 2) / s)
    frame = crop.transform((W, H), Image.AFFINE, data, resample=Image.BICUBIC, fillcolor=(255, 255, 255, 255))
    def to_frame(px, py):
        dx, dy = (px - cx) * s, (py - cy) * s
        return W / 2 + dx * co + dy * si, H / 2 - dx * si + dy * co
    return frame, to_frame

def box_to_frame(box, to_frame):
    pts = [to_frame(x, y) for x, y in ((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]))]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)

def shake(canvas, k, amp=14, seed=0):
    """impact shake: k = frames since hit (0..3)"""
    if not 0 <= k < 4: return canvas
    r = np.random.default_rng(seed + k); a = amp * (1 - k / 4)
    dx, dy = int(r.uniform(-a, a)), int(r.uniform(-a, a))
    out = Image.new("RGBA", canvas.size, (0, 0, 0, 255)); out.alpha_composite(canvas.resize((W + 40, H + 22)), (dx - 20, dy - 11))
    return out

def swipe_band(w, h, color=YEL, seed=0, progress=1.0):
    """an opaque highlighter swipe for DARK backgrounds (multiply needs light paper): ragged ends, felt-tip streaks"""
    r = np.random.default_rng(seed); n = 30; xe = w * progress
    im = Image.new("RGBA", (int(w + h), int(h * 1.3)), (0, 0, 0, 0))
    if xe < 4: return im
    xs = np.linspace(h * 0.15, xe, n); y0, y1 = h * 0.15, h * 1.15
    top = y0 + _noise(n, seed, h * 0.04) + np.linspace(0, -h * 0.05, n); bot = y1 + _noise(n, seed + 5, h * 0.04) + np.linspace(0, -h * 0.05, n)
    poly = list(zip(xs, top)) + [(xe + h * 0.12, (top[-1] + bot[-1]) / 2)] + list(zip(xs[::-1], bot[::-1])) + [(h * 0.05, (top[0] + bot[0]) / 2)]
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255); m = m.filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(m, np.float32) * (0.9 + _noise(im.size[1], seed + 2, 0.08, freqs=(3, 6, 11)))[:, None]
    col = Image.new("RGBA", im.size, tuple(color) + (255,)); col.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "L"))
    return col
