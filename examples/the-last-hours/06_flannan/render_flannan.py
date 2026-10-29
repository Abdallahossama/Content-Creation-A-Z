"""The Last Hours #5: Flannan Isles, 15-29 Dec 1900 (Case File style, 1920x1080). Built on render_roanoke.py.
Every shot starts on a narration line (index into vo_lines.txt without '##'), or on a spoken word in it: key (line, "word").
Line timing comes from the exact-zero gaps in the VO, word timing from whisper (vo/vo_words.json).
  uv run --no-project --with pillow --with numpy --with soundfile python render_flannan.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines (they cut across the sounds at this scale)
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/06_flannan/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
HAND = "C:/Windows/Fonts/segoeprb.ttf"                 # hand-printed look for the reconstruction cards
ROMAN = "C:/Windows/Fonts/timesbd.ttf"                 # Roman capitals for the carved-letter reconstructions
LEAD = 0.8; TAIL = 20.0

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = ROOT + "vo/flannan_vo_chatterbox.wav"
_vo, VSR = sf.read(VOF, dtype="float32")
if _vo.ndim > 1: _vo = _vo.mean(1)
_z = np.concatenate([[False], _vo == 0.0, [False]]).astype(np.int8); _d = np.diff(_z)
GAPS = [(a, b) for a, b in zip(np.where(_d == 1)[0], np.where(_d == -1)[0]) if b - a >= int(0.3 * VSR)]
assert len(GAPS) == len(LINES), (len(GAPS), len(LINES))
T = [LEAD + (0 if i == 0 else GAPS[i - 1][1]) / VSR for i in range(len(LINES))]
LE = [LEAD + g[0] / VSR for g in GAPS]
VO_END = LEAD + len(_vo) / VSR; DUR = VO_END + TAIL; NF = int(DUR * FPS); del _vo, _z, _d
WORDS = {}
if os.path.exists(ROOT + "vo/vo_words.json"):
    for sg in json.load(open(ROOT + "vo/vo_words.json", encoding="utf-8")):
        WORDS[sg["line"]] = [(w["s"] - sg["start"], w["w"]) for w in sg["words"]]
def wt(line, word, off=0.0):
    for rel, w in WORDS.get(line, []):
        if any(re.sub(r"[^a-z0-9]", "", w.lower()).startswith(x) for x in word.lower().split("|")): return T[line] + rel + off
    return None
def AT(key):
    if isinstance(key, int): return T[key]
    ln, w = key
    if isinstance(w, (int, float)): return T[ln] + w
    tm = wt(ln, w); return tm if tm is not None else T[ln] + 0.3
def KT(key): return AT(key) - (0.12 if isinstance(key, int) else 0.08)


# ------------------------------------------------------------------ assets
def P(rid):
    for f in sorted(glob.glob(B + f"_small_{rid}.png")) + sorted(glob.glob(M + rid + "_*")):
        h = open(f, "rb").read(4)
        if h[:3] == b"\xff\xd8\xff" or h == b"\x89PNG" or h in (b"II*\x00", b"MM\x00*"): return f
    return None
ROT = {"C1", "C3", "C4", "C9"}                          # Talbot plates printed sideways: turn 90 degrees clockwise after the crop
IMG = {}
def tone(rid, crop=None, rot=0):
    k = (rid, crop)
    if k not in IMG:
        im = L.bw(P(rid), crop)
        IMG[k] = im.transpose(Image.Transpose.ROTATE_270) if rid in ROT else im
    return IMG[k]

def prep():
    for f in glob.glob(M + "*"):
        rid = os.path.basename(f).split("_")[0]
        if os.path.exists(B + f"_small_{rid}.png"): continue
        try: im = Image.open(f)
        except Exception: continue
        if max(im.size) > 4200:
            im = im.convert("RGB"); k = 4200 / max(im.size); im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS).save(B + f"_small_{rid}.png")

# map points (lon, lat)
FLAN, GALLAN, UIG, BREAS, CALLAN = (-7.588, 58.288), (-7.029, 58.241), (-7.026, 58.179), (-6.743, 58.218), (-6.745, 58.201)
OBAN, EDIN, LEITH, PHIL, LAB = (-5.472, 56.412), (-3.19, 55.95), (-3.17, 55.98), (-75.16, 39.95), (-62.4, 58.3)
ARCH = [PHIL, (-62, 44.5), (-42, 53.5), (-22, 58.2), (-8.2, 58.35), (-5.0, 58.75), (-3.1, 58.72), (-1.9, 57.7), (-2.3, 56.3), LEITH]
V_HEB, V_LEWIS, V_SCOT, V_ATL = (-6.95, 58.12, 2.6), (-7.0, 58.22, 1.6), (-5.0, 56.8, 11.0), (-38.0, 50.0, 80.0)

# ------------------------------------------------------------------ shot constructors
CROP = {"B1": (0.06, 0.10, 0.88, 0.80), "B2": (0.06, 0.11, 0.88, 0.80), "C1": (0.04, 0.11, 0.86, 0.81), "C3": (0.12, 0.12, 0.84, 0.85),
        "C4": (0.14, 0.12, 0.84, 0.85), "C5": (0.05, 0.03, 0.96, 0.86), "C6": (0.15, 0.04, 0.93, 0.80), "C7": (0.07, 0.06, 0.92, 0.81),
        "C8": (0.10, 0.04, 0.96, 0.53), "C9": (0.11, 0.10, 0.86, 0.80), "H4": (0.2, 0.37, 0.86, 0.655), "H5": (0.06, 0.25, 0.955, 0.66),
        "H6": (0.06, 0.25, 0.955, 0.66), "H7": (0.11, 0.20, 0.85, 0.72), "E5": (0.08, 0.15, 0.62, 0.92), "E6": (0.2, 0.0, 1.0, 1.0),
        "E7": (0.12, 0.12, 0.9, 1.0), "E9": (0.12, 0.05, 1.0, 1.0), "G2": (0.0, 0.0, 1.0, 0.75), "D3": (0.0, 0.1, 1.0, 0.7),
        "A5": (0.35, 0.0, 0.85, 0.45), "A7": (0.0, 0.15, 0.5, 0.5)}
C2_LAND, C2_TOP = (0.05, 0.48, 0.95, 0.86), (0.05, 0.03, 0.95, 0.40)
IL = "ILLUSTRATIVE"
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag))
def CARD(big, sub): return ("card", dict(big=big, sub=sub))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def LETTER(key): return ("letter", dict(key=key))
def TYPED(key): return ("typed", dict(key=key))
def BLACK(): return ("black", {})
def COUNTER(steps, sub, bg, red=False): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red))
def CLIFF(marks): return ("cliff", dict(marks=marks))
def pr(rid, x, label=None, d=0.1, w=430, rot=-2, y=None): return (rid, CROP.get(rid), w, x, (y or H / 2 - 40), rot, d, label)
def PRINTS(items): return ("prints", dict(items=items))
def D(line, word): return AT((line, word)) - KT(line)              # a word's offset inside its line's shot

SHOTS = [
 (0, ("vanish", dict(mark=(0, "three"), gone=(0, "gone")))),        # frame 1: the real keepers; on "gone" they vanish
 (2, TCARD("ABOUT NOON", "Wednesday, December 26, 1900", "H5")),
 (3, NMAP(V_HEB, ops=[("pin", *FLAN, "FLANNAN ISLES", 0.6), ("pin", *GALLAN, "ISLE OF LEWIS", 1.6), ("arrow", FLAN, GALLAN, "20 MILES", 2.4)])),
 (4, KBP("H20", h=920, tag="THE FLANNAN LIGHT FROM THE SEA · 2012")),
 ((4, "flag"), KBP("H15", h=920, rot=1.2, tag="THE FLANNAN LIGHT · 2012")),
 (5, KB("E17", z=(1.0, 1.12), tag=IL)),
 (6, KB("H5", z=(1.05, 1.2))),
 (7, KB("H6", z=(1.0, 1.12), c0=(0.6, 0.5))),
 (8, KBP("H19", h=920, tag="THE LANDING STEPS · 2012")),
 ((8, "gate"), KB("D4", z=(1.05, 1.18), c0=(0.55, 0.4), tag="NEIST POINT · A SISTER STATION")),
 (9, KB("E9", z=(1.0, 1.12), tag=IL)),
 ((9, "clock"), KB("E6", z=(1.1, 1.3), c0=(0.55, 0.42), tag=IL)),
 (10, KB("C4", z=(1.0, 1.12))),
 (11, KB("E18", z=(1.0, 1.1), tag=IL)),
 (12, KB("E15", z=(1.15, 1.35), c0=(0.5, 0.6), tag=IL)),
 (13, LETTER("fake")),
 ((14, "made"), CARD("DECADES LATER", "Not in a single record from 1900")),
 (15, PRINTS([pr("E7", W / 2 - 560, "A NOTE ON A SLATE", 0.1), pr("G4", W / 2, "A COAT ON ITS PEG", D(15, "coat"), rot=1.5),
              pr("E2", W / 2 + 560, "MOVED BY THE SEA", D(15, "stone"), rot=-1)])),
 (16, KB("E3", z=(1.0, 1.12), tag=IL)),
 (17, TCARD("9:00 AM", "Saturday, December 15, 1900", "E7")),
 (18, KB("H4", z=(1.1, 1.25), c0=(0.53, 0.47))),
 (19, KB("B2", z=(1.0, 1.1), tag="A KEEPER, 1913 · NOT ONE OF THE THREE")),
 (20, KB("B1", z=(1.0, 1.1), tag="A KEEPER, 1913 · NOT ONE OF THE THREE")),
 (21, KB("C8", z=(1.0, 1.1), tag="BARRA HEAD LIGHT, HEBRIDES · 1913")),
 (22, KB("E7", z=(1.0, 1.15), tag=IL)),
 ((22, "barometer"), LETTER("slate")),
 (23, KB("E7", z=(1.2, 1.35), tag=IL)),
 (24, CARD("DEC 7", "Remember this date")),
 (25, KB("C1", z=(1.0, 1.12))),
 (26, NMAP(V_HEB, ops=[("pin", *FLAN, "FLANNAN ISLES", 0.2), ("pin", *GALLAN, "LEWIS", 0.8), ("arrow", FLAN, GALLAN, "20 MILES", 1.2)])),
 ((26, "due"), NMAP(V_ATL, ops=[("pin", *FLAN, "FLANNAN ISLES", 0.1, -330, 0), ("arrow", FLAN, LAB, "", 0.4), ("pin", *LAB, "CANADA · ABOUT 1,900 MILES", 1.1)])),
 (27, KB("E10", z=(1.0, 1.12), tag=IL)),
 (28, KB("B1", z=(1.1, 1.25), c0=(0.5, 0.4), tag="A KEEPER CLEANING THE LAMP · 1913")),
 ((28, "oil"), KB("B2", z=(1.1, 1.2), tag="THE OIL PUMPS OF A LIGHTHOUSE · 1913")),
 ((28, "lens"), KB("E4", z=(1.0, 1.12), tag=IL)),
 ((28, "blinds"), KB("C6", z=(1.0, 1.1), tag="A LANTERN · 1913")),
 (29, KB("C3", z=(1.0, 1.1))),
 (30, KB("C3", z=(1.2, 1.3), c0=(0.45, 0.5))),
 (31, KB("E18", z=(1.1, 1.2), c0=(0.5, 0.55), tag=IL)),
 (32, TCARD("AFTERNOON", "Saturday, December 15, 1900", "E1")),
 (33, KB("E5", z=(1.0, 1.12), tag=IL)),
 (34, KBP("H17", h=920, tag="THE TRAMWAY AND STEPS TO THE WEST LANDING · 2012")),
 (35, ("chart", dict(rid="G1", crop=(0.62, 0.355, 0.77, 0.4733), foot="ADMIRALTY CHART 3331  ·  1903  ·  LANDING POSITIONS APPROXIMATE",
                     pins=[(0.513, 0.47, "THE LIGHTHOUSE", (35, 0.0), "up"), (0.546, 0.571, "EAST LANDING", (35, "east"), "right"),
                           (0.471, 0.571, "WEST LANDING", (35, "west"), "left")]))),
 (36, KB("H7", z=(1.0, 1.12), c0=(0.5, 0.6))),
 ((36, "70|seventy"), CLIFF([("crane", (36, "70|seventy"))])),
 (37, KB("E2", z=(1.0, 1.15), tag=IL)),
 (38, KB("G4", z=(1.0, 1.12), c0=(0.5, 0.45), tag=IL)),
 (39, KB("E1", z=(1.15, 1.35), tag=IL)),
 (40, KB("C7", z=(1.0, 1.1), tag="A LIGHT AT NIGHT · 1913")),
 (41, KB("D4", z=(1.1, 1.25), c0=(0.4, 0.6), tag="NEIST POINT · A SISTER STATION")),
 (42, TCARD("3:39 PM", "Sunset  ·  Saturday, December 15", "E14")),
 (43, KB("C5", z=(1.0, 1.15), tag="A LANTERN FROM BELOW · 1913")),
 (44, BLACK()),
 (45, CARD("MIDNIGHT", "Saturday, December 15, 1900")),
 ((45, "steamer"), NMAP(V_ATL, ops=[("pin", *PHIL, "PHILADELPHIA", 0.2), ("route", ARCH, 0.5, 3.0), ("pin", *FLAN, "FLANNAN ISLES", 2.6, -330, 0), ("pin", *LEITH, "LEITH", 3.6, -150, 0)])),
 (46, KB("G5", z=(1.0, 1.12), tag=IL)),
 (47, KB("E10", z=(1.1, 1.25), tag=IL)),
 (48, KB("E1", z=(1.0, 1.1), tag=IL)),
 (49, NMAP(V_SCOT, ops=[("pin", *FLAN, "", -9), ("pin", *LEITH, "LEITH · EDINBURGH", 0.4)])),
 (50, NMAP(V_LEWIS, ops=[("pin", *FLAN, "FLANNAN ISLES", 0.2), ("pin", *UIG, "THE LOOKOUT · UIG", 0.9)])),
 (51, KB("A7", z=(1.0, 1.12), tag="ORDNANCE SURVEY, LEWIS · 1959")),
 (52, KB("E17", z=(1.1, 1.2), tag=IL)),
 (53, COUNTER([((53, "six"), "6"), ((53, "seven"), "7"), ((53, "eight"), "8")], "NIGHTS WITHOUT THE LIGHT", "E3")),
 (54, KB("D3", z=(1.0, 1.12), tag=IL)),
 (55, NMAP(V_SCOT, ops=[("pin", *FLAN, "FLANNAN ISLES", -9), ("pin", *EDIN, "NORTHERN LIGHTHOUSE BOARD", 0.4)])),
 (56, CARD("DEC 20", "The great gale")),
 ((56, "wrecks"), KB("E2", z=(1.1, 1.25), tag=IL)),
 (57, KB("C2", crop=C2_LAND, z=(1.0, 1.1), tag="A RELIEF LANDING AT ANOTHER ROCK LIGHT · 1913")),
 (58, NMAP(V_SCOT, ops=[("pin", *OBAN, "OBAN · DEC 24", 0.3), ("arrow", OBAN, FLAN, "", 1.0), ("pin", *FLAN, "FLANNAN ISLES", 1.8)])),
 (59, KBP("H21", h=920, tag="THE FLANNAN LIGHT · 2012")),
 (60, COUNTER([((60, 0.0), "11")], "NIGHTS DARK", "E14", red=True)),
 (61, TCARD("EARLY AFTERNOON", "Wednesday, December 26, 1900", "H6")),
 (62, KBP("H19", h=920, rot=1.5, tag="THE LANDING STEPS · 2012")),
 (63, KB("D4", z=(1.0, 1.1), c0=(0.5, 0.45), tag="NEIST POINT · A SISTER STATION")),
 (64, KB("C6", z=(1.05, 1.15), tag="A LANTERN · 1913")),
 (65, LETTER("inventory")),
 (68, KB("G4", z=(1.15, 1.3), c0=(0.55, 0.4), tag=IL)),
 (69, KB("D3", z=(1.1, 1.2), tag=IL)),
 (70, KB("H5", z=(1.0, 1.12))),
 (71, TCARD("3:43 PM", "Sunset  ·  Wednesday, December 26", "E3")),
 ((71, "lights"), KB("E3", z=(1.0, 1.15), tag=IL)),
 (72, NMAP(V_LEWIS, ops=[("pin", *UIG, "THE LOOKOUT", -9), ("pin", *FLAN, "THE LIGHT IS BACK", 0.4)])),
 (73, NMAP(V_SCOT, ops=[("pin", *CALLAN, "CALLANISH TELEGRAPH", 0.2), ("arrow", CALLAN, EDIN, "", 0.9), ("pin", *EDIN, "EDINBURGH", 1.6)])),
 (74, TYPED("telegram")),
 (77, KB("A5", z=(1.0, 1.12), tag="MAP OF THE FLANNAN ISLES · 1888")),
 (78, KB("H6", z=(1.1, 1.2), c0=(0.65, 0.55))),
 (79, KB("H7", z=(1.0, 1.1))),
 (80, CLIFF([("crane", -9), ("box", (80, "wooden")), ("gone", (80, "gone"))])),
 (81, KBP("H17", h=920, rot=1.0, tag="THE PATH TO THE WEST LANDING · 2012")),
 (82, TCARD("EARLY MORNING", "Saturday, December 29, 1900", "H7")),
 (83, CLIFF([("crane", (83, "crane"))])),
 (84, KB("H7", z=(1.2, 1.35), c0=(0.45, 0.6))),
 (85, KB("E13", z=(1.0, 1.12), tag=IL)),
 (86, CLIFF([("crane", -9), ("box", -9), ("gone", -9), ("buoy", (86, "life"))])),
 (87, CARD("2,240 LB", "More than a ton of stone, moved")),
 (88, KB("E2", z=(1.15, 1.3), c0=(0.55, 0.5), tag=IL)),
 (89, KB("E1", z=(1.0, 1.12), tag=IL)),
 (90, KB("C9", z=(1.0, 1.1), tag="A STEVENSON ROCK LIGHT · 1913")),
 (91, CARD("DEC 7, 1900", "The last relief")),
 (92, KB("H6", z=(1.0, 1.1))),
 (93, KB("E14", z=(1.0, 1.2), tag=IL)),
 (94, KB("E3", z=(1.1, 1.2), tag=IL)),
 (95, KB("E17", z=(1.1, 1.25), tag=IL)),
 (96, CARD("JAN 8, 1901", "Muirhead's report")),
 (97, KB("H7", z=(1.05, 1.18), c0=(0.5, 0.65))),
 (98, KB("E2", z=(1.0, 1.12), tag=IL)),
 (99, KB("D1", z=(1.0, 1.12), tag=IL)),
 (100, KB("E10", z=(1.0, 1.12), tag=IL)),
 (101, KB("G4", z=(1.0, 1.1), tag=IL)),
 (102, BLACK()),
 (103, KB("E2", z=(1.0, 1.12), tag=IL)),
 (104, KB("E15", z=(1.0, 1.15), c0=(0.5, 0.6), tag=IL)),
 ((104, "second"), KB("E2", z=(1.2, 1.35), tag=IL)),
 (105, CARD("1990", "Ducat's daughter, aged 98")),
 (106, KB("H7", z=(1.1, 1.2))),
 (107, KB("E18", z=(1.0, 1.12), tag=IL)),
 (108, KB("D1", z=(1.1, 1.25), c0=(0.5, 0.6), tag=IL)),
 (109, KB("E2", z=(1.0, 1.15), tag=IL)),
 (110, BLACK()),
 (111, KB("E11", z=(1.0, 1.12), tag="LEGEND · ILLUSTRATIVE")),
 (112, CARD("JAN 5, 1901", "The Oban Times")),
 ((112, "local"), NMAP(V_SCOT, ops=[("pin", *FLAN, "FLANNAN ISLES", -9), ("pin", *OBAN, "OBAN  ·  THE OBAN TIMES", 0.3)])),
 (113, KB("E8", z=(1.0, 1.12), tag="LEGEND · ILLUSTRATIVE")),
 (114, KB("C3", z=(1.0, 1.12))),
 (115, CARD("1912", "A poem")),
 ((115, "meal"), KB("E11", z=(1.1, 1.25), tag="LEGEND · ILLUSTRATIVE")),
 (116, CARD("1929", "True Strange Stories")),
 (117, LETTER("fake2")),
 (118, BLACK()),
 (119, LETTER("fake2")),
 (120, KB("E7", z=(1.0, 1.12), tag=IL)),
 ((120, "stops"), LETTER("real")),
 (121, KBP("H15", h=920, tag="THE FLANNAN LIGHT · 2012")),
 (122, NMAP(V_LEWIS, ops=[("pin", *FLAN, "FLANNAN ISLES", -9), ("pin", *BREAS, "BREASCLETE · THE MEMORIAL", 0.4)])),
 (123, CARD("2026", "Moore's letter, on display in Edinburgh")),
 (124, KB("E10", z=(1.1, 1.25), tag=IL)),
 (125, KB("E7", z=(1.1, 1.3), tag=IL)),
 (126, KB("H4", z=(1.0, 1.15), c0=(0.53, 0.47))),
 (127, KB("E1", z=(1.0, 1.1), tag=IL)),
 (128, ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "lower", "THE 3 KEEPERS + THEIR SUPERINTENDENT (RIGHT)  ·  AS CAPTIONED, c. 1900"),
 (1, "never", "typecenter_red", "NEVER FOUND"),
 (4, "isn", "typecenter", "NO FLAG"),
 (5, 0.3, "under", "THE STEAM WHISTLE  ·  THEN THE SIREN"),
 (6, 0.1, "lower", "EILEAN MOR FROM THE SOUTH  ·  PHOTO c. 1904-11"),
 (6, "nothing", "typecenter", "NO ANSWER"),
 (7, 0.1, "lower", "THE EAST LANDING  ·  PHOTO c. 1904-11"),
 (7, "joseph", "under", "JOSEPH MOORE, KEEPER  ·  NO PHOTO OF HIM IS KNOWN"),
 (8, "gate", "under", "GATE: CLOSED  ·  DOORS: CLOSED"),
 (9, 0.3, "under", "THE FIRE: NOT LIT FOR DAYS"),
 (9, "clock", "typecenter", "THE CLOCK: STOPPED"),
 (10, 0.1, "lower", "A LIGHTHOUSE BEDROOM  ·  1913"),
 (10, "empty", "typecenter", "THE BEDS: EMPTY"),
 (11, 0.0, "quote", ("“I did not take time to search further...”", "JOSEPH MOORE  ·  LETTER, 28 DECEMBER 1900")),
 (14, "fake", "stamp", ("FAKE", 1430, 470)),
 (16, 0.1, "brand", None),
 (16, "famous", "under", "TRUE OR MADE UP?  BY THE END, YOU'LL KNOW"),
 (17, "eleven", "under", "11 DAYS BEFORE MOORE LANDS"),
 (18, 0.1, "lower", "EILEAN MOR, “THE BIG ISLAND”  ·  ABOUT 40 ACRES"),
 (19, 0.0, "nameplate", ("JAMES DUCAT", "PRINCIPAL KEEPER  ·  IN HIS 40s  ·  MARRIED, 4 CHILDREN")),
 (20, 0.0, "nameplate", ("THOMAS MARSHALL", "ASSISTANT KEEPER  ·  ABOUT 30  ·  NOT MARRIED")),
 (21, 0.0, "nameplate", ("DONALD McARTHUR", "STAND-IN KEEPER  ·  EX-ARMY  ·  FROM LEWIS")),
 (23, 0.1, "typecenter", "THE LAST THING THEY WROTE"),
 (25, 0.1, "lower", "THE FLANNAN LIGHT IN FLAGS, c. 1913  ·  MEN IN PHOTO UNNAMED"),
 (25, "first", "under", "FIRST LIT: DECEMBER 7, 1899"),
 (27, 0.0, "quote", ("“There is no land between\nthe Flannan Islands and America.”", "THE SCOTSMAN  ·  28 DECEMBER 1900")),
 (29, 0.1, "lower", "A LIGHTHOUSE KITCHEN  ·  1913"),
 (29, "pots", "under", "POTS AND PANS: CLEANED  ·  KITCHEN: TIDY"),
 (30, 0.0, "typecenter", "REMEMBER THE KITCHEN"),
 (31, "things", "under", "WHAT THEY LEFT BEHIND"),
 (33, 0.1, "under", "MARSHALL: SEA BOOTS + OILSKINS"),
 (33, "ducat", "under", "DUCAT: SEA BOOTS + AN OLD WATERPROOF COAT"),
 (34, "landings", "under", "WORN ONLY FOR THE LANDINGS  ·  JOSEPH MOORE"),
 (36, 0.1, "lower", "THE CRANE LANDING (“SOUTH LANDING” IN 1912)  ·  c. 1904-11"),
 (37, "sea", "under", "WINTER 1899-1900: THE FIRST CRANE, WASHED AWAY"),
 (38, "coat", "typecenter", "HIS COAT STAYED ON THE PEG"),
 (39, "shirt", "typecenter_red", "IN HIS SHIRTSLEEVES"),
 (40, "night", "under", "THE RULE: ONE MAN WITH THE LIGHT AT NIGHT"),
 (41, "nobody", "typecenter", "WHO CLOSED THE GATE?"),
 (43, "trimmed", "under", "TRIMMED  ·  FULL  ·  READY"),
 (44, 0.0, "typecenter_red", "NOBODY LIGHTS IT"),
 (46, "moon", "under", "NO MOON UNTIL ABOUT 3 AM  ·  COMPUTED"),
 (47, "can", "typecenter", "NO LIGHT"),
 (48, 0.0, "quote", ("“...he felt satisfied that\nhe should have seen it.”", "CAPTAIN HOLMAN, SS ARCHTOR  ·  MUIRHEAD'S REPORT, 1901")),
 (49, 0.6, "under", "THE BOARD HEARS ABOUT IT ON DECEMBER 28"),
 (50, "8|eight", "under", "PAID £8 A YEAR"),
 (51, "12|twelfth", "under", "LAST SEEN FROM LEWIS: DECEMBER 12"),
 (52, "four", "under", "IN HAZE, 4 OR 5 DARK NIGHTS WERE NORMAL"),
 (54, "neighbors|neighbours", "under", "THE NEIGHBORS HELP THEM LOOK"),
 (55, 0.6, "under", "NOBODY TELLS THE BOARD"),
 (57, "weather", "under", "THE RELIEF IS HELD UP BY STORMS"),
 (59, "dark", "typecenter", "CHRISTMAS DAY: STILL DARK"),
 (62, "shouts", "under", "MOORE CALLS UP THE BOAT CREW"),
 (63, "again", "under", "THE SECOND SEARCH"),
 (64, "lamp", "list", ["THE LAMP: CLEANED", "THE FOUNTAIN: FULL", "BLINDS: ON THE WINDOWS"]),
 (68, 0.0, "quote", ("“He never used any other coat...”", "JOSEPH MOORE  ·  28 DECEMBER 1900")),
 (69, "night", "under", "“NIGHT COMING ON”  ·  CAPTAIN HARVIE"),
 (70, "volunteers", "under", "MOORE + 3 VOLUNTEERS KEEP THE LIGHT"),
 (72, "first", "under", "THE FIRST LIGHT IN 11 NIGHTS"),
 (77, 0.0, "subpop", None),
 (77, "end", "under", "THURSDAY, DECEMBER 27  ·  THE ISLAND SEARCHED"),
 (78, "touched", "under", "EAST LANDING: UNTOUCHED  ·  ROPES STILL COILED"),
 (79, "west", "typecenter", "THE WEST SIDE"),
 (81, "torn", "under", "IRON RAILINGS: TORN OUT AND TWISTED"),
 (82, "robert", "under", "SUPERINTENDENT ROBERT MUIRHEAD"),
 (84, "fine", "under", "THE CRANE: UNHARMED  ·  ARM LASHED DOWN"),
 (85, "every", "under", "EVERY COIL STILL FASTENED"),
 (88, 0.2, "typecenter", "VERY HIGH. VERY HARD."),
 (89, "15|fifteenth", "list", ["DECEMBER 15?", "OR THE GALE OF DECEMBER 20?"]),
 (90, "chosen", "under", "MUIRHEAD HAD CHOSEN THESE MEN"),
 (92, 0.0, "quote", ("“I was the last person to shake hands\nwith them and bid them adieu.”", "ROBERT MUIRHEAD  ·  REPORT, 8 JANUARY 1901")),
 (93, 0.2, "typecenter", "WHAT DUCAT SAID"),
 (94, 0.0, "quote", ("“...just to ascertain how soon it would be seen ashore\nand how soon it would be acted upon.”", "JAMES DUCAT, 7 DEC 1900  ·  AS RECORDED BY MUIRHEAD")),
 (95, "eleven", "typecenter_red", "11 NIGHTS. NOBODY ACTED."),
 (97, "west", "under", "HIS FINDING: THE WEST LANDING"),
 (98, 0.0, "quote", ("“...an unexpectedly large roller...”", "ROBERT MUIRHEAD  ·  8 JANUARY 1901")),
 (99, "west", "under", "A WESTERLY WIND: UP THE ISLAND, NOT INTO THE SEA"),
 (100, 0.2, "list", ["NO WITNESS", "NO BODIES", "NO INQUIRY"]),
 (102, 0.0, "typecenter", "WHY ALL THREE?"),
 (102, "mcarthur|macarthur", "typecenter_red", "WHY NO COAT?"),
 (103, "theory", "under", "THEORY 1  ·  TWO WAVES  ·  KEEPER WALTER ALDEBERT, 1950s"),
 (104, "second", "typecenter_red", "A SECOND WAVE"),
 (106, "fined", "under", "FINED 5 SHILLINGS  ·  FAMILY ACCOUNT"),
 (107, 0.2, "under", "THEORY 2  ·  THEY WENT TO CHECK THE DAMAGE"),
 (108, "cave", "under", "THEORY 3  ·  THE CAVE UNDER THE LANDING"),
 (109, "boulders", "under", "STORM BOULDERS UP TO 164 FT UP  ·  HALL ET AL., 2006"),
 (110, 0.0, "typecenter", "NONE OF IT IS PROOF"),
 (111, 0.2, "typecenter", "THE LEGEND"),
 (113, "chairs", "stamp", ("LEGEND", 1450, 800)),
 (114, "official", "under", "THE OFFICIAL REPORT: POTS CLEANED, KITCHEN TIDY"),
 (115, "meal", "under", "1912  ·  A POEM: A MEAL, A CHAIR, THREE BLACK BIRDS"),
 (118, 0.0, "typecenter_red", "IT WAS THE ARCHTOR"),
 (119, "fiction", "stamp", ("FICTION", 1420, 470)),
 (121, 0.2, "under", "AUTOMATED: SEPTEMBER 28, 1971"),
 (122, "bronze", "under", "A BRONZE WAVE, 3 NAMES  ·  UNVEILED 2017"),
 (124, "body", "list", ["NO BODY", "NO WITNESS", "NO LOG"]),
 (125, "chalked", "under", "9 AM, DECEMBER 15, 1900  ·  THE WEATHER"),
 (127, "tell", "under", "ONE WAVE, OR SOMETHING ELSE?  TELL ME BELOW"),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

LETTERS = {
 "fake": ([("McARTHUR CRYING", (13, "crying")), ("ME, DUCAT AND McARTHUR PRAYED", (13, "pray")), ("STORM ENDED, SEA CALM.", (13, "last")),
           ("GOD IS OVER ALL.", (13, "god"))], "THE FAMOUS “LOG”  ·  AS RETOLD SINCE 1965  ·  NOT IN ANY RECORD FROM 1900"),
 "fake2": ([("DUCAT IRRITABLE", (117, "ducat")), ("McARTHUR CRYING", (117, "crying")), ("THE PRAYERS", (117, "prayers")),
            ("GOD IS OVER ALL", (117, "god"))], "VINCENT GADDIS, INVISIBLE HORIZONS (1965)  ·  FIRST CONFIRMED PRINTING OF THE “LOG”"),
 "slate": ([("9 A.M.,  SAT 15 DEC", (22, "barometer", )), ("BAROMETER", (22, "barometer")), ("THERMOMETER", (22, "thermometer")),
            ("WIND", (22, "wind"))], "RECONSTRUCTION  ·  WHAT THE SLATE RECORDED (THE SLATE ITSELF IS LOST)"),
 "real": ([("REAL LOG: ENDS DEC 13", (120, "stops")), ("LAST NOTE: THE SLATE", (120, "slate")), ("9 A.M., DEC 15", (120, "nine|9")),
           ("IN DUCAT'S HAND", (120, "ducat")), ("THE WEATHER", (120, "weather"))], "WHAT THE RECORDS SAY  ·  NORTHERN LIGHTHOUSE BOARD"),
 "inventory": ([("MARSHALL: BOOTS, OILSKINS - GONE", (66, "marshall")), ("DUCAT: BOOTS, WATERPROOF - GONE", (66, "ducat")),
                ("McARTHUR: HIS COAT - STILL HERE", (67, "everyday|coat"))], "FROM JOSEPH MOORE'S LETTER, 28 DECEMBER 1900"),
}
TYPES = {
 "telegram": ([("A DREADFUL ACCIDENT HAS", (74, 0.0)), ("HAPPENED AT FLANNANS.", (74, "happened")), ("THE THREE KEEPERS ... HAVE", (75, "three")),
               ("DISAPPEARED FROM THE ISLAND.", (75, "disappeared")), ("POOR FELLOWS THEY MUST HAVE BEEN", (76, "poor")),
               ("BLOWN OVER THE CLIFFS OR DROWNED", (76, "blown"))], "CAPTAIN HARVIE'S TELEGRAM, 26 DECEMBER 1900  ·  WORDS FROM THE RECORD, TYPESET BY US"),
}
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

SLOT = {"lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "list_side": "side"}
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
        else: ov_extra(c, kind, a, t, t0)

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


def tag(c, s):
    if not s: return
    f = L.font(TYPE, 24); w = f.getlength(s)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((W - 60 - w, 30, W - 30, 72), fill=(0, 0, 0, 150)); c.alpha_composite(lay)
    ImageDraw.Draw(c).text((W - 45, 51), s, font=f, fill=STEEL, anchor="rm")

def ov_extra(c, kind, a, t, t0):
    if kind == "nameplate":
        lay = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); g = np.clip(np.linspace(0, 1, 300) * 1.6, 0, 1)[:, None] ** 1.2 * 240
        lay.putalpha(Image.fromarray(np.repeat(g, W, 1).astype(np.uint8))); c.alpha_composite(lay, (0, H - 300))
        L.typewriter(c, a[0], t, t0, 90, H - 150, size=96, fill=BONE, cps=18, anchor="lm", fnt=COND, cursor=False)
        L.rule(c, 92, 92 + len(a[0]) * 44, H - 96, t, t0 + 0.4, width=6)
        L.typewriter(c, a[1], t, t0 + 0.6, 92, H - 58, size=32, fill=STEEL, cps=40, anchor="lm", cursor=False)
    elif kind == "brand":                                      # 2 s channel stamp over moving footage: no spoken ident, no pause
        u = t - t0
        if u < 2.2:
            al = ease(u / 0.35) * ease((2.2 - u) / 0.35)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 150, W, H / 2 + 150), fill=(0, 0, 0, int(150 * al))); c.alpha_composite(lay)
            L.text(c, "the", W / 2, H / 2 - 95, 52, STEEL, SER, alpha=al); L.text(c, "LAST HOURS", W / 2, H / 2 + 5, 150, BONE, COND, alpha=al)
            L.text(c, "FILE 05  ·  FLANNAN ISLES  ·  DECEMBER 1900", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
    elif kind == "subpop":                                     # mid-video subscribe nudge, top-left, 4 s
        u = t - t0
        if u < 4.0:
            k = ease(u / 0.4) * ease((4.0 - u) / 0.4); x = 40 - (1 - k) * 640
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x, 40, x + 600, 112), 36, fill=RED + (int(235 * k),))
            c.alpha_composite(lay); L.text(c, "SUBSCRIBE FOR THE NEXT FILE", x + 300, 77, 34, BONE, TYPE, alpha=k)

def typed_paper(c, t, rows, foot, t_foot):
    """typewritten sheet (telegram text from the record, set in type by us)"""
    d = ImageDraw.Draw(c); x0, x1, y0, y1 = W / 2 - 620, W / 2 + 620, 110, H - 150
    d.rectangle((x0 + 14, y0 + 18, x1 + 14, y1 + 18), fill=(4, 4, 5)); d.rectangle((x0, y0, x1, y1), fill=(232, 226, 206))
    d.text((x0 + 70, y0 + 60), "TELEGRAM", font=L.font(TYPE, 30), fill=(120, 40, 36), anchor="lm")
    d.line((x0 + 70, y0 + 92, x1 - 70, y0 + 92), fill=(120, 40, 36), width=3)
    n = len(rows); gap = min(108, (y1 - y0 - 190) / max(n, 1))
    for i, (s, key) in enumerate(rows):
        L.typewriter(c, s, t, AT(key), x0 + 80, y0 + 170 + i * gap, size=48, fill=(28, 26, 30), cps=26, anchor="lm", fnt=TYPE, cursor=False)
    L.typewriter(c, foot, t, t_foot, W / 2, H - 78, size=27, fill=STEEL, cps=50, anchor="mm", cursor=False)

def cliff_frame(a, t, t0, t1):
    """our own diagram: the west side of Eilean Mor with the heights from Muirhead's report (not to scale)"""
    c = Image.new("RGBA", (W, H), INK + (255,)); d = ImageDraw.Draw(c)
    def Y(ft): return 905 - ft * 2.45                          # 0 ft at y 905, 289 ft near the top
    sea_t = None
    for name, key in a["marks"]:
        if name == "gone": sea_t = t0 - 9 if key == -9 else AT(key) - 0.6
    surge = 0.0 if sea_t is None else ease((t - sea_t) / 0.9) * (1 - 0.35 * ease((t - sea_t - 1.4) / 1.5))
    face = [(160, H), (160, Y(0)), (300, Y(30)), (360, Y(70)), (560, Y(70)), (600, Y(110)), (700, Y(150)), (760, Y(200)), (900, Y(240)),
            (1000, Y(270)), (1180, Y(289)), (1180, H)]
    d.polygon(face, fill=(58, 57, 55)); d.line(face[1:-1], fill=(120, 124, 128), width=4)
    d.rectangle((0, Y(0), W, H), fill=(18, 22, 27)); d.line((0, Y(0), W, Y(0)), fill=(80, 90, 100), width=3)
    if surge > 0:
        top = Y(115 * surge); d.polygon([(0, Y(0)), (0, top + 40), (380, top + 20), (640, top), (700, Y(0))], fill=(150, 165, 180, 255))
    x = 1300
    for ft in (0, 70, 110, 200, 289):
        d.line((x, Y(ft), x + 30, Y(ft)), fill=STEEL, width=3); d.text((x + 44, Y(ft)), f"{ft} FT", font=L.font(TYPE, 30), fill=STEEL, anchor="lm")
    d.line((x, Y(0), x, Y(289)), fill=STEEL, width=3)
    d.text((1080, Y(289) - 30), "TOP OF THE ISLAND", font=L.font(TYPE, 24), fill=STEEL, anchor="mm")
    lab = {"crane": (Y(70) + 30, "CRANE PLATFORM  ·  70 FT"), "box": (Y(110) - 8, "ROPE BOX  ·  110 FT"), "gone": (Y(110) + 46, "WASHED AWAY"),
           "buoy": (Y(110) - 66, "LIFE BUOY  ·  110 FT  ·  TORN OFF")}
    for name, key in a["marks"]:
        tm = t0 - 9 if key == -9 else AT(key)
        if t < tm: continue
        y, s = lab[name]
        if name == "crane":
            d.line((380, Y(70), 560, Y(70)), fill=RED, width=8); d.line((470, Y(70), 470, Y(70) - 60), fill=BONE, width=6); d.line((470, Y(70) - 60, 540, Y(70) - 40), fill=BONE, width=5)
        elif name == "box": d.rectangle((585, Y(110) - 22, 625, Y(110) + 4), outline=BONE, width=5)
        elif name == "gone":
            d.line((575, Y(110) - 30, 635, Y(110) + 12), fill=RED, width=8); d.line((575, Y(110) + 12, 635, Y(110) - 30), fill=RED, width=8)
        elif name == "buoy": d.ellipse((640, Y(110) - 70, 690, Y(110) - 20), outline=RED, width=8)
        d.line((700, y, 1240, y), fill=RED if name == "gone" else BONE, width=2)
        L.typewriter(c, s, t, tm, 720, y - 26, size=38, fill=RED if name in ("gone", "buoy") else BONE, cps=30, anchor="lm", cursor=False)
    L.typewriter(c, "DIAGRAM  ·  HEIGHTS FROM MUIRHEAD'S REPORT, 8 JANUARY 1901  ·  NOT TO SCALE", t, t0 + 0.2, W / 2, H - 50, size=26, fill=STEEL, cps=60, anchor="mm", cursor=False)
    return c

def chart_frame(a, t, t0, t1):
    src = tone(a["rid"], a["crop"]); s = max(W / src.width, H / src.height)
    im = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS); ox, oy = (im.width - W) / 2, (im.height - H) / 2
    c = L.vignette(im.crop((int(ox), int(oy), int(ox) + W, int(oy) + H)).convert("RGBA"), 0.35); d = ImageDraw.Draw(c)
    for fx, fy, label, key, side in a["pins"]:
        tm = AT(key)
        if t < tm: continue
        x, y = fx * im.width - ox, fy * im.height - oy; u = ease((t - tm) / 0.25); r = 13 * (1.6 - 0.6 * u)
        d.ellipse((x - r - 5, y - r - 5, x + r + 5, y + r + 5), fill=INK); d.ellipse((x - r, y - r, x + r, y + r), fill=RED)
        lx, ly, anc = {"up": (x, y - 70, "mm"), "right": (x + 40, y + 70, "lm"), "left": (x - 40, y + 70, "rm")}[side]
        f = L.font(TYPE, 36); w = f.getlength(label); bx = lx - (w / 2 if anc == "mm" else w if anc == "rm" else 0)
        d.rectangle((bx - 14, ly - 28, bx + w + 14, ly + 28), fill=INK)
        L.typewriter(c, label, t, tm + 0.1, lx, ly, size=36, fill=BONE, cps=30, anchor=anc, cursor=False)
    L.typewriter(c, a["foot"], t, t0 + 0.3, W / 2, H - 50, size=26, fill=STEEL, cps=60, anchor="mm", cursor=False)
    return c

def counter_frame(a, t, t0, t1):
    c = blur_bg(a["bg"], CROP.get(a["bg"])).copy(); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 120)))
    cur = None
    for key, s in a["steps"]:
        if t >= AT(key) - 0.05: cur = (s, AT(key))
    if cur:
        s, tm = cur; u = ease((t - tm) / 0.25); f = L.font(COND, int(420 * (1.15 - 0.15 * u)))
        ImageDraw.Draw(c).text((W / 2, H / 2 - 60), s, font=f, fill=(RED if a["red"] else BONE), anchor="mm")
    L.typewriter(c, a["sub"], t, t0 + 0.2, W / 2, H / 2 + 230, size=52, fill=STEEL, cps=30, anchor="mm", cursor=False)
    return c

def tcard_frame(a, t, t0, t1):
    bg = a["bg"]; crop = CROP.get(bg)
    c = blur_bg(bg, crop).copy(); card = pcard_h(bg, crop, 560, 3)
    c.alpha_composite(card, (int(W * 0.72 - card.width / 2), int(H / 2 - card.height / 2)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip(1.25 - np.linspace(0, 1, W) * 1.9, 0, 1)[None, :] * 235
    lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
    big = a["big"]; size = 140 if len(big) < 11 else 104
    L.typewriter(c, big, t, t0 + 0.05, 110, H / 2 - 60, size=size, cps=12, anchor="lm", cursor=False)
    L.text(c, a["sub"], 115, H / 2 + 60, 50, BONE, SER, anchor="lm", alpha=ease((t - t0 - 0.9) / 0.4))
    L.rule(c, 115, 760, H / 2 + 110, t, t0 + 1.1)
    return c

# ------------------------------------------------------------------ the cold open: the three keepers, then they vanish
# c.1900 group photo (NRS blog), 900x575: three keepers in caps, Superintendent Muirhead (bowler hat) on the right.
# Polygons are hand-traced in the photo's own pixels; the "erased" plate is a plain numpy diffusion fill (no AI).
KEEPERS = [
 [(215, 66), (268, 66), (266, 95), (262, 135), (300, 146), (320, 165), (330, 352), (302, 358), (297, 546), (255, 550), (242, 335), (230, 550),
  (198, 550), (194, 356), (154, 352), (155, 170), (176, 148), (220, 137), (217, 95)],
 [(372, 106), (431, 106), (427, 132), (421, 170), (456, 181), (471, 200), (478, 380), (450, 384), (449, 546), (414, 551), (407, 372), (398, 372),
  (395, 549), (361, 549), (362, 384), (329, 380), (332, 200), (349, 181), (384, 170), (377, 132)],
 [(539, 104), (594, 104), (591, 130), (585, 170), (626, 180), (646, 200), (651, 357), (616, 362), (613, 546), (585, 549), (566, 380), (555, 380),
  (546, 549), (509, 546), (514, 362), (487, 357), (491, 200), (509, 180), (552, 170), (546, 130)],
]
VAN = {}
def vanish_assets():
    if VAN: return VAN
    base = tone("H1"); a = np.asarray(base, np.float32); h, w = a.shape[:2]; masks = []
    for poly in KEEPERS:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
        masks.append(np.asarray(m.filter(ImageFilter.MaxFilter(9)), np.float32) / 255)
    cache = B + "_erased_H1.png"
    if os.path.exists(cache): er = np.asarray(Image.open(cache).convert("RGB"), np.float32)
    else:
        hole = np.clip(sum(masks), 0, 1) > 0.5; er = a.copy(); er[hole] = a[~hole].mean(0)
        for k in range(1500):                                   # Laplace fill: each hole pixel -> mean of its 4 neighbours
            n = (np.roll(er, 1, 0) + np.roll(er, -1, 0) + np.roll(er, 1, 1) + np.roll(er, -1, 1)) / 4; er[hole] = n[hole]
        er[hole] += np.random.default_rng(3).normal(0, 6, (int(hole.sum()), 1))      # film grain so the gap isn't a flat smear
        Image.fromarray(er.clip(0, 255).astype(np.uint8)).save(cache)
    soft = [np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)), np.float32)[..., None] / 255 for m in masks]
    VAN.update(base=a, er=er, masks=soft); return VAN

def vanish_frame(a, t, t0, t1):
    v = vanish_assets(); comp = v["base"].copy(); tm, tg = AT(a["mark"]), AT(a["gone"])
    for i, m in enumerate(v["masks"]):
        g = tg + i * 0.22; u = t - g
        if u < 0: k = 0.0
        elif u < 0.36: k = (0.85 if int(u / 0.06) % 2 else 0.15) * ease(u / 0.36) + 0.1   # flicker like a failing lamp
        else: k = 1.0
        if k > 0: comp = comp * (1 - m * k) + v["er"] * (m * k)
    im = Image.fromarray(comp.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for i, poly in enumerate(KEEPERS):                         # red dashed outline: on "three" around each man, kept after he is gone
        if t < tm + i * 0.14: continue
        pts = poly + [poly[0]]
        for j in range(len(pts) - 1):
            (xa, ya), (xb, yb) = pts[j], pts[j + 1]; L_ = math.dist(pts[j], pts[j + 1]); n = max(1, int(L_ / 9))
            for q in range(0, n, 2):
                d.line([(xa + (xb - xa) * q / n, ya + (yb - ya) * q / n), (xa + (xb - xa) * min(q + 1, n) / n, ya + (yb - ya) * min(q + 1, n) / n)],
                       fill=RED, width=3)
    z0, z1, c0, c1 = 1.0, 1.08, (0.45, 0.45), (0.42, 0.42)
    c = L.vignette(L.kenburns(im, t, t0, t1, z0, z1, c0, c1), 0.4)
    u = clamp01((t - t0) / max(t1 - t0, 1e-6)); z = z0 + (z1 - z0) * u; cx = c0[0] + (c1[0] - c0[0]) * u; cy = c0[1] + (c1[1] - c0[1]) * u
    s = max(W / im.width, H / im.height) * z; ww, hh = W / s, H / s
    x0 = min(max(cx * im.width - ww / 2, 0), im.width - ww); y0 = min(max(cy * im.height - hh / 2, 0), im.height - hh)
    for i, poly in enumerate(KEEPERS):                         # "GONE" over each empty space, at head height
        g = tg + i * 0.22 + 0.4
        if t < g: continue
        hx = (poly[0][0] + poly[1][0]) / 2; hy = poly[0][1] + 60
        X, Y = (hx - x0) * s, (hy - y0) * s; f = L.font(COND, 64); wd = f.getlength("GONE")
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((X - wd / 2 - 14, Y - 40, X + wd / 2 + 14, Y + 40), fill=RED + (int(235 * ease((t - g) / 0.2)),))
        c.alpha_composite(lay); L.text(c, "GONE", X, Y, 64, BONE, COND, alpha=ease((t - g) / 0.2))
    if t >= tm:
        L.typewriter(c, "3 KEEPERS", t, tm, W / 2, 70, size=74, fill=BONE, cps=18, anchor="mm", cursor=False)
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
        src = tone(a["rid"], a["crop"]); c = L.vignette(L.kenburns(src, t, t0, t1, a["z"][0], a["z"][1], a["c0"], a["c1"])); tag(c, a.get("tag"))
    elif kind == "kbp":
        c = blur_bg(a["rid"], a["crop"]).copy(); u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6)))
        card = pcard_h(a["rid"], a["crop"], a["h"], a["rot"]); k2 = 1.0 + 0.05 * u
        card = card.resize((int(card.width * k2), int(card.height * k2)), Image.BICUBIC)
        L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag"))
    elif kind == "tcard": c = tcard_frame(a, t, t0, t1)
    elif kind == "vanish": c = vanish_frame(a, t, t0, t1)
    elif kind == "card":
        c = ambient(k); big = a["big"]
        L.typewriter(c, big, t, t0 + 0.05, W / 2, H / 2 - 50, size=200 if len(big) < 10 else 140, cps=12, anchor="mm", cursor=False)
        t2 = t0 + 0.05 + len(big) / 12
        L.text(c, a["sub"], W / 2, H / 2 + 120, 58, STEEL, SER, alpha=ease((t - t2) / 0.4)); L.rule(c, W / 2 - 280, W / 2 + 280, H / 2 + 185, t, t2 + 0.15)
    elif kind == "nmap": c = MS.map_panel(a, t, t0, t1)
    elif kind == "chart": c = chart_frame(a, t, t0, t1)
    elif kind == "cliff": c = cliff_frame(a, t, t0, t1)
    elif kind == "counter": c = counter_frame(a, t, t0, t1)
    elif kind == "prints":
        c = ambient(k)
        for rid, crop, w, x, y, rot, d, label in a["items"]:
            L.drop(c, pcard(rid, crop, w, rot), x, y, t, t0 + d)
            if label: L.typewriter(c, label, t, t0 + d + 0.35, x, y + pcard(rid, crop, w, rot).height / 2 + 30, size=32, cps=30, anchor="mm", cursor=False)
    elif kind == "letter":
        c = ambient(k); rows, foot = LETTERS[a["key"]]; hand_paper(c, t, rows, foot, t0 + 0.4)
    elif kind == "typed":
        c = ambient(k); rows, foot = TYPES[a["key"]]; typed_paper(c, t, rows, foot, t0 + 0.4)
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 120, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 230, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 320, t, t0, width=7)
        L.typewriter(c, "NEXT FILE:  D.B. COOPER", t, T[128] + 0.2, W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
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
        i = int(t * sr)
        if i < 0: a = a[-i:]; i = 0                                             # effects timed just before frame 1
        a = a[: max(0, N - i)] * 10 ** (db / 20)
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
    music("Rising Tide.mp3", 0.0, tl(17), -26); music("Man Down.mp3", tl(17), tl(42), -25); music("Thunder Dreams.mp3", tl(42), tl(61), -24)
    music("Rising Tide.mp3", tl(61), tl(90), -26); music("Industrial Cinematic.mp3", tl(90), tl(111), -27); music("Man Down.mp3", tl(111), tl(121), -26)
    music("Thunder Dreams.mp3", tl(121), DUR, -23)
    loop("waves_windy_sea_loop", 0, tl(8), -24); loop("wind_cold_interior", tl(8), tl(13), -30); loop("waves_rough_sea_loop", tl(36), tl(42), -28)
    loop("wind_scary", tl(45), tl(50), -28); loop("wind_ambience", tl(53), tl(61), -30); loop("waves_rocky_shore", tl(79), tl(90), -32)
    HITS = [("hit_deep_heartbeat_impact", -17), ("hit_short_bass", -19), ("hit_glass_suspense", -21), ("hit_cinematic_deep_impact", -20)]
    for i, (key, (kind, a)) in enumerate(SHOTS):
        t0 = SHOT_T[i]
        if kind in ("card", "tcard"):
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "kbp": sfx("paper_slide", t0, -19); sfx("camera_vintage_shutter", t0 + 0.12, -25)
        elif kind in ("nmap", "chart", "cliff"): sfx("paper_page_turn", t0, -22)
        elif kind == "prints":
            for it in a["items"]: sfx("paper_slide", t0 + it[6], -19); sfx("camera_vintage_shutter", t0 + it[6] + 0.1, -25)
        elif kind == "letter":
            sfx("paper_slide", t0, -18)
            for s, k2 in LETTERS[a["key"]][0]:
                if AT(k2) > t0: sfx("paper_writing_pencil", AT(k2), -22, maxlen=1.2)
        elif kind == "typed":
            sfx("paper_slide", t0, -18)
            for s, k2 in TYPES[a["key"]][0]: sfx("typewriter_typing_old", AT(k2), -24, maxlen=1.0)
        elif kind == "counter":
            for k2, s in a["steps"]: sfx("hit_short_bass", AT(k2), -18, maxlen=1.2); sfx("clock_tick_single", AT(k2), -16)
        elif kind == "kb": sfx("whoosh_fast_transition", t0 - 0.1, -32)
        if kind == "nmap":
            for op in a["ops"]:
                if op[0] == "pin" and op[4] >= 0: sfx("camera_classic_click", t0 + op[4], -22)
        if kind == "chart":
            for p in a["pins"]: sfx("camera_classic_click", AT(p[3]), -22)
        if kind == "cliff":
            for n, (name, k2) in enumerate(a["marks"]):
                if k2 != -9: h = HITS[n % len(HITS)]; sfx(h[0], AT(k2), h[1], maxlen=1.8)
    for j, (ln, off, kind, a) in enumerate(OV):
        if kind == "stamp": sfx("hit_horror_drum", OVT[j], -14)
        if kind in ("typecenter", "typecenter_red", "list"): sfx("typewriter_typing_old", OVT[j], -26)
        if kind == "nameplate": sfx("typewriter_typing_old", OVT[j], -24, maxlen=1.2)
        if kind == "brand": sfx("hit_cinematic_deep_impact", OVT[j], -16)
        if kind == "subpop": sfx("whoosh_fast_transition", OVT[j], -24)
    sfx("hit_cinematic_deep_impact", 0.0, -12)                                   # the cold open starts on a hit
    for i in range(3):                                                           # the three keepers: marked, then gone
        sfx("camera_classic_click", AT((0, "three")) + i * 0.14, -20); sfx("whoosh_ghostly", AT((0, "gone")) + i * 0.22, -20, maxlen=1.2)
    sfx("hit_deep_heartbeat_impact", AT((0, "gone")) + 0.4, -15, maxlen=2.0)
    EV = [(0, 0.0, "thunder_deep_rumble", -20), (5, "steam", "siren_vintage_manual", -28), (5, "siren", "siren_manual_fire_alert", -30),
          (6, "rocket", "riser_cinematic_trailer", -26), (6, "nothing", "hit_deep_heartbeat_impact", -18), (7, "jumps", "water_splash", -24),
          (8, "gate", "heavy_sliding_door", -26), (9, "clock", "clock_tick_single", -14), (10, "empty", "heartbeat_single", -20),
          (12, 0.0, "hit_cinematic_deep_impact", -14), (12, 0.1, "footsteps_stones_loop", -26), (22, "chalk", "paper_writing_pencil", -22),
          (39, "shirt", "wind_scary", -24), (42, 0.0, "clock_bells_hour", -26), (44, 0.0, "hit_cinematic_deep_impact", -14), (45, 0.0, "clock_old_big_hour", -22),
          (46, "stormy", "thunder_deep_rumble", -22), (47, "can", "heartbeat_single", -20), (56, "gale", "wind_scary", -22), (56, "wrecks", "thunder_deep_rumble", -20),
          (58, "sails", "ship_hull_creak", -24), (60, 0.0, "heartbeat_slow", -20), (62, "shouts", "footsteps_stones_loop", -28), (69, "night", "wind_ambience", -28),
          (71, "lights", "hit_glass_suspense", -22), (80, "gone", "sea_water_splash", -18), (81, "twisted", "metal_tool_falling", -24),
          (86, "tore", "sea_water_splash", -20), (87, 0.0, "hit_big_cinematic_impact", -18), (88, 0.1, "waves_rocky_shore", -26), (92, "hands", "heartbeat_single", -22),
          (95, "acted", "hit_horror_drum", -18), (98, "swept", "sea_water_splash", -18), (104, "second", "jump_in_water", -20), (113, "breakfast", "paper_big_page_turn", -22),
          (116, 0.2, "newspaper_drop", -20), (121, 0.2, "light_switch", -26), (126, "sea", "waves_rocky_shore", -26), (128, 0.2, "typewriter_return_bell", -18)]
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
def final(n, name="TheLastHours_05_Flannan.mp4"):
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
    elif m == "keys":                                                            # word keys whisper did not hear (they fall back to line start + 0.3 s)
        keys = [s[0] for s in SHOTS] + [(ln, off) for ln, off, _, _ in OV] + [k for rows, _ in list(LETTERS.values()) + list(TYPES.values()) for _, k in rows]
        for s in SHOTS:
            if s[1][0] == "counter": keys += [k for k, _ in s[1][1]["steps"]]
            if s[1][0] == "chart": keys += [p[3] for p in s[1][1]["pins"]]
            if s[1][0] == "cliff": keys += [k for _, k in s[1][1]["marks"] if k != -9]
        for k in keys:
            if isinstance(k, tuple) and isinstance(k[1], str) and wt(k[0], k[1]) is None: print("MISSING", k, "|", LINES[k[0]][:80])
        gaps = [(SHOT_T[i + 1] - SHOT_T[i], i) for i in range(len(SHOTS) - 1)]
        print("shots", len(SHOTS), "longest", sorted(gaps)[-6:], "shortest", sorted(gaps)[:4])
    elif m == "chapters":
        CH = [(0, "Dec 26, 1900: nobody answers"), (17, "Dec 15, 9 AM: the last note"), (31, "Afternoon: the coat on the peg"),
              (42, "3:39 PM: the lamp stays dark"), (50, "Eleven dark nights"), (61, "Boxing Day: the second search"), (73, "The telegram"),
              (77, "The west side: 110 feet up"), (90, "The handshake and the report"), (101, "Why all three?"), (111, "How the fake log was made"),
              (121, "What's left in 2026")]
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
        low = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0)
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), "seg", str(i), str(n)], env=env, creationflags=low) for i in range(n)]
        for p in ps: p.wait()
        audio(); final(n)
    elif m == "prep": prep()
