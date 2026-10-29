"""Ep 8 v2 (user rules 18 Oct 2026): real dogs/objects instead of the 3D potato dog, drawn TV/pool/house/brain and emojis."""
import shutil
p = "D:/why habibi/_pipeline/episodes/ep08_dog/render_ep08.py"
shutil.copy(p, "D:/why habibi/_archive/render_ep08_drawn.py")
s = open(p, encoding="utf-8").read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)
R('''def dogpng(face): p = CUT + f"potato_dog_{face}.png"; return p if os.path.exists(p) else None''',
  '''def dogpng(face): return None          # the 3D potato dog is retired (user: real things only, no cartoons)
PC = {}
def pcard(name, w, rot=0):
    if not ph(name): return None
    if (name, w, rot) not in PC: PC[(name, w, rot)] = L._photo_card(ph(name), w, rot, None)
    return PC[(name, w, rot)]
def real(c, name, t, t0, x, y, w, rot=0, t1=None):
    if t >= t0 and (t1 is None or t < t1) and pcard(name, w, rot): put(c, pcard(name, w, rot), x, y, popk(t, t0))''')
R('''        put(c, D.brain(0, q=True).resize((620, 520), Image.LANCZOS), W / 2, 580, popk(t, 0.3))''', '''        real(c, "f8_brain.jpg", t, 0.3, W / 2, 600, 560, -2)''')
R('''        if dogpng("sideeye"): L.cutout(c, dogpng("sideeye"), t, A["recognizes"] + 0.5, W / 2, 620, 440)''', '''        real(c, "f8_brows.jpg", t, A["recognizes"] + 0.5, W / 2, 640, 640, 2)''')
R('''        if dogpng("fine"): L.cutout(c, dogpng("fine"), t, A["habibi"] + 0.6, 620, 640, 420)''', '''        real(c, "f8_dog_eyes.jpg", t, A["habibi"] + 0.6, 600, 620, 620, -3)''')
R('''        put(c, S(D.tv(t), 1.5), W / 2, 590, popk(t, A["flicker"] + 1.0))''', '''        real(c, "f8_tv.jpg", t, A["flicker"] + 1.0, W / 2, 600, 600, 2)''')
R('''            if dogpng("shocked"): L.cutout(c, dogpng("shocked"), t, A["dim"] + 0.4, W / 2, 600, 460)''', '''            real(c, "f8_dog_eyes.jpg", t, A["dim"] + 0.4, W / 2, 600, 620, -2)''')
R('''        for k, emo in enumerate(("😊", "😠")): put(c, emoji(emo, 260), W / 2 - 260 + k * 520, 560, popk(t, A["happy"] + k * 0.6))''',
  '''        real(c, "f8_man.jpg", t, A["happy"], W / 2, 600, 640, -2)''')
R('''        put(c, S(D.brain(0.6 if t >= A["cared"] else 0), 1.7), W / 2, 590, popk(t, A["brain2"]))''', '''        real(c, "f8_brain.jpg", t, A["brain2"], W / 2, 600, 560, 2)''')
R('''        put(c, S(D.pools(lit=ease((t - A["trillion"] - 1.0) / 0.6)), 1.45), W / 2, 600, popk(t, A["trillion"] + 0.3))''',
  '''        real(c, "f8_pool.jpg", t, A["trillion"] + 0.3, W / 2, 600, 760, -2)
        if t >= A["trillion"] + 1.0: put(c, pill("about 1 drop in 20 Olympic pools", 48, YEL), W / 2, 880 - 60, popk(t, A["trillion"] + 1.0))''')
R('''        put(c, S(D.scent_house(min(1, max(0, (t - A["fades"]) / 4.0))), 1.5), W / 2, 600, popk(t, A["horowitz"] + 0.3))''', '''        real(c, "f8_door.jpg", t, A["horowitz"] + 0.3, W / 2, 610, 620, -2)''')
R('''        put(c, S(D.brain(ease((t - A["brain3"] - 2.0) / 0.8)), 1.7), W / 2, 590, popk(t, A["brain3"]))''', '''        real(c, "f8_brain.jpg", t, A["brain3"], W / 2, 600, 560, -2)''')
R('''        if dogpng("sideeye"): L.cutout(c, dogpng("sideeye"), t, A["stressed"], 1560, 760, 360)''', '''        real(c, "f8_nose.jpg", t, A["stressed"], 1560, 760, 420, 3)''')
R('''        if dogpng("fine"): L.cutout(c, dogpng("fine"), t, A["evolve"] + 0.4, 1420, 760, 360)''', '''        real(c, "f8_eye_contact.jpg", t, A["evolve"] + 0.4, 1380, 700, 560, 3)''')
R('''        if dogpng("fine"): L.cutout(c, dogpng("fine"), t, A["toddlers"] + 0.4, 760, 760, 320)''', '''        real(c, "f8_park_dog.jpg", t, A["toddlers"] + 0.4, 760, 700, 460, -2)''')
R('''        if dogpng("sleepy"): L.cutout(c, dogpng("sleepy"), t, A["safe"], W / 2, 640, 440)''', '''        real(c, "f8_shoes.jpg", t, A["safe"], W / 2, 620, 360, 2)''')
# the toddler beat had the host potato standing in for an owner; real dog photo is enough
R('''        L.character(c, "host_cool", t, A["toddlers"], 400, y=900, h=420)\n''', '')
R('''        L.character(c, "host_cool", t, A["evolve"], 520, y=930, h=380)\n''', '')
open(p, "w", encoding="utf-8").write(s); print("patched")
