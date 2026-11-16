"""thumbdoc: documentary-style thumbnails on REAL photos (the look of the million-view data-center videos:
Business Insider "SURROUNDED", More Perfect Union, ABC). No AI images.
Parts: photo grade, red/yellow label boxes, thick white arrows with black edge, rings, big number.
  from thumbdoc import *
  im = base(photo, crop); label(im, "AI DATA CENTERS", (x, y)); arrow(im, (x0, y0), (x1, y1)); ring(im, (cx, cy), r)"""
import sys, math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/the-bill-explained/tools")
from brandkit import font, shadow, WORD, NUM, RED, YELLOW, INK
from thumbkit import cover

W, H = 1280, 720
WHITE = (255, 255, 255)


def base(photo, crop=None, bright=1.0, contrast=1.15, color=1.1, vignette=0.45):
    im = cover(Image.open(photo).convert("RGB"), crop)
    im = ImageEnhance.Contrast(ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(bright)).enhance(color)).enhance(contrast)
    if vignette:
        m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
        d.ellipse((-W * 0.25, -H * 0.35, W * 1.25, H * 1.35), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(160))
        dark = Image.new("RGB", (W, H), (0, 0, 0))
        im = Image.composite(im, Image.blend(im, dark, vignette), m)
    return im.convert("RGBA")


def label(im, text, xy, bg=RED, fg=WHITE, size=64, pad=(22, 12), tilt=-2, fontp=WORD):
    f = font(fontp, size)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10))); l, t, r, b = d0.textbbox((0, 0), text, font=f)
    w, h = r - l + pad[0] * 2, b - t + pad[1] * 2
    box = Image.new("RGBA", (w, h), bg + (255,))
    ImageDraw.Draw(box).text((pad[0] - l, pad[1] - t), text, font=f, fill=fg)
    box = box.rotate(tilt, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(shadow(box, off=(6, 10), blur=10, alpha=150), (xy[0] - 40, xy[1] - 40))
    im.alpha_composite(box, xy)
    return (xy[0], xy[1], xy[0] + box.width, xy[1] + box.height)


def bigtext(im, text, xy, size=150, fill=WHITE, stroke=12, fontp=WORD):
    f = font(fontp, size)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10))); l, t, r, b = d0.textbbox((0, 0), text, font=f, stroke_width=stroke)
    lay = Image.new("RGBA", (r - l + 8, b - t + 8), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((4 - l, 4 - t), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    im.alpha_composite(shadow(lay, off=(8, 12), blur=14, alpha=170), (xy[0] - 40, xy[1] - 40))
    im.alpha_composite(lay, xy)
    return lay.size


def arrow(im, p0, p1, width=22, head=62, color=WHITE, edge=7, bend=0.18):
    """Curved hand-drawn style arrow p0 -> p1 (quadratic bend), white with black edge."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in [i / 40 for i in range(41)]]
    ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    tip = pts[-1]; back = (tip[0] - head * math.cos(ang), tip[1] - head * math.sin(ang))
    wing = lambda s: (back[0] + s * head * 0.6 * math.sin(ang), back[1] - s * head * 0.6 * math.cos(ang))
    shaft = pts[:-3] + [back]
    for col, extra in ((INK, edge * 2), (color, 0)):
        d.line(shaft, fill=col, width=width + extra, joint="curve")
        d.polygon([tip, wing(1), wing(-1)], fill=col, outline=col, width=extra or 1)
    im.alpha_composite(shadow(lay, off=(5, 8), blur=8, alpha=120), (-40, -40))
    im.alpha_composite(lay)


def ring(im, c, r, color=RED, width=12, ry=None):
    ry = ry or r
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    box = (c[0] - r, c[1] - ry, c[0] + r, c[1] + ry)
    d.ellipse(box, outline=INK, width=width + 8); d.ellipse(box, outline=color, width=width)
    im.alpha_composite(lay)


def save(im, out):
    im = im.convert("RGB"); im.save(out); im.save(out.replace(".png", "_upload.jpg"), quality=90)
    im.resize((320, 180), Image.LANCZOS).save(out.replace(".png", "_small.png"))
    return out
