"""File 13 (Göring's last night) thumbnails, BREAKOUT style: one real image filling the frame, 1-3 words on a red block, the date BIG.
YouTube safety (research.md section 13): no swastika, no rope/noose/gallows/body; the text is about the clock and the searches, not death.
Real images only (U.S. Army / National Archives): Göring in his cell (B3), in the dock (B2), the guard at his cell door (C13),
the Army lab photo of the case and the vial (A4), the Army's English copy of his note (A5). Men only. Preview only: never uploaded
until the owner approves.
  uv run --no-project --with pillow --with numpy python thumbs_goering.py"""
import sys, os
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, vign, block, card, ellipse, paste_faded, TW, TH, YEL, WHITE, RED
EP = "13_goering_last_night"; OUT = "D:/why habibi/_newchannel/13_goering_last_night/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None

COLOUR = os.environ.get("TH_COLOUR") == "1"          # channel colour look (Hakawi): teal shadows, warm amber highlights
def bw(im, contrast=1.3, bright=0.95):
    g = ImageOps.grayscale(im.convert("RGB")); g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(contrast); g = ImageEnhance.Brightness(g).enhance(bright)
    if not COLOUR: return Image.merge("RGB", (g, g, g))
    sh, mid, hi = (10, 34, 48), (120, 118, 104), (255, 212, 150)                  # cinematic duotone of the B&W original
    lut = []
    for ch in range(3):
        for v in range(256):
            x = v / 255
            lut.append(int(sh[ch] + (mid[ch] - sh[ch]) * (x / 0.5)) if x < 0.5 else int(mid[ch] + (hi[ch] - mid[ch]) * ((x - 0.5) / 0.5)))
    return Image.merge("RGB", (g, g, g)).point(lut)

def face_right(key, box, h=820, y=-40, blend=260, x=None):
    """the subject on the right (crop box in source fractions), a dark blurred copy of the same photo behind it on the left"""
    f = src(EP, key); W, H = f.size; f = bw(f.crop((int(W * box[0]), int(H * box[1]), int(W * box[2]), int(H * box[3]))))
    s = h / f.height; f = f.resize((int(f.width * s), h), Image.LANCZOS)
    bg = cover(f, TW, TH, cx=0.5, cy=0.5, z=1.6).filter(ImageFilter.GaussianBlur(28)); bg = ImageEnhance.Brightness(bg).enhance(0.28)
    c = bg.convert("RGBA"); paste_faded(c, f, TW - f.width + 30 if x is None else x, y, left=blend)
    return vign(c, 0.4).convert("RGBA")

def A():   # Göring in his cell, close-up (B3) + 100 SEARCHES / HOW?
    c = face_right("B3_", (0.05, 0.02, 1.0, 0.80), h=840)
    block(c, "100 SEARCHES.", 40, 330, 104)
    block(c, "HOW?", 40, 500, 170, fill=WHITE, bg=RED + (255,))
    block(c, "15 OCT 1946", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def B():   # the guard at "H. GOERING"'s door (C13) + zoom bubble on the Army's photo of the case and vial (A4): WATCHED 24/7
    f = src(EP, "C13_"); c = bw(cover(f, TW, TH, cx=0.55, cy=0.33, z=1.08)); c = vign(c, 0.5).convert("RGBA")
    lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(560): d.line((x, 0, x, TH), fill=(0, 0, 0, int(215 * (1 - x / 560) ** 1.3)))
    c.alpha_composite(lay)
    cap = src(EP, "A4_").convert("RGB"); W0, H0 = cap.size; cap = cap.crop((int(W0 * 0.30), int(H0 * 0.04), int(W0 * 0.74), int(H0 * 0.58)))
    r = 190; cap = cover(cap, 2 * r, 2 * r, cx=0.5, cy=0.5, z=1.0).convert("RGBA")
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255); cap.putalpha(m)
    cx, cy = 1040, 470; c.alpha_composite(cap, (cx - r, cy - r))
    ImageDraw.Draw(c).ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=RED + (255,), width=12)
    block(c, "WATCHED", 40, 330, 130)
    block(c, "24/7", 40, 490, 150, fill=WHITE, bg=RED + (255,))
    block(c, "15 OCT 1946", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def C():   # Göring in the dock (B2) + the real line of his note on a paper strip, underlined: HIS NOTE
    c = face_right("B2_", (0.0, 0.0, 1.0, 0.78), h=820, y=-30)
    pg = src(EP, "A5_").convert("RGB"); W0, H0 = pg.size
    strip = pg.crop((int(W0 * 0.160), int(H0 * 0.2150), int(W0 * 0.870), int(H0 * 0.2480)))     # "I have always had the capsule of poison with me from the time"
    d = ImageDraw.Draw(strip); d.rectangle((int(strip.width * 0.02), int(strip.height * 0.43), int(strip.width * 0.98), int(strip.height * 0.43) + 6), fill=(205, 25, 25))
    cd = card(strip.resize((680, int(strip.height * 680 / strip.width)), Image.LANCZOS), 680, rot=-2.0, border=14)
    c.alpha_composite(cd, (24, 420))
    block(c, "HIS NOTE", 40, 300, 130, fill=WHITE, bg=RED + (255,))
    block(c, "15 OCT 1946", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "U.S. ARMY FILE", 40, 625, 44, fill=WHITE, bg=(0, 0, 0, 255))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_100_SEARCHES_HOW", A), ("B_WATCHED_24_7", B), ("C_HIS_NOTE", C)):
        sfx = "_COLOR" if COLOUR else ""; im = fn().convert("RGB"); im.save(OUT + name + sfx + ".png"); im.save(OUT + name + sfx + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
    for i, t in enumerate(tiles):
        S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0))
        S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
    S.save(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"), quality=88); print(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"))
