"""Avatar v2 (owner, 31 Oct: "on mobile with low brightness the logo doesn't appear, it is all black in black, no contrast").
Same approved noir File Keeper (draw_mark_real.render, figure only), now on a BRIGHT wall so the dark silhouette reads at 48 px and
at low screen brightness. Variants: A amber spotlight, B bone paper + blinds, C thumbnail yellow, D deep red.
Writes avatar_v2_<X>_800.png into channel/ and _sheet_avatar_v2.png (sizes on YouTube dark/light + a dimmed-phone row).
  uv run --no-project --with pillow --with numpy python avatar_contrast.py"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "D:/why habibi/_newchannel/brand/file_keeper")
import draw_mark_real as R
OUT = "D:/why habibi/_newchannel/brand/file_keeper/channel/"
N = R.N

def walls():
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32) / N
    d_head = np.hypot(xx - 0.5, yy - 0.32)                                    # light centred behind the hat
    stripes = R.blur((np.sin((xx * 0.55 + yy * 0.83) * 2 * np.pi * 7) > 0.35).astype(np.float32), 16)
    def lerp(c0, c1, t): return np.array(c0, np.float32) * (1 - t[..., None]) + np.array(c1, np.float32) * t[..., None]
    spot = np.clip(1 - d_head * 1.45, 0, 1) ** 1.3
    A = lerp((52, 36, 24), (246, 200, 128), spot)                             # amber lamp
    B = lerp((196, 186, 164), (240, 234, 218), np.clip(1 - d_head * 1.1, 0, 1)); B *= (1 - 0.10 * stripes)[..., None]   # bone + blinds
    C = lerp((226, 172, 0), (255, 214, 40), np.clip(1 - d_head * 1.2, 0, 1))  # thumbnail yellow
    D = lerp((92, 10, 14), (196, 34, 38), spot)                               # deep red
    # owner, 31 Oct: "the red is good and the [light streaks of the old avatar] is good" -> red wall + the venetian-blind light
    light = np.clip(1.1 - np.hypot(xx - 0.15, yy - 0.1) * 1.5, 0, 1) ** 1.6
    blinds = R.blur(stripes * light, 10)[..., None]
    E = lerp((120, 16, 22), (206, 40, 44), np.clip(1 - d_head * 1.2, 0, 1)) + blinds * np.array([150, 105, 70], np.float32)
    F = lerp((150, 22, 28), (232, 58, 54), np.clip(1 - d_head * 1.1, 0, 1)) + blinds * np.array([190, 140, 95], np.float32)
    # owner, 31 Oct: "make the light thing for all of them" -> the same blind light on amber (G), bone (H), yellow (I); on the
    # bright walls the gaps between the slats go a shade darker so the light bands still read
    lit = blinds / max(float(blinds.max()), 1e-6); slats = np.clip(light[..., None] * 1.4, 0, 1) * (1 - lit)
    G = lerp((70, 46, 28), (236, 180, 104), np.clip(1 - d_head * 1.25, 0, 1)) + blinds * np.array([150, 115, 70], np.float32)
    H = lerp((200, 190, 168), (238, 232, 216), np.clip(1 - d_head * 1.1, 0, 1)) * (1 - 0.20 * slats) + blinds * np.array([30, 28, 24], np.float32)
    I = lerp((226, 172, 0), (255, 210, 30), np.clip(1 - d_head * 1.2, 0, 1)) * (1 - 0.22 * slats) + blinds * np.array([40, 34, 10], np.float32)
    # owner picked A, 31 Oct: "more contrast in the lighting, or make it lower" -> the amber light moves down behind the shoulders
    # so the coat reads too: J lower, K lower + brighter + wider, L brightest (almost flat amber)
    d_low = np.hypot(xx - 0.5, yy - 0.52)
    J = lerp((66, 44, 28), (246, 200, 128), np.clip(1 - d_low * 1.25, 0, 1) ** 1.1)
    K = lerp((104, 70, 40), (252, 212, 146), np.clip(1 - d_low * 1.05, 0, 1) ** 0.9)
    Lw = lerp((150, 104, 58), (255, 224, 164), np.clip(1 - d_low * 0.9, 0, 1))
    return dict(A=A, B=B, C=C, D=D, E=E, F=F, G=G, H=H, I=I, J=J, K=K, L=Lw)

# outer corner pushed down into the shoulder (272, 628): at (292, 610) the smoothed coat corner left a wedge of wall showing (owner 31 Oct)
COLL_LOW = [(272, 628), (350, 475), (444, 500), (488, 548), (466, 664)]          # owner 31 Oct ("the collar: more contrast, or lower")
COLL_LOWER = [(292, 610), (352, 530), (444, 548), (488, 578), (452, 640)]        # owner 31 Oct, on the live G: "make the collar lower"
COLL_NARROW = [(330, 632), (392, 478), (450, 502), (490, 548), (466, 664)]       # owner 31 Oct, on P: "thinner in width, to the centre"

def avatar(wall, ring, collar_light=False, collar_low=False):
    keep = R.F.COLL_L, R.F.COLL_R
    if collar_low:
        cp = collar_low if isinstance(collar_low, list) else COLL_LOW
        R.F.COLL_L = cp; R.F.COLL_R = [(1000 - x, y) for x, y in cp]
    L = R.figure_layers()
    fig = np.asarray(R.render(bg_on=False), np.float32)
    R.F.COLL_L, R.F.COLL_R = keep
    if collar_light:                                                          # warm charcoal collar that catches the lamp
        cm = R.blur(L["coll"], 1.0)[..., None]
        fig = fig * (1 - cm) + (fig * 2.1 + np.array([30, 22, 12], np.float32)) * cm
    a = R.blur(L["body"], 1.2)[..., None]
    sh = R.blur(np.roll(np.roll(L["body"], int(0.03 * N), 1), int(0.02 * N), 0), 22)[..., None]      # his soft shadow on the wall
    img = wall * (1 - 0.45 * sh)
    img = img * (1 - a) + fig * a
    img += R.rng.normal(0, 4.0, (N, N, 1)).astype(np.float32)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((1024, 1024), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (1024, 1024), 0); ImageDraw.Draw(m).ellipse((8, 8, 1015, 1015), fill=255)
    out = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    if ring: ImageDraw.Draw(out).ellipse((14, 14, 1009, 1009), outline=ring, width=12)
    return out.resize((800, 800), Image.LANCZOS)

def sheet(avs):
    old = Image.open(OUT + "avatar_800.png").convert("RGBA")
    items = [("NOW", old)] + list(avs.items())
    W = 40 + len(items) * 300; S = Image.new("RGB", (W, 790), (15, 15, 15)); d = ImageDraw.Draw(S)
    f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26); fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    d.rectangle((0, 470, W, 600), fill=(255, 255, 255))
    for i, (n, im) in enumerate(items):
        x = 40 + i * 300
        d.text((x + 130, 14), n, font=f, fill=(240, 240, 240), anchor="mt")
        big = im.resize((240, 240), Image.LANCZOS); S.paste(big, (x + 10, 50), big)
        for j, sz in enumerate((88, 48, 32)):                                  # YouTube dark mode
            sm = im.resize((sz, sz), Image.LANCZOS); S.paste(sm, (x + 10 + j * 100, 330 + (88 - sz) // 2), sm)
        for j, sz in enumerate((88, 48, 32)):                                  # YouTube light mode
            sm = im.resize((sz, sz), Image.LANCZOS); S.paste(sm, (x + 10 + j * 100, 490 + (88 - sz) // 2), sm)
    d.text((20, 300), "YouTube dark mode", font=fs, fill=(170, 170, 170)); d.text((20, 474), "light mode", font=fs, fill=(90, 90, 90))
    # dimmed phone: the whole strip at ~25 % brightness (gamma), as on a phone turned down
    dim = S.crop((0, 326, W, 440)).point(lambda v: int(255 * (v / 255) ** 1.6 * 0.38))
    S.paste(dim, (0, 641)); d.text((20, 612), "phone at low brightness", font=fs, fill=(120, 120, 120))
    p = OUT + "_sheet_avatar_v2_" + "".join(avs) + ".png"; S.save(p); return p

if __name__ == "__main__":
    W = walls(); BONE = (236, 230, 214, 255); INK = (20, 20, 22, 255)
    rings = dict(A=BONE, B=INK, C=INK, D=BONE, E=BONE, F=BONE, G=BONE, H=INK, I=INK, J=BONE, K=BONE, L=BONE)
    # collar variants on the owner's amber pick A: M lighter collar, N lower collar, O both
    COLLAR = dict(M=("A", True, False), N=("A", False, True), O=("A", True, True),
                  P=("G", False, True), Q=("G", False, COLL_LOWER),           # the live G with a lower / much lower collar
                  R=("G", False, COLL_NARROW))                                # P with a narrower collar
    avs = {}
    for k in (sys.argv[1] if len(sys.argv) > 1 else "ABCD"):
        wk, cl, lo = COLLAR.get(k, (k, False, False))
        avs[k] = avatar(W[wk], rings[wk], cl, lo); avs[k].save(OUT + f"avatar_v2_{k}_800.png")
    print(sheet(avs))
