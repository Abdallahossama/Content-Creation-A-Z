"""File 17 (Gaddafi's last day, Sirte, 20 October 2011) thumbnails, BREAKOUT style: one real image filling the frame, his face from the
US Navy's AU-summit photos (2 Feb 2009, public domain, file 12's B1/B2), 1-3 words on black / red blocks, the date on a yellow tab.
  A  Sirte's ruins, 2011 (Pexels) + his face ghosted: KING OF KINGS / LAST DAY
  B  a concrete culvert (Pexels, illustrative) + his face in a bubble: KING OF AFRICA / IN A PIPE?
  C  NASA's satellite image of the Gulf of Sidra on 20 Oct 2011, a red pin on Sirte + his face ghosted: HIS LAST / MORNING
No CC footage in thumbnails, no capture image, no blood, no women. Preview only: never uploaded until the owner approves.
  uv run --no-project --with pillow --with numpy python thumbs_gaddafi17.py              (B&W set)
  TH_COLOUR=1 uv run --no-project --with pillow --with numpy python thumbs_gaddafi17.py  (colour set)"""
import sys, os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/13_goering_last_night")
from thumbs_hakawi import src, cover, vign, block, ellipse, paste_faded, TW, TH, YEL, WHITE, RED
from thumbs_goering import bw
EP = "17_gaddafi_last_day"; ROOT = "D:/why habibi/_newchannel/17_gaddafi_last_day/"; OUT = ROOT + "export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None
COLOUR = os.environ.get("TH_COLOUR") == "1"
FACE = lambda: src("12_gaddafi_stadium", "B1_")                    # US Navy, AU summit, Addis Ababa, 2 Feb 2009 (PD)

def ghost(c, im, box, h, x, y, left=280):
    W0, H0 = im.size; f = bw(im.crop((int(W0 * box[0]), int(H0 * box[1]), int(W0 * box[2]), int(H0 * box[3]))))
    s = h / f.height; f = f.resize((int(f.width * s), h), Image.LANCZOS); paste_faded(c, f, x if x >= 0 else TW - f.width + 30, y, left=left)

def bubble(c, im, cx, cy, r=170, box=None):
    """his face in natural colour inside a red ring (owner, 31 Oct: the face must stand out from the toned background)"""
    if box: W0, H0 = im.size; im = im.crop((int(W0 * box[0]), int(H0 * box[1]), int(W0 * box[2]), int(H0 * box[3])))
    im = cover(im.convert("RGB"), 2 * r, 2 * r, cy=0.42)
    im = ImageEnhance.Contrast(im).enhance(1.15); im = ImageEnhance.Brightness(im).enhance(1.12); im = ImageEnhance.Color(im).enhance(1.1)
    im = im.convert("RGBA")
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255); im.putalpha(m)
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30), fill=(0, 0, 0, 170))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))                                        # a dark halo lifts the bubble off the background
    c.alpha_composite(im, (cx - r, cy - r)); ImageDraw.Draw(c).ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=RED + (255,), width=12)

def A():   # Sirte's ruins + his face: KING OF KINGS / LAST DAY
    c = bw(cover(src(EP, "A23_"), TW, TH, cx=0.42, cy=0.42, z=1.15)); c = ImageEnhance.Brightness(c).enhance(0.75).convert("RGBA")
    ghost(c, FACE(), (0.30, 0.0, 1.0, 1.0), 720, -1, 0, left=320); c = vign(c, 0.45).convert("RGBA")
    block(c, "KING OF KINGS", 40, 300, 120)
    block(c, "LAST DAY", 40, 460, 140, fill=WHITE, bg=RED + (255,))
    block(c, "SIRTE · 20 OCT 2011", 40, 92, 50, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def B():   # a concrete culvert (illustrative) + his face in a bubble: KING OF AFRICA / IN A PIPE?
    culv = Image.open(ROOT + "build/culvert.jpg").convert("RGB")
    c = bw(cover(culv, TW, TH, cx=0.42, cy=0.5, z=1.05)); c = vign(c, 0.5).convert("RGBA")
    lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(620): d.line((x, 0, x, TH), fill=(0, 0, 0, int(200 * (1 - x / 620) ** 1.2)))
    c.alpha_composite(lay)
    bubble(c, FACE(), 1040, 455, r=205, box=(0.30, 0.0, 1.0, 0.95))
    block(c, "KING OF AFRICA", 40, 300, 110)
    block(c, "IN A PIPE?", 40, 450, 140, fill=WHITE, bg=RED + (255,))
    block(c, "20 OCTOBER 2011", 40, 92, 54, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def C():   # NASA MODIS, Gulf of Sidra, 20 Oct 2011, red pin on Sirte + his face ghosted: HIS LAST / MORNING
    sat = src(EP, "A24_"); c = cover(sat, TW, TH, cx=0.5, cy=0.5, z=1.0).convert("RGB")
    if not COLOUR: c = bw(c)
    c = ImageEnhance.Brightness(c).enhance(0.85).convert("RGBA")
    # Sirte 31.205 N, 16.588 E in the snapshot's BBOX (lat 29.0-34.625, lon 12.5-22.5) -> after the cover crop above
    W0, H0 = sat.size; fx, fy = (16.588 - 12.5) / 10.0, (34.625 - 31.205) / 5.625
    s = max(TW / W0, TH / H0) * 1.0; vw, vh = W0 * s, H0 * s; ox, oy = (vw - TW) * 0.5, (vh - TH) * 0.5
    px, py = fx * vw - ox, fy * vh - oy
    d = ImageDraw.Draw(c); d.ellipse((px - 22, py - 22, px + 22, py + 22), outline=RED + (255,), width=8); d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=RED + (255,))
    block(c, "SIRTE", int(px + 34), int(py), 44, fill=(0, 0, 0), bg=YEL + (255,))
    ghost(c, src("12_gaddafi_stadium", "B2_"), (0.0, 0.0, 1.0, 0.75), 600, -1, 120, left=300); c = vign(c, 0.35).convert("RGBA")
    block(c, "HIS LAST", 40, 190, 130)
    block(c, "MORNING", 40, 345, 130, fill=WHITE, bg=RED + (255,))
    block(c, "20 OCT 2011 · NASA", 40, 60, 46, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def libya_flag(w, h):
    """the 1951 / 2011 flag (red, black, green; white crescent and star), drawn by us, waved with a sine warp and fold shading"""
    import numpy as np, math
    f = Image.new("RGB", (w, h), (0, 0, 0)); d = ImageDraw.Draw(f)
    d.rectangle((0, 0, w, h // 4), fill=(231, 0, 19)); d.rectangle((0, h // 4, w, 3 * h // 4), fill=(8, 8, 8)); d.rectangle((0, 3 * h // 4, w, h), fill=(35, 158, 70))
    cx, cy, r = w // 2, h // 2, h * 0.17
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255)); d.ellipse((cx - r * 0.62, cy - r * 0.8, cx + r * 1.12, cy + r * 0.8), fill=(8, 8, 8))
    st = [(cx + r * 0.9 + r * 0.42 * math.cos(math.radians(-90 + i * 36)) * (1 if i % 2 == 0 else 0.4), cy + r * 0.42 * math.sin(math.radians(-90 + i * 36)) * (1 if i % 2 == 0 else 0.4)) for i in range(10)]
    d.polygon(st, fill=(255, 255, 255))
    a = np.asarray(f, np.float32); out = np.zeros_like(a); xs = np.arange(w)
    shift = (18 * np.sin(xs / w * 2 * math.pi * 1.6)).astype(int); shade = 0.72 + 0.28 * np.cos(xs / w * 2 * math.pi * 1.6)
    for x in range(w): out[:, x] = np.roll(a[:, x], shift[x], axis=0) * shade[x]
    return Image.fromarray(out.clip(0, 255).astype("uint8"))

def libya_map(w, h):
    """Libya's outline from Natural Earth (public domain), dark grey fill"""
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); from mapkit import _load
    rings = [r for name, rs in _load() if name == "Libya" for r in rs]
    xs = [p[0] for r in rings for p in r]; ys = [p[1] for r in rings for p in r]; x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    k = min(w / (x1 - x0), h / (y1 - y0)); m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    for r in rings: d.polygon([((p[0] - x0) * k, (y1 - p[1]) * k) for p in r], fill=255)
    return m

def D():   # the reference look (owner, 30 Oct): dark, our own drawn Libyan flag + map, his stern face big: THE FALL OF THE / KING OF KINGS
    c = Image.new("RGBA", (TW, TH), (6, 6, 8, 255))
    fl = libya_flag(980, 520).convert("RGBA"); al = Image.new("L", fl.size, 0); ad = ImageDraw.Draw(al)
    for x in range(fl.width): ad.line((x, 0, x, fl.height), fill=int(120 * min(1, x / 140) * min(1, (fl.width - x) / 380)))
    fl.putalpha(al.filter(ImageFilter.GaussianBlur(6))); c.alpha_composite(fl, (-40, 30))
    mp = libya_map(520, 460); lay = Image.new("RGBA", mp.size, (150, 150, 150, 0)); lay.putalpha(mp.point(lambda v: int(v * 0.22))); c.alpha_composite(lay, (300, 210))
    im = FACE.__globals__["src"]("12_gaddafi_stadium", "B2_"); W0, H0 = im.size
    face = im.convert("RGB").crop((0, int(H0 * 0.03), W0, int(H0 * 0.64)))
    face = ImageEnhance.Contrast(face).enhance(1.25); face = ImageEnhance.Color(face).enhance(0.9)
    s = 760 / face.height; face = face.resize((int(face.width * s), 760), Image.LANCZOS)
    paste_faded(c, face, TW - face.width + 130, -10, left=330)
    c = vign(c, 0.35).convert("RGBA"); d = ImageDraw.Draw(c)
    import lastkit as L
    fw = L.font(L.SER, 74); d.text((60, 400), "The fall of the", font=fw, fill=(245, 242, 235), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0))
    fr = L.font(L.COND, 150); d.text((52, 525), "KING OF KINGS", font=fr, fill=(214, 28, 28), anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
    block(c, "20 OCTOBER 2011", 40, 640, 44, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def africa_one(w, h):
    """Africa from Natural Earth (public domain): every country's polygon -> (one merged mask, the inner borders as lines)"""
    import json
    d = json.load(open("D:/why habibi/_style_kit/maps/ne_10m_admin_0_countries.geojson", encoding="utf-8"))
    polys = []
    for f in d["features"]:
        if f["properties"].get("CONTINENT") != "Africa": continue
        g = f["geometry"]; ps = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        polys += [p[0] for p in ps if len(p[0]) > 40]
    x0, x1, y0, y1 = -18.0, 52.0, -35.5, 38.0                        # the mainland frame (islands far out are dropped by the frame)
    k = min(w / (x1 - x0), h / (y1 - y0)); P = lambda r: [((x - x0) * k, (y1 - y) * k) for x, y in r]
    mask = Image.new("L", (w, h), 0); dm = ImageDraw.Draw(mask); lines = Image.new("L", (w, h), 0); dl = ImageDraw.Draw(lines)
    for r in polys:
        q = P(r); dm.polygon(q, fill=255); dl.line(q + [q[0]], fill=255, width=2)
    return mask, lines

def E():   # owner, 30 Oct: "Africa united as one nation, Gaddafi as king": the borders fade out into one gold continent; his face in the gold cap
    import numpy as np
    c = Image.new("RGBA", (TW, TH), (0, 0, 0, 255)); a = np.zeros((TH, TW, 3), np.float32)
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
    a[...] = np.array([10, 24, 16], np.float32) * (1.15 - 0.6 * np.hypot((xx - 420) / TW, (yy - 330) / TH))[..., None]   # deep Libyan green
    ang = np.arctan2(yy - 330, xx - 420); rays = (np.cos(ang * 18) * 0.5 + 0.5) ** 6 * np.clip(1 - np.hypot(xx - 420, yy - 330) / 900, 0, 1)
    a += rays[..., None] * np.array([90, 70, 20], np.float32)                                    # gold rays behind the continent
    c = Image.fromarray(a.clip(0, 255).astype("uint8")).convert("RGBA")
    mw, mh = 560, 600; mask, lines = africa_one(mw, mh)
    gold = np.zeros((mh, mw, 3), np.float32); gy = np.linspace(0, 1, mh)[:, None]
    gold[...] = (np.array([255, 214, 110]) * (1 - gy) + np.array([196, 132, 30]) * gy)[:, None, :] if False else 0
    gold[...] = np.stack([255 - 60 * gy, 210 - 80 * gy, 100 - 70 * gy], -1).repeat(mw, 1)
    noise = np.random.default_rng(3).normal(0, 6, (mh, mw, 1)); gold = (gold + noise).clip(0, 255)
    ox, oy, pad = 150, 90, 90                                        # the glow is blurred on a padded canvas: no box edge around Africa (owner, 31 Oct)
    pm = Image.new("L", (mw + 2 * pad, mh + 2 * pad), 0); pm.paste(mask, (pad, pad))
    glow = pm.filter(ImageFilter.GaussianBlur(26)); gl = Image.new("RGBA", pm.size, (255, 200, 80, 0)); gl.putalpha(glow.point(lambda v: int(v * 0.85)))
    c.alpha_composite(gl, (ox - pad, oy - pad))
    g = Image.fromarray(gold.astype("uint8")).convert("RGBA"); g.putalpha(mask); c.alpha_composite(g, (ox, oy))
    # the old borders: strong on the left (north-west), fading to nothing on the right: "54 countries -> one"
    fade = (np.clip(1.15 - np.linspace(0, 1, mw) * 1.6, 0, 1)[None, :] * np.asarray(lines, np.float32) * np.asarray(mask, np.float32) / 255).clip(0, 255)
    bl = Image.new("RGBA", (mw, mh), (90, 50, 10, 0)); bl.putalpha(Image.fromarray((fade * 0.9).astype("uint8"))); c.alpha_composite(bl, (ox, oy))
    face = src("12_gaddafi_stadium", "B1_").convert("RGB"); W0, H0 = face.size
    face = face.crop((int(W0 * 0.30), 0, W0, H0)); face = ImageEnhance.Contrast(face).enhance(1.18)
    s = 730 / face.height; face = face.resize((int(face.width * s), 730), Image.LANCZOS)
    paste_faded(c, face, TW - face.width + 60, -5, left=300)
    c = vign(c, 0.3).convert("RGBA"); d = ImageDraw.Draw(c)
    import lastkit as L
    f1 = L.font(L.COND, 112); f2 = L.font(L.COND, 150)
    d.text((48, 120), "ONE AFRICA.", font=f1, fill=(250, 246, 236), anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((44, 590), "ONE KING.", font=f2, fill=(255, 196, 30), anchor="lm", stroke_width=8, stroke_fill=(0, 0, 0))
    block(c, "2008: 200 KINGS NAMED HIM 'KING OF KINGS'", 48, 680, 32, fill=(0, 0, 0), bg=YEL + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("E_ONE_AFRICA_ONE_KING", E), ("D_FALL_OF_THE_KING", D), ("B_IN_A_PIPE", B), ("C_HIS_LAST_MORNING", C), ("A_KING_OF_KINGS", A)):
        sfx = "_COLOR" if COLOUR else ""; im = fn().convert("RGB"); im.save(OUT + name + sfx + ".png"); im.save(OUT + name + sfx + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
    for i, t in enumerate(tiles):
        S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0))
        S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
    S.save(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"), quality=88); print(OUT + ("_sheet_COLOR.jpg" if COLOUR else "_sheet.jpg"))
