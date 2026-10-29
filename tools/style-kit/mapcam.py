"""Moving maps for documentaries (doc mode): Natural Earth bases pre-rendered at several zoom levels (cached PNGs),
an eased camera (centre lon/lat + view height in degrees of latitude), and geo overlays drawn per frame in screen space.

    bases = [Base("world", -25, 145, -45, 62, 16), Base("arabia", 28, 68, 4, 34, 110), ...]
    cam = Cam([(t0, lon, lat, span), (t1, lon, lat, span, "fly"), ...])     # "fly" = zoom out a little mid-move
    bg = MapBG(bases, cam, [Route(...), Pulse(...), Ship(...), Label(...)])  # a background for the beat engine
One horizontal scale (cos 20 deg) is used by every base, so switching from a coarse base to a fine one never jumps."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from mapkit import Map, RUBIK
import marker as MK

W, H = 1920, 1080
COSF = math.cos(math.radians(20))
CACHE = "D:/why habibi/_style_kit/maps/cache/"
WHITE, YEL, RED, NAVY = (255, 255, 255), (255, 194, 26), (240, 64, 47), (11, 16, 80)

def smooth(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def inout(x): x = min(1.0, max(0.0, x)); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

class Base:
    def __init__(self, name, lon0, lon1, lat0, lat1, ppd, pal=None):
        self.name, self.lon0, self.lon1, self.lat0, self.lat1, self.ppd = name, lon0, lon1, lat0, lat1, ppd
        self.w, self.h = int(round((lon1 - lon0) * ppd * COSF)), int(round((lat1 - lat0) * ppd))
        tag = "" if not pal else "_" + str(abs(hash(tuple(sorted(pal.items())))) % 10 ** 6)
        self.path = f"{CACHE}{name}_{self.w}x{self.h}{tag}.png"; self._img = None
        if not os.path.exists(self.path):
            os.makedirs(CACHE, exist_ok=True)
            halo, line = max(3, 0.07 * ppd), 1.2 * max(1.0, math.sqrt(ppd / 110))
            Map(lon0, lon1, lat0, lat1, self.w, self.h, ss=1, halo=halo, line=line).render(pal=pal).convert("RGB").save(self.path)
            print("rendered base", self.path, flush=True)
    @property
    def img(self):
        if self._img is None: self._img = Image.open(self.path).convert("RGB")
        return self._img
    def px(self, lon, lat): return (lon - self.lon0) * self.ppd * COSF, (self.lat1 - lat) * self.ppd
    def covers(self, l0, l1, b0, b1): return l0 >= self.lon0 and l1 <= self.lon1 and b0 >= self.lat0 and b1 <= self.lat1

class Cam:
    """keys: (t, lon, lat, span[, "fly"]) - span = view height in degrees of latitude; eased between keys, zoom in log space"""
    def __init__(self, keys): self.k = sorted(keys, key=lambda k: k[0])
    def at(self, t):
        k = self.k
        if t <= k[0][0]: return k[0][1:4]
        for a, b in zip(k, k[1:]):
            if t <= b[0]:
                u = inout((t - a[0]) / max(1e-6, b[0] - a[0]))
                lon, lat = a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
                ls = math.log(a[3]) + (math.log(b[3]) - math.log(a[3])) * u
                if len(b) > 4 and b[4] == "fly":                          # pull back a little in the middle of a long move
                    dist = math.hypot((b[1] - a[1]) * COSF, b[2] - a[2])
                    ls += max(0.0, math.log(max(dist * 0.9, a[3], b[3])) - max(math.log(a[3]), math.log(b[3]))) * 4 * u * (1 - u)
                return lon, lat, math.exp(ls)
        return k[-1][1:4]

class View:
    def __init__(self, lon, lat, span):
        self.span, self.sw = span, span * W / H / COSF
        self.l0, self.b1 = lon - self.sw / 2, lat + span / 2
    def __call__(self, lon, lat): return (lon - self.l0) / self.sw * W, (self.b1 - lat) / self.span * H
    def ppd(self): return H / self.span

def _grain(seed, amt=7):
    g = np.random.default_rng(seed).normal(128, amt, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
    return Image.fromarray(g).resize((W, H), Image.BILINEAR)
_GRAINS = None

class MapBG:
    """beat background: the camera's view of the finest base that covers it, geo overlays, doc grade + film grain"""
    def __init__(self, bases, cam, items=(), grain=True, vig=0.35, grid=True):
        self.bases, self.cam, self.items, self.grain, self.vig, self.grid = sorted(bases, key=lambda b: b.ppd), cam, list(items), grain, vig, grid
        self.view = None
    def frame(self, t, d, tl):
        global _GRAINS
        lon, lat, span = self.cam.at(tl); v = View(lon, lat, span); self.view = v
        l0, l1, b0, b1 = v.l0, v.l0 + v.sw, lat - span / 2, lat + span / 2
        cands = [b for b in self.bases if b.covers(l0, l1, b0, b1)] or [self.bases[0]]
        good = [b for b in cands if b.ppd >= v.ppd() * 0.85]
        base = good[0] if good else cands[-1]
        x0, y0 = base.px(l0, b1); x1, y1 = base.px(l1, b0)
        if x0 < 0 or y0 < 0 or x1 > base.w or y1 > base.h:      # the view runs off the map: slide it back inside
            bw, bh = x1 - x0, y1 - y0
            if bw > base.w or bh > base.h:                       # wider than the whole base: shrink to fit, keep aspect
                k = min(base.w / bw, base.h / bh); bw, bh = bw * k, bh * k
            x0 = min(max(x0, 0), base.w - bw); y0 = min(max(y0, 0), base.h - bh); x1, y1 = x0 + bw, y0 + bh
            l0 = base.lon0 + x0 / (base.ppd * COSF); b1 = base.lat1 - y0 / base.ppd
            span = bh / base.ppd; v = View(l0 + span * W / H / COSF / 2, b1 - span / 2, span); self.view = v
            l1, b0 = l0 + v.sw, b1 - span
        img = base.img.resize((W, H), Image.BILINEAR, box=(x0, y0, x1, y1)).convert("RGBA")
        if self.grid:                                    # faint graticule, like a printed chart
            step = next(s for s in (1, 2, 5, 10, 20) if span / s <= 8)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(lay)
            for lo in np.arange(math.floor(l0 / step) * step, l1 + step, step):
                x = (lo - l0) / v.sw * W; dg.line([(x, 0), (x, H)], fill=(255, 255, 255, 22), width=1)
            for la in np.arange(math.floor(b0 / step) * step, b1 + step, step):
                y = (b1 - la) / span * H; dg.line([(0, y), (W, y)], fill=(255, 255, 255, 22), width=1)
            img.alpha_composite(lay)
        for o in self.items:
            if o.on(tl): o.draw(img, tl, v)
        if self.vig: img = MK.vignette(img, self.vig)
        if self.grain:
            if _GRAINS is None: _GRAINS = [_grain(s) for s in range(6)]
            g = _GRAINS[int(tl * 24) % 6]
            img = Image.composite(img, img, Image.new("L", (W, H), 255))     # keep RGBA
            a = np.asarray(img, np.int16); n = (np.asarray(g, np.int16) - 128)[..., None] * 0.35
            a[..., :3] = (a[..., :3] + n).clip(0, 255); img = Image.fromarray(a.astype(np.uint8), "RGBA")
        return img

# ------------------------------------------------------------------ geo overlays (positions in lon/lat, drawn in screen space)
class Geo:
    t_out = None
    def on(self, tl): return tl >= self.t_in - 1e-6 and (self.t_out is None or tl < self.t_out)
    def alpha(self, tl, fade=0.35):
        a = min(1.0, (tl - self.t_in) / fade) if fade else 1.0
        if self.t_out is not None: a = min(a, max(0.0, (self.t_out - tl) / fade))
        return max(0.0, a)

def _poly_len(p): return float(np.sum(np.hypot(*np.diff(p, axis=0).T))) if len(p) > 1 else 0.0
def _partial(p, frac):
    if frac >= 1: return p
    seg = np.hypot(*np.diff(p, axis=0).T); cum = np.concatenate([[0], np.cumsum(seg)]); L = cum[-1] * frac
    i = max(1, int(np.searchsorted(cum, L)))
    r = (L - cum[i - 1]) / max(seg[i - 1], 1e-6)
    return np.vstack([p[:i], p[i - 1] + (p[i] - p[i - 1]) * r])
def _densify(pts, n=12):
    pts = np.asarray(pts, float); out = [pts[0]]
    for a, b in zip(pts, pts[1:]): out += list(np.linspace(a, b, n)[1:])
    return np.array(out)

def _layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def _paste(c, lay, a):
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    c.alpha_composite(lay)

class Route(Geo):
    """a line that draws itself along lon/lat points; dash=(on, off) px; glow = soft halo underneath"""
    def __init__(self, pts, t_in, dur=1.2, color=YEL, width=6, dash=None, glow=True, t_out=None):
        self.pts, self.t_in, self.dur, self.color, self.width, self.dash, self.glow, self.t_out = _densify(pts), t_in, dur, color, width, dash, glow, t_out
    def draw(self, c, tl, v):
        p = np.array([v(*q) for q in self.pts]); p = _partial(p, smooth((tl - self.t_in) / self.dur))
        lay = _layer(); d = ImageDraw.Draw(lay); w = max(2, int(self.width))
        if self.glow:
            g = _layer(); ImageDraw.Draw(g).line([tuple(q) for q in p], fill=tuple(self.color) + (150,), width=w * 3, joint="curve")
            lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(w * 1.5)))
        if self.dash:
            on, off = self.dash; L = 0.0
            for a, b in zip(p, p[1:]):
                seg = np.hypot(*(b - a)); s = 0.0
                while s < seg:
                    ph = (L + s) % (on + off); step = min(seg - s, (on - ph) if ph < on else (on + off - ph))
                    if ph < on: d.line([tuple(a + (b - a) * s / seg), tuple(a + (b - a) * (s + step) / seg)], fill=tuple(self.color) + (255,), width=w)
                    s += max(step, 0.5)
                L += seg
        else:
            d.line([tuple(q) for q in p], fill=tuple(self.color) + (255,), width=w, joint="curve")
            r = w / 2; e = p[-1]; d.ellipse((e[0] - r, e[1] - r, e[0] + r, e[1] + r), fill=tuple(self.color) + (255,))
        _paste(c, lay, self.alpha(tl, 0.2))

class Flow(Geo):
    """chevrons streaming along a path (oil flowing); speed in px/s"""
    def __init__(self, pts, t_in, color=YEL, n=7, size=16, speed=140, t_out=None):
        self.pts, self.t_in, self.color, self.n, self.size, self.speed, self.t_out = _densify(pts, 24), t_in, color, n, size, speed, t_out
    def draw(self, c, tl, v):
        p = np.array([v(*q) for q in self.pts]); L = _poly_len(p)
        if L < 10: return
        seg = np.hypot(*np.diff(p, axis=0).T); cum = np.concatenate([[0], np.cumsum(seg)])
        lay = _layer(); d = ImageDraw.Draw(lay); gap = L / self.n; off = ((tl - self.t_in) * self.speed) % gap
        for k in range(self.n):
            s = off + k * gap; i = max(1, int(np.searchsorted(cum, s))); i = min(i, len(p) - 1)
            a, b = p[i - 1], p[i]; dirv = (b - a) / max(np.hypot(*(b - a)), 1e-6); pos = a + dirv * (s - cum[i - 1])
            nrm = np.array([-dirv[1], dirv[0]]); z = self.size
            tri = [tuple(pos + dirv * z), tuple(pos - dirv * z * 0.6 + nrm * z * 0.7), tuple(pos - dirv * z * 0.2), tuple(pos - dirv * z * 0.6 - nrm * z * 0.7)]
            d.polygon(tri, fill=tuple(self.color) + (235,))
        _paste(c, lay, self.alpha(tl))

class Pulse(Geo):
    """a solid dot with rings that keep expanding (a place that matters)"""
    def __init__(self, lon, lat, t_in, color=RED, r=10, ring=70, period=1.6, t_out=None):
        self.p, self.t_in, self.color, self.r, self.ring, self.period, self.t_out = (lon, lat), t_in, color, r, ring, period, t_out
    def draw(self, c, tl, v):
        x, y = v(*self.p); lay = _layer(); d = ImageDraw.Draw(lay)
        for k in range(2):
            u = (((tl - self.t_in) / self.period) + k * 0.5) % 1.0; R = self.r + (self.ring - self.r) * u
            d.ellipse((x - R, y - R, x + R, y + R), outline=tuple(self.color) + (int(230 * (1 - u)),), width=4)
        d.ellipse((x - self.r, y - self.r, x + self.r, y + self.r), fill=tuple(self.color) + (255,), outline=(255, 255, 255, 255), width=3)
        _paste(c, lay, self.alpha(tl))

class Dot(Geo):
    def __init__(self, lon, lat, t_in, color=WHITE, r=7, t_out=None):
        self.p, self.t_in, self.color, self.r, self.t_out = (lon, lat), t_in, color, r, t_out
    def draw(self, c, tl, v):
        x, y = v(*self.p); lay = _layer(); r = self.r
        ImageDraw.Draw(lay).ellipse((x - r, y - r, x + r, y + r), fill=tuple(self.color) + (255,), outline=(20, 20, 30, 255), width=2)
        _paste(c, lay, self.alpha(tl))

_fonts = {}
def _font(size):
    if size not in _fonts: _fonts[size] = ImageFont.truetype(RUBIK, size)
    return _fonts[size]

class Label(Geo):
    """a Rubik map label pinned to a place (sentence case); fades in; dx/dy in px.
    smin/smax: only shown while the view height (degrees) is in that range (base-map labels that follow the zoom)"""
    BAND = (420, 850, 1500, 1020)            # burned-in captions live here (user rule: they never cover our text)
    def __init__(self, text, lon, lat, t_in, size=34, color=WHITE, stroke=(8, 14, 34), dx=0, dy=0, anchor="mm", t_out=None, sw=4, smin=0, smax=999,
                 base=False):
        self.text, self.p, self.t_in, self.size, self.color, self.stroke, self.dx, self.dy, self.anchor, self.t_out, self.sw = text, (lon, lat), t_in, size, color, stroke, dx, dy, anchor, t_out, sw
        self.smin, self.smax, self.base = smin, smax, base
    def draw(self, c, tl, v):
        if not (self.smin <= v.span <= self.smax): return
        x, y = v(*self.p); x += self.dx; y += self.dy
        if not (-300 < x < W + 300 and -100 < y < H + 100): return
        w = _font(self.size).getlength(self.text); bx0 = x - w / 2 if self.anchor[0] == "m" else x
        z = self.BAND
        if min(bx0 + w, z[2]) - max(bx0, z[0]) > 4 and min(y + self.size / 2 + self.sw, z[3]) - max(y - self.size / 2 - self.sw, z[1]) > 0:
            if self.base: return                                         # background map names step aside for captions
            y = z[1] - self.size / 2 - self.sw - 6                         # our story labels are lifted above the captions
        lay = _layer()
        ImageDraw.Draw(lay).text((x, y), self.text, font=_font(self.size), fill=tuple(self.color) + (255,),
                                 anchor=self.anchor, stroke_width=self.sw, stroke_fill=tuple(self.stroke) + (255,))
        _paste(c, lay, self.alpha(tl, 0.4))

class Barrier(Geo):
    """a thick bar drawn across a strait (closed); angle in degrees, length in px"""
    def __init__(self, lon, lat, t_in, angle=60, length=120, color=RED, width=16, t_out=None):
        self.p, self.t_in, self.angle, self.length, self.color, self.width, self.t_out = (lon, lat), t_in, angle, length, color, width, t_out
    def draw(self, c, tl, v):
        x, y = v(*self.p); a = math.radians(self.angle); u = smooth((tl - self.t_in) / 0.4)
        dx, dy = math.cos(a) * self.length / 2, -math.sin(a) * self.length / 2
        p0 = (x - dx, y - dy); p1 = (x - dx + 2 * dx * u, y - dy + 2 * dy * u)
        lay = _layer(); d = ImageDraw.Draw(lay)
        d.line([p0, p1], fill=(255, 255, 255, 255), width=self.width + 8); d.line([p0, p1], fill=tuple(self.color) + (255,), width=self.width)
        c.alpha_composite(lay)

class Ship(Geo):
    """a tanker marker moving along a lon/lat path between t_in and t_end; dark=(t0, t1) = transponder off (ghosted)"""
    def __init__(self, pts, t_in, t_end, color=WHITE, size=14, dark=None, t_out=None, trail=True):
        self.pts, self.t_in, self.t_end, self.color, self.size, self.dark, self.t_out, self.trail = _densify(pts, 30), t_in, t_end, color, size, dark, t_out, trail
    def draw(self, c, tl, v):
        p = np.array([v(*q) for q in self.pts]); u = inout((tl - self.t_in) / max(1e-6, self.t_end - self.t_in))
        q = _partial(p, max(u, 1e-3)); pos = q[-1]; prev = q[-2] if len(q) > 1 else p[0]
        dirv = pos - prev; n = np.hypot(*dirv); dirv = dirv / n if n > 1e-6 else np.array([1.0, 0.0]); nrm = np.array([-dirv[1], dirv[0]])
        ghost = self.dark and self.dark[0] <= tl < self.dark[1]
        lay = _layer(); d = ImageDraw.Draw(lay); z = self.size
        if self.trail and len(q) > 2 and not ghost:
            d.line([tuple(x) for x in q], fill=tuple(self.color) + (90,), width=3)
        hull = [tuple(pos + dirv * z * 1.3), tuple(pos + nrm * z * 0.55 + dirv * z * 0.2), tuple(pos + nrm * z * 0.55 - dirv * z),
                tuple(pos - nrm * z * 0.55 - dirv * z), tuple(pos - nrm * z * 0.55 + dirv * z * 0.2)]
        if ghost: d.polygon(hull, outline=tuple(self.color) + (150,), width=2)
        else: d.polygon(hull, fill=tuple(self.color) + (255,), outline=(10, 14, 30, 255), width=2)
        _paste(c, lay, self.alpha(tl, 0.3))

class Area(Geo):
    """fill a lon/lat ring (an island, a zone) in a colour with a white edge"""
    def __init__(self, ring, t_in, color=RED, alpha=230, t_out=None, edge=3):
        self.ring, self.t_in, self.color, self.a, self.t_out, self.edge = ring, t_in, color, alpha, t_out, edge
    def draw(self, c, tl, v):
        p = [v(*q) for q in self.ring]; lay = _layer(); d = ImageDraw.Draw(lay)
        d.polygon(p, fill=tuple(self.color) + (self.a,)); d.line(p + [p[0]], fill=(255, 255, 255, 255), width=self.edge)
        _paste(c, lay, self.alpha(tl, 0.5))

class HandCircle(Geo):
    """our marker circle around a place (rx, ry in px)"""
    def __init__(self, lon, lat, t_in, rx=90, ry=70, color=RED, width=10, seed=5, t_out=None):
        self.p, self.t_in, self.rx, self.ry, self.color, self.width, self.seed, self.t_out = (lon, lat), t_in, rx, ry, color, width, seed, t_out
    def draw(self, c, tl, v):
        x, y = v(*self.p)
        MK.strokes(c, MK.circle_path(x, y, self.rx, self.ry, seed=self.seed), self.color, self.width, min(1.0, (tl - self.t_in) / 0.45), seed=self.seed)

class HandArrow(Geo):
    """our marker arrow from a screen offset to a place; outlined white so it reads on any map"""
    def __init__(self, lon, lat, t_in, frm=(-260, -160), color=RED, width=14, bend=0.25, head=40, seed=3, t_out=None):
        self.p, self.t_in, self.frm, self.color, self.width, self.bend, self.head, self.seed, self.t_out = (lon, lat), t_in, frm, color, width, bend, head, seed, t_out
    def draw(self, c, tl, v):
        x, y = v(*self.p); paths = MK.arrow_path((x + self.frm[0], y + self.frm[1]), (x, y), bend=self.bend, head=self.head, seed=self.seed)
        pr = min(1.0, (tl - self.t_in) / 0.35)
        MK.strokes(c, paths, WHITE, self.width + 10, pr, seed=self.seed); MK.strokes(c, paths, self.color, self.width, pr, seed=self.seed)
