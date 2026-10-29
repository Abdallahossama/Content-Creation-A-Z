"""Hakawi-style (@7akawi-AA) colour thumbnails for The Last Hours (1280x720), 3 per video for the A/B test.
One full-colour cinematic real scene (only colour-graded), a real period photo ghosted in, 1-2 huge lines on solid black/yellow/red
blocks (Impact). Real images only; no women.
  uv run --no-project --with pillow --with numpy python thumbs_hakawi.py alcatraz|franklin|cooper|all"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
import lastkit as L
Image.MAX_IMAGE_PIXELS = None
NC = "D:/why habibi/_newchannel/"
TW, TH = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"
YEL, WHITE, RED = (255, 204, 0), (255, 255, 255), (190, 30, 30)

def src(ep, name):
    fs = glob.glob(NC + ep + "/media/" + name + "*")
    return Image.open(sorted(fs)[0]).convert("RGB")
def cover(im, w, h, cx=0.5, cy=0.5, z=1.0):
    s = max(w / im.width, h / im.height) * z; cw, ch = w / s, h / s
    x0 = min(max(cx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(cy * im.height - ch / 2, 0), im.height - ch)
    return im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
def grade(im, sat=1.2, contrast=1.12, teal=0.12, warm=0.08):
    a = np.asarray(im.convert("RGB"), np.float32) / 255; a = np.clip((a - 0.5) * contrast + 0.5, 0, 1)
    g = a.mean(2, keepdims=True); a = np.clip(g + (a - g) * sat, 0, 1)
    a = a + (1 - g) * teal * np.array([-0.6, 0.15, 0.35]) + g * warm * np.array([0.5, 0.15, -0.4])
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
def tint(im, col=(70, 110, 140), k=0.55, contrast=1.25):
    """a B&W archive photo given a cold cinematic duotone so it sits in a colour thumbnail"""
    g = np.asarray(im.convert("L"), np.float32) / 255; g = np.clip((g - 0.5) * contrast + 0.5, 0, 1)[..., None]
    c = np.array(col, np.float32) / 255; out = g * (1 - k) + g * c * k * 1.6
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
def vign(im, k=0.5):
    a = np.asarray(im.convert("RGB"), np.float32); yy, xx = np.mgrid[0:im.height, 0:im.width]
    r = np.sqrt(((xx - im.width / 2) / (im.width / 2)) ** 2 + ((yy - im.height / 2) / (im.height / 2)) ** 2)
    a *= np.clip(1 - k * np.clip(r - 0.45, 0, None) ** 1.5, 0, 1)[..., None]; return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
def fade_mask(w, h, left=0, right=0, top=0, bottom=0):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); m = np.ones((h, w), np.float32)
    if left: m *= np.clip(xx / left, 0, 1)
    if right: m *= np.clip((w - 1 - xx) / right, 0, 1)
    if top: m *= np.clip(yy / top, 0, 1)
    if bottom: m *= np.clip((h - 1 - yy) / bottom, 0, 1)
    return Image.fromarray((m * 255).astype(np.uint8))
def paste_faded(c, im, x, y, **fade):
    im = im.convert("RGBA"); m = fade_mask(im.width, im.height, **fade)
    a = np.minimum(np.asarray(im.split()[3]), np.asarray(m)); im.putalpha(Image.fromarray(a)); c.alpha_composite(im, (int(x), int(y)))
def block(c, s, x, y, size, fill=WHITE, bg=(0, 0, 0, 255), anchor="l", pad=(24, 10)):
    f = L.font(IMPACT, size); bb = f.getbbox(s); w, h = bb[2] - bb[0], bb[3] - bb[1]
    x0 = x if anchor == "l" else (x - w / 2 - pad[0] if anchor == "m" else x - w - 2 * pad[0])
    d = ImageDraw.Draw(c); d.rectangle((x0, y - h / 2 - pad[1], x0 + w + 2 * pad[0], y + h / 2 + pad[1]), fill=bg)
    d.text((x0 + pad[0] - bb[0], y - h / 2 - bb[1]), s, font=f, fill=fill)
def ellipse(c, box, width=11, col=(230, 30, 30)):
    import math
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = [(cx + rx * (1 + 0.035 * math.sin(i / 9)) * math.cos(-2.3 + 2 * math.pi * 1.1 * i / 120), cy + ry * (1 + 0.035 * math.cos(i / 7)) * math.sin(-2.3 + 2 * math.pi * 1.1 * i / 120)) for i in range(121)]
    ImageDraw.Draw(c).line(pts, fill=col + (255,), width=width, joint="curve")
def card(im, w, rot=-2, border=10):
    return L.print_card(im.convert("RGB"), w, border=border, rot=rot)

# ------------------------------------------------------------------ ALCATRAZ
def alc_A():   # dusk island + the three men ghosted: WHERE DID THEY GO?
    c = grade(cover(src("01_alcatraz", "pexels_3488039"), TW, TH, cx=0.5, cy=0.52, z=1.15), sat=1.35, teal=0.08, warm=0.16)
    c = vign(c, 0.5)
    faces = [src("01_alcatraz", n) for n in ("mug_frank_morris", "mug_john_anglin", "mug_clarence_anglin")]
    for i, (f, rot) in enumerate(zip(faces, (-5, 2, -3))):                  # the three real mugshots as prints over the island
        f = f.crop((int(f.width * 0.06), int(f.height * 0.02), int(f.width * 0.94), int(f.height * 0.72)))
        k = card(tint(f, col=(150, 160, 170), k=0.25), 250, rot=rot, border=9)
        c.alpha_composite(k, (int(TW - 3 * 235 - 115 + i * 235), 300 + (i % 2) * 30))
    block(c, "WHERE DID", 40, 95, 120)
    block(c, "THEY GO?", 40, 225, 120, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def alc_B():   # the real 1962 colour photo of the dummy head in the bed: IT WAS A DUMMY
    c = grade(cover(src("01_alcatraz", "B5_nps_dummy_morris"), TW, TH, cx=0.55, cy=0.45, z=1.08), sat=1.1, teal=0.06, warm=0.10)
    c = vign(c, 0.55)
    block(c, "IT WAS", 40, 520, 130)
    block(c, "A DUMMY.", 40, 655, 130, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def alc_C():   # the island from the water + the real FBI wanted poster: STILL WANTED
    c = grade(cover(src("01_alcatraz", "pexels_17765343"), TW, TH, cx=0.5, cy=0.5, z=1.05), sat=1.2, teal=0.22, warm=0.04)
    c = vign(c, 0.5)
    poster = src("01_alcatraz", "A8_wanted_john_anglin_nps"); poster = poster.crop((0, 0, poster.width, int(poster.height * 0.93)))
    k = card(poster, 560, rot=4); c.alpha_composite(k, (TW - k.width - 20, TH - k.height + 40))
    block(c, "STILL", 40, 120, 140, fill=WHITE)
    block(c, "WANTED", 40, 270, 140, fill=WHITE, bg=RED + (255,))
    return c

# ------------------------------------------------------------------ FRANKLIN
def fr_A():   # icebergs in a black sea + Franklin ghosted: 129 MEN / GONE
    c = grade(cover(src("03_franklin", "G3_"), TW, TH, cx=0.5, cy=0.62, z=1.1), sat=1.3, teal=0.14, warm=0.04)
    c = vign(c, 0.45)
    fr = src("03_franklin", "A1_"); fr = fr.crop((int(fr.width * 0.30), int(fr.height * 0.18), int(fr.width * 0.80), int(fr.height * 0.66)))
    t = tint(fr, k=0.55).resize((470, int(470 * fr.height / fr.width)), Image.LANCZOS)
    t.putalpha(Image.fromarray((np.asarray(fade_mask(t.width, t.height, left=90, right=40, top=40, bottom=160)) * 0.85).astype(np.uint8)))
    c.alpha_composite(t, (TW - t.width - 10, 0))
    block(c, "129 MEN", 40, 150, 150, fill=YEL)
    block(c, "GONE", 40, 310, 130, fill=WHITE, bg=RED + (255,))
    return c
def fr_B():   # the real 1847/1848 note on a blue iceberg sea: "ALL WELL"?
    c = grade(cover(src("03_franklin", "G6_"), TW, TH, cx=0.5, cy=0.6, z=1.05), sat=1.35, teal=0.12, warm=0.03)
    c = vign(c, 0.4)
    note = src("03_franklin", "B1_"); NOTE_CROP = (380 / 1280, 560 / 2035, 1240 / 1280, 1044 / 2035)
    n = note.crop(tuple(int(v * s) for v, s in zip(NOTE_CROP, (note.width, note.height, note.width, note.height))))
    k = card(n, 640, rot=-3); c.alpha_composite(k, (TW - k.width - 30, 150))
    block(c, "\u201cALL", 40, 200, 150)
    block(c, "WELL\u201d?", 40, 370, 150, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def fr_C():   # pack ice + the 1859 engraving of the ships in the ice: TRAPPED IN THE ICE
    c = grade(cover(src("03_franklin", "G4_"), TW, TH, cx=0.5, cy=0.5), sat=1.0, teal=0.30, warm=0.05)
    c = vign(c, 0.45)
    eng = src("03_franklin", "D4_"); eng = eng.crop((0, int(eng.height * 0.15), eng.width, int(eng.height * 0.85)))
    t = tint(eng, k=0.5).resize((520, int(520 * eng.height / eng.width)), Image.LANCZOS)
    t.putalpha(Image.fromarray((np.asarray(fade_mask(t.width, t.height, left=120, right=20, top=30, bottom=30)) * 0.8).astype(np.uint8)))
    c.alpha_composite(t, (TW - t.width, (TH - t.height) // 2))
    block(c, "TRAPPED", 40, 200, 150)
    block(c, "FOR 588 DAYS", 40, 360, 110, fill=(0, 0, 0), bg=YEL + (255,))
    return c

# ------------------------------------------------------------------ COOPER
def co_A():   # blood-red 1973 sky over Portland airport, a jet + the FBI sketch: WHO WAS HE?
    c = grade(cover(src("04_dbcooper", "C3_"), TW, TH, cx=0.42, cy=0.45, z=1.15), sat=1.1, teal=0.02, warm=0.06)
    c = vign(c, 0.5)
    sk = src("04_dbcooper", "A10_"); sk = sk.crop((int(sk.width * 0.05), int(sk.height * 0.04), int(sk.width * 0.95), int(sk.height * 0.82)))
    t = sk.convert("RGBA").resize((470, int(470 * sk.height / sk.width)), Image.LANCZOS)
    t.putalpha(Image.fromarray((np.asarray(fade_mask(t.width, t.height, left=100, right=20, top=20, bottom=120)) * 0.92).astype(np.uint8)))
    c.alpha_composite(t, (TW - t.width - 10, TH - t.height + 20))
    block(c, "WHO WAS", 40, 470, 130)
    block(c, "HE?", 40, 610, 130, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def co_B():   # the real 1980 money find, colour: $200,000 / NEVER FOUND
    c = grade(cover(src("04_dbcooper", "A2_"), TW, TH, cx=0.5, cy=0.5, z=1.05), sat=1.25, teal=0.08, warm=0.10)
    c.alpha_composite(Image.new("RGBA", (TW, TH), (0, 0, 0, 70))); c = vign(c, 0.6)
    block(c, "$200,000", 40, 130, 160, fill=YEL)
    block(c, "NEVER FOUND", 40, 300, 130, fill=WHITE, bg=RED + (255,))
    return c
def co_C():   # jet landing at night + his real ticket: HE JUMPED.
    c = grade(cover(src("04_dbcooper", "B3_"), TW, TH, cx=0.62, cy=0.4, z=1.0), sat=1.2, teal=0.06, warm=0.08)
    c = vign(c, 0.45)
    tk = src("04_dbcooper", "A12_"); tk = tk.crop((int(tk.width * 0.04), int(tk.height * 0.12), int(tk.width * 0.62), int(tk.height * 0.66)))
    k = card(tk, 520, rot=-4); c.alpha_composite(k, (30, TH - k.height - 10))
    block(c, "HE JUMPED", 40, 95, 120)
    block(c, "WITH $200,000", 40, 225, 100, fill=(0, 0, 0), bg=YEL + (255,))
    return c


# ------------------------------------------------------------------ v2 A/C: one strong real image filling the frame (like the B ones)
def side_fill(im, w, h, cx=0.5, cy=0.5, z=1.0, right=True, frac=0.62, dark=0.55):
    """subject on one side at full height; the rest is the same image blurred and darkened (no empty borders)"""
    bg = cover(im, w, h, cx, cy, 1.3).filter(ImageFilter.GaussianBlur(28)).convert("RGBA")
    bg.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, int(255 * dark))))
    fw = int(w * frac); fg = cover(im, fw, h, cx, cy, z).convert("RGBA")
    m = fade_mask(fw, h, left=160 if right else 0, right=0 if right else 160)
    fg.putalpha(m); bg.alpha_composite(fg, (w - fw if right else 0, 0)); return bg
def alc_A2():   # the real 1962 colour photo in the utility corridor behind the cells: THE WAY OUT
    im = src("01_alcatraz", "C2_nps_utility_corridor"); im = im.crop((int(im.width * 0.02), int(im.height * 0.02), int(im.width * 0.98), int(im.height * 0.95)))
    c = grade(cover(im, TW, TH, cx=0.5, cy=0.42, z=1.0), sat=1.15, teal=0.06, warm=0.10); c = vign(c, 0.55)
    block(c, "THE WAY", TW - 40, 470, 130, anchor="r")
    block(c, "OUT", TW - 40, 610, 130, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c
def alc_C2():   # the whole real FBI wanted poster (header + both faces) above a text strip: 64 YEARS. NEVER FOUND.
    im = src("01_alcatraz", "A8_wanted_john_anglin_nps"); im = im.crop((int(im.width * 0.03), int(im.height * 0.02), int(im.width * 0.97), int(im.height * 0.735)))
    a = np.asarray(im, np.float32) / 255; a = a * np.array([1.0, 0.93, 0.80]); im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    c = cover(im, TW, TH, 0.5, 0.5, 1.3).filter(ImageFilter.GaussianBlur(26)).convert("RGBA")
    c.alpha_composite(Image.new("RGBA", (TW, TH), (0, 0, 0, 150)))
    ph = 600; pw = int(ph * im.width / im.height); p_ = im.resize((pw, ph), Image.LANCZOS).convert("RGBA")
    c.alpha_composite(p_, ((TW - pw) // 2, 0)); c = vign(c, 0.35)
    block(c, "64 YEARS.", 95, 662, 88, fill=YEL)
    block(c, "NEVER FOUND.", 500, 662, 88, fill=WHITE, bg=RED + (255,))
    return c
def fr_A2():   # Franklin's own 1845 daguerreotype in its red velvet case: 129 MEN / NONE CAME HOME
    im = src("03_franklin", "A1_")
    c = side_fill(im, TW, TH, cx=0.5, cy=0.42, z=1.0, right=True, frac=0.55); c = vign(c, 0.45)
    block(c, "129 MEN", 40, 260, 150, fill=YEL)
    block(c, "NONE CAME", 40, 430, 110, fill=WHITE, bg=RED + (255,))
    block(c, "HOME", 40, 560, 110, fill=WHITE, bg=RED + (255,))
    return c
def fr_C2():   # the 1860 engraving of Erebus and Terror in the ice, moonlit: TRAPPED FOR 588 DAYS
    im = src("03_franklin", "D4_"); im = im.crop((0, int(im.height * 0.36), im.width, int(im.height * 0.36 + im.width * 9 / 16)))
    c = tint(im, col=(90, 150, 190), k=0.75, contrast=1.3).resize((TW, TH), Image.LANCZOS); c = vign(c, 0.5)
    block(c, "TRAPPED", 40, 470, 140)
    block(c, "FOR 588 DAYS", 40, 620, 110, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def co_A2():   # the FBI's 1973 colour sketch, face filling the right side: WHO WAS HE?
    im = src("04_dbcooper", "A10_"); im = im.crop((0, int(im.height * 0.03), im.width, int(im.height * 0.78)))
    c = side_fill(im, TW, TH, cx=0.5, cy=0.45, z=1.0, right=True, frac=0.58, dark=0.6)
    a = np.asarray(c.convert("RGB"), np.float32); a[..., 0] *= 1.08; a[..., 2] *= 0.9; c = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    c = vign(c, 0.45)
    block(c, "WHO WAS", 40, 300, 150)
    block(c, "HE?", 40, 470, 150, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def co_C2():   # May 1973: a 727 seen from directly below, rear stairs circled: HE JUMPED FROM HERE
    im = src("04_dbcooper", "B2_"); im = im.crop((0, int(im.height * 0.15), im.width, int(im.height * 0.525)))
    c = grade(im.resize((TW, TH), Image.LANCZOS), sat=1.25, teal=0.08, warm=0.06); c = vign(c, 0.4)
    ellipse(c, (545, 575, 700, 695), width=11)
    block(c, "HE JUMPED", TW - 30, 200, 120, anchor="r")
    block(c, "FROM HERE", TW - 30, 350, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c
def co_D():   # user's mix of A + C (26 Oct): the sketch face close on the right, the 727 from below on the left, stairs circled
    jet = src("04_dbcooper", "B2_").crop((241, 580, 1507, 1882))          # nose top-left, rear stairs (857, 1271) -> (341, 382)
    c = Image.new("RGBA", (TW, TH)); c.alpha_composite(grade(jet.resize((700, TH), Image.LANCZOS), sat=1.25, teal=0.08, warm=0.06))
    sk = src("04_dbcooper", "A10_").crop((0, 30, 506, 600))
    f = cover(sk, 720, TH, cx=0.5, cy=0.45).convert("RGBA")
    a = np.asarray(f.convert("RGB"), np.float32); a[..., 0] *= 1.08; a[..., 2] *= 0.9; f = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    f.putalpha(fade_mask(720, TH, left=160)); c.alpha_composite(f, (TW - 720, 0))
    c = vign(c, 0.45)
    ellipse(c, (276, 330, 406, 432), width=10)
    block(c, "WHO WAS", 40, 520, 120)
    block(c, "HE?", 40, 650, 120, fill=(0, 0, 0), bg=YEL + (255,))
    return c

SETS ={"alcatraz": ("01_alcatraz/export/thumbs_colour/", [("A_THE_WAY_OUT", alc_A2), ("B_IT_WAS_A_DUMMY", alc_B), ("C_64_YEARS", alc_C2)]),
        "franklin": ("03_franklin/export/thumbnails_colour/", [("A_NONE_CAME_HOME", fr_A2), ("B_ALL_WELL", fr_B), ("C_TRAPPED_588_DAYS", fr_C2)]),
        "cooper": ("04_dbcooper/export/thumbnails_colour/", [("A_WHO_WAS_HE", co_A2), ("B_NEVER_FOUND", co_B), ("C_JUMPED_FROM_HERE", co_C2)]),
        "cooper_mix": ("04_dbcooper/export/thumbnails_colour/", [("D_WHO_WAS_HE_JET", co_D)])}
def make(key):
    out, items = SETS[key]; out = NC + out; os.makedirs(out, exist_ok=True)
    for name, fn in items:
        im = fn().convert("RGB"); im.save(out + name + ".png"); im.save(out + name + "_upload.jpg", quality=92)
    if len(items) != 3: print(key, "->", out); return              # single extra thumbnail: keep the set's 3-up sheet
    sheet =Image.new("RGB", (TW, TH * 3 // 2 + 20), (30, 30, 30))
    for i, (n, _) in enumerate(items):
        sheet.paste(Image.open(out + n + ".png").resize((TW // 2 - 10, TH // 2 - 6)), ((i % 2) * (TW // 2 + 10), (i // 2) * (TH // 2 + 10)))
    for i, (n, _) in enumerate(items):
        s_ = Image.open(out + n + ".png").resize((246, 138)); sheet.paste(s_, (TW // 2 + 20 + (i % 2) * 205, TH // 2 + 30 + (i // 2) * 160))
    sheet.save(out + "_sheet.png"); print(key, "->", out)
if __name__ == "__main__":
    for k in (SETS if sys.argv[1] == "all" else [sys.argv[1]]): make(k)
