"""Owner 27 Nov: the ChatGPT scenes are good but Noah melts into them ("looks like an AI picture"). Thumbnail treatment:
cut Noah out of the owner's scene (rembg isnet), blur + darken the scene behind him, enlarge him, add a back glow behind the head
and a two-colour rim light on his edges, then the real-photo cards, words and stamp (make_qany3 helpers).
  F:/thumbkit/venv/Scripts/python.exe make_pop.py <scene.png> <cut.png> <out.jpg> <preset>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import make_qany3 as Q                       # card / text_band / tag / stamp / string / first / F
W, H = 1280, 720

def fit(im, cx=0.5):
    s = H / im.height; im = im.resize((int(im.width * s), H), Image.LANCZOS)
    x = int(im.width * cx - W / 2); x = max(0, min(im.width - W, x)); return im.crop((x, 0, x + W, H))

def pop(scene, cut, cx=0.5, scale=1.14, blur=3, dark=0.62, left=(60, 140, 255), right=(255, 140, 40), glow=(255, 225, 170)):
    bg = fit(scene.convert("RGB"), cx).filter(ImageFilter.GaussianBlur(blur))
    bg = ImageEnhance.Brightness(ImageEnhance.Color(bg).enhance(1.15)).enhance(dark).convert("RGBA")
    sub = fit(cut, cx); a = sub.split()[3]
    bb = a.getbbox(); hx = (bb[0] + bb[2]) // 2; hy = bb[1] + 120                       # head ~ top of the subject
    g = Image.new("L", (W, H), 0); d = ImageDraw.Draw(g)                                   # back glow behind the head
    for r in range(420, 0, -6): d.ellipse((hx - r * 1.3, hy - r, hx + r * 1.3, hy + r), fill=int(200 * (1 - r / 420) ** 1.6))
    bg.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (W, H), glow).split(), g.filter(ImageFilter.GaussianBlur(30)))))
    nw, nh = int(W * scale), int(H * scale)                                                # enlarge, anchored bottom-centre
    sub = sub.resize((nw, nh), Image.LANCZOS); ox = int(hx - hx * scale); oy = H - nh + 30
    big = Image.new("RGBA", (W, H), (0, 0, 0, 0)); big.alpha_composite(sub, (ox, oy)) if ox >= 0 else big.paste(sub, (ox, oy), sub)
    a = big.split()[3]
    edge = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(9)), a)                      # rim light: thin coloured outline
    ramp = Image.linear_gradient("L").rotate(90).resize((W, H))                            # left -> right colour mix
    rim = Image.composite(Image.new("RGB", (W, H), right), Image.new("RGB", (W, H), left), ramp)
    soft = edge.filter(ImageFilter.GaussianBlur(6)).point(lambda v: min(255, v * 3))
    bg.alpha_composite(Image.merge("RGBA", (*rim.split(), soft)))
    inner = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(7))).filter(ImageFilter.GaussianBlur(2))   # light wrapping the edge
    lit = Image.composite(Image.blend(big.convert("RGB"), rim, 0.55), big.convert("RGB"), inner)
    big = Image.merge("RGBA", (*lit.split(), a)); big = ImageEnhance.Contrast(big).enhance(1.08)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.6)))
    bg.alpha_composite(sh, (10, 8)); bg.alpha_composite(big)
    return bg

if __name__ == "__main__":
    scene, cut, out, preset = sys.argv[1:5]
    c = pop(Image.open(scene), Image.open(cut).convert("RGBA"), cx=float(sys.argv[5]) if len(sys.argv) > 5 else 0.5)
    if preset == "dw":
        M = Q.N + "29_dreamworks_revenge/media/"
        e = Q.card(Image.open(Q.first(M, "B14_")), 230, 280, 7, bw=True, label="EISNER"); k = Q.card(Image.open(Q.first(M, "B1_")), 230, 280, -7, fx=0.35, fy=0.2, label="KATZENBERG")
        c.alpha_composite(e, (14, 90)); c.alpha_composite(k, (W - k.width - 14, 90)); Q.string(c, (220, 130), (W - 220, 130))
        Q.text_band(c, "DISNEY", (255, 255, 255), "SAID NO.", (255, 196, 40)); Q.tag(c, "1994-2016"); Q.stamp(c, "$3.8 BILLION", (W - 380, 470), angle=-8)
    elif preset == "px":
        P = Q.N + "30_pixar_10_million/media/"
        Q.text_band(c, "NOBODY", (255, 255, 255), "WANTED IT.", (80, 230, 120)); Q.tag(c, "STEVE JOBS' $10M BET"); Q.stamp(c, "SOLD: $7.4B", (W - 360, 470), angle=-8)
    c.convert("RGB").save(out, quality=92); print("ok", out)
