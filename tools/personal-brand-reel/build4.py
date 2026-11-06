"""Pop-up cards kept OFF the face (chest area), captions drop under cards while shown.
usage: python build4.py <music|halal> <out.mp4>
"""
import re, subprocess, sys

mode, OUT = sys.argv[1], sys.argv[2]
BASE, DUR = "base.mp4", 23.21
SFX = "D:/why habibi/_style_kit/sfx/"
BED = {"music": ("D:/why habibi/_music_library/Late Night Radio.mp3", -18),
       "halal": ("D:/codebyabdullah_assets/music/halal_nasheed_60.mp3", -21)}[mode]
CY = 1280  # vertical centre of the card area (face ends ~1100)

# (png, start, end, x, width, angle)
OV = [("broll/analysis.png", 0.95, 2.36, 240, 600, -3), ("broll/process.png", 2.40, 4.40, 240, 600, 3),
      ("broll/prd.png", 5.70, 8.05, 240, 600, -3),
      ("broll/site_rakeeza.png", 8.90, 11.30, 45, 470, -3), ("broll/site_athar.png", 9.15, 11.30, 560, 470, 3),
      ("broll/comment.png", 11.40, 12.65, 240, 600, 3), ("broll/inbox.png", 14.00, 16.90, 240, 600, -3),
      ("broll/site_coachmind.png", 18.40, 21.50, 45, 470, 3), ("broll/site_home.png", 18.65, 21.50, 560, 470, -3)]
FX = [("swoosh_in.wav", 0.90, -12), ("swoosh_in.wav", 2.35, -13), ("whoosh_fast.wav", 5.65, -13),
      ("whoosh_fast.wav", 8.85, -12), ("pop.wav", 9.12, -15), ("pop.wav", 11.38, -12),
      ("swoosh_in.wav", 13.95, -13), ("whoosh_fast.wav", 18.35, -12), ("pop.wav", 18.62, -15)]

# captions: second style sitting under the cards
ass = open("captions.ass", encoding="utf-8").read()
cap_style = re.search(r"^Style: Cap,.*$", ass, re.M).group(0)
low = cap_style.replace("Style: Cap,", "Style: CapLow,").rsplit(",", 2)
low[-2] = "360"  # MarginV
ass = ass.replace(cap_style, cap_style + "\n" + ",".join(low))
win = [(s, e) for _, s, e, *_ in OV]
def t2s(t):
    h, m, s = t.split(":"); return int(h) * 3600 + int(m) * 60 + float(s)
def fix(m):
    st = t2s(m.group(1))
    inside = any(s - 0.12 <= st < e for s, e in win)
    return m.group(0).replace(",Cap,", ",CapLow,") if inside else m.group(0)
ass = re.sub(r"^Dialogue: 0,([^,]+),[^,]+,Cap,.*$", fix, ass, flags=re.M)
open("captions_low.ass", "w", encoding="utf-8").write(ass)

args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", BASE]
for png, s, e, *_ in OV:
    args += ["-loop", "1", "-t", f"{DUR}", "-framerate", "30", "-i", png]
for f, *_ in FX:
    args += ["-i", SFX + f]
args += ["-stream_loop", "-1", "-i", BED[0]]

fc, prev = ["[0:v]format=yuv420p," + open("glow.txt", encoding="utf-8").read().strip() + ",format=yuv420p[g0]"], "g0"
for i, (png, s, e, x, w, ang) in enumerate(OV, start=1):
    a = ang * 3.14159265 / 180
    site = "site_" in png
    h = round((w * 800 / 1280) if site else (w * 640 / 900)) + (12 if site else 0)
    y = CY - h // 2
    border = ",pad=iw+12:ih+12:6:6:color=0x2A2A2AFF" if site else ""
    fc.append(f"[{i}:v]format=rgba,scale={w}:-1{border},rotate={a}:c=none:ow=rotw({a}):oh=roth({a}),"
              f"fade=t=in:st={s}:d=0.16:alpha=1,fade=t=out:st={e-0.12}:d=0.12:alpha=1[o{i}]")
    fc.append(f"[{prev}][o{i}]overlay=x={x}:y='{y}+40*max(0\\,1-(t-{s})/0.2)':enable='between(t,{s},{e})'[b{i}]")
    prev = f"b{i}"
fc.append(f"[{prev}]ass=captions_low.ass:fontsdir=fonts:shaping=complex[vout]")

k = 1 + len(OV)
mix, labels = ["[0:a]asplit=2[voice][key]"], ["[voice]"]
for j, (f, at, g) in enumerate(FX):
    mix.append(f"[{k+j}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={int(at*1000)}:all=1[fx{j}]")
    labels.append(f"[fx{j}]")
b = k + len(FX)
mix.append(f"[{b}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR},volume={BED[1]}dB,"
           f"afade=t=in:d=0.8,afade=t=out:st={DUR-1.8}:d=1.8[bedraw]")
mix.append("[bedraw][key]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=300[bed]")
labels.append("[bed]")
mix.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.89,"
           "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
fc += mix
open("filter4.txt", "w", encoding="utf-8").write(";\n".join(fc))
args += ["-filter_complex_script", "filter4.txt", "-map", "[vout]", "-map", "[aout]", "-t", f"{DUR}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         "-c:a", "aac", "-b:a", "192k", OUT]
subprocess.run(args, check=True)
