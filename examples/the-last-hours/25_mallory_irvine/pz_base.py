"""The Last Hours #25 Mallory & Irvine - base: timing, assets, text helpers. Look: light explainer (grid paper, red/yellow word labels,
cream chapter cards, archive photos with slow push-ins), 1920x1080/30."""
import sys, os, re, glob, math
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, "D:/why habibi/_arabic_docs/_tools")
import akit as K
K.ar = lambda s: s                                    # English text: no reshaping
from akit import W, H, FPS, INK, RED, YEL, TEAL, PAPER, ease, eout, clamp01
Image.MAX_IMAGE_PIXELS = None
ROOT = "D:/why habibi/_newchannel/25_mallory_irvine/"; M = ROOT + "media/"; B = ROOT + "build/"
LEAD, TAIL = 0.6, 4.0
GREY = (150, 150, 146); LGREY = (205, 204, 198); GREEN = (96, 160, 80); DRED = (150, 24, 30)
FONTS = {"bold": "C:/Windows/Fonts/segoeuib.ttf", "black": "C:/Windows/Fonts/seguibl.ttf", "reg": "C:/Windows/Fonts/segoeui.ttf",
         "mono": "C:/Windows/Fonts/consolab.ttf", "serif": "C:/Windows/Fonts/georgiab.ttf"}
_F = {}
def F(kind, size):
    k = (kind, size)
    if k not in _F: _F[k] = ImageFont.truetype(FONTS[kind], size)
    return _F[k]

# ---------------------------------------------------------------- narration timing: exact-zero gaps between lines
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
_vo, VSR = sf.read(ROOT + "vo/mi_vo.wav", dtype="float32")
if _vo.ndim > 1: _vo = _vo.mean(1)
_z = np.concatenate([[False], _vo == 0.0, [False]]).astype(np.int8); _d = np.diff(_z)
GAPS = [(a, b) for a, b in zip(np.where(_d == 1)[0], np.where(_d == -1)[0]) if b - a >= int(0.3 * VSR)]
assert len(GAPS) == len(LINES), (len(GAPS), len(LINES))
T = [LEAD + (0 if i == 0 else GAPS[i - 1][1]) / VSR for i in range(len(LINES))]
LE = [LEAD + g[0] / VSR for g in GAPS]
VO_END = LEAD + len(_vo) / VSR; DUR = VO_END + TAIL; NF = int(DUR * FPS); del _vo, _z, _d

def AT(key):
    """a time: int line, float seconds, (line, seconds) or (line, 'word') = where the word sits in the line (character share)"""
    if isinstance(key, int): return T[key]
    if isinstance(key, float): return key
    ln, w = key
    if isinstance(w, (int, float)): return T[ln] + w
    s = LINES[ln].lower(); i = s.find(w.lower()); span = LE[ln] - T[ln]
    return T[ln] + (0.0 if i < 0 else span * i / max(len(s), 1)) - 0.05

# ---------------------------------------------------------------- assets
IMG = {}
def P(rid):
    f = sorted(glob.glob(M + rid + "_*")); return f[0] if f else None
def pic(rid, crop=None, bw=False):
    k = (rid, crop, bw)
    if k not in IMG:
        im = Image.open(P(rid)).convert("RGB")
        if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
        if max(im.size) > 3000: s = 3000 / max(im.size); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        a = np.asarray(im, np.float32) / 255
        if bw: a = np.repeat(a.mean(2, keepdims=True), 3, 2) * np.array([1.0, 0.99, 0.96], np.float32)
        a = np.clip((a - 0.5) * 1.08 + 0.5, 0, 1); IMG[k] = Image.fromarray((a * 255).astype(np.uint8))
    return IMG[k]
CREDIT = {}
for l in open(M + "credits.tsv", encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) >= 3: CREDIT[p[0]] = p
def credit_line(c, rid):
    p = CREDIT.get(rid)
    if not p: return
    lic = "Public domain" if p[2] in ("Public domain", "No restrictions") else p[2]
    who = re.sub(r"\s+", " ", p[3]).strip()[:44]; s = f"{who} · {lic}" if who and lic != "Public domain" else lic
    if rid in ("B10", "B11", "B21"): s = "NASA · Public domain"
    ImageDraw.Draw(c).text((W - 24, H - 18), s, font=F("bold", 18), fill=(236, 236, 236), anchor="rs", stroke_width=2, stroke_fill=(30, 30, 30))

# ---------------------------------------------------------------- text + labels
def ttext(c, s, x, y, size=84, fill=INK, kind="black", anchor="mm", alpha=1.0):
    K.text(c, s, x, y, F(kind, size), fill, anchor, alpha)
LBL = {}
def lab(s, size=60, style="red"):
    k = (s, size, style)
    if k not in LBL:
        bg, fg = {"red": (RED, (255, 255, 255)), "yel": (YEL, INK), "ink": (INK, (255, 255, 255))}[style]
        f = F("black", size); d = ImageDraw.Draw(Image.new("L", (1, 1))); b = d.textbbox((0, 0), s, font=f, anchor="mm")
        w, h = b[2] - b[0] + 44, int(size * 1.32) + 8; im = Image.new("RGBA", (w, h), bg + (255,))
        ImageDraw.Draw(im).text((w / 2, h / 2), s, font=f, fill=fg, anchor="mm"); LBL[k] = im
    return LBL[k]
def put_labels(c, t, labels, t_end):
    """labels: (text, style, x, y, at[, size])"""
    for L in labels:
        s, st, x, y, at = L[:5]; size = L[5] if len(L) > 5 else (62 if st == "red" else 44)
        K.pop(c, lab(s, size, st), x, y, t, AT(at), t1=t_end - 0.25)
