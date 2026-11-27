"""File 28 thumbnails in the Noah rebrand look (owner 27 Nov): Noah on the LEFT (crop hidden), real/stock scene, 2-3 words top-right,
never over his face, date block, bottom-right 170x70 clear. No game art, no women.
  F:/thumbkit/venv/Scripts/python.exe make_thumbs.py"""
import sys, os
sys.path.insert(0, "D:/why habibi/_newchannel/_rethumb_nov17"); sys.path.insert(0, "D:/why habibi/_newchannel/_tools")
from thumbls import *
import hostkit as HK
R = "D:/why habibi/_newchannel/28_vice_city_real/"; M = R + "media/"; OUT = R + "export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
def noah(c, pose="hero_file_flashlight", h=650, x=-70):
    hd = HK.head(pose, 0, h); c._safe(hd, (x - 50, H - hd.height + 95))
def wave(c, h=700, x=10):
    f = HK.wave_figure(h, 0.0); c._safe(f, (x, H - f.height + 60))

def A():   # neon Ocean Drive (Pexels E3, crowd cropped) + VICE CITY / WAS REAL.
    im = Image.open(R + "build/tbg/e3.png").convert("RGB"); im = im.crop((0, 0, im.width, int(im.height * 0.65)))
    c = Canvas(bg_img := cover(im, focus=(0.55, 0.5))); c.grade_finish(left_dark=0.25)
    c.headline(["VICE CITY", "WAS REAL."], "brush", x=600, y=40, maxw=640, sizes=(130, 130)); c.date("MIAMI  1979-1986", xy=(600, 600))
    noah(c); c.save(OUT + "A_VICE_CITY_WAS_REAL.jpg")

def B():   # 1986 downtown Miami (Metro-Dade, PD) + 621 MURDERS. 1 YEAR.
    c = Canvas(bg(M + [f for f in os.listdir(M) if f.startswith("C2_")][0], "teal", focus=(0.5, 0.5), zoom=1.1)); c.grade_finish(left_dark=0.3)
    c.headline(["621 MURDERS.", "ONE YEAR."], "brush", x=560, y=40, maxw=680, sizes=(120, 120)); c.date("MIAMI  1981", xy=(560, 600))
    noah(c, "shock", h=600, x=-40); c.save(OUT + "B_621_MURDERS.jpg")

def C():   # night skyline + Noah waving + THE REAL / VICE CITY
    c = Canvas(cover(Image.open(R + "build/tbg/e1.png").convert("RGB"), focus=(0.6, 0.5))); c.grade_finish(left_dark=0.2)
    c.headline(["THE REAL", "VICE CITY"], "yellow", x=560, y=40, maxw=660, sizes=(140, 140)); c.date("1979-1986", xy=(560, 600))
    noah(c, "smirk", h=600, x=-40); c.save(OUT + "C_THE_REAL_VICE_CITY.jpg")

if __name__ == "__main__":
    for f in (A, B, C):
        try: f()
        except Exception as e: print("FAIL", f.__name__, repr(e)[:200])
