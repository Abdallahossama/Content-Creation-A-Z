"""Roanoke thumbnails v2 (user, 22 Oct): 115 PEOPLE GONE gets a new, more detailed background; ONE WORD / NO CROSS keeps its
look but the ship must show; WHERE DID THEY GO? needs the people clearly visible plus one thing that grabs attention.
Real images only: John White's 1585 map (PD), the 1600 Hakluyt names page (PD), Bakhuizen 1667 (PD), the 1876 engraving (PD),
Pexels photos. Outputs sit next to v1 (A_, B_, C_ files are untouched)."""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel/05_roanoke")
from thumbs_roanoke import *                                             # cover, vign, grade, ghost, blockI, ellipse, CP, P, TW, TH, OUT, YEL, RED, L

def glow_mask(w, h, cx, cy, rx, ry, k=1.0):
    yy, xx = np.mgrid[0:h, 0:w]; r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    return np.clip(1 - r, 0, 1) ** 1.4 * k
def lift(c, cx, cy, rx, ry, k=0.35):
    """brighten one area of the scene (a pool of light on the subject)"""
    a = np.asarray(c.convert("RGB"), np.float32); m = glow_mask(c.width, c.height, cx, cy, rx, ry, k)[..., None]
    a = a * (1 + m) + m * 25; return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
def bubble(c, disc, bx, by, R_, px, py, pr=26):
    """M1-style zoom bubble: two white lines from the spot (px, py) to a white-rimmed disc, red outer ring"""
    disc = disc.resize((2 * R_, 2 * R_), Image.LANCZOS); mk = Image.new("L", disc.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, 2 * R_ - 1, 2 * R_ - 1), fill=255)
    d = ImageDraw.Draw(c)
    for sgn in (-1, 1):
        ang = np.arctan2(by - py, bx - px) + sgn * np.pi / 2
        d.line([(px + pr * np.cos(ang), py + pr * np.sin(ang)), (bx + R_ * np.cos(ang), by + R_ * np.sin(ang))], fill=(240, 240, 240, 255), width=4)
    d.ellipse((bx - R_ - 9, by - R_ - 9, bx + R_ + 9, by + R_ + 9), fill=(240, 240, 240, 255))
    c.paste(disc, (bx - R_, by - R_), mk)
    ImageDraw.Draw(c).ellipse((bx - R_ - 9, by - R_ - 9, bx + R_ + 9, by + R_ + 9), outline=RED + (255,), width=8)
def tag(c, s, x, y, size=46, fill=(0, 0, 0), bg=(240, 232, 214, 255)):
    return blockI(c, s, x, y, size, fill=fill, bg=bg, pad=(16, 8))

# B2: 115 PEOPLE / GONE on John White's own 1585 map: Roanoke Island circled, a zoom bubble on the printed list of their names
def B2():
    mp = CP("A1"); W, H = mp.size
    box = (0.035, 0.405, 0.915, 0.405 + 0.88 * W / H * 9 / 16)                 # landscape window, clear of the museum colour bar
    c = mp.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H))).resize((TW, TH), Image.LANCZOS)
    c = grade(c, sat=1.55, contrast=1.22, teal=0.05, warm=0.12); c = vign(c, 0.55)
    def X(fx): return (fx - box[0]) / (box[2] - box[0]) * TW
    def Y(fy): return (fy - box[1]) / (box[3] - box[1]) * TH
    ix, iy = X(0.628), Y(0.541)                                                  # Roanoke Island (pink, with the settlement dots)
    pg = Image.open(P("A8")).convert("RGB"); pw, ph = pg.size
    side = int(pw * 0.40); sx, sy = int(pw * 0.085), int(ph * 0.125)               # heading + the first names ("Iohn White ...")
    disc = grade(pg.crop((sx, sy, sx + side, sy + side)), sat=0.9, contrast=1.25, teal=0.0, warm=0.10)
    bx, by, R_ = 1040, 520, 168
    bubble(c, disc, bx, by, R_, ix, iy, pr=40)
    ellipse(c, (ix - 82, iy - 40, ix + 78, iy + 44), width=9)
    blockI(c, "115 PEOPLE", 34, 118, 150, fill=YEL)
    blockI(c, "GONE", 34, 290, 140, fill=(255, 255, 255), bg=(178, 34, 34, 255))
    tag(c, "1587", 40, 640); tag(c, "1590: EMPTY", 168, 640, fill=(255, 255, 255), bg=(0, 0, 0, 255))
    return c

# B3: 115 PEOPLE / GONE in a ghost forest at dusk (dead trunks in a salt marsh, NC coast), their names ghosted large
def B3():
    c = grade(cover(CP("D10"), TW, TH, cx=0.5, cy=0.55, z=1.05), sat=1.25, contrast=1.25, teal=0.22, warm=0.10)
    a = np.asarray(c.convert("RGB"), np.float32); sky = np.clip(1 - np.arange(TH) / (TH * 0.62), 0, 1)[:, None, None]
    a = a * (1 - 0.45 * sky) + sky * 0.45 * np.array([214, 120, 70]); a *= 0.78                       # dusk sky, darker ground
    c = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    names = Image.open(P("A8")).convert("RGB"); names = names.crop((200, 780, 2420, 3250))
    c.alpha_composite(ghost(names, 600, int(600 * names.height / names.width), 0.62), (TW - 640, 40))
    c = vign(c, 0.5)
    blockI(c, "115 PEOPLE", 34, 470, 160, fill=YEL)
    blockI(c, "GONE", 34, 640, 130, fill=(255, 255, 255), bg=(178, 34, 34, 255))
    tag(c, "1587", 40, 330); tag(c, "1590: EMPTY", 168, 330, fill=(255, 255, 255), bg=(0, 0, 0, 255))
    return c

# C2: ONE WORD. / NO CROSS. - same painting and page line, re-framed so the ship is big and lit, the line moved below it
def C2():
    c = grade(cover(CP("C5"), TW, TH, cx=0.352, cy=0.563, z=1.425), sat=1.2, contrast=1.15, teal=0.10, warm=0.12)
    c = lift(c, 925, 300, 260, 240, 0.32); c = vign(c, 0.4)
    pg = Image.open(P("A12")).convert("L")
    rows = json.load(open("D:/why habibi/_newchannel/05_roanoke/build/lines_A12.json")); ya, yb = rows[6][0] - 70, rows[6][1] + 60
    strip = pg.crop((420, ya, 2420, yb)); a = np.asarray(strip, np.float32); lo, hi = np.percentile(a, 5), np.percentile(a, 99)
    a = np.clip((a - lo) / (hi - lo), 0, 1); strip = Image.fromarray((a[..., None] * np.array([240, 230, 205])).astype(np.uint8))
    sw = 1080; k = sw / strip.width; strip = strip.resize((sw, int(strip.height * k)), Image.LANCZOS).convert("RGBA")
    ty0, ty1 = (rows[6][0] - ya) * k, (rows[6][1] - ya) * k; tx0, tx1 = (1650 - 420) * k, (2105 - 420) * k
    ellipse(strip, (tx0 - 24, ty0 - 24, tx1 + 24, ty1 + 20), width=9)
    card = L.print_card(strip.convert("RGB"), sw, border=10, rot=-2); c.alpha_composite(card, ((TW - card.width) // 2, TH - card.height - 14))
    blockI(c, "ONE WORD.", 34, 120, 128)
    blockI(c, "NO CROSS.", 34, 270, 128, fill=(0, 0, 0), bg=YEL + (255,))
    return c

# A2: WHERE DID THEY GO? - the 1876 engraving's men stand out dark against a pool of fog light; the carved CROATOAN glows red
def A2():
    c = grade(cover(CP("E4"), TW, TH, cx=0.45, cy=0.5), sat=1.25, teal=0.16, warm=0.10); c = vign(c, 0.45)
    eng = Image.open(P("A14")).convert("L"); EW, EH = eng.size
    ex0, ey0, ex1, ey1 = 0.08, 0.075, 0.70, 0.97
    eng = eng.crop((int(ex0 * EW), int(ey0 * EH), int(ex1 * EW), int(ey1 * EH)))
    ew = 800; eh = int(ew * eng.height / eng.width); gx, gy = TW - ew, TH - eh + 24
    # the engraving itself as a warm, contrasty print emerging from the dark forest (left edge melts into the trees)
    g = np.asarray(eng.resize((ew, eh), Image.LANCZOS), np.float32); lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    g = np.clip((g - lo) / (hi - lo), 0, 1) ** 1.15
    rgb = np.stack([g * 236 + 8, g * 222 + 8, g * 190 + 10], -1)                      # sepia paper, near-black ink
    yy, xx = np.mgrid[0:eh, 0:ew]
    edge = np.minimum.reduce([np.clip(xx / 230, 0, 1), np.clip(yy / 50, 0, 1), np.clip((ew - 1 - xx) / 30, 0, 1), np.clip((eh - 1 - yy) / 40, 0, 1)]) ** 1.3
    pr = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).convert("RGBA"); pr.putalpha(Image.fromarray((edge * 255).astype(np.uint8)))
    c.alpha_composite(pr, (gx, gy))
    # the carved word: re-ink it red, glow, ring
    def FX(fx): return gx + (fx - ex0) / (ex1 - ex0) * ew
    def FY(fy): return gy + (fy - ey0) / (ey1 - ey0) * eh
    wx0, wy0, wx1, wy1 = FX(0.231), FY(0.205), FX(0.345), FY(0.258)
    sub = np.asarray(eng.resize((ew, eh), Image.LANCZOS), np.float32)[int(wy0 - gy):int(wy1 - gy), int(wx0 - gx):int(wx1 - gx)]
    wa = Image.fromarray((np.clip((170 - sub) / 110, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    word = Image.new("RGBA", wa.size, (255, 46, 30, 0)); word.putalpha(wa)
    halo = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); halo.alpha_composite(word, (int(wx0), int(wy0))); halo = halo.filter(ImageFilter.GaussianBlur(7))
    for _ in range(3): c.alpha_composite(halo)
    c.alpha_composite(word, (int(wx0), int(wy0)))
    # zoom bubble on the carved word: the engraving's own tree trunk, its letters re-inked red
    side = int(0.17 * EW); sx, sy = int(0.205 * EW), int(0.232 * EH) - side // 2
    disc = Image.open(P("A14")).convert("L").crop((sx, sy, sx + side, sy + side)); da = np.asarray(disc, np.float32)
    rgb = np.stack([da * 0.96 + 6, da * 0.90 + 4, da * 0.78], -1)                  # warm paper tone
    lyy, lxx = np.mgrid[0:side, 0:side]; ly0, ly1 = 0.203 * EH - sy, 0.260 * EH - sy; lx0, lx1 = 0.231 * EW - sx, 0.344 * EW - sx
    let = ((lyy > ly0) & (lyy < ly1) & (lxx > lx0) & (lxx < lx1)).astype(np.float32) * np.clip((165 - da) / 100, 0, 1)
    let = np.asarray(Image.fromarray((let * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)), np.float32)[..., None] / 255
    rgb = rgb * (1 - let) + let * np.array([225, 30, 22])
    bubble(c, Image.fromarray(rgb.clip(0, 255).astype(np.uint8)), 395, 560, 135, (wx0 + wx1) / 2, (wy0 + wy1) / 2, pr=60)
    ellipse(c, (wx0 - 34, wy0 - 30, wx1 + 34, wy1 + 28), width=9)
    blockI(c, "WHERE DID", 34, 150, 138)
    blockI(c, "THEY GO?", 34, 320, 138, fill=(0, 0, 0), bg=YEL + (255,))
    return c

if __name__ == "__main__":
    items = [("A2_WHERE_DID_THEY_GO", A2), ("B2_115_PEOPLE_MAP", B2), ("B3_115_PEOPLE_FOREST", B3), ("C2_ONE_WORD_SHIP", C2)]
    only = sys.argv[1:]
    for name, fn in items:
        if only and name.split("_")[0] not in only: continue
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
    sheet = Image.new("RGB", (2 * 640 + 30, 2 * 360 + 30), (30, 30, 30))
    for i, (n, _) in enumerate(items):
        if os.path.exists(OUT + n + ".png"): sheet.paste(Image.open(OUT + n + ".png").resize((640, 360)), (10 + (i % 2) * 650, 10 + (i // 2) * 370))
    sheet.save(OUT + "_sheet_v2.png"); print("ok")
