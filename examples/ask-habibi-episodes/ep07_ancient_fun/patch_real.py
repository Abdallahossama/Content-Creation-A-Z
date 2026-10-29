"""Ep 7 v2 (user rules 18 Oct 2026): REAL objects instead of drawings, and no women anywhere.
Drawn objects -> real photos (existing or the round-3 downloads, used when present); Ur rules annotated ON the real board photo."""
import shutil
p = "D:/why habibi/_pipeline/episodes/ep07_ancient_fun/render_ep07.py"
shutil.copy(p, "D:/why habibi/_archive/render_ep07_drawn.py")
s = open(p, encoding="utf-8").read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)

# --- helpers: real-photo cards + the annotated real Ur board
R('''ICONS = [D.crossed(k, 200) for k in ("phone", "book", "writing")]''', '''import marker as MK
PC = {}
def pcard(name, w, rot=0):
    """a real photo as a white-bordered card (cached); None if the file is missing"""
    if not ph(name): return None
    if (name, w, rot) not in PC: PC[(name, w, rot)] = L._photo_card(ph(name), w, rot, None)
    return PC[(name, w, rot)]
def xcross(im):
    im = im.copy(); MK.strokes(im, [__import__("numpy").array([(40, 40), (im.width - 40, im.height - 40)]), __import__("numpy").array([(im.width - 40, 40), (40, im.height - 40)])], MK.RED, 16, seed=3); return im
UR = {}
UR_PATH = [(835, 660), (640, 660), (420, 660), (205, 660), (240, 505), (445, 505), (655, 505), (835, 505), (1035, 505), (1235, 505), (1430, 505), (1610, 505), (1650, 660), (1440, 660)]
UR_ROSES = [(265, 375), (205, 660), (835, 505), (1380, 355), (1440, 660)]
def ur_real(t, w=1180):
    """the real Royal Game of Ur (British Museum photo) with the rules drawn on it in marker as the voice explains them"""
    import numpy as np
    if "base" not in UR: UR["base"] = Image.open(PH + "f7_ur_board.jpg").convert("RGBA").crop((0, 250, 1920, 900))
    im = UR["base"].copy()
    if t >= A["race"]: MK.strokes(im, [np.array(UR_PATH, float)], MK.YEL, 16, min(1, (t - A["race"]) / 2.5), seed=2)
    if t >= A["land"]:
        x, y = UR_PATH[8]; MK.strokes(im, [np.array([(x - 60, y - 60), (x + 60, y + 60)]), np.array([(x + 60, y - 60), (x - 60, y + 60)])], MK.RED, 18, min(1, (t - A["land"]) / 0.5), seed=5)
    if t >= A["luck"]:
        for k, (x, y) in enumerate(UR_ROSES): MK.strokes(im, MK.circle_path(x, y - 250, 105, 95, seed=k), MK.RED, 14, min(1, (t - A["luck"] - k * 0.25) / 0.5), seed=k)
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS); card = Image.new("RGBA", (im.width + 24, im.height + 24), (250, 247, 240, 255)); card.alpha_composite(im, (12, 12)); return card''')
# the drawn Ur board path used only y = cell centres in the cropped photo (crop starts at y=250)
s = s.replace("UR_PATH = [(835, 660), (640, 660), (420, 660), (205, 660), (240, 505), (445, 505), (655, 505), (835, 505), (1035, 505), (1235, 505), (1430, 505), (1610, 505), (1650, 660), (1440, 660)]",
              "UR_PATH = [(x, y - 250) for x, y in ((835, 660), (640, 660), (420, 660), (205, 660), (240, 505), (445, 505), (655, 505), (835, 505), (1035, 505), (1235, 505), (1430, 505), (1610, 505), (1650, 660), (1440, 660))]")
# --- HOOK
R('''put(c, outlined("IT'S A FART JOKE", 130, fill=YEL, f=IMPACT, stroke=10, emoji="💨"), W / 2, 220, popk(t, A["fart"])); L.character(c, "sleepy", t, A["fart"], 1580, h=440)''',
  '''put(c, outlined("IT'S A FART JOKE", 130, fill=YEL, f=IMPACT, stroke=10, emoji="💨"), W / 2, 220, popk(t, A["fart"]))
        if pcard("f7_tablet.jpg", 520): put(c, pcard("f7_tablet.jpg", 520, -3), 1500, 640, popk(t, A["fart"] + 0.2))''')
R('''        for k, (nm, im) in enumerate(zip(("phones", "books", "writing"), ICONS)):
            if t >= A[nm]: put(c, im, 600 + k * 360, 560, popk(t, A[nm]))''',
  '''        for k, (nm, f) in enumerate(zip(("phones", "books", "writing"), ("f7_phone.jpg", "f7_books.jpg", "f7_tablet.jpg"))):
            if t >= A[nm] and pcard(f, 340): put(c, xcross(pcard(f, 340, (-3, 2, -2)[k])), 560 + k * 400, 580, popk(t, A[nm]))''')
R('''ur_show(c, t, A["games"] + 0.3, W / 2, 560)''', '''put(c, pcard("f7_ur_board.jpg", 900, -2), W / 2, 590, popk(t, A["games"] + 0.3))''')
# --- CH1 art: real photos only
R('''        if t >= A["blew"]: put(c, HAND, 1500, 600, popk(t, A["blew"]))''', '''        if t >= A["blew"]: put(c, pcard("f7_hands.jpg", 600, 3), 1460, 640, popk(t, A["blew"])); L.sub(c, "stencils like these (Cueva de las Manos, Argentina, much younger) · Pexels", t, A["blew"] + 0.4, y=900 - 60, col=(255, 255, 255))''')
R('''    ("f7_hands.jpg", A["rockart"] - 0.2, A["sulawesi"] - 0.1, 440, 660, 540, -3, "hand stencils like these: Cueva de las Manos, Argentina (much younger) · Pexels / Jose Luis Vanasco"),\n''', '')
R('''        if t >= A["pig"] - 0.6: put(c, PIG, 1430, 620, popk(t, A["pig"] - 0.6))''',
  '''        if t >= A["pig"] - 0.6 and pcard("f7_cave_animal.jpg", 640): put(c, pcard("f7_cave_animal.jpg", 640, 3), 1440, 640, popk(t, A["pig"] - 0.6)); L.sub(c, "cave animals like these (a younger cave, for illustration)", t, A["pig"], y=900 - 60, col=(255, 255, 255))''')
R('''        if t >= A["kids"]: put(c, D.flutings(), 440, 560, popk(t, A["kids"])); L.sub''', '''        if t >= A["kids"]: L.sub''')
R('''    ("f7_flutings.jpg", A["rouffignac"] + 0.6, A["kids"] - 0.1, W / 2, 600, 760, 2,''', '''    ("f7_flutings.jpg", A["rouffignac"] + 0.6, A["music"] - 0.6, 600, 620, 720, 2,''')
R('''        if t >= A["lift"]:
            L.character(c, "ice_age_cape", t, A["lift"], 1500, y=840, h=380)
            lift = ease((t - A["lift"]) / 1.2); L.character(c, "ice_age_naked", t, A["lift"] + 0.2, 1500, y=520 - 120 * lift, h=180)''',
  '''        if t >= A["lift"]: put(c, outlined("A PARENT LIFTED A TODDLER UP", 64, fill=YEL), 1380, 640, popk(t, A["lift"]))''')
# --- CH2 music: the real bone flute instead of drawn flutes
R('''        if t >= A["vulture"]: put(c, FLUTE, W / 2, 640, popk(t, A["vulture"])); L.big''', '''        if t >= A["vulture"]: put(c, pcard("f7_bone_flute.jpg", 760, -2), W / 2, 680, popk(t, A["vulture"])); L.big''')
R('''put(c, IVORY, W / 2, 780, popk(t, A["geissen"] + 1.5))''', '''None''')
R('''    ("f7_bone_flute.jpg", A["survive"] - 0.2, A["slovenia"] - 0.1, 1500, 580, 470, 3, "a younger Stone Age bone flute (Germany) · Burkhard Mücke, CC BY 4.0"),\n''',
  '''    ("f7_bone_flute.jpg", A["vulture"], A["slovenia"] - 0.1, W / 2, 690, 760, -2, "a Stone Age bone flute like these (Germany, younger) · Burkhard Mücke, CC BY 4.0"),\n''')
# --- CH3 games
R('''        put(c, DICE, 1600, 600, popk(t, A["dice"]))''', '''        if pcard("f7_bone_dice.jpg", 520): put(c, pcard("f7_bone_dice.jpg", 520, 3), 1580, 620, popk(t, A["dice"])); L.sub(c, "later bone dice, for comparison", t, A["dice"] + 0.3, y=900 - 60, col=(255, 255, 255))''')
R('''        ur_show(c, t, A["finkel"], W / 2, 670, lit=UR_ROSE_LIT if t >= A["luck"] else (), moves=t >= A["race"], scale=1.25)''', '''        if t >= A["finkel"]: put(c, ur_real(t), W / 2, 680, popk(t, A["finkel"]))''')
R('''        if t >= A["senet"] and not ph("f7_senet_box.jpg"): put(c, SENET, W / 2, 640, popk(t, A["senet"] + 0.3))\n''', '')
R('''    ("f7_senet_box.jpg", A["senet"] + 0.3, A["tut"] - 0.1, W / 2, 640, 820, 2, "senet + 'twenty squares' game box · The Met, CC0"),''',
  '''    ("f7_senet_box.jpg", A["senet"] + 0.3, A["ai"] - 0.4, W / 2, 660, 760, 2, "senet + 'twenty squares' game box · The Met, CC0"),''')
R('''    ("f7_nefertari_senet.jpg", A["tut"] - 0.1, A["ai"] - 0.4, 1500, 680, 460, 3, "Queen Nefertari playing senet (facsimile) · The Met, CC0"),\n''', '')
# --- CH4 sports
R('''        if not ph("f7_ballcourt.jpg") or t >= A["manati"]: put(c, COURT, 1430, 640, popk(t, A["manati"] if ph("f7_ballcourt.jpg") else A["mexico"] + 1.2))''', '''        pass''')
R('''    ("f7_ballcourt.jpg", A["mexico"] + 1.2, A["manati"] - 0.1, 1520, 640, 600, 3,''', '''    ("f7_ballcourt.jpg", A["mexico"] + 1.2, A["greece"] - 1.7, 1520, 640, 600, 3,''')
R('''            L.character(c, "ice_age_naked", t, A["naked"] - 0.5, 1560, y=900, h=380)
            d = ImageDraw.Draw(c); d.rectangle((1460, 760, 1660, 820), fill=(10, 10, 10)); d.text((1560, 790), "CENSORED", font=font(IMPACT, 40), fill=(255, 255, 255), anchor="mm")
''', '')
# --- CH5 jokes: real tablet + the real graffiti photo with the translation as a caption pill
R('''        put(c, TABLET, 520, 620, popk(t, A["sumer"] + 1.0))''', '''        if pcard("f7_tablet.jpg", 560): put(c, pcard("f7_tablet.jpg", 560, -3), 520, 640, popk(t, A["sumer"] + 1.0))''')
R('''            if t >= A["amazed"] - 0.3: put(c, WALL, W / 2, 620, popk(t, A["amazed"] - 0.3))''',
  '''            if t >= A["amazed"] - 0.3: put(c, pill("'I'm amazed, wall, that you haven't collapsed under so much boring graffiti'", 38, YEL), W / 2, 880 - 60, popk(t, A["amazed"] - 0.3))''')
R('''    ("f7_pompeii_graffiti.jpg", A["pompeii"] + 1.6, A["amazed"] - 0.3, W / 2, 620, 760, 2,''', '''    ("f7_pompeii_graffiti.jpg", A["pompeii"] + 1.6, A["festival"] - 0.4, W / 2, 600, 760, 2,''')
R('''    ("f7_banquet.jpg", A["festival"] + 0.6, CH[5][1], 440, 660, 620, -2, "banquet with musicians, tomb of Nakht (facsimile) · The Met, CC0"),\n''', '')
# --- CH6 kids: real rattle, no drawn owl / doll
R('''        sh = 6 * math.sin(t * 40) if t >= A["rattles"] else 0; put(c, D.rattle(t if t >= A["rattles"] else 0), 1450 + sh, 640, popk(t, A["siberia"] + 1.0))''',
  '''        sh = 6 * math.sin(t * 40) if t >= A["rattles"] else 0
        if pcard("f7_rattle.jpg", 520): put(c, pcard("f7_rattle.jpg", 520, 3), 1450 + sh, 640, popk(t, A["siberia"] + 1.0)); L.sub(c, "an ancient clay rattle like it (similar, for illustration)", t, A["siberia"] + 1.2, y=900 - 60, col=(255, 255, 255))''')
R('''        put(c, OWL, 1450, 620, popk(t, A["owls"]))\n''', '')
R('''        if not ph("f7_dolls.jpg"): put(c, DOLL, 1450, 640, popk(t, A["doll"]))\n''', '')
R('''    ("f7_dolls.jpg", A["doll"] - 0.2, CH[6][1], 1450, 620, 360, 3, "Roman dolls like hers (Getty Villa) · Gary Todd, CC0"),\n''', '')
R('''L.big(c, "CREPEREIA'S IVORY DOLL", t, A["rome"] + 0.4, size=90, sub="jointed arms and legs · mid-2nd century AD · Capitoline Museums")''',
  '''L.big(c, "AN IVORY DOLL, ~1,850 YEARS OLD", t, A["rome"] + 0.4, size=90, sub="arms and legs that bend at the joints · Capitoline Museums")''')
# --- CH7 recap: real photos
R('''        for k, (nm, im) in enumerate(((A["walls"], HAND), (A["walls"] + 0.6, FLUTE), (A["gambled"] - 0.4, D.ur_board()), (A["gambled"] + 0.6, COURT), (A["gambled"] + 1.4, TABLET), (A["gambled"] + 2.2, D.rattle()))):
            if t >= nm:
                s = im.copy(); s.thumbnail((360, 260)); put(c, s, 330 + (k % 3) * 630, 420 + (k // 3) * 300, popk(t, nm))''',
  '''        recap = [(A["walls"], "f7_hands.jpg"), (A["walls"] + 0.6, "f7_bone_flute.jpg"), (A["gambled"] - 0.4, "f7_ur_board.jpg"), (A["gambled"] + 0.6, "f7_ballcourt.jpg"),
                 (A["gambled"] + 1.4, "f7_pompeii_graffiti.jpg"), (A["gambled"] + 2.2, "f7_rattle.jpg")]
        for k, (tt, f) in enumerate(recap):
            if t >= tt and pcard(f, 420): put(c, pcard(f, 420, (-3, 2, -2, 3, -2, 2)[k]), 330 + (k % 3) * 630, 440 + (k // 3) * 300, popk(t, tt))''')
R('''        put(c, D.shock_button(t >= A["men"]), 1650, 300, popk(t, A["button"]))''', '''        if pcard("f7_button.jpg", 360): put(c, pcard("f7_button.jpg", 360, 3), 1640, 330, popk(t, A["button"]))''')
open(p, "w", encoding="utf-8").write(s); print("patched")
