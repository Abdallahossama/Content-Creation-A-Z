"""truesize: a Web-Mercator world map + "drag a country to its true size" for map Shorts (Greenland, Alaska, Africa...).
Same old-paper palette as shortkit (OLD). A country is moved on the SPHERE (rotation along a great circle), then
re-projected, so it shrinks/grows exactly like on thetruesize.com. Use from shortkit with CFG["bgfn"].

    import truesize as TS
    V = TS.View(lon_c=-20, lat_c=30, deg_w=110, w=1080, h=1920)   # centre + how many degrees of longitude fit across
    base = V.base()                                                  # RGBA world (cached per view)
    gl = TS.country("Greenland")                                     # [[(lon, lat), ...], ...]  rings
    ak = TS.country("United States of America", bbox=(-180, 50, -129, 72))   # just Alaska (Aleutians unwrapped)
    TS.draw(img, V, TS.moved(gl, (-42, 5), u), fill=(196, 60, 48), alpha=0.85)  # u = 0..1 along the path
    TS.area_mi2(gl)                                                  # true area in square miles (spherical)
"""
import math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from mapkit import _load

OLD = dict(sea_top=(112, 156, 160), sea_bot=(96, 140, 148), shallow=(140, 178, 172), land=(224, 206, 162), border=(140, 112, 76))
MAXLAT = 84.0

def merc(lat): lat = max(-MAXLAT, min(MAXLAT, lat)); return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

class View:
    def __init__(self, lon_c, lat_c, deg_w, w=1080, h=1920):
        self.lon_c, self.lat_c, self.w, self.h = lon_c, lat_c, w, h
        self.s = w / math.radians(deg_w)                       # pixels per radian (x) == per merc unit (y)
        self.yc = merc(lat_c)
    def xy(self, lon, lat):
        return self.w / 2 + self.s * math.radians(lon - self.lon_c), self.h / 2 - self.s * (merc(lat) - self.yc)
    def pts(self, ring): return [self.xy(x, y) for x, y in ring]
    def base(self, ss=2, border=True):
        return _base(self.lon_c, self.lat_c, self.s, self.w, self.h, ss, border)

@functools.lru_cache(8)
def _base(lon_c, lat_c, s, w, h, ss, border):
    v = View.__new__(View); v.lon_c, v.lat_c, v.s, v.w, v.h, v.yc = lon_c, lat_c, s * ss, w * ss, h * ss, merc(lat_c)
    W, H = w * ss, h * ss
    mask = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(mask); rings = []
    half = math.degrees(W / 2 / v.s)
    for name, rs in _load():
        for r in rs:
            a = np.asarray(r)
            for sh in (0, -360, 360):
                if a[:, 0].max() + sh < lon_c - half - 2 or a[:, 0].min() + sh > lon_c + half + 2: continue
                p = [v.xy(x + sh, y) for x, y in r]
                if max(q[1] for q in p) < 0 or min(q[1] for q in p) > H: continue
                dm.polygon(p, fill=255); rings.append((name, p))
    f32 = np.float32; yy = np.linspace(0, 1, H, dtype=f32)[:, None, None]
    sea = (np.array(OLD["sea_top"], f32) * (1 - yy) + np.array(OLD["sea_bot"], f32) * yy) * np.ones((1, W, 1), f32)
    halo = np.asarray(mask.filter(ImageFilter.GaussianBlur(9 * ss)), f32)[..., None] / 255
    sea = sea * (1 - 0.55 * halo) + np.array(OLD["shallow"], f32) * 0.55 * halo
    land = np.array(OLD["land"], f32) * (1.03 - 0.08 * yy) + np.random.default_rng(3).normal(0, 3, (H, W, 1)).astype(f32)
    m = np.asarray(mask, f32)[..., None] / 255
    img = Image.fromarray((sea * (1 - m) + land * m).clip(0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(img)
    if border:
        for name, p in rings: d.line(p + [p[0]], fill=OLD["border"] + (255,), width=max(1, int(1.4 * ss)))
    return img.resize((w, h), Image.LANCZOS) if ss > 1 else img

def _unwrap(ring):
    out = [list(ring[0])]
    for x, y in ring[1:]:
        px = out[-1][0]
        while x - px > 180: x -= 360
        while x - px < -180: x += 360
        out.append([x, y])
    return out

def country(name, bbox=None, min_pts=6, min_km2=800):
    """rings of a Natural Earth country; bbox=(lon0, lat0, lon1, lat1) keeps only parts inside it (e.g. Alaska).
    Parts just east of the dateline (lon > 170) count as west of it, so the Aleutians come along."""
    out = []
    for n, rs in _load():
        if n != name: continue
        for r in rs:
            a = np.asarray(r, float)
            if len(a) < min_pts or _ring_area(a) < min_km2: continue
            if bbox:
                lon = a[:, 0].mean(); lat = a[:, 1].mean()
                if lon > 170 and bbox[0] <= -170: a[:, 0] -= 360; lon -= 360
                if not (bbox[0] <= lon <= bbox[2] and bbox[1] <= lat <= bbox[3]): continue
            out.append(_unwrap(a.tolist()))
    return out

def _vec(lon, lat):
    lo, la = np.radians(lon), np.radians(lat)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)
def _ll(v):
    return np.degrees(np.arctan2(v[..., 1], v[..., 0])), np.degrees(np.arcsin(np.clip(v[..., 2], -1, 1)))

def centroid(rings):
    """area-weighted centre on the sphere (good enough for big countries)"""
    acc = np.zeros(3)
    for r in rings:
        a = np.asarray(r, float); v = _vec(a[:, 0], a[:, 1])
        acc += v.sum(0) * max(_ring_area(a), 1e-9) / len(a)
    lon, lat = _ll(acc / np.linalg.norm(acc)); return float(lon), float(lat)

def moved(rings, to, u=1.0, frm=None):
    """rotate rings on the sphere so their centroid travels a fraction u of the great circle to `to` (lon, lat)"""
    c = _vec(*(frm or centroid(rings))); t = _vec(*to)
    k = np.cross(c, t); n = np.linalg.norm(k)
    if n < 1e-9 or u <= 0: return rings
    k /= n; th = math.acos(float(np.clip(c @ t, -1, 1))) * u
    out = []
    for r in rings:
        a = np.asarray(r, float); v = _vec(a[:, 0], a[:, 1])
        v2 = v * math.cos(th) + np.cross(k, v) * math.sin(th) + np.outer(v @ k, k) * (1 - math.cos(th))
        lon, lat = _ll(v2); out.append(_unwrap(np.stack([lon, lat], -1).tolist()))
    return out

def _ring_area(a):
    """spherical polygon area in km^2 (Earth R = 6371 km), signed sum via the l'Huilier-free trapezoid formula"""
    lon, lat = np.radians(a[:, 0]), np.radians(a[:, 1])
    s = np.sum((np.roll(lon, -1) - lon) * (2 + np.sin(lat) + np.sin(np.roll(lat, -1))))
    return abs(s) * 6371.0 ** 2 / 2
def area_mi2(rings): return sum(_ring_area(np.asarray(r, float)) for r in rings) / 2.58999

def draw(img, view, rings, fill=(196, 60, 48), alpha=0.85, outline=(255, 255, 255), width=4, dash=False, ghost=False):
    """filled shape (alpha) + outline; dash=True: dashed outline only; ghost=True: faint fill + thin outline (where it started)"""
    if ghost:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for r in rings:
            p = view.pts(r); d.polygon(p, fill=tuple(fill) + (70,)); d.line(p + [p[0]], fill=tuple(fill) + (200,), width=2)
        img.alpha_composite(lay); return img
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for r in rings:
        p = view.pts(r)
        if dash:
            P = np.asarray(p + [p[0]], float); seg = np.linalg.norm(np.diff(P, axis=0), axis=1); L = np.concatenate([[0], np.cumsum(seg)])
            for s0 in np.arange(0, L[-1], 22):
                q = [tuple(np.array([np.interp(s, L, P[:, 0]), np.interp(s, L, P[:, 1])])) for s in (s0, min(s0 + 12, L[-1]))]
                d.line(q, fill=outline + (230,), width=width)
        else:
            d.polygon(p, fill=tuple(fill) + (int(255 * alpha),)); d.line(p + [p[0]], fill=outline + (255,), width=width)
    img.alpha_composite(lay); return img
