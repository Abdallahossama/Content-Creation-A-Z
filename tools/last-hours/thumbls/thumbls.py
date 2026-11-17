"""thumbls.py - The Last Hours thumbnails in the owner's ChatGPT reference style (17 Nov 2026). FREE, local.

Look (owner's refs "66 NAMES. ONE ORDER.", "NO WAY HOME", "HE DISAPPEARED", "THEY LEFT ONE WORD"):
  cinematic photoreal scene filling the frame (AI background from Z-Image, or a real archive photo)
  + the REAL person from an archive photo (MediaPipe cutout, B&W/sepia, big, one side)
  + story props (real archive print, red hand-drawn circle, case folder)
  + 2-4 huge distressed condensed words (Anton), line 2 on a torn red brush stroke or in one colour word
  + dark gritty grade, vignette, grain + small date block.
Rules: no women anywhere; faces of real people only from real photos; no fake records (props say FILE NN / CASE FILE).

Run with F:/thumbkit/venv/Scripts/python.exe (Pillow 13 + numpy + mediapipe 0.10.14).
  from thumbls import *
  c = Canvas(bg("scene.png", look="teal"))
  c.subject("mugshot.jpg", side="right", h=640, tone="bw")
  c.headline(["NEVER", "FOUND"], mode="brush")      # mode: brush | yellow | ice | red
  c.date("12 JUNE 1962"); c.save("out/alcatraz_A.jpg")
Backgrounds: python thumbls.py bg out.png "prompt" [seed]   (Z-Image Turbo, ~4 min on the Radeon 780M)
"""
import os, sys, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

W, H = 1280, 720
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = ["F:/thumbkit/fonts/Anton-Regular.ttf", os.path.join(HERE, "fonts/Anton-Regular.ttf"), "C:/Windows/Fonts/impact.ttf"]
RED, YELLOW, ICE, WHITE = (200, 22, 22), (255, 204, 0), (150, 220, 255), (245, 242, 235)


def font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    raise SystemExit("no font")


# ---------------------------------------------------------------- background
def ai_bg(prompt, out, seed=7):
    """Z-Image Turbo (stable-diffusion.cpp Vulkan) - F:/zimage. Men/places/objects only, never real faces."""
    sys.path.insert(0, "D:/the-bill-explained/tools")
    from zimage import gen
    return gen(prompt + ", cinematic still, photorealistic, gritty dark film grade, 35mm grain, no women", out, 1344, 768, seed=seed)


def cover(img, focus=(0.5, 0.5), zoom=1.0):
    s = max(W / img.width, H / img.height) * zoom
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = int((img.width - W) * focus[0]); y = int((img.height - H) * focus[1])
    return img.crop((x, y, x + W, y + H))


def grade(img, look="teal", sat=0.8, contrast=1.18, bright=0.92):
    """look: teal (night/sea), ice (arctic), warm (sunset/sepia-ish), red (blood/power), bw"""
    img = ImageEnhance.Color(img).enhance(0 if look == "bw" else sat)
    img = ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(bright)).enhance(contrast)
    a = np.asarray(img).astype(np.float32) / 255
    lum = a.mean(axis=2, keepdims=True)
    tints = {"teal": ((0.0, 0.10, 0.14), (0.10, 0.04, -0.04)), "ice": ((-0.02, 0.06, 0.16), (0.02, 0.06, 0.10)),
             "warm": ((0.06, 0.02, -0.04), (0.12, 0.05, -0.06)), "red": ((0.08, -0.02, -0.03), (0.10, 0.02, -0.04)),
             "bw": ((0, 0, 0), (0.04, 0.02, -0.01))}
    sh, hi = tints.get(look, tints["teal"])
    a = a + (1 - lum) * np.array(sh) * 0.6 + lum * np.array(hi) * 0.5
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def bg(path, look="teal", focus=(0.5, 0.5), zoom=1.0, mirror=False, **kw):
    im = Image.open(path).convert("RGB")
    if mirror: im = ImageOps.mirror(im)
    return grade(cover(im, focus, zoom), look, **kw)


def finish(img, vignette=0.55, grain=0.05, left_dark=0.55):
    a = np.asarray(img).astype(np.float32) / 255
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    v = 1 - vignette * np.clip(r - 0.45, 0, 1) ** 1.4
    side = 1 - left_dark * np.clip(1 - xx / (W * 0.55), 0, 1) ** 1.6   # dark left side for the text
    a = a * (v * side)[..., None]
    rng = np.random.default_rng(3)
    a = a + rng.normal(0, grain, (H, W, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


# ---------------------------------------------------------------- subject (real archive photo)
_seg = None


def cutout(path, crop=None, thresh=0.5, feather=3):
    """Person cutout from a REAL photo with MediaPipe selfie segmentation -> RGBA."""
    global _seg
    import mediapipe as mp
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    if _seg is None:
        _seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
    m = _seg.process(np.asarray(im)).segmentation_mask
    m = (np.clip((m - thresh) * 6 + 0.5, 0, 1) * 255).astype(np.uint8)
    mask = Image.fromarray(m).filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGBA"); out.putalpha(mask)
    return out.crop(mask.getbbox() or (0, 0, im.width, im.height))


def fade_card(path, crop=None, fade=0.35, side="right"):
    """No clean cutout possible (sketch, engraving): photo with a long feathered inner edge."""
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    w, h = im.size
    x = np.linspace(0, 1, w)
    ramp = np.clip(x / fade, 0, 1) if side == "right" else np.clip((1 - x) / fade, 0, 1)
    y = np.linspace(0, 1, h)
    vr = np.clip((1 - y) / 0.12, 0, 1) * np.clip(y / 0.06, 0, 1)
    a = (np.outer(vr, ramp) ** 1.3 * 255).astype(np.uint8)
    out = im.convert("RGBA"); out.putalpha(Image.fromarray(a))
    return out


def white_cut(path, crop=None, thr=232, feather=2):
    """Sketch/print on white paper: remove the white that touches the border (flood fill) -> RGBA."""
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    g = ImageOps.grayscale(im).point(lambda v: 255 if v >= thr else 0)
    g = g.copy()
    for xy in [(0, 0), (g.width - 1, 0), (0, g.height - 1), (g.width - 1, g.height - 1), (g.width // 2, 0)]:
        if g.getpixel(xy) == 255: ImageDraw.floodfill(g, xy, 128)
    a = g.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGBA"); out.putalpha(a)
    return out.crop(a.getbbox())


def tone(rgba, mode="bw", contrast=1.35, bright=0.88, tint=(0.96, 1.0, 1.04)):
    rgb = rgba.convert("RGB"); a = rgba.getchannel("A")
    if mode in ("bw", "sepia"):
        g = ImageOps.autocontrast(ImageOps.grayscale(rgb), cutoff=1)
        g = ImageEnhance.Contrast(g).enhance(contrast)
        rgb = ImageOps.colorize(g, (12, 10, 8), (240, 232, 215)) if mode == "sepia" else g.convert("RGB")
    elif mode == "colour":
        rgb = ImageEnhance.Contrast(ImageEnhance.Color(rgb).enhance(0.75)).enhance(1.15)
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    arr = np.asarray(rgb).astype(np.float32) * np.array(tint)
    # side light: darker on the far side, like the refs (face half in shadow)
    w = arr.shape[1]; ramp = np.linspace(0.62, 1.0, w)[None, :, None]
    rgb = Image.fromarray(np.clip(arr * ramp, 0, 255).astype(np.uint8))
    out = rgb.convert("RGBA"); out.putalpha(a)
    return out


def shadow_of(rgba, blur=18, alpha=200, grow=6):
    a = rgba.getchannel("A").filter(ImageFilter.MaxFilter(3) if grow else ImageFilter.BLUR)
    a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * alpha // 255)
    s = Image.new("RGBA", rgba.size, (0, 0, 0, 0)); s.putalpha(a)
    return s


# ---------------------------------------------------------------- lettering
def grunge(size, seed=1, amount=0.10):
    """alpha mask with worn specks/scratches (1 = keep)."""
    rng = np.random.default_rng(seed)
    w, h = size
    n = rng.random((h // 3 + 1, w // 3 + 1)).astype(np.float32)
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
                   .filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    fine = rng.random((h, w)).astype(np.float32)
    keep = (n > amount + 0.02) & (fine > amount * 0.35)
    scratch = Image.new("L", size, 255); d = ImageDraw.Draw(scratch)
    for _ in range(int(w * h / 9000)):
        x, y = rng.integers(0, w), rng.integers(0, h)
        d.line((x, y, x + rng.integers(-40, 40), y + rng.integers(-6, 6)), fill=0, width=int(rng.integers(1, 3)))
    return (keep * (np.asarray(scratch) > 0)).astype(np.float32)


def word_layer(text, size, fill=WHITE, seed=1, wear=0.10, track=0):
    f = font(size)
    bb = f.getbbox(text)
    w, h = bb[2] - bb[0] + 20 + track * len(text), bb[3] - bb[1] + 20
    mask = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mask)
    if track:
        x = 10
        for ch in text:
            d.text((x - bb[0], 10 - bb[1]), ch, font=f, fill=255); x += f.getlength(ch) + track
    else:
        d.text((10 - bb[0], 10 - bb[1]), text, font=f, fill=255)
    m = np.asarray(mask).astype(np.float32) / 255 * grunge((w, h), seed, wear)
    lay = Image.new("RGBA", (w, h), fill + (0,)); lay.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
    if fill == ICE:   # icy: vertical gradient + crack lines
        g = np.linspace(1.0, 0.72, h)[:, None, None] * np.array([235, 250, 255]) + np.linspace(0, 1, h)[:, None, None] * np.array([0, 0, 0])
        rgb = np.broadcast_to(g, (h, w, 3)).astype(np.uint8)
        a = lay.getchannel("A"); lay = Image.fromarray(rgb).convert("RGBA"); lay.putalpha(a)
        d2 = ImageDraw.Draw(lay); rng = random.Random(seed)
        for _ in range(len(text) * 3):
            x, y = rng.randint(0, w), rng.randint(0, h)
            pts = [(x, y)]
            for _ in range(4): x += rng.randint(-25, 25); y += rng.randint(-18, 18); pts.append((x, y))
            d2.line(pts, fill=(60, 120, 170, 0), width=2)
        lay.putalpha(Image.fromarray((np.asarray(lay.getchannel("A")) * (np.asarray(a) > 0)).astype(np.uint8)))
    return lay


def brush_stroke(w, h, color=RED, seed=4):
    """torn dry-brush paint stroke (RGBA)."""
    rng = np.random.default_rng(seed)
    def walk(n, s):
        v = np.cumsum(rng.normal(0, s, n)); v -= np.linspace(v[0], v[-1], n); return v
    top = h * 0.10 + walk(w, 1.6) + rng.normal(0, 1.5, w)
    bot = h * 0.90 + walk(w, 1.6) + rng.normal(0, 1.5, w)
    yy = np.arange(h)[:, None]
    a = ((yy > top[None, :]) & (yy < bot[None, :])).astype(np.float32)
    xs = np.arange(w)[None, :]
    lend = w * 0.03 + np.abs(walk(h, 3))[:, None] + rng.random((h, 1)) * 18
    rend = w * 0.97 - np.abs(walk(h, 3))[:, None] - rng.random((h, 1)) * 30
    a *= (xs > lend) & (xs < rend)
    streak = np.clip(rng.normal(1, 0.25, (h, 1)), 0.55, 1)                  # dry-brush rows
    a *= np.where(rng.random((h, w)) > 0.985, 0.2, 1) * streak
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)))
    tex = 1 - 0.18 * rng.random((h, w, 1))
    rgb = (np.array(color)[None, None, :] * tex).astype(np.uint8)
    out = Image.fromarray(rgb).convert("RGBA"); out.putalpha(Image.fromarray(a))
    return out


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, base):
        self.img = base.convert("RGBA")
        self.base_done = False

    def paste(self, lay, xy, shadow=True, blur=16, alpha=190, off=(8, 12)):
        if shadow:
            s = shadow_of(lay, blur, alpha)
            self._safe(s, (xy[0] + off[0], xy[1] + off[1]))
        self._safe(lay, xy)

    def _safe(self, lay, xy):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0)); layer.paste(lay, xy, lay)
        self.img = Image.alpha_composite(self.img, layer)

    def grade_finish(self, **kw):
        self.img = finish(self.img.convert("RGB"), **kw).convert("RGBA")

    def subject(self, rgba, side="right", h=650, x=None, y=None, rim=True, bottom_fade=0.18):
        s = rgba.resize((round(rgba.width * h / rgba.height), h), Image.LANCZOS)
        if bottom_fade:
            yy = np.linspace(0, 1, s.height)[:, None]
            f = np.clip((1 - yy) / bottom_fade, 0, 1) ** 1.2
            s.putalpha(Image.fromarray((np.asarray(s.getchannel("A")) * f).astype(np.uint8)))
        if x is None: x = W - s.width + 30 if side == "right" else -30
        if y is None: y = H - h + 10
        if rim:   # thin cold rim light behind the subject so it separates from a dark scene
            a = s.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 110 // 255)
            glow = Image.new("RGBA", s.size, (200, 220, 235, 0)); glow.putalpha(a)
            self._safe(glow, (x, y))
        self.paste(s, (x, y), blur=24, alpha=170, off=(-14, 10))
        return (x, y, x + s.width, y + s.height)

    def print_photo(self, path, xy, w=360, angle=-6, crop=None, mode="sepia", border=14):
        im = Image.open(path).convert("RGB")
        if crop: im = im.crop(crop)
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        if mode == "sepia":
            im = ImageOps.colorize(ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.3), (25, 18, 10), (238, 225, 198))
        card = Image.new("RGBA", (im.width + 2 * border, im.height + 2 * border), (232, 226, 210, 255))
        card.paste(im, (border, border))
        card = card.rotate(angle, resample=Image.BICUBIC, expand=True)
        self.paste(card, xy, blur=14, alpha=200)
        return card.size

    def circle(self, box, color=RED, width=9, turns=1.15, seed=2):
        """hand-drawn red ring around a clue."""
        rng = random.Random(seed)
        x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        pts = []
        n = 120
        for i in range(int(n * turns)):
            t = 2 * np.pi * i / n - 0.6
            k = 1 + 0.05 * np.sin(i / 9) + rng.uniform(-0.01, 0.01) + 0.06 * i / n
            pts.append((cx + rx * k * np.cos(t), cy + ry * k * np.sin(t)))
        lay = Image.new("RGBA", self.img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.line(pts, fill=color + (255,), width=width, joint="curve")
        self.img = Image.alpha_composite(self.img, Image.alpha_composite(shadow_of(lay, 6, 160, 0), lay))

    def arrow(self, p0, p1, color=RED, width=14):
        lay = Image.new("RGBA", self.img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.line([p0, p1], fill=color + (255,), width=width)
        ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0]); L = width * 3.2
        for s in (0.5, -0.5):
            d.line([p1, (p1[0] - L * np.cos(ang + s), p1[1] - L * np.sin(ang + s))], fill=color + (255,), width=width)
        self.img = Image.alpha_composite(self.img, Image.alpha_composite(shadow_of(lay, 6, 160, 0), lay))

    def folder(self, xy, label="FILE 01", stamp="CASE FILE", w=330, angle=8):
        """manila case-file folder prop (channel brand, not a fake record)."""
        h = int(w * 0.72)
        f = Image.new("RGBA", (w, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(f)
        d.rounded_rectangle((0, 0, w * 0.4, 60), 10, fill=(196, 160, 98, 255))
        d.rectangle((0, 34, w, h + 34), fill=(205, 170, 108, 255))
        d.text((24, 60), label, font=font(int(w * 0.12)), fill=(60, 40, 20, 255))
        st = word_layer(stamp, int(w * 0.16), fill=RED, seed=9, wear=0.25).rotate(-12, expand=True, resample=Image.BICUBIC)
        f.alpha_composite(st, (int(w * 0.12), int(h * 0.45)))
        tex = (np.random.default_rng(5).random((h + 40, w)) * 30).astype(np.uint8)
        a = np.asarray(f).copy(); a[..., :3] = np.clip(a[..., :3].astype(int) - tex[..., None], 0, 255); f = Image.fromarray(a)
        self.paste(f.rotate(angle, expand=True, resample=Image.BICUBIC), xy, blur=14, alpha=210)

    def headline(self, lines, mode="brush", x=50, y=None, maxw=640, sizes=(170, 150), seed=1, gap=6, colors=None):
        """lines: 1-3 short lines. mode: brush (last line white on red brush) | yellow | ice | red (last line in colour)."""
        lays = []
        for i, t in enumerate(lines):
            last = i == len(lines) - 1 and len(lines) > 1
            col = (colors[i] if colors else None) or ({"yellow": YELLOW, "ice": ICE, "red": RED}.get(mode) if last else WHITE) or WHITE
            size = sizes[min(i, len(sizes) - 1)]
            lay = word_layer(t, size, col, seed + i)
            while lay.width > maxw and size > 60:
                size -= 6; lay = word_layer(t, size, col, seed + i)
            lays.append((lay, last and mode == "brush"))
        total = sum(l.height for l, _ in lays) + gap * (len(lays) - 1) + (30 if lays[-1][1] else 0)
        cy = y if y is not None else (H - total) // 2 - 20
        for lay, on_brush in lays:
            if on_brush:
                br = brush_stroke(lay.width + 70, lay.height + 46, RED, seed + 7)
                self.paste(br, (x - 30, cy - 10), blur=10, alpha=170, off=(6, 8))
                self.paste(lay, (x + 5, cy + 13), blur=6, alpha=200, off=(4, 5))
                cy += lay.height + 30 + gap
            else:
                outline = shadow_of(lay, 2, 255, 1)
                self._safe(outline, (x + 3, cy + 3))
                self.paste(lay, (x, cy), blur=12, alpha=230, off=(7, 9))
                cy += lay.height + gap
        return cy

    def bark_patch(self, center, size, seed=8):
        """pale stripped-bark area (where letters were cut), ragged edge."""
        w, h = size; rng = np.random.default_rng(seed)
        m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
        pts = [(w / 2 + (w / 2 - 8) * np.cos(t) * rng.uniform(0.9, 1.0), h / 2 + (h / 2 - 8) * np.sin(t) * rng.uniform(0.85, 1.0))
               for t in np.linspace(0, 2 * np.pi, 60)]
        d.polygon(pts, fill=245); m = m.filter(ImageFilter.GaussianBlur(5))
        grain = (rng.random((h, w)) * 40).astype(np.float32)
        streak = np.repeat(rng.normal(0, 14, (1, w)), h, axis=0)
        base = np.stack([214 - grain + streak, 178 - grain + streak, 126 - grain + streak], 2)
        lay = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA"); lay.putalpha(m)
        self._safe(lay, (center[0] - w // 2, center[1] - h // 2))

    def carve(self, text, center, size=120, angle=-3, seed=5):
        """letters cut into wood/bark: dark groove + light lower lip."""
        lay = word_layer(text, size, (20, 11, 5), seed, wear=0.10)
        a = lay.getchannel("A")
        lip = Image.new("RGBA", lay.size, (235, 210, 170, 0)); lip.putalpha(a.point(lambda v: v * 230 // 255))
        grp = Image.new("RGBA", (lay.width + 6, lay.height + 6), (0, 0, 0, 0))
        grp.alpha_composite(lip, (3, 4)); grp.alpha_composite(lay, (0, 0))
        grp = grp.rotate(angle, expand=True, resample=Image.BICUBIC)
        self._safe(grp, (center[0] - grp.width // 2, center[1] - grp.height // 2))

    def date(self, text, xy=(56, 610), color=YELLOW, ink=(15, 12, 10), size=46):
        lay = word_layer(text, size, ink, seed=11, wear=0.04, track=2)
        box = Image.new("RGBA", (lay.width + 26, lay.height + 6), color + (255,))
        box.alpha_composite(lay, (13, 3))
        self.paste(box.rotate(1.5, expand=True, resample=Image.BICUBIC), xy, blur=8, alpha=180)

    def save(self, out, sheet_small=True):
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        rgb = self.img.convert("RGB")
        q = 92
        while True:
            rgb.save(out, "JPEG", quality=q, optimize=True, progressive=True)
            if os.path.getsize(out) < 1_900_000 or q < 60: break
            q -= 6
        if sheet_small:
            rgb.resize((320, 180), Image.LANCZOS).save(out.replace(".jpg", "_320.jpg"), quality=90)
        print(out, f"{os.path.getsize(out) / 1e6:.2f} MB")
        return out


def sheet(rows, out, cell=(480, 270), labels=True):
    """rows: [(row_title, [(label, path), ...]), ...] -> review sheet with a 320x180 phone strip under each row."""
    pad, th = 16, 34
    ncol = max(len(r[1]) for r in rows)
    rw = pad + ncol * (cell[0] + pad)
    rh = th + cell[1] + pad + 180 + pad + 20
    S = Image.new("RGB", (rw, pad + len(rows) * rh), (18, 18, 20)); d = ImageDraw.Draw(S)
    f, fs = font(26), font(18)
    for r, (title, items) in enumerate(rows):
        y0 = pad + r * rh
        d.text((pad, y0), title, font=f, fill=(240, 240, 240))
        for c, (lab, p) in enumerate(items):
            x = pad + c * (cell[0] + pad)
            im = Image.open(p).convert("RGB")
            S.paste(im.resize(cell, Image.LANCZOS), (x, y0 + th))
            S.paste(im.resize((320, 180), Image.LANCZOS), (x, y0 + th + cell[1] + pad))
            d.text((x + 330, y0 + th + cell[1] + pad + 4), lab, font=fs, fill=(255, 204, 0) if lab != "CURRENT" else (170, 170, 170))
            d.text((x + 330, y0 + th + cell[1] + pad + 30), "phone size", font=fs, fill=(120, 120, 120))
    S.save(out, quality=88)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "bg":
        ai_bg(sys.argv[3], sys.argv[2], int(sys.argv[4]) if len(sys.argv) > 4 else 7)
