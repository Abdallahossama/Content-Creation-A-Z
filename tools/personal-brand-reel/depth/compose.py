import re, subprocess, sys
DUR = 23.21; F = 0.15
# (png, start, end, layer, fade_in, fade_out)
S = []
def seq(names, times, end, layer):
    for i, n in enumerate(names):
        s = times[i]; e = times[i + 1] if i + 1 < len(names) else end
        S.append((f"p/{n}.png", s, e, layer, i == 0, i == len(names) - 1))
seq(["a1","a2","a3","a4","a5"], [0.95,1.15,1.35,1.55,1.75], 2.38, "B")
seq(["scope0","scope1","scope2","scope3","scope4"], [2.40,2.70,2.80,2.90,3.00], 4.40, "F")
seq(["prd1","prd2","prd3","prd4","prd5"], [5.70,5.95,6.20,6.45,6.70], 8.05, "B")
seq(["client"], [8.90], 11.30, "B")
seq(["cm0","cm1","cm2","cm3"], [11.40,11.55,11.70,11.85], 12.65, "F")
seq(["inbox"], [14.00], 16.90, "F")
seq(["home"], [18.40], 21.50, "B")
front_win = [(2.40, 4.40), (11.40, 12.65), (14.00, 16.90)]

ass = open("../captions.ass", encoding="utf-8").read()
st = re.search(r"^Style: Cap,.*$", ass, re.M).group(0)
low = st.replace("Style: Cap,", "Style: CapLow,").rsplit(",", 2); low[-2] = "360"
ass = ass.replace(st, st + "\n" + ",".join(low))
def t2s(t): h, m, s = t.split(":"); return int(h)*3600 + int(m)*60 + float(s)
ass = re.sub(r"^Dialogue: 0,([^,]+),[^,]+,Cap,.*$",
             lambda m: m.group(0).replace(",Cap,", ",CapLow,") if any(a-0.12 <= t2s(m.group(1)) < b for a, b in front_win) else m.group(0),
             ass, flags=re.M)
open("captions_depth.ass", "w", encoding="utf-8").write(ass)

glow = open("../glow.txt", encoding="utf-8").read().strip()
args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", "../base.mp4",
        "-framerate", "30", "-i", "D:/codebyabdullah_assets/tmp_masks/%04d.png"]
for p, *_ in S:
    args += ["-loop", "1", "-framerate", "30", "-t", f"{DUR}", "-i", p]
fc = [f"[0:v]format=yuv420p,{glow},format=yuv420p,split[bg][per]",
      "[1:v]format=gray,scale=1080:1920[m]", "[per][m]alphamerge[person]"]
prev = "bg"; k = 0
def add(layer, prev):
    global k
    for i, (p, s, e, l, fi, fo) in enumerate(S):
        if l != layer: continue
        idx = i + 2; fx = ""
        if fi: fx += f",fade=t=in:st={s}:d={F}:alpha=1"
        if fo: fx += f",fade=t=out:st={e-F:.2f}:d={F}:alpha=1"
        fc.append(f"[{idx}:v]format=rgba{fx}[s{idx}]")
        y = f"'40*max(0\,1-(t-{s})/0.2)'" if fi else "0"
        k += 1; out = f"L{k}"
        fc.append(f"[{prev}][s{idx}]overlay=x=0:y={y}:enable='between(t,{s},{e})'[{out}]")
        prev = out
    return prev
prev = add("B", prev)
fc.append(f"[{prev}][person]overlay=0:0[withp]")
prev = add("F", "withp")
fc.append(f"[{prev}]ass=captions_depth.ass:fontsdir=../fonts:shaping=complex,format=yuv420p[vout]")
open("filter_depth.txt", "w", encoding="utf-8").write(";\n".join(fc))
args += ["-filter_complex_script", "filter_depth.txt", "-map", "[vout]", "-t", f"{DUR}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "depth_video.mp4"]
subprocess.run(args, check=True); print("video ok")
