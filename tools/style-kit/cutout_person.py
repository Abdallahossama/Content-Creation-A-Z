"""Cut a person (or object) out of a plain studio backdrop without any ML model: fit a smooth quadratic to the backdrop
(top, left and right borders), mark pixels that differ from it, keep the component touching the bottom centre, fill holes.
  python cutout_person.py <in.jpg> <out.png> [threshold=26] [max_side=2400]"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def cut(src, out, thr=26, maxw=2400, seed=None, side=0.6):
    im = Image.open(src).convert("RGB"); im.thumbnail((maxw, maxw)); w, h = im.size; a = np.asarray(im, np.float32)
    b = max(4, int(min(w, h) * 0.03)); ys, xs = np.mgrid[0:h, 0:w]
    border = np.zeros((h, w), bool); border[:b] = True; border[:int(h * side), :b] = True; border[:int(h * side), -b:] = True
    X, Y = xs[border] / w, ys[border] / h; F = np.stack([np.ones_like(X), X, Y, X * X, Y * Y, X * Y], 1)
    Fa = np.stack([np.ones(w * h), (xs / w).ravel(), (ys / h).ravel(), ((xs / w) ** 2).ravel(), ((ys / h) ** 2).ravel(), ((xs / w) * (ys / h)).ravel()], 1)
    bg = np.stack([(Fa @ np.linalg.lstsq(F, a[..., k][border], rcond=None)[0]).reshape(h, w) for k in range(3)], 2)
    diff = np.abs(a - bg).max(2)
    m = Image.fromarray(np.where(diff > thr, 255, 0).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    m = m.filter(ImageFilter.MedianFilter(5)); mm = Image.new("L", m.size, 0); mm.paste(m)
    sx, sy = seed or (w // 2, h - 3)
    if mm.getpixel((sx, sy)) != 255:                                  # walk up from the bottom to find the subject
        for yy in range(h - 3, h // 3, -4):
            if mm.getpixel((sx, yy)) == 255: sy = yy; break
    ImageDraw.floodfill(mm, (sx, sy), 128)
    subj = np.asarray(mm) == 128
    inv = Image.new("L", m.size, 0); inv.paste(Image.fromarray(np.where(subj, 0, 255).astype(np.uint8)))
    for xy in ((0, 0), (w - 1, 0), (0, h // 2), (w - 1, h // 2)):
        if inv.getpixel(xy) == 255: ImageDraw.floodfill(inv, xy, 64)
    keep = np.asarray(inv) != 64
    al = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.3))
    rgba = im.copy(); rgba.putalpha(al); rgba = rgba.crop(al.point(lambda v: 255 if v > 100 else 0).getbbox()); rgba.save(out)
    return rgba

if __name__ == "__main__":
    r = cut(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 26, int(sys.argv[4]) if len(sys.argv) > 4 else 2400)
    print(sys.argv[2], r.size)
