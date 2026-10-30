"""The File Keeper: the Last Hours host mark (owner decision 30 Oct 2026: drawn by us, no AI). A front-facing detective silhouette:
fedora with a red band, face lost in the brim's shadow, trench-coat collar turned up, red tie. Three treatments for the owner to pick:
  v1 badge  : bone silhouette on the channel's ink, thin bone ring (avatar, watermark, video stamp)
  v2 stamp  : red rubber-stamp on paper with "THE FILE KEEPER · THE LAST HOURS" round the rim (end card "CASE CLOSED")
  v3 folder : ink silhouette on a manila case-file with a "FILE KEEPER" tab (thumbnail corner, mid-video badge)
Drawn at 4x and scaled down (smooth edges). Outputs here: mark_v*.png (1024 px) + _sheet.png (each at 512 / 98 / 48 px).
  uv run --no-project --with pillow --with numpy python draw_mark.py"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
import lastkit as L
from lastkit import INK, BONE, RED, COND, TYPE, SER
OUT = "D:/why habibi/_newchannel/brand/file_keeper/"
S = 4096                                                   # drawing canvas (4x of 1024)
def P(pts, k=S / 1000, dx=0, dy=0): return [(x * k + dx, y * k + dy) for x, y in pts]

# the figure on a 1000 x 1000 grid (front view)
CROWN = [(330, 300), (343, 215), (378, 150), (440, 118), (500, 140), (560, 118), (622, 150), (657, 215), (670, 300)]
BAND = [(334, 256), (666, 256), (670, 298), (330, 298)]
FACE = [(386, 318), (382, 388), (398, 444), (440, 486), (500, 502), (560, 486), (602, 444), (618, 388), (614, 318)]   # the head fills the hat
COLL_L = [(292, 610), (350, 405), (444, 450), (488, 522), (452, 640)]
COLL_R = [(1000 - x, y) for x, y in COLL_L]
COAT = [(80, 1180), (128, 820), (160, 730), (215, 660), (292, 610), (452, 640), (500, 690), (548, 640), (708, 610), (785, 660), (840, 730), (872, 820), (920, 1180)]
VEE = [(452, 640), (500, 690), (548, 640), (500, 860)]
TIE = [(488, 690), (512, 690), (521, 790), (500, 830), (479, 790)]

def figure(fg, face, accent, scale=0.86, dy=60):
    """the silhouette on a transparent 4096 canvas"""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = S / 1000 * scale; dx = S * (1 - scale) / 2; oy = dy * S / 1000
    q = lambda pts: P(pts, k, dx, oy)
    d.polygon(q(COAT), fill=fg); d.polygon(q(VEE), fill=face); d.polygon(q(TIE), fill=accent)
    d.polygon(q(FACE), fill=face); d.polygon(q([(440, 450), (560, 450), (556, 600), (548, 640), (500, 690), (452, 640), (444, 600)]), fill=face)      # neck + throat: no gaps beside it
    d.polygon(q(COLL_L), fill=fg); d.polygon(q(COLL_R), fill=fg)
    bx0, by0 = q([(250, 254)])[0]; bx1, by1 = q([(750, 346)])[0]; d.ellipse((bx0, by0, bx1, by1), fill=fg)          # brim
    d.polygon(q(CROWN), fill=fg); d.polygon(q(BAND), fill=accent)
    return im

def circle_mask(r_frac=0.5):
    m = Image.new("L", (S, S), 0); r = S * r_frac; ImageDraw.Draw(m).ellipse((S / 2 - r, S / 2 - r, S / 2 + r, S / 2 + r), fill=255); return m

def v1_badge():
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0)); bg = Image.new("RGBA", (S, S), (18, 26, 29, 255))       # the channel ink, teal-leaning
    g = np.linspace(1.15, 0.75, S)[:, None] * np.ones((1, S)); bga = (np.asarray(bg, np.float32)[..., :3] * g[..., None]).clip(0, 255).astype(np.uint8)
    bg = Image.fromarray(bga).convert("RGBA"); c.paste(bg, (0, 0), circle_mask(0.5))
    fig = figure(BONE + (255,), (40, 44, 46, 255), RED + (255,), scale=0.8, dy=110)
    c.paste(fig, (0, 0), Image.fromarray(np.minimum(np.asarray(circle_mask(0.455)), np.asarray(fig.split()[3]))))
    ImageDraw.Draw(c).ellipse((S * 0.03, S * 0.03, S * 0.97, S * 0.97), outline=BONE + (255,), width=S // 90)
    return c

def ring_text(c, text, r, size, fill, font=COND, top=True, track=1.08):
    """text on the rim, upright: clockwise across the top arc, counter-clockwise across the bottom arc"""
    f = L.font(font, size); total = sum(f.getlength(ch) for ch in text) * track; sg = 1 if top else -1
    ang = (-90 if top else 90) - sg * math.degrees(total / r) / 2
    for ch in text:
        w = f.getlength(ch) * track; a = ang + sg * math.degrees(w / r) / 2
        g = Image.new("RGBA", (int(size * 1.6), int(size * 1.6)), (0, 0, 0, 0)); ImageDraw.Draw(g).text((g.width / 2, g.height / 2), ch, font=f, fill=fill, anchor="mm")
        g = g.rotate(-(a + 90) if top else -(a - 90), resample=Image.BICUBIC); x = S / 2 + r * math.cos(math.radians(a)); y = S / 2 + r * math.sin(math.radians(a))
        c.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2))); ang += sg * math.degrees(w / r)

def v2_stamp():
    ink = RED + (255,); c = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse((S * 0.03, S * 0.03, S * 0.97, S * 0.97), outline=ink, width=S // 45); d.ellipse((S * 0.2, S * 0.2, S * 0.8, S * 0.8), outline=ink, width=S // 110)
    fig = figure(ink, (0, 0, 0, 0), (0, 0, 0, 0), scale=0.56, dy=200); m = circle_mask(0.3); c.paste(fig, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(fig.split()[3]))))
    ring_text(c, "THE FILE KEEPER", S * 0.385, S // 11, ink, top=True); ring_text(c, "THE LAST HOURS", S * 0.385, S // 13, ink, top=False)
    for a in (180, 0):
        x, y, rr = S / 2 + S * 0.385 * math.cos(math.radians(a)), S / 2 + S * 0.385 * math.sin(math.radians(a)), S // 70
        d.polygon([(x, y - rr), (x + rr, y), (x, y + rr), (x - rr, y)], fill=ink)                              # small diamonds between the texts
    rng = np.random.default_rng(14); al = np.asarray(c.split()[3], np.float32)                                 # worn rubber-stamp ink
    noise = Image.fromarray((rng.random((S // 8, S // 8)) * 255).astype(np.uint8)).resize((S, S), Image.BICUBIC)
    al = al * np.clip((np.asarray(noise, np.float32) - 40) / 120, 0.35, 1.0); c.putalpha(Image.fromarray(al.clip(0, 255).astype(np.uint8)))
    paper = Image.new("RGBA", (S, S), (0, 0, 0, 0)); paper.paste(Image.new("RGBA", (S, S), BONE + (255,)), (0, 0), circle_mask(0.5)); paper.alpha_composite(c)
    return paper

def v3_folder():
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(c); man = (200, 168, 112, 255)
    d.rounded_rectangle((S * 0.06, S * 0.16, S * 0.94, S * 0.94), S // 40, fill=man)                         # the folder
    d.rounded_rectangle((S * 0.06, S * 0.06, S * 0.56, S * 0.24), S // 40, fill=man)                         # its tab
    d.text((S * 0.31, S * 0.12), "FILE KEEPER", font=L.font(TYPE, S // 16), fill=INK + (255,), anchor="mm")
    d.line((S * 0.06, S * 0.2, S * 0.94, S * 0.2), fill=(170, 140, 90, 255), width=S // 120)
    fig = figure(INK + (255,), (70, 64, 52, 255), RED + (255,), scale=0.74, dy=230)
    clip = Image.new("L", (S, S), 0); ImageDraw.Draw(clip).rounded_rectangle((S * 0.06, S * 0.16, S * 0.94, S * 0.94), S // 40, fill=255)
    c.paste(fig, (0, 0), Image.fromarray(np.minimum(np.asarray(clip), np.asarray(fig.split()[3]))))
    return c

if __name__ == "__main__":
    marks = {"v1_badge": v1_badge(), "v2_stamp": v2_stamp(), "v3_folder": v3_folder()}
    for n, im in marks.items(): im.resize((1024, 1024), Image.LANCZOS).save(OUT + f"mark_{n}.png")
    sheet = Image.new("RGB", (3 * 560 + 40, 560 + 160), (30, 30, 32)); d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(marks.items()):
        x = 20 + i * 560; big = im.resize((512, 512), Image.LANCZOS); sheet.paste(big, (x, 20), big)
        for j, sz in enumerate((98, 48)):
            sm = im.resize((sz, sz), Image.LANCZOS); sheet.paste(sm, (x + 40 + j * 140, 560 + (98 - sz) // 2), sm)
        d.text((x + 330, 600), n.replace("_", "  "), font=L.font(TYPE, 26), fill=(230, 220, 190))
    sheet.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
