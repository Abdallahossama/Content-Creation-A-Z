"""Scene definitions. Every scene is (name, src_start, src_end, draw_fn).
Cue times are written in VO-source seconds and converted to scene-local time with L()."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw
from gfxlib import *

SCENES = {}

def scene(name, s0, s1):
    def deco(fn):
        SCENES[name] = (s0, s1, fn)
        return fn
    return deco

# ============ ICEBERG ============
IX, WL = 700, 250
BANDS = [(260, 420), (420, 580), (580, 740), (740, 925)]
LEVELS = [("LEVEL 1", "The Sleepless Night"), ("LEVEL 2", "The Replay"),
          ("LEVEL 3", "Sleep vs. Cringe"), ("LEVEL 4", "Why 3AM?")]
_ice = {}

def iceberg_layer():
    """2x-res opaque frame: bg + water + iceberg (no labels)."""
    if "img" in _ice:
        return _ice["img"]
    S = 2
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    # water gradient
    yy = np.linspace(0, 1, (H - WL) * S)[:, None]
    top = np.array([38, 62, 168]); bot = np.array([8, 11, 48])
    g = (top * (1 - yy) + bot * yy)
    water = np.zeros(((H - WL) * S, W * S, 4), np.uint8)
    water[..., :3] = np.repeat(g[:, None, :], W * S, axis=1).reshape((H - WL) * S, W * S, 3)
    water[..., 3] = 240
    im.alpha_composite(Image.fromarray(water, "RGBA"), (0, WL * S))
    # body
    body = [(IX - 200, WL), (IX - 330, 380), (IX - 420, 560), (IX - 385, 720), (IX - 300, 860), (IX - 140, 925),
            (IX + 60, 940), (IX + 250, 892), (IX + 380, 760), (IX + 432, 580), (IX + 360, 400), (IX + 190, WL)]
    body = [(x * S, y * S) for x, y in body]
    mask = Image.new("L", (W * S, H * S), 0); ImageDraw.Draw(mask).polygon(body, fill=215)
    yy = np.linspace(0, 1, H * S)[:, None]
    ctop = np.array([150, 214, 255]); cbot = np.array([34, 50, 150])
    t2 = np.clip((yy - WL / H) / (1 - WL / H), 0, 1)
    gc = ctop * (1 - t2) + cbot * t2
    bimg = np.zeros((H * S, W * S, 4), np.uint8)
    bimg[..., :3] = np.repeat(gc[:, None, :], W * S, axis=1).reshape(H * S, W * S, 3)
    bl = Image.fromarray(bimg, "RGBA"); bl.putalpha(mask)
    im.alpha_composite(bl)
    d = ImageDraw.Draw(im)
    d.line(body + [body[0]], fill=NAVY, width=7 * S // 2, joint="curve")
    # tip
    tip = [(IX - 200, WL), (IX - 120, 170), (IX - 60, 140), (IX - 10, 92), (IX + 40, 120), (IX + 110, 178), (IX + 190, WL)]
    tip = [(x * S, y * S) for x, y in tip]
    d.polygon(tip, fill=(240, 250, 255), outline=NAVY, width=7 * S // 2)
    d.polygon([(IX * S - 10 * S, 92 * S), (IX * S + 40 * S, 120 * S), (IX * S + 5 * S, 200 * S), (IX * S - 60 * S, 140 * S)], fill=(205, 232, 250))
    # water line
    d.line([(0, WL * S), (W * S, WL * S)], fill=(160, 210, 255), width=4 * S)
    # band separators (dashed)
    for y0, _ in BANDS[1:]:
        for x in range(120, 1820, 40):
            d.line([(x * S, y0 * S), ((x + 22) * S, y0 * S)], fill=(255, 255, 255, 90), width=3 * S)
    _ice["img"] = im
    return im

def ice_frame(z=1.0, cx=W / 2, cy=H / 2):
    S = 2; src = iceberg_layer()
    hw, hh = W / (2 * z), H / (2 * z)
    cx = clamp(cx, hw, W - hw); cy = clamp(cy, hh, H - hh)
    box = (int((cx - hw) * S), int((cy - hh) * S), int((cx + hw) * S), int((cy + hh) * S))
    return src.crop(box).resize((W, H), Image.BILINEAR), (cx, cy, z)

def to_screen(p, cam):
    cx, cy, z = cam
    return ((p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2)

def band_overlay(canvas, cam, cur, dim=150, glow=True):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i, (y0, y1) in enumerate(BANDS):
        a = to_screen((0, y0), cam); b = to_screen((W, y1), cam)
        if i != cur:
            d.rectangle((0, a[1], W, b[1]), fill=(5, 6, 25, dim))
        elif glow:
            d.rectangle((0, a[1], W, b[1]), outline=YEL + (230,), width=6)
    canvas.alpha_composite(ov)

def level_label(i, hot=False):
    tag, title = LEVELS[i]
    p = pill(tag, 38, fill=RED2 if hot else YEL, tc=WHITE if hot else NAVY)
    t = text(title, 44, WHITE, stroke=6, stroke_fill=NAVY)
    im = Image.new("RGBA", (p.width + 24 + t.width, max(p.height, t.height)), (0, 0, 0, 0))
    im.alpha_composite(p, (0, (im.height - p.height) // 2)); im.alpha_composite(t, (p.width + 24, (im.height - t.height) // 2))
    return im

@scene("02_iceberg_overview", 35.98, 38.80)
def s_overview(c, t):
    rise = slide(t, 0.0, 0.4)
    fr, cam = ice_frame()
    fr = fr.copy(); a = fr.getchannel("A").point(lambda v: int(v * rise)); fr.putalpha(a)
    place(c, fr, W / 2, H / 2 + (1 - rise) * 60)
    L = lambda s: s - 35.98
    for i in range(4):
        x = slide(t, 0.05 + i * 0.32, 0.4)
        hot = i == 3 and t >= L(37.86)
        lab = level_label(i, hot)
        by = sum(BANDS[i]) / 2
        place_tl(c, lab, 1110 + (1 - x) * 300, by, alpha=x)
    if t >= L(37.86):
        s = pop(t, L(37.86) + 0.05, 0.35)
        place(c, pill("the disappointing one", 34, fill=WHITE, tc=RED), 1480, 900, s, rot=-4)

def level_card(i, dur, title_lines):
    by = sum(BANDS[i]) / 2
    def draw(c, t):
        zx = ease_in_out(prog(t, 0.0, 0.8))
        z = lerp(1.0, 1.6, zx)
        cx = lerp(W / 2, IX - 340 / 1.6, zx); cy = lerp(H / 2, by, zx)
        fr, cam = ice_frame(z, cx, cy)
        c.alpha_composite(fr)
        band_overlay(c, cam, i, dim=int(150 * zx))
        if i == 3:
            dk = Image.new("RGBA", (W, H), (0, 0, 10, int(90 * zx))); c.alpha_composite(dk)
        # left scrim for legibility
        sc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g = np.zeros((H, W, 4), np.uint8); ramp = np.clip(1 - np.linspace(0, 1, W) / 0.5, 0, 1)
        g[..., 3] = (ramp[None, :] * 170 * zx).astype(np.uint8); c.alpha_composite(Image.fromarray(g, "RGBA"))
        x = slide(t, 0.25, 0.5)
        lv = text(f"LEVEL {i + 1}", 150, YEL, stroke=12, stroke_fill=NAVY, shadow=8)
        place_tl(c, lv, 110 - (1 - x) * 500, 360, alpha=x)
        x2 = slide(t, 0.45, 0.5)
        st = text(title_lines, 74, WHITE, stroke=8, stroke_fill=NAVY, align="left")
        place_tl(c, st, 120 - (1 - x2) * 500, 360 + lv.height / 2 + st.height / 2 + 10, alpha=x2)
    return draw

for _i, (_n, _s0, _s1, _tl) in enumerate([("03_level1", 40.32, 42.10, "THE SLEEPLESS\nNIGHT"),
                                         ("08_level2", 70.16, 72.84, "THE REPLAY"),
                                         ("13_level3", 88.44, 90.06, "SLEEP VS.\nCRINGE"),
                                         ("18_level4", 121.16, 123.14, "WHY 3AM?")]):
    SCENES[_n] = (_s0, _s1, level_card(_i, _s1 - _s0, _tl))

# ============ 01 BRAND REVEAL ============
@scene("01_brand_reveal", 24.96, 33.92)
def s_brand(c, t):
    L = lambda s: s - 24.96
    circle_reveal(c, sunburst(t), t, 0.0, 0.45)
    logo = load(B + "AskHabibi_Logo/AskHabibi_Logo/logo_stacked.png", height=600)
    out_all = slide(t, L(31.30) - 0.05, 0.3)            # everything clears for subscribe
    mv = ease_in_out(prog(t, L(26.68) - 0.1, 0.45))
    ls = pop(t, L(25.48) - 0.12, 0.45) * lerp(1.0, 0.55, mv) * (1 - out_all)
    ly = lerp(450, 255, mv)
    if ls > 0:
        place(c, logo, W / 2, ly + math.sin(t * 2.2) * 4, ls)
    fade_lines = 1 - slide(t, L(29.30), 0.2)
    s1 = pop(t, L(26.68), 0.4) * fade_lines
    place(c, text("MIDNIGHT QUESTIONS.", 96, WHITE, stroke=10, shadow=8), W / 2, 590, s1)
    s2 = pop(t, L(28.06), 0.4) * fade_lines
    place(c, text("ANSWERED.", 140, YEL, stroke=12, shadow=10), W / 2, 735, s2, rot=-3)
    # play button
    pb = pop(t, L(29.30), 0.35) * (1 - out_all)
    if pb > 0:
        press = 1 - 0.12 * math.sin(math.pi * prog(t, L(29.58), 0.22))
        r = 120
        im = Image.new("RGBA", (r * 2 + 30, r * 2 + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((6, 18, 6 + 2 * r, 18 + 2 * r), fill=NAVY)
        d.ellipse((6, 6, 6 + 2 * r, 6 + 2 * r), fill=RED, outline=NAVY, width=8)
        cxp, cyp = 6 + r, 6 + r
        d.polygon([(cxp - 35, cyp - 55), (cxp - 35, cyp + 55), (cxp + 60, cyp)], fill=WHITE)
        place(c, im, W / 2, 650, pb * press)
        ripple(c, W / 2, 650, t, L(29.58), 0.5, 120, 260)
        place(c, text("PRESS PLAY. EAT.", 60, YEL, stroke=8), W / 2, 845, pop(t, L(29.76), 0.35) * (1 - out_all))
    # subscribe
    sb = pop(t, L(31.30), 0.4)
    if sb > 0:
        click = L(32.05)
        press = 1 - 0.07 * math.sin(math.pi * prog(t, click, 0.2))
        wig = math.sin((t - click) * 40) * 4 * max(0, 1 - (t - click) / 0.6) if t > click else 0
        btn = load(PK + "07_Brand/subscribe_button.png", width=760)
        place(c, btn, W / 2, 480, sb * press, rot=wig)
        cx = lerp(1560, 1130, ease_in_out(prog(t, L(31.55), 0.45))); cy = lerp(980, 520, ease_in_out(prog(t, L(31.55), 0.45)))
        place(c, cursor(70), cx + 25, cy + 40, 1.0, alpha=slide(t, L(31.5), 0.15))
        ripple(c, 1130, 520, t, click, 0.45, 30, 140)
        place(c, pill("SUBSCRIBED", 46, fill=GRN, tc=WHITE), W / 2, 680, pop(t, click + 0.1, 0.35))

# ============ 04 STUDY 2007 ============
@scene("04_study_2007", 42.10, 46.88)
def s_study07(c, t):
    L = lambda s: s - 42.10
    place(c, pill("STUDY  ·  2007", 52), W / 2, 130, pop(t, 0.0))
    place(c, text("Brain imaging", 58, WHITE, stroke=6), W / 2, 225, slide(t, 0.15, 0.3))
    # card 1
    s = pop(t, L(43.26))
    if s > 0:
        p = panel(640, 420, fill=WHITE).copy()
        for k, (col, shp) in enumerate([(SKY, "tri"), (GRN, "dot"), (YEL, "sq")]):
            x0 = 95 + k * 165; y0 = 70
            d = ImageDraw.Draw(p); d.rounded_rectangle((x0, y0, x0 + 130, y0 + 130), 24, fill=col, outline=NAVY, width=6)
            cxk, cyk = x0 + 65, y0 + 65
            if shp == "tri": d.polygon([(cxk, cyk - 35), (cxk - 38, cyk + 30), (cxk + 38, cyk + 30)], fill=NAVY)
            if shp == "dot": d.ellipse((cxk - 34, cyk - 34, cxk + 34, cyk + 34), fill=NAVY)
            if shp == "sq": d.rectangle((cxk - 30, cyk - 30, cxk + 30, cyk + 30), fill=NAVY)
        tt = text("LEARN A SET\nOF ITEMS", 50, NAVY); p.alpha_composite(tt, (int(322 - tt.width / 2), 235))
        place(c, p, 540, 540, s)
    ar = Image.new("RGBA", (170, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(ar)
    d.polygon([(8, 42), (100, 42), (100, 10), (162, 60), (100, 110), (100, 78), (8, 78)], fill=YEL, outline=NAVY, width=7)
    place(c, ar, W / 2, 540, pop(t, L(44.60)))
    s = pop(t, L(44.80))
    if s > 0:
        p = panel(640, 420, fill=BLUE).copy()
        m = moon(70); p.alpha_composite(m, (int(322 - m.width / 2), 50))
        d = ImageDraw.Draw(p)
        for (sx, sy) in [(200, 70), (450, 110), (470, 60), (170, 150)]:
            d.polygon(star_pts(sx, sy, 14, 6), fill=WHITE)
        tt = text("STAY AWAKE\nALL NIGHT", 50, WHITE); p.alpha_composite(tt, (int(322 - tt.width / 2), 235))
        place(c, p, 1380, 540, s)
        place(c, char("Batata", "sleepy", 300), 1690, 800 + math.sin(t * 3) * 5, pop(t, L(45.10)))

# ============ 05 BARS 3 DAYS ============
@scene("05_three_days_bars", 46.88, 54.68)
def s_bars(c, t):
    L = lambda s: s - 46.88
    place(c, text("3 DAYS LATER", 92, WHITE, stroke=10, shadow=8), W / 2, 125, pop(t, 0.0))
    ps = slide(t, 0.2, 0.4)
    if ps > 0:
        place(c, panel(1240, 620, fill=WHITE), W / 2, 545 + (1 - ps) * 40, alpha=ps)
    base = 760; maxh = 400
    fade = ease_in_out(prog(t, L(50.14), 0.6))
    held = t >= L(52.44)
    bars = [("NEUTRAL", GREY, True), ("POSITIVE", GRN, True), ("NEGATIVE", RED2, False)]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k, (lab, col, fades) in enumerate(bars):
        x = 620 + k * 340
        g = ease_out_cubic(prog(t, L(47.94) + k * 0.15, 0.5))
        h = maxh * g * (lerp(1, 0.3, fade) if fades else 1)
        cc = lerp_col(col, (205, 205, 215), fade * 0.8) if fades else col
        if held and not fades:
            h *= 1 + 0.04 * math.sin(math.pi * prog(t, L(52.44), 0.3))
        if h > 2:
            d.rounded_rectangle((x - 90, base - h, x + 90, base), 18, fill=cc, outline=NAVY, width=7)
    c.alpha_composite(ov)
    for k, (lab, col, fades) in enumerate(bars):
        place(c, text(lab, 40, NAVY), 620 + k * 340, 800, alpha=ps)
    if t >= L(50.14):
        for k in (0, 1):
            place(c, text("faded", 40, GREY), 620 + k * 340, base - 400 * 0.3 - 40, alpha=slide(t, L(50.5), 0.3))
    if held:
        place(c, pill("HELD UP", 44, fill=RED2, tc=WHITE), 1300, base - 400 - 55, pop(t, L(52.44)))
    if t >= L(53.80):
        x = prog(t, L(53.80), 0.22)
        place(c, stamp("LAB ITEMS", 90, RED, -12), 760, 380, lerp(1.8, 1.0, ease_out_cubic(x)), alpha=x)

# ============ 06 NOT THE SAME ============
@scene("06_not_the_same", 56.34, 62.08)
def s_notsame(c, t):
    L = lambda s: s - 56.34
    shrink = ease_in_out(prog(t, L(60.18), 0.45))
    sc = lerp(1.0, 0.78, shrink); y = lerp(480, 360, shrink)
    s = pop(t, 0.05)
    if s > 0:
        p = panel(640, 400, fill=BLUE).copy()
        m = moon(58); p.alpha_composite(m, (int(322 - m.width / 2), 40))
        tt = text("A FULL\nSLEEPLESS NIGHT", 52, WHITE); p.alpha_composite(tt, (int(322 - tt.width / 2), 190))
        place(c, p, lerp(540, 600, shrink), y, s * sc)
    s = pop(t, L(59.22))
    if s > 0:
        p = panel(640, 400, fill=WHITE).copy(); d = ImageDraw.Draw(p)
        d.ellipse((262, 60, 382, 180), fill=YEL, outline=NAVY, width=6)
        d.arc((292, 120, 352, 160), 200, 340, fill=NAVY, width=7)
        d.ellipse((295, 100, 309, 114), fill=NAVY); d.ellipse((335, 100, 349, 114), fill=NAVY)
        tt = text("ONE BAD\nEVENING", 56, NAVY); p.alpha_composite(tt, (int(322 - tt.width / 2), 200))
        place(c, p, lerp(1380, 1320, shrink), y, s * sc)
    place(c, text("≠", 230, YEL, stroke=12, shadow=10), W / 2 + (lerp(0, 0, shrink)), y - 10, pop(t, L(58.04)) * sc)
    s = pop(t, L(60.86), 0.45)
    place(c, text("...but it fits a", 56, WHITE, stroke=6), W / 2, 640, slide(t, L(60.18), 0.3))
    place(c, pill("BROADER PATTERN", 78, fill=YEL), W / 2, 760, s)

# ============ 07 STREAMING ============
TILES = [("THE WAVE", (88, 60, 160), (220, 70, 110)), ('"YOU TOO!"', (20, 120, 140), (40, 40, 90)),
         ("THE TOAST", (190, 120, 30), (90, 30, 30)), ("GROUP\nPROJECT", (40, 140, 80), (20, 40, 60)),
         ("THAT\nEMAIL", (130, 40, 50), (30, 20, 40))]

def tile(title, c1, c2, w=300, h=430):
    yy = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(c1) * (1 - yy) + np.array(c2) * yy).repeat(w, axis=1).astype(np.uint8)
    im = Image.fromarray(arr, "RGB").convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=255); im.putalpha(m)
    tt = text(title, 46, WHITE, stroke=4, stroke_fill=(0, 0, 0)); im.alpha_composite(tt, (int(w / 2 - tt.width / 2), h - tt.height - 70))
    mt = text("98% match", 28, (70, 210, 120)); im.alpha_composite(mt, (int(w / 2 - mt.width / 2), h - 60))
    return im

@scene("07_streaming", 65.56, 70.16)
def s_stream(c, t):
    L = lambda s: s - 65.56
    a = slide(t, 0.0, 0.3)
    ui = Image.new("RGBA", (1720, 780), (0, 0, 0, 0)); d = ImageDraw.Draw(ui)
    d.rounded_rectangle((0, 0, 1719, 779), 30, fill=(18, 18, 22, 245), outline=(60, 60, 70), width=3)
    ui.alpha_composite(text("BRAIN+", 64, RED2), (40, 22))
    for k, n in enumerate(["Home", "Replays", "My Cringe", "Downloads: all of them"]):
        ui.alpha_composite(text(n, 30, (170, 170, 180)), (330 + k * 230 if k < 3 else 1050, 45))
    ui.alpha_composite(text("Top picks for you at 3:00 AM", 44, WHITE), (40, 140))
    place(c, ui, W / 2, 470 + (1 - a) * 30, alpha=a)
    hi = t >= L(67.94)
    for k, (tt, c1, c2) in enumerate(TILES):
        x = slide(t, L(66.68) + k * 0.09, 0.45)
        cx = 290 + k * 335 + (1 - x) * 900
        sc = 1.0
        if k == 0 and hi:
            sc = 1 + 0.08 * ease_out_back(prog(t, L(67.94), 0.35))
        place(c, tile(tt, c1, c2), cx, 545, sc, alpha=x)
        if k == 0 and hi:
            fr = Image.new("RGBA", (330, 460), (0, 0, 0, 0))
            ImageDraw.Draw(fr).rounded_rectangle((2, 2, 327, 457), 26, outline=YEL, width=9)
            place(c, fr, cx, 545, sc)
    if t >= L(68.72):
        place(c, pill("#1 IN CRINGE", 40, fill=RED2, tc=WHITE), 290, 325, pop(t, L(68.72)), rot=-6)

# ============ 09 TERM ============
@scene("09_term_post_event", 72.84, 75.72)
def s_term(c, t):
    place(c, pill("PSYCHOLOGY TERM", 44, fill=SKY), W / 2, 260, pop(t, 0.0))
    full = "POST-EVENT PROCESSING"
    n = int(len(full) * prog(t, 0.15, 1.3))
    shown = full[:n]
    if shown:
        tt = text(shown, 112, WHITE, stroke=10, shadow=8)
        ref = text(full, 112, WHITE, stroke=10, shadow=8)
        place_tl(c, tt, W / 2 - ref.width / 2, 440)
        if n < len(full) or int(t * 3) % 2 == 0:
            cur = Image.new("RGBA", (14, 110), YEL + (255,))
            place(c, cur, W / 2 - ref.width / 2 + tt.width + 4, 440)
    u = ease_out_cubic(prog(t, 1.5, 0.4))
    if u > 0:
        bar = Image.new("RGBA", (max(1, int(1150 * u)), 16), YEL + (255,)); place(c, bar, W / 2, 530)
    place(c, text("(replaying a social moment after it's over)", 54, SKY, stroke=5), W / 2, 640, alpha=slide(t, 1.7, 0.4))

# ============ 10 CHAT WITH STRANGER ============
def bubble(txt, w=420, flip=False):
    b = load(PK + "07_Brand/bubble_speech.png", width=w, flip=flip).copy()
    tt = text(txt, 74, NAVY); b.alpha_composite(tt, (int(b.width / 2 - tt.width / 2), int(b.height * 0.42 - tt.height / 2)))
    return b

@scene("10_chat_stranger", 75.72, 78.28)
def s_chat(c, t):
    L = lambda s: s - 75.72
    place(c, pill("STUDY", 40), W / 2, 85, pop(t, 0.0))
    place(c, text("chat with a stranger", 60, WHITE, stroke=6), W / 2, 165, slide(t, 0.1, 0.3))
    place(c, pose("Batata", "wave", 480), 560, 650 + math.sin(t * 5) * 6, pop(t, 0.05))
    place(c, char("Tamatem", "confused", 450, flip=True), 1380, 660 + math.sin(t * 5 + 1) * 6, pop(t, 0.2))
    place(c, bubble("hi!", 380), 760, 330, pop(t, L(76.58)))
    place(c, bubble("...hello?", 420, flip=True), 1230, 340, pop(t, L(77.32)))

# ============ 11 RATING ============
@scene("11_rating", 78.28, 84.02)
def s_rating(c, t):
    L = lambda s: s - 78.28
    place(c, pill("SOCIALLY ANXIOUS", 46, fill=RED2, tc=WHITE), W / 2, 120, pop(t, L(78.58)))
    a = slide(t, L(79.6), 0.3)
    place(c, text("REPLAYS", 60, WHITE, stroke=6), 500, 290, alpha=a)
    n = 1 + int(8 * prog(t, L(79.80), 1.4)) if t >= L(79.80) else 0
    if n:
        place(c, text(str(n), 220, YEL, stroke=12, shadow=10), 500, 480, 1 + 0.08 * math.sin(t * 20) * (1 - prog(t, L(81.2), 0.1)))
        ring = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(ring)
        st = (t * 360) % 360
        d.arc((20, 20, 280, 280), st, st + 290, fill=SKY, width=14)
        place(c, ring, 500, 480, alpha=a)
    ps = pop(t, L(81.2), 0.4)
    if ps > 0:
        p = panel(860, 480, fill=WHITE).copy()
        p.alpha_composite(text("THEIR RATING", 44, NAVY), (50, 50))
        p.alpha_composite(text("REALITY", 44, NAVY), (50, 270))
        place(c, p, 1300, 500, ps)
        for row, (cue, filled, col) in enumerate([(L(81.42), 2, RED2), (L(83.30), 4, GRN)]):
            for k in range(5):
                on = k < filled
                s = pop(t, cue + k * 0.08, 0.3)
                place(c, star(42, fill=(YEL if on else (220, 222, 235))), 1300 - 210 + k * 105, 405 + row * 220, s * ps)
        if t >= L(83.38):
            place(c, text("(better than they thought)", 34, GRN), 1300, 688, alpha=slide(t, L(83.6), 0.3))

# ============ 12 CALENDAR ============
@scene("12_calendar_postmortem", 84.02, 88.44)
def s_cal(c, t):
    L = lambda s: s - 84.02
    s = pop(t, 0.0, 0.42)
    p = panel(1180, 640, fill=WHITE).copy(); d = ImageDraw.Draw(p)
    d.rounded_rectangle((2, 2, 1181, 110), 36, fill=BLUE, outline=NAVY, width=8); d.rectangle((10, 60, 1173, 110), fill=BLUE)
    d.line((2, 110, 1181, 110), fill=NAVY, width=8)
    d.rounded_rectangle((40, 26, 100, 86), 8, fill=WHITE, outline=NAVY, width=5); d.rectangle((40, 26, 100, 44), fill=RED2)
    p.alpha_composite(text("MEETING INVITE", 42, WHITE), (125, 28))
    p.alpha_composite(text("Post-mortem: That Conversation", 58, NAVY), (50, 140))
    rows = [("When:", "3:00 AM  –  ∞", NAVY, 0.0), ("Organizer:", "Your Brain", NAVY, 0.0)]
    for k, (a_, b_, col, _) in enumerate(rows):
        p.alpha_composite(text(a_, 42, GREY), (60, 250 + k * 75)); p.alpha_composite(text(b_, 42, col), (330, 250 + k * 75))
    place(c, p, W / 2, 470, s)
    if t >= L(86.10):
        x = slide(t, L(86.10), 0.3)
        place_tl(c, text("Scheduled by:", 42, GREY), W / 2 - 590 + 60, 470 - 320 + 250 + 150 + 30, alpha=x)
        place_tl(c, text("nobody", 42, RED), W / 2 - 590 + 380, 470 - 320 + 250 + 150 + 30, alpha=x)
    # buttons
    if s >= 0.99:
        by = 470 + 320 - 90
        place(c, pill("Accept", 40, fill=GRN, tc=WHITE, shadow=4), W / 2 - 220, by)
        click = L(86.98) + 0.05
        shake = math.sin((t - click) * 55) * 14 * max(0, 1 - (t - click) / 0.5) if t > click else 0
        if t < click + 0.12:
            btn = pill("End meeting", 40, fill=WHITE, tc=RED, shadow=4)
        else:
            btn = pill("Can't end", 40, fill=(200, 200, 210), tc=(110, 110, 130), shadow=4)
        place(c, btn, W / 2 + 200 + shake, by)
        cx = lerp(1500, W / 2 + 230, ease_in_out(prog(t, L(86.35), 0.55))); cy = lerp(1000, by + 5, ease_in_out(prog(t, L(86.35), 0.55)))
        place(c, cursor(64), cx + 22, cy + 38, alpha=slide(t, L(86.30), 0.15))
        ripple(c, W / 2 + 230, by + 5, t, click, 0.4, 20, 110, RED2)

# ============ 14 KARAOKE STEPS ============
def mic_icon():
    im = Image.new("RGBA", (200, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((85, 110, 115, 210), 12, fill=NAVY)
    d.ellipse((50, 10, 150, 120), fill=GREY, outline=NAVY, width=7)
    for k in range(3): d.line((62, 45 + k * 22, 138, 45 + k * 22), fill=NAVY, width=4)
    return im

def speaker_icon():
    im = Image.new("RGBA", (220, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((20, 70, 70, 130), fill=NAVY); d.polygon([(70, 70), (130, 25), (130, 175), (70, 130)], fill=NAVY)
    for k, r in enumerate([40, 70]):
        d.arc((130 - r, 100 - r, 130 + r, 100 + r), -45, 45, fill=SKY, width=10)
    return im

def brain_icon():
    im = Image.new("RGBA", (220, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, 210, 190), 30, fill=(20, 30, 70), outline=NAVY, width=6)
    d.ellipse((50, 45, 170, 150), fill=(255, 150, 190), outline=NAVY, width=6)
    d.arc((70, 60, 120, 120), 180, 360, fill=NAVY, width=5); d.arc((100, 80, 150, 140), 0, 180, fill=NAVY, width=5)
    d.line((110, 48, 110, 148), fill=NAVY, width=4)
    return im

@scene("14_karaoke_steps", 90.06, 94.20)
def s_kara(c, t):
    L = lambda s: s - 90.06
    place(c, pill("STUDY", 40), W / 2, 85, pop(t, 0.0))
    place(c, text("the karaoke experiment", 60, WHITE, stroke=6), W / 2, 165, slide(t, 0.1, 0.3))
    for k, (cue, ic, lab) in enumerate([(0.05, mic_icon(), "SING\nKARAOKE"), (L(91.42), speaker_icon(), "HEAR IT\nPLAYED BACK"),
                                        (L(92.80), brain_icon(), "SCAN THE\nBRAIN")]):
        s = pop(t, cue)
        if s <= 0: continue
        p = panel(470, 470, fill=WHITE).copy()
        p.alpha_composite(ic, (int(237 - ic.width / 2), 50))
        tt = text(lab, 48, NAVY); p.alpha_composite(tt, (int(237 - tt.width / 2), 290))
        cx = 400 + k * 560
        place(c, p, cx, 540, s)
        place(c, num_badge(k + 1, 40), cx - 210, 320, s)

# ============ 15 SENSITIVITY GAUGE ============
@scene("15_sensitivity_gauge", 97.54, 102.20)
def s_gauge(c, t):
    L = lambda s: s - 97.54
    place(c, text("RESTLESS SLEEP", 90, WHITE, stroke=10, shadow=8), W / 2, 130, pop(t, L(98.22) - 0.3))
    zz = Image.new("RGBA", (420, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(zz)
    d.line([(10 + k * 50, 30 + (-20 if k % 2 else 20)) for k in range(9)], fill=YEL, width=10, joint="curve")
    place(c, zz, W / 2, 215, alpha=slide(t, L(98.22), 0.3))
    a = slide(t, 0.1, 0.4)
    g = Image.new("RGBA", (900, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    cx, cy, r = 450, 470, 400
    for k in range(60):
        col = lerp_col(GRN, YEL, k / 30) if k < 30 else lerp_col(YEL, RED2, (k - 30) / 30)
        a0 = 180 + k * 3; d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 3.4, fill=col, width=70)
    d.arc((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), 180, 360, fill=NAVY, width=8)
    d.arc((cx - r + 70, cy - r + 70, cx + r - 70, cy + r - 70), 180, 360, fill=NAVY, width=8)
    place(c, g, W / 2, 500, alpha=a)
    v = 0.18 + 0.7 * ease_out_back(prog(t, L(99.9), 0.9), 1.2)
    v += 0.015 * math.sin(t * 30) * prog(t, L(100.8), 0.2)
    ang = math.radians(180 + 180 * v)
    gx, gy = W / 2, 500 - 260 + 470
    nd = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(nd)
    ex, ey = gx + 330 * math.cos(ang), gy + 330 * math.sin(ang)
    d.line((gx, gy, ex, ey), fill=NAVY, width=26); d.line((gx, gy, ex, ey), fill=WHITE, width=14)
    d.ellipse((gx - 34, gy - 34, gx + 34, gy + 34), fill=WHITE, outline=NAVY, width=8)
    nd.putalpha(nd.getchannel("A").point(lambda q: int(q * a))); c.alpha_composite(nd)
    hot = t >= L(100.90)
    lab = text("SENSITIVITY TO\nNEGATIVE FEELINGS", 46, RED2 if hot else WHITE, stroke=6)
    place(c, lab, W / 2, 815, 1 + 0.06 * math.sin(math.pi * prog(t, L(100.9), 0.3)), alpha=slide(t, 0.6, 0.3))

# ============ 16 REM PROPOSAL ============
def block(txt, fill, tc, w=470, h=200):
    p = panel(w, h, r=30, fill=fill).copy(); tt = text(txt, 70, tc)
    p.alpha_composite(tt, (int(w / 2 - tt.width / 2 + 2), int(h / 2 - tt.height / 2 + 2))); return p

def toggle(on_amt):
    im = Image.new("RGBA", (300, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = lerp_col((170, 172, 190), GRN, on_amt)
    d.rounded_rectangle((6, 6, 294, 134), 64, fill=col, outline=NAVY, width=8)
    kx = lerp(76, 224, on_amt); d.ellipse((kx - 52, 18, kx + 52, 122), fill=WHITE, outline=NAVY, width=7)
    return im

@scene("16_rem_proposal", 104.40, 115.52)
def s_rem(c, t):
    L = lambda s: s - 104.40
    pp = pop(t, 0.0) * (1 + 0.12 * math.sin(math.pi * prog(t, L(112.42), 0.4)))
    place(c, pill("THE PROPOSAL", 56), W / 2, 115, pp)
    place(c, text("(not proven yet)", 40, GREY), W / 2, 195, alpha=slide(t, 0.2, 0.3))
    outA = slide(t, L(107.30), 0.35)
    if outA < 1:
        aA = 1 - outA; dy = -60 * outA
        s = pop(t, L(104.64) - 0.1)
        hx = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(hx)
        d.polygon([(75 + 60 * math.cos(math.radians(60 * k + 30)), 75 + 60 * math.sin(math.radians(60 * k + 30))) for k in range(6)], outline=YEL, width=10)
        d.ellipse((60, 60, 90, 90), fill=YEL)
        place(c, hx, W / 2 - 430, 400 + dy, s, aA, rot=t * 40)
        place(c, pill("NORADRENALINE", 66, fill=BLUE, tc=WHITE), W / 2 + 60, 400 + dy, s, aA)
        tg = ease_in_out(prog(t, L(105.74), 0.35))
        place(c, toggle(1 - tg), W / 2 - 150, 610 + dy, pop(t, L(105.5)), aA)
        place(c, text("ON" if tg < 0.5 else "OFF", 80, GRN if tg < 0.5 else RED2, stroke=8), W / 2 + 90, 610 + dy, pop(t, L(105.5)), aA)
        place(c, text("during REM sleep  z z z", 56, SKY, stroke=6), W / 2, 760 + dy, slide(t, L(106.45), 0.3) * aA)
    if t >= L(107.30):
        ap = slide(t, L(107.35), 0.35)
        sep = ease_in_out(prog(t, L(107.76), 0.7))
        back = ease_in_out(prog(t, L(109.80), 0.8))
        gap = lerp(0, 1, sep) - 0.55 * back
        wob = math.sin((t - L(109.8)) * 16) * 10 * max(0, 1 - (t - L(109.8)) / 1.2) if t > L(109.8) else 0
        mx = W / 2 - 236 - gap * 230 + wob; fx = W / 2 + 236 + gap * 230 - wob
        place(c, block("MEMORY", SKY, NAVY), mx, 470, alpha=ap)
        place(c, block("FEELING", RED2, WHITE), fx, 470, alpha=ap)
        if sep > 0.3 and back < 0.5:
            place(c, text("separated", 56, SKY, stroke=6), W / 2, 680, alpha=clamp(sep * 2 - 0.6) * (1 - back * 2))
        if back > 0.2:
            place(c, text("restless sleepers: maybe less", 54, YEL, stroke=6), W / 2, 680, alpha=clamp(back * 2 - 0.4))
    if t >= L(113.80):
        x = prog(t, L(113.80), 0.2)
        place(c, stamp("NOT PROVEN", 110, RED, -9), W / 2, 330, lerp(1.9, 1.0, ease_out_cubic(x)), alpha=x)

# ============ 17 CRINGE VOLUME ============
def spk(loud):
    im = Image.new("RGBA", (160, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((10, 45, 45, 95), fill=WHITE); d.polygon([(45, 45), (90, 12), (90, 128), (45, 95)], fill=WHITE)
    for r in ([28, 52] if loud else [28]):
        d.arc((90 - r, 70 - r, 90 + r, 70 + r), -50, 50, fill=WHITE, width=9)
    return im

@scene("17_cringe_volume", 115.52, 121.16)
def s_vol(c, t):
    L = lambda s: s - 115.52
    place(c, pill("TRANSLATION", 40, fill=SKY), W / 2, 95, pop(t, 0.0))
    place(c, text("CRINGE VOLUME", 110, WHITE, stroke=10, shadow=8), W / 2, 220, pop(t, 0.1))
    v = 0.7
    v = lerp(v, 0.12, ease_in_out(prog(t, L(117.92), 0.5)))
    v = lerp(v, 1.0, ease_out_back(prog(t, L(119.76), 0.45), 1.3))
    shake = math.sin(t * 60) * 8 * prog(t, L(120.1), 0.1) if t > L(120.1) else 0
    x0, x1, y = 400, 1520, 500
    a = slide(t, 0.2, 0.3)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((x0, y - 26, x1, y + 26), 26, fill=(60, 60, 90), outline=NAVY, width=6)
    kx = lerp(x0 + 30, x1 - 30, clamp(v))
    col = lerp_col(GRN, YEL, clamp(v / 0.5)) if v < 0.5 else lerp_col(YEL, RED2, clamp((v - 0.5) / 0.5))
    d.rounded_rectangle((x0, y - 26, kx, y + 26), 26, fill=col, outline=NAVY, width=6)
    for k in range(20):   # equaliser bars
        bx = x0 + 20 + k * 56; on = (k / 20) < v
        bh = 40 + k * 7
        d.rounded_rectangle((bx, y - 70 - bh, bx + 36, y - 70), 8, fill=(col if on else (50, 52, 80)))
    d.ellipse((kx - 52, y - 52, kx + 52, y + 52), fill=WHITE, outline=NAVY, width=8)
    s.putalpha(s.getchannel("A").point(lambda q: int(q * a))); place(c, s, W / 2 + shake, H / 2)
    place(c, spk(False), x0 - 120, y, alpha=a); place(c, spk(True), x1 + 120, y, alpha=a)
    place(c, text(f"{int(round(clamp(v) * 100))}%", 60, col, stroke=6), kx + shake, y + 110, alpha=a)
    if L(116.56) <= t < L(119.10):
        place(c, moon(40), W / 2 - 260, 720, pop(t, L(116.56)))
        place(c, text("GOOD SLEEP", 70, GRN, stroke=8), W / 2 + 60, 720, pop(t, L(116.56)))
    if t >= L(119.10):
        eye = Image.new("RGBA", (130, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(eye)
        d.ellipse((5, 5, 125, 75), fill=WHITE, outline=NAVY, width=6); d.ellipse((45, 18, 85, 62), fill=RED2); d.ellipse((57, 30, 73, 48), fill=NAVY)
        place(c, eye, W / 2 - 260, 720, pop(t, L(119.18)))
        place(c, text("LYING AWAKE", 70, RED2, stroke=8), W / 2 + 70, 720, pop(t, L(119.18)))

# ============ 19 SEARCH ============
@scene("19_search_no_study", 123.14, 126.70)
def s_search(c, t):
    L = lambda s: s - 123.14
    s = pop(t, 0.0)
    bar = Image.new("RGBA", (1300, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(bar)
    d.rounded_rectangle((4, 14, 1296, 146), 66, fill=NAVY); d.rounded_rectangle((4, 4, 1296, 136), 66, fill=WHITE, outline=NAVY, width=8)
    d.ellipse((50, 35, 110, 95), outline=NAVY, width=10); d.line((100, 88, 128, 116), fill=NAVY, width=12)
    q = "is 3 a.m. itself dangerous? study"
    n = int(len(q) * prog(t, 0.25, 1.5)); tt = text(q[:n] if n else " ", 52, NAVY)
    bar.alpha_composite(tt, (160, int(70 - tt.height / 2)))
    if int(t * 3) % 2 == 0 or n < len(q):
        d.rectangle((166 + tt.width, 40, 172 + tt.width, 100), fill=BLUE)
    place(c, bar, W / 2, 360, s)
    if t >= L(125.55):
        place(c, text("0 results found", 96, WHITE, stroke=10, shadow=8), W / 2, 560, pop(t, L(125.55)))
        place(c, text("(that I could find)", 46, GREY), W / 2, 670, alpha=slide(t, L(125.9), 0.3))

# ============ 20 MY GUESS ============
@scene("20_my_guess", 126.70, 130.90)
def s_guess(c, t):
    L = lambda s: s - 126.70
    place(c, pill("MY GUESS", 84), 520, 175, pop(t, 0.0), rot=-3)
    place(c, text("(an opinion, not a study)", 40, GREY), 520, 275, alpha=slide(t, 0.25, 0.3))
    place(c, char("Batata", "thinking", 560), 1500, 560 + math.sin(t * 3) * 6, pop(t, 0.12))
    for k, (cue, line) in enumerate([(L(127.45), "Nothing is distracting you"), (L(128.85), "You're awake"),
                                    (L(130.05), "A tired brain is bad\nat calming itself down")]):
        x = slide(t, cue, 0.35)
        if x <= 0: continue
        dot = Image.new("RGBA", (40, 40), (0, 0, 0, 0)); ImageDraw.Draw(dot).ellipse((4, 4, 36, 36), fill=YEL, outline=NAVY, width=4)
        yy = 410 + k * 130
        place(c, dot, 190 - (1 - x) * 80, yy, alpha=x)
        place_tl(c, text(line, 54, WHITE, stroke=6, align="left"), 240 - (1 - x) * 80, yy + (22 if k == 2 else 0), alpha=x)

# ============ 21 CORNELL ============
def tshirt():
    im = Image.new("RGBA", (420, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(120, 20), (165, 50), (255, 50), (300, 20), (400, 90), (350, 170), (310, 145), (310, 380), (110, 380), (110, 145), (70, 170), (20, 90)]
    d.polygon(pts, fill=RED2, outline=NAVY, width=9)
    d.arc((160, 20, 260, 90), 0, 180, fill=NAVY, width=8)
    t1 = text("CRINGE", 50, WHITE, stroke=4); im.alpha_composite(t1, (int(210 - t1.width / 2), 200))
    return im

@scene("21_cornell_tshirt", 134.28, 141.32)
def s_cornell(c, t):
    L = lambda s: s - 134.28
    place(c, pill("STUDY  ·  2000  ·  CORNELL", 50), W / 2, 120, pop(t, 0.0))
    place(c, tshirt(), 470, 470 + math.sin(t * 3) * 5, pop(t, L(136.30)), rot=math.sin(t * 2) * 3)
    place(c, text("embarrassing t-shirt", 46, WHITE, stroke=5), 470, 730, slide(t, L(136.84), 0.3))
    ps = pop(t, L(137.8), 0.4)
    if ps > 0:
        p = panel(900, 470, fill=WHITE).copy()
        p.alpha_composite(text("THEY GUESSED", 44, NAVY), (50, 45))
        p.alpha_composite(text("ACTUALLY NOTICED", 44, NAVY), (50, 250))
        place(c, p, 1310, 470, ps)
        unit = 340
        for row, (cue, mult, col) in enumerate([(L(138.12), 2.0, YEL), (L(140.70), 1.0, GRN)]):
            g = ease_out_cubic(prog(t, cue, 0.6))
            if g > 0:
                bw = int(unit * mult * g * 1.1)
                bar = Image.new("RGBA", (max(bw, 2), 80), (0, 0, 0, 0))
                ImageDraw.Draw(bar).rounded_rectangle((0, 0, max(bw, 2) - 1, 79), 20, fill=col, outline=NAVY, width=6)
                place_tl(c, bar, 1310 - 400, 470 - 235 + 160 + row * 205)
        if t >= L(138.80):
            b = num_badge("2×", 70, fill=RED2, tc=WHITE)
            place(c, b, 1690, 300, pop(t, L(138.80)), rot=8)

# ============ 22 NOTICING VS REMEMBERING ============
@scene("22_noticing_remembering", 142.74, 145.84)
def s_notice(c, t):
    L = lambda s: s - 142.74
    s = pop(t, 0.0)
    p = panel(680, 440, fill=WHITE).copy()
    tt = text("NOTICING", 76, NAVY); p.alpha_composite(tt, (int(342 - tt.width / 2), 220))
    t2 = text("measured", 44, GRN); p.alpha_composite(t2, (int(342 - t2.width / 2), 330))
    place(c, p, 560, 470, s)
    place(c, check_icon(70), 560, 340, pop(t, L(143.72)))
    s = pop(t, L(144.70))
    if s > 0:
        p = panel(680, 440, fill=BLUE).copy()
        tt = text("REMEMBERING", 72, WHITE); p.alpha_composite(tt, (int(342 - tt.width / 2), 220))
        t2 = text("not measured", 44, YEL); p.alpha_composite(t2, (int(342 - t2.width / 2), 330))
        place(c, p, 1360, 470, s)
        place(c, num_badge("?", 70, fill=YEL), 1360, 340, pop(t, L(144.85)))

# ============ 23 STRATEGY TITLE ============
@scene("23_strategy_title", 150.10, 152.70)
def s_strat(c, t):
    L = lambda s: s - 150.10
    place(c, text("ONE STRATEGY", 150, YEL, stroke=12, shadow=10), 800, 420, pop(t, 0.0))
    place(c, text("psychologists describe", 62, WHITE, stroke=6), 800, 560, slide(t, L(150.80), 0.35))
    place(c, pose("Batata", "point", 520, flip=True), 1580, 560 + math.sin(t * 3) * 6, pop(t, 0.2))

# ============ 24 STEPS ============
def chip(txt, fill, tc=NAVY):
    return pill(txt, 60, fill=fill, tc=tc)

@scene("24_steps_notice_move", 152.70, 161.34)
def s_steps(c, t):
    L = lambda s: s - 152.70
    for k, (cue, kw, rest, col) in enumerate([(0.0, "NOTICE", " the replay is happening", RED2),
                                            (L(154.62), "MOVE", " your attention to something\nthat holds it", BLUE2)]):
        x = slide(t, cue, 0.4)
        if x <= 0: continue
        h = 200 if k == 0 else 250
        p = panel(1500, h, fill=WHITE).copy()
        kwi = text(kw, 64, col); rs = text(rest, 52, NAVY, align="left")
        p.alpha_composite(kwi, (170, int(h / 2 - kwi.height / 2)))
        p.alpha_composite(rs, (170 + kwi.width, int(h / 2 - rs.height / 2 + 4)))
        b = num_badge(k + 1, 50); p.alpha_composite(b, (40, int(h / 2 - b.height / 2)))
        y = 200 if k == 0 else 450
        place(c, p, W / 2 + (1 - x) * 200, y, alpha=x)
    xs = [560, 900, 1330]
    for k, (cue, lab, col) in enumerate([(L(158.36), "SEE", SKY), (L(159.28), "HEAR", GRN), (L(159.92), "DO (hands)", YEL)]):
        place(c, chip(lab, col), xs[k], 720, pop(t, cue))

# ============ 25 DOCTOR ============
@scene("25_doctor_disclaimer", 165.78, 175.26)
def s_doc(c, t):
    L = lambda s: s - 165.78
    a = slide(t, 0.0, 0.6)
    p = panel(1440, 640, fill=BLUE, shadow=10)
    place(c, p, W / 2, 420 + (1 - a) * 30, alpha=a)
    place(c, text("WHEN TO GET HELP", 66, YEL, stroke=6), W / 2, 185, alpha=slide(t, 0.2, 0.5))
    for k, (cue, line) in enumerate([(L(166.90), "It happens constantly"), (L(168.20), "It's hurting your daily life")]):
        x = slide(t, cue, 0.5)
        dot = Image.new("RGBA", (36, 36), (0, 0, 0, 0)); ImageDraw.Draw(dot).ellipse((4, 4, 32, 32), fill=SKY)
        place(c, dot, 470, 320 + k * 100, alpha=x)
        place_tl(c, text(line, 58, WHITE), 515 + (1 - x) * 40, 320 + k * 100, alpha=x)
    x = slide(t, L(169.70), 0.5)
    hp = pill("Talk to a doctor or therapist", 62, fill=GRN, tc=WHITE)
    place(c, hp, W / 2, 590 + (1 - x) * 20, 0.96 + 0.04 * x, alpha=x)
    x = slide(t, L(171.80), 0.5)
    ic = Image.new("RGBA", (56, 56), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
    d.ellipse((3, 3, 53, 53), outline=WHITE, width=5); d.rectangle((25, 24, 31, 42), fill=WHITE); d.ellipse((24, 12, 32, 20), fill=WHITE)
    disc = text("General information, not medical advice.", 42, (220, 225, 245))
    place(c, ic, W / 2 - disc.width / 2 - 20, 805, alpha=x)
    place(c, disc, W / 2 + 18, 805, alpha=x)


if __name__ == "__main__":
    OFFSET = 3.45          # VO-source -> timeline shift after the hen/throat gag (see build_draft.py)
    END = 193.0333
    want = sys.argv[1:]
    if want and want[0] == "qa":
        for name, (s0, s1, fn) in sorted(SCENES.items()):
            if len(want) > 1 and not any(w in name for w in want[1:]):
                continue
            still(name, s1 - s0, fn, (s1 - s0) * 0.92, s0 + OFFSET)
        sys.exit()
    if want and want[0] == "bg":
        render("00_background_midnight", END, lambda c, t: None, 0.0)
        sys.exit()
    for name, (s0, s1, fn) in sorted(SCENES.items()):
        if want and not any(w in name for w in want):
            continue
        render(name, s1 - s0, fn, s0 + OFFSET)
