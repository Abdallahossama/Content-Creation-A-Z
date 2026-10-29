import shutil
p = "D:/why habibi/_pipeline/episodes/ep06_clothes/render_ep06.py"
shutil.copy(p, "D:/why habibi/_archive/render_ep06_v1.py")
s = open(p, encoding="utf-8").read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)

R('''WORLD = (20.0, 30.0, 8.5); AFRICA = (18.0, 5.0, 16); MOROCCO = (-6.5, 33.5, 120); FRANCE = (1.5, 45.0, 120); GEORGIA = (43.0, 42.3, 120)
EURASIA = (75.0, 46.0, 9.6); SIBERIA = (85.0, 52.0, 70); NORTH = (-35.0, 44.0, 9.2); BERING = (-170.0, 63.0, 30); OREGON = (-121.0, 43.5, 120)
ALPS = (10.8, 46.7, 150); EGYPT = (31.0, 27.5, 60); SUNG = (40.5, 56.0, 120)''',
'''WORLD = (20.0, 30.0, 8.5); AFRICA = (18.0, 5.0, 16); MOROCCO = (-6.0, 32.5, 40); FRANCE = (1.0, 46.0, 40); GEORGIA = (43.0, 42.5, 40)
EURASIA = (75.0, 46.0, 9.6); SIBERIA = (85.0, 52.0, 22); NORTH = (-35.0, 44.0, 9.2); BERING = (-170.0, 63.0, 30); OREGON = (-121.0, 43.8, 34)
ALPS = (10.8, 46.5, 40); EGYPT = (31.0, 28.0, 28); SUNG = (42.0, 55.0, 26)
MED = "D:/why habibi/_media/"; PH = MED + "photos_2026-10-18/"; LB = MED + "cutouts/louse_body.png"; LH = MED + "cutouts/louse_head.png"
BM = PH + "world_bluemarble_5400.jpg"; BMB = (-180.0, 180.0, -90.0, 90.0)
def ph(name): return PH + name if os.path.exists(PH + name) and os.path.getsize(PH + name) > 50000 else None''')
R('import sys, math\n', 'import os, sys, math\n')
R('(A["caucasus"], 60.0, 55.0, 12)', '(A["caucasus"], *EURASIA)')
R('''        ph = ((t - t0) * 0.8 + k * 0.11) % 1.0; xx = x + (k - 4) * 70; yy = y + ph * 300''',
  '''        ph = ((t - t0) * 0.8 + k * 0.11) % 1.0; xx = x + (k - 4) * 26; yy = y + ph * 220''')
R(s[s.index("ICE = [["):s.index("def wind(")], '''ICE = [  # approximate ice sheets at the Last Glacial Maximum (drawn by us)
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
''')
R('''    lon, lat, p = cam
    # ---- HOOK''', '''    lon, lat, p = cam
    # real (NASA Blue Marble) <-> our drawn map, now and then
    L.real_map(c, cam, max(L.fade(t, -1.0, A["dressed"], 0.6), L.fade(t, A["froze"] - 0.3, A["beringia"] - 0.4, 0.7), L.fade(t, A["fiber"] - 0.6, A["modesty2"], 0.6)), BM, BMB)
    # ---- HOOK''')
R('''put(c, LOUSE, W / 2, 560, popk(t, A["louse1"] + 0.3))''', '''L.cutout(c, LB, t, A["louse1"] + 0.3, W / 2, 600, 450, rot=-4)''')
R('''drops(c, t, A["sweat1"], W / 2, 460)''', '''drops(c, t, A["sweat1"], 1600, 640)''')
R('''        put(c, LOUSE, 620, 560, popk(t, A["kinds"] + 0.4)); L.sub(c, "HEAD LICE: live in hair", t, A["kinds"] + 0.6, y=760, col=(255, 255, 255))
        if t >= A["seams"] - 1.2:
            put(c, louse(1.0, (170, 140, 100)), 1300, 560, popk(t, A["seams"] - 1.2))
            put(c, pill("BODY LICE: live in CLOTHES (the seams) · CDC", 36, (255, 225, 120)), 1300, 760, popk(t, A["seams"] - 1.0))''',
'''        L.cutout(c, LH, t, A["kinds"] + 0.4, 560, 560, 250, rot=-8); put(c, pill("HEAD LICE: live in hair", 36), 560, 760, popk(t, A["kinds"] + 0.6))
        if t >= A["seams"] - 1.2:
            L.cutout(c, LB, t, A["seams"] - 1.2, 1340, 540, 400, rot=5)
            put(c, pill("BODY LICE: live in CLOTHES (the seams) · CDC", 36, (255, 225, 120)), 1340, 790, popk(t, A["seams"] - 1.0))''')
R('''        if t >= A["tools1"]: put(c, BONE, W / 2, 560, popk(t, A["tools1"]))''',
  '''        if t >= A["tools1"] and ph("cl_lissoir.jpg"): L.photo(c, ph("cl_lissoir.jpg"), t, A["tools1"], x=W / 2, y=600, w=700, rot=-2, credit="Ice Age bone tool · Musée de l'Homme · public domain")''')
R('''        if t >= A["scraping"]: put(c, BONE, 1500, 700, popk(t, A["scraping"]))''',
  '''        if ph("cl_lissoir.jpg"): L.photo(c, ph("cl_lissoir.jpg"), t, A["scraping"], A["carnivores"] + 0.2, x=1440, y=620, w=620, rot=3, credit="a bone hide-smoother (a later one, France) · public domain")''')
R('''        if t >= A["georgia"] + 2.0: put(c, fibers(t), W / 2, 640, popk(t, A["georgia"] + 2.0))''', '''        if t >= A["georgia"] + 2.0:
            L.panel(c, (1180, 470, 1860, 800)); put(c, fibers(t), 1520, 635, popk(t, A["georgia"] + 2.0))''')
R('''put(c, NEEDLE, W / 2, 380, popk(t, A["invention"] + 1.0))''',
  '''(L.photo(c, ph("cl_eyed_needle.jpg"), t, A["invention"] + 1.0, A["draped1"], x=W / 2, y=590, w=860, rot=-2, credit="Ice Age eyed needle and bone tools · Musée d'Archéologie nationale · CC0") if ph("cl_eyed_needle.jpg") else put(c, NEEDLE, W / 2, 380, popk(t, A["invention"] + 1.0)))''')
R('''L.character(c, "ice_age_cape", t, A["draped1"], 960, h=480); L.sub''', '''L.character(c, "ice_age_cape", t, A["draped1"], 1600, h=480); L.sub''')
R('''        L.character(c, "ice_age_cape", t, A["fitted1"], 640, h=500); L.character(c, "ice_age_parka", t, A["fitted1"] + 0.4, 1280, h=500)''',
  '''        L.character(c, "ice_age_cape", t, A["fitted1"], 640, y=850, h=430); L.character(c, "ice_age_parka", t, A["fitted1"] + 0.4, 1280, y=850, h=430)''')
R('''        if t >= A["wind"] - 1.5: wind(c, t, 300, 520); put(c, pill("wind gets in", 34), 640, 1000, popk(t, A["wind"] - 1.5)); put(c, pill("warm air stays in", 34, (255, 225, 120)), 1280, 1000, popk(t, A["wind"] - 1.2))''',
  '''        if t >= A["wind"] - 1.5: wind(c, t, 300, 560); put(c, pill("wind gets in", 34), 640, 370, popk(t, A["wind"] - 1.5)); put(c, pill("warm air stays in", 34, (255, 225, 120)), 1280, 370, popk(t, A["wind"] - 1.2))''')
R('''            for r in range(int(min(60, (t - A["sunghir"] - 1.2) * 30))): x = 1470 + (r % 12) * 20; y = 760 + (r // 12) * 34; d.ellipse((x, y, x + 12, y + 12), fill=(250, 245, 230))''',
  '''            for r in range(int(min(44, (t - A["sunghir"] - 1.2) * 30))): x = 1478 + (r % 11) * 20; y = 905 + (r // 11) * 26; d.ellipse((x, y, x + 11, y + 11), fill=(250, 245, 230), outline=(120, 100, 70))''')
R('''        L.place(c, cam, "Beringia: dry land", P["Beringia"], popk(t, A["beringia"]), (150, 110, 60), dy=70)''',
  '''        L.place(c, cam, "Beringia: dry land", P["Beringia"], popk(t, A["beringia"]), (150, 110, 60), dy=70)
        if ph("cl_beringia_nps.png"): L.photo(c, ph("cl_beringia_nps.png"), t, A["beringia"] + 0.8, A["alaska2"] - 0.4, x=1460, y=560, w=640, rot=2, credit="Beringia map · US National Park Service")''')
R('''        L.character(c, "ice_age_parka", t, A["iceman"], 1600, h=460)''', '''        L.character(c, "ice_age_parka", t, A["iceman"], 1600, h=460)
        if ph("cl_otzi_shoe.jpg"): L.photo(c, ph("cl_otzi_shoe.jpg"), t, A["iceman"] + 1.6, A["linen"] - 0.5, x=560, y=620, w=560, rot=-3, credit="Ötzi's shoe (replica) · Bata Shoe Museum · CC0")''')
R('''L.headline(c, "HI AGAIN, EGYPT", t, A["again"] - 0.2, y=360, size=70, col=YEL)''', '''put(c, outlined("HI AGAIN, EGYPT", 70, fill=YEL), 1250, 640, popk(t, A["again"] - 0.2))''')
R('''        else: L.big(c, "132 MILLION TONNES", t, A["fiber"] - 0.6, size=110, sub="of fiber a year (2024) · ~69% synthetic · Textile Exchange")''',
  '''        else:
            L.big(c, "132 MILLION TONNES", t, A["fiber"] - 0.6, size=110, sub="of fiber a year (2024) · ~69% synthetic · Textile Exchange")
            if ph("cl_textile_factory.jpg"): L.photo(c, ph("cl_textile_factory.jpg"), t, A["fiber"], x=W / 2, y=600, w=720, rot=2, credit="Pexels · Rajesh Kumar Verma")''')
R('''        L.character(c, "ice_age_naked", t, A["fur_end"], 520, h=460); L.headline''', '''        L.character(c, "ice_age_naked", t, A["fur_end"], 520, y=850, h=400); L.headline''')
R('''        if t >= A["borrowed"]: L.character(c, "ice_age_cape", t, A["borrowed"], 960, h=460); L.sub''',
  '''        if t >= A["borrowed"]: L.character(c, "ice_age_cape", t, A["borrowed"], 960, y=850, h=400); L.sub''')
R('''        L.character(c, "ice_age_naked", t, 0, 520, h=460); L.character(c, "ice_age_cape", t, 0, 960, h=460); L.character(c, "ice_age_parka", t, A["needle_end"], 1400, h=460)''',
  '''        L.character(c, "ice_age_naked", t, 0, 520, y=850, h=400); L.character(c, "ice_age_cape", t, 0, 960, y=850, h=400); L.character(c, "ice_age_parka", t, A["needle_end"], 1400, y=850, h=400)''')
R('''put(c, LOUSE.resize((110, 130)), 1520, 640, popk(t, A["lice_end"]))''', '''L.cutout(c, LB, t, A["lice_end"], 1560, 520, 170, rot=12)''')
open(p, "w", encoding="utf-8").write(s); print("patched")
