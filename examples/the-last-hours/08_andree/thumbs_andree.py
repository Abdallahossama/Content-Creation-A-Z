"""The Andrée balloon (file 07) thumbnails, Hakawi colour style: ONE strong real image filling the frame + 2 short text lines.
Title: "3 Men Vanished in a Balloon. 33 Years Later, Their Film Was Developed." - the thumbnails never repeat its words.
Real images only (Strindberg's 1897 frames, NASA/USGS Landsat); men only; no remains, no shot animals.
  uv run --no-project --with pillow --with numpy python thumbs_andree.py"""
import sys, os
from PIL import Image
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, vign, block, ellipse, TW, TH, YEL, WHITE, RED
OUT = "D:/why habibi/_newchannel/08_andree/export/thumbnails/"

from PIL import ImageDraw, ImageFilter, ImageEnhance
def bubble(c, im, box, cx, cy, r, src_xy=None, ring=RED, bright=1.0):
    """zoom bubble: box (fractions) of the full-res source shown in a circle at (cx, cy), white rim + red ring, optional connector"""
    w, h = im.size; z = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))).convert("RGB")
    z = z.resize((2 * r, 2 * r), Image.LANCZOS)
    if bright != 1.0: z = ImageEnhance.Brightness(z).enhance(bright); z = ImageEnhance.Contrast(z).enhance(1.15)
    d = ImageDraw.Draw(c)
    if src_xy:
        d.line((src_xy[0], src_xy[1], cx, cy), fill=(0, 0, 0, 200), width=14); d.line((src_xy[0], src_xy[1], cx, cy), fill=ring, width=8)
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - r - 8, cy - r + 4, cx + r + 16, cy + r + 20), fill=(0, 0, 0, 170))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    d.ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=ring); d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=(255, 255, 255))
    c.paste(z, (cx - r, cy - r), m)
def tagbox(c, s, x, y, size=34, fill=(255, 255, 255), bg=(0, 0, 0, 225)):
    block(c, s, x, y, size, fill=fill, bg=bg)

def crop(im, box): w, h = im.size; return im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))

def A():   # Strindberg's frame of the Eagle on the ice, 14 July 1897: THEIR LAST PHOTOS + a zoom bubble on the man (balloon left fully visible)
    im = src("08_andree", "C1_")
    c = grade(cover(im, TW, TH, cx=0.58, cy=0.55, z=1.12), sat=1.0, contrast=1.2, teal=0.18, warm=0.10); c = vign(c, 0.55)
    ellipse(c, (225, 415, 345, 545), width=10)                                  # the man beside the gondola
    g = grade(im.crop((int(0.262 * im.width), int(0.600 * im.height), int(0.350 * im.width), int(0.732 * im.height))), sat=1.0, contrast=1.2, teal=0.18, warm=0.10)
    bubble(c, g, (0, 0, 1, 1), 125, 352, 86, src_xy=(240, 448), bright=1.12)
    block(c, "THEIR LAST", 34, 72, 98)
    block(c, "PHOTOS", 34, 188, 98, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "14 JULY 1897", 34, 662, 54, fill=WHITE, bg=RED + (255,))            # the date, big (user 24 Oct: dates on every thumbnail)
    return c
def B():   # all three shove the boat-sledge over a pressure ridge (self-timer, 1897): HOW DID THEY DIE?
    im = src("08_andree", "C10_")
    c = grade(cover(im, TW, TH, cx=0.42, cy=0.55, z=1.15), sat=1.0, contrast=1.22, teal=0.16, warm=0.12); c = vign(c, 0.55)
    block(c, "HOW DID", TW - 34, 70, 124, anchor="r")
    block(c, "THEY DIE?", TW - 34, 215, 124, fill=WHITE, bg=RED + (255,), anchor="r")
    block(c, "1897", 34, 662, 60, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def C():   # White Island from space (NASA/USGS Landsat, 2021), the south-west point circled + zoom bubble of that shore today (CC0)
    im = src("08_andree", "F2_")
    c = grade(cover(im, TW, TH, cx=0.47, cy=0.42, z=1.25), sat=1.15, contrast=1.1, teal=0.04, warm=0.03); c = vign(c, 0.5)
    ellipse(c, (285, 535, 470, 705), width=12)
    shore = src("08_andree", "E2_")
    bubble(c, shore, (0.10, 0.30, 0.62, 1.0), 860, 505, 160, src_xy=(455, 600))
    tagbox(c, "THEIR LAST CAMP", 700, 676, 34)
    block(c, "THEY REACHED", TW - 34, 60, 104, anchor="r")
    block(c, "THIS ISLAND", TW - 34, 190, 104, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    block(c, "5 OCTOBER 1897", TW - 34, 286, 48, fill=WHITE, bg=RED + (255,), anchor="r")
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_THEIR_LAST_PHOTOS", A), ("B_HOW_DID_THEY_DIE", B), ("C_THIS_ISLAND", C)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (TW * 3 // 2 + 20, TH + TH // 2 + 20), (25, 25, 25))
    S.paste(tiles[0], (0, 0)); S.paste(tiles[1].resize((TW // 2, TH // 2)), (TW + 20, 0)); S.paste(tiles[2].resize((TW // 2, TH // 2)), (TW + 20, TH // 2 + 20))
    S.paste(tiles[0].resize((TW // 3, TH // 3)), (0, TH + 20)); S.paste(tiles[1].resize((TW // 3, TH // 3)), (TW // 3 + 10, TH + 20)); S.paste(tiles[2].resize((TW // 3, TH // 3)), (2 * TW // 3 + 20, TH + 20))
    S.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
