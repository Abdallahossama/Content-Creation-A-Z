"""File 15 (USS Indianapolis, 30 July - 3 August 1945) thumbnails, BREAKOUT style: one real image filling the frame, 1-3 words on
black / red blocks, the date on a yellow tab. Each pairs with one A/B title and never repeats its words:
  A  "Nobody Reported the USS Indianapolis Missing for 4 Days"       -> her last portrait (A13) + a raft from the Navy's rescue film: 8 PLANES / NONE LOOKED
  B  "They Asked the Man Who Sank the USS Indianapolis 1 Question"   -> I-58 at Sasebo (A20): HE / TESTIFIED
  C  "The USS Indianapolis Survivors Waited 4 Days. Nobody Looked."  -> Lt Gwinn by his Ventura (A24): HE LOOKED / DOWN
Real images only (US Navy / NARA / USMC). Men only; no bodies, no wounds, no sharks. Preview only: never uploaded until the owner approves.
  uv run --no-project --with pillow --with numpy python thumbs_indy.py              (B&W set)
  TH_COLOUR=1 uv run --no-project --with pillow --with numpy python thumbs_indy.py  (colour set)"""
import sys, os, subprocess, io
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/13_goering_last_night")
from thumbs_hakawi import src, cover, vign, block, ellipse, paste_faded, TW, TH, YEL, WHITE, RED
from thumbs_goering import bw
EP = "15_uss_indianapolis"; ROOT = "D:/why habibi/_newchannel/15_uss_indianapolis/"; OUT = ROOT + "export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None
COLOUR = os.environ.get("TH_COLOUR") == "1"

def film_frame(name, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", ROOT + "media/" + name, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")

def bubble(c, im, cx, cy, r=170):
    im = bw(cover(im, 2 * r, 2 * r)).convert("RGBA")
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255); im.putalpha(m)
    c.alpha_composite(im, (cx - r, cy - r)); ImageDraw.Draw(c).ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=RED + (255,), width=12)

def A():   # her last portrait, 10 July 1945 (A13) + a raft on the open sea (Navy film, A34a): 8 PLANES / NONE LOOKED
    f = src(EP, "A13_"); c = bw(cover(f, TW, TH, cx=0.5, cy=0.52, z=1.05)); c = vign(c, 0.45).convert("RGBA")
    bubble(c, film_frame("A34a_navy_film_raft_and_plane.mp4", 16.0).crop((40, 60, 680, 420)), 1080, 520, r=150)
    block(c, "8 PLANES", 40, 300, 140)
    block(c, "NONE LOOKED", 40, 470, 130, fill=WHITE, bg=RED + (255,))
    block(c, "30 JULY 1945", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def B():   # I-58 at Sasebo, January 1946 (A20): HE / TESTIFIED
    f = src(EP, "A20_"); c = bw(cover(f, TW, TH, cx=0.5, cy=0.45, z=1.1)); c = vign(c, 0.5).convert("RGBA")
    lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(640): d.line((x, 0, x, TH), fill=(0, 0, 0, int(225 * (1 - x / 640) ** 1.2)))
    c.alpha_composite(lay)
    block(c, "HE", 40, 300, 150)
    block(c, "TESTIFIED", 40, 480, 150, fill=WHITE, bg=RED + (255,))
    block(c, "THE SUB THAT SANK HER", 40, 92, 46, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def C():   # Lt (jg) Wilbur Gwinn beside his PV-1 Ventura, August 1945 (A24): HE LOOKED / DOWN
    f = src(EP, "A24_"); W0, H0 = f.size; man = bw(f.crop((int(W0 * 0.34), int(H0 * 0.10), int(W0 * 0.88), int(H0 * 0.97))))
    s = 720 / man.height; man = man.resize((int(man.width * s), 720), Image.LANCZOS)
    bg = bw(cover(src(EP, "F1_"), TW, TH)); bg = ImageEnhance.Brightness(bg).enhance(0.55)
    c = bg.convert("RGBA"); paste_faded(c, man, TW - man.width + 40, 0, left=260); c = vign(c, 0.4).convert("RGBA")
    block(c, "HE LOOKED", 40, 300, 140)
    block(c, "DOWN", 40, 470, 160, fill=WHITE, bg=RED + (255,))
    block(c, "2 AUGUST 1945", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_8_PLANES", A), ("B_HE_TESTIFIED", B), ("C_HE_LOOKED_DOWN", C)):
        sfx = "_COLOR" if COLOUR else ""; im = fn().convert("RGB"); im.save(OUT + name + sfx + ".png"); im.save(OUT + name + sfx + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
    for i, t in enumerate(tiles):
        S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0))
        S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
    S.save(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"), quality=88); print(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"))
