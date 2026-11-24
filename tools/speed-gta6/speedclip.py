"""speedclip: turn a stream section into a 1080x1920 Short.
Layout: facecam (top 700 px) over gameplay (bottom 1220 px), hook title bar at the seam,
word-by-word captions (current word yellow), small source credit. Curse words masked.
  python speedclip.py <section.mp4> <words.json> <out.mp4> "<HOOK TEXT>" fx fy fw fh [t0 t1]
fx..fh = facecam box as fractions of the source frame. t0/t1 trim inside the section (seconds)."""
import sys, json, re, subprocess, os

src, wj, out, hook = sys.argv[1:5]
fx, fy, fw, fh = (float(v) for v in sys.argv[5:9])
t0 = float(sys.argv[9]) if len(sys.argv) > 9 else 0.0
t1 = float(sys.argv[10]) if len(sys.argv) > 10 else None
BAD = re.compile(r"\b(f+u+c*k+\w*|sh+i+t+\w*|bitch\w*|n+i+g+\w*|ass(hole)?|damn|dick\w*|pussy|motherf\w*|hell)\b", re.I)
def clean(w): return BAD.sub(lambda m: m.group(0)[0] + "*" * (len(m.group(0)) - 1), w)
def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

words = [w for w in json.load(open(wj, encoding="utf-8")) if w["s"] >= t0 and (t1 is None or w["e"] <= t1)]
for w in words: w["s"] -= t0; w["e"] -= t0; w["w"] = clean(w["w"].strip()).upper()
chunks, cur = [], []
for w in words:
    cur.append(w)
    if len(cur) >= 3 or w["w"].endswith((".", "!", "?", ",")): chunks.append(cur); cur = []
if cur: chunks.append(cur)

ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Arial Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,9,3,5,40,40,0,1",
       "Style: Hook,Arial Black,64,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,18,0,5,60,60,0,1",
       "Style: Credit,Arial,34,&H00E0E0E0,&H00E0E0E0,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,40,40,40,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
dur = (t1 - t0) if t1 else (words[-1]["e"] + 1.0 if words else 45)
ass.append(f"Dialogue: 2,{ts(0)},{ts(dur)},Hook,,0,0,0,,{{\\pos(540,700)}}{hook}")
ass.append(f"Dialogue: 2,{ts(0)},{ts(dur)},Credit,,0,0,0,,clip: @IShowSpeed (YouTube live)")
for ch in chunks:
    for i, w in enumerate(ch):
        end = ch[i + 1]["s"] if i + 1 < len(ch) else w["e"] + 0.25
        txt = " ".join(("{\\c&H00D7FF&}" + x["w"] + "{\\c&HFFFFFF&}") if j == i else x["w"] for j, x in enumerate(ch))
        ass.append(f"Dialogue: 1,{ts(w['s'])},{ts(end)},Cap,,0,0,0,,{{\\pos(540,1330)}}{txt}")
ap = out.replace(".mp4", ".ass"); open(ap, "w", encoding="utf-8").write("\n".join(ass) + "\n")

sub = ap.replace("\\", "/").replace(":", "\\:")
FIT = os.environ.get("SC_FIT")
if FIT:   # landscape camera clip: 16:9 video centred on a blurred fill, hook above it, captions below
    ass = [l.replace("{\\pos(540,700)}", "{\\pos(540,470)}") for l in ass]
    open(ap, "w", encoding="utf-8").write("\n".join(ass) + "\n")
BLUR = ",gblur=sigma=45,eq=brightness=-0.12" if os.environ.get("SC_BLUR") else ""
if FIT:
    fc = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.25[bg];"
          f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2-80,setsar=1,subtitles='{sub}'[v]")
else:
    fc = (f"[0:v]crop=iw*{fw}:ih*{fh}:iw*{fx}:ih*{fy},scale=1080:700:force_original_aspect_ratio=increase,crop=1080:700[top];"
          f"[0:v]crop=ih*1080/1220:ih:(iw-ih*1080/1220)/2:0,scale=1080:1220{BLUR}[bot];"
          f"[top][bot]vstack,setsar=1,subtitles='{sub}'[v]")
cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(t0)] + (["-to", str(t1)] if t1 else []) + ["-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k",
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True); print(out)
