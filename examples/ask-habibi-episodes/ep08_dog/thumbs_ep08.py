"""Ep 8 thumbnails (3 genuinely different compositions):
  A  SPLIT   a real face, half normal / half 'dog vision' (our dichromat + blur filter), "YOU, TO A DOG"
  B  MACRO   a real dog nose full-bleed (Pexels), red marker loop, potato dog sticker, "300 MILLION"
  C  FACE    puppy eyes full-bleed (Pexels), marker arrows to the eyebrows, boss Batata side-eye, "IT'S A TRICK?"
-> 8th video/export/thumbnails/"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import cinekit as CK, marker as MK, dogvision as DV
from thumbkit import W, H
OUT = "D:/why habibi/8th video/export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
P8 = "D:/why habibi/_media/photos_ep08/"; CUT = "D:/why habibi/_media/cutouts/"; BOSS = "D:/why habibi/_style_kit/mascot/batata_boss/Batata_boss_{}.png"

def fill(path, w, h, focus=(0.5, 0.5), sat=1.15, con=1.1, bright=1.0):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); im = im.crop((x, y, x + w, y + h))
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con); return ImageEnhance.Brightness(im).enhance(bright)

def dog_sticker(face, h, rot=0):
    im = Image.open(CUT + f"potato_dog_{face}.png").convert("RGBA"); im = im.crop(im.getbbox()); tmp = OUT + f"_tmp_{face}.png"; im.save(tmp)
    s = MK.sticker(tmp, h, border=10, rot=rot); os.remove(tmp); return s

def make_A():
    src = Image.open(P8 + "f8_face.jpg").convert("RGB"); z = 1.12 * H / src.height; src = src.resize((int(src.width * z), int(src.height * z)), Image.LANCZOS)
    fx = max(0, int(src.width * 0.43 - W / 2)); fy = max(0, min(src.height - H, int(src.height * 0.42 - H / 2))); base = ImageEnhance.Contrast(src.crop((fx, fy, fx + W, fy + H))).enhance(1.15); dog = DV.dog_view(base, blur=5.0)
    c = base.copy(); c.paste(dog.crop((W // 2, 0, W, H)), (W // 2, 0)); c = c.convert("RGBA"); d = ImageDraw.Draw(c)
    d.line((W // 2, 0, W // 2, H), fill=(255, 255, 255), width=10)
    for txt, x in (("YOU", W // 2 - 30), ("YOUR DOG", W // 2 + 30)):
        im = MK.hand(txt, 64, MK.WHITE, rot=0); MK.place(c, im, x - (im.width if x < W // 2 else 0) + im.width / 2, H - 70)
    CK.words(c, ["YOU, TO", "A DOG"], size=140, x=30, y=10); CK.corner_vignette(c); return c

def make_B():
    c = fill(P8 + "f8_nose.jpg", W, H, (0.45, 0.5), sat=1.2, con=1.2, bright=1.05).convert("RGBA")
    MK.strokes(c, MK.circle_path(610, 300, 240, 170, seed=6), MK.RED, 14, seed=6)
    CK.words(c, ["300", "MILLION"], size=140, x=W - 600, y=10)
    s = dog_sticker("shocked", 330, rot=-6); MK.place(c, s, W - s.width // 2 - 30, H - s.height // 2 - 10); CK.corner_vignette(c); return c

def make_C():
    c = fill(P8 + "f8_puppy_eyes.jpg", W, H, (0.5, 0.38), sat=1.2, con=1.15, bright=1.05).convert("RGBA")
    for p0, p1, sd in (((300, 160), (530, 300), 3), ((1000, 150), (770, 290), 4)):
        MK.strokes(c, MK.arrow_path(p0, p1, bend=0.2, head=40, seed=sd), MK.YEL, 14, seed=sd)
    CK.words(c, ["IT'S A", "TRICK?"], size=140, x=30, y=330)
    b = CK.batata(BOSS.format("sideeye"), 330); c.alpha_composite(b, (W - b.width - 20, H - b.height + 50)); CK.corner_vignette(c); return c

if __name__ == "__main__":
    ims = {"A_YOU_TO_A_DOG": make_A(), "B_300_MILLION": make_B(), "C_ITS_A_TRICK": make_C()}
    for n, im in ims.items(): im.convert("RGB").save(OUT + n + ".png"); print(OUT + n + ".png")
    sheet = Image.new("RGB", (W * 3 // 2 + 20, H // 2), (20, 20, 20))
    for k, im in enumerate(ims.values()): sheet.paste(im.convert("RGB").resize((W // 2, H // 2)), (k * (W // 2 + 10), 0))
    sheet.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
