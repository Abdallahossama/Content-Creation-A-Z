p = "D:/why habibi/_pipeline/episodes/ep07_ancient_fun/render_ep07.py"
s = open(p, encoding="utf-8").read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)
R('''PHOTOS = []   # (file, t0, t1, x, y, w, rot, credit) - filled once the photo batch is approved and downloaded''',
'''PHOTOS = [   # (file, t0, t1, x, y, w, rot, credit) - real photos as proof (approved downloads 18 Oct 2026); "like these" where it's a similar example
    ("f7_hands.jpg", A["rockart"] - 0.2, A["sulawesi"] - 0.1, 520, 600, 640, -3, "hand stencils like these: Cueva de las Manos, Argentina (much younger) · Pexels / Jose Luis Vanasco"),
    ("f7_flutings.jpg", A["rouffignac"] + 0.6, A["kids"] - 0.1, W / 2, 600, 760, 2, "finger flutings like these (La Roche-Cotard, France) · Marquet et al. 2023, CC BY 4.0"),
    ("f7_bone_flute.jpg", A["survive"] - 0.2, A["slovenia"] - 0.1, 1420, 760, 520, 3, "a younger Stone Age bone flute (Germany) · Burkhard Mücke, CC BY 4.0"),
    ("f7_divje_babe.jpg", A["slovenia"] + 0.6, CH[2][1], 520, 600, 300, -3, "the Divje Babe bone · Szilas, CC0"),
    ("f7_ur_board.jpg", A["royal"] - 0.2, A["finkel"] - 0.1, W / 2, 610, 860, -2, "the Royal Game of Ur, British Museum · BabelStone, CC0"),
    ("f7_senet_box.jpg", A["senet"] + 0.3, A["tut"] - 0.1, W / 2, 640, 820, 2, "senet + 'twenty squares' game box · The Met, CC0"),
    ("f7_nefertari_senet.jpg", A["tut"] - 0.1, A["ai"] - 0.4, 560, 640, 520, -3, "Queen Nefertari playing senet (facsimile) · The Met, CC0"),
    ("f7_beni_hasan.jpg", A["beni"] + 1.6, A["mexico"] - 1.7, 560, 620, 440, -3, "Beni Hasan wrestlers (facsimile) · public domain"),
    ("f7_ballcourt.jpg", A["mexico"] + 1.2, A["manati"] - 0.1, 1440, 640, 640, 3, "a much later ballcourt: Chichen Itza · Pexels / Henry VL"),
    ("f7_olympia.jpg", A["greece"] + 1.0, A["naked"] - 0.6, 1440, 640, 620, 3, "Olympia's stadium entrance · Erik Drost, CC BY 2.0"),
    ("f7_pompeii_street.jpg", A["pompeii"], A["pompeii"] + 1.6, W / 2, 620, 820, -2, "Pompeii · Pexels / Bogdan Giurca"),
    ("f7_pompeii_graffiti.jpg", A["pompeii"] + 1.6, A["amazed"] - 0.3, W / 2, 620, 760, 2, "real graffiti, House of the Vettii, Pompeii · Buzz Ferebee, public domain"),
    ("f7_banquet.jpg", A["festival"] + 0.6, CH[5][1], 560, 640, 700, -2, "banquet with musicians, tomb of Nakht (facsimile) · The Met, CC0"),
    ("f7_dolls.jpg", A["doll"] - 0.2, CH[6][1], 1450, 620, 360, 3, "Roman dolls like hers (Getty Villa) · Gary Todd, CC0"),
]''')
R('''        ur_show(c, t, A["royal"] - 0.3, W / 2, 620, lit=UR_ROSE_LIT if t >= A["luck"] else (), moves=t >= A["race"], scale=1.25)''',
  '''        ur_show(c, t, A["finkel"], W / 2, 620, lit=UR_ROSE_LIT if t >= A["luck"] else (), moves=t >= A["race"], scale=1.25)''')
R('''        if t >= A["senet"]: put(c, SENET, W / 2, 640, popk(t, A["senet"] + 0.3))''', '''        if t >= A["senet"] and not ph("f7_senet_box.jpg"): put(c, SENET, W / 2, 640, popk(t, A["senet"] + 0.3))''')
R('''        if t >= A["red"]:
            for k, col in enumerate(((190, 60, 40), (120, 80, 40))): L.character(c, "ice_age_naked", t, A["red"] + k * 0.2, 1380 + k * 170, y=860, h=300, flip=k == 1)
            L.sub(c, "one red, one brown: follow every hold", t, A["red"], y=360, col=(255, 255, 255))
        if t >= A["manual"]: put(c, D.stamp("WRESTLING MANUAL", 60, (40, 90, 180)), 600, 640, popk(t, A["manual"]))''',
'''        if t >= A["red"]: L.sub(c, "one red, one brown: follow every hold", t, A["red"], y=360, col=(255, 255, 255))
        if t >= A["manual"]: put(c, D.stamp("WRESTLING MANUAL", 60, (40, 90, 180)), 1420, 640, popk(t, A["manual"]))''')
R('''        put(c, COURT, 1430, 640, popk(t, A["mexico"] + 1.2))''', '''        if not ph("f7_ballcourt.jpg") or t >= A["manati"]: put(c, COURT, 1430, 640, popk(t, A["manati"] if ph("f7_ballcourt.jpg") else A["mexico"] + 1.2))''')
R('''L.big(c, "POMPEII GRAFFITI", t, A["pompeii"], size=110, sub="before AD 79 · World History Encyclopedia"); put(c, WALL, W / 2, 620, popk(t, A["amazed"] - 0.3))''',
  '''L.big(c, "POMPEII GRAFFITI", t, A["pompeii"], size=110, sub="before AD 79 · World History Encyclopedia")
            if t >= A["amazed"] - 0.3: put(c, WALL, W / 2, 620, popk(t, A["amazed"] - 0.3))''')
R('''        put(c, DOLL, 1450, 640, popk(t, A["doll"]))''', '''        if not ph("f7_dolls.jpg"): put(c, DOLL, 1450, 640, popk(t, A["doll"]))''')
R('''SFX += [("paper_slide", t0, -20) for _, t0 in CH]''', '''SFX += [("paper_slide", t0, -20) for _, t0 in CH]
SFX += [("pop", ph_[1], -21) for ph_ in PHOTOS]''')
open(p, "w", encoding="utf-8").write(s); print("patched")
