"""Split the owner's ChatGPT avatar sheets (3x2 grids, 1254x1254) into tiles and key out the flat grey background.
  uv run --no-project --with pillow --with numpy --with scipy python cut_avatar.py"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
A = "D:/why habibi/_newchannel/brand/avatar/"
EXPR = ["shock", "smirk", "think", "serious", "laugh", "disappointed"]

def key(im):
    a = np.asarray(im.convert("RGB"), np.float32)
    h, w, _ = a.shape
    border = np.concatenate([a[:4].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    bg = np.median(border, 0)
    d = np.sqrt(((a - bg) ** 2).sum(2)); sat = a.max(2) - a.min(2)
    cand = (d < 30) & (sat < 22)
    lab, n = ndimage.label(cand)                                  # only grey regions touching top/left/right edges, or big ones
    keep = set(np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]]))) - {0}
    sizes = ndimage.sum(cand, lab, range(1, n + 1))
    for i, s in enumerate(sizes, 1):
        if s > 0.004 * h * w: keep.add(i)
    bgm = np.isin(lab, list(keep))
    bgm = ndimage.binary_opening(bgm, iterations=1)
    alpha = Image.fromarray(((~bgm) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA"); out.putalpha(alpha)
    return out.crop(out.getbbox())

if __name__ == "__main__":
    for s in range(5, 10):
        im = Image.open(A + f"raw/img{s}.webp").convert("RGB"); W, H = im.size
        for r in range(2):
            for c in range(3):
                t = im.crop((int(c * W / 3) + 6, int(r * H / 2) + 6, int((c + 1) * W / 3) - 6, int((r + 1) * H / 2) - 4))
                name = f"{EXPR[r * 3 + c]}_s{s}"
                t.save(A + f"tiles/{name}.png"); key(t).save(A + f"cut/{name}.png")
    key(Image.open(A + "raw/img10.webp")).save(A + "cut/hero_file_flashlight.png")
    key(Image.open(A + "host_master_v2.webp")).save(A + "cut/master.png")
    # contact sheet on dark red/black checker to see the edges
    import glob, os
    fs = sorted(glob.glob(A + "cut/*.png")); cols = 8; tw, th = 240, 320
    S = Image.new("RGB", (cols * tw, ((len(fs) + cols - 1) // cols) * th), (30, 10, 10))
    for i, p in enumerate(fs):
        t = Image.open(p); t.thumbnail((tw - 10, th - 30)); bgc = Image.new("RGBA", (tw, th), (20, 20, 24, 255) if (i // cols) % 2 == 0 else (70, 20, 20, 255))
        bgc.alpha_composite(t, ((tw - t.width) // 2, th - 30 - t.height)); S.paste(bgc.convert("RGB"), ((i % cols) * tw, (i // cols) * th))
        from PIL import ImageDraw; ImageDraw.Draw(S).text(((i % cols) * tw + 4, (i // cols) * th + th - 22), os.path.basename(p)[:-4], fill=(255, 220, 0))
    S.save(A + "_cut_sheet.jpg", quality=85); print(len(fs), "cut")
