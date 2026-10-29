"""Contact sheets (LESSONS 38): every clip at 8 evenly spaced points, every photo once, so a person checks each frame.
  uv run --no-project --with pillow python contact.py vid|img [prefix...]"""
import sys, os, glob, subprocess, json
from PIL import Image, ImageDraw, ImageFont
ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"; M = ROOT + "media/"; OUT = ROOT + "build/contact/"; os.makedirs(OUT, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None
F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 0)
def frame(p, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "-vf", "scale=384:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    import io; return Image.open(io.BytesIO(r.stdout)).convert("RGB") if r.stdout else Image.new("RGB", (384, 216))
mode = sys.argv[1]; pre = sys.argv[2:] or ["D", "E"]
if mode == "vid":
    for p in sorted(f for x in pre for f in glob.glob(M + x + "*") if f.endswith((".mp4", ".webm", ".ogv"))):
        d = dur(p); ts = [d * (k + 0.5) / 8 for k in range(8)]
        sheet = Image.new("RGB", (4 * 384, 2 * 230 + 30), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
        dr.text((6, 4), f"{os.path.basename(p)}  ({d:.1f}s)", font=F, fill=(255, 220, 0))
        for k, t in enumerate(ts):
            im = frame(p, t); im.thumbnail((384, 216)); x, y = (k % 4) * 384, 30 + (k // 4) * 230
            sheet.paste(im, (x, y)); dr.text((x + 4, y + 2), f"{t:.1f}s", font=F, fill=(255, 255, 255))
        sheet.save(OUT + os.path.basename(p).split("_")[0] + ("_" + os.path.basename(p).rsplit("_", 1)[1][:1] if os.path.basename(p).split("_")[0] in ("D1", "D2") else "") + ".jpg", quality=80)
        print("sheet", os.path.basename(p), round(d, 1))
else:
    files = sorted(f for x in pre for f in glob.glob(M + x + "*") if f.lower().endswith((".jpg", ".jpeg", ".png")))
    for s in range(0, len(files), 12):
        sheet = Image.new("RGB", (4 * 480, 3 * 330), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
        for k, f in enumerate(files[s:s + 12]):
            im = Image.open(f).convert("RGB"); im.thumbnail((470, 300)); x, y = (k % 4) * 480, (k // 4) * 330
            sheet.paste(im, (x + 5, y + 26)); dr.text((x + 6, y + 4), os.path.basename(f)[:44], font=F, fill=(255, 220, 0))
        sheet.save(OUT + f"img_{'_'.join(pre)}_{s // 12}.jpg", quality=80); print("sheet", s // 12, len(files[s:s + 12]))
