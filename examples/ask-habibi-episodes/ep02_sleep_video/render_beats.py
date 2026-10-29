"""Render Ep 2 beats.   python render_beats.py qa [i,j,...]   -> build/qa_sheet.png (+ build/qa/NN.png)
                       python render_beats.py all [shard nshards] -> build/beats/NN_name.mp4 (frame-exact, 30 fps)"""
import sys, os, subprocess, time
from beats_ep02 import *

OUTB = BUILD + "beats/"; QA = BUILD + "qa/"
os.makedirs(OUTB, exist_ok=True); os.makedirs(QA, exist_ok=True)
FR = lambda t: int(round(t * FPS))

def qa(sel=None):
    tiles = []
    for i, b in enumerate(BEATS):
        if sel and i not in sel: continue
        tl = b.t0 + (b.t1 - b.t0) * 0.82
        c = b.frame(tl); b.close()
        c.convert("RGB").save(QA + f"{i:02d}.png")
        th = c.convert("RGB").resize((384, 216)); ImageDraw.Draw(th).text((6, 4), f"{i:02d} {b.name}", fill=(255, 255, 0))
        tiles.append(th); print("qa", i, b.name, flush=True)
    cols = 6; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 384, rows * 216), (20, 20, 20))
    for k, t in enumerate(tiles): sheet.paste(t, ((k % cols) * 384, (k // cols) * 216))
    sheet.save(BUILD + "qa_sheet.png"); print("sheet", BUILD + "qa_sheet.png")

def render(shard=0, n=1):
    for i, b in enumerate(BEATS):
        if i % n != shard: continue
        out = OUTB + f"{i:02d}_{b.name}.mp4"
        f0, f1 = FR(b.t0), FR(b.t1)
        if os.path.exists(out) and os.path.getsize(out) > 1000: continue
        t = time.time()
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                               "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out + ".tmp.mp4"],
                              stdin=subprocess.PIPE)
        for f in range(f0, f1):
            ff.stdin.write(b.frame(f / FPS).convert("RGB").tobytes())
        ff.stdin.close(); ff.wait(); b.close()
        os.replace(out + ".tmp.mp4", out)
        print(f"beat {i:02d} {b.name}: {f1 - f0} frames in {time.time() - t:.0f}s", flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "qa": qa({int(x) for x in sys.argv[2].split(",")} if len(sys.argv) > 2 else None)
    else: render(int(sys.argv[2]) if len(sys.argv) > 2 else 0, int(sys.argv[3]) if len(sys.argv) > 3 else 1)
