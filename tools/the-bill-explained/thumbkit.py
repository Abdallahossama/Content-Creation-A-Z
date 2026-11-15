"""The Bill, Explained - thumbnail template (1280x720).
Look: one REAL object photo, big, full bleed + a red price tag with the money number + a small torn-receipt
strip (2-4 words, mono, highlighter). Never repeat the title; no faces unless men only; no AI images.
  from thumbkit import thumb
  thumb(photo, crop=(x0,y0,x1,y1), tag="+$2.00", strip="DIESEL vs GAS", out="...png")
Run directly for the demo: python tools/thumbkit.py
"""
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/the-bill-explained/tools")
from brandkit import receipt, shadow, highlighter, font, INK, RED, YELLOW, WORD, NUM, MONOB

W, H = 1280, 720


def cover(img, crop=None):
    if crop: img = img.crop(crop)
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


def price_tag(text, h=200):
    f = font(NUM, int(h * 0.72))
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = tmp.textlength(text, font=f)
    point = int(h * 0.42)
    w = int(tw + point + h * 0.45)
    tag = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tag)
    d.polygon([(0, h // 2), (point, 0), (w, 0), (w, h), (point, h)], fill=RED)
    hole = int(h * 0.09)
    d.ellipse((point * 0.55 - hole, h / 2 - hole, point * 0.55 + hole, h / 2 + hole), fill=(0, 0, 0, 0))
    bb = d.textbbox((0, 0), text, font=f)
    d.text((point + (w - point - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=(255, 255, 255))
    return tag


def strip(text):
    f = font(MONOB, 52)
    tw = ImageDraw.Draw(Image.new("RGB", (10, 10))).textlength(text, font=f)
    w, h = int(tw + 70), 104
    r = receipt(w, h, tooth=14, depth=9, top=True)
    d = ImageDraw.Draw(r)
    highlighter(d, (28, 52, w - 28, 82))
    d.text((35, 22), text, font=f, fill=INK)
    return r


def thumb(photo, crop=None, tag="$?", strip_text="", out="thumb.png", tag_xy=None, strip_xy=(40, 36),
          darken=0.92):
    bg = cover(Image.open(photo).convert("RGB"), crop)
    bg = ImageEnhance.Contrast(ImageEnhance.Brightness(bg).enhance(darken)).enhance(1.12)
    img = bg.convert("RGBA")
    t = price_tag(tag).rotate(8, resample=Image.BICUBIC, expand=True)
    if tag_xy is None:   # keep clear of the edge and of YouTube's timestamp (bottom-right ~170x70)
        tag_xy = (W - t.width - 40, H - t.height - 95)
    img.alpha_composite(shadow(t, off=(10, 14), blur=14, alpha=150), (tag_xy[0] - 40, tag_xy[1] - 40))
    img.alpha_composite(t, tag_xy)
    if strip_text:
        s = strip(strip_text).rotate(-3, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(shadow(s, off=(6, 10), blur=10, alpha=140), (strip_xy[0] - 40, strip_xy[1] - 40))
        img.alpha_composite(s, strip_xy)
    img = img.convert("RGB")
    img.save(out)
    # phone-size check (what the feed shows)
    img.resize((320, 180), Image.LANCZOS).save(out.replace(".png", "_small.png"))
    return out


if __name__ == "__main__":
    thumb("D:/why habibi/_ASK_HABIBI_ARCHIVE (delete me)/_media/photos_s09/fuel_pump.jpg",
          crop=(80, 470, 1960, 1180), tag="+$2.00", strip_text="DIESEL vs GAS",
          out="D:/the-bill-explained/brand/thumb_demo_diesel.png")
    print("ok")
