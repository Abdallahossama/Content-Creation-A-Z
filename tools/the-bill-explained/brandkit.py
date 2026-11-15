"""The Bill, Explained - brand kit, drawn in code (no AI images, system/OFL fonts only).
Outputs to D:/the-bill-explained/brand/:
  logo_800.png        profile picture (YouTube crops it to a circle)
  watermark_150.png   video watermark (transparent)
  banner_2560x1440.png channel banner (text inside the 1546x423 safe area)
  banner_safe_check.png same banner with the safe areas drawn on (do not upload)
  thumb_template.py   is separate (needs a real object cut-out)
Run: E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe tools/brandkit.py
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

OUT = "D:/the-bill-explained/brand/"
F = "C:/Windows/Fonts/"
INK, PAPER, RED, YELLOW, GREY = (18, 18, 18), (244, 240, 231), (214, 40, 32), (255, 212, 0), (128, 122, 112)
WORD = F + "ariblk.ttf"      # wordmark
NUM = F + "impact.ttf"       # prices on thumbnails
MONO, MONOB = F + "consola.ttf", F + "consolab.ttf"   # receipt print


def font(p, s): return ImageFont.truetype(p, s)


def grain(img, amount=6, seed=1):
    """Very light paper grain so flat paper doesn't look like a vector card."""
    rnd = random.Random(seed)
    n = Image.effect_noise(img.size, 40).convert("L")
    n = n.point(lambda v: 128 + (v - 128) * amount // 40)
    base = img.convert("RGB")
    return ImageChops.add(base, Image.merge("RGB", [n] * 3), 1, -128)


def zigzag(w, h, tooth=18, depth=12, top=False, bottom=True):
    """Receipt mask: rectangle with torn zigzag edges."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    pts = []
    if top:
        for x in range(0, w + tooth, tooth):
            pts.append((min(x, w), 0 if (x // tooth) % 2 else depth))
    else:
        pts += [(0, 0), (w, 0)]
    if bottom:
        xs = list(range(w, -tooth, -tooth))
        for i, x in enumerate(xs):
            pts.append((max(x, 0), h - (depth if i % 2 else 0)))
    else:
        pts += [(w, h), (0, h)]
    d.polygon(pts, fill=255)
    return m


def receipt(w, h, tooth=18, depth=12, top=False):
    paper = grain(Image.new("RGB", (w, h), PAPER), 5)
    r = paper.convert("RGBA")
    r.putalpha(zigzag(w, h, tooth, depth, top=top))
    return r


def shadow(layer, off=(10, 14), blur=18, alpha=110):
    a = layer.split()[-1].point(lambda v: v * alpha // 255)
    s = Image.new("RGBA", (layer.width + 80, layer.height + 80), (0, 0, 0, 0))
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 255)); sh.putalpha(a)
    s.paste(sh, (40 + off[0], 40 + off[1]), sh)
    return s.filter(ImageFilter.GaussianBlur(blur))


def highlighter(d, box, color=YELLOW):
    """Marker swipe: slightly uneven ends, sits behind text."""
    x0, y0, x1, y1 = box
    d.polygon([(x0 - 6, y0 + 4), (x1 + 4, y0), (x1 + 8, y1 - 2), (x0 - 2, y1 + 3)], fill=color)


def dotted_row(d, x0, x1, y, left, right, f, fill=INK):
    d.text((x0, y), left, font=f, fill=fill)
    rw = d.textlength(right, font=f)
    d.text((x1 - rw, y), right, font=f, fill=fill)
    lx = x0 + d.textlength(left, font=f) + 10
    dots = "." * max(0, int((x1 - rw - 10 - lx) / d.textlength(".", font=f)))
    d.text((lx, y), dots, font=f, fill=GREY)


def receipt_mark(scale=1.0):
    """The mark: a torn receipt, big 'B', item rows priced '$?.??', TOTAL row highlighted."""
    w, h = int(430 * scale), int(590 * scale)
    r = receipt(w, h, tooth=int(22 * scale), depth=int(14 * scale))
    d = ImageDraw.Draw(r)
    m = int(38 * scale)
    fm = font(MONO, int(30 * scale)); fmb = font(MONOB, int(34 * scale))
    fb = font(WORD, int(250 * scale))
    # big B
    bw = d.textlength("B", font=fb)
    d.text(((w - bw) / 2, int(18 * scale)), "B", font=fb, fill=INK)
    y = int(330 * scale)
    for item in ("ITEM", "ITEM"):
        dotted_row(d, m, w - m, y, item, "$?.??", fm, INK)
        y += int(44 * scale)
    d.line([(m, y + int(10 * scale)), (w - m, y + int(10 * scale))], fill=INK, width=max(2, int(3 * scale)))
    y += int(28 * scale)
    highlighter(d, (m - 4, y - 2, w - m + 4, y + int(44 * scale)))
    dotted_row(d, m, w - m, y + int(2 * scale), "TOTAL", "$", fmb, INK)
    return r


def logo():
    S = 800
    img = Image.new("RGBA", (S, S), RED + (255,))
    mark = receipt_mark(1.0).rotate(-7, resample=Image.BICUBIC, expand=True)
    sh = shadow(mark, off=(8, 12), blur=16, alpha=90)
    x, y = (S - mark.width) // 2, (S - mark.height) // 2 - 6
    img.alpha_composite(sh, (x - 40, y - 40))
    img.alpha_composite(mark, (x, y))
    img.convert("RGB").save(OUT + "logo_800.png")
    # small-size check: what the circle looks like at 98 px
    c = img.resize((98, 98), Image.LANCZOS)
    mk = Image.new("L", (98, 98), 0); ImageDraw.Draw(mk).ellipse((0, 0, 97, 97), fill=255)
    prev = Image.new("RGB", (140, 140), (255, 255, 255)); prev.paste(c, (21, 21), mk)
    prev.save(OUT + "logo_98_preview.png")


def watermark():
    mark = receipt_mark(0.32).rotate(-7, resample=Image.BICUBIC, expand=True)
    S = 150
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    img.alpha_composite(mark, ((S - mark.width) // 2, (S - mark.height) // 2))
    img.save(OUT + "watermark_150.png")


def banner():
    W, H = 2560, 1440
    img = Image.new("RGBA", (W, H), INK + (255,))
    # receipt band across the whole width, torn top and bottom
    bh = 560
    band = receipt(W + 40, bh, tooth=26, depth=16, top=True)
    by = (H - bh) // 2
    img.alpha_composite(shadow(band, off=(0, 16), blur=22, alpha=140), (-60, by - 40))
    img.alpha_composite(band, (-20, by))
    d = ImageDraw.Draw(img)
    # safe area for all devices: 1546 x 423 centred
    sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
    sx1, sy1 = sx0 + 1546, sy0 + 423
    fw = font(WORD, 128)
    t1, t2 = "The Bill, ", "Explained"
    w1, w2 = d.textlength(t1, font=fw), d.textlength(t2, font=fw)
    x = (W - (w1 + w2)) / 2
    ty = sy0 + 40
    hb = d.textbbox((x + w1, ty), t2, font=fw)
    highlighter(d, (hb[0] - 8, hb[1] + 52, hb[2] + 8, hb[3] + 14))
    d.text((x, ty), t1, font=fw, fill=INK)
    d.text((x + w1, ty), t2, font=fw, fill=INK)
    fm = font(MONO, 46); fmb = font(MONOB, 46)
    tag = "Why everyday things cost what they cost."
    d.text(((W - d.textlength(tag, font=fm)) / 2, ty + 190), tag, font=fm, fill=INK)
    dotted_row(d, sx0 + 210, sx1 - 210, ty + 280, "NEW BILL", "EVERY WEDNESDAY", fmb, INK)
    # desktop-only item rows left and right of the safe area (prices are the question)
    fi = font(MONO, 32)
    rows_l = [("GAS, 1 GAL", "$?.??"), ("EGGS", "$?.??"), ("NEW TRUCK", "$?????")]
    rows_r = [("RENT", "$????"), ("INSURANCE", "$???"), ("POWER BILL", "$???")]
    for i, (a, b) in enumerate(rows_l):
        dotted_row(d, 70, sx0 - 90, by + 120 + i * 70, a, b, fi, GREY)
    for i, (a, b) in enumerate(rows_r):
        dotted_row(d, sx1 + 90, W - 70, by + 120 + i * 70, a, b, fi, GREY)
    img.convert("RGB").save(OUT + "banner_2560x1440.png")
    chk = img.copy(); cd = ImageDraw.Draw(chk)
    cd.rectangle((sx0, sy0, sx1, sy1), outline=(0, 160, 255), width=4)          # all devices
    cd.rectangle(((W - 2560) // 2, (H - 423) // 2, W, (H + 423) // 2), outline=(0, 200, 0), width=3)  # desktop max
    chk.convert("RGB").resize((1280, 720)).save(OUT + "banner_safe_check.png")


if __name__ == "__main__":
    logo(); watermark(); banner()
    print("ok")
