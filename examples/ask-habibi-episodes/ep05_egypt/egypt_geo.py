"""Egypt map geometry for Ep 5 (approximate, traced from city coordinates; Natural Earth has no rivers in our kit)."""
import math, random
NILE = [(31.35, 21.80), (31.60, 22.30), (32.10, 22.70), (32.50, 23.20), (32.88, 23.97), (32.90, 24.09), (32.95, 24.47), (32.88, 24.98),
        (32.55, 25.29), (32.64, 25.69), (32.72, 26.16), (32.24, 26.05), (31.69, 26.56), (31.18, 27.18), (30.75, 28.10), (30.90, 28.60),
        (31.10, 29.07), (31.20, 29.60), (31.24, 30.04)]
LAKE_NASSER = NILE[:5]
ROSETTA = [(31.24, 30.04), (30.95, 30.65), (30.70, 31.05), (30.42, 31.40)]
DAMIETTA = [(31.24, 30.04), (31.30, 30.70), (31.55, 31.05), (31.81, 31.42)]
DELTA = [(31.24, 30.04), (30.55, 30.45), (29.92, 31.20), (30.40, 31.45), (31.00, 31.58), (31.81, 31.48), (32.30, 31.26), (31.95, 30.85), (31.55, 30.35)]
FAYUM = [(30.85 + 0.24 * math.cos(k * math.pi / 8), 29.30 + 0.15 * math.sin(k * math.pi / 8)) for k in range(16)]
CITY = dict(Cairo=(31.24, 30.04), Alexandria=(29.92, 31.20), Aswan=(32.90, 24.09), Luxor=(32.64, 25.69), Asyut=(31.18, 27.18),
            Minya=(30.75, 28.10), PortSaid=(32.30, 31.26), Suez=(32.55, 29.97), Siwa=(25.52, 29.20), Kharga=(30.55, 25.44),
            Dakhla=(29.00, 25.50), Sharm=(34.33, 27.92), AbuSimbel=(31.63, 22.34), WadiHalfa=(31.35, 21.80), Qattara=(27.5, 29.6),
            NewCapital=(31.75, 30.02), Toshka=(31.30, 22.80), Hurghada=(33.81, 27.26))
def valley_poly(width_deg=0.09):
    """the green strip either side of the Nile from Aswan to Cairo"""
    pts = NILE[5:]; L, R = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n; L.append((x + nx * width_deg, y + ny * width_deg)); R.append((x - nx * width_deg, y - ny * width_deg))
    return L + R[::-1]
def _inside(pt, poly):
    x, y = pt; c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1: c = not c
    return c
def people_dots(total=1080, seed=4):
    """dot-density sample, 1 dot ~ 100,000 people: ~95% valley+delta, the rest coasts, canal, oases, Sinai (illustrative)"""
    rng = random.Random(seed); V = valley_poly(0.10); out = []
    def fill(poly, n, box):
        k = 0
        while k < n:
            p = (rng.uniform(box[0], box[1]), rng.uniform(box[2], box[3]))
            if _inside(p, poly): out.append(p); k += 1
    fill(DELTA, int(total * 0.55), (29.9, 32.3, 30.0, 31.6))
    fill(V, int(total * 0.36), (30.6, 33.1, 24.0, 30.1))
    fill(FAYUM, int(total * 0.03), (30.5, 31.05, 29.1, 29.6))
    for (cx, cy), n, r in ((CITY["Suez"], 8, 0.15), ((32.27, 30.60), 8, 0.12), (CITY["Hurghada"], 4, 0.12), (CITY["Sharm"], 2, 0.1),
                           ((27.25, 31.35), 6, 0.3), (CITY["Kharga"], 2, 0.1), (CITY["Siwa"], 1, 0.05), ((33.8, 31.1), 4, 0.25), (CITY["Aswan"], 6, 0.1)):
        for _ in range(n): out.append((cx + rng.gauss(0, r), cy + rng.gauss(0, r)))
    return out
