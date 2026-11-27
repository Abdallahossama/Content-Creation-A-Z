"""Channel branding with the host avatar (owner 27 Nov 2026: "change the channel picture to the new avatar and the branding").
Banner 2560x1440 (desktop strip = the middle 2560x423, safe area 1546x423), picture 800x800, watermark 150x150.
  uv run --no-project --with pillow --with numpy python make_channel_brand.py"""
import sys
sys.path.insert(0, "D:/why habibi/_newchannel/_tools")
import numpy as np
import hostkit as HK
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A = "D:/why habibi/_newchannel/brand/avatar/"; OUT = "D:/why habibi/_newchannel/brand/channel_v3/"
import os; os.makedirs(OUT, exist_ok=True)
COND = "C:/Windows/Fonts/FRAMDCN.TTF"; SER = "C:/Windows/Fonts/georgiai.ttf"; ANTON = "F:/thumbkit/fonts/Anton-Regular.ttf"
RED, BONE = (190, 30, 30), (236, 230, 214)
def F(p, s): return ImageFont.truetype(p, s)

def grid_bg(w, h, cell=60):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.zeros((h, w, 3), np.float32) + 12
    a += np.exp(-(((xx - w * .3) / (w * .3)) ** 2 + ((yy - h * .5) / (h * .45)) ** 2))[..., None] * np.array([90, 12, 14], np.float32)
    a += np.exp(-(((xx - w * .85) / (w * .3)) ** 2 + ((yy - h * .5) / (h * .5)) ** 2))[..., None] * np.array([10, 18, 70], np.float32)
    a += np.random.default_rng(3).normal(0, 4, (h, w, 1))
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(0, w, cell): d.line((x, 0, x, h), fill=(255, 255, 255, 13))
    for y in range(0, h, cell): d.line((0, y, w, y), fill=(255, 255, 255, 13))
    im.alpha_composite(lay); return im

def banner():
    W, H = 2560, 1440; c = grid_bg(W, H)
    hero = Image.open(A + "cut/hero_file_flashlight.png").convert("RGBA"); k = 600 / hero.height
    hero = hero.resize((int(hero.width * k), 600), Image.LANCZOS)
    sh = Image.new("RGBA", (hero.width + 80, hero.height + 80), (0, 0, 0, 0)); blk = Image.new("RGBA", hero.size, (0, 0, 0, 255))
    blk.putalpha(hero.split()[3].point(lambda v: int(v * .6))); sh.paste(blk, (40, 52), blk); sh = sh.filter(ImageFilter.GaussianBlur(16)); sh.alpha_composite(hero, (40, 40))
    c.alpha_composite(sh, (515 - 40, 522 - 40))                     # hat top at y≈522 (strip 508-931), the cut bottom falls below the strip
    d = ImageDraw.Draw(c); x0 = 515 + hero.width + 40
    d.text((x0, 600), "THE LAST HOURS", font=F(ANTON, 128), fill=BONE, anchor="lm")
    d.rectangle((x0 + 4, 682, x0 + 300, 690), fill=RED)
    d.text((x0 + 2, 745), "with Noah, the File Keeper", font=F(COND, 58), fill=(255, 214, 64), anchor="lm")
    d.text((x0 + 2, 830), "Famous cases, hour by hour, from the real files.", font=F(SER, 37), fill=(200, 200, 200), anchor="lm")
    d.text((x0 + 2, 895), "TRUE CASES  ·  REAL RECORDS  ·  NO REENACTMENTS", font=F(COND, 36), fill=(150, 150, 150), anchor="lm")
    c = c.convert("RGB"); c.save(OUT + "banner_2560x1440.jpg", quality=92)
    # check sheet: TV full, desktop strip, phone safe area
    S = Image.new("RGB", (1280, 720 + 260 + 40), (30, 30, 30)); S.paste(c.resize((1280, 720)), (0, 0))
    g = ImageDraw.Draw(S); g.rectangle((253, 254, 1027, 466), outline=(0, 255, 0), width=2); g.rectangle((0, 254, 1279, 466), outline=(255, 0, 255), width=1)
    S.paste(c.crop((0, 508, 2560, 932)).resize((1280, 212)), (0, 760)); S.save(OUT + "_banner_check.jpg", quality=85)

def picture():
    s = 800; c = grid_bg(s, s, cell=50)
    hd = Image.open(A + "cut/master.png").convert("RGBA"); hd = hd.resize((int(hd.width * 860 / hd.height), 860), Image.LANCZOS)
    c.alpha_composite(hd, ((s - hd.width) // 2 + 10, 20))
    m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0)); out.paste(c, (0, 0), m); ImageDraw.Draw(out).ellipse((6, 6, s - 7, s - 7), outline=RED + (255,), width=16)
    sq = c.convert("RGB"); ImageDraw.Draw(sq).ellipse((6, 6, s - 7, s - 7), outline=RED, width=16)
    sq.save(OUT + "picture_800.png")                                      # square upload (YouTube crops the circle itself)
    out.resize((150, 150), Image.LANCZOS).save(OUT + "watermark_150.png")  # round, transparent corners
    T = Image.new("RGB", (900, 320), (15, 15, 15)); T.paste(out.resize((240, 240)), (20, 40), out.resize((240, 240)))
    for i, z in enumerate((88, 48, 32)): r = out.resize((z, z)); T.paste(r, (320 + i * 140, 140 - z // 2), r)
    T.save(OUT + "_picture_check.jpg", quality=90)

if __name__ == "__main__":
    banner(); picture(); print(OUT)
