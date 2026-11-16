"""thumbhero: bold thumbnail on a cinematic AI scene (replaces the flat stock-photo look of thumbkit).
Layout: full-bleed scene, dark fade on the text side, 2 short lines of huge Arial Black
(line 1 white, line 2 yellow) with a thick black outline, plus the red price tag with the money number.
Max ~4 words in total; never repeat the title. Keep clear of the timestamp (bottom-right ~170x70).
  hero(scene_png, ["YOU'RE PAYING", "FOR AI"], "+$43", out, side="left")"""
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/the-bill-explained/tools")
from brandkit import font, shadow, WORD, YELLOW
from thumbkit import cover, price_tag

W, H = 1280, 720


def outlined(text, size, fill, stroke=14):
    f = font(WORD, size)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    l, t, r, b = d0.textbbox((0, 0), text, font=f, stroke_width=stroke)
    im = Image.new("RGBA", (r - l + 8, b - t + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - l, 4 - t), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return im


def fit(text, maxw, size, fill):
    while True:
        im = outlined(text, size, fill)
        if im.width <= maxw or size < 60: return im
        size -= 6


def hero(scene, lines, tag, out, side="left", crop=None, tag_xy=None, bright=1.0, maxw=760, size=118, tag_h=190):
    bg = cover(Image.open(scene).convert("RGB"), crop)
    bg = ImageEnhance.Contrast(ImageEnhance.Color(ImageEnhance.Brightness(bg).enhance(bright)).enhance(1.12)).enhance(1.1)
    img = bg.convert("RGBA")
    # dark fade behind the words
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    for x in range(W):
        k = x / W if side == "right" else 1 - x / W
        gd.line([(x, 0), (x, H)], fill=int(200 * max(0.0, k - 0.25) / 0.75))
    img.alpha_composite(Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), Image.new("RGBA", (W, H), (0, 0, 0, 0)), g))
    # words
    y = 46
    for i, ln in enumerate(lines):
        t = fit(ln, maxw, size, (255, 255, 255) if i == 0 else YELLOW)
        x = 40 if side == "left" else W - t.width - 40
        img.alpha_composite(shadow(t, off=(8, 12), blur=14, alpha=170), (x - 40, y - 40))
        img.alpha_composite(t, (x, y)); y += t.height - 6
    # price tag
    if tag:
        p = price_tag(tag, h=tag_h).rotate(8, resample=Image.BICUBIC, expand=True)
        if tag_xy is None:
            tag_xy = (40, H - p.height - 40) if side == "left" else (W - p.width - 200, H - p.height - 40)
        img.alpha_composite(shadow(p, off=(10, 14), blur=14, alpha=160), (tag_xy[0] - 40, tag_xy[1] - 40))
        img.alpha_composite(p, tag_xy)
    img = img.convert("RGB"); img.save(out)
    img.save(out.replace(".png", "_upload.jpg"), quality=90)
    img.resize((320, 180), Image.LANCZOS).save(out.replace(".png", "_small.png"))
    return out
