"""al-Khuld Hall (file 10) thumbnails v3, BREAKOUT style (owner 29 Oct: "make the Saddam thumbnail too, don't apply it, preview first").
Model: the WWII breakout thumbs (B&W real face filling the frame + 1-3 words on a red block). Pairs with the proposed title
"The FBI Asked Saddam About His 1979 Purge. He Said 4 Words." (his answer in FBI session 8, 20 Feb 2004, p. 8: "we were all scared").
Real images only: DoD photos of Saddam after his capture, Dec 2003 (B5 shaved, B4 bearded) and the FBI session-8 page (A11). Men only.
Preview only: writes export/thumbnails/_v3_preview/, never touches Studio.
  uv run --no-project --with pillow --with numpy python thumbs_khuld_v3.py"""
import sys, os
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, vign, block, card, paste_faded, TW, TH, YEL, WHITE, RED
import lastkit as LK
EP = "11_khuld_hall"; OUT = "D:/why habibi/_newchannel/11_khuld_hall/export/thumbnails/_v3_preview/"
Image.MAX_IMAGE_PIXELS = None

def bw(im, contrast=1.35, bright=0.95):
    g = ImageOps.grayscale(im.convert("RGB")); g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(contrast); g = ImageEnhance.Brightness(g).enhance(bright)
    return Image.merge("RGB", (g, g, g))

def left_dark(c, frac=0.55, k=0.85):
    """darken the left part so the text blocks read, fading into the face"""
    w = int(TW * frac); m = Image.new("L", (TW, TH), 0); d = ImageDraw.Draw(m)
    for x in range(w): d.line((x, 0, x, TH), fill=int(255 * k * (1 - x / w) ** 1.4))
    c.paste(Image.new("RGB", (TW, TH), (0, 0, 0)), (0, 0), m); return c

def face_right(key, box, h=820, x=None, y=-50, blend=260):
    """the whole head on the right (crop box in source fractions), a dark blurred copy of the same photo behind it on the left"""
    f = src(EP, key); W, H = f.size; f = bw(f.crop((int(W * box[0]), int(H * box[1]), int(W * box[2]), int(H * box[3]))))
    s = h / f.height; f = f.resize((int(f.width * s), h), Image.LANCZOS)
    bg = cover(f, TW, TH, cx=0.5, cy=0.5, z=1.6).filter(ImageFilter.GaussianBlur(28)); bg = ImageEnhance.Brightness(bg).enhance(0.28)
    c = bg.convert("RGBA"); paste_faded(c, f, TW - f.width + 30 if x is None else x, y, left=blend)
    return vign(c, 0.4).convert("RGBA")

def V1():   # B&W face (DoD, Dec 2003), whole head on the right: ALL / SCARED
    c = face_right("B5_", (0.0, 0.0, 1.0, 0.92))
    block(c, "ALL", 40, 330, 165)
    block(c, "SCARED", 40, 520, 165, fill=WHITE, bg=RED + (255,))
    block(c, "22 JULY 1979", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def V2():   # same face, a little closer: 4 WORDS / TO THE FBI
    c = face_right("B5_", (0.0, 0.02, 1.0, 0.80), h=860, y=-40)
    block(c, "4 WORDS", 40, 340, 145, fill=WHITE, bg=RED + (255,))
    block(c, "TO THE FBI", 40, 515, 84)
    block(c, "22 JULY 1979", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def V3():   # bearded capture face (DoD, Dec 2003) + the real FBI line on a paper strip, underlined: HIS ANSWER
    c = face_right("B4_", (0.02, 0.0, 1.0, 0.90), h=800, y=-30)
    pg = src(EP, "A11_").convert("RGB"); strip = pg.crop((165, 505, 905, 532))   # interviewer was not correct, "we were all scared."
    d = ImageDraw.Draw(strip); d.rectangle((447, 23, 725, 27), fill=(205, 25, 25))   # red underline under "we were all scared."
    cd = card(strip.resize((640, int(strip.height * 640 / strip.width)), Image.LANCZOS), 640, rot=-2.0, border=14)
    c.alpha_composite(cd, (24, 430))
    block(c, "HIS ANSWER", 40, 300, 120, fill=WHITE, bg=RED + (255,))
    block(c, "22 JULY 1979", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "FBI FILE, 2004", 40, 625, 44, fill=WHITE, bg=(0, 0, 0, 255))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("V1_ALL_SCARED", V1), ("V2_4_WORDS", V2), ("V3_HIS_ANSWER", V3)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append(im)
    # sheet: the three at half size on top, then all three at phone size (~1/4) under them
    S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
    for i, t in enumerate(tiles):
        S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0))
        S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
    S.save(OUT + "_sheet.jpg", quality=88); print(OUT + "_sheet.jpg")
