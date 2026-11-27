"""DEEP DIVE vertical series (owner 26 Nov 2026: copy the 'Shot and Forgot' Alcatraz reel look): black film-dust frame, real
archive photos as cards with slow push-ins, flash-to-white cuts, Courier typewriter labels ("REAL PHOTO"), episode title typed
over the corridor, clean word captions, free CC BY music (Kevin MacLeod) instead of the reel's Artlist tracks.
  uv run --no-project --with pillow --with numpy --with soundfile python dd_render.py <ep_dir> [qa t..|audio|video|all]
The episode folder holds shots.py (SHOTS list + META) and vo/ (dd_vo.wav, vo_words.json from transcribe_lines.py)."""
import sys, os, json, subprocess, math, random, importlib.util
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance

VW, VH, FPS = 1080, 1920, 30
F = "C:/Windows/Fonts/"
TYPE, COND, SER = F + "courbd.ttf", F + "FRAMDCN.TTF", F + "georgiai.ttf"
WHITE, BONE, RED, GREY, INK = (245, 243, 236), (236, 230, 214), (190, 30, 30), (160, 160, 160), (8, 8, 8)
SFX, MUS = "D:/why habibi/_newchannel/sfx/", "D:/why habibi/_music_library/"
_F = {}
def font(p, s):
    k = (p, int(s))
    if k not in _F: _F[k] = ImageFont.truetype(p, int(s))
    return _F[k]
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)

EP = sys.argv[1].rstrip("/") + "/"
spec = importlib.util.spec_from_file_location("shots", EP + "shots.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
VOJ = json.load(open(EP + "vo/vo_words.json", encoding="utf-8"))
LEAD = 0.35                                                      # silence before the first word
VODUR = sf.info(EP + "vo/dd_vo.wav").duration
LS = [l["start"] + LEAD for l in VOJ]                            # line starts on the video clock
LE = [(l["words"][-1]["e"] if l["words"] else l["start"] + 1) + LEAD for l in VOJ]
import difflib, re as _re
SCRIPT = [l.strip() for l in open(EP + "vo/vo_tts.txt", encoding="utf-8") if l.strip() and l.strip() != "##"]
def _n(x): return _re.sub(r"[^a-z0-9]", "", x.lower())
WORDS = []
for li, l in enumerate(VOJ):                       # captions: whisper timing, script spelling (1:1 word swaps only; numerals stay)
    hw = [w["w"].strip() for w in l["words"]]; sw = SCRIPT[li].split()
    txt = list(hw)
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(a=[_n(x) for x in hw], b=[_n(x) for x in sw]).get_opcodes():
        if op == "replace" and a1 - a0 == b1 - b0:
            for k in range(a1 - a0): txt[a0 + k] = sw[b0 + k]
    WORDS += [dict(w=t, s=w["s"] + LEAD, e=w["e"] + LEAD) for t, w in zip(txt, l["words"])]
_M = []
for w in WORDS:                                        # "9" ".30pm" -> "9:30 PM"
    if _M and w["w"].startswith("."): _M[-1]["w"] += w["w"].replace(".", ":", 1).replace("pm", " PM").replace("am", " AM"); _M[-1]["e"] = w["e"]
    else: _M.append(w)
WORDS = _M
TAIL = getattr(S, "TAIL", 2.2)
DUR = round(VODUR + LEAD + TAIL, 2)

# ---------------------------------------------------------------- shots -> absolute times
SH = []
for i, sh in enumerate(S.SHOTS):
    t0 = LS[sh["line"]] - 0.12 if sh["line"] > 0 else 0.0
    if "at" in sh: t0 = [w for w in WORDS if w["s"] >= LS[sh["line"]] - 0.05 and w["w"].lower().strip(",.?!") == sh["at"]][0]["s"] - 0.06
    SH.append(dict(sh, t0=t0))
for i in range(len(SH)): SH[i]["t1"] = SH[i + 1]["t0"] if i + 1 < len(SH) else DUR

# ---------------------------------------------------------------- images
_IM = {}
def load(path, crop=None, colour=False):
    k = (path, crop, colour)
    if k not in _IM:
        im = Image.open(path).convert("RGB")
        if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
        if not colour:
            g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=0.4); im = Image.merge("RGB", (g, g, g))
        else:
            im = ImageEnhance.Contrast(im).enhance(1.08)
        _IM[k] = im
    return _IM[k]

_VID = {}
def vframe(path, t, crop=None):
    """one frame of a (proxy) video at t seconds, cached per 1/30 s"""
    k = (path, round(t * FPS))
    if k not in _VID:
        if len(_VID) > 400: _VID.clear()
        out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        import io; im = Image.open(io.BytesIO(out)).convert("RGB")
        if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
        g = ImageOps.grayscale(im); _VID[k] = Image.merge("RGB", (g, g, g))
    return _VID[k]

def cover(im, w, h, z=1.0, cx=0.5, cy=0.5):
    s = max(w / im.width, h / im.height) * z; bw, bh = w / s, h / s
    x0 = min(max(cx * im.width - bw / 2, 0), im.width - bw); y0 = min(max(cy * im.height - bh / 2, 0), im.height - bh)
    return im.resize((w, h), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))

# ---------------------------------------------------------------- film dust frame (procedural, seeded per frame)
GRAIN = [Image.fromarray((np.random.default_rng(i).normal(0, 9, (VH // 2, VW // 2))).clip(-40, 40).astype(np.int16).astype(np.uint8)) for i in range(6)]
def dust(c, fi):
    rnd = random.Random(fi * 7919); d = ImageDraw.Draw(c)
    for _ in range(rnd.randint(4, 12)):                                       # specks
        x, y, r = rnd.randint(0, VW), rnd.randint(0, VH), rnd.choice((1, 1, 2, 2, 3))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(235, 235, 230) if rnd.random() < 0.8 else (10, 10, 10))
    for _ in range(rnd.randint(0, 2)):                                        # hairs
        x, y = rnd.randint(0, VW), rnd.randint(0, VH); pts = [(x, y)]
        for _ in range(4): x += rnd.randint(-9, 9); y += rnd.randint(3, 14); pts.append((x, y))
        d.line(pts, fill=(220, 220, 215), width=1)
    if rnd.random() < 0.25:                                                   # vertical scratch
        x = rnd.randint(40, VW - 40); d.line((x, 0, x + rnd.randint(-6, 6), VH), fill=(200, 200, 195), width=1)

def grain(c, fi):
    a = np.asarray(c.convert("RGB"), np.int16)
    n = np.asarray(GRAIN[fi % 6], np.uint8).astype(np.int8).astype(np.int16)
    n = np.repeat(np.repeat(n, 2, 0), 2, 1)[..., None]
    return Image.fromarray((a + n).clip(0, 255).astype(np.uint8))

# ---------------------------------------------------------------- text
def typed(c, s, t, t0, x, y, size=58, fill=WHITE, cps=24, anchor="mm", shadow=True):
    if t < t0 or not s: return
    n = min(len(s), int((t - t0) * cps) + 1); d = ImageDraw.Draw(c); f = font(TYPE, size)
    if shadow: d.text((x + 3, y + 3), s[:n], font=f, fill=(0, 0, 0), anchor=anchor)
    d.text((x, y), s[:n], font=f, fill=fill, anchor=anchor)

def caption(c, t):
    ws = [w for w in WORDS if w["s"] - 0.02 <= t]
    if not ws: return
    # chunk words in 3s (break at punctuation), show the chunk the current word belongs to
    chunks, cur = [], []
    for w in WORDS:
        cur.append(w)
        if len(cur) == 3 or w["w"].endswith((",", ".", "?", "!")): chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for ch in chunks:
        if ch[0]["s"] - 0.02 <= t < ch[-1]["e"] + 0.18:
            d = ImageDraw.Draw(c); f = font(COND, 84); x0 = VW / 2
            words = [w["w"].strip(",.") for w in ch]; full = " ".join(words)
            wid = d.textlength(full, font=f); x = x0 - wid / 2
            for w, s in zip(ch, words):
                col = (255, 214, 64) if w["s"] - 0.02 <= t < w["e"] + 0.05 else WHITE
                d.text((x, S.CAP_Y), s, font=f, fill=col, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
                x += d.textlength(s + " ", font=f)
            return

# ---------------------------------------------------------------- one frame
CARD_W = 980
def card(c, im, t, sh):
    u = (t - sh["t0"]) / max(sh["t1"] - sh["t0"], 0.1); z = sh.get("z0", 1.0) + (sh.get("z1", 1.08) - sh.get("z0", 1.0)) * u
    cx = sh.get("cx", 0.5); cy = sh.get("cy", 0.5)
    if sh.get("full"):
        c.paste(cover(im, VW, VH, z, cx, cy), (0, 0)); return VH * 0.12, VH * 0.88
    w = sh.get("w", CARD_W); ar = sh.get("ar", im.width / im.height); h = int(w / ar)
    h = min(h, 1250); w = int(h * ar) if h == 1250 else w
    y = int(sh.get("y", 860) - h / 2)
    c.paste(cover(im, w, h, z, cx, cy), (int((VW - w) / 2), y)); return y, y + h

def render(t, fi):
    c = Image.new("RGB", (VW, VH), INK)
    sh = [s for s in SH if s["t0"] <= t][-1] if t >= SH[0]["t0"] else SH[0]
    kind = sh.get("kind", "photo")
    if kind == "photo" or kind == "pair":
        if kind == "pair":
            for k, (p, lab) in enumerate(sh["imgs"]):
                im = load(S.M + p, sh.get("crop"), sh.get("colour", False)); w = 500; h = int(w * 1.28)
                c.paste(cover(im, w, h, 1.0 + 0.05 * (t - sh["t0"]) / max(sh["t1"] - sh["t0"], .1), 0.5, 0.4), (27 + k * 526, 860 - h // 2))
                typed(c, lab, t, sh["t0"] + 0.15 + 0.5 * k, 27 + k * 526 + w / 2, 860 + h // 2 + 50, size=40)
            top, bot = 860 - 320, 860 + 320
        elif "vid" in sh:
            im = vframe(S.M + sh["vid"], sh.get("vt", 0) + (t - sh["t0"]), sh.get("crop")); top, bot = card(c, im, t, sh)
        else:
            im = load(S.M + sh["img"], sh.get("crop"), sh.get("colour", False)); top, bot = card(c, im, t, sh)
        if sh.get("label"): typed(c, sh["label"], t, sh["t0"] + 0.1, VW / 2, (top - 70) if not sh.get("full") else 300, size=sh.get("lsize", 56))
        if sh.get("label2"): typed(c, sh["label2"], t, sh["t0"] + 0.6, VW / 2, bot + 60 if not sh.get("full") else 380, size=40, fill=BONE)
        if sh.get("ring"):
            u = ease((t - sh["t0"] - sh.get("ring_at", 0.5)) / 0.5)
            if u > 0:
                x0, y0, x1, y1 = sh["ring"]; cx_, cy_, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
                n = int(80 * u) + 2; pts = [(cx_ + rx * math.cos(-2.2 + 2 * math.pi * 1.08 * i / 80), cy_ + ry * math.sin(-2.2 + 2 * math.pi * 1.08 * i / 80)) for i in range(n)]
                ImageDraw.Draw(c).line(pts, fill=RED, width=9, joint="curve")
    elif kind == "title":                                                 # episode card over a dark photo
        im = load(S.M + sh["img"], sh.get("crop")); u = (t - sh["t0"]) / max(sh["t1"] - sh["t0"], .1)
        bg = cover(im, VW, VH, 1.05 + 0.08 * u, sh.get("cx", 0.5), 0.5); c.paste(ImageEnhance.Brightness(bg).enhance(0.45), (0, 0))
        for k, ln in enumerate(sh["lines"]): typed(c, ln, t, sh["t0"] + 0.25 + 0.55 * k, VW / 2, 820 + k * 92, size=78 if k < len(sh["lines"]) - 1 else 60, cps=20)
    elif kind == "hour":                                                  # black card, big typed time + sub
        typed(c, sh["big"], t, sh["t0"] + 0.1, VW / 2, 820, size=190, cps=12, shadow=False)
        typed(c, sh.get("sub", ""), t, sh["t0"] + 0.1 + len(sh["big"]) / 12 + 0.1, VW / 2, 990, size=50, fill=GREY, cps=30, shadow=False)
    elif kind == "end":
        im = load(sh["img"], None, True); w = 960; h = int(w * 9 / 16)
        c.paste(cover(im, w, h), (60, 760 - h // 2))
        typed(c, sh.get("label", ""), t, sh["t0"] + 0.1, VW / 2, 760 - h // 2 - 70, size=56)
        for k, ln in enumerate(sh.get("lines", [])):
            typed(c, ln, t, sh["t0"] + 0.6 + 0.4 * k, VW / 2, 760 + h // 2 + 70 + k * 64, size=44, fill=BONE, cps=40)
    # flash-to-white on the cut (first 4 frames), as in the reference
    if sh.get("flash", True) and sh is not SH[0]:
        a = 1 - (t - sh["t0"]) / 0.16
        if a > 0: c = Image.blend(c, Image.new("RGB", c.size, (255, 255, 255)), min(1.0, a) * 0.92)
    dust(c, fi); caption(c, t)
    ImageDraw.Draw(c).text((VW / 2, 1840), "THE LAST HOURS", font=font(TYPE, 30), fill=(120, 120, 118), anchor="mm")
    return grain(c, fi)

# ---------------------------------------------------------------- audio
def rd(p, sr=48000):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True).stdout
    return np.frombuffer(out, np.float32).copy()
def db(x): return 10 ** (x / 20)
def audio():
    sr = 48000; n = int(DUR * sr); mix = np.zeros(n, np.float32)
    vo = rd(EP + "vo/dd_vo.wav"); a = int(LEAD * sr); mix[a:a + len(vo)] += vo[: n - a]
    def put(p, t, gain, fade=0.0):
        x = rd(p) * db(gain); i = int(t * sr); x = x[: max(0, n - i)]
        if fade and len(x): f = min(len(x), int(fade * sr)); x[-f:] *= np.linspace(1, 0, f)
        mix[i:i + len(x)] += x
    for m in S.MUSIC:                                                    # (file, t0, t1, gain, offset)
        x = rd(MUS + m[0])[int(m[4] * sr):] * db(m[3]); L = int((min(m[2], DUR) - m[1]) * sr)
        while len(x) < L: x = np.concatenate([x, x])
        x = x[:L].copy(); f = int(1.5 * sr); x[:int(0.4 * sr)] *= np.linspace(0, 1, int(0.4 * sr)); x[-f:] *= np.linspace(1, 0, f)
        i = int(m[1] * sr); mix[i:i + len(x)] += x[: n - i]
    for sh in SH:                                                         # cut sounds
        if sh is SH[0]: continue
        if sh.get("flash", True): put(SFX + "camera_old_shutter_click.mp3", sh["t0"] - 0.02, -20)
        if sh.get("label") or sh.get("kind") in ("hour", "title"): put(SFX + "typewriter_typing_old.mp3", sh["t0"] + 0.1, -27, fade=0.25) if False else None
    for (line, word, f, g) in S.SFX_EV:
        t = LS[line] if word is None else [w for w in WORDS if w["s"] >= LS[line] - 0.05 and w["w"].lower().strip(",.?!") == word][0]["s"]
        put(SFX + f + ".mp3", t, g)
    for sh in SH:                                                         # short typewriter burst under every typed label
        lab = sh.get("label") or (sh.get("big") if sh.get("kind") == "hour" else None) or (sh.get("lines", [None])[0] if sh.get("kind") == "title" else None)
        if lab:
            x = rd(SFX + "typewriter_typing_old.mp3")[: int(min(1.2, len(lab) / 24 + 0.1) * sr)] * db(-26)
            f = int(0.1 * sr); x[-f:] *= np.linspace(1, 0, f); i = int((sh["t0"] + 0.1) * sr); mix[i:i + len(x)] += x[: n - i]
    # loudness: -14 LUFS-ish via RMS of voiced parts, then peak guard
    vo_rms = np.sqrt(np.mean(vo[np.abs(vo) > 0.02] ** 2)); mix *= db(-16.5) / max(vo_rms, 1e-6)
    pk = np.max(np.abs(mix)); mix *= min(1.0, 0.89 / pk)
    sf.write(EP + "build/mix.wav", np.stack([mix, mix], 1), sr, subtype="PCM_16"); print("audio", round(DUR, 2), "s")

def video():
    out = EP + "export/" + S.NAME
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-",
                          "-i", EP + "build/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    N = int(DUR * FPS)
    for fi in range(N):
        p.stdin.write(render(fi / FPS, fi).tobytes())
        if fi % 300 == 0: print(f"{fi}/{N}", flush=True)
    p.stdin.close(); p.wait(); print("WROTE", out)

if __name__ == "__main__":
    cmd = sys.argv[2] if len(sys.argv) > 2 else "all"
    print("DUR", DUR, "shots", len(SH))
    if cmd == "qa":
        ts = [float(x) for x in sys.argv[3:]] or [s["t0"] + 0.6 for s in SH]
        tiles = [render(t, int(t * FPS)).resize((270, 480)) for t in ts]
        cols = 8; G = Image.new("RGB", (cols * 274, ((len(tiles) + cols - 1) // cols) * 484), (40, 40, 40))
        for i, im in enumerate(tiles): G.paste(im, ((i % cols) * 274, (i // cols) * 484))
        G.save(EP + "build/qa.jpg", quality=85); print(EP + "build/qa.jpg")
    if cmd in ("audio", "all"): audio()
    if cmd in ("video", "all"): video()
