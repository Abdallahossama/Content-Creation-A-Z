"""Habibi Explains the News — Short #5 "Why Diesel Costs $2 More Than Gas ⛽" (post Wed 21 Oct; re-check AAA that morning).
Engine: _style_kit/tools/shortkit.py.   python render_s05.py build | qa t.. | caps | seg i n | audio | final | all"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, sprite, panel, pin, W, H, YEL, SANS, IMPACT

DIESEL, GAS, CA = "$6.32", "$4.30", "$8.51"              # AAA 18 Oct 2026 (re-check before posting)
K.setup(root="D:/why habibi/shorts/s05_diesel/", vo="vo/s05_vo_chatterbox.wav", lat_mid=40, pyr=[10, 20, 40, 80],
        fills=[("United States of America", (120, 150, 196)), ("Russia", (190, 70, 50)), ("Iran", (206, 150, 70))],
        music="Stay the Course.mp3", out="Ask_Habibi_Short05_Diesel.mp4", fill_alpha=0.6, cap_fix=[("U .S.", "US"), ("U .S", "US")])
at = K.at
def after(word, n=1, d=0.0): return at(word, n) + d
T = dict(first=at("first"), fifth=at("fifth"), week=at("week"), twelve=at("12"), second=at("second"), drone=at("drone"),
         used=at("used"), lowest=at("lowest"), together=at("together"), moves=at("moves"), trucks=at("trucks"),
         so=at("so", 1), senators=at("senators"), analysts=at("analysts"), next=at("next"), sign=at("sign"))
END = K.DUR
USA = (-97.0, 38.0, 16); WORLD = (-10.0, 38.0, 6.6); HORMUZ = (56.4, 26.2, 62); RUS = (38.0, 54.5, 24); MER = (46.0, 42.0, 11)
K.set_camera([(0.0, *USA), (T["first"] - 0.4, *USA), (T["first"] + 0.6, *WORLD), (T["fifth"] - 0.6, *HORMUZ), (T["second"] - 0.4, 56.2, 26.4, 66),
              (T["second"] + 0.8, *RUS), (T["together"] - 0.3, 39.0, 54.8, 26), (T["together"] + 0.6, *MER), (T["moves"] - 0.4, *MER),
              (T["moves"] + 0.6, *WORLD), (T["trucks"] - 0.2, *USA), (END + 1, *USA)])
HZ = (56.25, 26.57); RYAZAN = (39.70, 54.58); PRIMORSK = (28.61, 60.36); SAC = (-121.49, 38.58)
SHIPS = [(53.8, 26.6), (54.6, 26.3), (55.3, 26.5), (55.9, 26.6), (56.45, 26.45), (56.6, 26.1), (56.9, 25.5), (57.3, 25.1),
         (57.8, 24.7), (58.4, 24.3), (57.6, 25.35), (58.2, 24.95)]

def price_sign(label, price, col, w=430):
    im = Image.new("RGBA", (w, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 229), 26, fill=(24, 22, 26, 238), outline=col + (255,), width=6)
    d.text((w / 2, 52), label, font=font(SANS, 42), fill=(235, 230, 220), anchor="mm")
    d.text((w / 2, 150), price, font=font(IMPACT, 110), fill=col, anchor="mm", stroke_width=5, stroke_fill=(10, 10, 10)); return im
SIGN_D = price_sign("DIESEL", DIESEL, YEL); SIGN_G = price_sign("GAS", GAS, (235, 235, 235))
def ship(sc=1.0):
    im = Image.new("RGBA", (int(70 * sc), int(34 * sc)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = im.size
    d.polygon([(0, h * 0.35), (w, h * 0.35), (w * 0.85, h), (w * 0.12, h)], fill=(40, 40, 46, 255)); d.rectangle((w * 0.55, 0, w * 0.8, h * 0.35), fill=(230, 230, 230, 255))
    return im
SHIP = ship(1.2)
def truck():
    im = Image.new("RGBA", (150, 74), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 6, 104, 54), 6, fill=(245, 245, 240, 255), outline=(30, 30, 30, 255), width=3)
    d.rounded_rectangle((106, 22, 148, 54), 6, fill=(200, 60, 45, 255), outline=(30, 30, 30, 255), width=3); d.rectangle((118, 28, 140, 40), fill=(170, 210, 240, 255))
    for x in (20, 80, 126): d.ellipse((x - 11, 46, x + 11, 68), fill=(25, 25, 25, 255))
    return im
TRUCK = truck()
ROUTES = [((-118.2, 34.0), (-96.8, 32.8)), ((-122.3, 47.6), (-87.6, 41.9)), ((-95.4, 29.8), (-84.4, 33.7)), ((-87.6, 41.9), (-74.0, 40.7)), ((-104.9, 39.7), (-90.2, 38.6))]

def overlay(c, t, cam):
    lon, lat, p = cam; d = ImageDraw.Draw(c)
    if p < 10:
        serif_label(c, "United States", *geo(cam, -99, 41), 34); serif_label(c, "Russia", *geo(cam, 70, 62), 34); serif_label(c, "Iran", *geo(cam, 54, 32.5), 30)
    # B1 frame 1 (+ loop): the two pump prices
    loop = T["sign"] - 0.3
    if t < T["first"] - 0.1 or t >= loop:
        t0 = 0.0 if t < T["first"] else loop; k0 = (lambda dd: 1.0) if t0 == 0 else (lambda dd: popk(t, t0 + dd))
        put(c, outlined("WHY IS DIESEL", 90), W / 2, 300, k0(0)); put(c, outlined("$2 MORE THAN GAS?", 84, emoji="⛽"), W / 2, 400, k0(0))
        put(c, SIGN_D, 300, 640, k0(0.1)); put(c, SIGN_G, 790, 640, k0(0.2))
        put(c, pill("US averages · AAA, 18 Oct", 32), W / 2, 790, k0(0.3))
        if p > 12:
            x, y = geo(cam, *SAC); pin(c, x, y, (200, 40, 40)); put(c, pill(f"California diesel: {CA}", 32, (255, 225, 120), (150, 40, 30, 235)), x + 200, y + 70)
    # B2 Hormuz
    if T["first"] - 0.1 <= t < T["second"] - 0.1:
        hx, hy = geo(cam, *HZ)
        if p > 20: serif_label(c, "Strait of Hormuz", hx - 40, hy - 150, 44); serif_label(c, "Iran", *geo(cam, 57.5, 27.6), 46); serif_label(c, "Oman", *geo(cam, 56.7, 24.2), 40)
        if t >= T["fifth"] - 0.2:
            put(c, outlined("~1/5 OF THE WORLD'S OIL", 74, fill=YEL), W / 2, 330, popk(t, T["fifth"] - 0.2))
            put(c, pill("normally passes here · EIA", 36), W / 2, 430, popk(t, T["fifth"]))
        if t >= T["twelve"] - 0.2:
            for k, ll in enumerate(SHIPS):
                x, y = geo(cam, *ll); kk = popk(t, T["twelve"] - 0.2 + k * 0.08)
                if kk > 0:
                    put(c, SHIP, x, y, kk); ImageDraw.Draw(c).ellipse((x - 34, y - 34, x + 34, y + 34), outline=(220, 40, 40), width=5)
            put(c, outlined("12 SHIPS ATTACKED", 92, fill=(255, 255, 255)), W / 2, 560, popk(t, T["twelve"]))
            put(c, pill("in one week · BBC Verify / UKMTO", 36), W / 2, 670, popk(t, T["twelve"] + 0.2))
    # B3 Russia: Ryazan refinery, exports at a low
    if T["second"] - 0.1 <= t < T["together"] - 0.1:
        rx, ry = geo(cam, *RYAZAN); pin(c, rx, ry, (40, 30, 20)); serif_label(c, "Ryazan", rx + 110, ry + 10, 40)
        serif_label(c, "Moscow", *geo(cam, 37.6, 56.1), 34); serif_label(c, "Russia", *geo(cam, 44.0, 57.5), 56)
        if t >= T["drone"]:
            st = Image.new("RGBA", (520, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); red = (200, 30, 30, 240)
            sd.rounded_rectangle((5, 5, 515, 115), 16, outline=red, width=8); sd.text((260, 60), "KEY UNIT SHUT", font=font(IMPACT, 76), fill=red, anchor="mm")
            st = st.rotate(8, expand=True, resample=Image.BICUBIC); put(c, st, rx + 60, ry - 230, popk(t, T["drone"] + 0.4))
            put(c, pill("refinery hit by a Ukrainian drone, 15 Oct · Reuters", 32), W / 2, 330, popk(t, T["drone"] + 0.6))
        if t >= T["used"]: put(c, pill("2023: the world's top seaborne diesel exporter · Vortexa", 30), W / 2, 420, popk(t, T["used"]))
        if t >= T["lowest"]:
            put(c, outlined("LOWEST SINCE 2016", 90, fill=YEL, f=IMPACT, stroke=8), W / 2, 540, popk(t, T["lowest"]))
            put(c, pill("Russian diesel exports, 1-10 Oct · Vortexa", 34), W / 2, 640, popk(t, T["lowest"] + 0.2))
    # B4 together: -60%
    if T["together"] - 0.1 <= t < T["moves"] - 0.1:
        put(c, outlined("-60%", 190, fill=YEL, f=IMPACT, stroke=10), W / 2, 360, popk(t, T["together"] + 0.4))
        put(c, pill("diesel exports, Middle East + Russia · IEA, Sept", 34), W / 2, 500, popk(t, T["together"] + 0.6))
    # B5 diesel moves America: trucks on the highways
    if T["moves"] - 0.1 <= t < T["so"] - 0.1:
        for k, (a, b) in enumerate(ROUTES):
            u = ((t - T["moves"]) * 0.18 + k * 0.21) % 1.0; x0, y0 = geo(cam, *a); x1, y1 = geo(cam, *b)
            ImageDraw.Draw(c).line((x0, y0, x1, y1), fill=(90, 80, 70), width=6)
            put(c, TRUCK if x1 >= x0 else TRUCK.transpose(Image.FLIP_LEFT_RIGHT), x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 30, 0.8 if p > 12 else 0.0)
        if t >= T["trucks"]:
            put(c, outlined("73%", 190, fill=YEL, f=IMPACT, stroke=10), W / 2, 340, popk(t, T["trucks"] + 0.6))
            put(c, pill("of US freight moves by truck · ATA", 38), W / 2, 480, popk(t, T["trucks"] + 0.8))
    # B6 the US response
    if T["so"] - 0.1 <= t < loop:
        put(c, pill("US: Russian diesel allowed in until 7 Apr 2027 · Treasury", 32, (255, 225, 120)), W / 2, 330, popk(t, T["so"] + 0.4))
        u = ease((t - T["so"]) / 5.0); x0, y0 = geo(cam, -52.0, 38.5); x1, y1 = geo(cam, -73.4, 40.3)
        put(c, SHIP, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 1.6 if t >= T["so"] else 0.0)
        if t >= T["so"]: put(c, pill("Russian diesel", 30), x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + 60)
        if t >= T["senators"]: put(c, pill("senators from both parties: reverse it", 38), W / 2, 430, popk(t, T["senators"] + 0.2))
        if t >= T["analysts"]: put(c, outlined("≈ 3-4 DAYS", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 580, popk(t, T["analysts"] + 0.6))
        if t >= T["analysts"]: put(c, pill("of US diesel use · TD Economics", 36), W / 2, 700, popk(t, T["analysts"] + 0.8))

SFX = [("pop", 0.15, -20), ("pop", T["fifth"] - 0.2, -18), ("pop", T["twelve"], -18), ("sticker_slap", T["drone"] + 0.4, -20), ("pop", T["lowest"], -18),
       ("pop", T["together"] + 0.4, -16), ("pop", T["trucks"] + 0.6, -16), ("pop", T["so"] + 0.4, -20), ("pop", T["analysts"] + 0.6, -18), ("cash_register", T["sign"] - 0.3, -22)]

if __name__ == "__main__":
    K.main(sys.argv, overlay, SFX)
