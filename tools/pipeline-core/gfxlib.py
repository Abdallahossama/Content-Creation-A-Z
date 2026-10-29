"""Tiny PIL motion-graphics engine for the Ask Habibi edit (1920x1080 @30fps -> H.264)."""
import math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
FONT = "C:/Users/ossam/AppData/Local/CapCut/User Data/Cache/effect/7148699606082130433/9b03aa8db4f8d431e15f1660108d512b/Rubik-Bold.ttf"
B = "D:/why habibi/"
PK = B + "WhyHabibi_Pack1_characters_rig_brand (1)/"
OUT = B + "1st video/claude_gfx/"

NAVY = (11, 16, 80); BLUE = (30, 42, 138); BLUE2 = (39, 52, 161); YEL = (255, 194, 26)
RED = (240, 64, 47); RED2 = (255, 90, 78); GRN = (60, 196, 124); SKY = (124, 200, 255)
WHITE = (255, 255, 255); CREAM = (255, 246, 224); GREY = (145, 151, 198); DARK = (16, 13, 14)
PURP = (185, 166, 245)


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def prog(t, t0, d):
    return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)

def ease_out_cubic(x):
    return 1 - (1 - x) ** 3

def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

def ease_out_back(x, s=1.70158):
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2

def pop(t, t0, d=0.38):
    """0 before t0, overshoots to ~1.1 then settles to 1."""
    if t < t0:
        return 0.0
    return ease_out_back(prog(t, t0, d))

def slide(t, t0, d=0.45):
    return ease_out_cubic(prog(t, t0, d))

def lerp(a, b, x):
    return a + (b - a) * x

def lerp_col(c1, c2, x):
    return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))


@functools.lru_cache(maxsize=64)
def font(size):
    return ImageFont.truetype(FONT, size)


@functools.lru_cache(maxsize=512)
def text(txt, size, fill=WHITE, stroke=0, stroke_fill=NAVY, shadow=0, spacing=8, align="center"):
    f = font(size)
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = d.multiline_textbbox((0, 0), txt, font=f, stroke_width=stroke, spacing=spacing, align=align)
    pad = stroke + 6 + shadow
    w, h = int(math.ceil(bb[2] - bb[0])) + pad * 2, int(math.ceil(bb[3] - bb[1])) + pad * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if shadow:
        dr.multiline_text((pad - bb[0], pad - bb[1] + shadow), txt, font=f, fill=NAVY + (255,),
                          stroke_width=stroke, stroke_fill=NAVY, spacing=spacing, align=align)
    dr.multiline_text((pad - bb[0], pad - bb[1]), txt, font=f, fill=fill, stroke_width=stroke,
                      stroke_fill=stroke_fill, spacing=spacing, align=align)
    return im


@functools.lru_cache(maxsize=256)
def panel(w, h, r=36, fill=WHITE, outline=NAVY, ow=8, shadow=14):
    im = Image.new("RGBA", (w + shadow + 4, h + shadow + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        d.rounded_rectangle((2, 2 + shadow, w + 1, h + 1 + shadow), r, fill=NAVY + (200,))
    d.rounded_rectangle((2, 2, w + 1, h + 1), r, fill=fill, outline=outline, width=ow)
    return im


@functools.lru_cache(maxsize=256)
def pill(txt, size, fill=YEL, tc=NAVY, padx=None, pady=None, ow=6, shadow=8):
    t = text(txt, size, tc)
    padx = padx if padx is not None else int(size * 0.7)
    pady = pady if pady is not None else int(size * 0.32)
    w, h = t.width + padx * 2, t.height + pady * 2
    p = panel(w, h, r=h // 2, fill=fill, outline=NAVY, ow=ow, shadow=shadow).copy()
    p.alpha_composite(t, (2 + padx, 2 + pady))
    return p


@functools.lru_cache(maxsize=128)
def load(path, height=None, width=None, flip=False):
    im = Image.open(path).convert("RGBA")
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    if height:
        im = im.resize((max(1, int(im.width * height / im.height)), int(height)), Image.LANCZOS)
    elif width:
        im = im.resize((int(width), max(1, int(im.height * width / im.width))), Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


def char(name, mood, height, outfit="01_Characters_Plain", flip=False):
    return load(f"{PK}{outfit}/{name}/{name}_{mood}.png", height=height, flip=flip)

def pose(name, p, height, flip=False):
    return load(f"{PK}03_Poses/{name}/{name}_pose_{p}.png", height=height, flip=flip)


def place(canvas, spr, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if spr is None or alpha <= 0.003 or scale <= 0.01:
        return
    s = spr
    if abs(scale - 1.0) > 1e-3:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BILINEAR)
    if abs(rot) > 0.05:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = s.getchannel("A").point(lambda v: int(v * alpha))
        s = s.copy(); s.putalpha(a)
    x, y = int(round(cx - s.width / 2)), int(round(cy - s.height / 2))
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(s.width, W - x), min(s.height, H - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    if sx0 or sy0 or sx1 < s.width or sy1 < s.height:
        s = s.crop((sx0, sy0, sx1, sy1))
    canvas.alpha_composite(s, (x + sx0, y + sy0))


def place_tl(canvas, spr, x, y, scale=1.0, alpha=1.0):
    """place by left edge / vertical center"""
    place(canvas, spr, x + spr.width * scale / 2, y, scale, alpha)


# ---------- backgrounds ----------
# "Midnight questions" animated background. bg_at(tg) is a pure function of TIMELINE time, so the
# standalone background clip and every graphic that bakes it in line up seamlessly at the cuts.
_mid = {}

def _midnight_static():
    if "base" in _mid:
        return
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = (yy / H)[..., None]
    top = np.array([17, 21, 66], np.float32); bot = np.array([6, 8, 28], np.float32)
    base = top * (1 - g) + bot * g
    dist = np.sqrt(((xx - W / 2) / (W * 0.55)) ** 2 + ((yy - H * 0.42) / (H * 0.62)) ** 2)
    glow = (np.clip(1 - dist, 0, 1) ** 1.8)[..., None]
    base = base * (1 - glow * 0.45) + np.array([34, 46, 150], np.float32) * glow * 0.45
    vd = np.sqrt(((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2)
    base *= np.clip(1 - 0.55 * np.clip(vd - 0.45, 0, 1) ** 1.4, 0, 1)[..., None]
    _mid["arr"] = base
    _mid["base"] = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    rng = np.random.default_rng(3)
    # soft drifting glows
    blobs = []
    for col, size, a in [((60, 80, 210), 900, 0.30), ((110, 70, 200), 760, 0.24), ((40, 120, 200), 680, 0.20)]:
        r = size / 2; y2, x2 = np.mgrid[0:size, 0:size].astype(np.float32)
        d2 = ((x2 - r) ** 2 + (y2 - r) ** 2) / (r * r)
        al = (np.exp(-d2 * 3.2) * a * 255).astype(np.uint8)
        arr = np.zeros((size, size, 4), np.uint8); arr[..., :3] = col; arr[..., 3] = al
        blobs.append(dict(img=Image.fromarray(arr, "RGBA"), cx=rng.uniform(300, W - 300), cy=rng.uniform(200, H - 200),
                          ax=rng.uniform(250, 420), ay=rng.uniform(120, 220), px=rng.uniform(45, 70), py=rng.uniform(35, 60),
                          ph=rng.uniform(0, 6.28)))
    _mid["blobs"] = blobs
    # stars
    n = 170
    _mid["stars"] = dict(x=rng.uniform(0, W, n), y=rng.uniform(0, H * 0.95, n) ** 1.0, r=rng.choice([1.0, 1.4, 1.9, 2.6], n, p=[.45, .3, .17, .08]),
                         f=rng.uniform(0.08, 0.45, n), ph=rng.uniform(0, 6.28, n), a=rng.uniform(0.35, 0.95, n))
    # floating question marks / z's
    glyphs = []
    for k in range(16):
        ch = "?" if k % 3 else "z"
        size = int(rng.uniform(46, 120))
        spr = text(ch, size, (200, 215, 255))
        glyphs.append(dict(img=spr, x=rng.uniform(80, W - 80), y=rng.uniform(0, H + 200), v=rng.uniform(7, 16),
                           sw=rng.uniform(15, 40), sp=rng.uniform(5, 11), ph=rng.uniform(0, 6.28),
                           rs=rng.uniform(-6, 6), a=rng.uniform(0.05, 0.10)))
    _mid["glyphs"] = glyphs

def bg_at(tg):
    _midnight_static()
    im = _mid["base"].copy()
    for b in _mid["blobs"]:
        x = b["cx"] + b["ax"] * math.sin(2 * math.pi * tg / b["px"] + b["ph"])
        y = b["cy"] + b["ay"] * math.sin(2 * math.pi * tg / b["py"] + b["ph"] * 1.7)
        place(im, b["img"], x, y)
    s = _mid["stars"]; arr = _mid["arr"]
    tw = s["a"] * (0.55 + 0.45 * np.sin(2 * np.pi * s["f"] * tg + s["ph"]))
    d = ImageDraw.Draw(im)
    for x, y, r, a in zip(s["x"], s["y"], s["r"], tw):
        bc = arr[int(y), int(x)]
        col = tuple(int(c + (255 - c) * a) for c in bc) + (255,)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    span = H + 240
    for g in _mid["glyphs"]:
        y = (g["y"] - g["v"] * tg) % span - 120
        x = g["x"] + g["sw"] * math.sin(2 * math.pi * tg / g["sp"] + g["ph"])
        place(im, g["img"], x, y, 1.0, g["a"], rot=g["rs"] * math.sin(tg / 3 + g["ph"]))
    return im

def base_bg():
    return bg_at(0.0)

_ang = None
def sunburst(t, rays=22, speed=0.08, c1=BLUE2, c2=BLUE, cx=W / 2, cy=H / 2):
    global _ang
    if _ang is None:
        yy, xx = np.mgrid[0:H, 0:W]
        _ang = np.arctan2(yy - cy, xx - cx).astype(np.float32)
    seg = 2 * np.pi / rays
    m = ((_ang + speed * t) % seg) < seg / 2
    arr = np.empty((H, W, 4), np.uint8)
    arr[...] = c2 + (255,)
    arr[m] = c1 + (255,)
    return Image.fromarray(arr, "RGBA")


def circle_reveal(canvas, top, t, t0=0.0, d=0.45, cx=W / 2, cy=H / 2):
    x = ease_out_cubic(prog(t, t0, d))
    if x >= 1:
        canvas.alpha_composite(top); return
    if x <= 0:
        return
    r = x * math.hypot(W, H) / 2 + 2
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    canvas.paste(top, (0, 0), mask)


# ---------- icons ----------
def moon(r, col=YEL):
    s = int(r * 2 + 8)
    m = Image.new("L", (s, s), 0); d = ImageDraw.Draw(m)
    d.ellipse((4, 4, 4 + 2 * r, 4 + 2 * r), fill=255)
    cut = Image.new("L", (s, s), 0)
    ImageDraw.Draw(cut).ellipse((4 + r * 0.55, 4 - r * 0.35, 4 + r * 0.55 + 2 * r, 4 - r * 0.35 + 2 * r), fill=255)
    m = Image.fromarray(np.clip(np.array(m, np.int16) - np.array(cut, np.int16), 0, 255).astype(np.uint8))
    im = Image.new("RGBA", (s, s), col + (0,)); im.putalpha(m)
    return im

def star_pts(cx, cy, R, r, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        rad = R if i % 2 == 0 else r
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts

def star(R, fill=YEL, outline=NAVY):
    s = int(R * 2 + 16); im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon(star_pts(s / 2, s / 2 + 2, R, R * 0.45), fill=fill, outline=outline, width=6)
    return im

def check_icon(r, bg=GRN):
    s = int(r * 2 + 12); im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((6, 6, s - 6, s - 6), fill=bg, outline=NAVY, width=6)
    c = s / 2
    d.line([(c - r * 0.45, c + r * 0.02), (c - r * 0.1, c + r * 0.38), (c + r * 0.5, c - r * 0.35)], fill=WHITE, width=int(r * 0.22), joint="curve")
    return im

def num_badge(n, r=46, fill=YEL, tc=NAVY):
    s = int(r * 2 + 12); im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((6, 6, s - 6, s - 6), fill=fill, outline=NAVY, width=6)
    t = text(str(n), int(r * 1.15), tc); im.alpha_composite(t, (int(s / 2 - t.width / 2), int(s / 2 - t.height / 2)))
    return im

def cursor(size=70):
    im = Image.new("RGBA", (size, int(size * 1.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    p = [(4, 4), (4, size * 1.15), (size * 0.32, size * 0.88), (size * 0.55, size * 1.35), (size * 0.72, size * 1.27),
         (size * 0.5, size * 0.8), (size * 0.88, size * 0.8)]
    d.polygon(p, fill=WHITE, outline=NAVY, width=5)
    return im

def ripple(canvas, cx, cy, t, t0, d=0.45, r0=40, r1=170, col=WHITE):
    x = prog(t, t0, d)
    if 0 < x < 1:
        r = lerp(r0, r1, ease_out_cubic(x)); a = int(255 * (1 - x))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (a,), width=10)
        canvas.alpha_composite(ov)

def stamp(txt, size=120, col=RED2, rot=-10):
    t = text(txt, size, col)
    w, h = t.width + 60, t.height + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w - 6, h - 6), 18, outline=col, width=12)
    im.alpha_composite(t, (30, 20))
    return im.rotate(rot, resample=Image.BICUBIC, expand=True)


# ---------- renderer ----------
def render(name, dur, draw, tg0=0.0):
    """draw(canvas, t) paints onto an RGBA canvas that already has the background at timeline time tg0+t."""
    import os
    os.makedirs(OUT, exist_ok=True)
    n = int(round(dur * FPS)) + 3
    path = OUT + name + ".mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        c = bg_at(tg0 + t)
        draw(c, t)
        p.stdin.write(c.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    print("rendered", name, round(dur, 2), "s", n, "frames", flush=True)
    return path


def still(name, dur, draw, t, tg0=0.0):
    """Render one frame to PNG for QA."""
    c = bg_at(tg0 + t); draw(c, t)
    c.convert("RGB").save(f"qa_{name}_{t:.2f}.png")
