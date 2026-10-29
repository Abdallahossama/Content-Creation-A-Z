"""Ep 4 map bases (Natural Earth, public domain) at five zoom levels + the places we keep pointing at."""
import sys
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
from mapcam import Base, Cam, MapBG, Route, Flow, Pulse, Dot, Label, Barrier, Ship, Area, HandCircle, HandArrow, View, YEL, RED, WHITE, NAVY

BASES = [Base("world", -60, 175, -55, 70, 16),
         Base("arabia", 26, 72, 2, 35, 110),
         Base("hormuz2", 50.5, 62.5, 22.0, 29.8, 400),
         Base("bab2", 40.0, 47.0, 9.8, 16.0, 560),
         Base("mayun2", 42.4, 44.4, 11.9, 13.6, 1400)]

HORMUZ = (56.45, 26.45); BAB = (43.40, 12.62); MAYUN = (43.42, 12.653); YANBU = (38.06, 24.09); ABQAIQ = (49.68, 25.94)
RIYADH_AIRPORT = (46.70, 24.96); SANAA = (44.21, 15.37)
PORTS = [("Ras Tanura", 50.16, 26.64), ("Basra", 47.78, 30.51), ("Kuwait", 47.98, 29.37), ("Ras Laffan", 51.53, 25.91), ("Jebel Ali", 55.03, 25.01),
         ("Kharg", 50.32, 29.24)]
EAST_WEST = [ABQAIQ, (47.0, 25.4), (44.5, 25.0), (41.5, 24.5), YANBU]
UAE_BYPASS = [(53.85, 23.65), (55.3, 24.4), (56.33, 25.12)]                       # Habshan -> Fujairah (approximate path)
RED_SEA_SOUTH = [(38.0, 23.6), (38.9, 21.3), (40.4, 18.4), (41.9, 15.6), (43.0, 13.2), (43.32, 12.75), (43.6, 12.45), (45.0, 12.1), (48.0, 12.6), (52, 13.6)]
HORMUZ_OUT = [(52.0, 26.6), (54.5, 26.4), (56.0, 26.55), (56.6, 26.3), (57.4, 25.4), (59.5, 24.0), (63, 22.5), (68, 21)]
CAPE = [(43.6, 12.4), (48, 11.6), (51.5, 6), (47, -6), (41, -18), (35, -28), (20, -36), (12, -26), (6, -10), (0, 0), (-12, 15), (-16, 28), (-10, 38)]
PERIM_RING = None                                                                 # filled in from the coastline data below

def _perim():
    import json
    c = json.load(open("D:/why habibi/_style_kit/maps/ne_10m_admin_0_countries.geojson", encoding="utf-8"))
    for f in c["features"]:
        if f["properties"]["NAME"] != "Yemen": continue
        g = f["geometry"]; ps = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for p in ps:
            xs = [q[0] for q in p[0]]; ys = [q[1] for q in p[0]]
            if abs(min(xs) - 43.39) < 0.01 and abs(min(ys) - 12.632) < 0.01: return p[0]
PERIM_RING = _perim()

if __name__ == "__main__":
    print([(b.name, b.w, b.h) for b in BASES], "perim pts:", len(PERIM_RING or []))

# base-map labels that follow the zoom (shown only while the view height in degrees is within smin..smax)
_LT, _LS, _ST, _SS = (70, 55, 35), (236, 224, 196), (200, 215, 240), (8, 14, 34)
def _land(t, lon, lat, s, smin, smax): return Label(t, lon, lat, -10, size=s, color=_LT, stroke=_LS, sw=3, smin=smin, smax=smax, base=True)
def _sea(t, lon, lat, s, smin, smax): return Label(t, lon, lat, -10, size=s, color=_ST, stroke=_SS, sw=3, smin=smin, smax=smax, base=True)
BASE_LABELS = [
    _land("Saudi Arabia", 45.0, 23.8, 34, 6, 45), _land("Iran", 54.5, 30.6, 34, 10, 45), _land("Iran", 57.3, 27.6, 30, 2.4, 10),
    _land("Oman", 57.0, 21.4, 30, 8, 45), _land("Oman", 56.25, 25.9, 26, 2.0, 8), _land("UAE", 54.3, 23.7, 26, 4, 25),
    _land("Qatar", 51.2, 25.25, 22, 4, 16), _land("Kuwait", 47.6, 29.4, 22, 5, 18), _land("Iraq", 44.5, 32.4, 30, 10, 45),
    _land("Yemen", 47.5, 15.9, 32, 6, 45), _land("Eritrea", 38.6, 15.6, 26, 6, 40), _land("Djibouti", 42.55, 11.75, 24, 3, 20),
    _land("Somalia", 47.5, 8.6, 28, 8, 45), _land("Egypt", 30.8, 26.5, 30, 12, 45), _land("Sudan", 31.5, 17.5, 30, 12, 45),
    _land("Africa", 20.0, 5.0, 44, 40, 200), _land("Asia", 90.0, 42.0, 44, 40, 200), _land("Europe", 15.0, 50.0, 40, 40, 200),
    _sea("Red Sea", 38.6, 21.2, 30, 6, 40), _sea("The Gulf", 51.4, 27.4, 30, 5, 40), _sea("Gulf of Oman", 58.7, 24.5, 26, 3, 25),
    _land("Yemen", 43.62, 12.86, 30, 0.2, 3), _land("Djibouti", 43.27, 12.43, 26, 0.2, 3),
    _sea("Arabian Sea", 62.0, 15.5, 32, 8, 60), _sea("Gulf of Aden", 48.5, 12.7, 28, 5, 40), _sea("Indian Ocean", 75.0, -5.0, 36, 40, 200)]
