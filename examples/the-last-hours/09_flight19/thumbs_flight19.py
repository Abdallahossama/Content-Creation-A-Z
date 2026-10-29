"""Flight 19 (file 08) thumbnails, Hakawi colour style: ONE strong real image filling the frame + 2 short text lines + the date BIG.
Titles (A/B): 1 "14 Men Vanished Off Florida. Their Last Call Got No Answer." + A, 2 "Flight 19: 14 Men Vanished. Here Are Their Last Words." + B,
3 "5 Planes Vanished. The Navy Knew Where. Nobody Told Them." + C. The thumbnails never repeat the title's words.
Real images only (Navy 1942-43 Avenger photos, NHHC NH 84038, the NARA crash log, NASA MODIS); men only; Taylor's photo with neutral text.
  uv run --no-project --with pillow --with numpy python thumbs_flight19.py"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, tint, vign, block, ellipse, paste_faded, card, TW, TH, YEL, WHITE, RED
OUT = "D:/why habibi/_newchannel/09_flight19/export/thumbnails/"

def strip(im, box, w):
    """a strip of a document page (page px box), paper-toned, as a print card"""
    z = im.crop(box).convert("L").convert("RGB"); return card(z, w, rot=-1.5, border=8)

def A():   # five Avengers in a column over the clouds (1942, same type): WHERE ARE THEY?
    im = src("09_flight19", "B3_")
    c = grade(tint(cover(im, TW, TH, cx=0.55, cy=0.40, z=1.05), col=(60, 110, 150), k=0.6, contrast=1.3), sat=1.25, contrast=1.1, teal=0.10, warm=0.10); c = vign(c, 0.55)
    block(c, "WHERE", 34, 92, 130)
    block(c, "ARE THEY?", 34, 238, 130, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "5 DEC 1945", 34, 660, 58, fill=WHITE, bg=RED + (255,))
    return c
def B():   # Lt. Taylor (NHHC 1941 photo) ghosted over a dark sea + the crash-log line: 7:04 PM / NO ANSWER (neutral, no blame)
    c = grade(cover(src("09_flight19", "E1_"), TW, TH, cx=0.5, cy=0.5, z=1.1), sat=1.2, teal=0.12, warm=0.02); c = vign(c, 0.45)
    t = src("09_flight19", "I17_"); t = t.crop((int(t.width * 0.12), int(t.height * 0.04), int(t.width * 0.88), int(t.height * 0.74)))
    t = tint(t, col=(120, 150, 170), k=0.35, contrast=1.2); s = 760 / t.height; t = t.resize((int(t.width * s), 760), Image.LANCZOS)
    paste_faded(c, t, TW - t.width + 60, -20, left=260, bottom=140)
    log = src("09_flight19", "A13_"); k = strip(log, (930, 2735, 2470, 2890), 720)
    c.alpha_composite(k, (20, 430))
    d = ImageDraw.Draw(c); d.line((50, 430 + k.height - 22, 50 + 650, 430 + k.height - 22), fill=RED + (255,), width=6)
    block(c, "NO", 34, 92, 140)
    block(c, "ANSWER", 34, 250, 140, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "7:04 PM  ·  5 DEC 1945", 34, 662, 54, fill=WHITE, bg=RED + (255,))
    return c
def C():   # NASA MODIS: Florida, the Bahamas, open sea; the Navy's 5:50 p.m. fix circled (29°15'N 79°W): THEY WERE HERE
    im = src("09_flight19", "F1_")                                # BBOX lat 24.3-30.3, lon -84.6..-72.6, 1920x1080
    z, cx, cy = 1.35, 0.60, 0.36
    c = grade(cover(im, TW, TH, cx=cx, cy=cy, z=z), sat=1.25, contrast=1.12, teal=0.04, warm=0.04); c = vign(c, 0.4)
    s = max(TW / im.width, TH / im.height) * z; cw, ch = TW / s, TH / s
    x0 = min(max(cx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(cy * im.height - ch / 2, 0), im.height - ch)
    def xy(lon, lat): return ((lon + 84.6) / 12 * 1920 - x0) * s, ((30.3 - lat) / 6 * 1080 - y0) * s
    fx, fy = xy(-79.0, 29.25); hx, hy = xy(-80.12, 26.05)
    ellipse(c, (fx - 150, fy - 118, fx + 150, fy + 118), width=12)
    d = ImageDraw.Draw(c); d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=RED + (255,), outline=WHITE + (255,), width=4)
    block(c, "HOME", hx + 26, hy, 34, fill=WHITE, bg=(0, 0, 0, 220))
    block(c, "THEY WERE", TW - 34, 96, 118, anchor="r")
    block(c, "HERE", TW - 34, 228, 118, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    ax0, ay0, ax1, ay1 = TW - 330, 236, fx + 165, fy + 20                     # arrow from HERE to the circle
    d.line((ax0, ay0, ax1, ay1), fill=YEL + (255,), width=12)
    ang = math.atan2(ay1 - ay0, ax1 - ax0)
    d.polygon([(ax1, ay1), (ax1 - 34 * math.cos(ang - 0.45), ay1 - 34 * math.sin(ang - 0.45)), (ax1 - 34 * math.cos(ang + 0.45), ay1 - 34 * math.sin(ang + 0.45))], fill=YEL + (255,))
    block(c, "5:50 PM  ·  5 DEC 1945", TW - 34, 662, 54, fill=WHITE, bg=RED + (255,), anchor="r")
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_WHERE_ARE_THEY", A), ("B_NO_ANSWER_TAYLOR", B), ("C_THEY_WERE_HERE", C)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (TW * 3 // 2 + 20, TH + TH // 2 + 20), (25, 25, 25))
    S.paste(tiles[0], (0, 0)); S.paste(tiles[1].resize((TW // 2, TH // 2)), (TW + 20, 0)); S.paste(tiles[2].resize((TW // 2, TH // 2)), (TW + 20, TH // 2 + 20))
    S.paste(tiles[0].resize((TW // 3, TH // 3)), (0, TH + 20)); S.paste(tiles[1].resize((TW // 3, TH // 3)), (TW // 3 + 10, TH + 20)); S.paste(tiles[2].resize((TW // 3, TH // 3)), (2 * TW // 3 + 20, TH + 20))
    S.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
