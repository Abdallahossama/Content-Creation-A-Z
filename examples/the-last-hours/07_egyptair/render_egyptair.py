"""The Last Hours #6: EgyptAir 990, 30-31 Oct 1999 (Case File style, 1920x1080). Built on render_roanoke.py.
Every shot starts on a narration line (index into vo_lines.txt without '##'), or on a spoken word in it: key (line, "word").
Line timing comes from the exact-zero gaps in the VO, word timing from whisper (vo/vo_words.json).
  uv run --no-project --with pillow --with numpy --with soundfile python render_egyptair.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines (they cut across the sounds at this scale)
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/07_egyptair/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
HAND = "C:/Windows/Fonts/segoeprb.ttf"                 # hand-printed look for the reconstruction cards
ROMAN = "C:/Windows/Fonts/timesbd.ttf"                 # Roman capitals for the carved-letter reconstructions
LEAD = 0.8; TAIL = 20.0

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = ROOT + "vo/egyptair_vo_chatterbox.wav"
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
COLOR = os.environ.get("LH_COLOR") == "1"                 # the colour version: photos graded like the thumbnails, documents stay paper-toned
DOCS = {f"A{i}" for i in range(1, 17)} | {"B3", "F8", "H10", "H11"}
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
JFK, NANT, SITE, NEWPORT, QUONSET = (-73.778, 40.641), (-70.060, 41.253), (-69.757, 40.348), (-71.359, 41.451), (-71.412, 41.597)
CAIRO, NEWARK, LAX = (31.406, 30.122), (-74.168, 40.690), (-118.408, 33.942)
V_NE, V_SITE, V_WORLD = (-71.6, 40.9, 6.4), (-69.75, 40.8, 2.8), (-45.0, 36.0, 175.0)

# ------------------------------------------------------------------ shot constructors
CROP = {"A1": (0.05, 0.15, 0.95, 0.75), "A2": (0.10, 0.12, 0.92, 0.55), "A3": (0.14, 0.13, 0.76, 0.83), "A4": (0.14, 0.13, 0.80, 0.83),
        "A5": (0.12, 0.04, 0.92, 0.62), "A7": (0.0, 0.04, 0.62, 0.75), "A9": (0.0, 0.04, 0.62, 0.80), "A12": (0.0, 0.05, 1.0, 0.60),
        "A13": (0.0, 0.0, 1.0, 0.60), "A15": (0.0, 0.0, 1.0, 0.55), "B1": (0.09, 0.02, 0.91, 0.88), "B3": (0.03, 0.10, 0.92, 0.88),
        "B4": (0.10, 0.02, 0.90, 0.50), "C2": (0.0, 0.0, 0.90, 1.0), "C4": (0.09, 0.15, 0.91, 0.86), "C5": (0.09, 0.15, 0.91, 0.86),
        "C9": (0.17, 0.09, 0.84, 0.44), "F8": (0.21, 0.13, 0.89, 0.83), "H10": (0.10, 0.10, 0.90, 0.70), "H11": (0.10, 0.45, 0.92, 0.98)}
IL = "ILLUSTRATIVE"
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag, dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag))
def CARD(big, sub): return ("card", dict(big=big, sub=sub))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def TYPED(key): return ("typed", dict(key=key))
def BLACK(): return ("black", {})
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def pr(rid, x, label=None, d=0.1, w=430, rot=-2, y=None): return (rid, CROP.get(rid), w, x, (y or H / 2 - 40), rot, d, label)
def PRINTS(items): return ("prints", dict(items=items))
def D(line, word): return AT((line, word)) - KT(line)

SHOTS = [
 (0, KB("B1", z=(1.0, 1.16), c0=(0.5, 0.5), c1=(0.56, 0.46), tag="A BOEING 767 COCKPIT · NASA")),       # frame 1: the empty cockpit
 (1, KB("E1", z=(1.05, 1.2), tag=IL)),
 (2, TCARD("1:48 AM", "Sunday, October 31, 1999", "E5")),
 (3, NMAP(V_NE, ops=[("pin", *JFK, "NEW YORK JFK", 0.2), ("route", [JFK, (-72.6, 40.45), (-71.0, 40.36), SITE], 0.6, 2.6), ("pin", *SITE, "FLIGHT 990 · 33,000 FT", 3.0)])),
 (4, TYPED("leave")),
 (6, KB("B1", z=(1.15, 1.3), c0=(0.62, 0.55), tag="A BOEING 767 COCKPIT · NASA")),
 (7, KB("E2", z=(1.05, 1.25), tag=IL)),
 (8, TYPED("back")),
 (9, BLACK()),
 (10, KB("A1", z=(1.0, 1.1), c0=(0.5, 0.3), tag="NTSB AIRCRAFT ACCIDENT BRIEF AAB-02/01 · 2002")),
 ((10, "egypt"), KB("H10", z=(1.0, 1.1), c0=(0.5, 0.3), tag="EGYPT'S OWN REPORT (ECAA)")),
 (11, KB("A5", z=(1.0, 1.12), c0=(0.5, 0.6))),
 (12, PRINTS([pr("C3", W / 2 - 560, "THE VOICE RECORDER", D(12, "voice")), pr("C4", W / 2, "THE FLIGHT DATA RECORDER", D(12, "flight"), rot=1.5),
              pr("A11", W / 2 + 560, "THE RADAR", D(12, "radar"), rot=-1)])),
 (13, COUNTER([((13, "clocks"), "1:53")], "REMEMBER THIS TIME", "E5")),
 (14, TCARD("11:30 PM", "Saturday, October 30  ·  Manhattan", "D2")),
 ((15, "plane"), NMAP(V_WORLD, ops=[("pin", *CAIRO, "CAIRO", 0.1), ("route", [CAIRO, (10, 48), (-30, 50), NEWARK], 0.4, 1.8), ("route", [NEWARK, (-96, 41), LAX], 2.2, 1.2),
                                     ("route", [LAX, (-96, 42), JFK], 3.4, 1.2), ("pin", *JFK, "JFK", 4.6)])),
 (16, KB("B2", z=(1.0, 1.12), tag="A BOEING 767-300ER · NOT THE ACCIDENT AIRCRAFT")),
 (17, KB("H1", z=(1.0, 1.1))),
 (18, KB("A13", z=(1.0, 1.1), c0=(0.5, 0.35))),
 (19, COUNTER([((19, 0.0), "1:53"), ((19, "two"), "2:00"), ((19, "fall|back"), "1:00")], "THE CLOCKS FALL BACK AN HOUR", "D1", red=True)),
 (20, KB("A14", z=(1.0, 1.12), c0=(0.5, 0.4))),
 (21, KB("D1", z=(1.0, 1.15))),
 (22, KB("E4", z=(1.0, 1.15), tag=IL)),
 (23, TYPED("evening")),
 (24, TCARD("1:40 AM", "20 minutes after takeoff", "E3")),
 (25, KB("B1", z=(1.1, 1.22), c0=(0.62, 0.55), tag="A BOEING 767 COCKPIT · NASA")),
 (26, TYPED("seat1")),
 (27, KB("E3", z=(1.0, 1.12), tag=IL)),
 (28, TYPED("seat2")),
 (29, KB("B1", z=(1.2, 1.32), c0=(0.65, 0.6), tag="A BOEING 767 COCKPIT · NASA")),
 (30, KB("F8", z=(1.0, 1.1))),
 ((30, "moon"), KB("E1", z=(1.0, 1.12), tag=IL)),
 (31, TYPED("morning")),
 (32, KB("A3", z=(1.0, 1.1))),
 (33, COUNTER([((33, "eighteen|18"), "1:48:18")], "THE DOOR CLOSES", "E5", size=300)),
 (34, KB("B1", z=(1.0, 1.08), c0=(0.5, 0.5), tag="A BOEING 767 COCKPIT · NASA")),
 (35, KB("E6", z=(1.0, 1.15), tag=IL)),
 (36, KB("A7", z=(1.0, 1.12), c0=(0.45, 0.35))),
 (37, KB("E5", z=(1.0, 1.12), tag=IL)),
 ((37, "already"), KB("B1", z=(1.05, 1.15), c0=(0.35, 0.5), tag="A BOEING 767 COCKPIT · NASA")),
 (38, KB("A3", z=(1.1, 1.22), c0=(0.6, 0.5))),
 (39, KB("E6", z=(1.1, 1.25), tag=IL)),
 ((39, "seat"), KB("B1", z=(1.25, 1.4), c0=(0.65, 0.65), tag="A BOEING 767 COCKPIT · NASA")),
 (40, KB("E5", z=(1.15, 1.3), c0=(0.5, 0.45), tag=IL)),
 (41, KB("A7", z=(1.2, 1.32), c0=(0.45, 0.5))),
 (42, KB("E7", z=(1.0, 1.15), tag=IL)),
 (43, KB("A4", z=(1.0, 1.12))),
 (44, KB("A7", z=(1.0, 1.15), c0=(0.45, 0.6))),
 (45, KB("E3", z=(1.15, 1.35), tag=IL)),
 (46, TYPED("return")),
 (47, KB("E5", z=(1.2, 1.4), c0=(0.45, 0.5), tag=IL)),
 (48, KB("A7", z=(1.25, 1.4), c0=(0.45, 0.75))),
 (49, KB("A11", z=(1.0, 1.15))),
 (50, TYPED("noanswer")),
 (51, KB("B3", z=(1.0, 1.12))),
 (52, KB("A10", z=(1.0, 1.15))),
 (53, KB("B3", z=(1.2, 1.35), c0=(0.3, 0.5))),
 (54, KB("E7", z=(1.15, 1.3), tag=IL)),
 (55, KB("E2", z=(1.2, 1.45), tag=IL)),
 (56, TYPED("end")),
 (59, KB("A9", z=(1.0, 1.1), c0=(0.5, 0.4))),
 (60, KB("A9", z=(1.15, 1.3), c0=(0.5, 0.8))),
 (61, KB("A11", z=(1.0, 1.1), c0=(0.6, 0.5))),
 (62, KB("A11", z=(1.15, 1.3), c0=(0.7, 0.45))),
 (63, KB("E2", z=(1.0, 1.25), tag=IL)),
 (64, NMAP(V_SITE, ops=[("pin", *NANT, "NANTUCKET", 0.2), ("pin", *SITE, "01:52:30 · THE CRASH SITE", 0.8), ("circle", *SITE, 4, "", 1.2)])),
 (65, COUNTER([((65, 0.0), "1:52"), ((65, "never"), "1:53")], "THE CLOCKS NEVER REACHED 1:53 AGAIN FOR THEM", "E1", red=True)),
 (66, CARD("2:45", "Autopilot off to the sea")),
 (67, KB("E8", z=(1.0, 1.12), tag=IL)),
 (68, KB("E8", z=(1.2, 1.35), c0=(0.55, 0.5), tag=IL)),
 (69, KB("A12", z=(1.0, 1.12), c0=(0.5, 0.4))),
 ((69, "distress"), KB("A15", z=(1.0, 1.12), c0=(0.5, 0.4))),
 (70, KB("C14", z=(1.0, 1.12), tag="COAST GUARD AIR STATION CAPE COD · 2004")),
 (71, KB("F2", z=(1.0, 1.12))),
 ((71, "seats"), KB("C7", z=(1.0, 1.12), tag="WRECKAGE FROM FLIGHT 990 · FAA")),
 (72, KB("E12", z=(1.0, 1.12), tag=IL)),
 (73, KB("C1", z=(1.0, 1.12))),
 (74, KB("C4", z=(1.0, 1.15))),
 (75, KB("C2", z=(1.0, 1.12))),
 (76, KB("C3", z=(1.0, 1.12))),
 (77, KB("E7", z=(1.05, 1.15), dim=0.3, tag=IL)),                # no black screens > 1.5 s: quotes sit on a dimmed photo (no text under text)
 (78, KB("A9", z=(1.0, 1.1), c0=(0.5, 0.5))),
 (79, KB("C3", z=(1.15, 1.3), c0=(0.55, 0.45))),
 (80, PRINTS([pr("A1", W / 2 - 300, "NTSB  ·  WASHINGTON", 0.1, w=470), pr("H10", W / 2 + 300, "ECAA  ·  CAIRO", 0.6, w=470, rot=2)])),
 (81, KB("A1", z=(1.1, 1.2), c0=(0.5, 0.4))),
 (82, KB("A3", z=(1.0, 1.1))),
 (83, KB("A4", z=(1.1, 1.22), c0=(0.45, 0.5))),
 (84, KB("A10", z=(1.1, 1.22), c0=(0.55, 0.5))),
 (85, KB("B1", z=(1.0, 1.1), c0=(0.5, 0.45), tag="A BOEING 767 COCKPIT · NASA")),
 (86, KB("H10", z=(1.0, 1.1), c0=(0.5, 0.35))),
 (87, KB("E1", z=(1.05, 1.15), dim=0.3, tag=IL)),
 (88, KB("B4", z=(1.0, 1.12))),
 (89, KB("A2", z=(1.0, 1.12))),
 (90, KB("F4", z=(1.0, 1.12))),
 (91, TCARD("MAR 21, 2002", "The final report", "A1")),
 (92, KB("A5", z=(1.05, 1.2), c0=(0.5, 0.7))),
 ((92, "reason"), KB("E2", z=(1.05, 1.15), dim=0.3, tag=IL)),
 (93, KB("H11", z=(1.0, 1.15), c0=(0.5, 0.5))),
 ((93, "evidence"), KB("E11", z=(1.05, 1.15), dim=0.3, tag=IL)),
 (94, KB("B1", z=(1.14, 1.22), c0=(0.5, 0.5), dim=0.3, tag="A BOEING 767 COCKPIT · NASA")),
 (95, KB("B3", z=(1.0, 1.1))),
 (96, KB("E5", z=(1.0, 1.12), tag=IL)),
 ((97, "nine|flight"), KB("C3", z=(1.2, 1.35), c0=(0.5, 0.55))),
 (97, CARD("25 HOURS", "New voice recorders, 2026  ·  Flight 990's: 31 minutes")),
 (98, NMAP(V_NE, ops=[("pin", *SITE, "THE CRASH SITE", -9), ("pin", *NEWPORT, "NEWPORT, R.I.  ·  THE MEMORIAL", 0.4)])),
 ((98, "granite"), KB("D7", z=(1.0, 1.12), tag="BEAVERTAIL LIGHT, ACROSS THE BAY FROM NEWPORT")),
 (99, KB("E12", z=(1.1, 1.25), tag=IL)),
 (100, KB("B1", z=(1.0, 1.12), c0=(0.5, 0.5), tag="A BOEING 767 COCKPIT · NASA")),
 (101, KB("C1", z=(1.1, 1.2))),
 (102, KB("H10", z=(1.0, 1.1), c0=(0.5, 0.4))),
 (103, KB("C4", z=(1.05, 1.2))),
 (104, KB("E1", z=(1.0, 1.1), tag=IL)),
 (105, ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "lower", "EGYPTAIR FLIGHT 990  ·  NEW YORK TO CAIRO  ·  31 OCTOBER 1999"),
 (0, "hundred|107", "typecenter", "107 SECONDS"),
 (1, "lives", "typecenter_red", "217 LIVES LOST"),
 (6, "unlocked", "under", "THE DOOR: UNLOCKED  ·  COMPANY RULE"),
 (7, 0.1, "typecenter", "107 SECONDS LATER"),
 (9, 0.0, "typecenter_red", "NO ANSWER"),
 (12, 0.0, "brand", None),
 (16, "two", "under", "2 CREWS  ·  COMMAND + RELIEF"),
 (17, 0.1, "lower", "SU-GAP, THE ACCIDENT AIRCRAFT  ·  ZURICH, 1991  ·  CC BY 2.0"),
 (17, "203|two", "under", "203 PASSENGERS  ·  14 CREW"),
 (18, 0.1, "lower", "NEW YORK CENTER FLIGHT STRIPS FOR MSR990"),
 (18, "clearance", "typecenter", "1:53 A.M.  ·  DAYLIGHT TIME"),
 (20, 0.0, "typecenter", "1:53 WILL COME AGAIN TONIGHT"),
 (21, 0.1, "lower", "JFK AIRPORT, 1994  ·  USGS"),
 (21, "cabin", "under", "01:19:54  ·  “CABIN CREW, TAKEOFF POSITION.”"),
 (22, "lift", "under", "LIFT-OFF  ·  ABOUT 01:20 A.M."),
 (25, 0.0, "nameplate", ("THE RELIEF FIRST OFFICER", "AGE 59  ·  FORMER AIR FORCE INSTRUCTOR  ·  12,000+ HOURS")),
 (27, 0.0, "typecenter", "THE USUAL SWAP: HOURS LATER"),
 (29, 0.2, "under", "01:42  ·  THE RELIEF FIRST OFFICER IS IN THE RIGHT SEAT"),
 (30, 0.1, "lower", "SATELLITE, 1:45 A.M.  ·  THE CLOUD BELOW THE FLIGHT  ·  NTSB"),
 (32, 0.1, "lower", "FLIGHT DATA, 01:47:40 - 01:48:40  ·  NTSB"),
 (32, "last", "under", "THE LAST TRANSMISSION FROM FLIGHT 990"),
 (34, 0.0, "typecenter", "107 SECONDS"),
 (35, 0.0, "badge", "01:48:30  ·  +12 S"),
 (35, "three", "under", "A 3-SYLLABLE WORD  ·  NEVER IDENTIFIED"),
 (36, 0.0, "badge", "01:48:39  ·  +21 S"),
 (36, 0.1, "lower", "THE COCKPIT VOICE RECORDER TRANSCRIPT  ·  NTSB"),
 (36, "means", "under", "TAWAKKALT ALA ALLAH  =  “I RELY ON GOD”"),
 (37, "nine", "under", "AN EVERYDAY PHRASE  ·  SIMILAR WORDS 9 TIMES EARLIER ON THE TAPE"),
 (38, 0.2, "under", "FLIGHT DATA: LEVEL CRUISE  ·  NOTHING WRONG"),
 (39, "seat", "badge", "01:49:18  ·  +60 S"),
 (39, "seat", "under", "AN ELECTRIC SEAT MOTOR"),
 (40, 0.0, "badge", "01:49:45  ·  +87 S"),
 (40, "autopilot", "typecenter", "AUTOPILOT: OFF"),
 (40, "tone", "under", "NO WARNING TONE  ·  BUTTON PRESSED TWICE"),
 (41, 0.0, "badge", "01:49:48  ·  +90 S"),
 (41, 0.3, "under", "2 OF 11"),
 (42, 0.0, "badge", "01:49:53  ·  +95 S"),
 (42, "idle", "typecenter", "THROTTLES: IDLE"),
 (43, 0.0, "badge", "01:49:54  ·  +96 S"),
 (43, "nose", "typecenter_red", "NOSE DOWN"),
 (44, "seven", "under", "7 MORE TIMES IN 12 SECONDS  ·  “CALM”  ·  “RHYTHMIC” (NTSB)"),
 (45, 0.2, "under", "BELOW ZERO G  ·  WEIGHTLESS"),
 (46, 0.0, "badge", "01:50:06  ·  +108 S  ·  CAPTAIN BACK"),
 (47, 0.0, "badge", "01:50:08"),
 (47, "maximum", "typecenter_red", "OVERSPEED"),
 (47, "warning", "under", "MASTER WARNING  ·  UNTIL THE END"),
 (48, 0.2, "under", "11 OF 11"),
 (49, 0.0, "badge", "01:50:15"),
 (49, "forty|40", "under", "40° NOSE DOWN  ·  39,000 FT A MINUTE"),
 (51, "elevators", "under", "THE ELEVATORS START MOVING NOSE-UP  ·  NTSB: THE CAPTAIN"),
 (52, "twenty|21", "badge", "01:50:21"),
 (52, 0.1, "lower", "FLIGHT DATA: ELEVATORS, ALTITUDE, ENGINES  ·  NTSB"),
 (52, "right", "typecenter_red", "THE ELEVATORS SPLIT"),
 (53, 0.3, "under", "LEFT ELEVATOR = CAPTAIN'S COLUMN  ·  RIGHT = THE RIGHT SEAT"),
 (54, 0.0, "badge", "01:50:21 - 01:50:23"),
 (54, "engines", "typecenter_red", "BOTH ENGINES: CUTOFF"),
 (55, 0.0, "badge", "01:50:23"),
 (55, "mach|mock", "typecenter", "MACH 0.99"),
 (56, 0.0, "badge", "01:50:25"),
 (59, 0.0, "badge", "01:50:36"),
 (59, 0.2, "under", "16,416 FT  ·  THE DIVE IS SLOWING"),
 (60, 0.0, "badge", "01:50:38"),
 (61, 0.1, "lower", "THE FLIGHT PROFILE FROM RADAR  ·  NTSB"),
 (62, 0.2, "under", "CLIMB TO ABOUT 25,000 FT  ·  NO ENGINES  ·  TURNING SOUTHEAST"),
 (63, 0.0, "typecenter_red", "THEN IT FALLS AGAIN"),
 (67, 0.3, "under", "THE CONTROLLER LOOKED AWAY FOR UNDER A MINUTE"),
 (68, "x", "typecenter", "ALTITUDE:  XXXX"),
 (69, 0.0, "badge", "01:54"),
 (69, 0.1, "lower", "NEW YORK CENTER TAPE TRANSCRIPT  ·  FAA / NTSB"),
 (69, "distress", "lower", "NEW YORK CENTER DAILY LOG, 31 OCT 1999"),
 (70, 0.3, "under", "02:11  ·  THE COAST GUARD IS ALERTED"),
 (71, 0.1, "lower", "THE SEARCH AREA, SOUTH OF NANTUCKET  ·  NASA"),
 (71, "seats", "under", "SEATS  ·  LIFE JACKETS  ·  SMALL PIECES  ·  NO BURN MARKS"),
 (72, 0.0, "typecenter", "217 PEOPLE. NO SURVIVORS."),
 (73, 0.1, "lower", "USS GRAPPLE SAILS FOR THE SEARCH  ·  31 OCT 1999  ·  US NAVY"),
 (73, 0.0, "subpop", None),
 (74, 0.1, "lower", "THE FLIGHT DATA RECORDER  ·  NTSB"),
 (74, "ninth", "under", "TUESDAY, NOV 9  ·  RECOVERED"),
 (75, 0.1, "lower", "THE NAVY'S DEEP DRONE  ·  NEWPORT, NOV 1999  ·  US NAVY"),
 (76, 0.1, "lower", "TAGGING THE VOICE RECORDER ON USS GRAPPLE  ·  US NAVY"),
 (75, "230|two", "under", "SAT NOV 13, 10:12 P.M.  ·  FROM ABOUT 230 FT"),
 (76, "leaks", "under", "NOVEMBER 1999  ·  LEAKS TO THE PRESS"),
 (77, 0.0, "quote", ("“I made my decision now.”", "QUOTED IN 1999 PRESS REPORTS")),
 (78, "not", "stamp", ("NOT ON THE TAPE", 1300, 470)),
 (79, "never", "under", "THE FBI NEVER TOOK OVER  ·  THE NTSB LED TO THE END"),
 (81, 0.2, "under", "THE NTSB'S CASE"),
 (82, 0.0, "list", ["NOTHING WRONG BEFORE THE FIRST PHRASE", "AUTOPILOT OFF BY HAND", "THROTTLES: FASTER THAN ANY MACHINE"]),
 (83, 0.2, "under", "28 SECONDS  ·  NO REAL NOSE-UP INPUT  ·  NTSB"),
 (84, 0.2, "under", "SPLIT ELEVATORS  ·  ENGINES OFF"),
 (85, "simulator", "under", "SIMULATOR: EVERY FAILURE RECOVERABLE BY ONE PILOT  ·  NTSB"),
 (86, 0.1, "lower", "EGYPT'S INVESTIGATORS (ECAA)"),
 (87, 0.0, "quote", ("“...would never be used by a person\nwho was about to do an evil deed.”", "ECAA, ON THE PHRASE  ·  RESPONSE TO THE NTSB")),
 (88, 0.1, "lower", "A RECOVERED RIGHT-ELEVATOR ACTUATOR PART  ·  NTSB DOCKET"),
 (88, "rivets", "under", "BROKEN RIVETS  ·  A SHEARED PIN"),
 (89, 0.1, "lower", "NTSB: THE RECORDED ELEVATORS vs A SIMULATED JAM"),
 (89, "americans", "under", "NTSB: NO JAM MATCHED THE RECORDER"),
 (90, 0.3, "under", "UNIDENTIFIED RADAR ECHOES  ·  US AIR FORCE: INTERFERENCE"),
 (92, "reason", "quote", ("“The reason for the relief first officer's\nactions was not determined.”", "NTSB PROBABLE CAUSE  ·  AAB-02/01")),
 (93, "evidence", "quote", ("“...the evidence is not sufficient to identify\none particular set of events as the cause”", "EGYPT (ECAA)  ·  REPORT, SECTION 3.2")),
 (94, 0.0, "list", ["NO NOTE", "NO CONFESSION", "NO PROVEN MOTIVE"]),
 (95, 0.2, "under", "FAA: ELEVATOR RIVET CHECKS ON 767s  ·  2000-2001"),
 (96, 0.2, "under", "2000: NTSB ASKS FOR COCKPIT CAMERAS  ·  2026: STILL NONE"),
 (99, 0.0, "quote", ("“They are not gone from us.”", "EGYPTAIR 990 MEMORIAL  ·  NEWPORT, 2000")),
 (100, 0.2, "under", "01:48  ·  107 SECONDS"),
 (101, "why", "typecenter", "WHAT. NOT WHY."),
 (102, 0.0, "under", "EGYPT: NEVER ACCEPTED"),
 (104, "tell", "under", "WHAT HAPPENED IN THOSE 107 SECONDS?  TELL ME BELOW"),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

LETTERS = {}
H_CVR = "COCKPIT VOICE RECORDER  ·  NTSB TRANSCRIPT (TRANSLATED)"
F_CVR = "NTSB AAB-02/01, APPENDIX B  ·  WORDS FROM THE RECORD, TYPESET BY US  ·  NO AUDIO WAS EVER RELEASED"
TYPES = {
 "leave": (H_CVR, [("01:48:03  CAPTAIN:", (4, "excuse")), ("  EXCUSE ME, [...] WHILE I TAKE A", (4, "excuse")), ("  QUICK TRIP TO THE TOILET...", (4, "toilet")),
                   ("  BEFORE IT GETS CROWDED.", (4, "crowded")), ("01:48:08  RELIEF F/O:", (5, "go")), ("  GO AHEAD PLEASE.", (5, "go"))], F_CVR),
 "back": (H_CVR, [("01:50:06  CAPTAIN:", (8, 0.0)), ("  WHAT'S HAPPENING?", (8, 0.0)), ("  WHAT'S HAPPENING?", (8, "what|asks"))], F_CVR),
 "evening": (H_CVR, [("01:26:35  FIRST OFFICER (RADIO):", (23, 0.0)), ("  NEW YORK, EGYPTAIR NINE NINE", (23, "egypt")), ("  ZERO HEAVY, GOOD EVENING.", (23, "good"))], F_CVR),
 "seat1": (H_CVR, [("01:40:00  RELIEF F/O:", (26, 0.0)), ("  I'M NOT GOING TO SLEEP AT ALL.", (26, "sleep|going"))], F_CVR),
 "seat2": (H_CVR, [("01:40:35  FIRST OFFICER:", (28, 0.0)), ("  IF YOU WANT TO SIT HERE,", (28, "if")), ("  THERE'S NO PROBLEM.", (28, "problem"))], F_CVR),
 "morning": (H_CVR, [("01:47:40  CAPTAIN (RADIO):", (31, 0.0)), ("  NEW YORK, EGYPTAIR, AH, NINE NINE", (31, "egypt")),
                     ("  ZERO HEAVY, GOOD MORNING.", (31, "good"))], F_CVR),
 "return": (H_CVR, [("01:50:06  CAPTAIN:", (46, "captain|back")), ("  WHAT'S HAPPENING?", (46, "what")), ("  WHAT'S HAPPENING?", (46, 2.6))], F_CVR),
 "noanswer": (H_CVR, [("01:50:15  CAPTAIN:", (50, 0.0)), ("  WHAT'S HAPPENING? [...]", (50, 0.0)), ("  WHAT'S HAPPENING?", (50, "asks")), ("  [NO REPLY]", (50, "answer|no"))], F_CVR),
 "end": (H_CVR, [("01:50:25  CAPTAIN: WHAT IS THIS?", (56, 0.0)), ("  WHAT IS THIS? DID YOU SHUT THE ENGINE(S)?", (56, "did")),
                 ("01:50:30  RELIEF F/O: IT'S SHUT.", (57, 0.0)), ("01:50:33  CAPTAIN: PULL WITH ME.", (58, 0.0)),
                 ("01:50:35  CAPTAIN: PULL WITH ME.", (58, 1.6)), ("01:50:37  CAPTAIN: PULL WITH ME.", (58, 3.0))], F_CVR),
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
            L.text(c, "FILE 06  ·  EGYPTAIR 990  ·  OCTOBER 1999", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
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
    elif kind == "chart": c = chart_frame(a, t, t0, t1)
    elif kind == "cliff": c = cliff_frame(a, t, t0, t1)
    elif kind == "counter": c = counter_frame(a, t, t0, t1)
    elif kind == "prints":
        c = Image.new("RGBA", (W, H), INK + (255,))
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
        L.typewriter(c, "NEXT FILE:  THE ANDRÉE BALLOON, 1897", t, T[105] + 0.2, W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
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
    music("Thunder Dreams.mp3", 0.0, tl(14), -20); music("Rising Tide.mp3", tl(14), tl(34), -21); music("Man Down.mp3", tl(34), tl(61), -21)
    music("Thunder Dreams.mp3", tl(61), tl(80), -20); music("Industrial Cinematic.mp3", tl(80), tl(98), -22); music("Rising Tide.mp3", tl(98), DUR, -19)
    loop("wind_cold_interior", tl(30), tl(43), -32); loop("roomtone_dark_cinematic", tl(34), tl(43), -30); loop("wind_scary", tl(43), tl(60), -27)
    loop("alarm_facility", tl(47), tl(60), -37); loop("waves_windy_sea_loop", tl(70), tl(76), -30)
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
            for s, k2 in TYPES[a["key"]][1]: sfx("typewriter_typing_old", AT(k2), -24, maxlen=1.0)
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
    EV = [(0, 0.0, "thunder_deep_rumble", -22), (3, 0.2, "radio_static_crackles", -32), (6, "closes", "heavy_sliding_door", -30), (8, 0.0, "heartbeat_single", -20),
          (9, 0.0, "hit_horror_drum", -18), (13, "clocks", "clock_ticking_closeup", -24), (18, "clearance", "clock_tick_single", -14), (19, "two", "clock_bells_hour", -24),
          (19, "fall|back", "whoosh_tunnel_reverb", -22), (23, 0.2, "radio_static_fx", -30), (31, 0.2, "radio_static_fx", -30), (33, "door|closes", "heavy_sliding_door", -26),
          (35, "three", "heartbeat_slow", -24), (39, "seat", "drill_on_off", -30), (40, "autopilot", "light_switch", -22), (42, "idle", "gear_metallic_lock", -24),
          (43, "nose", "hit_big_cinematic_impact", -16), (45, 0.2, "keys_moving", -24), (47, "warning", "alarm_vintage_warning", -30), (52, "right", "metal_hammer_hit", -20),
          (54, "engines", "hit_short_bass", -16), (58, 0.0, "heartbeat_horror_drum", -20), (60, "stop", "hit_cinematic_deep_impact", -12), (63, 0.0, "sweep_terror_darkness", -22),
          (64, "hits", "water_splash", -20), (69, 0.0, "radio_static_crackles", -28), (72, 0.0, "heartbeat_single", -22), (73, 0.2, "ship_engine_loop", -30),
          (75, "230|two", "sea_water_splash", -24), (91, 0.0, "paper_big_page_turn", -20), (101, "why", "hit_glass_suspense", -20), (105, 0.2, "typewriter_return_bell", -18)]
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
    name = name or ("TheLastHours_06_EgyptAir990_COLOR.mp4" if COLOR else "TheLastHours_06_EgyptAir990.mp4")
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
        CH = [(0, "1:48 AM: the captain steps out"), (14, "11:30 PM: two crews, one late plane"), (18, "1:53 AM, twice: the clocks fall back"),
              (24, "1:40 AM: the early seat change"), (34, "The 107 seconds"), (43, "1:49:54: the dive"), (61, "Radar only"), (67, "Radar contact lost"),
              (73, "The recorders come up"), (80, "Washington vs Cairo"), (95, "What changed, and what's still unknown")]
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
        if not (COLOR and os.path.exists(B + "mix.wav")): audio()
        final(n)
    elif m == "prep": prep()
