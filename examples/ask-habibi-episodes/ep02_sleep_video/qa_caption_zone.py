"""QA sheet for the caption-zone fix: grab a frame from the FINAL export (captions burned in) in the middle of each
re-rendered beat, draw the caption band in red, tile them. Usage: qa_caption_zone.py [video] [out.png]"""
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont
from beats_ep02 import BEATS

ROOT = r"D:\why habibi\2nd video"
VIDEO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "export", "Ask_Habibi_Ep2_1440p.mp4")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "build", "qa_caption_zone.png")
CHANGED = [5, 6, 8, 11, 12, 13, 15, 16, 19, 21, 24, 25, 27, 30, 35, 36, 38, 39, 41, 43, 46, 48, 49, 51, 56, 57, 61, 63, 64,
           65, 66, 67, 68]

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", p],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])

starts, t = [], 0.0
for i, b in enumerate(BEATS):
    starts.append(t); t += dur(os.path.join(ROOT, "build", "beats", f"{i:02d}_{b.name}.mp4"))

W, H, COLS = 640, 360, 6
font = ImageFont.truetype(r"D:\why habibi\_style_kit\fonts\Rubik-Bold.ttf", 20)
tiles = []
for i in CHANGED:
    b = BEATS[i]; d = dur(os.path.join(ROOT, "build", "beats", f"{i:02d}_{b.name}.mp4"))
    ts = starts[i] + d * 0.8                     # late in the beat: every overlay has arrived
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ts:.2f}", "-i", VIDEO, "-frames:v", "1",
                          "-vf", f"scale={W}:{H}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    im = Image.open(__import__("io").BytesIO(png)).convert("RGB")
    dr = ImageDraw.Draw(im); k = W / 1920
    dr.rectangle([420 * k, 860 * k, 1500 * k, 1010 * k], outline=(255, 40, 40), width=2)
    dr.rectangle([0, 0, 260, 26], fill=(0, 0, 0)); dr.text((6, 2), f"{i:02d} {b.name} {ts:.1f}s", font=font, fill="white")
    tiles.append(im)

rows = (len(tiles) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * W, rows * H), "black")
for n, im in enumerate(tiles): sheet.paste(im, ((n % COLS) * W, (n // COLS) * H))
sheet.save(OUT); print("saved", OUT, len(tiles), "frames")
