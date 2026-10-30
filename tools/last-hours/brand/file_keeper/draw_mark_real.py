"""The File Keeper, REALISTIC (noir) pass (owner 30 Oct: "nice but let's make it more realistic"). Same figure as draw_mark.py, drawn in
code (no AI): smoothed outlines, wool texture, coat folds, a warm back-light rim along the hat and shoulders, the face lost under the
brim, venetian-blind light + haze on the wall behind, his soft shadow on the wall, film grain and vignette.
Owner, 30 Oct (on the 2nd pass): "make variants of this like before" -> mark_noir_badge / mark_noir_seal / mark_noir_folder + _sheet_noir.png.
  uv run --no-project --with pillow --with numpy python draw_mark_real.py"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel/brand/file_keeper")
import draw_mark as F                                           # the approved silhouette geometry (head fixed 30 Oct)
OUT = "D:/why habibi/_newchannel/brand/file_keeper/"
N = 2048; K = N / 1000
rng = np.random.default_rng(1946)

def chaikin(pts, n=3):
    p = np.array(pts, float)
    for _ in range(n):
        q = np.roll(p, -1, 0); p = np.stack([0.75 * p + 0.25 * q, 0.25 * p + 0.75 * q], 1).reshape(-1, 2)
    return [tuple(x) for x in p]
def poly(pts, scale=0.84, dy=90, smooth=1):
    dx = N * (1 - scale) / 2; pts = [(x * K * scale + dx, y * K * scale + dy * K) for x, y in pts]
    return chaikin(pts, smooth) if smooth else pts
def mask(pts, smooth=1, **kw):
    m = Image.new("L", (N, N), 0); ImageDraw.Draw(m).polygon(poly(pts, smooth=smooth, **kw), fill=255); return np.asarray(m, np.float32) / 255
def ellipse_mask(box, scale=0.84, dy=90):
    dx = N * (1 - scale) / 2; (x0, y0), (x1, y1) = [(x * K * scale + dx, y * K * scale + dy * K) for x, y in box]
    m = Image.new("L", (N, N), 0); ImageDraw.Draw(m).ellipse((x0, y0, x1, y1), fill=255); return np.asarray(m, np.float32) / 255
def blur(a, r): return np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), np.float32) / 255
def fractal(oct_=6, base=4, seed=0):
    g = np.random.default_rng(seed); out = np.zeros((N, N), np.float32); amp = 1.0; tot = 0
    for o in range(oct_):
        s = base * 2 ** o; a = g.random((s, s)).astype(np.float32)
        out += amp * np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC), np.float32) / 255; tot += amp; amp *= 0.55
    return out / tot

def figure_layers():
    coat = mask(F.COAT); coll = np.maximum(mask(F.COLL_L, smooth=0), mask(F.COLL_R, smooth=0))      # sharp lapel points (no "ear muffs")
    throat = mask([(440, 450), (560, 450), (556, 600), (548, 640), (500, 690), (452, 640), (444, 600)], smooth=1)
    face = mask(F.FACE); vee = mask(F.VEE, smooth=1); tie = mask(F.TIE, smooth=1)
    brim = ellipse_mask([(250, 254), (750, 346)]); crown = mask(F.CROWN); band = mask(F.BAND, smooth=1) * crown
    body = np.clip(coat + coll + throat + face + brim + crown, 0, 1)
    return dict(coat=coat, coll=coll, throat=throat, face=face, vee=vee, tie=tie, brim=brim, crown=crown, band=band, body=body)

def render(bg_on=True):
    L = figure_layers(); yy, xx = np.mgrid[0:N, 0:N].astype(np.float32) / N
    # --- the wall behind: near-black, warm venetian-blind light from the upper left, haze
    wall = np.zeros((N, N, 3), np.float32) + np.array([12, 13, 15], np.float32)
    if bg_on:
        u = (xx * 0.55 + yy * 0.83); stripes = (np.sin(u * 2 * np.pi * 7) > 0.35).astype(np.float32)
        light = np.clip(1.1 - np.hypot(xx - 0.15, yy - 0.1) * 1.7, 0, 1) ** 2.0
        stripes = blur(stripes * light, 16) * 0.55
        haze = fractal(seed=7) * light * 0.9
        wall += stripes[..., None] * np.array([150, 112, 70], np.float32) + haze[..., None] * np.array([46, 38, 30], np.float32)
        sh = blur(np.roll(np.roll(L["body"], int(0.035 * N), 1), int(0.02 * N), 0), 14)          # his shadow on the wall
        wall *= (1 - 0.75 * sh)[..., None]
    # --- the man: charcoal wool, slightly lighter collar, black hat, dark red band and tie
    wool = 0.85 + 0.3 * (fractal(oct_=7, base=32, seed=3) - 0.5)
    img = wall.copy()
    def put(m, rgb, tex=1.0):
        nonlocal img; c = np.array(rgb, np.float32) * (tex[..., None] if isinstance(tex, np.ndarray) else tex); img = img * (1 - m[..., None]) + c * m[..., None]
    key = np.clip(1.25 - np.hypot(xx - 0.25, yy - 0.2) * 1.3, 0.45, 1.25)                         # key light from the upper left
    grad = key * (0.8 + 0.3 * (1 - yy))
    put(L["coat"], (34, 34, 37), wool * grad)
    put(L["throat"], (14, 13, 13)); put(L["face"], (16, 15, 15))
    put(L["vee"], (44, 41, 38), wool); put(L["tie"], (104, 20, 22), wool)
    put(L["coll"], (44, 44, 48), wool * grad)
    put(L["brim"], (24, 24, 26), wool * key); put(L["crown"], (30, 30, 33), wool * key * (0.85 + 0.35 * (1 - yy))); put(L["band"], (96, 18, 20), wool * key)
    # coat folds: soft dark/light strokes along the lapels and down the front
    folds = np.zeros((N, N), np.float32); d = Image.new("L", (N, N), 0); dd = ImageDraw.Draw(d)
    for line, w in (([(452, 640), (430, 760), (405, 1000)], 14), ([(548, 640), (570, 760), (595, 1000)], 14), ([(300, 640), (260, 820)], 10), ([(700, 640), (740, 820)], 10)):
        dd.line(poly(line, smooth=0), fill=255, width=w)
    folds = blur(np.asarray(d, np.float32) / 255, 10) * L["coat"]
    img *= (1 - 0.35 * folds)[..., None]
    # the brim's shadow over the face and throat
    brim_sh = blur(np.roll(L["brim"], int(0.03 * N), 0), 18) * (L["face"] + L["throat"])
    img *= (1 - 0.6 * np.clip(brim_sh, 0, 1))[..., None]
    # back-light rim: where the figure's edge faces the light (upper left)
    inner = blur(L["body"], 1.5); shifted = np.roll(np.roll(inner, int(0.004 * N), 0), int(0.003 * N), 1)
    rim = np.clip(inner - shifted, 0, 1) * L["body"]; rim = blur(rim, 1.5) * 1.1
    side = np.clip(inner - np.roll(inner, -int(0.003 * N), 1), 0, 1) * L["body"]                   # a faint cool fill on the right edge
    img += (rim * key)[..., None] * np.array([230, 190, 135], np.float32)
    img += blur(side, 1.5)[..., None] * np.array([60, 75, 90], np.float32)
    # haze in front of him, very light, so he sits IN the room
    if bg_on: img += (fractal(seed=11) * 0.08 * np.clip(1.2 - np.hypot(xx - 0.2, yy - 0.15) * 1.8, 0, 1))[..., None] * np.array([200, 170, 130], np.float32)
    # grain + vignette
    img += rng.normal(0, 5.5, (N, N, 1)).astype(np.float32)
    vig = np.clip(1 - 0.55 * np.clip(np.hypot(xx - 0.5, yy - 0.5) - 0.25, 0, None) * 2.2, 0, 1)
    img *= vig[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

def noir_seal(hero):
    """round seal: the noir portrait in a disc, bone rings, THE FILE KEEPER / THE LAST HOURS on the rim, red diamonds"""
    S = F.S; c = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse((0, 0, S - 1, S - 1), fill=(14, 15, 17, 255))
    h = hero.resize((int(S * 0.74), int(S * 0.74)), Image.LANCZOS).convert("RGBA"); m = Image.new("L", h.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, h.width - 1, h.height - 1), fill=255); c.paste(h, ((S - h.width) // 2, (S - h.height) // 2), m)
    for r, wd in ((0.372, S // 160), (0.488, S // 90)): d.ellipse((S / 2 - S * r, S / 2 - S * r, S / 2 + S * r, S / 2 + S * r), outline=F.BONE + (255,), width=wd)
    F.ring_text(c, "THE FILE KEEPER", S * 0.43, S // 12, F.BONE + (255,), top=True); F.ring_text(c, "THE LAST HOURS", S * 0.43, S // 14, F.BONE + (255,), top=False)
    for a in (180, 0):
        x, y, rr = S / 2 + S * 0.43 * np.cos(np.radians(a)), S / 2 + S * 0.43 * np.sin(np.radians(a)), S // 60
        d.polygon([(x, y - rr), (x + rr, y), (x, y + rr), (x - rr, y)], fill=F.RED + (255,))
    return c.resize((1024, 1024), Image.LANCZOS)

def noir_folder(hero):
    """the manila case file (FILE KEEPER tab) with the noir portrait clipped on as a photo print"""
    S = F.S; c = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(c); man = (200, 168, 112, 255)
    d.rounded_rectangle((S * 0.06, S * 0.16, S * 0.94, S * 0.94), S // 40, fill=man); d.rounded_rectangle((S * 0.06, S * 0.06, S * 0.56, S * 0.24), S // 40, fill=man)
    d.text((S * 0.31, S * 0.12), "FILE KEEPER", font=F.L.font(F.TYPE, S // 16), fill=F.INK + (255,), anchor="mm")
    d.line((S * 0.06, S * 0.2, S * 0.94, S * 0.2), fill=(170, 140, 90, 255), width=S // 120)
    ph = hero.resize((int(S * 0.64), int(S * 0.64)), Image.LANCZOS).convert("RGBA"); b = S // 55
    pr = Image.new("RGBA", (ph.width + 2 * b, ph.height + int(2.6 * b)), (238, 234, 222, 255)); pr.paste(ph, (b, b)); pr = pr.rotate(-3, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", pr.size, (0, 0, 0, 0)); sh.putalpha(pr.split()[3].point(lambda v: int(v * 0.45))); sh = sh.filter(ImageFilter.GaussianBlur(S // 120))
    x0, y0 = int(S * 0.5 - pr.width / 2), int(S * 0.27)
    c.alpha_composite(Image.composite(Image.new("RGBA", pr.size, (0, 0, 0, 120)), Image.new("RGBA", pr.size, (0, 0, 0, 0)), sh.split()[3]), (x0 + S // 90, y0 + S // 70))
    c.alpha_composite(pr, (x0, y0))
    cx, cy = x0 + int(pr.width * 0.18), y0 - S // 60                                      # a paper clip over the print's top edge
    for o, col in ((0, (120, 122, 126, 255)), (S // 400, (190, 192, 196, 255))):
        d2 = ImageDraw.Draw(c); d2.rounded_rectangle((cx + o, cy + o, cx + S // 22 + o, cy + S // 7 + o), S // 44, outline=col, width=S // 160)
    return c.resize((1024, 1024), Image.LANCZOS)

if __name__ == "__main__":
    hero = render()                                                                        # 2048 px
    hero.resize((1024, 1024), Image.LANCZOS).save(OUT + "noir_hero.png")
    b = hero.resize((1024, 1024), Image.LANCZOS).convert("RGBA"); m = Image.new("L", (1024, 1024), 0); ImageDraw.Draw(m).ellipse((8, 8, 1015, 1015), fill=255)
    badge = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); badge.paste(b, (0, 0), m)
    ImageDraw.Draw(badge).ellipse((14, 14, 1009, 1009), outline=(236, 230, 214, 255), width=12); badge.save(OUT + "mark_noir_badge.png")
    seal = noir_seal(hero); seal.save(OUT + "mark_noir_seal.png")
    folder = noir_folder(hero); folder.save(OUT + "mark_noir_folder.png")
    sheet = Image.new("RGB", (3 * 560 + 40, 720), (30, 30, 32)); dd = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate((("noir  badge", badge), ("noir  seal", seal), ("noir  folder", folder))):
        x = 20 + i * 560; big = im.resize((512, 512), Image.LANCZOS); sheet.paste(big, (x, 20), big)
        for j, sz in enumerate((98, 48)):
            sm = im.resize((sz, sz), Image.LANCZOS); sheet.paste(sm, (x + 40 + j * 140, 560 + (98 - sz) // 2), sm)
        dd.text((x + 330, 600), n, font=F.L.font(F.TYPE, 26), fill=(230, 220, 190))
    sheet.save(OUT + "_sheet_noir.png"); print(OUT + "_sheet_noir.png")
