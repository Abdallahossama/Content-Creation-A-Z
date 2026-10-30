"""File 16 (the fog escape, Alcatraz, 16 December 1937) thumbnails, Hakawi / BREAKOUT style: one real image filling the frame, the two real
mugs from the NARA cards, 1-3 words on black / red blocks, the date on a yellow tab. Each pairs with one A/B title and never repeats its words:
  A  "Counted at 1:00. Gone From Alcatraz at 1:30. Never Found."  -> the island in fog + both mugs ghosted: WHERE / DID THEY GO?
  B  "2 Men Vanished From Alcatraz in 30 Minutes of Fog"          -> Roe's card, the red ESCAPED stamp: DROWNED? / OR FREE?
  C  "They Escaped Alcatraz 25 Years Before the Famous Raft"      -> the FBI's aerial of the island + Cole in a bubble: NEVER / FOUND
Real images only (NARA, FBI, Pexels for today's island). Men only. Preview only: never uploaded until the owner approves.
  uv run --no-project --with pillow --with numpy python thumbs_coleroe.py              (B&W set)
  TH_COLOUR=1 uv run --no-project --with pillow --with numpy python thumbs_coleroe.py  (colour set)"""
import sys, os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/13_goering_last_night")
from thumbs_hakawi import src, cover, vign, block, ellipse, paste_faded, TW, TH, YEL, WHITE, RED
from thumbs_goering import bw
EP = "16_cole_roe_1937"; OUT = "D:/why habibi/_newchannel/16_cole_roe_1937/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None
COLOUR = os.environ.get("TH_COLOUR") == "1"
MUG = (0.738, 0.088, 0.925, 0.368)                                   # the mug photo on a warden's notebook card (fraction of the card)

def mug(key, h):
    f = src(EP, key); W0, H0 = f.size; m = bw(f.crop((int(W0 * MUG[0]), int(H0 * MUG[1]), int(W0 * MUG[2]), int(H0 * MUG[3]))))
    s = h / m.height; return m.resize((int(m.width * s), h), Image.LANCZOS)

def bubble(c, im, cx, cy, r=170):
    im = cover(im, 2 * r, 2 * r).convert("RGBA")
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255); im.putalpha(m)
    c.alpha_composite(im, (cx - r, cy - r)); ImageDraw.Draw(c).ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=RED + (255,), width=12)

def A():   # Alcatraz today in fog-grey B&W (Pexels) + Cole and Roe ghosted on the right: WHERE / DID THEY GO?
    c = bw(cover(src(EP, "G17_"), TW, TH, cx=0.5, cy=0.5, z=1.15)); c = ImageEnhance.Brightness(c).enhance(0.8).convert("RGBA")
    a, b = mug("A1_", 560), mug("A2_", 560)
    paste_faded(c, a, TW - a.width - b.width + 120, 170, left=150, right=60); paste_faded(c, b, TW - b.width + 30, 170, left=150)
    c = vign(c, 0.45).convert("RGBA")
    block(c, "WHERE", 40, 300, 150)
    block(c, "DID THEY GO?", 40, 480, 120, fill=WHITE, bg=RED + (255,))
    block(c, "16 DEC 1937", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def B():   # Roe's card (A2), the red stamp "ESCAPED DECEMBER 16, 1937" and his mug: DROWNED? / OR FREE?
    f = src(EP, "A2_"); W0, H0 = f.size; card = f.convert("RGB").crop((0, 0, W0, int(H0 * 0.45)))
    c = cover(card, TW, TH, cx=0.55, cy=0.45, z=1.0); c = ImageEnhance.Contrast(c).enhance(1.15).convert("RGBA")
    lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(700): d.line((x, 0, x, TH), fill=(0, 0, 0, int(215 * (1 - x / 700) ** 1.1)))
    c.alpha_composite(lay)
    block(c, "DROWNED?", 40, 330, 140)
    block(c, "OR FREE?", 40, 500, 140, fill=WHITE, bg=RED + (255,))
    block(c, "ALCATRAZ, 1937", 40, 650, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def C():   # the FBI's aerial of Alcatraz before 1934 (G1) + Cole's mug in a bubble: NEVER / FOUND
    c = bw(cover(src(EP, "G1_"), TW, TH, cx=0.5, cy=0.55, z=1.6)); c = vign(c, 0.5).convert("RGBA")
    bubble(c, mug("A1_", 420), 1060, 470, r=160)
    block(c, "NEVER", 40, 300, 150)
    block(c, "FOUND", 40, 480, 160, fill=WHITE, bg=RED + (255,))
    block(c, "THE FOG ESCAPE · 1937", 40, 92, 46, fill=(0, 0, 0), bg=YEL + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_WHERE_DID_THEY_GO", A), ("B_DROWNED_OR_FREE", B), ("C_NEVER_FOUND", C)):
        sfx = "_COLOR" if COLOUR else ""; im = fn().convert("RGB"); im.save(OUT + name + sfx + ".png"); im.save(OUT + name + sfx + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
    for i, t in enumerate(tiles):
        S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0))
        S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
    S.save(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"), quality=88); print(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"))
