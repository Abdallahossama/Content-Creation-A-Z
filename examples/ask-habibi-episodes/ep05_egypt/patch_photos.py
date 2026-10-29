"""Ep 5 v2 (user feedback 18 Oct 2026): proof photos in paper style + SFX, real-map (Blue Marble) switches."""
import shutil
p = "D:/why habibi/_pipeline/episodes/ep05_egypt/render_ep05.py"
shutil.copy(p, "D:/why habibi/_archive/render_ep05_v1b.py")
s = open(p, encoding="utf-8").read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)

R('''END = K.DUR\n''', '''END = K.DUR
PH = "D:/why habibi/_media/photos_2026-10-18/"; BME = ("D:/why habibi/_media/cutouts/bm_egypt_15_45_15_38.jpg", (15.0, 45.0, 15.0, 38.0))
PHOTOS = [  # (file, t0, t1, x, y, width, tilt, credit) - real photos as proof, shown while the voice talks about them
    ("eg_nile_night_iss.jpg", A["live"] + 1.2, A["nobody"] - 0.1, 450, 600, 640, -3, "the real thing: Egypt at night from the ISS · NASA"),
    ("eg_sand_sea_iss.jpg", A["western"] + 0.6, A["picture"] - 0.1, 1460, 620, 560, 3, "the Great Sand Sea from the ISS · NASA"),
    ("eg_cairo_aerial.jpg", A["capital"] + 2.2, A["ribbon"] - 0.1, 1430, 640, 600, 2, "Cairo · Pexels / Farid Abdel Aziz"),
    ("eg_nile_modis.jpg", A["cliffs"], A["qattara"] - 0.4, 1450, 640, 560, 3, "green vs sand, from space · NASA MODIS"),
    ("eg_menna_harvest.jpg", A["mud"] + 0.8, A["kemet"] - 0.1, W / 2, 620, 820, -2, "harvest, Tomb of Menna (facsimile) · The Met, CC0"),
    ("eg_aswan_dam_iss.jpg", A["dam"] + 0.6, A["nasser"] - 0.1, 1430, 620, 620, 3, "the Aswan High Dam from the ISS · NASA"),
    ("eg_lake_nasser_iss.jpg", A["nasser"] + 2.0, A["abusimbel"] - 0.1, 470, 640, 560, -3, "Lake Nasser from the ISS · NASA"),
    ("eg_feluccas.jpg", A["tamed"], A["agency"] - 0.1, 1430, 640, 600, 2, "the Nile at Aswan · Pexels / Eyup Sayar"),
    ("eg_new_capital.jpg", A["east"] + 1.5, A["westnd"] - 0.1, 1520, 600, 330, 3, "the New Capital · Pexels / Nada Mohamed"),
    ("eg_toshka_iss.jpg", A["toshka"] + 2.2, A["housing"] - 0.1, 1430, 640, 620, 3, "Toshka farms from the ISS · NASA"),
]
''')
R('''    if kemet_on: draw_nile(c, cam, black=True)\n''', '''    if kemet_on: draw_nile(c, cam, black=True)
    L.real_map(c, cam, max(L.fade(t, A["covers"] - 0.3, A["seven"] + 1.2, 0.6), L.fade(t, A["why_end"] - 0.2, A["smart"] - 0.2, 0.6)), *BME)   # real satellite map now and then
''')
R('''    L.subscribe_nudge(c, t, A["sub_mid"]''', '''    for f, t0, t1, x, y, w, rot, cr in PHOTOS: L.photo(c, PH + f, t, t0, t1, x=x, y=y, w=w, rot=rot, credit=cr)
    L.subscribe_nudge(c, t, A["sub_mid"]''')
R('''SFX += [("pop", A["sub_word"] + 0.25, -18)''', '''SFX += [("pop", ph[1], -19) for ph in PHOTOS]
SFX += [("pop", A["sub_word"] + 0.25, -18)''')
open(p, "w", encoding="utf-8").write(s); print("patched")
