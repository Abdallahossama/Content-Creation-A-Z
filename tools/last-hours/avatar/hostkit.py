"""hostkit: the owner's illustrated host avatar (fedora, red band) used like Omar Qany's straw-hat head (owner OK 27 Nov 2026). Host name: NOAH, THE FILE KEEPER.
OWNER RULES 27 Nov: do not overuse (about 1 cutaway per 3-4 min + a few pops); text never over the face.
- cutaway(t, t0, t1, expr): full-frame noir grid + the head pops up from the bottom with a small settle, gentle bob, red/blue rim glow.
- corner(c, t, t0, t1, expr): reaction head slides in at the bottom-left over the footage, holds, slides out.
- bug(c): small round head + THE LAST HOURS (cutaways / end screen).
Expressions: shock, smirk, think, serious, laugh, disappointed, master; 5 drawings each (s5..s9) rotated so repeats differ.
Cut-outs: brand/avatar/cut/*.png (cut_avatar.py)."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
CUT = "D:/why habibi/_newchannel/brand/avatar/cut/"
W, H = 1920, 1080
RED, BONE, INK = (190, 30, 30), (236, 230, 214), (12, 12, 14)
COND = "C:/Windows/Fonts/FRAMDCN.TTF"
_C = {}
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def back(x, s=1.4):                                       # ease-out with a small overshoot (the "pop")
    x = min(max(x, 0.0), 1.0) - 1; return x * x * ((s + 1) * x + s) + 1

def head(expr, k, h):
    """sheet 9 only: its hats are complete (the other sheets clip the hat crown). The drawings are cut at the left, right and
    bottom by ChatGPT's frame, so the head is always anchored to the LEFT screen edge and the bottom, and the right shoulder
    fades out (owner 27 Nov: hide the cropped coat)."""
    name = expr if expr in ("master", "hero_file_flashlight") else f"{expr}_s9"
    key = (name, h)
    if key not in _C:
        im = Image.open(CUT + name + ".png").convert("RGBA"); im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
        if name != "hero_file_flashlight":
            a = np.asarray(im, np.float32).copy(); w = im.width
            ramp = np.clip((w - 1 - np.arange(w)) / (0.22 * w), 0, 1) ** 1.5                     # right 22 %: fade to nothing
            yy = np.arange(im.height)[:, None] / im.height; low = np.clip((yy - 0.55) / 0.45, 0, 1)  # only below the face
            a[..., 3] *= 1 - (1 - ramp[None, :]) * low
            im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        sh = Image.new("RGBA", (im.width + 100, im.height + 100), (0, 0, 0, 0))
        blk = Image.new("RGBA", im.size, (0, 0, 0, 255)); blk.putalpha(im.split()[3].point(lambda v: int(v * 0.6)))
        sh.paste(blk, (50, 64), blk); sh = sh.filter(ImageFilter.GaussianBlur(20)); sh.alpha_composite(im, (50, 50)); _C[key] = sh
    return _C[key]

def host_bg():
    if "bg" not in _C:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        a = np.zeros((H, W, 3), np.float32) + np.array(INK, np.float32)
        a += np.exp(-((xx / (W * .4)) ** 2 + ((yy - H * .55) / (H * .6)) ** 2))[..., None] * np.array([80, 10, 12], np.float32)
        a += np.exp(-(((xx - W) / (W * .4)) ** 2 + ((yy - H * .45) / (H * .6)) ** 2))[..., None] * np.array([10, 18, 60], np.float32)
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for x in range(0, W, 60): d.line((x, 0, x, H), fill=(255, 255, 255, 14))
        for y in range(0, H, 60): d.line((0, y, W, y), fill=(255, 255, 255, 14))
        im.alpha_composite(lay); _C["bg"] = im
    return _C["bg"]

def bug(c, x=34, y=30):
    if "bug" not in _C:
        hd = Image.open(CUT + "master.png").convert("RGBA"); hd = hd.resize((int(hd.width * 150 / hd.height), 150), Image.LANCZOS)
        tile = Image.new("RGBA", (110, 110), (25, 25, 28, 255)); tile.alpha_composite(hd.crop((hd.width // 2 - 70, 0, hd.width // 2 + 70, 140)).resize((110, 110)))
        m = Image.new("L", (110, 110), 0); ImageDraw.Draw(m).ellipse((0, 0, 109, 109), fill=255); tile.putalpha(m)
        b = Image.new("RGBA", (420, 120), (0, 0, 0, 0)); b.alpha_composite(tile, (2, 2)); d = ImageDraw.Draw(b)
        d.ellipse((0, 0, 113, 113), outline=RED, width=4); d.text((128, 57), "THE LAST HOURS", font=ImageFont.truetype(COND, 34), fill=BONE, anchor="lm")
        _C["bug"] = b
    c.alpha_composite(_C["bug"], (x, y))

def wave_figure(h, tt):
    """full-body Noah waving (owner's drawing, cut/wave_base.png + wave_hand.png from make_wave.py): the hand rocks around the wrist
    (2.2 waves/s for ~2.4 s, then settles), the body breathes; soft drop shadow, 50 px pad like head()."""
    key = ("wave", h)
    if key not in _C:
        b = Image.open(CUT + "wave_base.png").convert("RGBA"); hnd = Image.open(CUT + "wave_hand.png").convert("RGBA"); s = h / b.height
        _C[key] = (b.resize((int(b.width * s), h), Image.LANCZOS), hnd.resize((int(hnd.width * s), h), Image.LANCZOS), s)
    b, hnd, s = _C[key]
    amp = 7.0 * (1.0 if tt < 2.4 else max(0.0, 1 - (tt - 2.4) / 0.6))
    ang = amp * math.sin(tt * 2 * math.pi * 2.2)
    fig = b.copy(); fig.alpha_composite(hnd.rotate(ang, Image.BICUBIC, center=(112 * s, 236 * s)))
    out = Image.new("RGBA", (fig.width + 100, fig.height + 100), (0, 0, 0, 0))
    blk = Image.new("RGBA", fig.size, (0, 0, 0, 255)); blk.putalpha(fig.split()[3].point(lambda v: int(v * 0.6)))
    out.paste(blk, (50, 64), blk); out = out.filter(ImageFilter.GaussianBlur(20)); out.alpha_composite(fig, (50, 50)); return out

def alive(expr, k, h, tt):
    """idle life on a still drawing (owner 27 Nov: 'moving around ... still in the same place'): a slow sway around the bottom-left
    (the shoulders stay put), a breathing scale, a little nod on the first beat. expr may be 'wave' (two drawings toggled = a wave)."""
    if expr == "wave": return wave_figure(int(h * 1.18), tt)
    hd = head(expr, k, h)
    ang = 1.6 * math.sin(tt * 2 * math.pi / 3.4) + 1.2 * math.exp(-tt * 3) * math.sin(tt * 14)      # sway + quick settle nod
    sc = 1.0 + 0.012 * math.sin(tt * 2 * math.pi / 2.6)                                              # breathing
    im = hd.resize((int(hd.width * sc), int(hd.height * sc)), Image.BICUBIC) if abs(sc - 1) > 0.002 else hd
    im = im.rotate(ang, Image.BICUBIC, center=(im.width * 0.3, im.height), expand=False)
    out = Image.new("RGBA", hd.size, (0, 0, 0, 0)); out.alpha_composite(im.crop((0, im.height - hd.height, min(im.width, hd.width), im.height)), (0, 0))
    return out

def cutaway(t, t0, t1, expr="smirk", k=0, name=None):
    """full-frame host cutaway: pops up from below (0.35 s, overshoot), bobs gently, sinks out in the last 0.2 s"""
    c = host_bg().copy(); hd = alive(expr, k, 860, t - t0)
    u = back((t - t0) / 0.35); v = ease((t1 - t) / 0.2) if t1 - t < 0.2 else 1.0
    y = H - hd.height + 70 + (1 - u) * 520 + (1 - v) * 520 + 6 * math.sin((t - t0) * 2.2)
    c.alpha_composite(hd, (80 if expr == "wave" else -50, int(y))); bug(c, x=W - 470, y=30)    # left-anchored (cropped coat on the screen edge); the full-body wave is not cropped
    if name:
        f = ImageFont.truetype(COND, 64); u2 = ease((t - t0 - 0.3) / 0.3); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((hd.width + 10, 430), name[0], font=f, fill=BONE + (int(255 * u2),), anchor="lm")
        d.rectangle((hd.width + 12, 478, hd.width + 12 + 380 * u2, 486), fill=RED + (int(255 * u2),))
        d.text((hd.width + 12, 520), name[1], font=ImageFont.truetype(COND, 40), fill=(170, 170, 170, int(255 * u2)), anchor="lm"); c.alpha_composite(lay)
    return c

def end_screen(t, sub_at=None, like_at=None, next_title=None, wave_at=None):
    """end card (last ~20 s): Noah with the file + flashlight on the right, two empty end-screen video slots on the left (YouTube
    places its elements there), SUBSCRIBE button that presses when the word is spoken, 'Whose last hours next?'."""
    c = host_bg().copy()
    if wave_at is not None and t >= wave_at:                                             # goodbye: the full-body wave
        fig = wave_figure(1000, t - wave_at); c.alpha_composite(fig, (W - fig.width - 60, H - fig.height + 70))
    else:
        hero = head("hero_file_flashlight", 0, 900)
        u = back(t / 0.45); c.alpha_composite(hero, (int(W - hero.width + 40 + (1 - u) * 700), H - hero.height + 110))
    d = ImageDraw.Draw(c); f = ImageFont.truetype(COND, 46)
    for i, y in enumerate((150, 590)):
        a = int(150 * ease((t - 0.3 - 0.2 * i) / 0.4)); d.rectangle((110, y, 110 + 600, y + 338), outline=(200, 200, 200, a), width=3)
    pressed = sub_at is not None and t >= sub_at
    bx, by = 800, 470; s = 1.0 + (0.12 * math.sin(min(1, max(0, t - (sub_at or 99))) * math.pi) if pressed else 0)
    w, h = int(330 * s), int(90 * s)
    d.rounded_rectangle((bx, by, bx + w, by + h), 14, fill=(90, 90, 90) if pressed else RED)
    d.text((bx + w / 2, by + h / 2), "SUBSCRIBED" if pressed else "SUBSCRIBE", font=ImageFont.truetype(COND, int(52 * s)), fill=(255, 255, 255), anchor="mm")
    d.text((bx + 165, 400), next_title or "Whose last hours next?", font=f, fill=BONE, anchor="mm")
    bug(c, x=34, y=30); return c

def corner(c, t, t0, t1, expr="shock", k=0):
    """reaction pop over footage, bottom-left; slides in 0.28 s, out 0.2 s. Use sparingly (owner: do not overuse)"""
    if not (t0 <= t < t1): return
    hd = head(expr, k, 560); u = back((t - t0) / 0.28); v = ease((t1 - t) / 0.2) if t1 - t < 0.2 else 1.0
    x = -40 - (1 - u) * 600 - (1 - v) * 600; y = H - hd.height + 70                    # bottom-LEFT, cropped coat on the edge
    c.alpha_composite(hd, (int(x), int(y)))
