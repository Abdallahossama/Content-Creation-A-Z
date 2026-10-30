"""QA every File Keeper re-brand before the owner's bulk upload (owner, 30 Oct: "make sure everything is good").
Per file: length vs the original (+13.16 s mid ask, - the cut end lines, + the new end card), loudness, and a contact sheet of the moments
that can go wrong: the stamp (start / letters / file line), the case tab, the mid ask (in / buttons / out / the reveal after it),
the end card (the junction frame, the seal, the buttons, the last second). The junction tile must NOT show the old end card.
  uv run --no-project --with pillow --with numpy python brand_qa.py [key ...]  -> _upload_queue_last_hours/branded/qa_<key>.jpg"""
import sys, os, json, subprocess, re
from PIL import Image, ImageDraw, ImageFont
CTA = "D:/why habibi/_newchannel/_cta/"; B = "D:/why habibi/_upload_queue_last_hours/branded/"
T = json.load(open(CTA + "brand_times.json", encoding="utf-8")); F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 0)
def lufs(p):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); return float(m[-1]) if m else None
def grab(p, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", p, "-frames:v", "1", "-vf", "scale=320:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    import io; return Image.open(io.BytesIO(r.stdout)).convert("RGB") if r.stdout else Image.new("RGB", (320, 180))
for key in (sys.argv[1:] or list(T)):
    R = T[key]; out = B + os.path.basename(R["src"]).replace(".mp4", "_FILEKEEPER.mp4")
    if not os.path.exists(out): print(key, "MISSING", out); continue
    MID = 13.16; tm, cut = R["mid_t"], R["cut_t"] - 0.25; e0 = cut + MID                     # where the end card starts in the new file
    pts = [("stamp 0.3", R["brand_t"] + 0.3), ("stamp 1.0", R["brand_t"] + 1.0), ("stamp 1.8", R["brand_t"] + 1.8), ("tab 1.5", R["subpop_t"] + 1.5 + (MID if R["subpop_t"] > tm else 0)),
           ("before ask", tm - 0.6), ("ask 1.0", tm + 1.0), ("ask buttons", tm + 9.0), ("ask out", tm + 12.9), ("reveal", tm + MID + 1.0),
           ("end -0.4", e0 - 0.4), ("end +0.05", e0 + 0.05), ("end +0.5", e0 + 0.5), ("end +6", e0 + 6.0), ("end +14", e0 + 14.0), ("last", dur(out) - 0.3)]
    tiles = [(n, grab(out, t)) for n, t in pts]
    S = Image.new("RGB", (5 * 330, 3 * 210), (20, 20, 22)); d = ImageDraw.Draw(S)
    for i, (n, im) in enumerate(tiles):
        x, y = (i % 5) * 330 + 5, (i // 5) * 210 + 24; S.paste(im, (x, y)); d.text((x, y - 20), n, font=F, fill=(255, 210, 80))
    S.save(B + f"qa_{key}.jpg", quality=85)
    exp = R["dur_mp4"] - (R["dur_mp4"] - cut) + MID                                          # story + ask, before the end card
    print(f"{key:9s} {dur(out):7.2f}s (orig {R['dur_mp4']:.2f}s; story+ask {exp:.2f}s + end card {dur(out) - exp:.2f}s)  LUFS {lufs(out)}  -> qa_{key}.jpg", flush=True)
