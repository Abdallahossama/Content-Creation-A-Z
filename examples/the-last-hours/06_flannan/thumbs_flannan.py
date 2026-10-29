"""Flannan Isles (file 05) thumbnails, Hakawi colour style: ONE strong real image filling the frame + 2 short text lines
(the lesson from the 22 Oct review). Title: "3 Lighthouse Keepers Vanished in 1900. One Left His Coat." - the thumbnails
never repeat its words. Real images only; no women.
  uv run --no-project --with pillow --with numpy python thumbs_flannan.py"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
sys.path.insert(0, "D:/why habibi/_newchannel")
import thumbs_hakawi as TH_
from thumbs_hakawi import src, cover, grade, tint, vign, block, ellipse, TW, TH, YEL, WHITE, RED
OUT = "D:/why habibi/_newchannel/06_flannan/export/thumbnails/"

def A():   # the real island, photographed c.1904-11, lighthouse on its crown: WHERE DID THEY GO?
    im = src("06_flannan", "H4_"); w, h = im.size
    ch = 0.52 * w * 9 / 16; y0 = 0.50 * h - ch / 2
    im = im.crop((int(0.27 * w), int(y0), int(0.79 * w), int(y0 + ch)))
    c = tint(im, col=(80, 130, 170), k=0.72, contrast=1.5).resize((TW, TH), Image.LANCZOS); c = vign(c, 0.65)
    block(c, "WHERE DID", 30, 110, 120)
    block(c, "THEY GO?", 30, 255, 120, fill=(0, 0, 0), bg=YEL + (255,))
    ellipse(c, (832, 192, 930, 302), width=9)
    return c
def B():   # coats on a row of hooks, one circled: HE RAN OUT WITHOUT IT
    im = src("06_flannan", "G4_")
    c = grade(cover(im, TW, TH, cx=0.5, cy=0.5, z=1.0), sat=1.1, teal=0.10, warm=0.06); c = vign(c, 0.5)
    ellipse(c, (700, 150, 1010, 690), width=12)
    block(c, "HE RAN OUT", 40, 470, 118)
    block(c, "WITHOUT IT", 40, 610, 118, fill=WHITE, bg=RED + (255,))
    return c
def C():   # a lighthouse lantern at night, beams out: DARK FOR 11 NIGHTS
    im = src("06_flannan", "E3_")
    c = grade(cover(im, TW, TH, cx=0.5, cy=0.45, z=1.08), sat=1.25, teal=0.12, warm=0.04); c = vign(c, 0.45)
    block(c, "DARK FOR", 40, 470, 130)
    block(c, "11 NIGHTS", 40, 620, 130, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def D():   # the real c.1900 photo of the three keepers (+ Muirhead, right), the three outlined: NEVER FOUND
    im = src("06_flannan", "H1_"); im = im.crop((0, 40, 900, 40 + int(900 * 9 / 16)))
    a = np.asarray(im.convert("L"), np.float32)[..., None] / 255; a = np.clip((a - 0.5) * 1.25 + 0.5, 0, 1)
    c = Image.fromarray((a * np.array([236, 214, 178]) ).clip(0, 255).astype(np.uint8)).resize((TW, TH), Image.LANCZOS).convert("RGBA")
    c = vign(c, 0.55); s = TW / 900
    for x0, x1 in ((150, 330), (326, 480), (484, 656)):                     # each keeper, head to knee
        ellipse(c, (x0 * s, (60 - 40) * s, x1 * s, (330 - 40) * s), width=9)
    block(c, "NEVER", TW - 30, 470, 130, anchor="r")
    block(c, "FOUND", TW - 30, 620, 130, fill=WHITE, bg=RED + (255,), anchor="r")
    return c

KEEPERS = [                                                       # hand-traced outlines of the three keepers in H1 (900x575), as in render_flannan.py
 [(215, 66), (268, 66), (266, 95), (262, 135), (300, 146), (320, 165), (330, 352), (302, 358), (297, 546), (255, 550), (242, 335), (230, 550),
  (198, 550), (194, 356), (154, 352), (155, 170), (176, 148), (220, 137), (217, 95)],
 [(372, 106), (431, 106), (427, 132), (421, 170), (456, 181), (471, 200), (478, 380), (450, 384), (449, 546), (414, 551), (407, 372), (398, 372),
  (395, 549), (361, 549), (362, 384), (329, 380), (332, 200), (349, 181), (384, 170), (377, 132)],
 [(539, 104), (594, 104), (591, 130), (585, 170), (626, 180), (646, 200), (651, 357), (616, 362), (613, 546), (585, 549), (566, 380), (555, 380),
  (546, 549), (509, 546), (514, 362), (487, 357), (491, 200), (509, 180), (552, 170), (546, 130)],
]
def E(opacity=0.88):   # A + D: the real island and lighthouse, the three real keepers cut out of their photo, standing over it
    im = src("06_flannan", "H4_"); w, h = im.size
    ch = 0.52 * w * 9 / 16; y0 = 0.50 * h - ch / 2
    im = im.crop((int(0.27 * w), int(y0), int(0.79 * w), int(y0 + ch)))
    c = tint(im, col=(80, 130, 170), k=0.72, contrast=1.5).resize((TW, TH), Image.LANCZOS); c = vign(c, 0.65)
    ph = src("06_flannan", "H1_"); m = Image.new("L", ph.size, 0); d = ImageDraw.Draw(m)
    for poly in KEEPERS: d.polygon(poly, fill=255)
    m = m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(6)); box = (140, 50, 668, 556)
    g = np.asarray(ph.crop(box).convert("L"), np.float32); g = np.clip(g / np.percentile(g, 85), 0, 1) ** 1.15   # the wall -> white
    sc = 610 / g.shape[0]; size = (int(g.shape[1] * sc), 610)
    g = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize(size, Image.LANCZOS), np.float32)[..., None] / 255
    a = np.asarray(m.crop(box).resize(size, Image.LANCZOS), np.float32)[..., None] / 255 * opacity
    a *= np.clip((size[1] - np.arange(size[1])) / (size[1] * 0.35), 0, 1)[:, None, None]       # legs melt into the sea
    bg = np.asarray(c.convert("RGB"), np.float32); x0, y0_ = 30, 22; reg = bg[y0_:y0_ + size[1], x0:x0 + size[0]]
    ink = np.array([28, 30, 36], np.float32)                     # the men printed in near-black ink: multiply, so white wall vanishes
    reg[:] = reg * (1 - a) + (reg * (g + (1 - g) * ink / 255)) * a
    c = Image.fromarray(bg.clip(0, 255).astype(np.uint8)).convert("RGBA")
    ellipse(c, (832, 192, 930, 302), width=9)
    block(c, "WHERE DID", TW - 30, 470, 120, anchor="r")
    block(c, "THEY GO?", TW - 30, 615, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c

HEADS = [  # light parts the multiply blend would lose: (cap box, face ellipse centre + radii, collar box), in H1 pixels
 ((215, 68, 268, 98), (241, 118, 16, 21), (232, 136, 252, 152)),
 ((372, 106, 430, 129), (401, 150, 16, 22), (390, 172, 414, 204)),
 ((539, 106, 594, 133), (569, 155, 15, 21), (558, 175, 584, 190)),
]
def keepers_over_island(alphas, dashed=(), beam=False, sc=1.344, at=(10, 12)):
    """the real island (A) with the three real keepers (D) standing over it: bodies multiplied in as dark ink, faces and
    collars laid in as light, so they read on a phone; alphas = how much of each man is still there"""
    im = src("06_flannan", "H4_"); w, h = im.size
    ch = 0.52 * w * 9 / 16; y0 = 0.50 * h - ch / 2
    im = im.crop((int(0.27 * w), int(y0), int(0.79 * w), int(y0 + ch)))
    c = tint(im, col=(80, 130, 170), k=0.72, contrast=1.5).resize((TW, TH), Image.LANCZOS)
    bg = np.asarray(c.convert("RGB"), np.float32)
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)                      # deep teal shadow behind the men so the faces glow
    sh = np.clip(1.15 - np.sqrt(((xx - 360) / 560) ** 2 + ((yy - 230) / 420) ** 2), 0, 1) ** 0.9
    bg = bg * (1 - 0.6 * sh[..., None]) + np.array([12, 32, 46], np.float32) * 0.6 * sh[..., None]
    if beam:                                                             # the lighthouse's beam, swung round onto them
        lx, ly = 880, 248; ang = np.arctan2(yy - ly, xx - lx); tgt = np.arctan2(300 - ly, 330 - lx)
        d_ = np.abs(np.angle(np.exp(1j * (ang - tgt)))); cone = np.clip(1 - d_ / 0.30, 0, 1) ** 1.3
        cone *= np.clip(np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / 80, 0, 1) * np.clip(1 - (xx < 0), 0, 1)
        bg = bg + cone[..., None] * np.array([170, 205, 215], np.float32) * 0.85
    ph = src("06_flannan", "H1_"); box = (140, 50, 668, 556); bw_, bh_ = box[2] - box[0], box[3] - box[1]
    size = (int(bw_ * sc), int(bh_ * sc)); X0, Y0 = at
    g = np.asarray(ph.crop(box).convert("L"), np.float32); gw = np.clip(g / np.percentile(g, 85), 0, 1) ** 1.15
    gw = np.asarray(Image.fromarray((gw * 255).astype(np.uint8)).resize(size, Image.LANCZOS), np.float32)[..., None] / 255
    lit = np.asarray(Image.fromarray(np.clip((g - g.min()) / (np.percentile(g, 99) - g.min()), 0, 1).__mul__(255).astype(np.uint8)).resize(size, Image.LANCZOS), np.float32)[..., None] / 255
    melt = np.clip((size[1] - np.arange(size[1])) / (size[1] * 0.33), 0, 1)[:, None, None]          # legs melt into the sea
    reg = bg[Y0:Y0 + size[1], X0:X0 + size[0]]
    wall = np.clip((gw - 0.66) / 0.2, 0, 1); wall = wall * wall * (3 - 2 * wall)                    # 1 where the pixel is as bright as the wall
    col_rgb = (lit ** 0.85) * np.array([236, 230, 218], np.float32)                               # the men, lifted a little, cool-neutral
    for i, (poly, (cap, (fx, fy, rx, ry), col)) in enumerate(zip(KEEPERS, HEADS)):
        if alphas[i] <= 0: continue
        m = Image.new("L", ph.size, 0); d = ImageDraw.Draw(m); d.polygon(poly, fill=255)
        mb = np.asarray(m.filter(ImageFilter.GaussianBlur(1.5)).crop(box).resize(size, Image.LANCZOS), np.float32)[..., None] / 255
        hm = Image.new("L", ph.size, 0); d = ImageDraw.Draw(hm); d.ellipse((fx - rx, fy - ry, fx + rx, fy + ry), fill=255); d.rectangle(col, fill=255)
        hb = np.asarray(hm.filter(ImageFilter.GaussianBlur(3)).crop(box).resize(size, Image.LANCZOS), np.float32)[..., None] / 255
        a = np.maximum(mb * (1 - wall), hb) * melt * alphas[i]                                      # body without the wall, plus face and collar
        gl = np.asarray(Image.fromarray((a[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(16)), np.float32)[..., None] / 255
        reg[:] = reg * (1 - 0.8 * gl) + np.array([185, 222, 235], np.float32) * 0.8 * gl          # soft light rim behind each man
        reg[:] = reg * (1 - a) + col_rgb * a
    c = Image.fromarray(bg.clip(0, 255).astype(np.uint8)).convert("RGBA"); c = vign(c, 0.6)
    for i in dashed:                                                     # a man who is gone: only his red dashed outline is left
        pts = [((x - box[0]) * sc + X0, (y - box[1]) * sc + Y0) for x, y in KEEPERS[i]]; pts.append(pts[0]); d = ImageDraw.Draw(c)
        for j in range(len(pts) - 1):
            (xa, ya), (xb, yb) = pts[j], pts[j + 1]; n = max(1, int(np.hypot(xb - xa, yb - ya) / 16))
            for q in range(0, n, 2):
                d.line([(xa + (xb - xa) * q / n, ya + (yb - ya) * q / n), (xa + (xb - xa) * min(q + 1, n) / n, ya + (yb - ya) * min(q + 1, n) / n)], fill=RED + (255,), width=7)
        cap = HEADS[i][0]; hx = ((cap[0] + cap[2]) / 2 - box[0]) * sc + X0; hy = (HEADS[i][1][1] - box[1]) * sc + Y0 + 40
        block(c, "GONE", hx, hy, 58, fill=WHITE, bg=RED + (255,), anchor="m", pad=(14, 8))
    return c
def E2():   # unique: they vanish left to right - one solid, one a ghost, one only a red outline marked GONE
    c = keepers_over_island([1.0, 0.45, 0.0], dashed=(2,))
    ellipse(c, (832, 192, 930, 302), width=9)
    block(c, "WHERE DID", TW - 30, 470, 120, anchor="r")
    block(c, "THEY GO?", TW - 30, 615, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c
def E3():   # unique: the lighthouse beam swung onto the three of them
    c = keepers_over_island([1.0, 1.0, 1.0], beam=True)
    block(c, "WHERE DID", TW - 30, 470, 120, anchor="r")
    block(c, "THEY GO?", TW - 30, 615, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); items = [("A_WHERE_DID_THEY_GO", A), ("B_RAN_OUT_WITHOUT_IT", B), ("C_DARK_11_NIGHTS", C), ("D_NEVER_FOUND", D)]
    for name, fn in items:
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
    sheet = Image.new("RGB", (2 * 640 + 20, 2 * 380 + 158), (30, 30, 30))       # 2x2 full size + a phone-feed size row
    for i, (n, _) in enumerate(items):
        im = Image.open(OUT + n + ".png"); sheet.paste(im.resize((640, 360)), ((i % 2) * 660, (i // 2) * 380))
        sheet.paste(im.resize((246, 138)), (i * 266 + 120, 2 * 380))
    sheet.save(OUT + "_sheet.png"); print(OUT)
