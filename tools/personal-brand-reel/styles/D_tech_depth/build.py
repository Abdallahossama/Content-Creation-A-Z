"""Style D 'Tech Depth' render. Background is darkened and desaturated (kills the warm lamp), dark UI panels
sit between the background and the person (mask from tmp_masks), so his hair overlaps the panel corner.
usage: uv run --no-project python build.py [out.mp4] [--test SECONDS]"""
import pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from de_common import *

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else f"{OUTDIR}/style_D_tech_depth.mp4"
TEST = float(sys.argv[sys.argv.index("--test") + 1]) if "--test" in sys.argv else None
T = TEST or DUR

L, R, Y = 36, 574, 170
# (prefix, n_states, start, end, x, step)
PANELS = [("an", 7, 0.25, 4.85, L, 0.32), ("prd", 7, 4.95, 8.85, R, 0.30), ("tst", 6, 8.95, 11.28, L, 0.26),
          ("cm", 2, 11.40, 12.62, R, 0.60), ("ib", 6, 12.75, 17.25, L, 0.34), ("ho", 5, 17.40, 22.95, R, 0.42)]
TAGS = [(0.30, 4.87), (4.87, 8.89), (8.89, 11.34), (11.34, 12.68), (12.68, 17.32), (17.32, 23.0)]
F = 0.16

args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", BASE, "-framerate", "30", "-i", MASKS]
fc = ["[0:v]format=yuv420p,split[b0][p0]",
      "[b0]eq=brightness=-0.10:contrast=1.06:saturation=0.40,vignette=angle=0.55,format=yuv420p[bg]",
      "[p0]eq=contrast=1.04:saturation=0.92,format=rgba[pc]",
      "[1:v]format=gray,scale=1080:1920[m]", "[pc][m]alphamerge[person]"]
k, prev, j = 2, "bg", 0
FX = []
def ov(png, s, e, x, y, fin, fout, slide):
    global k, prev, j
    args.extend(["-loop", "1", "-framerate", "30", "-t", f"{T:.2f}", "-i", png])
    fx = "format=rgba"
    if fin: fx += f",fade=t=in:st={s}:d={F}:alpha=1"
    if fout: fx += f",fade=t=out:st={e-F:.2f}:d={F}:alpha=1"
    fc.append(f"[{k}:v]{fx}[s{j}]")
    yy = f"'{y}+{slide}*pow(max(0\\,1-(t-{s})/0.22)\\,2)'" if fin and slide else str(y)
    fc.append(f"[{prev}][s{j}]overlay=x={x}:y={yy}:enable='between(t,{s},{e})'[o{j}]")
    prev, k, j = f"o{j}", k + 1, j + 1

for pre, n, s, e, x, step in PANELS:
    for i in range(n):
        a = s + i * step; b = s + (i + 1) * step if i < n - 1 else e
        ov(f"png/{pre}{i+1}.png", round(a, 3), round(b, 3), x, Y, i == 0, i == n - 1, 26)
        FX.append((CLICK, a + 0.02, -27 if i else -24))
    FX.append(("swoosh_in.wav", s - 0.03, -23))

fc.append(f"[{prev}][person]overlay=0:0[wp]"); prev = "wp"
for i, (s, e) in enumerate(TAGS, 1):
    ov(f"png/tag{i}.png", s, e, 320, 1190, True, True, 12)
ass = "captions_D.ass"
fc.append(f"[{prev}]ass={ass}:fontsdir=../../edit/fonts:shaping=complex,scale=out_range=tv,format=yuv420p,setrange=tv[vout]")

aargs, mix = audio_chain(k, [f for f in FX if f[1] < T])
args += aargs
fc += mix
(HERE / "filter_D.txt").write_text(";\n".join(fc), encoding="utf-8")
args += ["-filter_complex_script", "filter_D.txt", "-map", "[vout]", "-map", "[aout]", "-t", f"{T}"] + ENC + [OUT]
subprocess.run(args, check=True, cwd=HERE)
print("done", OUT)
