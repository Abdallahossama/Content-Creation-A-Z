"""News with Habibi — Short #3 "France's debt" (map style, potato cast in roles), 1080x1920, 30 fps.
Engine = Short #1 v3 rules: logo top-left, map pyramid (no blur), paper in screen space, payoff on frame 1, no idle
bobbing, quiet pops, plain captions. Voice = local Chatterbox clone (vo/s03_vo_chatterbox.wav), timings from vo_words.json.
  build | qa t... | seg i n | audio | final"""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
from mapkit import Map

ROOT = "D:/why habibi/shorts/s03_france_debt/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
W, H, FPS = 1080, 1920, 30; KY = 1 / math.cos(math.radians(46.5))
VO = ROOT + "vo/s03_vo_chatterbox.wav"
SERIF = "C:/Windows/Fonts/georgiai.ttf"; SANS = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"; EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
CAST = "D:/why habibi/_style_kit/brand/potato_cast/"; SFXD = "D:/why habibi/_style_kit/sfx/"
OLD = dict(sea_top=(112, 156, 160), sea_bot=(96, 140, 148), shallow=(140, 178, 172), land=(224, 206, 162), border=(140, 112, 76), edge=(110, 86, 56))
FILLS = [("France", (190, 66, 50)), ("Greece", (60, 104, 176)), ("Italy", (96, 134, 92))]
PYR = [20, 40, 80, 160]
YEL = (255, 206, 60)

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def font(p, s): return ImageFont.truetype(p, int(s))
WORDS = [w for seg in json.load(open(ROOT + "vo/vo_words.json", encoding="utf-8")) for w in seg["words"]]
DUR = WORDS[-1]["e"] + 0.8; NF = int(DUR * FPS) + 1
def at(word, n=1):
    k = 0
    for w in WORDS:
        if w["w"].strip(" ,.?!").lower() == word.lower():
            k += 1
            if k == n: return w["s"]
    raise KeyError(word)
T = dict(debt=at("its"), pct=at("that's", 1), borrow=at("and", 1), problem=at("problem", 2), five=at("5"), highest=at("highest"),
         nextyr=at("next", 2), ninety=at("91"), day=at("that's", 2), govt=at("so", 1), teachers=at("teachers"), students=at("students"),
         oct=at("on"), bankrupt=at("so", 2), no=at("no"), lenders=at("its", 2), loop=at("and", 2))
END = DUR

# ------------------------------------------------------------------ camera (lon, lat, px/deg)
EUROPE = (11.5, 44.6, 30); FRANCE = (2.6, 46.3, 62); PARIS = (2.35, 47.9, 82)
CAM = [(0.0, *EUROPE), (T["debt"] - 0.3, *EUROPE), (T["debt"] + 0.9, *FRANCE), (T["borrow"] - 0.2, 2.5, 46.6, 64), (T["borrow"] + 0.6, *PARIS),
       (T["problem"] - 0.2, 2.35, 47.8, 86), (T["problem"] + 0.6, *FRANCE), (T["oct"] + 3.0, 2.5, 46.6, 66), (T["bankrupt"] - 0.2, 2.6, 46.4, 64),
       (T["loop"] - 0.2, 2.6, 46.4, 62), (T["loop"] + 1.4, *EUROPE), (END + 1, *EUROPE)]
def camera(t):
    for (t0, x0, y0, p0), (t1, x1, y1, p1) in zip(CAM, CAM[1:]):
        if t0 <= t <= t1:
            u = ease((t - t0) / max(t1 - t0, 1e-6)); p = math.exp(math.log(p0) + (math.log(p1) - math.log(p0)) * u)
            v = (p - p0) / (p1 - p0) if abs(p1 - p0) > 1e-6 else u; dr = 1 + 0.012 * math.sin(t * 0.9)
            return x0 + (x1 - x0) * v + 3 * math.sin(t * 0.7) / p, y0 + (y1 - y0) * v + 2 * math.cos(t * 0.6) / p, p * dr
    return CAM[-1][1:]
def level_for(p):
    for cp in PYR:
        if cp >= p: return cp
    return PYR[-1]

def coverage():
    box = {}
    for f in range(NF + 1):
        lon, lat, p = camera(f / FPS); vw, vh = W / p, H / (p * KY); lv = level_for(p); lo = [c for c in PYR if c < lv]
        for cp in {lv} | ({lo[-1]} if lo and p < lo[-1] * 1.25 else set()):
            b = box.setdefault(cp, [1e9, -1e9, 1e9, -1e9])
            b[0] = min(b[0], lon - vw * 0.6); b[1] = max(b[1], lon + vw * 0.6); b[2] = min(b[2], lat - vh * 0.6); b[3] = max(b[3], lat + vh * 0.6)
    return box

def build():
    cov = coverage(); json.dump({str(k): v for k, v in cov.items()}, open(B + "levels.json", "w"))
    for cp, (lon0, lon1, lat0, lat1) in sorted(cov.items()):
        w, h = int((lon1 - lon0) * cp), int((lat1 - lat0) * cp * KY)
        m = Map(lon0, lon1, lat0, lat1, w, h, ss=1, halo=9, line=1.5); c = m.render(pal=OLD).convert("RGBA")
        for name, col in FILLS:
            mk = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mk)
            for n, r, b in m._rings():
                if n == name: d.polygon([m.xy(x, y) for x, y in r], fill=255)
            mk = mk.filter(ImageFilter.GaussianBlur(0.7)); lay = Image.new("RGBA", (w, h), col + (0,)); lay.putalpha(mk.point(lambda v: int(v * 0.74))); c.alpha_composite(lay)
            e = np.asarray(mk.filter(ImageFilter.MaxFilter(3)), np.int16) - np.asarray(mk, np.int16)
            ol = Image.new("RGBA", (w, h), (36, 26, 16, 0)); ol.putalpha(Image.fromarray(e.clip(0, 255).astype(np.uint8))); c.alpha_composite(ol)
        c.convert("RGB").save(B + f"pv_{cp}.png"); print(cp, w, h, flush=True)

LV = None; CV = {}
def crop(cp, lon, lat, p):
    global LV
    if LV is None: LV = {int(k): v for k, v in json.load(open(B + "levels.json")).items()}
    if cp not in CV:
        if len(CV) > 3: CV.pop(next(iter(CV)))
        CV[cp] = Image.open(B + f"pv_{cp}.png").convert("RGB")
    lon0, lon1, lat0, lat1 = LV[cp]; vw, vh = W / p, H / (p * KY)
    box = ((lon - vw / 2 - lon0) * cp, (lat1 - lat - vh / 2) * cp * KY, (lon + vw / 2 - lon0) * cp, (lat1 - lat + vh / 2) * cp * KY)
    return CV[cp].resize((W, H), Image.BICUBIC, box=box, reducing_gap=2.0)
def map_frame(t):
    lon, lat, p = camera(t); cp = level_for(p); lower = [c for c in PYR if c < cp]; img = crop(cp, lon, lat, p)
    if lower and p < lower[-1] * 1.25: img = Image.blend(crop(lower[-1], lon, lat, p), img, min(max((p - lower[-1]) / (lower[-1] * 0.25), 0), 1))
    return img, (lon, lat, p)
def geo(cam, lon, lat): clon, clat, p = cam; return (lon - clon) * p + W / 2, (clat - lat) * p * KY + H / 2

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

# ------------------------------------------------------------------ sprites + text helpers
def cast(name, h):
    im = Image.open(CAST + name + ".png").convert("RGBA"); im = im.crop(im.getbbox()); k = h / im.height
    return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
SPR = {}
def sprite(name, h):
    k = (name, h)
    if k not in SPR: SPR[k] = cast(name, h)
    return SPR[k]
def make_logo():
    lg = Image.open("D:/why habibi/_style_kit/brand/logo_horizontal.png").convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((300, int(300 * lg.height / lg.width)), Image.LANCZOS)
    out = Image.new("RGBA", (lg.width + 30, lg.height + 30), (0, 0, 0, 0)); s = Image.new("RGBA", lg.size, (0, 0, 0, 0)); s.putalpha(lg.split()[3].point(lambda v: int(v * 0.45)))
    out.alpha_composite(s, (12, 14)); out = out.filter(ImageFilter.GaussianBlur(6)); out.alpha_composite(lg, (8, 8)); return out
LOGO = make_logo()
POP = [0.0, 0.55, 1.14, 1.05, 0.98, 1.0]
def popk(t, t0):
    f = int((t - t0) * FPS); return 0.0 if f < 0 else (POP[f] if f < len(POP) else 1.0)
def put(c, spr, cx, cy, k=1.0, anchor="c"):
    if k <= 0.01: return
    s = spr if abs(k - 1) < 0.01 else spr.resize((max(1, int(spr.width * k)), max(1, int(spr.height * k))), Image.BILINEAR)
    y = cy - s.height / 2 if anchor == "c" else cy - s.height
    c.alpha_composite(s, (int(cx - s.width / 2), int(y)))
TX = {}
def outlined(text, size, fill=(255, 255, 255), f=SANS, stroke=9, emoji=None):
    key = (text, size, fill, f, stroke, emoji)
    if key in TX: return TX[key]
    fo = font(f, size); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); bb = d0.textbbox((0, 0), text, font=fo, stroke_width=stroke); ew = 0; em = None
    if emoji:
        em = Image.new("RGBA", (160, 140), (0, 0, 0, 0)); ImageDraw.Draw(em).text((5, 5), emoji, font=font(EMOJI, 109), embedded_color=True)
        em = em.crop(em.getbbox()); k = size * 1.0 / em.height; em = em.resize((int(em.width * k), int(em.height * k)), Image.LANCZOS); ew = em.width + 16
    im = Image.new("RGBA", (bb[2] - bb[0] + ew + 30, max(bb[3] - bb[1], em.height if em else 0) + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((20 - bb[0], 22 - bb[1]), text, font=fo, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4))); d.text((15 - bb[0], 15 - bb[1]), text, font=fo, fill=fill + (255,), stroke_width=stroke, stroke_fill=(12, 10, 10, 255))
    if em: im.alpha_composite(em, (im.width - em.width - 10, (im.height - em.height) // 2))
    TX[key] = im; return im
def pill(text, size, col=(255, 255, 255), bg=(24, 18, 12, 215)):
    key = ("pill", text, size, col)
    if key in TX: return TX[key]
    f = font(SANS, size); tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text, font=f)
    im = Image.new("RGBA", (int(tw) + 60, size + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 18, fill=bg); d.text((im.width / 2, im.height / 2), text, font=f, fill=col + (255,), anchor="mm")
    TX[key] = im; return im
def serif_label(c, s, x, y, size, alpha=1.0, col=(246, 238, 218)):
    if alpha <= 0: return
    f = font(SERIF, size); im = Image.new("RGBA", (int(size * len(s) * 0.66) + 60, size + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((im.width / 2 + 2, im.height / 2 + 3), s, font=f, fill=(30, 20, 10, int(140 * alpha)), anchor="mm"); d.text((im.width / 2, im.height / 2), s, font=f, fill=col + (int(255 * alpha),), anchor="mm")
    c.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
PS = {}
def payslip(stamped):
    if stamped in PS: return PS[stamped]
    im = Image.new("RGBA", (640, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((20, 20, 620, 450), fill=(250, 246, 236, 255), outline=(90, 80, 70, 255), width=3)
    d.text((50, 48), "PAY SLIP · 2027", font=font(SANS, 40), fill=(40, 34, 28)); d.text((50, 100), "Teacher, public school", font=font(SANS, 30), fill=(110, 100, 90))
    for k, (a, b) in enumerate((("Salary", "same as 2026"), ("Raise", "€0"), ("Inflation", "still there"))):
        y = 175 + k * 70; d.line((50, y - 14, 590, y - 14), fill=(210, 200, 185), width=2)
        d.text((50, y), a, font=font(SANS, 34), fill=(60, 52, 44)); d.text((590, y), b, font=font(SANS, 34), fill=(60, 52, 44), anchor="ra")
    if stamped:
        st = Image.new("RGBA", (470, 150), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); red = (200, 30, 30, 235)
        sd.rounded_rectangle((6, 6, 464, 144), 18, outline=red, width=10); sd.text((235, 76), "PAY FROZEN", font=font(IMPACT, 92), fill=red, anchor="mm")
        st = st.rotate(14, expand=True, resample=Image.BICUBIC); im.alpha_composite(st, (im.width // 2 - st.width // 2, 150))
    PS[stamped] = im; return im
def bills(n):
    """a stack of n euro notes (drawn), seen in perspective"""
    im = Image.new("RGBA", (260, 40 + n * 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(n):
        y = im.height - 40 - k * 14; d.rounded_rectangle((10, y, 250, y + 34), 6, fill=(118, 160, 120, 255), outline=(40, 70, 40, 255), width=3)
        d.ellipse((112, y + 6, 148, y + 28), outline=(40, 70, 40, 255), width=3); d.text((30, y + 17), "€", font=font(SANS, 24), fill=(40, 70, 40, 255), anchor="lm")
    return im

# ------------------------------------------------------------------ captions
def chunks():
    out, cur, ws = [], [], []
    for w in WORDS:                                                      # glue "3" ".6", "119" "%", "550" ",000"
        if ws and w["w"].strip()[:1] in ".%," and w["w"].strip()[1:2].isdigit() | (w["w"].strip() == "%"):
            ws[-1] = dict(ws[-1], w=ws[-1]["w"].strip() + w["w"].strip(), e=w["e"])
        else: ws.append(dict(w))
    clause = []
    for w in ws:
        clause.append(w)
        if w["w"].strip().endswith((",", ".", "?", "!")): out.append(clause); clause = []
    if clause: out.append(clause)
    UNIT = ("million", "billion", "trillion", "euros", "euros.", "billion,")
    res0 = []
    for cl in out:                                                       # balanced 1-3 word chunks per clause
        k = math.ceil(len(cl) / 3); sizes = [len(cl) // k + (1 if i >= k - len(cl) % k else 0) for i in range(k)] if len(cl) % k else [len(cl) // k] * k
        i = 0; parts = []
        for n in sizes: parts.append(cl[i:i + n]); i += n
        for j in range(len(parts) - 1):                                  # never split "340 | billion"
            if parts[j][-1]["w"].strip()[:1].isdigit() and parts[j + 1][0]["w"].strip().lower() in UNIT:
                parts[j + 1].insert(0, parts[j].pop())
        res0 += [p for p in parts if p]
    out = res0
    res = []
    for i, c in enumerate(out):
        t1 = out[i + 1][0]["s"] if i + 1 < len(out) else c[-1]["e"] + 0.5
        txt = ""
        for w in c:
            s = w["w"].strip()
            txt += s if (txt and s[:1] in ".%,") else (" " + s if txt else s)
        txt = txt.replace("savings in new", "savings and new").replace("in new taxes", "and new taxes")
        res.append((c[0]["s"] - 0.05, min(t1, c[-1]["e"] + 0.5), txt.strip(",. ")))
    return res
CAPS = chunks()

CITIES = [(-1.55, 47.22), (4.84, 45.76), (5.37, 43.30), (1.44, 43.60), (-0.58, 44.84), (7.75, 48.57), (3.06, 50.63)]   # Nantes Lyon Marseille Toulouse Bordeaux Strasbourg Lille
PARIS_LL = (2.35, 48.86)

def frame(t):
    img, cam = map_frame(t); c = papered(img); d = ImageDraw.Draw(c); lon, lat, p = cam
    # names on the Europe view
    if p < 40:
        for nm, ll, sz in (("France", (2.2, 46.4), 46), ("Greece", (22.0, 39.6), 36), ("Italy", (12.6, 42.8), 36), ("Spain", (-3.8, 40.0), 32), ("UK", (-1.8, 52.8), 30)):
            serif_label(c, nm, *geo(cam, *ll), sz)
    # B1: frame-1 payoff: who pays more to borrow (and the loop at the end)
    if t < T["debt"] - 0.1 or t >= T["loop"]:
        t0 = 0.0 if t < T["debt"] else T["loop"]; k0 = (lambda d: 1.0) if t0 == 0 else (lambda d: popk(t, t0 + d))
        put(c, outlined("IS FRANCE BROKE?", 96, emoji="🤔"), W / 2, 330)
        fx, fy = geo(cam, 2.4, 46.6); gx, gy = geo(cam, 22.3, 39.0)
        put(c, pill("FRANCE PAYS ~5%", 46, (255, 225, 120), (150, 40, 30, 235)), max(fx, 250), min(fy + 95, 1180), k0(0.2))
        put(c, pill("GREECE PAYS LESS", 40, (230, 240, 255), (40, 70, 130, 235)), min(gx, 830), min(gy + 85, 1265), k0(0.5))
    # B2: the debt counter, then 119%
    if T["debt"] <= t < T["borrow"] - 0.1:
        pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle((70, 290, 1010, 700), 32, fill=(22, 16, 12, 185)); c.alpha_composite(pan); d = ImageDraw.Draw(c)
        n = 3.6e12 * ease((t - T["debt"] - 0.3) / 2.0)
        d.text((W / 2, 410), f"€{int(n):,}", font=font(IMPACT, 96), fill=YEL, anchor="mm", stroke_width=7, stroke_fill=(12, 10, 10))
        d.text((W / 2, 520), "public debt, mid-2026 · INSEE", font=font(SANS, 34), fill=(235, 225, 210), anchor="mm", stroke_width=4, stroke_fill=(12, 10, 10))
        if t >= T["pct"]:
            u = ease((t - T["pct"]) / 1.4); x0, x1, y = 160, 920, 615; full = x0 + (x1 - x0) / 1.19
            d.rounded_rectangle((x0, y - 22, x1, y + 22), 22, fill=(70, 60, 50, 255))
            d.rounded_rectangle((x0, y - 22, x0 + (x1 - x0) * u, y + 22), 22, fill=(205, 70, 50, 255))
            d.line((full, y - 40, full, y + 40), fill=(255, 255, 255), width=5); d.text((full, y - 58), "100%", font=font(SANS, 28), fill=(255, 255, 255), anchor="mm")
            put(c, outlined("119% OF GDP", 64, fill=YEL), W / 2, 760, popk(t, T["pct"] + 0.4))
    # B3: next year's borrowing, a growing stack over Paris
    if T["borrow"] <= t < T["problem"] - 0.1:
        px, py = geo(cam, *PARIS_LL); n = 3 + int(14 * ease((t - T["borrow"] - 0.3) / 2.5))
        d.ellipse((px - 12, py - 12, px + 12, py + 12), fill=(30, 20, 10), outline=(255, 255, 255), width=4); serif_label(c, "Paris", px + 90, py + 40, 44)
        put(c, bills(n), px, py - 30, 1.7, anchor="b")
        put(c, outlined("+ €340 BILLION", 90, fill=YEL, f=IMPACT, stroke=8), W / 2, 380, popk(t, T["borrow"] + 0.6))
        put(c, pill("to borrow in 2027", 40), W / 2, 485, popk(t, T["borrow"] + 0.8))
    # B4: the lender wants 5%; the line jumps
    if T["problem"] <= t < T["nextyr"] - 0.1:
        pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle((70, 300, 1010, 760), 32, fill=(22, 16, 12, 185)); c.alpha_composite(pan); d = ImageDraw.Draw(c)
        xs = np.linspace(130, 950, 26); base = 680; ys = [base - 40 - 30 * math.sin(i / 3) - (i / 25) ** 3 * 0 for i in range(26)]
        up = ease((t - T["five"]) / 1.0) if t >= T["five"] else 0.0
        pts = [(x, y - (250 * up * ((i - 18) / 7) ** 2 if i > 18 else 0)) for i, (x, y) in enumerate(zip(xs, ys))]
        d.line(pts, fill=(255, 120, 90), width=8, joint="curve"); d.text((130, 330), "France 10-year borrowing rate", font=font(SANS, 34), fill=(235, 225, 210))
        d.text((130, 705), "2002", font=font(SANS, 28), fill=(200, 190, 175)); d.text((950, 705), "2026", font=font(SANS, 28), fill=(200, 190, 175), anchor="ra")
        if t >= T["five"]: put(c, outlined("5%", 150, fill=YEL, f=IMPACT, stroke=9), 860, 420, popk(t, T["five"]))
        if t >= T["highest"]: put(c, pill("highest since 2002", 44, (255, 225, 120)), W / 2, 830, popk(t, T["highest"]))
        put(c, sprite("diplomat", 330), 230, 1250, popk(t, T["problem"] + 0.2), anchor="b")
        put(c, pill("the lenders", 34), 230, 1290, popk(t, T["problem"] + 0.3))
    # B5: the interest bill
    if T["nextyr"] <= t < T["govt"] - 0.1:
        if t < T["day"] + 1.1:                                               # interest bill bars: 2026 vs 2027 (budget)
            kp = popk(t, T["nextyr"] + 0.2); pan = Image.new("RGBA", (740, 470), (0, 0, 0, 0)); pd = ImageDraw.Draw(pan)
            pd.rounded_rectangle((0, 0, 739, 469), 30, fill=(22, 16, 12, 215)); pd.text((370, 46), "France's yearly interest bill", font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
            for k, (yr, v, col, t0) in enumerate((("2026", 79.2, (205, 160, 120), T["nextyr"] + 0.4), ("2027", 91.2, (220, 70, 50), T["nextyr"] + 1.0))):
                u = ease((t - t0) / 1.1); h = 290 * v / 91.2 * u; x = 170 + k * 260
                pd.rectangle((x, 410 - h, x + 140, 410), fill=col + (255,)); pd.text((x + 70, 440), yr, font=font(SANS, 34), fill=(235, 225, 210), anchor="mm")
                if u > 0.05: pd.text((x + 70, 410 - h - 28), f"€{v * u:.0f}bn", font=font(SANS, 38), fill=(255, 255, 255), anchor="mm")
            put(c, pan, W / 2, 940, kp)
        put(c, outlined("€91 BILLION", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 400, popk(t, T["ninety"]))
        put(c, pill("interest in 2027 · French government", 36), W / 2, 505, popk(t, T["ninety"] + 0.2))
        if t >= T["day"]: put(c, outlined("≈ €250 MILLION A DAY", 72, fill=(255, 255, 255)), W / 2, 640, popk(t, T["day"]))
        if t >= T["day"] + 1.2:
            k = popk(t, T["day"] + 1.2); bx = Image.new("RGBA", (900, 230), (0, 0, 0, 0)); bd = ImageDraw.Draw(bx)
            bd.rounded_rectangle((0, 0, 899, 229), 30, fill=(22, 16, 12, 225), outline=(255, 206, 60, 255), width=4)
            bd.text((450, 52), "France's interest bill since you", font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
            bd.text((450, 95), "started watching this video:", font=font(SANS, 36), fill=(235, 225, 210), anchor="mm")
            bd.text((450, 168), f"€{int(t * 91.2e9 / (365 * 86400)):,}", font=font(IMPACT, 92), fill=YEL, anchor="mm")
            put(c, bx, W / 2, 900, k)
    # B6: the budget: 54bn, teachers' pay frozen
    if T["govt"] <= t < T["students"] - 0.1:
        put(c, outlined("€54 BILLION", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 400, popk(t, T["govt"] + 0.4))
        put(c, pill("savings + new taxes in the 2027 budget", 36), W / 2, 505, popk(t, T["govt"] + 0.6))
        if t >= T["govt"] + 2.4: put(c, payslip(t >= T["teachers"] - 0.3), W / 2, 900, popk(t, T["govt"] + 2.4))
    # B7: students walk toward Paris (blank signs, no slogans, no clashes)
    if T["students"] <= t < T["bankrupt"] - 0.1:
        px, py = geo(cam, *PARIS_LL); u = ease((t - T["students"]) / (T["bankrupt"] - T["students"]))
        for k, (clo, cla) in enumerate(CITIES):
            sx, sy = geo(cam, clo, cla); x = sx + (px - sx) * u * 0.75; y = sy + (py - sy) * u * 0.75
            name = ("student", "student", "viewer", "student", "viewer", "student", "student")[k]
            spr = sprite(name, 150); s2 = spr.transpose(Image.FLIP_LEFT_RIGHT) if x > px else spr
            sg = Image.new("RGBA", (70, 90), (0, 0, 0, 0)); ImageDraw.Draw(sg).rectangle((5, 0, 65, 40), fill=(250, 248, 240, 255), outline=(60, 50, 40, 255), width=3)
            ImageDraw.Draw(sg).line((35, 40, 35, 90), fill=(90, 70, 50, 255), width=5)
            put(c, sg, x + 30, y - 120, popk(t, T["students"] + k * 0.1), anchor="b"); put(c, s2, x, y, popk(t, T["students"] + k * 0.1), anchor="b")
        if t >= T["oct"]:
            put(c, outlined("550,000", 150, fill=YEL, f=IMPACT, stroke=9), W / 2, 380, popk(t, T["oct"] + 0.5))
            put(c, pill("marched on 17 Oct · French authorities", 36), W / 2, 490, popk(t, T["oct"] + 0.7))
    # B8: going bankrupt? no
    if T["bankrupt"] <= t < T["loop"] - 0.1:
        put(c, outlined("GOING BANKRUPT?", 92), W / 2, 380, popk(t, T["bankrupt"]))
        if t >= T["no"]: put(c, outlined("NO.", 180, fill=YEL, f=IMPACT, stroke=10), W / 2, 540, popk(t, T["no"]))
        if T["no"] + 0.6 <= t < T["lenders"]: put(c, pill("it can still borrow", 48, (255, 225, 120)), W / 2, 700, popk(t, T["no"] + 0.6))
        if t >= T["lenders"]: put(c, pill("lenders just want to be paid more", 44, (255, 225, 120)), W / 2, 700, popk(t, T["lenders"]))
        put(c, sprite("diplomat", 380), W / 2, 1290, popk(t, T["no"] + 0.6), anchor="b")
    c.alpha_composite(LOGO, (26, 92))
    for t0, t1, s in CAPS:
        if t0 <= t < t1: put(c, outlined(s, 76, stroke=8), W / 2, 1400); break
    return c.convert("RGB")

SFX = [("pop", 0.2, -18), ("pop", 0.5, -20), ("pop", T["pct"] + 0.4, -18), ("pop", T["borrow"] + 0.6, -18), ("pop", T["five"], -16), ("pop", T["highest"], -20),
       ("cash_register", T["ninety"], -20), ("pop", T["day"], -20), ("pop", T["govt"] + 0.4, -18), ("pop", T["teachers"] - 0.4, -18),
       ("pop", T["oct"] + 0.5, -18), ("pop", T["bankrupt"], -18), ("pop", T["no"], -16), ("pop", T["lenders"], -20)]

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
    for f in range(a, b): p.stdin.write(frame(f / FPS).tobytes())
    p.stdin.close(); p.wait(); print("seg done", i)
def audio():
    import soundfile as sf
    import audio_master as AM
    SR = 48000
    def dec(path):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).copy()
    vo = dec(VO); n = int((DUR + 0.3) * SR); out = np.zeros(n, np.float32); out[:min(n, len(vo))] += vo[:n]
    vrms = np.sqrt(np.mean(vo[np.abs(vo) > 1e-3] ** 2) + 1e-12)
    mus = dec("D:/why habibi/_music_library/Stay the Course.mp3")[:n]; mus = np.pad(mus, (0, max(0, n - len(mus))))
    fade = np.ones(n, np.float32); fl = int(0.6 * SR); fade[:fl] = np.linspace(0.3, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
    out += mus * fade * (vrms / (np.sqrt(np.mean(mus ** 2)) + 1e-12)) * 10 ** (-21 / 20)
    for name, t0, db in SFX:
        s = dec(SFXD + name + ".wav")[: int(1.0 * SR)]; srms = np.sqrt(np.mean(s[np.abs(s) > 1e-4] ** 2)) + 1e-12
        i0 = int(max(t0, 0) * SR); j = min(n, i0 + len(s)); out[i0:j] += s[: j - i0] * (vrms / srms) * 10 ** (db / 20)
    k = 0.89 / max(1e-6, np.abs(out).max()); sf.write(B + "mix_raw.wav", out * k, SR, subtype="FLOAT")
    AM.master(B + "mix_raw.wav", B + "mix.wav", target=-16.0, tp=-1.0); print("audio", AM.measure(B + "mix.wav"))
def final():
    with open(B + "segs.txt", "w") as f:
        for i in range(3): f.write(f"file 'seg_{i}.mp4'\n")
    E = ROOT + "export/"; os.makedirs(E, exist_ok=True); out = E + "Ask_Habibi_Short03_FranceDebt.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "build": build()
    elif m == "qa": qa(sys.argv[2:])
    elif m == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "audio": audio()
    elif m == "final": final()
