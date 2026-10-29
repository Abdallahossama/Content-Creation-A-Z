"""Doc mode (Ask Habibi documentaries): the serious sibling of Cut & Marker. Same brand colours and fonts, no memes.
Screen-space overlays for the beat engine (each has t_in / t_out / on(tl) / draw(c, tl)):
  ChapterCard  full-frame dim + big yellow hand number + Rubik title + marker underline (fades in and out)
  LowerThird   a dated fact, bottom-left ABOVE the caption band: Rubik line on a yellow highlighter swipe + hand sub-line
  PullQuote    a sourced quote: big marker quote marks, Rubik text, hand attribution, soft dark scrim (no boxes)
  Counter      a number that rolls up to its value, Rubik, with a hand label
  SourceTag    small hand source line top-left
  Stamp        a dated "as of" stamp
Plus grade(img) for photos (cooler, a touch desaturated) and TitleCard (a beat background)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
import marker as MK

W, H = 1920, 1080
WHITE, YEL, RED, NAVY, INK = (255, 255, 255), (255, 194, 26), (240, 64, 47), (11, 16, 80), (8, 12, 30)
_f = {}
def rubik(size):
    if size not in _f: _f[size] = ImageFont.truetype(MK.RUBIK, size)
    return _f[size]
def smooth(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)

class DOv:
    t_out = None
    def on(self, tl): return tl >= self.t_in - 1e-6 and (self.t_out is None or tl < self.t_out)
    def fade(self, tl, fin=0.35, fout=0.35):
        a = smooth((tl - self.t_in) / fin) if fin else 1.0
        if self.t_out is not None and fout: a = min(a, smooth((self.t_out - tl) / fout))
        return a

def _alpha(img, a):
    if a >= 0.999: return img
    img = img.copy(); img.putalpha(img.split()[3].point(lambda v: int(v * a))); return img

def text_img(s, size, color=WHITE, stroke=0, stroke_fill=INK):
    f = rubik(size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = d.multiline_textbbox((0, 0), s, font=f, stroke_width=stroke, spacing=int(size * 0.18))
    im = Image.new("RGBA", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).multiline_text((4 - bb[0], 4 - bb[1]), s, font=f, fill=color + (255,), stroke_width=stroke,
                                      stroke_fill=stroke_fill + (255,), spacing=int(size * 0.18))
    return im

def scrim(c, box, a=170, blur=40):
    """a soft dark patch behind text (not a card: no edges)"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle(box, 30, fill=INK + (a,))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

class ChapterCard(DOv):
    """a chapter break over whatever is behind (usually the moving map): dims it, writes the number and the title"""
    def __init__(self, n, title, t_in, t_out):
        self.n, self.title, self.t_in, self.t_out = str(n), title, t_in, t_out
        self.num = MK.hand(self.n, 230, YEL, rot=-4); self.tit = text_img(title, 96, WHITE)
    def draw(self, c, tl):
        a = self.fade(tl, 0.45, 0.45)
        dim = Image.new("RGBA", (W, H), INK + (int(185 * a),)); c.alpha_composite(dim)
        u = smooth((tl - self.t_in - 0.15) / 0.5)
        x = 300; y = H / 2 - 40
        MK.place(c, _alpha(self.num, a), x + 70, y, "c")
        MK.place(c, _alpha(self.tit, a), x + 200 + (1 - u) * 40, y - self.tit.height / 2, "lt")
        if u > 0.05:
            MK.strokes(c, [MK.underline_path(x + 200, x + 200 + self.tit.width, y + self.tit.height / 2 + 26, seed=4, flick=False)],
                       YEL, 9, min(1.0, u) * a, seed=4)

class LowerThird(DOv):
    """a dated fact, bottom-left, above the caption band (bottom edge <= 800)"""
    def __init__(self, main, t_in, sub=None, t_out=None, x=90, y=690, size=48):
        self.main, self.sub, self.t_in, self.t_out, self.x, self.y = main, sub, t_in, t_out, x, y
        self.mi = text_img(main, size, INK); self.si = MK.hand(sub, 36, WHITE, rot=0) if sub else None
    def draw(self, c, tl):
        a = self.fade(tl, 0.3, 0.3); u = smooth((tl - self.t_in) / 0.45)
        w, h = self.mi.width + 40, self.mi.height + 18
        sw_ = max(w, (self.si.width + 20) if self.si is not None else 0)
        scrim(c, (self.x - 50, self.y - 40, self.x + sw_ + 40, self.y + h + (self.si.height + 30 if self.si is not None else 20)), int(150 * a), 24)
        band = MK.swipe_band(w, h, YEL, seed=7, progress=u)
        MK.place(c, _alpha(band, a), self.x - 20, self.y - 9, "lt")
        if u > 0.3: MK.place(c, _alpha(self.mi, a * smooth((u - 0.3) / 0.4)), self.x, self.y, "lt")
        if self.si is not None and u > 0.6:
            sh = Image.new("RGBA", (self.si.width + 30, self.si.height + 20), (0, 0, 0, 0))
            MK.place(c, _alpha(self.si, a), self.x + 4, self.y + h + 4, "lt")

class PullQuote(DOv):
    """a sourced quote in the middle of the frame (above captions)"""
    def __init__(self, quote, who, t_in, t_out=None, width=1300, size=58, y=380):
        self.t_in, self.t_out, self.y = t_in, t_out, y
        words, lines, cur = quote.split(), [], ""
        for w_ in words:
            test = (cur + " " + w_).strip()
            if rubik(size).getlength(test) > width and cur: lines.append(cur); cur = w_
            else: cur = test
        lines.append(cur)
        self.q = text_img("\n".join(lines), size, WHITE); self.who = MK.hand(who, 38, YEL, rot=-1)
        self.mark = MK.hand("“", 260, YEL, rot=0)
    def draw(self, c, tl):
        a = self.fade(tl, 0.4, 0.4); x0 = (W - self.q.width) / 2
        scrim(c, (x0 - 120, self.y - 140, x0 + self.q.width + 120, self.y + self.q.height + self.who.height + 120), int(190 * a))
        MK.place(c, _alpha(self.mark, a), x0 - 90, self.y - 60, "c")
        MK.place(c, _alpha(self.q, a), x0, self.y, "lt")
        MK.place(c, _alpha(self.who, a), x0 + self.q.width - self.who.width, self.y + self.q.height + 24, "lt")

class Counter(DOv):
    """a number rolling up to its value (fmt like '{:,.0f}'), with a hand label under it"""
    def __init__(self, value, t_in, label="", fmt="{:,.0f}", t_out=None, x=W / 2, y=360, size=170, dur=1.4, color=WHITE, start=0.0):
        self.v, self.t_in, self.label, self.fmt, self.t_out, self.x, self.y, self.size, self.dur, self.color, self.start = value, t_in, label, fmt, t_out, x, y, size, dur, color, start
        self.li = MK.hand(label, 46, YEL, rot=-1) if label else None
    def draw(self, c, tl):
        a = self.fade(tl, 0.25, 0.35); u = smooth((tl - self.t_in) / self.dur)
        val = self.start + (self.v - self.start) * (1 - (1 - u) ** 3)
        ti = text_img(self.fmt.format(val), self.size, self.color, stroke=6)
        lw = self.li.width if self.li is not None else 0; bw = max(ti.width, lw) / 2 + 60
        scrim(c, (self.x - bw, self.y - ti.height / 2 - 40, self.x + bw, self.y + ti.height / 2 + (110 if self.li is not None else 40)), int(140 * a), 30)
        MK.place(c, _alpha(ti, a), self.x, self.y, "c")
        if self.li is not None: MK.place(c, _alpha(self.li, a), self.x, self.y + ti.height / 2 + 50, "c")

class SourceTag(DOv):
    def __init__(self, text, t_in, t_out=None, x=70, y=60):
        self.t_in, self.t_out, self.x, self.y = t_in, t_out, x, y; self.im = MK.hand(text, 38, WHITE, rot=-1)
    def draw(self, c, tl):
        a = self.fade(tl, 0.3, 0.3)
        scrim(c, (self.x - 30, self.y - 20, self.x + self.im.width + 30, self.y + self.im.height + 20), int(140 * a), 18)
        MK.place(c, _alpha(self.im, a), self.x, self.y, "lt")

class Stamp(DOv):
    """'as of 13 Oct 2026' - a hand-stamped date, slightly rotated, red"""
    def __init__(self, text, t_in, x=W - 360, y=150, t_out=None):
        self.t_in, self.t_out, self.x, self.y = t_in, t_out, x, y; self.im = MK.hand(text, 64, RED, rot=-6)
    def draw(self, c, tl):
        u = smooth((tl - self.t_in) / 0.25); s = 1.25 - 0.25 * u
        im = self.im.resize((int(self.im.width * s), int(self.im.height * s)), Image.BILINEAR)
        MK.place(c, _alpha(im, self.fade(tl, 0.15, 0.3)), self.x, self.y, "c")

def grade(img, sat=0.82, contrast=1.08, cool=0.05):
    """doc grade for photos: a touch desaturated, cooler shadows"""
    im = ImageEnhance.Contrast(ImageEnhance.Color(img.convert("RGB")).enhance(sat)).enhance(contrast)
    a = np.asarray(im, np.float32); lum = a.mean(axis=2, keepdims=True) / 255
    a[..., 2:3] += cool * 255 * (1 - lum); a[..., 0:1] -= cool * 120 * (1 - lum)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

class TitleCard:
    """beat background: the world map slowly pushing in, dimmed, the title written over it, Batata small and calm"""
    def __init__(self, title, sub, base_img, batata=None):
        self.bg = ImageEnhance.Brightness(base_img.convert("RGB")).enhance(0.45).convert("RGBA")
        self.t = text_img(title, 150, WHITE); self.s = MK.hand(sub, 48, YEL, rot=-2); self.b = batata
    def frame(self, t, d, tl):
        z = 1.0 + 0.05 * t / max(d, 1e-3); bw, bh = self.bg.size; cw, ch = bw / z, bh / z
        c = self.bg.resize((W, H), Image.BILINEAR, box=((bw - cw) / 2, (bh - ch) / 2, (bw + cw) / 2, (bh + ch) / 2))
        a = smooth(t / 0.6); u = smooth((t - 0.3) / 0.6)
        MK.place(c, _alpha(self.t, a), W / 2, H / 2 - 60, "c")
        if u > 0: MK.place(c, _alpha(self.s, u), W / 2, H / 2 + 70, "c")
        if self.b is not None and t > 0.6: MK.place(c, self.b, W - 150, 820, "c")
        return MK.vignette(c, 0.45)
