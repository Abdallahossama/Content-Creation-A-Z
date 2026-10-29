"""Batata "boss" trial (2026-10-14, user: "make the potato more handsome, like the reference"). The same REAL potato
(potato_cut.png, Pexels 33948200) with a grown-up marker face and a painted navy suit + brand-yellow tie, so in a
thumbnail he reads as a confident host, not a vegetable. Our own drawing, no AI.
Faces: confident (heavy brows, almond eyes, nose hint, smirk) / confident + stubble / the brand "cool" shades / shocked.
Writes mascot/batata_boss/Batata_boss_<face>.png (+ a comparison sheet); nothing in mascot/batata/ is touched."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from batata2 import POT, INK, line, arc, dot, lens, face as v2_face
from marker import strokes, circle_path, _noise

OUT = "D:/why habibi/_style_kit/mascot/batata_boss/"; os.makedirs(OUT, exist_ok=True)
Wp, Hp = POT.size; ALPHA = POT.getchannel("A")
C = np.array([520.0, 700.0])

def ink_onto(pot_rgba, lay):
    """multiply marker ink onto the skin (same recipe as batata2.draw: ink skips a little on the bumps)"""
    a = np.asarray(lay.getchannel("A"), np.float32) / 255; pot = np.asarray(pot_rgba, np.float32)
    lum = pot[..., :3].mean(-1); tex = lum - np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32)
    a = np.clip(a * (0.93 + tex / 60.0), 0, 1) * (pot[..., 3] / 255)
    pot[..., :3] *= (1 - a[..., None]) + a[..., None] * (np.array(INK, np.float32) / 255)
    return Image.fromarray(np.clip(pot, 0, 255).astype(np.uint8), "RGBA")

def quad(p0, c, p1, n=40, seed=0, wob=2.5):
    t = np.linspace(0, 1, n)[:, None]; p0, c, p1 = map(lambda v: np.array(v, float), (p0, c, p1))
    pts = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1
    return pts + np.stack([_noise(n, seed, wob), _noise(n, seed + 1, wob)], 1)

def brow(outer, inner, lift=0, thick=(24, 42), seed=0):
    """a filled, tapered marker eyebrow (thin outer end, heavy inner end)"""
    (x0, y0), (x1, y1) = outer, inner; y0 -= lift
    top = quad((x0, y0), ((x0 + x1) / 2, min(y0, y1) - 22), (x1, y1), seed=seed)
    tk = np.linspace(thick[0], thick[1], len(top))[:, None]
    return np.concatenate([top, (top + np.array([0, 1]) * tk)[::-1]])

def confident(stubble=False):
    lay = Image.new("RGBA", POT.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for b in (brow((226, 468), (440, 506), thick=(18, 40), seed=1), brow((814, 452), (600, 500), thick=(18, 40), seed=2)):
        d.polygon([tuple(p) for p in b], fill=INK + (255,))
    strokes(lay, [quad((248, 602), (346, 540), (446, 594), seed=3), quad((594, 594), (694, 540), (792, 602), seed=4)], INK, 28, seed=3)
    strokes(lay, [quad((266, 614), (346, 646), (430, 606), seed=5), quad((610, 606), (694, 646), (774, 614), seed=6)], INK, 12, seed=5)
    for cx in (356, 704):
        d.ellipse((cx - 31, 568, cx + 31, 630), fill=INK + (255,)); d.ellipse((cx + 4, 576, cx + 20, 592), fill=(0, 0, 0, 0))
    strokes(lay, [quad((532, 690), (566, 760), (522, 790), seed=7)], INK, 14, seed=7)                     # nose hint
    strokes(lay, [quad((428, 902), (520, 940), (628, 876), seed=8)], INK, 25, seed=8)                     # smirk
    strokes(lay, [line((632, 862), (650, 902), 9, 2)], INK, 16, seed=9)                                   # dimple
    if stubble:
        rng = np.random.default_rng(11); jaw = Image.new("L", POT.size, 0)
        ImageDraw.Draw(jaw).polygon([(232, 790), (262, 930), (330, 1010), (430, 1055), (520, 1068), (612, 1055), (712, 1010), (782, 930), (812, 790),
                                     (742, 850), (650, 960), (520, 990), (395, 960), (300, 850)], fill=255)
        ImageDraw.Draw(jaw).ellipse((400, 860, 660, 975), fill=0)                                       # keep the mouth clear
        jm = np.asarray(jaw) > 0; ys, xs = np.where(jm); pick = rng.choice(len(xs), 1900, replace=False)
        sl = Image.new("RGBA", POT.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sl)
        for i in pick:
            a = np.radians(rng.uniform(70, 110)); L = rng.uniform(7, 15); x, y = xs[i], ys[i]
            ds.line((x, y, x + L * np.cos(a), y + L * np.sin(a)), fill=INK + (int(rng.uniform(150, 235)),), width=5)
        lay.alpha_composite(sl)
    return lay

def v2_layer(expr):
    """the existing Batata v2 faces (cool, shocked, ...), drawn the same way as batata2.draw"""
    lay = Image.new("RGBA", POT.size, (0, 0, 0, 0))
    for k, (paths, w) in enumerate(v2_face(expr)):
        paths = [C + (p - C) * 1.2 for p in paths]
        if w == "fill":
            for p in paths: ImageDraw.Draw(lay).polygon([tuple(q) for q in p], fill=INK + (255,))
        elif isinstance(w, tuple):
            for p in paths: ImageDraw.Draw(lay).line([tuple(q) for q in p], fill=(0, 0, 0, 0), width=w[1], joint="curve")
        else: strokes(lay, paths, INK, w * 1.22, seed=k * 7 + 1)
    return lay

NAVY_HI, NAVY_LO = np.array([40, 54, 128.0]), np.array([10, 14, 42.0])
YEL_HI, YEL_LO = np.array([255, 214, 70.0]), np.array([214, 140, 0.0])

def shaded(mask, hi, lo, light=(0.25, 0.0), noise=5, seed=1):
    yy, xx = np.mgrid[0:Hp, 0:Wp].astype(np.float32); t = np.clip(((xx / Wp - light[0]) * 0.9 + (yy / Hp - light[1]) * 0.6), 0, 1)[..., None]
    col = hi * (1 - t) + lo * t + np.random.default_rng(seed).normal(0, noise, (Hp, Wp, 1))
    im = Image.fromarray(col.clip(0, 255).astype(np.uint8)).convert("RGBA"); im.putalpha(mask); return im

def suit(im, tie=True):
    """navy jacket wrapped round the potato's lower third, white shirt V + collar, brand-yellow tie, yellow pocket square"""
    body = ALPHA.filter(ImageFilter.MaxFilter(25)); cut = Image.new("L", POT.size, 0)
    ImageDraw.Draw(cut).polygon([(0, 1150), (150, 1090), (330, 1066), (520, 1062), (710, 1066), (890, 1090), (Wp, 1150), (Wp, Hp), (0, Hp)], fill=255)
    jacket = Image.fromarray(np.minimum(np.asarray(body), np.asarray(cut)))
    vee = [(392, 1060), (648, 1060), (520, 1410)]
    shirt_m = Image.new("L", POT.size, 0); ImageDraw.Draw(shirt_m).polygon(vee, fill=255)
    shirt_m = Image.fromarray(np.minimum(np.asarray(shirt_m), np.asarray(jacket)))
    out = im.copy()
    sh = Image.new("RGBA", POT.size, (0, 0, 0, 0)); sh.putalpha(jacket.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55)))
    out.alpha_composite(Image.fromarray(np.dstack([np.zeros((Hp, Wp, 3), np.uint8), np.asarray(ImageChopsShift(sh))])))
    out.alpha_composite(shaded(jacket, NAVY_HI, NAVY_LO, seed=2))
    lap = Image.new("L", POT.size, 0); dl = ImageDraw.Draw(lap)
    dl.polygon([(392, 1060), (300, 1068), (350, 1190), (318, 1214), (470, 1440), (520, 1410)], fill=255)                       # left lapel + notch
    dl.polygon([(648, 1060), (740, 1068), (690, 1190), (722, 1214), (570, 1440), (520, 1410)], fill=255)
    lap = Image.fromarray(np.minimum(np.asarray(lap), np.asarray(jacket)))
    out.alpha_composite(shaded(lap, NAVY_HI * 0.78, NAVY_LO * 0.7, light=(0.1, -0.1), seed=3))
    edge = ImageDraw.Draw(out)
    for a, b in [((392, 1060), (520, 1410)), ((648, 1060), (520, 1410)), ((350, 1190), (318, 1214)), ((690, 1190), (722, 1214))]:
        edge.line([a, b], fill=(6, 8, 26, 255), width=5)
    out.alpha_composite(shaded(shirt_m, np.array([252, 252, 250.0]), np.array([196, 200, 212.0]), light=(0.4, 0.0), noise=2, seed=4))
    dc = ImageDraw.Draw(out)
    for flap in ([(396, 1062), (520, 1104), (452, 1172)], [(644, 1062), (520, 1104), (588, 1172)]):
        dc.polygon(flap, fill=(246, 246, 244, 255), outline=(150, 155, 170, 255), width=4)
    if tie:
        tm = Image.new("L", POT.size, 0); dt = ImageDraw.Draw(tm)
        dt.polygon([(488, 1100), (552, 1100), (542, 1162), (498, 1162)], fill=255)
        dt.polygon([(498, 1162), (542, 1162), (574, 1400), (520, 1452), (466, 1400)], fill=255)
        tm = Image.fromarray(np.minimum(np.asarray(tm), np.asarray(ALPHA.filter(ImageFilter.MaxFilter(25)))))
        tie_im = shaded(tm, YEL_HI, YEL_LO, light=(0.42, 0.0), noise=3, seed=5)
        st = Image.new("RGBA", POT.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(st)
        for k in range(-6, 12): y = 1130 + k * 42; ds.line([(430, y), (620, y - 70)], fill=(150, 92, 0, 120), width=12)
        st.putalpha(Image.fromarray(np.minimum(np.asarray(st.getchannel("A")), np.asarray(tm))))
        out.alpha_composite(tie_im); out.alpha_composite(st)
        ImageDraw.Draw(out).line([(498, 1162), (542, 1162)], fill=(140, 86, 0, 255), width=4)
    pq = Image.new("L", POT.size, 0); ImageDraw.Draw(pq).polygon([(206, 1236), (296, 1222), (262, 1252), (236, 1262)], fill=255)
    out.alpha_composite(shaded(pq, YEL_HI, YEL_LO, noise=2, seed=6))
    out.putalpha(Image.fromarray(np.maximum(np.asarray(ALPHA), np.asarray(jacket))))
    return out

def ImageChopsShift(sh):
    from PIL import ImageChops
    return ImageChops.offset(sh, 0, -14).getchannel("A")

FACES = {"confident": lambda: confident(), "stubble": lambda: confident(stubble=True), "cool": lambda: v2_layer("cool"),
         "shocked": lambda: v2_layer("shocked"), "panic": lambda: v2_layer("panic"), "sideeye": lambda: v2_layer("sideeye")}

def make(name, dressed=True):
    im = ink_onto(POT, FACES[name]())
    if dressed: im = suit(im)
    p = OUT + f"Batata_boss_{name}.png"; im.save(p); return p

if __name__ == "__main__":
    for n in FACES: print(make(n))
