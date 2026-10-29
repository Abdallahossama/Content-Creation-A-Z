"""Ask Habibi Ep 5 "Why Is 95% Of Egypt Empty?" — 16:9 long-form map explainer, fast montage (a new visual every 2-3 s).
Engine: _style_kit/tools/shortkit.py (size 1920x1080). Voice: local Chatterbox clone, word timings in vo_words.json.
  python render_ep05.py build | qa t.. | caps | anchors | allseg [n] | audio | final"""
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep05_egypt")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, sprite, pin, YEL, SANS, IMPACT, SERIF
import egypt_geo as G
import longkit as L

ROOT = "D:/why habibi/5th video/"
K.setup(root=ROOT, vo="vo/ep05_vo_v2.wav", lat_mid=27, pyr=[40, 80, 160, 320, 640], size=(1920, 1080), cap_size=64,
        fills=[("Egypt", (226, 190, 128))], fill_alpha=0.55, tail=21.5, out="Ask_Habibi_Ep05_Why_Egypt_Is_Empty.mp4",
        music=[("Floating Cities.mp3", 0.0), ("Industrial Cinematic.mp3", 205.0), ("Rising Tide.mp3", 345.0), ("Stay the Course.mp3", 445.0)],
        cap_fix=[("U .S.", "US"), ("U .S", "US"), ("El Nino", "El Niño")])
W, H = K.W, K.H
WORDS = K.WORDS
def norm(s): return s.strip(" ,.?!:;\"'").lower()
def at(word, n=1, after=0.0):
    k = 0
    for w in WORDS:
        if w["s"] >= after and norm(w["w"]) == word.lower():
            k += 1
            if k == n: return w["s"]
    raise KeyError(f"{word} #{n} after {after}")

# ------------------------------------------------------------------ anchors (one per sentence/beat)
A = {}
def a(name, word, n=1, after=None):
    A[name] = at(word, n, A[after] if isinstance(after, str) else (after or 0.0)); return A[name]
a("wrong", "wrong"); a("texas", "texas"); a("river1", "river"); a("live", "live", 2); a("nobody", "nobody")
a("squeeze", "squeeze"); a("nowhere", "nowhere"); a("sense", "sense"); a("habibi", "habibi")
a("covers", "covers"); a("govt", "government"); a("seven", "7", 1, "govt"); a("desert1", "desert", 1, "seven"); a("western", "western")
a("picture", "picture"); a("roughly", "roughly"); a("vermont", "vermont"); a("together", "together"); a("strip1", "strip", 1, "together")
a("math", "math"); a("capital", "capital"); a("asia", "asia"); a("ribbon", "ribbon"); a("sky", "sky")
a("cairo_rain", "rain"); a("newyork", "york"); a("aswan1", "south", 1, "newyork"); a("zero", "zero"); a("norain", "rivers"); a("minister", "minister")
a("translation", "translation"); a("farms", "farms"); a("looks", "looks", 1, "farms"); a("valleywide", "wide"); a("cliffs", "cliffs")
a("wall", "wall"); a("qattara", "depression"); a("oases", "oases"); a("newvalley", "valley", 1, "oases"); a("sinai", "sinai")
a("isegypt", "is", 1, "sinai"); a("strange", "strange")
a("nile_len", "long"); a("ethiopia", "ethiopia"); a("flood1", "flood"); a("august", "august"); a("mud", "mud"); a("kemet", "kemet")
a("deshret", "deshret"); a("calendar", "calendar"); a("herodotus", "herodotus"); a("rule", "rule"); a("pyramids", "pyramids")
a("decided", "decided"); a("control", "control")
a("dam", "dam"); a("pharaoh", "pharaoh"); a("nasser", "nasser"); a("abusimbel", "simbel"); a("electricity", "electricity")
a("allyear", "year", 1, "electricity"); a("catch", "catch"); a("tamed", "tamed"); a("agency", "agency"); a("barely", "barely")
a("drastic", "drastic")
a("east", "east", 1, "drastic"); a("sixmillion", "planned"); a("newname", "name"); a("westnd", "west", 1, "newname"); a("manmade", "man-made", 1, "westnd")
a("toshka", "toshka"); a("fifth", "fifth"); a("housing", "housing"); a("target", "target"); a("water_problem", "problem", 1, "target")
a("share", "share", 1, "water_problem"); a("percap", "person"); a("upstream", "upstream"); a("reservoir", "reservoir")
a("land", "land", 1, "reservoir"); a("movingwater", "moving", 2, "reservoir")
a("why_end", "why", 1, "movingwater"); a("onlyriver", "only", 1, "why_end"); a("smart", "smart"); a("full1", "full"); a("twist", "twist")
a("isnt", "isn't", 1, "twist"); a("full2", "full", 1, "isnt"); a("subscribe", "subscribe", 1, "why_end")
a("sub_mid", "quick", 1, "control"); a("sub_more", "more", 1, "sub_mid"); a("sub_word", "subscribe", 1, "sub_mid")
A["endscreen"] = K.WORDS[-1]["e"] + 0.6
END = K.DUR
PH = "D:/why habibi/_media/photos_2026-10-18/"; BME = ("D:/why habibi/_media/cutouts/bm_egypt_15_45_15_38.jpg", (15.0, 45.0, 15.0, 38.0))
PHOTOS = [  # (file, t0, t1, x, y, width, tilt, credit) - real photos as proof, shown while the voice talks about them
    ("eg_nile_night_iss.jpg", A["live"] + 0.2, A["nobody"] + 1.2, 440, 500, 600, -3, "the real thing: Egypt at night from the ISS · NASA"),
    ("eg_sand_sea_iss.jpg", A["western"] + 0.6, A["picture"] - 0.1, 1580, 680, 480, 3, "the Great Sand Sea from the ISS · NASA"),
    ("eg_cairo_aerial.jpg", A["capital"] + 2.2, A["ribbon"] - 0.1, 1520, 650, 560, 2, "Cairo · Pexels / Farid Abdel Aziz"),
    ("eg_nile_modis.jpg", A["cliffs"], A["qattara"] - 0.4, 470, 640, 560, -3, "green vs sand, from space · NASA MODIS"),
    # (Tomb of Menna painting removed 18 Oct 2026: it includes female figures - user rule: no women on screen)
    ("eg_aswan_dam_iss.jpg", A["dam"] + 0.6, A["nasser"] - 0.1, 1520, 690, 560, 3, "the Aswan High Dam from the ISS · NASA"),
    ("eg_lake_nasser_iss.jpg", A["nasser"] + 2.0, A["abusimbel"] - 0.1, 470, 640, 560, -3, "Lake Nasser from the ISS · NASA"),
    ("eg_feluccas.jpg", A["tamed"], A["agency"] - 0.1, 1430, 640, 600, 2, "the Nile at Aswan · Pexels / Eyup Sayar"),
    ("eg_new_capital.jpg", A["east"] + 1.5, A["westnd"] - 0.1, 1520, 600, 330, 3, "the New Capital · Pexels / Nada Mohamed"),
    ("eg_toshka_iss.jpg", A["toshka"] + 2.2, A["housing"] - 0.1, 1430, 640, 620, 3, "Toshka farms from the ISS · NASA"),
]
K.CFG["music"] = [("Floating Cities.mp3", 0.0), ("Promises to Keep.mp3", A["nile_len"] - 2.5), ("Industrial Cinematic.mp3", A["dam"] - 1.5),
                  ("Rising Tide.mp3", A["east"] - 1.0), ("Stay the Course.mp3", A["why_end"] - 0.8)]
CH = [("THE MAP THAT LOOKS WRONG", A["covers"]), ("THE SKY THAT FORGOT TO RAIN", A["cairo_rain"] - 0.4), ("A RIVER FROM SOMEWHERE ELSE", A["nile_len"] - 2.2),
      ("THE DAM", A["dam"] - 1.2), ("ESCAPING THE RIVER", A["east"] - 0.6), ("SO... WHY?", A["why_end"] - 0.4)]

# ------------------------------------------------------------------ camera
EG = (30.0, 26.7, 92); VALLEY = (31.6, 27.2, 200); DELTA = (31.1, 30.75, 300); CAIRO = (31.3, 30.05, 560); WDES = (27.8, 27.2, 120)
QATT = (27.7, 29.6, 240); SIN = (33.9, 29.4, 210); ASW = (32.2, 23.3, 210); ABS = (31.75, 22.5, 400); NCAP = (31.55, 30.05, 420)
NDEL = (29.9, 30.5, 230); TOSH = (31.5, 23.0, 240); AFR = (33.0, 14.0, 32); EGW = (30.0, 26.7, 80)
def cam_keys():
    k = [(0.0, *EGW), (A["texas"] - 0.3, *EGW), (A["river1"] + 0.6, *EG), (A["live"] - 0.4, 30.4, 26.9, 100), (A["nobody"] - 0.3, *WDES),
         (A["squeeze"], *EG), (A["nowhere"], *NCAP), (A["sense"] + 0.2, *EG), (A["covers"], *EGW), (A["govt"] + 0.6, *EG),
         (A["western"] - 0.2, *WDES), (A["picture"], *EG), (A["roughly"] + 0.3, *VALLEY), (A["vermont"], *VALLEY), (A["capital"] - 0.3, *DELTA),
         (A["asia"], *CAIRO), (A["ribbon"], *VALLEY), (A["sky"] + 0.5, *EG), (A["aswan1"] - 0.4, *ASW), (A["norain"], *EG), (A["minister"], *VALLEY),
         (A["looks"], *EG), (A["valleywide"] - 0.3, 31.0, 28.2, 420), (A["wall"] + 0.5, 31.0, 28.2, 380), (A["qattara"] - 0.3, *QATT),
         (A["oases"], *WDES), (A["sinai"] - 0.2, *SIN), (A["isegypt"], *EG), (A["strange"] + 0.5, *EGW), (A["nile_len"], *AFR),
         (A["flood1"], 31.5, 26.0, 150), (A["mud"], *VALLEY), (A["kemet"], 31.3, 27.5, 260), (A["calendar"], *EG), (A["herodotus"], *DELTA),
         (A["pyramids"] - 0.2, 31.13, 29.98, 640), (A["decided"], *EG), (A["control"] + 0.4, *ASW), (A["nasser"] + 0.2, 32.0, 22.9, 160),
         (A["abusimbel"], *ABS), (A["electricity"], *ASW), (A["catch"], 32.4, 23.6, 300), (A["tamed"], *EG), (A["agency"], *DELTA),
         (A["drastic"], *EG), (A["east"], *NCAP), (A["westnd"], *NDEL), (A["toshka"] - 0.2, *TOSH), (A["housing"], *EGW), (A["water_problem"], *EG),
         (A["share"], *ASW), (A["upstream"] - 0.3, *AFR), (A["land"], *EGW), (A["why_end"], *EG), (A["onlyriver"] + 0.5, *VALLEY),
         (A["smart"], *DELTA), (A["twist"], *EGW), (A["subscribe"], *EGW), (END + 2, *EGW)]
    out = []
    for t, x, y, p in sorted(k):
        if out and t <= out[-1][0] + 0.05: t = out[-1][0] + 0.05
        out.append((t, x, y, p))
    held = []                                                     # arrive, slow push-in, then a quick 1.1 s move to the next shot
    for (t0, x0, y0, p0), (t1, x1, y1, p1) in zip(out, out[1:]):
        held.append((t0, x0, y0, p0))
        if t1 - t0 > 2.6: held.append((t1 - 1.1, x0, y0, p0 * 1.07))
    held.append(out[-1])
    return held
K.set_camera(cam_keys())

# ------------------------------------------------------------------ geography drawing (screen space, crisp at any zoom)
VALLEY_POLY = G.valley_poly(0.09); DOTS = G.people_dots(1100)
def poly_px(cam, pts): return [geo(cam, *p) for p in pts]
def layer(c, draw_fn, alpha=255, blur=0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(lay))
    if blur: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 255: lay.putalpha(lay.split()[3].point(lambda v: v * alpha // 255))
    c.alpha_composite(lay)
def draw_nile(c, cam, green=0.85, glow=False, black=False):
    p = cam[2]; wl = max(3, int(p / 55)); col = (24, 18, 14) if black else ((255, 205, 100) if glow else (60, 150, 80))
    def f(d):
        d.polygon(poly_px(cam, VALLEY_POLY), fill=col + (int(220 * green),)); d.polygon(poly_px(cam, G.DELTA), fill=col + (int(200 * green),))
        d.polygon(poly_px(cam, G.FAYUM), fill=col + (int(190 * green),))
    layer(c, f, blur=1 if p < 150 else 2)
    def r(d):
        d.line(poly_px(cam, G.LAKE_NASSER), fill=(70, 140, 210, 255), width=wl * 3, joint="curve")
        for line in (G.NILE[4:], G.ROSETTA, G.DAMIETTA): d.line(poly_px(cam, line), fill=(52, 120, 200, 255), width=wl, joint="curve")
    layer(c, r)
    if glow: layer(c, f, alpha=200, blur=22); layer(c, f, alpha=160, blur=8)
def night(c, k):
    if k <= 0: return
    c.alpha_composite(Image.new("RGBA", (W, H), (6, 8, 20, int(205 * k))))
def dots(c, cam, k, t0, t, col=(255, 214, 110)):
    if k <= 0: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = max(2, cam[2] / 60)
    for i, (x, y) in enumerate(DOTS):
        u = ease((t - t0 - (i % 97) * 0.012) / 0.4)
        if u <= 0: continue
        px, py = geo(cam, x, y); d.ellipse((px - r * u, py - r * u, px + r * u, py + r * u), fill=col + (int(235 * k),))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(2.5))); c.alpha_composite(lay)
import mapkit as _MK
EG_RING = max((r for n, rs in _MK._load() if n == "Egypt" for r in rs), key=len)[::2]
def desert_tint(c, cam, k, col=(200, 60, 40)):
    """tint Egypt's land outside the green strip"""
    if k <= 0: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon(poly_px(cam, EG_RING), fill=col + (int(120 * k),)); d.polygon(poly_px(cam, VALLEY_POLY), fill=(0, 0, 0, 0)); d.polygon(poly_px(cam, G.DELTA), fill=(0, 0, 0, 0))
    c.alpha_composite(lay)
def place(c, cam, name, ll, k=1.0, col=(200, 40, 40), dx=0, dy=-46, size=34):
    if k <= 0: return
    x, y = geo(cam, *ll); pin(c, x, y, col); put(c, pill(name, size), x + dx, y + dy, k)

# ------------------------------------------------------------------ graphic cards
def panel(c, box, a=210):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle(box, 36, fill=(22, 16, 12, a)); c.alpha_composite(lay)
    return ImageDraw.Draw(c)
def fitw(im, maxw=1220):
    if im.width <= maxw: return im
    k = maxw / im.width; return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
def big(c, text, t, t0, y=250, size=150, col=YEL, sub=None, sub_y=None):
    if t < t0: return
    put(c, fitw(outlined(text, size, fill=col, f=IMPACT, stroke=10)), W / 2, y, popk(t, t0))
    if sub: put(c, pill(sub, 40), W / 2, sub_y or y + size * 0.75, popk(t, t0 + 0.15))
def headline(c, text, t, t0, y=150, size=86, emoji=None):
    if t < t0: return
    put(c, fitw(outlined(text, size, emoji=emoji)), W / 2, y, popk(t, t0))
def chapter_card(c, t):
    for i, (name, t0) in enumerate(CH):
        if t0 - 0.05 <= t < t0 + 1.6:
            u = (t - t0) / 1.6; k = ease(min(1, u * 4)) * (1 - ease(max(0, (u - 0.75) * 4)))
            c.alpha_composite(Image.new("RGBA", (W, H), (14, 10, 8, int(200 * k))))
            put(c, outlined(f"{i + 1}" if i < 5 else "", 200, fill=YEL, f=IMPACT, stroke=10), W / 2, H / 2 - 120, k)
            put(c, outlined(name, 96), W / 2 + (1 - k) * 200, H / 2 + 60, k)
def rain_bars(c, t, t0):
    d = panel(c, (360, 300, 1560, 860), 225); data = [("CAIRO", 25, A["cairo_rain"]), ("NEW YORK", 1016, A["newyork"]), ("ASWAN", 1.2, A["aswan1"])]
    d.text((W / 2, 350), "Rain per year (mm)", font=font(SANS, 44), fill=(235, 225, 210), anchor="mm")
    for k, (lab, mm, tt) in enumerate(data):
        x = 560 + k * 400; u = ease((t - tt) / 1.0); h = 380 * (mm / 1016) ** 0.5 * u
        d.rounded_rectangle((x - 70, 800 - max(h, 4 if u > 0 else 0), x + 70, 800), 14, fill=(70, 140, 210) if lab != "NEW YORK" else (110, 160, 220))
        d.text((x, 830), lab, font=font(SANS, 38), fill=(255, 255, 255), anchor="mm")
        if u > 0.05: d.text((x, 800 - h - 34), f"{mm * u:,.0f}" if mm > 2 else f"{mm * u:.1f}", font=font(IMPACT, 54), fill=YEL, anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))
def compare_card(c, t, t0):
    d = panel(c, (260, 250, 1660, 840), 225)
    d.text((W / 2, 300), "Same area, very different crowds", font=font(SANS, 44), fill=(235, 225, 210), anchor="mm")
    for k, (lab, n, col, tt) in enumerate((("Vermont + New Hampshire", 2, (110, 160, 220), A["together"]), ("Egypt's green strip", 100, (90, 170, 90), A["strip1"]))):
        y = 430 + k * 220; u = ease((t - tt) / 1.2); d.text((320, y - 60), lab, font=font(SANS, 44), fill=(255, 255, 255))
        for i in range(int(50 * min(1, n / 100) * u) if n > 2 else (1 if u > 0.1 else 0)):
            xx = 330 + (i % 25) * 50; yy = y + (i // 25) * 44; d.ellipse((xx, yy, xx + 34, yy + 34), fill=col)
        if u > 0.1: d.text((1600, y + 20), f"~{n} million" if n > 2 else "~2 million", font=font(IMPACT, 60), fill=YEL, anchor="rm", stroke_width=4, stroke_fill=(10, 10, 10))
def calendar_wheel(c, t, t0):
    d = panel(c, (560, 230, 1360, 880), 220); cx, cy, r = W / 2, 560, 250
    names = [("AKHET", "Inundation", (60, 120, 200)), ("PERET", "Emergence", (70, 150, 80)), ("SHEMU", "Harvest", (200, 160, 60))]
    for k, (nm, sub, col) in enumerate(names):
        u = ease((t - t0 - k * 0.3) / 0.6)
        if u <= 0: continue
        d.pieslice((cx - r, cy - r, cx + r, cy + r), -90 + k * 120, -90 + k * 120 + 120 * u, fill=col, outline=(20, 16, 12), width=6)
        ang = math.radians(-90 + k * 120 + 60); tx, ty = cx + r * 0.58 * math.cos(ang), cy + r * 0.58 * math.sin(ang)
        d.text((tx, ty - 18), nm, font=font(IMPACT, 54), fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))
        d.text((tx, ty + 30), sub, font=font(SANS, 30), fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(10, 10, 10))
    d.text((cx, 280), "Three seasons, set by the river", font=font(SANS, 40), fill=(235, 225, 210), anchor="mm")
def pct_bar(c, t, t0):
    d = panel(c, (260, 300, 1660, 800), 225); x0, x1 = 340, 1580; S = 20.0
    d.text((W / 2, 350), "Share of Egypt that is inhabited (housing ministry)", font=font(SANS, 40), fill=(235, 225, 210), anchor="mm")
    d.rounded_rectangle((x0, 520, x1, 600), 20, fill=(200, 160, 110))
    for lab, v, tt, col, ly in (("2014", 7, t0, (90, 170, 90), 470), ("2026", 14, A["housing"] + 2.5, (60, 140, 70), 650), ("2030 target", 17, A["target"], (40, 110, 60), 430)):
        u = ease((t - tt) / 0.8)
        if u <= 0: continue
        xv = x0 + (x1 - x0) * v / S * u; d.rounded_rectangle((x0, 520, xv, 600), 20, fill=col)
        d.line((xv, 500, xv, 620), fill=(255, 255, 255), width=4); d.text((xv, ly), f"{lab}: {v}%", font=font(SANS, 36), fill=(255, 255, 255), anchor="mm")
    d.text((x0, 740), "scale: 0-20% of the country", font=font(SANS, 30), fill=(200, 190, 175), anchor="lm"); d.text((x1, 740), "everything else: desert", font=font(SANS, 30), fill=(235, 225, 210), anchor="rm")
def water_card(c, t, t0):
    d = panel(c, (300, 300, 1620, 820), 225)
    d.text((W / 2, 350), "Water per person per year", font=font(SANS, 44), fill=(235, 225, 210), anchor="mm")
    for k, (lab, v, col) in enumerate((("Egypt today (water minister)", 500, (200, 80, 60)), ("Scarcity line", 1000, (200, 160, 60)))):
        y = 470 + k * 160; u = ease((t - t0 - k * 0.6) / 0.9); d.text((360, y - 50), lab, font=font(SANS, 38), fill=(255, 255, 255))
        d.rounded_rectangle((360, y, 360 + 1100 * v / 1000 * u, y + 70), 18, fill=col)
        if u > 0.1: d.text((380 + 1100 * v / 1000 * u, y + 35), f"{v * u:,.0f} m³", font=font(IMPACT, 50), fill=YEL, anchor="lm", stroke_width=4, stroke_fill=(10, 10, 10))
    d.text((W / 2, 780), "500 m³ = what experts call absolute water scarcity", font=font(SANS, 32), fill=(255, 225, 120), anchor="mm")
def crane(x, y, s=1.0):
    im = Image.new("RGBA", (int(220 * s), int(260 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = s
    d.line((60 * k, 250 * k, 60 * k, 30 * k), fill=(240, 190, 40, 255), width=int(10 * k)); d.line((20 * k, 40 * k, 210 * k, 40 * k), fill=(240, 190, 40, 255), width=int(9 * k))
    d.line((180 * k, 40 * k, 180 * k, 120 * k), fill=(40, 40, 40, 255), width=int(3 * k)); d.rectangle((165 * k, 120 * k, 195 * k, 140 * k), fill=(40, 40, 40, 255))
    return im
CRANE = crane(0, 0, 0.9)

# ------------------------------------------------------------------ the montage
def overlay(c, t, cam):
    lon, lat, p = cam
    # base layers: Nile + green strip almost always on
    kemet_on = A["kemet"] <= t < A["calendar"]
    nightk = 1.0 if A["live"] - 0.3 <= t < A["nobody"] else (max(0, 1 - (t - A["nobody"]) / 0.6) if A["nobody"] <= t < A["nobody"] + 0.6 else 0)
    night(c, nightk)
    if kemet_on: desert_tint(c, cam, 1.0, (190, 60, 40))
    draw_nile(c, cam, green=0.9 if not kemet_on else 0.0, glow=nightk > 0.5)
    if kemet_on: draw_nile(c, cam, black=True)
    L.real_map(c, cam, max(L.fade(t, A["covers"] - 0.3, A["seven"] + 1.2, 0.6), L.fade(t, A["why_end"] - 0.2, A["smart"] - 0.2, 0.6)), *BME)   # real satellite map now and then
    # opening: dots (each ~100,000 people)
    if A["live"] - 0.3 <= t < A["squeeze"]:
        dots(c, cam, 1.0, A["live"] - 0.3, t)
        if t < A["nobody"]: put(c, pill("1 dot = about 100,000 people (illustrative)", 34), W / 2, 980 - 110, popk(t, A["live"]))
    if A["nobody"] <= t < A["squeeze"]: desert_tint(c, cam, ease((t - A["nobody"]) / 0.6))
    # labels of the big places on wide views
    if p < 130 and not (A["live"] - 0.3 <= t < A["nobody"]):
        for nm, ll in (("Libya", (25.6, 27.5)), ("Sudan", (30.0, 21.0)), ("Mediterranean Sea", (28.5, 32.6)), ("Red Sea", (35.6, 25.0))):
            serif_label(c, nm, *geo(cam, *ll), 38, alpha=0.9)
    # ---- HOOK
    if t < A["texas"]: headline(c, "WHY IS 95% OF EGYPT EMPTY?", t, 0.0, y=170)
    if A["texas"] <= t < A["river1"]:
        big(c, "≈ TEXAS + NEW MEXICO", t, A["texas"] - 0.2, y=170, size=110, sub="Egypt's size · Library of Congress")
    if A["river1"] <= t < A["live"] - 0.3:
        big(c, "~95%", t, A["river1"] - 0.1, y=190, size=170, sub="of Egyptians live within 20 km of the Nile · CIA")
    if A["live"] - 0.3 <= t < A["nobody"]: headline(c, "~110 MILLION PEOPLE", t, A["live"], y=150, size=96)
    if A["nobody"] <= t < A["squeeze"]: headline(c, "...AND ALMOST NOBODY HERE", t, A["nobody"], y=150, size=86)
    if A["squeeze"] <= t < A["nowhere"]:
        headline(c, "WHY SQUEEZE ONTO THIS?", t, A["squeeze"], y=150, size=90, emoji="🤔")
        place(c, cam, "the green strip", (31.2, 27.2), popk(t, A["squeeze"] + 0.5), (60, 150, 80))
    if A["nowhere"] <= t < A["sense"] - 1.2:                      # gone before the camera pulls out (user: leftover crane looked unprofessional)
        place(c, cam, "a brand new capital", G.CITY["NewCapital"], popk(t, A["nowhere"] + 0.3), dy=60)
        cx_, cy_ = geo(cam, *G.CITY["NewCapital"]); put(c, CRANE, cx_ + 120, cy_ + 30, popk(t, A["nowhere"] + 0.5), anchor="b")
    if A["sense"] <= t < A["habibi"]: headline(c, "BY THE END, THIS MAP MAKES SENSE", t, A["sense"], y=150, size=74)
    if A["habibi"] <= t < A["covers"] - 0.1:
        put(c, sprite("host_cool", 520), 1560, 1020, popk(t, A["habibi"]), anchor="b")
        headline(c, "THE MAP THAT LOOKS WRONG", t, A["habibi"] + 0.6, y=150, size=86)
    # ---- CH1
    if A["covers"] + 1.6 <= t < A["govt"]: big(c, "~1,000,000 km²", t, A["covers"] + 1.6, y=170, size=120, sub="Egypt's total area · CIA")
    if A["govt"] <= t < A["desert1"]:
        big(c, "7%", t, A["govt"] + 1.0, y=200, size=200, sub="inhabited in 2014 · Egypt's government")
        put(c, sprite("diplomat", 380), 300, 1040, popk(t, A["govt"]), anchor="b")
    if A["desert1"] <= t < A["picture"]:
        desert_tint(c, cam, ease((t - A["desert1"]) / 0.5))
        if t >= A["western"]: place(c, cam, "Western Desert ≈ the size of Texas", (27.5, 26.2), popk(t, A["western"]), (200, 60, 40), size=40)
    if A["picture"] <= t < A["together"]:
        if t >= A["roughly"]:
            u = 0.5 + 0.5 * math.sin((t - A["roughly"]) * 6); layer(c, lambda d: d.polygon(poly_px(cam, VALLEY_POLY), outline=(255, 230, 120, 255), width=6), alpha=int(150 + 100 * u))
            big(c, "~5% OF THE LAND", t, A["roughly"], y=170, size=110)
        else: big(c, "100,000,000+", t, A["picture"] + 1.6, y=170, size=120, sub="95% of Egyptians")
        if t >= A["vermont"]: put(c, pill("≈ Vermont + New Hampshire", 46, (255, 225, 120)), W / 2, 300, popk(t, A["vermont"]))
    if A["together"] <= t < A["math"]: compare_card(c, t, A["together"])
    if A["math"] <= t < A["capital"]:
        big(c, "~2,000 PER KM²", t, A["math"] + 0.4, y=200, size=130, sub="my rough math · ~19x Egypt's average")
    if A["capital"] <= t < A["ribbon"]:
        place(c, cam, "Greater Cairo", G.CITY["Cairo"], popk(t, A["capital"] + 0.2))
        big(c, "25.6 MILLION", t, A["capital"] + 1.6, y=170, size=120, sub="Greater Cairo · UN 2025")
        if t >= A["asia"]: put(c, pill("the only city outside Asia in the world's top 10", 40, (255, 225, 120)), W / 2, 330, popk(t, A["asia"]))
    if A["ribbon"] <= t < A["cairo_rain"] - 0.4:
        headline(c, "A WHOLE COUNTRY ON A RIBBON", t, A["ribbon"], y=150, size=86)
        if t >= A["sky"]: put(c, outlined("THE REASON IS IN THE SKY", 70, fill=YEL), W / 2, 260, popk(t, A["sky"]))
    # ---- CH2
    if A["cairo_rain"] + 1.2 <= t < A["zero"] + 0.2: rain_bars(c, t, A["cairo_rain"])
    if A["zero"] + 0.2 <= t < A["minister"]:
        headline(c, "NO RAIN = NO RIVERS", t, A["zero"] + 0.2, y=150, size=96)
        if t >= A["norain"]: put(c, outlined("...EXCEPT ONE", 90, fill=(120, 190, 255)), W / 2, 270, popk(t, A["norain"] + 0.6))
    if A["minister"] <= t < A["translation"]:
        big(c, "~98%", t, A["minister"] + 0.8, y=200, size=200, col=(120, 190, 255), sub="of Egypt's water comes from the Nile · water minister, Feb 2026")
        put(c, sprite("scientist", 380), 300, 1040, popk(t, A["minister"]), anchor="b")
    if A["translation"] <= t < A["looks"]:
        headline(c, "TRANSLATION?", t, A["translation"], y=150, size=96)
        for k2, (lab, tt) in enumerate((("no water", A["translation"] + 1.0), ("no farms", A["farms"]), ("no food", A["farms"] + 0.5), ("no one", A["farms"] + 1.0))):
            if t >= tt: put(c, pill(lab, 50, (255, 225, 120), (150, 40, 30, 235)), 420 + k2 * 360, 300, popk(t, tt))
    if A["looks"] <= t < A["valleywide"]: dots(c, cam, 1.0, A["looks"], t)
    if A["valleywide"] <= t < A["qattara"]:
        big(c, "< 20 KM WIDE", t, A["valleywide"] + 0.2, y=170, size=130, sub="the Nile valley, in most places")
        if t >= A["cliffs"]: put(c, sprite("egyptian_galabeya", 360), 1600, 1030, popk(t, A["cliffs"]), anchor="b")
        if t >= A["wall"]: put(c, outlined("NOT A GRADIENT. A WALL.", 76, fill=YEL), W / 2, 300, popk(t, A["wall"]))
    if A["qattara"] <= t < A["oases"]:
        place(c, cam, "Qattara Depression", (27.7, 29.8), popk(t, A["qattara"]), (120, 60, 30), dy=60)
        big(c, "-133 m", t, A["qattara"] + 1.2, y=190, size=150, sub="below sea level · NASA")
    if A["oases"] <= t < A["sinai"]:
        for k2, (nm, ll) in enumerate((("Siwa", G.CITY["Siwa"]), ("Dakhla", G.CITY["Dakhla"]), ("Kharga", G.CITY["Kharga"]))):
            place(c, cam, nm, ll, popk(t, A["oases"] + 0.3 + k2 * 0.25), (60, 150, 80))
        if t >= A["newvalley"]: big(c, "< 300,000 PEOPLE", t, A["newvalley"] + 0.3, y=170, size=110, sub="New Valley province · CAPMAS, Sep 2026")
    if A["sinai"] <= t < A["isegypt"]:
        big(c, "~600,000", t, A["sinai"] + 0.8, y=170, size=140, sub="the whole Sinai peninsula · CAPMAS, Sep 2026")
    if A["isegypt"] <= t < A["nile_len"] - 2.2:
        headline(c, "THE RIVER IS EGYPT", t, A["isegypt"], y=150, size=96)
        if t >= A["strange"]: put(c, outlined("...BUT ITS WATER ISN'T FROM EGYPT", 70, fill=YEL), W / 2, 260, popk(t, A["strange"] + 0.4))
    # ---- CH3
    if A["nile_len"] <= t < A["flood1"]:
        draw_full_nile(c, cam, t, A["nile_len"])
        big(c, "~6,650 KM", t, A["nile_len"] + 0.3, y=150, size=120, sub="only ~1,600 km in Egypt")
        if t >= A["ethiopia"]:
            place(c, cam, "Ethiopian Highlands", (38.5, 10.0), popk(t, A["ethiopia"]), (60, 120, 200))
            place(c, cam, "Lake Victoria", (33.0, -1.0), popk(t, A["ethiopia"] + 0.4), (60, 120, 200))
    if A["flood1"] <= t < A["mud"]:
        u = 0.5 + 0.5 * math.sin((t - A["flood1"]) * 3); layer(c, lambda d: d.polygon(poly_px(cam, G.valley_poly(0.16)), fill=(70, 140, 210, int(120 + 80 * u))))
        headline(c, "EVERY YEAR: THE FLOOD", t, A["flood1"], y=150, size=90, emoji="🌊")
        if t >= A["august"]: put(c, pill("usually Aug · Sep · Oct · Library of Congress", 40), W / 2, 260, popk(t, A["august"]))
    if A["mud"] <= t < A["kemet"]: headline(c, "THE GIFT: BLACK MUD", t, A["mud"] + 0.3, y=150, size=90)
    if A["kemet"] <= t < A["calendar"]:
        put(c, pill("KEMET", 120, (25, 22, 20), (245, 235, 215, 235)), 640, 180, popk(t, A["kemet"])); put(c, pill("the Black Land", 40), 640, 300, popk(t, A["kemet"] + 0.3))
        if t >= A["deshret"]:
            put(c, outlined("DESHRET", 140, fill=(200, 60, 40), stroke=10), 1300, 180, popk(t, A["deshret"])); put(c, pill("the Red Land", 40), 1300, 290, popk(t, A["deshret"] + 0.3))
    if A["calendar"] <= t < A["herodotus"]: calendar_wheel(c, t, A["calendar"])
    if A["herodotus"] <= t < A["rule"]:
        put(c, outlined("\"THE RIVER'S GIFT\"", 100, fill=YEL), W / 2, 170, popk(t, A["herodotus"] + 0.6)); put(c, pill("Herodotus, Histories 2.5", 38), W / 2, 280, popk(t, A["herodotus"] + 0.9))
    if A["rule"] <= t < A["pyramids"]:
        headline(c, "LIVE WHERE THE FLOOD REACHES", t, A["rule"] + 0.8, y=150, size=80)
        if t >= A["rule"] + 2.8: put(c, outlined("BURY YOUR DEAD WHERE IT DOESN'T", 70, fill=YEL), W / 2, 260, popk(t, A["rule"] + 2.8))
    if A["pyramids"] <= t < A["decided"]:
        x, y = geo(cam, 31.134, 29.979); tri = Image.new("RGBA", (300, 200), (0, 0, 0, 0)); td = ImageDraw.Draw(tri)
        for k2, (ox, s2) in enumerate(((0, 1.0), (110, 0.8), (190, 0.55))): td.polygon([(20 + ox, 190), (20 + ox + 120 * s2, 190 - 150 * s2), (20 + ox + 240 * s2, 190)], fill=(222, 190, 120, 255), outline=(120, 90, 50, 255))
        put(c, tri, x - 60, y + 40, popk(t, A["pyramids"]), anchor="b"); place(c, cam, "Giza: on the desert edge", (31.134, 29.979), popk(t, A["pyramids"] + 0.4), dy=-230)
    if A["decided"] <= t < A["sub_mid"] - 0.2:
        headline(c, "5,000 YEARS: THE RIVER DECIDED", t, A["decided"], y=150, size=80)
        if t >= A["control"]: put(c, outlined("THEN EGYPT DECIDED TO CONTROL IT", 66, fill=YEL), W / 2, 260, popk(t, A["control"] + 0.3))
    # ---- CH4
    if A["dam"] <= t < A["nasser"]:
        x, y = geo(cam, 32.878, 23.971); layer(c, lambda d: d.line((x - 70, y - 20, x + 70, y + 20), fill=(90, 90, 96, 255), width=18))
        place(c, cam, "Aswan High Dam", (32.878, 23.971), popk(t, A["dam"] + 0.2), (60, 60, 70), dy=-60)
        big(c, "1970", t, A["dam"] + 1.4, y=170, size=150)
        if t >= A["pharaoh"]: put(c, outlined("IT STOPPED THE FLOOD", 76, fill=YEL), W / 2, 290, popk(t, A["pharaoh"] + 1.4))
    if A["nasser"] <= t < A["abusimbel"]:
        layer(c, lambda d: d.line(poly_px(cam, G.LAKE_NASSER), fill=(60, 130, 210, 255), width=int(max(10, cam[2] / 9)), joint="curve"))
        place(c, cam, "Lake Nasser", (32.0, 22.9), popk(t, A["nasser"]), (60, 120, 200)); big(c, "~500 KM LONG", t, A["nasser"] + 1.0, y=170, size=120, sub="reaching into Sudan · FAO")
    if A["abusimbel"] <= t < A["electricity"]:
        place(c, cam, "Abu Simbel", G.CITY["AbuSimbel"], popk(t, A["abusimbel"]), (150, 110, 60))
        if t >= A["abusimbel"] + 1.6:
            st = Image.new("RGBA", (560, 130), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); red = (200, 30, 30, 240)
            sd.rounded_rectangle((5, 5, 555, 125), 16, outline=red, width=8); sd.text((280, 65), "MOVED UPHILL", font=font(IMPACT, 80), fill=red, anchor="mm")
            put(c, st.rotate(7, expand=True), W / 2, 260, popk(t, A["abusimbel"] + 1.6))
    if A["electricity"] <= t < A["catch"]:
        big(c, "~50%", t, A["electricity"] + 0.6, y=190, size=180, sub="of Egypt's electricity in 1970 · NASA")
        if t >= A["allyear"]: put(c, sprite("egyptian_galabeya", 380), 300, 1040, popk(t, A["allyear"]), anchor="b"); put(c, pill("crops all year", 46, (255, 225, 120)), W / 2, 430, popk(t, A["allyear"]))
    if A["catch"] <= t < A["agency"]:
        headline(c, "THE CATCH", t, A["catch"], y=150, size=100)
        if t >= A["catch"] + 1.2: put(c, pill("the black mud now sinks to the bottom of Lake Nasser", 42, (255, 225, 120)), W / 2, 260, popk(t, A["catch"] + 1.2))
    if A["agency"] <= t < A["drastic"]:
        n = 109.5e6 * ease((t - A["agency"] - 0.4) / 1.6); dots(c, cam, 1.0, A["agency"], t)
        put(c, outlined(f"{int(n):,}", 140, fill=YEL, f=IMPACT, stroke=10), W / 2, 170, popk(t, A["agency"]))
        put(c, pill("Egyptians · CAPMAS population clock, Sep 2026", 38), W / 2, 280, popk(t, A["agency"] + 0.3))
        if t >= A["barely"]: put(c, outlined("THE STRIP BARELY MOVED", 70), W / 2, 380, popk(t, A["barely"]))
    if A["drastic"] <= t < A["east"] - 0.6: headline(c, "PLAN: MOVE PEOPLE INTO THE DESERT", t, A["drastic"] + 0.4, y=150, size=76)
    # ---- CH5
    if A["east"] <= t < A["westnd"]:
        for k2 in range(3): put(c, CRANE, *geo(cam, G.CITY["NewCapital"][0] + 0.10 + k2 * 0.09, G.CITY["NewCapital"][1] - 0.10 - k2 * 0.04), popk(t, A["east"] + 0.6 + k2 * 0.2), anchor="b")
        place(c, cam, "The New Capital", G.CITY["NewCapital"], popk(t, A["east"] + 0.3), (60, 60, 70), dx=120, dy=60); place(c, cam, "Cairo", G.CITY["Cairo"], popk(t, A["east"] + 0.2), dx=-90, dy=-40)
        if t >= A["sixmillion"]: big(c, "6 MILLION", t, A["sixmillion"] + 0.5, y=170, size=120, sub="planned residents · Dezeen")
        if t >= A["newname"]: put(c, pill("renamed \"The New Capital\", Nov 2025", 42, (255, 225, 120)), W / 2, 330, popk(t, A["newname"]))
    if A["westnd"] <= t < A["toshka"]:
        u = ease((t - A["manmade"]) / 2.0) if t >= A["manmade"] else 0
        pts = [(28.95, 30.85), (29.35, 30.70), (29.75, 30.55), (30.15, 30.45), (30.55, 30.35)]; seg = pts[: max(2, int(2 + u * (len(pts) - 2)))]
        layer(c, lambda d: d.line(poly_px(cam, seg), fill=(60, 140, 220, 255), width=10, joint="curve"))
        place(c, cam, "New Delta (approx.)", (29.6, 30.45), popk(t, A["westnd"] + 0.3), (60, 150, 80), dy=60)
        if t >= A["manmade"]: big(c, "~170 KM MAN-MADE RIVER", t, A["manmade"] + 0.3, y=170, size=96, sub="New Delta, opened May 2026 · The National")
    if A["toshka"] <= t < A["housing"]:
        place(c, cam, "Toshka", (30.9, 23.1), popk(t, A["toshka"] + 0.2), (60, 150, 80)); big(c, "1997", t, A["toshka"] + 0.8, y=170, size=130, sub="plan: a second Nile valley")
        if t >= A["fifth"]: put(c, pill("goal: move 1 in 5 Egyptians · by 2012: < 10% of its farming goal (The National)", 34, (255, 225, 120)), W / 2, 330, popk(t, A["fifth"]))
    if A["housing"] <= t < A["water_problem"]: pct_bar(c, t, A["housing"] + 1.0)
    if A["water_problem"] <= t < A["share"]: headline(c, "THE SAME PROBLEM: WATER", t, A["water_problem"], y=150, size=96, emoji="💧")
    if A["share"] <= t < A["percap"]: big(c, "55.5 BILLION m³", t, A["share"] + 0.6, y=180, size=110, col=(120, 190, 255), sub="Egypt's Nile share since 1959 · FAO")
    if A["percap"] <= t < A["upstream"]: water_card(c, t, A["percap"])
    if A["upstream"] <= t < A["land"]:
        place(c, cam, "Ethiopia's giant dam (GERD)", (35.09, 11.22), popk(t, A["upstream"] + 0.6), (60, 60, 70))
        draw_full_nile(c, cam, t, A["upstream"] - 5)
        if t >= A["reservoir"]: big(c, "74 BILLION m³", t, A["reservoir"] + 0.3, y=170, size=110, col=(120, 190, 255), sub="its reservoir · inaugurated Sep 2025 · CNN, ASCE")
    if A["land"] <= t < A["why_end"] - 0.4:
        headline(c, "PLENTY OF LAND", t, A["land"], y=150, size=96)
        if t >= A["movingwater"]: put(c, outlined("IT'S ABOUT MOVING WATER", 90, fill=(120, 190, 255)), W / 2, 270, popk(t, A["movingwater"]))
    # ---- END
    if A["why_end"] + 1.6 <= t < A["smart"]:
        headline(c, "ALMOST NO RAIN + ONE RIVER", t, A["why_end"] + 1.6, y=150, size=86)
    if A["smart"] <= t < A["twist"]:
        dots(c, cam, 1.0, A["smart"], t)
        if t >= A["full1"]: put(c, outlined("THE STRIP IS FULL", 96, fill=YEL), W / 2, 160, popk(t, A["full1"]))
    if A["twist"] <= t < A["subscribe"]:
        if t < A["full2"] - 0.5: put(c, outlined("NOT 95% EMPTY...", 110), W / 2, 200, popk(t, A["isnt"]) if t >= A["isnt"] else 0)
        if t >= A["full2"] - 0.5: put(c, outlined("5% FULL.", 170, fill=YEL, f=IMPACT, stroke=10), W / 2, 210, popk(t, A["full2"] - 0.5))
        dots(c, cam, 1.0, A["twist"], t)
    if A["subscribe"] <= t < A["endscreen"]:
        put(c, sprite("host_cool", 520), 1560, 1020, popk(t, A["subscribe"]), anchor="b")
        put(c, pill("SUBSCRIBE · more maps that look wrong", 54, (255, 255, 255), (200, 30, 30, 240)), W / 2 - 150, 300, popk(t, A["subscribe"] + 0.3))
    for f, t0, t1, x, y, w, rot, cr in PHOTOS: L.photo(c, PH + f, t, t0, t1, x=x, y=y, w=w, rot=rot, credit=cr)
    L.subscribe_nudge(c, t, A["sub_mid"], A["sub_more"] + 1.4, x=1200, y=470, t_click=A["sub_word"])
    L.end_screen(c, t, A["endscreen"], "more maps that look wrong?")
    chapter_card(c, t)

NILE_FULL = [(33.2, 0.4), (32.6, 3.6), (31.6, 9.5), (32.5, 15.6), (33.9, 17.7), (33.0, 19.2), (30.6, 19.6), (31.35, 21.8)] + G.NILE[1:]
BLUE_NILE = [(37.4, 12.0), (35.4, 11.3), (34.4, 12.6), (33.5, 14.4), (32.5, 15.6)]
def draw_full_nile(c, cam, t, t0):
    u = ease((t - t0) / 2.5); n = max(2, int(len(NILE_FULL) * u)); wl = max(4, int(cam[2] / 6))
    layer(c, lambda d: (d.line(poly_px(cam, NILE_FULL[:n]), fill=(52, 120, 200, 255), width=wl, joint="curve"),
                        d.line(poly_px(cam, BLUE_NILE[: max(2, int(len(BLUE_NILE) * u))]), fill=(52, 120, 200, 255), width=wl, joint="curve")))

SFX = []
for nm, t0 in A.items():
    if nm in ("texas", "river1", "govt", "roughly", "math", "capital", "minister", "valleywide", "qattara", "newvalley", "sinai", "nile_len", "kemet",
              "deshret", "herodotus", "dam", "nasser", "electricity", "agency", "sixmillion", "manmade", "toshka", "share", "reservoir", "isnt"):
        SFX.append(("pop", t0 + 0.3, -20))
for name, t0 in CH: SFX.append(("paper_slide", t0, -20))
SFX += [("pop", ph[1], -19) for ph in PHOTOS]
SFX += [("pop", A["sub_word"] + 0.25, -18), ("paper_slide", A["endscreen"], -18), ("pop", A["endscreen"] + 2.3, -20)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END)
    else: K.main(sys.argv, overlay, SFX)
