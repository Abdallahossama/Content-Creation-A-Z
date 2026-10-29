"""Ep 6 thumbnails v2 (user, 18 Oct 2026: every option a genuinely different composition, real photos/people, real insect).
  A  OBJECT   giant REAL body louse (CDC micrograph, public domain) glowing + shocked boss Batata, "THE LOUSE KNEW"
  B  FACE     surprised woman (Pexels) + shivering naked potato on the REAL ice-age Earth (NASA Blue Marble + our ice), "NOT MODESTY"
  C  SPLIT    cold blue half (naked potato, snow) -> warm half (fur-parka potato), big arrow, "170K YEARS"
-> 6th video/export/thumbnails/"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep06_clothes")
import cinekit as CK, marker as MK
from thumbkit import W, H
from ep06_draw import ICE
OUT = "D:/why habibi/6th video/export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
BOSS = "D:/why habibi/_style_kit/mascot/batata_boss/Batata_boss_{}.png"
CAST = "D:/why habibi/_style_kit/brand/potato_cast/"; MED = "D:/why habibi/_media/"

def cast(name, h, tint=None):
    im = Image.open(CAST + name + ".png").convert("RGBA"); im = im.crop(im.getbbox()); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if tint:
        t = Image.new("RGBA", im.size, tint + (0,)); t.putalpha(im.split()[3].point(lambda v: v * 70 // 255)); im.alpha_composite(t)
    return im
def cutout(path, h):
    im = Image.open(path).convert("RGBA"); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

def ice_earth(lon_c=-30, lat_c=48, ppd=7.0, ky=1.35):
    bm = Image.open(MED + "photos_2026-10-18/world_bluemarble_5400.jpg").convert("RGB"); sx = bm.width / 360; sy = bm.height / 180
    lon0, lon1 = lon_c - W / 2 / ppd, lon_c + W / 2 / ppd; lat1 = lat_c + H / 2 / (ppd * ky); lat0 = lat_c - H / 2 / (ppd * ky)
    im = bm.resize((W, H), Image.BICUBIC, box=((lon0 + 180) * sx, (90 - lat1) * sy, (lon1 + 180) * sx, (90 - lat0) * sy)).convert("RGBA")
    im = ImageEnhance.Brightness(im).enhance(0.8)
    xy = lambda lo, la: ((lo - lon0) / (lon1 - lon0) * W, (lat1 - la) / (lat1 - lat0) * H)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for p in ICE: d.polygon([xy(*q) for q in p], fill=(240, 250, 255, 255))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18))); im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))
    return im

def shiver(c, x, y, w, h, seed=1):
    """marker 'brrr' shake lines either side of a shivering character + snowflakes"""
    for sx in (-1, 1):
        for j in range(3):
            x0 = x + sx * (w / 2 + 14 + j * 16); MK.strokes(c, [np.array([(x0, y - h * 0.15 + j * 10), (x0 + sx * 6, y + h * 0.15 + j * 10)])], MK.WHITE, 7, seed=seed + j)
    r = np.random.default_rng(seed); d = ImageDraw.Draw(c, "RGBA")
    for _ in range(40):
        fx, fy, fs = r.uniform(0, W), r.uniform(0, H), r.uniform(3, 9); d.ellipse((fx - fs, fy - fs, fx + fs, fy + fs), fill=(255, 255, 255, 200))

def make_A():
    lou = cutout(MED + "cutouts/louse_body.png", 600).rotate(-8, Image.BICUBIC, expand=True)
    return CK.scene(CK.NIGHT, BOSS.format("shocked"), lou, (255, 140, 60), ["THE LOUSE", "KNEW"], prop_xy=(260, 90), b_cx=1030, b_top=170, b_h=620,
                    sleeves=True, hold=False, word_size=130)

def make_B():
    c = ice_earth()
    nk = cast("ice_age_naked", 330, tint=(120, 180, 255)); CK.glow(c, nk, 360, 330, (150, 210, 255), r=40, a=0.9); c.alpha_composite(nk, (360, 330))
    shiver(c, 360 + nk.width / 2, 330 + nk.height / 2, nk.width, nk.height)
    w = MK.sticker(MED + "cutouts/person_surprised_woman.png", 640, border=10, rot=-3); MK.place(c, w, W - w.width // 2 - 10, H - w.height // 2 + 80)
    CK.words(c, ["NOT", "MODESTY"], size=150, x=30, y=10)
    CK.corner_vignette(c); return c

def make_C():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); left = xx < W / 2
    cold = np.array([30, 90, 200], np.float32) * (1 - yy[..., None] / H * 0.5); warm = np.array([235, 120, 30], np.float32) * (1 - yy[..., None] / H * 0.45)
    a = np.where(left[..., None], cold, warm) + np.random.default_rng(2).normal(0, 3, (H, W, 3))
    c = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    bx, by = (W * 0.75, H * 0.55); r = np.sqrt((xx - bx) ** 2 + (yy - by) ** 2); gl = np.clip(1 - r / 420, 0, 1) ** 1.5
    g = Image.fromarray((np.array([255, 210, 120]) * gl[..., None]).astype(np.uint8)).convert("RGBA"); g.putalpha(Image.fromarray((gl * 160).astype(np.uint8))); c.alpha_composite(g)
    nk = cast("ice_age_naked", 380, tint=(120, 180, 255)); c.alpha_composite(nk, (int(W * 0.25 - nk.width / 2), H - nk.height - 20))
    shiver(c, W * 0.25, H - nk.height / 2 - 20, nk.width, nk.height, seed=3)
    pk = cast("ice_age_parka", 420); c.alpha_composite(pk, (int(W * 0.75 - pk.width / 2), H - pk.height - 10))
    MK.strokes(c, MK.arrow_path((470, 470), (800, 470), bend=-0.15, head=48, seed=8), MK.WHITE, 20, seed=8)
    CK.words(c, ["170K YEARS"], size=150, x=W // 2 - 380, y=10, rot=-2)
    CK.corner_vignette(c); return c

if __name__ == "__main__":
    ims = {"A_THE_LOUSE_KNEW": make_A(), "B_NOT_MODESTY": make_B(), "C_170K_YEARS": make_C()}
    for n, im in ims.items(): im.convert("RGB").save(OUT + n + ".png"); print(OUT + n + ".png")
    sheet = Image.new("RGB", (W * 3 // 2 + 20, H // 2), (20, 20, 20))
    for k, im in enumerate(ims.values()): sheet.paste(im.convert("RGB").resize((W // 2, H // 2)), (k * (W // 2 + 10), 0))
    sheet.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
