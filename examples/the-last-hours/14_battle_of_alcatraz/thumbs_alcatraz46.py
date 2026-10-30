"""File 14 (the Battle of Alcatraz, 2-4 May 1946) thumbnails, BREAKOUT style: one real image filling the frame, 1-3 words on a red block,
the date on a yellow tab. Owner's mix rule (29 Oct): A in B&W (main) + B and C in the channel colour (TH_COLOUR=1 -> *_COLOR).
Real images only (NPS Golden Gate NRA): Bernard Coy's Alcatraz mugshot (B1), smoke from the cell house in May 1946 (C1), the officer
pointing at the gun-gallery bars Coy pried apart (C2), the bar spreader itself (A7), the US brief's "Miller told him, 107" line (A11).
Men only; no dead, no wounded. Preview only: never uploaded until the owner approves.
  uv run --no-project --with pillow --with numpy python thumbs_alcatraz46.py          (B&W set)
  TH_COLOUR=1 uv run --no-project --with pillow --with numpy python thumbs_alcatraz46.py (colour set)"""
import sys, os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/13_goering_last_night")
from thumbs_hakawi import src, cover, vign, block, card, ellipse, paste_faded, TW, TH, YEL, WHITE, RED
from thumbs_goering import bw
EP = "14_battle_of_alcatraz"; OUT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None
COLOUR = os.environ.get("TH_COLOUR") == "1"

def face_right(key, box, h=760, y=-20, blend=260):
    f = src(EP, key); W, H = f.size; f = bw(f.crop((int(W * box[0]), int(H * box[1]), int(W * box[2]), int(H * box[3]))))
    s = h / f.height; f = f.resize((int(f.width * s), h), Image.LANCZOS)
    bg = cover(f, TW, TH, cx=0.5, cy=0.4, z=1.6).filter(ImageFilter.GaussianBlur(28)); bg = ImageEnhance.Brightness(bg).enhance(0.28)
    c = bg.convert("RGBA"); paste_faded(c, f, TW - f.width + 20, y, left=blend)
    return vign(c, 0.4).convert("RGBA")

def bubble(c, key, box, cx, cy, r=170):
    im = src(EP, key).convert("RGB"); W0, H0 = im.size; im = im.crop((int(W0 * box[0]), int(H0 * box[1]), int(W0 * box[2]), int(H0 * box[3])))
    im = bw(cover(im, 2 * r, 2 * r)).convert("RGBA")
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255); im.putalpha(m)
    c.alpha_composite(im, (cx - r, cy - r)); ImageDraw.Draw(c).ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=RED + (255,), width=12)

def A():   # Bernard Coy, Alcatraz No. 415 (B1): KEY 107?
    c = face_right("B1_", (0.07, 0.04, 0.93, 0.97))
    block(c, "KEY", 40, 300, 150)
    block(c, "107?", 40, 490, 170, fill=WHITE, bg=RED + (255,))
    block(c, "2 MAY 1946", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def B():   # smoke bursting from the cell house, May 1946 (C1), the puff circled in red: GRENADES INSIDE
    f = src(EP, "C1_"); cx, cy, z = 0.56, 0.6, 1.7
    c = bw(cover(f, TW, TH, cx=cx, cy=cy, z=z)); c = vign(c, 0.5).convert("RGBA")
    ellipse(c, (440 - 125, 395 - 115, 440 + 125, 395 + 115), width=12)       # the smoke puff on the wall (canvas px for this framing)
    block(c, "GRENADES", 1240, 330, 140, anchor="r")
    block(c, "INSIDE", 1240, 490, 130, fill=WHITE, bg=RED + (255,), anchor="r")
    block(c, "ALCATRAZ, MAY 1946", 40, 72, 46, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def C():   # the officer at the gun-gallery bars Coy pried apart (C2) + the bar spreader (A7) in a bubble: THE GUN CAGE
    f = src(EP, "C2_"); c = bw(cover(f, TW, TH, cx=0.72, cy=0.4, z=1.0)); c = vign(c, 0.45).convert("RGBA")
    lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(620): d.line((x, 0, x, TH), fill=(0, 0, 0, int(220 * (1 - x / 620) ** 1.3)))
    c.alpha_composite(lay)
    bubble(c, "A7_", (0.0, 0.25, 0.62, 1.0), 200, 590, r=115)
    block(c, "THE GUN", 40, 215, 140)
    block(c, "CAGE", 40, 385, 160, fill=WHITE, bg=RED + (255,))
    block(c, "2 MAY 1946", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_KEY_107", A), ("B_GRENADES_INSIDE", B), ("C_THE_GUN_CAGE", C)):
        sfx = "_COLOR" if COLOUR else ""; im = fn().convert("RGB"); im.save(OUT + name + sfx + ".png"); im.save(OUT + name + sfx + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
    for i, t in enumerate(tiles):
        S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0))
        S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
    S.save(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"), quality=88); print(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"))
