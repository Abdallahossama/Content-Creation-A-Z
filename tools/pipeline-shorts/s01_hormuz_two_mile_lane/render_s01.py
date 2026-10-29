"""Ask Habibi Short #1 "21 Miles Wide, But Ships Only Get 2" (potato-cast map style), 1080x1920, 30 fps, 56.6 s. v2.
v2 (user notes on v1): fixed Ask Habibi logo top-left; no blur/bloom while zooming (6-level map pyramid, coverage
computed from the camera path, levels blended, paper texture fixed in SCREEN space, constant coast halo); the hero
tanker sails ONE continuous route (no jumps) and the "Strait of Hormuz" label sits in open water with an arrow;
more motion for retention (red circle hook, moving lane arrows, wakes, reactions, rolling pump price, quiet pops).
v1 kept as render_s01_v1.py. Modes: build | qa t... | seg i n | audio | final"""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
from mapkit import Map
from potato_cast import cast

ROOT = "D:/why habibi/shorts/s01_hormuz/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
W, H, FPS, KY = 1080, 1920, 30, 1.1
VO = ROOT + "vo/s01_vo.mp3"; DUR = 56.56; NF = int(DUR * FPS) + 1
SERIF = "C:/Windows/Fonts/georgiai.ttf"; SANS = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"
SFXD = "D:/why habibi/_style_kit/sfx/"
OLD = dict(sea_top=(112, 156, 160), sea_bot=(96, 140, 148), shallow=(140, 178, 172), land=(224, 206, 162), border=(140, 112, 76), edge=(110, 86, 56))
FILLS = [("Iran", (178, 72, 54)), ("Oman", (86, 124, 88)), ("United Arab Emirates", (198, 162, 86))]
PYR = [40, 80, 160, 320, 640, 1280]

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def font(p, s): return ImageFont.truetype(p, int(s))
WORDS = [w for seg in json.load(open(B + "vo_words.json", encoding="utf-8")) for w in seg["words"]]
def at(word, n=1):
    k = 0
    for w in WORDS:
        if w["w"].strip(" ,.?!").lower() == word.lower():
            k += 1
            if k == n: return w["s"]
    raise KeyError(word)
T = dict(one=at("one"), lane=at("lane"), hormuz=at("hormuz"), iran=at("iran"), oman=at("oman"), narrowest=at("narrowest"), m21=at("21"),
         plenty=at("plenty"), but2=at("but", 2), they=at("they"), m_in=at("in", 2), m_out=at("out"), gap=at("gap"), y2024=at("2024"),
         barrels=at("barrels", 2), fifth=at("fifth"), shore=at("shore"), thats_iran=at("iran", 2), coast=at("coast"), week=at("week"),
         twelve=at("12"), oil=at("oil", 3), why=at("why"), pump=at("pump"), two_end=at("two", 6))
END = DUR

# ------------------------------------------------------------------ camera
CAM = [  # t, lon, lat, px per degree
    (0.0, 50.6, 24.6, 38), (T["lane"] - 0.2, 56.7, 26.0, 150), (T["narrowest"] - 0.3, 56.5, 26.25, 178),
    (T["narrowest"] + 0.9, 56.38, 26.6, 900), (T["shore"] - 0.4, 56.35, 26.62, 980),
    (T["shore"] + 0.7, 55.9, 26.45, 200), (T["why"] - 0.15, 56.0, 26.45, 232),
    (T["why"] - 0.1, 56.35, 26.6, 900), (T["two_end"] - 0.1, 56.35, 26.6, 900),
    (T["two_end"] + 2.0, 56.3, 26.4, 300), (END - 0.1, 50.6, 24.6, 38), (END + 1, 50.6, 24.6, 38)]
def camera(t):
    for (t0, x0, y0, p0), (t1, x1, y1, p1) in zip(CAM, CAM[1:]):
        if t0 <= t <= t1:
            u = ease((t - t0) / max(t1 - t0, 1e-6)); p = math.exp(math.log(p0) + (math.log(p1) - math.log(p0)) * u)
            v = (p - p0) / (p1 - p0) if abs(p1 - p0) > 1e-6 else u
            dr = 1 + 0.012 * math.sin(t * 0.9)                                   # never fully still: a slow breathe + drift
            return x0 + (x1 - x0) * v + 4 * math.sin(t * 0.7) / p, y0 + (y1 - y0) * v + 3 * math.cos(t * 0.6) / p, p * dr
    return CAM[-1][1:]

def level_for(p):
    for cp in PYR:
        if cp >= p: return cp
    return PYR[-1]

# ------------------------------------------------------------------ map pyramid
def coverage():
    box = {}
    for f in range(NF + 1):
        lon, lat, p = camera(f / FPS); vw, vh = W / p, H / (p * KY)
        lv = level_for(p); lo = [c for c in PYR if c < lv]
        for cp in {lv} | ({lo[-1]} if lo and p < lo[-1] * 1.25 else set()):
            b = box.setdefault(cp, [1e9, -1e9, 1e9, -1e9])
            b[0] = min(b[0], lon - vw * 0.6); b[1] = max(b[1], lon + vw * 0.6); b[2] = min(b[2], lat - vh * 0.6); b[3] = max(b[3], lat + vh * 0.6)
    return box

def build():
    cov = coverage(); json.dump({str(k): v for k, v in cov.items()}, open(B + "levels.json", "w"))
    for cp, (lon0, lon1, lat0, lat1) in sorted(cov.items()):
        w, h = int((lon1 - lon0) * cp), int((lat1 - lat0) * cp * KY)
        m = Map(lon0, lon1, lat0, lat1, w, h, ss=1, halo=9, line=1.6); base = m.render(pal=OLD).convert("RGBA")
        masks = {}
        for name, col in FILLS:
            mk = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mk)
            for n, r, b in m._rings():
                if n == name: d.polygon([m.xy(x, y) for x, y in r], fill=255)
            masks[name] = mk.filter(ImageFilter.GaussianBlur(0.7))
        for si, names in enumerate([[], ["Iran"], ["Iran", "Oman", "United Arab Emirates"]]):
            c = base.copy()
            for name, col in FILLS:
                if name in names:
                    lay = Image.new("RGBA", (w, h), col + (0,)); lay.putalpha(masks[name].point(lambda v: int(v * 0.82))); c.alpha_composite(lay)
                    e = np.asarray(masks[name].filter(ImageFilter.MaxFilter(3)), np.int16) - np.asarray(masks[name], np.int16)
                    ol = Image.new("RGBA", (w, h), (36, 26, 16, 0)); ol.putalpha(Image.fromarray(e.clip(0, 255).astype(np.uint8))); c.alpha_composite(ol)
            c.convert("RGB").save(B + f"pv_{cp}_{si}.png"); print(cp, si, w, h, flush=True)

LV = None; CV = {}
def canvas(cp, si):
    k = (cp, si)
    if k not in CV:
        if len(CV) > 5: CV.pop(next(iter(CV)))
        CV[k] = Image.open(B + f"pv_{cp}_{si}.png").convert("RGB")
    return CV[k]

def crop(cp, si, lon, lat, p):
    global LV
    if LV is None: LV = {int(k): v for k, v in json.load(open(B + "levels.json")).items()}
    lon0, lon1, lat0, lat1 = LV[cp]; vw, vh = W / p, H / (p * KY)
    box = ((lon - vw / 2 - lon0) * cp, (lat1 - lat - vh / 2) * cp * KY, (lon + vw / 2 - lon0) * cp, (lat1 - lat + vh / 2) * cp * KY)
    return canvas(cp, si).resize((W, H), Image.BICUBIC, box=box, reducing_gap=2.0)

def state_at(t):
    if t < T["iran"]: return 0, 0.0
    if t < T["iran"] + 0.35: return 0, (t - T["iran"]) / 0.35
    if t < T["oman"]: return 1, 0.0
    if t < T["oman"] + 0.35: return 1, (t - T["oman"]) / 0.35
    return 2, 0.0

def map_frame(t):
    lon, lat, p = camera(t); cp = level_for(p); lower = [c for c in PYR if c < cp]; s, f = state_at(t)
    def one(cp_):
        img = crop(cp_, s, lon, lat, p)
        if f > 0: img = Image.blend(img, crop(cp_, s + 1, lon, lat, p), f)
        return img
    img = one(cp)
    if lower and p < lower[-1] * 1.25:                                           # just above a level: blend from the lower one, no pop
        wgt = (p - lower[-1]) / (lower[-1] * 0.25); img = Image.blend(one(lower[-1]), img, min(max(wgt, 0), 1))
    return img, (lon, lat, p)

def geo(cam, lon, lat):
    clon, clat, p = cam; return (lon - clon) * p + W / 2, (clat - lat) * p * KY + H / 2

# ------------------------------------------------------------------ screen-space paper + vignette (never zooms)
def paper_tex():
    rng = np.random.default_rng(7); f = rng.normal(0, 1, (H // 2, W // 2))
    fib = np.asarray(Image.fromarray(((f * 22) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    st = rng.normal(0, 1, (9, 6)); st = np.asarray(Image.fromarray(((st * 30) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); v = np.clip(np.hypot((xx - W / 2) / (W * 0.7), (yy - H / 2) / (H * 0.62)) - 0.5, 0, 1)
    return ((1 + fib * 0.0018 + st * 0.0012) * (1 - v * 0.38))[..., None] * np.array([1.0, 0.985, 0.94], np.float32)
PAPER = None
def papered(img):
    global PAPER
    if PAPER is None: PAPER = paper_tex()
    return Image.fromarray((np.asarray(img, np.float32) * PAPER).clip(0, 255).astype(np.uint8)).convert("RGBA")

# ------------------------------------------------------------------ sprites
def tanker(L=260):
    h = int(L * 0.36); im = Image.new("RGBA", (L + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y0 = int(h * 0.48)
    d.polygon([(8, y0), (L, y0), (L - 22, h), (34, h)], fill=(36, 34, 40, 255))
    d.polygon([(14, y0 + (h - y0) * 0.55), (L - 4, y0 + (h - y0) * 0.55), (L - 22, h), (34, h)], fill=(170, 40, 34, 255))
    d.line([(8, y0), (L, y0)], fill=(230, 230, 226, 255), width=3)
    for k in range(6): d.line((28 + k * int(L * 0.1), y0 - 2, 28 + k * int(L * 0.1), y0 - int(L * 0.04)), fill=(120, 120, 126, 255), width=3)
    d.line((22, y0 - int(L * 0.03), L - int(L * 0.3), y0 - int(L * 0.03)), fill=(150, 150, 156, 255), width=3)
    sx = L - int(L * 0.3); d.rectangle((sx, y0 - int(L * 0.17), L - 10, y0), fill=(244, 242, 236, 255), outline=(80, 80, 86, 255), width=2)
    for k in range(4): d.rectangle((sx + 6 + k * int(L * 0.06), y0 - int(L * 0.13), sx + 6 + k * int(L * 0.06) + int(L * 0.035), y0 - int(L * 0.1)), fill=(50, 70, 100, 255))
    d.rectangle((L - int(L * 0.17), y0 - int(L * 0.25), L - int(L * 0.1), y0 - int(L * 0.17)), fill=(230, 80, 40, 255), outline=(60, 30, 20, 255), width=2)
    return im
TANK = tanker(250); TANK_S = tanker(140)
SPR = {}
def sprite(key, *a, **k):
    if key not in SPR: SPR[key] = cast(*a, **k)
    return SPR[key]
def make_logo():
    lg = Image.open("D:/why habibi/_style_kit/brand/logo_horizontal.png").convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((300, int(300 * lg.height / lg.width)), Image.LANCZOS)
    out = Image.new("RGBA", (lg.width + 30, lg.height + 30), (0, 0, 0, 0)); s = Image.new("RGBA", lg.size, (0, 0, 0, 0)); s.putalpha(lg.split()[3].point(lambda v: int(v * 0.45)))
    out.alpha_composite(s, (12, 14)); out = out.filter(ImageFilter.GaussianBlur(6)); out.alpha_composite(lg, (8, 8)); return out
LOGO = make_logo()

POP = [0.0, 0.55, 1.14, 1.05, 0.98, 1.0]
def popk(t, t0):
    f = int((t - t0) * FPS); return 0.0 if f < 0 else (POP[f] if f < len(POP) else 1.0)
def put(c, spr, cx, by, k=1.0, bob=0.0, flip=False):
    if k <= 0.01: return
    s = spr.transpose(Image.FLIP_LEFT_RIGHT) if flip else spr
    if abs(k - 1) > 0.01: s = s.resize((max(1, int(s.width * k)), max(1, int(s.height * k))), Image.BILINEAR)
    c.alpha_composite(s, (int(cx - s.width / 2), int(by - s.height + bob)))
def text(d, xy, s, size, fill=(255, 255, 255), f=SANS, anchor="mm", stroke=6, sfill=(20, 16, 12)):
    d.text(xy, s, font=font(f, size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)
def serif_label(c, s, x, y, size, alpha=1.0, rot=0, col=(246, 238, 218)):
    if alpha <= 0: return
    f = font(SERIF, size); im = Image.new("RGBA", (int(size * len(s) * 0.66) + 60, size + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((im.width / 2 + 2, im.height / 2 + 3), s, font=f, fill=(30, 20, 10, int(140 * alpha)), anchor="mm")
    d.text((im.width / 2, im.height / 2), s, font=f, fill=col + (int(255 * alpha),), anchor="mm")
    im = im.rotate(rot, Image.BICUBIC, expand=True); c.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
LP = {}
def label_pill(s, size, col):
    k = (s, size, col)
    if k not in LP:
        f = font(SANS, size); tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(s, font=f)
        im = Image.new("RGBA", (int(tw) + 60, size + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 18, fill=(24, 18, 12, 205)); d.text((im.width / 2, im.height / 2), s, font=f, fill=col + (255,), anchor="mm")
        LP[k] = im
    return LP[k]
def poly_upto(pts, upto):
    pts = np.asarray(pts, float); L = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    if upto <= 0 or L[-1] == 0: return []
    end = L[-1] * min(upto, 1); out = [tuple(pts[0])]
    for i in range(1, len(pts)):
        if L[i] <= end: out.append(tuple(pts[i]))
        else: f = (end - L[i - 1]) / (L[i] - L[i - 1]); out.append(tuple(pts[i - 1] + (pts[i] - pts[i - 1]) * f)); break
    return out
def along(pts, u):
    pts = np.asarray(pts, float); L = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]; s = L[-1] * min(max(u, 0), 1)
    i = max(min(np.searchsorted(L, s) - 1, len(pts) - 2), 0); f = (s - L[i]) / max(L[i + 1] - L[i], 1e-9)
    return pts[i] + (pts[i + 1] - pts[i]) * f, pts[i + 1] - pts[i]

# ------------------------------------------------------------------ geography (lanes are a DIAGRAM: routes redrawn in 2026)
CENTER = [(55.75, 26.40), (56.10, 26.58), (56.42, 26.66), (56.68, 26.50), (56.82, 26.18), (57.0, 25.82)]
def offset(path, d_deg):
    p = np.asarray(path, float); out = []
    for i in range(len(p)):
        a, b = p[max(i - 1, 0)], p[min(i + 1, len(p) - 1)]; tt = b - a; n = np.array([-tt[1], tt[0]]) / (np.hypot(*tt) + 1e-9); out.append(p[i] + n * d_deg)
    return out
MI = 1 / 69.0
LANE_IN, LANE_OUT = offset(CENTER, +2 * MI), offset(CENTER, -2 * MI)
ROUTE = [(58.55, 24.3), (57.95, 24.55), (57.4, 24.85), (57.05, 25.3), (56.98, 25.6)] + [tuple(q) for q in LANE_IN[::-1]] + [(55.3, 26.22), (54.6, 25.95)]
HERO_U = [(0.0, 0.0), (T["narrowest"], 0.42), (T["they"], 0.50), (T["shore"], 0.62), (END, 0.9)]
def hero_u(t):
    for (a, ua), (b, ub) in zip(HERO_U, HERO_U[1:]):
        if a <= t <= b: return ua + (ub - ua) * (t - a) / (b - a)
    return HERO_U[-1][1]
RULER = [(56.30, 26.52), (56.36, 26.82)]
ISLANDS = [(55.95, 26.80), (56.46, 27.06), (56.36, 26.86), (55.90, 26.64), (55.03, 25.88), (55.30, 26.26), (55.14, 26.24)]

def trail(c, cam, path, u, back=0.05, dy=24, width=7):
    """a soft white wake along the path the ship has just sailed (fades out behind it)"""
    pts = [geo(cam, *along(path, u - back * k / 12)[0]) for k in range(13)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for k in range(12):
        a = int(150 * (1 - k / 12)); (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        dl.line([(x0, y0 + dy), (x1, y1 + dy)], fill=(250, 252, 255, a), width=max(2, int(width * (1 - k / 14))))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.5)))

def lane_band(c, cam, lane, upto, col, t, reverse=False):
    pts = [geo(cam, *q) for q in lane]; drawn = poly_upto(pts, upto)
    if len(drawn) < 2: return
    lw = max(10, int(2 * MI * cam[2] * KY))
    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0)); de = ImageDraw.Draw(edge); de.line(drawn, fill=col + (255,), width=lw + 6, joint="curve")
    de.line(drawn, fill=col + (105,), width=lw - 2, joint="curve"); c.alpha_composite(edge)
    arr = np.asarray(drawn); L = np.r_[0, np.cumsum(np.hypot(*np.diff(arr, axis=0).T))]; d = ImageDraw.Draw(c); step = 70
    for s0 in np.arange((t * 60) % step, L[-1], step):                          # moving arrows = direction of travel
        s = (L[-1] - s0) if reverse else s0; i = max(min(np.searchsorted(L, s) - 1, len(arr) - 2), 0); f = (s - L[i]) / max(L[i + 1] - L[i], 1e-9)
        q = arr[i] + (arr[i + 1] - arr[i]) * f; v = (arr[i + 1] - arr[i]) / (np.hypot(*(arr[i + 1] - arr[i])) + 1e-9) * (-1 if reverse else 1)
        nrm = np.array([-v[1], v[0]]); tip = q + v * 12
        d.polygon([tuple(tip), tuple(q - v * 8 + nrm * 9), tuple(q - v * 8 - nrm * 9)], fill=(255, 255, 255, 230))

# ------------------------------------------------------------------ captions
def chunks():
    out, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w); s = w["w"].strip(); nxt = WORDS[i + 1]["w"].strip() if i + 1 < len(WORDS) else ""
        if nxt.startswith("-"): continue
        if len([x for x in cur if not x["w"].strip().startswith("-")]) >= 4 or s.endswith((",", ".", "?", "!")): out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        t1 = out[i + 1][0]["s"] if i + 1 < len(out) else c[-1]["e"] + 0.4; txt = ""
        for w in c: tok = w["w"].strip(); txt += tok if (tok.startswith("-") or not txt) else " " + tok
        res.append((c[0]["s"], min(t1, c[-1]["e"] + 0.6), txt))
    return res
CAPS = chunks()

# ------------------------------------------------------------------ sound effects (quiet; never whooshes or impacts)
SFX = [("marker_write", 0.15), ("pop", T["one"]), ("pop", T["hormuz"]), ("pop", T["iran"]), ("pop", T["oman"]), ("marker_write", T["narrowest"] + 0.5),
       ("pop", T["plenty"] - 0.2), ("pop", T["but2"]), ("marker_write", T["m_in"] - 0.3), ("marker_write", T["m_out"] - 0.3), ("marker_write", T["gap"] - 0.2),
       ("paper_slide", T["y2024"]), ("pop", T["barrels"] - 0.3), ("pop", T["fifth"] - 0.2), ("highlighter", T["thats_iran"])] + \
      [("pop", T["coast"] + i * 0.28) for i in range(len(ISLANDS))] + [("paper_slide", T["week"] - 0.3)] + \
      [("pop", T["twelve"] + i * 0.12) for i in range(0, 12, 3)] + [("pop", T["oil"] - 0.2), ("pop", T["why"]), ("pop", T["pump"] - 0.2), ("marker_write", T["two_end"])]

# ------------------------------------------------------------------ the frame
PUMP = None
def pump_bg():
    global PUMP
    if PUMP is None:
        im = Image.open("D:/why habibi/4th video/media/photos/pexels-8266768.jpg").convert("RGB"); w, h = im.size
        cw = h * W / H; x0 = (w - cw) * 0.62; im = im.crop((int(x0), 0, int(x0 + cw), h)).resize((W, H), Image.LANCZOS)
        PUMP = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(9))).enhance(0.55)
    return PUMP

def frame(t):
    bob = 0.0                                                                   # user: moving potatoes are annoying -> still
    if T["why"] - 0.15 <= t < T["two_end"] - 0.1:
        zoom = 1 + 0.04 * max(0.0, t - T["why"] + 0.15) / 4; cw, ch = W / zoom, H / zoom
        c = papered(pump_bg().resize((W, H), Image.BICUBIC, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))); cam = None
    else:
        img, cam = map_frame(t); c = papered(img)
    d = ImageDraw.Draw(c)

    if cam:
        lon, lat, p = cam
        # hook: a red marker circle draws round the strait from the first frame; "1 in 5" pops
        if t < T["lane"] + 0.5:
            x, y = geo(cam, 56.45, 26.45); u = ease((t - 0.1) / 0.9); r = 92
            arc = [(x + r * math.cos(a), y + r * 0.86 * math.sin(a)) for a in np.linspace(-2.2, -2.2 + 2 * math.pi * 1.08 * u, 80)]
            if u > 0: d.line(arc, fill=(206, 34, 28, 255), width=11, joint="curve")
        if T["one"] - 0.1 <= t < T["lane"] + 0.6:
            k = popk(t, T["one"] - 0.1); s1 = Image.new("RGBA", (W, 270), (0, 0, 0, 0)); d1 = ImageDraw.Draw(s1)
            text(d1, (W / 2, 96), "1 in 5", 160, fill=(255, 220, 90), f=IMPACT, stroke=10); text(d1, (W / 2, 214), "barrels of oil on Earth", 56)
            put(c, s1, W / 2, 620, k); d = ImageDraw.Draw(c)
        # place names
        if T["hormuz"] - 0.1 <= t < T["narrowest"] - 0.2:
            a = ease((t - T["hormuz"] + 0.1) / 0.4) * (1 - ease((t - T["narrowest"] + 0.6) / 0.4))
            serif_label(c, "Strait of Hormuz", *geo(cam, 55.55, 26.62), 58, a, -4)                    # in the water, west of the narrows
        if T["narrowest"] + 1.0 <= t < T["they"]:
            serif_label(c, "Strait of Hormuz", *geo(cam, 56.05, 26.33), 50, ease((t - T["narrowest"] - 1.0) / 0.4))
        if t >= T["iran"]: serif_label(c, "Iran", *geo(cam, 56.6 if p > 400 else 56.9, 27.25 if p > 400 else 27.9), 84, ease((t - T["iran"]) / 0.35), -6)
        if t >= T["oman"]: serif_label(c, "Oman", *geo(cam, 56.2 if p > 400 else 57.2, 26.1 if p > 400 else 23.6), 66, ease((t - T["oman"]) / 0.35), 4)
        d = ImageDraw.Draw(c)
        # 21-mile ruler
        if T["narrowest"] + 0.5 <= t < T["they"] + 0.4:
            a_, b_ = geo(cam, *RULER[0]), geo(cam, *RULER[1]); u = ease((t - T["narrowest"] - 0.5) / 0.6); seg_ = poly_upto([a_, b_], u)
            if len(seg_) > 1: d.line(seg_, fill=(206, 34, 28, 255), width=11)
            if u > 0.95:
                for e in (a_, b_): d.line((e[0] - 24, e[1], e[0] + 24, e[1]), fill=(206, 34, 28, 255), width=9)
            if t >= T["m21"]: put(c, label_pill("21 miles", 60, (255, 230, 110)), b_[0] + 170, (a_[1] + b_[1]) / 2 + 40, popk(t, T["m21"]))
        # lanes: drawn word by word, then alive with moving arrows
        if t >= T["m_in"] - 0.3:
            lane_band(c, cam, LANE_IN, ease((t - T["m_in"] + 0.3) / 0.8), (255, 206, 60), t, reverse=True)
            if t >= T["m_out"] - 0.3: lane_band(c, cam, LANE_OUT, ease((t - T["m_out"] + 0.3) / 0.8), (255, 140, 60), t)
            if p > 400 and t < T["y2024"]:
                x, y = geo(cam, *LANE_IN[2]); put(c, label_pill("2 mi IN", 40, (255, 214, 80)), x - 10, y - 46, popk(t, T["m_in"]))
                if t >= T["m_out"]: x, y = geo(cam, *LANE_OUT[1]); put(c, label_pill("2 mi OUT", 40, (255, 160, 80)), x - 30, y + 96, popk(t, T["m_out"]))
                if t >= T["gap"]: x, y = geo(cam, *CENTER[3]); put(c, label_pill("2 mi gap", 40, (255, 255, 255)), min(x + 150, 930), y + 30, popk(t, T["gap"]))
            d = ImageDraw.Draw(c)
        # the convoy: ships enter, sail, never wrap around
        def convoy(t0):
            for k, off in enumerate((0.05, 0.2, 0.34, 0.5)):
                lane = LANE_IN[::-1] if k % 2 == 0 else LANE_OUT; u = off + (t - t0) * 0.028
                if u > 1: continue
                q, v = along(lane, u); x, y = geo(cam, *q); vx, vy = v[0], -v[1] * KY
                trail(c, cam, lane, u, back=0.06, dy=16, width=5)
                put(c, TANK_S, x, y + 22, min(1, (t - t0) * 3 + 0.01), flip=vx > 0)
        if T["they"] <= t < T["shore"]: convoy(T["they"])
        if t >= T["two_end"] - 0.1: convoy(T["two_end"] - 3.0)
        # the hero tanker + captain: ONE continuous route through the whole Short
        if not (T["week"] - 0.3 <= t < T["why"]):
            q, v = along(ROUTE, hero_u(t)); x, y = geo(cam, *q); vx, vy = v[0], -v[1] * KY
            if -200 < x < W + 200 and -200 < y < H + 200:
                trail(c, cam, ROUTE, hero_u(t), back=0.035, dy=22, width=8)
                put(c, TANK, x, y + 30)
                face = "shocked" if T["narrowest"] <= t < T["they"] else "panic"
                put(c, sprite("cap_" + face, "russet", face, "suit", "captain", height=96), x + 12, y - 10)       # stands still on the deck
        # host on Musandam: side-eye on "sounds like plenty", shocked on "but tankers don't get 21 miles"
        if T["plenty"] - 0.2 <= t < T["they"] + 0.3:
            x, y = geo(cam, 56.24, 26.12); face = "sideeye" if t < T["but2"] else "shocked"
            put(c, sprite("host_" + face, "russet", face, "suit", height=230), min(max(x, 160), 760), min(y, 1180), popk(t, T["plenty"] - 0.2), bob)
        # 2024: counter, oil worker, 1 in 5
        if T["y2024"] <= t < T["shore"] - 0.2:
            pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle((90, 300, 990, 720), 30, fill=(24, 18, 12, 175)); c.alpha_composite(pan); d = ImageDraw.Draw(c)
            n = int(20_000_000 * ease((t - T["y2024"] - 0.5) / 1.6))
            text(d, (W / 2, 420), f"{n:,}", 124, fill=(255, 220, 90), f=IMPACT, stroke=8); text(d, (W / 2, 538), "barrels of oil a day", 52)
            text(d, (W / 2, 612), "2024 · U.S. EIA", 30, fill=(220, 210, 190), stroke=4)
            if t >= T["fifth"] - 0.2:
                for i in range(5):
                    x = W / 2 - 240 + i * 120; kk = popk(t, T["fifth"] - 0.2 + i * 0.06)
                    if kk > 0: d.rounded_rectangle((x - 34 * kk, 652, x + 34 * kk, 712), 8, fill=(220, 50, 40, 255) if i == 2 else (90, 80, 70, 255), outline=(20, 16, 12, 255), width=3)
                put(c, label_pill("1 in 5", 60, (255, 230, 110)), W / 2, 820, popk(t, T["fifth"]))
            hop = -abs(math.sin((t - T["barrels"]) * 6)) * 20 if 0 < t - T["barrels"] < 1.04 else 0
            put(c, sprite("worker", "red", "panic", "hivis", "hardhat", height=230), 240, 1215, popk(t, T["barrels"] - 0.3), hop)
        # Iran's coast + the islands it holds
        if T["thats_iran"] - 0.2 <= t < T["week"] - 0.3:
            for i, (lo, la) in enumerate(ISLANDS):
                t0 = T["coast"] + i * 0.28
                if t >= t0:
                    x, y = geo(cam, lo, la); k = popk(t, t0); r = 14 + 12 * k
                    d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 236, 120, 255), width=6); d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 236, 120, 255))
            put(c, label_pill("Iran's coast + the islands it holds", 44, (255, 238, 120)), W / 2, 380, popk(t, T["thats_iran"] - 0.2))
        # this week: a tally (NOT positions on the map) + the oil price; no characters here
        if T["week"] - 0.3 <= t < T["why"] - 0.15:
            dim = Image.new("RGBA", (W, H), (10, 8, 6, int(160 * ease((t - T["week"] + 0.3) / 0.4)))); c.alpha_composite(dim); d = ImageDraw.Draw(c)
            put(c, label_pill("THIS WEEK", 54, (255, 255, 255)), W / 2, 360, popk(t, T["week"] - 0.3))
            for i in range(12):
                ti = T["twelve"] + i * 0.12
                if t >= ti:
                    x = 200 + (i % 4) * 228; y = 480 + (i // 4) * 120; k = popk(t, ti); put(c, TANK_S, x, y + 40, k)
                    if k > 0.9: d.line((x - 42, y - 28, x + 42, y + 28), fill=(220, 40, 30, 255), width=11); d.line((x - 42, y + 28, x + 42, y - 28), fill=(220, 40, 30, 255), width=11)
            if t >= T["twelve"]: text(d, (W / 2, 868), "12+ tankers attacked in & around the strait", 40, fill=(255, 224, 206))
            text(d, (W / 2, 920), "The National, 13 Oct 2026", 28, fill=(205, 195, 180), stroke=4)
            if t >= T["oil"] - 0.2:
                from cinekit import price_sign
                if "oil" not in SPR: SPR["oil"] = price_sign("106", label="OIL PER BARREL", h=120)
                put(c, SPR["oil"], W / 2, 1235, popk(t, T["oil"] - 0.2))
    else:
        # the pump: the price rolls from a year ago to now, the host reacts
        from cinekit import price_sign
        u = ease((t - T["why"] - 0.3) / 1.6); val = 3.08 + (4.34 - 3.08) * u; key = f"g{val:.2f}"
        if key not in SPR: SPR[key] = price_sign(f"{val:.2f}", label="REGULAR", h=130)
        put(c, SPR[key], W / 2, 650, popk(t, T["why"]))
        text(d, (W / 2, 708), "a year ago: $3.08   ·   AAA U.S. average, 13 Oct 2026", 32, fill=(232, 222, 206), stroke=4)
        face = "sideeye" if t < T["pump"] - 0.2 else "panic"
        put(c, sprite("hostp_" + face, "russet", face, "suit", height=400), W / 2, 1255, popk(t, T["why"] + 0.2), bob)

    c.alpha_composite(LOGO, (26, 92))                                               # fixed brand logo, top-left
    for t0, t1, s in CAPS:
        if t0 <= t < t1: text(ImageDraw.Draw(c), (W / 2, 1365), s, 60, stroke=7); break
    return c.convert("RGB")

# ------------------------------------------------------------------ modes
def qa(times):
    ims = [frame(float(t)).resize((270, 480), Image.LANCZOS) for t in times]; cols = 6
    sheet = Image.new("RGB", (cols * 280, ((len(ims) + cols - 1) // cols) * 520), (20, 20, 20)); d = ImageDraw.Draw(sheet)
    for i, (im, t) in enumerate(zip(ims, times)):
        x, y = (i % cols) * 280, (i // cols) * 520; sheet.paste(im, (x + 5, y + 5)); d.text((x + 10, y + 490), f"{float(t):.1f}s", fill=(255, 220, 90))
    sheet.save(B + "qa_sheet.png"); print(B + "qa_sheet.png")

def seg(i, n):
    a, b = NF * i // n, NF * (i + 1) // n
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", B + f"seg_{i}.mp4"], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(frame(f / FPS).tobytes())
        if (f - a) % 150 == 0: print(f"seg {i}: {f - a}/{b - a}", flush=True)
    p.stdin.close(); p.wait(); print("seg done", i)

def audio():
    import soundfile as sf
    import audio_master as AM
    SR = 48000
    def dec(path):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).copy()
    vo = dec(VO); n = int((DUR + 0.6) * SR); out = np.zeros(n, np.float32); out[:len(vo)] += vo
    vrms = np.sqrt(np.mean(vo ** 2) + 1e-12)
    mus = dec("D:/why habibi/_music_library/Floating Cities.mp3")[:n]; mus = np.pad(mus, (0, max(0, n - len(mus))))
    fade = np.ones(n, np.float32); fl = int(0.6 * SR); fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
    out += mus * fade * (vrms / (np.sqrt(np.mean(mus ** 2)) + 1e-12)) * 10 ** (-20 / 20)
    for name, t0 in SFX:
        s = dec(SFXD + name + ".wav")[: int(0.9 * SR)]; g = (vrms / (np.sqrt(np.mean(s[np.abs(s) > 1e-4] ** 2)) + 1e-12)) * 10 ** (-17 / 20)
        i0 = int(max(t0, 0) * SR); j = min(n, i0 + len(s)); out[i0:j] += s[: j - i0] * g
    k = 0.89 / max(1e-6, np.abs(out).max()); sf.write(B + "mix_raw.wav", out * k, SR, subtype="FLOAT")
    AM.gain_only(B + "mix_raw.wav", B + "mix.wav", target=-14.0, tp=-1.0)
    AM.master(B + "mix_raw.wav", B + "mix_loud.wav", target=-16.0, tp=-1.0); print("audio", AM.measure(B + "mix.wav"), AM.measure(B + "mix_loud.wav"))

def final():
    with open(B + "segs.txt", "w") as f:
        for i in range(3): f.write(f"file 'seg_{i}.mp4'\n")
    E = ROOT + "export/"; os.makedirs(E, exist_ok=True)
    for wav, name in (("mix.wav", "Ask_Habibi_Short01_Hormuz.mp4"), ("mix_loud.wav", "Ask_Habibi_Short01_Hormuz_LOUDER.mp4")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", E + name], check=True); print(E + name)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "build": build()
    elif m == "qa": qa(sys.argv[2:])
    elif m == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "audio": audio()
    elif m == "final": final()
