"""v2 of the Omar-style thumbnails (owner 27 Nov: "background too simple", "not symmetrical", "McQueen in front of Buzz",
"Cartoon Network feels empty", "Woody too dark"). Rich layered backgrounds (photo + sky/stars/moon/clouds + fireball +
debris + city lights), mirrored 2+2 character layout (back-outer big, front-inner bigger, cropped by the frame like his).
  F:/thumbkit/venv/Scripts/python.exe make_omar2.py"""
import os, sys, random, math, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import make_omar as O
W, H = 1280, 720; N = O.N; C = O.C; SP = os.path.dirname(C.rstrip("/")) + "/"

def cover(im, fx=0.5, fy=0.5):
    s = max(W / im.width, H / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy); return im.crop((x, y, x + W, y + H))

def noise_clouds(seed, col, alpha=150, scale=6):
    random.seed(seed); small = Image.new("L", (W // scale, H // scale), 0); d = ImageDraw.Draw(small)
    for _ in range(70):
        x, y, r = random.randint(-20, W // scale), random.randint(-10, H // scale), random.randint(8, 30)
        d.ellipse((x - r, y - r * 0.6, x + r, y + r * 0.6), fill=random.randint(60, 200))
    m = small.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * alpha / 255))
    lay = Image.new("RGBA", (W, H), col + (0,)); lay.putalpha(m); return lay

def fire_photo(c, cx, cy, h):
    ph = Image.open(SP + "expl_2.jpg").convert("RGB"); ph = ph.crop((0, 0, ph.width, int(ph.height * 0.62)))      # the fireball, not the column
    ph = ImageEnhance.Contrast(ph).enhance(1.25); ph = ph.resize((int(ph.width * h / ph.height), h), Image.LANCZOS)
    x0, y0 = int(cx - ph.width / 2), int(cy - ph.height / 2); base = c.convert("RGB")
    reg = base.crop((x0, y0, x0 + ph.width, y0 + ph.height)); scr = ImageChops.screen(reg, ph)
    m = Image.new("L", ph.size, 0); ImageDraw.Draw(m).ellipse((0, 0, ph.width, ph.height), fill=255); m = m.filter(ImageFilter.GaussianBlur(60))
    reg = Image.composite(scr, reg, m); base.paste(reg, (x0, y0)); c.paste(base.convert("RGBA"), (0, 0))

def fireball(c, cx, cy, r, seed):
    fire_photo(c, cx, cy, int(r * 2.3)); random.seed(seed)
    deb = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(deb)       # flying debris shards + embers
    for _ in range(90):
        a = random.uniform(0, 2 * math.pi); dist = random.uniform(r * 0.5, r * 2.2); x, y = cx + math.cos(a) * dist * 1.3, cy + math.sin(a) * dist * 0.9
        s = random.uniform(4, 16); rot = random.uniform(0, math.pi)
        pts = [(x + s * math.cos(rot + k * 2.1) * random.uniform(0.5, 1.2), y + s * math.sin(rot + k * 2.1) * random.uniform(0.5, 1.2)) for k in range(3)]
        dd.polygon(pts, fill=(30, 20, 15, 230))
    for _ in range(160):
        a = random.uniform(0, 2 * math.pi); dist = random.uniform(r * 0.3, r * 2.5); x, y = cx + math.cos(a) * dist * 1.3, cy + math.sin(a) * dist * 0.9; e = random.choice([1, 2, 2, 3])
        dd.ellipse((x - e, y - e, x + e, y + e), fill=(255, random.randint(150, 230), 80, 230))
    c.alpha_composite(deb)

def stars(c, seed, n=220):
    random.seed(seed); d = ImageDraw.Draw(c)
    for _ in range(n):
        x, y, e = random.randint(0, W), random.randint(0, int(H * 0.75)), random.choice([1, 1, 1, 2, 2, 3])
        d.ellipse((x - e, y - e, x + e, y + e), fill=(255, 255, 255, random.randint(120, 255)))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    for _ in range(25):
        x, y = random.randint(0, W), random.randint(0, int(H * 0.8)); dg.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(200, 230, 255, 200))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(4)))

def moon(c, x, y, r):
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m); d.ellipse((x - r, y - r, x + r, y + r), fill=255); d.ellipse((x - r * 0.45, y - r * 1.05, x + r * 1.5, y + r * 0.95), fill=0)
    glow = Image.new("RGBA", (W, H), (220, 235, 255, 0)); glow.putalpha(m.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.7))); c.alpha_composite(glow)
    body = Image.new("RGBA", (W, H), (250, 250, 240, 0)); body.putalpha(m); c.alpha_composite(body)

def city_lights(c, photo, h=170):
    ph = cover(Image.open(photo).convert("RGB"), 0.5, 0.85).crop((0, H - h, W, H)); ph = ImageEnhance.Brightness(ph).enhance(1.3)
    m = Image.linear_gradient("L").resize((W, h)); lay = ph.convert("RGBA"); lay.putalpha(m); c.alpha_composite(lay, (0, H - h))

def vignette(c, k=0.55):
    v = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(v)
    for i in range(60): dv.rectangle((i * 6, i * 4, W - i * 6, H - i * 4), fill=min(255, int(255 * (1 - k) + i * 4)))
    return Image.composite(c, Image.new("RGBA", (W, H), (3, 3, 10, 255)), v.filter(ImageFilter.GaussianBlur(60)))

def bg_night(seed, top, bot, city, fire=True, moon_at=(900, 120)):
    c = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(c)
    for y in range(H): t = y / H; d.line((0, y, W, y), fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)) + (255,))
    c.alpha_composite(noise_clouds(seed, (90, 110, 170), 120)); stars(c, seed)
    if moon_at: moon(c, *moon_at, 46)
    city_lights(c, city)
    c = vignette(c)
    if fire: fireball(c, W // 2, 240, 300, seed)
    return c

def bg_sky(seed, sky):
    c = cover(Image.open(sky).convert("RGB"), 0.5, 0.4); c = ImageEnhance.Color(ImageEnhance.Brightness(c).enhance(1.1)).enhance(1.35).convert("RGBA")
    rays = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(rays); random.seed(seed); cx, cy = W // 2, 230
    for k in range(24):
        a = k / 24 * 2 * math.pi; w = 0.045; dr.polygon([(cx, cy), (cx + 1500 * math.cos(a - w), cy + 1500 * math.sin(a - w)), (cx + 1500 * math.cos(a + w), cy + 1500 * math.sin(a + w))], fill=70)
    sun = Image.new("RGBA", (W, H), (255, 250, 210, 0)); sun.putalpha(rays.filter(ImageFilter.GaussianBlur(10))); c.alpha_composite(sun)
    g = Image.new("L", (W, H), 0); dg = ImageDraw.Draw(g)
    for r in range(380, 0, -6): dg.ellipse((cx - r * 1.3, cy - r, cx + r * 1.3, cy + r), fill=int(230 * (1 - r / 380) ** 1.5))
    glow = Image.new("RGBA", (W, H), (255, 245, 200, 0)); glow.putalpha(g.filter(ImageFilter.GaussianBlur(25))); c.alpha_composite(glow)
    return vignette(c, 0.35)

def char(c, path, h, xy, flip=False, rot=0, bright=1.0, crop_bottom=0.0):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.split()[3].getbbox())
    if crop_bottom: im = im.crop((0, 0, im.width, int(im.height * (1 - crop_bottom))))
    if bright != 1.0:
        r, g, b, a = im.split(); rgb = ImageEnhance.Brightness(Image.merge("RGB", (r, g, b))).enhance(bright); im = Image.merge("RGBA", (*rgb.split(), a))
    tmp = SP + "_tmp_char.png"; im.save(tmp); O.place(c, tmp, h, xy, flip=flip, rot=rot)

def logo(c, key, y=615):
    if key == "dw": O.logo_row(c, C + "logo_dw.png", "THE FULL", "STORY", 175, y, white=True)
    if key == "px": O.logo_row(c, C + "logo_px.png", "THE FULL", "STORY", 120, y, white=True, lw=560)
    if key == "cn": O.logo_row(c, C + "logo_cn.png", "THE FULL", "STORY", 160, y)

def have(n): return os.path.exists(C + n)
if __name__ == "__main__":
    DWM = N + "29_dreamworks_revenge/media/"; LA = O.N + "29_dreamworks_revenge/media/" + [f for f in os.listdir(DWM) if f.startswith("E19_")][0]
    CITY2 = DWM + [f for f in os.listdir(DWM) if f.startswith("E18_")][0]
    OUT = []
    for name, pose, seed in (("OMAR2_DW_A", "master", 21), ("OMAR2_DW_B", "shock_s7", 22)):
        c = bg_night(seed, (8, 14, 45), (35, 45, 95), LA)
        char(c, C + "dw_puss.png", 520, (170, 560), rot=4); char(c, C + "dw_donkey.png", 520, (1110, 560), flip=True, rot=-4)
        O.noah(c, pose, 680)
        char(c, C + "dw_po.png", 560, (290, 820)); char(c, C + "dw_shrek.png", 600, (990, 860), flip=True)
        logo(c, "dw"); p = N + "29_dreamworks_revenge/export/thumbnails/" + name + ".jpg"; O.save(c, p); OUT.append(p)
    SKY = SP + "sky_clouds.jpg"
    for name, pose, seed in (("OMAR2_PX_A", "master", 31), ("OMAR2_PX_B", "shock_s7", 32)):
        c = bg_sky(seed, SKY) if os.path.exists(SKY) and os.path.getsize(SKY) > 50000 else bg_night(seed, (40, 120, 210), (150, 200, 240), LA, fire=False, moon_at=None)
        char(c, C + "px_woody_cut.png", 640, (170, 700), rot=3, bright=1.45); char(c, C + "px_buzz_cut.png", 640, (1110, 700), rot=-3, bright=1.05)
        O.noah(c, pose, 680)
        char(c, C + "px_mike.png", 330, (370, 760)); char(c, C + "px_walle.png", 330, (910, 760), flip=True)
        logo(c, "px"); p = N + "30_pixar_10_million/export/thumbnails/" + name + ".jpg"; O.save(c, p); OUT.append(p)
    cn_extra = ["cn_ben0.png"]
    for name, pose, seed in (("OMAR2_CN_A", "shock_s7", 41), ("OMAR2_CN_B", "master", 42)):
        c = bg_night(seed, (35, 10, 60), (110, 35, 130), CITY2, moon_at=(1000, 110))
        char(c, C + "cn_jake.png", 430, (180, 520), rot=6)
        if cn_extra: char(c, C + cn_extra[0], 460, (1100, 540), flip=True, rot=-4)
        O.noah(c, pose, 680)
        char(c, C + "cn_finn.png", 520, (300, 800), rot=-3); char(c, C + "cn_ben1.png", 640, (1010, 860), flip=True)
        logo(c, "cn"); p = N + "31_cartoon_network/export/thumbnails/" + name + ".jpg"; O.save(c, p); OUT.append(p)
    ims = [Image.open(o).resize((640, 360), Image.LANCZOS) for o in OUT]; sheet = Image.new("RGB", (1280, 1080))
    for i, im in enumerate(ims): sheet.paste(im, ((i % 2) * 640, (i // 2) * 360))
    sheet.save(os.path.dirname(os.path.abspath(__file__)) + "/OMAR2_STYLE_SHEET.jpg", quality=90); print("ok", cn_extra)
