"""Contact sheet of media/ (checks: no women, real images, legibility). usage: build_sheet.py <out.png> [prefix...]"""
import sys, glob, os
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
M = "D:/why habibi/_newchannel/06_flannan/media/"
pre = sys.argv[2:] or [""]
fs = sorted(f for f in glob.glob(M + "*") if any(os.path.basename(f).startswith(p) for p in pre) and not f.endswith(".bad"))
tw, th, cols = 360, 270, 5
S = Image.new("RGB", (cols * (tw + 10), ((len(fs) + cols - 1) // cols) * (th + 30)), (25, 25, 25)); d = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    try:
        im = Image.open(f); im.draft("RGB", (tw * 2, th * 2)); im = im.convert("RGB"); w, h = im.size
    except Exception as e:
        print("ERR", f, e); continue
    im.thumbnail((tw, th)); x, y = (i % cols) * (tw + 10), (i // cols) * (th + 30)
    S.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
    d.text((x + 4, y + th + 6), f"{os.path.basename(f)[:40]} {w}x{h}", fill=(255, 220, 90))
S.save(sys.argv[1]); print(sys.argv[1], len(fs))
