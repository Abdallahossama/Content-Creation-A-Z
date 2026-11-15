"""#24 scenes: each fn(c, t, s, t0, t1) paints one frame of a shot onto canvas c (RGB 1920x1080)."""
from pz_draw import *

def sc_photo(c, t, s, t0, t1):
    im = pic(s["id"], s.get("crop"), s.get("bw", False)); c0 = s.get("c0", (0.5, 0.5))
    f = K.kenburns(im, t, t0, t1 + 0.6, s.get("z0", 1.03), s.get("z1", 1.13), c0, s.get("c1", c0))
    c.paste(K.vignette(f, 0.32)); credit_line(c, s["id"])
    if s.get("badge") == "sil": K.pop(c, silhouette(300), s.get("bx", 420), s.get("by", 430), t, t0 + 0.2)
    put_labels(c, t, s.get("labels", []), t1)
def darken(c, k=0.55): c.paste(Image.blend(c, Image.new("RGB", (W, H), (18, 18, 20)), k))

_CARD = {}
def sc_card(c, t, s, t0, t1):
    """chapter card: warm cream/white gradient, a big black title that de-blurs and settles"""
    if "bg" not in _CARD:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32); g = np.clip((x / W) * 0.7 + (y / H) * 0.5 - 0.25, 0, 1)[..., None]
        _CARD["bg"] = Image.fromarray((np.array(PAPER, np.float32) * (1 - g) + np.array(K.CREAM, np.float32) * g).astype(np.uint8))
    c.paste(_CARD["bg"]); k = float(ease(float(t - t0) / 0.6)); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rows = s["title"].split("|"); y0 = H / 2 - (len(rows) - 1) * 105
    for i, r in enumerate(rows): d.text((W / 2, y0 + i * 210), r.strip().upper(), font=F("black", 190), fill=INK + (255,), anchor="mm")
    if s.get("num"): d.text((W / 2, y0 - 190), s["num"], font=F("bold", 44), fill=RED + (255,), anchor="mm")
    sc = 1.08 - 0.08 * k; lw, lh = int(W * sc), int(H * sc); lay = lay.resize((lw, lh), Image.BILINEAR).crop(((lw - W) // 2, (lh - H) // 2, (lw - W) // 2 + W, (lh - H) // 2 + H))
    if k < 1: lay = lay.filter(ImageFilter.GaussianBlur(14 * (1 - k)))
    c.paste(lay, (0, 0), lay)

def grid(c, s):
    c.paste(K.grid_paper())
    if s.get("top"): ttext(c, s["top"], W / 2, 118, s.get("top_size", 84))
def sc_text(c, t, s, t0, t1):
    grid(c, s); k = eout((t - t0) / 0.4)
    ttext(c, s["text"], W / 2, s.get("y", H / 2 - 30) + 30 * (1 - k), s.get("size", 150), fill=s.get("col", INK), alpha=k)
    put_labels(c, t, s.get("labels", []), t1)

_NEWS = {}
def sc_news(c, t, s, t0, t1):
    k = s["head"]
    if k not in _NEWS:
        im = Image.new("RGB", (W, H), (58, 56, 52)); pg = np.full((980, 1500, 3), (236, 231, 218), np.float32)
        pg = Image.fromarray(np.clip(pg + np.random.default_rng(5).normal(0, 6, (980, 1500, 1)), 0, 255).astype(np.uint8)); d = ImageDraw.Draw(pg)
        d.text((750, 78), s.get("mast", "THE EVENING CHRONICLE"), font=F("serif", 74), fill=INK, anchor="mm")
        d.line((60, 132, 1440, 132), fill=INK, width=5); d.line((60, 144, 1440, 144), fill=INK, width=2)
        d.text((80, 172), s.get("date", ""), font=F("bold", 26), fill=INK, anchor="la")
        rows = s["head"].split("|")
        for i, r in enumerate(rows): d.text((750, 330 + i * 150 - (len(rows) - 1) * 75), r.strip(), font=F("black", 132), fill=INK, anchor="mm")
        for i in range(6):
            for x0 in (80, 800): d.line((x0, 560 + i * 58, x0 + 620, 560 + i * 58), fill=(150, 146, 136), width=10)
        d.text((750, 950), "ILLUSTRATION · NOT A REAL FRONT PAGE", font=F("bold", 20), fill=(120, 116, 106), anchor="mm")
        im.paste(pg.rotate(-1.5, expand=True, fillcolor=(58, 56, 52)), (190, 30)); _NEWS[k] = im
    c.paste(K.vignette(K.kenburns(_NEWS[k], t, t0, t1 + 0.6, 1.02, 1.10), 0.4)); put_labels(c, t, s.get("labels", []), t1)

def sc_letter(c, t, s, t0, t1):
    grid(c, s); d = ImageDraw.Draw(c); f = F("black", 400); x0 = W / 2; y = H / 2 - 10
    if s.get("morph") is None: d.text((x0, y), "O", font=f, fill=INK, anchor="mm")
    else:
        k = ease((t - AT(s["morph"])) / 0.8); d.text((x0 - 300 * k, y), "O", font=f, fill=INK, anchor="mm")
        if k > 0: d.text((x0 + 300 * k, y), "0", font=f, fill=RED, anchor="mm")
        if k >= 1: d.text((x0, y), "=", font=F("black", 180), fill=INK, anchor="mm")
    put_labels(c, t, s.get("labels", []), t1)

def sc_counter(c, t, s, t0, t1):
    if s.get("bg"): sc_photo(c, t, {"id": s["bg"], "z0": 1.05, "z1": 1.12, "c0": s.get("c0", (0.5, 0.5))}, t0, t1); darken(c)
    else: grid(c, s)
    k = eout((t - t0 - 0.15) / s.get("dur", 1.8)); v = s["to"] * k
    txt = s.get("pre", "") + (f"{v:,.0f}" if s.get("int", True) else f"{v:.1f}") + s.get("post", "")
    ttext(c, txt, W / 2, H / 2 - 40, s.get("size", 210), fill=(255, 255, 255) if s.get("bg") else INK)
    put_labels(c, t, s.get("labels", []), t1)

def sc_people(c, t, s, t0, t1):
    grid(c, s); d = ImageDraw.Draw(c); n = s.get("n", 5); xs = [W / 2 + (i - (n - 1) / 2) * 230 for i in range(n)]
    for i, x in enumerate(xs):
        k = eout((t - t0 - 0.12 * i) / 0.3)
        if k <= 0: continue
        col, out = TEAL, None
        if s.get("sick") is not None and t >= AT(s["sick"]): out = RED
        if s.get("dead") is not None and t >= AT(s["dead"]) and i in (1, 3): col, out = LGREY, None
        person(d, x, H / 2 + 80 + 40 * (1 - k), 150, col, out)
    put_labels(c, t, s.get("labels", []), t1)
