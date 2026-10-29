"""Ep 5 thumbnails (cinematic Batata default): a night map of Egypt from our Natural Earth data, the desert dark red,
the Nile strip glowing like city lights, the suited boss Batata on the right, 1-3 huge words (never the title's words).
  A "95% EMPTY"  B "ONE THIN LINE"  C "NOBODY HERE?" (arrow into the desert)  -> 5th video/export/thumbnails/"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep05_egypt")
import cinekit as CK, marker as MK, egypt_geo as G
from thumbkit import W, H, put
from mapkit import Map, _load
OUT = "D:/why habibi/5th video/export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
BOSS = "D:/why habibi/_style_kit/mascot/batata_boss/Batata_boss_{}.png"
NIGHTPAL = dict(sea_top=(8, 18, 40), sea_bot=(4, 10, 24), shallow=(14, 34, 66), land=(40, 34, 38), border=(80, 70, 70), edge=(60, 54, 56))

def night_map(lon_c=31.4, lat_c=27.3, ppd=74):
    lon0, lon1 = lon_c - W / 2 / ppd, lon_c + W / 2 / ppd; ky = 1.12; lat1 = lat_c + H / 2 / (ppd * ky); lat0 = lat_c - H / 2 / (ppd * ky)
    m = Map(lon0, lon1, lat0, lat1, W, H, ss=2); im = m.render(pal=NIGHTPAL).convert("RGBA")
    xy = lambda pts: [m.xy(x, y) for x, y in pts]
    eg = max((r for n, rs in _load() if n == "Egypt" for r in rs), key=len)
    des = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(des).polygon(xy(eg), fill=(120, 40, 26, 150)); im.alpha_composite(des)
    lights = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lights)
    d.polygon(xy(G.valley_poly(0.20)), fill=(255, 210, 110, 255)); d.polygon(xy(G.DELTA), fill=(255, 210, 110, 255)); d.polygon(xy(G.FAYUM), fill=(255, 210, 110, 255))
    for (x, y) in G.people_dots(1600, seed=9):
        px, py = m.xy(x, y); d.ellipse((px - 2.5, py - 2.5, px + 2.5, py + 2.5), fill=(255, 240, 190, 255))
    im.alpha_composite(lights.filter(ImageFilter.GaussianBlur(30))); im.alpha_composite(lights.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(lights.filter(ImageFilter.GaussianBlur(4))); im.alpha_composite(lights)
    riv = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(riv).line(xy(G.NILE), fill=(120, 200, 255, 255), width=4); im.alpha_composite(riv)
    return im, m

def make(name, lines, face, arrow=False, size=170, lon_c=31.4):
    bg, m = night_map(lon_c=lon_c)
    c = CK.scene(CK.NIGHT, BOSS.format(face), Image.new("RGBA", (10, 10), (0, 0, 0, 0)), None, lines, b_cx=1010, b_top=150, b_h=640,
                 sleeves=True, hold=False, bg=bg, word_size=size)
    if arrow:
        x0, y0 = 250, 360; x1, y1 = m.xy(28.6, 24.2)
        MK.strokes(c, MK.arrow_path((x0, y0), (x1, y1), bend=0.25, head=34, seed=3), MK.RED, 14, seed=3)
    c.convert("RGB").save(OUT + name + ".png"); print(OUT + name + ".png")
    return c

if __name__ == "__main__":
    ims = [make("A_95_EMPTY", ["95%", "EMPTY"], "shocked"), make("B_ONE_THIN_LINE", ["ONE THIN", "LINE"], "sideeye", size=150),
           make("C_NOBODY_HERE", ["NOBODY", "HERE?"], "panic", arrow=True)]
    sheet = Image.new("RGB", (W * 3 // 2 + 20, H // 2), (20, 20, 20))
    for k, im in enumerate(ims): sheet.paste(im.convert("RGB").resize((W // 2, H // 2)), (k * (W // 2 + 10), 0))
    sheet.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
