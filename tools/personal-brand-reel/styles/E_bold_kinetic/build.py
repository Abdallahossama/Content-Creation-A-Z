"""Style E 'Bold Kinetic' render: punch-in zoom on every cut and keyword (zoompan on a 2x upscale, no jitter),
b-roll + caption + title-card tracks from gen.py, whoosh/hit SFX.
usage: uv run --no-project python build.py [out.mp4] [--test SECONDS]"""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "D"))
from de_common import *

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else f"{OUTDIR}/style_E_bold_kinetic.mp4"
TEST = float(sys.argv[sys.argv.index("--test") + 1]) if "--test" in sys.argv else None
T = TEST or DUR
TL = json.load(open(HERE / "timeline_E.json", encoding="utf-8"))

# ---- zoom curve: alternate 1.00 / 1.06 on every jump cut, +0.06 punch on every keyword (max 1.12)
CUTS = [0.0, 2.36, 4.87, 8.09, 11.34, 12.68, 17.32, 21.62, 99]
lvl = "+".join(f"0.06*gte(it,{CUTS[i]})*lt(it,{CUTS[i+1]})" for i in range(1, len(CUTS) - 1, 2))
kws = sorted({round(s, 3) for s, e, g, kw in TL["groups"] if kw and kw in g})
bump = "+".join(f"0.06*(1-pow(1-clip((it-{k})/0.12,0,1),2))*clip(1-(it-{k+0.7:.3f})/0.45,0,1)" for k in kws)
Z = f"1+{lvl}+{bump}"
CY = 0.37  # zoom anchor on the face (fraction of height)

args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", BASE]
for tr in ["broll", "cap", "title"]:
    args += ["-framerate", "30", "-i", str(HERE / "tracks" / tr / "%04d.png")]
fc = ["[0:v]eq=contrast=1.07:saturation=0.97,scale=2160:3840:flags=lanczos,"
      f"zoompan=z='{Z}':x='(iw-iw/zoom)/2':y='ih*{CY}*(1-1/zoom)':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p[zv]",
      "[1:v]format=rgba[br]", "[2:v]format=rgba[cp]", "[3:v]format=rgba[tt]",
      "[zv][br]overlay=0:1250:format=auto[v1]",
      "[v1][cp]overlay=0:990:format=auto[v2]",
      "[v2][tt]overlay=0:0:format=auto,scale=out_range=tv,format=yuv420p,setrange=tv[vout]"]

FX = []
for s, e, w in [(b[1], b[2], b[3]) for b in TL["broll"]]:
    FX.append(("whoosh_fast.wav", s - 0.05, -19))
for word, lab, s, e in TL["titles"]:
    FX.append(("impact_soft.wav", s, -14))
    FX.append(("whoosh_fast.wav", e - 0.06, -24))
for k in kws:
    FX.append(("pop.wav", k, -25))
aargs, mix = audio_chain(4, [f for f in FX if f[1] < T])
args += aargs
fc += mix
(HERE / "filter_E.txt").write_text(";\n".join(fc), encoding="utf-8")
args += ["-filter_complex_script", "filter_E.txt", "-map", "[vout]", "-map", "[aout]", "-t", f"{T}"] + ENC + [OUT]
subprocess.run(args, check=True, cwd=HERE)
print("done", OUT)
