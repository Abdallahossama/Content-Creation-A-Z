"""Render the edited reel from plan.json.

plan.json = {
  "src": "...mp4",
  "out": "...mp4",
  "keep": [[start, end, zoom], ...],          # source seconds; zoom 1.0 or e.g. 1.1
  "captions": [[src_start, src_end, "text", "orange word or ''"], ...]
}
"""
import json, subprocess, sys

plan = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "plan.json", encoding="utf-8"))
SRC, OUT = plan["src"], plan["out"]
keep = plan["keep"]
grade = open("grade.txt", encoding="utf-8").read().strip()
W, H = 1080, 1920
FADE = 0.012  # tiny audio fades so cuts don't click


def remap(t):
    """Source time -> output time, or None if t is cut."""
    acc = 0.0
    for s, e, *_ in keep:
        if s - 0.05 <= t <= e + 0.05:
            return acc + min(max(t, s), e) - s
        acc += e - s
    return None


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


# ---- captions (ASS) ----
ORANGE = "&H002B4FFF"  # #FF4F2B in ASS BGR
lines = []
for s, e, text, hl in plan["captions"]:
    a, b = remap(s), remap(e)
    if a is None or b is None or b - a < 0.15:
        continue
    t = text
    if hl:
        t = t.replace(hl, "{\\c" + ORANGE + "}" + hl + "{\\c&H00ECF0F2&}")
    lines.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{{\\fad(60,0)\\t(0,120,\\fscx104\\fscy104)\\t(120,200,\\fscx100\\fscy100)}}{t}")

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Alexandria ExtraBold,82,&H00ECF0F2,&H00ECF0F2,&H00151515,&H96000000,-1,0,0,0,100,100,0,0,1,3,4,2,80,80,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(lines) + "\n"
open("captions.ass", "w", encoding="utf-8").write(ass)

# ---- filter graph ----
fc = []
for i, (s, e, z) in enumerate(keep):
    d = e - s
    zf = f",scale={int(W*z)//2*2}:{int(H*z)//2*2},crop={W}:{H}:(iw-{W})/2:(ih-{H})*0.35" if z != 1.0 else ""
    fc.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS,scale={W}:{H}{zf},setsar=1,fps=30[v{i}]")
    fc.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d={FADE},afade=t=out:st={d-FADE:.3f}:d={FADE}[a{i}]")
n = len(keep)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
fc.append(f"[vc]{grade},ass=captions.ass:fontsdir=fonts:shaping=complex[vout]")
voice = ("highpass=f=85,lowpass=f=14000,afftdn=nr=12:nf=-42:tn=1,"
         "equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=7000:t=q:w=1:g=-1.5,"
         "acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=4,"
         "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000")
fc.append(f"[ac]{voice}[aout]")
open("filter.txt", "w", encoding="utf-8").write(";\n".join(fc))

cmd = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", SRC, "-filter_complex_script", "filter.txt",
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
       "-c:a", "aac", "-b:a", "192k", OUT]
print("output length:", round(sum(e - s for s, e, *_ in keep), 2), "s;", len(lines), "captions")
subprocess.run(cmd, check=True)
