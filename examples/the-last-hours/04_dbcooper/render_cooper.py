"""The Last Hours #3: D.B. Cooper, Flight 305, Nov 24 1971 (Case File style, 1920x1080). Built on render_franklin.py.
Every shot starts on a narration line (index into vo_lines.txt without '##'), or on a spoken word in it: key (line, "word").
Line timing comes from the exact-zero gaps in the VO, word timing from whisper (vo/vo_words.json).
  uv run --no-project --with pillow --with numpy --with soundfile --with pyproj python render_cooper.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel), US state lines on
MS.PW, MS.PH = W, H; MS._VIG.clear()
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/04_dbcooper/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
HAND = "C:/Windows/Fonts/segoeprb.ttf"                 # hand-printed look for the two reconstructions (note, flight plan)
LEAD = 0.8; TAIL = 20.0

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = ROOT + "vo/cooper_vo_chatterbox.wav"
_vo, VSR = sf.read(VOF, dtype="float32")
if _vo.ndim > 1: _vo = _vo.mean(1)
_z = np.concatenate([[False], _vo == 0.0, [False]]).astype(np.int8); _d = np.diff(_z)
GAPS = [(a, b) for a, b in zip(np.where(_d == 1)[0], np.where(_d == -1)[0]) if b - a >= int(0.3 * VSR)]
assert len(GAPS) == len(LINES), (len(GAPS), len(LINES))
T = [LEAD + (0 if i == 0 else GAPS[i - 1][1]) / VSR for i in range(len(LINES))]
LE = [LEAD + g[0] / VSR for g in GAPS]
VO_END = LEAD + len(_vo) / VSR; DUR = VO_END + TAIL; NF = int(DUR * FPS); del _vo, _z, _d
WORDS = {}                                     # line -> [(seconds after the line starts, word)]
if os.path.exists(ROOT + "vo/vo_words.json"):
    for sg in json.load(open(ROOT + "vo/vo_words.json", encoding="utf-8")):
        WORDS[sg["line"]] = [(w["s"] - sg["start"], w["w"]) for w in sg["words"]]
def wt(line, word, off=0.0):
    """video-clock time the narrator says `word` (prefix match, 'a|b' = either) inside line `line`; None if not heard"""
    for rel, w in WORDS.get(line, []):
        if any(re.sub(r"[^a-z0-9]", "", w.lower()).startswith(x) for x in word.lower().split("|")): return T[line] + rel + off
    return None
def AT(key):
    """absolute time of a key: line (start), (line, offset) or (line, 'word')"""
    if isinstance(key, int): return T[key]
    ln, w = key
    if isinstance(w, (int, float)): return T[ln] + w
    tm = wt(ln, w); return tm if tm is not None else T[ln] + 0.3
def KT(key): return AT(key) - (0.12 if isinstance(key, int) else 0.08)     # cut a beat before the word

# ------------------------------------------------------------------ assets
def P(rid):
    for f in sorted(glob.glob(B + f"_small_{rid}.png")) + sorted(glob.glob(M + rid + "_*")):
        h = open(f, "rb").read(4)
        if h[:3] == b"\xff\xd8\xff" or h == b"\x89PNG" or h in (b"II*\x00", b"MM\x00*"): return f
    return None
IMG = {}
def tone(rid, crop=None, rot=0):
    k = (rid, crop, rot)
    if k not in IMG: IMG[k] = L.bw(P(rid), crop)
    return IMG[k]

# FBI pages: boxes (page pixels) from the OCR pass (ocr_docs.py -> build/ocr/), padded by hand
PH = {
 "A12": {"name": (178, 292, 600, 356), "fare": (158, 738, 340, 862), "total": (343, 738, 535, 862), "flight": (762, 468, 852, 600), "used": (1140, 592, 1700, 692)},
 "A13": {"date": (778, 218, 998, 258), "ground": (138, 546, 1106, 610), "demand": (138, 594, 1102, 638), "bomb": (138, 622, 1102, 660), "flight": (138, 746, 1092, 808)},
 "A14": {"arrived": (385, 1543, 2030, 1707), "hand": (2045, 1345, 2495, 1592), "reardoor": (228, 2546, 2095, 2617)},
 "A15": {"time": (142, 304, 1122, 376), "seat": (142, 610, 1122, 678), "pink": (288, 992, 1152, 1112), "unopened": (288, 1122, 1104, 1242)},
 "A16": {"drinks": (150, 320, 1078, 410), "butts": (150, 604, 1052, 718), "tie": (150, 932, 1062, 1078)},
 "A17": {"list": (474, 1326, 2272, 1530), "parachuted": (478, 1780, 2172, 1972)},
 "A18": {"demand": (140, 718, 1002, 834), "ready": (140, 842, 1006, 934), "film": (140, 946, 1080, 1086)},
 "A19": {"victor": (130, 948, 1124, 1088), "airport": (132, 438, 752, 480)},
 "A21": {"ariel": (143, 626, 1047, 702)},
 "A22": {"tena": (112, 376, 1112, 517), "rise": (114, 1264, 1142, 1408)},
 "A24": {}, "A25": {},
}
FULL = {"A12": (150, 180, 1790, 900), "A13": (30, 50, 1180, 1000), "A14": (220, 420, 2500, 2930), "A15": (70, 70, 1220, 1460), "A16": (140, 220, 1110, 1340),
        "A17": (230, 590, 2360, 2660), "A18": (130, 180, 1090, 1370), "A19": (120, 180, 1220, 1350), "A21": (140, 250, 1110, 1480), "A22": (60, 100, 1290, 1620),
        "A24": (60, 60, 1250, 1600), "A25": (200, 150, 1100, 1560)}
def page_img(rid):
    k = ("doc", rid)
    if k not in IMG:
        im = Image.open(P(rid)).convert("L"); a = np.asarray(im, np.float32); lo, hi = np.percentile(a, 1), np.percentile(a, 99.5)
        a = np.clip((a - lo) / max(hi - lo, 1), 0, 1); IMG[k] = Image.fromarray((a[..., None] * np.array([236, 230, 214], np.float32)).astype(np.uint8))
    return IMG[k]

# the 1979 USGS 'Vancouver, Wash.-Oreg.' 1:100,000 sheet (C12), georeferenced from its GeoTIFF tags (NAD27, transverse Mercator)
TS = 0.5; TOPO_RES = 8.466666666666665; TOPO_TIE = (-45055.31889531485, 5098599.105603176); PXKM = 1000 / TOPO_RES * TS
_TR = None
def topo_px(lon, lat):
    global _TR
    if _TR is None:
        from pyproj import Transformer
        _TR = Transformer.from_crs("+proj=longlat +ellps=clrk66 +no_defs", "+proj=tmerc +lat_0=0 +lon_0=-122.5 +k=1 +x_0=0 +y_0=0 +ellps=clrk66 +units=m +no_defs", always_xy=True)
    x, y = _TR.transform(lon, lat); return (x - TOPO_TIE[0]) / TOPO_RES * TS, (TOPO_TIE[1] - y) / TOPO_RES * TS
def topo_img():
    if "topo" not in IMG: IMG["topo"] = Image.open(B + "_topo_C12.png").convert("RGB")
    return IMG["topo"]

def prep():
    """big scans are reduced once (and the topo toned once) before the parallel render starts"""
    if not os.path.exists(B + "_topo_C12.png"):
        im = Image.open(glob.glob(M + "C12_*")[0]).convert("RGB"); im = im.resize((int(im.width * TS), int(im.height * TS)), Image.LANCZOS)
        g = np.asarray(im.convert("L"), np.float32); lo, hi = np.percentile(g, 0.5), np.percentile(g, 99.7); g = np.clip((g - lo) / (hi - lo), 0, 1) ** 1.15
        Image.fromarray((g[..., None] * np.array([236, 230, 214], np.float32)).astype(np.uint8)).save(B + "_topo_C12.png")
    for f in glob.glob(M + "*"):
        rid = os.path.basename(f).split("_")[0]
        if rid in ("C12",) or os.path.exists(B + f"_small_{rid}.png"): continue
        try: im = Image.open(f)
        except Exception: continue
        if max(im.size) > 4200:
            im = im.convert("RGB"); k = 4200 / max(im.size); im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS).save(B + f"_small_{rid}.png")

# map points (lon, lat)
PDX, SEA, TAC, MCC, LOF, RNO = (-122.597, 45.589), (-122.309, 47.449), (-122.444, 47.253), (-122.476, 47.137), (-122.656, 47.817), (-119.768, 39.499)
ARIEL, TENA, VAN = (-122.571, 45.956), (-122.759, 45.717), (-122.672, 45.627)
EUG, MED, RBF = (-123.09, 44.05), (-122.87, 42.33), (-122.24, 40.18)
V23 = [SEA, (-122.52, 47.05), (-122.72, 46.6), (-122.64, 46.2), (-122.58, 45.96), (-122.6, 45.72), (-122.62, 45.55)]     # approximate
ROUTE = V23 + [(-122.9, 45.1), EUG, (-122.98, 43.2), MED, (-122.6, 41.2), RBF, (-121.0, 39.8), RNO]
V_PNW, V_SOUND, V_ROUTE = (-122.5, 46.62, 6.6), (-122.45, 47.52, 2.6), (-120.5, 43.2, 30.0)

# ------------------------------------------------------------------ shot constructors
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, rot=0): return ("kb", dict(rid=rid, crop=crop, z=z, c0=c0, c1=c1 or c0, rot=rot))
def KBP(rid, crop=None, h=820, rot=-1.5): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot))
def CARD(big, sub): return ("card", dict(big=big, sub=sub))
def DOC(rid, focus=None, z=(0.95, 1.08), marks=()): return ("doc", dict(rid=rid, focus=focus or FULL[rid], z=z, marks=marks))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def TOPO(c, km, ops=(), z=(1.0, 1.08), c1=None): return ("topo", dict(c=c, km=km, ops=list(ops), z=z, c1=c1))
def PRINTS(items): return ("prints", dict(items=items))
def LETTER(key): return ("letter", dict(key=key))
def BLACK(): return ("black", {})
def pr(rid, x, label=None, d=0.1, w=430, rot=-2, y=None): return (rid, None, w, x, (y or H / 2 - 40), rot, d, label)

SHOTS = [
 (0, ("coldopen", {})),
 (1, KB("B1", z=(1.02, 1.12))),
 (2, KB("B2", z=(1.0, 1.18), c0=(0.5, 0.3), c1=(0.52, 0.22))),
 (3, KB("E1", z=(1.0, 1.1), c0=(0.5, 0.45))),
 (4, KBP("A10")),
 (5, CARD("8:05 PM", "\u201cIs everything OK?\u201d  He said it was")),
 (6, KB("E5", z=(1.0, 1.1), c0=(0.5, 0.5))),
 (7, PRINTS([pr("A7", W / 2 - 430, "SKETCH A  \u00b7  NOV 1971", 0.1, 700), pr("A8", W / 2 + 430, "SKETCH B  \u00b7  1972", 0.7, 700, rot=2)])),
 (8, KBP("A9", h=640)),
 (9, DOC("A13", z=(0.95, 1.05), marks=[("date", 9, "night", 0.8)])),
 (10, ("title", {})),
 (11, KB("C3", z=(1.02, 1.12), c0=(0.45, 0.45))),
 (12, KB("C1", z=(1.02, 1.12))),
 (13, DOC("A12", z=(0.95, 1.05), marks=[("fare", 13, "eighteen|18", 0.5), ("total", 13, "twenty|20", 3.0)])),
 (14, DOC("A12", PH["A12"]["name"], z=(0.7, 0.85), marks=[("name", 14, "dan", 0.8)])),
 (15, CARD("SEAT 18E", "Flight 305  \u00b7  the last row")),
 (16, DOC("A16", (150, 300, 1080, 720), z=(1.0, 1.1), marks=[("drinks", 16, "bourbon", 1.5)])),
 (17, NMAP(V_PNW, ops=[("pin", *PDX, "PORTLAND", 0.2), ("route", [PDX, (-122.75, 46.3), (-122.6, 47.0), SEA], 0.5, 2.0), ("pin", *SEA, "SEATTLE", 2.4)])),
 (18, CARD("2:58 PM", "Wheels up  \u00b7  Portland")),
 (19, KB("E3", z=(1.0, 1.1), c0=(0.5, 0.45))),
 (20, LETTER("note")),
 (21, KBP("A7", h=520)),
 (22, BLACK()),
 (23, KB("E3", z=(1.1, 1.2), c0=(0.5, 0.4))),
 (24, BLACK()),
 (26, DOC("A18", (130, 700, 1010, 950), z=(1.0, 1.1), marks=[("ready", 26, "five|5", 0.6)])),
 (27, LETTER("note")),
 (28, CARD("3:20 PM", "It starts to circle")),
 (29, NMAP(V_SOUND, ops=[("pin", *SEA, "SEATTLE-TACOMA AIRPORT", 0.2), ("circle", *LOF, 7, "CIRCLING", 0.8)])),
 (30, CARD("3:22 PM", "A phone rings  \u00b7  FBI, Seattle")),
 (31, DOC("A13", (130, 530, 1110, 700), z=(1.0, 1.1), marks=[("demand", 31, "two|200", 1.5), ("bomb", 31, "bomb", 0.6)])),
 (32, DOC("A16", (150, 590, 1060, 880), z=(1.0, 1.1), marks=[("butts", 32, "smokes", 1.2)])),
 (33, KBP("A9", h=640)),
 (34, KBP("A11", h=860, rot=1.5)),
 (35, BLACK()),
 (36, NMAP(V_SOUND, ops=[("circle", *LOF, 7, "", -9), ("pin", *TAC, "TACOMA", 0.5)])),
 (37, NMAP(V_SOUND, ops=[("pin", *TAC, "TACOMA", -9), ("pin", *MCC, "McCHORD AIR FORCE BASE", 0.6)], c0=(0.5, 0.6))),
 (38, KB("C6", z=(1.02, 1.12))),
 (39, CARD("5:15 PM", "The deadline has passed")),
 (40, KBP("A10", h=860, rot=1.2)),
 (41, KB("A25", crop=(0.15, 0.08, 0.85, 0.36), z=(1.0, 1.12))),
 (42, DOC("A18", (130, 930, 1090, 1100), z=(1.0, 1.1), marks=[("film", 42, "photograph", 1.0)])),
 (43, CARD("19 LB", "The money bag")),
 (44, NMAP(V_SOUND, ops=[("circle", *LOF, 7, "", -9), ("route", [LOF, (-122.55, 47.62), SEA], 0.3, 2.0), ("pin", *SEA, "SEA-TAC  \u00b7  ABOUT 5:45 PM", 2.2)])),
 (45, KB("E2", z=(1.0, 1.1), c0=(0.5, 0.42))),
 (46, BLACK()),
 (47, KB("B2", z=(1.1, 1.25), c0=(0.55, 0.22))),
 (48, KB("A25", crop=(0.15, 0.08, 0.85, 0.36), z=(1.2, 1.35), c0=(0.6, 0.45))),
 (49, CARD("36", "Passengers let go")),
 (50, KB("A25", crop=(0.15, 0.62, 0.85, 0.92), z=(1.0, 1.12))),
 (51, KB("A3", z=(1.0, 1.12))),
 (52, KB("E7", z=(1.0, 1.1))),
 (53, KB("A3", z=(1.25, 1.4), c0=(0.3, 0.3))),
 (54, LETTER("plan")),
 (56, NMAP(V_ROUTE, ops=[("pin", *SEA, "SEATTLE", 0.2), ("pin", *RNO, "RENO, NEVADA", 1.5)])),
 (57, KB("B3", z=(1.0, 1.1))),
 (58, KB("B2", z=(1.15, 1.3), c0=(0.55, 0.2))),
 (59, KB("B1", z=(1.15, 1.25), c0=(0.6, 0.5))),
 (60, KB("C2", z=(1.0, 1.1))),
 (61, ("cta", {})),
 (65, CARD("7:36 PM", "Takeoff  \u00b7  heading south")),
 (66, KB("B5", z=(1.0, 1.12))),
 (67, KBP("A8", h=520, rot=1.5)),
 (68, KB("A3", z=(1.3, 1.45), c0=(0.2, 0.25))),
 (69, KB("E5", z=(1.1, 1.2), c0=(0.5, 0.6))),
 (70, BLACK()),
 (71, CARD("7:42 PM", "Trouble with the stairs")),
 (72, CARD("7:43 PM", "Warning light: rear stairs open")),
 (73, NMAP(V_PNW, ops=[("pin", *SEA, "SEATTLE", 0.0), ("route", V23, 0.3, 3.5), ("label", -123.75, 46.45, "AIRWAY VICTOR 23", 1.5, 30)])),
 (74, CARD("8:05 PM", "\u201cIs everything OK?\u201d")),
 (75, BLACK()),
 (76, KBP("A10", h=900)),
 (77, BLACK()),
 (78, CARD("8:10 PM", "A needle jumps")),
 (79, BLACK()),
 (80, KB("B2", z=(1.2, 1.4), c0=(0.55, 0.22), c1=(0.6, 0.2))),
 (81, KB("C8", z=(1.0, 1.15))),
 (82, BLACK()),
 (83, NMAP(V_ROUTE, ops=[("pin", *SEA, "SEATTLE", 0.0), ("route", ROUTE, 0.3, 5.0), ("pin", *RNO, "RENO", 5.2)])),
 (84, KB("E3", z=(1.05, 1.15), c0=(0.5, 0.5))),
 (85, KB("E5", z=(1.05, 1.15), c0=(0.5, 0.35))),
 (86, BLACK()),
 (87, KB("B3", z=(1.1, 1.2), c0=(0.5, 0.45))),
 (88, BLACK()),
 (89, DOC("A14", (220, 1300, 2500, 1720), z=(1.0, 1.08), marks=[("arrived", 89, "lands", 0.8), ("hand", 89, "eleven|11", 1.8)])),
 (90, KB("C7", z=(1.02, 1.12))),
 (91, BLACK()),
 (92, CARD("11:25 PM", "FBI agents climb aboard")),
 (93, KB("A1", z=(1.0, 1.12))),
 (94, DOC("A15", (140, 980, 1160, 1250), z=(1.0, 1.08), marks=[("pink", 94, "chest", 0.3), ("unopened", 94, "back", 1.8)])),
 (95, BLACK()),
 (96, KBP("A10", h=900, rot=1.0)),
 (97, KBP("A11", h=880)),
 (98, BLACK()),
 (99, DOC("A17", (470, 760, 2280, 1540), z=(1.0, 1.08), marks=[("list", 99, "serial", 1.2)])),
 (100, CARD("NORJAK", "Northwest hijacking")),
 (101, KB("E4", z=(1.0, 1.1), c0=(0.5, 0.45))),
 ((101, "ariel"), TOPO(ARIEL, 16, ops=[("ring", ARIEL, 4.0, "", (101, "ariel")), ("pin", ARIEL, "ARIEL, WASH.", (101, "ariel"))])),
 (102, DOC("A21", (140, 470, 1110, 880), z=(1.0, 1.08), marks=[("ariel", 102, "they", 0.2)])),
 (103, CARD("17", "More extortion attempts in 6 months")),
 (104, KBP("D2", h=600)),
 (106, CARD("NOV 24, 1972", "One year to the day: a new rule")),
 (107, KB("B4", z=(1.0, 1.12))),
 (108, CARD("JAN 1973", "Every passenger is screened")),
 (109, BLACK()),
 (110, TOPO((-122.70, 45.67), 24, ops=[("pin", VAN, "VANCOUVER, WASH.", (110, "vancouver")), ("pin", TENA, "TENA BAR", (110, "columbia")), ("ring", TENA, 1.3, "", (110, "columbia"))],
             c1=TENA, z=(1.0, 1.3))),
 (111, KB("A2", z=(1.0, 1.12))),
 (112, DOC("A24", (90, 110, 780, 640), z=(1.0, 1.15))),
 (113, CARD("$5,800", "290 bills")),
 (114, DOC("A22", (100, 280, 1120, 560), z=(1.0, 1.08), marks=[("tena", 114, "only", 0.3)])),
 (115, KB("C4", z=(1.02, 1.12))),
 (116, KB("A23", crop=(0.05, 0.05, 0.95, 0.5), z=(1.0, 1.12))),
 (117, KBP("A9", h=640)),
 (118, BLACK()),
 (120, KB("A1", z=(1.25, 1.4), c0=(0.35, 0.3))),
 (121, CARD("JULY 2016", "After 45 years")),
 (122, KB("A3", z=(1.05, 1.15), c0=(0.55, 0.5))),
 (123, BLACK()),
 (124, PRINTS([pr("A19", W / 2 - 560, None, 0.1, 420, -3), pr("A22", W / 2, None, 0.6, 420, 1.5), pr("A20", W / 2 + 560, None, 1.1, 420, -1)])),
 (125, BLACK()),
 (126, KBP("D2", h=600, rot=1.5)),
 (127, KB("A1", z=(1.1, 1.22), c0=(0.6, 0.55))),
 (128, CARD("OCT 2025", "Flight 305's co-pilot dies, age 86")),
 (129, CARD("$134,200", "One scrap of a ransom bill, at auction")),
 (130, BLACK()),
 (131, DOC("A12", (150, 560, 960, 880), z=(0.95, 1.05), marks=[("total", 131, "twenty|20", 0.8)])),
 (132, DOC("A18", (130, 700, 1010, 950), z=(1.0, 1.08), marks=[("demand", 132, "two|200", 1.0)])),
 (133, CARD("8:05 PM", "\u201cEverything is OK\u201d")),
 (134, KBP("A10", h=900, rot=-1)),
 (135, KB("C8", z=(1.08, 1.2))),
 (136, TOPO((-122.635, 45.81), 70, z=(1.0, 1.05), ops=[("pin", ARIEL, "1972 SEARCH", (136, "landed")),("pin", TENA, "$5,800  \u00b7  1980", (136, "other"))])),
 (137, KB("E3", z=(1.15, 1.25), c0=(0.5, 0.4))),
 (138, KBP("A10", h=920, rot=0.8)),
 (139, ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]
def sline(k): return k if isinstance(k, int) else k[0]

# overlays: (line, offset seconds | 'word', kind, args)   one text per screen slot: bottom / center / side
OV = [
 (1, 0.3, "lower", "BOEING 727-100  \u00b7  THE SAME MODEL AS FLIGHT 305"),
 (2, 0.4, "under", "THE REAR STAIRS ARE UNDER THE TAIL"),
 (7, "wasn", "under", "THE NAME ON HIS TICKET: DAN COOPER"),
 (8, 0.2, "typecenter", "800+ SUSPECTS"),
 (9, 0.3, "lower", "FBI MEMO WRITTEN THAT NIGHT  \u00b7  NOV 24, 1971"),
 (11, 0.3, "lower", "OVER PORTLAND AIRPORT  \u00b7  1973"),
 (12, 0.3, "lower", "PORTLAND INTERNATIONAL AIRPORT  \u00b7  1973"),
 (13, 0.2, "lower", "HIS TICKET  \u00b7  FBI EVIDENCE PHOTO"),
 (16, 0.2, "lower", "FBI CASE SUMMARY  \u00b7  \u201cHABITS\u201d"),
 (17, 0.6, "under", "PORTLAND \u2192 SEATTLE  \u00b7  ABOUT 36 MINUTES"),
 (22, 0.0, "list", ["RED CYLINDERS  \u00b7  ABOUT 8", "WIRES", "A LARGE BATTERY"]),
 (23, "nobody", "typecenter", "REAL? NEVER PROVEN"),
 (25, 0.0, "list", ["$200,000", "4 PARACHUTES", "A FUEL TRUCK"]),
 (26, 0.2, "lower", "FBI SEATTLE TO THE SECRET SERVICE  \u00b7  DEC 10, 1971"),
 (27, "nobody", "stamp", ("NEVER FOUND", 1430, 800)),
 (29, 1.0, "under", "PASSENGERS ARE TOLD: \u201cA MINOR MECHANICAL PROBLEM\u201d"),
 (31, 0.2, "lower", "FBI MEMO  \u00b7  NOV 24, 1971"),
 (32, 0.2, "lower", "8 CIGARETTE BUTTS IN HIS ASHTRAY  \u00b7  FBI"),
 (33, 0.3, "under", "\u201cNOT GOING TO CUBA\u201d"),
 (35, 0.0, "quote", ("\u201cIt's not because I have a grudge against your airlines.\nIt's just because I have a grudge.\u201d", "THE HIJACKER  \u00b7  AS TOLD TO THE FBI")),
 (36, 0.4, "under", "\u201cWE'RE OVER TACOMA NOW\u201d"),
 (37, "twenty|20", "under", "\u201cONLY 20 MINUTES AWAY\u201d"),
 (38, 0.3, "lower", "SEATTLE FROM THE AIR  \u00b7  1973"),
 (40, "still", "under", "\u201cSTILL WAITING\u201d"),
 (41, 0.3, "lower", "RANSOM-SERIES $20 BILLS  \u00b7  FBI LAB COPY"),
 (41, "ten|10", "typecenter", "10,000 \u00d7 $20"),
 (42, 0.2, "lower", "\u201cMICROFILMED FOR LATER EVIDENTIARY USE\u201d"),
 (45, 0.4, "under", "FAR FROM THE TERMINAL"),
 (46, 0.0, "list", ["ONE CAR", "THE STAIR TRUCK", "THE FUEL TRUCK", "NO FLASHING LIGHTS"]),
 (48, "looks", "under", "\u201cIT LOOKS OKAY\u201d"),
 (51, 0.3, "lower", "ONE OF THE PARACHUTES HE LEFT BEHIND  \u00b7  FBI"),
 (52, "doesn", "under", "HE SAYS HE DOESN'T NEED IT"),
 (53, 0.4, "under", "THE NYLON CORD FROM A CHEST PARACHUTE"),
 (56, 0.3, "under", "MEXICO IS TOO FAR WITH THE GEAR DOWN  \u00b7  FUEL STOP: RENO"),
 (57, "show", "under", "\u201cLET'S GET THE SHOW ON THE ROAD\u201d"),
 (58, "can", "typecenter", "REAR STAIRS DOWN, IN FLIGHT?"),
 (59, 0.2, "under", "BOEING: YES"),
 (60, "one", "under", "ONE FLIGHT ATTENDANT STAYS"),
 (66, 0.3, "lower", "318TH FIGHTER INTERCEPTOR SQUADRON  \u00b7  McCHORD AIR FORCE BASE"),
 (68, 0.3, "under", "A NYLON CORD AROUND HIS WAIST"),
 (69, "says", "quote", ("\u201cHe will take it, or disarm it.\u201d", "HIS ANSWER  \u00b7  PER THE FLIGHT ATTENDANT")),
 (70, "nobody", "typecenter", "NOBODY CAN SEE HIM"),
 (73, 0.8, "under", "AIRWAY VICTOR 23  \u00b7  APPROXIMATE ROUTE"),
 (75, 0.0, "typecenter", "\u201cEVERYTHING IS OK\u201d"),
 (76, 0.3, "under", "THE LAST WORDS ON RECORD"),
 (77, 0.0, "list", ["10,000 FEET", "ABOUT 200 MPH", "19\u00b0F  \u00b7  RAIN"]),
 (79, 0.0, "quote", ("\u201cIt is a virtual certainty that the pressure \u2018bump\u2019\nmarks the time that the high-jacker left the airplane.\u201d", "FBI ANALYSIS  \u00b7  DEC 4, 1971")),
 (80, 0.4, "under", "DOWN THE REAR STAIRS"),
 (83, 0.4, "under", "ALMOST 3 MORE HOURS  \u00b7  APPROXIMATE ROUTE"),
 (84, 0.4, "under", "A COLDER CABIN, A LITTLE HIGHER"),
 (85, 0.3, "under", "ICE OVER OREGON"),
 (86, 0.0, "typecenter", "NO ANSWER"),
 (87, "sir", "under", "\u201cSIR, WE ARE GOING TO LAND NOW\u201d"),
 (89, 0.2, "lower", "FBI TELETYPE  \u00b7  LAS VEGAS  \u00b7  7:25 AM, NOV 25, 1971"),
 (90, 0.3, "lower", "RENO, NEVADA  \u00b7  1973"),
 (91, 0.1, "typecenter", "EMPTY"),
 (93, 0.3, "lower", "HIS TIE  \u00b7  J.C. PENNEY \u201cTOWNCRAFT\u201d  \u00b7  FBI EVIDENCE"),
 (94, 0.2, "lower", "FBI SEARCH REPORT  \u00b7  RENO, 11:25 PM"),
 (95, 0.0, "list", ["THE BRIEFCASE", "THE MONEY", "2 PARACHUTES"]),
 (95, "gone", "stamp", ("GONE", 1500, 830)),
 (96, "cooper", "stamp", ("MISSING", 1420, 820)),
 (97, 0.4, "under", "THE FBI'S BULLETIN, 1971"),
 (98, 0.2, "typecenter", "DAN COOPER  \u2192  \u201cD.B.\u201d"),
 (99, 0.2, "lower", "FBI PRESS RELEASE  \u00b7  DEC 3, 1971  \u00b7  THE RANSOM LIST"),
 (101, 0.3, "lower", "SOUTHWEST WASHINGTON"),
 (101, "ariel", "lower", "USGS MAP, 1979  \u00b7  THE 1972 SEARCH AREA (APPROX.)"),
 (102, 0.2, "under", "NO PARACHUTE  \u00b7  NO MONEY  \u00b7  NO BODY"),
 (104, 0.3, "lower", "RICHARD McCOY  \u00b7  HIJACKED A UNITED FLIGHT, APRIL 1972"),
 (105, "ruled", "stamp", ("RULED OUT", 1420, 820)),
 (107, 0.3, "lower", "THE \u201cCOOPER VANE\u201d  \u00b7  UNDER A 727 TAIL"),
 (108, "before", "under", "BEFORE THAT: ABOUT 1 IN 100"),
 (109, 0.0, "typecenter", "1973 \u2192 1980"),
 (110, 0.2, "lower", "USGS MAP  \u00b7  VANCOUVER, WASH.  \u00b7  1979"),
 (111, 0.3, "lower", "THE MONEY FOUND AT TENA BAR  \u00b7  FBI PHOTO"),
 (112, 0.2, "lower", "FBI INVENTORY OF THE RECOVERED BILLS"),
 (114, 0.2, "lower", "FBI INTERVIEW  \u00b7  FEB 1980"),
 (115, 0.4, "under", "2020 STUDY: ALGAE ON A BILL POINT TO SUMMER"),
 (116, 0.3, "lower", "TENA BAR SAND LAYERS  \u00b7  FBI FILE, 1980"),
 (117, 0.2, "typecenter", "800+ PEOPLE"),
 (118, 0.0, "list", ["A FORMER PARATROOPER", "A MAN WHOSE WIDOW SAID HE CONFESSED", "A MAN NAMED BY HIS NIECE"]),
 (119, "ruled", "stamp", ("NO LINK", 1500, 900)),
 (120, 0.3, "under", "2001: DNA FROM THE TIE  \u00b7  WEAK AND MIXED"),
 (122, 0.3, "under", "THE FBI STILL ASKS: A PARACHUTE, OR THE MONEY"),
 (123, 0.0, "typecenter", "THE FILE IS STILL OPEN"),
 (124, 0.4, "under", "THE FBI KEEPS RELEASING ITS FILES"),
 (125, "eliminate", "typecenter_red", "\u201cELIMINATE RUSSELL\u201d"),
 (125, 0.2, "under", "A PILOT FROM MAINE  \u00b7  FBI PAGE FROM 1972, RELEASED 2026"),
 (126, 0.3, "under", "HIS FAMILY: RIG RETURNED DEC 2025, NO FINDINGS GIVEN"),
 (127, 0.3, "under", "MAY 2026: A NEW STUDY OF THE TIE"),
 (130, 0.0, "typecenter", "WHAT THE RECORDS SAY"),
 (134, 0.3, "typecenter", "WHO: UNKNOWN"),
 (135, "probably", "under", "FBI AGENTS: PROBABLY DIDN'T SURVIVE"),
 (136, "other", "under", "$194,000: NEVER FOUND"),
 (137, 0.1, "typecenter", "THE BOMB: REAL?"),
 (138, "certain", "stamp", ("UNSOLVED", 1440, 830)),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

# ------------------------------------------------------------------ drawing helpers
def shot_at(t):
    k = 0
    for j, st in enumerate(SHOT_T):
        if st <= t: k = j
    t0 = SHOT_T[k]; t1 = SHOT_T[k + 1] if k + 1 < len(SHOTS) else DUR
    return k, SHOTS[k], t0, t1

def view(src, cx, cy, s):
    w, h = W / s, H / s; box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    if box[0] >= 0 and box[1] >= 0 and box[2] <= src.width and box[3] <= src.height:
        return src.resize((W, H), Image.BICUBIC, box=box).convert("RGBA")
    c = Image.new("RGB", (W, H), INK)
    ix0, iy0, ix1, iy1 = max(box[0], 0), max(box[1], 0), min(box[2], src.width), min(box[3], src.height)
    if ix1 > ix0 and iy1 > iy0:
        part = src.resize((max(1, int((ix1 - ix0) * s)), max(1, int((iy1 - iy0) * s))), Image.BICUBIC, box=(ix0, iy0, ix1, iy1))
        c.paste(part, (int((ix0 - box[0]) * s), int((iy0 - box[1]) * s)))
    return c.convert("RGBA")

def spotlight(c, box, k):
    if k <= 0: return
    m = Image.new("L", (W, H), 255); ImageDraw.Draw(m).rectangle([int(v) for v in box], fill=0); m = m.filter(ImageFilter.GaussianBlur(10))
    lay = Image.new("RGBA", (W, H), (8, 8, 9, 0)); lay.putalpha(m.point(lambda v: int(v * 0.62 * k))); c.alpha_composite(lay)

def lower(c, s, t, t0):
    if t < t0: return
    lay = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); g = np.clip(np.linspace(0, 1, 260) * 1.7, 0, 1)[:, None] ** 1.3 * 238
    lay.putalpha(Image.fromarray(np.repeat(g, W, 1).astype(np.uint8))); c.alpha_composite(lay, (0, H - 260))
    L.typewriter(c, s, t, t0, 90, H - 110, size=38, cps=34, cursor=False)
    L.rule(c, 90, 90 + min(len(s), 40) * 23, H - 76, t, t0 + 0.2, width=5)
def under(c, s, t, t0):
    if t < t0: return
    lay = Image.new("RGBA", (W, 170), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, 0, W, 170), fill=(0, 0, 0, 190))
    c.alpha_composite(lay, (0, H - 170)); L.typewriter(c, s, t, t0, W / 2, H - 92, size=50 if len(s) < 48 else 42, cps=30, anchor="mm", cursor=False)

SLOT = {"lower": "bottom", "under": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "list_side": "side"}
OVT = [OT(ln, off) for ln, off, _, _ in OV]
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    for j2 in range(len(OV)):
        if OVT[j2] <= OVT[j] or j2 == j: continue
        k2 = OV[j2][2]
        if SLOT.get(k2) == sl or (sl == "bottom" and k2 in ("list", "typecenter", "typecenter_red", "quote")):
            return min(OVT[j2] - 0.05, shot_t1)
    return shot_t1
NO_BOTTOM = False                                  # teasers: their own captions replace the bottom band
def draw_ov(c, t, shot_t0, shot_t1):
    for j, (ln, off, kind, a) in enumerate(OV):
        t0 = OVT[j]
        if t < t0 or t >= shot_t1 or t0 < shot_t0 - 0.2: continue
        if NO_BOTTOM and SLOT.get(kind) == "bottom": continue
        if t >= ov_end(j, shot_t1): continue
        if kind == "lower": lower(c, a, t, t0)
        elif kind == "under": under(c, a, t, t0)
        elif kind in ("typecenter", "typecenter_red"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 110, W, H / 2 + 110), fill=(0, 0, 0, 185)); c.alpha_composite(lay)
            L.typewriter(c, a, t, t0, W / 2, H / 2, size=96 if len(a) < 26 else 74, fill=RED if kind.endswith("red") else BONE, cps=16, anchor="mm", cursor=False)
        elif kind == "list":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay); sz = 74 if max(len(s) for s in a) < 30 else 58
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W / 2, H / 2 - (len(a) - 1) * 60 + i * 120, size=sz, cps=20, anchor="mm", cursor=False)
        elif kind == "stamp": L.stamp(c, a[0], a[1], a[2], t, t0, size=100)
        elif kind == "quote":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay); qs = a[0].split("\n")
            for i, q in enumerate(qs):
                L.text(c, q, W / 2, H / 2 - 40 - (len(qs) - 1) * 42 + i * 84, 50 if NO_BOTTOM and len(q) > 44 else 60, BONE, SER, alpha=ease((t - t0 - 0.25 * i) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, W / 2, H / 2 + 60 + (len(qs) - 1) * 42, size=34, fill=STEEL, cps=34, anchor="mm", cursor=False)

PC = {}
def pcard(rid, crop, w, rot):
    k = (rid, crop, w, rot)
    if k not in PC: PC[k] = L.print_card(tone(rid, crop), w, rot=rot)
    return PC[k]
def pcard_h(rid, crop, h, rot):
    src = tone(rid, crop); return pcard(rid, crop, int(h * src.width / src.height), rot)
BG = {}
def blur_bg(rid, crop):
    k = (rid, crop)
    if k not in BG:
        src = tone(rid, crop); s = max(W / src.width, H / src.height)
        im = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.BICUBIC); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(30))
        BG[k] = Image.blend(im, Image.new("RGB", (W, H), INK), 0.62).convert("RGBA")
    return BG[k]

def hand_paper(c, t, rows, foot, t_foot):
    """a sheet of paper with hand-printed rows, each written when its key word is spoken"""
    d = ImageDraw.Draw(c); x0, x1, y0, y1 = W / 2 - 560, W / 2 + 560, 120, H - 150
    d.rectangle((x0 + 14, y0 + 18, x1 + 14, y1 + 18), fill=(4, 4, 5)); d.rectangle((x0, y0, x1, y1), fill=(226, 220, 204))
    n = len(rows); gap = min(120, (y1 - y0 - 120) / max(n, 1))
    for i, (s, key) in enumerate(rows):
        L.typewriter(c, s, t, AT(key), x0 + 90, y0 + 110 + i * gap, size=62 if len(s) < 22 else 50, fill=(28, 26, 30), cps=24, anchor="lm", fnt=HAND, cursor=False)
    L.typewriter(c, foot, t, t_foot, W / 2, H - 78, size=27, fill=STEEL, cps=50, anchor="mm", cursor=False)

LETTERS = {
 "note": ([("MISS \u2014", (20, "miss")), ("I AM HIJACKING THIS PLANE.", (20, "hijacking")), ("I HAVE A BOMB.", (20, "bomb")), ("SIT NEXT TO ME.", (20, "sit"))],
          "RECONSTRUCTION  \u00b7  FROM THE FLIGHT ATTENDANT'S ACCOUNT  \u00b7  THE REAL NOTE WAS NEVER FOUND"),
 "plan": ([("MEXICO CITY", (55, "mexico")), ("GEAR DOWN", (55, "landing")), ("FLAPS 15\u00b0", (55, "flaps")), ("UNDER 10,000 FT", (55, "stay")),
           ("CABIN LIGHTS OUT", (55, "cabin")), ("NOBODY BEHIND THE CURTAIN", (55, "nobody"))],
          "RECONSTRUCTION  \u00b7  FROM WHAT THE FLIGHT ATTENDANT WROTE DOWN"),
}

def topo_frame(a, t, t0, t1):
    src = topo_img(); u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6))); z = a["z"][0] + (a["z"][1] - a["z"][0]) * u
    (ax, ay), (bx, by) = topo_px(*a["c"]), topo_px(*(a["c1"] or a["c"])); cx, cy = ax + (bx - ax) * u, ay + (by - ay) * u
    s = W / (a["km"] * PXKM) * z
    cx = min(max(cx, W / 2 / s), src.width - W / 2 / s); cy = min(max(cy, H / 2 / s), src.height - H / 2 / s)
    c = L.vignette(view(src, cx, cy, s), 0.35)
    def S(p): x, y = topo_px(*p); return (x - cx) * s + W / 2, (y - cy) * s + H / 2
    for op in a["ops"]:
        if op[0] == "ring":
            _, p, r_km, label, key = op; ts = AT(key)
            if t >= ts:
                x, y = S(p); r = r_km * PXKM * s; L.red_ellipse(c, (x - r, y - r * 0.8, x + r, y + r * 0.8), t, ts, dur=0.7, width=7)
    for op in a["ops"]:
        if op[0] == "pin":
            _, p, label, key = op; ts = AT(key)
            if t < ts: continue
            x, y = S(p); u2 = ease((t - ts) / 0.25); r = 12 * (1.6 - 0.6 * u2); d = ImageDraw.Draw(c)
            d.ellipse((x - r - 5, y - r - 5, x + r + 5, y + r + 5), fill=INK); d.ellipse((x - r, y - r, x + r, y + r), fill=RED)
            if label and t >= ts + 0.15:
                f = L.font(TYPE, 34); n = min(len(label), int((t - ts - 0.15) * 34) + 1); tw = f.getlength(label)
                lx = x + 30 if x + 40 + tw < W - 30 else x - 30 - tw - 28
                d.rectangle((lx - 12, y - 28, lx + tw + 14, y + 26), fill=INK); d.text((lx, y), label[:n], font=f, fill=BONE, anchor="lm")
    return c


AMB = {}
def ambient(k):
    """no flat black screens (LESSONS 19): the nearest photo shot, blurred a little and dimmed, sits behind every card"""
    if k not in AMB:
        if len(AMB) > 6: AMB.clear()
        im = None
        for j in list(range(k - 1, -1, -1)) + list(range(k + 1, len(SHOTS))):
            kind_j, a_j = SHOTS[j][1]
            if kind_j in ("kb", "kbp") and a_j.get("rid"):
                src = tone(a_j["rid"], a_j.get("crop")).convert("RGB"); s = max(W / src.width, H / src.height)
                im = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.BICUBIC)
                x0, y0 = (im.width - W) // 2, (im.height - H) // 2
                im = im.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(6))
                im = Image.blend(im, Image.new("RGB", (W, H), INK), 0.52).convert("RGBA"); break
        if im is None: im = Image.new("RGBA", (W, H), INK + (255,))
        band = np.clip(1 - np.abs(np.arange(H) - H / 2) / (H * 0.34), 0, 1)[:, None] * 125
        lay = Image.new("RGBA", (W, H), INK + (0,)); lay.putalpha(Image.fromarray(np.repeat(band, W, 1).astype(np.uint8))); im.alpha_composite(lay)
        AMB[k] = im
    return AMB[k].copy()


def frame(t):
    k, (key, (kind, a)), t0, t1 = shot_at(t)
    if kind == "kb":
        src = tone(a["rid"], a["crop"], a["rot"]); c = L.vignette(L.kenburns(src, t, t0, t1, a["z"][0], a["z"][1], a["c0"], a["c1"]))
    elif kind == "kbp":
        c = blur_bg(a["rid"], a["crop"]).copy(); u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6)))
        card = pcard_h(a["rid"], a["crop"], a["h"], a["rot"]); k2 = 1.0 + 0.05 * u
        card = card.resize((int(card.width * k2), int(card.height * k2)), Image.BICUBIC)
        L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30)
    elif kind == "coldopen":
        c = blur_bg("E3", None).copy()
        if NO_BOTTOM:                                                    # vertical teaser: centred, no print card
            L.typewriter(c, "8:10 PM", t, t0 + 0.05, W / 2, H / 2 - 60, size=150, cps=10, anchor="mm", cursor=False)
            L.text(c, "Wednesday, November 24, 1971", W / 2, H / 2 + 60, 50, BONE, SER, alpha=ease((t - t0 - 1.0) / 0.4))
            L.rule(c, W / 2 - 290, W / 2 + 290, H / 2 + 110, t, t0 + 1.2); draw_ov(c, t, t0, t1); return c
        card = pcard_h("B2", None, 760, 3); c.alpha_composite(card, (int(W * 0.70 - card.width / 2), int(H / 2 - card.height / 2)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip(1.25 - np.linspace(0, 1, W) * 1.9, 0, 1)[None, :] * 235
        lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
        L.typewriter(c, "8:10 PM", t, t0 + 0.05, 110, H / 2 - 60, size=150, cps=10, anchor="lm", cursor=False)
        L.text(c, "Wednesday, November 24, 1971", 115, H / 2 + 60, 50, BONE, SER, anchor="lm", alpha=ease((t - t0 - 1.0) / 0.4))
        L.rule(c, 115, 700, H / 2 + 110, t, t0 + 1.2)
    elif kind == "card":
        c = ambient(k); big = a["big"]
        L.typewriter(c, big, t, t0 + 0.05, W / 2, H / 2 - 50, size=200 if len(big) < 10 else 150, cps=12, anchor="mm", cursor=False)
        t2 = t0 + 0.05 + len(big) / 12
        L.text(c, a["sub"], W / 2, H / 2 + 120, 58, STEEL, SER, alpha=ease((t - t2) / 0.4)); L.rule(c, W / 2 - 280, W / 2 + 280, H / 2 + 185, t, t2 + 0.15)
    elif kind == "doc":
        rid = a["rid"]; src = page_img(rid); fx0, fy0, fx1, fy1 = a["focus"]; u = ease((t - t0) / max(t1 - t0, 0.5))
        s_fit = min(W * 0.8 / (fx1 - fx0), H * 0.62 / (fy1 - fy0)); s = s_fit * (a["z"][0] + (a["z"][1] - a["z"][0]) * u)
        cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2; act = None
        for box, ln, word, off in a["marks"]:
            tm = wt(ln, word) or T[ln] + off
            if t >= tm: act = (PH[rid][box], tm)
        if act:
            b, tm = act; v = ease((t - tm) / 0.6); cx += ((b[0] + b[2]) / 2 - cx) * 0.55 * v; cy += ((b[1] + b[3]) / 2 - cy) * 0.8 * v
        cx = min(max(cx, W / 2 / s), src.width - W / 2 / s) if src.width * s > W else src.width / 2
        cy = min(max(cy, H / 2 / s), src.height - H / 2 / s) if src.height * s > H else src.height / 2
        c = view(src, cx, cy, s)
        if act:
            b, tm = act; sx0, sy0, sx1, sy1 = (b[0] - cx) * s + W / 2 - 18, (b[1] - cy) * s + H / 2 - 12, (b[2] - cx) * s + W / 2 + 18, (b[3] - cy) * s + H / 2 + 12
            spotlight(c, (sx0, sy0, sx1, sy1), ease((t - tm) / 0.35))
            uu = ease((t - tm - 0.1) / 0.3); ImageDraw.Draw(c).rectangle((sx0 + 10, sy1 + 4, sx0 + 10 + (sx1 - sx0 - 20) * uu, sy1 + 11), fill=RED)
        c = L.vignette(c, 0.45)
    elif kind == "nmap":
        c = MS.map_panel(a, t, t0, t1)
    elif kind == "topo":
        c = topo_frame(a, t, t0, t1)
    elif kind == "prints":
        c = ambient(k)
        for rid, crop, w, x, y, rot, d, label in a["items"]:
            if NO_BOTTOM: w, x = int(w * 0.85), W / 2 + (x - W / 2) * 0.75     # keep both prints inside the vertical crop
            L.drop(c, pcard(rid, crop, w, rot), x, y, t, t0 + d)
            if label: L.typewriter(c, label, t, t0 + d + 0.35, x, y + pcard(rid, crop, w, rot).height / 2 + 30, size=32, cps=30, anchor="mm", cursor=False)
    elif kind == "letter":
        c = ambient(k); rows, foot = LETTERS[a["key"]]; hand_paper(c, t, rows, foot, t0 + 0.4)
    elif kind == "title":
        c = ambient(k); u = ease((t - t0) / 0.6)
        L.text(c, "the", W / 2, H / 2 - 170, 80, STEEL, SER, alpha=u); L.text(c, "LAST HOURS", W / 2, H / 2 - 10, 240, BONE, COND, alpha=u)
        L.rule(c, W / 2 - 320, W / 2 + 320, H / 2 + 135, t, t0 + 0.4, width=9)
        L.typewriter(c, "FILE 03  \u00b7  D.B. COOPER  \u00b7  NOV 24, 1971", t, t0 + 0.9, W / 2, H / 2 + 230, size=40, fill=STEEL, cps=30, anchor="mm", cursor=False)
    elif kind == "cta":
        c = L.vignette(L.kenburns(tone("F4"), t, t0, t1, 1.05, 1.15)); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 150)))
        pass  # spoken ask cut 23 Oct (LESSONS 21): L.typewriter(c, "EVERYTHING HERE IS FROM
        if t >= T[64]: L.typewriter(c, "7:36 PM", t, T[64] + 0.3, W / 2, H / 2, size=120, fill=BONE, cps=10, anchor="mm", cursor=False)
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 120, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 230, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 320, t, t0, width=7)
        L.typewriter(c, "NEXT FILE:  EGYPTAIR 990", t, T[140], W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
        if t > VO_END:
            d = ImageDraw.Draw(c)
            for x in (110, 1170): d.rectangle((x, 520, x + 640, 880), outline=STEEL + (255,), width=3)
            d.ellipse((835, 575, 1085, 825), outline=STEEL + (255,), width=3)
    else:
        c = ambient(k)
    draw_ov(c, t, t0, t1)
    return c

# ------------------------------------------------------------------ audio
def load(p, sr=48000):
    a, s = sf.read(p, dtype="float32", always_2d=True); a = a.mean(1)
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    return a
def tl(i, off=0.0): return T[i] + off
def audio():
    sr = 48000; N = int(DUR * sr); vo = load(VOF); y = np.zeros(N, np.float32)
    s0 = int(LEAD * sr); y[s0:s0 + len(vo)] += vo[: N - s0]
    vr = np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)); bed = np.zeros(N, np.float32)
    def put(a, t, db, fade=0.02):
        i = int(t * sr); a = a[: max(0, N - i)] * 10 ** (db / 20)
        if len(a) == 0: return
        f = int(fade * sr)
        if f > 1 and len(a) > 2 * f: a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        bed[i:i + len(a)] += a
    def sfx(name, t, db, maxlen=None):
        a = load(SFXD + name + ".mp3"); a = a / (np.max(np.abs(a)) + 1e-9) * vr * 3.2
        if maxlen and len(a) > maxlen * sr:
            a = a[: int(maxlen * sr)].copy(); f = int(0.25 * sr); a[-f:] *= np.linspace(1, 0, f)
        put(a, t, db)
    def music(file, t0, t1, db):
        a = load(MUS + file); n = int((t1 - t0) * sr)
        while len(a) < n: a = np.concatenate([a, load(MUS + file)])
        a = a[:n] / (np.sqrt(np.mean(a[:n] ** 2)) + 1e-9) * vr; put(a, t0, db, fade=2.5)
    def loop(name, t0, t1, db):
        a = load(SFXD + name + ".mp3"); n = int((t1 - t0) * sr)
        while len(a) < n: a = np.concatenate([a, a])
        a = a[:n] / (np.sqrt(np.mean(a[:n] ** 2)) + 1e-9) * vr; put(a, t0, db, fade=1.5)
    # music beds (Kevin MacLeod, CC BY), at or below -22 dB under the voice
    music("Late Night Radio.mp3", tl(10), tl(28), -27); music("Man Down.mp3", tl(28), tl(61), -25); music("Thunder Dreams.mp3", tl(61), tl(65), -22)
    music("Thunder Dreams.mp3", tl(65), tl(92), -25); music("Rising Tide.mp3", tl(92), tl(123), -26); music("Industrial Cinematic.mp3", tl(123), tl(139), -26)
    music("Thunder Dreams.mp3", tl(139), DUR, -22)
    loop("wind_deep_cinematic_hum", 0, tl(10), -24); loop("roomtone_dark_cinematic", tl(18), tl(28), -32); loop("wind_deep_cinematic_hum", tl(65), tl(92), -31)
    loop("wind_ambience", tl(77), tl(82), -28); loop("wind_scary", tl(101), tl(103), -30)
    HITS = [("hit_deep_heartbeat_impact", -17), ("hit_short_bass", -19), ("hit_glass_suspense", -21), ("hit_cinematic_deep_impact", -20)]
    SWIPES = [("whoosh_fast_transition", -22), ("paper_slide", -20), ("whoosh_ghostly", -24)]; MK = [0]
    for i, (key, (kind, a)) in enumerate(SHOTS):
        t0 = SHOT_T[i]
        if kind == "card":
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "doc": sfx("paper_slide", t0, -18); sfx("typewriter_soft_click", t0 + 0.2, -24)
        elif kind == "prints":
            for it in a["items"]: sfx("paper_slide", t0 + it[6], -17); sfx("camera_vintage_shutter", t0 + it[6] + 0.15, -24)
        elif kind == "kbp": sfx("paper_slide", t0, -19); sfx("camera_vintage_shutter", t0 + 0.12, -25)
        elif kind in ("nmap", "topo"): sfx("paper_page_turn", t0, -22)
        elif kind == "letter":
            sfx("paper_slide", t0, -18)
            for s, k2 in LETTERS[a["key"]][0]:
                if AT(k2) > t0: sfx("paper_writing_pencil", AT(k2), -22, maxlen=1.2)
        elif kind == "title": sfx("hit_cinematic_deep_impact", t0, -12); sfx("typewriter_return_bell", t0 + 2.0, -20)
        elif kind == "kb": sfx("whoosh_fast_transition", t0 - 0.1, -32)
        for box, ln, word, off in a.get("marks", ()):
            tm = wt(ln, word) or T[ln] + off; MK[0] += 1; h = HITS[MK[0] % len(HITS)]; w = SWIPES[MK[0] % len(SWIPES)]
            sfx(h[0], tm, h[1], maxlen=1.8); sfx(w[0], tm + 0.1, w[1], maxlen=0.9)
        if kind == "nmap":
            for op in a["ops"]:
                if op[0] == "pin" and op[4] >= 0: sfx("camera_classic_click", t0 + op[4], -22)
                if op[0] == "circle" and op[5] >= 0: sfx("camera_lens_autofocus", t0 + op[5], -26, maxlen=1.0)
        if kind == "topo":
            for op in a["ops"]:
                if op[0] == "pin": sfx("camera_classic_click", AT(op[3]), -22)
                if op[0] == "ring": sfx("paper_writing_pencil", AT(op[4]), -24, maxlen=0.8)
    for j, (ln, off, kind, a) in enumerate(OV):
        if kind == "stamp": sfx("hit_horror_drum", OVT[j], -14)
        if kind in ("typecenter", "typecenter_red", "list"): sfx("typewriter_typing_old", OVT[j], -26)
    sfx("hit_cinematic_deep_impact", 0.0, -14)
    for j in range(len("8:10 PM")): sfx("typewriter_single_hit", 0.05 + j / 10, -20)
    EV = [(1, 0.2, "thunder_deep_rumble", -24), (3, "needle", "hit_deep_heartbeat_impact", -16), (6, 0.3, "wind_scary", -26), (11, 0.2, "helicopter_far_away", -34),
          (13, 0.3, "papers_moving", -24), (16, "bourbon", "keys_moving", -30), (18, 0.2, "whoosh_tunnel_reverb", -22), (19, "note", "paper_slide", -18),
          (21, "briefcase", "gear_metallic_lock", -22), (30, 0.3, "telephone_vintage_ring", -20), (32, "smokes", "light_switch", -30), (34, "laughs", "heartbeat_single", -28),
          (39, 0.2, "clock_ticking_closeup", -24), (41, 0.3, "papers_moving", -22), (42, "photographs", "camera_old_shutter_click", -20),
          (43, 0.3, "newspaper_drop", -20), (47, 0.3, "footsteps_tunnel_loop", -28), (53, "cuts", "metal_tool_drop", -24), (57, "show", "heartbeat_slow", -22),
          (66, 0.3, "helicopter_far_away", -30), (67, "stands", "heavy_sliding_door", -30), (70, 0.2, "heavy_sliding_door", -24), (71, 0.6, "radio_static_crackles", -26),
          (72, 0.6, "alarm_vintage_warning", -26), (74, 0.6, "radio_static_fx", -24), (75, 0.0, "radio_static_crackles", -26), (78, "needle", "hit_big_cinematic_impact", -14),
          (80, 0.3, "whoosh_ghostly", -20), (81, 0.2, "wind_scary", -22), (85, 0.3, "wind_cold_interior", -24), (87, "sir", "radio_static_crackles", -24),
          (88, 0.0, "heartbeat_slow", -20), (90, "switches|lights", "light_switch", -16), (91, 0.1, "hit_cinematic_deep_impact", -14), (93, 0.3, "camera_vintage_shutter", -20),
          (97, 0.3, "reporters_camera_flashes", -22), (98, 0.3, "newspaper_drop", -18), (101, 0.4, "helicopter_flying", -30), (102, "nothing", "wind_ambience", -26),
          (106, 0.3, "paper_signing", -22), (107, 0.3, "metal_hammer_hit", -24), (110, 0.3, "waves_harbor_rocks", -28), (111, "bundles", "paper_big_page_turn", -20),
          (115, 0.4, "waves_rocky_shore", -28), (121, 0.4, "locking_door_with_keys", -22), (125, "eliminate", "typewriter_classic_return", -20),
          (128, 0.4, "clock_bells_hour", -24), (133, 0.4, "radio_static_crackles", -26), (138, "certain", "clock_wall_tick", -22), (139, 0.2, "typewriter_return_bell", -18)]
    for ln, off, name, db in EV: sfx(name, OT(ln, off), db, maxlen=4.0)
    y += bed; pk = np.max(np.abs(y)); y = y / max(pk, 1e-6) * 0.9
    sf.write(B + "mix_raw.wav", y, sr, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(B + "mix_raw.wav", B + "mix.wav", target=-14, tp=-1); print("audio", AM.measure(B + "mix.wav"))

def seg(i, n):
    a, b = NF * i // n, NF * (i + 1) // n
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "3", "-pix_fmt", "yuv420p", B + f"seg_{i}.mp4"], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(frame(f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("seg done", i, flush=True)
def final(n, name="TheLastHours_03_DBCooper.mp4"):
    with open(B + "segs.txt", "w") as f:
        for i in range(n): f.write(f"file 'seg_{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "qa":
        prep()
        ts = [float(x) for x in sys.argv[2:]] or [(SHOT_T[i] + (SHOT_T[i + 1] if i + 1 < len(SHOTS) else DUR)) / 2 for i in range(len(SHOTS))]
        tiles = [frame(t).convert("RGB").resize((384, 216)) for t in ts]; cols = 6
        S = Image.new("RGB", (cols * 394, ((len(tiles) + cols - 1) // cols) * 236), (20, 20, 20))
        for i, (im, tt) in enumerate(zip(tiles, ts)):
            S.paste(im, ((i % cols) * 394, (i // cols) * 236)); ImageDraw.Draw(S).text(((i % cols) * 394 + 6, (i // cols) * 236 + 218), f"{tt:.1f}", fill=(255, 220, 90))
        out = B + ("qa.png" if len(sys.argv) > 2 else "qa_all.png"); S.save(out); print(out)
    elif m == "chapters":
        CH = [(0, "8:10 PM: the plane moves"),(11, "Portland: a $20 ticket"), (18, "2:58 PM: the note"), (28, "3:20 PM: circling Seattle"),
              (39, "5:15 PM: the money"), (44, "Sea-Tac: parachutes and a flight plan"), (65, "7:36 PM: the stairs"), (74, "8:05 PM: the last words"),
              (82, "Three hours to Reno"), (92, "11:25 PM: an empty seat"), (97, "The search, the copycats, the Cooper vane"), (109, "1980: money in the sand"),
              (117, "800 suspects"), (123, "2025\u201326: the file is still open"), (130, "What the records can't tell us")]
        for i, (ln, name) in enumerate(CH):
            t = 0 if i == 0 else T[ln] - 0.12; print(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    elif m == "times":
        for i in range(len(LINES)): print(f"{i:3d} {T[i]:7.2f} {LINES[i][:70]}")
        print("VO_END", VO_END, "DUR", DUR, "shots", len(SHOTS))
    elif m == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "audio": audio()
    elif m == "final": final(int(sys.argv[2]))
    elif m == "all":
        n = int(sys.argv[2]); env = dict(os.environ, PYTHONUTF8="1"); prep()
        low = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0)          # stay out of the way of whatever else runs on the PC
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), "seg", str(i), str(n)], env=env, creationflags=low) for i in range(n)]
        for p in ps: p.wait()
        audio(); final(n)
    elif m == "prep": prep()
