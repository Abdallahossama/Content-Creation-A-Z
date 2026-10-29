"""Thumbnails v3 for Ep 5-9 (user, 18 Oct 2026): REAL photos only, men only (no women ever), no cartoons, 3 truly different layouts
per video. Layout families: SPLIT (before/after or packed/empty, torn seam, arrow) · PROOF (real object/photo full-bleed + marker loop
or zoom bubble) · FACE (a real man reacting next to a real object). Words: 1-3, never the title's words.
  python thumbs_v3.py [egypt|clothes|fun|dog|walk|all]"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import cinekit as CK, marker as MK, dogvision as DV
from thumbkit import W, H
M = "D:/why habibi/_media/"; PT = M + "photos_thumbs/"; P5 = M + "photos_2026-10-18/"; P7 = M + "photos_ep07/"; P8 = M + "photos_ep08/"; P9 = M + "photos_ep09/"; CUT = M + "cutouts/"
SHOCK, SHOCK2, PUZZ = CUT + "person_shocked_man.png", CUT + "person_shocked_man2.png", CUT + "person_puzzled_man.png"

def fill(path, w=W, h=H, focus=(0.5, 0.5), sat=1.15, con=1.1, bright=1.0, zoom=1.0):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height) * zoom; im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); im = im.crop((x, y, x + w, y + h))
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con); return ImageEnhance.Brightness(im).enhance(bright).convert("RGBA")
def man(c, path, h, x, y_bottom=None, rot=0):
    s = MK.sticker(path, h, border=10, rot=rot); MK.place(c, s, x, (y_bottom or H + 60) - s.height // 2); return s
def seam(c, x, seed=4):
    r = np.random.default_rng(seed); pts = [(x + r.uniform(-14, 14), y) for y in range(-10, H + 20, 22)]
    left = [(p[0] - 9, p[1]) for p in pts]; right = [(p[0] + 9, p[1]) for p in pts[::-1]]
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(a + 8, b) for a, b in left + right], fill=(0, 0, 0, 140)); c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(c).polygon(left + right, fill=(248, 244, 232, 255))
def split(left, right, lw=W // 2):
    c = Image.new("RGBA", (W, H)); c.alpha_composite(left.crop((0, 0, lw, H)), (0, 0)); c.alpha_composite(right.crop((0, 0, W - lw, H)), (lw, 0)); seam(c, lw); return c
def card(path, w, rot=0, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS); bd = 12
    cd = Image.new("RGBA", (im.width + 2 * bd, im.height + 2 * bd), (250, 247, 240, 255)); cd.paste(im, (bd, bd)); return cd.rotate(rot, Image.BICUBIC, expand=True)
def bubble(c, src, box, center, r=160):
    crop = src.crop(box).resize((2 * r, 2 * r), Image.LANCZOS); m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    b = Image.new("RGBA", (2 * r + 24, 2 * r + 24), (0, 0, 0, 0)); ImageDraw.Draw(b).ellipse((0, 0, 2 * r + 23, 2 * r + 23), fill=(255, 255, 255, 255)); crop.putalpha(m); b.alpha_composite(crop, (12, 12))
    MK.strokes(c, MK.arrow_path(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), center, bend=0.1, head=0, seed=2), MK.WHITE, 8, seed=2)
    c.alpha_composite(b, (int(center[0] - r - 12), int(center[1] - r - 12)))
def strike(c, text, x, y, size=150):
    w = CK.grad_word(text, size, top=(255, 255, 255), bot=(220, 220, 220)); MK.place(c, w, x, y)
    MK.strokes(c, [np.array([(x - w.width / 2 + 10, y + 10), (x + w.width / 2 - 10, y - 20)])], MK.RED, 22, seed=7)
def glowed(c, im, x, y, col, r=40):
    g = Image.new("RGBA", c.size, (0, 0, 0, 0)); a = im.split()[3].filter(ImageFilter.MaxFilter(9)); s = Image.new("RGBA", im.size, col + (255,)); s.putalpha(a)
    g.alpha_composite(s, (int(x - im.width / 2), int(y - im.height / 2))); c.alpha_composite(g.filter(ImageFilter.GaussianBlur(r))); MK.place(c, im, x, y)
def save(c, folder, name):
    os.makedirs(folder, exist_ok=True); CK.corner_vignette(c); c.convert("RGB").save(folder + name + ".png"); print(folder + name + ".png"); return c
def sheet(folder, names):
    ims = [Image.open(folder + n + ".png") for n in names]; sh = Image.new("RGB", (W * 3 // 2 + 20, H // 2), (20, 20, 20))
    for k, im in enumerate(ims): sh.paste(im.resize((W // 2, H // 2)), (k * (W // 2 + 10), 0))
    sh.save(folder + "_sheet_v3.png"); print(folder + "_sheet_v3.png")

def real_flag(c, x, y, h=230, label="EGYPT", size=68):
    """the real Egyptian flag photo (Pexels 13884502), cut out, as a white-edged sticker, the word under it"""
    st = MK.sticker(CUT + "flag_egypt_real.png", h, border=8, rot=0)
    sh_ = Image.new("RGBA", c.size, (0, 0, 0, 0)); s_ = Image.new("RGBA", st.size, (0, 0, 0, 255)); s_.putalpha(st.split()[3].point(lambda v: v * 120 // 255))
    sh_.alpha_composite(s_, (int(x - st.width / 2 + 8), int(y - st.height / 2 + 10))); c.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(7)))
    MK.place(c, st, x, y)
    word = CK.grad_word(label, size); MK.place(c, word, x + 8, y + st.height / 2 + word.height / 2 - 14)

def egypt_flag(c, x, y, w=240, label="EGYPT", size=66):
    """the real Egyptian flag (Wikimedia, public domain) with a soft wave, white border and shadow, the word under it"""
    fl = Image.open(CUT + "flag_egypt.png").convert("RGBA"); h = int(fl.height * w / fl.width); fl = fl.resize((w, h), Image.LANCZOS)
    a = np.pad(np.asarray(fl).astype(np.float32), ((8, 8), (0, 0), (0, 0))); out = np.zeros_like(a); h = a.shape[0]          # transparent margin: no wrap-around
    for xx in range(w):                                                         # gentle wave + light/shade
        dy = 6 * np.sin(xx / w * 2 * np.pi * 1.2); sh = 1 + 0.10 * np.cos(xx / w * 2 * np.pi * 1.2)
        col = np.roll(a[:, xx], int(dy), axis=0); col[..., :3] *= sh; out[:, xx] = col
    fl = Image.fromarray(out.clip(0, 255).astype(np.uint8)); bd = 8
    card = Image.new("RGBA", (w + 2 * bd, h + 2 * bd + 12), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle((0, 0, w + 2 * bd - 1, h + 2 * bd + 11), 10, fill=(255, 255, 255, 255))
    card.alpha_composite(fl, (bd, bd + 6)); card = card.rotate(-3, Image.BICUBIC, expand=True)
    sh_ = Image.new("RGBA", c.size, (0, 0, 0, 0)); s_ = Image.new("RGBA", card.size, (0, 0, 0, 150)); s_.putalpha(card.split()[3].point(lambda v: v * 150 // 255))
    sh_.alpha_composite(s_, (int(x - card.width / 2 + 8), int(y - card.height / 2 + 10))); c.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(6)))
    MK.place(c, card, x, y)
    word = CK.grad_word(label, size); MK.place(c, word, x, y + card.height / 2 + word.height / 2 - 6)

def egypt_banner(c, x, y, size=96):
    """'EGYPT' on a red-white-black flag-stripe banner, tilted, with a hard shadow"""
    f = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", size); tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength("EGYPT", font=f))
    bw, bh = tw + 90, int(size * 1.35); b = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((14, 14, bw + 14, bh + 14), 18, fill=(0, 0, 0, 160))
    for k, col in enumerate(((206, 17, 38), (255, 255, 255), (20, 20, 20))): d.rectangle((4, 4 + k * bh / 3, bw + 4, 4 + (k + 1) * bh / 3), fill=col + (255,))
    d.rounded_rectangle((4, 4, bw + 4, bh + 4), 18, outline=(14, 10, 8, 255), width=6)
    d.text((bw / 2 + 4, bh / 2 + 4), "EGYPT", font=f, fill=(255, 206, 60), anchor="mm", stroke_width=7, stroke_fill=(14, 10, 8))
    MK.place(c, b.rotate(-4, Image.BICUBIC, expand=True), x, y)

# ---------------------------------------------------------------- Ep 5 Egypt (A = the night map)
def egypt():
    F = "D:/why habibi/5th video/export/thumbnails/"
    L_ = fill(PT + "th_pyramids_cairo.jpg", W // 2 + 40, H, (0.45, 0.4), sat=1.2, con=1.15, zoom=1.15)
    R_ = fill(PT + "th_dunes.jpg", W // 2, H, (0.5, 0.5), sat=1.5, con=1.2, bright=1.15); R_.alpha_composite(Image.new("RGBA", R_.size, (255, 180, 80, 50)))
    c = Image.new("RGBA", (W, H)); c.alpha_composite(L_.crop((0, 0, W // 2, H)), (0, 0)); c.alpha_composite(R_, (W // 2, 0)); seam(c, W // 2)
    CK.words(c, ["PACKED"], size=128, x=20, y=20, rot=-3); CK.words(c, ["EMPTY"], size=128, x=W // 2 + 150, y=20, rot=-3)
    MK.strokes(c, MK.circle_path(1020, 520, 170, 100, seed=3), MK.RED, 12, seed=3)
    man(c, SHOCK, 400, W // 2 - 10, H + 40, rot=2); real_flag(c, W // 2 + 5, 140, 262, size=60); save(c, F, "B_PACKED_EMPTY")
    c = fill(P5 + "eg_nile_modis.jpg", W, H, (0.42, 0.55), sat=1.35, con=1.2, bright=1.1, zoom=1.35)
    MK.strokes(c, MK.circle_path(650, 370, 120, 345, seed=6, tilt=-7), MK.RED, 14, seed=6)
    CK.words(c, ["EGYPT:", "95% HERE"], size=118, x=690, y=20)
    man(c, PUZZ, 440, W - 150, H + 40, rot=-2); save(c, F, "C_95_HERE")
    sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep05_egypt"); import thumbs_ep05 as T5
    T5.make("A_95_EMPTY", ["EGYPT", "95% EMPTY"], "shocked", size=128)
    sheet(F, ["A_95_EMPTY", "B_PACKED_EMPTY", "C_95_HERE"])

# ---------------------------------------------------------------- Ep 6 clothes
def clothes():
    F = "D:/why habibi/6th video/export/thumbnails/"
    L_ = fill(PT + "th_glacier.jpg", W // 2, H, (0.5, 0.5), sat=1.2, con=1.15); R_ = fill(P5 + "cl_otzi_shoe.jpg", W // 2, H, (0.45, 0.5), sat=1.25, con=1.15, bright=1.1)
    c = split(L_, R_); CK.words(c, ["WHY", "CLOTHES?"], size=150, x=W // 2 - 330, y=8, rot=-2)
    MK.strokes(c, MK.arrow_path((330, 560), (930, 560), bend=-0.2, head=50, seed=8), MK.RED, 20, seed=8)
    man(c, PUZZ, 400, W // 2 + 10, H + 40); save(c, F, "A_WHY_CLOTHES")
    c = fill(PT + "th_fur.jpg", W, H, (0.5, 0.5), sat=1.15, con=1.2, bright=0.9)
    lou = Image.open(CUT + "louse_body.png").convert("RGBA"); lou = lou.resize((int(lou.width * 600 / lou.height), 600), Image.LANCZOS).rotate(-10, Image.BICUBIC, expand=True)
    glowed(c, lou, 470, 390, (255, 230, 150), r=36); CK.words(c, ["THE LOUSE", "KNEW"], size=130, x=640, y=20)
    man(c, SHOCK2, 470, W - 200, H + 40); save(c, F, "B_THE_LOUSE_KNEW")
    src = fill(P5 + "cl_eyed_needle.jpg", W, H, (0.5, 0.5), sat=1.05, con=1.15, bright=1.1, zoom=1.0)
    c = src.copy(); sw = Image.open(P5 + "cl_eyed_needle.jpg").size; k = max(W / sw[0], H / sw[1]); ox = (sw[0] * k - W) / 2; oy = (sw[1] * k - H) / 2
    box = tuple(int(v) for v in (1180 * k - ox, 860 * k - oy, 1320 * k - ox, 1230 * k - oy))
    MK.strokes(c, MK.circle_path((box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 70, 140, seed=4), MK.RED, 12, seed=4)
    bubble(c, src, (box[0] - 20, box[1], box[2] + 20, box[1] + 160), (1060, 200), r=150)
    CK.words(c, ["40,000", "YEARS"], size=140, x=30, y=10); man(c, SHOCK, 380, 170, H + 40, rot=-3); save(c, F, "C_40000_YEARS")
    sheet(F, ["A_WHY_CLOTHES", "B_THE_LOUSE_KNEW", "C_40000_YEARS"])

# ---------------------------------------------------------------- Ep 7 ancient fun
def fun():
    F = "D:/why habibi/7th video/export/thumbnails/"
    c = CK.backdrop(CK.BLUE, burst=(560, 380)); b = card(P7 + "f7_ur_board.jpg", 780, -6, crop=(0, 200, 1920, 1529)); glowed(c, b, 470, 420, (255, 210, 120), r=34)
    CK.words(c, ["4600", "YEARS"], size=150, x=20, y=10); man(c, SHOCK2, 520, W - 200, H + 40); save(c, F, "A_4600_YEARS")
    c = CK.backdrop(CK.RED, burst=(420, 380)); t_ = card(P7 + "f7_tablet.jpg", 520, 8); glowed(c, t_, 380, 470, (255, 210, 120), r=34)
    CK.words(c, ["OLDEST", "JOKE"], size=150, x=40, y=10); man(c, SHOCK, 560, W - 230, H + 60, rot=3)
    puff = Image.new("RGBA", (260, 200), (0, 0, 0, 0)); ImageDraw.Draw(puff).text((10, 10), "💨", font=ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 150), embedded_color=True)
    c.alpha_composite(puff.rotate(-10, expand=True), (600, 470)); save(c, F, "B_OLDEST_JOKE")
    c = fill(P7 + "f7_cave_animal.jpg", W, H, (0.5, 0.45), sat=1.3, con=1.2, bright=1.05, zoom=1.1)
    MK.strokes(c, MK.circle_path(560, 380, 330, 240, seed=5), MK.RED, 14, seed=5)
    CK.words(c, ["BEFORE", "WIFI"], size=150, x=W - 520, y=10); man(c, PUZZ, 430, W - 180, H + 40); save(c, F, "C_BEFORE_WIFI")
    sheet(F, ["A_4600_YEARS", "B_OLDEST_JOKE", "C_BEFORE_WIFI"])

# ---------------------------------------------------------------- Ep 8 dog
def dog():
    F = "D:/why habibi/8th video/export/thumbnails/"
    src = Image.open(P5 + "th_shocked_man.jpg").convert("RGB"); z = 1.25 * H / src.height; src = src.resize((int(src.width * z), int(src.height * z)), Image.LANCZOS)
    fx = max(0, int(src.width * 0.50 - W / 2)); fy = max(0, min(src.height - H, int(src.height * 0.30 - H / 2))); base = ImageEnhance.Contrast(src.crop((fx, fy, fx + W, fy + H))).enhance(1.1)
    dv = DV.dog_view(base, blur=5.0); c = base.copy(); c.paste(dv.crop((W // 2, 0, W, H)), (W // 2, 0)); c = c.convert("RGBA"); ImageDraw.Draw(c).line((W // 2, 0, W // 2, H), fill=(255, 255, 255), width=10)
    for txt, x in (("YOU", W // 2 - 110), ("YOUR DOG", W // 2 + 170)): MK.place(c, MK.hand(txt, 64, MK.WHITE, rot=0), x, H - 70)
    CK.words(c, ["YOU, TO", "A DOG"], size=130, x=20, y=10); save(c, F, "A_YOU_TO_A_DOG")
    c = fill(P8 + "f8_nose.jpg", W, H, (0.45, 0.5), sat=1.2, con=1.2, bright=1.05)
    MK.strokes(c, MK.circle_path(610, 300, 240, 170, seed=6), MK.RED, 14, seed=6); CK.words(c, ["300", "MILLION"], size=140, x=W - 600, y=10)
    man(c, SHOCK2, 420, W - 200, H + 40); save(c, F, "B_300_MILLION")
    c = fill(P8 + "f8_puppy_eyes.jpg", W, H, (0.5, 0.38), sat=1.2, con=1.15, bright=1.05)
    for p0, p1, sd in (((300, 160), (530, 300), 3), ((1000, 150), (770, 290), 4)): MK.strokes(c, MK.arrow_path(p0, p1, bend=0.2, head=40, seed=sd), MK.YEL, 14, seed=sd)
    CK.words(c, ["IT'S A", "TRICK?"], size=140, x=30, y=330); man(c, PUZZ, 400, W - 170, H + 40); save(c, F, "C_ITS_A_TRICK")
    sheet(F, ["A_YOU_TO_A_DOG", "B_300_MILLION", "C_ITS_A_TRICK"])

# ---------------------------------------------------------------- Ep 9 walking
def walk():
    F = "D:/why habibi/9th video/export/thumbnails/"
    c = fill(P9 + "f9_feet.jpg", W, H, (0.5, 0.6), sat=1.15, con=1.15)
    strike(c, "10,000", 380, 170, 150); CK.words(c, ["7,000"], size=190, x=120, y=260, rot=-4)
    man(c, SHOCK2, 500, W - 200, H + 40); save(c, F, "A_10000_MYTH")
    c = CK.backdrop(CK.BLUE, burst=(460, 380)); x_ = Image.open(P9 + "f9_gray_hippocampus.png").convert("L")
    xr = Image.eval(x_, lambda v: 255 - v); a = np.asarray(xr, np.float32) / 255; rgb = np.stack([10 + a * 120, 20 + a * 200, 40 + a * 255], 2).clip(0, 255).astype(np.uint8)
    brain = Image.fromarray(rgb).convert("RGBA"); brain.putalpha(Image.fromarray((a * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)))
    brain = brain.resize((760, int(brain.height * 760 / brain.width)), Image.LANCZOS); glowed(c, brain, 470, 420, (90, 180, 255), r=40)
    CK.words(c, ["+2%", "BRAIN"], size=150, x=W - 640, y=10); man(c, PUZZ, 400, W - 170, H + 40); save(c, F, "B_BRAIN_PLUS_2")
    L_ = fill(P9 + "f9_desk.jpg", W // 2, H, (0.55, 0.5), sat=1.1, con=1.15); R_ = fill(P9 + "f9_park.jpg", W // 2, H, (0.5, 0.5), sat=1.25, con=1.1, bright=1.1)
    c = split(L_, R_); CK.words(c, ["3 DAYS", "OFF?"], size=140, x=20, y=10)
    MK.strokes(c, MK.arrow_path((W - 330, 560), (420, 560), bend=0.2, head=50, seed=9), MK.RED, 20, seed=9); save(c, F, "C_3_DAYS_OFF")
    sheet(F, ["A_10000_MYTH", "B_BRAIN_PLUS_2", "C_3_DAYS_OFF"])

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in (("egypt", egypt), ("clothes", clothes), ("fun", fun), ("dog", dog), ("walk", walk)):
        if which in (name, "all"): fn()
