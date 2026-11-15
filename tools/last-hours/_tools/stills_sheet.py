"""Contact sheet of every still in a media folder (id-sorted, labelled) for shot planning.
  uv run --no-project --with pillow python stills_sheet.py <media dir> <out.jpg>"""
import sys, glob, os, re
from PIL import Image, ImageDraw, ImageFont

M, out = sys.argv[1], sys.argv[2]
def key(f):
    b = os.path.basename(f); m = re.match(r"([A-Z])(\d+)", b)
    return (m.group(1), int(m.group(2)), b) if m else ("~", 0, b)
fs = sorted([f for f in glob.glob(M + "/*") if re.search(r"\.(jpe?g|png)$", f, re.I) and not os.path.basename(f).startswith("_")], key=key)
W, H, C = 300, 190, 9
rows = (len(fs) + C - 1) // C
sheet = Image.new("RGB", (W * C, rows * (H + 18)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
font = ImageFont.truetype("arial.ttf", 14)
for i, f in enumerate(fs):
    try:
        im = Image.open(f).convert("RGB"); im.thumbnail((W - 6, H - 6))
    except Exception:
        continue
    x, y = (i % C) * W, (i // C) * (H + 18)
    sheet.paste(im, (x + (W - im.width) // 2, y + 18 + (H - im.height) // 2))
    d.text((x + 4, y + 1), os.path.basename(f)[:40], fill=(255, 210, 60), font=font)
sheet.save(out, quality=85); print(len(fs), sheet.size)
