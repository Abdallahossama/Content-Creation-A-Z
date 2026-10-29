"""5 thumbnails (1280x720) for 'Why Do Embarrassing Memories Hit at 3 a.m.?' in the Why/Ask Habibi brand style."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gfxlib as G
G.W, G.H = 1280, 720
from gfxlib import text, pill, load, place, star_pts, moon, NAVY, YEL, WHITE, RED, RED2, SKY, GRN, PK, B

W, H = 1280, 720
OUT = B + "1st video/claude_package/thumbnails/"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(5)

def night_bg(c1=(70, 36, 160), c2=(16, 14, 66), rays=True, cx=900, cy=360, seed=1):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - cx) / 900) ** 2 + ((yy - cy) / 650) ** 2)
    g = np.clip(d, 0, 1)[..., None]
    arr = np.array(c1, np.float32) * (1 - g) + np.array(c2, np.float32) * g
    if rays:
        ang = np.arctan2(yy - cy, xx - cx); seg = 2 * np.pi / 24
        m = ((ang % seg) < seg / 2)[..., None]
        arr = np.where(m, arr * 1.09, arr)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    dr = ImageDraw.Draw(im); r = np.random.default_rng(seed)
    for _ in range(70):
        x, y, s = r.uniform(0, W), r.uniform(0, H), r.choice([2, 3, 4, 7], p=[.5, .3, .15, .05])
        if s >= 7:
            dr.polygon(star_pts(x, y, s * 1.6, s * 0.6, n=4), fill=(255, 255, 255, 230))
        else:
            dr.ellipse((x - s / 2, y - s / 2, x + s / 2, y + s / 2), fill=(255, 255, 255, 200))
    return im

def headline(top, big, top_size=86, big_size=150, top_col=WHITE, big_col=YEL):
    t1 = text(top, top_size, top_col, stroke=13, stroke_fill=NAVY, shadow=9) if top else None
    t2 = text(big, big_size, big_col, stroke=16, stroke_fill=NAVY, shadow=12)
    w = max(t2.width, t1.width if t1 else 0); h = t2.height + (t1.height - 22 if t1 else 0)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    if t1:
        im.alpha_composite(t1, (0, 0)); y = t1.height - 22
    im.alpha_composite(t2, (0, y))
    return im

def outline_glow(spr, col=(255, 255, 255), r=10, a=110):
    al = spr.getchannel("A").filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", spr.size, col + (0,)); g.putalpha(al.point(lambda v: min(255, int(v * a / 100))))
    out = Image.new("RGBA", spr.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(spr)
    return out

def padded(spr, pad=30):
    im = Image.new("RGBA", (spr.width + pad * 2, spr.height + pad * 2), (0, 0, 0, 0)); im.alpha_composite(spr, (pad, pad)); return im

def char(name, mood, h, flip=False, outfit="01_Characters_Plain"):
    return outline_glow(padded(load(f"{PK}{outfit}/{name}/{name}_{mood}.png", height=h, flip=flip)), (255, 255, 255), 12, 70)

def pose(name, p, h, flip=False):
    return outline_glow(padded(load(f"{PK}03_Poses/{name}/{name}_pose_{p}.png", height=h, flip=flip)), (255, 255, 255), 12, 70)

def tag(c):
    t = pill("ASK HABIBI", 26, fill=NAVY, tc=YEL, shadow=0, ow=4)
    place(c, t, 30 + t.width / 2, H - 34)

def clock(digits="3:00", w=420, glow=True):
    h = int(w * 0.52)
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 52, 40 + w, 52 + h), 40, fill=NAVY)
    d.rounded_rectangle((40, 40, 40 + w, 40 + h), 40, fill=(30, 30, 46), outline=NAVY, width=10)
    d.rounded_rectangle((70, 66, 10 + w, 14 + h), 24, fill=(12, 6, 10))
    t = text(digits, int(h * 0.56), (255, 60, 50))
    if glow:
        gl = t.copy().filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(gl, (int(40 + w / 2 - t.width / 2), int(40 + h / 2 - t.height / 2)))
    im.alpha_composite(t, (int(40 + w / 2 - t.width / 2), int(40 + h / 2 - t.height / 2)))
    d.ellipse((40 + w - 34, 40 + 14, 40 + w - 20, 40 + 28), fill=(255, 60, 50))
    return im

def save(c, name):
    p = OUT + name + ".png"; c.convert("RGB").save(p); print(p); return p

# ---------- 1: NOT AGAIN ----------
c = night_bg(cx=930)
mn = moon(70, (255, 244, 200)); place(c, mn, 1180, 90)
bub = load(PK + "07_Brand/bubble_thought.png", width=470, flip=True).copy()
mem = load(f"{PK}03_Poses/Batata/Batata_pose_wave.png", height=150)
bub.alpha_composite(mem, (int(bub.width * 0.5 - mem.width / 2), 18))
place(c, bub, 1010, 150, rot=4)
place(c, pose("Batata", "facepalm", 560), 960, 455)
place(c, clock("3:00", 250), 250, 610, rot=-6)
place(c, headline("NOT", "AGAIN", 110, 190), 330, 255, rot=-4)
tag(c); save(c, "thumb_1_NOT_AGAIN")

# ---------- 2: CRINGE O'CLOCK ----------
c = night_bg(c1=(150, 30, 60), c2=(30, 10, 40), cx=420, cy=430)
place(c, clock("3:00", 520), 430, 480, rot=-5)
place(c, char("Batata", "shocked", 560), 1040, 430, rot=6)
place(c, headline("CRINGE", "O'CLOCK", 96, 140), 450, 160, rot=-3)
tag(c); save(c, "thumb_2_CRINGE_OCLOCK")

# ---------- 3: BRAIN, STOP. ----------
c = night_bg(c1=(30, 46, 160), c2=(8, 10, 40), cx=380, cy=380)
ui = Image.new("RGBA", (640, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(ui)
d.rounded_rectangle((0, 0, 639, 419), 26, fill=(14, 14, 18), outline=NAVY, width=8)
ui.alpha_composite(text("BRAIN+", 46, RED2), (28, 16))
yy = np.linspace(0, 1, 250)[:, None, None]
tile = Image.fromarray((np.array((120, 60, 190)) * (1 - yy) + np.array((230, 70, 110)) * yy).repeat(560, axis=1).astype(np.uint8), "RGB").convert("RGBA")
ui.alpha_composite(tile, (40, 90))
tt = text("THE WAVE", 64, WHITE, stroke=6, stroke_fill=(0, 0, 0)); ui.alpha_composite(tt, (int(320 - tt.width / 2), 150))
d.rectangle((40, 330, 600, 344), fill=(70, 70, 80)); d.rectangle((40, 330, 470, 344), fill=RED2)
ui.alpha_composite(text("NOW PLAYING  ·  for the 900th time", 22, (200, 200, 210)), (40, 360))
place(c, ui, 400, 430, rot=-4)
place(c, char("Batata", "angry", 540), 1010, 430)
place(c, headline("", "BRAIN, STOP.", 0, 130), 640, 110, rot=-2)
tag(c); save(c, "thumb_3_BRAIN_STOP")

# ---------- 4: 4 LEVELS DEEP ----------
import scenes as SC
SC.W, SC.H = 1920, 1080
c = night_bg(c1=(40, 60, 170), c2=(8, 10, 40), rays=False, cx=640, cy=200)
ice = SC.iceberg_layer().resize((1280, 720), Image.LANCZOS)
c.alpha_composite(ice.crop((0, 0, 1280, 720)) if ice.size == (1280, 720) else ice)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((300, 470, 640, 720), fill=(255, 210, 80, 120))
c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
place(c, char("Batata", "shocked", 300), 470, 580)
place(c, pill("LEVEL 4", 40, fill=RED2, tc=WHITE), 700, 640, rot=-6)
place(c, headline("4 LEVELS", "DEEP", 100, 190), 1010, 290, rot=-3)
tag(c); save(c, "thumb_4_4_LEVELS_DEEP")

# ---------- 5: THEY BARELY NOTICED ----------
c = night_bg(c1=(40, 30, 110), c2=(6, 6, 24), rays=False, cx=420, cy=300)
sp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sp)
d.polygon([(330, -20), (510, -20), (700, 720), (140, 720)], fill=(255, 245, 200, 70))
sp = sp.filter(ImageFilter.GaussianBlur(18)); c.alpha_composite(sp)
d = ImageDraw.Draw(c); d.ellipse((190, 620, 650, 700), fill=(255, 245, 200, 90))
place(c, char("Batata", "shocked", 500), 420, 410)
dim = lambda s: Image.fromarray((np.asarray(s).astype(np.float32) * np.array([0.55, 0.55, 0.7, 1])).astype(np.uint8), "RGBA")
place(c, dim(char("Tamatem", "sleepy", 300)), 900, 560)
place(c, dim(char("Dorra", "deadpan", 300, flip=True)), 1140, 560)
place(c, headline("THEY BARELY", "NOTICED", 76, 140), 960, 170, rot=-3)
tag(c); save(c, "thumb_5_THEY_BARELY_NOTICED")
