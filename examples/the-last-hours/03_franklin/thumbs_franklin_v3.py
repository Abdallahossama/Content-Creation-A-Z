"""The Last Hours #2 (Franklin) - thumbnail OPTIONS v3 (24 Oct 2026). New ideas next to the live A/B set
(A_NONE_CAME_HOME, B_ALL_WELL, C_TRAPPED_588_DAYS) and _v1 (A_129_MEN_GONE). Hakawi colour style: ONE real hero image filling
the frame, 2 short lines of huge Impact text (<= 4 words, none from the title "129 Men Vanished in the Arctic. This Is Their
Last Note."), a red circle + zoom bubble on the key clue, small date tags, nothing in the bottom-right (duration badge).
Real images only (all from media/, PD): B1 note, A2 Crozier daguerreotype, C5 McClintock's 1859 map, D2 ILN 1845 ships
(boats with passengers cropped out), D15 ILN 1859 cairn engraving, C1 1850 reward poster, A1 Franklin. No women, no remains.
Facts: research/research.md (105 souls / none survived; Crozier's fate unknown; ships abandoned 22 Apr 1848; note written
25 Apr 1848, found 6 May 1859 = 11 years; 7 Mar 1850 poster, nobody relieved the crews).
  uv run --no-project --with pillow --with numpy python thumbs_franklin_v3.py"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, vign, block, TW, TH, YEL, WHITE, RED, IMPACT
import lastkit as L
Image.MAX_IMAGE_PIXELS = None
OUT = "D:/why habibi/_newchannel/03_franklin/export/thumbnails_colour/_options_v3/"
EP = "03_franklin"
BLACK = (0, 0, 0)
RING = (232, 28, 28)

# ------------------------------------------------------------------ helpers
def duo(im, lo=(14, 32, 44), hi=(244, 230, 200), cut=(1.5, 99.0), gamma=1.0):
    """an engraving kept an engraving: ink lines stay, black ink -> deep teal, paper -> warm cream (a colour print, not a fake photo)"""
    g = np.asarray(im.convert("L"), np.float32); a, b = np.percentile(g, cut); g = np.clip((g - a) / (b - a), 0, 1) ** gamma
    lo, hi = np.array(lo, np.float32), np.array(hi, np.float32)
    return Image.fromarray((lo + (hi - lo) * g[..., None]).clip(0, 255).astype(np.uint8)).convert("RGBA")

def spot(c, cx, cy, rx, ry, lift=0.25, dark=0.3):
    """a pool of light on the subject: brighten inside a soft ellipse, darken outside (same picture, no new content)"""
    yy, xx = np.mgrid[0:c.height, 0:c.width]; r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    m = np.clip(1 - r, 0, 1) ** 1.2; k = (1 - dark) + (dark + lift) * m
    a = np.asarray(c.convert("RGB"), np.float32) * k[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def fit_size(s, size, maxw):
    """largest Impact size <= size whose text width (+ block padding) fits maxw"""
    while size > 40:
        bb = L.font(IMPACT, size).getbbox(s)
        if bb[2] - bb[0] + 48 <= maxw: return size
        size -= 2
    return size

def aa(draw_fn, S=3):
    """supersampled overlay layer (smooth rings and lines)"""
    lay = Image.new("RGBA", (TW * S, TH * S), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(lay), S)
    return lay.resize((TW, TH), Image.LANCZOS)

def ring(c, box, w=10):
    """clean red ellipse with a thin dark edge so it reads on light paper and dark scenes alike"""
    x0, y0, x1, y1 = box
    def f(d, S):
        d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), outline=(0, 0, 0, 150), width=int((w + 6) * S))
        d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), outline=RING + (255,), width=int(w * S))
    c.alpha_composite(aa(f))

def bubble(c, disc, cx, cy, r, src_xy=None, src_r=30):
    """zoom bubble (M1 / Roanoke B2 style): two white lines from the circled spot to a white-rimmed disc with a red outer ring"""
    if src_xy:
        px, py = src_xy; ang = np.arctan2(cy - py, cx - px)
        def lines(d, S):
            for sgn in (-1, 1):
                a = ang + sgn * np.pi / 2
                p0 = (S * (px + src_r * np.cos(a)), S * (py + src_r * np.sin(a))); p1 = (S * (cx + r * np.cos(a)), S * (cy + r * np.sin(a)))
                d.line([p0, p1], fill=(0, 0, 0, 140), width=int(9 * S)); d.line([p0, p1], fill=(245, 245, 245, 255), width=int(4 * S))
        c.alpha_composite(aa(lines))
    sh = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - r - 10, cy - r + 2, cx + r + 18, cy + r + 22), fill=(0, 0, 0, 170))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    def rim(d, S): d.ellipse((S * (cx - r - 9), S * (cy - r - 9), S * (cx + r + 9), S * (cy + r + 9)), fill=(245, 245, 245, 255))
    c.alpha_composite(aa(rim))
    disc = disc.convert("RGB").resize((2 * r, 2 * r), Image.LANCZOS)
    S = 4; m = Image.new("L", (2 * r * S, 2 * r * S), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r * S - 1, 2 * r * S - 1), fill=255)
    c.paste(disc, (cx - r, cy - r), m.resize((2 * r, 2 * r), Image.LANCZOS))
    def outer(d, S): d.ellipse((S * (cx - r - 9), S * (cy - r - 9), S * (cx + r + 9), S * (cy + r + 9)), outline=RING + (255,), width=int(9 * S))
    c.alpha_composite(aa(outer))

def tag(c, s, x, y, size=40, fill=WHITE, bg=(0, 0, 0, 235), anchor="l"):
    block(c, s, x, y, size, fill=fill, bg=bg, anchor=anchor, pad=(14, 7))

def two_lines(c, l1, l2, x, y1, y2, size, maxw, anchor="l", st1=(WHITE, (0, 0, 0, 255)), st2=(BLACK, YEL + (255,))):
    s1, s2 = fit_size(l1, size, maxw), fit_size(l2, size, maxw); s = min(s1, s2) if abs(s1 - s2) < 12 else None
    block(c, l1, x, y1, s or s1, fill=st1[0], bg=st1[1], anchor=anchor)
    block(c, l2, x, y2, s or s2, fill=st2[0], bg=st2[1], anchor=anchor)

def win(im, box):
    """exact 16:9 window of the source (fractions not needed: pixel box), resized to the frame"""
    return im.crop(box).resize((TW, TH), Image.LANCZOS)

# ------------------------------------------------------------------ N1: the real note, "105 souls" circled + rotated zoom
def N1():
    im = src(EP, "B1_"); box = (30, 140, 1546, 993); s = TW / (box[2] - box[0])
    c = grade(win(im, box), sat=1.18, contrast=1.16, teal=0.10, warm=0.12); c = vign(c, 0.55)
    T = lambda x, y: ((x - box[0]) * s, (y - box[1]) * s)
    (x0, y0), (x1, y1) = T(92, 592), T(134, 826)                                  # "105 souls" runs up the left margin (1848 hand)
    ring(c, (x0 - 26, y0 - 18, x1 + 24, y1 + 16), w=9)
    z = im.crop((40, 578, 300, 838)).rotate(-90, Image.BICUBIC)                  # paper only (scan border left out), turned to read left to right
    z = grade(z, sat=1.18, contrast=1.25, teal=0.06, warm=0.12)
    bubble(c, z, 350, 470, 168, src_xy=((x0 + x1) / 2, (y0 + y1) / 2), src_r=40)
    two_lines(c, "105 WALKED", "0 SURVIVED", TW - 30, 95, 245, 132, 760, anchor="r", st1=(YEL, (0, 0, 0, 255)), st2=(WHITE, RED + (255,)))
    tag(c, "APRIL 1848", 196, 672)
    return c

# ------------------------------------------------------------------ N2: Crozier's daguerreotype + his own 1848 signature
def N2():
    im = src(EP, "A2_"); box = (430, 420, 1415, 974)                            # inside the plate: hat to chest, he looks right
    c = grade(win(im, box), sat=1.15, contrast=1.14, teal=0.13, warm=0.10); c = vign(c, 0.5)
    note = src(EP, "B1_")
    z = note.crop((1140, 50, 1470, 380)).rotate(180, Image.BICUBIC)              # upside-down top-right corner: "F R M Crozier /
    z = grade(z, sat=1.15, contrast=1.3, teal=0.04, warm=0.12)                     # Captain & Senior Offr / and start on tomorrow 26th"
    bubble(c, z, 1060, 182, 150)
    two_lines(c, "WHAT HAPPENED", "TO CROZIER?", TW - 30, 432, 565, 112, 640, anchor="r")
    tag(c, "HIS SIGNATURE, APRIL 1848", 1060, 365, size=30, anchor="m")
    return c

# ------------------------------------------------------------------ N3: McClintock's own 1859 map, "abandoned" dot circled, the ship zoomed
def N3():
    im = src(EP, "C5_"); box = (430, 835, 1480, 1425); s = TW / (box[2] - box[0])
    c = grade(win(im, box), sat=1.4, contrast=1.15, teal=0.05, warm=0.10); c = vign(c, 0.5)
    T = lambda x, y: ((x - box[0]) * s, (y - box[1]) * s)
    dx, dy = T(802, 1172)                                                         # red dot: "EREBUS & TERROR ABANDONED 22nd APRIL 1848"
    ring(c, (dx - 335, dy - 63, dx + 39, dy + 25), w=9)                         # the whole label + dot, so "1848" stays readable
    sh = src(EP, "D11_").crop((1130, 640, 1580, 1090))                            # 1853 lithograph: men hauling a sledge past a ship frozen in (user: "make the men more seen")
    z = grade(sh, sat=1.15, contrast=1.35, teal=0.08, warm=0.08)
    bubble(c, z, 1005, 455, 178, src_xy=(dx, dy), src_r=46)
    two_lines(c, "WHY ABANDON", "SHIP?", TW - 30, 88, 232, 128, 720, anchor="r")
    block(c, "22 APRIL 1848", 1005, 668, 58, fill=WHITE, bg=RED + (255,), anchor="m")            # the date, big (user: dates on every thumbnail)
    return c

# ------------------------------------------------------------------ N4: ILN 1859, opening the Point Victory cairn; the note zoomed
def N4():
    im = src(EP, "D15_"); box = (420, 600, 3600, 2389); s = TW / (box[2] - box[0])
    c = duo(win(im, box), lo=(8, 24, 36), hi=(250, 236, 206), cut=(3, 99.0), gamma=1.12); c = grade(c, sat=1.1, contrast=1.14, teal=0.06, warm=0.06)
    T = lambda x, y: ((x - box[0]) * s, (y - box[1]) * s)
    (x0, y0), (x1, y1) = T(1830, 1240), T(2290, 1950)                             # the cairn the men are pulling apart
    c = spot(c, (x0 + x1) / 2, (y0 + y1) / 2, 520, 360, lift=0.22, dark=0.30); c = vign(c, 0.45)   # light pool on the cairn + men
    ring(c, (x0 - 10, y0 - 14, x1 + 10, y1 + 8), w=10)
    note = src(EP, "B1_")
    z = grade(note.crop((120, 280, 720, 880)), sat=1.15, contrast=1.2, teal=0.04, warm=0.12)   # "H.M.S. Ships Erebus and Terror / 28 of May 1847"
    bubble(c, z, 1078, 170, 140, src_xy=((x0 + x1) / 2 + 30, y0 + 40), src_r=40)
    block(c, "FOUND", 30, 92, 132)
    block(c, "11 YEARS LATER", 30, 648, 104, fill=BLACK, bg=YEL + (255,))
    block(c, "6 MAY 1859", 1078, 352, 54, fill=WHITE, bg=RED + (255,), anchor="m")              # the date, big
    return c

# ------------------------------------------------------------------ N5: the real 1850 reward poster, £20,000 circled
def N5():
    im = src(EP, "C1_"); box = (0, 8, 726, 416)                                   # £20,000 REWARD / Her Majesty's Government / DISCOVERY SHIPS
    c = grade(win(im, box), sat=1.15, contrast=1.18, teal=0.10, warm=0.10); c = vign(c, 0.6)
    s = TW / 726; T = lambda x, y: ((x - box[0]) * s, (y - box[1]) * s)
    (x0, y0), (x1, y1) = T(128, 22), T(588, 112)
    ring(c, (x0 - 26, y0 - 20, x1 + 26, y1 + 16), w=11)
    two_lines(c, "NO ONE", "SAVED THEM", 30, 500, 640, 128, 760, st1=(WHITE, RED + (255,)), st2=(BLACK, YEL + (255,)))
    tag(c, "7 MARCH 1850", 22, 34, size=32)                                       # top-left, clear of the ring
    return c

OPTIONS = [("N1_105_WALKED", N1, "B1 note: '105 souls' circled + zoom"), ("N2_WHAT_HAPPENED_TO_CROZIER", N2, "A2 Crozier + his 1848 signature"),
           ("N3_WHY_ABANDON_SHIP", N3, "C5 McClintock 1859 map + D2 ship"), ("N4_FOUND_11_YEARS_LATER", N4, "D15 ILN 1859 cairn + B1 note"),
           ("N5_NO_ONE_SAVED_THEM", N5, "C1 1850 reward poster")]

def sheet(items, path):
    """every option at full size (left) and at phone size, 320 px wide (right), plus a phone-size row of all of them on top"""
    lab = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30); small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    PW, PH = 320, 180; G = 30; rowh = TH + 70
    top = 70 + PH + 60; W = TW + G * 3 + PW; H = top + len(items) * rowh + G
    S = Image.new("RGB", (W, H), (28, 28, 28)); d = ImageDraw.Draw(S)
    d.text((G, 20), "PHONE SIZE (320 px wide), side by side", font=lab, fill=(255, 204, 0))
    for i, (n, im, note) in enumerate(items):
        x = G + i * (PW + 14)
        if x + PW > W: break
        S.paste(im.resize((PW, PH), Image.LANCZOS), (x, 70)); d.text((x, 70 + PH + 8), n.split("_")[0], font=small, fill=(230, 230, 230))
    for i, (n, im, note) in enumerate(items):
        y = top + i * rowh
        d.text((G, y), n, font=lab, fill=(255, 204, 0)); d.text((G + 620, y + 6), note, font=small, fill=(200, 200, 200))
        S.paste(im, (G, y + 45)); S.paste(im.resize((PW, PH), Image.LANCZOS), (TW + 2 * G, y + 45))
        d.text((TW + 2 * G, y + 45 + PH + 8), "phone size", font=small, fill=(200, 200, 200))
    S.save(path)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); items = []
    only = sys.argv[1:]
    for name, fn, note in OPTIONS:
        if only and name.split("_")[0] not in only: continue
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); items.append((name, im, note))
        print(name)
    if not only: sheet(items, OUT + "_sheet.png"); print(OUT + "_sheet.png")
