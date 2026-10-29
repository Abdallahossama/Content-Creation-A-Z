"""Final Ep 4 video: concat the beat clips (frame-exact), burn the captions, add the -14 LUFS mix, upscale to 1440p
(YouTube gives 1440p uploads its better codec). -> D:/why habibi/4th video/export/Ask_Habibi_Ep4_1440p.mp4"""
import os, subprocess, shutil, sys
from ep04_common import *
from beats_ep04 import BEATS

B = BUILD; EXP = EP + "export/"; os.makedirs(EXP, exist_ok=True)
files = sorted(f for f in os.listdir(B + "beats") if f.endswith(".mp4") and not f.endswith(".tmp.mp4"))
assert len(files) == len(BEATS), f"{len(files)}/{len(BEATS)} beats rendered"
with open(B + "concat.txt", "w", encoding="utf-8") as f:
    for x in files: f.write(f"file 'beats/{x}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "video_ep04.mp4"], cwd=B, check=True)
os.makedirs(B + "fonts", exist_ok=True); shutil.copy2("D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf", B + "fonts/Rubik-Bold.ttf")
res = sys.argv[1] if len(sys.argv) > 1 else "1440"
w, h = (2560, 1440) if res == "1440" else (1920, 1080)
out = EXP + f"Ask_Habibi_Ep4_{res}p.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-stats", "-y", "-i", "video_ep04.mp4", "-i", "mix_ep04.wav",
                "-vf", f"scale={w}:{h}:flags=lanczos,subtitles=captions_ep04.ass:fontsdir=fonts",
                "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                "-r", "30", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", out], cwd=B, check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "csv=p=0", out], capture_output=True, text=True).stdout
print("exported", out, d.strip())
