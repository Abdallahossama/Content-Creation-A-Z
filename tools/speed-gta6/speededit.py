"""speededit: viral-style Short editor (look of the 53M-view Speed edits).
- layouts: "split" (facecam top 960 / gameplay bottom 960, captions on the seam) or "vertical" (9:16 crop of a camera clip)
- warm high-saturation grade, slow push-in, PUNCH-IN zoom + shake + colour flash on every scream peak
- captions: 1-3 word phrases snapped to the real audio onset (whisper is ~0.3 s late), Segoe UI Black, pop-in bounce,
  colour cycle green / white / mint / yellow with glow, hype words in italic
- hook card for the first ~2 s (white line + green line)
- original phonk bed (phonk.py), ducked under speech, drops at the first big peak; whoosh / bass hits on punches
- ending: freeze, zoom-blur, warm sepia, skull emoji pop + boom
  python speededit.py job.json"""
import sys, json, re, subprocess, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phonk

W, H, FPS, SR = 1080, 1920, 60, 48000
F = "C:/Windows/Fonts/"
FB, FBI, EMO = F + "seguibl.ttf", F + "seguibli.ttf", F + "seguiemj.ttf"
MX, MXB = "F:/speed-gta6/fonts/Montserrat-ExtraBold.ttf", "F:/speed-gta6/fonts/Montserrat-Black.ttf"
PAL = [(57, 255, 57), (255, 255, 255), (124, 255, 212), (255, 230, 0)]
HYPE = re.compile(r"^(OH|GOD|NO+|WHAT|YO+|BRO|LET'?S|GO+|W|YES+|DID|IT|WOW|CHAT|STOP|HELL|NAH|SIU+|I GOT)\W*$")
BAD = re.compile(r"\b(f+u+c*k+\w*|sh+i+t+\w*|bitch\w*|n+i+g+\w*|ass(hole)?|dick\w*|pussy|motherf\w*)\b", re.I)
SFX = {"whoosh": "D:/why habibi/_style_kit/sfx/whoosh_fast.wav", "hit": "D:/why habibi/_newchannel/sfx/hit_short_bass.mp3",
       "flash": "D:/why habibi/_newchannel/sfx/camera_old_shutter_click.mp3"}
_FT = {}
def font(p, s):
    k = (p, int(s))
    if k not in _FT: _FT[k] = ImageFont.truetype(p, int(s))
    return _FT[k]
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def clean(w): return BAD.sub(lambda m: m.group(0)[0] + "*" * (len(m.group(0)) - 1), w)

job = json.load(open(sys.argv[1], encoding="utf-8"))
src, out = job["src"], job["out"]; t0, t1 = job.get("t0", 0.0), job["t1"]; L = t1 - t0
TT = job.get("style") == "tt"          # TikTok clip style: facecam top 520 / game 1400, purple karaoke captions, no FX, no music
END = job.get("outro_len", 2.6); TOTAL = L + END; NF = int(TOTAL * FPS)
CAPSTYLE = job.get("caps", "frayzz" if TT else "pop")

# ---------------------------------------------------------------- audio analysis
def load_audio(path, a, b, sr=SR):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(a), "-to", str(b), "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
aud = load_audio(src, t0, t1); mono = aud.mean(1)
hop = SR // 100; nfr = len(mono) // hop
db = 20 * np.log10(np.sqrt((mono[: nfr * hop].reshape(nfr, hop) ** 2).mean(1)) + 1e-9)
sm = np.convolve(db, np.ones(5) / 5, "same"); base = np.median(sm)
hits = []; s2 = sm.copy(); thr = max(base + 5, np.percentile(sm, 88))
for _ in range(job.get("max_hits", 6)):
    i = int(np.argmax(s2))
    if s2[i] < thr: break
    hits.append(i / 100); s2[max(0, i - 130):i + 130] = -200
hits.sort()
if job.get("hits") is not None: hits = job["hits"]
if TT: hits = []

# ---------------------------------------------------------------- captions (snapped to onsets)
words = [dict(w) for w in json.load(open(job["words"], encoding="utf-8")) if t0 - 0.5 <= w["s"] < t1 and w.get("p", 1.0) >= 0.3]   # drop whisper inventions
for w in words:
    w["s"] -= t0; w["e"] -= t0; i = int(w["s"] * 100); lo = max(0, i - 60)
    seg = db[lo:i + 15]; pre = np.median(db[max(0, i - 90):max(1, i - 40)]) if i > 50 else (seg.min() if len(seg) else 0)
    k = np.argmax(seg > pre + 8) if len(seg) else 0
    w["s"] = (lo + k) / 100 if len(seg) and seg[k] > pre + 8 else w["s"] - 0.28
    w["s"] = max(0.0, w["s"] - 0.04); w["w"] = clean(w["w"].strip()).upper()
for a, b in zip(words, words[1:]):
    if b["w"].startswith("'"): a["w"] += b["w"]; b["w"] = ""
words = [w for w in words if w["w"]]
phr, cur = [], []
for j, w in enumerate(words):
    if cur and (len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.35): phr.append(cur); cur = []
    cur.append(w)
    if w["w"].endswith((".", "!", "?", ",")): phr.append(cur); cur = []
if cur: phr.append(cur)
CAPS = []
for k, p in enumerate(phr):
    s = p[0]["s"]; e = (phr[k + 1][0]["s"] if k + 1 < len(phr) else p[-1]["e"] + 0.4); e = min(e, p[-1]["e"] + 0.6)
    txt = " ".join(x["w"] for x in p).strip(" ,.-")
    hype = any(HYPE.match(x["w"]) for x in p) or txt.endswith("!")
    CAPS.append((s, max(e, s + 0.25), txt, PAL[k % len(PAL)], hype))

def text_img(txt, size, fill, italic=False, glow=True, stroke=7):
    f = font(FBI if italic else FB, size)
    while ImageDraw.Draw(Image.new("L", (1, 1))).textlength(txt, font=f) > W - 90 and f.size > 40: f = font(FBI if italic else FB, f.size - 4)
    l, t, r, b = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), txt, font=f, stroke_width=stroke)
    pad = 40; im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((pad - l, pad - t), txt, font=f, fill=fill + (230,), stroke_width=stroke + 6, stroke_fill=fill + (160,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(im).text((pad - l, pad - t + 5), txt, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    ImageDraw.Draw(im).text((pad - l, pad - t), txt, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return im
_TI = {}
def cap_img(c):
    if c not in _TI: _TI[c] = text_img(c[2], 118 if len(c[2]) < 12 else 96, c[3], italic=c[4])
    return _TI[c]

# ---------------------------------------------------------------- video
def frames(path, a, b):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(a), "-to", str(b), "-i", path, "-vf", f"fps={FPS},scale=1920:1080", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    n = 1920 * 1080 * 3; last = None
    while True:
        bb = p.stdout.read(n)
        if len(bb) < n: break
        last = Image.frombuffer("RGB", (1920, 1080), bb); yield last
    while True: yield last

def cover(im, box, size, zoom=1.0, cx=0.5, cy=0.5):
    x0, y0, x1, y1 = box; bw, bh = (x1 - x0) / zoom, (y1 - y0) / zoom; tw, th = size
    r = tw / th
    if bw / bh > r: bw = bh * r
    else: bh = bw / r
    mx, my = x0 + (x1 - x0) * cx, y0 + (y1 - y0) * cy
    l = min(max(mx - bw / 2, x0), x1 - bw); t = min(max(my - bh / 2, y0), y1 - bh)
    return im.resize(size, Image.BICUBIC, box=(l, t, l + bw, t + bh))

LUT = None
def grade(im, warm=1.0, sepia=0.0):
    global LUT
    im = ImageEnhance.Color(im).enhance(1.35); im = ImageEnhance.Contrast(im).enhance(1.12)
    a = np.asarray(im).astype(np.float32)
    a[..., 0] *= 1.0 + 0.05 * warm; a[..., 2] *= 1.0 - 0.06 * warm
    if sepia > 0:
        g = a.mean(2, keepdims=True); sep = np.concatenate([g * 1.25, g * 1.0, g * 0.7], 2); a = a * (1 - sepia) + sep * sepia
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def punch(t):
    z = 0.0; sh = (0, 0); fl = None
    for k, h in enumerate(hits):
        d = t - h
        if -0.05 <= d < 0.6:
            z = max(z, 0.16 * (ease(d / 0.07) if d < 0.07 else 1 - ease((d - 0.07) / 0.53)))
            if d < 0.22: amp = 14 * (1 - d / 0.22); sh = (math.sin(t * 90) * amp, math.cos(t * 77) * amp)
            if 0 <= d < 0.14: fl = (PAL[k % 3] if k % 3 != 1 else (255, 255, 255), 0.55 * (1 - d / 0.14))
    return z, sh, fl

SRCBOX = tuple(job.get("srcbox", (0, 0, 1920, 1080)))
TRACK = None
def build_track():
    """x of the moving subject over time (static camera): foreground vs median background, column centroid."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t0), "-to", str(t1), "-i", src, "-vf", "fps=6,scale=192:108,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 108, 192).astype(np.float32)
    y0, y1 = int(SRCBOX[1] / 10), int(SRCBOX[3] / 10); fr = fr[:, y0:y1]
    bg = np.median(fr, 0); xs = []; prev = job.get("cx", 0.5)
    for f in fr:
        m = (np.abs(f - bg) > 22).astype(np.float32); col = m.sum(0)
        if col.sum() > 0.02 * m.size: prev = float((col * np.arange(192)).sum() / col.sum() / 192)
        xs.append(prev)
    xs = np.array(xs); k = 9; xs = np.convolve(np.pad(xs, (k // 2, k // 2), mode="edge"), np.ones(k) / k, "valid")
    return np.arange(len(xs)) / 6, xs
def subject_x(t):
    global TRACK
    if not job.get("track"): return job.get("cx", 0.5)
    if TRACK is None: TRACK = build_track()
    return float(np.interp(t, *TRACK))

def compose(fr, t):
    z, (sx, sy), fl = punch(t); base_z = 1.0 + 0.06 * (t / L)
    if TT:
        fb = job["face"]; gb = job.get("game", (0, 0, 1920, 1080)); TH = job.get("top_h", 520)
        top = cover(fr, fb, (W, TH), job.get("face_zoom", 1.0), *job.get("face_c", (0.5, 0.45))).filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
        bot = cover(fr, gb, (W, H - TH), 1.0, *job.get("game_c", (0.5, 0.5)))
        if job.get("game_blur"): bot = ImageEnhance.Brightness(bot.filter(ImageFilter.GaussianBlur(22))).enhance(0.8)
        c = Image.new("RGB", (W, H)); c.paste(top, (0, 0)); c.paste(bot, (0, TH))
        c = ImageEnhance.Color(c).enhance(1.08)
        return c.convert("RGBA")
    if job["layout"] == "split":
        fb = job["face"]; gb = job.get("game", (0, 0, 1920, 1080))
        top = cover(fr, fb, (W, H // 2), (base_z + z) * job.get("face_zoom", 1.0), *job.get("face_c", (0.5, 0.45)))
        top = top.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
        bot = cover(fr, gb, (W, H // 2), base_z + z * 0.5, *job.get("game_c", (0.5, 0.5)))
        if job.get("game_blur"): bot = ImageEnhance.Brightness(bot.filter(ImageFilter.GaussianBlur(22))).enhance(0.8)
        c = Image.new("RGB", (W, H)); c.paste(top, (int(sx), int(sy))); c.paste(bot, (0, H // 2))
    else:
        c = cover(fr, SRCBOX, (W, H), base_z + z, subject_x(t), job.get("cy", 0.5))
        if sx or sy: c = c.transform(c.size, Image.AFFINE, (1, 0, -sx, 0, 1, -sy), Image.BICUBIC)
    c = grade(c)
    if fl:
        ov = Image.new("RGB", c.size, fl[0]); c = Image.blend(c, ov, fl[1])
    return c.convert("RGBA")

CAP_Y = H // 2 if job["layout"] == "split" else int(H * 0.62)
KF = font(F + "arialbd.ttf", 64)
def tt_caps(c, t):
    for k, p in enumerate(phr):
        s0 = p[0]["s"]; e0 = (phr[k + 1][0]["s"] if k + 1 < len(phr) else p[-1]["e"] + 0.4); e0 = min(e0, p[-1]["e"] + 0.6)
        if not (s0 <= t < e0): continue
        ws = [x["w"].strip(" ,.").capitalize() if j == 0 else x["w"].strip(" ,.").lower() for j, x in enumerate(p)]
        d = ImageDraw.Draw(c); sp = d.textlength(" ", font=KF); widths = [d.textlength(w, font=KF) for w in ws]
        x = W / 2 - (sum(widths) + sp * (len(ws) - 1)) / 2; y = job.get("top_h", 520) - 2
        cur = max([j for j, x2 in enumerate(p) if x2["s"] <= t] or [0])
        for j, (w, wd) in enumerate(zip(ws, widths)):
            if j == cur:
                d.rounded_rectangle((x - 8, y - 40, x + wd + 8, y + 36), radius=8, fill=(124, 58, 237, 255))
            d.text((x, y), w, font=KF, fill=(255, 255, 255), anchor="lm", stroke_width=6, stroke_fill=(0, 0, 0))
            x += wd + sp
        return

FZ_PAL = [(57, 255, 57), (255, 52, 52), (255, 214, 0), (0, 229, 255), (255, 80, 220)]
def spaced(d, x, y, txt, f, fill, track):
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    return x
def spaced_w(txt, f, track):
    d = ImageDraw.Draw(Image.new("L", (1, 1))); return sum(d.textlength(ch, font=f) + track for ch in txt) - track
FZ = []
cur = []
for w in words:
    if cur and (len(cur) >= 6 or w["s"] - cur[-1]["e"] > 0.45): FZ.append(cur); cur = []
    cur.append(w)
    if w["w"].endswith((".", "!", "?")): FZ.append(cur); cur = []
if cur: FZ.append(cur)
def fz_caps(c, t, y_mid):
    for k, p in enumerate(FZ):
        s0 = p[0]["s"]; e0 = (FZ[k + 1][0]["s"] if k + 1 < len(FZ) else p[-1]["e"] + 0.5); e0 = min(e0, p[-1]["e"] + 0.7)
        if not (s0 <= t < e0): continue
        ws = [x["w"].strip(",") for x in p]
        key = next((j for j, x in enumerate(ws) if HYPE.match(x)), max(range(len(ws)), key=lambda j: len(ws[j].strip("?!."))))
        col = FZ_PAL[k % len(FZ_PAL)]
        lines, ln = [], []
        for j, w in enumerate(ws):
            if ln and len(" ".join(ws[i] for i in ln + [j])) > 16: lines.append(ln); ln = []
            ln.append(j)
        if ln: lines.append(ln)
        f = font(MX, 66); tr = 5; lh = 84
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d, g = ImageDraw.Draw(lay), ImageDraw.Draw(glow)
        y = y_mid - lh * len(lines) / 2
        for ln in lines:
            full = " ".join(ws[j] for j in ln); x = W / 2 - spaced_w(full, f, tr) / 2
            for j in ln:
                if p[j]["s"] <= t:
                    fill = col if j == key else (255, 255, 255)
                    g.text((x, y + 4), ws[j], font=f, fill=(0, 0, 0, 200))
                    if j == key: g.text((x, y), ws[j], font=f, fill=col + (255,))
                    spaced(d, x, y, ws[j], f, fill + (255,), tr)
                x += spaced_w(ws[j] + " ", f, tr) + tr
            y += lh
        c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9))); c.alpha_composite(lay); return

def draw_text(c, t):
    if CAPSTYLE == "frayzz": return fz_caps(c, t, job.get("top_h", 520) if TT else int(H * job.get("cap_y", 0.55)))
    if TT: return tt_caps(c, t)
    hk = job.get("hook")
    if hk and t < 2.2:
        k = ease(t / 0.15); a = 1 - ease((t - 1.9) / 0.3)
        for j, (ln, col) in enumerate(zip(hk, [(255, 255, 255), (57, 255, 57)])):
            im = text_img(ln, 88, col, italic=(j == 1));
            if a < 1: im.putalpha(Image.eval(im.getchannel("A"), lambda v: int(v * a)))
            s = 0.7 + 0.3 * k; im2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
            y = (int(H * 0.30) if job["layout"] != "split" else int(H * 0.36)) + j * 110
            c.alpha_composite(im2, (W // 2 - im2.width // 2, y - im2.height // 2))
        if t < 1.6: return
    for cp in CAPS:
        s, e = cp[0], cp[1]
        if s <= t < e:
            d = t - s; sc = 0.65 + 0.43 * ease(d / 0.08) - 0.08 * ease((d - 0.08) / 0.06) if d < 0.14 else 1.0
            im = cap_img(cp); im2 = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
            c.alpha_composite(im2, (W // 2 - im2.width // 2, CAP_Y - im2.height // 2)); break

def zoom_blur(im, amt):
    acc = np.asarray(im).astype(np.float32); n = 6
    for i in range(1, n):
        s = 1 + amt * i / n; w, h = int(W * s), int(H * s)
        z = im.resize((w, h), Image.BILINEAR).crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))
        acc += np.asarray(z).astype(np.float32)
    return Image.fromarray((acc / n).astype(np.uint8))

def emoji_img(ch, size):
    f = font(EMO, size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t_, r, b = d.textbbox((0, 0), ch, font=f, embedded_color=True); pad = 30
    im = Image.new("RGBA", (r - l + 2 * pad, b - t_ + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t_), ch, font=f, embedded_color=True); return im
_OUT = {}
def outro_layers():
    if _OUT: return _OUT
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.45) / 0.6, 0, 1) ** 1.4
    vig = np.zeros((H, W, 4), np.uint8); vig[..., 0] = 235; vig[..., 1] = 60; vig[..., 2] = 20; vig[..., 3] = (a * 190).astype(np.uint8)
    _OUT["vig"] = Image.fromarray(vig, "RGBA")
    txt = job.get("outro", "*BRO REALLY DID THAT*").upper(); f = font(MXB, 66); tr = 4
    lines, ln = [], ""
    for w in txt.split():
        if ln and len(ln + " " + w) > 18: lines.append(ln); ln = w
        else: ln = (ln + " " + w).strip()
    lines.append(ln)
    lay = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); glow = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    for k, l2 in enumerate(lines):
        x = W / 2 - spaced_w(l2, f, tr) / 2; y = 20 + k * 82
        ImageDraw.Draw(glow).text((x, y), l2, font=f, fill=(255, 40, 20, 255))
        dl = ImageDraw.Draw(lay); xx = x
        for ch in l2:
            dl.text((xx, y), ch, font=f, fill=(255, 38, 38, 255), stroke_width=5, stroke_fill=(20, 0, 0, 255)); xx += dl.textlength(ch, font=f) + tr
    g = glow.filter(ImageFilter.GaussianBlur(16)); g.alpha_composite(lay); _OUT["txt"] = g; _OUT["nl"] = len(lines)
    _OUT["emo"] = emoji_img(job.get("emoji", "\U0001F602"), 150)
    return _OUT
def ring_pos():
    if job.get("ring") is not None: return job["ring"]
    if TT: return (W // 2, job.get("top_h", 520) // 2, 230)
    return None
def ending(last, u):
    o = outro_layers()
    if u < 0.35:
        c = zoom_blur(last.convert("RGB"), 0.25 * ease(u / 0.35))
    else:
        z = 1.0 + 0.04 * ease((u - 0.35) / (END - 0.35)); im = last.convert("RGB")
        c = im.resize((int(W * z), int(H * z)), Image.BICUBIC).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
        if u < 0.5: c = zoom_blur(c, 0.25 * (1 - ease((u - 0.35) / 0.15)))
    c = grade(c, warm=1.3).convert("RGBA")
    if u >= 0.35:
        k = ease((u - 0.35) / 0.25); v = o["vig"].copy(); v.putalpha(Image.eval(v.getchannel("A"), lambda a: int(a * k))); c.alpha_composite(v)
        rp = ring_pos()
        if rp and u > 0.4:
            x, y, r = rp; rr = r * (1.25 - 0.25 * ease((u - 0.4) / 0.2))
            gl = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((x - rr, y - rr, x + rr, y + rr), outline=(57, 255, 57, 255), width=22)
            c.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10))); ImageDraw.Draw(c).ellipse((x - rr, y - rr, x + rr, y + rr), outline=(70, 255, 70, 255), width=10)
        ty = int(H * job.get("outro_y", 0.36))
        if u > 0.45:
            a = ease((u - 0.45) / 0.15); tx = o["txt"].copy(); tx.putalpha(Image.eval(tx.getchannel("A"), lambda v2: int(v2 * a))); c.alpha_composite(tx, (0, ty - 40))
        if u > 0.6:
            d2 = u - 0.6; s = 0.4 + 0.75 * ease(d2 / 0.12) - 0.15 * ease((d2 - 0.12) / 0.1); e = o["emo"]
            e2 = e.resize((max(1, int(e.width * s)), max(1, int(e.height * s))), Image.BICUBIC)
            c.alpha_composite(e2, (W // 2 - e2.width // 2, ty + 20 + 82 * o["nl"]))
    return c

# ---------------------------------------------------------------- render video
tmpv = out.replace(".mp4", "_v.mp4")
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
gen = frames(src, t0, t1); last = None
for f in range(NF):
    t = f / FPS
    if t < L:
        c = compose(next(gen), t); last = c.copy(); draw_text(c, t)
    else:
        c = ending(last, t - L)
    enc.stdin.write(c.convert("RGB").tobytes())
enc.stdin.close(); enc.wait()

# ---------------------------------------------------------------- audio mix
N = int(TOTAL * SR); mix = np.zeros((N, 2), np.float32)
v = aud[: min(len(aud), N)]; rms = np.sqrt(np.mean(v ** 2)) + 1e-9; v = v / rms * 0.12; mix[: len(v)] += v
drop = hits[0] if hits and hits[0] < L * 0.6 else 0.0
m = phonk.beat(TOTAL + 1, job.get("bpm", 140), job.get("seed", 1))[: int(TOTAL * SR)]
env_s = np.interp(np.arange(len(m)) / SR, np.arange(nfr) / 100, np.clip((sm - (base - 3)) / 15, 0, 1), right=0.0)   # speech present -> duck
tt_ = np.arange(len(m)) / SR; lvl = np.where(tt_ < drop, 0.045, 0.085) * (1 - 0.55 * env_s); lvl = np.where(tt_ >= L, 0.11, lvl)
fo = int(0.6 * SR); m[-fo:] *= np.linspace(1, 0, fo)
if job.get("music", True): mix[: len(m)] += (m * lvl)[:, None]
def put(path, t, g):
    if not os.path.exists(path): return
    a = load_audio(path, 0, 3).mean(1); a = a / (np.abs(a).max() + 1e-9) * g; i = int(t * SR); n = min(len(a), N - i)
    if n > 0: mix[i:i + n] += a[:n, None]
for h in hits: put(SFX["whoosh"], max(0, h - 0.12), 0.25); put(SFX["hit"], h, 0.35)
bm = phonk.boom(); i = int((L + 0.35) * SR); n = min(len(bm), N - i); mix[i:i + n] += (bm[:n] * 0.45)[:, None]
mix = np.tanh(mix * 1.6) / 1.6
import soundfile as sf
tmpa = out.replace(".mp4", "_a.wav"); sf.write(tmpa, mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", tmpv, "-i", tmpa, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-af", "loudnorm=I=-12:TP=-1.0:LRA=9", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
os.remove(tmpv); os.remove(tmpa); print(out, "hits", [round(h, 2) for h in hits], "caps", len(CAPS))
