"""14 Nov 2026: re-thumbnails for old weak long videos in the @sparrow0y0 look, adapted to The Last Hours.
Look: dark grain background, ONE big real B&W subject (cut out), ONE accent colour, a huge word BEHIND the subject
and a white word in FRONT with a horizontal slice, a thin accent frame, the date in an accent block, a small channel tag.
Real archival images only (no AI, no cartoons, no women). Output: out/<key>.jpg + sheet.jpg
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

NC = "D:/why habibi/_newchannel/"
OUT = NC + "_rethumb_nov14/out/"
os.makedirs(OUT, exist_ok=True)
W, H = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"
BLACK = "C:/Windows/Fonts/ariblk.ttf"
rng = np.random.default_rng(7)


def font(p, s):
    return ImageFont.truetype(p, s)


def background(accent, spot=(0.62, 0.45)):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x / W - spot[0]) * 1.6) ** 2 + ((y / H - spot[1])) ** 2)
    base = np.array([9, 11, 18], np.float32)
    glow = np.clip(1 - d * 1.35, 0, 1)[..., None]
    acc = np.array(accent, np.float32)
    img = base + glow * (np.array([34, 36, 46], np.float32) + acc * 0.10)
    img += rng.normal(0, 7, (H, W, 1))                      # film grain
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def cutout(path, crop=None, seeds=None, thresh=38, erode=3, feather=2):
    """flood-fill the plain studio background from the given seed points -> RGBA subject"""
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    w, h = im.size
    probe = im.copy()
    seeds = seeds or [(2, 2), (w - 3, 2), (2, h // 3), (w - 3, h // 3)]
    for s in seeds:
        ImageDraw.floodfill(probe, s, (255, 0, 255), thresh=thresh)
    a = np.array(probe)
    m = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    mask = Image.fromarray((m * 255).astype(np.uint8))
    mask = mask.filter(ImageFilter.MinFilter(erode * 2 + 1)).filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def bw(im, contrast=1.35, gamma=0.9):
    a = im.getchannel("A") if im.mode == "RGBA" else None
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    arr = np.asarray(g, np.float32) / 255
    arr = np.clip((arr - 0.5) * contrast + 0.5, 0, 1) ** gamma
    g = Image.fromarray((arr * 255).astype(np.uint8)).convert("RGBA")
    if a is not None:
        g.putalpha(a)
    return g


def fit_h(im, h):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def text_layer(s, size, fill, fnt=IMPACT, slice_col=None, slice_at=0.56, slice_h=10, tracking=0):
    f = font(fnt, size)
    bb = f.getbbox(s)
    tw, th = bb[2] - bb[0] + tracking * len(s), bb[3] - bb[1]
    lay = Image.new("RGBA", (tw + 20, th + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = 10 - bb[0]
    for ch in s:
        d.text((x, 10 - bb[1]), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking
    if slice_col:                                           # the sparrow "slice", inside the glyphs only (no strikethrough look):
        y0 = int(10 + th * 0.80)                            # a thin gap low in the letters, the part below nudged right,
        arr = np.array(lay)                                 # and an accent stripe only where the letters are
        lower = arr[y0 + slice_h:].copy()
        arr[y0:] = 0
        arr[y0 + slice_h:, 6:] = lower[:, :-6]
        band = arr[y0 + slice_h: y0 + slice_h + 7]
        on = band[..., 3] > 0
        band[on, 0], band[on, 1], band[on, 2] = slice_col[0], slice_col[1], slice_col[2]
        lay = Image.fromarray(arr)
    return lay


def shadow(lay, r=14, k=200):
    a = lay.getchannel("A").filter(ImageFilter.GaussianBlur(r))
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: min(255, v * k // 255)))
    return sh


def put(c, lay, x, y, sh=True):
    if sh:
        c.alpha_composite(shadow(lay), (x + 6, y + 10))
    c.alpha_composite(lay, (x, y))


def chip(c, s, x, y, accent, size=46, fg=(10, 10, 12)):
    f = font(BLACK, size)
    bb = f.getbbox(s)
    d = ImageDraw.Draw(c)
    d.rectangle([x, y, x + bb[2] - bb[0] + 36, y + bb[3] - bb[1] + 26], fill=accent + (255,))
    d.text((x + 18 - bb[0], y + 13 - bb[1]), s, font=f, fill=fg)


def finish(c, accent, key, tag=True):
    d = ImageDraw.Draw(c)
    if tag:
        f = font(BLACK, 22)
        d.text((W - 34, 28), "#THELASTHOURS", font=f, fill=(235, 235, 235), anchor="ra")
    d.rectangle([0, 0, W - 1, H - 1], outline=accent + (255,), width=9)   # thin accent frame
    c.convert("RGB").save(OUT + key + ".jpg", quality=92)
    print("saved", key)


def subject_with_rim(c, subj, x, y, accent, rim=5):
    if rim <= 0:
        c.alpha_composite(subj, (x, y))
        return
    a = subj.getchannel("A")
    big = a.filter(ImageFilter.MaxFilter(rim * 2 + 1))
    rimlay = Image.new("RGBA", subj.size, accent + (0,))
    rimlay.putalpha(big)
    c.alpha_composite(rimlay, (x, y))
    c.alpha_composite(subj, (x, y))


# ---------------------------------------------------------------- Alcatraz (accent orange)
ORANGE = (255, 122, 26)
def alc_A():     # Frank Morris's FBI mugshot huge; NEVER behind, FOUND in front
    c = background(ORANGE, (0.66, 0.42)).convert("RGBA")
    put(c, text_layer("NEVER", 330, ORANGE + (255,)), 40, 10, sh=False)
    s = bw(cutout(NC + "01_alcatraz/media/A1_fbi_morris.jpg", thresh=34))
    s = fit_h(s, 820)
    subject_with_rim(c, s, W - s.width + 40, 60, ORANGE, rim=0)
    put(c, text_layer("FOUND.", 230, (255, 255, 255, 255), slice_col=ORANGE + (255,)), 40, 330)
    chip(c, "JUNE 11, 1962", 48, 600, ORANGE)
    finish(c, ORANGE, "alcatraz_A")


def alc_B():     # the real plaster dummy head huge; IT WAS / A DUMMY
    c = background(ORANGE, (0.66, 0.5)).convert("RGBA")
    im = Image.open(NC + "01_alcatraz/media/dummy_head_morris.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.02), int(h * 0.0), int(w * 0.98), int(h * 0.92)))
    s = bw(im.convert("RGBA"), contrast=1.3, gamma=1.15)
    s = fit_h(s, 720)
    ma = np.clip(np.linspace(0, 7.0, s.width), 0, 1)[None, :] * np.ones((s.height, 1))
    s.putalpha(Image.fromarray((ma * 255).astype(np.uint8)))
    c.alpha_composite(s, (W - s.width, 0))
    put(c, text_layer("DUMMY", 200, ORANGE + (255,)), 30, 360)
    put(c, text_layer("IT WAS A", 150, (255, 255, 255, 255), slice_col=ORANGE + (255,)), 44, 90)
    chip(c, "JUNE 11, 1962", 48, 28, ORANGE, size=36)
    finish(c, ORANGE, "alcatraz_B")


# ---------------------------------------------------------------- Franklin (accent ice blue)
ICE = (64, 170, 255)
def fr_A():      # Franklin's own 1845 daguerreotype, face big on the right; 129 behind, MEN. GONE. in front
    c = background(ICE, (0.68, 0.4)).convert("RGBA")
    put(c, text_layer("129", 430, ICE + (255,)), 30, -30, sh=False)
    im = Image.open(NC + "03_franklin/media/A1_sir_john_franklin_captain_of_erebus_ex.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.24), int(h * 0.17), int(w * 0.76), int(h * 0.72)))
    s = bw(im.convert("RGBA"), contrast=1.3)
    s = fit_h(s, 720)
    m = Image.new("L", s.size, 0)                         # soft left edge so the plate melts into the dark
    ma = np.tile(np.clip(np.linspace(0, 3.2, s.width), 0, 1), (s.height, 1))
    s.putalpha(Image.fromarray((ma * 255).astype(np.uint8)))
    c.alpha_composite(s, (W - s.width, 0))
    put(c, text_layer("MEN. GONE.", 160, (255, 255, 255, 255), slice_col=ICE + (255,)), 40, 400)
    chip(c, "1845 - 1848", 48, 610, ICE)
    finish(c, ICE, "franklin_A")


def fr_B():      # the real 1848 Victory Point note, tilted big; ALL WELL? behind/in front
    c = background(ICE, (0.6, 0.5)).convert("RGBA")
    put(c, text_layer("ALL", 300, ICE + (255,)), 30, 20, sh=False)
    note = Image.open(NC + "03_franklin/media/B1_victory_point_record_1847_1848_message.jpg").convert("RGB")
    note = bw(note.convert("RGBA"), contrast=1.15, gamma=1.0)
    note = fit_h(note, 760).rotate(-6, expand=True, resample=Image.BICUBIC)
    put(c, note, W - note.width + 30, -30)
    put(c, text_layer("WELL?", 230, (255, 255, 255, 255), slice_col=ICE + (255,)), 40, 300)
    chip(c, "APRIL 25, 1848", 48, 610, ICE)
    finish(c, ICE, "franklin_B")


# ---------------------------------------------------------------- D.B. Cooper (accent red)
RED = (232, 40, 40)
def co_A():      # the FBI sketch (no glasses) huge; WHO behind, WAS HE? in front
    c = background(RED, (0.66, 0.45)).convert("RGBA")
    put(c, text_layer("WHO", 360, RED + (255,)), 30, -10, sh=False)
    src = NC + "04_dbcooper/media/A7_composite_sketch_a_nov_1971_the_same_m.jpg"
    im = Image.open(src).convert("RGB"); w, h = im.size
    s = cutout(src, crop=(0, 0, w // 2, h), thresh=24, erode=1, feather=1)
    s = bw(s, contrast=1.5, gamma=1.0)
    s = fit_h(s, 760)
    c.alpha_composite(s, (W - s.width + 30, 20))
    put(c, text_layer("WAS HE?", 210, (255, 255, 255, 255), slice_col=RED + (255,)), 40, 350)
    chip(c, "NOV. 24, 1971", 48, 605, RED)
    finish(c, RED, "cooper_A")


def co_B():      # sketch WITH the sunglasses huge; $200,000 behind, GONE. in front
    c = background(RED, (0.66, 0.45)).convert("RGBA")
    put(c, text_layer("$200,000", 200, RED + (255,)), 26, 30, sh=False)
    src = NC + "04_dbcooper/media/A7_composite_sketch_a_nov_1971_the_same_m.jpg"
    im = Image.open(src).convert("RGB"); w, h = im.size
    s = cutout(src, crop=(w // 2, 0, w, h), thresh=24, erode=1, feather=1)
    s = bw(s, contrast=1.5, gamma=1.0)
    s = fit_h(s, 760)
    c.alpha_composite(s, (W - s.width + 20, 20))
    put(c, text_layer("HE JUMPED.", 170, (255, 255, 255, 255), slice_col=RED + (255,)), 40, 380)
    chip(c, "NOV. 24, 1971", 48, 605, RED)
    finish(c, RED, "cooper_B")


# ---------------------------------------------------------------- Roanoke (accent yellow)
YEL = (255, 200, 0)
def ro_A():      # the 1876 engraving of the men finding the carved post, big; 115 behind, GONE. in front
    c = background(YEL, (0.62, 0.45)).convert("RGBA")
    im = Image.open(NC + "05_roanoke/media/A14_croatoan_wood_engraving_1876_design_w.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.02), int(h * 0.02), int(w * 0.62), int(h * 0.98)))
    s = bw(im.convert("RGBA"), contrast=1.45, gamma=1.1)
    s = fit_h(s, 720)
    ma = np.tile(np.clip(np.linspace(0, 2.6, s.width), 0, 1), (s.height, 1))
    s.putalpha(Image.fromarray((ma * 255).astype(np.uint8)))
    put(c, text_layer("115", 420, YEL + (255,)), 20, -20, sh=False)
    c.alpha_composite(s, (W - s.width, 0))
    put(c, text_layer("GONE.", 220, (255, 255, 255, 255), slice_col=YEL + (255,)), 40, 330)
    chip(c, "AUGUST 18, 1590", 48, 605, YEL)
    finish(c, YEL, "roanoke_A")


def ro_B():      # Raleigh's 1588 portrait, face huge; ONE WORD / WAS LEFT + CROATOAN chip
    c = background(YEL, (0.7, 0.4)).convert("RGBA")
    im = Image.open(NC + "05_roanoke/media/B1_sir_walter_raleigh_1588_national_portr.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.18), int(h * 0.04), int(w * 0.78), int(h * 0.56)))
    s = bw(im.convert("RGBA"), contrast=1.35)
    s = fit_h(s, 720)
    ma = np.tile(np.clip(np.linspace(0, 2.8, s.width), 0, 1), (s.height, 1))
    s.putalpha(Image.fromarray((ma * 255).astype(np.uint8)))
    c.alpha_composite(s, (W - s.width, 0))
    put(c, text_layer("CROATOAN", 190, YEL + (255,)), 30, 230)
    put(c, text_layer("ONE WORD.", 150, (255, 255, 255, 255), slice_col=YEL + (255,)), 40, 40)
    chip(c, "115 PEOPLE GONE", 48, 610, YEL)
    finish(c, YEL, "roanoke_B")


ALL = {"alcatraz_A": alc_A, "alcatraz_B": alc_B, "franklin_A": fr_A, "franklin_B": fr_B,
       "cooper_A": co_A, "cooper_B": co_B, "roanoke_A": ro_A, "roanoke_B": ro_B}


def sheet():
    keys = list(ALL)
    tw, th = 640, 360
    s = Image.new("RGB", (tw * 2 + 30, (th + 50) * 4 + 10), (250, 250, 250))
    d = ImageDraw.Draw(s)
    f = font(BLACK, 22)
    for i, k in enumerate(keys):
        im = Image.open(OUT + k + ".jpg").resize((tw, th), Image.LANCZOS)
        x, y = 10 + (i % 2) * (tw + 10), 10 + (i // 2) * (th + 50)
        s.paste(im, (x, y + 34))
        d.text((x, y + 4), k.replace("_", "  "), font=f, fill=(20, 20, 20))
    s.save(OUT + "sheet.jpg", quality=90)


if __name__ == "__main__":
    for k in (sys.argv[1:] or ALL):
        ALL[k]()
    sheet()
