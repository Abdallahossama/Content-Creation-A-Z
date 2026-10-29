"""Our own north-up polar map for the Andrée file (Natural Earth 10 m land, public domain), case-file look like mshorts.VMap.
Polar stereographic on a sphere, centred meridian LON0 pointing straight down, so Svalbard and the Pole read north-up.
A view = (lon_c, lat_c, km_w): the point at the frame centre and the width of the frame in km.
  pmap_panel(b, t, t0, t1) with b = dict(view=..., ops=[...], z=(z0, z1), c0, c1)   (same ops as mshorts.map_panel: pin, route, circle, label)"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, INK, BONE, RED, STEEL, TYPE, ease, clamp01
import mshorts as MS

R, LON0 = 6371.0, 20.0
def proj(lon, lat):
    r = 2 * R * math.tan(math.pi / 4 - math.radians(lat) / 2) * 0.9330          # scale true at 70 N, like EPSG:3413 (k0 = 0.933)
    a = math.radians(lon - LON0); return r * math.sin(a), r * math.cos(a)      # x east, y south (km)
def gc_km(lon1, lat1, lon2, lat2):
    p1, p2, dl = math.radians(lat1), math.radians(lat2), math.radians(lon2 - lon1)
    return 2 * R * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))
def gc_path(a, b, n=40):                                                        # points along the great circle a -> b (lon, lat)
    (l1, f1), (l2, f2) = [(math.radians(x), math.radians(y)) for x, y in (a, b)]
    v1 = np.array([math.cos(f1) * math.cos(l1), math.cos(f1) * math.sin(l1), math.sin(f1)])
    v2 = np.array([math.cos(f2) * math.cos(l2), math.cos(f2) * math.sin(l2), math.sin(f2)])
    om = math.acos(max(-1, min(1, float(v1 @ v2))))
    if om < 1e-9: return [a, b]
    out = []
    for s in np.linspace(0, 1, n):
        v = (math.sin((1 - s) * om) * v1 + math.sin(s * om) * v2) / math.sin(om)
        out.append((math.degrees(math.atan2(v[1], v[0])), math.degrees(math.asin(v[2]))))
    return out

_BASES = {}
class PMap:
    PAD = 1.3
    def __init__(s, lon_c, lat_c, km_w):
        s.key = (lon_c, lat_c, km_w); s.W, s.H = int(W * s.PAD), int(H * s.PAD)
        s.cx, s.cy = proj(lon_c, lat_c); s.k = W / km_w                         # px per km
    def xy(s, lon, lat):
        x, y = proj(lon, lat); return s.W / 2 + (x - s.cx) * s.k, s.H / 2 + (y - s.cy) * s.k
    def base(s):
        if s.key in _BASES: return _BASES[s.key]
        ss = 2; WW, HH = s.W * ss, s.H * ss
        mask = Image.new("L", (WW, HH), 0); dm = ImageDraw.Draw(mask); outl = []
        for name, rs in MS.feats():
            for r in rs:
                a = np.asarray(r)
                if a[:, 1].max() < 55: continue
                p = [(x * ss, y * ss) for x, y in (s.xy(lo, la) for lo, la in r)]
                xs, ys = [q[0] for q in p], [q[1] for q in p]
                if max(xs) < 0 or min(xs) > WW or max(ys) < 0 or min(ys) > HH: continue
                dm.polygon(p, fill=255); outl.append(p)
        f32 = np.float32; yy = np.linspace(0, 1, HH, dtype=f32)[:, None, None]
        sea = np.array((15, 16, 18), f32) * (1.05 - 0.1 * yy) * np.ones((1, WW, 1), f32)
        halo = np.asarray(mask.filter(ImageFilter.GaussianBlur(10 * ss)), f32)[..., None] / 255
        sea = sea + 10 * halo
        land = np.array((52, 51, 49), f32) * (1.05 - 0.12 * yy) + np.random.default_rng(5).normal(0, 2.2, (HH, WW, 1)).astype(f32)
        m = np.asarray(mask, f32)[..., None] / 255
        im = Image.fromarray((sea * (1 - m) + land * m).clip(0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
        for p in outl: d.line(p + [p[0]], fill=(120, 124, 128, 255), width=2 * ss)
        for lat in (75, 80, 85):                                                # latitude circles + meridians every 10 degrees
            d.line([(x * ss, y * ss) for x, y in (s.xy(lo, lat) for lo in np.linspace(-180, 180, 721))], fill=(70, 70, 72, 255), width=ss)
        for lo in range(-180, 180, 10):
            d.line([(x * ss, y * ss) for x, y in (s.xy(lo, la) for la in np.linspace(70, 90, 41))], fill=(70, 70, 72, 255), width=ss)
        _BASES[s.key] = im.resize((s.W, s.H), Image.LANCZOS); return _BASES[s.key]

def pmap_panel(b, t, t0, t1):
    V = PMap(*b["view"]); base = V.base()
    u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6)))
    z = b["z"][0] + (b["z"][1] - b["z"][0]) * u; cx = b["c0"][0] + (b["c1"][0] - b["c0"][0]) * u; cy = b["c0"][1] + (b["c1"][1] - b["c0"][1]) * u
    s = z * W / V.W * V.PAD                                                     # zoom 1.0 shows exactly km_w across the frame
    x0, y0 = cx * V.W - W / 2 / s, cy * V.H - H / 2 / s
    c = base.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + W / s, y0 + H / s)); d = ImageDraw.Draw(c)
    def T(lon, lat): x, y = V.xy(lon, lat); return ((x - x0) * s, (y - y0) * s)
    labels = []
    for op in b["ops"]:
        kind = op[0]
        if kind == "route":                                                     # ("route", [(lon, lat), ...], t_start, dur[, dashed])
            _, pts, ts, du = op[:4]; dashed = len(op) > 4 and op[4]
            tt = t - t0
            if tt < ts: continue
            path = []
            for a_, b_ in zip(pts, pts[1:]): path += gc_path(a_, b_, 30)[:-1]
            path.append(pts[-1]); q = [T(*p) for p in path]
            segl = [math.dist(q[i], q[i + 1]) for i in range(len(q) - 1)]; tot = sum(segl) or 1; want = tot * ease(clamp01((tt - ts) / du)); acc = 0; drawn = [q[0]]
            for i, sl in enumerate(segl):
                if acc + sl >= want: f = (want - acc) / sl if sl else 0; drawn.append((q[i][0] + (q[i + 1][0] - q[i][0]) * f, q[i][1] + (q[i + 1][1] - q[i][1]) * f)); break
                acc += sl; drawn.append(q[i + 1])
            if dashed:
                for i in range(0, len(drawn) - 1, 2): d.line(drawn[i:i + 2], fill=BONE, width=5)
            else:
                d.line(drawn, fill=INK, width=12, joint="curve"); d.line(drawn, fill=RED, width=6, joint="curve")
        elif kind == "pin":                                                     # ("pin", lon, lat, label, t_start[, side])
            _, lon, lat, label, ts = op[:5]; side = op[5] if len(op) > 5 else "right"
            tt = t - t0
            if tt < ts: continue
            x, y = T(lon, lat); u2 = ease((tt - ts) / 0.25); r = 11 * (1.6 - 0.6 * u2)
            d.ellipse((x - r - 5, y - r - 5, x + r + 5, y + r + 5), fill=INK); d.ellipse((x - r, y - r, x + r, y + r), fill=RED)
            if label: labels.append((label, x, y, ts, side))
        elif kind == "pole":                                                    # ("pole", t_start)
            tt = t - t0
            if tt < op[1]: continue
            x, y = T(0, 90); a = ease((tt - op[1]) / 0.3)
            d.line((x - 18, y, x + 18, y), fill=BONE, width=4); d.line((x, y - 18, x, y + 18), fill=BONE, width=4)
            labels.append(("NORTH POLE", x, y, op[1], "up"))
        elif kind == "label":                                                   # ("label", lon, lat, text, t_start)
            _, lon, lat, s_, ts = op; x, y = T(lon, lat)
            if t - t0 >= ts: L.text(c, s_, x, y, 28, STEEL, TYPE, alpha=ease((t - t0 - ts) / 0.4))
        elif kind == "dist":                                                    # ("dist", (lon, lat), (lon, lat), text, t_start): dashed line + midpoint label
            _, a_, b_, s_, ts = op; tt = t - t0
            if tt < ts: continue
            q = [T(*p) for p in gc_path(a_, b_, 40)]; n = max(2, int(len(q) * ease(clamp01((tt - ts) / 0.8))))
            for i in range(0, n - 1, 2): d.line(q[i:i + 2], fill=BONE, width=4)
            if n == len(q): mx, my = q[len(q) // 2]; labels.append((s_, mx, my, ts + 0.8, "mid"))
    f = L.font(TYPE, 34)
    for label, x, y, ts, side in labels:
        w = f.getlength(label)
        lx, ly, anc = {"up": (x, y - 52, "mm"), "down": (x, y + 52, "mm"), "right": (x + 30, y, "lm"), "left": (x - 30, y, "rm"), "mid": (x, y, "mm")}[side]
        bx = lx - (w / 2 if anc == "mm" else w if anc == "rm" else 0)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((bx - 12, ly - 26, bx + w + 12, ly + 26), fill=(10, 10, 12, 215)); c.alpha_composite(lay)
        L.typewriter(c, label, t, t0 + ts + 0.1, lx, ly, size=34, fill=BONE, cps=34, anchor=anc, cursor=False)
    L.typewriter(c, "MAP: OUR OWN, NATURAL EARTH  ·  TRACKS APPROXIMATE (MED ÖRNEN MOT POLEN, 1930)", t, t0 + 0.3, W / 2, H - 40, size=22, fill=STEEL, cps=80, anchor="mm", cursor=False)
    return L.vignette(c.convert("RGB"), 0.3) if hasattr(L, "vignette") else c

if __name__ == "__main__":
    LAUNCH, VOGEL, LAND, KVIT = (10.912, 79.723), (11.301, 79.852), (29.867, 82.933), (31.428, 80.084)
    for lo1, la1, lo2, la2 in [(*LAUNCH, 0, 90), (*LAND, 0, 90), (*LAND, *KVIT)]: print(round(gc_km(lo1, la1, lo2, la2) / 1.609), "mi")
    b = dict(view=(24.0, 83.0, 1900), ops=[("pole", 0.0), ("pin", *LAUNCH, "DANES ISLAND", 0.0, "left"), ("route", [LAUNCH, VOGEL, (25.0, 82.0), (24.22, 82.48), (15.08, 82.03), LAND], 0.2, 1.0),
                                             ("pin", *LAND, "14 JULY", 1.3), ("pin", *KVIT, "WHITE ISLAND", 1.3, "right"), ("dist", LAND, (0, 90), "488 MILES", 1.5)],
             z=(1.0, 1.0), c0=(0.5, 0.5), c1=(0.5, 0.5))
    pmap_panel(b, 4.0, 0.0, 5.0).convert("RGB").save("D:/why habibi/_newchannel/08_andree/build/_pmap_test.png"); print("ok")
