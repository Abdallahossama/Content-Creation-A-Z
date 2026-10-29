"""Habibi Explains the News — Short #4 "Alberta votes on leaving Canada" (19 Oct 2026). Engine: _style_kit/tools/shortkit.py.
  python render_s04.py build | qa t.. | caps | seg i n | audio | final | all"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, sprite, panel, pin, W, H, YEL, SANS, IMPACT

RED, CAN, BLUE = (196, 52, 44), (222, 172, 140), (60, 104, 176)
# Alberta: 49N (Montana), 110W (Saskatchewan), 60N (NWT), 120W south to the Rocky Mountain divide, then the divide via the passes
ALBERTA = [(-120.0, 60.0), (-110.0, 60.0), (-110.0, 49.0), (-114.07, 49.0), (-114.4, 49.3), (-114.70, 49.63), (-114.75, 49.95),
           (-115.2, 50.4), (-115.65, 50.87), (-115.95, 51.2), (-116.29, 51.45), (-116.7, 51.75), (-117.3, 52.17), (-117.9, 52.6),
           (-118.46, 52.89), (-119.25, 53.35), (-120.0, 53.8)]
K.setup(root="D:/why habibi/shorts/s04_alberta_vote/", vo="vo/s04_vo_chatterbox.wav", lat_mid=52, pyr=[20, 40, 80],
        fills=[("Canada", CAN)], polys=[("Alberta", ALBERTA, RED)], music="Stay the Course.mp3", out="Ask_Habibi_Short04_AlbertaVote.mp4",
        fill_alpha=0.62)
at = K.at
T = dict(alberta=at("alberta"), france=at("france"), oil=at("sits"), ninety=at("about"), ballot=at("there"), tenth=at("10th"),
         yes=at("so", 1), door=at("only"), stay=at("most"), poll=at("latest"), showing=at("but", 2), first=at("first"),
         quebec=at("quebec"), trump=at("but", 3), breaking=at("so", 2), tonight=at("tonight"))
END = K.DUR

WIDE = (-105.0, 51.0, 22); AB = (-114.8, 54.2, 58); QC = (-86.0, 50.0, 18)
K.set_camera([(0.0, *WIDE), (T["france"] + 0.6, *WIDE), (T["oil"] - 0.1, *AB), (T["ninety"] - 0.2, -112.0, 51.0, 40), (T["ballot"] - 0.2, -112.0, 51.0, 40),
              (T["ballot"] + 0.5, *AB), (T["quebec"] - 0.6, -113.5, 53.0, 50), (T["quebec"] + 0.6, *QC), (T["breaking"] - 0.3, *QC),
              (T["breaking"] + 0.8, *WIDE), (END + 1, *WIDE)])

CITIES = dict(Edmonton=(-113.49, 53.55), Calgary=(-114.07, 51.05))
QUEBEC = (-71.21, 46.81)

def france_ring():
    """France's mainland outline moved onto Alberta at true size (km), for 'bigger than France'"""
    best = None
    import mapkit
    for name, rings in mapkit._load():
        if name != "France": continue
        for r in rings:
            a = np.asarray(r)
            if -6 < a[:, 0].mean() < 9 and 41 < a[:, 1].mean() < 52 and (best is None or len(r) > len(best)): best = r
    a = np.asarray(best, float); c0 = (2.45, 46.6); c1 = (-99.0, 54.2)
    lon = c1[0] + (a[:, 0] - c0[0]) * math.cos(math.radians(46.6)) / math.cos(math.radians(54.6)); lat = c1[1] + (a[:, 1] - c0[1])
    return list(zip(lon[::3], lat[::3]))
FR = france_ring()

def dashed_poly(c, pts, col, width=5, dash=16, gap=11):
    d = ImageDraw.Draw(c); pts = np.asarray(pts + pts[:1], float); on, run = True, 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; L = float(np.hypot(*(b - a)))
        if L < 1e-6: continue
        n = max(1, int(L));
        for k in range(n):
            p0 = a + (b - a) * k / n; p1 = a + (b - a) * (k + 1) / n
            if on: d.line([tuple(p0), tuple(p1)], fill=col, width=width)
            run += L / n
            if run >= (dash if on else gap): on, run = not on, 0.0

def barrel(h):
    im = Image.new("RGBA", (int(h * 0.72), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = im.width
    d.rounded_rectangle((2, 6, w - 3, h - 6), 14, fill=(40, 40, 46, 255), outline=(10, 10, 12, 255), width=4)
    for y in (h * 0.3, h * 0.66): d.line((4, y, w - 5, y), fill=(120, 120, 130, 255), width=5)
    d.ellipse((6, 2, w - 7, 22), fill=(70, 70, 80, 255), outline=(10, 10, 12, 255), width=3)
    d.text((w / 2, h * 0.48), "OIL", font=font(SANS, h * 0.2), fill=(255, 206, 60, 255), anchor="mm")
    return im
BARREL = barrel(150)

def ballot():
    im = Image.new("RGBA", (860, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((10, 10, 850, 460), fill=(250, 247, 238, 255), outline=(60, 50, 40, 255), width=4)
    d.text((40, 36), "BALLOT · THE 10TH QUESTION", font=font(SANS, 34), fill=(120, 40, 34))
    for k, (a, b) in enumerate((("Stay in Canada", ""), ("Start the legal process toward", "a future vote on leaving"))):
        y = 120 + k * 150; d.rectangle((40, y, 110, y + 70), outline=(40, 34, 28, 255), width=6)
        d.text((140, y + (6 if b else 18)), a, font=font(SANS, 42), fill=(40, 34, 28));
        if b: d.text((140, y + 58), b, font=font(SANS, 42), fill=(40, 34, 28))
    return im
BALLOT = ballot()

def overlay(c, t, cam):
    lon, lat, p = cam; d = ImageDraw.Draw(c)
    ax, ay = geo(cam, -115.0, 55.0)
    if p < 30:
        serif_label(c, "Canada", *geo(cam, -96.0, 60.5), 50); serif_label(c, "United States", *geo(cam, -99.0, 40.0), 44)
        serif_label(c, "Alberta", ax, ay + 10, 40, col=(255, 244, 228))
        if lon > -95: serif_label(c, "Quebec", *geo(cam, -72.5, 52.0), 42)
    else:
        if not (T["ninety"] <= t < T["ballot"]): serif_label(c, "Alberta", *geo(cam, -114.6, 56.6), 56, col=(255, 244, 228))
        for nm, ll in CITIES.items():
            x, y = geo(cam, *ll); pin(c, x, y, (40, 30, 20)); serif_label(c, nm, x + (110 if nm == "Calgary" else -125), y + 6, 38)
    # B1 (frame 1 + loop): the question, Alberta red, France at the same scale
    loop = T["tonight"] + 1.2
    if t < T["oil"] - 0.1 or t >= loop:
        t0 = 0.0 if t < T["oil"] else loop; k0 = (lambda dd: 1.0) if t0 == 0 else (lambda dd: popk(t, t0 + dd))
        put(c, outlined("IS ALBERTA LEAVING", 88), W / 2, 300, k0(0)); put(c, outlined("CANADA?", 88, emoji="🍁"), W / 2, 405, k0(0))
        put(c, pill("VOTING TODAY · 19 OCT", 44, (255, 225, 120), (150, 40, 30, 235)), W / 2, 520, k0(0.1))
        if t >= T["france"] - 0.2 or t0 > 0:
            pts = [geo(cam, *q) for q in FR]; dashed_poly(c, pts, (255, 255, 255, 235), width=4)
            kf = k0(0.2) if t0 else popk(t, T["france"] - 0.2)
            x1, y1 = geo(cam, -115.0, 48.2); put(c, pill("Alberta ~660,000 km²", 30, (255, 225, 120), (150, 40, 30, 235)), max(x1 - 20, 175), y1 + 62, kf)
            x2, y2 = geo(cam, -99.0, 48.9); put(c, pill("France ~550,000 km²", 30), min(x2 + 30, 890), y2, kf)
    # B2: oil
    if T["oil"] <= t < T["ballot"] - 0.1:
        put(c, BARREL, 820, ay + 470, popk(t, T["oil"] + 0.3), anchor="b")
        put(c, outlined("4TH-LARGEST", 100, fill=YEL, f=IMPACT, stroke=8), W / 2, 330, popk(t, T["oil"] + 0.5))
        put(c, pill("proven oil reserves on Earth · AP", 38), W / 2, 430, popk(t, T["oil"] + 0.7))
        put(c, sprite("oil_worker", 300), 960, ay + 480, popk(t, T["oil"] + 0.4), anchor="b")
        if t >= T["ninety"]:
            u = ease((t - T["ninety"]) / 1.4); x0, y0 = geo(cam, -112.5, 50.0); x1, y1 = geo(cam, -103.0, 42.5)
            pts = [(x0 + (x1 - x0) * s * u, y0 + (y1 - y0) * s * u + 60 * math.sin(math.pi * s * u)) for s in np.linspace(0, 1, 30)]
            ImageDraw.Draw(c).line(pts, fill=(30, 22, 16), width=16, joint="curve"); ImageDraw.Draw(c).line(pts, fill=(255, 206, 60), width=9, joint="curve")
            put(c, outlined("~90%", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 560, popk(t, T["ninety"] + 0.8))
            put(c, pill("of its oil exports go to the US", 40), W / 2, 670, popk(t, T["ninety"] + 1.0))
    # B3: the ballot
    if T["ballot"] <= t < T["yes"] - 0.1:
        put(c, outlined("10 QUESTIONS", 110, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["ballot"] + 0.2))
        if t >= T["tenth"] - 0.2: put(c, BALLOT, W / 2, 720, popk(t, T["tenth"] - 0.2))
    # B4: a yes does not mean leaving
    if T["yes"] <= t < T["stay"] - 0.1:
        put(c, outlined("A YES ≠ LEAVING", 100, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["yes"] + 0.3))
        if t >= T["door"]: put(c, pill("it only opens the door to another referendum", 38), W / 2, 450, popk(t, T["door"]))
        put(c, BALLOT, W / 2, 760, 1.0 if t < T["yes"] + 0.5 else max(0.0, 1 - (t - T["yes"] - 0.5) * 3))
    # B5: polls
    if T["stay"] <= t < T["showing"] - 0.1:
        dd = panel(c, (110, 260, 970, 800), 205)
        dd.text((W / 2, 320), "Poll average · The Writ, 17 Oct", font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
        for k, (lab, v, col) in enumerate((("REMAIN", 68, BLUE), ("START THE PROCESS", 26, RED))):
            y = 430 + k * 190; u = ease((t - T["poll"] - 0.2 - k * 0.5) / 1.0); x0 = 160; full = 760
            dd.text((x0, y - 50), lab, font=font(SANS, 38), fill=(255, 255, 255))
            dd.rounded_rectangle((x0, y, x0 + full, y + 70), 16, fill=(70, 60, 50))
            if u > 0: dd.rounded_rectangle((x0, y, x0 + full * v / 100 * u, y + 70), 16, fill=col)
            if u > 0.05: dd.text((x0 + full * v / 100 * u + 20, y + 35), f"{v * u:.0f}%", font=font(IMPACT, 60), fill=YEL, anchor="lm", stroke_width=5, stroke_fill=(12, 10, 10))
    # B6: early voting
    if T["showing"] <= t < T["quebec"] - 0.6:
        if t >= T["first"] - 0.3:
            n = 174532 * ease((t - T["first"] + 0.3) / 1.6)
            put(c, outlined(f"{int(n):,}", 140, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["first"] - 0.3))
            put(c, pill("votes on day 1 of early voting · CP24", 38), W / 2, 450, popk(t, T["first"]))
        ex, ey = geo(cam, *CITIES["Edmonton"])
        box = Image.new("RGBA", (130, 120), (0, 0, 0, 0)); bd = ImageDraw.Draw(box); bd.rectangle((5, 25, 125, 115), fill=(235, 230, 220, 255), outline=(40, 34, 28, 255), width=5); bd.rectangle((35, 15, 95, 32), fill=(40, 34, 28, 255))
        put(c, box, ex + 150, ey + 40, popk(t, T["showing"] + 0.2), anchor="b")
        for k, nm in enumerate(("viewer", "student", "host", "oil_worker", "viewer")):
            u = ease((t - T["showing"] - 0.2 - k * 0.15) / 2.2); x = ex - 60 - k * 95 + 70 * u; y = ey + 60 + k * 30
            put(c, sprite(nm, 150), x, y, popk(t, T["showing"] + 0.1 + k * 0.1), anchor="b")
    # B7: Quebec
    if T["quebec"] - 0.6 <= t < T["breaking"] - 0.1:
        qx, qy = geo(cam, *QUEBEC); pin(c, qx, qy, RED)
        if t >= T["quebec"]:
            put(c, outlined("QUEBEC TOO?", 100, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["quebec"]))
            put(c, pill("5 Oct: separatist party back in power", 38), W / 2, 445, popk(t, T["quebec"] + 0.4))
        if t >= T["trump"]: put(c, pill("leader: no independence vote while Trump is president · AP", 32, (255, 225, 120)), W / 2, 540, popk(t, T["trump"] + 0.2))
    # B8: is Canada breaking up?
    if T["breaking"] <= t < loop:
        put(c, outlined("IS CANADA BREAKING UP?", 76), W / 2, 330, popk(t, T["breaking"]))
        if t >= T["breaking"] + 1.3: put(c, outlined("NOT TODAY.", 150, fill=YEL, f=IMPACT, stroke=10), W / 2, 480, popk(t, T["breaking"] + 1.3))
        if t >= T["tonight"]: put(c, pill("results come in tonight", 44, (255, 225, 120)), W / 2, 620, popk(t, T["tonight"]))

SFX = [("pop", 0.15, -20), ("pop", T["france"] - 0.2, -18), ("pop", T["oil"] + 0.5, -18), ("pop", T["ninety"] + 0.8, -18), ("pop", T["ballot"] + 0.2, -18),
       ("paper_slide", T["tenth"] - 0.2, -18), ("pop", T["yes"] + 0.3, -18), ("pop", T["poll"] + 0.2, -20), ("pop", T["first"] - 0.3, -18),
       ("pop", T["quebec"], -18), ("pop", T["trump"] + 0.2, -20), ("pop", T["breaking"] + 1.3, -16), ("pop", T["tonight"], -20)]

if __name__ == "__main__":
    K.main(sys.argv, overlay, SFX)
