"""27 Nov 2026 re-package (owner: low views/reach on 9 videos). One new thumbnail per video in the rebrand look:
Noah (the host avatar) on the LEFT edge (crop hidden), flashlight/eyes toward the evidence, real scene + real archive print,
2-3 words top-right (never over Noah's face), date block, bottom-right 170x70 kept clear.
  F:/thumbkit/venv/Scripts/python.exe make_noah.py"""
import sys, os
sys.path.insert(0, "D:/why habibi/_newchannel/_rethumb_nov17"); sys.path.insert(0, "D:/why habibi/_newchannel/_tools")
from thumbls import *
import hostkit as HK
N = "D:/why habibi/_newchannel/"; BG = N + "_rethumb_nov17/bg/"; OUT = N + "_rethumb_nov27/out/"; os.makedirs(OUT, exist_ok=True)

def noah(c, pose="hero_file_flashlight", h=650, x=-70):
    hd = HK.head(pose, 0, h)                                    # includes a soft drop shadow (50 px pad)
    c._safe(hd, (x - 50, H - hd.height + 95))

def realbg(path, look="teal", focus=(0.5, 0.5), zoom=1.0, **kw): return bg(path, look, focus=focus, zoom=zoom, **kw)

def alcatraz():
    M = N + "01_alcatraz/media/"
    c = Canvas(bg(BG + "alc_cell2.png", "teal", mirror=False)); c.grade_finish(left_dark=0.35)
    c.print_photo(M + "C4_fbi_vent.jpg", (720, 330), w=330, angle=-4, mode="bw"); c.circle((760, 400, 1010, 560), seed=3)
    c.headline(["DUG WITH", "SPOONS."], "brush", x=600, y=40, maxw=620, sizes=(130, 130)); c.date("11 JUNE 1962", xy=(600, 620))
    noah(c); c.save(OUT + "alcatraz_N.jpg")

def franklin():
    M = N + "03_franklin/media/"
    c = Canvas(bg(BG + "fra_ships.png", "ice", focus=(0.75, 0.5))); c.grade_finish(left_dark=0.3)
    c.print_photo(M + "B1_victory_point_record_1847_1848_message.jpg", (850, 300), w=260, angle=5, mode="sepia")
    c.headline(["129 MEN.", "NONE CAME BACK."], "brush", x=560, y=40, maxw=680, sizes=(120, 92)); c.date("22 APRIL 1848", xy=(560, 620), color=ICE)
    noah(c); c.save(OUT + "franklin_N.jpg")

def cooper():
    M = N + "04_dbcooper/media/"
    c = Canvas(bg(BG + "coo_jet.png", "teal", focus=(0.6, 0.5))); c.grade_finish(left_dark=0.3)
    c.print_photo(M + "A10_composite_b_as_a_single_portrait_1973.jpg", (870, 290), w=250, angle=4, mode="bw"); c.circle((880, 300, 1130, 600), seed=5)
    c.headline(["$200,000.", "NO NAME."], "yellow", x=560, y=40, maxw=640, sizes=(130, 130)); c.date("24 NOV 1971", xy=(560, 620))
    noah(c, "think", h=600, x=-40); c.save(OUT + "cooper_N.jpg")

def roanoke():
    M = N + "05_roanoke/media/"
    c = Canvas(bg(BG + "roa_tree.png", "warm" if False else "teal", focus=(0.55, 0.5))); c.grade_finish(left_dark=0.3)
    c.bark_patch((900, 450), (420, 150)); c.carve("CROATOAN", (900, 450), size=96)
    c.headline(["115 PEOPLE.", "ONE WORD."], "yellow", x=560, y=40, maxw=660, sizes=(120, 120)); c.date("18 AUG 1590", xy=(560, 620))
    noah(c); c.save(OUT + "roanoke_N.jpg")

def andree():
    M = N + "08_andree/media/"
    c = Canvas(bg(BG + "and_balloon.png", "ice", focus=(0.65, 0.5))); c.grade_finish(left_dark=0.3)
    c.print_photo(M + "B1_the_three_at_florman_s_studio_stockhol.jpg", (860, 300), w=280, angle=-5, mode="sepia")
    c.headline(["THE FILM", "SURVIVED."], "brush", x=560, y=40, maxw=640, sizes=(130, 130)); c.date("14 JULY 1897", xy=(560, 620), color=ICE)
    noah(c, "shock", h=600, x=-40); c.save(OUT + "andree_N.jpg")

def flight19():
    M = N + "09_flight19/media/"
    c = Canvas(realbg(M + "B1_five_tbf_1_avengers_in_echelon_off_for.jpg", "teal", focus=(0.6, 0.5), zoom=1.05)); c.grade_finish(left_dark=0.3)
    c.headline(["5 PLANES.", "14 MEN. GONE."], "brush", x=560, y=40, maxw=680, sizes=(124, 96)); c.date("5 DEC 1945", xy=(560, 620))
    noah(c); c.save(OUT + "flight19_N.jpg")

def gaddafi_bb():
    M = N + "12_gaddafi_stadium/media/"
    c = Canvas(realbg(M + "C10_benghazi_lights_at_night_from_the_iss.jpg", "teal", focus=(0.5, 0.5), zoom=1.2)); c.grade_finish(left_dark=0.3)
    c.subject(tone(cutout(M + "B5_gaddafi_brussels_27_apr_2004_head_and.jpg"), "bw"), "right", h=480, x=860, y=250)
    c.headline(["LIVE", "ON TV."], "brush", x=560, y=40, maxw=520, sizes=(140, 140)); c.date("JUNE 1984", xy=(560, 620))
    noah(c, "serious", h=600, x=-40); c.save(OUT + "gaddafi_bb_N.jpg")

def gaddafi_last():
    M = N + "17_gaddafi_last_day/media/"
    c = Canvas(realbg(M + "A23_sirte_a_pickup_painted_17_february_and.jpg", "teal", focus=(0.5, 0.5), zoom=1.05)); c.grade_finish(left_dark=0.3)
    c.subject(tone(cutout(M + "B5_gaddafi_brussels_27_apr_2004_head_and.jpg"), "bw"), "right", h=400, x=930, y=330)
    c.headline(["8:30 AM.", "11:00 AM."], "red", x=560, y=30, maxw=480, sizes=(110, 110)); c.date("20 OCT 2011", xy=(560, 620))
    noah(c); c.save(OUT + "gaddafi_last_N.jpg")

def brotherhood():
    M = N + "18_muslim_brotherhood/media/"
    c = Canvas(bg(BG + "mb_street.png", "teal", focus=(0.6, 0.5))); c.grade_finish(left_dark=0.3)
    c.print_photo(M + "A1_classic_portrait_in_a_tarboosh.jpg", (880, 280), w=250, angle=4, mode="bw")
    c.headline(["WHO", "FIRED?"], "brush", x=560, y=40, maxw=520, sizes=(140, 140)); c.date("12 FEB 1949", xy=(560, 620))
    noah(c, "think", h=600, x=-40); c.save(OUT + "brotherhood_N.jpg")

if __name__ == "__main__":
    for f in (alcatraz, franklin, cooper, roanoke, andree, flight19, gaddafi_bb, gaddafi_last, brotherhood):
        try: f()
        except Exception as e: print("FAIL", f.__name__, repr(e)[:200])
