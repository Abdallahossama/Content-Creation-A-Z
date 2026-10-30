"""Channel banner v2 (owner, 30 Oct 2026: "the old banner was good too: keep its background, and the current dark one on top, a little
see-through, so the background is seen"). The old banner's real Alcatraz photo (Pexels 17765343, B&W) under the noir dark layer +
light streaks, the File Keeper and the title as in v1. All text inside YouTube's 1546 x 423 safe area.
  uv run --no-project --with pillow --with numpy python banner_v2.py [dark_opacity ...]   -> channel/banner_2560x1440_v2[_NN].jpg"""
import sys
import numpy as np
from PIL import Image, ImageFilter
NC = "D:/why habibi/_newchannel/"; sys.path.insert(0, NC)
import lastkit as L
from lastkit import BONE, STEEL, COND, TYPE, SER
MK = NC + "brand/file_keeper/"; CH = MK + "channel/"; bw, bh = 2560, 1440
_CUT = {}
def cutout(S=900):
    """the noir File Keeper WITHOUT his wall (draw_mark_real.render(bg_on=False)), alpha = his silhouette + the rim light, a soft shadow
    behind him, the coat dissolving at the bottom (no dark square on the photo)"""
    if S not in _CUT:
        sys.path.insert(0, MK); import draw_mark_real as R
        fig = R.render(bg_on=False).convert("RGB").resize((S, S), Image.LANCZOS); body = R.figure_layers()["body"]
        a = np.asarray(Image.fromarray((body * 255).astype(np.uint8)).resize((S, S), Image.LANCZOS).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
        ys = np.linspace(0, 1, S)[:, None]; a = a * np.clip((1 - ys) / 0.22, 0, 1)                            # coat fades out at the bottom
        sh = np.asarray(Image.fromarray((np.roll(np.roll(a, 26, 1), 14, 0) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40)), np.float32) / 255
        out = np.zeros((S, S, 4), np.float32); f = np.asarray(fig, np.float32)
        aa = np.clip(a + sh * 0.55 * (1 - a), 0, 1)                                                               # figure over its own soft shadow
        out[..., :3] = (f * a[..., None] + np.array([6, 6, 7], np.float32) * (sh * 0.55 * (1 - a))[..., None]) / np.maximum(aa, 1e-4)[..., None]
        out[..., 3] = aa * 255; _CUT[S] = (Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA"), a)
    return _CUT[S]
def banner(dark=0.70):
    ph = L.bw(NC + "01_alcatraz/media/pexels_17765343.jpg"); s = max(bw / ph.width, bh / ph.height)
    ph = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS); x0, y0 = (ph.width - bw) // 2, (ph.height - bh) // 2
    photo = np.asarray(ph.crop((x0, y0, x0 + bw, y0 + bh)).convert("RGB"), np.float32)
    yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32); u = (xx / bw * 0.55 * bw / bh + yy / bh * 0.83)             # the v1 light streaks
    light = np.clip(1.1 - np.hypot(xx / bw - 0.25, yy / bh - 0.2) * 1.6, 0, 1) ** 2
    st = (np.sin(u * 2 * np.pi * 7) > 0.35).astype(np.float32) * light
    st = np.asarray(Image.fromarray((st * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18)), np.float32) / 255 * 0.5
    ink = np.array([12, 13, 15], np.float32)
    bg = photo * (1 - dark) + ink * dark + st[..., None] * np.array([150, 112, 70]) * (0.6 + 0.4 * dark)        # the dark layer, see-through
    ban = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")
    hero, alpha = cutout(640); ban.alpha_composite(hero, (1520, 437))                     # the File Keeper, cut out by his silhouette. Owner 30 Oct:
    # "the head is cropped": desktop shows only the centre strip (y ~508-931), so hat top at y 560, shoulders 866, right edge 2051 (phone safe 2053)
    L.text(ban, "THE LAST HOURS", 1060, 640, 150, BONE, COND); L.rule(ban, 700, 1420, 735, 99, 0, width=8)
    L.text(ban, "Famous cases, told hour by hour, from the real files.", 1060, 795, 46, BONE, SER)
    L.text(ban, "WITH THE FILE KEEPER  ·  NEW FILES SUN + MON", 1060, 870, 34, STEEL, TYPE)
    return ban.convert("RGB")
if __name__ == "__main__":
    from PIL import ImageDraw
    for d in [float(x) for x in sys.argv[1:]] or [0.70]:
        p = CH + ("banner_2560x1440_v2.jpg" if d == 0.70 else f"banner_2560x1440_v2_{int(d * 100)}.jpg"); b = banner(d); b.save(p, quality=92); print(p)
        pv = Image.new("RGB", (1280, 212 + 24 + 212), (24, 24, 26)); pv.paste(b.crop((0, 508, 2560, 931)).resize((1280, 212)), (0, 0))     # what YouTube shows:
        pv.paste(b.crop((507, 508, 2053, 931)).resize((int(1546 * 212 / 423), 212)), (0, 236)); pv.save(p.replace(".jpg", "_HOW_IT_SHOWS.jpg"), quality=90)   # desktop / phone
