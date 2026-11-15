"""#24 drawing pieces: simple icons and light Natural Earth maps."""
import math, json
import numpy as np
from PIL import Image, ImageDraw
from pz_base import *

def person(d, x, y, s, col, outline=None):
    w = 6 if outline else 0
    d.ellipse((x - s * 0.32, y - s * 1.0, x + s * 0.32, y - s * 0.36), fill=col, outline=outline, width=w)
    d.rounded_rectangle((x - s * 0.55, y - s * 0.28, x + s * 0.55, y + s * 0.62), radius=int(s * 0.4), fill=col, outline=outline, width=w)
def virus(d, x, y, r, col=RED, spikes=12, rot=0.0):
    for i in range(spikes):
        a = rot + i * 2 * math.pi / spikes; x1, y1 = x + math.cos(a) * r * 1.45, y + math.sin(a) * r * 1.45
        d.line((x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8, x1, y1), fill=col, width=max(3, int(r * 0.14)))
        d.ellipse((x1 - r * 0.16, y1 - r * 0.16, x1 + r * 0.16, y1 + r * 0.16), fill=col)
    d.ellipse((x - r, y - r, x + r, y + r), fill=col); d.ellipse((x - r * 0.5, y - r * 0.5, x + r * 0.5, y + r * 0.5), fill=DRED)
def cell(d, x, y, r, col=TEAL, star=False, dead=False):
    c1 = GREY if dead else col; dk = tuple(int(v * 0.75) for v in c1)
    d.ellipse((x - r, y - r, x + r, y + r), fill=c1, outline=dk, width=max(3, int(r * 0.08)))
    d.ellipse((x - r * 0.38, y - r * 0.38, x + r * 0.38, y + r * 0.38), fill=tuple(int(v * 0.85) for v in c1))
    if star and not dead:
        pts = [(x + math.cos(-math.pi / 2 + i * math.pi / 5) * (r * 0.55 if i % 2 == 0 else r * 0.24),
                y - r * 1.5 + math.sin(-math.pi / 2 + i * math.pi / 5) * (r * 0.55 if i % 2 == 0 else r * 0.24)) for i in range(10)]
        d.polygon(pts, fill=YEL, outline=INK)
def microbe(d, x, y, r, col=GREEN):
    d.rounded_rectangle((x - r * 1.4, y - r * 0.7, x + r * 1.4, y + r * 0.7), radius=int(r * 0.7), fill=col, outline=(60, 110, 50), width=4)
def syringe(d, x, y, s, col=INK, fill=(210, 60, 60)):
    d.rectangle((x - s, y - s * 0.16, x + s * 0.55, y + s * 0.16), outline=col, width=6)
    d.rectangle((x - s * 0.95, y - s * 0.1, x + s * 0.1, y + s * 0.1), fill=fill)
    d.rectangle((x + s * 0.55, y - s * 0.05, x + s * 0.9, y + s * 0.05), fill=col); d.line((x + s * 0.9, y, x + s * 1.35, y), fill=col, width=4)
    d.rectangle((x - s * 1.25, y - s * 0.05, x - s, y + s * 0.05), fill=col); d.rectangle((x - s * 1.32, y - s * 0.22, x - s * 1.25, y + s * 0.22), fill=col)
def arrow(d, x0, y0, x1, y1, col=INK, w=8, k=1.0):
    if k <= 0: return
    x1, y1 = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k; d.line((x0, y0, x1, y1), fill=col, width=w)
    a = math.atan2(y1 - y0, x1 - x0); h = w * 3.2
    d.polygon([(x1, y1), (x1 - h * math.cos(a - 0.45), y1 - h * math.sin(a - 0.45)), (x1 - h * math.cos(a + 0.45), y1 - h * math.sin(a + 0.45))], fill=col)
def vial(d, x, y, s, fill=(170, 30, 40)):
    d.rounded_rectangle((x - s * 0.22, y - s, x + s * 0.22, y + s), radius=int(s * 0.22), outline=INK, width=6)
    d.rounded_rectangle((x - s * 0.17, y - s * 0.1, x + s * 0.17, y + s * 0.95), radius=int(s * 0.17), fill=fill)
    d.rectangle((x - s * 0.28, y - s * 1.15, x + s * 0.28, y - s * 0.92), fill=(70, 90, 160))
def wax_block(d, x, y, s):
    d.rounded_rectangle((x - s, y - s * 0.75, x + s, y + s * 0.75), radius=18, fill=(236, 226, 200), outline=(150, 140, 120), width=6)
    d.ellipse((x - s * 0.45, y - s * 0.3, x + s * 0.35, y + s * 0.3), fill=(222, 196, 170))
def badge(img, d=300, ring=9): return K.circle_badge(img, d, ring)
def silhouette(d=320):
    k = ("sil", d)
    if k not in IMG:
        im = Image.new("RGB", (600, 600), (196, 196, 190)); dd = ImageDraw.Draw(im)
        dd.ellipse((210, 110, 390, 320), fill=(92, 92, 96)); dd.rounded_rectangle((120, 330, 480, 700), radius=170, fill=(92, 92, 96))
        dd.text((300, 215), "?", font=F("black", 130), fill=(196, 196, 190), anchor="mm"); IMG[k] = K.circle_badge(im, d, 9)
    return IMG[k]

# ---------------------------------------------------------------- maps
_FE = []
def feats():
    if not _FE:
        g = json.load(open("D:/why habibi/_style_kit/maps/ne_10m_admin_0_countries.geojson", encoding="utf-8"))
        for f in g["features"]:
            gg = f["geometry"]; ps = gg["coordinates"] if gg["type"] == "MultiPolygon" else [gg["coordinates"]]
            _FE.append((f["properties"]["NAME"], [np.asarray(p[0], np.float32) for p in ps]))
    return _FE
def merc(lat): lat = max(-80.0, min(80.0, lat)); return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def proj(view, lon, lat):
    lo, la, wd = view; kx = W / wd
    return (lon - lo) * kx + W / 2, H / 2 - (merc(lat) - merc(la)) * kx * 180 / math.pi
def basemap(view, hi=None):
    hi = hi or {}; k = ("map", view, tuple(sorted(hi.items())))
    if k in IMG: return IMG[k]
    S = 2; im = Image.new("RGB", (W * S, H * S), (222, 231, 235)); d = ImageDraw.Draw(im); lo, la, wd = view
    for name, polys in feats():
        for p in polys:
            if p[:, 0].max() < lo - wd * 0.7 or p[:, 0].min() > lo + wd * 0.7: continue
            q = p[:: max(1, len(p) // 1500)]; xy = [(proj(view, a, b)[0] * S, proj(view, a, b)[1] * S) for a, b in q]
            if len(xy) > 2: d.polygon(xy, fill=hi.get(name, (245, 243, 237)), outline=(165, 162, 154), width=3)
    im = im.resize((W, H), Image.LANCZOS); IMG[k] = im; return im
def route(d, view, pts, k, col=RED, w=7):
    xy = [proj(view, a, b) for a, b in pts]; L = [math.dist(xy[i], xy[i + 1]) for i in range(len(xy) - 1)]; tot = sum(L) * clamp01(k)
    if tot <= 0: return
    out = [xy[0]]
    for i, l in enumerate(L):
        if tot >= l: out.append(xy[i + 1]); tot -= l
        else: f = tot / l; out.append((xy[i][0] + (xy[i + 1][0] - xy[i][0]) * f, xy[i][1] + (xy[i + 1][1] - xy[i][1]) * f)); break
    d.line(out, fill=col, width=w, joint="curve"); x, y = out[-1]; d.ellipse((x - w * 1.3, y - w * 1.3, x + w * 1.3, y + w * 1.3), fill=col)
def arc_pts(a, b, n=48, bend=0.22):
    (x0, y0), (x1, y1) = a, b; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; nx, ny = -(y1 - y0), (x1 - x0)
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * (mx + nx * bend) + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (my + ny * bend) + t * t * y1) for t in np.linspace(0, 1, n)]
def pin(c, view, ll, name, t, t0, style="yel", size=40, dy=-48):
    x, y = proj(view, *ll); d = ImageDraw.Draw(c)
    if t >= t0: r = 11 * eout((t - t0) / 0.3); d.ellipse((x - r, y - r, x + r, y + r), fill=INK, outline=(255, 255, 255), width=3)
    K.pop(c, lab(name, size, style), x, y + dy, t, t0 + 0.1)

SE_CAM = (15.3, 2.6); KIN = (15.31, -4.32); LUB = (27.48, -11.66); MBM = (23.6, -6.13); KIS = (25.19, 0.52)
PAP = (-72.34, 18.54); NYC = (-74.0, 40.71); SFO = (-122.42, 37.77)
RIVER = [(15.6, 2.4), (16.05, 1.62), (16.6, 0.2), (16.9, -1.0), (16.5, -2.2), (16.0, -3.2), (15.5, -4.1), KIN]
RAIL_LUB = [KIN, (17.5, -4.6), (20.6, -4.3), (22.4, -5.9), MBM, (25.0, -7.8), (26.2, -10.2), LUB]
RIVER_KIS = [KIN, (16.4, -3.2), (17.3, -1.0), (18.3, 0.0), (20.5, 1.2), (22.5, 1.8), (24.2, 0.9), KIS]
V_AF = (18.0, -1.0, 62.0); V_CB = (19.0, -3.0, 24.0); V_CM = (13.5, 4.8, 13.0); V_ATL = (-28.0, 14.0, 120.0); V_WORLD = (-20.0, 15.0, 220.0)
HI_CM = {"Cameroon": (214, 232, 228)}; HI_CB = {"Cameroon": (214, 232, 228), "Dem. Rep. Congo": (246, 222, 210)}
HI_ATL = {"Dem. Rep. Congo": (246, 222, 210), "Haiti": (246, 222, 210), "United States of America": (214, 232, 228)}
