"""Paper-collage / Pistachio edit of the base reel.
usage: uv run --no-project python build.py <music|halal> <out.mp4>
"""
import re, subprocess, sys

mode, OUT = sys.argv[1], sys.argv[2]
BASE, DUR = "base.mp4", 23.21
SFX = "D:/why habibi/_style_kit/sfx/"
BED = {"music": ("D:/why habibi/_music_library/Late Night Radio.mp3", -18),
       "halal": ("D:/codebyabdullah_assets/music/halal_nasheed_60.mp3", -21)}[mode]

# caption timings (base timeline) from the previous word-timed captions
ass = open("captions.ass", encoding="utf-8").read()
def t2s(t):
    h, m, s = t.split(":"); return int(h) * 3600 + int(m) * 60 + float(s)
CAPT = [(t2s(a), t2s(b)) for a, b in re.findall(r"^Dialogue: 0,([^,]+),([^,]+),Cap,", ass, re.M)]
assert len(CAPT) == 21

# ---- timeline -------------------------------------------------------------
# (png, start, end, x, y, scale, anim)  anim: slide | fade | none | drop
CARDS = [("card_analysis", 0.95, 2.36), ("card_process", 2.40, 4.00), ("card_prd", 5.70, 8.09),
         ("card_comment", 11.40, 13.10), ("card_inbox", 14.00, 16.90)]
POLS = [("pol_rakeeza", 8.89, 11.30, 10), ("pol_athar", 9.12, 11.30, 490),
        ("pol_home_top", 18.40, 21.50, 110)]
CARD_CY = 1335
LAYERS = []
for n, s, e in CARDS:
    LAYERS.append((f"png/{n}.png", s, e, 198, CARD_CY - 576 // 2, 0.9, "slide"))
for n, s, e, x in POLS:
    LAYERS.append((f"png/{n}.png", s, e, x, CARD_CY - (260 if "home" in n else 230), 1.0, "slide"))
card_win = [(l[1], l[2]) for l in LAYERS]

for s, e in [(0.0, 2.36), (11.34, 14.26), (20.20, DUR)]:
    LAYERS.append(("png/frame_solid.png", s, e, 0, 0, 1.0, "none"))
LAYERS.append(("png/frame_dash.png", 5.79, 8.09, 0, 0, 1.0, "none"))
for i, (s, e) in enumerate([(0.95, 4.00), (4.87, 8.09), (8.89, 11.34)], 1):
    LAYERS.append((f"png/pill_{i}.png", s, e, 280, 100, 1.0, "drop"))

# captions (skip the two lines carried by paper beats)
CAP_Y, CAP_Y_LOW = 1180, 1505
for i, (s, e) in enumerate(CAPT):
    if i in (5, 10):
        continue
    low = any(s < ce and e > cs + 0.05 for cs, ce in card_win)
    LAYERS.append((f"png/cap_{i:02d}.png", s, e, 0, CAP_Y_LOW if low else CAP_Y, 1.0, "cap"))

# paper interlude 1 + collage beat (drawn last, full screen)
P1, P2 = (4.00, 4.87), (8.09, 8.89)
LAYERS += [("png/paper1_bg.png", *P1, 0, 0, 1.0, "none"), ("png/paper1_box.png", P1[0] + 0.08, P1[1], 0, 0, 1.0, "drop"),
           ("png/paper2_bg.png", *P2, 0, 0, 1.0, "none"), ("STICKER", *P2, 0, 0, 1.0, "none"),
           ("png/paper2_box.png", P2[0] + 0.10, P2[1], 0, 0, 1.0, "drop")]

CL = "D:/codebyabdullah_assets/workspace/edit_paper/click.wav"
FX = [("swoosh_in.wav", 0.93, -18), (CL, 2.40, -20), (CL, 0.95, -22),
      ("whoosh_long.wav", 3.98, -20), (CL, 4.08, -18), ("swoosh_in.wav", 4.86, -20),
      ("swoosh_in.wav", 5.68, -18), (CL, 4.87, -22), ("whoosh_long.wav", 8.07, -20), (CL, 8.19, -18),
      (CL, 8.89, -20), (CL, 9.12, -22), ("swoosh_in.wav", 11.38, -18),
      ("swoosh_in.wav", 13.98, -18), ("swoosh_in.wav", 18.38, -18)]

# ---- graph ------------------------------------------------------------------
args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", BASE]
fc, prev, k = ["[0:v]eq=contrast=1.04:saturation=0.96,format=yuv420p[g0]"], "g0", 1
for j, (png, s, e, x, y, sc, an) in enumerate(LAYERS):
    if png == "STICKER":
        args += ["-itsoffset", "8.0", "-i", "sticker_clean.mov"]
        a = -3 * 3.14159265 / 180
        fc.append(f"[{k}:v]format=rgba,"
                  f"fade=t=in:st={s}:d=0.06:alpha=1[L{j}]")
        ox, oy = "0", f"250+60*pow(max(0\\,1-(t-{s})/0.2)\\,2)"
    else:
        args += ["-loop", "1", "-t", f"{e + 0.3:.2f}", "-framerate", "30", "-i", png]
        sca = f"scale=iw*{sc}:-1," if sc != 1.0 else ""
        fade = {"slide": f"fade=t=in:st={s}:d=0.16:alpha=1,fade=t=out:st={e-0.12}:d=0.12:alpha=1",
                "fade": f"fade=t=in:st={s}:d=0.2:alpha=1",
                "cap": f"fade=t=in:st={s}:d=0.07:alpha=1",
                "drop": f"fade=t=in:st={s}:d=0.05:alpha=1", "none": "null"}[an]
        fc.append(f"[{k}:v]format=rgba,{sca}{fade}[L{j}]")
        ox = str(x)
        oy = {"slide": f"{y}+60*pow(max(0\\,1-(t-{s})/0.22)\\,2)",
              "cap": f"{y}+14*max(0\\,1-(t-{s})/0.12)",
              "drop": f"{y}-40*pow(max(0\\,1-(t-{s})/0.12)\\,2)"}.get(an, str(y))
    fc.append(f"[{prev}][L{j}]overlay=x={ox}:y='{oy}':eof_action=pass:enable='between(t,{s},{e})'[v{j}]")
    prev, k = f"v{j}", k + 1
fc.append(f"[{prev}]scale=out_range=tv,format=yuv420p,setrange=tv[vout]")

mix, labels = ["[0:a]asplit=2[voice][key]"], ["[voice]"]
for j, (f, at, g) in enumerate(FX):
    args += ["-i", f if ":" in f else SFX + f]
    mix.append(f"[{k+j}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={int(at*1000)}:all=1[fx{j}]")
    labels.append(f"[fx{j}]")
b = k + len(FX)
args += ["-stream_loop", "-1", "-i", BED[0]]
mix.append(f"[{b}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR},volume={BED[1]}dB,"
           f"afade=t=in:d=0.8,afade=t=out:st={DUR-1.8}:d=1.8[bedraw]")
mix.append("[bedraw][key]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=300[bed]")
labels.append("[bed]")
mix.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.89,"
           "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
fc += mix
open("filter.txt", "w", encoding="utf-8").write(";\n".join(fc))
args += ["-filter_complex_script", "filter.txt", "-map", "[vout]", "-map", "[aout]", "-t", f"{DUR}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-color_range", "tv", "-r", "30", "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "192k", OUT]
subprocess.run(args, check=True)
