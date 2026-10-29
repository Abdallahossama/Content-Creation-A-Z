"""Benghazi stadium (file 11) thumbnails, Hakawi colour style: Gaddafi's face large + one real scene + short text blocks + the date BIG.
The thumbnails never repeat the title's words. Faces: U.S. Navy 2009 (B1, PD), European Commission 2004 (B5, CC BY 4.0), Kremlin.ru 2008
(B7, CC BY 4.0): credited in the description with their years. Scenes: Pexels stills of empty arenas (G1, G3), Libyan radio's own words
as translated by FBIS (A14, US government). No frame of the 1984 broadcast, no rope or gallows graphic, no share-alike photos, men only.
  uv run --no-project --with pillow --with numpy python thumbs_gaddafi.py"""
import sys, os
from PIL import Image, ImageDraw, ImageEnhance
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, tint, vign, block, paste_faded, TW, TH, YEL, WHITE, RED
EP = "12_gaddafi_stadium"; OUT = "D:/why habibi/_newchannel/12_gaddafi_stadium/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None
DATE = "5 JUNE 1984"

def face(prefix, box, h, k=0.10, bright=1.06):
    m = src(EP, prefix); m = m.crop(tuple(int(v * s) for v, s in zip(box, (m.width, m.height, m.width, m.height))))
    m = grade(m, sat=1.12, contrast=1.15, teal=0.02, warm=0.08 + k * 0.4); m = ImageEnhance.Brightness(m).enhance(bright)
    s = h / m.height; return m.resize((int(m.width * s), h), Image.LANCZOS)

def A():   # mirrored sunglasses (U.S. Navy, 2009) over empty red arena seats: 8 MEN.
    c = grade(cover(src(EP, "G1_"), TW, TH, cx=0.4, cy=0.5, z=1.0), sat=1.25, contrast=1.12, teal=0.06, warm=0.12); c = vign(c, 0.5).convert("RGBA")
    m = face("B1_", (0.30, 0.0, 0.98, 1.0), TH); paste_faded(c, m, TW - m.width + 10, 0, left=260)
    block(c, "8 MEN.", 34, 96, 132)
    block(c, "8 DAYS.", 34, 248, 132, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, DATE, 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c
def B():   # straight at the camera (EC, 2004) + Libyan radio's own words, FBIS 6 Jun 1984, underlined: AGENT OF AMERICA?
    import lastkit as LK
    c = grade(cover(src(EP, "G3_"), TW, TH, cx=0.5, cy=0.5, z=1.0), sat=1.15, contrast=1.15, teal=0.06, warm=0.10); c = vign(c, 0.55).convert("RGBA")
    f = face("B5_", (0.0, 0.0, 1.0, 0.92), TH, k=0.06, bright=1.08); paste_faded(c, f, TW - f.width + 20, 0, left=160)
    pg = src(EP, "A14_").convert("RGB"); pg = pg.crop((0, 0, pg.width, int(pg.height * 0.62))); w = 430; pg = pg.resize((w, int(pg.height * w / pg.width)), Image.LANCZOS)
    card = LK.print_card(pg, w, border=12, rot=-3); c.alpha_composite(card, (30, 330))
    block(c, "AGENT OF", 34, 96, 120)
    block(c, "AMERICA?", 34, 238, 120, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, DATE, 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c
def C():   # cap and sunglasses (Kremlin.ru, 2008) over a dark floodlit arena: SHOW TRIAL. (HRW's words for 5 June 1984)
    c = grade(cover(src(EP, "G3_"), TW, TH, cx=0.35, cy=0.45, z=1.1), sat=1.2, contrast=1.2, teal=0.08, warm=0.12); c = vign(c, 0.45).convert("RGBA")
    m = face("B7_", (0.0, 0.0, 0.62, 1.0), 720, k=0.08); paste_faded(c, m, TW - m.width + 10, 0, left=220, bottom=60)                       # no background figures
    block(c, "SHOW", 34, 110, 150)
    block(c, "TRIAL.", 34, 276, 150, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, DATE, 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_8_MEN", A), ("B_AGENT_OF_AMERICA", B), ("C_SHOW_TRIAL", C)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (TW * 3 // 2 + 20, TH + TH // 2 + 20), (25, 25, 25))
    S.paste(tiles[0], (0, 0)); S.paste(tiles[1].resize((TW // 2, TH // 2)), (TW + 20, 0)); S.paste(tiles[2].resize((TW // 2, TH // 2)), (TW + 20, TH // 2 + 20))
    S.paste(tiles[0].resize((TW // 3, TH // 3)), (0, TH + 20)); S.paste(tiles[1].resize((TW // 3, TH // 3)), (TW // 3 + 10, TH + 20)); S.paste(tiles[2].resize((TW // 3, TH // 3)), (2 * TW // 3 + 20, TH + 20))
    S.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
