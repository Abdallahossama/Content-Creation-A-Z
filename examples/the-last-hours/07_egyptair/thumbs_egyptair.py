"""EgyptAir 990 (file 06) thumbnails, Hakawi colour style: ONE strong real image filling the frame + 2 short text lines.
Title: "He Left the Cockpit for 107 Seconds. Then the Dive Began." - the thumbnails never repeat its words.
No crew faces, no religious words or imagery, no women; real images only.
  uv run --no-project --with pillow --with numpy python thumbs_egyptair.py"""
import sys, os
import numpy as np
from PIL import Image
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, tint, vign, block, ellipse, TW, TH, YEL, WHITE, RED
OUT = "D:/why habibi/_newchannel/07_egyptair/export/thumbnails/"

def crop(im, box): w, h = im.size; return im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
def night(im, k=0.55):
    a = np.asarray(im.convert("RGB"), np.float32); a = a * (1 - k) + a * np.array([0.55, 0.75, 1.0]) * k * 0.8
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def A():   # the empty 767 cockpit (NASA), the captain's seat circled: THE EMPTY SEAT
    im = crop(src("07_egyptair", "B1_"), (0.09, 0.02, 0.91, 0.88))
    c = night(grade(cover(im, TW, TH, cx=0.5, cy=0.55, z=1.05), sat=1.1, teal=0.12, warm=0.02), 0.6); c = vign(c, 0.6)
    ellipse(c, (150, 430, 470, 720), width=12)
    block(c, "THE EMPTY", TW - 30, 470, 120, anchor="r")
    block(c, "SEAT", TW - 30, 615, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c
def B():   # the crushed flight data recorder, colour: "IT'S SHUT." / HIS LAST WORDS
    im = crop(src("07_egyptair", "C4_"), (0.11, 0.17, 0.89, 0.84))
    c = grade(cover(im, TW, TH, cx=0.5, cy=0.5, z=1.0), sat=1.2, teal=0.06, warm=0.08); c = vign(c, 0.55)
    block(c, "\u201cIT'S SHUT.\u201d", 40, 110, 130, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "HIS LAST WORDS", 40, 255, 90)
    return c
def C():   # SU-GAP itself (Zurich 1991, CC BY 2.0), graded to dusk: 2 COUNTRIES / 2 ANSWERS
    im = src("07_egyptair", "H1_")
    c = night(grade(cover(im, TW, TH, cx=0.55, cy=0.55, z=1.08), sat=1.15, teal=0.10, warm=0.04), 0.45); c = vign(c, 0.55)
    block(c, "2 COUNTRIES.", 40, 110, 118)
    block(c, "2 ANSWERS.", 40, 255, 118, fill=WHITE, bg=RED + (255,))
    return c

from PIL import ImageDraw, ImageOps, ImageFilter
def N1():   # US Navy 1999: an FBI agent and a sailor tag the real voice recorder ("NTSB / EGYPT AIR 990"): WHAT'S ON THE TAPE?
    im = crop(src("07_egyptair", "C3_"), (0.20, 0.04, 0.92, 0.98))
    c = grade(cover(im, TW, TH, cx=0.55, cy=0.45, z=1.0), sat=1.25, teal=0.05, warm=0.10); c = vign(c, 0.5)
    ellipse(c, (690, 400, 960, 715), width=11)
    block(c, "WHAT'S ON", 30, 95, 112)
    block(c, "THE TAPE?", 30, 230, 112, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def N2():   # the real last page of the NTSB transcript: "it's shut", "pull with me" x3 underlined, END OF RECORDING: THEN SILENCE.
    box = (0.06, 0.40, 0.60, 0.84); im = crop(src("07_egyptair", "A9_"), box).convert("L")
    a = np.asarray(ImageOps.autocontrast(im, cutoff=1), np.float32)[..., None] / 255
    paper = Image.fromarray((a * np.array([238, 228, 205]) + (1 - a) * np.array([22, 20, 24])).clip(0, 255).astype(np.uint8))
    s = TH / paper.height; pw = int(paper.width * s); paper = paper.resize((pw, TH), Image.LANCZOS)
    c = Image.new("RGBA", (TW, TH), (14, 14, 16, 255)); c.alpha_composite(paper.convert("RGBA"), (0, 0)); d = ImageDraw.Draw(c)
    def Y(fy): return (fy - box[1]) / (box[3] - box[1]) * TH                    # page fraction -> thumbnail y
    def X(fx): return (fx - box[0]) / (box[2] - box[0]) * pw
    for fy in (0.611, 0.668, 0.725):                                             # the three "pull with me" lines (page y)
        d.line((X(0.165), Y(fy) + 14, X(0.245), Y(fy) + 14), fill=RED, width=7)
    ellipse(c, (X(0.07), Y(0.76), X(0.215), Y(0.80)), width=8)
    c = vign(c, 0.4)
    block(c, "THEN", TW - 30, 300, 150, anchor="r")
    block(c, "SILENCE.", TW - 30, 470, 150, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c
def N3():   # the NTSB's own flight-profile chart on paper, the dive traced in red: WHY DID IT DIVE?
    im = src("07_egyptair", "A11_").convert("L"); W0, H0 = im.size
    a = np.asarray(ImageOps.autocontrast(im, cutoff=1), np.float32)[..., None] / 255
    paper = Image.fromarray((a * np.array([236, 226, 204]) + (1 - a) * np.array([30, 28, 32])).clip(0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(paper); k = W0 / 900
    pts = [(190, 102), (430, 102), (470, 108), (510, 145), (550, 205), (580, 265), (605, 330), (630, 385), (648, 400)]
    d.line([(x * k, y * k) for x, y in pts], fill=RED + (235,), width=int(14 * k), joint="curve")
    c = vign(cover(paper, TW, TH, cx=0.55, cy=0.42, z=1.18), 0.55)
    block(c, "WHY DID", 30, 470, 120)
    block(c, "IT DIVE?", 30, 615, 120, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def N4():   # SU-GAP itself (CC BY 2.0), at dusk, the cockpit circled: WHO WAS FLYING?
    im = crop(src("07_egyptair", "H1_"), (0.0, 0.18, 1.0, 0.74)); sc = TW / im.width
    plane = night(grade(im.resize((TW, int(im.height * sc)), Image.LANCZOS), sat=1.15, teal=0.08, warm=0.05), 0.35)
    c = Image.new("RGBA", (TW, TH), (10, 16, 26, 255)); yy = np.linspace(0, 1, TH)[:, None]
    sky = (np.array([18, 30, 48]) * (1 - yy) + np.array([60, 70, 82]) * yy)[:, None, :] * np.ones((1, TW, 1)) / 1
    c = Image.fromarray(sky.reshape(TH, TW, 3).astype(np.uint8)).convert("RGBA")
    y0 = TH - plane.height + 20; m = Image.new("L", plane.size, 255)
    fade = np.clip(np.arange(plane.height) / 90, 0, 1)[:, None] * np.ones((1, plane.width)); m = Image.fromarray((fade * 255).astype(np.uint8))
    c.paste(plane, (0, y0), m); c = vign(c, 0.5)
    cx = 0.935 * TW; cy = y0 + (0.53 - 0.18) / 0.56 * plane.height
    ellipse(c, (cx - 80, cy - 60, cx + 70, cy + 60), width=10)
    block(c, "WHO WAS", 30, 110, 130)
    block(c, "FLYING?", 30, 260, 130, fill=(0, 0, 0), bg=YEL + (255,))
    return c

def plane_dusk():
    """N4's base: SU-GAP (CC BY 2.0) under a dusk sky; returns the frame and where its cockpit windows are"""
    im = crop(src("07_egyptair", "H1_"), (0.0, 0.18, 1.0, 0.74)); sc = TW / im.width
    plane = night(grade(im.resize((TW, int(im.height * sc)), Image.LANCZOS), sat=1.15, teal=0.08, warm=0.05), 0.35)
    yy = np.linspace(0, 1, TH)[:, None]
    sky = (np.array([18, 30, 48]) * (1 - yy) + np.array([60, 70, 82]) * yy)[:, None, :] * np.ones((1, TW, 1))
    c = Image.fromarray(sky.reshape(TH, TW, 3).astype(np.uint8)).convert("RGBA")
    y0 = TH - plane.height + 20
    fade = np.clip(np.arange(plane.height) / 90, 0, 1)[:, None] * np.ones((1, plane.width)); m = Image.fromarray((fade * 255).astype(np.uint8))
    c.paste(plane, (0, y0), m)
    return c, (0.935 * TW, y0 + (0.53 - 0.18) / 0.56 * plane.height)
def cockpit_img():
    return crop(src("07_egyptair", "B1_"), (0.09, 0.02, 0.91, 0.88))
def M1():   # N4 + A: the real plane, its cockpit circled, a zoom bubble with the empty 767 cockpit inside: WHO WAS FLYING?
    c, (px, py) = plane_dusk(); c = vign(c, 0.45)
    R_, bx, by = 235, 905, 262                                             # the bubble
    ck = cockpit_img(); side = int(ck.width * 0.42)                          # zoom on the captain's (left) seat and his control column
    cx0 = int(ck.width * 0.08); cy0 = int(ck.height * 0.98) - side
    disc = ck.crop((cx0, cy0, cx0 + side, cy0 + side)).resize((2 * R_, 2 * R_), Image.LANCZOS)
    disc = grade(disc, sat=1.15, contrast=1.18, teal=0.04, warm=0.04)
    def DX(fx): return (fx * ck.width - cx0) / side * 2 * R_ + bx - R_            # cockpit-photo fraction -> thumbnail px
    def DY(fy): return (fy * ck.height - cy0) / side * 2 * R_ + by - R_
    mk = Image.new("L", disc.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, 2 * R_ - 1, 2 * R_ - 1), fill=255)
    d = ImageDraw.Draw(c)
    for sgn in (-1, 1):                                                    # the two lines from the windows to the bubble
        ang = np.arctan2(by - py, bx - px) + sgn * np.pi / 2
        d.line([(px + 26 * np.cos(ang), py + 26 * np.sin(ang)), (bx + R_ * np.cos(ang), by + R_ * np.sin(ang))], fill=(240, 240, 240, 255), width=4)
    d.ellipse((bx - R_ - 9, by - R_ - 9, bx + R_ + 9, by + R_ + 9), fill=(240, 240, 240, 255))
    c.paste(disc, (bx - R_, by - R_), mk)
    d = ImageDraw.Draw(c); d.ellipse((bx - R_ - 9, by - R_ - 9, bx + R_ + 9, by + R_ + 9), outline=RED + (255,), width=8)
    ellipse(c, (px - 62, py - 46, px + 52, py + 46), width=9)
    ellipse(c, (DX(0.10), DY(0.66), DX(0.36), DY(0.97)), width=9)         # the captain's empty seat inside the bubble
    block(c, "WHO WAS", 30, 110, 130)
    block(c, "FLYING?", 30, 260, 130, fill=(0, 0, 0), bg=YEL + (255,))
    return c
def M2():   # N4 + A as a double exposure: the empty cockpit fades into the dusk sky above the real plane
    c, (px, py) = plane_dusk()
    ck = cockpit_img(); ck = cover(ck, TW, int(TH * 0.72), cx=0.5, cy=0.45, z=1.0)
    ck = night(grade(ck, sat=1.0, teal=0.12, warm=0.0), 0.4)
    a = np.asarray(ck.convert("L"), np.float32) / 255 * 0.0 + 1.0
    fade = np.clip((ck.height - np.arange(ck.height)) / (ck.height * 0.45), 0, 1)[:, None] * 0.62
    ck.putalpha(Image.fromarray((fade * np.ones((1, ck.width)) * 255).astype(np.uint8))); c.alpha_composite(ck, (0, 0)); c = vign(c, 0.5)
    ellipse(c, (px - 62, py - 46, px + 52, py + 46), width=9)
    ellipse(c, (150, 300, 420, 520), width=9)                              # the captain's empty seat in the ghost
    block(c, "WHO WAS", TW - 30, 95, 120, anchor="r")
    block(c, "FLYING?", TW - 30, 240, 120, fill=(0, 0, 0), bg=YEL + (255,), anchor="r")
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); items = [("A_THE_EMPTY_SEAT", A), ("B_ITS_SHUT", B), ("C_2_COUNTRIES", C)]
    for name, fn in items:
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=92)
    sheet = Image.new("RGB", (3 * 640 + 40, 360 + 40 + 138 + 20), (30, 30, 30))
    for i, (n, _) in enumerate(items):
        im = Image.open(OUT + n + ".png"); sheet.paste(im.resize((640, 360)), (i * 660, 0)); sheet.paste(im.resize((246, 138)), (i * 660, 400))
    sheet.save(OUT + "_sheet.png"); print(OUT)
