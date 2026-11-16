"""billvid: The Bill, Explained - 16:9 explainer engine (1920x1080, 30 fps). Colour photos, paper receipts, charts, paper maps.
A video folder has: vo_lines.txt (## = chapter pause), vo/vo.wav (Chatterbox, exact-zero gaps between lines), vo/vo_words.json
(whisper), media/<ID>_*.jpg, and spec.py that defines SHOTS, OV, CH, MUSIC, EV, NAME, CAPFIX and calls billvid.run(globals()).
Shot keys: int line  or  (line, "word")  (snapped to whisper word times).
Modes: times | keys | qa | seg i n | audio | final n | all n | chapters
"""
import os, sys, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance, ImageFont

W, H, FPS = (1080, 1080, 30) if os.environ.get("BV_SQUARE") else (1920, 1080, 30)
VW, VH = 1080, 1920
F = "C:/Windows/Fonts/"
WORD, NUMF, MONO, MONOB, SANSB = F + "ariblk.ttf", F + "impact.ttf", F + "consola.ttf", F + "consolab.ttf", F + "arialbd.ttf"
INK, PAPER, RED, YELLOW, GREY = (18, 18, 18), (244, 240, 231), (214, 40, 32), (255, 212, 0), (128, 122, 112)
BLUE, SEA, LAND = (36, 84, 140), (214, 223, 228), (236, 230, 214)
SFX1 = "D:/why habibi/_style_kit/sfx/"; SFX2 = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
_FT = {}
def font(p, s):
    k = (p, int(s))
    if k not in _FT: _FT[k] = ImageFont.truetype(p, int(s))
    return _FT[k]
def fitf(d, s, p, size, maxw):
    f = font(p, size)
    while d.textlength(s, font=f) > maxw and f.size > 20: f = font(p, f.size - 2)
    return f
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def cl(x): return min(max(x, 0.0), 1.0)

G = {}          # the spec's globals (set by run)

# ------------------------------------------------------------------ timing
def setup(spec):
    G.update(spec); R = spec["ROOT"]
    raw = [l.strip() for l in open(R + "vo_lines.txt", encoding="utf-8") if l.strip()]
    G["LINES"] = [l for l in raw if l != "##"]
    vo, sr = sf.read(R + spec.get("VOF", "vo/vo.wav"), dtype="float32")
    if vo.ndim > 1: vo = vo.mean(1)
    z = np.concatenate([[False], vo == 0.0, [False]]).astype(np.int8); d = np.diff(z)
    gaps = [(a, b) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]) if b - a >= int(0.3 * sr)]
    n = len(G["LINES"]); gaps = gaps[:n]
    lead = spec.get("LEAD", 0.6)
    G["T"] = [lead + (0 if i == 0 else gaps[i - 1][1]) / sr for i in range(n)]
    G["LE"] = [lead + g[0] / sr for g in gaps]
    G["VO_END"] = lead + len(vo) / sr; G["DUR"] = G["VO_END"] + spec.get("TAIL", 12.0); G["NF"] = int(G["DUR"] * FPS)
    G["LEAD"] = lead; G["VOSR"] = sr
    G["WORDS"] = {}
    wp = R + "vo/vo_words.json"
    if os.path.exists(wp):
        for row in json.load(open(wp, encoding="utf-8")):
            i = row["line"]; end = G["LE"][i] - lead if i < len(G["LE"]) else 1e9     # whisper hallucinations: zero-length / past the line's audio
            G["WORDS"][i] = [dict(w, s=w["s"] + lead, e=w["e"] + lead) for w in row["words"] if w["e"] - w["s"] >= 0.02 and w["s"] < end - 0.05 and not (w["p"] < 0.05 and w["e"] - w["s"] < 0.1)]
    G["SHOT_T"] = [KT(s[0]) for s in spec["SHOTS"]]; G["SHOT_T"][0] = 0.0
    G["OVT"] = [AT(k) for k, _, _ in spec.get("OV", [])]

def nrm(s): return re.sub(r"[^a-z0-9$%.]", "", s.lower())
def wt(line, word):
    for w in G["WORDS"].get(line, []):
        if nrm(w["w"]).startswith(nrm(word)): return w["s"]
    return None
def AT(key):
    if isinstance(key, (int, np.integer)): return G["T"][key]
    ln, w = key
    if isinstance(w, (int, float)): return G["T"][ln] + w
    for alt in w.split("|"):
        v = wt(ln, alt)
        if v is not None: return v
    return G["T"][ln] + 0.3
def KT(key): return AT(key) - 0.1

# ------------------------------------------------------------------ images
_IM = {}
def media(rid):
    M = G.get("MEDIA", G["ROOT"] + "media/"); fs = sorted(glob.glob(M + rid + "_*")) + sorted(glob.glob(M + rid + ".*"))
    if not fs: raise FileNotFoundError(rid)
    return fs[0]
def photo(rid, crop=None):
    k = (rid, crop)
    if k not in _IM:
        f = media(rid)
        if f.lower().endswith((".mp4", ".mov", ".webm", ".mkv")):                 # a video used as a still (blurred backgrounds, thumbnails)
            import billclip as BC, io; _, _, ln = BC.probe(f)
            png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ln / 2:.2f}", "-i", f, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            im = Image.open(io.BytesIO(png)).convert("RGB")
        else:
            im = Image.open(f).convert("RGB")
        if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
        if max(im.size) > 2600: im.thumbnail((2600, 2600), Image.LANCZOS)
        if len(_IM) > 8: _IM.pop(next(iter(_IM)))                             # small cache: 4 render processes must fit in RAM
        im = ImageEnhance.Contrast(im).enhance(1.08); im = ImageEnhance.Color(im).enhance(1.06)
        _IM[k] = im
    return _IM[k]
def kenburns(src, u, z0, z1, c0, c1):
    z = z0 + (z1 - z0) * u; cx = c0[0] + (c1[0] - c0[0]) * u; cy = c0[1] + (c1[1] - c0[1]) * u
    s = max(W / src.width, H / src.height) * z; w, h = W / s, H / s
    w, h = min(w, src.width), min(h, src.height)
    x0 = max(0.0, min(max(cx * src.width - w / 2, 0), src.width - w)); y0 = max(0.0, min(max(cy * src.height - h / 2, 0), src.height - h))
    return src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert("RGBA")
_BL = {}
def blurbg(rid, crop=None, dark=0.55):
    k = (rid, crop, dark)
    if k not in _BL:
        im = kenburns(photo(rid, crop), 0, 1.0, 1.0, (.5, .5), (.5, .5)).convert("RGB").filter(ImageFilter.GaussianBlur(30))
        if len(_BL) > 6: _BL.pop(next(iter(_BL)))
        _BL[k] = Image.blend(im, Image.new("RGB", (W, H), INK), dark).convert("RGBA")
    return _BL[k].copy()
_PN = {}
def paper(w=W, h=H, seed=3):
    k = (w, h)
    if k not in _PN:
        n = Image.effect_noise((w, h), 40).convert("L").point(lambda v: 128 + (v - 128) // 8)
        base = Image.new("RGB", (w, h), PAPER); from PIL import ImageChops
        _PN[k] = ImageChops.add(base, Image.merge("RGB", [n] * 3), 1, -128).convert("RGBA")
    return _PN[k].copy()

def shadowed(c, spr, x, y, blur=16, alpha=120, off=(8, 12)):
    a = spr.split()[3].point(lambda v: v * alpha // 255)
    sh = Image.new("RGBA", (spr.width + 80, spr.height + 80), (0, 0, 0, 0))
    blk = Image.new("RGBA", spr.size, (0, 0, 0, 255)); blk.putalpha(a); sh.paste(blk, (40 + off[0], 40 + off[1]), blk)
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (int(x - 40), int(y - 40))); c.alpha_composite(spr, (int(x), int(y)))

def zig_mask(w, h, tooth=20, depth=12, top=True, bottom=True):
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m); pts = []
    if top: pts += [(min(x, w), depth if (x // tooth) % 2 == 0 else 0) for x in range(0, w + tooth, tooth)]
    else: pts += [(0, 0), (w, 0)]
    if bottom: pts += [(max(x, 0), h - (depth if i % 2 else 0)) for i, x in enumerate(range(w, -tooth, -tooth))]
    else: pts += [(w, h), (0, h)]
    d.polygon(pts, fill=255); return m

def hl(d, box, col=YELLOW, u=1.0):
    x0, y0, x1, y1 = box; x1 = x0 + (x1 - x0) * u
    if u <= 0: return
    d.polygon([(x0 - 6, y0 + 4), (x1 + 4, y0), (x1 + 8, y1 - 2), (x0 - 2, y1 + 3)], fill=col)

def dots_row(d, x0, x1, y, left, right, f, fill=INK, dotc=GREY):
    d.text((x0, y), left, font=f, fill=fill); rw = d.textlength(right, font=f); d.text((x1 - rw, y), right, font=f, fill=fill)
    lx = x0 + d.textlength(left, font=f) + 12; dw = d.textlength(".", font=f)
    n = max(0, int((x1 - rw - 12 - lx) / dw)); d.text((lx, y), "." * n, font=f, fill=dotc)

def price_tag(text, h=150, col=RED):
    f = font(NUMF, int(h * 0.72)); tw = ImageDraw.Draw(Image.new("RGB", (4, 4))).textlength(text, font=f)
    p = int(h * 0.42); w = int(tw + p + h * 0.45); tag = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(tag)
    d.polygon([(0, h // 2), (p, 0), (w, 0), (w, h), (p, h)], fill=col); r = int(h * 0.09)
    d.ellipse((p * 0.55 - r, h / 2 - r, p * 0.55 + r, h / 2 + r), fill=(0, 0, 0, 0))
    bb = d.textbbox((0, 0), text, font=f)
    d.text((p + (w - p - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=(255, 255, 255))
    return tag

def credit(c, s):
    if not s: return
    d = ImageDraw.Draw(c); f = font(MONO, 22); w = d.textlength(s, font=f)
    d.rectangle((W - w - 40, H - 46, W - 16, H - 14), fill=(0, 0, 0, 150)); d.text((W - w - 28, H - 42), s, font=f, fill=(230, 226, 216))

def source(c, s, dark=False):
    if s: ImageDraw.Draw(c).text((80, H - 70), "Source: " + s, font=font(MONO, 26), fill=(200, 196, 186) if dark else GREY)

def pop(c, spr, cx, cy, t, t0, dur=0.22):
    if t < t0: return
    u = ease((t - t0) / dur); k = 0.7 + 0.3 * u
    s = spr.resize((max(1, int(spr.width * k)), max(1, int(spr.height * k))), Image.BICUBIC)
    if u < 1: s.putalpha(s.split()[3].point(lambda v: int(v * u)))
    shadowed(c, s, cx - s.width / 2, cy - s.height / 2, blur=12, alpha=130)

# ------------------------------------------------------------------ shot kinds
def KB(rid, crop=None, z=(1.03, 1.12), c0=(.5, .5), c1=None, credit=None, tags=(), dim=0.0):
    return ("kb", dict(rid=rid, crop=crop, z=z, c0=c0, c1=c1 or c0, credit=credit, tags=tags, dim=dim))
def VID(rid, at=0.0, speed=1.0, crop=None, z=(1.0, 1.06), c=(.5, .5), credit=None, tags=(), dim=0.0):
    """stock video clip: rid = media file id (e.g. "VA1"), at = seconds into the source, speed < 1 = slow motion"""
    return ("vid", dict(rid=rid, at=at, speed=speed, crop=crop, z=z, c=c, credit=credit, tags=tags, dim=dim))
def RECEIPT(title, rows, total=None, bg=None, sub=None, src=None):
    """rows: [(key, left, right)], total: (key, left, right) highlighted"""
    return ("receipt", dict(title=title, rows=rows, total=total, bg=bg, sub=sub, src=src))
def BARS(title, bars, src=None, fmt="${:,.2f}", unit="", maxv=None):
    """bars: [(key, label, value, color)]"""
    return ("bars", dict(title=title, bars=bars, src=src, fmt=fmt, unit=unit, maxv=maxv))
def LINE(title, xs, series, src=None, ymin=0, ymax=None, fmt="${:.2f}", gap=None, marks=()):
    """series: [(name, [y...], color)]; draws left->right over the shot; gap=(i,j) shades between series i and j; marks: [(x_index, label)]"""
    return ("line", dict(title=title, xs=xs, series=series, src=src, ymin=ymin, ymax=ymax, fmt=fmt, gap=gap, marks=marks))
def BIG(num, sub, count=None, fmt=None, col=INK, bg=None, hl_sub=True):
    return ("big", dict(num=num, sub=sub, count=count, fmt=fmt, col=col, bg=bg, hl_sub=hl_sub))
def CHAPTER(item, title, bg=None):
    return ("chapter", dict(item=item, title=title, bg=bg))
def MAP(view, ops=(), z=(1.0, 1.06), title=None, src=None):
    """view=(lon_c, lat_c, deg_w); ops: ("pin", lon, lat, label, key) ("country", name, key) ("route", [(lon,lat)...], key, dur) ("x", lon, lat, key)"""
    return ("map", dict(view=view, ops=list(ops), z=z, title=title, src=src))
def END(): return ("end", {})

def tags_on(c, tags, t):
    for key, text, x, y in tags:
        pop(c, price_tag(text), x, y, t, AT(key))

def kb_frame(a, t, t0, t1):
    u = cl((t - t0) / max(t1 - t0, 1e-6))
    c = kenburns(photo(a["rid"], a["crop"]), u, a["z"][0], a["z"][1], a["c0"], a["c1"])
    if a["dim"]: c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * a["dim"]))))
    tags_on(c, a["tags"], t); credit(c, a["credit"]); return c

CLIPS = {}
def clip_for(a, t0, t1):
    import billclip as BC
    k = (a["rid"], a["at"], round(t0, 3))
    if k not in CLIPS:
        for k2 in list(CLIPS): CLIPS.pop(k2).close()                    # one reader at a time inside a segment
        f = media(a["rid"]); need = max(t1 - t0, 0.5); _, _, ln = BC.probe(f)
        avail = max(ln - a["at"] - 0.1, 0.5); sp = min(a["speed"], max(0.4, avail / need))   # stretch a short clip, never below 0.4x
        CLIPS[k] = BC.Clip(f, out=(W, H), src_in=a["at"], speed=sp, crop=a["crop"], z0=a["z"][0], z1=a["z"][1], c=a["c"], dur=need)
    return CLIPS[k]
def vid_frame(a, t, t0, t1):
    c = clip_for(a, t0, t1).at(t - t0)
    if a["dim"]: c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * a["dim"]))))
    tags_on(c, a["tags"], t); credit(c, a["credit"]); return c

def receipt_frame(a, t, t0, t1):
    c = blurbg(*a["bg"]) if a["bg"] else Image.new("RGBA", (W, H), INK + (255,))
    rows = a["rows"] + ([a["total"]] if a["total"] else [])
    rw, pad, lh = min(1000, W - 60), 60, 74
    rh = 190 + len(rows) * lh + (40 if a["total"] else 0) + 70
    u = ease((t - t0) / 0.35)
    r = paper(rw, rh); r.putalpha(zig_mask(rw, rh, 22, 13)); d = ImageDraw.Draw(r)
    ft = font(WORD, 58); tw = d.textlength(a["title"], font=ft); d.text(((rw - tw) / 2, 50), a["title"], font=ft, fill=INK)
    if a["sub"]:
        fs = font(MONO, 30); sw = d.textlength(a["sub"], font=fs); d.text(((rw - sw) / 2, 128), a["sub"], font=fs, fill=GREY)
    y = 190; fr = font(MONO, 44); fb = font(MONOB, 50)
    for i, (key, left, right) in enumerate(a["rows"]):
        if t >= AT(key): dots_row(d, pad, rw - pad, y, left, right, fr)
        y += lh
    if a["total"]:
        key, left, right = a["total"]; d.line([(pad, y + 8), (rw - pad, y + 8)], fill=INK, width=4); y += 34
        if t >= AT(key):
            hl(d, (pad - 8, y + 2, rw - pad + 8, y + 62), u=ease((t - AT(key)) / 0.4)); dots_row(d, pad, rw - pad, y + 4, left, right, fb, dotc=INK)
    x = (W - rw) / 2; yy = (H - rh) / 2 + 60 * (1 - u) - 10
    shadowed(c, r, x, yy, blur=20, alpha=150); source(c, a["src"], dark=True); return c

def bars_frame(a, t, t0, t1):
    c = paper(); d = ImageDraw.Draw(c)
    d.text((70 if W < 1500 else 110, 90), a["title"], font=fitf(d, a["title"], WORD, 64, W - 160), fill=INK)
    bars = a["bars"]; mx = a["maxv"] or max(b[2] for b in bars) * 1.12
    x0, x1 = int(W * 0.27), W - int(W * 0.135); y = 250; bh = min(120, int((H - 380) / max(len(bars), 1)) - 30)
    for key, label, val, col in bars:
        tk = AT(key)
        d.text((70 if W < 1500 else 110, y + bh / 2), label, font=font(SANSB, 46 if W > 1500 else 40), fill=INK, anchor="lm")
        if t >= tk:
            u = ease((t - tk) / 0.7); v = val * u; xe = x0 + (x1 - x0) * v / mx
            d.rectangle((x0, y, xe, y + bh), fill=col)
            d.text((xe + 20, y + bh / 2), a["fmt"].format(v) + a["unit"], font=font(NUMF, int(bh * 0.7)), fill=col, anchor="lm")
        y += bh + 34
    source(c, a["src"]); return c

def line_frame(a, t, t0, t1):
    c = paper(); d = ImageDraw.Draw(c)
    d.text((70 if W < 1500 else 110, 80), a["title"], font=fitf(d, a["title"], WORD, 60, W - 160), fill=INK)
    X0, X1, Y0, Y1 = 170, W - (330 if W > 1500 else 250), H - 170, 230
    xs = a["xs"]; n = len(xs); allv = [v for _, ys, _ in a["series"] for v in ys if v is not None]
    ymin = a["ymin"]; ymax = a["ymax"] or max(allv) * 1.1
    def P(i, v): return (X0 + (X1 - X0) * i / (n - 1), Y0 - (Y0 - Y1) * (v - ymin) / (ymax - ymin))
    for k in range(5):
        v = ymin + (ymax - ymin) * k / 4; yy = P(0, v)[1]
        d.line([(X0, yy), (X1, yy)], fill=(214, 208, 196), width=2); d.text((X0 - 20, yy), a["fmt"].format(v), font=font(MONO, 28), fill=GREY, anchor="rm")
    step = max(1, n // 8)
    for i in range(0, n, step): d.text((P(i, ymin)[0], Y0 + 30), str(xs[i]), font=font(MONO, 28), fill=GREY, anchor="mm")
    u = ease(cl((t - t0 - 0.3) / max(min(t1 - t0 - 1.0, 6.0), 1.0))); upto = u * (n - 1)
    def pts(ys):
        out = []
        for i, v in enumerate(ys):
            if v is None: continue
            if i <= upto: out.append(P(i, v))
            elif i - 1 <= upto and i >= 1 and ys[i - 1] is not None:
                f = upto - (i - 1); p0, p1 = P(i - 1, ys[i - 1]), P(i, v); out.append((p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f))
        return out
    if a["gap"]:
        i, j = a["gap"]; pa, pb = pts(a["series"][i][1]), pts(a["series"][j][1])
        m = min(len(pa), len(pb))
        if m > 1:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(pa[:m] + pb[:m][::-1], fill=YELLOW + (110,)); c.alpha_composite(lay); d = ImageDraw.Draw(c)
    for name, ys, col in a["series"]:
        p = pts(ys)
        if len(p) > 1: d.line(p, fill=col, width=8, joint="curve")
        if p:
            d.ellipse((p[-1][0] - 9, p[-1][1] - 9, p[-1][0] + 9, p[-1][1] + 9), fill=col)
            last = [v for v in ys[: int(upto) + 1] if v is not None]
            if last: d.text((p[-1][0] + 22, p[-1][1]), f"{name} " + a["fmt"].format(last[-1]), font=font(SANSB, 38), fill=col, anchor="lm")
    for xi, label in a["marks"]:
        if xi <= upto:
            x = P(xi, ymin)[0]; d.line([(x, Y1 - 10), (x, Y0)], fill=RED, width=3); d.text((x + 10, Y1 - 6), label, font=font(MONOB, 28), fill=RED)
    source(c, a["src"]); return c

def big_frame(a, t, t0, t1):
    c = blurbg(*a["bg"]) if a["bg"] else paper(); dark = bool(a["bg"]); d = ImageDraw.Draw(c); tt = t - t0
    s = a["num"]
    if a["count"]:
        v0, v1, dur = a["count"]; v = v0 + (v1 - v0) * ease(cl((tt - 0.15) / dur)); s = a["fmt"].format(v)
    col = (255, 255, 255) if dark and a["col"] == INK else a["col"]
    f = font(NUMF, 300)
    while d.textlength(s, font=f) > W - 240: f = font(NUMF, f.size - 10)
    d.text((W / 2, H / 2 - 70), s, font=f, fill=col, anchor="mm")
    if a["sub"] and tt > 0.3:
        fs = font(WORD, 58); sw = d.textlength(a["sub"], font=fs); y = H / 2 + 150
        if a["hl_sub"]: hl(d, (W / 2 - sw / 2 - 10, y - 4, W / 2 + sw / 2 + 10, y + 64), u=ease((tt - 0.3) / 0.4))
        d.text((W / 2, y + 30), a["sub"], font=fs, fill=INK if a["hl_sub"] or not dark else (255, 255, 255), anchor="mm")
    return c

def chapter_frame(a, t, t0, t1):
    c = blurbg(*a["bg"]) if a["bg"] else Image.new("RGBA", (W, H), INK + (255,)); tt = t - t0
    sw, sh = min(1500, W - 60), 330; s = paper(sw, sh); s.putalpha(zig_mask(sw, sh, 26, 15)); d = ImageDraw.Draw(s)
    d.text((70, 50), a["item"], font=font(MONOB, 46), fill=GREY)
    ft = font(WORD, 92); txt = a["title"]
    while d.textlength(txt, font=ft) > sw - 140: ft = font(WORD, ft.size - 4)
    n = int(max(0, tt - 0.3) * 30); shown = txt[:n]; tw = d.textlength(txt, font=ft)
    if n >= len(txt): hl(d, (64, 150, 64 + tw + 16, 260), u=ease((tt - 0.3 - len(txt) / 30) / 0.35))
    d.text((70, 140), shown, font=ft, fill=INK)
    u = ease(tt / 0.35); shadowed(c, s, (W - sw) / 2, (H - sh) / 2 + 50 * (1 - u), blur=22, alpha=150); return c

_GEO = {}
def geo():
    if not _GEO:
        js = json.load(open("D:/why habibi/_style_kit/maps/ne_10m_admin_0_countries.geojson", encoding="utf-8"))
        for f in js["features"]:
            g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            _GEO[f["properties"].get("ADMIN") or f["properties"].get("NAME")] = [p[0] for p in polys]
    return _GEO
_ST = {}
def us_states():
    if not _ST:
        js = json.load(open("D:/why habibi/_style_kit/maps/ne_50m_admin_1_states_provinces_lakes.geojson", encoding="utf-8"))
        for f in js["features"]:
            pr = f["properties"]
            if pr.get("iso_a2") != "US": continue
            g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            _ST[pr.get("name")] = [p[0] for p in polys]
    return _ST
def merc(lat): lat = max(-84.0, min(84.0, lat)); return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
_MB = {}
def map_frame(a, t, t0, t1):
    lon_c, lat_c, deg_w = a["view"]; S2 = 1.25; MW, MH = int(W * S2), int(H * S2); k = MW / math.radians(deg_w); yc = merc(lat_c)
    def xy(lon, lat): return MW / 2 + k * math.radians(lon - lon_c), MH / 2 - k * (merc(lat) - yc)
    key = a["view"]
    if key not in _MB:
        m = Image.new("RGBA", (MW, MH), SEA + (255,)); d = ImageDraw.Draw(m)
        for name, polys in geo().items():
            for ring in polys:
                xs = [p[0] for p in ring]
                if max(xs) < lon_c - deg_w or min(xs) > lon_c + deg_w: continue
                q = [xy(lo, la) for lo, la in ring]
                if len(q) > 2: d.polygon(q, fill=LAND, outline=(176, 168, 152))
        if -130 < lon_c < -60:                                                   # US views: state borders
            for name, polys in us_states().items():
                for ring in polys:
                    q = [xy(lo, la) for lo, la in ring]
                    if len(q) > 2: d.line(q + [q[0]], fill=(196, 188, 172), width=2)
        _MB[key] = m
    u = cl((t - t0) / max(t1 - t0, 1e-6)); z = a["z"][0] + (a["z"][1] - a["z"][0]) * u
    ww, hh = W / z, H / z; x0, y0 = MW / 2 - ww / 2 * S2 / S2 * 1, MH / 2 - hh / 2
    base = _MB[key].copy(); d = ImageDraw.Draw(base); tt = t
    for op in a["ops"]:
        kind = op[0]
        if kind in ("country", "states"):
            _, name, kk = op
            if tt < AT(kk): continue
            al = ease((tt - AT(kk)) / 0.5)
            lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            rings = geo().get(name, []) if kind == "country" else [r for n in name for r in us_states().get(n, [])]
            for ring in rings:
                q = [xy(lo, la) for lo, la in ring]
                if len(q) > 2: dl.polygon(q, fill=RED + (int(120 * al),), outline=RED + (int(255 * al),))
            base.alpha_composite(lay); d = ImageDraw.Draw(base)
        elif kind == "route":
            _, pts, kk, dur = op
            if tt < AT(kk): continue
            q = [xy(*p) for p in pts]; f = ease((tt - AT(kk)) / dur); seg = [q[0]]; Ls = [math.dist(q[i], q[i + 1]) for i in range(len(q) - 1)]
            want = sum(Ls) * f; acc = 0
            for i, l in enumerate(Ls):
                if acc + l <= want: seg.append(q[i + 1]); acc += l
                else: g = (want - acc) / max(l, 1e-6); seg.append((q[i][0] + (q[i + 1][0] - q[i][0]) * g, q[i][1] + (q[i + 1][1] - q[i][1]) * g)); break
            d.line(seg, fill=BLUE, width=9, joint="curve")
        elif kind in ("pin", "x"):
            lon, lat, label, kk = (op[1], op[2], op[3], op[4]) if kind == "pin" else (op[1], op[2], "", op[3])
            if tt < AT(kk): continue
            x, y = xy(lon, lat); al = ease((tt - AT(kk)) / 0.25); r = 16
            if kind == "x":
                d.line([(x - 26, y - 26), (x + 26, y + 26)], fill=RED, width=11); d.line([(x - 26, y + 26), (x + 26, y - 26)], fill=RED, width=11)
            else:
                d.ellipse((x - r, y - r, x + r, y + r), fill=RED, outline=(255, 255, 255), width=4)
            if label:
                fl = font(SANSB, 48); lw = d.textlength(label, font=fl)
                d.rectangle((x + 28, y - 34, x + 52 + lw, y + 30), fill=(255, 255, 255)); d.text((x + 40, y), label, font=fl, fill=INK, anchor="lm")
    view = base.resize((W, H), Image.BICUBIC, box=(MW / 2 - ww / 2 * S2, MH / 2 - hh / 2 * S2, MW / 2 + ww / 2 * S2, MH / 2 + hh / 2 * S2))
    if a["title"]:
        dv = ImageDraw.Draw(view); ft = font(WORD, 56); tw = dv.textlength(a["title"], font=ft)
        dv.rectangle((70, 60, 70 + tw + 60, 160), fill=PAPER); dv.text((100, 110), a["title"], font=ft, fill=INK, anchor="lm")
    source(view, a["src"]); return view

def end_frame(a, t, t0, t1):
    c = Image.new("RGBA", (W, H), INK + (255,)); tt = t - t0
    logo = G.get("_logo")
    if logo is None:
        logo = Image.open("D:/the-bill-explained/brand/logo_800.png").convert("RGBA").resize((300, 300), Image.LANCZOS)
        m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 299, 299), fill=255); logo.putalpha(m); G["_logo"] = logo
    pop(c, logo, W / 2, 250, t, t0 + 0.2, 0.3)
    d = ImageDraw.Draw(c)
    if tt > 0.6: d.text((W / 2, 470), "The Bill, Explained", font=font(WORD, 64), fill=PAPER, anchor="mm")
    if tt > 0.9: d.text((W / 2, 545), "New bill every Wednesday", font=font(MONO, 40), fill=(190, 184, 172), anchor="mm")
    # end-screen element slots (YouTube draws video + subscribe here): two light frames
    for x0 in (180, 1000):
        d.rectangle((x0, 640, x0 + 740, 640 + 416 - 40), outline=(60, 60, 60), width=3)
    return c

KINDS = dict(vid=vid_frame, kb=kb_frame, receipt=receipt_frame, bars=bars_frame, line=line_frame, big=big_frame, chapter=chapter_frame, map=map_frame, end=end_frame)

# ------------------------------------------------------------------ overlays + captions
def shot_at(t):
    st = G["SHOT_T"]; i = max(0, np.searchsorted(st, t, side="right") - 1)
    t1 = st[i + 1] if i + 1 < len(st) else G["DUR"]; return i, G["SHOTS"][i], st[i], t1

def draw_ov(c, t):
    for j, (key, kind, a) in enumerate(G.get("OV", [])):
        t0 = G["OVT"][j]; t1 = t0 + a.get("dur", 3.0)
        if not (t0 <= t < t1): continue
        u = ease((t - t0) / 0.25) * (1 - ease((t - (t1 - 0.25)) / 0.25))
        if kind == "tag": pop(c, price_tag(a["text"], a.get("h", 150)), a["x"], a["y"], t, t0)
        elif kind == "label":
            d = ImageDraw.Draw(c); f = font(WORD, a.get("size", 54)); tw = d.textlength(a["text"], font=f); x, y = a.get("x", 100), a.get("y", 90)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            dl.rectangle((x - 24, y - 14, x + tw + 24, y + f.size + 20), fill=PAPER + (int(255 * u),)); hl(dl, (x - 6, y + f.size * 0.55, x + tw + 6, y + f.size + 12), col=YELLOW + (int(255 * u),))
            dl.text((x, y), a["text"], font=f, fill=INK + (int(255 * u),)); c.alpha_composite(lay)

CAP_Y = H - 150
def _caps():
    out = []; fix = G.get("CAPFIX", {})
    for ln, ws in sorted(G["WORDS"].items()):
        cur = []
        for w in ws:
            tok = fix.get((ln, w["w"].strip()), fix.get(w["w"].strip(), w["w"].strip()))
            if not tok: continue
            if re.match(r"^[.,]\d|^%", tok):                                          # "$2" + ".13" -> "$2.13" (also across a chunk break)
                if cur: cur[-1] = (cur[-1][0] + tok, cur[-1][1], w["e"]); continue
                if out: out[-1][-1] = (out[-1][-1][0] + tok, out[-1][-1][1], w["e"]); continue
            cur.append((tok, w["s"], w["e"]))
            if len(cur) >= 5 or cur[-1][0].endswith((".", ",", "?", "!", ":")) and len(cur) >= 3:
                out.append(cur); cur = []
        if cur: out.append(cur)
    return [(ch[0][1], ch[-1][2] + 0.15, " ".join(x[0] for x in ch)) for ch in out]
def draw_caps(c, t):
    if "CAPS" not in G: G["CAPS"] = _caps()
    for s, e, txt in G["CAPS"]:
        if s <= t < e:
            d = ImageDraw.Draw(c); f = font(SANSB, 54)
            d.text((W / 2, CAP_Y), txt, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0)); return

def vframe(t):
    """Shorts: header (question, 2 lines) | 1080x1080 panel | captions | footer"""
    i, (key, (kind, a)), t0, t1 = shot_at(t)
    p = KINDS[kind](a, t, t0, t1); draw_ov(p, t)
    c = Image.new("RGBA", (VW, VH), INK + (255,)); c.alpha_composite(p.convert("RGBA"), (0, 400))
    d = ImageDraw.Draw(c); head = G.get("HEAD", ["", ""])
    for j, ln in enumerate(head):
        f = fitf(d, ln, WORD, 84, VW - 120); y = 90 + j * 120; tw = d.textlength(ln, font=f)
        if j == len(head) - 1: hl(d, (VW / 2 - tw / 2 - 18, y + 8, VW / 2 + tw / 2 + 18, y + 104))
        d.text((VW / 2, y + 55), ln, font=f, fill=(255, 255, 255) if j < len(head) - 1 else INK, anchor="mm")
    if "CAPS" not in G: G["CAPS"] = _caps()
    for s0, e, txt in G["CAPS"]:
        if s0 <= t < e:
            f = fitf(d, txt, SANSB, 66, VW - 80); d.text((VW / 2, 1610), txt, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0)); break
    d.text((VW / 2, 1800), "The Bill, Explained", font=font(MONOB, 38), fill=(190, 184, 172), anchor="mm")
    return c

def frame(t):
    if G.get("VERT"): return vframe(t)
    i, (key, (kind, a)), t0, t1 = shot_at(t)
    c = KINDS[kind](a, t, t0, t1)
    if kind != "end":
        draw_ov(c, t)
        if not G.get("NO_CAPS"): draw_caps(c, t)
    return c

# ------------------------------------------------------------------ audio
def load(p, sr=48000):
    a, s = sf.read(p, dtype="float32", always_2d=True); a = a.mean(1)
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    return a
def sfxpath(n):
    for d, ext in ((SFX1, ".wav"), (SFX2, ".mp3")):
        if os.path.exists(d + n + ext): return d + n + ext
    return None
def audio():
    sr = 48000; N = int(G["DUR"] * sr); vo = load(G["ROOT"] + G.get("VOF", "vo/vo.wav")); y = np.zeros(N, np.float32)
    s0 = int(G["LEAD"] * sr); y[s0:s0 + len(vo)] += vo[: N - s0]
    vr = np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)); bed = np.zeros(N, np.float32)
    def put(a, t, db, fade=0.02):
        i = int(t * sr)
        if i < 0: a = a[-i:]; i = 0
        a = a[: max(0, N - i)] * 10 ** (db / 20)
        if len(a) == 0: return
        f = int(fade * sr)
        if f > 1 and len(a) > 2 * f: a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        bed[i:i + len(a)] += a
    def sfx(name, t, db, maxlen=2.5):
        p = sfxpath(name)
        if not p: return
        a = load(p); a = a / (np.max(np.abs(a)) + 1e-9) * vr * 3.0
        if maxlen and len(a) > maxlen * sr: a = a[: int(maxlen * sr)].copy(); f = int(0.2 * sr); a[-f:] *= np.linspace(1, 0, f)
        put(a, t, db)
    for file, t0, t1, db in G["MUSIC"]:
        t0, t1 = (AT(t0) if not isinstance(t0, float) else t0), (G["DUR"] if t1 is None else AT(t1) if not isinstance(t1, float) else t1)
        a = load(MUS + file); n = int((t1 - t0) * sr)
        while len(a) < n: a = np.concatenate([a, load(MUS + file)])
        a = a[:n] / (np.sqrt(np.mean(a[:n] ** 2)) + 1e-9) * vr; put(a, t0, db, fade=2.0)
    for i, (key, (kind, a)) in enumerate(G["SHOTS"]):
        t0 = G["SHOT_T"][i]
        if kind in ("kb", "vid"):
            sfx("whoosh_fast", t0 - 0.12, -30)
            for k2, *_ in a["tags"]: sfx("sticker_slap", AT(k2), -20)
        elif kind == "receipt":
            sfx("paper_slide", t0, -20)
            for k2, *_ in a["rows"]: sfx("typewriter_soft_click", AT(k2), -22, 0.5)
            if a["total"]: sfx("cash_register", AT(a["total"][0]), -16); sfx("highlighter", AT(a["total"][0]) + 0.05, -22)
        elif kind == "bars":
            sfx("paper_slide", t0, -24)
            for k2, *_ in a["bars"]: sfx("swoosh_in", AT(k2), -24)
        elif kind == "line": sfx("marker_write", t0 + 0.3, -24, 2.0)
        elif kind == "big": sfx("impact_soft", t0, -16); sfx("highlighter", t0 + 0.3, -22)
        elif kind == "chapter": sfx("paper_slide", t0, -18); sfx("typewriter_typing_old", t0 + 0.3, -24, 1.4); sfx("highlighter", t0 + 0.3 + len(a["title"]) / 30, -20)
        elif kind == "map":
            sfx("paper_page_turn", t0, -22)
            for op in a["ops"]:
                kk = op[2] if op[0] in ("country", "states", "route") else op[4] if op[0] == "pin" else op[3]
                sfx("pop" if op[0] == "pin" else "marker_squeak" if op[0] == "route" else "hit_short_bass", AT(kk), -22)
        elif kind == "end": sfx("cash_register", t0 + 0.2, -18)
    for j, (key, kind, a) in enumerate(G.get("OV", [])):
        sfx("sticker_slap" if kind == "tag" else "marker_squeak", G["OVT"][j], -22)
    for key, name, db in G.get("EV", []): sfx(name, AT(key), db, 3.0)
    y += bed; y = y / max(np.max(np.abs(y)), 1e-6) * 0.9
    B = G["ROOT"] + "build/"; os.makedirs(B, exist_ok=True); sf.write(B + "mix_raw.wav", y, sr, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(B + "mix_raw.wav", B + "mix.wav", target=-14, tp=-1); print("audio", AM.measure(B + "mix.wav"))

# ------------------------------------------------------------------ render
def seg(i, n):
    B = G["ROOT"] + "build/"; os.makedirs(B, exist_ok=True); a, b = G["NF"] * i // n, G["NF"] * (i + 1) // n
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}" if G.get("VERT") else f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-threads", "3", "-pix_fmt", "yuv420p", B + f"seg_{i}.mp4"], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(frame(f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("seg done", i, flush=True)
def final(n):
    B = G["ROOT"] + "build/"
    with open(B + "list.txt", "w") as f:
        for i in range(n): f.write(f"file 'seg_{i}.mp4'\n")
    os.makedirs(G["ROOT"] + "export", exist_ok=True); out = G["ROOT"] + "export/" + G["NAME"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

def run(spec):
    setup(spec); m = sys.argv[1] if len(sys.argv) > 1 else "times"; me = spec["__file__"]
    if m == "times":
        for i, l in enumerate(G["LINES"]): print(f"{i:3d} {G['T'][i]:7.2f} {l[:80]}")
        print("DUR", round(G["DUR"], 1), "shots", len(G["SHOTS"]))
    elif m == "keys":
        keys = [s[0] for s in G["SHOTS"]] + [k for k, _, _ in G.get("OV", [])] + [k for k, _, _ in G.get("EV", [])]
        for s in G["SHOTS"]:
            a = s[1][1]
            keys += [r[0] for r in a.get("rows", [])] + ([a["total"][0]] if a.get("total") else []) + [b[0] for b in a.get("bars", [])] + [tg[0] for tg in a.get("tags", ())]
        for k in keys:
            if isinstance(k, tuple) and isinstance(k[1], str) and all(wt(k[0], x) is None for x in k[1].split("|")): print("MISSING", k, "|", G["LINES"][k[0]][:90])
        st = G["SHOT_T"]; gaps = sorted((st[i + 1] - st[i], i) for i in range(len(st) - 1))
        print("shots", len(st), "shortest", [(round(g, 2), i) for g, i in gaps[:5]], "longest", [(round(g, 2), i) for g, i in gaps[-6:]])
        bad = [i for i in range(len(st) - 1) if st[i + 1] < st[i]]
        if bad: print("OUT OF ORDER", bad)
    elif m == "qa":
        st = G["SHOT_T"]; ts = [float(x) for x in sys.argv[2:]] or [(st[i] + (st[i + 1] if i + 1 < len(st) else G["DUR"])) / 2 for i in range(len(st))]
        tw, th = (270, 480) if G.get("VERT") else (384, 216)
        tiles = [frame(t).convert("RGB").resize((tw, th)) for t in ts]; cols = 6
        S = Image.new("RGB", (cols * (tw + 10), ((len(tiles) + cols - 1) // cols) * (th + 20)), (20, 20, 20))
        for i, (im, tt) in enumerate(zip(tiles, ts)):
            S.paste(im, ((i % cols) * (tw + 10), (i // cols) * (th + 20))); ImageDraw.Draw(S).text(((i % cols) * (tw + 10) + 6, (i // cols) * (th + 20) + th + 2), f"{i}: {tt:.1f}", fill=(255, 220, 90))
        out = G["ROOT"] + "build/" + ("qa.png" if len(sys.argv) > 2 else "qa_all.png"); os.makedirs(G["ROOT"] + "build", exist_ok=True); S.save(out); print(out)
    elif m == "frame":
        out = G["ROOT"] + "build/frame.png"; frame(float(sys.argv[2])).convert("RGB").save(out); print(out)
    elif m == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "audio": audio()
    elif m == "final": final(int(sys.argv[2]))
    elif m == "chapters":
        for i, (ln, name) in enumerate(G["CH"]):
            t = 0 if i == 0 else G["T"][ln] - 0.1; print(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    elif m == "all":
        n = int(sys.argv[2]); env = dict(os.environ, PYTHONUTF8="1"); low = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0)
        ps = [subprocess.Popen([sys.executable, me, "seg", str(i), str(n)], env=env, creationflags=low) for i in range(n)]
        for p in ps: p.wait()
        audio(); final(n)
