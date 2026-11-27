"""Thumbnails for Files 29 DreamWorks / 30 Pixar / 31 Cartoon Network (owner 27 Nov: "you pick what's better, show me").
Look = Vice City GTA set the owner liked: Noah CENTRED (cut-out from brand/avatar/cut), real PD/CC-BY photos as tilted paper cards
left/right (Last Hours "proof photo" style + red string), split cold/warm background, big Anton words at the bottom, never on the face.
No film art, characters, logos or women. CC BY photos credited in the description.
  F:/thumbkit/venv/Scripts/python.exe make_qany3.py"""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
N = "D:/why habibi/_newchannel/"; CUT = N + "brand/avatar/cut/"
ANTON = "F:/thumbkit/fonts/Anton-Regular.ttf"; W, H = 1280, 720
def F(s): return ImageFont.truetype(ANTON, s)
def first(d, pre): return d + [f for f in sorted(os.listdir(d)) if f.startswith(pre)][0]

def cover(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))

def tint(im, rgb, k=0.55, bw=True):
    g = ImageOps.grayscale(im).convert("RGB") if bw else im.convert("RGB")
    return Image.blend(g, Image.new("RGB", g.size, rgb), k)

def bg_split(left, right, lrgb, rrgb, lf=(0.5, 0.5), rf=(0.5, 0.5)):
    c = Image.new("RGB", (W, H))
    L = tint(cover(left, W // 2 + 60, H, *lf), lrgb, 0.5); R = tint(cover(right, W // 2 + 60, H, *rf), rrgb, 0.45, bw=False)
    c.paste(L, (0, 0)); m = Image.linear_gradient("L").rotate(90).resize((120, H))      # soft seam
    Rm = Image.new("L", R.size, 255); Rm.paste(m, (0, 0)); c.paste(R, (W // 2 - 60, 0), Rm)
    c = ImageEnhance.Brightness(c).enhance(0.55)
    v = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(v)                                  # vignette
    for i in range(60): dv.rectangle((i * 6, i * 4, W - i * 6, H - i * 4), fill=int(i * 4.2))
    return Image.composite(c, Image.new("RGB", (W, H), (5, 5, 10)), v.filter(ImageFilter.GaussianBlur(40))).convert("RGBA")

def card(photo, w, h, angle, fx=0.5, fy=0.3, bw=False, label=None):
    p = cover(photo.convert("RGB"), w, h, fx, fy)
    if bw: p = ImageOps.grayscale(p).convert("RGB")
    p = ImageEnhance.Contrast(p).enhance(1.15)
    b = 14; cd = Image.new("RGBA", (w + 2 * b, h + 2 * b + (44 if label else 0)), (238, 232, 218, 255)); cd.paste(p, (b, b))
    if label:
        d = ImageDraw.Draw(cd); d.text((cd.width // 2, h + b + 24), label, font=F(30), fill=(30, 25, 20), anchor="mm")
    sh = Image.new("RGBA", (cd.width + 40, cd.height + 40), (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), (20, 26, 20 + cd.width, 26 + cd.height))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(cd, (20, 20))
    return sh.rotate(angle, Image.BICUBIC, expand=True)

def noah(c, pose, h, cx, bottom=H + 10):
    im = Image.open(CUT + pose + ".png").convert("RGBA"); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    a = im.split()[3]; rim = Image.new("RGBA", im.size, (0, 0, 0, 0)); rim.putalpha(a.filter(ImageFilter.MaxFilter(11)).point(lambda v: int(v * 0.9)))
    blk = Image.new("RGBA", im.size, (8, 6, 12, 255)); blk.putalpha(rim.split()[3])
    x = int(cx - im.width / 2); y = bottom - h; c.alpha_composite(blk, (x, y)); c.alpha_composite(im, (x, y)); return (x, y, x + im.width, y + h)

def text_band(c, l1, c1, l2, c2, y=640, size=104):
    d = ImageDraw.Draw(c); sz = size
    while d.textlength(l1 + " " + l2, font=F(sz)) > 1220 and sz > 60: sz -= 4
    wl = d.textlength(l1 + " ", font=F(sz)); wr = d.textlength(l2, font=F(sz)); x0 = W / 2 - (wl + wr) / 2
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for yy in range(y - 150, H): g.line((0, yy, W, yy), fill=(5, 3, 8, int(200 * min(1, (yy - y + 150) / 150) ** 1.3)))
    c.alpha_composite(lay); d = ImageDraw.Draw(c)
    d.text((x0, y), l1, font=F(sz), fill=c1, anchor="lm", stroke_width=9, stroke_fill=(8, 5, 10))
    d.text((x0 + wl, y), l2, font=F(sz), fill=c2, anchor="lm", stroke_width=9, stroke_fill=(8, 5, 10))

def tag(c, s, xy=(26, 22), fill=(255, 214, 64)):
    d = ImageDraw.Draw(c); tw = d.textlength(s, font=F(34)); x, y = xy
    d.rounded_rectangle((x, y, x + tw + 36, y + 56), 8, fill=fill); d.text((x + 18, y + 28), s, font=F(34), fill=(15, 10, 20), anchor="lm")

def string(c, a, b):
    d = ImageDraw.Draw(c); d.line((a, b), fill=(200, 30, 35), width=5)
    for p in (a, b): d.ellipse((p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9), fill=(220, 40, 40), outline=(60, 0, 0), width=2)

def stamp(c, s, xy, angle=-12, col=(210, 30, 35), size=58):
    f = F(size); tw = int(ImageDraw.Draw(c).textlength(s, font=f)); lay = Image.new("RGBA", (tw + 50, size + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((4, 4, lay.width - 4, lay.height - 4), 10, outline=col + (255,), width=6)
    d.text((lay.width // 2, lay.height // 2), s, font=f, fill=col + (255,), anchor="mm")
    c.alpha_composite(lay.rotate(angle, Image.BICUBIC, expand=True), xy)

def save(c, path):
    os.makedirs(os.path.dirname(path), exist_ok=True); c.convert("RGB").save(path, quality=92)
    c.convert("RGB").resize((320, 180), Image.LANCZOS).save(path.replace(".jpg", "_320.jpg"), quality=90)

# ---------- 29 DreamWorks: Eisner (cold, left) vs Katzenberg (warm, right), Burbank aerial / LA at sunset ----------
DW = N + "29_dreamworks_revenge/"; M = DW + "media/"
def dreamworks(name, l1, l2, tg, pose="master"):
    c = bg_split(Image.open(first(M, "C11_")), Image.open(first(M, "E23_")), (40, 80, 160), (230, 110, 30), rf=(0.6, 0.5))
    e = card(Image.open(first(M, "B14_")), 300, 360, 6, bw=True, label="EISNER")
    k = card(Image.open(first(M, "B1_")), 300, 360, -6, fx=0.35, fy=0.2, label="KATZENBERG")
    c.alpha_composite(e, (20, 70)); c.alpha_composite(k, (W - k.width - 20, 70))
    string(c, (300, 120), (W - 300, 120))
    noah(c, pose, 600, W // 2, H + 30)
    text_band(c, l1[0], (255, 255, 255), l1[1], (255, 196, 40)); tag(c, tg)
    if l2: stamp(c, l2, (W - 360, 500), angle=-8)
    save(c, DW + "export/thumbnails/" + name + ".jpg")
if __name__ == "__main__": dreamworks("DW_A_DISNEY_SAID_NO", ("DISNEY", "SAID NO."), "$3.8 BILLION", "1994-2016")
if __name__ == "__main__": dreamworks("DW_B_38_BILLION_REVENGE", ("$3.8 BILLION", "REVENGE"), None, "DISNEY vs DREAMWORKS", pose="smirk_s7")

# ---------- 30 Pixar: young Jobs + Macintosh 1984 (left) / Jobs 2007 (right), money ----------
PX = N + "30_pixar_10_million/"; P = PX + "media/"
def cheque():
    im = Image.new("RGB", (900, 1080), (226, 236, 222)); d = ImageDraw.Draw(im)
    for y in range(0, 1080, 6): d.line((0, y, 900, y), fill=(214, 228, 212))
    d.rectangle((30, 30, 870, 1050), outline=(60, 90, 70), width=6)
    T = lambda xy, t, sz, col=(30, 50, 40), a="la": d.text(xy, t, font=F(sz), fill=col, anchor=a)
    T((60, 70), "FIRST NATIONAL BANK", 52); T((840, 70), "FEB 3, 1986", 48, a="ra")
    T((60, 220), "PAY TO THE ORDER OF", 40); T((60, 280), "THE GRAPHICS GROUP", 70, (20, 20, 20))
    d.rectangle((60, 420, 840, 560), outline=(30, 50, 40), width=5); T((450, 490), "$10,000,000.00", 110, (20, 20, 20), "mm")
    T((60, 620), "TEN MILLION AND 00/100 DOLLARS", 46, (20, 20, 20))
    T((60, 900), "MEMO:  PIXAR", 50); d.line((470, 960, 840, 960), fill=(30, 50, 40), width=4)
    d.line([(490, 940), (540, 880), (580, 950), (640, 870), (700, 945), (760, 900), (820, 930)], fill=(20, 30, 90), width=7)
    return im
def pixar(name, l1, tg, st, right="B5_", rlabel="2006: $7.4 BILLION", rfy=0.2):
    jobs84 = Image.open(first(P, "B1_")).convert("RGB")
    d = ImageDraw.Draw(jobs84)                     # no-women rule: the Mac screen showed a drawing of a woman -> plain glowing screen
    d.rounded_rectangle((1175, 2765, 2045, 3415), 40, fill=(52, 66, 70))
    d.text((1250, 2860), "> _", font=F(150), fill=(150, 220, 170))
    box = (1120, 3700, 1250, 3840); jobs84.paste(jobs84.crop(box).filter(ImageFilter.GaussianBlur(25)), box)   # blur the Apple badge
    rim = cheque() if right == "CHEQUE" else Image.open(first(P, right))
    money = Image.open(first(M, "E6_"))
    c = bg_split(money, money, (30, 60, 120), (40, 150, 90), lf=(0.3, 0.5), rf=(0.7, 0.5))
    a = card(jobs84, 290, 360, 6, fx=0.45, fy=0.25, label="1986: $10 MILLION"); b = card(rim, 290, 360, -6, fx=0.5, fy=rfy, label=rlabel)
    c.alpha_composite(a, (20, 70)); c.alpha_composite(b, (W - b.width - 20, 70)); string(c, (300, 120), (W - 300, 120))
    noah(c, "hero_file_flashlight", 620, W // 2, H + 40)
    text_band(c, l1[0], (255, 255, 255), l1[1], (80, 230, 120)); tag(c, tg)
    if st: stamp(c, st, (W - 330, 500), angle=-8)
    save(c, PX + "export/thumbnails/" + name + ".jpg")
if __name__ == "__main__": pixar("PX_A_10M_TO_74B", ("FROM $10M", "TO $7.4B"), "PIXAR 1986-2006", None)
if __name__ == "__main__": pixar("PX_B_NOBODY_WANTED_IT", ("NOBODY", "WANTED IT."), "STEVE JOBS' $10M BET", "SOLD: $7.4B", right="CHEQUE", rlabel="ILLUSTRATION", rfy=0.5)

# ---------- 31 Cartoon Network: Ted Turner (left), CRT TV glow (right), cracking checker (no logo) ----------
CN = N + "31_cartoon_network/"; Q = CN + "media/"
def checker_tv(w, h):
    im = Image.new("RGB", (w, h), (10, 10, 10)); d = ImageDraw.Draw(im); s = w // 8
    for i in range(9):
        for j in range(8):
            if (i + j) % 2 == 0: d.rectangle((i * s, j * s, i * s + s, j * s + s), fill=(235, 235, 235))
    random.seed(3); x, y = w // 2, 0                                              # crack
    pts = [(x, y)]
    while y < h: x += random.randint(-40, 40); y += random.randint(30, 60); pts.append((x, y))
    d.line(pts, fill=(200, 20, 20), width=9); im = im.filter(ImageFilter.GaussianBlur(1.2))
    tv = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); dt = ImageDraw.Draw(tv)
    dt.rounded_rectangle((0, 0, w + 79, h + 79), 40, fill=(70, 62, 55, 255)); dt.rounded_rectangle((26, 26, w + 53, h + 53), 30, fill=(0, 0, 0, 255))
    msk = Image.new("L", (w, h), 0); ImageDraw.Draw(msk).rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=255); tv.paste(im, (40, 40), msk)
    return tv
def cartoon(name, l1, tg, st):
    tt = Image.open(first(Q, "B1_")) if any(f.startswith("B1_") and os.path.getsize(Q + f) > 50000 for f in os.listdir(Q)) else Image.open(first(Q, "B7_"))
    c = bg_split(tt, Image.new("RGB", (800, 720), (20, 20, 40)), (40, 70, 140), (120, 40, 160), lf=(0.5, 0.25))
    a = card(tt, 300, 360, 6, fx=0.5, fy=0.15, bw=True, label="TED TURNER")
    c.alpha_composite(a, (20, 70))
    tv = checker_tv(360, 280).rotate(-5, Image.BICUBIC, expand=True); c.alpha_composite(tv, (W - tv.width - 10, 60))
    string(c, (300, 120), (W - 330, 110))
    noah(c, "shock_s7", 600, W // 2, H + 30)
    text_band(c, l1[0], (255, 255, 255), l1[1], (255, 196, 40)); tag(c, tg)
    if st: stamp(c, st, (W - 330, 400), angle=-10)
    save(c, CN + "export/thumbnails/" + name + ".jpg")
if __name__ == "__main__": cartoon("CN_A_34M_HOMES_GONE", ("34 MILLION", "HOMES GONE."), "CARTOON NETWORK 1992-2026", "FADING?")
if __name__ == "__main__": cartoon("CN_B_320M_CHANNEL", ("$320 MILLION.", "THEN IT FADED."), "1992-2026", None)
if __name__ == "__main__": print("ok")
