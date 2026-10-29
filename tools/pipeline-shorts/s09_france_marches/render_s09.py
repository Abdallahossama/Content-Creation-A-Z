"""Habibi Explains the News — Short #9 "Why 550,000 French people marched" (19 Oct 2026). Doc mode: map + real photos, no people
on screen, no cartoons, sources on screen. Engine: shortkit (+ longkit helpers).  python render_s09.py build | qa t.. | all"""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, pin, YEL, SANS, IMPACT
import longkit as L
import marker as MK

K.setup(root="D:/why habibi/shorts/s09_france_marches/", vo="vo/s09_vo_chatterbox.wav", lat_mid=46.5, pyr=[40, 80, 160],
        fills=[("France", (196, 60, 48))], music="Stay the Course.mp3", out="Ask_Habibi_Short09_FranceMarches.mp4", fill_alpha=0.55)
W, H = K.W, K.H
at = L.at
A = L.Anchors(); a = A.a
a("arrests", "arrests"); a("saturday", "saturday"); a("why", "why"); a("three", "three"); a("high", "high"); a("vests", "vests")
a("unions", "unions"); a("billion", "billion"); a("cut", "cut"); a("trillion", "trillion"); a("borrowing", "borrowing"); a("violent", "violent")
a("limoges", "limoges"); a("next", "next"); a("tuesday", "tuesday"); a("november", "november"); a("so", "so", 1, "november"); a("marches", "marches")
END = K.DUR
PH = "D:/why habibi/_media/photos_s09/"; FLAG = "D:/why habibi/_media/cutouts/flag_france_real.png"
PARIS, LIMOGES = (2.35, 48.86), (1.26, 45.83)
FR = (2.4, 46.6, 88); PAR = (2.35, 48.4, 150); LIM = (1.3, 45.9, 150)
K.set_camera(L.hold_keys([(0.0, *FR), (A["why"], *FR), (A["high"] - 0.2, *PAR), (A["unions"] - 0.2, *FR), (A["violent"], *LIM),
                          (A["next"] - 0.2, *PAR), (A["so"] - 0.2, *FR), (END + 1, *FR)], gap=2.2, move=0.9, push=1.05))

def card(path, w, rot, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS); bd = 14
    c = Image.new("RGBA", (im.width + 2 * bd, im.height + 2 * bd), (250, 247, 240, 255)); c.paste(im, (bd, bd))
    return c.rotate(rot, Image.BICUBIC, expand=True)
CLASS = card(PH + "classroom.jpg", 760, -2); EURO = card(PH + "euro_notes.jpg", 700, 2, crop=(0, 0.1, 1, 0.8))
PARL = card(PH + "parliament.jpg", 780, -2, crop=(0, 0.0, 1, 0.62))            # cropped above street level (no people)

def counter(c, t, t0, target, y, size, suffix="", dur=1.0):
    if t < t0: return
    n = target * ease((t - t0) / dur); put(c, outlined(f"{int(n):,}{suffix}", size, fill=YEL, f=IMPACT, stroke=9), W / 2, y, popk(t, t0))

def overlay(c, t, cam):
    lon, lat, p = cam
    show = p < 120 and not (A["cut"] - 0.2 <= t < A["violent"] - 0.2)              # label would sit behind the 4.94% pill
    serif_label(c, "France", *geo(cam, 2.4, 47.6), 64 if show else 0, alpha=0.9 if show else 0)
    loop = A["marches"] + 0.6
    # B1 + loop: frame-1 payoff
    if t < A["why"] - 0.2 or t >= loop:
        t0 = 0.0 if t < loop else loop
        L.cutout(c, FLAG, t, t0, 850, 1010, 400, rot=3)
        if t0 == 0:
            put(c, outlined("550,000", 170, fill=YEL, f=IMPACT, stroke=10), W / 2, 330, 1.0)
            put(c, pill("marched in France · Interior Ministry · 17 Oct", 36), W / 2, 450, 1.0)
            if t >= A["arrests"] - 0.3: put(c, outlined("2,400 ARRESTS", 96, fill=(255, 255, 255)), W / 2, 570, popk(t, A["arrests"] - 0.3))
            if t >= A["saturday"] - 0.4: put(c, pill("ONE SATURDAY", 52, (255, 225, 120), (150, 40, 30, 235)), W / 2, 690, popk(t, A["saturday"] - 0.4))
        else:
            put(c, outlined("550,000", 170, fill=YEL, f=IMPACT, stroke=10), W / 2, 330, popk(t, loop))
    # B2: why?
    if A["why"] - 0.2 <= t < A["three"] - 0.2:
        put(c, outlined("WHY DID THEY MARCH?", 86), W / 2, 330, popk(t, A["why"] - 0.2))
    # B3: three protests, one day
    groups = [("STUDENTS", A["high"], (60, 104, 176)), ("YELLOW VESTS", A["vests"] - 0.4, (230, 190, 30)), ("UNIONS", A["unions"], (196, 52, 44))]
    if A["three"] - 0.2 <= t < A["cut"] - 0.2:
        put(c, outlined("3 PROTESTS · 1 DAY", 92, fill=YEL, f=IMPACT, stroke=8), W / 2, 300, popk(t, A["three"] - 0.2))
        for k, (lab, tt, col) in enumerate(groups):
            if t >= tt - 0.1:
                active = (k == 2 and t >= A["unions"]) or (k == 1 and A["vests"] - 0.4 <= t < A["unions"]) or (k == 0 and t < A["vests"] - 0.4)
                put(c, pill(lab, 46 if active else 36, (255, 255, 255), col + ((245,) if active else (150,))), 220 + k * 320, 420, popk(t, tt - 0.1))
        if A["high"] <= t < A["vests"] - 0.4:
            put(c, CLASS, W / 2, 800, popk(t, A["high"] + 0.2)); put(c, pill("classes of up to 35 · run-down schools", 40, YEL), W / 2, 1110, popk(t, A["high"] + 0.6))
        if A["vests"] - 0.4 <= t < A["unions"]:
            d = ImageDraw.Draw(c, "RGBA"); u = ease((t - A["vests"] + 0.4) / 0.6)
            d.rectangle((0, 640, W * u, 900), fill=(240, 200, 30, 235)); d.rectangle((0, 700, W * u, 720), fill=(220, 220, 220, 255)); d.rectangle((0, 820, W * u, 840), fill=(220, 220, 220, 255))
            put(c, outlined("LIVING COSTS + FUEL PRICES", 64), W / 2, 770, popk(t, A["vests"] + 0.2))
        if t >= A["unions"]:
            put(c, EURO, W / 2, 780, popk(t, A["unions"] + 0.2))
            if t >= A["billion"] - 0.8: put(c, outlined("€54 BILLION", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 1010, popk(t, A["billion"] - 0.8))
            put(c, pill("in savings · public pay frozen · 2027 budget", 38), W / 2, 1120, popk(t, A["unions"] + 0.6))
    # B4: why cut
    if A["cut"] - 0.2 <= t < A["violent"] - 0.2:
        put(c, outlined("WHY CUT?", 100), W / 2, 300, popk(t, A["cut"] - 0.2))
        if t >= A["trillion"] - 1.0:
            put(c, outlined("€3.6 TRILLION", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 450, popk(t, A["trillion"] - 1.0))
            put(c, pill("public debt · 119% of GDP · INSEE", 38), W / 2, 560, popk(t, A["trillion"] - 0.8))
        if t >= A["borrowing"]:
            put(c, outlined("4.94%", 120, fill=(255, 255, 255), f=IMPACT, stroke=9), W / 2, 760, popk(t, A["borrowing"]))
            put(c, pill("10-year borrowing rate · highest since 2002", 38, YEL), W / 2, 870, popk(t, A["borrowing"] + 0.3))
    # B5: violence (doc mode: plain facts)
    if A["violent"] - 0.2 <= t < A["next"] - 0.2:
        put(c, outlined("THEN IT TURNED VIOLENT", 84), W / 2, 300, popk(t, A["violent"] - 0.2))
        x, y = geo(cam, *LIMOGES); d = ImageDraw.Draw(c, "RGBA")
        for k in range(2):                                                         # pulsing marker rings on Limoges
            ph = ((t - A["violent"]) * 0.8 + k * 0.5) % 1.0; r = 40 + 90 * ph
            d.ellipse((x - r, y - r, x + r, y + r), outline=(200, 30, 30, int(230 * (1 - ph))), width=9)
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(200, 30, 30), outline=(255, 255, 255), width=7)
        if t >= A["limoges"] - 0.2:
            put(c, pill("Limoges: 19th-century city hall burned · AP", 38, YEL), W / 2, y - 140, popk(t, A["limoges"] - 0.2))
            put(c, pill("~2,400 arrests nationwide · Interior Ministry", 36), W / 2, 430, popk(t, A["limoges"] + 0.6))
    # B6: what's next
    if A["next"] - 0.2 <= t < A["so"] - 0.2:
        put(c, outlined("WHAT'S NEXT?", 100), W / 2, 300, popk(t, A["next"] - 0.2))
        if t >= A["tuesday"] - 0.3:
            put(c, PARL, W / 2, 640, popk(t, A["tuesday"] - 0.3))
            put(c, pill("TUE 20 OCT · parliament votes on the budget", 42, (255, 255, 255), (30, 60, 140, 240)), W / 2, 900, popk(t, A["tuesday"]))
        if t >= A["november"] - 0.3:
            put(c, pill("THU 5 NOV · nationwide union strike", 42, (255, 255, 255), (196, 52, 44, 240)), W / 2, 1010, popk(t, A["november"] - 0.3))
    # B7: end line
    if A["so"] - 0.2 <= t < loop:
        put(c, outlined("THE CUTS AREN'T OVER.", 80), W / 2, 330, popk(t, A["so"] - 0.2))
        if t >= A["marches"] - 1.4: put(c, outlined("NEITHER ARE THE MARCHES.", 68, fill=YEL), W / 2, 450, popk(t, A["marches"] - 1.4))

SFX = [("pop", 0.1, -20), ("pop", A["arrests"] - 0.3, -18), ("pop", A["saturday"] - 0.4, -20), ("pop", A["three"] - 0.2, -18),
       ("paper_slide", A["high"] + 0.2, -18), ("swoosh_in", A["vests"] - 0.4, -20), ("cash_register", A["billion"] - 0.8, -22),
       ("pop", A["trillion"] - 1.0, -18), ("pop", A["borrowing"], -18), ("impact_soft", A["violent"] - 0.2, -20), ("pop", A["limoges"] - 0.2, -18),
       ("paper_slide", A["tuesday"] - 0.3, -18), ("pop", A["november"] - 0.3, -18), ("pop", A["marches"] - 1.4, -18)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END)
    else: K.main(sys.argv, overlay, SFX)
