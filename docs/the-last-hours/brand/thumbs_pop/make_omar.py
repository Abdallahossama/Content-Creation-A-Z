"""Omar-Qany-style thumbnails for Files 29-31 (owner 27 Nov: "literally the same": studio characters around him, the studio logo
in the middle, bright, no date tag). Owner accepted the copyright risk of studio characters/logos for these thumbnails.
No female characters (channel rule). Noah = clean avatar cut-out, centred and big, back burst + rim light.
  F:/thumbkit/venv/Scripts/python.exe make_omar.py"""
import os, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops, ImageFont
N = "D:/why habibi/_newchannel/"; CUT = N + "brand/avatar/cut/"
C = "C:/Users/ossam/AppData/Local/Temp/claude/4e5240680a12582b/0deccdd2-4bb6-4df6-90bc-0ed43495fcc4/scratchpad/chars/"
ANTON = "F:/thumbkit/fonts/Anton-Regular.ttf"; W, H = 1280, 720
def F(s): return ImageFont.truetype(ANTON, s)

def burst_bg(inner, outer, seed=1):
    random.seed(seed); c = Image.new("RGB", (W, H), outer); d = ImageDraw.Draw(c); cx, cy = W // 2, 300
    for r in range(900, 0, -8):                                            # radial burst
        t = r / 900; col = tuple(int(inner[i] * (1 - t) ** 1.4 + outer[i] * (1 - (1 - t) ** 1.4)) for i in range(3))
        d.ellipse((cx - r * 1.4, cy - r, cx + r * 1.4, cy + r), fill=col)
    rays = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(rays)              # light rays
    for k in range(28):
        a = k / 28 * 2 * math.pi + random.uniform(-0.05, 0.05); w = random.uniform(0.02, 0.05)
        dr.polygon([(cx, cy), (cx + 1600 * math.cos(a - w), cy + 1600 * math.sin(a - w)), (cx + 1600 * math.cos(a + w), cy + 1600 * math.sin(a + w))], fill=random.randint(25, 60))
    c = Image.composite(Image.new("RGB", (W, H), (255, 240, 200)), c, rays.filter(ImageFilter.GaussianBlur(6)))
    sp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sp)     # sparks + debris
    for _ in range(140):
        x, y = random.randint(0, W), random.randint(0, H); r = random.choice([1, 1, 2, 2, 3, 5])
        ds.ellipse((x - r, y - r, x + r, y + r), fill=(255, random.randint(180, 240), 120, random.randint(120, 230)))
    c = c.convert("RGBA"); c.alpha_composite(sp.filter(ImageFilter.GaussianBlur(0.8)))
    v = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(v)
    for i in range(50): dv.rectangle((i * 7, i * 5, W - i * 7, H - i * 5), fill=min(255, 90 + int(i * 4)))
    return Image.composite(c, Image.new("RGBA", (W, H), (5, 5, 15, 255)), v.filter(ImageFilter.GaussianBlur(50)))

def outline(im, col=(255, 255, 255), px=5, glow=None):
    a = im.split()[3]; o = Image.new("RGBA", im.size, col + (0,)); o.putalpha(a.filter(ImageFilter.MaxFilter(px * 2 + 1)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, glow + (0,)); g.putalpha(a.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(16))); out.alpha_composite(g)
    out.alpha_composite(o); out.alpha_composite(im); return out

def place(c, path, h, xy, flip=False, rot=0, crop=None, pad=40, ol=(255, 255, 255), olpx=4):
    im = Image.open(path).convert("RGBA")
    if crop: im = im.crop(crop)
    im = im.crop(im.split()[3].getbbox())
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS); im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.15)).enhance(1.05)
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad))
    big = outline(big, ol, olpx); sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); sh.putalpha(big.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55)))
    if rot: big = big.rotate(rot, Image.BICUBIC, expand=True); sh = sh.rotate(rot, Image.BICUBIC, expand=True)
    x, y = xy; c.alpha_composite(sh, (int(x - big.width / 2) + 8, int(y - big.height) + 12)); c.alpha_composite(big, (int(x - big.width / 2), int(y - big.height)))

def noah(c, pose, h, rim=(255, 210, 120)):
    im = Image.open(C + "noah_" + pose + ".png").convert("RGBA"); r_, g_, b_, a_ = im.split(); a_ = a_.point(lambda v: 0 if v < 40 else v); im = Image.merge("RGBA", (r_, g_, b_, a_)); im = im.crop(a_.getbbox())
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    a = im.split()[3]; inner = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(9))).filter(ImageFilter.GaussianBlur(2))
    lit = Image.composite(Image.blend(im.convert("RGB"), Image.new("RGB", im.size, rim), 0.6), im.convert("RGB"), inner)
    im = Image.merge("RGBA", (*lit.split(), a)); pd = Image.new("RGBA", (im.width + 120, im.height + 120), (0, 0, 0, 0)); pd.alpha_composite(im, (60, 60))
    im = outline(pd, (15, 10, 20), 4, glow=rim)
    c.alpha_composite(im, (W // 2 - im.width // 2, H - im.height + 90))

def logo_row(c, logo_path, left, right, lh, y, white=False, lw=None):
    lg = Image.open(logo_path).convert("RGBA"); lg = lg.crop(lg.split()[3].getbbox())
    if white:
        a = lg.split()[3]; lg = Image.new("RGBA", lg.size, (255, 255, 255, 255)); lg.putalpha(a)
    s = lh / lg.height
    if lw and lg.width * s > lw: s = lw / lg.width
    lg = lg.resize((int(lg.width * s), int(lg.height * s)), Image.LANCZOS)
    lg = outline(lg, (10, 10, 25), 5, glow=(0, 0, 0))
    d = ImageDraw.Draw(c); f = F(92); wl = d.textlength(left, font=f); wr = d.textlength(right, font=f); gap = 26
    total = wl + gap + lg.width + gap + wr; x0 = W / 2 - total / 2
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for yy in range(y - 140, H): g.line((0, yy, W, yy), fill=(5, 3, 10, int(190 * min(1, (yy - y + 140) / 140) ** 1.3)))
    c.alpha_composite(lay); d = ImageDraw.Draw(c)
    d.text((x0, y), left, font=f, fill=(255, 255, 255), anchor="lm", stroke_width=8, stroke_fill=(10, 8, 15))
    c.alpha_composite(lg, (int(x0 + wl + gap), int(y - lg.height / 2)))
    d.text((x0 + wl + gap + lg.width + gap, y), right, font=f, fill=(255, 214, 64), anchor="lm", stroke_width=8, stroke_fill=(10, 8, 15))

def save(c, path):
    os.makedirs(os.path.dirname(path), exist_ok=True); c.convert("RGB").save(path, quality=93)
    c.convert("RGB").resize((320, 180), Image.LANCZOS).save(path.replace(".jpg", "_320.jpg"), quality=90)

if __name__ == "__main__":
    OUT = []
    # ---- DreamWorks: night-blue burst (like his), crowd around Noah ----
    for name, pose, seed in (("OMAR_DW_A", "master", 3), ("OMAR_DW_B", "shock_s7", 5)):
        c = burst_bg((255, 200, 90), (30, 60, 150), seed)
        place(c, C + "dw_puss.png", 430, (150, 520), rot=6); place(c, C + "dw_donkey.png", 440, (1150, 500), flip=True, rot=-5)
        noah(c, pose, 660)
        place(c, C + "dw_po.png", 470, (300, 760)); place(c, C + "dw_shrek.png", 520, (990, 790), flip=True)
        logo_row(c, C + "logo_dw.png", "THE FULL", "STORY", 165, 600, white=True)
        p = N + "29_dreamworks_revenge/export/thumbnails/" + name + ".jpg"; save(c, p); OUT.append(p)
    # ---- Pixar: bright sky-blue burst ----
    for name, pose, seed in (("OMAR_PX_A", "master", 7), ("OMAR_PX_B", "shock_s7", 9)):
        c = burst_bg((255, 245, 190), (50, 150, 235), seed)
        place(c, C + "px_woody_cut.png", 600, (170, 640), rot=4); place(c, C + "px_buzz_cut.png", 580, (1110, 640), rot=-4)
        noah(c, pose, 660)
        place(c, C + "px_mike.png", 330, (360, 760)); place(c, C + "px_walle.png", 320, (920, 760), flip=True); place(c, C + "px_mcqueen.png", 190, (1120, 250), flip=True, rot=-8)
        logo_row(c, C + "logo_px.png", "THE FULL", "STORY", 120, 615, white=True, lw=560)
        p = N + "30_pixar_10_million/export/thumbnails/" + name + ".jpg"; save(c, p); OUT.append(p)
    # ---- Cartoon Network: purple/orange burst ----
    for name, pose, seed in (("OMAR_CN_A", "shock_s7", 11), ("OMAR_CN_B", "master", 13)):
        c = burst_bg((255, 170, 70), (110, 40, 170), seed)
        place(c, C + "cn_jake.png", 380, (170, 470), rot=8); place(c, C + "cn_ben1.png", 600, (1110, 760), flip=True)
        noah(c, pose, 660)
        place(c, C + "cn_finn.png", 470, (330, 770), rot=-4)
        logo_row(c, C + "logo_cn.png", "THE FULL", "STORY", 150, 610)
        p = N + "31_cartoon_network/export/thumbnails/" + name + ".jpg"; save(c, p); OUT.append(p)
    ims = [Image.open(o).resize((640, 360), Image.LANCZOS) for o in OUT]; sheet = Image.new("RGB", (1280, 1080))
    for i, im in enumerate(ims): sheet.paste(im, ((i % 2) * 640, (i // 2) * 360))
    sheet.save(os.path.dirname(os.path.abspath(__file__)) + "/OMAR_STYLE_SHEET.jpg", quality=90); print("ok")
