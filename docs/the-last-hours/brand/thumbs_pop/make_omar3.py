"""v3 Omar-style thumbnails. Owner 27 Nov, layer order like Omar: CITY -> SKY -> BIG EXPLOSION behind his back -> CARTOON
CHARACTERS (all BEHIND Noah, NO white borders) -> NOAH -> logo + "THE FULL | logo | STORY". Pixar: no Toy Story statue photos.
  F:/thumbkit/venv/Scripts/python.exe make_omar3.py"""
import os, sys, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import make_omar as O, make_omar2 as O2
W, H = 1280, 720; N = O.N; C = O.C; SP = O2.SP
DWM = N + "29_dreamworks_revenge/media/"; MED = lambda p: DWM + [f for f in os.listdir(DWM) if f.startswith(p)][0]

def city_sky(city, sky_top, sky_mid, horizon=0.62, fy=0.85, stars=True, moon_at=None, seed=1, bright=1.0):
    c = O2.cover(Image.open(city).convert("RGB"), 0.5, fy); c = ImageEnhance.Brightness(c).enhance(bright).convert("RGBA")
    sky = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(sky); hy = int(H * horizon)
    for y in range(H):
        t = min(1, y / hy); col = tuple(int(sky_top[i] * (1 - t) + sky_mid[i] * t) for i in range(3))
        a = 255 if y < hy * 0.8 else int(255 * max(0, 1 - (y - hy * 0.8) / (hy * 0.35)))
        d.line((0, y, W, y), fill=col + (a,))
    c.alpha_composite(sky); c.alpha_composite(O2.noise_clouds(seed, (120, 130, 190), 90))
    if stars: O2.stars(c, seed, 260)
    if moon_at: O2.moon(c, *moon_at, 44)
    return c

def explosion(c, seed, big=620):
    O2.fire_photo(c, W // 2, 270, big)                                      # main fireball behind the head/back
    O2.fire_photo(c, W // 2 - 300, 330, int(big * 0.55)); O2.fire_photo(c, W // 2 + 300, 320, int(big * 0.6))
    random.seed(seed); deb = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(deb); cx, cy = W // 2, 270
    for _ in range(140):
        a = random.uniform(0, 2 * math.pi); dist = random.uniform(150, 650); x, y = cx + math.cos(a) * dist * 1.3, cy + math.sin(a) * dist * 0.8
        s = random.uniform(4, 18); rot = random.uniform(0, math.pi)
        dd.polygon([(x + s * math.cos(rot + k * 2.1) * random.uniform(0.5, 1.2), y + s * math.sin(rot + k * 2.1) * random.uniform(0.5, 1.2)) for k in range(3)], fill=(25, 18, 14, 235))
    for _ in range(260):
        a = random.uniform(0, 2 * math.pi); dist = random.uniform(80, 700); x, y = cx + math.cos(a) * dist * 1.3, cy + math.sin(a) * dist * 0.8; e = random.choice([1, 2, 2, 3])
        dd.ellipse((x - e, y - e, x + e, y + e), fill=(255, random.randint(150, 230), 80, 230))
    c.alpha_composite(deb)

def char(c, name, h, x, ybottom, flip=False, rot=0, bright=1.0):
    """no white border (owner): plain cut-out + a soft dark contact shadow only"""
    im = Image.open(C + name).convert("RGBA"); im = im.crop(im.split()[3].getbbox())
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    r, g, b, a = im.split(); rgb = ImageEnhance.Contrast(ImageEnhance.Color(ImageEnhance.Brightness(Image.merge("RGB", (r, g, b))).enhance(bright)).enhance(1.12)).enhance(1.05)
    im = Image.merge("RGBA", (*rgb.split(), a)).filter(ImageFilter.UnsharpMask(2, 80, 2))
    pad = 40; big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad))
    if rot: big = big.rotate(rot, Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); sh.putalpha(big.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5)))
    X, Y = int(x - big.width / 2), int(ybottom - big.height + pad)
    c.alpha_composite(sh, (X + 10, Y + 10)); c.alpha_composite(big, (X, Y))

def build(name, bg, chars, logo_key, pose, seed, out_dir):
    c = bg; explosion(c, seed)
    for ch in chars: char(c, *ch)
    O.noah(c, pose, 690); O2.logo(c, logo_key)
    p = N + out_dir + "/export/thumbnails/" + name + ".jpg"; O.save(c, p); return p

have = lambda n: os.path.exists(C + n)
OUT = []
for nm, pose, sd in (("OMAR3_DW_A", "master", 51), ("OMAR3_DW_B", "shock_s7", 52)):
    bg = city_sky(MED("E19_"), (6, 10, 40), (40, 50, 110), moon_at=(1060, 95), seed=sd)
    OUT.append(build(nm, bg, [("dw_puss.png", 520, 175, 560, False, 4), ("dw_donkey.png", 540, 1110, 560, True, -4),
                              ("dw_po.png", 600, 330, 800), ("dw_shrek.png", 640, 960, 840, True)], "dw", pose, sd, "29_dreamworks_revenge"))
px_side = [("px_carl.png", 560, 190, 640, False, 3), ("px_walle.png", 470, 1090, 620, True, -3),
           ("px_mike.png", 460, 360, 780), ("px_mcqueen.png", 260, 960, 690, True)]
if have("px_sulley.png"): px_side[0] = ("px_sulley.png", 600, 190, 660, False, 3)
for nm, pose, sd in (("OMAR3_PX_A", "master", 61), ("OMAR3_PX_B", "shock_s7", 62)):
    bg = city_sky(MED("E23_"), (40, 30, 90), (250, 140, 60), horizon=0.7, fy=0.6, stars=False, seed=sd, bright=1.15)
    OUT.append(build(nm, bg, px_side, "px", pose, sd, "30_pixar_10_million"))
cn_extra = [n for n in ("cn_mojo.png", "cn_grim.png", "cn_mordecai.png", "cn_rigby.png", "cn_iceking.png", "cn_bmo.png", "cn_courage.png", "cn_gumball.png", "cn_darwin.png") if have(n)]
cn_chars = [("cn_jake.png", 430, 175, 520, False, 6), ("cn_iceking.png", 430, 1105, 540, True, -5),
            ("cn_finn.png", 560, 330, 800, False, -3), ("cn_ben1.png", 640, 960, 860, True)]
if False: cn_chars = [(cn_extra[0], 380, 90, 330, False, 6), (cn_extra[1], 380, 1190, 330, True, -6)] + cn_chars
for nm, pose, sd in (("OMAR3_CN_A", "shock_s7", 71), ("OMAR3_CN_B", "master", 72)):
    bg = city_sky(MED("E18_"), (30, 8, 55), (110, 30, 140), moon_at=(1080, 95), seed=sd)
    OUT.append(build(nm, bg, cn_chars, "cn", pose, sd, "31_cartoon_network"))
ims = [Image.open(o).resize((640, 360), Image.LANCZOS) for o in OUT]; sheet = Image.new("RGB", (1280, 1080))
for i, im in enumerate(ims): sheet.paste(im, ((i % 2) * 640, (i // 2) * 360))
sheet.save(os.path.dirname(os.path.abspath(__file__)) + "/OMAR3_STYLE_SHEET.jpg", quality=90); print("ok", cn_extra)
