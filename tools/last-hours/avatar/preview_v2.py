"""Preview v2 after the owner's notes (27 Nov): name NOAH, THE FILE KEEPER; cropped coat hidden on the left screen edge;
text never over the face; used sparingly.  uv run --no-project --with pillow --with numpy python preview_v2.py"""
import sys, io, subprocess
sys.path.insert(0, "D:/why habibi/_newchannel/_tools")
import hostkit as HK
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
A = "D:/why habibi/_newchannel/brand/avatar/"; NC = "D:/why habibi/_newchannel/"
ANTON = "F:/thumbkit/fonts/Anton-Regular.ttf"; COND = "C:/Windows/Fonts/FRAMDCN.TTF"; RED = (190, 30, 30)
def F(p, s): return ImageFont.truetype(p, s)
def grab(path, t):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(out)).convert("RGBA").resize((1920, 1080))
def caps(c, a, b, x):
    d = ImageDraw.Draw(c); d.text((x, 900), a, font=F(COND, 72), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((x, 980), b, font=F(COND, 72), fill=(255, 214, 64), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))

def f1():
    c = HK.cutaway(1.0, 0.0, 3.0, "master", name=("NOAH", "THE FILE KEEPER")); caps(c, "I'm Noah, the File Keeper.", "And this is the real Vice City.", 1250); return c, "1. FIRST CUTAWAY: name card, head on the left edge (coat crop hidden), captions to the right"
def f2():
    c = HK.cutaway(1.0, 0.0, 3.0, "smirk"); caps(c, "Boston didn't have a meat truck", "parked outside the morgue.", 1250); return c, "2. LATER CUTAWAYS: no name, a different expression (about one every 3-4 minutes)"
def f3():
    c = grab(NC + "26_saddam_capture/export/TheLastHours_26_Saddam_Capture.mp4", 200); HK.corner(c, 1.0, 0.0, 2.0, "shock"); return c, "3. CORNER POP: bottom-left, 1.5 s, only on the biggest shocks (3-4 per video)"
def f4():
    bgp = Image.open(NC + "01_alcatraz/media/B3_fbi_dummy_head.jpg").convert("RGB"); g = ImageOps.grayscale(bgp)
    bgp = Image.merge("RGB", (g, g.point(lambda v: int(v * .92)), g.point(lambda v: int(v * .82))))
    bgp = ImageOps.fit(bgp, (900, 720), centering=(0.2, 0.45)); c = Image.new("RGBA", (1280, 720), (10, 10, 12, 255)); c.paste(bgp, (380, 0))
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(380, 560): d.line((x, 0, x, 720), fill=(10, 10, 12, int(255 * (1 - (x - 380) / 180))))
    c.alpha_composite(lay)
    hero = HK.head("hero_file_flashlight", 0, 700); hero = hero.resize((int(hero.width * 0.92), int(hero.height * 0.92)))
    c.alpha_composite(hero, (-150, 720 - hero.height + 50))
    d = ImageDraw.Draw(c)
    d.text((1250, 40), "IT WAS", font=F(ANTON, 118), fill=(255, 255, 255), anchor="ra", stroke_width=6, stroke_fill=(0, 0, 0))
    d.rectangle((790, 190, 1255, 318), fill=RED); d.text((1240, 182), "A DUMMY.", font=F(ANTON, 118), fill=(255, 255, 255), anchor="ra")
    d.rectangle((960, 625, 1250, 690), fill=(255, 214, 64)); d.text((1105, 657), "12 JUNE 1962", font=F(ANTON, 44), fill=(0, 0, 0), anchor="mm")
    d.ellipse((560, 260, 900, 610), outline=RED, width=10)
    return c.resize((1920, 1080)), "4. THUMBNAIL: you on the left with the flashlight, evidence centre, words top-right: nothing over your face"

if __name__ == "__main__":
    T = [f1(), f2(), f3(), f4()]
    S = Image.new("RGB", (1980, 1240), (28, 28, 30)); d = ImageDraw.Draw(S)
    for i, (im, cap) in enumerate(T):
        x, y = 20 + (i % 2) * 980, 60 + (i // 2) * 600; S.paste(im.convert("RGB").resize((960, 540)), (x, y)); d.text((x, y - 40), cap, font=F(COND, 24), fill=(255, 214, 64))
    S.save(A + "AVATAR_PREVIEW_v2.jpg", quality=88); print(A + "AVATAR_PREVIEW_v2.jpg")
