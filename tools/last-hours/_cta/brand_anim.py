"""The File Keeper animations (owner, 30 Oct 2026: "make this display come in, not out of nowhere: the logo and the text written,
a different cool sound for each, smoothly; subscribe and like too"). Shared by brand_patch.py (already-rendered files) and the renderers.
  stamp_apply(c, u, label) -> the stamp ON a frame (frosted see-through band); stamp_frame(u, label) -> full-frame RGBA, STAMP_LEN s: dark band sweeps in, the mark slides + turns + lands, "the" drops,
                            LAST HOURS builds letter by letter, the file line types out, all fade together.   STAMP_SFX
  pill_frame(u, text)    -> W x PILL_H RGBA, PILL_LEN s: the pill slides in, a cursor clicks SUBSCRIBE -> SUBSCRIBED + tick,
                            a LIKE chip pops, it slides out.                                                       PILL_SFX
  end_buttons(c, t, t_like, t_sub) -> on the end card: LIKE / SUBSCRIBE pop in on the words "like" / "Subscribe", the cursor presses
                            SUBSCRIBE.                                                                              end_sfx(t_like, t_sub)
Each SFX list: (seconds from the start, sfx file in _newchannel/sfx, dB under the voice, max length s)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import lastkit as L
from lastkit import W, H, BONE, RED, STEEL, COND, TYPE, SER, ease
MK = "D:/why habibi/_newchannel/brand/file_keeper/"
_M = {}
def mark(name, size):
    k = (name, size)
    if k not in _M: _M[k] = Image.open(MK + f"mark_{name}.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    return _M[k]
def clamp(x): return max(0.0, min(1.0, x))
def back(x, s=1.6): x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2            # ease-out with a small overshoot
def fade(im, a):
    if a >= 0.999: return im
    arr = np.asarray(im, np.float32).copy(); arr[..., 3] *= max(0.0, a); return Image.fromarray(arr.astype(np.uint8))

# ------------------------------------------------------------------ the 2.9 s channel stamp
STAMP_LEN = 2.9
STAMP_SFX = [(0.0, "whoosh_tunnel_reverb", -24, 1.2), (0.1, "whoosh_metal_hit", -22, 0.9), (0.42, "hit_cinematic_deep_impact", -21, 1.6),
             (0.95, "typewriter_typing_old", -27, 0.7), (2.5, "whoosh_fast_transition", -30, 0.8)]
BAND_INK, BAND_DARK, BAND_BLUR = (7, 7, 8), 0.70, 3       # owner 30 Oct: the old see-through band, but darker: "just the background be seen"
def band_mask(u):
    """the band's cover 0..1 per pixel (H x W): sweeps in from the left, soft top/bottom edges, fades out with the stamp"""
    out = ease((STAMP_LEN - u) / 0.35); ba = ease(u / 0.18) * out; sweep = int(W * ease(u / 0.22)); y0, y1 = H // 2 - 150, H // 2 + 150
    m = np.zeros((H, W), np.float32); m[y0:y1 + 1, :sweep] = ba
    for k in range(1, 18): m[y0 - k, :sweep] = m[y1 + k, :sweep] = ba * (1 - k / 18) ** 2
    return m
def _blur_np(a, s):
    """gaussian-like blur of an H x W (x C) float array (three box passes per axis)"""
    r = max(1, int(round(s * 0.87)))
    for ax in (0, 1):
        for _ in range(3):
            cs = np.cumsum(np.pad(a, [(r + 1, r) if i == ax else (0, 0) for i in range(a.ndim)], mode="edge"), axis=ax); n = a.shape[ax]
            a = (np.take(cs, np.arange(2 * r + 1, n + 2 * r + 1), axis=ax) - np.take(cs, np.arange(0, n), axis=ax)) / (2 * r + 1)
    return a
_OLD = {}
_YC = np.array([[0.299, 0.587, 0.114], [-0.168736, -0.331264, 0.5], [0.5, -0.418688, -0.081312]], np.float32); _YCi = np.linalg.inv(_YC).astype(np.float32)
def erase_old_stamp(c, u, label):
    """Files rendered before 30 Oct carry the OLD 2.2 s stamp (lastkit: a 59 % black band H/2 +-150 + "the / LAST HOURS / file line",
    alpha ease in/out 0.35 s). Rebuild the clean scene under it (RGBA, in place) so the see-through band shows the scene, not the old
    letters. Same clock as the old render, so its alpha is known: the band and faint letters are SUBTRACTED exactly; where the letters
    were nearly solid, the scene is filled from the pixels around them."""
    if not 0 <= u < 2.2: return c
    al = ease(u / 0.35) * ease((2.2 - u) / 0.35); a = int(150 * al) / 255; at = int(255 * al) / 255
    if al <= 0: return c
    if label not in _OLD:
        cov = np.zeros((H, W), np.float32); col = np.zeros((H, W, 3), np.float32); sl = slice(H // 2 - 150, H // 2 + 151)
        for s_, y_, sz, cl, fn in (("the", H / 2 - 95, 52, STEEL, SER), ("LAST HOURS", H / 2 + 5, 150, BONE, COND), (label, H / 2 + 105, 34, STEEL, TYPE)):
            mk = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L.text(mk, s_, W / 2, y_, sz, cl, fn); k = np.asarray(mk.getchannel("A"), np.float32) / 255
            cov = np.maximum(cov, k); col[k > 0] = cl
        hole = np.asarray(Image.fromarray((cov * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7)), np.float32)[sl] > 8
        _OLD[label] = (cov[sl], col[sl], hole)
    cov, col, hole = _OLD[label]; ya = H // 2 - 150; al_t = (cov * at)[..., None]
    arr = np.asarray(c, np.float32).copy(); x = arr[ya:ya + cov.shape[0], :, :3]
    aY = al_t[..., 0]; aC = _blur_np(aY, 1.2)[..., None]; xy, cy = x @ _YC.T, col @ _YC.T                  # exact where the letters were faint;
    rec = np.concatenate([(xy[..., :1] - cy[..., :1] * al_t) / np.maximum(1 - al_t, 0.1),                     # colour in YCbCr: the video's 4:2:0
                          (xy[..., 1:] - cy[..., 1:] * aC) / np.maximum(1 - aC, 0.1)], -1) @ _YCi.T / max(1 - a, 0.05)   # colour is smeared 1-2 px
    wf = np.maximum(np.clip((cov * at - 0.35) / 0.35, 0, 1), hole * np.clip((al - 0.5) / 0.3, 0, 1))[..., None]   # nearly solid -> fill
    if wf.max() > 0:
        ok = (~hole).astype(np.float32)
        f7, w7 = _blur_np(rec * ok[..., None], 7), _blur_np(ok, 7); f22, w22 = _blur_np(rec * ok[..., None], 22), _blur_np(ok, 22)
        fill = np.where((w7 > 0.05)[..., None], f7 / np.maximum(w7, 1e-4)[..., None], f22 / np.maximum(w22, 1e-4)[..., None])
        rec = rec * (1 - wf) + fill * wf
    arr[ya:ya + cov.shape[0], :, :3] = np.clip(rec, 0, 255); c.paste(Image.fromarray(arr.astype(np.uint8), "RGBA")); return c
def stamp_apply(c, u, label, mark_name="noir_badge"):
    """the stamp ON a frame (RGBA, in place): a see-through dark band (the scene darkened 70 %, a touch softened, still seen),
    then the mark, the letters and the file line. Already-rendered files: erase_old_stamp() first."""
    m = band_mask(u)
    if m.max() > 0:
        ya, yb, pad = H // 2 - 168, H // 2 + 169, 3 * BAND_BLUR
        fro = np.asarray(c.crop((0, ya - pad, W, yb + pad)).convert("RGB").filter(ImageFilter.GaussianBlur(BAND_BLUR)), np.float32)[pad:pad + yb - ya]
        fro = fro * (1 - BAND_DARK) + np.array(BAND_INK, np.float32) * BAND_DARK
        base = np.asarray(c.crop((0, ya, W, yb)), np.float32).copy(); mm = m[ya:yb, :, None]
        base[..., :3] = base[..., :3] * (1 - mm) + fro * mm; c.paste(Image.fromarray(base.astype(np.uint8), c.mode), (0, ya))
    c.alpha_composite(stamp_frame(u, label, mark_name, band=False)); return c
def stamp_frame(u, label, mark_name="noir_badge", band=True):
    out = ease((STAMP_LEN - u) / 0.35); c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    ba = ease(u / 0.18) * out; y0, y1 = H / 2 - 150, H / 2 + 150
    sweep = W * ease(u / 0.22)                                                               # the band sweeps in from the left
    if band:                                                                                 # solid version (stamp_apply draws the frosted one)
        d.rectangle((0, y0, sweep, y1), fill=BAND_INK + (int(255 * ba),))
        for k in range(18):                                                                  # soft top/bottom edges
            a = int(255 * ba * (1 - k / 18) ** 2); d.line((0, y0 - k, sweep, y0 - k), fill=BAND_INK + (a,)); d.line((0, y1 + k, sweep, y1 + k), fill=BAND_INK + (a,))
    k = back((u - 0.08) / 0.4); m = mark(mark_name, 250).rotate(-28 * (1 - clamp((u - 0.08) / 0.4)), resample=Image.BICUBIC)
    c.alpha_composite(fade(m, clamp((u - 0.08) / 0.12) * out), (int(-260 + (400 + 260) * k - m.width / 2), int(H / 2 - m.height / 2)))
    if u > 0.3:
        a = ease((u - 0.3) / 0.3) * out; L.text(c, "the", W / 2, H / 2 - 95 - 12 * (1 - ease((u - 0.3) / 0.3)), 52, STEEL, SER, alpha=a)
    f = L.font(COND, 150); word = "LAST HOURS"; ws = [f.getlength(ch) for ch in word]; x = W / 2 - sum(ws) / 2
    for i, (ch, wl) in enumerate(zip(word, ws)):                                             # built letter by letter
        ti = 0.40 + i * 0.045; a = ease((u - ti) / 0.12) * out
        if a > 0: d.text((x + wl / 2, H / 2 + 5 + 26 * (1 - ease((u - ti) / 0.18))), ch, font=f, fill=BONE + (int(255 * a),), anchor="mm")
        x += wl
    if u > 0.95:                                                                             # the file line types out
        ft = L.font(TYPE, 34); full = ft.getlength(label); n = int(len(label) * clamp((u - 0.95) / 0.6))
        d.text((W / 2 - full / 2, H / 2 + 105), label[:n], font=ft, fill=STEEL + (int(255 * out),), anchor="lm")
    return c

# ------------------------------------------------------------------ the ~75 % subscribe pill
PILL_LEN, PILL_H, T_CLICK, T_LIKE = 4.6, 200, 1.75, 2.15
PILL_SFX = [(0.0, "whoosh_fast_transition", -24, 0.8), (T_CLICK, "camera_classic_click", -16, 0.5), (T_CLICK + 0.06, "typewriter_return_bell", -24, 1.2),
            (T_LIKE, "camera_auto_focus", -24, 0.5), (4.15, "whoosh_fast_transition", -30, 0.8)]
def thumb(d, cx, cy, s, fill):
    """a small thumbs-up drawn from shapes (no emoji font needed)"""
    d.rounded_rectangle((cx - 0.15 * s, cy - 0.05 * s, cx + 0.42 * s, cy + 0.48 * s), int(0.12 * s), fill=fill)
    d.polygon([(cx - 0.12 * s, cy + 0.02 * s), (cx + 0.02 * s, cy - 0.5 * s), (cx + 0.2 * s, cy - 0.46 * s), (cx + 0.16 * s, cy + 0.02 * s)], fill=fill)
    d.rounded_rectangle((cx - 0.46 * s, cy - 0.02 * s, cx - 0.22 * s, cy + 0.48 * s), int(0.05 * s), fill=fill)
def tick(d, x, y, s, fill): d.line([(x, y), (x + 0.35 * s, y + 0.35 * s), (x + s, y - 0.4 * s)], fill=fill, width=max(3, int(s / 6)), joint="curve")
def cursor(c, x, y, a, press=0.0):
    s = 1.0 - 0.15 * press; pts = [(0, 0), (0, 34), (9, 26), (16, 41), (22, 38), (15, 24), (27, 24)]
    lay = Image.new("RGBA", (40, 50), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); dl.polygon([(px * s + 4, py * s + 2) for px, py in pts], fill=(255, 255, 255, int(255 * a)), outline=(0, 0, 0, int(255 * a)))
    c.alpha_composite(lay, (int(x), int(y)))
def pill_frame(u, text, mark_name="noir_folder"):
    c = Image.new("RGBA", (W, PILL_H), (0, 0, 0, 0)); d = ImageDraw.Draw(c); fs = L.font(COND, 46); fl = L.font(COND, 34)
    sub_on = u >= T_CLICK; btxt = "SUBSCRIBED" if sub_on else "SUBSCRIBE"; bw = fs.getlength("SUBSCRIBED") + 70
    w = int(118 + bw + 26 + fs.getlength("·  " + text) + 30 + 150); k = ease(u / 0.4) * ease((PILL_LEN - u) / 0.4); x = 30 - (1 - k) * (w + 40); al = min(1.0, 2.2 * k)
    d.rounded_rectangle((x, 8, x + w, 104), 26, fill=(14, 14, 16, int(250 * al)), outline=RED + (int(255 * al),), width=4)
    c.alpha_composite(fade(mark(mark_name, 84), al), (int(x + 18), 14))
    press = clamp(1 - abs(u - T_CLICK) / 0.12); bs = 1 - 0.08 * press; bx0, bx1 = x + 112, x + 112 + bw * bs
    d.rounded_rectangle((bx0, 56 - 30 * bs, bx1, 56 + 30 * bs), 30, fill=((70, 70, 74) if sub_on else RED) + (int(255 * al),))
    d.text(((bx0 + bx1) / 2 - (14 if sub_on else 0), 56), btxt, font=fs, fill=BONE + (int(255 * al),), anchor="mm")
    if sub_on: tick(d, bx1 - 40, 58, 22, BONE + (int(255 * al),))
    tx = bx1 + 26; d.text((tx, 56), "·  " + text, font=fs, fill=BONE + (int(255 * al),), anchor="lm")
    if u >= T_LIKE:                                                                          # the LIKE chip pops at the right end
        p = back((u - T_LIKE) / 0.25); lx = x + w - 140; ch = Image.new("RGBA", (130, 70), (0, 0, 0, 0)); dc = ImageDraw.Draw(ch)
        dc.rounded_rectangle((0, 0, 129, 69), 34, fill=(236, 230, 214, int(255 * al))); thumb(dc, 32, 33, 34, (14, 14, 16, int(255 * al)))
        dc.text((84, 35), "LIKE", font=fl, fill=(14, 14, 16, int(255 * al)), anchor="mm"); ch = ch.resize((max(1, int(130 * p)), max(1, int(70 * p))), Image.BICUBIC)
        c.alpha_composite(ch, (int(lx + 65 - ch.width / 2), int(56 - ch.height / 2)))
    if 1.0 <= u < 2.5:                                                                       # the cursor glides to SUBSCRIBE and clicks
        g = ease((u - 1.0) / 0.65); cx0, cy0 = x + w + 60, 150; cx1, cy1 = (bx0 + bx1) / 2 + 10, 62
        cursor(c, cx0 + (cx1 - cx0) * g, cy0 + (cy1 - cy0) * g, ease((u - 1.0) / 0.2) * ease((2.5 - u) / 0.3) * al, press)
    return c

# ------------------------------------------------------------------ LIKE / SUBSCRIBE on the end card, on the spoken words
def end_buttons(c, t, t_like, t_sub):
    d = ImageDraw.Draw(c); fs = L.font(COND, 44)
    if t_like is not None and t >= t_like - 0.1:                                            # left of the seal
        p = back((t - t_like + 0.1) / 0.3); on = t >= t_like + 0.35
        b = Image.new("RGBA", (260, 84), (0, 0, 0, 0)); db = ImageDraw.Draw(b)
        db.rounded_rectangle((0, 0, 259, 83), 42, fill=(RED if on else (236, 230, 214)) + (255,))
        thumb(db, 62, 42, 40, (BONE if on else (14, 14, 16)) + (255,)); db.text((165, 44), "LIKE", font=fs, fill=(BONE if on else (14, 14, 16)) + (255,), anchor="mm")
        b = b.resize((max(1, int(260 * p)), max(1, int(84 * p))), Image.BICUBIC); c.alpha_composite(b, (int(W / 2 - 440 - b.width / 2), int(245 - b.height / 2)))
    if t_sub is not None and t >= t_sub - 0.1:                                              # right of the seal, then the cursor presses it
        p = back((t - t_sub + 0.1) / 0.3); on = t >= t_sub + 0.55; press = clamp(1 - abs(t - t_sub - 0.55) / 0.12); s = p * (1 - 0.08 * press)
        b = Image.new("RGBA", (340, 84), (0, 0, 0, 0)); db = ImageDraw.Draw(b)
        db.rounded_rectangle((0, 0, 339, 83), 42, fill=((70, 70, 74) if on else RED) + (255,))
        db.text((170 - (16 if on else 0), 44), "SUBSCRIBED" if on else "SUBSCRIBE", font=fs, fill=BONE + (255,), anchor="mm")
        if on: tick(db, 285, 46, 22, BONE + (255,))
        b = b.resize((max(1, int(340 * s)), max(1, int(84 * s))), Image.BICUBIC); bx, by = W / 2 + 440, 245
        c.alpha_composite(b, (int(bx - b.width / 2), int(by - b.height / 2)))
        if t_sub + 0.1 <= t < t_sub + 1.3:
            g = ease((t - t_sub - 0.1) / 0.45); cursor(c, bx + 200 + (40 - 200) * g, by + 120 + (0 - 120) * g, ease((t_sub + 1.3 - t) / 0.3), press)
def end_sfx(t_like, t_sub):
    out = []
    if t_like is not None: out += [(t_like - 0.1, "camera_auto_focus", -24, 0.5), (t_like + 0.35, "camera_classic_click", -18, 0.5)]
    if t_sub is not None: out += [(t_sub - 0.1, "whoosh_fast_transition", -30, 0.6), (t_sub + 0.55, "camera_classic_click", -16, 0.5), (t_sub + 0.6, "typewriter_return_bell", -24, 1.2)]
    return out
def word_time(words, *keys):
    """start time of the first word starting with one of keys (words = [(start, end, word)])"""
    for a, b, w in words:
        if any(w.lower().strip(".,?!").startswith(k) for k in keys): return a
    return None

# ------------------------------------------------------------------ the case tab that now covers the old red pill (no ask: the spoken mid ask does that)
CHIP_SFX = [(0.0, "whoosh_fast_transition", -28, 0.8), (4.15, "whoosh_fast_transition", -32, 0.8)]
def chip_frame(u, text, mark_name="noir_folder"):
    """W x PILL_H, PILL_LEN s: an ink case tab with the folder mark and the file line slides over the old pill and back out"""
    c = Image.new("RGBA", (W, PILL_H), (0, 0, 0, 0)); d = ImageDraw.Draw(c); ft = L.font(TYPE, 34)
    w = max(780, int(118 + ft.getlength(text) + 40)); k = ease(u / 0.4) * ease((PILL_LEN - u) / 0.4); x = 30 - (1 - k) * (w + 40); al = min(1.0, 2.2 * k)
    d.rounded_rectangle((x, 8, x + w, 104), 26, fill=(14, 14, 16, int(250 * al)), outline=STEEL + (int(200 * al),), width=3)
    c.alpha_composite(fade(mark(mark_name, 84), al), (int(x + 18), 14))
    n = int(len(text) * clamp((u - 0.35) / 0.7)); d.text((x + 118, 56), text[:n], font=ft, fill=BONE + (int(255 * al),), anchor="lm")
    return c

# ------------------------------------------------------------------ the spoken mid-video ask (owner, 30 Oct: at a cliffhanger, polite, like + subscribe + comments)
def bubble(d, cx, cy, s, fill):
    d.rounded_rectangle((cx - 0.5 * s, cy - 0.38 * s, cx + 0.5 * s, cy + 0.3 * s), int(0.18 * s), fill=fill)
    d.polygon([(cx - 0.22 * s, cy + 0.26 * s), (cx - 0.3 * s, cy + 0.55 * s), (cx + 0.02 * s, cy + 0.28 * s)], fill=fill)
def mid_sfx(dur, t_like, t_sub, t_com):
    out = [(0.0, "whoosh_ghostly", -26, 1.2), (0.12, "hit_short_bass", -24, 1.0), (dur - 0.55, "whoosh_fast_transition", -26, 0.8)]
    if t_like is not None: out += [(t_like - 0.1, "camera_auto_focus", -24, 0.5), (t_like + 0.35, "camera_classic_click", -18, 0.5)]
    if t_sub is not None: out += [(t_sub - 0.1, "camera_auto_focus", -26, 0.5), (t_sub + 0.55, "camera_classic_click", -16, 0.5), (t_sub + 0.6, "typewriter_return_bell", -24, 1.2)]
    if t_com is not None: out += [(t_com - 0.05, "paper_slide", -24, 0.8)]
    return out
def _btn(label, w, fill, ink, icon=None):
    b = Image.new("RGBA", (w, 84), (0, 0, 0, 0)); db = ImageDraw.Draw(b); fs = L.font(COND, 44)
    db.rounded_rectangle((0, 0, w - 1, 83), 42, fill=fill + (255,))
    if icon == "thumb": thumb(db, 58, 42, 40, ink + (255,))
    if icon == "bubble": bubble(db, 56, 40, 46, ink + (255,))
    db.text(((w + (56 if icon else 0)) / 2, 44), label, font=fs, fill=ink + (255,), anchor="mm"); return b
def mid_overlay(c, t, dur, t_like, t_sub, t_com, mark_name="noir_badge"):
    """over a frozen, dimmed frame: the File Keeper badge drops in, then LIKE / SUBSCRIBE / COMMENT pop on their spoken words"""
    a = ease(t / 0.4) * ease((dur - t) / 0.45)
    c.alpha_composite(Image.new("RGBA", (W, H), (6, 6, 7, int(205 * a))))
    k = back((t - 0.1) / 0.45); m = fade(mark(mark_name, 230), clamp((t - 0.1) / 0.15) * a)
    c.alpha_composite(m, (int(W / 2 - 115), int(330 - 115 - 90 * (1 - k))))
    if t > 0.45: L.text(c, "THE FILE KEEPER", W / 2, 485, 38, BONE, TYPE, alpha=ease((t - 0.45) / 0.3) * a)
    row = []
    if t_like is not None and t >= t_like - 0.1:
        on = t >= t_like + 0.35; row.append((W / 2 - 400, back((t - t_like + 0.1) / 0.3), _btn("LIKE", 250, RED if on else (236, 230, 214), BONE if on else (14, 14, 16), "thumb"), 0.0))
    if t_sub is not None and t >= t_sub - 0.1:
        on = t >= t_sub + 0.55; press = clamp(1 - abs(t - t_sub - 0.55) / 0.12)
        b = _btn("SUBSCRIBED" if on else "SUBSCRIBE", 340, (70, 70, 74) if on else RED, BONE)
        if on: tick(ImageDraw.Draw(b), 292, 46, 22, BONE + (255,))
        row.append((W / 2, back((t - t_sub + 0.1) / 0.3) * (1 - 0.08 * press), b, press))
    if t_com is not None and t >= t_com - 0.05:
        row.append((W / 2 + 420, back((t - t_com + 0.05) / 0.3), _btn("COMMENT", 300, (236, 230, 214), (14, 14, 16), "bubble"), 0.0))
    for x, s, b, _ in row:
        b = fade(b.resize((max(1, int(b.width * s)), max(1, int(b.height * s))), Image.BICUBIC), a); c.alpha_composite(b, (int(x - b.width / 2), int(620 - b.height / 2)))
    if t_sub is not None and t_sub + 0.1 <= t < t_sub + 1.3:
        g = ease((t - t_sub - 0.1) / 0.45); press = clamp(1 - abs(t - t_sub - 0.55) / 0.12)
        cursor(c, W / 2 + 220 + (30 - 220) * g, 620 + 140 + (0 - 140) * g, ease((t_sub + 1.3 - t) / 0.3) * a, press)
