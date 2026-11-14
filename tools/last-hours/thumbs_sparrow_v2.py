"""14 Nov 2026 v2: colourful, sparrow-exact re-thumbs (owner: "make it colorful ... same cut, same font, same everything").
Sparrow recipe copied:
- each line = left word(s) + a long baseline BAR + right word(s); the bar runs BEHIND the subject in the middle (the kashida "cut")
- Lalezar (sparrow's heavy display face; OFL, has Latin): light white-grey letters with a gradient and a coloured 3D offset
  (one colour or a multicolour run), plus a soft shadow
- dark navy background with a faint grid, colourful blurred blobs, film grain, a huge faint ghost word behind
- the subject in full colour (or tinted) with a coloured sticker outline, over the bars
- "#THELASTHOURS" tag top right in the same font; the date (owner rule) in the same 3D letter style
Real archival images only; no AI, no cartoons, no women. Output: out_v2/<key>.jpg + sheet.jpg
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

NC = "D:/why habibi/_newchannel/"
HERE = NC + "_rethumb_nov14/"
OUT = HERE + "out_v2/"
os.makedirs(OUT, exist_ok=True)
W, H = 1280, 720
LAL = HERE + "fonts/Lalezar-Regular.ttf"
IMPACT = "C:/Windows/Fonts/impact.ttf"
rng = np.random.default_rng(11)

RED, ORANGE, YELLOW, GREEN, BLUE, TEAL, PURPLE, PINK = (
    (238, 45, 62), (255, 138, 30), (255, 204, 0), (40, 200, 110), (40, 110, 255), (40, 225, 200), (150, 80, 255), (255, 70, 160))


def F(s, p=LAL):
    return ImageFont.truetype(p, s)


# ------------------------------------------------------------------ background
def background(blobs, base=(12, 13, 30), ghost=None, ghost_col=(46, 50, 88)):
    img = np.zeros((H, W, 3), np.float32) + np.array(base, np.float32)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    for (cx, cy, r, col, k) in blobs:                       # colourful soft blobs (sparrow corners)
        d = np.sqrt((x - cx * W) ** 2 + (y - cy * H) ** 2) / (r * W)
        a = np.clip(1 - d, 0, 1) ** 1.6 * k
        img = img * (1 - a[..., None]) + np.array(col, np.float32) * a[..., None]
    c = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))             # faint grid
    d = ImageDraw.Draw(g)
    for gx in range(0, W, 64):
        d.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 14), width=1)
    for gy in range(0, H, 64):
        d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 14), width=1)
    c.alpha_composite(g)
    if ghost:                                               # huge faint tall word behind everything (ARGON-style)
        f = F(380, IMPACT)
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).text((W // 2, H + 30), ghost, font=f, fill=ghost_col + (150,), anchor="ms")
        gl = gl.resize((W, H))
        c.alpha_composite(gl)
    return c


def grain(c, k=9):
    a = np.asarray(c.convert("RGB"), np.float32)
    a += rng.normal(0, k, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


# ------------------------------------------------------------------ sparrow letters
def glyph_mask(parts, size, bar_to=None):
    """parts = [(text, x)] drawn on one baseline; bar_to=(x0,x1) adds the long kashida bar between them"""
    f = F(size)
    m = Image.new("L", (W, size * 2), 0)
    d = ImageDraw.Draw(m)
    base = int(size * 1.25)
    for t, x in parts:
        d.text((x, base), t, font=f, fill=255, anchor="ls")
    if bar_to:
        th = max(10, int(size * 0.17))
        d.rectangle([bar_to[0], base - th, bar_to[1], base], fill=255)
    return m, base


def word_w(t, size):
    return F(size).getlength(t)


def sparrow_text(c, mask, y, colors, depth=7, face_top=(250, 250, 252), face_bot=(196, 198, 212)):
    """mask: L layer W wide; y: top where the mask is pasted. colours: 1 colour or a list -> horizontal multicolour 3D offset"""
    h = mask.height
    sh = Image.new("RGBA", (W, h), (0, 0, 0, 0))            # soft drop shadow
    sh.putalpha(mask.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 160 // 255))
    c.alpha_composite(sh, (10, y + 14))
    if isinstance(colors[0], int):
        colors = [colors]
    col = np.zeros((h, W, 3), np.float32)                   # coloured extrusion: a run of colours left -> right
    xs = np.linspace(0, len(colors) - 1, W)
    for i in range(W):
        a = int(np.floor(xs[i])); b = min(a + 1, len(colors) - 1); t = xs[i] - a
        col[:, i] = np.array(colors[a]) * (1 - t) + np.array(colors[b]) * t
    ext = Image.fromarray(col.astype(np.uint8)).convert("RGBA")
    for k in range(depth, 0, -1):
        e = ext.copy()
        e.putalpha(mask)
        c.alpha_composite(e, (int(k * 0.55), y + k))
    gy = np.linspace(0, 1, h)[:, None, None]                # white-grey gradient face
    face = (np.array(face_top) * (1 - gy) + np.array(face_bot) * gy) * np.ones((h, W, 3))
    fl = Image.fromarray(face.astype(np.uint8)).convert("RGBA")
    fl.putalpha(mask)
    c.alpha_composite(fl, (0, y))


def split_line(c, left, right, y, size, colors, gap=(520, 760), x0=46, x1=None, bar=True):
    """left text from x0, right text ending at x1; bar joins them behind the subject (gap = where the subject sits)"""
    x1 = x1 or W - 46
    lw, rw = word_w(left, size), word_w(right, size)
    rx = x1 - rw
    m, base = glyph_mask([(left, x0), (right, rx)], size, (x0 + lw - 4, rx + 4) if bar else None)
    sparrow_text(c, m, y - base, colors)


def plain_line(c, text, x, y, size, colors, anchor_right=False):
    w = word_w(text, size)
    if anchor_right:
        x = x - w
    m, base = glyph_mask([(text, x)], size)
    sparrow_text(c, m, y - base, colors, depth=max(3, size // 22))


# ------------------------------------------------------------------ subjects
def cutout(path, crop=None, thresh=38, seeds=None, erode=2, feather=2):
    im = Image.open(path).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    w, h = im.size
    probe = im.copy()
    for s in (seeds or [(2, 2), (w - 3, 2), (2, h // 3), (w - 3, h // 3)]):
        ImageDraw.floodfill(probe, s, (255, 0, 255), thresh=thresh)
    a = np.array(probe)
    m = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    mask = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(erode * 2 + 1)).filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def feathered(path, crop, shape="oval", soft=0.22):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h))).convert("RGBA")
    w, h = im.size
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    if shape == "oval":
        d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h * 0.45) / (h * 0.62)) ** 2)
        a = np.clip((1 - d) / soft, 0, 1)
        a[y > h * 0.45] = np.maximum(a[y > h * 0.45], np.clip((1 - np.abs(x - w / 2) / (w / 2)) / soft, 0, 1)[y > h * 0.45])
    else:
        a = np.ones((h, w), np.float32)
    im.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return im


def look(im, sat=1.15, contrast=1.15, tint=None, k=0.0, bright=1.0):
    a = im.getchannel("A")
    rgb = im.convert("RGB")
    rgb = ImageOps.autocontrast(rgb, cutoff=1)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Color(rgb).enhance(sat)
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    if tint:
        t = Image.new("RGB", rgb.size, tint)
        rgb = Image.blend(rgb, ImageOps.colorize(rgb.convert("L"), (12, 10, 30), tint).convert("RGB"), k)
    out = rgb.convert("RGBA")
    out.putalpha(a)
    return out


def fit_h(im, h):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def place(c, s, cx, top, outline=None, ow=7):
    x = int(cx - s.width / 2)
    if outline:                                             # coloured sticker outline (sparrow's teal rim)
        a = s.getchannel("A").point(lambda v: 255 if v > 110 else 0)
        big = a.filter(ImageFilter.MaxFilter(ow * 2 + 1)).filter(ImageFilter.GaussianBlur(1.5))
        ol = Image.new("RGBA", s.size, outline + (0,))
        ol.putalpha(big)
        c.alpha_composite(ol, (x, top))
    c.alpha_composite(s, (x, top))


def tag(c):
    d = ImageDraw.Draw(c)
    d.text((W - 40, 62), "#THELASTHOURS", font=F(38), fill=(245, 245, 248), anchor="rs")


def save(c, key):
    c = grain(c, 6)
    c.convert("RGB").save(OUT + key + ".jpg", quality=93)
    print("saved", key)


# ================================================================== layout helpers (v2b)
def card(path, crop=(0, 0, 1, 1), h=560, rot=-4, outline=(255, 255, 255), sat=1.3, contrast=1.15, bright=1.0, radius=18):
    im = Image.open(path).convert("RGB")
    w0, h0 = im.size
    im = im.crop((int(crop[0] * w0), int(crop[1] * h0), int(crop[2] * w0), int(crop[3] * h0))).convert("RGBA")
    im = look(im, sat=sat, contrast=contrast, bright=bright)
    im = fit_h(im, h)
    b = 9
    fr = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (0, 0, 0, 0))
    m = Image.new("L", fr.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, fr.width - 1, fr.height - 1], radius=radius + b, fill=255)
    col = Image.new("RGBA", fr.size, outline + (255,))
    fr.paste(col, (0, 0), m)
    mi = Image.new("L", im.size, 0)
    ImageDraw.Draw(mi).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radius, fill=255)
    fr.paste(im, (b, b), mi)
    return fr.rotate(rot, expand=True, resample=Image.BICUBIC)


def lineart(path, crop, h, ink=(250, 236, 205)):
    """engraving -> its lines only, in a light ink, on transparent (paper removed)"""
    im = Image.open(path).convert("L")
    w0, h0 = im.size
    im = im.crop((int(crop[0] * w0), int(crop[1] * h0), int(crop[2] * w0), int(crop[3] * h0)))
    im = ImageOps.autocontrast(im, cutoff=2)
    a = 255 - np.asarray(im, np.float32)
    a = np.clip((a - 40) * 1.6, 0, 255)
    out = Image.new("RGBA", im.size, ink + (0,))
    out.putalpha(Image.fromarray(a.astype(np.uint8)))
    return fit_h(out, h)


def bbox_x(s, cx):
    x = int(cx - s.width / 2)
    bb = s.getchannel("A").point(lambda v: 255 if v > 60 else 0).getbbox()
    return x, x + bb[0], x + bb[2]


def fit_size(t, max_w, size):
    while size > 60 and word_w(t, size) > max_w:
        size -= 4
    return size


def kashida(c, left, right, y, size, colors, gl, gr, m=22):
    """sparrow cut: left word(s) left of the subject, right word(s) right of it, the bar runs behind the subject"""
    s1 = fit_size(left, gl - m - 46, size)
    s2 = fit_size(right, W - 46 - gr - m, size)
    size = min(s1, s2)
    lw, rw = word_w(left, size), word_w(right, size)
    rx = W - 46 - rw
    mk, base = glyph_mask([(left, 46), (right, rx)], size, (46 + lw - 4, rx + 4))
    sparrow_text(c, mk, y - base, colors)


def compose(key, blobs, ghost, subj, cx, top, lines, accent, outline=None, extras=(), date=None, date_cols=None, date_right=False):
    c = background(blobs, ghost=ghost)
    x, gl, gr = bbox_x(subj, cx)
    for (l, r, y, size, cols) in lines:
        kashida(c, l, r, y, size, cols, gl, gr)
    place(c, subj, cx, top, outline=outline)
    for (t, xx, y, size, cols) in extras:
        plain_line(c, t, xx, y, size, cols)
    if date:
        plain_line(c, date, (W - 46) if date_right else 46, 690, 60, date_cols or [accent], anchor_right=date_right)
    tag(c)
    save(c, key)


# ================================================================== the 8 thumbnails
def alc_A():
    s = look(cutout(NC + "01_alcatraz/media/A1_fbi_morris.jpg", thresh=34), sat=0.0, contrast=1.3, tint=(255, 170, 120), k=0.35)
    compose("alcatraz_A", [(0.0, 0.0, 0.55, ORANGE, 0.75), (1.0, 1.0, 0.55, PURPLE, 0.7), (1.0, 0.0, 0.35, RED, 0.5)], "ALCATRAZ",
            fit_h(s, 700), W * 0.5, 40, [("3 MEN", "GONE", 250, 170, [ORANGE, RED, PURPLE]), ("NEVER", "FOUND", 470, 170, [ORANGE, RED, PURPLE])],
            ORANGE, outline=ORANGE, date="JUNE 11, 1962", date_cols=[ORANGE, RED])


def alc_B():
    s = card(NC + "01_alcatraz/media/B5_nps_dummy_morris.jpg", (0.30, 0.02, 0.97, 0.92), h=470, rot=-5, outline=YELLOW, sat=1.35)
    compose("alcatraz_B", [(0.0, 1.0, 0.6, ORANGE, 0.8), (1.0, 0.0, 0.5, BLUE, 0.7), (0.5, 0.0, 0.3, PINK, 0.35)], "1962",
            s, W * 0.5, 90, [("IT WAS", "A DUMMY", 250, 150, [YELLOW, ORANGE, RED]), ("HIS HEAD", "IN BED", 470, 150, [YELLOW, ORANGE, RED])],
            ORANGE, date="JUNE 11, 1962", date_cols=[ORANGE, RED])


def fr_A():
    s = card(NC + "03_franklin/media/A1_sir_john_franklin_captain_of_erebus_ex.jpg", (0.22, 0.14, 0.78, 0.80), h=560, rot=4, outline=TEAL, sat=1.5, bright=1.1)
    compose("franklin_A", [(0.0, 0.0, 0.55, BLUE, 0.85), (1.0, 1.0, 0.55, TEAL, 0.6), (1.0, 0.0, 0.35, PURPLE, 0.5)], "ARCTIC",
            s, W * 0.5, 50, [("129", "MEN", 250, 190, [TEAL, BLUE, PURPLE]), ("ALL", "GONE", 480, 190, [TEAL, BLUE, PURPLE])],
            TEAL, date="1845 - 1848", date_cols=[TEAL, BLUE])


def fr_B():
    s = card(NC + "03_franklin/media/B1_victory_point_record_1847_1848_message.jpg", (0, 0, 1, 1), h=600, rot=-5, outline=ORANGE, sat=1.5)
    compose("franklin_B", [(0.0, 1.0, 0.6, BLUE, 0.8), (1.0, 0.0, 0.45, ORANGE, 0.6), (1.0, 1.0, 0.35, TEAL, 0.5)], "1848",
            s, W * 0.5, 20, [("ALL", "WELL?", 330, 210, [ORANGE, PINK, BLUE]), ("LAST", "NOTE", 540, 150, [ORANGE, PINK, BLUE])],
            BLUE, date="APRIL 25, 1848", date_cols=[TEAL, BLUE])


def co_A():
    s = look(cutout(NC + "04_dbcooper/media/A10_composite_b_as_a_single_portrait_1973.jpg", thresh=30, erode=2), sat=1.4, contrast=1.2)
    compose("cooper_A", [(0.0, 0.0, 0.55, RED, 0.8), (1.0, 1.0, 0.55, BLUE, 0.7), (0.0, 1.0, 0.35, ORANGE, 0.45)], "FBI",
            fit_h(s, 660), W * 0.5, 70, [("WHO", "WAS HE?", 270, 190, [ORANGE, RED, BLUE]), ("$200,000", "GONE", 490, 140, [YELLOW, ORANGE, RED])],
            RED, outline=TEAL, date="NOV. 24, 1971", date_cols=[RED, PURPLE])


def co_B():
    src = NC + "04_dbcooper/media/A7_composite_sketch_a_nov_1971_the_same_m.jpg"
    s = look(cutout(src, crop=(0.5, 0, 1.0, 1.0), thresh=24, erode=1, feather=1), sat=0.0, contrast=1.5, tint=(255, 150, 160), k=0.3)
    compose("cooper_B", [(0.0, 1.0, 0.6, PURPLE, 0.8), (1.0, 0.0, 0.5, RED, 0.75), (1.0, 1.0, 0.3, ORANGE, 0.5)], "727",
            fit_h(s, 680), W * 0.5, 40, [("HE", "JUMPED", 260, 170, [RED, PINK, PURPLE]), ("NEVER", "FOUND", 480, 170, [RED, PINK, PURPLE])],
            RED, outline=RED, date="NOV. 24, 1971", date_cols=[RED, PURPLE])


def ro_A():
    s = card(NC + "05_roanoke/media/A14_croatoan_wood_engraving_1876_design_w.jpg", (0.04, 0.02, 0.60, 0.98), h=560, rot=-4, outline=YELLOW, sat=1.6, contrast=1.3)
    compose("roanoke_A", [(0.0, 0.0, 0.55, GREEN, 0.7), (1.0, 1.0, 0.55, YELLOW, 0.55), (1.0, 0.0, 0.35, TEAL, 0.5)], "CROATOAN",
            s, W * 0.5, 50, [("115", "GONE", 250, 190, [YELLOW, GREEN, TEAL]), ("ONE", "WORD", 480, 190, [YELLOW, GREEN, TEAL])],
            YELLOW, date="AUGUST 18, 1590", date_cols=[YELLOW, GREEN])


def ro_B():
    s = card(NC + "05_roanoke/media/B1_sir_walter_raleigh_1588_national_portr.jpg", (0.16, 0.03, 0.82, 0.58), h=540, rot=4, outline=YELLOW, sat=1.3, bright=1.1)
    compose("roanoke_B", [(0.0, 1.0, 0.6, YELLOW, 0.6), (1.0, 0.0, 0.5, GREEN, 0.65), (0.0, 0.0, 0.35, ORANGE, 0.5)], "1590",
            s, W * 0.5, 60, [("115", "GONE", 250, 190, [YELLOW, ORANGE, GREEN]), ("ONE", "WORD", 480, 190, [YELLOW, ORANGE, GREEN])],
            YELLOW, extras=(), date="AUGUST 18, 1590", date_cols=[YELLOW, GREEN])


ALL = {"alcatraz_A": alc_A, "alcatraz_B": alc_B, "franklin_A": fr_A, "franklin_B": fr_B,
       "cooper_A": co_A, "cooper_B": co_B, "roanoke_A": ro_A, "roanoke_B": ro_B}


def sheet():
    tw, th = 640, 360
    s = Image.new("RGB", (tw * 2 + 30, (th + 50) * 4 + 10), (250, 250, 250))
    d = ImageDraw.Draw(s)
    for i, k in enumerate(ALL):
        if not os.path.exists(OUT + k + ".jpg"):
            continue
        im = Image.open(OUT + k + ".jpg").resize((tw, th), Image.LANCZOS)
        x, y = 10 + (i % 2) * (tw + 10), 10 + (i // 2) * (th + 50)
        s.paste(im, (x, y + 34))
        d.text((x, y + 2), k.replace("_", "  "), font=F(30), fill=(20, 20, 20))
    s.save(OUT + "sheet.jpg", quality=90)


if __name__ == "__main__":
    for k in (sys.argv[1:] or ALL):
        ALL[k]()
    sheet()
