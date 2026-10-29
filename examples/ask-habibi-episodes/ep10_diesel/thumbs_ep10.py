"""Ep 10 Diesel thumbnails in the v3 rules (REAL photos, men only, 3 truly different layouts, 1-3 words, never the title's words):
A PROOF  = the real pump, the two real prices as signs, a marker arrow "+$2"
B MAP    = the Gulf from the ISS (NASA), Hormuz looped in red, a zoom bubble on a tanker: THIS STRAIT
C FACE   = a puzzled man next to the pump, NOT TAX. (the hook: almost none of the gap is tax)"""
import sys
sys.path.insert(0, "D:/why habibi/_pipeline/episodes")
from thumbs_v3 import *                                     # fill, man, bubble, card, save, sheet, CK, MK, W, H, SHOCK, PUZZ
F = "D:/why habibi/10th video/export/thumbnails/"; P = "D:/why habibi/_media/photos_ep10/"; P4 = "D:/why habibi/4th video/media/photos/"

def sign(label, price, col, w=430):
    im = Image.new("RGBA", (w, 250), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 249), 28, fill=(22, 20, 24, 245), outline=col + (255,), width=8)
    d.text((w / 2, 52), label, font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 46), fill=(240, 236, 228), anchor="mm")
    d.text((w / 2, 160), price, font=ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 130), fill=col, anchor="mm", stroke_width=6, stroke_fill=(10, 10, 10))
    return im.rotate(-3, Image.BICUBIC, expand=True)

def A():
    c = fill(P + "pexels-4744712.jpg", W, H, (0.5, 0.45), sat=1.25, con=1.15, bright=0.8, zoom=1.15)
    c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    glowed(c, sign("DIESEL", "$6.31", (255, 206, 40)), 330, 230, (255, 190, 40), r=34)
    MK.place(c, sign("GAS", "$4.27", (235, 235, 235)), 330, 540)
    MK.strokes(c, MK.arrow_path((560, 560), (590, 250), bend=-0.5, head=46, seed=3), MK.RED, 18, seed=3)
    CK.words(c, ["+$2"], size=170, x=620, y=300, rot=-6)
    man(c, SHOCK, 470, W - 200, H + 40, rot=-2)
    return save(c, F, "A_PUMP_PLUS_2")

def B():
    c = fill(P + "iss_gulf_day.jpg", W, H, (1.0, 0.38), sat=1.35, con=1.2, bright=1.05, zoom=1.3)      # NASA ISS069-E-92132: Hormuz top right
    hx, hy = 1062, 332                                                                              # the strait (Musandam vs Iran)
    MK.strokes(c, MK.circle_path(hx, hy, 115, 85, seed=6, tilt=-12), MK.RED, 13, seed=6)
    tk = Image.open(P4 + "pexels-35757999.jpg").convert("RGB").crop((900, 700, 3900, 2700)); r = 160; bx, by = 820, 525
    crop = tk.resize((2 * r, 2 * r), Image.LANCZOS); m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    bub = Image.new("RGBA", (2 * r + 24, 2 * r + 24), (0, 0, 0, 0)); ImageDraw.Draw(bub).ellipse((0, 0, 2 * r + 23, 2 * r + 23), fill=(255, 255, 255, 255)); crop.putalpha(m); bub.alpha_composite(crop, (12, 12))
    MK.strokes(c, MK.arrow_path((hx - 70, hy + 70), (bx + 90, by - 120), bend=0.1, head=0, seed=2), MK.WHITE, 8, seed=2)
    c.alpha_composite(bub, (bx - r - 12, by - r - 12))
    CK.words(c, ["THIS", "STRAIT"], size=150, x=30, y=20, rot=-4, step=150)
    return save(c, F, "B_THIS_STRAIT")

def C():
    c = fill(P + "pexels-28264496.jpg", W, H, (0.5, 0.5), sat=1.3, con=1.15, bright=0.95, zoom=1.0)
    c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60)))
    CK.words(c, ["IT'S NOT"], size=120, x=40, y=20, rot=-4)
    strike(c, "TAX", 330, 330, size=200)
    man(c, PUZZ, 520, W - 230, H + 40, rot=2)
    return save(c, F, "C_NOT_TAX")

if __name__ == "__main__":
    A(); B(); C(); sheet(F, ["A_PUMP_PLUS_2", "B_THIS_STRAIT", "C_NOT_TAX"])
