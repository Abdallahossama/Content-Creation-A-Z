"""#25 Mallory & Irvine: 3 colour thumbnails (1280x720) for the A/B test, Hakawi style (real colour scene, ghosted real portraits,
huge text on solid blocks). Real images only, no women.
  uv run --no-project --with pillow --with numpy python thumbs_mi.py"""
import sys, glob
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import *
EP = "25_mallory_irvine"; OUT = NC + EP + "/export/"
def S(n): return src(EP, n)
def ghost(c, im, x, y, w, k=0.85, col=(70, 110, 140)):
    g = tint(im, col, 0.5).convert("RGBA"); g = g.resize((w, int(g.height * w / g.width)), Image.LANCZOS)
    m = fade_mask(g.width, g.height, left=int(w * 0.25), right=int(w * 0.25), top=int(g.height * 0.1), bottom=int(g.height * 0.35))
    m = m.point(lambda v: int(v * k)); c.paste(g, (x, y), m)
def ring(c, cx, cy, r, col=(230, 30, 30)): ellipse(c, (cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), 10, col)

def A():   # north face in colour + both men ghosted: DID THEY MAKE IT?
    c = grade(cover(S("B6_"), TW, TH, 0.55, 0.35, 1.05), sat=1.25, teal=0.16); c = vign(c, 0.45)
    ghost(c, S("B1_"), -30, 120, 430); ghost(c, S("B2_"), 880, 140, 420)
    ring(c, 520, 175, 52)
    block(c, "DID THEY", 360, 470, 96, fill=(0, 0, 0), bg=YEL + (255,)); block(c, "MAKE IT?", 360, 590, 120, fill=WHITE, bg=(0, 0, 0, 255))
    c.convert("RGB").save(OUT + "thumb_A_DID_THEY_MAKE_IT.jpg", quality=92)
def B():   # Everest from Rongbuk, the ridge circled: LAST SEEN 12:50
    c = grade(cover(S("B8_"), TW, TH, 0.6, 0.3, 1.25), sat=1.3, teal=0.18); c = vign(c, 0.5)
    ring(c, 470, 222, 60); d = ImageDraw.Draw(c)
    for x, y in ((458, 228), (480, 218)): d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(10, 10, 10))
    ghost(c, S("B1_"), 20, 260, 380, 0.8)
    block(c, "LAST SEEN", 460, 470, 100, fill=WHITE, bg=(0, 0, 0, 255)); block(c, "12:50 PM", 460, 600, 120, fill=(0, 0, 0), bg=YEL + (255,))
    c.convert("RGB").save(OUT + "thumb_B_LAST_SEEN_1250.jpg", quality=92)
def C():   # the north face + a Vest Pocket Kodak as a print: THE CAMERA IS STILL UP THERE
    c = grade(cover(S("B7_"), TW, TH, 0.5, 0.4, 1.35), sat=1.25, teal=0.16); c = vign(c, 0.5)
    cam = card(grade(cover(S("B14_"), 520, 560, 0.5, 0.5, 1.0), sat=1.1), 380, rot=-4); c.paste(cam, (790, 50), cam)
    ghost(c, S("B2_"), 0, 120, 380, 0.75)
    block(c, "THE CAMERA IS", 60, 480, 84, fill=(0, 0, 0), bg=YEL + (255,)); block(c, "STILL UP THERE", 60, 590, 96, fill=WHITE, bg=(190, 30, 30, 255))
    c.convert("RGB").save(OUT + "thumb_C_CAMERA_STILL_UP_THERE.jpg", quality=92)
if __name__ == "__main__":
    A(); B(); C(); print("ok")
