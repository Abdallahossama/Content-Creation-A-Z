"""File 28 GTA-poster thumbnails (owner 27 Nov: "more catchy ... GTA things ... centered ... like Omar Qany").
Base = the owner's ChatGPT image (build/tsrc/gta_noah_A.webp: Noah centred, original 1980s Miami archetypes, no Rockstar art).
The tiny sidewalk figures behind the car are painted out (no-women rule). Title in a band over the coat, never on the face.
  uv run --no-project --with pillow --with numpy --with opencv-python-headless python make_thumbs_gta.py"""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = "D:/why habibi/_newchannel/28_vice_city_real/"; OUT = R + "export/thumbnails/"
ANTON = "F:/thumbkit/fonts/Anton-Regular.ttf"
src = cv2.imread(R + "build/tsrc/gta_noah_A.png")
mask = np.zeros(src.shape[:2], np.uint8)
for (x0, y0, x1, y1) in [(60, 470, 110, 540), (150, 462, 245, 505), (240, 455, 300, 500)]:   # sidewalk silhouettes (1672x941 px)
    mask[y0:y1, x0:x1] = 255
clean = cv2.inpaint(src, mask, 9, cv2.INPAINT_TELEA)
base = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).resize((1280, 720), Image.LANCZOS).convert("RGBA")
base.convert("RGB").save(R + "build/tsrc/gta_noah_A_clean.png")

def F(s): return ImageFont.truetype(ANTON, s)
def outlined(d, xy, s, size, fill, anchor="mm", stroke=10):
    d.text(xy, s, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(10, 6, 20))

def make(name, l1, l2, col2, tag):
    c = base.copy()
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for y in range(430, 720): g.line((0, y, 1280, y), fill=(20, 0, 40, int(150 * ((y - 430) / 290) ** 1.4)))   # purple shade under the title
    c.alpha_composite(lay); d = ImageDraw.Draw(c)
    outlined(d, (640, 560), l1, 92, (255, 255, 255))
    outlined(d, (640, 650), l2, 118, col2)
    tw = d.textlength(tag, font=F(34)); d.rounded_rectangle((26, 22, 26 + tw + 36, 78), 8, fill=(255, 214, 64))
    d.text((44, 50), tag, font=F(34), fill=(15, 10, 20), anchor="lm")
    c.convert("RGB").save(OUT + name + ".jpg", quality=92); c.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT + name + "_320.jpg", quality=90)

make("GTA_A_THE_REAL_VICE_CITY", "THE REAL", "VICE CITY", (255, 79, 170), "MIAMI  1979-1986")
make("GTA_B_621_MURDERS", "621 MURDERS.", "ONE YEAR.", (255, 214, 64), "THE REAL VICE CITY")
make("GTA_C_MIAMI_WAS_REAL", "VICE CITY", "WAS REAL.", (64, 220, 255), "MIAMI  1979-1986")
print("ok")

# owner 27 Nov: "write Grand Theft Auto the same way as his thumbnail": the game's NAME, stacked, in our own font (Anton), not
# Rockstar's logo artwork or Pricedown font: "THE REAL | GRAND/THEFT/AUTO | VICE CITY" across the bottom like his "القصة | logo | الكاملة".
def make_gta(name, left, right, colr, tag):
    c = base.copy()
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for y in range(400, 720): g.line((0, y, 1280, y), fill=(20, 0, 40, int(170 * ((y - 400) / 320) ** 1.3)))
    c.alpha_composite(lay); d = ImageDraw.Draw(c)
    box = Image.new("RGBA", (250, 236), (0, 0, 0, 0)); b = ImageDraw.Draw(box)
    b.rounded_rectangle((0, 0, 249, 235), 18, fill=(28, 10, 48, 235), outline=(255, 255, 255, 255), width=5)
    for i, w in enumerate(("GRAND", "THEFT", "AUTO")):
        b.text((125, 44 + i * 74), w, font=F(70), fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    c.alpha_composite(box.rotate(-3, Image.BICUBIC, expand=True), (515, 455))
    outlined(d, (290, 600), left, 96, (255, 255, 255)); outlined(d, (1000, 600), right, 96, colr)
    tw = d.textlength(tag, font=F(34)); d.rounded_rectangle((26, 22, 26 + tw + 36, 78), 8, fill=(255, 214, 64))
    d.text((44, 50), tag, font=F(34), fill=(15, 10, 20), anchor="lm")
    c.convert("RGB").save(OUT + name + ".jpg", quality=92); c.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT + name + "_320.jpg", quality=90)

make_gta("GTA_D_REAL_GTA_VICE_CITY", "THE REAL", "VICE CITY", (255, 79, 170), "MIAMI  1979-1986")
print("ok2")

# owner 27 Nov: "use the same one in GTA V": the stacked logo lettering in Pricedown (Typodermic free desktop EULA: commercial images OK),
# white with a heavy black outline on a dark panel, between "THE REAL" and "VICE CITY" like his "القصة | logo | الكاملة".
PD = "F:/thumbkit/fonts/PricedownBl.otf"
def gta_logo(scale=1.0):
    words = ["grand", "theft", "auto"]; size = int(86 * scale); f = ImageFont.truetype(PD, size)
    w = int(max(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(x, font=f) for x in words)) + int(50 * scale)
    hgt = int(size * 0.82 * 3 + 40 * scale); lay = Image.new("RGBA", (w + 20, hgt + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, x in enumerate(words):
        d.text((28 * scale, 14 * scale + i * size * 0.82), x, font=f, fill=(255, 255, 255), stroke_width=int(7 * scale), stroke_fill=(0, 0, 0))
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.85)))
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0)); out.alpha_composite(sh); out.alpha_composite(lay); return out
def make_logo(name, left, right, colr, tag):
    c = base.copy()
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for y in range(400, 720): g.line((0, y, 1280, y), fill=(20, 0, 40, int(170 * ((y - 400) / 320) ** 1.3)))
    c.alpha_composite(lay); d = ImageDraw.Draw(c)
    lg = gta_logo(0.82); c.alpha_composite(lg, (1280 - lg.width - 6, 4))          # owner: the logo top-right (like the GTA V cover)
    sz = 112
    while True:
        f = F(sz); wl = d.textlength(left + " ", font=f); wr = d.textlength(right, font=f)
        if wl + wr <= 1180 or sz <= 70: break
        sz -= 4
    x0 = 640 - (wl + wr) / 2
    outlined(d, (x0, 650), left, sz, (255, 255, 255), anchor="lm"); outlined(d, (x0 + wl, 650), right, sz, colr, anchor="lm")
    tw = d.textlength(tag, font=F(34)); d.rounded_rectangle((26, 22, 26 + tw + 36, 78), 8, fill=(255, 214, 64))
    d.text((44, 50), tag, font=F(34), fill=(15, 10, 20), anchor="lm")
    c.convert("RGB").save(OUT + name + ".jpg", quality=92); c.convert("RGB").resize((320, 180), Image.LANCZOS).save(OUT + name + "_320.jpg", quality=90)
make_logo("GTA_E_LOGO_REAL_VICE_CITY", "THE REAL", "VICE CITY", (255, 79, 170), "MIAMI  1979-1986")
make_logo("GTA_F_LOGO_621_MURDERS", "621 MURDERS.", "ONE YEAR.", (255, 214, 64), "MIAMI  1981")
make_logo("GTA_G_LOGO_WAS_REAL", "VICE CITY", "WAS REAL.", (64, 220, 255), "MIAMI  1979-1986")
print("ok3")
