"""Ep 4 render engine (copied from Ep 3) on top of the style kit: backgrounds (graded photo with push, graded video B-roll, navy paper,
real study pages) + timed overlays (hand notes, arrows, circles, underlines, scribble-outs, ticks, Batata pops, big
words, pasted prints, hand-drawn bars) + beat-level punch-ins and shakes. Cue times are FINAL-TIMELINE seconds."""
import math, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from ep04_common import *
from marker import *
from brand_v2 import texture

Image.MAX_IMAGE_PIXELS = None
RCROP = BUILD + "receipts/"
STOCK1 = "D:/why habibi/1st video/claude_package/stock/"
PH = MEDIA + "photos/"
VID = MEDIA + "video/"
PH2 = "D:/why habibi/2nd video/media/photos/"
VID2 = "D:/why habibi/2nd video/media/video/"

def ease(x): x = min(1.0, max(0.0, x)); return 1 - (1 - x) ** 3

# ============================================================== backgrounds
class TextureBG:
    _c = None
    def frame(self, t, d, tl):
        if TextureBG._c is None: TextureBG._c = texture(W, H)
        return TextureBG._c.copy()

class PhotoBG:
    """photo filled to 16:9 around `focus`, night-graded once, slow push from z[0] to z[1] over the beat"""
    Z = 1.14
    def __init__(self, path, focus=(0.5, 0.5), amt=0.45, z=(1.0, 1.05), grade=True, mirror=False, dark=1.0):
        self.path, self.focus, self.amt, self.z, self.grade, self.mirror, self.dark = path, focus, amt, z, grade, mirror, dark
        self.big = None
    def _load(self):
        im = Image.open(self.path).convert("RGB")
        if self.mirror: im = ImageOps.mirror(im)
        iw, ih = im.size; ar = W / H
        cw, ch = (iw, iw / ar) if iw / ih < ar else (ih * ar, ih)
        cx = min(max(self.focus[0] * iw, cw / 2), iw - cw / 2); cy = min(max(self.focus[1] * ih, ch / 2), ih - ch / 2)
        im = im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2)))
        im = im.resize((int(W * self.Z), int(H * self.Z)), Image.LANCZOS)
        if self.grade: im = night(im, self.amt).convert("RGB")
        if self.dark != 1.0:
            im = Image.fromarray(np.clip(np.asarray(im, np.float32) * self.dark, 0, 255).astype(np.uint8))
        self.big = im
    def frame(self, t, d, tl):
        if self.big is None: self._load()
        z = self.z[0] + (self.z[1] - self.z[0]) * min(1.0, t / max(d, 1e-3))
        bw, bh = self.big.size
        cw, ch = min(bw, bw / z), min(bh, bh / z)            # z = 1 shows the whole (oversized) photo
        x0, y0 = max(0.0, (bw - cw) / 2), max(0.0, (bh - ch) / 2)
        return self.big.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")

class VideoBG:
    """B-roll streamed through ffmpeg (scaled, cropped, graded); slowed down if the clip is shorter than the beat"""
    GRADE = ("eq=brightness=-0.035:contrast=1.06:saturation=0.82,"
             "colorbalance=rs=-0.05:gs=-0.015:bs=0.08:rm=-0.02:bm=0.05")
    def __init__(self, path, start=0.0, z=1.0, grade=True, mirror=False):
        self.path, self.start, self.z, self.grade, self.mirror = path, start, z, grade, mirror
        self.p = None; self.last = None
    def _open(self, d):
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", self.path],
                                   capture_output=True, text=True).stdout or 0)
        avail = max(0.5, dur - self.start - 0.05)
        speed = min(1.0, avail / d) if d > 0 else 1.0
        vf = [f"setpts=PTS/{speed:.4f}", "fps=30", f"scale={int(W * self.z)}:{int(H * self.z)}:force_original_aspect_ratio=increase",
              f"crop={W}:{H}"]
        if self.mirror: vf.append("hflip")
        if self.grade: vf.append(self.GRADE)
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(self.start), "-i", self.path, "-vf", ",".join(vf),
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    def frame(self, t, d, tl):
        if self.p is None: self._open(d)
        buf = self.p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3: self.last = Image.frombytes("RGB", (W, H), buf)
        return (self.last or Image.new("RGB", (W, H))).convert("RGBA")
    def close(self):
        if self.p: self.p.stdout.close(); self.p.kill(); self.p = None

class Receipt:
    """a real study page, cropped off the frame edges, tilted; views switch on cues; highlights / circles / focus-dim
    are timed to the voiceover. phrases = the exact strings captured by receipt.py."""
    def __init__(self, name, views, marks=(), tag=None, angle=-1.4):
        self.meta = json.load(open(RCROP + name + ".json", encoding="utf-8"))
        self.pages = {}; self.views = sorted(views, key=lambda v: v["t"]); self.marks = list(marks)
        self.tag, self.angle, self.tf = tag, angle, None
    def _crop_for(self, phrase):
        for k, c in enumerate(self.meta["crops"]):
            if phrase in c["phrases"]: return k
        raise KeyError(phrase)
    def boxes(self, k, phrase):
        return self.meta["crops"][k]["phrases"].get(phrase, [])
    def page(self, k):
        if k not in self.pages: self.pages[k] = Image.open(RCROP + self.meta["crops"][k]["file"]).convert("RGBA")
        return self.pages[k]
    def frame(self, t, d, tl):
        v = [v for v in self.views if v["t"] <= tl + 1e-6] or self.views[:1]; v = v[-1]
        k = self._crop_for(v["at"]); bx = self.boxes(k, v["at"])
        cx = (min(b[0] for b in bx) + max(b[2] for b in bx)) / 2 + v.get("dx", 0)
        cy = (min(b[1] for b in bx) + max(b[3] for b in bx)) / 2 + v.get("dy", 0)
        s = v.get("s", 1.25) + v.get("push", 0.012) * (tl - v["t"])
        hl, focus, tf0 = [], [], None
        for m in self.marks:
            if m["t"] > tl or m.get("kind", "hl") != "hl" or m["phrase"] not in self.meta["crops"][k]["phrases"]: continue
            lines = self.boxes(k, m["phrase"]); p = (tl - m["t"]) / m.get("dur", 0.45) * len(lines)
            for i, b in enumerate(lines): hl.append((b, max(0.0, min(1.0, p - i)), 7 + i))
        for m in self.marks:
            if m.get("focus", True) and m["t"] <= tl and m["phrase"] in self.meta["crops"][k]["phrases"]:
                focus += self.boxes(k, m["phrase"]); tf0 = m["t"] if tf0 is None else min(tf0, m["t"])
        dim = min(1.0, (tl - tf0) / 0.25) if tf0 is not None else 0.0
        c, self.tf = page_view(self.page(k), (cx, cy), s, self.angle, marks=hl, focus=focus, dim=dim)
        c = vignette(c, 0.30)
        for m in self.marks:                       # marker on top (frame space)
            if m["t"] > tl or m.get("kind") not in ("circle", "underline") or m["phrase"] not in self.meta["crops"][k]["phrases"]:
                continue
            lines = self.boxes(k, m["phrase"]); fb = [box_to_frame(b, self.tf) for b in lines]
            x0, y0, x1, y1 = min(b[0] for b in fb), min(b[1] for b in fb), max(b[2] for b in fb), max(b[3] for b in fb)
            prog = min(1.0, (tl - m["t"]) / 0.35)
            if m["kind"] == "circle":
                strokes(c, circle_path((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 30, (y1 - y0) / 2 + 26, seed=m.get("seed", 3)),
                        m.get("color", RED), 10, prog, seed=m.get("seed", 3))
            else:
                strokes(c, underline_path(x0, x1, y1 + 10, seed=m.get("seed", 4), flick=False), m.get("color", RED), 9, prog, seed=4)
        if self.tag and tl >= self.views[0]["t"]:
            place(c, tagimg(self.tag), 70, 60, "lt")
        return c
    def phrase_frame_box(self, phrase):
        """frame-space box of a phrase in the current view (call after frame())"""
        for k, c in enumerate(self.meta["crops"]):
            if phrase in c["phrases"] and self.tf:
                fb = [box_to_frame(b, self.tf) for b in c["phrases"][phrase]]
                return min(b[0] for b in fb), min(b[1] for b in fb), max(b[2] for b in fb), max(b[3] for b in fb)

_tags = {}
def tagimg(s):
    """the source tag on every receipt: small handwritten white note, top-left"""
    if s not in _tags: _tags[s] = hand(s, 40, WHITE, rot=-1, thick=1)
    return _tags[s]

# ============================================================== overlays
class Ov:
    t_out = None
    def on(self, tl): return tl >= self.t_in - 1e-6 and (self.t_out is None or tl < self.t_out)

class Static(Ov):
    """an overlay that is drawn with a write-on, then cached as a finished layer"""
    def __init__(self, t_in, dur=0.3, t_out=None): self.t_in, self.dur, self.t_out, self._cache = t_in, dur, t_out, None
    def paint(self, layer, prog): raise NotImplementedError
    def draw(self, c, tl):
        if not self.on(tl): return
        prog = (tl - self.t_in) / self.dur if self.dur > 0 else 1.0
        if prog >= 1.0:
            if self._cache is None:
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); self.paint(lay, 1.0)
                bb = lay.getbbox() or (0, 0, 1, 1); self._cache = (lay.crop(bb), bb[:2])
            c.alpha_composite(self._cache[0], self._cache[1])
        else:
            self.paint(c, max(0.0, prog))

class Note(Static):
    def __init__(self, text, x, y, t_in, size=64, color=YEL, rot=-3, anchor="c", t_out=None, dur=0.3):
        super().__init__(t_in, dur, t_out); self.a = (text, x, y, size, color, rot, anchor)
    def paint(self, layer, prog):
        text, x, y, size, color, rot, anchor = self.a
        place(layer, hand(text, size, color, rot=rot, reveal=prog), x, y, anchor)

class Arrow(Static):
    def __init__(self, p0, p1, t_in, color=YEL, width=10, bend=0.25, head=40, t_out=None, seed=2):
        super().__init__(t_in, 0.25, t_out); self.a = (p0, p1, color, width, bend, head, seed)
    def paint(self, layer, prog):
        p0, p1, color, width, bend, head, seed = self.a
        strokes(layer, arrow_path(p0, p1, bend=bend, head=head, seed=seed), color, width, prog, seed=seed)

class Circle(Static):
    def __init__(self, cx, cy, rx, ry, t_in, color=RED, width=10, tilt=-3, t_out=None, seed=5):
        super().__init__(t_in, 0.35, t_out); self.a = (cx, cy, rx, ry, color, width, tilt, seed)
    def paint(self, layer, prog):
        cx, cy, rx, ry, color, width, tilt, seed = self.a
        strokes(layer, circle_path(cx, cy, rx, ry, seed=seed, tilt=tilt), color, width, prog, seed=seed)

class Underline(Static):
    def __init__(self, x0, x1, y, t_in, color=YEL, width=9, t_out=None, seed=8):
        super().__init__(t_in, 0.25, t_out); self.a = (x0, x1, y, color, width, seed)
    def paint(self, layer, prog):
        x0, x1, y, color, width, seed = self.a
        strokes(layer, underline_path(x0, x1, y, seed=seed), color, width, prog, seed=seed)

class Strike(Static):
    """scribble-out: a hand zigzag over a word"""
    def __init__(self, x0, x1, y, t_in, color=RED, width=9, h=34, t_out=None, seed=6):
        super().__init__(t_in, 0.3, t_out); self.a = (x0, x1, y, color, width, h, seed)
    def paint(self, layer, prog):
        x0, x1, y, color, width, h, seed = self.a
        n = max(4, int((x1 - x0) / 38)); xs = np.linspace(x0, x1, n * 2 + 1)
        ys = np.array([y - h / 2 if i % 2 else y + h / 2 for i in range(len(xs))], float)
        pts = np.concatenate([np.linspace([xs[i], ys[i]], [xs[i + 1], ys[i + 1]], 8) for i in range(len(xs) - 1)])
        strokes(layer, [pts], color, width, prog, seed=seed)

class Tick(Static):
    def __init__(self, x, y, t_in, size=70, color=YEL, width=12, t_out=None, seed=9):
        super().__init__(t_in, 0.2, t_out); self.a = (x, y, size, color, width, seed)
    def paint(self, layer, prog):
        x, y, s, color, width, seed = self.a
        p = np.concatenate([np.linspace([x - s * 0.5, y], [x - s * 0.1, y + s * 0.4], 12), np.linspace([x - s * 0.1, y + s * 0.4], [x + s * 0.6, y - s * 0.6], 20)])
        strokes(layer, [p], color, width, prog, seed=seed)

class Big(Ov):
    """big Rubik words; punch = lands at 115% and settles in 3 frames"""
    def __init__(self, text, x, y, t_in, size=170, color=WHITE, anchor="c", t_out=None, outline=0):
        self.t_in, self.t_out, self.text = t_in, t_out, text.replace("\n", " ")
        self.img = outlined(text, size, color, stroke=outline) if outline else bold(text, size, color)
        self.x, self.y, self.anchor = x, y, anchor
    def draw(self, c, tl):
        if not self.on(tl): return
        k = int((tl - self.t_in) * FPS); sc = [1.15, 1.07, 1.02][k] if k < 3 else 1.0
        im = self.img if sc == 1.0 else self.img.resize((int(self.img.width * sc), int(self.img.height * sc)), Image.BILINEAR)
        if self.anchor == "lt":
            place(c, im, self.x - (im.width - self.img.width) / 2, self.y - (im.height - self.img.height) / 2, "lt")
        else:
            place(c, im, self.x, self.y, "c")

class Sticker(Ov):
    def __init__(self, expr, h, x, y, t_in, rot=6, mirror=False, t_out=None, path=None):
        self.t_in, self.t_out = t_in, t_out
        self.a = (path or BATATA + f"Batata_{expr}.png", h, x, y, rot, mirror); self._full = None
    def draw(self, c, tl):
        if not self.on(tl): return
        path, h, x, y, rot, mirror = self.a; k = int((tl - self.t_in) * FPS); sc = pop(k)
        if sc == 1.0 and self._full is not None: im = self._full
        else:
            im = sticker(path, h, rot=0, scale=max(sc, 0.05))
            if mirror: im = ImageOps.mirror(im)
            im = im.rotate(rot, Image.BICUBIC, expand=True)
            if sc == 1.0: self._full = im
        place(c, im, x, y)

class Censor(Ov):
    """a Batata sticker slapped over one word of a receipt (follows the page as it moves)"""
    def __init__(self, rec, phrase, t_in, expr="smug", h=170, line=0, rot=-8):
        self.rec, self.phrase, self.t_in, self.t_out, self.line = rec, phrase, t_in, None, line
        self.st = Sticker(expr, h, 0, 0, t_in, rot=rot)
    def draw(self, c, tl):
        if not self.on(tl) or not self.rec.tf: return
        for crop in self.rec.meta["crops"]:
            if self.phrase in crop["phrases"]:
                b = box_to_frame(crop["phrases"][self.phrase][self.line], self.rec.tf)
                self.st.a = self.st.a[:2] + ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) + self.st.a[4:]
                self.st.draw(c, tl); return

class Pasted(Ov):
    """a picture pasted in like a print: white edge, small shadow, tilt; pops in"""
    def __init__(self, path, w, x, y, t_in, rot=-3, t_out=None, grade=False):
        self.t_in, self.t_out = t_in, t_out
        im = Image.open(path).convert("RGB"); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        if grade: im = night(im, 0.4).convert("RGB")
        e = Image.new("RGBA", (im.width + 16, im.height + 16), (255, 255, 255, 255)); e.paste(im, (8, 8))
        s = Image.new("RGBA", (e.width + 30, e.height + 30), (0, 0, 0, 0)); s.alpha_composite(Image.new("RGBA", e.size, (0, 0, 0, 130)), (10, 12))
        s = s.filter(ImageFilter.GaussianBlur(6)); s.alpha_composite(e, (0, 0))
        self.img = s.rotate(rot, Image.BICUBIC, expand=True); self.x, self.y = x, y
    def draw(self, c, tl):
        if not self.on(tl): return
        k = int((tl - self.t_in) * FPS); sc = pop(k)
        im = self.img if sc == 1.0 else self.img.resize((max(1, int(self.img.width * sc)), max(1, int(self.img.height * sc))), Image.BILINEAR)
        place(c, im, self.x, self.y)

class Bar(Static):
    """hand-drawn bar: marker outline grows up, hatched fill, handwritten number on top + label under"""
    def __init__(self, x, base, w, h, t_in, color=YEL, num="", label="", t_out=None, seed=11):
        super().__init__(t_in, 0.45, t_out); self.a = (x, base, w, h, color, num, label, seed)
    def paint(self, layer, prog):
        x, base, w, h, color, num, label, seed = self.a; hh = h * ease(prog)
        pts = np.array([[x, base], [x + 2, base - hh], [x + w - 2, base - hh + 3], [x + w, base]], float)
        strokes(layer, [np.concatenate([np.linspace(pts[i], pts[i + 1], 30) for i in range(3)])], color, 9, 1.0, seed=seed)
        d = ImageDraw.Draw(layer)
        for yy in np.arange(base - 14, base - hh + 10, -22):
            d.line([(x + 10, yy), (x + w - 10, yy - 14)], fill=tuple(color) + (150,), width=5)
        if prog >= 0.6 and num: place(layer, hand(num, 92, color, rot=-3), x + w / 2, base - hh - 70)
        if label: place(layer, hand(label, 44, WHITE, rot=-2), x + w / 2, base + 50)

# ============================================================== caption zone (user rule: captions never cover our text)
CAPTION_ZONE = (420, 860, 1500, 1010)        # where the burned-in captions sit (Rubik 72, MarginV 108)

def ov_bbox(o):
    k = type(o).__name__
    if k == "Note":
        text, x, y, size, color, rot, anchor = o.a; im = hand(text, size, color, rot=rot)
        return (x - im.width / 2, y - im.height / 2, x + im.width / 2, y + im.height / 2) if anchor == "c" else (x, y, x + im.width, y + im.height)
    if k == "Big":
        w, h = o.img.size
        return (o.x - w / 2, o.y - h / 2, o.x + w / 2, o.y + h / 2) if o.anchor == "c" else (o.x, o.y, o.x + w, o.y + h)
    if k == "Sticker":
        path, h, x, y = o.a[:4]; w = h * 0.75; return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if k == "Pasted": return (o.x - o.img.width / 2, o.y - o.img.height / 2, o.x + o.img.width / 2, o.y + o.img.height / 2)
    if k == "Tick": x, y, s = o.a[:3]; return (x - s * 0.5, y - s * 0.6, x + s * 0.6, y + s * 0.4)
    if k in ("Underline", "Strike"): x0, x1, y = o.a[:3]; return (x0, y - 25, x1, y + 25)
    if k == "Bar": x, base, w, h = o.a[:4]; return (x, base - h - 110, x + w, base + 75)
    if k == "Circle": cx, cy, rx, ry = o.a[:4]; return (cx - rx, cy - ry, cx + rx, cy + ry)
    return None

def _hits_zone(bb, z=CAPTION_ZONE):
    return bb and min(bb[2], z[2]) - max(bb[0], z[0]) > 20 and min(bb[3], z[3]) - max(bb[1], z[1]) > 12

def _shift(o, dy):
    k = type(o).__name__
    if k == "Note": a = list(o.a); a[2] -= dy; o.a = tuple(a)
    elif k in ("Underline", "Strike"): a = list(o.a); a[2] -= dy; o.a = tuple(a)
    elif k == "Tick": a = list(o.a); a[1] -= dy; o.a = tuple(a)

def caption_safe(beats, bottom=850):
    """lift the bottom row of notes/ticks/underlines in any beat where one sits in the caption zone (same dy for the
    whole row so pairs stay together). Returns what still collides (stickers, circles, big words: fix by hand)."""
    left = []
    for b in beats:
        if b.name == "end_screen": continue
        row = [(o, ov_bbox(o)) for o in b.ovs if type(o).__name__ in ("Note", "Tick", "Underline", "Strike")]
        row = [(o, bb) for o, bb in row if bb and bb[1] > 700 and bb[3] > CAPTION_ZONE[1]]
        hit = [bb for o, bb in row if _hits_zone(bb)]
        if hit:
            dy = max(bb[3] for bb in hit) - bottom
            moved = {id(o) for o, bb in row}
            for o, bb in row: _shift(o, dy)
            changed = True                       # cascade: a lifted note pushes anything it now overlaps up too
            while changed:
                changed = False
                movable = [o for o in b.ovs if type(o).__name__ in ("Note", "Tick", "Underline", "Strike")]
                for o in movable:
                    if id(o) in moved: continue
                    bo = ov_bbox(o)
                    for m in movable:
                        if id(m) not in moved: continue
                        bm = ov_bbox(m)
                        if min(bo[2], bm[2]) - max(bo[0], bm[0]) > 10 and min(bo[3], bm[3]) - max(bo[1], bm[1]) > 6:
                            _shift(o, dy); moved.add(id(o)); changed = True; break
        for o in b.ovs:
            if _hits_zone(ov_bbox(o)): left.append((b.name, type(o).__name__, getattr(o, "text", "") or str(o.a[0])[:30]))
    return left

# ============================================================== beats
class Beat:
    def __init__(self, t0, bg, ovs=(), punch=(), shakes=(), name=""):
        self.t0, self.bg, self.ovs, self.punch, self.shakes, self.name = t0, bg, list(ovs), list(punch), list(shakes), name
        self.t1 = None
    def frame(self, tl):
        d = self.t1 - self.t0
        c = self.bg.frame(tl - self.t0, d, tl)
        for o in self.ovs:
            if getattr(o, "on", None) is None or o.on(tl): o.draw(c, tl)
        z = 1.0
        for (tp, zz) in self.punch:                # instant punch-in on a cue, holds until the next punch
            if tl >= tp: z = zz
        if z != 1.0:
            cw, ch = W / z, H / z; x0, y0 = (W - cw) / 2, (H - ch) / 2
            c = c.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        for ts in self.shakes:
            k = int(round((tl - ts) * FPS))
            if 0 <= k < 4: c = shake(c, k, 12, seed=int(ts * 10))
        return c
    def close(self):
        if hasattr(self.bg, "close"): self.bg.close()


# ============================================================== doc mode additions (Ep 4)
from docfx import grade as doc_grade

class DocPhotoBG(PhotoBG):
    """a photo in the documentary grade (cooler, a touch desaturated) with a slow push"""
    def _load(self):
        super()._load()
        self.big = doc_grade(self.big)
