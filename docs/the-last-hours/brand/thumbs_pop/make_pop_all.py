"""Build the 6 'pop' thumbnails (owner 27 Nov: use the small ChatGPT panels). F:/thumbkit/venv/Scripts/python.exe make_pop_all.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import make_qany3 as Q, make_pop as MP
S = "C:/Users/ossam/AppData/Local/Temp/claude/4e5240680a12582b/0deccdd2-4bb6-4df6-90bc-0ed43495fcc4/scratchpad/cut/"
W, H = 1280, 720; N = Q.N
def jobs84():
    im = Image.open(Q.first(N + "30_pixar_10_million/media/", "B1_")).convert("RGB"); d = ImageDraw.Draw(im)
    d.rounded_rectangle((1175, 2765, 2045, 3415), 40, fill=(52, 66, 70)); d.text((1250, 2860), "> _", font=Q.F(150), fill=(150, 220, 170))
    b = (1120, 3700, 1250, 3840); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(25)), b); return im
def build(key, cx, l1, c2, tg, st=None, cards=(), out=None, stxy=(W - 380, 470)):
    c = MP.pop(Image.open(S + key + "_2x.png"), Image.open(S + key + "_cut.png").convert("RGBA"), cx=cx)
    pts = []
    for (img, side, label, fx, fy, bw) in cards:
        cd = Q.card(img, 220, 270, 7 if side == "L" else -7, fx=fx, fy=fy, bw=bw, label=label)
        x = 14 if side == "L" else W - cd.width - 14; c.alpha_composite(cd, (x, 95)); pts.append((x + cd.width // 2, 135))
    if len(pts) == 2: Q.string(c, pts[0], pts[1])
    Q.text_band(c, l1[0], (255, 255, 255), l1[1], c2); Q.tag(c, tg)
    if st: Q.stamp(c, st, stxy, angle=-8, size=46 if key == "dw_a" else 58)
    os.makedirs(os.path.dirname(out), exist_ok=True); c.convert("RGB").save(out, quality=92)
    c.convert("RGB").resize((320, 180), Image.LANCZOS).save(out.replace(".jpg", "_320.jpg"), quality=90); return out
DWM = N + "29_dreamworks_revenge/media/"; eis = Image.open(Q.first(DWM, "B14_")); kat = Image.open(Q.first(DWM, "B1_"))
tt = Image.open(Q.first(N + "31_cartoon_network/media/", "B1_")); jb = jobs84()
YEL, GRN = (255, 196, 40), (80, 230, 120)
outs = [
 build("dw_a", 0.47, ("DISNEY", "SAID NO."), YEL, "1994-2016", "$3.8 BILLION", [(eis, "L", "EISNER", 0.5, 0.3, True), (kat, "R", "KATZENBERG", 0.35, 0.2, False)], N + "29_dreamworks_revenge/export/thumbnails/POP_DW_A_DISNEY_SAID_NO.jpg", stxy=(W - 330, 488)),
 build("dw_b", 0.5, ("$3.8 BILLION", "REVENGE"), YEL, "DISNEY vs DREAMWORKS", None, [], N + "29_dreamworks_revenge/export/thumbnails/POP_DW_B_38B_REVENGE.jpg"),
 build("px_a", 0.36, ("FROM $10M", "TO $7.4B"), GRN, "PIXAR 1986-2006", None, [], N + "30_pixar_10_million/export/thumbnails/POP_PX_A_10M_TO_74B.jpg"),
 build("px_b", 0.6, ("NOBODY", "WANTED IT."), GRN, "STEVE JOBS' $10M BET", "SOLD: $7.4B", [(jb, "L", "STEVE JOBS, 1984", 0.45, 0.25, False)], N + "30_pixar_10_million/export/thumbnails/POP_PX_B_NOBODY_WANTED_IT.jpg", stxy=(W - 400, 90)),
 build("cn_a", 0.64, ("34 MILLION", "HOMES GONE."), YEL, "CARTOON NETWORK 1992-2026", "FADING?", [], N + "31_cartoon_network/export/thumbnails/POP_CN_A_34M_HOMES_GONE.jpg", stxy=(W - 330, 90)),
 build("cn_b", 0.5, ("$320 MILLION.", "THEN IT FADED."), YEL, "1992-2026", None, [(tt, "L", "TED TURNER", 0.5, 0.15, True)], N + "31_cartoon_network/export/thumbnails/POP_CN_B_320M_FADED.jpg"),
]
ims = [Image.open(o).resize((640, 360), Image.LANCZOS) for o in outs]; sheet = Image.new("RGB", (1280, 1080))
for i, im in enumerate(ims): sheet.paste(im, ((i % 2) * 640, (i // 2) * 360))
sheet.save(os.path.dirname(os.path.abspath(__file__)) + "/POP_THUMBS_SHEET.jpg", quality=90); print("ok")
