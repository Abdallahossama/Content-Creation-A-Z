"""File 18 (Hassan al-Banna's last hours, Cairo, 12 February 1949) thumbnails, Hakawi style: one real scene in a cinematic duotone (the 1946
Cairo street, Nationaal Archief CC0), Banna's face ghosted (PD-Egypt), 1-3 words on black / red blocks, a yellow tab.
Never in a thumbnail (research/assets.md): the Brotherhood emblem, newspaper scans, any 2026 politician, Morsi, CC BY-SA.
  A  WHO ARE / THEY?          (pairs with "Trump Tied El-Sayed to the Muslim Brotherhood. The 1949 File")
  B  WHO SHOT / HIM?          (pairs with "El-Sayed and the Muslim Brotherhood: The 98-Year Record")
  C  CAR / 9979               (pairs with "The Muslim Brotherhood Founder's Last 4 Hours, Cairo 1949")
  TH_COLOUR=1 uv run --no-project --with pillow --with numpy python thumbs_mb18.py"""
import sys, os
os.environ["TH_COLOUR"] = "1"
from PIL import Image, ImageDraw, ImageEnhance
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/13_goering_last_night")
from thumbs_hakawi import src, cover, vign, block, paste_faded, TW, TH, YEL, WHITE, RED
from thumbs_goering import bw
EP = "18_muslim_brotherhood"; ROOT = "D:/why habibi/_newchannel/18_muslim_brotherhood/"; OUT = ROOT + "export/thumbnails/"

def street(z=1.05, cx=0.78, cy=0.6, bright=0.8):
    im = src(EP, "A21_"); W0, H0 = im.size; im = im.crop((0, int(H0 * 0.12), int(W0 * 0.64), int(H0 * 0.95)))      # a face peeks from behind the right-hand wall (x 0.71): cut away (no-women rule)
    c = bw(cover(im, TW, TH, cx=cx, cy=cy, z=z)); return ImageEnhance.Brightness(c).enhance(bright).convert("RGBA")
def face(c, prefix, box, h, x, y, left=300, contrast=1.15):
    im = src(EP, prefix).convert("RGB"); W0, H0 = im.size
    f = bw(im.crop((int(W0 * box[0]), int(H0 * box[1]), int(W0 * box[2]), int(H0 * box[3]))), contrast=1.35, bright=1.05)
    f = ImageEnhance.Contrast(f).enhance(contrast); s = h / f.height; f = f.resize((int(f.width * s), h), Image.LANCZOS)
    paste_faded(c, f, x if x >= 0 else TW - f.width + 40, y, left=left)

def A():
    c = street(); face(c, "A2_", (0.08, 0.04, 0.95, 0.98), 760, -1, -20, left=340); c = vign(c, 0.4).convert("RGBA")
    block(c, "WHO ARE", 44, 300, 128)
    block(c, "THEY?", 44, 460, 150, fill=WHITE, bg=RED + (255,))
    block(c, "FOUNDED 1928  ·  SHOT 1949", 44, 96, 50, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def B():
    c = street(z=1.12, cx=0.7); face(c, "A1_", (0.05, 0.02, 0.95, 0.9), 740, -1, -10, left=320); c = vign(c, 0.4).convert("RGBA")
    block(c, "WHO SHOT", 44, 300, 128)
    block(c, "HIM?", 44, 460, 150, fill=WHITE, bg=RED + (255,))
    block(c, "CAIRO  ·  12 FEB 1949  ·  8:30 PM", 44, 96, 50, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def plate(w=520, h=200):
    p = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(236, 230, 214, 255), outline=(20, 20, 20, 255), width=10)
    import lastkit as L
    d.text((w // 2, h // 2 + 6), "9979", font=L.font(L.COND, 170), fill=(18, 18, 18), anchor="mm")
    return p.rotate(-4, expand=True, resample=Image.BICUBIC)

def C():
    c = street(z=1.1, cx=0.74, bright=0.7); face(c, "A2_", (0.08, 0.04, 0.95, 0.98), 700, -1, 20, left=320); c = vign(c, 0.45).convert("RGBA")
    pl = plate(); c.alpha_composite(pl, (60, 250))
    block(c, "THE GETAWAY CAR", 44, 520, 84, fill=WHITE, bg=RED + (255,))
    block(c, "WHO RENTED IT?", 44, 96, 50, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def D():   # owner, 31 Oct: El-Sayed on the thumbnail. Him ALONE (US Senate photo, PD), framed as the claim under check; never merged with Banna
    import lastkit as L
    cap = cover(src(EP, "A52_").convert("RGB"), TW, TH, cx=0.5, cy=0.5, z=1.05)
    c = ImageEnhance.Brightness(ImageEnhance.Color(cap).enhance(0.8)).enhance(0.55).convert("RGBA")
    f = elsayed(420, 600)                                                                       # him alone, face centred
    from thumbs_hakawi import card
    cd = card(f, 400, rot=3, border=14).convert("RGBA"); c = vign(c, 0.35).convert("RGBA"); c.alpha_composite(cd, (TW - cd.width - 70, 40))   # a photo print, not a fade
    st = Image.new("RGBA", (420, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    d.rectangle((4, 4, 415, 115), outline=(214, 28, 28, 255), width=10); d.text((210, 62), "ACCUSED", font=L.font(L.COND, 92), fill=(214, 28, 28), anchor="mm")
    st = st.rotate(8, expand=True, resample=Image.BICUBIC); c.alpha_composite(st, (TW - 560, 560))
    block(c, "IS IT", 44, 300, 128)
    block(c, "TRUE?", 44, 460, 150, fill=WHITE, bg=RED + (255,))
    block(c, "FACT-CHECKED  ·  1928 → 2026", 44, 96, 50, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def elsayed(w, h):
    """El-Sayed alone (US Senate photo, PD), his face CENTRED (owner, 31 Oct): the crop stops before the blurred head behind him (x < 0.545),
    so the missing left side is filled with a soft extension of the wood wall, never with another person"""
    from PIL import ImageFilter
    im = src(EP, "A50_").convert("RGB"); W0, H0 = im.size
    cr = im.crop((int(W0 * 0.545), int(H0 * 0.03), int(W0 * 0.82), int(H0 * 0.75))); fx = (0.62 * W0 - 0.545 * W0) / cr.width   # face centre in the crop
    ext = int(cr.width * (1 - 2 * fx)) if fx < 0.5 else 0
    can = Image.new("RGB", (cr.width + ext, cr.height)); edge = cr.crop((0, 0, 6, cr.height)).resize((ext + 6, cr.height))
    can.paste(edge.filter(ImageFilter.GaussianBlur(14)), (0, 0)); can.paste(cr, (ext, 0))
    m = Image.new("L", (40, cr.height), 0); [m.putpixel((x, y), int(255 * x / 39)) for x in range(40) for y in range(cr.height)]
    can.paste(cr.crop((0, 0, 40, cr.height)), (ext, 0), m)
    out = cover(can, w, h, cx=0.5, cy=0.42).filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    return ImageEnhance.Contrast(out).enhance(1.08)

def split(top_text, tag_text=None, verdict=True):
    import lastkit as L
    c = Image.new("RGBA", (TW, TH), (0, 0, 0, 255)); half = TW // 2
    im = src(EP, "A1_").convert("RGB"); W0, H0 = im.size
    left = bw(cover(im.crop((int(W0 * 0.05), 0, int(W0 * 0.95), int(H0 * 0.92))), half, TH, cx=0.5, cy=0.4), contrast=1.35, bright=1.0)
    c.alpha_composite(left.convert("RGBA"), (0, 0)); c.alpha_composite(elsayed(half, TH).convert("RGBA"), (half, 0))
    c = vign(c, 0.3).convert("RGBA"); d = ImageDraw.Draw(c)
    d.rectangle((half - 5, 0, half + 5, TH), fill=YEL + (255,))                                   # a hard divider: two people, two eras
    block(c, "1949", 30, 660, 46, fill=(0, 0, 0), bg=YEL + (255,)); block(c, "2026", TW - 150, 60, 46, fill=(0, 0, 0), bg=YEL + (255,))
    f = L.font(L.COND, 96); tw = int(d.textlength(top_text, font=f)) + 48; block(c, top_text, half - tw // 2, 60, 96)
    if verdict:
        st = Image.new("RGBA", (470, 128), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle((5, 5, 464, 122), fill=(0, 0, 0, 140), outline=(226, 30, 30, 255), width=9)
        sd.text((235, 40), "FACT-CHECK:", font=L.font(L.COND, 40), fill=(255, 255, 255), anchor="mm")
        sd.text((235, 88), "PANTS ON FIRE", font=L.font(L.COND, 62), fill=(236, 40, 40), anchor="mm")
        st = st.rotate(4, expand=True, resample=Image.BICUBIC); c.alpha_composite(st, (half + 80, 565))
    if tag_text: block(c, tag_text, half + 30, 640, 40, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def cork(w=TW, h=TH):
    """a procedural cork board (a drawn graphic, not a photo)"""
    import numpy as np
    from PIL import ImageFilter
    rng = np.random.default_rng(7); a = np.zeros((h, w, 3), np.float32) + np.array([128, 88, 52], np.float32)
    for s, k in ((2, 26), (5, 18), (13, 12)):
        n = rng.normal(0, 1, (h // s + 1, w // s + 1)); n = np.kron(n, np.ones((s, s)))[:h, :w]; a += n[..., None] * k
    dots = rng.random((h, w)) < 0.012; a[dots] *= 0.55
    im = Image.fromarray(a.clip(0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))
    return vign(ImageEnhance.Brightness(im).enhance(0.62), 0.55).convert("RGBA")

def pin(d, x, y, r=13):
    d.ellipse((x - r + 3, y - r + 5, x + r + 3, y + r + 5), fill=(0, 0, 0, 120))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 24, 24, 255)); d.ellipse((x - r // 2 - 2, y - r // 2 - 3, x - 1, y - 2), fill=(255, 140, 140, 255))

def string(d, p0, p1, sag=18, gap=None):
    """red string with a slight sag; gap=(u0, u1) leaves it CUT between those fractions"""
    pts = [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u + sag * 4 * u * (1 - u)) for u in [i / 30 for i in range(31)]]
    segs = [pts] if not gap else [pts[:int(gap[0] * 30) + 1], pts[int(gap[1] * 30):]]
    for sg in segs:
        d.line(sg, fill=(0, 0, 0, 110), width=7); d.line(sg, fill=(214, 26, 26, 255), width=4)

def qcard(w=250, h=310):
    """the unknown man: a silhouette card with a question mark (graphic)"""
    import lastkit as L
    im = Image.new("RGB", (w, h), (52, 50, 48)); d = ImageDraw.Draw(im)
    d.ellipse((w * 0.3, h * 0.16, w * 0.7, h * 0.52), fill=(18, 18, 18)); d.rounded_rectangle((w * 0.12, h * 0.52, w * 0.88, h * 1.1), 60, fill=(18, 18, 18))
    d.text((w / 2, h * 0.42), "?", font=L.font(L.COND, int(h * 0.42)), fill=(236, 230, 214), anchor="mm")
    return im

def G():   # the detective board (owner's reference, 31 Oct): the real case on strings; El-Sayed at the edge, his string CUT: "AP: NO EVIDENCE"
    from thumbs_hakawi import card
    c = cork(); d = ImageDraw.Draw(c)
    ban = card(bw(src(EP, "A2_").convert("RGB"), contrast=1.3), 300, rot=-3, border=12).convert("RGBA")
    far = card(bw(src(EP, "A29_").convert("RGB"), contrast=1.25), 200, rot=4, border=10).convert("RGBA")
    unk = card(qcard(), 200, rot=-2, border=10).convert("RGBA")
    sid = card(elsayed(300, 380), 230, rot=3, border=10).convert("RGBA")
    pl = plate(340, 130)
    P = {"ban": (50, 100), "far": (430, 40), "unk": (690, 70), "pl": (410, 360), "sid": (TW - 280, 290)}
    for k in ("ban", "far", "unk", "pl", "sid"): c.alpha_composite({"ban": ban, "far": far, "unk": unk, "pl": pl, "sid": sid}[k], P[k])
    d = ImageDraw.Draw(c)
    hb, hf, hu, hp, hs = (200, 112), (530, 52), (790, 82), (580, 372), (TW - 165, 302)
    string(d, hb, hp, sag=24); string(d, hp, hu, sag=14); string(d, hu, hf, sag=10); string(d, hb, hf, sag=30)
    # El-Sayed: pinned apart, NO string to the case (a string, even a cut one, read as a link: it is not)
    for p in (hb, hf, hu, hp, hs): pin(d, *p)
    import lastkit as L
    note = Image.new("RGBA", (250, 96), (255, 214, 60, 255)); nd = ImageDraw.Draw(note)
    nd.text((125, 30), "2026 CLAIM. AP:", font=L.font(L.COND, 32), fill=(20, 20, 20), anchor="mm"); nd.text((125, 66), "NO EVIDENCE", font=L.font(L.COND, 40), fill=(20, 20, 20), anchor="mm")
    note = note.rotate(-5, expand=True, resample=Image.BICUBIC); c.alpha_composite(note, (TW - 300, 600))
    c = vign(c, 0.25).convert("RGBA")
    block(c, "WHO GAVE", 30, 560, 74); block(c, "THE ORDER?", 30, 650, 74, fill=WHITE, bg=RED + (255,))
    return c

def embers(c, n=70, seed=5, box=(0, 0, TW, TH)):
    """drifting embers: small warm dots with a glow (a drawn effect)"""
    import numpy as np
    from PIL import ImageFilter
    rng = np.random.default_rng(seed); lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y = rng.uniform(box[0], box[2]), rng.uniform(box[1], box[3]); r = rng.uniform(1.5, 4.5); a = int(rng.uniform(120, 255))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, int(rng.uniform(120, 190)), 60, a))
    glow = lay.filter(ImageFilter.GaussianBlur(6)); c.alpha_composite(glow); c.alpha_composite(glow); c.alpha_composite(lay)

def grade_tealred(im, k=0.35):
    """teal shadows, warm highlights (the reference look), on an RGB image"""
    import numpy as np
    a = np.asarray(im.convert("RGB"), np.float32) / 255; lum = a.mean(axis=2, keepdims=True)
    teal, warm = np.array([0.05, 0.32, 0.36]), np.array([1.0, 0.62, 0.38])
    out = a * (1 - k) + (teal * (1 - lum) + warm * lum) * lum * k * 2.0
    return Image.fromarray((out.clip(0, 1) * 255).astype("uint8"))

def I(bg="cork", rim=(255, 90, 40), head=("WHY", "HIM?"), note=("AP: NO EVIDENCE", "OF ANY LINK"), note_xy=(TW - 700, 540), board=True, scale=790, glow_bg=(230, 40, 30)):
    """owner's pick, 31 Oct: the 1949 case board + El-Sayed's CUTOUT on top (MediaPipe selfie segmentation of the PD Senate photo, build/elsayed_cut.png;
    the people behind him are outside the mask), a rim light and a shadow, only text above him. Headline never 'who gave the order?' beside his face.
    The defaults are the approved version; the arguments make the variations."""
    from thumbs_hakawi import card
    from PIL import ImageFilter
    import numpy as np, lastkit as L
    if bg == "cork": c = cork()
    else: c = street(z=1.05, cx=0.75, bright=0.5)
    if board:
        ban = card(bw(src(EP, "A2_").convert("RGB"), contrast=1.3), 250, rot=-4, border=11).convert("RGBA")
        far = card(bw(src(EP, "A29_").convert("RGB"), contrast=1.25), 175, rot=4, border=9).convert("RGBA")
        unk = card(qcard(), 170, rot=-2, border=9).convert("RGBA")
        pl = plate(300, 115)
        for im, p in ((ban, (40, 330)), (far, (330, 300)), (unk, (520, 330)), (pl, (300, 555))): c.alpha_composite(im, p)
        d = ImageDraw.Draw(c); hb, hf, hu, hp = (165, 342), (418, 310), (605, 342), (450, 565)
        string(d, hb, hp, sag=22); string(d, hp, hu, sag=14); string(d, hu, hf, sag=8); string(d, hb, hf, sag=22)
        for p in (hb, hf, hu, hp): pin(d, *p)
    else:                                                                                          # Banna ghosted large instead of the board
        g = bw(src(EP, "A2_").convert("RGB"), contrast=1.2); s_ = 700 / g.height; g = g.resize((int(g.width * s_), 700), Image.LANCZOS).convert("RGBA")
        m = Image.new("L", g.size, 0); ImageDraw.Draw(m).ellipse((int(g.width * 0.1), int(g.height * 0.05), int(g.width * 0.9), int(g.height * 0.98)), fill=120)
        g.putalpha(m.filter(ImageFilter.GaussianBlur(45))); c.alpha_composite(g, (230, 30))
    c = Image.fromarray(np.asarray(grade_tealred(c.convert("RGB"), 0.25))).convert("RGBA")
    rl = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); ImageDraw.Draw(rl).ellipse((TW - 700, 40, TW - 300, TH - 40), fill=glow_bg + (120,)); c.alpha_composite(rl.filter(ImageFilter.GaussianBlur(70)))
    leak = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); ImageDraw.Draw(leak).polygon([(TW * 0.40, 0), (TW * 0.52, 0), (TW * 0.30, TH), (TW * 0.18, TH)], fill=(255, 170, 80, 40))
    c.alpha_composite(leak.filter(ImageFilter.GaussianBlur(40))); embers(c, 110, box=(0, 0, TW, TH)); c = vign(c, 0.3).convert("RGBA")
    cut = Image.open(ROOT + "build/elsayed_cut.png").convert("RGBA"); cut = cut.crop((0, 0, cut.width, int(cut.height * 0.885)))
    s_ = scale / cut.height; cut = cut.resize((int(cut.width * s_), scale), Image.LANCZOS)
    rgb = grade_tealred(ImageEnhance.Contrast(cut.convert("RGB")).enhance(1.1), 0.15).filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    cut = Image.merge("RGBA", (*rgb.split(), cut.split()[3])); x0, y0 = TW - cut.width + 30, TH - cut.height + 40 + (scale - 790) // 2
    a_ = cut.split()[3]
    glow = Image.new("RGBA", cut.size, rim + (0,)); glow.putalpha(a_.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(14)))
    shadow = Image.new("RGBA", cut.size, (0, 0, 0, 0)); shadow.putalpha(a_.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.8)))
    c.alpha_composite(shadow, (x0 - 34, y0 + 10)); c.alpha_composite(glow, (x0, y0)); c.alpha_composite(cut, (x0, y0))
    block(c, head[0], 36, 110, 140); block(c, head[1], 36, 255, 140, fill=WHITE, bg=RED + (255,))
    st = Image.new("RGBA", (520, 150), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)                     # owner, 31 Oct: the fair note must read at phone size
    sd.rectangle((0, 0, 519, 149), fill=YEL + (255,)); sd.text((260, 44), note[0], font=L.font(L.COND, 60), fill=(15, 15, 15), anchor="mm")
    sd.text((260, 110), note[1], font=L.font(L.COND, 60), fill=(15, 15, 15), anchor="mm")
    st = st.rotate(-3, expand=True, resample=Image.BICUBIC); c.alpha_composite(st, note_xy)
    block(c, "1949", 40, 670, 40, fill=(0, 0, 0), bg=YEL + (255,)); block(c, "2026", TW - 160, 50, 44, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def I2(): return I(rim=(60, 200, 255), glow_bg=(30, 120, 200))                                           # cold blue rim light
def I3(): return I(head=("THE", "CLAIM"), note=("FACT-CHECK:", "PANTS ON FIRE"))                         # the fact-check verdict
def I4(): return I(bg="street", board=False)                                                              # 1946 Cairo street + Banna ghosted
def I5(): return I(head=("WHY", "HIM?"), note=("HE SAYS: NEVER", "A MEMBER"))                             # his own answer on the note

def J():   # owner, 31 Oct, after the creator-stack thumbnail rules: TWO focal points only (his face + "WHY HIM?"), headline 150-200 px with an
           # outline, nothing in the bottom corners, a clean edge (no haze on his face); Banna only as a faint ghost for context (1949)
    from PIL import ImageFilter
    import lastkit as L
    bg = street(z=1.05, cx=0.75, bright=0.42); c = Image.fromarray(__import__("numpy").asarray(grade_tealred(bg.convert("RGB"), 0.35))).convert("RGBA")
    g = bw(src(EP, "A2_").convert("RGB"), contrast=1.2); s_ = 640 / g.height; g = g.resize((int(g.width * s_), 640), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", g.size, 0); ImageDraw.Draw(m).ellipse((int(g.width * 0.12), int(g.height * 0.06), int(g.width * 0.88), int(g.height * 0.98)), fill=80)
    g.putalpha(m.filter(ImageFilter.GaussianBlur(45))); c.alpha_composite(g, (330, 40))           # Banna, ghosted (soft oval, no box edge): the 1949 context
    im = src(EP, "A50_").convert("RGB"); W0, H0 = im.size
    raw = im.crop((int(W0 * 0.545), int(H0 * 0.03), int(W0 * 0.86), int(H0 * 0.75)))                 # him alone
    s_ = TH / raw.height; raw = raw.resize((int(raw.width * s_), TH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
    face = ImageEnhance.Contrast(ImageEnhance.Color(raw).enhance(1.05)).enhance(1.12)
    paste_faded(c, face, TW - face.width, 0, left=110); embers(c, 40, box=(0, 0, TW - face.width, TH)); c = vign(c, 0.28).convert("RGBA")
    d = ImageDraw.Draw(c)
    def big(txt, x, y, size, fill, box=None):
        f = L.font(L.COND, size); w = d.textlength(txt, font=f)
        if box: d.rectangle((x - 18, y - size * 0.62, x + w + 18, y + size * 0.5), fill=box)
        d.text((x, y), txt, font=f, fill=fill, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
    big("WHY", 50, 165, 190, (255, 255, 255)); big("HIM?", 50, 345, 190, (255, 255, 255), box=RED + (255,))
    note = Image.new("RGBA", (470, 128), YEL + (255,)); nd = ImageDraw.Draw(note)
    nd.text((235, 40), "AP: NO EVIDENCE", font=L.font(L.COND, 54), fill=(15, 15, 15), anchor="mm"); nd.text((235, 96), "OF ANY LINK", font=L.font(L.COND, 54), fill=(15, 15, 15), anchor="mm")
    c.alpha_composite(note.rotate(-2, expand=True, resample=Image.BICUBIC), (48, 470))
    return c

def K():   # owner's reference (31 Oct, torn burning paper): Banna's face through a torn, burning 1940s US Army map of Cairo (PD), "WHO SHOT HIM?"
    import numpy as np, lastkit as L
    from PIL import ImageFilter
    c = Image.new("RGBA", (TW, TH), (12, 10, 9, 255))
    face = src(EP, "A1_").convert("RGB"); W0, H0 = face.size
    face = bw(face.crop((int(W0 * 0.08), 0, int(W0 * 0.92), int(H0 * 0.86))), contrast=1.4, bright=1.08)
    s_ = 760 / face.height; face = face.resize((int(face.width * s_), 760), Image.LANCZOS).convert("RGBA")
    c.alpha_composite(face, ((TW - face.width) // 2, -10))
    mp = src(EP, "A48_").convert("RGB"); W0, H0 = mp.size
    mp = mp.crop((int(W0 * 0.30), int(H0 * 0.25), int(W0 * 0.70), int(H0 * 0.75))).resize((TW, TH), Image.LANCZOS)
    mp = ImageEnhance.Color(ImageEnhance.Brightness(mp).enhance(0.92)).enhance(0.75)
    rng = np.random.default_rng(11); ys = np.arange(0, TH + 1, 12)
    def jag(x0, amp=38): return [(x0 + rng.normal(0, amp * 0.35) + amp * np.sin(y / 70.0), y) for y in ys]
    L_edge, R_edge = jag(TW * 0.36), jag(TW * 0.64)
    for edge, side in ((L_edge, "L"), (R_edge, "R")):
        poly = ([(0, 0)] + edge + [(0, TH)]) if side == "L" else ([(TW, 0)] + edge + [(TW, TH)])
        m = Image.new("L", (TW, TH), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
        piece = mp.convert("RGBA"); piece.putalpha(m)
        char = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); cd = ImageDraw.Draw(char)                  # the burnt band along the tear
        cd.line(edge, fill=(40, 22, 10, 255), width=46); char = char.filter(ImageFilter.GaussianBlur(16)); ca = np.asarray(char).copy(); ca[..., 3] = (ca[..., 3] * (np.asarray(m) / 255)).astype("uint8")
        sh = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon(poly, fill=(0, 0, 0, 200)); c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
        c.alpha_composite(piece); c.alpha_composite(Image.fromarray(ca))
        glow = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.line(edge, fill=(255, 120, 20, 230), width=12); c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
        hot = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); ImageDraw.Draw(hot).line(edge, fill=(255, 220, 120, 255), width=3); c.alpha_composite(hot)
    embers(c, 90, box=(TW * 0.25, 0, TW * 0.75, TH)); c = vign(c, 0.35).convert("RGBA"); d = ImageDraw.Draw(c)
    f = L.font(L.COND, 150); d.text((TW // 2, 600), "WHO SHOT HIM?", font=f, fill=YEL, anchor="mm", stroke_width=9, stroke_fill=(0, 0, 0))
    block(c, "CAIRO  ·  12 FEB 1949", 40, 70, 44, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def H():   # the hanging photos (owner's reference, 31 Oct): Banna | ? | King Farouk on a line, no 2026 politician
    from thumbs_hakawi import card
    c = street(z=1.05, cx=0.78, bright=0.55); d = ImageDraw.Draw(c)
    d.line([(0, 70), (TW // 2, 95), (TW, 70)], fill=(30, 22, 16, 255), width=5)
    for i, (im, x) in enumerate(((bw(src(EP, "A2_").convert("RGB"), contrast=1.3), 120), (qcard(), 500), (bw(src(EP, "A26_").convert("RGB"), contrast=1.25), 880))):
        cd = card(im, 270, rot=(-3, 1, 3)[i], border=12).convert("RGBA"); c.alpha_composite(cd, (x, 92))
        d = ImageDraw.Draw(c); d.rectangle((x + 118, 72, x + 150, 128), fill=(205, 170, 110, 255), outline=(60, 40, 20, 255), width=3)   # a wooden peg
    import lastkit as L
    for txt, x in (("HASSAN AL-BANNA", 120), ("WHO GAVE THE ORDER?", 500), ("KING FAROUK", 880)):
        block(c, txt, x + 6, 520, 34, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "SHOT IN CAIRO", 30, 640, 66, fill=WHITE, bg=RED + (255,))
    return c

def F():   # split, "WHY HIM?", the AP's finding on his side
    return split("WHY HIM?", tag_text="AP: NO EVIDENCE OF ANY LINK", verdict=False)

def E():   # owner, 31 Oct: "half Abdul, half el-Banna": two SEPARATE photos side by side (never one blended face), with the fact-check verdict
    return split("THE CLAIM")

OPTIONS = [("I2_BLUE_RIM", I2, "The Muslim Brotherhood, From 1928 to the Michigan Race"), ("I3_THE_CLAIM", I3, "The Muslim Brotherhood, From 1928 to the Michigan Race"),
           ("I4_CAIRO_STREET", I4, "The Muslim Brotherhood, From 1928 to the Michigan Race"), ("I5_HE_SAYS", I5, "The Muslim Brotherhood, From 1928 to the Michigan Race"),
           ("K_TORN_MAP", K, "The Muslim Brotherhood Founder's Last 4 Hours, Cairo 1949"),
           ("J_WHY_HIM_CLEAN", J, "The Muslim Brotherhood, From 1928 to the Michigan Race"),
           ("I_WHY_HIM_BIG", I, "The Muslim Brotherhood, From 1928 to the Michigan Race"),
           ("G_THE_BOARD", G, "The Muslim Brotherhood, From 1928 to the Michigan Race"),
           ("H_HANGING_PHOTOS", H, "Who Are the Muslim Brotherhood? The 1949 File"),
("E_THE_CLAIM", E, "Trump Tied El-Sayed to the Muslim Brotherhood. The 1949 File"),
           ("F_WHY_HIM", F, "El-Sayed and the Muslim Brotherhood: The 98-Year Record"),
           ("D_IS_IT_TRUE", D, "The 2026 Muslim Brotherhood Claim on El-Sayed, Fact-Checked"),
           ("A_WHO_ARE_THEY", A, "The Muslim Brotherhood, From 1928 to the Michigan Race"),
           ("B_WHO_SHOT_HIM", B, "The Muslim Brotherhood Founder's Last 4 Hours, Cairo 1949"),
           ("C_CAR_9979", C, "A Boy Shouted 4 Numbers. They Led to a Cairo Police Chief")]
if __name__ == "__main__":
    import lastkit as L
    os.makedirs(OUT, exist_ok=True); want = [a for a in sys.argv[1:]]
    tw, th = TW // 2, TH // 2; S = Image.new("RGB", (2 * tw + 60, 3 * (th + 70) + 20), (25, 25, 25)); d = ImageDraw.Draw(S)
    for k, (name, fn, title) in enumerate(OPTIONS):
        if want and name[0] not in want: continue
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90)
        x, y = 20 + (k % 2) * (tw + 20), 20 + (k // 2) * (th + 70)
        S.paste(im.resize((tw, th)), (x, y)); d.text((x, y + th + 8), f"{k + 1}. {title}", font=L.font(L.COND, 26), fill=(255, 210, 60))
    S.save(OUT + "_sheet_6_options.jpg", quality=88); print(OUT + "_sheet_6_options.jpg")
