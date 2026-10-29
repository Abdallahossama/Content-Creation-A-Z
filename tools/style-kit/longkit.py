"""longkit: shared helpers for the 16:9 long-form Ask Habibi explainers built on shortkit (from Ep 5 Egypt).
Use after K.setup(..., size=(1920, 1080)).
    import longkit as L; L.init(K)        # binds W/H
    L.big(c, "1970", t, t0, sub="source")  L.headline(c, "TEXT", t, t0)  L.place(c, cam, "name", (lon, lat), k)
    L.panel(c, box)  L.chapter_card(c, t, CH)  L.layer(c, fn)  L.poly_px(cam, pts)  L.at/L.anchors"""
import math
from PIL import Image, ImageDraw, ImageFilter
import shortkit as K
from shortkit import put, outlined, pill, popk, geo, ease, font, pin, YEL, SANS, IMPACT

def W(): return K.W
def H(): return K.H
def norm(s): return s.strip(" ,.?!:;\"'").lower()
def at(word, n=1, after=0.0):
    k = 0
    for w in K.WORDS:
        if w["s"] >= after and norm(w["w"]) == word.lower():
            k += 1
            if k == n: return w["s"]
    raise KeyError(f"{word} #{n} after {after}")
class Anchors(dict):
    def a(self, name, word, n=1, after=None):
        self[name] = at(word, n, self[after] if isinstance(after, str) else (after or 0.0)); return self[name]

def poly_px(cam, pts): return [geo(cam, *p) for p in pts]
def layer(c, draw_fn, alpha=255, blur=0):
    lay = Image.new("RGBA", (K.W, K.H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(lay))
    if blur: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 255: lay.putalpha(lay.split()[3].point(lambda v: v * alpha // 255))
    c.alpha_composite(lay)
def fitw(im, maxw=1220):
    if im.width <= maxw: return im
    k = maxw / im.width; return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
def big(c, text, t, t0, y=190, size=150, col=YEL, sub=None, sub_y=None, x=None):
    if t < t0: return
    put(c, fitw(outlined(text, size, fill=col, f=IMPACT, stroke=10)), x or K.W / 2, y, popk(t, t0))
    if sub: put(c, pill(sub, 38), x or K.W / 2, sub_y or y + size * 0.72, popk(t, t0 + 0.15))
def headline(c, text, t, t0, y=170, size=86, col=(255, 255, 255)):
    if t < t0: return
    put(c, fitw(outlined(text, size, fill=col)), K.W / 2, y, popk(t, t0))
def sub(c, text, t, t0, y=270, size=40, col=(255, 225, 120), bg=(24, 18, 12, 215)):
    if t < t0: return
    put(c, pill(text, size, col, bg), K.W / 2, y, popk(t, t0))
def place(c, cam, name, ll, k=1.0, col=(200, 40, 40), dx=0, dy=-46, size=34):
    if k <= 0: return
    x, y = geo(cam, *ll); pin(c, x, y, col); put(c, pill(name, size), x + dx, y + dy, k)
def panel(c, box, a=215):
    lay = Image.new("RGBA", (K.W, K.H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle(box, 36, fill=(22, 16, 12, a)); c.alpha_composite(lay)
    return ImageDraw.Draw(c)
def chapter_card(c, t, CH, dur=1.6):
    for i, (name, t0) in enumerate(CH):
        if t0 - 0.05 <= t < t0 + dur:
            u = (t - t0) / dur; k = ease(min(1, u * 4)) * (1 - ease(max(0, (u - 0.75) * 4)))
            c.alpha_composite(Image.new("RGBA", (K.W, K.H), (14, 10, 8, int(200 * k))))
            put(c, outlined(f"{i + 1}", 200, fill=YEL, f=IMPACT, stroke=10), K.W / 2, K.H / 2 - 120, k)
            put(c, fitw(outlined(name, 96)), K.W / 2 + (1 - k) * 200, K.H / 2 + 60, k)
def hold_keys(keys, gap=2.6, move=1.1, push=1.07):
    """camera keys -> arrive, slow push-in, quick move to the next shot"""
    out = []
    for t, x, y, p in sorted(keys):
        if out and t <= out[-1][0] + 0.05: t = out[-1][0] + 0.05
        out.append((t, x, y, p))
    held = []
    for (t0, x0, y0, p0), (t1, x1, y1, p1) in zip(out, out[1:]):
        held.append((t0, x0, y0, p0))
        if t1 - t0 > gap: held.append((t1 - move, x0, y0, p0 * push))
    held.append(out[-1]); return held
def character(c, name, t, t0, x, y=1040, h=420, flip=False, t1=None):
    if t < t0 or (t1 is not None and t >= t1): return
    put(c, K.sprite(name, h, flip), x, y, popk(t, t0), anchor="b")
def timeline(c, t, t0, marks, title="years ago", y=520, x0=260, x1=1660, span=200000, log=False):
    """a horizontal years-ago bar (left = older). marks: [(years, label, t_pop, colour, range_years or 0)]"""
    d = panel(c, (x0 - 60, y - 200, x1 + 60, y + 150), 225); d.text((K.W / 2, y - 160), title, font=font(SANS, 38), fill=(235, 225, 210), anchor="mm")
    d.line((x0, y, x1, y), fill=(200, 190, 175), width=6)
    xp = lambda yrs: x1 - (x1 - x0) * min(1, yrs / span)
    for k in range(0, span + 1, span // 4):
        d.line((xp(k), y - 12, xp(k), y + 12), fill=(200, 190, 175), width=4); d.text((xp(k), y + 40), f"{k // 1000}k" if k else "now", font=font(SANS, 28), fill=(200, 190, 175), anchor="mm")
    for yrs, lab, tp, col, rng in marks:
        if t < tp: continue
        u = popk(t, tp)
        if rng: d.rounded_rectangle((xp(yrs + rng), y - 14, xp(max(0, yrs - rng)), y + 14), 10, fill=col + (150,))
        r = 18 * u; d.ellipse((xp(yrs) - r, y - r, xp(yrs) + r, y + r), fill=col, outline=(255, 255, 255), width=4)
        ly = y - 55 - 46 * (marks.index((yrs, lab, tp, col, rng)) % 2)                      # stagger so close marks never overlap
        d.text((xp(yrs), ly), lab, font=font(IMPACT, 42), fill=YEL, anchor="mm", stroke_width=4, stroke_fill=(10, 10, 10))

# ------------------------------------------------------------------ outro end screen, subscribe nudge, paper photos (user feedback 18 Oct 2026)
import marker as MK
END_BOXES = ((150, 300, 870, 705), (1050, 300, 1770, 705))      # = brand/end_screen_1920x1080.png: place the 2 YouTube video elements here
END_SUB = (960, 900, 105)                                        # subscribe element circle (centre x, y, radius)
def _rect_path(b, seed):
    x0, y0, x1, y1 = b; r = __import__("numpy").random.default_rng(seed); j = lambda: r.uniform(-4, 4)
    pts = [(x0 + j(), y0 + j()), (x1 + j(), y0 + j()), (x1 + j(), y1 + j()), (x0 + j(), y1 + j()), (x0 + j() + 30, y0 + j())]
    import numpy as np
    return [np.concatenate([np.linspace(pts[k], pts[k + 1], 40) for k in range(4)])]
def end_screen(c, t, t0, title="still curious?", face="Batata_smug"):
    """the last ~20 s: the video dims to navy, marker boxes for 2 end-screen videos + the subscribe circle draw on, Batata pops in"""
    if t < t0: return
    u = t - t0; k = ease(u / 0.6)
    c.alpha_composite(Image.new("RGBA", (K.W, K.H), (10, 14, 64, int(240 * k))))
    MK.place(c, MK.hand(title, 110, MK.YEL, rot=-2, reveal=min(1, max(0, (u - 0.3) / 0.7))), K.W / 2, 150)
    for i, b in enumerate(END_BOXES):
        p = min(1, max(0, (u - 0.5 - i * 0.25) / 0.6))
        if p > 0:
            if p >= 1: c.alpha_composite(Image.new("RGBA", (b[2] - b[0], b[3] - b[1]), (0, 0, 0, 70)), (b[0], b[1]))
            MK.strokes(c, _rect_path(b, 7 + i), MK.WHITE, 9, p, seed=7 + i)
    if u > 1.2: MK.place(c, MK.hand("watch this next", 70, MK.WHITE, rot=-2, reveal=min(1, (u - 1.2) / 0.5)), 420, 765)
    if u > 1.5:
        cx, cy, r = END_SUB; MK.strokes(c, MK.circle_path(cx, cy, r, r, seed=5), MK.YEL, 10, min(1, (u - 1.5) / 0.6), seed=5)
    if u > 1.9: MK.place(c, MK.hand("subscribe\n(it's free)", 64, MK.YEL, rot=-3, reveal=min(1, (u - 1.9) / 0.5)), 1230, 905)
    f = int((u - 2.3) * K.FPS)
    if f >= 0: MK.place(c, MK.sticker(MK.BATATA + face + ".png", 300, rot=-6, scale=MK.pop(f)), 1730, 905)
def subscribe_nudge(c, t, t0, t1, x=1560, y=330, t_click=None):
    """smooth mid-video ask: a red SUBSCRIBE button slides in at the top right, a cursor clicks it, it turns grey 'SUBSCRIBED'"""
    if not (t0 <= t < t1): return
    u = t - t0; out = ease((t1 - t) / 0.4); slide = ease(u / 0.35) * out
    tc = (t_click - t0 + 0.25) if t_click else 1.6; u = u * 1.6 / tc     # the click lands on the spoken word
    clicked = u > 1.6
    btn = pill("SUBSCRIBED" if clicked else "SUBSCRIBE", 64, (255, 255, 255) if not clicked else (60, 60, 60),
               (204, 0, 0, 255) if not clicked else (226, 226, 226, 255))
    bx = x + (1 - slide) * 700; put(c, btn, bx, y, popk(t, t0 + tc) if clicked and u < 1.9 else 1.0)
    put(c, K.sprite("host_cool", 340), bx - btn.width / 2 - 150, y + 190, slide, anchor="b")
    if 0.7 < u < 2.4:                                                              # the cursor arrives, clicks, leaves
        v = ease((u - 0.7) / 0.8); cx, cy = bx + 260 - 200 * v, y + 160 - 140 * v
        d = ImageDraw.Draw(c); s = 1.0 if not (1.5 < u < 1.7) else 0.8
        pts = [(0, 0), (0, 44 * s), (12 * s, 33 * s), (21 * s, 52 * s), (29 * s, 48 * s), (20 * s, 30 * s), (36 * s, 30 * s)]
        d.polygon([(cx + a, cy + b) for a, b in pts], fill=(255, 255, 255), outline=(10, 10, 10), width=3)
PHOTO = {}
def _photo_card(path, w, rot, credit):
    key = (path, w, rot, credit)
    if key in PHOTO: return PHOTO[key]
    im = Image.open(path).convert("RGB"); w = min(w, int(520 * im.width / im.height)); h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    bd = max(14, w // 40); card = Image.new("RGBA", (w + 2 * bd, h + 2 * bd + (34 if credit else 0)), (250, 247, 240, 255)); card.paste(im, (bd, bd))
    if credit: ImageDraw.Draw(card).text((card.width - bd, h + bd + 20), credit, font=font(SANS, 20), fill=(90, 80, 70), anchor="rm")
    tape = Image.new("RGBA", (int(w * 0.22), 46), (236, 222, 170, 190))
    out = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 120)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (48, 52))
    out.alpha_composite(card, (40, 40)); out.alpha_composite(tape.rotate(-4, expand=True), (40 + card.width // 2 - tape.width // 2, 16))
    out = out.rotate(rot, Image.BICUBIC, expand=True); PHOTO[key] = out; return out
def photo(c, path, t, t0, t1=None, x=None, y=520, w=760, rot=-3, credit=None):
    """proof photo shown while we speak: a printed photo with a white border, tape and a shadow, slapped on with a pop"""
    if t < t0 or (t1 is not None and t >= t1): return
    k = popk(t, t0)
    if t1 is not None and t > t1 - 0.25: k = ease((t1 - t) / 0.25)
    put(c, _photo_card(path, w, rot, credit), x or K.W / 2, y, k)

def cutout(c, path, t, t0, x, y, h, rot=0, t1=None):
    """a real photo cut-out (e.g. a louse micrograph) as a white-edged sticker, popped in"""
    if t < t0 or (t1 is not None and t >= t1): return
    k = popk(t, t0)
    if k > 0.01: MK.place(c, MK.sticker(path, h, border=10, rot=rot, scale=k), x, y)
RM = {}
def _rm_src(path, bounds):
    """the source image, tiled 3x around the dateline for world maps and padded top/bottom (deep sea colour), with its new bounds"""
    key = (path, bounds)
    if key not in RM:
        RM.clear(); im = Image.open(path).convert("RGB"); lon0, lon1, lat0, lat1 = bounds; pw = 0
        if lon1 - lon0 >= 359:
            t = Image.new("RGB", (im.width * 3, im.height)); [t.paste(im, (k * im.width, 0)) for k in range(3)]; im = t; lon0 -= 360; lon1 += 360
        else: pw = im.width // 3
        ph = im.height // 8 if pw == 0 else im.height // 3
        p = Image.new("RGB", (im.width + 2 * pw, im.height + 2 * ph), (8, 14, 40)); p.paste(im, (pw, ph))
        dx = (lon1 - lon0) / im.width * pw; dy = (lat1 - lat0) / im.height * ph
        RM[key] = (p, (lon0 - dx, lon1 + dx, lat0 - dy, lat1 + dy))
    return RM[key]
def real_map(c, cam, k, path, bounds):
    """cross-fade to a REAL satellite map (NASA Blue Marble, public domain) under the same camera. bounds = (lon0, lon1, lat0, lat1) of the image"""
    if k <= 0.01: return
    im, (lon0, lon1, lat0, lat1) = _rm_src(path, bounds); lon, lat, p = cam; vw, vh = K.W / p, K.H / (p * K.KY)
    sx, sy = im.width / (lon1 - lon0), im.height / (lat1 - lat0)
    box = [(lon - vw / 2 - lon0) * sx, (lat1 - lat - vh / 2) * sy, (lon + vw / 2 - lon0) * sx, (lat1 - lat + vh / 2) * sy]
    box = (max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))     # last-resort clamp
    lay = im.resize((K.W, K.H), Image.BICUBIC, box=box).convert("RGBA"); lay.putalpha(int(255 * min(1, k))); c.alpha_composite(lay)
def fade(t, t0, t1, d=0.5):
    """0 -> 1 -> 0 envelope for [t0, t1)"""
    if t < t0 or t >= t1: return 0.0
    return ease(min((t - t0) / d, (t1 - t) / d, 1.0))
