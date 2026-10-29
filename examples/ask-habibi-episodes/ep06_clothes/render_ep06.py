"""Ask Habibi Ep 6 "Why Did Humans Start Wearing Clothes?" — 16:9 long form, fast montage on shortkit + longkit.
  python render_ep06.py build | qa t.. | anchors | allseg [n] | audio | final"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, serif_label, sprite, pin, YEL, SANS, IMPACT
import longkit as L
sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep06_clothes")

ROOT = "D:/why habibi/6th video/"
K.setup(root=ROOT, vo="vo/ep06_vo_v2.wav", lat_mid=40, pyr=[10, 20, 40, 80, 160, 320], size=(1920, 1080), cap_size=64, tail=21.5,
        fills=[], out="Ask_Habibi_Ep06_Why_Humans_Wear_Clothes.mp4",
        cap_fix=[("Otzi", "Ötzi"), ("Oetzi", "Ötzi")])
W, H = K.W, K.H
A = L.Anchors(); a = A.a
# ------------------------------------------------------------------ anchors (one per beat)
a("look", "look"); a("nobody", "nobody"); a("naked1", "naked"); a("dressed", "dressed"); a("louse1", "louse"); a("modesty1", "modesty"); a("habibi", "habibi")
a("strange", "strange"); a("mammals", "mammals"); a("fossilize", "fossilize"); a("genetic", "genetic"); a("protects", "protects"); a("heat1", "heat", 1, "protects")
a("sweat1", "sweat", 1, "heat1"); a("trap", "trap"); a("upgrade", "upgrade"); a("comfortable", "comfortable"); a("colder1", "colder"); a("iceage1", "ice", 1, "colder1")
a("comes", "comes"); a("kinds", "kinds"); a("seams", "seams"); a("exist", "exist"); a("split", "split"); a("dna1", "dna"); a("florida", "florida")
a("range", "range"); a("translation", "translation"); a("tools1", "tools", 1, "translation")
a("rabat", "rabat"); a("scraping", "scraping"); a("carnivores", "carnivores"); a("butchering", "butchering"); a("jacket", "jacket"); a("neander1", "neanderthals")
a("georgia", "georgia"); a("string1", "string")
a("invention", "invention"); a("draped1", "draped"); a("poncho", "poncho"); a("coldest1", "coldest"); a("linked", "linked", 1, "coldest1"); a("denisova", "denisova")
a("caucasus", "caucasus"); a("fitted1", "fitted"); a("wind", "wind"); a("fancy", "fancy"); a("sunghir", "russia", 1, "fancy"); a("sewn1", "sewn", 1, "sunghir")
a("fashion1", "fashion")
a("froze", "froze"); a("maximum", "maximum"); a("planet", "planet"); a("locked", "locked"); a("beringia", "beringia"); a("survive1", "survive", 1, "beringia")
a("alaska2", "alaska", 2); a("oregon1", "oregon"); a("moccasin", "moccasin"); a("sandals", "sandals")
a("alps", "alps"); a("iceman", "iceman"); a("bear", "bear"); a("linen", "linen"); a("again", "again"); a("archaeologist", "archaeologist", 1, "again")
a("fiber", "fiber", 1, "archaeologist")
a("why_end", "why", 1, "fiber"); a("modesty2", "modesty", 1, "why_end"); a("fur_end", "fur", 1, "modesty2"); a("borrowed", "borrowed"); a("needle_end", "needle", 1, "borrowed")
a("lice_end", "lice", 1, "needle_end"); a("subscribe", "subscribe", 1, "lice_end")
try: a("sub_mid", "quick", 1, "string1"); a("sub_more", "more", 1, "sub_mid"); a("sub_word", "subscribe", 1, "sub_mid")
except KeyError: A["sub_mid"] = A["sub_more"] = A["sub_word"] = -99.0      # before the subscribe line is inserted
A["endscreen"] = K.WORDS[-1]["e"] + 0.6
END = K.DUR
CH = [("THE NAKED APE", A["strange"] - 0.6), ("THE LOUSE WITNESS", A["comes"] - 0.6), ("THE FIRST TAILORS", A["rabat"] - 1.8),
      ("THE NEEDLE", A["invention"] - 1.2), ("THE WORLD FREEZES", A["froze"] - 0.5), ("FROM SURVIVAL TO STYLE", A["alps"] - 2.2), ("SO... WHY?", A["why_end"] - 0.4)]
K.CFG["music"] = [("Floating Cities.mp3", 0.0), ("Promises to Keep.mp3", A["rabat"] - 2.0), ("Rising Tide.mp3", A["froze"] - 1.0), ("Stay the Course.mp3", A["why_end"] - 0.8)]

# ------------------------------------------------------------------ places + camera
P = dict(Contrebandiers=(-6.96, 33.92), PechAze=(1.2, 44.85), Dzudzuana=(43.32, 42.31), Denisova=(84.68, 51.40), Mezmaiskaya=(40.0, 44.17),
         Yana=(135.4, 70.7), Europe=(14.0, 47.0), Sunghir=(40.50, 56.18), Beringia=(-168.98, 65.75), Alaska=(-146.1, 64.3),
         CougarMtn=(-121.2, 43.45), FortRock=(-121.10, 43.37), Otzi=(10.84, 46.78), Tarkhan=(31.23, 29.50), Blombos=(21.2, -34.4))
WORLD = (20.0, 30.0, 8.5); AFRICA = (18.0, 5.0, 16); MOROCCO = (-6.0, 32.5, 40); FRANCE = (1.0, 46.0, 40); GEORGIA = (43.0, 42.5, 40)
EURASIA = (75.0, 46.0, 9.6); SIBERIA = (85.0, 52.0, 22); NORTH = (-35.0, 44.0, 9.2); BERING = (-170.0, 63.0, 30); OREGON = (-121.0, 43.8, 34)
ALPS = (10.8, 46.5, 40); EGYPT = (31.0, 28.0, 28); SUNG = (42.0, 55.0, 26)
MED = "D:/why habibi/_media/"; PH = MED + "photos_2026-10-18/"; LB = MED + "cutouts/louse_body.png"; LH = MED + "cutouts/louse_head.png"
BM = PH + "world_bluemarble_5400.jpg"; BMB = (-180.0, 180.0, -90.0, 90.0)
def ph(name): return PH + name if os.path.exists(PH + name) and os.path.getsize(PH + name) > 50000 else None
def cam_keys():
    k = [(0.0, *WORLD), (A["naked1"], *AFRICA), (A["louse1"], *WORLD), (A["habibi"], *AFRICA), (A["strange"], *AFRICA), (A["genetic"], *AFRICA),
         (A["comfortable"], *AFRICA), (A["iceage1"], *NORTH), (A["comes"], *WORLD), (A["florida"], *AFRICA), (A["translation"], *WORLD),
         (A["rabat"] - 0.3, *MOROCCO), (A["neander1"], *FRANCE), (A["georgia"] - 0.3, *GEORGIA), (A["invention"], *EURASIA), (A["denisova"] - 0.3, *SIBERIA),
         (A["caucasus"], *EURASIA), (A["fitted1"], *EURASIA), (A["sunghir"] - 0.2, *SUNG), (A["froze"], *NORTH), (A["beringia"] - 0.3, *BERING),
         (A["alaska2"] - 0.3, -150.0, 60.0, 28), (A["oregon1"] - 0.3, *OREGON), (A["alps"] - 1.6, *WORLD), (A["alps"] - 0.4, *ALPS), (A["linen"] - 1.3, 20.0, 37.0, 22), (A["linen"] - 0.4, *EGYPT), (A["fiber"], *WORLD),
         (A["why_end"], *WORLD), (A["borrowed"], *EURASIA), (A["lice_end"], *WORLD), (END + 2, *WORLD)]
    return L.hold_keys(k)
K.set_camera(cam_keys())

# ------------------------------------------------------------------ drawings
from ep06_draw import louse
LOUSE = louse(1.0)
def needle(length=520):
    im = Image.new("RGBA", (length + 20, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(10, 40), (length - 40, 26), (length, 40), (length - 40, 54)], fill=(236, 226, 200, 255), outline=(120, 100, 70, 255))
    d.ellipse((length - 80, 33, length - 52, 47), fill=(0, 0, 0, 0), outline=(120, 100, 70, 255), width=4)
    d.line((length - 66, 40, length + 10, 70), fill=(150, 100, 50, 255), width=4); return im
NEEDLE = needle()
def bone_tool():
    im = Image.new("RGBA", (420, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 30, 400, 90), 30, fill=(230, 216, 186, 255), outline=(130, 110, 80, 255), width=5)
    d.ellipse((330, 20, 410, 100), fill=(230, 216, 186, 255), outline=(130, 110, 80, 255), width=5); return im
BONE = bone_tool()
def fibers(t):
    im = Image.new("RGBA", (700, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, col in enumerate(((60, 60, 60), (40, 140, 160), (200, 120, 160), (90, 70, 40))):
        pts = [(x, 60 + k * 60 + 14 * math.sin(x / 22 + k + t * 2)) for x in range(20, 680, 6)]; d.line(pts, fill=col + (255,), width=6)
    return im
def thermometer(c, x, y, frac):
    d = ImageDraw.Draw(c); d.rounded_rectangle((x - 30, y - 300, x + 30, y + 40), 30, fill=(240, 240, 240), outline=(30, 30, 30), width=6)
    d.ellipse((x - 55, y, x + 55, y + 110), fill=(220, 50, 40), outline=(30, 30, 30), width=6)
    d.rounded_rectangle((x - 14, y - 290 * frac, x + 14, y + 40), 14, fill=(220, 50, 40))
def drops(c, t, t0, x, y):
    d = ImageDraw.Draw(c, "RGBA")
    for k in range(9):
        ph = ((t - t0) * 0.8 + k * 0.11) % 1.0; xx = x + (k - 4) * 26; yy = y + ph * 220
        d.polygon([(xx, yy - 26), (xx - 14, yy), (xx + 14, yy)], fill=(120, 190, 255, int(255 * (1 - ph)))); d.ellipse((xx - 14, yy - 12, xx + 14, yy + 16), fill=(120, 190, 255, int(255 * (1 - ph))))
ICE = [  # approximate ice sheets at the Last Glacial Maximum (drawn by us)
    [(-138, 59), (-135, 58), (-128, 52), (-124, 48.5), (-121, 47), (-114, 48), (-105, 48), (-97, 45), (-93, 43), (-89, 40), (-85, 39), (-82, 40), (-77, 41),
     (-73, 40.8), (-70, 41.5), (-66, 43.5), (-60, 45.5), (-56, 47), (-55, 52), (-60, 58), (-64, 61), (-68, 66), (-75, 70), (-85, 72), (-100, 74), (-120, 74),
     (-135, 70), (-141, 69), (-141, 62)],
    [(-55, 60), (-43, 59.5), (-35, 65), (-22, 70), (-18, 77), (-25, 82), (-45, 83), (-62, 81), (-70, 77), (-58, 72), (-52, 66)],
    [(-10, 54), (-6, 51.5), (-3, 51), (2, 52.5), (8, 53), (13, 52.5), (20, 52.5), (27, 54), (32, 56), (35, 60), (40, 63), (50, 67), (60, 70), (65, 75),
     (55, 80), (30, 81), (15, 80), (5, 75), (0, 68), (-5, 62), (-9, 58)],
    [(6, 45.5), (9, 46.5), (13, 47.2), (15, 46.8), (12, 45.9), (8, 45.3)]]
BERINGIA = [(-190, 66), (-185, 70), (-175, 72), (-165, 72), (-157, 71.5), (-160, 66), (-165, 61), (-168, 58), (-172, 59), (-178, 61), (-182, 62.5), (-188, 64)]
def ice_layer(c, cam, k):
    if k <= 0: return
    L.layer(c, lambda d: [d.polygon(L.poly_px(cam, p), fill=(246, 251, 255, int(225 * k)), outline=(150, 190, 225, int(255 * k)), width=3) for p in ICE], blur=2)
def beringia(c, cam, k):
    if k <= 0: return
    L.layer(c, lambda d: d.polygon(L.poly_px(cam, BERINGIA), fill=(206, 184, 120, int(200 * k)), outline=(150, 110, 50, int(255 * k)), width=4), blur=3)
def wind(c, t, x0, y0):
    d = ImageDraw.Draw(c, "RGBA")
    for k in range(4):
        ph = ((t * 0.9) + k * 0.25) % 1.0; x = x0 + ph * 600; y = y0 + k * 60
        d.line((x, y, x + 120, y), fill=(220, 235, 255, int(255 * (1 - ph))), width=6)

# ------------------------------------------------------------------ the montage
def overlay(c, t, cam):
    lon, lat, p = cam
    # real (NASA Blue Marble) <-> our drawn map, now and then
    L.real_map(c, cam, max(L.fade(t, -1.0, A["dressed"], 0.6), L.fade(t, A["froze"] - 0.3, A["beringia"] - 0.4, 0.7), L.fade(t, A["fiber"] - 0.6, A["modesty2"], 0.6)), BM, BMB)
    # ---- HOOK
    if t < A["nobody"]: L.headline(c, "LOOK AT WHAT YOU'RE WEARING", t, 0.0)
    if A["nobody"] <= t < A["dressed"]:
        L.headline(c, "FOR MOST OF HISTORY: NOTHING", t, A["nobody"]); L.character(c, "ice_age_naked", t, A["naked1"], 1600, h=460)
    if A["dressed"] <= t < A["louse1"]: L.headline(c, "WHEN? AND WHY?", t, A["dressed"], size=110)
    if A["louse1"] <= t < A["habibi"]:
        L.headline(c, "THE BEST CLUE: A LOUSE", t, A["louse1"]); L.cutout(c, LB, t, A["louse1"] + 0.3, W / 2, 600, 450, rot=-4)
        if t >= A["modesty1"]: L.sub(c, "spoiler: it wasn't modesty", t, A["modesty1"], y=280)
    if A["habibi"] <= t < CH[0][1]: L.character(c, "host_cool", t, A["habibi"], 1560, h=520); L.headline(c, "BACK TO WHEN WE WERE NAKED", t, A["habibi"] + 0.5)
    # ---- CH1 the naked ape
    if A["strange"] <= t < A["genetic"]:
        L.headline(c, "A VERY NAKED APE", t, A["strange"] + 0.4); L.character(c, "ice_age_naked", t, A["strange"] + 0.4, 1600, h=460)
        if t >= A["mammals"]: L.sub(c, "most mammals: fur · us: thin, tiny hair", t, A["mammals"])
        if t >= A["fossilize"]: L.sub(c, "skin doesn't fossilize", t, A["fossilize"], y=360, col=(255, 255, 255))
    if A["genetic"] <= t < A["heat1"]:
        L.big(c, "1.2 MILLION YEARS", t, A["genetic"] + 1.2, size=120, sub="dark-skin gene variant (MC1R): at least that old · Rogers 2004, Jablonski 2010")
    if A["heat1"] <= t < A["upgrade"]:
        L.headline(c, "WHY LOSE FUR? HEAT", t, A["heat1"] - 0.3)
        if t >= A["sweat1"]: L.big(c, "2-5 MILLION", t, A["sweat1"], y=300, size=110, sub="sweat glands · up to 12 liters a day · Jablonski", sub_y=390); drops(c, t, A["sweat1"], 1600, 640)
        L.character(c, "ice_age_naked", t, A["heat1"], 1600, h=420)
    if A["upgrade"] <= t < A["iceage1"]:
        L.headline(c, "AN UPGRADE... UNTIL IT WASN'T", t, A["upgrade"] - 0.6)
        if t >= A["comfortable"]:
            panel_d = L.panel(c, (560, 260, 1360, 820)); thermometer(c, 760, 650, 0.62 * ease((t - A["comfortable"]) / 1.0))
            panel_d.text((1100, 420), "28°C", font=font(IMPACT, 130), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=(10, 10, 10))
            panel_d.text((1100, 530), "(about 82°F)", font=font(SANS, 44), fill=(255, 255, 255), anchor="mm")
            panel_d.text((1100, 640), "comfortable when naked", font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
            panel_d.text((1100, 690), "Ganeshan & Chawla 2017", font=font(SANS, 26), fill=(200, 190, 175), anchor="mm")
    if A["iceage1"] <= t < CH[1][1]:
        ice_layer(c, cam, ease((t - A["iceage1"]) / 0.8)); L.headline(c, "...AND THEN, AN ICE AGE", t, A["iceage1"])
    # ---- CH2 the louse witness
    if A["kinds"] <= t < A["split"]:
        L.headline(c, "TWO KINDS OF LICE", t, A["kinds"])
        L.cutout(c, LH, t, A["kinds"] + 0.4, 560, 560, 250, rot=-8); put(c, pill("HEAD LICE: live in hair", 36), 560, 760, popk(t, A["kinds"] + 0.6))
        if t >= A["seams"] - 1.2:
            L.cutout(c, LB, t, A["seams"] - 1.2, 1340, 540, 400, rot=5)
            put(c, pill("BODY LICE: live in CLOTHES (the seams) · CDC", 36, (255, 225, 120)), 1340, 790, popk(t, A["seams"] - 1.0))
        if t >= A["exist"]: L.big(c, "NO CLOTHES = NO BODY LICE", t, A["exist"], y=300, size=90)
    if A["split"] <= t < A["translation"]:
        L.timeline(c, t, A["split"], [(72000, "~72k (2003)", A["dna1"], (200, 120, 60), 42000), (83000, "83k", A["florida"] + 1.0, (60, 140, 200), 0),
                                      (170000, "maybe 170k", A["florida"] + 2.4, (60, 140, 200), 0)],
                   title="when body lice split from head lice = clothes worn regularly", y=560, span=200000)
        if t >= A["florida"]: L.sub(c, "Kittler 2003 · Toups et al. 2011 (University of Florida)", t, A["florida"], y=820, col=(255, 255, 255))
        if t >= A["range"]: L.headline(c, "LONG BEFORE THE COLD NORTH", t, A["range"] + 1.0, y=170, size=80)
    if A["translation"] <= t < CH[2][1]:
        L.headline(c, "TRANSLATION?", t, A["translation"]); L.sub(c, "clothes probably started with modern humans in Africa, in the ice ages", t, A["translation"] + 1.0)
        if t >= A["tools1"] and ph("cl_lissoir.jpg"): L.photo(c, ph("cl_lissoir.jpg"), t, A["tools1"], x=W / 2, y=600, w=700, rot=-2, credit="Ice Age bone tool · Musée de l'Homme · public domain")
    # ---- CH3 the first tailors
    if A["rabat"] <= t < A["neander1"]:
        L.place(c, cam, "Contrebandiers Cave, Morocco", P["Contrebandiers"], popk(t, A["rabat"]), (150, 110, 60), dy=70)
        L.big(c, "120,000-90,000 YEARS", t, A["rabat"] + 1.6, size=100, sub="60+ bone tools · Hallett et al. 2021")
        if ph("cl_lissoir.jpg"): L.photo(c, ph("cl_lissoir.jpg"), t, A["scraping"], A["carnivores"] + 0.2, x=1440, y=620, w=620, rot=3, credit="a bone hide-smoother (a later one, France) · public domain")
        if t >= A["carnivores"]: L.sub(c, "cut marks: skinned for FUR, not meat", t, A["butchering"] - 0.6, y=330)
        if t >= A["jacket"]: L.sub(c, "proxy evidence, not a jacket", t, A["jacket"], y=410, col=(255, 255, 255))
    if A["neander1"] <= t < A["georgia"]:
        L.place(c, cam, "Pech-de-l'Azé, France", P["PechAze"], popk(t, A["neander1"] + 0.3), (150, 110, 60), dy=70)
        L.big(c, "~50,000 YEARS", t, A["neander1"] + 1.0, size=110, sub="Neanderthal hide smoothers (deer ribs) · Soressi 2013")
        L.character(c, "ice_age_cape", t, A["neander1"] + 0.4, 1600, h=440)
    if A["georgia"] <= t < (A["sub_mid"] - 0.2 if A["sub_mid"] > 0 else CH[3][1]):
        L.place(c, cam, "Dzudzuana Cave, Georgia", P["Dzudzuana"], popk(t, A["georgia"]), (150, 110, 60), dy=70)
        L.big(c, "~30,000 YEARS", t, A["georgia"] + 0.8, size=110, sub="flax fibers: twisted + dyed · Kvavadze 2009")
        if t >= A["georgia"] + 2.0:
            L.panel(c, (1250, 470, 1890, 800)); put(c, fibers(t), 1570, 635, popk(t, A["georgia"] + 2.0))
        if t >= A["string1"]: L.headline(c, "STRING CHANGES EVERYTHING", t, A["string1"], y=420, size=76)
    # ---- CH4 the needle
    if A["invention"] <= t < A["coldest1"]:
        L.headline(c, "THE EYED NEEDLE", t, A["invention"] + 0.6, size=100); (L.photo(c, ph("cl_eyed_needle.jpg"), t, A["invention"] + 1.0, A["draped1"], x=W / 2, y=590, w=860, rot=-2, credit="Ice Age eyed needle and bone tools · Musée d'Archéologie nationale · CC0") if ph("cl_eyed_needle.jpg") else put(c, NEEDLE, W / 2, 380, popk(t, A["invention"] + 1.0)))
        if t >= A["draped1"]: L.character(c, "ice_age_cape", t, A["draped1"], 1600, h=480); L.sub(c, "before needles: DRAPED · tied, not sewn", t, A["draped1"], y=520)
    if A["coldest1"] <= t < A["denisova"] - 0.3:
        L.big(c, "UP TO 80%", t, A["coldest1"] + 1.0, size=140, sub="of the body covered, no tailoring (one estimate, Wales 2012)")
        L.character(c, "ice_age_cape", t, A["coldest1"], 1600, h=440)
        if t >= A["linked"]: L.sub(c, "no eyed needle linked to Neanderthals (so far)", t, A["linked"], y=360, col=(255, 255, 255))
    if A["denisova"] - 0.3 <= t < A["fitted1"]:
        for k2, (nm, yrs, tt) in enumerate((("Denisova", 40, A["denisova"]), ("Mezmaiskaya", 38, A["caucasus"]), ("Yana (Arctic)", 33, A["caucasus"] + 1.6), ("Europe", 26, A["caucasus"] + 3.0))):
            if t >= tt:
                key = {"Denisova": "Denisova", "Mezmaiskaya": "Mezmaiskaya", "Yana (Arctic)": "Yana", "Europe": "Europe"}[nm]
                L.place(c, cam, f"{nm} · ~{yrs}k", P[key], popk(t, tt), (60, 60, 70), dy=60 if k2 in (0, 2, 3) else -46)
        L.big(c, "~40,000 YEARS", t, A["denisova"] + 0.6, size=120, sub="oldest eyed needles · Gilligan et al. 2024", x=720)
    if A["fitted1"] <= t < A["fancy"]:
        L.headline(c, "DRAPED vs FITTED", t, A["fitted1"] - 0.2, size=100)
        L.character(c, "ice_age_cape", t, A["fitted1"], 640, y=850, h=430); L.character(c, "ice_age_parka", t, A["fitted1"] + 0.4, 1280, y=850, h=430)
        L.sub(c, "sleeves · trousers · layers · hoods", t, A["fitted1"] + 0.8, y=270)
        if t >= A["wind"] - 1.5: wind(c, t, 300, 560); put(c, pill("wind gets in", 34), 640, 370, popk(t, A["wind"] - 1.5)); put(c, pill("warm air stays in", 34, (255, 225, 120)), 1280, 370, popk(t, A["wind"] - 1.2))
    if A["fancy"] <= t < CH[4][1]:
        L.headline(c, "WARM... AND FANCY", t, A["fancy"] - 0.4)
        if t >= A["sunghir"]: L.place(c, cam, "Sunghir, Russia · ~34,000 years", P["Sunghir"], popk(t, A["sunghir"]), (150, 110, 60), dy=70)
        if t >= A["sunghir"] + 1.2:
            L.character(c, "ice_age_parka", t, A["sunghir"] + 1.2, 1580, h=500)
            d = ImageDraw.Draw(c)
            for r in range(int(min(44, (t - A["sunghir"] - 1.2) * 30))): x = 1478 + (r % 11) * 20; y = 905 + (r // 11) * 26; d.ellipse((x, y, x + 11, y + 11), fill=(250, 245, 230), outline=(120, 100, 70))
            L.sub(c, "thousands of ivory beads, in rows · probably sewn on", t, A["sunghir"] + 1.4, y=270)
        if t >= A["fashion1"]: L.headline(c, "ONE OF THE FIRST FASHION STATEMENTS", t, A["fashion1"], y=360, size=66, col=YEL)
    # ---- CH5 the world freezes
    icek = ease((t - A["froze"]) / 1.5) if A["froze"] <= t < CH[5][1] else 0
    ice_layer(c, cam, icek)
    if A["froze"] <= t < A["beringia"]:
        L.headline(c, "THE WORLD FROZE", t, A["froze"], size=110)
        if t >= A["maximum"]: L.sub(c, "Last Glacial Maximum · ~26,500-19,000 years ago", t, A["maximum"])
        if t >= A["planet"]: L.big(c, "-6°C", t, A["planet"] + 0.6, y=420, size=170, col=(170, 220, 255), sub="whole planet vs today · Arctic: about -14°C · Tierney 2020", sub_y=540)
        if t >= A["locked"]: L.big(c, "SEA LEVEL -130 M", t, A["locked"] + 1.2, y=700, size=90, col=(170, 220, 255))
    if A["beringia"] - 0.3 <= t < A["oregon1"] - 0.3:
        beringia(c, cam, ease((t - A["beringia"] + 0.3) / 1.0))
        L.place(c, cam, "Beringia: dry land", P["Beringia"], popk(t, A["beringia"]), (150, 110, 60), dy=70)
        if ph("cl_beringia_nps.png"): L.photo(c, ph("cl_beringia_nps.png"), t, A["beringia"] + 0.8, A["alaska2"] - 0.4, x=1500, y=560, w=620, rot=2, credit="Beringia map · US National Park Service")
        if t >= A["survive1"]: L.headline(c, "WHO SURVIVED UP HERE? THE SEWN", t, A["survive1"], size=76)
        if t >= A["alaska2"]: L.place(c, cam, "Alaska: eyed needles ~14,000 years", P["Alaska"], popk(t, A["alaska2"]), (60, 60, 70), dy=-46)
    if A["oregon1"] - 0.3 <= t < A["sandals"]:
        L.place(c, cam, "Cougar Mountain Cave, Oregon", P["CougarMtn"], popk(t, A["oregon1"]), (150, 110, 60), dy=-60)
        L.big(c, "~12,900-11,700 YEARS", t, A["oregon1"] + 1.4, size=100, sub="sewn elk hide · Science Advances, 2026")
        if t >= A["moccasin"]: L.sub(c, "clothing? a moccasin? a bag?", t, A["moccasin"], y=330, col=(255, 255, 255))
    if A["sandals"] <= t < CH[5][1]:
        L.place(c, cam, "Fort Rock Cave", P["FortRock"], popk(t, A["sandals"] - 0.4), (150, 110, 60), dy=70)
        L.big(c, "10,000+ YEARS", t, A["sandals"] + 0.4, size=120, sub="sagebrush-bark sandals · Fort Rock, Oregon")
    # ---- CH6 survival to style
    if A["alps"] <= t < A["linen"] - 1.4:
        L.place(c, cam, "Ötzi the Iceman · Alps", P["Otzi"], popk(t, A["alps"] + 0.2), (60, 60, 70), dy=70)
        L.big(c, "5,300 YEARS", t, A["alps"] + 0.6, size=120)
        if t >= A["iceman"]: L.sub(c, "coat: 4+ animals (sheep, goat) · hat: brown bear · O'Sullivan 2016", t, A["iceman"] + 1.0, y=300)
        L.character(c, "ice_age_parka", t, A["iceman"], 1600, h=460)
        if ph("cl_otzi_shoe.jpg"): L.photo(c, ph("cl_otzi_shoe.jpg"), t, A["iceman"] + 1.6, A["linen"] - 1.4, x=430, y=640, w=440, rot=-3, credit="Ötzi's shoe (replica) · Bata Shoe Museum · CC0")
    if A["linen"] - 0.4 <= t < A["archaeologist"]:
        L.place(c, cam, "Tarkhan, Egypt", P["Tarkhan"], popk(t, A["linen"] - 0.3), (60, 60, 70), dy=70)
        L.big(c, "THE TARKHAN DRESS", t, A["linen"] - 0.2, size=100, sub="linen · 3482-3102 BC (radiocarbon) · UCL")
        if t >= A["again"]: L.character(c, "egyptian_galabeya", t, A["again"] - 0.2, 1600, h=460); put(c, outlined("HI AGAIN, EGYPT", 70, fill=YEL), 1250, 640, popk(t, A["again"] - 0.2))
    if A["archaeologist"] <= t < A["why_end"] - 0.4:
        if t < A["fiber"] - 0.6:
            L.headline(c, "FROM NEED TO SOCIAL RULE", t, A["archaeologist"] + 0.8, size=80); L.sub(c, "Ian Gilligan, University of Sydney (2024)", t, A["archaeologist"] + 1.0)
        else:
            L.big(c, "132 MILLION TONNES", t, A["fiber"] - 0.6, size=110, sub="of fiber a year (2024) · ~69% synthetic · Textile Exchange")
            if ph("cl_textile_factory.jpg"): L.photo(c, ph("cl_textile_factory.jpg"), t, A["fiber"], x=W / 2, y=600, w=720, rot=2, credit="Pexels · Rajesh Kumar Verma")
    # ---- END
    if A["why_end"] <= t < A["fur_end"]:
        L.headline(c, "SO WHY DID WE START?", t, A["why_end"], size=100)
        if t >= A["modesty2"]: L.sub(c, "not modesty · not fashion · not at first", t, A["modesty2"])
    if A["fur_end"] <= t < A["needle_end"]:
        L.character(c, "ice_age_naked", t, A["fur_end"], 520, y=850, h=400); L.headline(c, "LOST FUR FOR THE HEAT", t, A["fur_end"], size=80)
        if t >= A["borrowed"]: L.character(c, "ice_age_cape", t, A["borrowed"], 960, y=850, h=400); L.sub(c, "...borrowed it back for the cold", t, A["borrowed"])
    if A["needle_end"] <= t < A["subscribe"]:
        L.character(c, "ice_age_naked", t, 0, 520, y=850, h=400); L.character(c, "ice_age_cape", t, 0, 960, y=850, h=400); L.character(c, "ice_age_parka", t, A["needle_end"], 1400, y=850, h=400)
        put(c, NEEDLE, W / 2, 230, popk(t, A["needle_end"]))
        if t >= A["lice_end"]: L.cutout(c, LB, t, A["lice_end"], 1560, 520, 170, rot=12); L.headline(c, "THE LICE CAME ALONG FOR THE RIDE", t, A["lice_end"], y=360, size=66, col=YEL)
    if A["subscribe"] <= t < A["endscreen"]:
        L.character(c, "host_cool", t, A["subscribe"], 1560, h=520)
        put(c, pill("SUBSCRIBE · next: what ancient humans did for fun", 50, (255, 255, 255), (200, 30, 30, 240)), W / 2 - 160, 300, popk(t, A["subscribe"] + 0.3))
    L.subscribe_nudge(c, t, A["sub_mid"], A["sub_more"] + 1.4, x=1200, y=470, t_click=A["sub_word"])
    L.end_screen(c, t, A["endscreen"], "still curious?")
    L.chapter_card(c, t, CH)

SFX = [("pop", A[n] + 0.3, -20) for n in ("louse1", "genetic", "sweat1", "comfortable", "seams", "dna1", "florida", "rabat", "neander1", "georgia", "invention",
                                          "denisova", "fitted1", "sunghir", "planet", "locked", "beringia", "oregon1", "sandals", "alps", "linen", "fiber")]
SFX += [("paper_slide", t0, -20) for _, t0 in CH]
SFX += [("pop", A[n] + d, -19) for n, d in (("tools1", 0.0), ("scraping", 0.0), ("beringia", 0.8), ("iceman", 1.6), ("fiber", 0.0))]
SFX += [("pop", A["sub_word"] + 0.25, -18), ("paper_slide", A["endscreen"], -18), ("pop", A["endscreen"] + 2.3, -20)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END)
    else: K.main(sys.argv, overlay, SFX)
