"""Real maps from Natural Earth (public domain, _style_kit/maps/*.geojson) in the Cut & Marker look:
deep navy sea with a soft shallow-water halo, warm paper land, thin borders, Rubik labels. Reusable for any episode.

    m = Map(lon0, lon1, lat0, lat1, w, h)      # equirectangular, x scaled by cos(mid latitude)
    img = m.render()                           # RGBA, supersampled 2x then downsampled
    x, y = m.xy(lon, lat)                      # pixel position of a place
    m.highlight(img, "Yemen", (43.39, 12.632, 43.449, 12.674), RED)   # fill one island / ring by its bbox
"""
import json, math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

KIT = "D:/why habibi/_style_kit/"
RUBIK = KIT + "fonts/Rubik-Bold.ttf"
SEA_TOP, SEA_BOT = (16, 34, 78), (9, 22, 56)
SHALLOW = (52, 92, 150)
LAND, LAND_EDGE, BORDER = (226, 211, 176), (120, 100, 70), (168, 150, 118)

@functools.lru_cache(None)
def _load():
    c = json.load(open(KIT + "maps/ne_10m_admin_0_countries.geojson", encoding="utf-8"))
    mi = json.load(open(KIT + "maps/ne_10m_minor_islands.geojson", encoding="utf-8"))
    feats = []
    for f in c["features"]:
        g = f["geometry"]; ps = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        feats.append((f["properties"]["NAME"], [p[0] for p in ps]))
    for f in mi["features"]:
        g = f["geometry"]; ps = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        feats.append(("_island", [p[0] for p in ps]))
    return feats

def _bb(ring):
    a = np.asarray(ring); return a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()

class Map:
    def __init__(self, lon0, lon1, lat0, lat1, w, h, ss=2, halo=10, line=1.2):
        self.lon0, self.lon1, self.lat0, self.lat1, self.w, self.h, self.ss = lon0, lon1, lat0, lat1, w, h, ss
        self.halo, self.line = halo, line                    # shallow-water halo radius and border width, in output px
    def xy(self, lon, lat, ss=1):
        return ((lon - self.lon0) / (self.lon1 - self.lon0) * self.w * ss, (self.lat1 - lat) / (self.lat1 - self.lat0) * self.h * ss)
    def _rings(self):
        shifts = [0] + ([-360] if self.lon0 < -180 else []) + ([360] if self.lon1 > 180 else [])   # views across the dateline
        for name, rings in _load():
            for r in rings:
                b0 = _bb(r)
                for s in shifts:
                    b = (b0[0] + s, b0[1], b0[2] + s, b0[3])
                    if b[2] < self.lon0 - 1 or b[0] > self.lon1 + 1 or b[3] < self.lat0 - 1 or b[1] > self.lat1 + 1: continue
                    yield name, (r if s == 0 else [[x + s, y] for x, y in r]), b
    def render(self, border=True, pal=None):
        """pal: optional dict overriding sea_top, sea_bot, shallow, land, border, edge (RGB tuples)"""
        p = dict(sea_top=SEA_TOP, sea_bot=SEA_BOT, shallow=SHALLOW, land=LAND, border=BORDER, edge=LAND_EDGE); p.update(pal or {})
        SEA_TOP_, SEA_BOT_, SHALLOW_, LAND_, BORDER_, EDGE_ = (p[k] for k in ("sea_top", "sea_bot", "shallow", "land", "border", "edge"))
        S = self.ss; W, H = self.w * S, self.h * S
        mask = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(mask)
        rings = list(self._rings())
        for name, r, b in rings: dm.polygon([self.xy(x, y, S) for x, y in r], fill=255)
        if S == 1: mask = mask.filter(ImageFilter.GaussianBlur(0.9))             # soft coast edges when not supersampled
        f32 = np.float32
        yy = np.linspace(0, 1, H, dtype=f32)[:, None, None]
        sea = (np.array(SEA_TOP_, f32) * (1 - yy) + np.array(SEA_BOT_, f32) * yy) * np.ones((1, W, 1), f32)
        halo = np.asarray(mask.filter(ImageFilter.GaussianBlur(self.halo * S)), f32)[..., None] / 255
        sea = sea * (1 - 0.55 * halo) + np.array(SHALLOW_, f32) * 0.55 * halo           # shallow water near coasts
        del halo
        land = np.array(LAND_, f32) * (1.03 - 0.08 * yy) + np.random.default_rng(3).normal(0, 3, (H, W, 1)).astype(f32)
        m = np.asarray(mask, f32)[..., None] / 255
        img = Image.fromarray((sea * (1 - m) + land * m).clip(0, 255).astype(np.uint8)).convert("RGBA")
        del sea, land, m
        d = ImageDraw.Draw(img)
        for name, r, b in rings:
            pts = [self.xy(x, y, S) for x, y in r]
            d.line(pts + [pts[0]], fill=tuple(BORDER_ if border and name != "_island" else EDGE_) + (255,), width=max(1, int(self.line * S)))
        return img if S == 1 else img.resize((self.w, self.h), Image.LANCZOS)
    def ring_pts(self, name, bbox):
        """pixel points of the ring of `name` whose bbox matches (within 0.01 deg)"""
        for n, r, b in self._rings():
            if (name is None or n == name) and all(abs(u - v) < 0.01 for u, v in zip(b, bbox)):
                return [self.xy(x, y) for x, y in r]
    def highlight(self, img, name, bbox, color, outline=(255, 255, 255)):
        pts = self.ring_pts(name, bbox)
        if pts:
            d = ImageDraw.Draw(img); d.polygon(pts, fill=tuple(color) + (255,)); d.line(pts + [pts[0]], fill=outline + (255,), width=2)
        return pts

def label(img, text, x, y, size=26, fill=(255, 255, 255), stroke=(10, 18, 45), anchor="mm", sw=3):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(RUBIK, size)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke)

def dashed(img, pts, color, width=4, dash=14, gap=10):
    d = ImageDraw.Draw(img); pts = np.asarray(pts, float)
    seg = np.concatenate([np.linspace(pts[i], pts[i + 1], max(2, int(np.linalg.norm(pts[i + 1] - pts[i])))) for i in range(len(pts) - 1)])
    on, run = True, 0
    for i in range(len(seg) - 1):
        if on: d.line([tuple(seg[i]), tuple(seg[i + 1])], fill=tuple(color) + (255,), width=width)
        run += 1
        if run >= (dash if on else gap): on, run = not on, 0
