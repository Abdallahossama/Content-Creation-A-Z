"""Habibi Explains the News — Short #8 "The Strongest El Niño In 75 Years? 🌊" (post Fri 23 Oct; re-check NOAA's weekly
Niño-3.4 value on 19-22 Oct). Engine: _style_kit/tools/shortkit.py.   python render_s08.py build | qa t.. | caps | all"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, pin, W, H, YEL, SANS, IMPACT

ANOM = "+2.4°C"                                           # NOAA CPC relative Niño-3.4, week of 7 Oct 2026 (re-check)
K.setup(root="D:/why habibi/shorts/s08_el_nino/", vo="vo/s08_vo_chatterbox.wav", lat_mid=20, pyr=[10, 20, 40],
        fills=[("United States of America", (150, 168, 196))], music="Stay the Course.mp3", out="Ask_Habibi_Short08_ElNino.mp4",
        fill_alpha=0.5, cap_fix=[("El Nino", "El Niño"), ("crossed the", "across the"), ("all -time", "all-time")])
at = K.at
T = dict(heres=at("here's"), weaken=at("weaken"), warm=at("warm"), now=at("now"), september=at("september"), alltime=at("all"),
         winter=at("winter", 2), north=at("north"), strange=at("strange"), atlantic=at("atlantic"), worldwide=at("worldwide"),
         so=at("so"), blame=at("blame"))
END = K.DUR
PAC = (-118.0, 6.0, 10); NINO = (-145.0, 0.0, 22); US = (-97.0, 37.0, 16); ATL = (-62.0, 24.0, 11); WORLD = (20.0, 4.0, 5.0)
K.set_camera([(0.0, *PAC), (T["now"] - 0.4, *PAC), (T["now"] + 0.6, *NINO), (T["winter"] - 0.5, -142.0, 2.0, 21), (T["winter"] + 0.7, *US),
              (T["strange"] - 0.2, -95.0, 36.0, 16.5), (T["strange"] + 0.8, *ATL), (T["worldwide"] - 0.3, -64.0, 23.0, 11.5),
              (T["worldwide"] + 0.9, *WORLD), (T["so"] - 0.3, *WORLD), (T["so"] + 1.0, *PAC), (END + 1, *PAC)])
BOX = (-170.0, -5.0, -120.0, 5.0)                          # Niño-3.4: 5N-5S, 170W-120W

def warm_patch(c, cam, k=1.0, shift=0.0):
    """a glowing warm-water blob over the Niño region (screen space), shifted east by `shift` degrees"""
    if k <= 0: return
    x0, y0 = geo(cam, BOX[0] + shift, BOX[3] + 3); x1, y1 = geo(cam, BOX[2] + 25 + shift, BOX[1] - 3)
    w, h = int(abs(x1 - x0)), int(abs(y1 - y0))
    if w < 4 or h < 4: return
    pad = max(20, w // 4); im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((pad, pad, pad + w, pad + h), fill=(232, 72, 40, int(170 * k))); d.ellipse((pad + w * 0.2, pad + h * 0.25, pad + w * 0.75, pad + h * 0.75), fill=(255, 160, 60, int(150 * k)))
    im = im.filter(ImageFilter.GaussianBlur(max(6, w // 18))); c.alpha_composite(im, (int(min(x0, x1) - pad), int(min(y0, y1) - pad)))
def arrow(c, p0, p1, col, width=12, head=34):
    d = ImageDraw.Draw(c); d.line((p0, p1), fill=(20, 16, 12), width=width + 6); d.line((p0, p1), fill=col, width=width)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-1, 1):
        a = ang + math.pi + s * 0.45; d.line((p1, (p1[0] + head * math.cos(a), p1[1] + head * math.sin(a))), fill=col, width=width)
def band(c, cam, lat0, lat1, lon0, lon1, col, alpha):
    pts = [geo(cam, lon0, lat1), geo(cam, lon1, lat1), geo(cam, lon1, lat0), geo(cam, lon0, lat0)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(pts, fill=col + (int(alpha),)); c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14)))
PLACES = [("Indonesia: drier", (106.85, -6.21), (200, 120, 40)), ("Somalia: flood risk", (45.32, 2.05), (60, 110, 200)), ("Peru: fishing paused", (-81.11, -5.09), (200, 60, 40))]

def overlay(c, t, cam):
    lon, lat, p = cam
    loop = T["so"] + 0.4
    # warm water everywhere it is on screen (bigger on frame 1)
    if p < 30 and not (T["winter"] + 0.3 < t < T["so"]):
        sh = 18 * ease((t - T["warm"]) / 1.6) if T["warm"] <= t < T["now"] else 0.0
        warm_patch(c, cam, 1.0, sh)
    if p >= 18 and t < T["winter"]:
        x0, y0 = geo(cam, BOX[0], BOX[3]); x1, y1 = geo(cam, BOX[2], BOX[1]); warm_patch(c, cam, 1.0)
        ImageDraw.Draw(c).rectangle((x0, y0, x1, y1), outline=(255, 255, 255), width=5); serif_label(c, "Niño-3.4 region", (x0 + x1) / 2, y1 + 50, 40)
    # B1 frame 1 (+ loop): question + 83%
    if t < T["heres"] - 0.1 or t >= loop:
        t0 = 0.0 if t < T["heres"] else loop; k0 = (lambda dd: 1.0) if t0 == 0 else (lambda dd: popk(t, t0 + dd))
        put(c, outlined("IS A RECORD", 92), W / 2, 300, k0(0)); put(c, outlined("EL NIÑO COMING?", 92, emoji="🌊"), W / 2, 405, k0(0))
        put(c, outlined("83%", 170, fill=YEL, f=IMPACT, stroke=10), W / 2, 590, k0(0.1))
        put(c, pill("chance: strongest since 1950 · NOAA", 38), W / 2, 715, k0(0.2))
        serif_label(c, "Pacific Ocean", *geo(cam, -135, 18), 48)
    # B2 how it works: trade winds weaken, warm water slides east
    if T["heres"] <= t < T["now"] - 0.1:
        serif_label(c, "Pacific Ocean", *geo(cam, -135, 22), 48)
        kw = 1.0 - 0.75 * ease((t - T["weaken"]) / 0.8)
        for k, la in enumerate((12, 2, -8)):
            a = geo(cam, -100, la); b = geo(cam, -100 - 30 * kw, la); arrow(c, a, b, (255, 255, 255, int(255 * max(kw, 0.3))), width=10)
        put(c, pill("trade winds weaken", 42), W / 2, 330, popk(t, T["weaken"] - 0.3))
        if t >= T["warm"]:
            u = ease((t - T["warm"]) / 1.6); a = geo(cam, -150, -14); b = geo(cam, -150 + 55 * u, -14); arrow(c, a, b, (255, 140, 60, 255), width=16, head=44)
            put(c, pill("warm water spreads east", 42, (255, 225, 120), (150, 40, 30, 235)), W / 2, 430, popk(t, T["warm"]))
        serif_label(c, "Americas", *geo(cam, -80, 4), 44)
    # B3 + B4: the number, the record
    if T["now"] <= t < T["winter"] - 0.1:
        put(c, outlined(ANOM, 170, fill=YEL, f=IMPACT, stroke=10), W / 2, 340, popk(t, T["now"] + 0.6))
        put(c, pill("above normal · NOAA official measure, week of 7 Oct", 32), W / 2, 470, popk(t, T["now"] + 0.9))
        if t >= T["alltime"] - 0.2:
            put(c, outlined("ALL-TIME HIGH", 100, fill=(255, 255, 255)), W / 2, 590, popk(t, T["alltime"] - 0.2))
            put(c, pill("Sept surface temp, above the 1997 + 2015 peaks · Copernicus", 30), W / 2, 700, popk(t, T["alltime"] + 0.2))
    # B5 your winter
    if T["winter"] <= t < T["strange"] - 0.1:
        band(c, cam, 25, 36.5, -125, -75, (60, 110, 210), 150 * ease((t - T["winter"] - 0.6) / 0.6))
        band(c, cam, 41.5, 49, -125, -67, (235, 150, 60), 140 * ease((t - T["north"] + 0.6) / 0.6))
        if t >= T["winter"] + 0.6: put(c, outlined("WETTER", 90, fill=(200, 225, 255)), *geo(cam, -98, 31.5), popk(t, T["winter"] + 0.6))
        if t >= T["north"] - 0.6: put(c, outlined("MILDER", 90, fill=(255, 220, 160)), *geo(cam, -98, 45.5), popk(t, T["north"] - 0.6))
        put(c, pill("NOAA winter outlook, Dec-Feb", 38), W / 2, 330, popk(t, T["winter"] + 0.3))
    # B6 the Atlantic hurricane
    if T["strange"] <= t < T["worldwide"] - 0.1:
        x, y = geo(cam, -60.0, 22.0); pin(c, x, y, (200, 40, 40))
        if t >= T["atlantic"]:
            k = popk(t, T["atlantic"]); sp = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(sp)
            for r in range(3): sd.arc((20 + r * 25, 20 + r * 25, 180 - r * 25, 180 - r * 25), 30 + r * 90 + t * 200, 250 + r * 90 + t * 200, fill=(255, 255, 255, 230), width=10)
            put(c, sp, x, y - 120, k)
            put(c, outlined("LATEST FIRST HURRICANE", 74, fill=YEL), W / 2, 330, k); put(c, pill("of the satellite era (since 1966) · Weather.com", 34), W / 2, 430, popk(t, T["atlantic"] + 0.3))
        serif_label(c, "Atlantic", *geo(cam, -48, 30), 46)
    # B7 worldwide
    if T["worldwide"] <= t < loop:
        for k, (lab, ll, col) in enumerate(PLACES):
            x, y = geo(cam, *ll); kk = popk(t, T["worldwide"] + 0.9 + k * 0.25)
            if kk > 0:
                pl = pill(lab, 30); pin(c, x, y, col); put(c, pl, min(max(x, pl.width / 2 + 12), W - pl.width / 2 - 12), y - 60 - 70 * (k == 1), kk)
        put(c, outlined("347 MILLION", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["worldwide"] + 0.5))
        put(c, pill("children in areas facing unusual floods or drought · UNICEF", 30), W / 2, 445, popk(t, T["worldwide"] + 0.8))

SFX = [("pop", 0.15, -20), ("pop", T["weaken"] - 0.3, -20), ("pop", T["warm"], -20), ("pop", T["now"] + 0.6, -16), ("pop", T["alltime"] - 0.2, -18),
       ("pop", T["winter"] + 0.6, -18), ("pop", T["north"] - 0.6, -18), ("pop", T["atlantic"], -18), ("pop", T["worldwide"] + 0.5, -16), ("pop", T["so"] + 0.4, -20)]

if __name__ == "__main__":
    K.main(sys.argv, overlay, SFX)
