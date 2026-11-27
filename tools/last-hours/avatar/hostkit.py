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

def cutaway(t, t0, t1, expr="smirk", k=0, name=None):
    """full-frame host cutaway: pops up from below (0.35 s, overshoot), bobs gently, sinks out in the last 0.2 s"""
    c = host_bg().copy(); hd = head(expr, k, 860)
    u = back((t - t0) / 0.35); v = ease((t1 - t) / 0.2) if t1 - t < 0.2 else 1.0
    y = H - hd.height + 70 + (1 - u) * 520 + (1 - v) * 520 + 6 * math.sin((t - t0) * 2.2)
    c.alpha_composite(hd, (-50, int(y))); bug(c, x=W - 470, y=30)                    # left-anchored (cropped coat on the screen edge)
    if name:
        f = ImageFont.truetype(COND, 64); u2 = ease((t - t0 - 0.3) / 0.3); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((hd.width + 10, 430), name[0], font=f, fill=BONE + (int(255 * u2),), anchor="lm")
        d.rectangle((hd.width + 12, 478, hd.width + 12 + 380 * u2, 486), fill=RED + (int(255 * u2),))
        d.text((hd.width + 12, 520), name[1], font=ImageFont.truetype(COND, 40), fill=(170, 170, 170, int(255 * u2)), anchor="lm"); c.alpha_composite(lay)
    return c

def corner(c, t, t0, t1, expr="shock", k=0):
    """reaction pop over footage, bottom-left; slides in 0.28 s, out 0.2 s. Use sparingly (owner: do not overuse)"""
    if not (t0 <= t < t1): return
    hd = head(expr, k, 560); u = back((t - t0) / 0.28); v = ease((t1 - t) / 0.2) if t1 - t < 0.2 else 1.0
    x = -40 - (1 - u) * 600 - (1 - v) * 600; y = H - hd.height + 70                    # bottom-LEFT, cropped coat on the edge
    c.alpha_composite(hd, (int(x), int(y)))
