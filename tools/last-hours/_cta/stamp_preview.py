"""Preview of the stamp on the REAL frames of each file (old stamp underneath on patched files): frosted band vs solid.
  uv run --no-project --with pillow --with numpy python stamp_preview.py [key ...] -> branded/gl/stamp_<key>.jpg"""
import sys, json, subprocess, io
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/_cta")
from PIL import Image, ImageDraw, ImageFont
import brand_anim as BA, brand_patch as BP
T = json.load(open("D:/why habibi/_newchannel/_cta/brand_times.json", encoding="utf-8")); F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
def grab(p, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert("RGBA")
for key in sys.argv[1:] or list(T):
    R = T[key]; rows = []
    for u0 in (0.1, 0.3, 0.7, 1.4, 2.05, 2.5):
        n = round((R["brand_t"] + u0) * 30); u = n / 30 - R["brand_t"]; f = grab(R["src"], (n - 0.5) / 30)
        a = BA.stamp_apply(BA.erase_old_stamp(f.copy(), u, BP.LABEL[key]), u, BP.LABEL[key])
        rows.append((round(u, 2), a.convert("RGB").crop((0, 330, 1920, 750)).resize((960, 210)), f.convert("RGB").crop((0, 330, 1920, 750)).resize((960, 210))))
    S = Image.new("RGB", (1940, len(rows) * 240 + 40), (20, 20, 22)); d = ImageDraw.Draw(S)
    d.text((10, 8), f"{key}: NEW see-through dark band", font=F, fill=(255, 210, 80)); d.text((980, 8), "the old upload (same frame)", font=F, fill=(170, 170, 170))
    for i, (u, a, b) in enumerate(rows):
        y = 40 + i * 240; S.paste(a, (10, y)); S.paste(b, (980, y)); d.text((14, y + 4), f"{u}s", font=F, fill=(255, 210, 80))
    S.save(f"D:/why habibi/_upload_queue_last_hours/branded/gl/stamp_{key}.jpg", quality=88); print(key, flush=True)
