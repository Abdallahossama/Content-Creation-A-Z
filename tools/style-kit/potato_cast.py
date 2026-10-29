"""Potato cast v2 (2026-10-14). Many characters from our one real potato photo (no AI), drawn costumes only.
User notes on v1: squashing/stretching looked like broken perspective; some hats floated above the head.
v2: never non-uniform scaling (variety = skin, size, mirror, lean, face, outfit, headwear); every hat is anchored to the
row where the potato's head is as wide as the hat's band, and overlaps the head, so it sits ON it.
  skin     : russet (our Batata), red, gold, pale
  face     : batata2 expressions (shocked, panic, sideeye, smug, sad, sleepy, fine, deadpan, cool) or "confident"
  outfit   : none, suit, thobe, galabeya, pajamas, labcoat, doctor, hivis, general, pilot, hoodie
  headwear : none, ghutra (white), shemagh (red-white), taqiyah, captain, pilot, hardhat, nightcap, bicorne
  extra    : aviators (pilot sunglasses)
cast(...) -> RGBA (transparent, standing on its flat bottom, soft contact shadow)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from batata_boss import POT, ALPHA, ink_onto, v2_layer, confident, suit, shaded

Wp, Hp = POT.size; TOP = 340
SOLID = np.asarray(ALPHA) > 128
INK = (22, 18, 16)

def span(y):
    xs = np.where(SOLID[int(y)])[0]; return int(xs.min()), int(xs.max())

def row_for_width(w):
    """first row from the top where the potato is at least w px wide (the head is narrow at the top)"""
    for y in range(0, Hp):
        a, b = span(y) if SOLID[y].any() else (0, -1)
        if b - a >= w: return y, (a + b) / 2
    return Hp // 2, Wp / 2

def skin(kind):
    a = np.asarray(POT, np.float32).copy()
    if kind == "red":    a[..., :3] = a[..., :3].mean(-1, keepdims=True) * np.array([1.25, 0.66, 0.62]) + a[..., :3] * 0.15
    elif kind == "gold": a[..., :3] *= np.array([1.12, 1.02, 0.66])
    elif kind == "pale": a[..., :3] *= np.array([1.08, 1.06, 0.98])
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")

# ---------------------------------------------------------------- outfits (potato coords, lower third)
def body_mask(top_c=1062, top_s=1090):
    body = ALPHA.filter(ImageFilter.MaxFilter(25)); cut = Image.new("L", POT.size, 0)
    ImageDraw.Draw(cut).polygon([(0, top_s + 60), (150, top_s), (330, top_c + 4), (520, top_c), (710, top_c + 4), (890, top_s), (Wp, top_s + 60), (Wp, Hp), (0, Hp)], fill=255)
    return Image.fromarray(np.minimum(np.asarray(body), np.asarray(cut)))

def _clip(mask, poly=None, box=None):
    m = Image.new("L", POT.size, 0); d = ImageDraw.Draw(m)
    if poly: d.polygon(poly, fill=255)
    if box: d.rectangle(box, fill=255)
    return Image.fromarray(np.minimum(np.asarray(m), np.asarray(mask)))

def _wear(im, mask, hi, lo, light=(0.3, 0.0), noise=4, seed=1):
    out = im.copy(); sh = Image.new("RGBA", POT.size, (0, 0, 0, 0))
    sh.putalpha(mask.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.5)))
    from PIL import ImageChops
    out.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", POT.size, (0, 0, 0)).split(), ImageChops.offset(sh, 0, -14).getchannel("A"))))
    out.alpha_composite(shaded(mask, np.array(hi, float), np.array(lo, float), light=light, noise=noise, seed=seed))
    return out

def _finish(out, mask):
    out.putalpha(Image.fromarray(np.maximum(np.asarray(ALPHA), np.asarray(mask)))); return out

def robe(im, hi, lo, collar="round", trim=None, buttons=3, seed=2):
    m = body_mask(); out = _wear(im, m, hi, lo, seed=seed); d = ImageDraw.Draw(out)
    for k in range(5):                                                   # soft vertical folds
        x = 260 + k * 130; d.line((x, 1140, x + (k - 2) * 14, Hp), fill=tuple(int(v * 0.86) for v in lo) + (90,), width=8)
    if collar == "round":
        d.chord((420, 1030, 620, 1130), 0, 180, fill=tuple(int(v * 0.8) for v in lo) + (255,))
        d.arc((420, 1030, 620, 1130), 0, 180, fill=INK + (200,), width=5)
    else:                                                                # V neck slit
        d.polygon([(450, 1066), (590, 1066), (520, 1220)], fill=tuple(int(v * 0.7) for v in lo) + (255,))
        if trim: d.line([(450, 1066), (520, 1220), (590, 1066)], fill=trim + (255,), width=12)
    for k in range(buttons): d.ellipse((510, 1150 + k * 70, 532, 1172 + k * 70), fill=(235, 235, 230, 255), outline=(120, 120, 120, 255), width=3)
    return _finish(out, m)

def thobe(im):    return robe(im, (252, 252, 248), (204, 204, 198), collar="round", buttons=3)
def galabeya(im): return robe(im, (182, 204, 222), (112, 136, 160), collar="v", trim=(40, 60, 110), buttons=0, seed=3)

def pajamas(im):
    out = robe(im, (150, 188, 238), (84, 118, 186), collar="v", trim=(250, 250, 250), buttons=3, seed=4); m = body_mask()
    st = Image.new("RGBA", POT.size, (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    for x in range(0, Wp, 70): d.line((x, 1040, x, Hp), fill=(245, 248, 255, 150), width=18)
    st.putalpha(Image.fromarray(np.minimum(np.asarray(st.getchannel("A")), np.asarray(m)))); out.alpha_composite(st); return out

def labcoat(im, doctor=False):
    m = body_mask(); out = _wear(im, m, (252, 252, 252), (200, 204, 212), seed=5); d = ImageDraw.Draw(out)
    d.polygon([(400, 1062), (640, 1062), (520, 1400)], fill=(86, 136, 200, 255))                                   # blue shirt in the opening
    for a, b in (((400, 1062), (520, 1400)), ((640, 1062), (520, 1400))): d.line([a, b], fill=(150, 154, 166, 255), width=8)
    d.polygon([(400, 1062), (330, 1070), (380, 1200), (350, 1222), (470, 1400)], fill=(236, 238, 242, 255), outline=(170, 172, 182, 255))
    d.polygon([(640, 1062), (710, 1070), (660, 1200), (690, 1222), (570, 1400)], fill=(236, 238, 242, 255), outline=(170, 172, 182, 255))
    d.rectangle((700, 1260, 800, 1290), fill=(70, 120, 200, 255))                                                   # pen in the pocket
    if doctor:
        d.arc((380, 980, 660, 1250), 20, 160, fill=(70, 74, 82, 255), width=16); d.line((402, 1160, 380, 1300), fill=(70, 74, 82, 255), width=14)
        d.ellipse((350, 1290, 410, 1350), fill=(190, 194, 204, 255), outline=(70, 74, 82, 255), width=8)
    return _finish(out, m)

def doctor(im): return labcoat(im, doctor=True)

def hivis(im):
    m = body_mask(); out = _wear(im, m, (120, 124, 132), (70, 74, 82), seed=6)
    vest = _clip(m, poly=[(0, 1100), (420, 1062), (520, 1300), (620, 1062), (Wp, 1100), (Wp, Hp), (0, Hp)])
    out.alpha_composite(shaded(vest, np.array([255, 150, 30.0]), np.array([214, 96, 0.0]), seed=7)); d = ImageDraw.Draw(out)
    band = Image.new("RGBA", POT.size, (0, 0, 0, 0)); db = ImageDraw.Draw(band)
    for y in (1290, 1380): db.rectangle((0, y, Wp, y + 34), fill=(230, 236, 240, 255))
    band.putalpha(Image.fromarray(np.minimum(np.asarray(band.getchannel("A")), np.asarray(vest)))); out.alpha_composite(band)
    return _finish(out, m)

def general(im):
    out = robe(im, (44, 58, 120), (14, 18, 52), collar="round", buttons=0, seed=8); d = ImageDraw.Draw(out)
    d.chord((420, 1030, 620, 1130), 0, 180, fill=(190, 30, 34, 255))
    for k in range(4):
        for x in (470, 570): d.ellipse((x - 14, 1150 + k * 66, x + 14, 1178 + k * 66), fill=(232, 190, 60, 255), outline=(150, 110, 10, 255), width=3)
    for x0 in (60, 860):                                                  # gold epaulettes with fringe
        d.rounded_rectangle((x0, 1080, x0 + 150, 1120), 18, fill=(232, 190, 60, 255))
        for k in range(8): d.line((x0 + 10 + k * 18, 1120, x0 + 10 + k * 18, 1160), fill=(212, 166, 40, 255), width=7)
    return out

def pilot_uniform(im):
    out = suit(im); d = ImageDraw.Draw(out)
    d.polygon([(500, 1100), (540, 1100), (532, 1160), (508, 1160)], fill=(20, 26, 60, 255))                         # navy tie knot over the yellow
    d.polygon([(508, 1160), (532, 1160), (556, 1400), (520, 1450), (484, 1400)], fill=(24, 30, 70, 255))
    d.polygon([(230, 1200), (330, 1186), (300, 1214), (260, 1222)], fill=(232, 190, 60, 255))                       # gold wings
    d.polygon([(330, 1186), (420, 1200), (390, 1222), (340, 1214)], fill=(232, 190, 60, 255))
    for x0 in (90, 830): d.rounded_rectangle((x0, 1096, x0 + 140, 1126), 10, fill=(16, 18, 30, 255)); d.line((x0 + 10, 1111, x0 + 130, 1111), fill=(232, 190, 60, 255), width=6)
    return out

def hoodie(im):
    out = robe(im, (150, 154, 162), (92, 96, 106), collar="round", buttons=0, seed=9); d = ImageDraw.Draw(out)
    for x in (480, 560): d.line((x, 1110, x - 6, 1260), fill=(240, 240, 240, 255), width=9); d.ellipse((x - 14, 1252, x + 2, 1270), fill=(240, 240, 240, 255))
    d.rounded_rectangle((330, 1330, 710, Hp), 40, outline=(80, 84, 94, 255), width=8)                                # front pocket
    return out


def _fur_texture(out, mask, col, seed=5, n=900):
    """short marker strokes for fur inside a mask"""
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(out); m = np.asarray(mask); ys, xs = np.nonzero(m > 128)
    if len(xs) == 0: return
    for i in rng.integers(0, len(xs), n):
        x, y = xs[i], ys[i]; a = rng.uniform(1.2, 1.9); L = rng.uniform(14, 30)
        d.line((x, y, x + L * np.cos(a), y + L * np.sin(a)), fill=col + (int(rng.uniform(90, 170)),), width=4)
def fur_cape(im):
    """a draped hide over the shoulders (ice-age 'simple clothing'), jagged hem, bone pin"""
    m = body_mask(); rng = np.random.default_rng(3); hem = [(Wp, 1330)]
    for k in range(14): x = Wp - (k + 1) * Wp / 14; hem.append((x, 1330 + (60 if k % 2 else 0) + rng.uniform(-20, 20)))
    cape = _clip(m, poly=[(0, 1000), (Wp, 1000)] + hem + [(0, 1330)])
    out = _wear(im, cape, (168, 118, 70), (92, 60, 32), seed=11); _fur_texture(out, cape, (60, 36, 18), seed=4)
    d = ImageDraw.Draw(out); d.line((470, 1110, 590, 1150), fill=(240, 232, 210, 255), width=18); d.ellipse((450, 1098, 482, 1126), fill=(240, 232, 210, 255))
    return _finish(out, cape)
def fur_parka(im):
    """fitted, sewn clothing (needle era): full body, fur trim collar, a stitched seam"""
    m = body_mask(); out = _wear(im, m, (182, 140, 92), (104, 72, 40), seed=12); _fur_texture(out, m, (70, 46, 24), seed=6, n=700)
    d = ImageDraw.Draw(out)
    for y in range(1150, Hp, 34): d.line((520, y, 520, y + 18), fill=(40, 26, 14, 255), width=6); d.line((508, y + 9, 532, y + 9), fill=(40, 26, 14, 255), width=4)
    collar = _clip(m, box=(0, 1040, Wp, 1120)); trim = Image.new("RGBA", POT.size, (246, 240, 228, 0)); trim.putalpha(collar); out.alpha_composite(trim)
    _fur_texture(out, collar, (210, 200, 185), seed=8, n=300)
    return _finish(out, m)

OUTFITS = {"none": lambda im: im, "suit": suit, "thobe": thobe, "galabeya": galabeya, "pajamas": pajamas, "labcoat": labcoat,
           "doctor": doctor, "hivis": hivis, "general": general, "pilot": pilot_uniform, "hoodie": hoodie,
           "fur_cape": fur_cape, "fur_parka": fur_parka}

# ---------------------------------------------------------------- headwear (canvas coords: potato top at y = TOP)
def _brim(width):
    y, cx = row_for_width(width); return cx, y + TOP

def captain_cap(d, navy=False):
    cx, y = _brim(700); crown = (24, 30, 64) if navy else (250, 250, 248)
    d.ellipse((cx - 370, y - 250, cx + 370, y - 20), fill=crown + (255,), outline=(40, 40, 50, 255), width=10)
    d.rectangle((cx - 330, y - 100, cx + 330, y + 10), fill=(18, 22, 38, 255))
    d.chord((cx - 300, y - 40, cx + 250, y + 120), 0, 180, fill=(12, 14, 24, 255))
    d.line((cx - 260, y + 2, cx + 220, y + 2), fill=(212, 170, 40, 255), width=12)
    d.ellipse((cx - 50, y - 96, cx + 50, y - 10), fill=(222, 178, 40, 255), outline=(150, 110, 10, 255), width=6)
    if navy:                                                              # pilot cap: gold wings on the badge
        d.polygon([(cx - 130, y - 70), (cx - 50, y - 60), (cx - 60, y - 40), (cx - 120, y - 46)], fill=(232, 190, 60, 255))
        d.polygon([(cx + 130, y - 70), (cx + 50, y - 60), (cx + 60, y - 40), (cx + 120, y - 46)], fill=(232, 190, 60, 255))

def hardhat(d):
    cx, y = _brim(760)
    d.chord((cx - 390, y - 330, cx + 390, y + 300), 180, 360, fill=(255, 196, 30, 255), outline=(150, 100, 0, 255), width=10)
    d.rounded_rectangle((cx - 450, y - 30, cx + 450, y + 20), 22, fill=(240, 176, 10, 255), outline=(150, 100, 0, 255), width=8)
    d.line((cx, y - 330, cx, y - 34), fill=(222, 160, 0, 255), width=30); d.arc((cx - 300, y - 290, cx + 40, y + 260), 200, 250, fill=(255, 238, 160, 230), width=16)

def bicorne(d):
    cx, y = _brim(640)
    d.polygon([(cx - 470, y + 30), (cx - 250, y - 200), (cx, y - 270), (cx + 250, y - 200), (cx + 470, y + 30), (cx, y - 10)], fill=(20, 20, 26, 255), outline=(70, 70, 80, 255))
    d.line((cx - 410, y + 18, cx + 410, y + 18), fill=(212, 170, 40, 255), width=12)
    for r, col in ((44, (30, 60, 160)), (24, (250, 250, 250)), (11, (200, 30, 30))): d.ellipse((cx + 110 - r, y - 150 - r, cx + 110 + r, y - 150 + r), fill=col + (255,))

def nightcap(d):
    cx, y = _brim(660)
    d.polygon([(cx - 320, y - 20), (cx - 120, y - 300), (cx + 160, y - 420), (cx + 470, y - 330), (cx + 520, y - 210), (cx + 300, y - 260), (cx + 320, y - 20)], fill=(70, 110, 210, 255), outline=(30, 50, 120, 255))
    for k in range(5): d.line((cx - 260 + k * 110, y - 40, cx - 60 + k * 100, y - 300 + k * 10), fill=(250, 250, 255, 160), width=14)
    d.rounded_rectangle((cx - 350, y - 60, cx + 350, y + 20), 40, fill=(250, 250, 252, 255), outline=(190, 196, 210, 255), width=6)
    d.ellipse((cx + 470, y - 250, cx + 590, y - 130), fill=(250, 250, 252, 255), outline=(190, 196, 210, 255), width=6)

def taqiyah(d):
    cx, y = _brim(600)
    d.chord((cx - 320, y - 240, cx + 320, y + 230), 180, 360, fill=(248, 248, 244, 255), outline=(170, 170, 160, 255), width=6)
    for yy in range(y - 200, y - 14, 34):
        for xx in range(int(cx - 280), int(cx + 280), 34): d.ellipse((xx, yy, xx + 8, yy + 8), fill=(214, 214, 206, 255))
    d.rectangle((cx - 322, y - 6, cx + 322, y + 26), fill=(236, 236, 230, 255))

def headcloth(can, red=True):
    """ghutra / shemagh draped over the head and down the sides, the face left open, a black agal on top"""
    m = Image.new("L", can.size, 0); md = ImageDraw.Draw(m)
    body = ALPHA.filter(ImageFilter.MaxFilter(61)); m.paste(body, (0, TOP))
    cut = Image.new("L", can.size, 0); cd = ImageDraw.Draw(cut)
    cd.polygon([(-200, TOP - 120), (Wp + 200, TOP - 120), (Wp + 200, TOP + 1250), (Wp - 60, TOP + 1250), (Wp - 190, TOP + 1066),
                (190, TOP + 1066), (60, TOP + 1250), (-200, TOP + 1250)], fill=255)          # drapes over the shoulders onto the thobe
    face = Image.new("L", can.size, 0); ImageDraw.Draw(face).ellipse((206, TOP + 350, 834, TOP + 1120), fill=255)
    cloth = np.minimum(np.asarray(m), np.asarray(cut)); cloth = np.where(np.asarray(face) > 0, 0, cloth)
    top_y, cx = row_for_width(10); dome = Image.new("L", can.size, 0)                                              # a little height above the head
    ImageDraw.Draw(dome).ellipse((cx - 330, TOP - 110, cx + 330, TOP + 260), fill=255); cloth = np.maximum(cloth, np.asarray(dome))
    cm = Image.fromarray(cloth.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    H2 = can.size[1]; yy, xx = np.mgrid[0:H2, 0:Wp].astype(np.float32)
    base = np.array([250, 250, 246.0]) - 30 * (np.abs(xx - Wp / 2) / (Wp / 2))[..., None]
    if red:
        pat = ((np.floor((xx + yy) / 44) + np.floor((xx - yy) / 44)) % 2 == 0) & ((np.floor(xx / 22) + np.floor(yy / 22)) % 2 == 0)
        base = np.where(pat[..., None], np.array([196, 36, 40.0]), base)
    folds = (np.sin(xx / 46 + yy / 300) * 10)[..., None]; col = (base + folds).clip(0, 255)
    lay = Image.fromarray(col.astype(np.uint8)).convert("RGBA"); lay.putalpha(cm)
    sh = Image.new("RGBA", can.size, (0, 0, 0, 0)); sh.putalpha(cm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.45)))
    can.alpha_composite(sh, (8, 10)); can.alpha_composite(lay)
    e = np.asarray(cm.filter(ImageFilter.MaxFilter(5)), np.int16) - np.asarray(cm, np.int16)
    ol = Image.new("RGBA", can.size, (110, 100, 90, 0)); ol.putalpha(Image.fromarray(e.clip(0, 200).astype(np.uint8))); can.alpha_composite(ol)
    d = ImageDraw.Draw(can); acx = row_for_width(10)[1]                                                          # agal: two thick black cords,
    for k, yc in enumerate((TOP + 230, TOP + 268)):                                                                # seen from the front = a curved band
        box = (acx - 400, yc - 70, acx + 400, yc + 70)
        d.arc(box, 8, 172, fill=(12, 12, 14, 255), width=30)
        d.arc((box[0] + 6, box[1] + 4, box[2] - 6, box[3] - 4), 30, 80, fill=(90, 90, 96, 255), width=6)        # a soft highlight on the cord

def aviators(d):
    for cx in (356, 704):
        d.ellipse((cx - 110, TOP + 540, cx + 110, TOP + 690), fill=(30, 36, 44, 240), outline=(212, 170, 40, 255), width=10)
        d.line((cx - 60, TOP + 575, cx - 20, TOP + 560), fill=(200, 210, 220, 200), width=8)
    d.line((466, TOP + 580, 594, TOP + 580), fill=(212, 170, 40, 255), width=10)

HEAD = {"none": None, "captain": lambda d: captain_cap(d), "pilot": lambda d: captain_cap(d, navy=True), "hardhat": hardhat,
        "bicorne": bicorne, "nightcap": nightcap, "taqiyah": taqiyah}

def cast(kind="russet", face="shocked", outfit="none", head="none", extra="none", height=300, flip=False, lean=0):
    im = ink_onto(skin(kind), confident() if face == "confident" else v2_layer(face))
    im = OUTFITS[outfit](im)
    can = Image.new("RGBA", (Wp, Hp + TOP), (0, 0, 0, 0)); can.alpha_composite(im, (0, TOP))
    if head in ("ghutra", "shemagh"): headcloth(can, red=(head == "shemagh"))
    elif HEAD.get(head): HEAD[head](ImageDraw.Draw(can))
    if extra == "aviators": aviators(ImageDraw.Draw(can))
    can = can.crop(can.getbbox())
    if flip: can = can.transpose(Image.FLIP_LEFT_RIGHT)
    if lean: can = can.rotate(lean, Image.BICUBIC, expand=True)
    k = height / Hp; can = can.resize((int(can.width * k), int(can.height * k)), Image.LANCZOS)    # uniform scale only
    out = Image.new("RGBA", (can.width + 40, can.height + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    w, h = can.size; ImageDraw.Draw(sh).ellipse((20 + w * 0.14, h - 8, 20 + w * 0.86, h + 22), fill=(30, 20, 10, 120))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5))); out.alpha_composite(can, (20, 0))
    return out
