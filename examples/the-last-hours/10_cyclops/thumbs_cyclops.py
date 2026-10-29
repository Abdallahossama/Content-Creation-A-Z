"""USS Cyclops (file 09) thumbnails, Hakawi colour style: ONE strong real image filling the frame + 2 short text lines + the date BIG.
Titles (A/B): 1 "306 Men Vanished at Sea. Their Last Message Was About Coal." + A, 2 "USS Cyclops: 306 Men Vanished With 10,800 Tons of Ore" + B,
3 "306 Men Vanished. The Navy Telegram Said: No Bad Weather." + C. The thumbnails never repeat the title's words.
Real images only (LoC Harris & Ewing broadside, NHHC NH 50636 seaman Crammer, NASA Blue Marble); men only.
  uv run --no-project --with pillow --with numpy python thumbs_cyclops.py"""
import sys, os, math
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, tint, vign, block, ellipse, paste_faded, TW, TH, YEL, WHITE, RED
OUT = "D:/why habibi/_newchannel/10_cyclops/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None

def ship(rid, box, cx, cy, z, col=(70, 120, 150), k=0.55):
    im = src("10_cyclops", rid); im = im.crop(tuple(int(v * s) for v, s in zip(box, (im.width, im.height, im.width, im.height))))
    return grade(tint(cover(im, TW, TH, cx=cx, cy=cy, z=z), col=col, k=k, contrast=1.3), sat=1.2, contrast=1.1, teal=0.10, warm=0.12)

def A():   # the ship herself, broadside (Harris & Ewing, LoC): WHERE DID SHE GO?
    c = vign(ship("B1_", (0.04, 0.05, 0.95, 0.93), 0.52, 0.60, 1.05), 0.55)
    block(c, "WHERE DID", 34, 88, 124)
    block(c, "SHE GO?", 34, 228, 124, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "4 MARCH 1918", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c
def B():   # Seaman Earnest R. Crammer, cap band "U.S.S. CYCLOPS" (NHHC NH 50636), ghosted over the ship: NEVER FOUND
    c = vign(ship("B2_", (0.0, 0.0, 1.0, 1.0), 0.40, 0.55, 1.08), 0.5)
    m = src("10_cyclops", "C3_"); m = m.crop((int(m.width * 0.04), int(m.height * 0.0), int(m.width * 0.96), int(m.height * 0.70)))
    m = tint(m, col=(120, 150, 170), k=0.35, contrast=1.25); s = 760 / m.height; m = m.resize((int(m.width * s), 760), Image.LANCZOS)
    paste_faded(c, m, TW - m.width + 40, -30, left=200, bottom=150)
    block(c, "NEVER", 34, 92, 140)
    block(c, "FOUND", 34, 250, 140, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "MARCH 1918", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c
def C():   # NASA Blue Marble, the last leg: Barbados circled, a short arrow SOUTH, the planned line north to Chesapeake Bay: SHE WENT SOUTH?
    im = src("10_cyclops", "F2_")                                        # Barbados x 1199 y 969; Cape Henry x 665 y 111 (1920x1080)
    c = grade(cover(im, TW, TH, cx=0.5, cy=0.5, z=1.0), sat=1.25, contrast=1.1, teal=0.04, warm=0.04); c = vign(c, 0.4)
    k = TW / 1920; bx, by, hx, hy = 1199 * k, 969 * k, 665 * k, 111 * k
    d = ImageDraw.Draw(c)
    n = 26
    for i in range(n):                                                  # the planned route north, dashed
        if i % 2: continue
        x0, y0 = bx + (hx - bx) * i / n, by + (hy - by) * i / n; x1, y1 = bx + (hx - bx) * (i + 1) / n, by + (hy - by) * (i + 1) / n
        d.line((x0, y0, x1, y1), fill=WHITE + (230,), width=6)
    block(c, "BALTIMORE", hx + 20, hy + 6, 30, fill=WHITE, bg=(0, 0, 0, 210))
    ellipse(c, (bx - 46, by - 40, bx + 46, by + 40), width=10)
    ax0, ay0, ax1, ay1 = bx + 70, by - 40, bx + 70, by + 52                 # an arrow beside the island, pointing south
    d.line((ax0, ay0, ax1, ay1), fill=YEL + (255,), width=12); ang = math.atan2(ay1 - ay0, ax1 - ax0)
    d.polygon([(ax1, ay1), (ax1 - 32 * math.cos(ang - 0.45), ay1 - 32 * math.sin(ang - 0.45)), (ax1 - 32 * math.cos(ang + 0.45), ay1 - 32 * math.sin(ang + 0.45))], fill=YEL + (255,))
    block(c, "SHE WENT", TW - 34, 96, 120, anchor="r")
    block(c, "SOUTH?", TW - 34, 232, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    block(c, "4 MAR 1918  ·  BARBADOS", 34, 662, 54, fill=WHITE, bg=RED + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_WHERE_DID_SHE_GO", A), ("B_NEVER_FOUND", B), ("C_SHE_WENT_SOUTH", C)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (TW * 3 // 2 + 20, TH + TH // 2 + 20), (25, 25, 25))
    S.paste(tiles[0], (0, 0)); S.paste(tiles[1].resize((TW // 2, TH // 2)), (TW + 20, 0)); S.paste(tiles[2].resize((TW // 2, TH // 2)), (TW + 20, TH // 2 + 20))
    S.paste(tiles[0].resize((TW // 3, TH // 3)), (0, TH + 20)); S.paste(tiles[1].resize((TW // 3, TH // 3)), (TW // 3 + 10, TH + 20)); S.paste(tiles[2].resize((TW // 3, TH // 3)), (2 * TW // 3 + 20, TH + 20))
    S.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
