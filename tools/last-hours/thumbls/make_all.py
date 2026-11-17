"""Re-thumbs 17 Nov 2026: 3 variants per older long video in the owner's ChatGPT style. Run: F:/thumbkit/venv/Scripts/python.exe make_all.py [name ...]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thumbls import *
import numpy as np

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


def _elsayed_panel(c, M, x0=880, seed=3):
    """Right panel, kept APART from Banna: torn paper edge, Michigan Capitol (real), El-Sayed in colour from a NEW
    CC BY-SA 4.0 photo (Kenneth C. Zirkel, 2025, Wikimedia Commons), '2026' tag and the fair AP note (owner rule)."""
    rng = np.random.default_rng(seed)
    cap = Image.open(M + 'A51_michigan_state_capitol_lansing_2019.jpg').convert('RGB')
    pw = W - x0 + 30
    cap = grade(cover_to(cap, pw, H), 'teal', sat=0.75, bright=0.7)
    edge = np.cumsum(rng.normal(0, 2.2, H)); edge = 18 + (edge - edge.min()) / (np.ptp(edge) + 1e-6) * 22
    a = (np.arange(pw)[None, :] > edge[:, None]).astype(np.uint8) * 255
    panel = cap.convert('RGBA'); panel.putalpha(Image.fromarray(a))
    paper = Image.new('RGBA', (pw, H), (236, 228, 210, 0))
    pa = ((np.arange(pw)[None, :] > edge[:, None] - 9) & (np.arange(pw)[None, :] <= edge[:, None] + 2)).astype(np.uint8) * 255
    paper.putalpha(Image.fromarray(pa))
    c.paste(paper, (x0 - 30, 0), blur=10, alpha=200, off=(-8, 0)); c._safe(panel, (x0 - 30, 0))
    es = tone(cutout(M + '_elsayed_new/B1_elsayed_zirkel_2025.jpg', crop=(0, 0, 1920, 2300)), 'colour', bright=1.0, tint=(1.0, 1.0, 1.0))
    c.subject(es, x=x0 - 5, y=H - 530 + 10, h=530, rim=False, bottom_fade=0.12)
    tag = word_layer('2026', 44, (15, 12, 10), seed=12, wear=0.03)
    box = Image.new('RGBA', (tag.width + 20, tag.height + 4), WHITE + (255,)); box.alpha_composite(tag, (10, 2))
    c.paste(box, (x0 + 20, 30), blur=6, alpha=160)
    note = [word_layer(t, 40, (15, 12, 10), seed=13, wear=0.02) for t in ('AP: NO EVIDENCE', 'OF ANY LINK')]
    nw = max(n.width for n in note) + 28; nh = sum(n.height for n in note) + 14
    nb = Image.new('RGBA', (nw, nh), YELLOW + (255,)); y = 7
    for n in note: nb.alpha_composite(n, ((nw - n.width) // 2, y)); y += n.height
    c.paste(nb.rotate(-2, expand=True, resample=Image.BICUBIC), (x0 + 5, 548), blur=8, alpha=190)


def cover_to(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def brotherhood():
    """File 18 (1CzBdYMw9T8). Owner 17 Nov: El-Sayed in ALL thumbnails, NEW photo. Rules kept: he sits in his own torn
    panel (never touching/linked to Banna), fair AP note on every one, headlines never point at him, no emblem/flag,
    no fake records (N2a = the real AP clipping, 13 Feb 1949). Crowd = men only."""
    M = N + '18_muslim_brotherhood/media/'
    banna = lambda: tone(cutout(M + 'A1_classic_portrait_in_a_tarboosh.jpg'), 'bw', contrast=1.25)
    if have('mb_crowd'):
        c = Canvas(bg(BG + 'mb_crowd.png', 'bw', focus=(0.3, 0.5), contrast=1.25)); c.grade_finish(left_dark=0.5)
        c.subject(banna(), x=560, y=H - 540 + 10, h=540)
        _elsayed_panel(c, M)
        c.headline(['1928 TO', 'MICHIGAN'], 'yellow', sizes=(140, 140), maxw=520); c.date('12 FEB 1949')
        c.save(OUT + 'brotherhood_A.jpg')
    if have('mb_street'):
        c = Canvas(bg(BG + 'mb_street.png', 'warm', focus=(0.6, 0.5), sat=0.5)); c.grade_finish(left_dark=0.5)
        c.subject(banna(), x=560, y=H - 540 + 10, h=540)
        _elsayed_panel(c, M, seed=5)
        c.headline(['THE CLAIM.', 'THE FACTS.'], 'yellow', sizes=(130, 130), maxw=520); c.date('12 FEB 1949')
        c.save(OUT + 'brotherhood_B.jpg')
    if have('mb_crowd'):
        c = Canvas(bg(BG + 'mb_crowd.png', 'bw', focus=(0.8, 0.5), contrast=1.2)); c.grade_finish(left_dark=0.5)
        c.print_photo(M + 'N2a_sheikh_succumbs_to_assassins_bullets.jpg', (560, 300), w=280, angle=-5, mode='none', crop=(300, 0, 1148, 700))
        c.circle((555, 300, 850, 520), seed=8)
        _elsayed_panel(c, M, seed=7)
        c.headline(["WHAT'S", 'TRUE?'], 'yellow', sizes=(150, 180), maxw=500); c.date('12 FEB 1949')
        c.save(OUT + 'brotherhood_C.jpg')


def _card(lines, size=46, fill=WHITE, ink=(15, 12, 10), pad=18, small=None):
    lays = [word_layer(t, size, ink, seed=21 + i, wear=0.02) for i, t in enumerate(lines)]
    sm = word_layer(small, 24, (70, 60, 50), seed=30, wear=0.0) if small else None
    w = max([l.width for l in lays] + ([sm.width] if sm else [])) + 2 * pad
    h = sum(l.height for l in lays) + (sm.height + 6 if sm else 0) + 2 * pad
    card = Image.new('RGBA', (w, h), fill + (255,)); y = pad
    for l in lays: card.alpha_composite(l, (pad, y)); y += l.height
    if sm: card.alpha_composite(sm, (pad, y + 6))
    return card


def brotherhood2():
    """File 18 v2 (owner 17 Nov: 'make new thumbnails', El-Sayed in all, NEW photo). El-Sayed = the hero (B1 Zirkel 2025 /
    B2 Houston 2025, both CC BY-SA 4.0). Only REAL, on-record wording: his Fox News quote (23 Oct 2026), PolitiFact
    'Pants on Fire', AP 'no evidence'. No Banna face beside him, no emblem, no strings."""
    M = N + '18_muslim_brotherhood/media/'
    E = M + '_elsayed_new/'
    es1 = lambda: tone(cutout(E + 'B1_elsayed_zirkel_2025.jpg', crop=(0, 0, 1920, 2400)), 'colour', bright=1.0, tint=(1.0, 1.0, 1.0))
    es2 = lambda: tone(cutout(E + 'B2_elsayed_houston5_cropped.jpg'), 'colour', bright=1.0, tint=(1.0, 1.0, 1.0))
    # A: hero right, US Capitol at dawn, THE CLAIM: / FALSE. on the red brush + PolitiFact note
    c = Canvas(bg(M + 'A52_us_capitol_west_front_at_dawn_2013.jpg', 'teal', focus=(0.3, 0.5), sat=0.8, bright=0.75)); c.grade_finish(left_dark=0.5)
    c.subject(es1(), 'right', h=690, rim=True)
    c.headline(['THE CLAIM:', 'FALSE.'], 'brush', sizes=(140, 180), maxw=560, y=110)
    c.paste(_card(['POLITIFACT:', 'PANTS ON FIRE'], 40, YELLOW), (60, 520), blur=8, alpha=180)
    c.save(OUT + 'brotherhood2_A.jpg')
    # B: 1949 crowd (sepia, left) fading into the Michigan Capitol (colour, right); hero right; 1928 TO / 2026
    left = bg(BG + 'mb_crowd.png', 'bw', focus=(0.2, 0.5), contrast=1.2)
    right = bg(M + 'A51_michigan_state_capitol_lansing_2019.jpg', 'teal', sat=0.8, bright=0.8)
    ramp = np.clip((np.arange(W) - 420) / 360, 0, 1)[None, :, None]
    mix = (np.asarray(left).astype(np.float32) * (1 - ramp) + np.asarray(right).astype(np.float32) * ramp).astype(np.uint8)
    c = Canvas(Image.fromarray(mix)); c.grade_finish(left_dark=0.45)
    c.subject(es2(), 'right', h=680)
    c.headline(['1928 TO', '2026'], 'yellow', sizes=(150, 200), maxw=520)
    c.paste(_card(['AP: NO EVIDENCE', 'OF ANY LINK'], 36, YELLOW), (56, 560), blur=8, alpha=180)
    c.save(OUT + 'brotherhood2_B.jpg')
    # C: hero LEFT, text right: HIS ANSWER + his exact quote on a white card
    c = Canvas(bg(M + 'A51_michigan_state_capitol_lansing_2019.jpg', 'teal', mirror=True, sat=0.75, bright=0.7)); c.grade_finish(left_dark=0.0)
    c.subject(es1(), 'left', h=690, x=-40)
    c.headline(['HIS', 'ANSWER:'], 'yellow', x=640, maxw=600, sizes=(130, 150), y=60)
    q = _card(['"I HAVE NEVER BEEN A MEMBER', 'OF THE MUSLIM BROTHERHOOD.', 'I NEVER WILL BE."'], 40, WHITE, small='ABDUL EL-SAYED, FOX NEWS, 23 OCT 2026')
    c.paste(q.rotate(-2, expand=True, resample=Image.BICUBIC), (640, 355), blur=10, alpha=190)
    c.save(OUT + 'brotherhood2_C.jpg')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    names = sys.argv[1:] or ['alcatraz', 'franklin', 'cooper', 'roanoke', 'andree']
    for n in names: globals()[n]()
