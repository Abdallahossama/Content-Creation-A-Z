"""Preview sheet: how the host avatar would be used (Qany-style). Nothing here goes live.
  uv run --no-project --with pillow --with numpy python preview_avatar.py"""
import subprocess, io, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
A = "D:/why habibi/_newchannel/brand/avatar/"; C = A + "cut/"
NC = "D:/why habibi/_newchannel/"
ANTON = "F:/thumbkit/fonts/Anton-Regular.ttf"; TYPE = "C:/Windows/Fonts/courbd.ttf"; COND = "C:/Windows/Fonts/FRAMDCN.TTF"
RED, BONE, INK = (190, 30, 30), (236, 230, 214), (12, 12, 14)
W, H = 1920, 1080
def F(p, s): return ImageFont.truetype(p, s)
def av(name, h):
    im = Image.open(C + name + ".png"); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
def shadow(sp, r=18, k=150):
    sh = Image.new("RGBA", (sp.width + 80, sp.height + 80), (0, 0, 0, 0)); a = sp.split()[3].point(lambda v: int(v * k / 255))
    blk = Image.new("RGBA", sp.size, (0, 0, 0, 255)); blk.putalpha(a); sh.paste(blk, (40, 52), blk); sh = sh.filter(ImageFilter.GaussianBlur(r))
    sh.alpha_composite(sp, (40, 40)); return sh
def grab(path, t):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(out)).convert("RGBA")
def brand_bg(w=W, h=H):
    """our cutaway background: near-black, faint red/blue rim glows, thin grid, film grain (the Qany grid idea in noir colours)"""
    a = np.zeros((h, w, 3), np.float32) + np.array(INK, np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    a += (np.exp(-(((xx - 0) / (w * .45)) ** 2 + ((yy - h * .6) / (h * .7)) ** 2)) * np.array([70, 8, 8]))[..., None].squeeze() if False else 0
    g1 = np.exp(-(((xx) / (w * .4)) ** 2 + ((yy - h * .55) / (h * .6)) ** 2))[..., None] * np.array([80, 10, 12])
    g2 = np.exp(-(((xx - w) / (w * .4)) ** 2 + ((yy - h * .45) / (h * .6)) ** 2))[..., None] * np.array([10, 18, 60])
    a = a + g1 + g2 + np.random.default_rng(1).normal(0, 5, (h, w, 1))
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for x in range(0, w, 60): dl.line((x, 0, x, h), fill=(255, 255, 255, 14))
    for y in range(0, h, 60): dl.line((0, y, w, y), fill=(255, 255, 255, 14))
    for x in range(0, w, 60):
        for y in range(0, h, 60): dl.point((x, y), fill=(255, 255, 255, 40))
    im.alpha_composite(lay); return im
def bug(c):
    """corner bug: small head in a red-ringed circle + THE LAST HOURS"""
    hd = av("master", 150); circ = Image.new("L", (110, 110), 0); ImageDraw.Draw(circ).ellipse((0, 0, 109, 109), fill=255)
    tile = Image.new("RGBA", (110, 110), (25, 25, 28, 255)); tile.alpha_composite(hd.crop((hd.width // 2 - 70, 0, hd.width // 2 + 70, 140)).resize((110, 110)))
    tile.putalpha(circ); c.alpha_composite(tile, (34, 30)); ImageDraw.Draw(c).ellipse((32, 28, 146, 142), outline=RED, width=4)
    ImageDraw.Draw(c).text((162, 66), "THE LAST HOURS", font=F(COND, 34), fill=BONE, anchor="lm")

def frame_cutaway():
    c = brand_bg(); hd = shadow(av("smirk_s6", 820)); c.alpha_composite(hd, ((W - hd.width) // 2, H - hd.height + 40))
    d = ImageDraw.Draw(c); d.text((W / 2, 900), "Boston didn't have a meat truck", font=F(COND, 76), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((W / 2, 985), "parked outside the morgue.", font=F(COND, 76), fill=(255, 214, 64), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    bug(c); return c, "1. CUTAWAY (like Qany's straw-hat head): on every 'friend' line, full screen on our noir grid"

def frame_corner():
    c = grab(NC + "26_saddam_capture/export/TheLastHours_26_Saddam_Capture.mp4", 200).resize((W, H))
    hd = shadow(av("shock_s8", 560)); c.alpha_composite(hd, (W - hd.width + 30, H - hd.height + 60))
    bug(c); return c, "2. CORNER POP: head slides in over the footage for a 1-2 s reaction (shock / laugh / think)"

def thumb():
    bgp = Image.open(NC + "01_alcatraz/media/B3_fbi_dummy_head.jpg").convert("RGB")
    bgp = ImageOps.pad(bgp.crop((0, 0, bgp.width, bgp.height)), (1280, 720), color=(0, 0, 0), centering=(0.12, 0.5)); g = ImageOps.grayscale(bgp)
    bgp = Image.merge("RGB", (g.point(lambda v: min(255, int(v * 1.0))), g.point(lambda v: int(v * .9)), g.point(lambda v: int(v * .8))))
    c = ImageEnhance.Brightness(bgp).enhance(0.75).convert("RGBA")
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for x in range(1280): dl.line((x, 0, x, 720), fill=(0, 0, 0, int(200 * max(0, (x - 560) / 720) ** 1.2)))
    c.alpha_composite(lay)
    hero = shadow(av("hero_file_flashlight", 700), r=14); c.alpha_composite(hero, (1280 - hero.width + 120, 720 - hero.height + 60))
    d = ImageDraw.Draw(c)
    d.text((560, 40), "IT WAS", font=F(ANTON, 110), fill=(255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
    d.rectangle((550, 180, 1010, 300), fill=RED); d.text((566, 172), "A DUMMY.", font=F(ANTON, 110), fill=(255, 255, 255))
    d.rectangle((40, 600, 330, 668), fill=(255, 214, 64)); d.text((185, 634), "12 JUNE 1962", font=F(ANTON, 46), fill=(0, 0, 0), anchor="mm")
    d.ellipse((60, 170, 470, 560), outline=RED, width=10)
    return c.resize((1280, 720)), "3. THUMBNAIL: you as the hero, flashlight on the real evidence (here: Alcatraz dummy head, FBI photo)"

def endscreen():
    c = brand_bg(); hero = shadow(av("hero_file_flashlight", 900)); c.alpha_composite(hero, (W - hero.width + 60, H - hero.height + 60))
    d = ImageDraw.Draw(c)
    for i, y in enumerate((130, 570)):
        d.rectangle((110, y, 110 + 680, y + 383), outline=(200, 200, 200), width=3); d.text((450, y + 190), "VIDEO " + str(i + 1), font=F(COND, 50), fill=(120, 120, 120), anchor="mm")
    d.rounded_rectangle((960, 470, 1290, 560), 14, fill=RED); d.text((1125, 515), "SUBSCRIBE", font=F(ANTON, 54), fill=(255, 255, 255), anchor="mm")
    d.text((1125, 400), "Whose last hours next?", font=F(COND, 48), fill=BONE, anchor="mm")
    bug(c); return c, "4. END SCREEN: you with the file + SUBSCRIBE (animated) + 2 video slots"

def avatar_icon():
    c = Image.new("RGBA", (800, 800), (20, 20, 24, 255)); g = brand_bg(800, 800); c.alpha_composite(g)
    hd = av("master", 900); c.alpha_composite(hd, ((800 - hd.width) // 2, 40))
    m = Image.new("L", (800, 800), 0); ImageDraw.Draw(m).ellipse((0, 0, 799, 799), fill=255); c.putalpha(m)
    ImageDraw.Draw(c).ellipse((4, 4, 795, 795), outline=RED + (255,), width=14); return c

if __name__ == "__main__":
    tiles = [frame_cutaway(), frame_corner(), thumb(), endscreen()]
    S = Image.new("RGB", (2 * 960 + 60, 2 * 540 + 3 * 70 + 380), (28, 28, 30)); d = ImageDraw.Draw(S)
    for i, (im, cap) in enumerate(tiles):
        x, y = 20 + (i % 2) * 980, 60 + (i // 2) * 620; S.paste(im.convert("RGB").resize((960, 540)), (x, y)); d.text((x, y - 40), cap, font=F(COND, 26), fill=(255, 214, 64))
    ic = avatar_icon(); ic.save(A + "channel_avatar_800.png"); icr = ic.resize((300, 300))
    S.paste(icr, (40, 1330), icr); d.text((40, 1290), "5. CHANNEL PICTURE (also the corner bug)", font=F(COND, 26), fill=(255, 214, 64))
    sm = icr.resize((88, 88)); S.paste(sm, (400, 1430), sm); d.text((500, 1474), "<- real size in search results", font=F(COND, 24), fill=(170, 170, 170), anchor="lm")
    S.save(A + "AVATAR_PREVIEW.jpg", quality=88); [t[0].convert("RGB").save(A + f"_prev_{i}.jpg", quality=90) for i, t in enumerate(tiles)]
    print(A + "AVATAR_PREVIEW.jpg")
