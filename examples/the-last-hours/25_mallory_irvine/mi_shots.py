"""#25 Mallory & Irvine, Everest 1924 - shot list. Each shot runs from 'at' until the next shot starts."""
from pz_map import *

OUTNAME = "TheLastHours_25_Mallory_Irvine.mp4"
MUSIC = ["Floating Cities.mp3", "Overcast.mp3", "Floating Cities.mp3"]
SFXF = {"whoosh": "D:/why habibi/_style_kit/sfx/whoosh_long.wav", "paper": "D:/why habibi/_style_kit/sfx/paper_slide.wav",
        "riser": "D:/why habibi/_style_kit/sfx/riser_short.wav", "hit": "D:/why habibi/_style_kit/sfx/impact_soft.wav",
        "wind": "D:/why habibi/_newchannel/sfx/wind_cold_interior.mp3", "click": "D:/why habibi/_newchannel/sfx/camera_old_shutter_click.mp3"}
SFXG = {"whoosh": 0.22, "paper": 0.3, "riser": 0.25, "hit": 0.35, "wind": 0.35, "click": 0.45}

R1, R2 = (1400, 220), (1400, 320)
L1, L2 = (520, 220), (520, 320)
C2 = 2.3
def sc_portrait(c, t, s, t0, t1):
    grid(c, s); b = badge(pic(s["id"], s.get("crop"), True), 460, 12); K.pop(c, b, W / 2 - 330, 560, t, t0 + 0.1, dur=0.35)
    put_labels(c, t, s.get("labels", []), t1)
def sc_pair(c, t, s, t0, t1):
    grid(c, s)
    for i, (rid, x) in enumerate((("B1", W / 2 - 330), ("B2", W / 2 + 330))):
        K.pop(c, badge(pic(rid, None, True), 400, 11), x, 500, t, t0 + 0.1 + 0.25 * i, dur=0.35)
    put_labels(c, t, s.get("labels", []), t1)
def PAIR(at, labels=(), **kw): return dict(at=at, fn=sc_pair, labels=list(labels), **kw)
def POR(at, rid, labels=(), **kw): return dict(at=at, fn=sc_portrait, id=rid, labels=list(labels), **kw)
def P_(at, rid, labels=(), **kw): return dict(at=at, fn=sc_photo, id=rid, labels=list(labels), **kw)
def CARD(at, title, num): return dict(at=at, fn=sc_card, title=title, num=num, sfx="whoosh")
def TXT(at, text, labels=(), **kw): return dict(at=at, fn=sc_text, text=text, labels=list(labels), **kw)
def CNT(at, to, labels=(), **kw): return dict(at=at, fn=sc_counter, to=to, labels=list(labels), **kw)

EV = (86.925, 27.988); DJ = (88.26, 27.04); PHARI = (89.15, 27.74); KAMPA = (88.5, 28.27); SHEKAR = (87.1, 28.67); RONG = (86.85, 28.2)
V_HIM = (87.6, 27.9, 8.5); V_ASIA = (84.0, 26.0, 48.0)
WALK = [DJ, (88.6, 27.4), PHARI, KAMPA, (87.8, 28.6), SHEKAR, RONG, EV]
HI_T = {"Nepal": (232, 238, 228), "China": (246, 238, 222), "India": (244, 240, 230)}

SHOTS = [
    # ---- cold open
    P_(0, "B10", [("The roof of the world", "red", *R1, (0, "roof"))], z0=1.0, z1=1.15),
    P_(1, "B6", [("Sunday, June 8, 1924", "red", *R1, (1, "sunday"), 58), ("12:50 p.m.", "yel", *R2, (1, "twelve"), 56)], z0=1.02, z1=1.12),
    P_(2, "B7", [("Noel Odell", "red", *L1, (2, "noel")), ("geologist, in support", "yel", *L2, (2, "geologist"))], z0=1.15, z1=1.3, c0=(0.5, 0.45)),
    P_(3, "B7", [("two black dots", "red", *R1, (3, "two"))], z0=1.5, z1=1.9, c0=(0.52, 0.32), c1=(0.53, 0.3)),
    PAIR(4, [("George Mallory", "red", W / 2 - 330, 790, (4, "george"), 54), ("Andrew Irvine", "red", W / 2 + 330, 790, (4, "andrew"), 54)]),
    P_(5, "B8", [], z0=1.02, z1=1.12, sfx="wind"),
    TXT(6, "Never seen alive again.", size=120, col=RED),
    TXT(7, "Summit?", size=240, labels=[("and died on the way down", "yel", W / 2, 700, (7, "die"))]),
    TXT(8, "Or turned back?", size=200),
    CNT(9, 75, post=" years later", labels=[("one of them is found", "red", W / 2, 700, (9, "found"), 60)]),
    TXT(10, "What was in his pockets", size=110, labels=[("still hasn't settled it", "yel", W / 2, 680, (10, "settled"))]),
    # ---- 1 the last prize
    CARD(11, "The Last|Prize", "CHAPTER 1"),
    P_((11, C2), "B11", [("Everest", "red", *R1, (11, "everest"))], z0=1.0, z1=1.12),
    TXT(12, "North Pole. South Pole.", size=110, labels=[("Highest mountain: not yet", "red", W / 2, 680, (12, "highest"), 64)]),
    P_(13, "B5", [("George Mallory · Tibet, 1924", "red", W / 2, 990, (13, "george"), 54)], z0=1.0, z1=1.08),
    POR(14, "B1", [("George Mallory", "red", 1280, 470, 14, 70), ("37 · schoolteacher · England", "yel", 1280, 580, (14, "thirty"))]),
    TXT(15, "1921 · 1922 · 1924", size=130, labels=[("his third expedition", "red", W / 2, 680, (15, "third"))]),
    TXT(16, "Why climb it?", size=170, labels=[("New York, 1923", "yel", W / 2, 680, (16, "new york"))]),
    TXT(17, "\u201cBecause it's there.\u201d", size=150, col=RED, sfx="hit"),
    POR(18, "B2", [("the youngest man on the team", "yel", 1280, 520, (18, "youngest"))]),
    P_(19, "B2", [("Andrew \u201cSandy\u201d Irvine", "red", *R1, (19, "andrew"), 60), ("22 · Oxford · engineer", "yel", *R2, (19, "twenty"))], bw=True, z0=1.0, z1=1.08),
    TXT(20, "Almost no big-mountain experience", size=84),
    TXT(21, "But...", size=200),
    TXT(22, "He could fix the oxygen sets.", size=100, labels=[("O\u2082", "red", W / 2, 700, (22, "oxygen"), 90)]),
    # ---- 2 one last try
    CARD(23, "One Last|Try", "CHAPTER 2"),
    dict(at=(23, C2), fn=sc_map, view=V_HIM, hi=HI_T, routes=[(WALK, (23, C2 + 0.2), 3.0)],
         pins=[(DJ, "Darjeeling", (23, C2 + 0.1)), (SHEKAR, "Tibet", (23, "tibet")), (EV, "Everest", (23, "mountain"), "red", 50)]),
    P_(24, "B12", [("storms · cold · sickness", "yel", *R2, (24, "storms"))], bw=True, z0=1.02, z1=1.1),
    P_(25, "B4", [("June 4 · Edward Norton", "red", W / 2, 900, (25, "june")), ("higher than anyone, ever", "yel", W / 2, 990, (25, "higher"))], bw=True, z0=1.03, z1=1.1),
    CNT(26, 28126, post=" ft", labels=[("without bottled oxygen", "red", W / 2, 700, (26, "without"), 60)], bg="B16"),
    TXT(27, "< 1,000 ft", size=220, labels=[("below the summit", "yel", W / 2, 720, (27, "below"))]),
    P_(28, "B9", crop=(0.1, 0.06, 0.9, 0.46), labels=[("The monsoon is coming", "red", *R1, (28, "monsoon"))], bw=True, z0=1.02, z1=1.12),
    PAIR(29, [("One last try", "red", W / 2, 160, (29, "last"), 64), ("with oxygen · with Irvine", "yel", W / 2, 860, (29, "oxygen"))]),
    # ---- 3 the last note
    CARD(30, "The Last|Note", "CHAPTER 3"),
    P_((30, C2), "B19", [("June 6 · North Col", "red", *R1, (30, "north"))], z0=1.0, z1=1.08),
    TXT(31, "June 6, 1924", size=170, labels=[("the last photograph of them together", "red", W / 2, 680, (31, "last"), 56)], sfx="click"),
    P_(32, "B19", [("June 7 · the highest camp", "red", *R1, (32, "june")), ("26,800 ft", "yel", *R2, (32, "twenty"), 56)], z0=1.1, z1=1.25, c0=(0.55, 0.45)),
    dict(at=33, fn=sc_news, head="NOTE FROM|CAMP VI", date="JUNE 7, 1924", mast="EXPEDITION NOTE", sfx="paper"),
    TXT(34, "\u201cPerfect weather for the job.\u201d", size=110, col=RED),
    TXT(35, "Watch for us", size=170, labels=[("on the ridge · about 8 a.m.", "yel", W / 2, 680, (35, "ridge"))]),
    # ---- 4 12:50
    CARD(36, "12:50|p.m.", "CHAPTER 4"),
    P_((36, C2), "B8", [("June 8 · they set off", "red", *R1, (36, "set off"))], z0=1.02, z1=1.12),
    CNT(37, 30, pre="~", post=" lb", labels=[("oxygen on their backs", "yel", W / 2, 700, (37, "oxygen"), 50)]),
    P_(38, "B14", [("Vest Pocket Kodak", "red", *R1, (38, "kodak"))], z0=1.0, z1=1.1),
    P_(39, "B14", [("proof of the summit?", "yel", *R2, (39, "prove"))], z0=1.1, z1=1.2),
    P_(40, "B7", [("Odell, alone, below", "yel", *L2, (40, "alone"))], z0=1.05, z1=1.15),
    P_(41, "B16", [("mist", "red", *R1, (41, "mist"))], z0=1.02, z1=1.1),
    TXT(42, "12:50", size=320, col=RED, sfx="hit"),
    P_(43, "B19", [("a tiny black spot", "red", *R1, (43, "spot")), ("then a second", "yel", *R2, (43, "second"))], z0=1.3, z1=1.6, c0=(0.6, 0.3)),
    TXT(44, "\u201cGoing strong for the top\u201d", size=110),
    TXT(45, "Hours behind schedule", size=120, col=RED),
    P_(46, "B8", [], z0=1.1, z1=1.2, sfx="wind"),
    # ---- 5 no trace
    CARD(47, "No|Trace", "CHAPTER 5"),
    P_((47, C2), "B16", [("~2 p.m. · snow squall", "red", *R1, (47, "two"))], z0=1.05, z1=1.15),
    P_(48, "B6", [("Odell waits at the high camp", "yel", *R2, (48, "waits"))], z0=1.1, z1=1.2),
    TXT(49, "Whistling. Shouting.", size=130),
    TXT(50, "Nothing.", size=240, col=RED),
    P_(51, "B9", crop=(0.1, 0.06, 0.9, 0.46), labels=[("back to the North Col", "yel", *R2, (51, "back"))], bw=True, z0=1.05, z1=1.12),
    TXT(52, "They never do.", size=160),
    P_(53, "B19", [("two days later", "red", *R1, (53, "two days")), ("the tent, untouched", "yel", *R2, (53, "exactly"))], z0=1.15, z1=1.3, c0=(0.55, 0.45)),
    TXT(54, "T", size=520, labels=[("two sleeping bags", "yel", W / 2, 260, (54, "sleeping"))]),
    TXT(55, "No trace.", size=220, col=RED, sfx="hit"),
    # ---- 6 clues in the snow
    CARD(56, "Clues in|the Snow", "CHAPTER 6"),
    TXT((56, C2), "9 years of silence", size=140),
    TXT(57, "1933", size=280, labels=[("another British team", "yel", W / 2, 720, (57, "british"))]),
    CNT(58, 27760, pre="~", post=" ft", labels=[("an ice axe on the rock", "red", W / 2, 700, (58, "ice axe"), 60)], bg="B7"),
    TXT(59, "Irvine's.", size=240, col=RED),
    TXT(60, "Dropped in a fall?", size=130, labels=[("or set down on the way up?", "yel", W / 2, 680, (60, "set"))]),
    TXT(61, "Nobody could say.", size=140),
    TXT(62, "1975 · Wang Hongbao", size=120, labels=[("a body high on the north face", "red", W / 2, 680, (62, "body"))]),
    TXT(63, "\u201cEnglish dead\u201d", size=170, col=RED, labels=[("old-fashioned clothes", "yel", W / 2, 700, (63, "old"))]),
    TXT(64, "1979", size=280, labels=[("he tells a Japanese climber", "yel", W / 2, 720, (64, "japanese"))]),
    TXT(65, "The next day: an avalanche.", size=110, col=RED),
    # ---- 7 may 1, 1999
    CARD(66, "May 1,|1999", "CHAPTER 7"),
    P_((66, C2), "B7", [("the search team", "red", *R1, (67, "search"))], z0=1.1, z1=1.25),
    P_(68, "B19", [("Conrad Anker", "red", *R1, (68, "conrad")), ("something white", "yel", *R2, (68, "white"))], z0=1.4, z1=1.6, c0=(0.45, 0.5)),
    TXT(69, "A body. Face down.", size=130),
    TXT(70, "A name tag", size=170),
    TXT(71, "G. MALLORY", size=220, col=RED, sfx="hit"),
    CNT(72, 75, post=" years", labels=[("on the mountain", "yel", W / 2, 700, (72, "lying"), 50)]),
    TXT(73, "A broken rope", size=170, labels=[("they were roped together", "red", W / 2, 680, (73, "roped"))]),
    TXT(74, "Broken leg · head wound", size=120),
    TXT(75, "He fell.", size=220, labels=[("good leg over the broken one", "yel", W / 2, 700, (75, "crossed"))]),
    # ---- 8 the pockets
    CARD(76, "The|Pockets", "CHAPTER 8"),
    TXT(77, "letters · knife · altimeter", size=96, labels=[("snow goggles", "red", W / 2, 640, (77, "goggles"), 64), ("oxygen notes", "yel", W / 2, 760, (77, "notes"))]),
    TXT(78, "3 clues", size=280, col=RED),
    TXT(79, "1. Goggles in the pocket", size=110),
    P_(80, "B16", [("snow blindness", "red", *R1, (80, "snow blind"))], z0=1.05, z1=1.15),
    TXT(81, "After sunset?", size=200, labels=[("still up there very late", "yel", W / 2, 720, (81, "late"))]),
    TXT(82, "2. A photograph", size=120, labels=[("to leave on the summit", "yel", W / 2, 680, (82, "summit"))]),
    TXT(83, "Not on his body.", size=150, col=RED),
    P_(84, "B14", [("3. The camera", "red", *R1, (84, "camera"))], z0=1.0, z1=1.08),
    P_(85, "B14", [("not with Mallory", "yel", *R2, (85, "not"))], z0=1.08, z1=1.18),
    TXT(86, "Frozen film", size=170, labels=[("might still develop", "red", W / 2, 680, (86, "developed"))]),
    # ---- 9 the second step
    CARD(87, "The Second|Step", "CHAPTER 9"),
    P_(88, "B19", [("The Second Step", "red", *R1, (88, "second")), ("~100 ft of rock", "yel", *R2, (88, "hundred"))], z0=1.3, z1=1.55, c0=(0.6, 0.3)),
    TXT(89, "1975", size=280, labels=[("a ladder is bolted on", "red", W / 2, 720, (89, "ladder"))]),
    TXT(90, "Most climbers use the ladder", size=96),
    TXT(91, "2007 · Conrad Anker", size=120, labels=[("climbs it free, no ladder", "red", W / 2, 680, (91, "free"))]),
    TXT(92, "\u201cVery hard\u201d", size=200, labels=[("in 1924 gear", "yel", W / 2, 720, (92, "gear"))]),
    TXT(93, "Stopped here?", size=200, col=RED),
    TXT(94, "Or higher?", size=200, labels=[("goggles · photo · late hour", "yel", W / 2, 700, (94, "goggles"))]),
    # ---- 10 the camera
    CARD(95, "The|Camera", "CHAPTER 10"),
    P_(96, "B15", [("May 29, 1953", "red", W / 2, 900, 96), ("Edmund Hillary & Tenzing Norgay", "yel", W / 2, 990, (96, "edmund"))], z0=1.0, z1=1.1),
    CNT(97, 29, post=" years later", labels=[("after the cloud", "yel", W / 2, 700, (97, "vanished"), 50)]),
    POR(98, "B2", [("Andrew Irvine", "red", 1280, 470, 98, 64), ("never found", "yel", 1280, 580, (98, "never"))]),
    P_(99, "B14", [("never found", "red", *R1, (99, "neither"))], z0=1.1, z1=1.2),
    P_(100, "B7", [("somewhere on the north face", "yel", *R2, (100, "somewhere"))], z0=1.0, z1=1.2),
    P_(101, "B14", [("the answer?", "red", *R1, (101, "answer"))], z0=1.2, z1=1.35),
    TXT(102, "After 12:50...?", size=200, col=RED, sfx="hit"),
    TXT(103, "LIKE  \u00b7  SUBSCRIBE", size=130, labels=[("The Last Hours", "red", W / 2, 700, (103, "subscribe"), 60)]),
    TXT(104, "Did they make it?", size=170, labels=[("tell me in the comments", "yel", W / 2, 700, (104, "comments"))]),
]
