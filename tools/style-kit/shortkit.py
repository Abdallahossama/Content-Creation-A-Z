"""shortkit: the Ask Habibi map-Short engine (from Short #1 v3 / Short #3), reusable for every "Habibi Explains the News" Short.
Rules baked in: logo top-left, map pyramid (no blur on zoom), paper texture in screen space, payoff on frame 1, no idle bobbing,
quiet pops, balanced 1-3 word captions at y=1400, VO decoded as float, music -21 dB, master -16 LUFS (limiter).

    import shortkit as K
    K.setup(root=".../shorts/s04_x/", vo="vo/s04_vo_chatterbox.wav", lat_mid=54, pyr=[10, 20, 40, 80],
            fills=[("Canada", (200, 60, 50))], polys=[("Alberta", [(lon, lat), ...], (200, 60, 50))],
            music="Stay the Course.mp3", out="Ask_Habibi_Short04_X.mp4")
    T = dict(a=K.at("word"), ...);  K.set_camera([(t, lon, lat, px_per_deg), ...])
    def overlay(c, t, cam): ...   # draw the beats with K.put / K.outlined / K.pill / K.serif_label / K.geo
    K.main(sys.argv, overlay, sfx=[("pop", t, -18), ...])     # build | qa t.. | seg i n | audio | final | all
"""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mapkit import Map

W, H, FPS = 1080, 1920, 30
KIT = "D:/why habibi/_style_kit/"
SERIF = "C:/Windows/Fonts/georgiai.ttf"; SANS = KIT + "fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"; EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
CAST = KIT + "brand/potato_cast/"; SFXD = KIT + "sfx/"; MUSIC = "D:/why habibi/_music_library/"
OLD = dict(sea_top=(112, 156, 160), sea_bot=(96, 140, 148), shallow=(140, 178, 172), land=(224, 206, 162), border=(140, 112, 76), edge=(110, 86, 56))
YEL = (255, 206, 60)
CFG = {}; WORDS = []; DUR = 0.0; NF = 0; KY = 1.0; CAM = []; PYR = []

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def font(p, s): return ImageFont.truetype(p, int(s))

def setup(root, vo, lat_mid=45, pyr=(40,), fills=(), polys=(), music="Stay the Course.mp3", out="short.mp4", cap_fix=(), fill_alpha=0.74, tail=0.8, frames=None,
          size=(1080, 1920), cap_y=None, cap_size=76):
    """music: one file name, or a list of (file, start_seconds) segments crossfaded into one bed (long videos)"""
    global WORDS, DUR, NF, KY, PYR, W, H, PAPER, LOGO
    W, H = size; PAPER = None; LOGO = None
    CFG.update(cap_y=cap_y if cap_y is not None else (1400 if H > W else H - 150), cap_size=cap_size)
    CFG.update(root=root, B=root + "build/", vo=root + vo, frames=frames, fills=list(fills), polys=list(polys), music=music, out=out, cap_fix=list(cap_fix), fill_alpha=fill_alpha)
    os.makedirs(CFG["B"], exist_ok=True)
    WORDS = [w for seg in json.load(open(root + "vo/vo_words.json", encoding="utf-8")) for w in seg["words"]]
    DUR = WORDS[-1]["e"] + tail; NF = int(DUR * FPS) + 1; KY = 1 / math.cos(math.radians(lat_mid)); PYR = list(pyr)

def at(word, n=1):
    k = 0
    for w in WORDS:
        if w["w"].strip(" ,.?!").lower() == word.lower():
            k += 1
            if k == n: return w["s"]
    raise KeyError(f"{word} #{n}")

# ------------------------------------------------------------------ camera (lon, lat, px/deg) + map pyramid
def set_camera(keys):
    CAM[:] = keys
def camera(t):
    for (t0, x0, y0, p0), (t1, x1, y1, p1) in zip(CAM, CAM[1:]):
        if t0 <= t <= t1:
            u = ease((t - t0) / max(t1 - t0, 1e-6)); p = math.exp(math.log(p0) + (math.log(p1) - math.log(p0)) * u)
            v = (p - p0) / (p1 - p0) if abs(p1 - p0) > 1e-6 else u; dr = 1 + 0.012 * math.sin(t * 0.9)
            return x0 + (x1 - x0) * v + 3 * math.sin(t * 0.7) / p, y0 + (y1 - y0) * v + 2 * math.cos(t * 0.6) / p, p * dr
    return CAM[-1][1:] if t > CAM[-1][0] else CAM[0][1:]
def level_for(p):
    for cp in PYR:
        if cp >= p: return cp
    return PYR[-1]
def coverage(max_px=9000):
    """per pyramid level, a list of map tiles (lon0, lon1, lat0, lat1) covering every frame's view; a tile grows along the
    camera path and a new one starts when it would pass max_px (world-hopping long videos)"""
    box = {}
    for f in range(NF + 1):
        lon, lat, p = camera(f / FPS); vw, vh = W / p, H / (p * KY); lv = level_for(p); lo = [c for c in PYR if c < lv]
        for cp in {lv} | ({lo[-1]} if lo and p < lo[-1] * 1.25 else set()):
            r = [lon - vw * 0.6, lon + vw * 0.6, lat - vh * 0.6, lat + vh * 0.6]; tiles = box.setdefault(cp, [])
            for b in reversed(tiles):
                u = [min(b[0], r[0]), max(b[1], r[1]), min(b[2], r[2]), max(b[3], r[3])]
                if (u[1] - u[0]) * cp <= max_px and (u[3] - u[2]) * cp * KY <= max_px: b[:] = u; break
            else: tiles.append(r)
    return box

def _fill(c, mk, col, alpha):
    mk = mk.filter(ImageFilter.GaussianBlur(0.7)); lay = Image.new("RGBA", c.size, col + (0,)); lay.putalpha(mk.point(lambda v: int(v * alpha))); c.alpha_composite(lay)
    e = np.asarray(mk.filter(ImageFilter.MaxFilter(3)), np.int16) - np.asarray(mk, np.int16)
    ol = Image.new("RGBA", c.size, (36, 26, 16, 0)); ol.putalpha(Image.fromarray(e.clip(0, 255).astype(np.uint8))); c.alpha_composite(ol)

def build():
    if CFG.get("bgfn"): print("no map to build (bgfn)"); return
    B = CFG["B"]; cov = coverage(); json.dump({str(k): v for k, v in cov.items()}, open(B + "levels.json", "w"))
    for cp, ti, (lon0, lon1, lat0, lat1) in sorted((cp, i, b) for cp, bs in cov.items() for i, b in enumerate(bs)):
        w, h = int((lon1 - lon0) * cp), int((lat1 - lat0) * cp * KY)
        m = Map(lon0, lon1, lat0, lat1, w, h, ss=1, halo=9, line=1.5); c = m.render(pal=OLD).convert("RGBA")
        for name, col in CFG["fills"]:
            mk = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mk)
            for n, r, b in m._rings():
                if n == name: d.polygon([m.xy(x, y) for x, y in r], fill=255)
            _fill(c, mk, col, CFG["fill_alpha"])
        land = None
        for name, ring, col in CFG["polys"]:                     # custom regions (provinces/states), clipped to land
            if land is None:
                land = Image.new("L", (w, h), 0); dl = ImageDraw.Draw(land)
                for n, r, b in m._rings(): dl.polygon([m.xy(x, y) for x, y in r], fill=255)
            mk = Image.new("L", (w, h), 0); ImageDraw.Draw(mk).polygon([m.xy(x, y) for x, y in ring], fill=255)
            mk = Image.fromarray(np.minimum(np.asarray(mk), np.asarray(land)))
            _fill(c, mk, col, CFG["fill_alpha"] + 0.1)
        c.convert("RGB").save(B + f"pv_{cp}_{ti}.png"); print("level", cp, "tile", ti, w, h, flush=True)

LV = None; CV = {}
def crop(cp, lon, lat, p):
    global LV
    if LV is None:
        LV = {int(k): (v if isinstance(v[0], list) else [v]) for k, v in json.load(open(CFG["B"] + "levels.json")).items()}
    vw, vh = W / p, H / (p * KY); x0, x1, y0, y1 = lon - vw / 2, lon + vw / 2, lat - vh / 2, lat + vh / 2
    ov = lambda b: max(0, min(b[1], x1) - max(b[0], x0)) * max(0, min(b[3], y1) - max(b[2], y0))
    ti = max(range(len(LV[cp])), key=lambda i: ov(LV[cp][i]))                       # the tile that holds this view
    if (cp, ti) not in CV:
        if len(CV) > 2: CV.pop(next(iter(CV)))                                      # big tiles: keep RAM per process low
        CV[(cp, ti)] = Image.open(CFG["B"] + f"pv_{cp}_{ti}.png").convert("RGB")
    lon0, lon1, lat0, lat1 = LV[cp][ti]
    box = ((lon - vw / 2 - lon0) * cp, (lat1 - lat - vh / 2) * cp * KY, (lon + vw / 2 - lon0) * cp, (lat1 - lat + vh / 2) * cp * KY)
    return CV[(cp, ti)].resize((W, H), Image.BICUBIC, box=box, reducing_gap=2.0)
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
SPR = {}
def sprite(name, h, flip=False):
    k = (name, h, flip)
    if k not in SPR:
        im = Image.open(CAST + name + ".png").convert("RGBA"); im = im.crop(im.getbbox()); s = h / im.height
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS); SPR[k] = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
    return SPR[k]
def make_logo():
    lg = Image.open(KIT + "brand/logo_horizontal.png").convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((300, int(300 * lg.height / lg.width)), Image.LANCZOS)
    out = Image.new("RGBA", (lg.width + 30, lg.height + 30), (0, 0, 0, 0)); s = Image.new("RGBA", lg.size, (0, 0, 0, 0)); s.putalpha(lg.split()[3].point(lambda v: int(v * 0.45)))
    out.alpha_composite(s, (12, 14)); out = out.filter(ImageFilter.GaussianBlur(6)); out.alpha_composite(lg, (8, 8)); return out
LOGO = None
POP = [0.0, 0.55, 1.14, 1.05, 0.98, 1.0]
def popk(t, t0):
    f = int((t - t0) * FPS); return 0.0 if f < 0 else (POP[f] if f < len(POP) else 1.0)
def put(c, spr, cx, cy, k=1.0, anchor="c"):
    if k <= 0.01: return
    s = spr if abs(k - 1) < 0.01 else spr.resize((max(1, int(spr.width * k)), max(1, int(spr.height * k))), Image.BILINEAR)
    y = cy - s.height / 2 if anchor == "c" else cy - s.height
    c.alpha_composite(s, (int(cx - s.width / 2), int(y)))
TX = {}
def outlined(text, size, fill=(255, 255, 255), f=None, stroke=9, emoji=None):
    f = f or SANS; key = (text, size, fill, f, stroke, emoji)
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
    key = ("pill", text, size, col, bg)
    if key in TX: return TX[key]
    f = font(SANS, size); tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text, font=f)
    im = Image.new("RGBA", (int(tw) + 60, size + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 18, fill=bg); d.text((im.width / 2, im.height / 2), text, font=f, fill=col + (255,), anchor="mm")
    TX[key] = im; return im
def panel(c, box, alpha=200):
    pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rounded_rectangle(box, 32, fill=(22, 16, 12, alpha)); c.alpha_composite(pan)
    return ImageDraw.Draw(c)
def serif_label(c, s, x, y, size, alpha=1.0, col=(246, 238, 218)):
    if alpha <= 0: return
    f = font(SERIF, size); im = Image.new("RGBA", (int(size * len(s) * 0.66) + 60, size + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((im.width / 2 + 2, im.height / 2 + 3), s, font=f, fill=(30, 20, 10, int(140 * alpha)), anchor="mm"); d.text((im.width / 2, im.height / 2), s, font=f, fill=col + (int(255 * alpha),), anchor="mm")
    c.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
def pin(c, x, y, col=(200, 40, 40)):
    d = ImageDraw.Draw(c); d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=col, outline=(255, 255, 255), width=5)

# ------------------------------------------------------------------ captions
UNIT = ("million", "billion", "trillion", "euros", "dollars", "percent", "barrels")
def chunks():
    out, ws = [], []
    for w in WORDS:                                                      # glue "3" ".6", "119" "%", "550" ",000"
        s = w["w"].strip()
        if ws and s[:1] in ".%," and (s[1:2].isdigit() or s == "%"): ws[-1] = dict(ws[-1], w=ws[-1]["w"].strip() + s, e=w["e"])
        else: ws.append(dict(w))
    clause = []
    for w in ws:
        clause.append(w)
        if w["w"].strip().endswith((",", ".", "?", "!")): out.append(clause); clause = []
    if clause: out.append(clause)
    parts_all = []
    for cl in out:                                                       # balanced 1-3 word chunks per clause
        k = math.ceil(len(cl) / 3); base, extra = divmod(len(cl), k); sizes = [base + (1 if i >= k - extra else 0) for i in range(k)]
        i = 0; parts = []
        for n in sizes: parts.append(cl[i:i + n]); i += n
        for j in range(len(parts) - 1):                                  # never split "340 | billion"
            if parts[j][-1]["w"].strip()[:1].isdigit() and parts[j + 1][0]["w"].strip(" ,.").lower() in UNIT: parts[j + 1].insert(0, parts[j].pop())
        parts_all += [p for p in parts if p]
    res = []
    for i, c in enumerate(parts_all):
        t1 = parts_all[i + 1][0]["s"] if i + 1 < len(parts_all) else c[-1]["e"] + 0.5
        txt = " ".join(w["w"].strip() for w in c)
        for a, b in CFG["cap_fix"]: txt = txt.replace(a, b)
        res.append((c[0]["s"] - 0.05, min(t1, c[-1]["e"] + 0.5), txt.strip(",. ")))
    return res
CAPS = None

def frame(t, overlay):
    global LOGO, CAPS
    if LOGO is None: LOGO = make_logo()
    if CAPS is None: CAPS = chunks()
    if CFG.get("frames"):                                            # 3D Shorts: Blender frames from disk (f_00001.png = t 0)
        i = int(round(t * FPS)) + 1
        while i > 1 and not os.path.exists(CFG["frames"] + f"f_{i:05d}.png"): i -= 1
        c = Image.open(CFG["frames"] + f"f_{i:05d}.png").convert("RGBA"); cam = None
    elif CFG.get("bgfn"):                                            # no map: a custom background function bgfn(t) -> RGB(A) image (e.g. the dog video)
        c = CFG["bgfn"](t).convert("RGBA"); cam = None
    else:
        img, cam = map_frame(t); c = papered(img)
    overlay(c, t, cam)
    c.alpha_composite(LOGO, (26, 92))
    for t0, t1, s in CAPS:
        if t0 <= t < t1: put(c, outlined(s, CFG["cap_size"], stroke=8), W / 2, CFG["cap_y"]); break
    return c.convert("RGB")

def qa(times, overlay):
    tw, th = (270, 480) if H > W else (480, 270); cols = 6 if H > W else 4
    ims = [frame(float(t), overlay).resize((tw, th), Image.LANCZOS) for t in times]
    sheet = Image.new("RGB", (cols * (tw + 10), ((len(ims) + cols - 1) // cols) * (th + 40)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
    for i, (im, t) in enumerate(zip(ims, times)):
        x, y = (i % cols) * (tw + 10), (i // cols) * (th + 40); sheet.paste(im, (x + 5, y + 5)); d.text((x + 10, y + th + 10), f"{float(t):.1f}s", fill=(255, 220, 90))
    sheet.save(CFG["B"] + "qa_sheet.png"); print(CFG["B"] + "qa_sheet.png")
def seg(i, n, overlay):
    a, b = NF * i // n, NF * (i + 1) // n
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", CFG["B"] + f"seg_{i}.mp4"], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(frame(f / FPS, overlay).tobytes())
    p.stdin.close(); p.wait(); print("seg done", i, flush=True)
def duck_gain(vo, SR, under_db=-15.0, gap_db=-10.0, hold=0.30, attack=0.06, release=0.40):
    """per-sample music gain (dB re the voice RMS): `under_db` while the voice talks, `gap_db` in pauses longer than `hold`"""
    hop = int(0.01 * SR); nf = len(vo) // hop + 1; v = np.pad(vo, (0, nf * hop - len(vo)))
    rms = np.sqrt(np.mean(v.reshape(nf, hop) ** 2, axis=1)); vr = np.sqrt(np.mean(vo[np.abs(vo) > 1e-3] ** 2) + 1e-12)
    act = rms > 0.1 * vr; h = int(hold / 0.01); act2 = act.copy()
    for i in np.where(act)[0]: act2[i:i + h] = True                      # hold over short gaps between words
    tgt = np.where(act2, under_db, gap_db).astype(np.float32); g = np.empty_like(tgt); cur = gap_db
    ka, kr = 1 - np.exp(-0.01 / attack), 1 - np.exp(-0.01 / release)
    for i, x in enumerate(tgt): cur += (x - cur) * (ka if x < cur else kr); g[i] = cur
    return np.interp(np.arange(len(vo)), np.arange(nf) * hop, g).astype(np.float32)

def mix(vo_path, music_path, sfx, dur, out_dir, under_db=-15.0, gap_db=-10.0):
    """VO (float) + ducked CC-BY music bed + SFX -> out_dir/mix.wav mastered to -16 LUFS (limiter)"""
    import soundfile as sf
    import audio_master as AM
    SR = 48000
    def dec(path):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).copy()
    vo = dec(vo_path); n = int((dur + 0.3) * SR); out = np.zeros(n, np.float32); out[:min(n, len(vo))] += vo[:n]
    vrms = np.sqrt(np.mean(vo[np.abs(vo) > 1e-3] ** 2) + 1e-12)
    if isinstance(music_path, (list, tuple)):                         # [(file, start_s), ...] -> one bed, 2 s crossfades
        mus = np.zeros(n, np.float32); xf = int(2.0 * SR)
        for k, (f, t0) in enumerate(music_path):
            t1 = music_path[k + 1][1] if k + 1 < len(music_path) else dur + 0.3
            a, b = int(t0 * SR), min(n, int(t1 * SR) + xf); seg = dec(MUSIC + f)
            seg = np.tile(seg, int(np.ceil((b - a) / max(1, len(seg)))) + 1)[: b - a]
            seg = seg / (np.sqrt(np.mean(seg ** 2)) + 1e-9)
            env = np.ones(b - a, np.float32); fi = min(xf, len(env) // 2); env[:fi] = np.linspace(0, 1, fi) if k else 1; env[-fi:] = np.linspace(1, 0, fi)
            mus[a:b] += seg * env
    else:
        mus = dec(music_path)[:n]; mus = np.pad(mus, (0, max(0, n - len(mus))))
    fade = np.ones(n, np.float32); fl = int(0.6 * SR); fade[:fl] = np.linspace(0.3, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
    gdb = duck_gain(np.pad(vo, (0, max(0, n - len(vo))))[:n], SR, under_db, gap_db)
    out += mus * fade * (vrms / (np.sqrt(np.mean(mus ** 2)) + 1e-12)) * (10 ** (gdb / 20))
    for name, t0, db in sfx:
        s = dec(SFXD + name + ".wav")[: int(1.0 * SR)]; srms = np.sqrt(np.mean(s[np.abs(s) > 1e-4] ** 2)) + 1e-12
        i0 = int(max(t0, 0) * SR); j = min(n, i0 + len(s)); out[i0:j] += s[: j - i0] * (vrms / srms) * 10 ** (db / 20)
    k = 0.89 / max(1e-6, np.abs(out).max()); sf.write(out_dir + "mix_raw.wav", out * k, SR, subtype="FLOAT")
    AM.master(out_dir + "mix_raw.wav", out_dir + "mix.wav", target=-16.0, tp=-1.0); print("audio", AM.measure(out_dir + "mix.wav"))

def audio(sfx, music_db=-15.0, gap_db=-10.0):
    m = CFG["music"]; mix(CFG["vo"], m if isinstance(m, (list, tuple)) else MUSIC + m, sfx, DUR, CFG["B"], music_db, gap_db)

def remux(video, wav, out):
    """swap the audio of a finished mp4 (video stream copied)"""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", "-movflags", "+faststart", out], check=True); print(out)

def final(nseg=3):
    B = CFG["B"]
    with open(B + "segs.txt", "w") as f:
        for i in range(nseg): f.write(f"file 'seg_{i}.mp4'\n")
    E = CFG["root"] + "export/"; os.makedirs(E, exist_ok=True); out = E + CFG["out"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)
def render_all(script, nseg=3):
    """build, then nseg parallel seg processes of the calling script, then wait"""
    build()
    env = dict(os.environ, PYTHONUTF8="1")
    ps = [subprocess.Popen([sys.executable, script, "seg", str(i), str(nseg)], env=env) for i in range(nseg)]
    for p in ps: p.wait()

def main(argv, overlay, sfx=(), music_db=-15.0):
    m = argv[1]
    if m == "build": build()
    elif m == "qa": qa(argv[2:], overlay)
    elif m == "seg": seg(int(argv[2]), int(argv[3]), overlay)
    elif m == "allseg":                                               # long videos: n parallel segments, then audio + final
        nseg = int(argv[2]) if len(argv) > 2 else 6; build(); env = dict(os.environ, PYTHONUTF8="1")
        ps = [subprocess.Popen([sys.executable, os.path.abspath(argv[0]), "seg", str(i), str(nseg)], env=env) for i in range(nseg)]
        for p in ps: p.wait()
        audio(sfx, music_db); final(nseg)
    elif m == "audio": audio(sfx, music_db)
    elif m == "final": final(int(argv[2]) if len(argv) > 2 else 3)
    elif m == "all":
        if CFG.get("frames"):
            env = dict(os.environ, PYTHONUTF8="1")
            ps = [subprocess.Popen([sys.executable, os.path.abspath(argv[0]), "seg", str(i), "3"], env=env) for i in range(3)]
            for p in ps: p.wait()
        else: render_all(os.path.abspath(argv[0]))
        audio(sfx, music_db); final()
    elif m == "caps":
        for a, b, s in chunks(): print(f"{a:6.2f} {s}")
