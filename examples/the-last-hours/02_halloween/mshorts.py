"""mshorts: The Last Hours vertical mystery Shorts (1080x1920, Case File look). Every Short ends on the Alcatraz file unless its spec has "end" (own long video: img, label, title, cta).
  cd "D:/why habibi/_newchannel/02_halloween"
  uv run --no-project --with pillow --with numpy --with soundfile python mshorts.py qa 33 0.2 5 12      (contact sheet)
  uv run --no-project --with pillow --with numpy --with soundfile python mshorts.py render 33
  uv run --no-project --with faster-whisper --with soundfile python mshorts.py words 33 34 ...           (whisper timings)
Specs: specs.py (S dict). VO: bank/<folder>/vo_chatterbox.wav = one take per vo_lines.txt line, exact-zero 0.35 s gaps.
Layout: header (kicker + 1-2 big lines) y 110-470 | evidence panel y 500-1460 | captions y 1555 | footer.
One text per slot: the header changes per beat, captions own the band under the panel, the end card turns captions off."""
import os, sys, json, math, re, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0, "D:/why habibi/_newchannel"); import lastkit as L
from lastkit import INK, BONE, RED, STEEL, COND, TYPE, SER, font, ease, clamp01

VW, VH, FPS = 1080, 1920, 30
PY, PW, PH = 500, 1080, 960
ROOT = "D:/why habibi/_newchannel/02_halloween/"; BANK = "D:/why habibi/_pipeline/shorts/bank/"
MEDIA = ROOT + "media/"; SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
ALC = "D:/why habibi/_newchannel/01_alcatraz/media/"; OUT = ROOT + "out/"; BUILD = ROOT + "build/"
MAPS = "D:/why habibi/_style_kit/maps/"; CTA = ROOT + "cta/cta.wav"
PAPER, PINK, DARKRED = (226, 220, 204), (40, 36, 30), (120, 26, 26)
ALC_TITLE = ("What the FBI Found When", "3 Men Vanished From Alcatraz")
for _d in (OUT, BUILD): os.makedirs(_d, exist_ok=True)

# ---------------------------------------------------------------- timing / words
def read_mono(path, sr_out=None):
    import soundfile as sf
    y, sr = sf.read(path, dtype="float32", always_2d=True); y = y.mean(1)
    if sr_out and sr != sr_out:
        y = np.interp(np.arange(int(len(y) * sr_out / sr)) / sr_out, np.arange(len(y)) / sr, y).astype(np.float32); sr = sr_out
    return y, sr

def line_times(wav, n):
    """line i = audio between the exact-zero gaps that vo_batch_chatterbox.py inserts (0.35 s)"""
    y, sr = read_mono(wav); z = (np.abs(y) < 1e-7).astype(np.int8)
    d = np.diff(np.concatenate([[0], z, [0]])); st, en = np.where(d == 1)[0], np.where(d == -1)[0]
    gaps = [(s, e) for s, e in zip(st, en) if e - s >= int(0.30 * sr)]
    out, cur = [], 0
    for s, e in gaps:
        if s > cur: out.append((cur / sr, s / sr))
        cur = e
    if cur < len(y) - int(0.05 * sr): out.append((cur / sr, len(y) / sr))
    assert len(out) == n, f"{wav}: found {len(out)} lines, expected {n}"
    return out, len(y) / sr

def load_words(path, fix, fix2=None):
    fix2 = fix2 or {}
    ws = []
    for seg in json.load(open(path, encoding="utf-8")):
        for w in seg["words"]:
            tx = w["w"].strip()
            if not tx: continue
            key = re.sub(r"[^\w'$%.,-]", "", tx)
            for k in (tx, key, key.strip(".,")):
                if k in fix: tx = fix[k]; break
            ws.append(dict(w=tx, s=w["s"], e=w["e"]))
    nz = lambda x: re.sub(r"[^a-z0-9']", "", x.lower())
    for (a, b), x in fix2.items():                                   # two-word context fixes, e.g. ("has", "ended") -> "is"
        for i in range(len(ws) - 1):
            if nz(ws[i]["w"]) == a and nz(ws[i + 1]["w"]) == b: ws[i]["w"] = x
    return ws

def chunks(ws, until):
    out, cur = [], []
    for w in ws:
        if w["s"] >= until: break
        cur.append(w)
        if len(cur) == 3 or w["w"].rstrip('"”').endswith((",", ".", "?", "!", ":")): out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        s, e = c[0]["s"], c[-1]["e"] + 0.18
        if i + 1 < len(out): e = min(e, out[i + 1][0]["s"])
        txt = " ".join(x["w"] for x in c).strip().strip(",:;")
        txt = re.sub(r"\.$", "", txt) if not txt.endswith("..") else txt
        res.append((s, e, txt))
    return res

# ---------------------------------------------------------------- drawing helpers
def img(path, crop=None):
    p = path if os.path.isabs(path) else MEDIA + path
    return L.bw(p, crop)

def cover(src, t, t0, t1, z0=1.0, z1=1.12, c0=(.5, .5), c1=(.5, .5), w=PW, h=PH, eased=False):
    u = clamp01((t - t0) / max(t1 - t0, 1e-6)); u = ease(u) if eased else u
    z = z0 + (z1 - z0) * u; cx = c0[0] + (c1[0] - c0[0]) * u; cy = c0[1] + (c1[1] - c0[1]) * u
    s = max(w / src.width, h / src.height) * z; ww, hh = min(w / s, src.width), min(h / s, src.height)
    x0 = max(0.0, min(max(cx * src.width - ww / 2, 0), src.width - ww)); y0 = max(0.0, min(max(cy * src.height - hh / 2, 0), src.height - hh))
    return src.resize((w, h), Image.BICUBIC, box=(x0, y0, x0 + ww, y0 + hh)).convert("RGBA"), (x0, y0, s)

_VIG = {}
def vig(im, k=0.5):
    if k not in _VIG:
        yy, xx = np.mgrid[0:PH, 0:PW]; r = np.sqrt(((xx - PW / 2) / (PW / 2)) ** 2 + ((yy - PH / 2) / (PH / 2)) ** 2)
        _VIG[k] = np.clip(1 - k * np.clip(r - 0.45, 0, None) ** 1.5, 0, 1).astype(np.float32)[..., None]
    a = np.asarray(im.convert("RGB"), np.float32) * _VIG[k]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def dim(im, k):
    return Image.blend(im.convert("RGBA"), Image.new("RGBA", im.size, (0, 0, 0, 255)), k)

def shadow_text(c, s, x, y, size, fill=BONE, fnt=TYPE, anchor="lm", alpha=1.0):
    if alpha <= 0 or not s: return
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); f = font(fnt, size)
    d.text((x + 3, y + 3), s, font=f, fill=(0, 0, 0, int(200 * alpha)), anchor=anchor)
    d.text((x, y), s, font=f, fill=tuple(fill) + (int(255 * alpha),), anchor=anchor); c.alpha_composite(lay)

def tlabel(c, s, x, y, t, t0, size=30, fill=BONE, anchor="lm", cps=34, fnt=TYPE):
    if t < t0: return
    n = min(len(s), int((t - t0) * cps) + 1); shadow_text(c, s[:n], x, y, size, fill, fnt, anchor)

def fit_size(s, fnt, size, maxw):
    while size > 30 and font(fnt, size).getlength(s) > maxw: size -= 4
    return size

def paper_strip(lines, size=44, pad=34, w=960):
    f = font(TYPE, size); lh = int(size * 1.32); h = pad * 2 + lh * len(lines)
    card = Image.new("RGBA", (w, h), PAPER + (255,)); d = ImageDraw.Draw(card)
    rng = np.random.default_rng(len(lines) * 7 + size)
    a = np.asarray(card, np.float32); a[..., :3] += rng.normal(0, 3.0, a[..., :3].shape); card = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    sh = Image.new("RGBA", (w + 50, h + 50), (0, 0, 0, 0)); sh.paste(Image.new("RGBA", (w, h), (0, 0, 0, 160)), (25, 32))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); sh.alpha_composite(card, (25, 25)); return sh, f, lh, pad

def wrap(s, n):
    lines = []
    for para in s.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            if len(cur) + len(w) + (1 if cur else 0) > n: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
    return lines

def arrowhead(d, p0, p1, col, size=26):
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    pts = [p1, (p1[0] - size * math.cos(ang - 0.45), p1[1] - size * math.sin(ang - 0.45)),
           (p1[0] - size * math.cos(ang + 0.45), p1[1] - size * math.sin(ang + 0.45))]
    d.polygon(pts, fill=col)

# ---------------------------------------------------------------- dark maps
def merc(lat): lat = max(-84.0, min(84.0, lat)); return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
_FEATS, _STATES, _BASES = None, None, {}
def feats():
    global _FEATS
    if _FEATS is None:
        sys.path.insert(0, "D:/why habibi/_style_kit/tools"); from mapkit import _load; _FEATS = _load()
    return _FEATS
def states():
    global _STATES
    if _STATES is None:
        _STATES = []; p = MAPS + "ne_50m_admin_1_states_provinces_lakes.geojson"
        if os.path.exists(p):
            for f in json.load(open(p, encoding="utf-8"))["features"]:
                pr = f["properties"]
                if pr.get("adm0_a3") not in ("USA", "CAN", "AUS"): continue
                g = f["geometry"]; ps = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
                _STATES.append((pr.get("name"), [q[0] for q in ps]))
    return _STATES

class VMap:
    PAD = 1.3
    def __init__(s, lon_c, lat_c, deg_w):
        s.key = (lon_c, lat_c, deg_w); s.W, s.H = int(PW * s.PAD), int(PH * s.PAD)
        s.lon_c, s.k, s.yc = lon_c, PW / math.radians(deg_w), merc(lat_c)
    def xy(s, lon, lat): return s.W / 2 + s.k * math.radians(lon - s.lon_c), s.H / 2 - s.k * (merc(lat) - s.yc)
    def base(s):
        if s.key in _BASES: return _BASES[s.key]
        ss = 2; W, H = s.W * ss, s.H * ss
        def P(r): return [(x * ss, y * ss) for x, y in (s.xy(a, b) for a, b in r)]
        half = math.degrees(s.W / 2 / s.k) + 3
        mask = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(mask); outl = []
        for name, rs in feats():
            for r in rs:
                a = np.asarray(r)
                if a[:, 0].max() < s.lon_c - half or a[:, 0].min() > s.lon_c + half: continue
                p = P(r)
                if max(q[1] for q in p) < 0 or min(q[1] for q in p) > H: continue
                dm.polygon(p, fill=255); outl.append(p)
        f32 = np.float32; yy = np.linspace(0, 1, H, dtype=f32)[:, None, None]
        sea = np.array((15, 16, 18), f32) * (1.05 - 0.1 * yy) * np.ones((1, W, 1), f32)
        halo = np.asarray(mask.filter(ImageFilter.GaussianBlur(10 * ss)), f32)[..., None] / 255
        sea = sea + 10 * halo
        land = np.array((52, 51, 49), f32) * (1.05 - 0.12 * yy) + np.random.default_rng(5).normal(0, 2.2, (H, W, 1)).astype(f32)
        m = np.asarray(mask, f32)[..., None] / 255
        im = Image.fromarray((sea * (1 - m) + land * m).clip(0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
        for name, rs in states():
            for r in rs:
                a = np.asarray(r)
                if a[:, 0].max() < s.lon_c - half or a[:, 0].min() > s.lon_c + half: continue
                p = P(r); d.line(p + [p[0]], fill=(92, 92, 92, 255), width=2 * ss // 2 + 1)
        for p in outl: d.line(p + [p[0]], fill=(120, 124, 128, 255), width=2 * ss)
        dw = s.key[2]; step = 1 if dw < 8 else 5 if dw < 30 else 10
        lon0 = math.floor((s.lon_c - half) / step) * step; lat_c = s.key[1]
        for lon in np.arange(lon0, s.lon_c + half + step, step):
            d.line([(x * ss, y * ss) for x, y in (s.xy(lon, la) for la in np.linspace(lat_c - 60, lat_c + 60, 60) if abs(la) < 84)], fill=(70, 70, 72, 255), width=ss)
        for lat in np.arange(math.floor((lat_c - 60) / step) * step, lat_c + 60, step):
            if abs(lat) >= 84: continue
            y = s.xy(s.lon_c, lat)[1] * ss; d.line([(0, y), (W, y)], fill=(70, 70, 72, 255), width=ss)
        _BASES[s.key] = im.resize((s.W, s.H), Image.LANCZOS); return _BASES[s.key]
    def state_poly(s, name):
        for nm, rs in states():
            if nm == name: return [[s.xy(a, b) for a, b in r] for r in rs]
        return []

def map_panel(b, t, t0, t1):
    V = VMap(*b["view"]); base = V.base(); z0, z1 = b.get("z", (1.0, 1.06)); u = clamp01((t - t0) / max(t1 - t0, 1e-6))
    z = z0 + (z1 - z0) * u; c0 = b.get("c0", (.5, .5)); c1 = b.get("c1", c0)
    cx = (c0[0] + (c1[0] - c0[0]) * ease(u)) * V.W; cy = (c0[1] + (c1[1] - c0[1]) * ease(u)) * V.H
    ww, hh = PW / z, PH / z; x0, y0 = cx - ww / 2, cy - hh / 2
    p = base.resize((PW, PH), Image.BICUBIC, box=(x0, y0, x0 + ww, y0 + hh)).convert("RGBA")
    def T(lon, lat): x, y = V.xy(lon, lat); return ((x - x0) * z, (y - y0) * z)
    lay = Image.new("RGBA", p.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); tt = t - t0; labels = []
    for op in b.get("ops", []):
        k, ts = op[0], op[-1] if isinstance(op[-1], (int, float)) else 0
        if k == "state":
            _, name, ts = op
            if tt < ts: continue
            a = ease((tt - ts) / 0.5)
            for r in V.state_poly(name):
                q = [((x - x0) * z, (y - y0) * z) for x, y in r]
                d.polygon(q, fill=DARKRED + (int(150 * a),)); d.line(q + [q[0]], fill=RED + (int(255 * a),), width=4)
        elif k == "route":
            _, pts, ts, dur = op
            if tt < ts: continue
            q = [T(*pt) for pt in pts]; L_ = [math.dist(q[i], q[i + 1]) for i in range(len(q) - 1)]; tot = sum(L_) or 1
            want = tot * ease((tt - ts) / dur); out = [q[0]]; acc = 0
            for i, l in enumerate(L_):
                if acc + l <= want: out.append(q[i + 1]); acc += l
                else: f = (want - acc) / max(l, 1e-6); out.append((q[i][0] + (q[i + 1][0] - q[i][0]) * f, q[i][1] + (q[i + 1][1] - q[i][1]) * f)); break
            d.line(out, fill=RED + (255,), width=6, joint="curve")
            if len(out) > 1 and tt - ts < dur + 0.05: d.ellipse((out[-1][0] - 7, out[-1][1] - 7, out[-1][0] + 7, out[-1][1] + 7), fill=BONE + (255,))
        elif k == "arrow":
            _, a0, a1, label, ts = op
            if tt < ts: continue
            p0, p1 = T(*a0), T(*a1); u2 = ease((tt - ts) / 0.6); pe = (p0[0] + (p1[0] - p0[0]) * u2, p0[1] + (p1[1] - p0[1]) * u2)
            d.line([p0, pe], fill=BONE + (255,), width=5)
            if u2 > 0.95: arrowhead(d, p0, p1, BONE + (255,))
            if label: labels.append((label, pe[0] + 16, pe[1] + 30, ts + 0.5, 30, BONE))
        elif k == "circle":
            _, lon, lat, r_mi, label, ts = op
            if tt < ts: continue
            c_ = T(lon, lat); e_ = T(lon, lat + r_mi / 69.0); r = abs(c_[1] - e_[1]); u2 = ease((tt - ts) / 0.45); rr = r * (0.88 + 0.12 * u2)
            d.ellipse((c_[0] - rr, c_[1] - rr, c_[0] + rr, c_[1] + rr), outline=RED + (int(255 * u2),), width=6)
            if label: labels.append((label, c_[0], c_[1] - rr - 34, ts + 0.3, 30, BONE, "mm"))
        elif k == "disc":
            _, lon, lat, r_km, label, ts = op
            if tt < ts: continue
            c_ = T(lon, lat); e_ = T(lon, lat + r_km / 111.0); r = abs(c_[1] - e_[1]); u2 = ease((tt - ts) / 0.6); rr = r * (0.6 + 0.4 * u2)
            d.ellipse((c_[0] - rr, c_[1] - rr, c_[0] + rr, c_[1] + rr), fill=DARKRED + (int(140 * u2),), outline=RED + (int(255 * u2),), width=5)
            if label: labels.append((label, c_[0], c_[1] + rr + 36, ts + 0.4, 30, BONE, "mm"))
        elif k == "pin":
            _, lon, lat, label, ts = op[:5]; dx, dy = (op[5] if len(op) > 6 else 22), (op[6] if len(op) > 6 else 0)
            if tt < ts: continue
            x, y = T(lon, lat); u2 = ease((tt - ts) / 0.25); r = 11 * (1.6 - 0.6 * u2)
            d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=BONE + (255,)); d.ellipse((x - r, y - r, x + r, y + r), fill=RED + (255,))
            if label: labels.append((label, x + dx, y + dy, ts + 0.15, 32, BONE))
        elif k == "label":
            _, lon, lat, label, ts = op[:5]; size = op[5] if len(op) > 5 else 30
            if tt < ts: continue
            x, y = T(lon, lat); labels.append((label, x, y, ts, size, STEEL, "mm"))
    p.alpha_composite(lay)
    lat_c = b["view"][1]; px_mi = V.k * math.radians(1.0 / (69.17 * math.cos(math.radians(lat_c)))) * z
    want = 170 / px_mi; nice = min([1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000], key=lambda v: abs(v - want)); L_px = nice * px_mi
    d2 = ImageDraw.Draw(p); x1, y1 = PW - 40, PH - 46
    d2.line([(x1 - L_px, y1), (x1, y1)], fill=BONE, width=4); d2.line([(x1 - L_px, y1 - 10), (x1 - L_px, y1 + 2)], fill=BONE, width=4); d2.line([(x1, y1 - 10), (x1, y1 + 2)], fill=BONE, width=4)
    shadow_text(p, f"{nice:,} MI", x1, y1 - 26, 26, BONE, TYPE, "rs")
    p = vig(p, 0.35)
    for lb in labels:
        s_, x, y, ts, size, col = lb[:6]; anc = lb[6] if len(lb) > 6 else "lm"
        tlabel(p, s_, x, y, tt, ts, size=size, fill=col, anchor=anc)
    return p

# ---------------------------------------------------------------- panels
def panel(b, t, t0, t1):
    k = b["kind"]; tt = t - t0
    if k == "photo":
        p, _ = cover(img(b["src"], b.get("crop")), t, t0, t1 + 0.6, *b.get("z", (1.0, 1.12)), b.get("c0", (.5, .5)), b.get("c1", b.get("c0", (.5, .5))))
        p = vig(p)
    elif k == "doc":
        src = img(b["src"], b.get("crop")); bx = b.get("box")
        cen = ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2) if bx else (.5, .5)
        p, (x0, y0, s) = cover(src, min(t, t0 + 1.2), t0, t0 + 1.2, *b.get("z", (1.0, 1.25)), b.get("c0", (.5, .5)), b.get("c1", cen), eased=True)
        p = vig(p, 0.35)
        if bx and tt > 0.9:
            a = ease((tt - 0.9) / 0.4)
            X0, Y0 = (bx[0] * src.width - x0) * s, (bx[1] * src.height - y0) * s; X1, Y1 = (bx[2] * src.width - x0) * s, (bx[3] * src.height - y0) * s
            m = Image.new("L", p.size, 0); ImageDraw.Draw(m).rounded_rectangle((X0 - 14, Y0 - 12, X1 + 14, Y1 + 12), 16, fill=255)
            m = m.filter(ImageFilter.GaussianBlur(12)); inv = ImageOps.invert(m).point(lambda v: int(v * 0.62 * a))
            p.paste(Image.new("RGBA", p.size, (0, 0, 0, 255)), (0, 0), inv)
            u2 = ease((tt - 1.2) / 0.45)
            if u2 > 0: ImageDraw.Draw(p).rectangle((X0, Y1 + 10, X0 + (X1 - X0) * u2, Y1 + 17), fill=RED)
    elif k == "map":
        p = map_panel(b, t, t0, t1)
    elif k == "quote":
        p = Image.new("RGBA", (PW, PH), INK + (255,))
        if b.get("bg"):
            bgp, _ = cover(img(b["bg"], b.get("crop")), t, t0, t1 + 0.6, 1.0, 1.08); p = dim(vig(bgp), 0.55)
        lines = wrap(b["text"], b.get("wrap", 30)); strip, f, lh, pad = paper_strip(lines, b.get("size", 44))
        u = ease(tt / 0.35); y = (PH - strip.height) / 2 + 40 * (1 - u) + b.get("dy", 30)
        s2 = strip.copy()
        if u < 1: s2.putalpha(s2.split()[3].point(lambda v: int(v * u)))
        p.alpha_composite(s2, (int((PW - strip.width) / 2), int(y)))
        d = ImageDraw.Draw(p); cps = b.get("cps", 26); t_type = tt - 0.35; shown = int(max(0, t_type) * cps)
        for i, ln in enumerate(lines):
            if shown <= 0: break
            d.text(((PW - strip.width) / 2 + 25 + pad, y + 25 + pad + i * lh), ln[:shown], font=f, fill=PINK); shown -= len(ln) + 1
        if b.get("when"): tlabel(p, b["when"], (PW - strip.width) / 2 + 30, y - 6, tt, 0.1, size=34, fill=RED, anchor="ls")
        if b.get("who"): tlabel(p, b["who"], (PW + strip.width) / 2 - 30, y + strip.height + 30, tt, 0.5, size=28, fill=STEEL, anchor="rm")
    elif k == "card":
        p = Image.new("RGBA", (PW, PH), INK + (255,))
        if b.get("bg"):
            bgp, _ = cover(img(b["bg"], b.get("crop")), t, t0, t1 + 0.6, 1.0, 1.08); p = dim(vig(bgp), 0.7)
        big = b["big"]
        if "count" in b:
            a0, a1, cd = b["count"]; v = a0 + (a1 - a0) * ease(clamp01((tt - 0.2) / cd)); big = b.get("fmt", "{:,.0f}").format(v)
        sz = fit_size(big, COND, b.get("size", 300), 980)
        L.text(p, big, PW / 2, PH / 2 - 40, sz, b.get("col", BONE), COND, alpha=ease(tt / 0.25))
        if b.get("sub"): tlabel(p, b["sub"], PW / 2, PH / 2 + sz * 0.55, tt, 0.3, size=40, fill=STEEL, anchor="mm")
    else:
        p = Image.new("RGBA", (PW, PH), INK + (255,))
    for ov in b.get("ov", []):
        k2 = ov[0]
        if k2 == "stamp":
            _, s_, ts = ov[:3]; x = ov[3] if len(ov) > 3 else PW / 2; y = ov[4] if len(ov) > 4 else PH - 170; size = ov[5] if len(ov) > 5 else 96
            L.stamp(p, s_, x, y, tt, ts, size=size, rot=-6)
        elif k2 == "tag":
            if "fade" not in _PR:
                g = np.zeros((PH, PW), np.uint8); g[PH - 170:] = (np.linspace(0, 170, 170)[:, None]).astype(np.uint8); _PR["fade"] = Image.fromarray(g)
            p.paste(Image.new("RGBA", p.size, (0, 0, 0, 255)), (0, 0), _PR["fade"])
            tlabel(p, ov[1], 36, PH - 44, tt, ov[2] if len(ov) > 2 else 0.2, size=30, fill=BONE)
        elif k2 == "type":
            _, s_, x, y, ts = ov[:5]; size = ov[5] if len(ov) > 5 else 40; col = ov[6] if len(ov) > 6 else BONE
            tlabel(p, s_, x, y, tt, ts, size=size, fill=col, anchor="mm")
        elif k2 == "print":
            _, src, x, y, w, rot, ts = ov
            if tt >= ts:
                key = ("print", src, w, rot)
                if key not in _PR: _PR[key] = L.print_card(img(src), w, border=12, rot=rot)
                L.drop(p, _PR[key], x, y, tt, ts, dur=0.3, dy=40)
    return p
_PR = {}

# ---------------------------------------------------------------- frame
class Short:
    def __init__(s, sid):
        import specs; s.sid = sid; s.spec = specs.S[sid]; sp = s.spec; s.dir = BANK + sp["folder"] + "/"
        s.lines = [l.strip() for l in open(s.dir + "vo_lines.txt", encoding="utf-8") if l.strip()]
        s.LT, s.vo_end = line_times(s.dir + "vo_chatterbox.wav", len(s.lines))
        s.words = load_words(s.dir + "vo_words_cb.json", sp.get("fix", {}), sp.get("fix2", {})) if os.path.exists(s.dir + "vo_words_cb.json") else []
        s.caps = chunks(s.words, s.vo_end + 0.1)
        import soundfile as sf
        s.end = sp.get("end", {}); s.cta = s.end.get("cta", CTA)   # per-Short end card + spoken line (default: the Alcatraz file)
        s.cta_len = sf.info(s.cta).duration if os.path.exists(s.cta) else 4.0
        s.end_len = round(0.5 + s.cta_len + 1.4, 2); s.total = s.vo_end + s.end_len
        bs = []
        for b in sp["beats"]:
            ln = b["line"]; a, e = s.LT[ln]; st = a + b.get("at", 0.0) * (e - a) + b.get("off", 0.0)
            if ln == 0 and b.get("at", 0) == 0 and b.get("off", 0) == 0: st = 0.0
            bs.append(dict(b, t0=st))
        bs.sort(key=lambda x: x["t0"])
        for i, b in enumerate(bs): b["t1"] = bs[i + 1]["t0"] if i + 1 < len(bs) else s.vo_end
        kick, head, hstart = None, None, 0.0
        for b in bs:
            if "kicker" in b or "head" in b:
                kick = b.get("kicker", kick); head = b.get("head", head); hstart = b["t0"]
            b["hdr"] = (kick, head, hstart)
        s.beats = bs

    def header(s, c, t, kick, head, hs):
        if kick: L.typewriter(c, kick, t, hs, VW / 2, 160, size=36, fill=STEEL, cps=46, anchor="mm", cursor=False)
        if head:
            lines = head if isinstance(head, (list, tuple)) else (head,); a = ease((t - hs) / 0.22)
            ys = (330,) if len(lines) == 1 else (268, 392)
            for ln, y in zip(lines, ys):
                col = RED if ln.startswith("!") else BONE; ln = ln.lstrip("!")
                L.text(c, ln, VW / 2, y + 14 * (1 - a), fit_size(ln, COND, 124, 1000), col, COND, alpha=a)

    def frame(s, t):
        c = Image.new("RGBA", (VW, VH), INK + (255,))
        if t < s.vo_end:
            b = next(x for x in reversed(s.beats) if x["t0"] <= t + 1e-9) if t >= s.beats[0]["t0"] else s.beats[0]
            c.alpha_composite(panel(b, t, b["t0"], b["t1"]), (0, PY))
            d = ImageDraw.Draw(c); d.rectangle((0, PY - 4, VW, PY), fill=RED); d.rectangle((0, PY + PH, VW, PY + PH + 4), fill=RED)
            s.header(c, t, *b["hdr"])
            for s0, s1, txt in s.caps:
                if s0 <= t < s1:
                    sz = fit_size(txt, COND, 88, 990)
                    d.text((VW / 2, 1555), txt, font=font(COND, sz), fill=BONE, anchor="mm", stroke_width=8, stroke_fill=(8, 8, 8)); break
            L.text(c, "the LAST HOURS", VW / 2, 1832, 40, STEEL, COND)
        else:
            s.endcard(c, t - s.vo_end)
        return c

    def endcard(s, c, te):
        L.typewriter(c, "THE FULL FILE", te, 0.0, VW / 2, 215, size=92, cps=18, anchor="mm", cursor=False)
        L.rule(c, VW / 2 - 300, VW / 2 + 300, 290, te, 0.75, width=6)
        key = "endpr_" + s.sid
        if key not in _PR: _PR[key] = L.print_card(L.bw(s.end.get("img", ALC + "B2_fbi_dummy_in_bed.jpg")), s.end.get("w", 720), border=14, rot=-2.0)
        L.drop(c, _PR[key], VW / 2, 690, te, 0.25, dur=0.35, dy=50)
        tlabel(c, s.end.get("label", "ALCATRAZ  ·  JUNE 11, 1962"), VW / 2, 1112, te, 0.7, size=36, fill=STEEL, anchor="mm")
        for i, ln in enumerate(s.end.get("title", ALC_TITLE)):
            L.text(c, ln, VW / 2, 1205 + i * 74, 58, BONE, SER, alpha=ease((te - 1.0) / 0.4))
        a = ease((te - 1.5) / 0.4)
        if a > 0:
            L.text(c, "LINK BELOW", VW / 2, 1430, 76, RED, COND, alpha=a)
            d = ImageDraw.Draw(c); y = 1498 + 10 * math.sin(te * 5); x = VW / 2
            d.polygon([(x - 34, y), (x + 34, y), (x, y + 44)], fill=RED)
        L.text(c, "the LAST HOURS", VW / 2, 1832, 40, STEEL, COND)

# ---------------------------------------------------------------- audio
def duck_gain(vo, SR, under_db=-15.0, gap_db=-10.0, hold=0.30, attack=0.06, release=0.40):
    hop = int(0.01 * SR); nf = len(vo) // hop + 1; v = np.pad(vo, (0, nf * hop - len(vo)))
    rms = np.sqrt(np.mean(v.reshape(nf, hop) ** 2, axis=1)); vr = np.sqrt(np.mean(vo[np.abs(vo) > 1e-3] ** 2) + 1e-12)
    act = rms > 0.1 * vr; h = int(hold / 0.01); act2 = act.copy()
    for i in np.where(act)[0]: act2[i:i + h] = True
    tgt = np.where(act2, under_db, gap_db).astype(np.float32); g = np.empty_like(tgt); cur = gap_db
    ka, kr = 1 - np.exp(-0.01 / attack), 1 - np.exp(-0.01 / release)
    for i, x in enumerate(tgt): cur += (x - cur) * (ka if x < cur else kr); g[i] = cur
    return np.interp(np.arange(len(vo)), np.arange(nf) * hop, g).astype(np.float32)

def dec(path, SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def build_audio(S):
    import soundfile as sf
    SR = 48000; n = int(S.total * SR); voice = np.zeros(n, np.float32)
    vo = dec(S.dir + "vo_chatterbox.wav", SR); voice[:min(n, len(vo))] += vo[:n]
    vr = np.sqrt(np.mean(vo[np.abs(vo) > 1e-3] ** 2) + 1e-12)
    cta = dec(S.cta, SR); cta = cta / (np.sqrt(np.mean(cta[np.abs(cta) > 1e-3] ** 2)) + 1e-12) * vr
    a = int((S.vo_end + 0.5) * SR); voice[a:a + len(cta)] += cta[: max(0, n - a)]
    mf, moff = S.spec.get("music", ("Thunder Dreams.mp3", 0)); mus = dec(MUS + mf, SR)[int(moff * SR):]
    mus = np.tile(mus, int(np.ceil(n / max(1, len(mus)))) + 1)[:n]; mus = mus / (np.sqrt(np.mean(mus ** 2)) + 1e-9) * vr
    g = duck_gain(voice, SR, S.spec.get("under_db", -15.0), S.spec.get("gap_db", -10.0))
    fade = np.ones(n, np.float32); fi, fo = int(0.25 * SR), int(1.2 * SR); fade[:fi] = np.linspace(0.4, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
    out = voice + mus * (10 ** (g / 20)) * fade
    for name, t0, db in sfx_list(S):
        s_ = dec(SFXD + name + ".mp3", SR); s_ = s_[: int(2.5 * SR)]
        if len(s_) == 0: continue
        e = min(len(s_), int(0.08 * SR)); s_[-e:] *= np.linspace(1, 0, e)
        s_ = s_ / (np.sqrt(np.mean(s_[np.abs(s_) > 1e-4] ** 2)) + 1e-9) * vr * 10 ** (db / 20)
        i0 = int(t0 * SR); m = min(len(s_), n - i0)
        if m > 0: out[i0:i0 + m] += s_[:m]
    raw = BUILD + f"{S.sid}_raw.wav"; fin = BUILD + f"{S.sid}.wav"
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.9; sf.write(raw, out, SR, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(raw, fin, target=-14, tp=-1); return fin

def sfx_list(S):
    ev = [("hit_deep_heartbeat_impact", 0.0, -20)]
    for i, b in enumerate(S.beats):
        if i == 0: continue
        t0 = b["t0"]
        if b["kind"] == "doc": ev.append(("paper_page_turn", t0, -22))
        elif b["kind"] == "quote": ev.append(("paper_slide", t0, -22)); ev.append(("typewriter_typing_old", t0 + 0.35, -27))
        elif b["kind"] == "map" and b.get("whoosh", True): ev.append(("whoosh_fast_transition", max(0, t0 - 0.12), -27))
        for ov in b.get("ov", []):
            if ov[0] == "stamp": ev.append(("hit_short_bass", t0 + ov[2], -19))
            if ov[0] == "print": ev.append(("paper_slide", t0 + ov[6], -24))
    ev.append(("hit_cinematic_deep_impact", S.vo_end + 0.05, -17)); ev.append(("typewriter_typing_old", S.vo_end + 0.05, -26))
    ev += [(n, S.LT[l][0] + off, db) for n, l, off, db in S.spec.get("sfx", [])]
    return ev

# ---------------------------------------------------------------- render / qa / words
def render(sid):
    S = Short(sid); wav = build_audio(S); n = int(S.total * FPS); out = OUT + f"TheLastHours_Short_{sid}_{S.spec['slug']}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(n): p.stdin.write(S.frame(f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("wrote", out, round(S.total, 1), "s", flush=True)

def qa(sid, ts):
    S = Short(sid)
    if not ts: ts = [b["t0"] + 0.9 for b in S.beats] + [S.vo_end + 2.5]
    tiles = [S.frame(t).convert("RGB").resize((270, 480)) for t in ts]
    cols = 8; rows = (len(tiles) + cols - 1) // cols; sh = Image.new("RGB", (cols * 280, rows * 500), (30, 30, 30))
    for i, im in enumerate(tiles): sh.paste(im, ((i % cols) * 280, (i // cols) * 500))
    out = BUILD + f"qa_{sid}.png"; sh.save(out); print(out, "vo_end", round(S.vo_end, 2), "beats", [round(b["t0"], 2) for b in S.beats])

def words(sids):
    from faster_whisper import WhisperModel
    m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
    for sid in sids:
        import specs; d = BANK + specs.S[sid]["folder"] + "/" if sid in specs.S else sid
        src = d + "vo_chatterbox.wav" if os.path.isdir(d) else sid
        a, _ = read_mono(src, 16000)
        segs, _ = m.transcribe(a, word_timestamps=True, beam_size=5, condition_on_previous_text=False); res = []
        for sg in segs: res.append({"start": sg.start, "end": sg.end, "text": sg.text, "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in sg.words]})
        json.dump(res, open((d + "vo_words_cb.json") if os.path.isdir(d) else src + ".words.json", "w", encoding="utf-8"), indent=1)
        print("==", sid, " ".join(r["text"].strip() for r in res), flush=True)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "render": [render(x) for x in sys.argv[2:]]
    elif m == "qa": qa(sys.argv[2], [float(x) for x in sys.argv[3:]])
    elif m == "words": words(sys.argv[2:])
