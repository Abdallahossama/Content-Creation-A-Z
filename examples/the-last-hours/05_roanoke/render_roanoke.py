"""The Last Hours #4: Roanoke, John White's return, 15-19 Aug 1590 (Case File style, 1920x1080). Built on render_cooper.py.
Every shot starts on a narration line (index into vo_lines.txt without '##'), or on a spoken word in it: key (line, "word").
Line timing comes from the exact-zero gaps in the VO, word timing from whisper (vo/vo_words.json).
Hakluyt (1600) page boxes come from build/lines_<rid>.json (build/lines.py: printed-line detection), picked by line number.
  uv run --no-project --with pillow --with numpy --with soundfile python render_roanoke.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines (they cut across the sounds at this scale)
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/05_roanoke/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
HAND = "C:/Windows/Fonts/segoeprb.ttf"                 # hand-printed look for the reconstruction cards
ROMAN = "C:/Windows/Fonts/timesbd.ttf"                 # Roman capitals for the carved-letter reconstructions
LEAD = 0.8; TAIL = 20.0

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = ROOT + "vo/roanoke_vo_chatterbox.wav"
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
IMG = {}
def tone(rid, crop=None, rot=0):
    k = (rid, crop, rot)
    if k not in IMG: IMG[k] = L.bw(P(rid), crop)
    return IMG[k]

# Hakluyt 1600 pages: boxes by printed line number (build/lines_<rid>.json) and the text column of each page
COLX = {"A6": (190, 2350), "A7": (190, 2340), "A9": (1090, 3260), "A10": (170, 2420), "A11": (1070, 3430), "A12": (200, 2420)}
_LN = {}
def LB(rid, k0, k1=None, x0=None, x1=None):
    if rid not in _LN: _LN[rid] = json.load(open(B + f"lines_{rid}.json"))
    r = _LN[rid]; k1 = k0 if k1 is None else k1; a, b = COLX[rid]
    return (x0 or a, r[k0][0] - 8, x1 or b, r[k1][1] + 8)
PH = {
 "A11": {"ten": LB("A11", 16), "gale": LB("A11", 22, 23), "spicer": LB("A11", 30, 31), "eleven": LB("A11", 34), "mind": LB("A11", 36, 37),
         "dark": LB("A11", 40, 42), "fire": LB("A11", 42, 43), "trumpet": LB("A11", 44, 45), "noanswer": LB("A11", 45, 45, 2470, 3200),
         "daybreak": LB("A11", 46), "prints": LB("A11", 50), "cro": LB("A11", 52, 52, 1740, 1945), "token": LB("A11", 53, 55), "fifty": LB("A11", 56),
         "cross": LB("A11", 57, 59)},
 "A12": {"houses": LB("A12", 3, 4), "post": LB("A12", 5), "croatoan": LB("A12", 6, 6, 1650, 2105), "nocross": LB("A12", 6, 7), "iron": LB("A12", 7, 9),
         "boats": LB("A12", 10, 12), "chests": LB("A12", 13, 14), "five": LB("A12", 16, 18), "books": LB("A12", 19, 21), "enemies": LB("A12", 21, 22),
         "joy": LB("A12", 24, 26), "storm": LB("A12", 28, 29), "evening": LB("A12", 30), "casks": LB("A12", 34, 35), "wind": LB("A12", 37, 39),
         "cable": LB("A12", 40, 43), "four": LB("A12", 47, 48), "water": LB("A12", 48, 49), "winter": LB("A12", 50, 53), "parted": LB("A12", 57, 58)},
 "A10": {"croatoan": LB("A10", 42, 43), "evening": LB("A10", 44), "smoke": LB("A10", 45, 47), "guns": LB("A10", 50, 52)},
 "A9": {"boy": LB("A9", 19, 21), "spoiles": LB("A9", 27, 28), "last": LB("A9", 36), "leave": LB("A9", 40, 41), "almighty": LB("A9", 41, 42),
        "house": LB("A9", 44), "fift": LB("A9", 45, 46)},
 "A7": {"birth": LB("A7", 3, 5), "voice": LB("A7", 20, 22), "fifty": LB("A7", 29, 30)},
 "A6": {"howe": LB("A6", 13, 14), "corne": LB("A6", 25, 26), "croatoan": LB("A6", 17, 18)},
}
FULL = {rid: (COLX[rid][0], LB(rid, 1)[1], COLX[rid][1], LB(rid, len(_LN[rid]) - 2)[3]) for rid in COLX}
FULL["A8"] = (200, 380, 2420, 4650)
def page_img(rid):
    k = ("doc", rid)
    if k not in IMG:
        im = Image.open(P(rid)).convert("L"); a = np.asarray(im, np.float32); lo, hi = np.percentile(a, 8), np.percentile(a, 99.5)
        a = np.clip((a - lo) / max(hi - lo, 1), 0, 1) ** 1.25; IMG[k] = Image.fromarray((a[..., None] * np.array([236, 230, 214], np.float32)).astype(np.uint8))
    return IMG[k]

def prep():
    for f in glob.glob(M + "*"):
        rid = os.path.basename(f).split("_")[0]
        if os.path.exists(B + f"_small_{rid}.png"): continue
        try: im = Image.open(f)
        except Exception: continue
        if max(im.size) > 4200 and rid not in COLX:
            im = im.convert("RGB"); k = 4200 / max(im.size); im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS).save(B + f"_small_{rid}.png")

# map points (lon, lat)
FORT, DASA, CROA, SITEX, CHES, JAMES = (-75.710, 35.9386), (-75.7628, 35.8858), (-75.5425, 35.2678), (-76.7725, 36.0119), (-76.0201, 36.9248), (-76.7775, 37.2092)
HATO, ANCH, SMOKE2, CROA_NE = (-75.5633, 35.8185), (-75.40, 35.845), (-75.635, 35.905), (-75.47, 35.45)
PLYM, DOMIN, AZOR = (-4.1422, 50.3714), (-61.37, 15.41), (-31.1, 39.45)
OUT1590 = [PLYM, (-9.5, 44), (-14, 31), (-16, 28), (-40, 20), DOMIN, (-67, 18.2), (-74.4, 18.6), (-80.5, 22.3), (-80, 26), (-78, 31), ANCH]
HOME1590 = [ANCH, (-73, 33), (-62, 36), (-45, 38.5), AZOR, (-20, 44), (-8, 48), PLYM]
V_COAST, V_ISLAND, V_SEA, V_ATL, V_VA = (-75.95, 35.95, 4.8), (-75.68, 35.88, 0.6), (-75.56, 35.87, 0.85), (-42.0, 33.0, 92.0), (-76.25, 36.4, 4.6)

# ------------------------------------------------------------------ shot constructors
CROP = {"A1": (0.0, 0.0, 0.9, 0.97), "A3": (0.01, 0.01, 0.99, 0.94), "A4": (0.02, 0.08, 0.98, 0.9), "B6": (0.07, 0.0, 0.92, 0.98),
        "B7": (0.06, 0.0, 0.93, 0.98), "B8": (0.06, 0.0, 0.93, 0.98), "B9": (0.04, 0.0, 0.94, 0.98), "B10": (0.0, 0.31, 0.93, 0.555),
        "E6": (0.0, 0.0, 1.0, 0.5)}                     # museum colour-chart strips; the heart-shaped groove in the bark photo
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, rot=0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, rot=rot))
def KBP(rid, crop=None, h=820, rot=-1.5): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot))
def CARD(big, sub): return ("card", dict(big=big, sub=sub))
def DOC(rid, focus=None, z=(0.95, 1.08), marks=()): return ("doc", dict(rid=rid, focus=focus or FULL[rid], z=z, marks=marks))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def CARVE(word, key=None, ghost_cross=None): return ("carve", dict(word=word, key=key, ghost=ghost_cross))
def LETTER(key): return ("letter", dict(key=key))
def BLACK(): return ("black", {})
def pr(rid, x, label=None, d=0.1, w=430, rot=-2, y=None): return (rid, None, w, x, (y or H / 2 - 40), rot, d, label)
def PRINTS(items): return ("prints", dict(items=items))
def F(rid, k, pad=60):                                 # a doc focus box around a named quote box
    b = PH[rid][k]; return (b[0] - pad, b[1] - 3 * pad, b[2] + pad, b[3] + 3 * pad)

SHOTS = [
 (0, KB("A14", z=(1.04, 1.22), c0=(0.42, 0.45), c1=(0.36, 0.4))),          # hero image from frame 1
 (1, CARVE("CROATOAN", key=(1, "one"))),
 (2, ("coldopen", {})),
 (3, KB("F4", z=(1.0, 1.15))),
 ((3, "nineteen"), KB("D8", z=(1.02, 1.12))),
 (4, KB("C6", z=(1.0, 1.12))),
 (5, KB("E12", z=(1.05, 1.2))),
 ((5, "fire"), KB("E7", z=(1.0, 1.12), c0=(0.5, 0.6))),
 (6, DOC("A11", F("A11", "trumpet"), z=(1.0, 1.08), marks=[("trumpet", 6, "john", 0.2), ("noanswer", 6, "but", 2.0)])),
 (7, KB("A4", z=(1.0, 1.1))),
 (8, KB("A14", z=(1.0, 1.15), c0=(0.55, 0.5))),
 (9, DOC("A12", F("A12", "croatoan", 40), z=(0.9, 1.0), marks=[("croatoan", 9, "what", 0.3)])),
 (10, ("title", {})),
 (11, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE ISLAND", 0.4)])),
 (12, DOC("A8", None, z=(0.95, 1.05))),
 (13, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE ISLAND", -9), ("pin", *CHES, "THE PLAN: CHESAPEAKE BAY", 0.6), ("arrow", FORT, CHES, "", 1.0)], c0=(0.5, 0.45))),
 (14, KB("D10", z=(1.02, 1.12))),
 (15, KBP("B7", h=880)),
 (16, NMAP(V_ISLAND, ops=[("pin", *FORT, "THE COLONY", 0.2), ("pin", *DASA, "ROANOKE TOWN (MAINLAND)", 0.8)])),
 (17, DOC("A6", F("A6", "howe"), z=(1.0, 1.08), marks=[("howe", 17, "george", 0.5)])),
 (18, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE", -9), ("route", [FORT, (-75.62, 35.75), (-75.52, 35.5), CROA], 0.3, 1.6), ("pin", *CROA, "CROATOAN", 1.8)])),
 (19, KB("B10", z=(1.0, 1.12))),
 (20, DOC("A7", F("A7", "birth"), z=(1.0, 1.08), marks=[("birth", 20, "eleanor", 0.6)])),
 (21, KBP("B9", h=880, rot=1.2)),
 (22, DOC("A7", F("A7", "voice"), z=(1.0, 1.08), marks=[("voice", 22, "voice", 1.5)])),
 (23, BLACK()),
 (24, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE", 0.0), ("circle", *FORT, 50, "50 MILES", 1.2)])),
 (25, LETTER("code")),
 (27, CARD("AUG 27, 1587", "John White sails for England")),
 (28, KB("C4", z=(1.02, 1.12))),
 (29, KB("C2", z=(1.0, 1.1))),
 (30, KB("C3", z=(1.0, 1.12))),
 (31, KB("C1", z=(1.0, 1.1))),
 (32, DOC("A9", F("A9", "boy"), z=(1.0, 1.08), marks=[("boy", 32, "boy", 0.8)])),
 (33, NMAP(V_ATL, ops=[("pin", *PLYM, "PLYMOUTH", 0.1), ("route", OUT1590, 0.4, 4.5), ("pin", *ANCH, "ROANOKE", 4.6)])),
 (34, NMAP(V_COAST, ops=[("pin", *CROA_NE, "AUG 12: OFF CROATOAN", 0.4)], c0=(0.5, 0.55))),
 (35, CARD("TOWARD EVENING", "Saturday, August 15, 1590")),
 (36, NMAP(V_SEA, ops=[("pin", *ANCH, "THE SHIPS", 0.3, -260, 0), ("pin", *FORT, "ROANOKE ISLAND", 1.8)])),
 (37, DOC("A10", F("A10", "smoke"), z=(1.0, 1.08), marks=[("smoke", 37, "great", 0.4)])),
 (38, KB("E3", z=(1.02, 1.12))),
 (39, KB("C1", z=(1.2, 1.32), c0=(0.45, 0.6))),
 ((39, "colonists"), DOC("A10", F("A10", "guns"), z=(1.0, 1.06), marks=[("guns", 39, "colonists", 0.0)])),
 (40, NMAP(V_SEA, ops=[("pin", *ANCH, "", -9), ("route", [ANCH, (-75.52, 35.88), (-75.60, 35.90)], 0.2, 1.4), ("pin", *SMOKE2, "THE SECOND SMOKE", 2.0, -300, 0)])),
 (41, KB("D7", z=(1.0, 1.1))),
 (42, KB("C4", z=(1.15, 1.25), c0=(0.6, 0.5))),
 (43, CARD("10:00 AM", "Monday, August 17, 1590")),
 (44, NMAP(V_SEA, ops=[("pin", *ANCH, "", -9), ("route", [ANCH, (-75.5, 35.83), HATO], 0.3, 1.6), ("label", -75.42, 35.97, "NORTHEAST GALE", 1.0, 30)])),
 (45, KB("E1", z=(1.1, 1.22), c0=(0.45, 0.5))),
 (46, KB("C6", z=(1.1, 1.25), c0=(0.55, 0.55))),
 (47, KB("C5", z=(1.0, 1.12))),
 (48, DOC("A11", F("A11", "spicer"), z=(1.0, 1.08), marks=[("spicer", 48, "hung", 0.8)])),
 (49, CARD("7 OF 11", "Drowned at the inlet")),
 (50, KB("C3", z=(1.15, 1.28), c0=(0.4, 0.5))),
 (51, DOC("A11", F("A11", "mind"), z=(1.0, 1.08), marks=[("mind", 51, "mind|one", 1.0)])),
 (52, KB("C4", z=(1.0, 1.08), c0=(0.3, 0.5))),
 (53, CARD("AFTER DARK", "19 men, 2 boats")),
 (54, NMAP(V_ISLAND, ops=[("route", [(-75.62, 35.92), (-75.665, 35.955), (-75.705, 35.958)], 0.3, 2.5), ("pin", *FORT, "THE SETTLEMENT", 2.6)], c0=(0.5, 0.45))),
 (55, KB("E7", z=(1.05, 1.18), c0=(0.5, 0.55))),
 (56, KB("C7", z=(1.0, 1.12))),
 (57, BLACK()),
 (58, KB("E3", z=(1.0, 1.1), c0=(0.5, 0.45))),
 (59, ("cta", {})),
 (63, CARD("DAYBREAK", "Tuesday, August 18, 1590")),
 (64, CARD("AUG 18", "Virginia Dare turns three")),
 (65, KB("E4", z=(1.02, 1.12))),
 (66, KB("D8", z=(1.1, 1.25), c0=(0.5, 0.65))),
 (67, KB("E2", z=(1.0, 1.12))),
 (68, CARVE("C R O", key=(68, "c"))),
 (69, DOC("A11", F("A11", "cro", 40), z=(0.95, 1.05), marks=[("cro", 69, "white", 0.2), ("token", 69, "code", 1.5)])),
 (70, KB("D1", z=(1.0, 1.1))),
 (71, DOC("A12", F("A12", "houses"), z=(1.0, 1.08), marks=[("houses", 71, "palisade", 0.4)])),
 (72, KB("A14", z=(1.1, 1.25), c0=(0.55, 0.45))),
 (73, CARVE("CROATOAN", key=(73, "croatoan|cro"))),
 (74, CARVE("CROATOAN", ghost_cross=(74, "cross"))),
 (75, BLACK()),
 (76, DOC("A12", F("A12", "iron"), z=(1.0, 1.08), marks=[("iron", 76, "bars", 0.3)])),
 (77, BLACK()),
 (78, KB("E11", z=(1.0, 1.12))),
 (79, KB("E9", z=(1.0, 1.1))),
 ((79, "armor"), KB("E10", z=(1.0, 1.12))),
 (80, NMAP(V_ISLAND, ops=[("pin", *FORT, "THE COLONY", -9), ("pin", *DASA, "ROANOKE TOWN (MAINLAND)", 0.4)])),
 (81, DOC("A12", F("A12", "joy"), z=(1.0, 1.08), marks=[("joy", 81, "overjoyed|over", 0.6)])),
 (82, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE", -9), ("route", [FORT, (-75.62, 35.75), (-75.52, 35.5), CROA], 0.6, 2.0), ("pin", *CROA, "CROATOAN · ~50 MILES", 2.4)])),
 (83, KB("C1", z=(1.05, 1.15), c0=(0.5, 0.5))),
 (84, KB("C5", z=(1.08, 1.2), c0=(0.5, 0.35))),
 (85, DOC("A12", F("A12", "evening"), z=(1.0, 1.08), marks=[("evening", 85, "danger", 0.8)])),
 (86, KB("E3", z=(1.1, 1.2), c0=(0.6, 0.5))),
 (87, KB("C4", z=(1.25, 1.35), c0=(0.5, 0.4))),
 (88, CARD("MORNING", "Wednesday, August 19, 1590")),
 (89, KB("E8", z=(1.0, 1.12))),
 (90, KB("C3", z=(1.05, 1.18), c0=(0.55, 0.5))),
 (91, DOC("A12", F("A12", "four"), z=(1.0, 1.08), marks=[("four", 91, "one", 0.6)])),
 (92, BLACK()),
 (93, DOC("A12", F("A12", "winter"), z=(1.0, 1.06), marks=[("winter", 93, "winter", 1.2)])),
 (94, KB("C5", z=(1.2, 1.32), c0=(0.35, 0.5))),
 (95, NMAP(V_ATL, ops=[("route", HOME1590, 0.3, 4.0), ("pin", *AZOR, "THE AZORES", 2.4), ("pin", *PLYM, "PLYMOUTH", 4.1)])),
 (96, CARD("OCT 24, 1590", "Plymouth, England")),
 (97, KB("A1", z=(1.0, 1.12))),
 (98, DOC("A9", F("A9", "house"), z=(1.0, 1.08), marks=[("house", 98, "house", 0.5)])),
 (99, DOC("A9", F("A9", "almighty"), z=(1.0, 1.08), marks=[("leave", 99, "giving", 0.4), ("almighty", 99, "merciful", 0.0)])),
 (100, KB("A3", z=(1.0, 1.1))),
 (101, KB("E4", z=(1.1, 1.2), c0=(0.6, 0.5))),
 (102, NMAP(V_VA, ops=[("pin", *FORT, "ROANOKE", -9), ("pin", *JAMES, "JAMESTOWN · 1607", 0.6)], c0=(0.5, 0.45))),
 (103, KB("A16", z=(1.0, 1.12))),
 (104, BLACK()),
 (105, KB("D4", z=(1.0, 1.12))),
 (106, BLACK()),
 (107, KB("F6", z=(1.0, 1.12))),
 (108, BLACK()),
 (109, KB("D11", z=(1.0, 1.12))),
 (110, KB("E6", z=(1.05, 1.15))),
 (111, CARD("800 YEARS", "The worst drought, 1587-1589")),
 (112, DOC("A6", F("A6", "corne"), z=(1.0, 1.08), marks=[("corne", 112, "corn", 0.5)])),
 (113, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE", -9), ("pin", *CROA, "THEORY 1: CROATOAN", 0.6), ("pin", *SITEX, "THEORY 2: CHOWAN RIVER", 1.6)])),
 (114, KB("F7", z=(1.0, 1.1))),
 (115, BLACK()),
 (116, BLACK()),
 (117, NMAP(V_COAST, ops=[("pin", *FORT, "ROANOKE", -9), ("route", [FORT, (-76.0, 35.97), (-76.4, 36.0), SITEX], 0.5, 2.5), ("pin", *SITEX, "SITE X", 2.7)])),
 (118, KB("A2", z=(1.0, 1.15))),
 (119, KB("F5", z=(1.0, 1.1))),
 (120, CARD("2026", "Two teams. Two claims.")),
 (121, KB("D11", z=(1.1, 1.2), c0=(0.4, 0.5))),
 (122, KB("D7", z=(1.1, 1.2), c0=(0.6, 0.5))),
 (123, KB("D1", z=(1.1, 1.2), c0=(0.5, 0.45))),
 (124, BLACK()),
 (125, DOC("A12", F("A12", "houses"), z=(1.0, 1.06), marks=[("houses", 125, "gone", 0.8)])),
 (126, BLACK()),
 (127, CARVE("CROATOAN")),
 (128, KB("E3", z=(1.15, 1.25), c0=(0.4, 0.5))),
 (129, KB("E7", z=(1.1, 1.2), c0=(0.5, 0.5))),
 (130, CARVE("C R O")),
 (131, KB("E2", z=(1.08, 1.2), c0=(0.5, 0.5))),
 (132, KB("A14", z=(1.0, 1.1), c0=(0.5, 0.5))),
 (133, DOC("A12", F("A12", "croatoan", 40), z=(0.95, 1.05), marks=[("croatoan", 133, "four", 0.2)])),
 (134, ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "lower", "ROANOKE ISLAND  ·  AUGUST 1590"),
 (0, "three", "typecenter", "3 YEARS"),
 (0, "seven", "typecenter", "7 MEN LOST"),
 (3, 0.3, "lower", "ROANOKE ISLAND TODAY  \u00b7  USGS AERIAL"),
 (5, 0.3, "lower", "A TRUMPET OF THE PERIOD  \u00b7  THE MET"),
 (6, 0.2, "lower", "JOHN WHITE'S OWN ACCOUNT  \u00b7  PRINTED 1600"),
 (7, 0.3, "lower", "JOHN WHITE'S HANDWRITING  \u00b7  1585"),
 (8, 0.3, "lower", "\u201cCROATOAN\u201d  \u00b7  ENGRAVING, 1876 (IMAGINED SCENE)"),
 (12, 0.2, "lower", "THE 1587 NAMES LIST  \u00b7  HAKLUYT, 1600"),
 (12, "first", "under", "MEN, WOMEN AND CHILDREN"),
 (15, 0.3, "lower", "A ROANOKE CHIEF, PROBABLY WINGINA  \u00b7  JOHN WHITE, 1585"),
 (17, 0.2, "lower", "JULY 1587  \u00b7  HAKLUYT, 1600"),
 (19, 0.3, "lower", "CAROLINA ALGONQUIAN MEN FISHING  \u00b7  JOHN WHITE, 1585"),
 (19, "manteo", "under", "NO PORTRAIT OF MANTEO EXISTS"),
 (20, 0.2, "lower", "\u201cTHE 18. ELENOR... WAS DELIUERED OF A DAUGHTER\u201d  \u00b7  1587"),
 (21, 0.3, "lower", "PAINTED BY JOHN WHITE, 1585"),
 (22, 0.2, "lower", "22 AUGUST 1587  \u00b7  \u201cWITH ONE VOICE\u201d"),
 (23, 0.0, "quote", ("\u201cnot once, but often refusing it, for our sakes...\u201d", "THE COLONISTS' STATEMENT  \u00b7  25 AUGUST 1587")),
 (27, "granddaughter", "under", "HIS GRANDDAUGHTER IS NINE DAYS OLD"),
 (29, 0.3, "lower", "ENGLISH SHIPS AND THE SPANISH ARMADA, 1588"),
 (30, 0.3, "under", "1588: ROBBED AT SEA, TURNED BACK"),
 (31, 0.3, "lower", "THE ARK RALEIGH  \u00b7  ENGRAVING, c. 1588"),
 (32, 0.2, "lower", "\u201cNO NOT SO MUCH AS A BOY\u201d  \u00b7  WHITE, 1593"),
 (33, 0.6, "under", "MARCH TO AUGUST 1590  \u00b7  RAIDING FIRST"),
 (34, "no", "under", "HE HAD NO IDEA YET THAT IT MATTERED"),
 (36, 0.6, "under", "ABOUT 10 MILES OFFSHORE"),
 (37, 0.2, "lower", "\u201cWE SAW A GREAT SMOKE RISE IN THE ILE RAONOAK\u201d"),
 (38, 0.3, "under", "\u201cIN GOOD HOPE\u201d"),
 (39, 0.3, "under", "2 MINIONS AND A FALCON  \u00b7  SMALL CANNON"),
 (41, 0.3, "under", "NO PEOPLE  \u00b7  NO FRESH WATER"),
 (45, 0.3, "under", "THE SANDBAR AT THE INLET"),
 (48, 0.2, "lower", "\u201cHUNG VNTILL THEY SUNKE, & WERE SEENE NO MORE\u201d"),
 (50, 0.3, "under", "EDWARD SPICER  \u00b7  1587: BROUGHT THE SECOND SHIP"),
 (51, 0.2, "lower", "\u201cALL OF ONE MIND NOT TO GOE ANY FURTHER\u201d"),
 (52, 0.3, "under", "WHITE AND CAPTAIN COOKE"),
 (54, 0.4, "under", "THEY OVERSHOOT BY A QUARTER MILE"),
 (56, 0.3, "lower", "A SAILOR SOUNDING THE TRUMPET  \u00b7  ENGRAVING, 1600s"),
 (57, 0.0, "typecenter", "NO ANSWER"),
 (64, "white", "under", "WHITE NEVER MENTIONS IT"),
 (66, 0.4, "under", "FOOTPRINTS, MADE DURING THE NIGHT"),
 (69, 0.2, "lower", "\u201cTHESE FAIRE ROMANE LETTERS C R O\u201d"),
 (70, 0.3, "lower", "FORT RALEIGH TODAY  \u00b7  THE RECONSTRUCTED EARTHWORK"),
 (71, 0.2, "lower", "\u201cA HIGH PALISADO OF GREAT TREES... VERY FORT-LIKE\u201d"),
 (72, 0.3, "lower", "\u201cCROATOAN\u201d  \u00b7  ENGRAVING, 1876 (IMAGINED SCENE)"),
 (75, 0.0, "typecenter", "NO CROSS"),
 (76, 0.2, "lower", "\u201cMANY BARRES OF IRON, TWO PIGGES OF LEAD\u201d"),
 (77, 0.0, "list", ["THE BOATS: GONE", "THE SMALL CANNON: GONE"]),
 (78, 0.3, "lower", "A CHEST OF THE PERIOD  \u00b7  THE MET"),
 (79, "armor", "lower", "A BREASTPLATE OF THE PERIOD  \u00b7  THE MET"),
 (81, 0.2, "lower", "\u201cI GREATLY IOYED\u201d  \u00b7  WHITE, 1590"),
 (85, 0.2, "lower", "\u201cWITH MUCH DANGER AND LABOUR\u201d"),
 (86, 0.4, "under", "THE FULL WATER CASKS ARE LEFT ON THE BEACH"),
 (89, 0.4, "under", "THE CABLE SNAPS"),
 (90, 0.3, "under", "A LEE SHORE  \u00b7  PAINTING, VAN DE VELDE"),
 (91, 0.2, "lower", "\u201cBUT ONE CABLE AND ANCHOR LEFT VS OF FOURE\u201d"),
 (92, 0.0, "list", ["FOOD: SHORT", "FRESH WATER: LOST"]),
 (93, 0.2, "lower", "THE NEW PLAN  \u00b7  WINTER IN THE WEST INDIES"),
 (97, 0.3, "lower", "JOHN WHITE'S MAP OF THE COAST  \u00b7  1585-86"),
 (98, 0.2, "lower", "\u201cFROM MY HOUSE AT NEWTOWNE IN KYLMORE\u201d  \u00b7  1593"),
 (100, 0.3, "under", "JOHN WHITE  \u00b7  DIED: UNKNOWN"),
 (103, 0.3, "lower", "THE Z\u00daÑIGA MAP, 1608  \u00b7  REDRAWN 1908"),
 (104, 0.0, "quote", ("\u201c...miserably slaughtered...\u201d", "WILLIAM STRACHEY  \u00b7  c. 1612  \u00b7  HEARSAY")),
 (105, 0.3, "lower", "ALGONQUIAN COPPER ORNAMENTS  \u00b7  FORT RALEIGH (NPS)"),
 (106, 0.0, "typecenter", "HEARSAY"),
 (107, 0.3, "lower", "HATTERAS ISLAND, ONCE CROATOAN  \u00b7  NASA, 2019"),
 (108, 0.0, "quote", ("\u201c...could talk in a Book, as we do...\u201d", "JOHN LAWSON  \u00b7  1709")),
 (108, "gray", "stamp", ("GRAY EYES", 1450, 860)),
 (110, 0.3, "under", "TREE RINGS FROM ANCIENT BALD CYPRESS"),
 (112, 0.2, "lower", "THE CROATOANS, 1587: THEY \u201cHAD BUT LITTLE\u201d CORN"),
 (114, 0.3, "lower", "CAPE HATTERAS FROM APOLLO 9  \u00b7  1969"),
 (115, 0.0, "list", ["PART OF A SWORD HILT", "A SLATE", "GUN PARTS", "IRON-WORKING WASTE"]),
 (116, 0.0, "typecenter", "OR TRADE?"),
 (118, 0.3, "lower", "JOHN WHITE'S MAP, LIT FROM BEHIND  \u00b7  2012"),
 (119, 0.3, "lower", "THE CHOWAN RIVER AREA  \u00b7  USGS AERIAL"),
 (121, 0.2, "under", "\u201cTHE LOST COLONY IS FOUND!\u201d  \u00b7  FIRST COLONY FOUNDATION"),
 (122, 0.2, "under", "HATTERAS TEAM  \u00b7  CLAIM, JUNE 2026"),
 (123, "neither", "stamp", ("UNPROVEN", 1420, 820)),
 (124, 0.0, "typecenter", "WHAT THE RECORDS SAY"),
 (126, 0.0, "list", ["HOUSES TAKEN DOWN", "A WALL BUILT", "CHESTS BURIED", "BOATS TAKEN"]),
 (131, 0.4, "under", "VIRGINIA DARE  \u00b7  FATE UNKNOWN"),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

# ------------------------------------------------------------------ drawing helpers
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
 "code": ([("IF THEY MOVE,", (25, "if")), ("CARVE THE NAME OF THE PLACE", (25, "carve")), ("IF IN DANGER,", (26, "danger")),
           ("CARVE A CROSS ABOVE IT", (26, "cross"))],
          "THE AGREED SIGN  \u00b7  FROM JOHN WHITE'S OWN ACCOUNT, 1590"),
}

def carve_frame(a, t, t0, t1):
    """reconstruction: letters cut into a peeled post (real bark texture photo; our own lettering, labelled)"""
    c = L.vignette(L.kenburns(tone("E6", CROP["E6"]), t, t0, t1, 1.05, 1.12), 0.55)
    c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    word = a["word"]; size = 210 if len(word) > 5 else 260; f = L.font(ROMAN, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tw = f.getlength(word); x0 = (W - tw) / 2; y = H / 2 + 10
    d.rounded_rectangle((x0 - 70, y - size * 0.75, x0 + tw + 70, y + size * 0.62), 26, fill=(214, 200, 172, 120))   # bark taken off
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
    start = AT(a["key"]) if a["key"] else t0 + 0.15; d = ImageDraw.Draw(c); x = x0
    for i, ch in enumerate(word):
        if t >= start + i * 0.09 and ch != " ":
            d.text((x + 4, y + 4), ch, font=f, fill=(226, 214, 188, 200), anchor="ls")          # lit lower edge
            d.text((x, y), ch, font=f, fill=(26, 22, 18, 255), anchor="ls")                    # cut
        x += f.getlength(ch)
    if a["ghost"] and t >= AT(a["ghost"]):
        u = ease((t - AT(a["ghost"])) / 0.5); cx, cy, r = W / 2, y - size - 60, 70
        for (xa, ya, xb, yb) in ((cx, cy - r, cx, cy + r), (cx - r, cy, cx + r, cy)):
            n = 9
            for k in range(n):
                if k % 2: continue
                p0 = (xa + (xb - xa) * k / n, ya + (yb - ya) * k / n); p1 = (xa + (xb - xa) * (k + 1) / n, ya + (yb - ya) * (k + 1) / n)
                d.line([p0, p1], fill=RED + (int(255 * u),), width=10)
        L.typewriter(c, "THE CROSS WOULD GO HERE", t, AT(a["ghost"]) + 0.4, W / 2, cy - r - 40, size=34, fill=RED, cps=30, anchor="mm", cursor=False)
    L.typewriter(c, "RECONSTRUCTION  \u00b7  THE ORIGINAL POST DID NOT SURVIVE", t, t0 + 0.4, W / 2, H - 70, size=28, fill=STEEL, cps=50, anchor="mm", cursor=False)
    return c

def frame(t):
    k, (key, (kind, a)), t0, t1 = shot_at(t)
    if kind == "kb":
        src = tone(a["rid"], a["crop"], a["rot"]); c = L.vignette(L.kenburns(src, t, t0, t1, a["z"][0], a["z"][1], a["c0"], a["c1"]))
    elif kind == "kbp":
        c = blur_bg(a["rid"], a["crop"]).copy(); u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6)))
        card = pcard_h(a["rid"], a["crop"], a["h"], a["rot"]); k2 = 1.0 + 0.05 * u
        card = card.resize((int(card.width * k2), int(card.height * k2)), Image.BICUBIC)
        L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30)
    elif kind == "carve":
        c = carve_frame(a, t, t0, t1)
    elif kind == "coldopen":
        c = blur_bg("D8", None).copy()
        if NO_BOTTOM:
            L.typewriter(c, "ABOUT 5 AM", t, t0 + 0.05, W / 2, H / 2 - 60, size=150, cps=10, anchor="mm", cursor=False)
            L.text(c, "Tuesday, August 18, 1590", W / 2, H / 2 + 60, 50, BONE, SER, alpha=ease((t - t0 - 1.0) / 0.4))
            L.rule(c, W / 2 - 290, W / 2 + 290, H / 2 + 110, t, t0 + 1.2); draw_ov(c, t, t0, t1); return c
        card = pcard_h("A14", None, 560, 3); c.alpha_composite(card, (int(W * 0.70 - card.width / 2), int(H / 2 - card.height / 2)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip(1.25 - np.linspace(0, 1, W) * 1.9, 0, 1)[None, :] * 235
        lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
        L.typewriter(c, "ABOUT 5 AM", t, t0 + 0.05, 110, H / 2 - 60, size=140, cps=10, anchor="lm", cursor=False)
        L.text(c, "Tuesday, August 18, 1590", 115, H / 2 + 60, 50, BONE, SER, anchor="lm", alpha=ease((t - t0 - 1.0) / 0.4))
        L.rule(c, 115, 700, H / 2 + 110, t, t0 + 1.2)
    elif kind == "card":
        c = Image.new("RGBA", (W, H), INK + (255,)); big = a["big"]
        L.typewriter(c, big, t, t0 + 0.05, W / 2, H / 2 - 50, size=200 if len(big) < 10 else 140, cps=12, anchor="mm", cursor=False)
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
    elif kind == "prints":
        c = Image.new("RGBA", (W, H), INK + (255,))
        for rid, crop, w, x, y, rot, d, label in a["items"]:
            if NO_BOTTOM: w, x = int(w * 0.85), W / 2 + (x - W / 2) * 0.75
            L.drop(c, pcard(rid, crop, w, rot), x, y, t, t0 + d)
            if label: L.typewriter(c, label, t, t0 + d + 0.35, x, y + pcard(rid, crop, w, rot).height / 2 + 30, size=32, cps=30, anchor="mm", cursor=False)
    elif kind == "letter":
        c = Image.new("RGBA", (W, H), INK + (255,)); rows, foot = LETTERS[a["key"]]; hand_paper(c, t, rows, foot, t0 + 0.4)
    elif kind == "title":
        c = Image.new("RGBA", (W, H), INK + (255,)); u = ease((t - t0) / 0.6)
        L.text(c, "the", W / 2, H / 2 - 170, 80, STEEL, SER, alpha=u); L.text(c, "LAST HOURS", W / 2, H / 2 - 10, 240, BONE, COND, alpha=u)
        L.rule(c, W / 2 - 320, W / 2 + 320, H / 2 + 135, t, t0 + 0.4, width=9)
        L.typewriter(c, "FILE 04  \u00b7  ROANOKE  \u00b7  AUGUST 1590", t, t0 + 0.9, W / 2, H / 2 + 230, size=40, fill=STEEL, cps=30, anchor="mm", cursor=False)
    elif kind == "cta":
        c = L.vignette(L.kenburns(tone("D1"), t, t0, t1, 1.05, 1.15)); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 150)))
        L.typewriter(c, "EVERYTHING HERE IS FROM THE REAL RECORDS", t, T[60], W / 2, H / 2 - 60, size=56, cps=30, anchor="mm", cursor=False)
        L.typewriter(c, "LIKE  \u00b7  SUBSCRIBE", t, T[61] + 0.8, W / 2, H / 2 + 60, size=70, fill=RED, cps=14, anchor="mm", cursor=False)
        if t >= T[62]: L.typewriter(c, "DAYBREAK", t, T[62] + 0.3, W / 2, H / 2 + 200, size=60, fill=BONE, cps=10, anchor="mm", cursor=False)
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 120, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 230, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 320, t, t0, width=7)
        L.typewriter(c, "NEXT FILE:  D.B. COOPER", t, T[135], W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
        if t > VO_END:
            d = ImageDraw.Draw(c)
            for x in (110, 1170): d.rectangle((x, 520, x + 640, 880), outline=STEEL + (255,), width=3)
            d.ellipse((835, 575, 1085, 825), outline=STEEL + (255,), width=3)
    else:
        c = Image.new("RGBA", (W, H), INK + (255,))
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
    music("Rising Tide.mp3", tl(10), tl(35), -26); music("Man Down.mp3", tl(35), tl(59), -25); music("Thunder Dreams.mp3", tl(59), tl(63), -22)
    music("Thunder Dreams.mp3", tl(63), tl(98), -25); music("Industrial Cinematic.mp3", tl(98), tl(124), -27); music("Rising Tide.mp3", tl(124), tl(134), -25)
    music("Thunder Dreams.mp3", tl(134), DUR, -22)
    loop("waves_windy_sea_loop", 0, tl(3), -24); loop("wind_cold_interior", tl(3), tl(10), -30); loop("waves_rough_sea_loop", tl(43), tl(53), -28)
    loop("wind_ambience", tl(53), tl(59), -30); loop("wind_scary", tl(84), tl(92), -30); loop("waves_rocky_shore", tl(65), tl(70), -34)
    HITS = [("hit_deep_heartbeat_impact", -17), ("hit_short_bass", -19), ("hit_glass_suspense", -21), ("hit_cinematic_deep_impact", -20)]
    SWIPES = [("whoosh_fast_transition", -22), ("paper_slide", -20), ("whoosh_ghostly", -24)]; MK = [0]
    for i, (key, (kind, a)) in enumerate(SHOTS):
        t0 = SHOT_T[i]
        if kind == "card":
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "doc": sfx("paper_slide", t0, -18); sfx("typewriter_soft_click", t0 + 0.2, -24)
        elif kind == "kbp": sfx("paper_slide", t0, -19); sfx("camera_vintage_shutter", t0 + 0.12, -25)
        elif kind == "nmap": sfx("paper_page_turn", t0, -22)
        elif kind == "carve":
            st = AT(a["key"]) if a["key"] else t0 + 0.15
            for j, ch in enumerate(a["word"]):
                if ch != " ": sfx("metal_tool_drop", st + j * 0.09, -30, maxlen=0.25)
            sfx("hit_deep_heartbeat_impact", st, -18, maxlen=1.5)
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
    for j, (ln, off, kind, a) in enumerate(OV):
        if kind == "stamp": sfx("hit_horror_drum", OVT[j], -14)
        if kind in ("typecenter", "typecenter_red", "list"): sfx("typewriter_typing_old", OVT[j], -26)
    sfx("hit_cinematic_deep_impact", T[2] - 0.1, -14)
    for j in range(len("ABOUT 5 AM")): sfx("typewriter_single_hit", T[2] + j / 10, -20)
    sfx("hit_cinematic_deep_impact", 0.0, -12)                                   # the cold open starts on a hit
    EV = [(0, 0.0, "thunder_deep_rumble", -20), (4, 0.2, "waves_rough_sea_loop", -24), (5, "trumpet", "radio_static_crackles", -34), (6, "answer", "heartbeat_single", -20),
          (14, 0.2, "wind_scary", -26), (15, "head", "hit_horror_drum", -20), (17, "killed", "heartbeat_single", -22), (27, 0.3, "ship_hull_creak", -22),
          (28, 0.2, "thunder_deep_rumble", -26), (29, 0.3, "ship_hull_creak", -24), (30, "boarded", "metal_hammer_hit", -24), (31, 0.4, "ship_hull_creak", -24),
          (36, "smoke", "wind_deep_cinematic_hum", -26), (39, "fire", "hit_big_cinematic_impact", -20), (39, "time", "hit_big_cinematic_impact", -22),
          (40, 0.3, "waves_with_birds", -30), (41, 0.3, "footsteps_stones_loop", -28), (44, "gale", "wind_scary", -22), (45, 0.3, "water_splash", -22),
          (46, "flips", "sea_water_splash", -18), (47, "rolls", "jump_in_water", -22), (49, "seven", "hit_deep_heartbeat_impact", -16),
          (55, "fire", "wind_deep_cinematic_hum", -28), (57, 0.0, "heartbeat_slow", -20), (58, 0.3, "wind_ambience", -30),
          (65, 0.3, "footsteps_stones_loop", -28), (67, 0.4, "footsteps_stones_loop", -28), (70, "houses", "wind_scary", -26), (71, "palisade", "metal_tool_falling", -28),
          (75, 0.0, "hit_cinematic_deep_impact", -14), (76, "bars", "metal_tool_drop", -22), (78, "broken", "heavy_sliding_door", -26), (79, "books", "paper_big_page_turn", -20),
          (84, "stormy", "thunder_deep_rumble", -20), (87, 0.2, "thunder_deep_rumble", -18), (89, "snaps", "metal_hammer_hit", -16), (90, "drags", "gear_metallic_lock", -22),
          (90, "aground", "ship_hull_creak", -18), (96, 0.3, "waves_harbor_rocks", -28), (98, 0.3, "paper_writing_pencil", -22), (100, 0.2, "clock_wall_tick", -24),
          (102, 0.3, "paper_page_turn", -22), (106, 0.0, "hit_horror_drum", -18), (111, 0.3, "wind_cold_interior", -26), (120, 0.3, "newspaper_drop", -20),
          (130, "stop", "heartbeat_single", -20), (132, "word", "clock_wall_tick", -22), (134, 0.2, "typewriter_return_bell", -18)]
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
def final(n, name="TheLastHours_04_Roanoke.mp4"):
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
        CH = [(0, "Aug 18, 1590: one word on a post"), (11, "1587: the colony and the secret code"), (28, "1588-1590: three years away"),
              (35, "Aug 15: smoke on the island"), (43, "Aug 17, 10 AM: seven drown"), (53, "After dark: the trumpet"), (63, "Daybreak: C R O"),
              (70, "CROATOAN, and no cross"), (84, "The storm and the anchors"), (98, "1593: White gives up"), (101, "Jamestown's stories"),
              (109, "The drought in the tree rings"), (113, "Croatoan or the Chowan River? The 2026 claims"), (124, "What the records can't tell us")]
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
