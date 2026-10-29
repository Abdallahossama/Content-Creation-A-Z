"""Ask Habibi Ep 10 "Why Diesel Costs $2 More Than Gas Right Now" - 16:9 long version of Short #5 (77.6% viewed).
Engine: _style_kit/tools/shortkit.py (1920x1080) + longkit. Voice: local Chatterbox clone, word timings in 10th video/vo/vo_words.json.
Every number: _pipeline/episodes/ep10_diesel/research.md (AAA / EIA / IEA ... checked 22 Oct 2026).
  python render_ep10.py anchors | build | qa t.. | caps | seg i n | audio | final | all"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, sprite, pin, YEL, SANS, IMPACT
import longkit as L

ROOT = "D:/why habibi/10th video/"
K.setup(root=ROOT, vo="vo/ep10_vo_chatterbox.wav", lat_mid=40, pyr=[10, 20, 40, 80, 160], size=(1920, 1080), cap_size=64, tail=21.5,
        fills=[("United States of America", (120, 150, 196)), ("Russia", (190, 70, 50)), ("Iran", (206, 150, 70))], fill_alpha=0.55,
        out="Ask_Habibi_Ep10_Why_Diesel_Costs_More.mp4",
        cap_fix=[("U .S.", "US"), ("U .S", "US"), ("$427", "$4.27"), ("$631", "$6.31"), ("653", "$6.53"), ("$849", "$8.49"), ("449", "$4.49"),
                 ("$0.24", "24 cents"), ("$0.18", "18 cents"), ("$0.83", "83 cents"), ("DAS", "Gas"), ("crewed", "crude"), ("straight", "strait"),
                 ("Strake", "Strait"), ("strake", "strait"), ("parley", "partly"), ("-low -sulfur", "low-sulfur"), ("ultra -low", "ultra-low"), ("$1600", "$1,600"), ("Haan", "Haan")])
W, H = K.W, K.H
YELLOW = YEL; RED = (210, 40, 36); BLUE = (110, 160, 220); GREY = (200, 192, 180); GREEN = (90, 170, 90)

# ------------------------------------------------------------------ anchors (spoken words; whisper writes numbers as digits)
A = L.Anchors(); MISSING = []
def a(name, word, n=1, after=None):
    try: return A.a(name, word, n, after)
    except KeyError as e: MISSING.append((name, str(e))); A[name] = A.get(after, 0.0) if isinstance(after, str) else 0.0; return A[name]
a("why0", "why"); a("oct22", "october"); a("yearago", "year"); a("strange", "strange"); a("three", "three"); a("barrel1", "barrel", 1, "three")
a("strait1", "strait", 1, "three"); a("refinery1", "refinery", 1, "three"); a("byend", "end", 1, "refinery1")
a("ch1", "start"); a("oneyear", "year", 1, "ch1"); a("sept1", "september", 1, "ch1"); a("record", "record", 1, "sept1")
a("cal", "california"); a("nc", "carolina"); a("different", "different")
a("ch2", "fake"); a("june", "june"); a("moved", "moved"); a("ulsd", "cleaner"); a("federal", "federal"); a("states", "states", 1, "federal")
a("taxman", "man", 1, "states"); a("inside", "inside", 1, "taxman"); a("gasoline", "gasoline", 1, "inside"); a("twelvehalf", "half", 1, "gasoline")
a("slice", "slice"); a("trucks", "trucks"); a("trains", "trains"); a("northeast", "northeast"); a("squeezed", "squeezed")
a("ch3", "really", 1, "squeezed"); a("uses", "uses", 1, "ch3"); a("week16", "week", 1, "uses"); a("abroad", "abroad")
a("houston", "houston"); a("brazil", "brazil"); a("rotterdam", "rotterdam"); a("texas", "texas"); a("cushion", "cushion")
a("eastcoast", "east", 1, "cushion"); a("fewer", "fewer"); a("left", "left", 1, "fewer"); a("slack", "slack"); a("suppliers", "suppliers")
a("ch4", "first", 1, "suppliers"); a("fifth", "fifth"); a("feb", "february"); a("twoweeks", "weeks", 1, "feb"); a("halfflow", "half", 1, "twoweeks")
a("dangerous", "dangerous"); a("ships12", "ships", 1, "dangerous"); a("gulf", "gulf"); a("middle", "middle", 1, "gulf")
a("ch5", "second", 1, "middle"); a("seaborne", "seaborne"); a("drones", "drones"); a("every3", "every", 1, "drones"); a("august", "august")
a("ryazan", "ryazan"); a("estimates", "estimates"); a("july", "july"); a("lowest", "lowest"); a("together", "together", 1, "lowest")
a("hole", "hole"); a("bidding", "bidding"); a("wholesale", "wholesale")
a("ch6", "washington"); a("license", "license"); a("plan", "plan", 1, "license"); a("senators", "senators"); a("gift", "gift")
a("shipment", "shipment"); a("wholedeal", "whole", 1, "shipment"); a("dehaan", "estimates", 1, "wholedeal"); a("tanker1", "tanker", 1, "dehaan")
a("ch7", "pays", 1, "tanker1"); a("truckers", "truckers"); a("math", "math"); a("fillup", "typical", 1, "math"); a("farmers", "farmers")
a("corn", "corn"); a("homes", "homes", 1, "corn"); a("groceries", "groceries"); a("react", "react"); a("pressure", "pressure", 1, "react")
a("ch8", "come", 1, "pressure"); a("eia", "energy", 1, "ch8"); a("iea", "international", 1, "eia"); a("change", "change", 1, "iea")
a("until", "until", 1, "change"); a("eight", "tax", 1, "until"); a("rest", "rest", 1, "until"); a("nexttime", "next", 1, "rest")
a("maps", "maps", 1, "nexttime"); a("subscribe", "subscribe", 1, "maps")
A["endscreen"] = K.WORDS[-1]["e"] + 0.6
END = K.DUR
CH = [("THE SIGN", A["ch1"] - 0.5), ("THE BARREL", A["ch2"] - 1.0), ("THE WORLD MARKET", A["ch3"] - 1.5), ("HORMUZ", A["ch4"] - 0.6),
      ("RUSSIA", A["ch5"] - 0.6), ("THE DEAL", A["ch6"] - 0.6), ("WHO PAYS", A["ch7"] - 1.0), ("WHAT'S NEXT", A["ch8"] - 0.9)]
K.CFG["music"] = [("Stay the Course.mp3", 0.0), ("Industrial Cinematic.mp3", A["ch4"] - 1.5), ("Rising Tide.mp3", A["ch6"] - 1.2),
                  ("Floating Cities.mp3", A["ch7"] - 1.2), ("Stay the Course.mp3", A["ch8"] - 1.0)]

# ------------------------------------------------------------------ photos (real, as proof; skipped if not downloaded)
PH = "D:/why habibi/_media/photos_ep10/"; P4 = "D:/why habibi/4th video/media/photos/"
PHOTOS = [  # (path, t0, t1, x, y, width, tilt, credit)
    (PH + "pexels-4744710.jpg", A["strange"], A["three"] - 0.1, 1500, 560, 520, 3, "Pexels"),
    (PH + "pexels-13763587.jpg", A["june"] + 0.2, A["moved"] - 0.1, 1480, 600, 460, 3, "Pexels"),
    (PH + "pexels-6563903.jpg", A["trucks"] + 1.6, A["trains"] - 0.1, 1480, 600, 560, 3, "Pexels"),
    (PH + "pexels-30743914.jpg", A["trains"] + 0.3, A["northeast"] - 0.2, 1480, 660, 480, 3, "Pexels"),
    (P4 + "pexels-36563588.jpg", A["houston"], A["texas"] - 0.2, 1500, 640, 480, 3, "Pexels"),
    (PH + "pexels-10407691.jpg", A["fewer"] + 0.4, A["left"] - 0.1, 1480, 600, 560, 3, "Pexels"),
    (PH + "iss_gulf_day.jpg", A["fifth"] + 1.4, A["feb"] - 0.1, 1460, 640, 600, 3, "the Gulf from the ISS · NASA"),
    (P4 + "pexels-35757999.jpg", A["gulf"] + 0.4, A["middle"] - 0.1, 1480, 640, 520, 3, "Pexels"),
    (PH + "pexels-15893881.jpg", A["drones"] + 0.3, A["every3"] - 0.1, 1480, 620, 460, 3, "illustrative · Pexels"),
    (P4 + "pexels-32294161.jpg", A["tanker1"] - 0.2, A["ch7"] - 1.2, 1460, 640, 560, 3, "illustrative · Pexels"),
    (PH + "pexels-27087941.jpg", A["truckers"], A["math"] - 0.1, 1590, 620, 400, 3, "Pexels"),
    (PH + "pexels-30743914.jpg", A["farmers"] + 0.2, A["corn"] - 0.1, 1480, 620, 520, 3, "Pexels"),
    (PH + "iss_houston_night.jpg", A["texas"] - 0.1, A["cushion"] - 0.1, 470, 640, 520, -3, "Houston's refineries at night · NASA"),
]
PHOTOS = [p for p in PHOTOS if os.path.exists(p[0])]

# ------------------------------------------------------------------ camera
USA = (-96.5, 38.0, 24); WORLD = (25.0, 30.0, 6.4); ATL = (-42.0, 22.0, 8.2); GULF = (52.6, 26.6, 64); HZ = (56.3, 26.4, 120)
RUS = (44.0, 55.0, 22); RYZ = (39.7, 54.6, 70); EUR = (12.0, 44.0, 12); NE = (-75.0, 41.5, 64); EAST = (-82.0, 36.0, 36)
CAL = (-119.5, 37.0, 60); ILL = (-89.0, 40.0, 60); MID = (55.0, 40.0, 9.5)
def cam_keys():
    k = [(0.0, *USA), (A["three"] - 0.3, *USA), (A["three"] + 0.5, *WORLD), (A["byend"], *WORLD), (A["ch1"] - 0.2, *USA),
         (A["cal"] - 0.3, *CAL), (A["nc"] - 0.3, -79.5, 35.5, 60), (A["different"], *USA), (A["ch2"], *USA), (A["trucks"] - 0.2, *USA),
         (A["northeast"] - 0.2, *NE), (A["squeezed"] + 0.4, *USA), (A["ch3"], *USA), (A["houston"] - 0.4, *ATL), (A["texas"] + 0.3, -95.0, 29.8, 90),
         (A["cushion"] - 0.2, *USA), (A["eastcoast"] - 0.3, *EAST), (A["fewer"] - 0.2, *USA), (A["slack"], *WORLD), (A["ch4"], *GULF),
         (A["fifth"] + 0.2, *HZ), (A["feb"], *GULF), (A["dangerous"] - 0.2, *HZ), (A["gulf"] - 0.3, *GULF), (A["middle"] + 0.4, 50.0, 28.0, 30),
         (A["ch5"], *RUS), (A["ryazan"] - 0.4, *RYZ), (A["estimates"] - 0.2, *RUS), (A["together"] - 0.2, *MID), (A["bidding"], *WORLD),
         (A["ch6"], *ATL), (A["senators"] - 0.2, -77.0, 38.9, 60), (A["shipment"] - 0.3, *ATL), (A["ch7"], *USA), (A["farmers"] - 0.3, *ILL),
         (A["homes"] - 0.3, *NE), (A["groceries"] - 0.2, *USA), (A["ch8"], *WORLD), (A["until"] - 0.3, *USA), (END + 2, *USA)]
    return L.hold_keys(k)
K.set_camera(cam_keys())

# ------------------------------------------------------------------ graphics
def price_sign(label, price, col, w=420, h=220):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(24, 22, 26, 238), outline=col + (255,), width=6)
    d.text((w / 2, 48), label, font=font(SANS, 40), fill=(235, 230, 220), anchor="mm")
    d.text((w / 2, h * 0.64), price, font=font(IMPACT, 108), fill=col, anchor="mm", stroke_width=5, stroke_fill=(10, 10, 10)); return im
SIGN_D = price_sign("DIESEL", "$6.31", YELLOW); SIGN_G = price_sign("GAS", "$4.27", (235, 235, 235))
OLD_D = price_sign("DIESEL · OCT 2025", "$3.63", YELLOW, 380, 190); OLD_G = price_sign("GAS · OCT 2025", "$3.07", (235, 235, 235), 380, 190)
J04_D = price_sign("DIESEL · JUNE 2004", "$1.71", YELLOW, 400, 200); J04_G = price_sign("GAS · JUNE 2004", "$1.97", (235, 235, 235), 400, 200)
def signs(c, t, t0, y=560, big=True):
    put(c, SIGN_D, W / 2 - 250, y, popk(t, t0)); put(c, SIGN_G, W / 2 + 250, y, popk(t, t0 + 0.12))
def stamp(c, text, x, y, t, t0, rot=7, size=76, col=(200, 30, 30, 240)):
    if t < t0: return
    f = font(IMPACT, size); bb = f.getbbox(text); w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 50
    st = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((5, 5, w + 5, h + 5), 16, outline=col, width=8); sd.text(((w + 10) / 2, (h + 10) / 2), text, font=f, fill=col, anchor="mm")
    put(c, st.rotate(rot, expand=True, resample=Image.BICUBIC), x, y, popk(t, t0))
def src(c, text, t, t0, y=330, size=34):
    if t >= t0: put(c, pill(text, size), W / 2, y, popk(t, t0))

WEEKLY = [("2025-10-06", 3.711, 3.124), ("2025-10-20", 3.620, 3.019), ("2025-11-03", 3.753, 3.019), ("2025-11-17", 3.868, 3.062), ("2025-12-01", 3.758, 2.985),
          ("2025-12-15", 3.607, 2.895), ("2025-12-29", 3.500, 2.811), ("2026-01-12", 3.459, 2.779), ("2026-01-26", 3.624, 2.853), ("2026-02-09", 3.688, 2.902),
          ("2026-02-23", 3.809, 2.937), ("2026-03-02", 3.897, 3.015), ("2026-03-09", 4.859, 3.502), ("2026-03-16", 5.071, 3.720), ("2026-03-23", 5.375, 3.961),
          ("2026-04-06", 5.643, 4.120), ("2026-04-20", 5.403, 4.044), ("2026-05-04", 5.640, 4.452), ("2026-05-18", 5.596, 4.490), ("2026-06-01", 5.350, 4.305),
          ("2026-06-15", 5.059, 4.052), ("2026-06-29", 4.668, 3.831), ("2026-07-06", 4.578, 3.777), ("2026-07-20", 5.134, 4.001), ("2026-08-03", 5.348, 4.079),
          ("2026-08-17", 5.454, 4.049), ("2026-08-31", 5.599, 4.071), ("2026-09-07", 5.967, 4.157), ("2026-09-14", 6.285, 4.319), ("2026-09-21", 6.529, 4.478),
          ("2026-09-28", 6.382, 4.465), ("2026-10-05", 6.199, 4.354), ("2026-10-12", 6.179, 4.331), ("2026-10-19", 6.276, 4.284)]
def price_chart(c, t, t0, upto=None, box=(250, 230, 1670, 830), mark_record=False, mark_war=False, gas_record=False, title="US average price per gallon, weekly · EIA"):
    d = L.panel(c, box, 228); x0, y0, x1, y1 = box[0] + 110, box[1] + 90, box[2] - 60, box[3] - 80; lo, hi = 2.5, 7.0
    X = lambda i: x0 + (x1 - x0) * i / (len(WEEKLY) - 1); Y = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    d.text(((box[0] + box[2]) / 2, box[1] + 45), title, font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
    for v in (3, 4, 5, 6, 7):
        d.line((x0, Y(v), x1, Y(v)), fill=(70, 62, 56), width=2); d.text((x0 - 18, Y(v)), f"${v}", font=font(SANS, 28), fill=GREY, anchor="rm")
    for i, lab in ((0, "Oct 2025"), (10, "Feb"), (22, "Jul"), (len(WEEKLY) - 1, "Oct 2026")): d.text((X(i), y1 + 34), lab, font=font(SANS, 28), fill=GREY, anchor="mm")
    u = ease((t - t0) / 2.2); n = max(2, int(2 + (len(WEEKLY) - 2) * u))
    if upto is not None: n = min(n, upto)
    if gas_record:
        d.line((x0, Y(5.016), x1, Y(5.016)), fill=(235, 235, 235), width=3); d.text((x0 + 16, Y(5.016) - 22), "gas record: $5.02 (June 2022)", font=font(SANS, 28), fill=(235, 235, 235), anchor="lm")
    if mark_war:
        d.line((X(10.9), y0, X(10.9), y1), fill=(220, 80, 60), width=4); d.text((X(10.9) + 12, y0 + 16), "war begins", font=font(SANS, 30), fill=(255, 140, 120), anchor="lm")
    d.line([(X(i), Y(g)) for i, (_, _, g) in enumerate(WEEKLY[:n])], fill=(235, 235, 235), width=7, joint="curve")
    d.line([(X(i), Y(v)) for i, (_, v, _) in enumerate(WEEKLY[:n])], fill=YELLOW, width=9, joint="curve")
    i = n - 1; d.text((X(i) + 14, Y(WEEKLY[i][1])), "diesel", font=font(SANS, 30), fill=YELLOW, anchor="lm"); d.text((X(i) + 14, Y(WEEKLY[i][2])), "gas", font=font(SANS, 30), fill=(235, 235, 235), anchor="lm")
    if mark_record and n >= 30:
        xr, yr = X(29), Y(6.529); d.ellipse((xr - 16, yr - 16, xr + 16, yr + 16), outline=RED, width=6)
        d.text((xr - 20, yr - 46), "RECORD $6.53 · 22 Sep (AAA)", font=font(IMPACT, 40), fill=YELLOW, anchor="rm", stroke_width=4, stroke_fill=(10, 10, 10))

SPREADS = [("2000", -0.21), ("2003", -0.07), ("2004", -0.26), ("2006", 0.01), ("2008", 0.62), ("2012", 0.22), ("2016", 0.06), ("2019", 0.37), ("2022", 0.83), ("2025", 0.62), ("2026", 1.94)]
def spread_bars(c, t, t0):
    d = L.panel(c, (250, 230, 1670, 830), 228); x0, x1, yz = 360, 1600, 600
    d.text((W / 2, 275), "Diesel minus gas, June each year (2025: Oct, 2026: Sep) · EIA", font=font(SANS, 34), fill=(235, 225, 210), anchor="mm")
    d.line((x0 - 30, yz, x1 + 30, yz), fill=GREY, width=3); d.text((x0 - 40, yz), "$0", font=font(SANS, 28), fill=GREY, anchor="rm")
    for k, (yr, v) in enumerate(SPREADS):
        u = ease((t - t0 - k * 0.12) / 0.5)
        if u <= 0: continue
        x = x0 + (x1 - x0) * k / (len(SPREADS) - 1); h = v * 150 * u
        col = (110, 190, 120) if v < 0 else YELLOW
        d.rounded_rectangle((x - 40, min(yz, yz - h), x + 40, max(yz, yz - h)), 8, fill=col)
        d.text((x, 780), yr, font=font(SANS, 28), fill=(235, 225, 210), anchor="mm")
        d.text((x, yz - h - 26 if v >= 0 else yz - h + 26), f"{'+' if v > 0 else ''}{v:.2f}", font=font(SANS, 26), fill=(255, 255, 255), anchor="mm")
    if t >= t0 + 1.4: d.text((380, 340), "below the line = diesel was CHEAPER", font=font(IMPACT, 40), fill=(110, 190, 120), anchor="lm")

def tax_bar(c, t, t0):
    d = L.panel(c, (250, 300, 1670, 760), 228); x0, x1 = 330, 1590; tot = 2.04
    d.text((W / 2, 350), "Today's gap: $2.04 a gallon", font=font(SANS, 40), fill=(235, 225, 210), anchor="mm")
    u = ease((t - t0) / 0.8); d.rounded_rectangle((x0, 450, x0 + (x1 - x0) * u, 560), 18, fill=(120, 110, 100))
    if t >= t0 + 0.8:
        k = ease((t - t0 - 0.8) / 0.5); xt = x0 + (x1 - x0) * 0.08 / tot
        d.rounded_rectangle((x0, 450, x0 + (xt - x0) * max(k, 0.05), 560), 12, fill=RED)
        d.line((xt, 430, xt, 600), fill=(255, 255, 255), width=3); d.text((x0, 640), "≈ 8¢ taxes", font=font(IMPACT, 54), fill=(255, 120, 110), anchor="lm", stroke_width=4, stroke_fill=(10, 10, 10))
        d.text((x1, 640), "≈ $1.96 everything else", font=font(IMPACT, 54), fill=YELLOW, anchor="rm", stroke_width=4, stroke_fill=(10, 10, 10))
        d.text((W / 2, 715), "federal 24.4¢ vs 18.4¢ + states 35.9¢ vs 33.6¢ · EIA", font=font(SANS, 30), fill=GREY, anchor="mm")

def barrel(c, t, t0, hl_diesel=False):
    d = L.panel(c, (300, 210, 1620, 850), 228); bx0, bx1, by0, by1 = 420, 720, 300, 790
    d.text((W / 2, 255), "One 42-gallon barrel of crude · US refineries · EIA", font=font(SANS, 32), fill=(235, 225, 210), anchor="mm")
    d.rounded_rectangle((bx0 - 12, by0 - 12, bx1 + 12, by1 + 12), 40, outline=(170, 150, 120), width=10)
    parts = [("gasoline", 19.6, (235, 235, 235)), ("diesel + heating oil", 12.5, YELLOW), ("jet fuel", 4.4, BLUE), ("everything else", 5.5, (150, 120, 90))]
    y = by1; tot = 42.0
    for k, (lab, g, col) in enumerate(parts):
        u = ease((t - t0 - k * 0.45) / 0.6)
        if u <= 0: continue
        h = (by1 - by0) * g / tot * u; d.rectangle((bx0, y - h, bx1, y), fill=col)
        if u > 0.6:
            big = hl_diesel and k == 1
            d.text((bx1 + 50, y - h / 2), f"{g:g} gal  {lab}", font=font(IMPACT if big else SANS, 52 if big else 40), fill=YELLOW if k == 1 else (240, 236, 228), anchor="lm",
                   stroke_width=4 if big else 0, stroke_fill=(10, 10, 10))
        y -= h

def balance_bars(c, t, t0):
    d = L.panel(c, (300, 260, 1620, 820), 228)
    d.text((W / 2, 305), "US diesel + heating oil, week to 16 Oct 2026 (million barrels a day) · EIA", font=font(SANS, 32), fill=(235, 225, 210), anchor="mm")
    rows = [("made", 5.2, YELLOW, t0), ("used", 3.9, BLUE, t0 + 0.6), ("shipped abroad", 1.38, (230, 130, 70), A["abroad"])]
    for k, (lab, v, col, tt) in enumerate(rows):
        u = ease((t - tt) / 0.8)
        if u <= 0: continue
        y = 420 + k * 130; d.text((360, y), lab, font=font(SANS, 40), fill=(255, 255, 255), anchor="lm")
        d.rounded_rectangle((700, y - 40, 700 + 160 * v * u, y + 40), 16, fill=col)
        d.text((720 + 160 * v * u, y), f"{v:g}", font=font(IMPACT, 54), fill=YELLOW, anchor="lm", stroke_width=4, stroke_fill=(10, 10, 10))

STOCKS = [("2016", 152.4), ("2017", 129.2), ("2018", 130.4), ("2019", 120.8), ("2020", 160.7), ("2021", 125.4), ("2022", 106.4), ("2023", 112.1), ("2024", 113.8), ("2025", 115.6), ("2026", 104.3)]
def stock_bars(c, t, t0):
    d = L.panel(c, (300, 230, 1620, 830), 228); x0, x1, yb = 400, 1520, 740
    d.text((W / 2, 275), "US diesel + heating oil in storage, mid-October (million barrels) · EIA", font=font(SANS, 32), fill=(235, 225, 210), anchor="mm")
    for k, (yr, v) in enumerate(STOCKS):
        u = ease((t - t0 - k * 0.08) / 0.5)
        if u <= 0: continue
        x = x0 + (x1 - x0) * k / (len(STOCKS) - 1); h = (v - 60) * 3.6 * u; col = RED if yr == "2026" else (120, 150, 196)
        d.rounded_rectangle((x - 36, yb - h, x + 36, yb), 8, fill=col); d.text((x, yb + 30), yr, font=font(SANS, 26), fill=(235, 225, 210), anchor="mm")
        if yr == "2026" and u > 0.8: d.text((x, yb - h - 40), "104", font=font(IMPACT, 50), fill=YELLOW, anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))

def flow_bars(c, t, t0, rows, title, unit="million barrels a day", box=(330, 280, 1590, 800)):
    d = L.panel(c, box, 228); d.text((W / 2, box[1] + 45), title, font=font(SANS, 32), fill=(235, 225, 210), anchor="mm")
    mx = max(v for _, v, _ in rows)
    for k, (lab, v, col) in enumerate(rows):
        u = ease((t - t0 - k * 0.7) / 0.8)
        if u <= 0: continue
        y = box[1] + 170 + k * 150; d.text((box[0] + 50, y), lab, font=font(SANS, 38), fill=(255, 255, 255), anchor="lm")
        bw = (box[2] - box[0] - 520) * v / mx * u; d.rounded_rectangle((box[0] + 380, y - 40, box[0] + 380 + bw, y + 40), 16, fill=col)
        d.text((box[0] + 400 + bw, y), f"{v:g}", font=font(IMPACT, 54), fill=YELLOW, anchor="lm", stroke_width=4, stroke_fill=(10, 10, 10))
    d.text((W / 2, box[3] - 40), unit, font=font(SANS, 28), fill=GREY, anchor="mm")

def refinery_grid(c, t, t0, t_hit):
    d = L.panel(c, (420, 250, 1500, 830), 228)
    d.text((W / 2, 295), "Russia's 32 major refineries, late August 2026 · IEA", font=font(SANS, 34), fill=(235, 225, 210), anchor="mm")
    for i in range(32):
        r, q = divmod(i, 8); x = 560 + q * 115; y = 400 + r * 110
        u = ease((t - t0 - i * 0.03) / 0.3)
        if u <= 0: continue
        hit = i < 28 and t >= t_hit + i * 0.05; col = RED if hit else (150, 145, 140)
        d.rounded_rectangle((x - 40 * u, y - 34 * u, x + 40 * u, y + 34 * u), 10, fill=col)
        d.rectangle((x - 22 * u, y - 60 * u, x - 10 * u, y - 34 * u), fill=col)
    if t >= t_hit + 1.6:
        d.text((W / 2, 790), "28 hit by drones · only 4 untouched", font=font(IMPACT, 48), fill=YELLOW, anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))

def days_card(c, t, t0, t_whole):
    d = L.panel(c, (330, 300, 1590, 820), 228)
    d.text((W / 2, 345), "Russian diesel deal vs American use (3.9 million barrels a day)", font=font(SANS, 34), fill=(235, 225, 210), anchor="mm")
    for i in range(10):
        x = 470 + i * 110; y = 520; on = (i == 0 and t >= t0 + 0.3) or (t >= t_whole + i * 0.12 and i < 9)
        col = YELLOW if on else (70, 62, 56); d.rounded_rectangle((x - 44, y - 50, x + 44, y + 50), 12, fill=col)
        d.text((x, y), f"{i + 1}", font=font(IMPACT, 44), fill=(20, 16, 12) if on else GREY, anchor="mm")
    if t >= t0 + 0.3: d.text((470, 630), "first shipment ≈ 1 day", font=font(SANS, 36), fill=(255, 255, 255), anchor="lm")
    if t >= t_whole + 1.0: d.text((1460, 700), "whole deal (up to 4.8M tons) ≈ 9 days", font=font(IMPACT, 48), fill=YELLOW, anchor="rm", stroke_width=4, stroke_fill=(10, 10, 10))

def senators(c, t, t0):
    d = L.panel(c, (560, 280, 1360, 640), 228); d.text((W / 2, 325), "12 senators, 13 Oct · CBS News", font=font(SANS, 34), fill=(235, 225, 210), anchor="mm")
    for i in range(12):
        u = ease((t - t0 - i * 0.07) / 0.3)
        if u <= 0: continue
        x = 660 + (i % 6) * 120; y = 420 + (i // 6) * 110; col = (200, 50, 45) if i < 6 else (60, 100, 200)
        d.ellipse((x - 40 * u, y - 40 * u, x + 40 * u, y + 40 * u), fill=col)
    d.text((W / 2, 610), "6 Republicans · 6 Democrats", font=font(SANS, 30), fill=(255, 255, 255), anchor="mm")

def cost_compare(c, t, t0, title, a_lab, a_v, b_lab, b_v, fmt, src_txt, box=(360, 280, 1560, 760)):
    d = L.panel(c, box, 228); d.text((W / 2, box[1] + 45), title, font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
    mx = max(a_v, b_v)
    for k, (lab, v, col) in enumerate(((a_lab, a_v, (150, 140, 130)), (b_lab, b_v, YELLOW))):
        u = ease((t - t0 - k * 0.7) / 0.8)
        if u <= 0: continue
        y = box[1] + 160 + k * 150; d.text((box[0] + 50, y), lab, font=font(SANS, 38), fill=(255, 255, 255), anchor="lm")
        bw = (box[2] - box[0] - 620) * v / mx * u; d.rounded_rectangle((box[0] + 390, y - 42, box[0] + 390 + bw, y + 42), 16, fill=col)
        d.text((box[0] + 410 + bw, y), fmt(v * u), font=font(IMPACT, 56), fill=YELLOW, anchor="lm", stroke_width=4, stroke_fill=(10, 10, 10))
    d.text(((box[0] + box[2]) / 2, box[3] - 40), src_txt, font=font(SANS, 28), fill=GREY, anchor="mm")

def forecast(c, t, t0):
    d = L.panel(c, (430, 260, 1490, 820), 228); d.text((W / 2, 305), "US diesel, yearly average · EIA forecast, 6 Oct 2026", font=font(SANS, 32), fill=(235, 225, 210), anchor="mm")
    for k, (yr, v, lab) in enumerate((("2025", 3.66, "actual"), ("2026", 5.19, "forecast"), ("2027", 4.49, "forecast"))):
        u = ease((t - t0 - k * 0.6) / 0.7)
        if u <= 0: continue
        x = 640 + k * 320; h = v * 62 * u; col = (150, 140, 130) if k == 0 else YELLOW
        d.rounded_rectangle((x - 70, 740 - h, x + 70, 740), 14, fill=col); d.text((x, 775), yr, font=font(SANS, 32), fill=(235, 225, 210), anchor="mm")
        d.text((x, 740 - h - 40), f"${v * u:.2f}", font=font(IMPACT, 54), fill=YELLOW, anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))

def recap(c, t, t0, t_rest):
    d = L.panel(c, (250, 230, 1670, 820), 230); d.text((W / 2, 280), "Where your $2 went", font=font(IMPACT, 64), fill=YELLOW, anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))
    x0, x1 = 330, 1590; d.rounded_rectangle((x0, 360, x1, 440), 16, fill=(120, 110, 100)); xt = x0 + (x1 - x0) * 0.08 / 2.04
    d.rounded_rectangle((x0, 360, xt, 440), 10, fill=RED); d.text((x0, 480), "≈ 8¢ tax", font=font(IMPACT, 44), fill=(255, 120, 110), anchor="lm")
    items = ["a barrel that makes less diesel than gas", "a world market that ships US diesel abroad", "Hormuz running at about half", "Russian refineries knocked offline"]
    for k, s in enumerate(items):
        if t >= t_rest + k * 0.9: put(c, pill(s, 40, (255, 255, 255), (60, 50, 40, 235)), W / 2, 560 + k * 66, popk(t, t_rest + k * 0.9))

# ------------------------------------------------------------------ places
HZ_LL = (56.25, 26.57); RYAZAN = (39.74, 54.58); MOSCOW = (37.62, 55.76); HOUSTON = (-95.0, 29.75); SANTOS = (-46.33, -23.96); ROTT = (4.14, 51.95)
NYH = (-74.05, 40.67); NCAR = (-78.64, 35.78); CALI = (-119.42, 36.78); ILLF = (-89.0, 40.0); DC = (-77.03, 38.9)
GULF_REF = [("Ras Tanura", (50.16, 26.64)), ("Jubail", (49.66, 27.01)), ("Al-Zour, Kuwait", (48.38, 28.73)), ("Ruwais, UAE", (52.73, 24.11))]
SHIPS = [(53.8, 26.6), (54.6, 26.3), (55.3, 26.5), (55.9, 26.6), (56.45, 26.45), (56.6, 26.1), (56.9, 25.5), (57.3, 25.1), (57.8, 24.7), (58.4, 24.3), (57.6, 25.35), (58.2, 24.95)]
CLOSED = [("Houston (LyondellBasell, 2025)", (-95.24, 29.71)), ("Los Angeles (Phillips 66, 2025)", (-118.25, 33.80)), ("Benicia (Valero, 2026)", (-122.15, 38.06))]
ROUTES = [((-118.2, 34.0), (-96.8, 32.8)), ((-122.3, 47.6), (-87.6, 41.9)), ((-95.4, 29.8), (-84.4, 33.7)), ((-87.6, 41.9), (-74.0, 40.7)), ((-104.9, 39.7), (-90.2, 38.6))]
def truck_icon():
    im = Image.new("RGBA", (150, 74), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 6, 104, 54), 6, fill=(245, 245, 240, 255), outline=(30, 30, 30, 255), width=3)
    d.rounded_rectangle((106, 22, 148, 54), 6, fill=(200, 60, 45, 255), outline=(30, 30, 30, 255), width=3); d.rectangle((118, 28, 140, 40), fill=(170, 210, 240, 255))
    for x in (20, 80, 126): d.ellipse((x - 11, 46, x + 11, 68), fill=(25, 25, 25, 255))
    return im
TRUCK = truck_icon()
def ship_icon(sc=1.0):
    im = Image.new("RGBA", (int(70 * sc), int(34 * sc)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = im.size
    d.polygon([(0, h * 0.35), (w, h * 0.35), (w * 0.85, h), (w * 0.12, h)], fill=(40, 40, 46, 255)); d.rectangle((w * 0.55, 0, w * 0.8, h * 0.35), fill=(230, 230, 230, 255))
    return im
SHIP = ship_icon(1.2); TANKER = ship_icon(1.8)
def arrow(c, cam, a_ll, b_ll, u, col=(230, 130, 70), width=8, dashed=False):
    (x0, y0), (x1, y1) = geo(cam, *a_ll), geo(cam, *b_ll); xe, ye = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    d = ImageDraw.Draw(c)
    if dashed:
        n = 24
        for k in range(n):
            if k % 2 == 0 and k / n < u: d.line((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n, x0 + (x1 - x0) * min(u, (k + 1) / n), y0 + (y1 - y0) * min(u, (k + 1) / n)), fill=col, width=width)
    else: d.line((x0, y0, xe, ye), fill=col, width=width)
    if u > 0.95:
        ang = math.atan2(y1 - y0, x1 - x0)
        d.polygon([(x1, y1), (x1 - 28 * math.cos(ang - 0.45), y1 - 28 * math.sin(ang - 0.45)), (x1 - 28 * math.cos(ang + 0.45), y1 - 28 * math.sin(ang + 0.45))], fill=col)

# ------------------------------------------------------------------ the montage
def overlay(c, t, cam):
    lon, lat, p = cam
    if p < 10:
        serif_label(c, "United States", *geo(cam, -99, 41), 34); serif_label(c, "Russia", *geo(cam, 80, 62), 34); serif_label(c, "Iran", *geo(cam, 54, 32.5), 30)
    # ---- HOOK (frame 1 = the payoff: two pump prices)
    if t < A["yearago"]:
        put(c, outlined("WHY IS DIESEL $2 MORE?", 100, fill=(255, 255, 255)), W / 2, 200, 1.0)
        put(c, SIGN_D, W / 2 - 250, 520, 1.0); put(c, SIGN_G, W / 2 + 250, 520, 1.0)
        src(c, "US averages, 22 Oct 2026 · AAA", t, A["oct22"], y=700)
    if A["yearago"] <= t < A["strange"]:
        put(c, OLD_D, W / 2 - 230, 480, popk(t, A["yearago"])); put(c, OLD_G, W / 2 + 230, 480, popk(t, A["yearago"] + 0.1))
        L.big(c, "GAP: 56¢ → $2.04", t, A["yearago"] + 0.6, y=220, size=110)
    if A["strange"] <= t < A["three"]:
        L.headline(c, "ALMOST NONE OF IT IS TAX", t, A["strange"] + 0.3, y=200, size=90)
    if A["three"] <= t < A["byend"]:
        for k, (lab, ll, tt) in enumerate((("the barrel", (-97.0, 39.0), A["barrel1"]), ("a strait", HZ_LL, A["strait1"]), ("a refinery", RYAZAN, A["refinery1"]))):
            if t >= tt: L.place(c, cam, lab, ll, popk(t, tt), (200, 40, 40), size=40)
        L.headline(c, "3 PLACES", t, A["three"], y=170, size=100)
    if A["byend"] <= t < CH[0][1]:
        L.headline(c, "WHERE YOUR $2 GOES", t, A["byend"], y=200, size=96); signs(c, t, A["byend"] + 0.3, y=560)
    # ---- 1 THE SIGN
    if CH[0][1] + 1.6 <= t < A["cal"] - 0.3:
        price_chart(c, t, CH[0][1] + 1.6, mark_record=t >= A["sept1"], gas_record=t >= A["record"] - 0.2)
        if t >= A["oneyear"] + 0.4 and t < A["sept1"]:
            put(c, pill("diesel +74% · gas +39% in a year · AAA", 40, YELLOW), W / 2, 175, popk(t, A["oneyear"] + 0.4))
    if A["cal"] - 0.3 <= t < A["nc"] - 0.3:
        L.place(c, cam, "California diesel: $8.49", CALI, popk(t, A["cal"]), RED, size=46); src(c, "most expensive state · AAA, 22 Oct", t, A["cal"] + 0.4, y=200)
    if A["nc"] - 0.3 <= t < A["different"]:
        L.place(c, cam, "North Carolina diesel: $5.59", NCAR, popk(t, A["nc"]), GREEN, size=46); src(c, "cheapest state · AAA, 22 Oct", t, A["nc"] + 0.4, y=200)
    if A["different"] <= t < CH[1][1]:
        L.headline(c, "WHY IS DIESEL DIFFERENT?", t, A["different"], y=200, size=96)
    # ---- 2 THE BARREL
    if CH[1][1] + 1.6 <= t < A["june"]: L.headline(c, "THIS SOUNDS FAKE", t, CH[1][1] + 1.6, y=200, size=96)
    if A["june"] <= t < A["moved"]:
        put(c, J04_D, 560, 520, popk(t, A["june"] + 0.3)); put(c, J04_G, 1020 if not PHOTOS else 560, 760 if PHOTOS else 520, popk(t, A["june"] + 0.5))
        L.big(c, "DIESEL WAS CHEAPER", t, A["june"] + 0.1, y=200, size=100)
    if A["moved"] <= t < A["federal"]:
        spread_bars(c, t, A["moved"] - 0.3)
        if t >= A["ulsd"]: put(c, pill("2006: ultra-low-sulfur diesel (EPA) · costs more to make and move", 34, YELLOW), W / 2, 175, popk(t, A["ulsd"]))
    if A["federal"] <= t < A["inside"]:
        tax_bar(c, t, A["federal"])
        if t >= A["taxman"]: put(c, sprite("host_cool", 300), 1700, 1040, popk(t, A["taxman"]), anchor="b")
    if A["inside"] <= t < A["trucks"]:
        barrel(c, t, A["inside"] + 0.6, hl_diesel=t >= A["slice"])
    if A["trucks"] <= t < A["northeast"] - 0.2:
        for k, (a_, b_) in enumerate(ROUTES):
            u = ((t - A["trucks"]) * 0.18 + k * 0.21) % 1.0; x0, y0 = geo(cam, *a_); x1, y1 = geo(cam, *b_)
            ImageDraw.Draw(c).line((x0, y0, x1, y1), fill=(90, 80, 70), width=6)
            put(c, TRUCK if x1 >= x0 else TRUCK.transpose(Image.FLIP_LEFT_RIGHT), x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 30, 0.8)
        L.big(c, "73%", t, A["trucks"] + 0.4, y=210, size=180, sub="of US freight by weight moves by truck · ATA")
        if t >= A["trains"]: put(c, pill("trains · tractors · ships · generators", 44, YELLOW), 700, 450, popk(t, A["trains"]))
    if A["northeast"] - 0.2 <= t < CH[2][1]:
        L.place(c, cam, "heating oil country", NYH, popk(t, A["northeast"] + 0.3), (230, 130, 70), size=40)
        L.headline(c, "HEATING OIL ≈ DIESEL", t, A["northeast"] + 1.2, y=190, size=90)
        if t >= A["squeezed"] - 0.5: put(c, pill("every fall: the heating season squeezes diesel · EIA", 38, YELLOW), W / 2, 300, popk(t, A["squeezed"] - 0.5))
    # ---- 3 THE WORLD MARKET
    if CH[2][1] + 1.6 <= t < A["houston"] - 0.3:
        if t < A["week16"]: L.headline(c, "AMERICA MAKES MORE DIESEL THAN IT USES", t, CH[2][1] + 1.6, y=200, size=72)
        else: balance_bars(c, t, A["week16"] + 0.3)
    if A["houston"] - 0.3 <= t < A["texas"] + 0.3:
        L.place(c, cam, "Houston", HOUSTON, popk(t, A["houston"]), (200, 40, 40))
        arrow(c, cam, HOUSTON, SANTOS, ease((t - A["brazil"] + 0.3) / 1.2)); arrow(c, cam, HOUSTON, ROTT, ease((t - A["rotterdam"] + 0.3) / 1.2))
        if t >= A["brazil"]: L.place(c, cam, "Brazil", SANTOS, popk(t, A["brazil"]), (230, 130, 70))
        if t >= A["rotterdam"]: L.place(c, cam, "Rotterdam", ROTT, popk(t, A["rotterdam"]), (230, 130, 70))
        if t >= A["rotterdam"] + 1.0: L.headline(c, "TO WHOEVER PAYS MOST", t, A["rotterdam"] + 1.0, y=170, size=86)
    if A["texas"] + 0.3 <= t < A["cushion"]:
        L.big(c, "TEXAS DIESEL, WORLD PRICE", t, A["texas"] + 0.3, y=200, size=96)
    if A["cushion"] <= t < A["eastcoast"] - 0.3: stock_bars(c, t, A["cushion"] + 0.2)
    if A["eastcoast"] - 0.3 <= t < A["fewer"] - 0.2:
        L.place(c, cam, "East Coast stocks: -32% vs normal (Sept)", NYH, popk(t, A["eastcoast"]), RED, size=40); src(c, "EIA", t, A["eastcoast"] + 0.4, y=200)
    if A["fewer"] - 0.2 <= t < A["slack"]:
        for k, (nm, ll) in enumerate(CLOSED):
            if t >= A["fewer"] + 0.4 + k * 0.4: L.place(c, cam, nm, ll, popk(t, A["fewer"] + 0.4 + k * 0.4), (60, 60, 70), size=30, dy=-46 - 52 * (k % 2))
        L.big(c, "-1,000,000 BARRELS A DAY", t, A["fewer"] + 1.4, y=190, size=86, sub="of US refining capacity since 2020 (~5%) · EIA")
        if t >= A["left"]: put(c, pill("the rest run at 93.4% · EIA, 16 Oct", 40, YELLOW), W / 2, 790, popk(t, A["left"]))
    if A["slack"] <= t < CH[3][1]:
        L.headline(c, "THEN THE WORLD LOST TWO SUPPLIERS", t, A["suppliers"] - 0.6, y=190, size=76)
        for k, (nm, ll) in enumerate((("1", HZ_LL), ("2", RYAZAN))):
            if t >= A["suppliers"] + k * 0.4: L.place(c, cam, nm, ll, popk(t, A["suppliers"] + k * 0.4), RED, size=48)
    # ---- 4 HORMUZ
    if CH[3][1] + 1.6 <= t < A["feb"]:
        hx, hy = geo(cam, *HZ_LL); serif_label(c, "Strait of Hormuz", hx - 40, hy - 150, 46); serif_label(c, "Iran", *geo(cam, 57.0, 28.6), 48); serif_label(c, "Oman", *geo(cam, 56.6, 24.0), 40)
        L.big(c, "~1/5 OF THE WORLD'S OIL", t, A["fifth"] - 0.2, y=190, size=96, sub="normally passed here · EIA (2024)")
    if A["feb"] <= t < A["halfflow"] - 0.4:
        price_chart(c, t, A["feb"] - 2.0, upto=14, mark_war=True, title="US diesel vs gas, weekly · EIA")
        if t >= A["twoweeks"]: put(c, outlined("+$1.05 IN 2 WEEKS", 90, fill=YELLOW, f=IMPACT, stroke=8), W / 2, 170, popk(t, A["twoweeks"]))
    if A["halfflow"] - 0.4 <= t < A["dangerous"] - 0.2:
        flow_bars(c, t, A["halfflow"] - 0.2, [("before the war (2024)", 20.0, (150, 140, 130)), ("September 2026", 10.9, YELLOW)], "Oil through the Strait of Hormuz · EIA / IEA")
    if A["dangerous"] - 0.2 <= t < A["gulf"] - 0.3:
        hx, hy = geo(cam, *HZ_LL); serif_label(c, "Strait of Hormuz", hx - 40, hy - 150, 46)
        for k, ll in enumerate(SHIPS):
            x, y = geo(cam, *ll); kk = popk(t, A["ships12"] - 0.3 + k * 0.08)
            if kk > 0: put(c, SHIP, x, y, kk); ImageDraw.Draw(c).ellipse((x - 34, y - 34, x + 34, y + 34), outline=(220, 40, 40), width=5)
        L.big(c, "12 SHIPS ATTACKED IN ONE WEEK", t, A["ships12"], y=190, size=86, sub="5-11 Oct, reported to UKMTO · BBC Verify · positions illustrative")
    if A["gulf"] - 0.3 <= t < A["middle"]:
        for k, (nm, ll) in enumerate(GULF_REF):
            if t >= A["gulf"] + k * 0.3: L.place(c, cam, nm, ll, popk(t, A["gulf"] + k * 0.3), (60, 60, 70), size=32)
        u = ease((t - A["gulf"] - 1.6) / 1.4)
        for nm, ll in GULF_REF: arrow(c, cam, ll, (58.6, 25.0), u, col=(230, 130, 70), width=6)
        L.headline(c, "EVERYTHING EXITS THROUGH HERE", t, A["gulf"] + 1.2, y=170, size=80)
    if A["middle"] <= t < CH[4][1]:
        flow_bars(c, t, A["middle"] + 0.4, [("before the war", 4.7, (150, 140, 130)), ("September 2026", 1.9, YELLOW)], "Middle East exports of refined fuels · IEA")
    # ---- 5 RUSSIA
    if CH[4][1] + 1.6 <= t < A["drones"]:
        L.place(c, cam, "Moscow", MOSCOW, 1.0, (60, 60, 70)); L.big(c, "WORLD'S TOP SEABORNE DIESEL EXPORTER", t, A["seaborne"] - 0.6, y=190, size=72, sub="Russia, until recently · Reuters (2023)")
    if A["drones"] <= t < A["ryazan"] - 0.4:
        refinery_grid(c, t, A["drones"] + 0.2, A["august"])
        if A["every3"] <= t < A["august"]: put(c, outlined("1 STRIKE EVERY 3 DAYS", 84, fill=YELLOW, f=IMPACT, stroke=8), W / 2, 170, popk(t, A["every3"]))
    if A["ryazan"] - 0.4 <= t < A["estimates"]:
        rx, ry = geo(cam, *RYAZAN); pin(c, rx, ry, (40, 30, 20)); serif_label(c, "Ryazan", rx + 110, ry + 10, 46); serif_label(c, "Moscow", *geo(cam, *MOSCOW), 38)
        stamp(c, "CRUDE UNIT HALTED", rx + 40, ry - 230, t, A["ryazan"] + 1.2)
        src(c, "Ukrainian drone strike, 15 Oct 2026 · Reuters", t, A["ryazan"] + 0.4, y=200)
    if A["estimates"] <= t < A["july"]:
        L.big(c, "~HALF OFFLINE (AT TIMES)", t, A["estimates"] + 0.2, y=200, size=100, sub="Russian refining capacity, by some estimates · not all verified")
    if A["july"] <= t < A["together"] - 0.2:
        stamp(c, "DIESEL EXPORT BAN", *geo(cam, 44.0, 57.0), t, A["july"] + 0.4, rot=-6, size=84)
        if t >= A["lowest"]: L.big(c, "LOWEST SINCE 2016", t, A["lowest"] + 0.2, y=200, size=110, sub="Russian diesel exports, 1-10 Oct · Vortexa via Bloomberg")
    if A["together"] - 0.2 <= t < A["hole"]:
        L.big(c, "-60%", t, A["together"] + 0.8, y=260, size=220, sub="diesel exports, Russia + Middle East, Sept vs a year ago · IEA", sub_y=430)
    if A["hole"] <= t < A["wholesale"]:
        L.headline(c, "THE HOLE", t, A["hole"], y=170, size=110)
        if t >= A["bidding"]:
            for k, ll in enumerate(((10.0, 50.0), (32.0, 39.0), (-47.0, -15.0), (-95.0, 35.0))):
                L.place(c, cam, "?", ll, popk(t, A["bidding"] + k * 0.25), (230, 130, 70), size=40)
    if A["wholesale"] <= t < CH[5][1]:
        L.big(c, "~$220 A BARREL", t, A["wholesale"] + 0.6, y=220, size=150, sub="wholesale diesel, Europe and the US, September · IEA · all-time high")
    L.subscribe_nudge(c, t, A["bidding"] + 0.4, A["wholesale"] + 0.2, x=1560, y=620)
    # ---- 6 THE DEAL
    if CH[5][1] + 1.6 <= t < A["senators"] - 0.2:
        u = ease((t - A["license"]) / 6.0); arrow(c, cam, (28.6, 60.3), (-73.5, 40.5), u, col=(190, 70, 50), width=7, dashed=True)
        L.place(c, cam, "?", (-73.5, 40.5), popk(t, A["license"] + 1.0), (190, 70, 50), size=40, dy=60)
        L.big(c, "RUSSIAN DIESEL: ALLOWED IN", t, A["license"], y=190, size=96, sub="US Treasury license, 9 Oct · until 7 Apr 2027")
        if t >= A["plan"]: put(c, pill("plan announced: up to 4.8 million tons", 40, YELLOW), W / 2, 790, popk(t, A["plan"]))
    if A["senators"] - 0.2 <= t < A["shipment"] - 0.2:
        senators(c, t, A["senators"])
        if t >= A["gift"] - 0.3: put(c, outlined("\"a gift to our adversary\"", 76, fill=YELLOW), W / 2, 760, popk(t, A["gift"] - 0.3))
    if A["shipment"] - 0.2 <= t < A["dehaan"]: days_card(c, t, A["shipment"], A["wholedeal"])
    if A["dehaan"] <= t < CH[6][1]:
        L.big(c, "-10 TO 15¢ A GALLON", t, A["dehaan"] + 0.6, y=200, size=110, sub="at most, if it arrives · Patrick De Haan, GasBuddy")
        if t >= A["tanker1"]: put(c, pill("22 Oct: the first tanker was only just leaving Russia", 38, YELLOW), W / 2, 420, popk(t, A["tanker1"]))
    # ---- 7 WHO PAYS
    if CH[6][1] + 1.6 <= t < A["fillup"]:
        cost_compare(c, t, A["truckers"] + 0.8, "Fuel cost per mile for a truck", "2025 average", 0.48, "at today's price", 0.83, lambda v: f"{v * 100:.0f}¢",
                     "ATRI 2025 · today: our math at $6.28 (EIA)", box=(200, 240, 1260, 700))
        if t >= A["math"]: put(c, outlined("≈ +$30,000 A YEAR", 110, fill=YELLOW, f=IMPACT, stroke=9), 710, 790, popk(t, A["math"]))
    if A["fillup"] <= t < A["farmers"]:
        cost_compare(c, t, A["fillup"] + 0.4, "A semi fill-up, ~250 gallons (our math, AAA prices)", "Oct 2025", 907, "Oct 2026", 1577, lambda v: f"${v:,.0f}", "AAA 22 Oct 2026 vs a year ago")
    if A["farmers"] <= t < A["homes"] - 0.3:
        L.place(c, cam, "Illinois farm diesel", ILLF, popk(t, A["farmers"]), (60, 150, 80), size=40)
        L.big(c, "$3.01 → $5.61", t, A["farmers"] + 1.2, y=190, size=120, sub="a gallon, Sep 2025 to Sep 2026 · Farm Bureau / USDA")
        if t >= A["corn"]: put(c, pill("harvest diesel: about +$8 per acre of corn · AFBF", 40, YELLOW), W / 2, 790, popk(t, A["corn"]))
    if A["homes"] - 0.3 <= t < A["groceries"] - 0.2:
        L.place(c, cam, "heating oil: $6.19 a gallon", NYH, popk(t, A["homes"]), (230, 130, 70), size=40)
        L.big(c, "+21% THIS WINTER", t, A["homes"] + 2.0, y=190, size=120, sub="heating-oil household bills, forecast · EIA")
    if A["groceries"] - 0.2 <= t < CH[7][1]:
        L.big(c, "GROCERIES: +1.8%", t, A["groceries"] + 1.6, y=200, size=130, col=(255, 255, 255), sub="food at home, Sept vs a year ago · BLS")
        if t >= A["react"] - 0.6:
            for k, s in enumerate(("diesel", "freight + farms", "food prices (later, partly)")):
                if t >= A["react"] - 0.6 + k * 0.6: put(c, pill(s, 46, YELLOW if k < 2 else (255, 255, 255)), (450, 900, 1500)[k], 560, popk(t, A["react"] - 0.6 + k * 0.6))
        if t >= A["pressure"]: put(c, outlined("NOT ON YOUR RECEIPT... YET", 74, fill=YELLOW), W / 2, 720, popk(t, A["pressure"] + 0.8))
    # ---- 8 WHAT'S NEXT
    if CH[7][1] + 1.6 <= t < A["iea"]: forecast(c, t, A["eia"])
    if A["iea"] <= t < A["change"]: L.big(c, "TIGHT INTO 2027", t, A["iea"] + 0.4, y=210, size=130, sub="International Energy Agency, 14 Oct 2026")
    if A["change"] <= t < A["until"]:
        L.headline(c, "WHAT COULD BRING IT DOWN", t, A["change"], y=170, size=86)
        for k, s in enumerate(("Hormuz really reopens", "a Russia-Ukraine deal", "refineries come back", "the world uses less")):
            if t >= A["change"] + 0.8 + k * 0.9: put(c, pill(s, 46, YELLOW), W / 2, 330 + k * 100, popk(t, A["change"] + 0.8 + k * 0.9))
    if A["until"] <= t < A["nexttime"]: recap(c, t, A["until"], A["rest"])
    if A["nexttime"] <= t < A["subscribe"] - 0.4:
        put(c, SIGN_D, W / 2 - 250, 520, popk(t, A["nexttime"])); put(c, SIGN_G, W / 2 + 250, 520, popk(t, A["nexttime"] + 0.1))
        L.headline(c, "NOW YOU KNOW", t, A["nexttime"] + 1.2, y=220, size=110)
    if A["subscribe"] - 0.4 <= t < A["endscreen"]:
        put(c, sprite("host_cool", 480), 1560, 1020, popk(t, A["subscribe"] - 0.4), anchor="b")
        put(c, pill("SUBSCRIBE · maps for the news that hits your wallet", 50, (255, 255, 255), (200, 30, 30, 240)), W / 2 - 160, 300, popk(t, A["subscribe"] - 0.1))
    for f, t0, t1, x, y, w, rot, cr in PHOTOS: L.photo(c, f, t, t0, t1, x=x, y=y, w=w, rot=rot, credit=cr)
    L.end_screen(c, t, A["endscreen"], "more money maps?")
    L.chapter_card(c, t, CH)

SFX = []
for nm in ("yearago", "three", "sept1", "cal", "nc", "june", "federal", "inside", "trucks", "week16", "houston", "cushion", "fewer", "fifth", "twoweeks",
           "ships12", "drones", "ryazan", "july", "together", "wholesale", "license", "senators", "shipment", "dehaan", "math", "fillup", "farmers",
           "homes", "groceries", "eia", "iea", "until"):
    SFX.append(("pop", A[nm] + 0.35, -20))
for name, t0 in CH: SFX.append(("paper_slide", t0, -20))
SFX += [("pop", ph[1], -19) for ph in PHOTOS]
SFX += [("sticker_slap", A["ryazan"] + 1.2, -20), ("sticker_slap", A["july"] + 0.4, -20), ("cash_register", A["nexttime"], -22),
        ("paper_slide", A["endscreen"], -18), ("pop", A["endscreen"] + 2.3, -20)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END, "| photos", len(PHOTOS)); print("MISSING", MISSING)
    else: K.main(sys.argv, overlay, SFX)
