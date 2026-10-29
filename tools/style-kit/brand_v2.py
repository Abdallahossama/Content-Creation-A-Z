"""Ask Habibi brand v2 (real Batata + marker). Writes everything into _style_kit/brand/:
logo_horizontal(.png / _on_navy), avatar_800, watermark_150, channel_banner_2560x1440, intro_card_1920x1080,
intro_sting.mp4 (2.4 s, for the CTA), end_screen_1920x1080.        python brand_v2.py  [sting]"""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from marker import *

OUT = KIT + "brand/"
SRC = KIT + "mascot/source/pexels-33948200.jpg"
TAGLINE = "questions you were\ntoo lazy to google."

_tex = {}
def texture(w, h):
    """the real dark paper behind the potato photo, toned into brand navy (no gradients, no glow)"""
    if (w, h) not in _tex:
        im = Image.open(SRC).convert("L").crop((0, 0, 1400, 1900))
        ar = w / h; cw, ch = (1400, 1400 / ar) if 1400 / 1900 < ar else (1900 * ar, 1900)
        im = im.crop((0, 0, int(cw), int(ch))).resize((w, h), Image.LANCZOS)
        L = np.asarray(im, np.float32); L = (L / L.mean()) ** 0.9
        base = np.array([11, 15, 64], np.float32)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        v = 1 - 0.35 * np.clip(np.sqrt(((xx - w / 2) / (w * 0.6)) ** 2 + ((yy - h / 2) / (h * 0.6)) ** 2) - 0.5, 0, 1)
        _tex[(w, h)] = Image.fromarray(np.clip(base * L[..., None] * v[..., None], 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    return _tex[(w, h)].copy()

def wordmark(size=200, progress=1.0, seed=4):
    """'ask' in white Rubik over 'habibi' in ink on a yellow highlighter swipe. progress animates the swipe."""
    a = bold("ask", size, WHITE); hb = bold("habibi", int(size * 1.08), NAVY)
    bh = hb.height * 1.08; band = swipe_band(hb.width + size * 0.25, bh, YEL, seed, progress)
    im = Image.new("RGBA", (max(a.width, band.width) + 20, int(a.height + band.height + size * 0.05)), (0, 0, 0, 0))
    im.alpha_composite(a, (int(size * 0.06), 0))
    by = int(a.height + size * 0.02); im.alpha_composite(band, (0, by))
    if progress > 0:
        reveal = Image.new("L", hb.size, 0)
        ImageDraw.Draw(reveal).rectangle((0, 0, int((band.width - size * 0.2) * progress), hb.height), fill=255)
        hb2 = hb.copy(); hb2.putalpha(Image.composite(hb.getchannel("A"), Image.new("L", hb.size, 0), reveal))
        im.alpha_composite(hb2, (int(size * 0.14), by + int(bh * 0.19)))
    im = im.rotate(2, Image.BICUBIC, expand=True); return im.crop(im.getbbox())

def batata(h, rot=-4, scale=1.0, expr="cool"): return sticker(BATATA + f"Batata_{expr}.png", h, border=max(6, h // 30), rot=rot, scale=scale)

def qmark(size, reveal=1.0): return hand("?", size, YEL, rot=12, thick=max(2, size // 40), reveal=reveal)

def logo(bg=None):
    W2, H2 = 1800, 640
    c = texture(W2, H2) if bg else Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    place(c, batata(560), 300, 330); place(c, qmark(190), 520, 120)
    place(c, wordmark(190), 640, 70, "lt")
    return c

def avatar():
    c = texture(800, 800)
    place(c, batata(600, rot=-3), 390, 440); place(c, qmark(190), 610, 190)
    return c

def watermark(): s = batata(150 - 12, rot=0); c = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); place(c, s, 75, 75); return c

def banner():
    c = texture(2560, 1440)                      # safe area for all devices: 1546 x 423 centred (x 507-2053, y 508-931)
    place(c, batata(400, rot=-5), 700, 720); place(c, qmark(130), 845, 560)
    wm = wordmark(150); place(c, wm, 930, 575, "lt")
    place(c, hand(TAGLINE, 64, YEL, rot=-4), 930 + wm.width + 50, 700, "lc")
    return c

def intro(t=9.0):
    c = texture(W, H); k = int(round(t * 30))
    place(c, batata(560, scale=pop(k - 2)), 600, 560)
    if t > 0.9: place(c, qmark(200, reveal=min(1, (t - 0.9) / 0.25)), 830, 300)
    if t > 0.3: place(c, wordmark(200, progress=min(1, (t - 0.45) / 0.35) if t > 0.45 else 0.0), 900, 380, "lt")
    return c

def end_screen():
    """YouTube end-screen template: put the 2 video elements on the marker frames and the subscribe button on the circle"""
    c = texture(W, H)
    place(c, hand("still awake?", 120, YEL, rot=-3), 960, 150)
    for x0 in (150, 1050):
        x1, y0, y1 = x0 + 720, 300, 705; pts = np.array([[x0, y0], [x1, y0 + 4], [x1 - 3, y1], [x0 + 2, y1 - 3], [x0, y0 - 2]], float)
        strokes(c, [np.concatenate([np.linspace(pts[i], pts[i + 1], 40) for i in range(4)])], WHITE, 7, seed=x0)
    place(c, hand("watch this next", 58, WHITE, rot=-2), 420, 760)
    strokes(c, circle_path(960, 905, 105, 100, seed=3), YEL, 9, seed=3)
    place(c, hand("subscribe\n(it's free)", 54, YEL, rot=-4), 1230, 905)
    place(c, batata(300, rot=7, expr="sleepy"), 1730, 905)
    return c

def save(c, name, rgb=True):
    p = OUT + name + ".png"; (c.convert("RGB") if rgb else c).save(p); print(p)

def sting():
    fps = 30; N = int(2.4 * fps); p = OUT + "intro_sting.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
                           "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", p], stdin=subprocess.PIPE)
    for i in range(N):
        c = shake(intro(i / fps), i - 2, 10, seed=5)
        ff.stdin.write(c.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait(); print(p)

def pasted(path, w, rot):
    """an example frame pasted on the board like a print: thin white edge, slight tilt, small shadow"""
    im = Image.open(path).convert("RGBA"); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    e = Image.new("RGBA", (im.width + 16, im.height + 16), (255, 255, 255, 255)); e.alpha_composite(im, (8, 8))
    s = Image.new("RGBA", (e.width + 30, e.height + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", e.size, (0, 0, 0, 120))
    s.alpha_composite(sh, (10, 12)); s = s.filter(ImageFilter.GaussianBlur(5)); s.alpha_composite(e, (0, 0))
    return s.rotate(rot, Image.BICUBIC, expand=True)

def board():
    """one-page visual brand reference (brand_board.png): logo, colours, type, Batata, the look, and what NOT to do"""
    BW, BH = 2400, 1640; c = texture(BW, BH)
    lg = logo(); lg = lg.resize((int(lg.width * 0.62), int(lg.height * 0.62)), Image.LANCZOS); place(c, lg, 50, 30, "lt")
    place(c, hand("brand board", 84, YEL, rot=-3), 1900, 110)
    place(c, hand("questions you were too lazy to google.", 46, WHITE, rot=-2), 1900, 215)
    # colours: marker swatches, not boxes
    place(c, hand("colours", 58, YEL, rot=-3), 150, 470)
    sw = [(YEL, NAVY, "#FFC21A  highlighter, notes"), (RED, WHITE, "#F0402F  marker on paper, alarms"),
          (WHITE, NAVY, "#FFFFFF  captions, big words"), ((28, 24, 22), WHITE, "#1C1816  batata's sharpie")]
    for i, (col, tc, label) in enumerate(sw):
        b = swipe_band(600, 74, col, seed=20 + i); place(c, b, 70, 520 + i * 100, "lt")
        place(c, bold(label, 32, tc), 115, 520 + i * 100 + 34, "lt")
    place(c, hand("background = #0B1050, the night\n(real navy paper texture, never a gradient)", 40, WHITE, rot=-1), 70, 935, "lt")
    # type
    place(c, hand("type", 58, YEL, rot=-3), 820, 470)
    place(c, outlined("captions: rubik bold", 48, WHITE, stroke=5), 760, 545, "lt")
    place(c, hand("notes: ink free", 60, WHITE, rot=0), 760, 630, "lt")
    f = font("C:/Windows/Fonts/impact.ttf", 60); t = Image.new("RGBA", (700, 110), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((8, 8), "THUMBNAILS: IMPACT", font=f, fill=WHITE, stroke_width=5, stroke_fill=BLACK); place(c, t.crop(t.getbbox()), 760, 735, "lt")
    place(c, hand("that's it. no other fonts.", 40, YEL, rot=-2), 760, 850, "lt")
    # the look: pasted examples + the rejected look crossed out
    place(c, hand("the look: real stuff + an editor's hand", 50, YEL, rot=-2), 1880, 470)
    place(c, pasted(KIT + "examples/2_receipt_finding.png", 400, 2), 1640, 640)
    place(c, pasted(KIT + "examples/5_photo_note.png", 400, -2), 2110, 650)
    place(c, pasted(KIT + "examples/shorts_endcard_part2.png", 150, 3), 1560, 930)
    no = "D:/why habibi/_archive/2026-10-12_rejected_midnight_noir/style_frames_v1/1_title_card.png"
    place(c, pasted(no, 330, -3), 1900, 905)
    strokes(c, [np.linspace([1760, 830], [2045, 980], 30), np.linspace([2045, 830], [1760, 980], 30)], RED, 13, seed=9)
    place(c, hand("not this: dot wordmark, caps labels,\nboxes, glow = ai slop", 36, RED, rot=-2), 1960, 1050)
    # batata
    place(c, hand("batata v2: a real potato + a sharpie face", 54, YEL, rot=-2), 520, 1095)
    ex = ["cool", "shocked", "deadpan", "sleepy", "sideeye", "smug", "sad", "panic", "fine"]
    for i, e in enumerate(ex):
        x = 150 + i * 262; place(c, batata(230, rot=[0, 5, -4, 3, -6, 4, -3, 6, -5][i], expr=e), x, 1300)
        place(c, hand(e + (" = brand" if e == "cool" else ""), 34, WHITE if e != "cool" else YEL, rot=-2), x, 1450)
    place(c, hand("everything else: brand\\BRAND_GUIDE.md", 40, WHITE, rot=-1), 1200, 1570)
    return c

if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    if sys.argv[1:] == ["sting"]: sting(); sys.exit()
    if sys.argv[1:] == ["board"]: save(board(), "brand_board"); sys.exit()
    save(logo(), "logo_horizontal", rgb=False); save(logo(bg=True), "logo_horizontal_on_navy")
    save(avatar(), "avatar_800"); save(watermark(), "watermark_150", rgb=False)
    save(banner(), "channel_banner_2560x1440"); save(intro(), "intro_card_1920x1080"); save(end_screen(), "end_screen_1920x1080")
