"""The Last Hours #7: the Andrée balloon expedition, 11 July 1897 - 6 August 1930 (Case File style, colour grade, 1920x1080). Built on render_egyptair.py.
Every shot starts on a narration line (index into vo_lines.txt without '##'), or on a spoken word in it: key (line, "word").
Line timing comes from the exact-zero gaps in the VO, word timing from whisper (vo/vo_words.json).
  uv run --no-project --with pillow --with numpy --with soundfile python render_andree.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
sys.path.insert(0, "D:/why habibi/_newchannel/08_andree"); import polarmap as PM
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines (they cut across the sounds at this scale)
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/08_andree/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
HAND = "C:/Windows/Fonts/segoeprb.ttf"                 # hand-printed look for the reconstruction cards
ROMAN = "C:/Windows/Fonts/timesbd.ttf"                 # Roman capitals for the carved-letter reconstructions
LEAD = 0.8; TAIL = 20.0

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/andree_vo_chatterbox.wav")
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
ROT = set()
IMG = {}
COLOR = os.environ.get("LH_COLOR", "1") == "1"                 # the colour version: photos graded like the thumbnails, documents stay paper-toned
DOCS = {"A1", "A2", "A5", "A6", "A7", "A10", "A11", "A12", "A13", "D2"}
def colour(path, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
    a = np.asarray(im, np.float32) / 255; a = np.clip((a - 0.5) * 1.10 + 0.5, 0, 1)
    g = a.mean(2, keepdims=True); a = np.clip(g + (a - g) * 1.15, 0, 1)
    a = a + (1 - g) * 0.10 * np.array([-0.6, 0.15, 0.35]) + g * 0.06 * np.array([0.5, 0.15, -0.4])   # teal shadows, warm highlights
    return Image.fromarray((np.clip(a * 0.94, 0, 1) * 255).astype(np.uint8))
def tone(rid, crop=None, rot=0):
    k = (rid, crop)
    if k not in IMG:
        im = colour(P(rid), crop) if COLOR and rid not in DOCS else L.bw(P(rid), crop)
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
LAUNCH, HOLL, VOGEL = (10.912, 79.723), (11.006, 79.739), (11.301, 79.852)
FREE_END, PIG_REL, LAND = (24.22, 82.48), (15.08, 82.03), (29.867, 82.933)
AUG3, CFLORA, SEVEN = (28.5, 82.45), (50.08, 79.95), (20.8, 80.75)
PIG_SHOT, KVIT, POLE = (20.33, 80.73), (31.428, 80.084), (0.0, 90.0)
SIBERIA, ALASKA, CANADA = (130.0, 72.0), (-152.0, 70.3), (-105.0, 69.0)
FLIGHT = [LAUNCH, HOLL, VOGEL, (17.5, 81.3), FREE_END, (19.5, 82.3), PIG_REL, (22.0, 82.4), LAND]   # approximate, after MOMP's 1930 map
MARCH = [LAND, (29.5, 82.7), AUG3, (27.5, 82.0), (29.0, 81.3), (30.5, 80.6), KVIT]                    # ice march + drift, approximate
V_POLE, V_PLAN, V_DANES = (13.0, 84.9, 2500), (0.0, 88.0, 8200), (11.15, 79.80, 110)
V_FLIGHT, V_STAGE, V_MARCH, V_PIG = (20.0, 81.9, 1150), (26.0, 84.2, 2900), (33.0, 81.3, 1500), (18.0, 81.35, 720)

# ------------------------------------------------------------------ shot constructors
CROP = {"A1": (0.10, 0.08, 0.80, 0.80), "A2": (0.53, 0.09, 0.79, 0.50), "A3": (0.05, 0.06, 0.95, 0.88), "A4": (0.05, 0.06, 0.95, 0.88),
        "A6": (0.02, 0.02, 0.98, 0.98), "A7": (0.05, 0.04, 0.95, 0.76), "B1": (0.08, 0.03, 0.92, 0.97), "B2": (0.06, 0.04, 0.94, 0.86),
        "B3": (0.06, 0.04, 0.94, 0.86), "B5": (0.0, 0.16, 1.0, 1.0), "B7": (0.06, 0.06, 0.94, 0.94), "B8": (0.06, 0.07, 0.92, 0.88),
        "B9": (0.0, 0.0, 0.95, 0.84), "B11": (0.08, 0.07, 0.92, 0.87), "B14": (0.0, 0.06, 1.0, 1.0), "B15": (0.19, 0.08, 0.88, 0.71),
        "C2": (0.0, 0.0, 0.99, 0.97), "C3": (0.0, 0.08, 1.0, 0.92), "D2": (0.37, 0.0, 1.0, 1.0), "D6": (0.10, 0.0, 1.0, 1.0),
        "E1": (0.21, 0.095, 0.885, 0.76), "E2": (0.0, 0.0, 0.85, 1.0), "F3": (0.2, 0.0, 1.0, 0.8), "I25": (0.33, 0.14, 0.80, 0.52),
        "I26": (0.10, 0.13, 0.78, 0.28), "I27": (0.235, 0.135, 0.895, 0.44), "A10": (0.06, 0.355, 0.245, 0.56), "A11": (0.800, 0.047, 0.944, 0.16)}
IL = "ILLUSTRATIVE"
STR = "NILS STRINDBERG, 1897  ·  DEVELOPED 1930"
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag, dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def PMAP(view, ops=(), z=(1.0, 1.05), c0=(0.5, 0.5), c1=None): return ("pmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def CHART(rid, pins, foot, crop=None): return ("chart", dict(rid=rid, crop=crop, pins=pins, foot=foot))
def TYPED(key): return ("typed", dict(key=key))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def pr(rid, x, label=None, d=0.1, w=430, rot=-2, y=None): return (rid, CROP.get(rid), w, x, (y or H / 2 - 40), rot, d, label)
def PRINTS(items): return ("prints", dict(items=items))
def D(line, word): return AT((line, word)) - KT(line)

SHOTS = [
 (0, KB("C1", z=(1.0, 1.14), c0=(0.55, 0.5), c1=(0.5, 0.52), tag=STR)),          # frame 1: the balloon on the ice
 ((0, "develops|film"), KB("C1", z=(1.25, 1.4), c0=(0.3, 0.62), tag=STR)),
 (1, TCARD("7:19 AM", "Wednesday, July 14, 1897  ·  Greenwich time", "C4")),
 (2, KB("C6", z=(1.05, 1.18), c0=(0.5, 0.55), tag=STR)),
 (3, KB("B3", z=(1.0, 1.1), c0=(0.5, 0.42))),
 ((3, "photographs"), KB("C1", z=(1.15, 1.3), c0=(0.45, 0.6), tag=STR)),
 (4, KB("C2", z=(1.0, 1.12), tag="THE SAME FRAME, AS THE FILM CAME OUT IN 1930")),
 (5, KB("E2", z=(1.0, 1.12), c0=(0.42, 0.5), dim=0.25, tag="WHITE ISLAND TODAY  ·  RICHARD NEILL, CC0")),
 (6, PRINTS([pr("A1", W / 2 - 560, "THEIR WORDS", D(6, "read|words"), w=380), pr("C10", W / 2, "THEIR FILM", D(6, "film"), rot=1.5, w=470),
             pr("E3", W / 2 + 560, "THE QUESTION", D(6, "heard|nobody"), rot=-1, w=430)])),
 (7, TCARD("3:00 AM", "Sunday, July 11, 1897  ·  Danes Island", "B5")),
 ((7, "danes|island"), PMAP(V_POLE, ops=[("pin", *LAUNCH, "DANES ISLAND", 0.1, "left"), ("pole", 0.6), ("dist", LAUNCH, POLE, "710 MILES", 1.0)])),
 (8, KB("E4", z=(1.0, 1.12), c0=(0.45, 0.5), tag="DANES ISLAND STRAIT  ·  COLOUR PRINT, 1900")),
 (9, KB("B5", z=(1.0, 1.1), tag="THE BASE, 1896  ·  TORE KNÖS")),
 (10, PMAP(V_PLAN, ops=[("pole", 0.0), ("pin", *LAUNCH, "DANES ISLAND", 0.0, "down"), ("route", [LAUNCH, POLE], 0.4, 1.4),
                        ("route", [POLE, SIBERIA], 2.0, 0.9, True), ("pin", *SIBERIA, "SIBERIA", 2.8, "right"),
                        ("route", [POLE, ALASKA], 2.6, 0.9, True), ("pin", *ALASKA, "ALASKA", 3.4, "up"),
                        ("route", [POLE, CANADA], 3.2, 0.9, True), ("pin", *CANADA, "CANADA", 4.0, "left")])),
 (11, KB("B2", z=(1.0, 1.1), c0=(0.5, 0.4))),
 ((11, "nobel"), KB("A8", z=(1.0, 1.1), tag="ANDRÉE'S TELEGRAM TO ALFRED NOBEL, 1896")),
 (12, KB("B6", z=(1.0, 1.12), c0=(0.5, 0.5), tag="THE BALLOON HOUSE  ·  COLOUR PRINT, c. 1897")),
 ((12, "ropes"), KB("A9", z=(1.0, 1.15), c0=(0.5, 0.35), c1=(0.5, 0.7), tag="THE EAGLE  ·  BLUEPRINT, 1:150")),
 (13, KB("B9", z=(1.05, 1.18), c0=(0.5, 0.65))),
 (14, KB("B7", z=(1.0, 1.1), tag="THE BALLOON HOUSE, DANES ISLAND")),
 ((14, "roof"), TYPED("vote")),
 (15, KB("B4", z=(1.0, 1.1), c0=(0.6, 0.45), tag="KNUT FRÆNKEL ON DANES ISLAND, 1897")),
 ((15, "strindberg"), TYPED("vote")),
 (17, KB("B15", z=(1.0, 1.1), tag="SVENSKSUND AND VIRGO IN VIRGO HARBOUR, 1897  ·  HASSELBLAD")),
 ((17, "agree"), KB("B10", z=(1.05, 1.15), dim=0.3, tag="DANES ISLAND, 1897  ·  HASSELBLAD")),
 (18, TCARD("1:43 PM", "Greenwich time  ·  8:43 AM in New York", "B12")),
 ((18, "climb"), KB("B12", z=(1.0, 1.12), c0=(0.45, 0.4), tag="“A MINUTE BEFORE THE START”  ·  11 JULY 1897")),
 (19, COUNTER([((19, 0.0), "1:46 PM")], "“CUT EVERYWHERE!”  ·  ANDRÉE", "B12", size=360)),
 (20, KB("B14", z=(1.0, 1.12), c0=(0.55, 0.45), tag="THE LAUNCH  ·  G. V. E. SVEDENBORG")),
 (21, KB("I27", z=(1.0, 1.1), dim=0.3)),
 (22, KB("B13", z=(1.0, 1.12), c0=(0.5, 0.45), tag="“JUST AFTER THE START”  ·  11 JULY 1897")),
 (23, KB("B13", z=(1.2, 1.4), c0=(0.45, 0.78))),
 (24, KB("B9", z=(1.0, 1.1), tag="THE BALLOON'S LOWER HALF, 1897")),
 (25, KB("B14", z=(1.25, 1.45), c0=(0.6, 0.5))),
 ((25, "notebook|strindberg"), TYPED("rope")),
 (26, PMAP(V_DANES, ops=[("pin", *LAUNCH, "1:46 PM  ·  LIFT-OFF", 0.0, "left"), ("route", [LAUNCH, HOLL, VOGEL], 0.3, 2.2),
                         ("pin", *VOGEL, "2:14 PM  ·  VOGELSANG", 2.5, "right")])),
 (28, KB("B14", z=(1.5, 1.8), c0=(0.6, 0.48))),
 (29, TCARD("5:36 PM", "Sunday, July 11  ·  over the sea ice", "A3")),
 (30, KB("A3", z=(1.0, 1.12), c0=(0.5, 0.45), tag="ANDRÉE'S PIGEON  ·  YMER, 1897")),
 (31, KB("F6", z=(1.0, 1.12), tag="THE ARCTIC SEA ICE FROM SPACE  ·  NASA")),
 ((31, "buoy|message"), KBP("A1", h=860, rot=-1.5)),
 (32, PMAP(V_FLIGHT, ops=[("pin", *LAUNCH, "", -9), ("route", FLIGHT[:5], 0.2, 2.6), ("pin", *FREE_END, "AFTER MIDNIGHT  ·  THE ROPES HIT THE ICE", 2.9, "right")])),
 (33, PMAP(V_FLIGHT, ops=[("pin", *LAUNCH, "", -9), ("route", FLIGHT[:5], -9, 0.1), ("route", FLIGHT[4:7], 0.6, 2.4), ("pin", *PIG_REL, "MONDAY  ·  BACK WEST", 3.0, "left")])),
 (34, COUNTER([((34, "eight|8"), "8")], "TOUCHES IN 30 MINUTES  ·  THE GONDOLA ON THE ICE", "B8", size=460)),
 (35, KB("I26", z=(1.0, 1.1))),
 (36, KB("B2", z=(1.1, 1.22), c0=(0.5, 0.4), dim=0.2)),
 ((36, "writes"), TYPED("watch")),
 (38, KB("D4", z=(1.0, 1.12), tag="STOCKHOLM, 5 OCTOBER 1930")),
 (39, KB("C3", z=(1.0, 1.0), c0=(0.25, 0.5), c1=(0.45, 0.5), tag="STRINDBERG'S 360° PANORAMA OF THE ICE, 1897")),
 (40, TCARD("10:55 AM", "Tuesday, July 13, 1897", "C4")),
 (41, TYPED("menu")),
 (42, KB("A4", z=(1.0, 1.12), c0=(0.5, 0.5))),
 ((42, "message"), KBP("A2", h=860, rot=1.5)),
 (43, KB("C4", z=(1.0, 1.15), c0=(0.7, 0.5), tag=STR)),
 ((43, "ton"), KB("I5", z=(1.0, 1.1), crop=(0.0, 0.0, 0.98, 0.97), tag="THE RAW FILM  ·  " + STR)),
 (44, KB("B8", z=(1.05, 1.2), c0=(0.45, 0.5), tag="THE GONDOLA  ·  HASSELBLAD, 1897")),
 (45, TCARD("5:28 AM", "Wednesday, July 14, 1897", "C4")),
 (46, COUNTER([((46, 0.0), "7:19 AM")], "“WE JUMPED OUT OF THE GONDOLA.”  ·  ANDRÉE", "C1", size=360)),
 (47, PMAP(V_STAGE, ops=[("pole", 0.0), ("pin", *LAUNCH, "DANES ISLAND", 0.0, "left"), ("route", FLIGHT, 0.2, 1.6), ("pin", *LAND, "14 JULY  ·  82°56' N", 1.8, "right"),
                         ("dist", LAND, POLE, "488 MILES", 2.4)])),
 (48, KB("C5", z=(1.0, 1.15), c0=(0.45, 0.55), tag=STR)),
 (49, KB("C1", z=(1.25, 1.0), c0=(0.5, 0.55), tag=STR)),
 (50, KB("C8", z=(1.0, 1.12), c0=(0.45, 0.5), tag="THE LANDING CAMP  ·  " + STR)),
 (51, PMAP(V_MARCH, ops=[("pin", *LAND, "THE LANDING", 0.0, "up"), ("pin", *CFLORA, "CAPE FLORA  ·  THE DEPOT", 0.6, "up"), ("dist", LAND, CFLORA, "290 MILES", 1.2)])),
 (52, KB("C9", z=(1.0, 1.12), c0=(0.55, 0.5), tag="19 JULY: ANDRÉE LOOKS FOR LAND  ·  " + STR)),
 ((52, "thursday|july"), TCARD("JULY 22", "Thursday  ·  the march begins", "C13")),
 (53, KB("C12", z=(1.0, 1.12), c0=(0.5, 0.5), tag="STRINDBERG AND HIS SLEDGE  ·  PHOTO: ANDRÉE, 1897")),
 (54, KB("C10", z=(1.0, 1.15), c0=(0.45, 0.5), tag="ALL THREE  ·  SELF-TIMER, 1897")),
 ((54, "cracks|across"), KB("C11", z=(1.0, 1.15), tag=STR)),
 (55, PMAP(V_MARCH, ops=[("pin", *LAND, "", -9), ("route", MARCH[:3], 0.2, 2.0), ("pin", *AUG3, "3 AUGUST", 2.2, "left"), ("pin", *CFLORA, "CAPE FLORA", -9, "up")])),
 (56, KB("C14", z=(1.0, 1.12), tag="3 AUGUST: “THE EVOLUTIONARY HISTORY OF OUR FORKS”")),
 ((56, "overcome"), KB("C13", z=(1.05, 1.15), dim=0.3)),
 (57, PMAP(V_MARCH, ops=[("pin", *LAND, "", -9), ("route", MARCH[:3], -9, 0.1), ("pin", *AUG3, "4 AUGUST: TURN", 0.0, "up"),
                         ("route", [AUG3, SEVEN], 0.6, 1.6, True), ("pin", *SEVEN, "SEVEN ISLANDS", 2.2, "left")])),
 (58, KB("A3", z=(1.1, 1.25), c0=(0.5, 0.4))),
 (59, PMAP(V_PIG, ops=[("pin", *PIG_REL, "13 JULY  ·  THE THIRD POST", 0.2, "up"), ("pin", *PIG_SHOT, "15 JULY  ·  THE ALKEN", 1.0, "right"), ("dist", PIG_REL, PIG_SHOT, "105 MILES", 1.6)])),
 (60, KB("A4", z=(1.0, 1.12), c0=(0.5, 0.45), tag="THE PIGEON  ·  YMER, 1897")),
 (61, KB("A3", z=(1.15, 1.3), c0=(0.5, 0.35), dim=0.3)),
 (62, KB("I25", z=(1.0, 1.1), tag="THE SAME BIRD, MOUNTED  ·  1930")),
 (63, KB("A4", z=(1.15, 1.3), c0=(0.6, 0.6))),
 (64, KB("A3", z=(1.2, 1.35), c0=(0.55, 0.7))),
 (65, KBP("A2", h=860, rot=-1)),
 (66, COUNTER([((66, 0.0), "36"), ((66, "only|one"), "1")], "PIGEONS CARRIED  ·  MESSAGES THAT EVER ARRIVED", "A3", size=460)),
 (67, KBP("A11", h=860, rot=-1.5)),
 (68, KBP("A10", h=860, rot=1.5)),
 (69, KB("C13", z=(1.0, 1.12), c0=(0.5, 0.5), tag=STR)),
 (70, KB("C7", z=(1.0, 1.12), tag=STR)),
 ((70, "position"), KB("C17", z=(1.0, 1.1), dim=0.35)),
 (71, TCARD("SEPT 17", "Friday  ·  land, for the first time since July 11", "E1")),
 ((71, "island|looks"), KB("E1", z=(1.0, 1.15), tag="WHITE ISLAND FROM THE SEA, 1898  ·  AXEL HAMBERG")),
 (72, KB("C15", z=(1.0, 1.08), tag="FOOD  ·  " + STR)),
 ((72, "april|meat"), KB("C16", z=(1.0, 1.1), tag=STR)),
 (73, TYPED("bear")),
 (74, KB("A6", z=(1.0, 1.1), c0=(0.5, 0.4), tag="STRINDBERG'S PLAN OF THE SNOW HUT “HOME”")),
 (75, TCARD("5:30 AM", "Saturday, October 2, 1897", "C11")),
 ((75, "flow|floe"), KB("C11", z=(1.1, 1.3), c0=(0.5, 0.7))),
 (76, KB("B1", z=(1.0, 1.08), c0=(0.5, 0.45), dim=0.3)),
 (77, PMAP(V_MARCH, ops=[("pin", *LAND, "THE LANDING", -9, "up"), ("route", MARCH, 0.2, 2.4), ("pin", *KVIT, "WHITE ISLAND", 2.6, "right")])),
 (78, TCARD("OCT 5", "Tuesday  ·  “Moved ashore.”", "E2")),
 ((78, "solid"), KB("E2", z=(1.0, 1.12), c0=(0.42, 0.5), tag="ANDRÉENESET, WHITE ISLAND, 2011  ·  RICHARD NEILL, CC0")),
 (79, TYPED("almanac")),
 ((81, "drag"), KB("D2", z=(1.0, 1.12), tag="THE CAMP, AS MAPPED IN 1930")),
 (82, KB("E2", z=(1.12, 1.25), c0=(0.6, 0.5), dim=0.35)),
 (83, KB("F4", z=(1.0, 1.15), c0=(0.39, 0.5), tag="WHITE ISLAND'S SOUTHWEST POINT  ·  NASA / USGS")),
 (84, TYPED("almanac")),
 (85, KB("F2", z=(1.0, 1.12), tag="WHITE ISLAND IN THE DRIFT ICE  ·  NASA / USGS LANDSAT")),
 (86, KB("F4", z=(1.15, 1.35), c0=(0.39, 0.5), dim=0.2)),
 (87, KB("E2", z=(1.0, 1.1), c0=(0.3, 0.55), dim=0.25)),
 ((87, "buried"), KB("E2", z=(1.25, 1.4), c0=(0.7, 0.6), dim=0.2)),
 (88, KB("E3", z=(1.0, 1.12), tag="THE MEMORIAL ON WHITE ISLAND  ·  RICHARD NEILL")),
 (89, KB("B1", z=(1.0, 1.1), dim=0.2, tag="ANDRÉE, STRINDBERG, FRÆNKEL  ·  3 MAY 1897  ·  GÖSTA FLORMAN")),
 (90, KB("E1", z=(1.0, 1.12), tag="WHITE ISLAND, 18 AUGUST 1898  ·  AXEL HAMBERG")),
 (91, CHART("F4", [(0.392, 0.509, "THE CAMP", (91, "stood|three"), "up")], "WHITE ISLAND'S SOUTHWEST POINT  ·  NASA / USGS LANDSAT, 2021")),
 (92, KB("E1", z=(1.15, 1.3), c0=(0.4, 0.5))),
 (93, KB("I26", z=(1.0, 1.12), tag="TWO OF THE BUOYS THAT CAME BACK")),
 (94, COUNTER([((94, "thirty|33"), "33 YEARS")], "1897 - 1930", "F2", size=300)),
 (95, TCARD("AUG 6, 1930", "Wednesday  ·  White Island", "F3")),
 (96, KB("D1", z=(1.0, 1.12), c0=(0.5, 0.45), tag="M/S BRATVAAG OF ÅLESUND, 1930")),
 (97, KB("E2", z=(1.0, 1.12), c0=(0.35, 0.6))),
 (98, KB("E2", z=(1.2, 1.4), c0=(0.3, 0.7))),
 (99, KB("D6", z=(1.0, 1.12), tag="THE FINDS ON SHOW, STOCKHOLM, 1931")),
 ((99, "canvas"), KB("C13", z=(1.0, 1.12), c0=(0.4, 0.55), tag="THE CANVAS BOAT ON ITS SLEDGE, 1897  ·  " + STR)),
 (100, KB("D1", z=(1.15, 1.3), c0=(0.5, 0.55))),
 (101, KB("D2", z=(1.0, 1.15), tag="PLAN OF THE CAMP  ·  HORN AND STUBBENDORFF, 1930")),
 ((101, "stove"), KB("F4", z=(1.2, 1.35), c0=(0.39, 0.5), dim=0.2)),
 (102, KB("F3", z=(1.0, 1.12), tag="WHITE ISLAND ICE-FREE, AUGUST 2020  ·  NASA / USGS")),
 ((102, "couple|feet"), KB("E2", z=(1.0, 1.1), c0=(0.5, 0.45))),
 (103, KB("D3", z=(1.0, 1.12), tag="THE COMMISSION, TROMSØ, SEPTEMBER 1930")),
 (104, COUNTER([((104, "february|develop"), "FEB 1898"), ((104, "now|nineteen|1930"), "1930")], "THE DATE TO DEVELOP IT BY", "B11", size=340)),
 (105, KB("C2", z=(1.1, 1.3), c0=(0.3, 0.4), tag="THE RAW FILM, AS DEVELOPED")),
 (106, KB("B11", z=(1.0, 1.12), tag="STRINDBERG TESTS A CAMERA, DANES ISLAND, 1897")),
 (107, COUNTER([((107, "fifty|50"), "50"), ((107, "twenty|20"), "20"), ((107, "ninety|93"), "93")], "FRAMES THAT CAME BACK", "C17", size=460)),
 (108, KB("C1", z=(1.0, 1.06), tag=STR)),
 ((108, "sledges"), KB("C12", z=(1.0, 1.06), tag=STR)),
 ((108, "bear"), KB("C17", z=(1.0, 1.04), tag="THE MOST DAMAGED FRAME  ·  " + STR)),
 ((108, "three"), KB("C10", z=(1.0, 1.08), tag=STR)),
 (109, PRINTS([pr("C2", W / 2 - 450, "THE FILM AS DEVELOPED", D(109, "retouched|prints"), w=820, rot=-1.5),
               pr("C1", W / 2 + 450, "THE RETOUCHED PRINT", D(109, "after"), w=820, rot=1.5)])),
 (110, TCARD("OCT 5, 1930", "Sunday  ·  33 years to the day", "D4")),
 (111, PRINTS([pr("B15", W / 2 - 460, "SVENSKSUND, 1897", 0.1, w=760), pr("D4", W / 2 + 460, "SVENSKSUND, 1930", D(111, "brings|home"), w=760, rot=1.5)])),
 (112, KB("B3", z=(1.05, 1.15), c0=(0.5, 0.4), dim=0.2)),
 (113, KB("D5", z=(1.0, 1.1), tag="STOCKHOLM, 5 OCTOBER 1930")),
 ((113, "we"), KB("B1", z=(1.0, 1.08), c0=(0.5, 0.45), dim=0.3)),
 (114, KB("E3", z=(1.0, 1.12), c0=(0.5, 0.5), dim=0.2)),
 ((114, "note"), KB("C9", z=(1.0, 1.1), dim=0.2)),
 (115, KB("D6", z=(1.0, 1.1))),
 (116, KB("C17", z=(1.05, 1.15), dim=0.35)),
 ((116, "rarely|famous"), KB("C13", z=(1.1, 1.2), dim=0.3)),
 (117, KB("D2", z=(1.05, 1.15), dim=0.35)),
 (118, TYPED("bear")),
 (119, KB("D6", z=(1.1, 1.22), c0=(0.6, 0.5), tag="THE FINDS ON SHOW, 1931")),
 ((119, "jacket"), KB("B3", z=(1.0, 1.1), c0=(0.5, 0.42), dim=0.2)),
 (120, KB("C12", z=(1.0, 1.1), dim=0.25, tag=STR)),
 (121, KB("F2", z=(1.1, 1.25), c0=(0.35, 0.55), tag="WHITE ISLAND  ·  NASA / USGS LANDSAT")),
 (122, KB("B1", z=(1.05, 1.15), dim=0.3)),
 (123, PMAP(V_DANES, ops=[("pin", *LAUNCH, "", -9), ("route", [LAUNCH, HOLL, VOGEL], -9, 0.1), ("pin", *VOGEL, "THE TIN  ·  NEVER FOUND", 0.3, "right")])),
 (124, KB("B1", z=(1.0, 1.12), c0=(0.5, 0.45))),
 (125, PRINTS([pr("A1", W / 2 - 560, "THEIR WORDS", D(125, "words"), w=380), pr("C10", W / 2, "THEIR FILM", D(125, "film"), rot=1.5, w=470),
               pr("D2", W / 2 + 560, "THEIR CAMP", D(125, "camp"), rot=-1, w=470)])),
 (126, KB("C10", z=(1.0, 1.18), c0=(0.45, 0.5), tag=STR)),
 (127, KB("E3", z=(1.0, 1.1))),
 (128, ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "lower", "THE ANDRÉE BALLOON EXPEDITION  ·  THE ARCTIC, 1897"),
 (0, "thirty|33", "typecenter", "33 YEARS"),
 (2, "eighty|82", "under", "82°56' NORTH  ·  THE DRIFTING SEA ICE"),
 (3, 0.0, "nameplate", ("NILS STRINDBERG", "24  ·  PHYSICIST, PHOTOGRAPHER, NAVIGATOR")),
 (4, "nineteen|1930", "typecenter", "DEVELOPED IN 1930"),
 (5, 0.0, "list", ["FOOD", "FUEL", "MATCHES", "GUNS"]),
 (5, "within", "under", "WITHIN WEEKS OF REACHING LAND, ALL THREE WERE DEAD"),
 (7, "danes|island", "brand", None),
 (9, 0.3, "under", "1896: THE WIND NEVER CAME  ·  1897: WAITING SINCE MAY 30"),
 (11, 0.0, "nameplate", ("S. A. ANDRÉE", "42  ·  ENGINEER, SWEDISH PATENT OFFICE  ·  LEADER")),
 (11, "nobel", "under", "ALFRED NOBEL: 65,000 OF THE 128,800 KRONOR"),
 (12, 0.3, "under", "ÖRNEN, “THE EAGLE”  ·  ABOUT 170,000 CU FT OF HYDROGEN"),
 (12, "ropes", "under", "3 DRAG ROPES  ·  3,281 FT  ·  1,874 LB"),
 (13, 0.0, "typecenter", "REMEMBER THE ROPES"),
 (14, 0.3, "under", "AROUND 8 A.M.  ·  “ONE HOUR TO THINK”"),
 (15, 0.0, "nameplate", ("KNUT FRÆNKEL", "27  ·  CIVIL ENGINEER  ·  THE WEATHER JOURNAL")),
 ((17), "hesitation", "quote", ("“...although with a certain hesitation.”", "ANDRÉE TO THE GUNBOAT'S CAPTAIN  ·  11 JULY 1897")),
 (20, "long|sweden", "under", "“LONG LIVE OLD SWEDEN!”"),
 (21, 0.0, "quote", ("“A strange feeling. Wonderful. Indescribable!”", "STRINDBERG  ·  11 JULY 1897  ·  OUR TRANSLATION")),
 (22, "dips|harbor", "under", "THE GONDOLA HITS THE WATER  ·  9 SANDBAGS (456 LB) OVERBOARD"),
 (23, "drag|ropes", "typecenter_red", "“THE DRAG ROPES ARE LYING ON THE BEACH!”"),
 (24, 0.3, "under", "THE SCREW JOINTS CAME APART  ·  2/3 OF ALL 3 ROPES STAYED BEHIND"),
 (26, "tin", "under", "A TIN WITH FAREWELL WORDS TO HIS FIANCÉE"),
 (27, 0.0, "typecenter", "REMEMBER THE TIN"),
 (28, "never", "under", "2:14 PM  ·  THE LAST TIME ANYONE SAW THE EAGLE"),
 (29, "pigeons", "under", "36 CARRIER PIGEONS  ·  FROM THE NEWSPAPER AFTONBLADET"),
 (30, 0.0, "typecenter", "HOW MANY GOT HOME?"),
 (31, "buoy|message", "lower", "BUOY No. 4  ·  THROWN 11 JULY, 10 P.M.  ·  FOUND ON A NORWEGIAN BEACH, 1900"),
 (31, "journey", "under", "“OUR JOURNEY HAS SO FAR GONE WELL... SPIRITS EXCELLENT.”"),
 (32, "fifty|55", "under", "55 HOURS OF DRAGGING AND BUMPING ON THE ICE"),
 (35, 0.1, "lower", "THE POLAR BUOY  ·  THROWN 12 JULY, 4:51 P.M.  ·  FOUND 1899"),
 (35, "no", "typecenter_red", "NO MESSAGE INSIDE"),
 (38, "archbishop", "under", "STOCKHOLM CATHEDRAL  ·  5 OCTOBER 1930"),
 (39, 0.2, "under", "HELD FAST BY AN ICE BLOCK  ·  13 HOURS"),
 (42, "message", "lower", "THE PIGEON DISPATCH  ·  DATED 13 JULY, 12:30 P.M."),
 (42, "all", "under", "“ALL WELL ON BOARD. THIS IS THE THIRD PIGEON POST.”"),
 (43, "ton", "typecenter", "ABOUT 2,200 LB OF ICE AND WATER"),
 (44, 0.2, "under", "OVERBOARD: SAND, BUOYS, THE WINCH, 440 LB OF FOOD"),
 (45, "valves", "typecenter", "BOTH VALVES OPEN"),
 (47, 0.2, "under", "65 HOURS 33 MINUTES IN THE AIR"),
 (48, 0.0, "under", "MYTH: THE BALLOON CRASHED"),
 (48, "didn|themselves", "stamp", ("THEY LANDED IT", 1260, 360)),
 (50, 0.2, "under", "“DECIDED TO START FROM THE POINT WHERE WE WERE.”  ·  ANDRÉE"),
 (53, 0.3, "under", "UP TO 440 LB A SLEDGE  ·  ALL 3 PULL ONE, THEN GO BACK"),
 (55, "eight|8", "typecenter", "8 MILES BACK NORTH IN 3 DAYS"),
 (56, "overcome", "quote", ("“We can overcome neither the current nor the ice.”", "ANDRÉE'S DIARY  ·  4 AUGUST 1897  ·  OUR TRANSLATION")),
 (61, 0.0, "quote", ("“Don't shoot it... it's a troll bird.”", "THE HARPOONER, AS THE SKIPPER TOLD IT  ·  YMER, 1897")),
 (62, 0.2, "under", "SHOT FROM THE RIGGING OF THE ALKEN  ·  15 JULY 1897"),
 (64, "tube", "under", "THE MESSAGE TUBE, TIED UNDER A TAIL FEATHER"),
 (65, 0.0, "under", "“ALL WELL ON BOARD. THIS IS THE THIRD PIGEON POST.”"),
 (67, 0.1, "lower", "THE LEDGER, GAFFNEY, S.C.  ·  19 AUGUST 1897"),
 (67, "rumor", "stamp", ("A RUMOR", 1580, 430)),
 (68, 0.1, "lower", "THE LANCASTER ENTERPRISE, S.C.  ·  28 JULY 1897"),
 (68, "believe", "under", "“I BELIEVE THAT ANDREE WILL NEVER RETURN.”  ·  GREELY"),
 (69, 0.0, "subpop", None),
 (70, "position", "quote", ("“Our position is not particularly good.”", "ANDRÉE'S DIARY  ·  SEPTEMBER 1897  ·  OUR TRANSLATION")),
 (72, 0.0, "under", "MYTH: THEY STARVED  ·  RECORD: MEAT “UNTIL APRIL”"),
 (74, "home", "under", "“HEMMET”  ·  HOME"),
 (75, "flow|floe", "typecenter_red", "THE FLOE SPLITS"),
 (76, 0.0, "quote", ("“No one had lost courage. With such comrades one should\nbe able to manage under practically any circumstances.”", "ANDRÉE'S DIARY  ·  2 OCTOBER 1897  ·  OUR TRANSLATION")),
 (80, "resignation", "stamp", ("NOT “RESIGNATION”", 1240, 790)),
 (81, "camp|rock", "under", "200 YARDS INLAND  ·  UNDER A ROCK RIDGE"),
 (82, 0.3, "list", ["STRONG WIND", "DARKNESS", "THE SNOW HUT", "DRIFTWOOD"]),
 (83, 0.0, "typecenter", "10 DAYS. NO ENTRIES."),
 (85, 0.0, "typecenter", "HOME, FROM WHERE?"),
 (86, 0.2, "under", "17 OCT: ABOUT 4 HOURS OF SUN  ·  ~20 OCT: THE POLAR NIGHT"),
 (87, "buried", "under", "A NARROW CRACK IN THE ROCK  ·  ABOUT 100 FT FROM THE TENT"),
 (88, 0.0, "typecenter", "DATES OF DEATH: UNKNOWN"),
 (90, 0.3, "under", "19 AUGUST 1898  ·  A SWEDISH SCIENTIFIC EXPEDITION GOES ASHORE"),
 (91, 0.2, "under", "A LITTLE OVER HALF A MILE FURTHER INLAND"),
 (93, 0.3, "under", "ICELAND, 1899  ·  KONG KARLS LAND, 1899  ·  NORWAY, 1900"),
 (97, 0.2, "under", "OLAV SALEN, 17  ·  KARL TUSVIK, 24  ·  LOOKING FOR WATER"),
 (98, 0.0, "typecenter", "AN ALUMINUM LID"),
 (99, "marked", "under", "“ANDRÉES POL.-EXP. 1896”  ·  ON THE GEAR"),
 (100, "found", "under", "“THEY HAD FOUND ANDRÉE”  ·  GUNNAR HORN, 1930"),
 (101, "stove", "typecenter", "THE STOVE STILL WORKED"),
 (102, "couple|feet", "under", "“...ALL WOULD HAVE BEEN HIDDEN.”  ·  GUNNAR HORN"),
 (103, "month", "under", "5 SEPTEMBER 1930  ·  THE ISBJØRN  ·  A BAG OF FILM CANISTERS"),
 (106, 0.2, "under", "JOHN HERTZBERG  ·  ROYAL INSTITUTE OF TECHNOLOGY, STOCKHOLM"),
 (110, "exactly", "under", "STEPPED ASHORE: 5 OCTOBER 1897  ·  HOME: 5 OCTOBER 1930"),
 (112, 0.2, "under", "IN ANDRÉE'S POCKET: A GOLD LOCKET, MONOGRAMMED N.S."),
 (113, "we", "quote", ("“We think we can well face death,\nhaving done what we have now done.”", "ANDRÉE, 12 JULY 1897  ·  READ IN STOCKHOLM CATHEDRAL, 1930")),
 (114, 0.0, "list", ["FOOD", "FUEL", "MATCHES", "GUNS AND AMMUNITION"]),
 (114, "note", "under", "NO NOTE  ·  NO DIARY ENTRY ABOUT ILLNESS OR A CRISIS"),
 (115, 0.0, "under", "1930: COLD AND EXHAUSTION"),
 (116, 0.0, "under", "1952: TRICHINOSIS  ·  IT RARELY KILLS"),
 (117, 0.0, "list", ["BOTULISM", "LEAD POISONING", "FUMES FROM THE STOVE"]),
 (117, "none", "stamp", ("NONE PROVEN", 1300, 820)),
 (118, "didn", "stamp", ("NOT EATEN", 1300, 790)),
 (119, 0.3, "under", "THE LEADING MODERN THEORY  ·  BEA UUSMA, SWEDISH DOCTOR"),
 (119, "jacket", "under", "STRINDBERG'S JACKET: LARGE RAGGED TEARS"),
 (120, 0.0, "under", "STRINDBERG: A POLAR BEAR (HER VIEW)  ·  THE OTHER TWO: UNDETERMINED"),
 (121, 0.2, "under", "AUGUST 2024  ·  POLAR BEARS: NO LANDING"),
 (122, "samples", "typecenter", "NO SAMPLES KEPT"),
 (124, 0.3, "under", "“WE THINK WE CAN WELL FACE DEATH...”"),
 (126, "ended", "under", "HOW IT ENDED: NEVER WRITTEN DOWN"),
 (127, "tell", "under", "HOW DO YOU THINK IT ENDED?  TELL ME BELOW"),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

LETTERS = {}
F_TR = "WORDS FROM THE RECORD  ·  OUR TRANSLATION FROM “MED ÖRNEN MOT POLEN” (1930)"
TYPES = {
 "vote": ("STRINDBERG'S LETTER, WRITTEN ON THE ICE, 21 JULY 1897", [("ANDRÉE:  SHALL WE TRY OR NOT?", (14, "shall")),
          ("FRÆNKEL:  [AFTER HEDGING]  GO.", (15, "says|go")), ("STRINDBERG:  I THINK WE OUGHT TO TRY.", (15, "think")), ("ANDRÉE:  [SAYS NOTHING]", (16, 0.0))], F_TR),
 "rope": ("STRINDBERG'S ALMANAC  ·  11 JULY 1897", [("THE GUIDE ROPE WAS LOST.", (25, "guide"))], F_TR),
 "watch": ("ANDRÉE'S DIARY  ·  12 JULY 1897, 10:53 P.M. GMT, ALONE ON WATCH", [("IT IS NOT A LITTLE STRANGE TO BE", (36, "strange")),
          ("FLOATING HERE ABOVE THE POLAR SEA.", (36, "floating")), ("THE FIRST TO HAVE FLOATED HERE", (36, "first")), ("IN A BALLOON. [...]", (36, "balloon")),
          ("WE THINK WE CAN WELL FACE DEATH,", (37, 0.0)), ("HAVING DONE WHAT WE HAVE NOW DONE.", (37, "having"))], F_TR),
 "menu": ("STRINDBERG'S NOTES  ·  13 JULY 1897  ·  AS WRITTEN", [("DINER DU 13 JUILLET.", (41, "menu")), ("POTAGE HOTCH POTCH.", (41, "soup")),
          ("CHATEAU BRIAND.", (41, "chateau")), ("KRONANS EXTRA ÖL.", (41, "beer")), ("CHOCOLAD MED KEX.", (41, "chocolate")),
          ("A GOOD AND STRENGTHENING MEAL!", (41, "good"))], "STRINDBERG'S MENU, AS PRINTED IN “MED ÖRNEN MOT POLEN” (1930)"),
 "bear": ("ANDRÉE'S DIARY  ·  SEPTEMBER 1897", [("THE BEAR IS THE POLAR EXPLORER'S", (73, "bear")), ("BEST FRIEND.", (73, "best")),
          ("[...] EVERYTHING EDIBLE,", (73, "everything")), ("EXCEPT OF COURSE THE BEAR LIVER.", (73, "liver"))], F_TR),
 "almanac": ("STRINDBERG'S ALMANAC  ·  OCTOBER 1897", [("TUE  5 OCT.   MOVED ASHORE.", (78, "moved|move")), ("WED  6 OCT.   SNOWSTORM. RECONNOITERING.", (79, 0.0)),
          ("THU  7 OCT.   MOVING.", (81, 0.0)), ("[ 10 DAYS: NO ENTRIES ]", (83, 0.0)), ("SUN 17 OCT.   HOME 7.05 A.M.", (84, "home"))], F_TR),
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

SLOT = {"lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "list_side": "side", "badge": "corner"}
OVT = [OT(ln, off) for ln, off, _, _ in OV]
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    end = shot_t1                                  # the EARLIEST later overlay in the slot wins, whatever its list order
    for j2 in range(len(OV)):
        if OVT[j2] <= OVT[j] or j2 == j: continue
        k2 = OV[j2][2]
        if SLOT.get(k2) == sl or (sl == "bottom" and k2 in ("list", "typecenter", "typecenter_red", "quote")):
            end = min(end, OVT[j2] - 0.05)
    return end
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
            L.text(c, "FILE 07  ·  THE ANDRÉE BALLOON  ·  JULY 1897", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
    elif kind == "badge":                                      # running cockpit clock, top-left, until the next badge
        f = L.font(TYPE, 34); w = f.getlength(a); al = ease((t - t0) / 0.2)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
        dd.rectangle((36, 34, 36 + w + 40, 90), fill=(0, 0, 0, int(200 * al))); dd.rectangle((36, 34, 44, 90), fill=RED + (int(255 * al),))
        c.alpha_composite(lay); ImageDraw.Draw(c).text((62, 62), a, font=f, fill=BONE, anchor="lm")
    elif kind == "subpop":                                     # mid-video subscribe nudge, top-left, 4 s
        u = t - t0
        if u < 4.0:
            k = ease(u / 0.4) * ease((4.0 - u) / 0.4); x = 40 - (1 - k) * 640
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x, 40, x + 600, 112), 36, fill=RED + (int(235 * k),))
            c.alpha_composite(lay); L.text(c, "SUBSCRIBE FOR THE NEXT FILE", x + 300, 77, 34, BONE, TYPE, alpha=k)

def typed_paper(c, t, header, rows, foot, t_foot):
    """typewritten sheet: words from the record (CVR transcript / ATC), set in type by us"""
    d = ImageDraw.Draw(c); x0, x1, y0, y1 = W / 2 - 640, W / 2 + 640, 100, H - 140
    d.rectangle((x0 + 14, y0 + 18, x1 + 14, y1 + 18), fill=(4, 4, 5)); d.rectangle((x0, y0, x1, y1), fill=(232, 226, 206))
    d.text((x0 + 70, y0 + 58), header, font=L.font(TYPE, 26), fill=(120, 40, 36), anchor="lm")
    d.line((x0 + 70, y0 + 88, x1 - 70, y0 + 88), fill=(120, 40, 36), width=3)
    n = len(rows); gap = min(104, (y1 - y0 - 180) / max(n, 1)); size = 46 if max(len(s) for s, _ in rows) <= 38 else 38
    for i, (s, key) in enumerate(rows):
        L.typewriter(c, s, t, AT(key), x0 + 70, y0 + 160 + i * gap, size=size, fill=(28, 26, 30), cps=30, anchor="lm", fnt=TYPE, cursor=False)
    L.typewriter(c, foot, t, t_foot, W / 2, H - 70, size=24, fill=STEEL, cps=60, anchor="mm", cursor=False)

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
        s, tm = cur; u = ease((t - tm) / 0.25); f = L.font(COND, int(a.get("size", 420) * (1.15 - 0.15 * u)))
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

def frame(t):
    k, (key, (kind, a)), t0, t1 = shot_at(t)
    if kind == "kb":
        src = tone(a["rid"], a["crop"]); c = L.vignette(L.kenburns(src, t, t0, t1, a["z"][0], a["z"][1], a["c0"], a["c1"])); tag(c, a.get("tag"))
        if a.get("dim"): c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * a["dim"]))))
    elif kind == "kbp":
        c = blur_bg(a["rid"], a["crop"]).copy(); u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6)))
        card = pcard_h(a["rid"], a["crop"], a["h"], a["rot"]); k2 = 1.0 + 0.05 * u
        card = card.resize((int(card.width * k2), int(card.height * k2)), Image.BICUBIC)
        L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag"))
    elif kind == "tcard": c = tcard_frame(a, t, t0, t1)
    elif kind == "card":
        c = Image.new("RGBA", (W, H), INK + (255,)); big = a["big"]
        L.typewriter(c, big, t, t0 + 0.05, W / 2, H / 2 - 50, size=200 if len(big) < 10 else 140, cps=12, anchor="mm", cursor=False)
        t2 = t0 + 0.05 + len(big) / 12
        L.text(c, a["sub"], W / 2, H / 2 + 120, 58, STEEL, SER, alpha=ease((t - t2) / 0.4)); L.rule(c, W / 2 - 280, W / 2 + 280, H / 2 + 185, t, t2 + 0.15)
    elif kind == "nmap": c = MS.map_panel(a, t, t0, t1)
    elif kind == "pmap": c = PM.pmap_panel(a, t, t0, t1).convert("RGBA")
    elif kind == "chart": c = chart_frame(a, t, t0, t1)
    elif kind == "cliff": c = cliff_frame(a, t, t0, t1)
    elif kind == "counter": c = counter_frame(a, t, t0, t1)
    elif kind == "prints":                                          # no black screens: the cards drop onto the first print, blurred
        it0 = a["items"][len(a["items"]) // 2]; c = blur_bg(it0[0], it0[1]).copy()
        for rid, crop, w, x, y, rot, d, label in a["items"]:
            L.drop(c, pcard(rid, crop, w, rot), x, y, t, t0 + d)
            if label: L.typewriter(c, label, t, t0 + d + 0.35, x, y + pcard(rid, crop, w, rot).height / 2 + 30, size=32, cps=30, anchor="mm", cursor=False)
    elif kind == "letter":
        c = Image.new("RGBA", (W, H), INK + (255,)); rows, foot = LETTERS[a["key"]]; hand_paper(c, t, rows, foot, t0 + 0.4)
    elif kind == "typed":
        c = Image.new("RGBA", (W, H), INK + (255,)); hd, rows, foot = TYPES[a["key"]]; typed_paper(c, t, hd, rows, foot, t0 + 0.4)
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 120, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 230, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 320, t, t0, width=7)
        L.typewriter(c, "NEXT FILE:  FLIGHT 19, 1945", t, T[128] + 0.2, W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
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
    # music beds (Kevin MacLeod, CC BY), about 19-22 dB under the voice (user 22 Oct: music can be higher)
    music("Thunder Dreams.mp3", 0.0, tl(7), -20); music("Floating Cities.mp3", tl(7), tl(18), -21); music("Rising Tide.mp3", tl(18), tl(39), -21)
    music("Man Down.mp3", tl(39), tl(58), -21); music("Thunder Dreams.mp3", tl(58), tl(78), -20); music("Promises to Keep.mp3", tl(78), tl(95), -21)
    music("Rising Tide.mp3", tl(95), tl(110), -21); music("Promises to Keep.mp3", tl(110), tl(114), -21); music("Thunder Dreams.mp3", tl(114), DUR, -20)
    loop("waves_harbor_rocks", tl(7), tl(10), -30); loop("wind_cold_interior", tl(29), tl(39), -32); loop("wind_ambience", tl(50), tl(58), -30)
    loop("waves_with_birds", tl(59), tl(63), -31); loop("wind_scary", tl(69), tl(78), -28); loop("wind_deep_cinematic_hum", tl(78), tl(89), -30)
    loop("waves_rocky_shore", tl(95), tl(100), -30)
    HITS = [("hit_deep_heartbeat_impact", -17), ("hit_short_bass", -19), ("hit_glass_suspense", -21), ("hit_cinematic_deep_impact", -20)]
    for i, (key, (kind, a)) in enumerate(SHOTS):
        t0 = SHOT_T[i]
        if kind in ("card", "tcard"):
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "kbp": sfx("paper_slide", t0, -19); sfx("camera_vintage_shutter", t0 + 0.12, -25)
        elif kind in ("nmap", "pmap", "chart", "cliff"): sfx("paper_page_turn", t0, -22)
        elif kind == "prints":
            for it in a["items"]: sfx("paper_slide", t0 + it[6], -19); sfx("camera_vintage_shutter", t0 + it[6] + 0.1, -25)
        elif kind == "letter":
            sfx("paper_slide", t0, -18)
            for s, k2 in LETTERS[a["key"]][0]:
                if AT(k2) > t0: sfx("paper_writing_pencil", AT(k2), -22, maxlen=1.2)
        elif kind == "typed":
            sfx("paper_slide", t0, -18)
            for s, k2 in TYPES[a["key"]][1]: sfx("typewriter_typing_old", AT(k2), -24, maxlen=1.0)
        elif kind == "counter":
            for k2, s in a["steps"]: sfx("hit_short_bass", AT(k2), -18, maxlen=1.2); sfx("clock_tick_single", AT(k2), -16)
        elif kind == "kb": sfx("whoosh_fast_transition", t0 - 0.1, -32)
        if kind in ("nmap", "pmap"):
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
    EV = [(0, 0.0, "thunder_deep_rumble", -22), (4, "nineteen|1930", "camera_old_shutter_click", -20), (19, "cut", "hit_cinematic_deep_impact", -14),
          (20, "rises", "whoosh_ghostly", -24), (22, "dips|harbor", "water_splash", -22), (23, "beach", "hit_horror_drum", -18), (28, "cloud", "whoosh_tunnel_reverb", -24),
          (31, "buoy", "sea_water_splash", -26), (35, "buoy", "sea_water_splash", -24), (40, "tears", "hit_short_bass", -18), (45, "valves", "whoosh_ghostly", -24),
          (46, "jumped", "hit_cinematic_deep_impact", -14), (55, "moving", "sweep_terror_darkness", -24), (59, 0.2, "ship_hull_creak", -26), (62, "shoots", "hit_short_bass", -18),
          (64, "floating", "water_splash", -26), (75, "crash", "hit_big_cinematic_impact", -14), (75, "water", "sea_water_splash", -22), (84, "home", "clock_tick_single", -14),
          (86, "sets", "sweep_horror_long", -26), (98, "lid", "metal_tool_drop", -22), (101, "pump|works", "gear_metallic_lock", -24), (104, "kodak|eastman", "camera_old_shutter_click", -20),
          (109, "after", "camera_vintage_shutter", -20), (110, 0.3, "clock_bells_hour", -26), (126, "ended", "hit_glass_suspense", -20), (128, 0.2, "typewriter_return_bell", -18)]
    for ln, off, name, db in EV: sfx(name, OT(ln, off), db, maxlen=4.0)
    y += bed; pk = np.max(np.abs(y)); y = y / max(pk, 1e-6) * 0.9
    sf.write(B + "mix_raw.wav", y, sr, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(B + "mix_raw.wav", B + "mix.wav", target=-14, tp=-1); print("audio", AM.measure(B + "mix.wav"))

def seg(i, n):
    a, b = NF * i // n, NF * (i + 1) // n
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "3", "-pix_fmt", "yuv420p", B + f"{SEGP}{i}.mp4"], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(frame(f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("seg done", i, flush=True)
SEGP = "cseg_" if COLOR else "seg_"                    # the colour version keeps its own segments; both share mix.wav
def final(n, name=None):
    name = name or "TheLastHours_07_Andree_Balloon.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
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
        keys = [s[0] for s in SHOTS] + [(ln, off) for ln, off, _, _ in OV] + [k for rows, _ in LETTERS.values() for _, k in rows] + [k for _, rows, _ in TYPES.values() for _, k in rows]
        for s in SHOTS:
            if s[1][0] == "counter": keys += [k for k, _ in s[1][1]["steps"]]
            if s[1][0] == "chart": keys += [p[3] for p in s[1][1]["pins"]]
            if s[1][0] == "cliff": keys += [k for _, k in s[1][1]["marks"] if k != -9]
        for k in keys:
            if isinstance(k, tuple) and isinstance(k[1], str) and wt(k[0], k[1]) is None: print("MISSING", k, "|", LINES[k[0]][:80])
        gaps = [(SHOT_T[i + 1] - SHOT_T[i], i) for i in range(len(SHOTS) - 1)]
        print("shots", len(SHOTS), "longest", sorted(gaps)[-6:], "shortest", sorted(gaps)[:4])
    elif m == "chapters":
        CH = [(0, "The film nobody developed"), (7, "Sunday, 3 AM: the south wind"), (18, "1:46 PM: “Cut everywhere!”"), (29, "Pigeons, buoys, and the long fall"),
              (39, "7:19 AM: down on the ice"), (50, "The march"), (58, "The troll bird"), (69, "Drifting to White Island"), (78, "“Home, 7:05 a.m.”"),
              (89, "33 years"), (95, "August 6, 1930: a lid on the beach"), (104, "The film"), (110, "Home"), (114, "How did they die?")]
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
        if not os.environ.get("LH_KEEP_MIX"): audio()
        final(n)
    elif m == "prep": prep()
