"""Roanoke thumbnails v3 (analytics 6 Nov: CTR 1.6% on 2,702 impressions, the channel's worst; Saddam's famous face got 4.3-5%).
R1: a FAMOUS FACE (Sir Walter Raleigh, 1588, PD) over the ghost forest at dusk, "115 VANISHED".
R2: the 1876 CROATOAN engraving (PD) pushed in on the carved post, "THE ONLY CLUE".
R3: an empty beach at dusk (Pexels) + the real 1600 printed line with CROATOAN in a zoom bubble, "NEVER FOUND".
Rules: <= 3 big words, words never repeat the paired title, nothing in the bottom corners, no text on a face.
  uv run --no-project --with pillow --with numpy python thumbs_roanoke_v3.py"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel/05_roanoke")
from thumbs_roanoke import *                                             # cover, vign, grade, ghost, blockI, ellipse, CP, P, TW, TH, OUT, YEL, RED, L
from thumbs_roanoke_v2 import bubble, lift, tag

def fade_right(img, w, h, fade=220):
    """an image placed on the right, its left edge fading into the scene"""
    im = img.convert("RGBA").resize((w, h), Image.LANCZOS)
    g = np.clip(np.arange(w) / fade, 0, 1) ** 1.3; a = (g[None, :] * np.ones((h, 1)) * 255).astype(np.uint8)
    im.putalpha(Image.fromarray(a)); return im

def R1():
    c = grade(cover(CP("D10"), TW, TH, cx=0.35, cy=0.55, z=1.1), sat=1.2, contrast=1.25, teal=0.25, warm=0.08)
    a = np.asarray(c.convert("RGB"), np.float32); sky = np.clip(1 - np.arange(TH) / (TH * 0.6), 0, 1)[:, None, None]
    a = a * (1 - 0.5 * sky) + sky * 0.5 * np.array([205, 110, 60]); a *= 0.62
    c = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    rp = CP("B1"); W, H = rp.size
    face = rp.crop((int(0.0 * W), int(0.0 * H), int(0.66 * W), int(0.52 * H)))       # Raleigh, head and shoulders
    face = grade(face, sat=1.15, contrast=1.15, teal=0.05, warm=0.12)
    fh = TH; fw = int(face.width * fh / face.height)
    c.alpha_composite(fade_right(face, fw, fh, fade=260), (TW - fw + 40, 0))
    c = vign(c, 0.45)
    blockI(c, "115", 40, 230, 190, fill=YEL)
    blockI(c, "VANISHED", 40, 420, 150, fill=(255, 255, 255), bg=(178, 34, 34, 255))
    tag(c, "SIR WALTER RALEIGH'S LOST COLONY  ·  1590", 40, 72, size=34, fill=(255, 255, 255), bg=(0, 0, 0, 255))
    return c

def R2():
    eng = Image.open(P("A14")).convert("L")
    c = cover(eng, TW, TH, cx=0.36, cy=0.27, z=1.75)
    a = np.asarray(c, np.float32) / 255; a = np.clip((a - 0.12) * 1.35, 0, 1)
    col = a[..., None] * np.array([238, 214, 170]) + (1 - a[..., None]) * np.array([38, 26, 18])   # warm sepia print
    c = Image.fromarray(col.clip(0, 255).astype(np.uint8)).convert("RGBA"); c = vign(c, 0.6)
    W, H = eng.size; s = max(TW / W, TH / H) * 1.75; cw, ch = TW / s, TH / s
    x0 = min(max(0.36 * W - cw / 2, 0), W - cw); y0 = min(max(0.27 * H - ch / 2, 0), H - ch)
    def X(fx): return (fx * W - x0) * s
    def Y(fy): return (fy * H - y0) * s
    ellipse(c, (318, 262, 652, 392), width=12)                                   # the carved CROATOAN on the post (pixel box, checked on the sheet)
    blockI(c, "THE ONLY", TW - 40, 470, 120, anchor="r")
    blockI(c, "CLUE", TW - 40, 610, 130, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c

def R3():
    c = grade(cover(CP("E2"), TW, TH, cx=0.62, cy=0.5, z=1.05), sat=1.1, contrast=1.2, teal=0.28, warm=0.06)
    c = lift(c, 1010, 330, 260, 300, k=0.25); c = vign(c, 0.5)
    pg = Image.open(P("A12")).convert("L")
    rows = json.load(open("D:/why habibi/_newchannel/05_roanoke/build/lines_A12.json")); r = rows[6]
    side = 500; cx, cy = (1650 + 2105) // 2, (r[0] + r[1]) // 2                     # just the word and a little of its lines
    disc = pg.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2))
    a = np.asarray(disc, np.float32); lo, hi = np.percentile(a, 5), np.percentile(a, 99); a = np.clip((a - lo) / (hi - lo), 0, 1)
    disc = Image.fromarray((a[..., None] * np.array([240, 230, 205])).astype(np.uint8)).convert("RGBA")
    k = 2 * 200 / side; wx0, wx1 = (1650 - (cx - side // 2)) * k, (2105 - (cx - side // 2)) * k
    wy0, wy1 = (r[0] - (cy - side // 2)) * k, (r[1] - (cy - side // 2)) * k
    disc = disc.resize((400, 400), Image.LANCZOS); ellipse(disc, (wx0 - 14, wy0 - 16, wx1 + 14, wy1 + 14), width=7)
    bubble(c, disc.convert("RGB"), 870, 250, 200, 1080, 480, pr=30)
    blockI(c, "NEVER", 40, 300, 170)
    blockI(c, "FOUND.", 40, 490, 170, fill=(0, 0, 0), bg=YEL + (255,))
    tag(c, "1590  ·  THE LOST COLONY", 40, 110, size=34, fill=(255, 255, 255), bg=(178, 34, 34, 255))
    return c

if __name__ == "__main__":
    names = [("R1_RALEIGH_115_VANISHED", R1), ("R2_THE_ONLY_CLUE", R2), ("R3_NEVER_FOUND", R3)]
    for name, fn in names:
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
    sheet = Image.new("RGB", (TW * 3 // 2 + 40, TH // 2 + 200), (30, 30, 30))
    for i, (n, _) in enumerate(names):
        im = Image.open(OUT + n + ".png"); sheet.paste(im.resize((TW // 2, TH // 2)), (10 + i * (TW // 2 + 10), 10))
        sheet.paste(im.resize((246, 138)), (10 + i * (TW // 2 + 10), TH // 2 + 40))
    sheet.save(OUT + "_sheet_v3.png"); print(OUT + "_sheet_v3.png")
