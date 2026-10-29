"""Ask Habibi Ep 7 "What Did Ancient Humans Do For Fun?" — 16:9 long form, fast montage on shortkit + longkit.
  python render_ep07.py build | qa t.. | anchors | allseg [n] | audio | final n"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep07_ancient_fun")
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, pin, YEL, SANS, IMPACT
import longkit as L
import ep07_draw as D

ROOT = "D:/why habibi/7th video/"
K.setup(root=ROOT, vo="vo/ep07_vo_chatterbox.wav", lat_mid=35, pyr=[10, 20, 40, 80], size=(1920, 1080), cap_size=64, tail=21.5,
        fills=[], out="Ask_Habibi_Ep07_What_Ancient_Humans_Did_For_Fun.mp4", cap_fix=[("Koroibos", "Koroibos")])
W, H = K.W, K.H
A = L.Anchors(); a = A.a
# ------------------------------------------------------------------ anchors
a("joke", "joke"); a("fart", "fart"); a("boredom", "boredom"); a("phones", "phones"); a("books", "books"); a("writing", "writing")
a("games", "games"); a("rules", "rules"); a("win", "win"); a("habibi", "habibi"); a("fun", "fun")
a("art", "art"); a("muna", "muna"); a("blew", "blew"); a("narrowed", "narrowed"); a("rockart", "rock"); a("sulawesi", "sulawesi"); a("pig", "pig")
a("story", "story"); a("rouffignac", "rouffignac"); a("kids", "kids"); a("lift", "lift"); a("toddler", "toddler")
a("music", "music"); a("hohle", "hohle"); a("vulture", "vulture's"); a("geissen", "geissenklösterle"); a("survive", "survive"); a("slovenia", "slovenia")
a("hyena", "hyena"); a("disputed", "disputed")
a("games2", "games", 1, "disputed"); a("dice", "dice"); a("colorado", "colorado"); a("fortune", "fortune"); a("ur", "ur"); a("royal", "royal")
a("boards", "boards"); a("finkel", "finkel"); a("race", "race"); a("land", "land", 1, "race"); a("off", "off", 1, "land"); a("luck", "luck")
a("india", "india"); a("kochi", "kochi"); a("onegame", "game", 1, "kochi"); a("again", "again"); a("senet", "senet"); a("tut", "tutankhamun")
a("ai", "ai"); a("netherlands", "netherlands"); a("ai2", "ai", 2)
a("sub_mid", "quick"); a("sub_word", "subscribe", 1, "sub_mid"); a("sub_more", "more", 1, "sub_mid")
a("sports", "sports"); a("beni", "beni"); a("red", "red", 1, "beni"); a("manual", "manual"); a("mexico", "mexico", 1, "manual"); a("manati", "manatí")
a("greece", "greece"); a("event", "event"); a("sprint", "sprint"); a("cook", "cook"); a("naked", "naked")
a("backjoke", "back", 1, "naked"); a("sumer", "sumer"); a("wife", "wife"); a("lap", "lap"); a("philo", "philogelos"); a("pompeii", "pompeii")
a("amazed", "amazed"); a("festival", "festival"); a("mut", "mut"); a("drummers", "drummers"); a("sober", "sober")
a("kids2", "kids", 2); a("siberia", "siberia"); a("rattles", "rattles"); a("spain", "spain"); a("owls", "owls"); a("children", "children", 1, "owls")
a("rome", "rome"); a("doll", "doll"); a("joints", "joints")
a("so_end", "so", 1, "joints"); a("same", "same"); a("walls", "walls"); a("gambled", "gambled"); a("reason", "reason", 1, "gambled"); a("y2014", "2014")
a("button", "button"); a("men", "men"); a("women", "women"); a("bored", "bored", 1, "women"); a("lasted", "lasted"); a("subscribe", "subscribe", 1, "lasted")
A["endscreen"] = K.WORDS[-1]["e"] + 0.6
END = K.DUR
CH = [("THE FIRST ART", A["art"] - 0.5), ("THE FIRST MUSIC", A["music"] - 0.4), ("GAMES & GAMBLING", A["games2"] - 0.4), ("SPORTS", A["sports"] - 0.4),
      ("JOKES & PARTIES", A["backjoke"] - 0.4), ("THE KIDS", A["kids2"] - 0.6), ("SO... WHY?", A["so_end"] - 0.3)]
K.CFG["music"] = [("Marty Gots a Plan.mp3", 0.0), ("Easy Lemon.mp3", A["games2"] - 1.0), ("Daily Beetle.mp3", A["sports"] - 1.0),
                  ("Vibing Over Venus.mp3", A["backjoke"] - 1.0), ("Stay the Course.mp3", A["so_end"] - 0.8)]

# ------------------------------------------------------------------ places + camera
P = dict(Muna=(122.7, -4.8), Sulawesi=(119.6, -4.9), Rouffignac=(0.99, 44.99), HohleFels=(9.76, 48.38), Geissen=(9.95, 48.55), DivjeBabe=(13.91, 46.10),
         Folsom=(-105.0, 40.5), Ur=(46.10, 30.96), Kochi=(76.26, 9.96), Saqqara=(31.22, 29.87), Heerlen=(5.98, 50.89), BeniHasan=(30.88, 27.93),
         PasoAmada=(-92.45, 14.87), ElManati=(-94.66, 17.77), Olympia=(21.63, 37.64), Sumer=(45.5, 31.5), Pompeii=(14.49, 40.75), Rome=(12.47, 41.90),
         Mut=(32.66, 25.71), Siberia=(82.9, 55.0), Iberia=(-6.0, 37.4))
WORLD = (20.0, 25.0, 8.5); INDO = (121.0, -3.0, 40); FR = (1.5, 46.0, 40); DE = (11.0, 47.5, 40); US = (-104.0, 40.0, 20); IRAQ = (45.0, 31.5, 30)
ARAB = (60.0, 20.0, 12); EG = (31.0, 28.0, 28); NL = (6.0, 50.5, 40); MEX = (-94.0, 16.0, 30); GR = (22.0, 38.0, 40); IT = (13.5, 41.3, 40)
EG2 = (32.5, 26.5, 28); SIB = (83.0, 55.0, 20); IB = (-6.0, 38.0, 30)
def cam_keys():
    k = [(0.0, *WORLD), (A["art"], *WORLD), (A["muna"] - 0.3, *INDO), (A["rouffignac"] - 1.6, *WORLD), (A["rouffignac"] - 0.3, *FR), (A["hohle"] - 0.3, *DE),
         (A["slovenia"] - 0.3, 13.0, 46.5, 40), (A["games2"], *WORLD), (A["dice"], *US), (A["ur"] - 1.6, *WORLD), (A["ur"] - 0.3, *IRAQ),
         (A["india"] - 0.3, *ARAB), (A["again"] - 0.3, *EG), (A["ai"] - 0.3, *NL), (A["sub_mid"], *NL), (A["sports"], *WORLD), (A["beni"] - 0.3, *EG),
         (A["mexico"] - 1.6, *WORLD), (A["mexico"] - 0.3, *MEX), (A["greece"] - 1.6, *WORLD), (A["greece"] - 0.3, *GR), (A["backjoke"], *GR),
         (A["sumer"] - 0.3, *IRAQ), (A["philo"] - 0.3, *IT), (A["festival"] - 0.3, *EG2), (A["kids2"], *WORLD), (A["siberia"] - 0.3, *SIB),
         (A["spain"] - 1.6, *WORLD), (A["spain"] - 0.3, *IB), (A["rome"] - 0.3, *IT), (A["so_end"], *WORLD), (END + 2, *WORLD)]
    return L.hold_keys(k)
K.set_camera(cam_keys())
MED = "D:/why habibi/_media/"; PH = MED + "photos_ep07/"; BM = MED + "photos_2026-10-18/world_bluemarble_5400.jpg"; BMB = (-180.0, 180.0, -90.0, 90.0)
def ph(name): return PH + name if os.path.exists(PH + name) and os.path.getsize(PH + name) > 50000 else None
PHOTOS = [   # (file, t0, t1, x, y, w, rot, credit) - real photos as proof (approved downloads 18 Oct 2026); "like these" where it's a similar example
    ("f7_flutings.jpg", A["rouffignac"] + 0.6, A["music"] - 0.6, 440, 640, 560, 2, "finger flutings like these (La Roche-Cotard, France) · Marquet et al. 2023, CC BY 4.0"),
    ("f7_bone_flute.jpg", A["vulture"], A["slovenia"] - 0.1, 1300, 690, 640, -2, "a Stone Age bone flute like these (Germany, younger) · Burkhard Mücke, CC BY 4.0"),
    ("f7_divje_babe.jpg", A["slovenia"] + 0.6, CH[2][1], 520, 600, 300, -3, "the Divje Babe bone · Szilas, CC0"),
    ("f7_ur_board.jpg", A["royal"] - 0.2, A["finkel"] - 0.1, W / 2, 660, 780, -2, "the Royal Game of Ur, British Museum · BabelStone, CC0"),
    ("f7_senet_box.jpg", A["senet"] + 0.3, A["ai"] - 0.4, W / 2, 700, 680, 2, "senet + 'twenty squares' game box · The Met, CC0"),
    ("f7_beni_hasan.jpg", A["beni"] + 1.6, A["mexico"] - 1.7, 470, 620, 420, -3, "Beni Hasan wrestlers (facsimile) · public domain"),
    ("f7_ballcourt.jpg", A["mexico"] + 1.2, A["greece"] - 1.7, 1520, 640, 600, 3, "a much later ballcourt: Chichen Itza · Pexels / Henry VL"),
    ("f7_olympia.jpg", A["greece"] + 1.0, A["naked"] - 0.6, 1440, 640, 620, 3, "Olympia's stadium entrance · Erik Drost, CC BY 2.0"),
    ("f7_pompeii_street.jpg", A["pompeii"], A["pompeii"] + 1.6, W / 2, 620, 820, -2, "Pompeii · Pexels / Bogdan Giurca"),
    ("f7_pompeii_graffiti.jpg", A["pompeii"] + 1.6, A["festival"] - 0.4, W / 2, 640, 600, 2, "real graffiti, House of the Vettii, Pompeii · Buzz Ferebee, public domain"),
]

# ------------------------------------------------------------------ cached drawings
HAND = D.hand_stencil(); PIG = D.pig_scene(); FLUTE = D.flute(); IVORY = D.flute(560, 3, ivory=True); DICE = D.dice_sticks(); SENET = D.senet_board()
TABLET = D.clay_tablet(); WALL = D.plaster_wall("I'm amazed, wall, that you haven't collapsed\nunder the weight of so much boring graffiti")
OWL = D.owl_plaque(); DOLL = D.doll(); COURT = D.ballcourt(); STAMP = D.stamp("DISPUTED"); WP, WK = D.ur_piece(True), D.ur_piece(False)
import marker as MK
PC = {}
def pcard(name, w, rot=0):
    """a real photo as a white-bordered card (cached); None if the file is missing"""
    if not ph(name): return None
    if (name, w, rot) not in PC: PC[(name, w, rot)] = L._photo_card(ph(name), w, rot, None)
    return PC[(name, w, rot)]
def xcross(im):
    im = im.copy(); MK.strokes(im, [__import__("numpy").array([(40, 40), (im.width - 40, im.height - 40)]), __import__("numpy").array([(im.width - 40, 40), (40, im.height - 40)])], MK.RED, 16, seed=3); return im
UR = {}
URP = [(x, y - 250) for x, y in ((835, 660), (640, 660), (420, 660), (205, 660), (240, 505), (445, 505), (655, 505), (835, 505), (1035, 505), (1235, 505), (1430, 505), (1610, 505), (1650, 660), (1440, 660))]
UR_ROSES = [(265, 375), (205, 660), (835, 505), (1380, 355), (1440, 660)]
def ur_real(t, w=1180):
    """the real Royal Game of Ur (British Museum photo) with the rules drawn on it in marker as the voice explains them"""
    import numpy as np
    if "base" not in UR: UR["base"] = Image.open(PH + "f7_ur_board.jpg").convert("RGBA").crop((0, 250, 1920, 900))
    im = UR["base"].copy()
    if t >= A["race"]: MK.strokes(im, [np.array(URP, float)], MK.YEL, 16, min(1, (t - A["race"]) / 2.5), seed=2)
    if t >= A["land"]:
        x, y = URP[8]; MK.strokes(im, [np.array([(x - 60, y - 60), (x + 60, y + 60)]), np.array([(x + 60, y - 60), (x - 60, y + 60)])], MK.RED, 18, min(1, (t - A["land"]) / 0.5), seed=5)
    if t >= A["luck"]:
        for k, (x, y) in enumerate(UR_ROSES): MK.strokes(im, MK.circle_path(x, y - 250, 105, 95, seed=k), MK.RED, 14, min(1, (t - A["luck"] - k * 0.25) / 0.5), seed=k)
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS); card = Image.new("RGBA", (im.width + 24, im.height + 24), (250, 247, 240, 255)); card.alpha_composite(im, (12, 12)); return card
UR_PATH = [(2, 3), (2, 2), (2, 1), (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 7), (2, 6)]   # one player's route

def ur_show(c, t, t0, x, y, lit=(), moves=False, scale=1.0):
    if t < t0: return
    b = D.ur_board(lit=lit).copy(); k = popk(t, t0)
    if moves:                                                              # a white piece races the route; at 'land' it knocks the black one back
        u = max(0.0, (t - t0 - 0.6) / 4.0); i = min(len(UR_PATH) - 1, int(u * len(UR_PATH))); r, cc = UR_PATH[i]
        bx, by = D.ur_cell_xy(1, 5)
        if not (t >= A["land"] and i >= 9): b.alpha_composite(WK, (int(bx - WK.width / 2), int(by - WK.height / 2)))
        px, py = D.ur_cell_xy(r, cc); b.alpha_composite(WP, (int(px - WP.width / 2), int(py - WP.height / 2)))
    if scale != 1.0: b = b.resize((int(b.width * scale), int(b.height * scale)), Image.LANCZOS)
    put(c, b, x, y, k)

def bars(c, t, t0, rows, y0=420):
    """simple horizontal share bars: [(label, n, of, colour)]"""
    d = L.panel(c, (360, y0 - 80, 1560, y0 + 120 * len(rows) - 10))
    for k, (lab, n, of, col) in enumerate(rows):
        y = y0 + k * 120; u = ease((t - t0 - k * 0.5) / 0.8); d.text((420, y - 30), lab, font=font(SANS, 40), fill=(255, 255, 255))
        d.rounded_rectangle((420, y + 10, 420 + 1000, y + 60), 14, fill=(70, 60, 52)); d.rounded_rectangle((420, y + 10, 420 + 1000 * n / of * u, y + 60), 14, fill=col)
        if u > 0.2: d.text((1440, y + 35), f"{n} of {of}", font=font(IMPACT, 54), fill=YEL, anchor="lm", stroke_width=4, stroke_fill=(10, 10, 10))

# ------------------------------------------------------------------ the montage
def overlay(c, t, cam):
    lon, lat, p = cam
    L.real_map(c, cam, max(L.fade(t, -1.0, A["games"], 0.6), L.fade(t, A["so_end"] - 0.3, A["y2014"] - 0.2, 0.6)), BM, BMB)
    # ---- HOOK
    if t < A["fart"]: L.big(c, "THE OLDEST JOKE EVER WRITTEN", t, 0.0, y=180, size=96, sub="~4,000 years old · Sumer")
    if A["fart"] <= t < A["boredom"]:
        put(c, outlined("IT'S A FART JOKE", 130, fill=YEL, f=IMPACT, stroke=10, emoji="💨"), W / 2, 220, popk(t, A["fart"]))
        if pcard("f7_tablet.jpg", 520): put(c, pcard("f7_tablet.jpg", 520, -3), 1500, 640, popk(t, A["fart"] + 0.2))
    if A["boredom"] <= t < A["games"]:
        L.headline(c, "HUMANS VS BOREDOM", t, A["boredom"], size=96)
        for k, (nm, f) in enumerate(zip(("phones", "books", "writing"), ("f7_phone.jpg", "f7_books.jpg", "f7_tablet.jpg"))):
            if t >= A[nm] and pcard(f, 340): put(c, xcross(pcard(f, 340, (-3, 2, -2)[k])), 560 + k * 400, 580, popk(t, A[nm]))
    if A["games"] <= t < A["habibi"]:
        L.headline(c, "SOME GAMES YOU CAN STILL PLAY", t, A["games"], size=84); put(c, pcard("f7_ur_board.jpg", 900, -2), W / 2, 590, popk(t, A["games"] + 0.3))
        if t >= A["rules"]: L.sub(c, "the oldest board game with rules we can read", t, A["rules"], y=270)
        if t >= A["win"]: put(c, D.stamp("HOW TO WIN", 70, (30, 140, 60)), 1500, 760, popk(t, A["win"]))
    if A["habibi"] <= t < CH[0][1]: L.character(c, "host_cool", t, A["habibi"], 1560, h=520); L.headline(c, "WHAT DID ANCIENT HUMANS DO FOR FUN?", t, A["habibi"] + 0.4, size=74)
    # ---- CH1 art
    if A["muna"] <= t < A["sulawesi"]:
        L.place(c, cam, "Muna Island, Indonesia", P["Muna"], popk(t, A["muna"]), (176, 62, 34), dy=70)
        L.big(c, "67,800+ YEARS", t, A["muna"] + 1.2, size=120, sub="the oldest known rock art · Oktaviana et al., Nature 2026")
        if t >= A["blew"]: put(c, pcard("f7_hands.jpg", 540, 3), 1540, 640, popk(t, A["blew"])); L.sub(c, "stencils like these (Cueva de las Manos, Argentina, much younger) · Pexels", t, A["blew"] + 0.4, y=900 - 60, col=(255, 255, 255))
        if t >= A["narrowed"]: L.sub(c, "fingers narrowed, like a claw", t, A["narrowed"], y=360, col=(255, 255, 255))
    if A["sulawesi"] <= t < A["rouffignac"] - 1.6:
        L.place(c, cam, "Leang Karampuang, Sulawesi", P["Sulawesi"], popk(t, A["sulawesi"]), (176, 62, 34), dy=70)
        L.big(c, "51,200+ YEARS", t, A["sulawesi"] + 1.4, size=120, sub="three figures + a wild pig · Nature 2024")
        if t >= A["pig"] - 0.6 and pcard("f7_cave_animal.jpg", 640): put(c, pcard("f7_cave_animal.jpg", 640, 3), 1440, 640, popk(t, A["pig"] - 0.6)); L.sub(c, "cave animals like these (a younger cave, for illustration)", t, A["pig"], y=900 - 60, col=(255, 255, 255))
        if t >= A["story"]: L.sub(c, "maybe the oldest picture STORY ever found", t, A["story"], y=360, col=(255, 255, 255))
    if A["rouffignac"] <= t < CH[1][1]:
        L.place(c, cam, "Rouffignac Cave, France", P["Rouffignac"], popk(t, A["rouffignac"]), (176, 62, 34), dy=70)
        L.headline(c, "CEILING COVERED IN FINGER LINES", t, A["rouffignac"] + 0.6, size=76)
        if t >= A["kids"]: L.sub(c, "many probably made by kids aged 2-5 · Sharpe & Van Gelder 2006", t, A["kids"], y=270)
        if t >= A["lift"]: put(c, outlined("A PARENT LIFTED A TODDLER UP", 64, fill=YEL), 1340, 800, popk(t, A["lift"]))
    # ---- CH2 music
    if A["hohle"] <= t < A["slovenia"]:
        L.place(c, cam, "Hohle Fels Cave, Germany", P["HohleFels"], popk(t, A["hohle"]), (120, 100, 70), dy=-50)
        if t >= A["vulture"]: L.big(c, "~40,000 YEARS", t, A["vulture"] + 1.0, size=120, sub="vulture wing-bone flute, 5 finger holes · Conard 2009")
        if t >= A["geissen"]:
            L.place(c, cam, "Geissenklösterle", P["Geissen"], popk(t, A["geissen"]), (120, 100, 70), dy=60); None
            if t < A["survive"]: L.sub(c, "42,000-43,000 years · bird bone + mammoth ivory · Higham 2012", t, A["geissen"] + 0.5, y=360, col=(255, 255, 255))
        if t >= A["survive"]: put(c, outlined("NOBODY NEEDS A FLUTE TO SURVIVE", 60, fill=YEL), W / 2, 370, popk(t, A["survive"]))
    if A["slovenia"] <= t < CH[2][1]:
        L.place(c, cam, "Divje Babe, Slovenia", P["DivjeBabe"], popk(t, A["slovenia"]), (120, 100, 70), dy=70)
        L.big(c, "50,000-60,000 YEARS", t, A["slovenia"] + 0.4, size=100, sub="a cave-bear bone with holes · National Museum of Slovenia")
        if t >= A["hyena"]: put(c, STAMP, 1450, 620, popk(t, A["disputed"] - 0.3)); L.sub(c, "Neanderthal flute... or a hyena's chew toy?", t, A["hyena"] - 1.2, y=360, col=(255, 255, 255))
    # ---- CH3 games
    if A["games2"] + 1.4 <= t < A["ur"] - 1.6:
        L.place(c, cam, "Folsom sites: Colorado, Wyoming, New Mexico", P["Folsom"], popk(t, A["games2"] + 1.6), (150, 110, 60), dy=70)
        L.big(c, "12,000+ YEARS", t, A["games2"] + 1.8, size=120, sub="565 two-sided dice, maybe the oldest · Madden, American Antiquity 2026")
        if pcard("f7_bone_dice.jpg", 440): put(c, pcard("f7_bone_dice.jpg", 440, 3), 1640, 600, popk(t, A["dice"])); L.sub(c, "later bone dice, for comparison", t, A["dice"] + 0.3, y=900 - 60, col=(255, 255, 255))
        if t >= A["fortune"]: L.sub(c, "games... or fortune telling? maybe both", t, A["fortune"], y=360, col=(255, 255, 255))
    if A["ur"] <= t < A["india"] - 0.3:
        if t < A["finkel"]: L.place(c, cam, "Ur, Iraq", P["Ur"], popk(t, A["ur"]), (40, 70, 150), dy=-50)
        if t < A["finkel"]: L.big(c, "~4,600 YEARS", t, A["ur"] + 0.5, size=120, sub="the Royal Game of Ur · 5 boards from the royal tombs")
        else: L.big(c, "RULES: A TABLET FROM 177 BC", t, A["finkel"], size=90, sub="read by Irving Finkel, British Museum")
        if t >= A["finkel"]: put(c, ur_real(t), W / 2, 680, popk(t, A["finkel"]))
        if t >= A["race"]: put(c, pill("race your pieces around the board", 40, YEL), W / 2, 335, popk(t, A["race"]))
        if t >= A["land"]: put(c, pill("land on your rival = send it back", 40, (255, 255, 255)), W / 2, 400, popk(t, A["land"]))
        if t >= A["off"]: put(c, D.stamp("FIRST OFF = WIN", 64, (30, 140, 60)), 1640, 700, popk(t, A["off"]))
        if t >= A["luck"]: put(c, pill("rosettes: good luck squares, says the tablet", 40, (255, 140, 140)), W / 2, 335, popk(t, A["luck"]))
    if A["india"] - 0.3 <= t < A["again"] - 0.3:
        L.place(c, cam, "Ur", P["Ur"], 1.0, (40, 70, 150), dy=-50); L.place(c, cam, "Kochi, India · until the 1950s", P["Kochi"], popk(t, A["kochi"]), (40, 70, 150), dy=70)
        u = ease((t - A["kochi"]) / 1.0)
        if u > 0: x0, y0 = geo(cam, *P["Ur"]); x1, y1 = geo(cam, *P["Kochi"]); ImageDraw.Draw(c).line((x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), fill=YEL, width=8)
        if t >= A["onegame"]: L.big(c, "ONE GAME, 4,000+ YEARS", t, A["onegame"], size=110)
    if A["again"] - 0.3 <= t < A["ai"] - 0.3:
        L.place(c, cam, "Saqqara, Egypt", P["Saqqara"], popk(t, A["again"]), (150, 110, 60), dy=70)
        if t < A["senet"]: put(c, outlined("HI AGAIN, EGYPT", 90, fill=YEL), W / 2, 200, popk(t, A["again"] - 0.2))
        else: L.big(c, "SENET", t, A["senet"], size=130, sub="already in a tomb painting c. 2620 BC · Hesy-Re")
        if t >= A["tut"]: L.sub(c, "Tutankhamun was buried with several senet boards", t, A["tut"], y=372, col=(255, 255, 255))
    if A["ai"] - 0.3 <= t < A["sub_mid"] - 0.2:
        L.place(c, cam, "Heerlen, Netherlands", P["Heerlen"], popk(t, A["ai"]), (120, 120, 130), dy=70)
        L.big(c, "100+ RULE SETS", t, A["ai"] + 0.4, size=120, sub="tested by AI players on a Roman stone board · Antiquity, Feb 2026")
        if t >= A["ai2"]: put(c, outlined("AI LEARNING ANCIENT BOARD GAMES", 66, fill=YEL), W / 2, 420, popk(t, A["ai2"]))
    L.subscribe_nudge(c, t, A["sub_mid"], A["sub_more"] + 1.4, x=1200, y=470, t_click=A["sub_word"])
    # ---- CH4 sports
    if A["beni"] <= t < A["mexico"] - 1.6:
        L.place(c, cam, "Beni Hasan, Egypt", P["BeniHasan"], popk(t, A["beni"]), (150, 110, 60), dy=70)
        L.big(c, "220 PAIRS OF WRESTLERS", t, A["beni"] + 0.8, size=100, sub="tomb wall, c. 2000 BC · Egypt's Ministry of Tourism & Antiquities")
        if t >= A["red"]: L.sub(c, "one red, one brown: follow every hold", t, A["red"], y=360, col=(255, 255, 255))
        if t >= A["manual"]: put(c, D.stamp("WRESTLING MANUAL", 60, (40, 90, 180)), 1420, 640, popk(t, A["manual"]))
    if A["mexico"] <= t < A["greece"] - 1.6:
        L.place(c, cam, "Paso de la Amada, Mexico", P["PasoAmada"], popk(t, A["mexico"]), (150, 110, 60), dy=70)
        L.big(c, "~1650 BC", t, A["mexico"] + 0.6, size=130, sub="a ballcourt ~80 m long · Hill, Blake & Clark, Nature 1998")
        pass
        if t >= A["manati"]:
            L.place(c, cam, "El Manatí", P["ElManati"], popk(t, A["manati"]), (30, 26, 24), dy=-50)
            L.sub(c, "solid rubber balls, ~3,600 years old: the oldest we know · The Met", t, A["manati"], y=360, col=(255, 255, 255))
    if A["greece"] <= t < A["backjoke"] - 0.3:
        L.place(c, cam, "Olympia, Greece", P["Olympia"], popk(t, A["greece"]), (40, 90, 180), dy=70)
        L.big(c, "776 BC: ONE EVENT", t, A["greece"] + 0.6, size=110, sub="a sprint of ~192 m · World History Encyclopedia")
        if t >= A["cook"]: L.sub(c, "the winner, by tradition: Koroibos, a cook", t, A["cook"] - 0.4, y=360, col=(255, 255, 255))
        if t >= A["naked"] - 0.5:
            put(c, outlined("BY 720 BC: COMPLETELY NAKED", 64, fill=YEL), 760, 480, popk(t, A["naked"]))
    # ---- CH5 jokes & parties
    if A["sumer"] <= t < A["philo"] - 0.3:
        L.place(c, cam, "Sumer, southern Iraq", P["Sumer"], popk(t, A["sumer"]), (150, 110, 60), dy=70)
        L.big(c, "~1900 BC", t, A["sumer"] + 0.5, size=120, sub="the oldest recorded joke · Univ. of Wolverhampton 2008")
        if pcard("f7_tablet.jpg", 480): put(c, pcard("f7_tablet.jpg", 480, -3), 420, 640, popk(t, A["sumer"] + 1.0))
        if t >= A["wife"] - 1.5:
            d = L.panel(c, (900, 330, 1800, 600)); f = font(SANS, 40)
            for k, l in enumerate(("Something that has never happened", "since time began:", "a young wife did not fart", "in her husband's lap.")):
                d.text((1350, 380 + k * 58), l, font=f, fill=(255, 255, 255) if k < 2 else YEL, anchor="mm")
        if t >= A["lap"] + 0.5: put(c, D.stamp("THAT'S THE JOKE", 64, (210, 40, 40)), 1560, 720, popk(t, A["lap"] + 0.5))
    if A["philo"] - 0.3 <= t < A["festival"] - 0.3:
        L.place(c, cam, "Rome", P["Rome"], popk(t, A["philo"]), (150, 40, 40), dy=-50)
        if t < A["pompeii"]: L.big(c, "PHILOGELOS", t, A["philo"], size=120, sub="'The Laughter Lover': ~265 jokes · late 4th-5th c. AD")
        else:
            L.place(c, cam, "Pompeii", P["Pompeii"], popk(t, A["pompeii"]), (150, 40, 40), dy=70)
            L.big(c, "POMPEII GRAFFITI", t, A["pompeii"], size=110, sub="before AD 79 · World History Encyclopedia")
            if t >= A["amazed"] - 0.3: put(c, pill("'I'm amazed, wall, that you haven't collapsed under so much boring graffiti'", 38, YEL), W / 2, 345, popk(t, A["amazed"] - 0.3))
    if A["festival"] - 0.3 <= t < CH[5][1]:
        L.place(c, cam, "Temple of Mut, Luxor", P["Mut"], popk(t, A["festival"]), (150, 110, 60), dy=70)
        L.big(c, "THE FESTIVAL OF DRUNKENNESS", t, A["festival"], size=90, sub="~1470 BC, under Hatshepsut · Betsy Bryan, Johns Hopkins")
        if t >= A["drummers"]: L.sub(c, "then drummers woke everyone up", t, A["drummers"], y=360, col=(255, 255, 255))
        if t >= A["sober"]: put(c, D.stamp("DESIGNATED SOBER", 60, (40, 90, 180)), 1450, 640, popk(t, A["sober"]))
    # ---- CH6 kids
    if A["siberia"] <= t < A["spain"] - 1.6:
        L.place(c, cam, "Siberia", P["Siberia"], popk(t, A["siberia"]), (150, 110, 60), dy=70)
        L.big(c, "~4,000 YEARS", t, A["siberia"] + 0.5, size=120, sub="a clay bear-head rattle · Archaeology 2016")
        sh = 6 * math.sin(t * 40) if t >= A["rattles"] else 0
        if pcard("f7_rattle.jpg", 520): put(c, pcard("f7_rattle.jpg", 520, 3), 1450 + sh, 640, popk(t, A["siberia"] + 1.0)); L.sub(c, "an ancient clay rattle like it (similar, for illustration)", t, A["siberia"] + 1.2, y=900 - 60, col=(255, 255, 255))
        if t >= A["rattles"]: put(c, outlined("IT STILL RATTLES", 76, fill=YEL), 1450, 900 - 60, popk(t, A["rattles"]))
    if A["spain"] <= t < A["rome"] - 0.3:
        L.place(c, cam, "Spain + Portugal", P["Iberia"], popk(t, A["spain"]), (96, 104, 112), dy=70)
        L.big(c, "5,500-4,750 YEARS", t, A["spain"] + 0.6, size=110, sub="owl-shaped slate plaques · Negro et al., Scientific Reports 2022")
        if t >= A["children"]: L.sub(c, "many probably made by children", t, A["children"], y=360, col=(255, 255, 255))
    if A["rome"] - 0.3 <= t < CH[6][1]:
        L.place(c, cam, "Rome", P["Rome"], popk(t, A["rome"]), (150, 40, 40), dy=70)
        L.big(c, "AN IVORY DOLL, ~1,850 YEARS OLD", t, A["rome"] + 0.4, size=90, sub="arms and legs that bend at the joints · Capitoline Museums")
    # ---- CH7 why
    if A["same"] <= t < A["reason"]:
        L.headline(c, "THE SAME THINGS WE DO", t, A["same"], size=100)
        recap = [(A["walls"], "f7_hands.jpg"), (A["walls"] + 0.6, "f7_bone_flute.jpg"), (A["gambled"] - 0.4, "f7_ur_board.jpg"), (A["gambled"] + 0.6, "f7_ballcourt.jpg"),
                 (A["gambled"] + 1.4, "f7_pompeii_graffiti.jpg"), (A["gambled"] + 2.2, "f7_rattle.jpg")]
        for k, (tt, f) in enumerate(recap):
            if t >= tt and pcard(f, 420): put(c, pcard(f, 420, (-3, 2, -2, 3, -2, 2)[k]), 330 + (k % 3) * 630, 440 + (k // 3) * 300, popk(t, tt))
    if A["y2014"] <= t < A["bored"]:
        L.big(c, "2014: BOREDOM VS ELECTRIC SHOCKS", t, A["y2014"], size=72, sub="Wilson et al., Science 2014 · up to 15 minutes alone")
        if pcard("f7_button.jpg", 300): put(c, pcard("f7_button.jpg", 300, 3), 1680, 560, popk(t, A["button"]))
        if t >= A["men"]: bars(c, t, A["men"], [("men who shocked themselves", 12, 18, (220, 60, 50)), ("women", 6, 24, (220, 140, 50))], y0=560)
    if A["bored"] <= t < A["subscribe"]:
        L.headline(c, "HUMANS REALLY HATE BEING BORED", t, A["bored"], size=90)
        if t >= A["lasted"]: put(c, outlined("A FART JOKE, 4,000 YEARS LATER", 70, fill=YEL, emoji="💨"), W / 2, 400, popk(t, A["lasted"]))
    if A["subscribe"] <= t < A["endscreen"]:
        L.character(c, "host_cool", t, A["subscribe"], 1560, h=520)
        put(c, pill("SUBSCRIBE · next: how your dog really sees you", 50, (255, 255, 255), (200, 30, 30, 240)), W / 2 - 160, 300, popk(t, A["subscribe"] + 0.3))
    for f, t0, t1, x, y, w, rot, cr in PHOTOS:
        if ph(f): L.photo(c, ph(f), t, t0, t1, x=x, y=y, w=w, rot=rot, credit=cr)
    L.end_screen(c, t, A["endscreen"], "still curious?")
    L.chapter_card(c, t, CH)
UR_ROSE_LIT = set(D.UR_ROSE)

SFX = [("pop", A[n] + 0.3, -20) for n in ("fart", "muna", "blew", "sulawesi", "pig", "rouffignac", "hohle", "vulture", "geissen", "slovenia", "dice", "ur",
                                          "finkel", "race", "land", "luck", "kochi", "senet", "ai", "beni", "mexico", "manati", "greece", "naked", "sumer",
                                          "lap", "philo", "pompeii", "festival", "sober", "siberia", "rattles", "owls", "doll", "y2014", "men")]
SFX += [("paper_slide", t0, -20) for _, t0 in CH]
SFX += [("pop", ph_[1], -21) for ph_ in PHOTOS]
SFX += [("pop", A["sub_word"] + 0.25, -18), ("paper_slide", A["endscreen"], -18), ("pop", A["endscreen"] + 2.3, -20)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END)
    else: K.main(sys.argv, overlay, SFX)
