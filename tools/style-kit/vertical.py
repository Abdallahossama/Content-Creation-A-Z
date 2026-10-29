"""Vertical 1080x1920 version of a finished 16:9 episode, for Facebook Reels / TikTok / Instagram.
Layout (phone safe zones: TikTok/Reels UI sits in the top ~220 px, the bottom ~380 px and the right ~160 px):
  background : the same video, zoomed to fill 9:16, heavily blurred and darkened (never black bars)
  header     : small "ask habibi" logo + the episode question in big Impact (y 230-600)
  middle     : the full 16:9 picture at full width (nothing cropped), y 640-1248
  captions   : big Rubik Bold, 1-3 words at a time, keyword in yellow (y ~1330), kept off the right-hand buttons
  audio      : the episode's final mix
  python vertical.py <video> <audio> <captions.json|.srt> <out.mp4> "LINE 1|LINE 2|LINE 3" [--crop-bottom 0.2] [--ss 60 --t 20]"""
import sys, json, re, os, subprocess, argparse
from PIL import Image, ImageDraw, ImageFont

FONT = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"
LOGO = "D:/why habibi/_style_kit/brand/logo_horizontal.png"
W, H, VY, VH = 1080, 1920, 640, 608

def header_png(lines, path):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.resize((330, int(330 * lg.height / lg.width)), Image.LANCZOS)
    c.alpha_composite(lg, ((W - lg.width) // 2, 225))
    size = 96 if max(len(l) for l in lines) <= 16 else 84; f = ImageFont.truetype(IMPACT, size); y = 225 + lg.height + 18
    for l in lines:
        w = d.textlength(l, font=f); d.text(((W - w) / 2, y), l, font=f, fill=(255, 255, 255), stroke_width=9, stroke_fill=(0, 0, 0)); y += int(size * 1.08)
    assert y < VY + 10, f"header too tall ({y} px), shorten the lines"
    c.save(path)

def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h}:{m:02d}:{s:05.2f}"

def load_caps(path):
    if path.endswith(".json"): return json.load(open(path, encoding="utf-8"))
    caps = []; txt = open(path, encoding="utf-8-sig").read()
    for blk in re.split(r"\n\s*\n", txt.strip()):
        ls = blk.strip().splitlines()
        if len(ls) < 3: continue
        a, b = [x.strip().replace(",", ".") for x in ls[1].split("-->")]
        sec = lambda s: sum(float(p) * 60 ** i for i, p in enumerate(reversed(s.split(":"))))
        caps.append({"t0": sec(a), "t1": sec(b), "words": " ".join(ls[2:]).split(), "key": None})
    return caps

def ass(caps, path, ss=0.0, t=None):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, "
            "StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Cap,Rubik,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,8,90,170,1300,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    out = []
    for c in caps:
        a, b = c["t0"] - ss, c["t1"] - ss
        if b <= 0 or (t is not None and a >= t): continue
        a = max(a, 0.0); ws = list(c["words"]); k = c.get("key")
        if k is not None and 0 <= k < len(ws): ws[k] = "{\\c&H1AC2FF&}" + ws[k] + "{\\c&HFFFFFF&}"
        out.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{' '.join(ws)}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(out) + "\n")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("audio"); ap.add_argument("caps"); ap.add_argument("out")
    ap.add_argument("title"); ap.add_argument("--crop-bottom", type=float, default=0.0); ap.add_argument("--ss", type=float, default=0.0)
    ap.add_argument("--t", type=float, default=None); a = ap.parse_args()
    tmp = os.path.splitext(a.out)[0]; hdr, sub = tmp + "_header.png", tmp + "_caps.ass"
    header_png(a.title.split("|"), hdr); ass(load_caps(a.caps), sub, a.ss, a.t)
    keep = 1.0 - a.crop_bottom; vh = int(VH * keep) // 2 * 2; vy = VY + (VH - vh) // 2
    fc = (f"[0:v]split=2[a][b];"
          f"[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.36:saturation=0.75[bg];"
          f"[b]crop=iw:ih*{keep:.4f}:0:0,scale=1080:{vh}:flags=lanczos[fg];"
          f"[bg][fg]overlay=0:{vy}[v1];[v1][2:v]overlay=0:0[v2];"
          f"[v2]subtitles='{sub.replace(chr(92), '/').replace(':', chr(92) + ':')}':fontsdir='{os.path.dirname(FONT).replace(':', chr(92) + ':')}',fps=30[v]")
    cut = (["-ss", str(a.ss)] if a.ss else []) + (["-t", str(a.t)] if a.t else [])
    cmd = ["ffmpeg", "-v", "error", "-stats", "-y", *cut, "-i", a.video, *cut, "-i", a.audio, "-i", hdr, "-filter_complex", fc,
           "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", a.out]
    subprocess.run(cmd, check=True); print("wrote", a.out)

if __name__ == "__main__":
    main()

