"""Ep 7 thumbnails (3 genuinely different compositions, real photos):
  A  OBJECT  the REAL Royal Game of Ur (British Museum, CC0) glowing + boss Batata side-eye, "4,600 YEARS"
  B  FACE    shocked man (Pexels) + the clay tablet with the oldest joke + 💨, "OLDEST JOKE"
  C  PROOF   Queen Nefertari playing senet (Met, CC0) full-bleed, red marker loop + zoom bubble on the board, "ANCIENT GAMER"
-> 7th video/export/thumbnails/"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep07_ancient_fun")
import cinekit as CK, marker as MK
from thumbkit import W, H
import ep07_draw as D
OUT = "D:/why habibi/7th video/export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
P7 = "D:/why habibi/_media/photos_ep07/"; CUT = "D:/why habibi/_media/cutouts/"; BOSS = "D:/why habibi/_style_kit/mascot/batata_boss/Batata_boss_{}.png"

def fill(path, w, h, focus=(0.5, 0.5), sat=1.15, con=1.1, bright=1.0):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); im = im.crop((x, y, x + w, y + h))
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con); im = ImageEnhance.Brightness(im).enhance(bright); return im.convert("RGBA")

def zoom_bubble(c, src, box, center, r=170):
    """magnify box (in c's coordinates) into a white-ringed circle at center, linked by a marker line"""
    crop = src.crop(box).resize((2 * r, 2 * r), Image.LANCZOS); m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    bub = Image.new("RGBA", (2 * r + 24, 2 * r + 24), (0, 0, 0, 0)); ImageDraw.Draw(bub).ellipse((0, 0, 2 * r + 23, 2 * r + 23), fill=(255, 255, 255, 255))
    crop.putalpha(m); bub.alpha_composite(crop, (12, 12))
    bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    MK.strokes(c, MK.arrow_path((bx, by), center, bend=0.1, head=0, seed=2), MK.WHITE, 8, seed=2)
    c.alpha_composite(bub, (int(center[0] - r - 12), int(center[1] - r - 12)))

def make_A():
    board = Image.open(P7 + "f7_ur_board.jpg").convert("RGB"); w, h = board.size; board = board.crop((int(w * 0.08), int(h * 0.12), int(w * 0.92), int(h * 0.80)))
    board = ImageEnhance.Contrast(board).enhance(1.15).convert("RGBA"); board = board.resize((640, int(640 * board.height / board.width)), Image.LANCZOS)
    rr = Image.new("L", board.size, 0); ImageDraw.Draw(rr).rounded_rectangle((0, 0, board.width - 1, board.height - 1), 26, fill=255); board.putalpha(rr)
    board = board.rotate(-6, Image.BICUBIC, expand=True)
    return CK.scene(CK.BLUE, BOSS.format("sideeye"), board, (255, 200, 90), ["4600", "YEARS"], prop_xy=(60, 250), b_cx=1040, b_top=170, b_h=600,
                    sleeves=True, hold=False, word_size=150)

def make_B():
    c = CK.backdrop(CK.RED, burst=(420, 380))
    tab = D.clay_tablet(560, 400).rotate(8, Image.BICUBIC, expand=True); CK.glow(c, tab, 80, 260, (255, 210, 120), r=40, a=0.9); c.alpha_composite(tab, (80, 260))
    CK.words(c, ["OLDEST", "JOKE"], size=150, x=40, y=10)
    m = MK.sticker(CUT + "person_shocked_man.png", 560, border=10, rot=3); MK.place(c, m, W - m.width // 2 + 30, H - m.height // 2 + 60)
    em = MK.place  # 💨 next to the tablet
    puff = Image.new("RGBA", (260, 200), (0, 0, 0, 0)); ImageDraw.Draw(puff).text((10, 10), "💨", font=__import__("PIL.ImageFont", fromlist=["x"]).truetype("C:/Windows/Fonts/seguiemj.ttf", 150), embedded_color=True)
    c.alpha_composite(puff.rotate(-10, expand=True), (540, 470)); CK.corner_vignette(c); return c

def make_C():
    src = fill(P7 + "f7_nefertari_senet.jpg", W, H, (0.5, 0.55), sat=1.25, con=1.15, bright=1.05); c = src.copy()
    sw, sh_ = Image.open(P7 + "f7_nefertari_senet.jpg").size; s = max(W / sw, H / sh_)
    bx0, by0 = 700, 360; box = (bx0, by0, bx0 + 300, by0 + 160)                       # the senet board on her table (approx.)
    MK.strokes(c, MK.circle_path((box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 180, 105, seed=4), MK.RED, 13, seed=4)
    zoom_bubble(c, src, box, (1080, 190), r=160)
    CK.words(c, ["ANCIENT", "GAMER"], size=140, x=30, y=10)
    b = CK.batata(BOSS.format("shocked"), 300); c.alpha_composite(b, (40, H - b.height + 40)); CK.corner_vignette(c); return c

if __name__ == "__main__":
    ims = {"A_4600_YEARS": make_A(), "B_OLDEST_JOKE": make_B(), "C_ANCIENT_GAMER": make_C()}
    for n, im in ims.items(): im.convert("RGB").save(OUT + n + ".png"); print(OUT + n + ".png")
    sheet = Image.new("RGB", (W * 3 // 2 + 20, H // 2), (20, 20, 20))
    for k, im in enumerate(ims.values()): sheet.paste(im.convert("RGB").resize((W // 2, H // 2)), (k * (W // 2 + 10), 0))
    sheet.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
