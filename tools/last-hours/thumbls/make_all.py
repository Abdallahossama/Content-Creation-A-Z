"""Re-thumbs 17 Nov 2026: 3 variants per older long video in the owner's ChatGPT style. Run: F:/thumbkit/venv/Scripts/python.exe make_all.py [name ...]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thumbls import *

N = 'D:/why habibi/_newchannel/'
BG = 'bg/'
OUT = 'out/'


def have(*names):
    return all(os.path.exists(BG + n + '.png') for n in names)


def alcatraz():
    M = N + '01_alcatraz/media/'
    if have('alc_raft_s1'):
        c = Canvas(bg(BG + 'alc_raft_s1.png', 'teal', focus=(0.15, 0.5), zoom=1.05)); c.grade_finish(left_dark=0.35)
        c.subject(tone(cutout(M + 'A1_fbi_morris.jpg'), 'bw'), 'right', h=660)
        c.headline(['NEVER', 'FOUND'], 'brush', sizes=(190, 170)); c.date('11 JUNE 1962')
        c.save(OUT + 'alcatraz_A.jpg')
    if have('alc_cell'):
        c = Canvas(bg(BG + ('alc_cell2.png' if have('alc_cell2') else 'alc_cell.png'), 'teal', mirror=True)); c.grade_finish(left_dark=0.55)
        c.circle((640, 200, 900, 460), seed=4)
        c.print_photo(M + 'B3_fbi_dummy_head.jpg', (990, 420), w=230, angle=7)
        c.headline(['IT WAS', 'A DUMMY'], 'yellow', sizes=(150, 140), maxw=560); c.date('11 JUNE 1962')
        c.save(OUT + 'alcatraz_B.jpg')
    if have('alc_boat2'):
        c = Canvas(bg(BG + 'alc_boat2.png', 'teal', focus=(0.6, 0.5))); c.grade_finish(left_dark=0.4)
        for i, (f, ang) in enumerate([('A1_fbi_morris.jpg', -7), ('A2_fbi_john_anglin.jpg', 4), ('A9_wanted_clarence_anglin_nps.jpg', -3)]):
            c.print_photo(M + f, (600 + i * 180, 110 + (i % 2) * 50), w=195, angle=ang, mode='sepia')
        c.headline(['3 MEN.', 'NO BODIES.'], 'red', sizes=(170, 150)); c.date('11 JUNE 1962')
        c.save(OUT + 'alcatraz_C.jpg')


def franklin():
    M = N + '03_franklin/media/'
    if have('fra_ships'):
        c = Canvas(bg(BG + 'fra_ships.png', 'ice', focus=(0.7, 0.5))); c.grade_finish(left_dark=0.35)
        c.headline(['NO WAY', 'HOME'], 'ice', sizes=(180, 200)); c.date('22 APRIL 1848', color=ICE)
        c.save(OUT + 'franklin_A.jpg')
        c = Canvas(bg(BG + 'fra_ships.png', 'ice', focus=(0.3, 0.5))); c.grade_finish(left_dark=0.45)
        c.subject(tone(cutout(M + 'A1_sir_john_franklin_captain_of_erebus_ex.jpg', crop=(380, 380, 1380, 1700)), 'sepia'), 'right', h=640)
        c.headline(['129 MEN.', 'GONE.'], 'brush', sizes=(170, 170)); c.date('22 APRIL 1848')
        c.save(OUT + 'franklin_C.jpg')
    if have('fra_close'):
        c = Canvas(bg(BG + 'fra_close.png', 'ice', focus=(0.6, 0.5))); c.grade_finish(left_dark=0.45)
        c.print_photo(M + 'B1_victory_point_record_1847_1848_message.jpg', (950, 150), w=240, angle=6, mode='sepia')
        c.headline(['THEY NEVER', 'CAME BACK'], 'ice', sizes=(150, 150)); c.date('22 APRIL 1848', color=ICE)
        c.save(OUT + 'franklin_B.jpg')


def cooper():
    M = N + '04_dbcooper/media/'
    sk = lambda: tone(white_cut(M + 'A7_composite_sketch_a_nov_1971_the_same_m.jpg', crop=(0, 0, 214, 297)), 'bw', bright=0.95)
    if have('coo_stairs'):
        c = Canvas(bg(BG + ('coo_jet_clean.png' if have('coo_jet_clean') else 'coo_stairs.png'), 'red', focus=(0.6, 0.5))); c.grade_finish(left_dark=0.4)
        c.subject(sk(), 'right', h=620)
        c.headline(['HE', 'DISAPPEARED'], 'brush', sizes=(190, 140)); c.date('24 NOV 1971')
        c.save(OUT + 'cooper_A.jpg')
        c = Canvas(bg(BG + ('coo_jet_clean.png' if have('coo_jet_clean') else 'coo_stairs.png'), 'teal', focus=(0.4, 0.5))); c.grade_finish(left_dark=0.4)
        c.print_photo(M + 'A11_fbi_bulletin_wanted_flyer_both_sketche.jpg', (930, 40), w=270, angle=5, mode='none', crop=(0, 0, 321, 330))
        c.circle((935, 50, 1240, 330), seed=6)
        c.headline(['WHO', 'WAS HE?'], 'red', sizes=(190, 170)); c.date('24 NOV 1971')
        c.save(OUT + 'cooper_C.jpg')
    if have('coo_forest'):
        c = Canvas(bg(BG + 'coo_forest.png', 'teal', focus=(0.6, 0.4))); c.grade_finish(left_dark=0.4)
        c.headline(['HE JUMPED', 'INTO THIS.'], 'yellow', sizes=(150, 150)); c.date('24 NOV 1971')
        c.save(OUT + 'cooper_B.jpg')


def roanoke():
    M = N + '05_roanoke/media/'
    if have('roa_tree'):
        c = Canvas(bg(BG + 'roa_tree.png', 'warm', mirror=True, focus=(0.0, 0.5), zoom=1.45))
        c.bark_patch((935, 430), (690, 250))
        c.carve('CROATOAN', (935, 430), size=128, angle=-3)
        c.grade_finish(left_dark=0.5)
        c.headline(['THEY LEFT', 'ONE WORD'], 'yellow', sizes=(140, 150)); c.date('18 AUG 1590')
        c.save(OUT + 'roanoke_A.jpg')
    if have('roa_fort'):
        c = Canvas(bg(BG + 'roa_fort.png', 'warm', focus=(0.6, 0.5))); c.grade_finish(left_dark=0.4)
        c.headline(['115 PEOPLE.', 'GONE.'], 'brush', sizes=(150, 170)); c.date('18 AUG 1590')
        c.save(OUT + 'roanoke_B.jpg')
        c = Canvas(bg(BG + 'roa_fort.png', 'warm', focus=(0.3, 0.5))); c.grade_finish(left_dark=0.45)
        c.print_photo(M + 'A14_croatoan_wood_engraving_1876_design_w.jpg', (720, 150), w=480, angle=4, crop=(0, 0, 2400, 2282))
        c.headline(['WHERE DID', 'THEY GO?'], 'yellow', sizes=(140, 150)); c.date('18 AUG 1590')
        c.save(OUT + 'roanoke_C.jpg')


def andree():
    M = N + '08_andree/media/'
    if have('and_balloon'):
        c = Canvas(bg(BG + ('and_balloon2.png' if have('and_balloon2') else 'and_balloon.png'), 'ice', focus=(0.6, 0.5))); c.grade_finish(left_dark=0.4)
        c.headline(['THE FILM', 'SURVIVED'], 'ice', sizes=(160, 170)); c.date('14 JULY 1897', color=ICE)
        c.save(OUT + 'andree_A.jpg')
        c = Canvas(bg(BG + ('and_balloon2.png' if have('and_balloon2') else 'and_balloon.png'), 'ice', focus=(0.3, 0.5))); c.grade_finish(left_dark=0.45)
        c.print_photo(M + 'B1_the_three_at_florman_s_studio_stockhol.jpg', (860, 90), w=330, angle=5, crop=(0, 700, 2576, 3100))
        c.headline(['3 MEN.', 'NO WAY BACK.'], 'brush', sizes=(170, 130)); c.date('14 JULY 1897')
        c.save(OUT + 'andree_C.jpg')
    # B: the REAL photo from their film (developed 1930) as the scene
    c = Canvas(bg(M + 'C1_the_eagle_on_the_ice_14_july_1897_reto.jpg', 'bw', focus=(0.85, 0.5), zoom=1.0, contrast=1.3)); c.grade_finish(left_dark=0.5)
    c.circle((690, 470, 850, 700), seed=3)
    c.headline(['FOUND', '33 YEARS', 'LATER'], 'red', sizes=(150, 120, 120)); c.date('14 JULY 1897')
    c.save(OUT + 'andree_B.jpg')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    names = sys.argv[1:] or ['alcatraz', 'franklin', 'cooper', 'roanoke', 'andree']
    for n in names: globals()[n]()
