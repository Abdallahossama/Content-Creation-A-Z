"""The Last Hours #8: Flight 19 and Training 49, Wednesday 5 December 1945 (Case File style, colour grade, 1920x1080). Built on render_andree.py
(+ the DOC spotlight shot from render_cooper.py, boxes from build/ocr/<rid>.json via ocr_docs.py).
Every shot starts on a narration line (index into vo_lines.txt without '##'), or on a spoken word in it: key (line, "word").
Line timing comes from the exact-zero gaps in the VO, word timing from whisper (vo/vo_words.json).
  uv run --no-project --with pillow --with numpy --with soundfile python render_flight19.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/09_flight19/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 20.0
NEXT = os.environ.get("LH_NEXT", "USS CYCLOPS, 1918")      # the next file named on the end card (user OK 24 Oct)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/flight19_vo_chatterbox.wav")
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
def ORIG(rid):
    for f in sorted(glob.glob(M + rid + "_*")):
        if os.path.isfile(f): return f
    return None
IMG = {}
COLOR = os.environ.get("LH_COLOR", "1") == "1"                 # photos graded like the thumbnails, documents stay paper-toned
def isdoc(rid): return rid[0] == "A" or rid in ("I5", "I6", "I7", "I8", "I13")
def colour(path, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
    a = np.asarray(im, np.float32) / 255; a = np.clip((a - 0.5) * 1.10 + 0.5, 0, 1)
    g = a.mean(2, keepdims=True); a = np.clip(g + (a - g) * 1.15, 0, 1)
    a = a + (1 - g) * 0.10 * np.array([-0.6, 0.15, 0.35]) + g * 0.06 * np.array([0.5, 0.15, -0.4])   # teal shadows, warm highlights
    return Image.fromarray((np.clip(a * 0.94, 0, 1) * 255).astype(np.uint8))
def tone(rid, crop=None, rot=0):
    k = (rid, crop)
    if k not in IMG: IMG[k] = colour(P(rid), crop) if COLOR and not isdoc(rid) else L.bw(P(rid), crop)
    return IMG[k]

def prep():
    for f in glob.glob(M + "*"):
        rid = os.path.basename(f).split("_")[0]
        if os.path.exists(B + f"_small_{rid}.png"): continue
        try: im = Image.open(f)
        except Exception: continue
        if max(im.size) > 4200:
            im = im.convert("RGB"); k = 4200 / max(im.size); im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS).save(B + f"_small_{rid}.png")

# documents: paper-toned full pages + OCR line boxes (page pixels of the ORIGINAL scan)
OCR = {}
def ocr(rid):
    if rid not in OCR:
        f = B + f"ocr/{rid}.json"; OCR[rid] = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []
    return OCR[rid]
def nrm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def ob(rid, q):
    """box of OCR rows: '12+13' = row indices (<= 3 digits), other fragments = normalized substring; a tuple = a box by hand (page px)"""
    if isinstance(q, tuple): return q
    rows = ocr(rid); bx = []
    for fr in q.split("+"):
        if fr.isdigit() and len(fr) <= 3:
            if int(fr) < len(rows): bx.append(rows[int(fr)]["box"])
            continue
        n = nrm(fr); hit = next((r for r in rows if n and n in nrm(r["text"])), None)
        if hit: bx.append(hit["box"])
    if not bx: return None
    return (min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx))
def page_img(rid):
    k = ("doc", rid)
    if k not in IMG:
        im = Image.open(ORIG(rid)).convert("L"); s = min(1.0, 3200 / im.height)
        if s < 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        a = np.asarray(im, np.float32); lo, hi = np.percentile(a, 1), np.percentile(a, 99.5)
        a = np.clip((a - lo) / max(hi - lo, 1), 0, 1); IMG[k] = (Image.fromarray((a[..., None] * np.array([236, 230, 214], np.float32)).astype(np.uint8)), s)
    return IMG[k]

# map points (lon, lat)
FLL, HC, T1, T2, END3 = (-80.117, 26.05), (-79.08, 26.03), (-77.84, 26.01), (-78.17, 27.19), (-80.12, 26.23)
KEYS, MIAMI, MIAMI_S = (-81.0, 24.75), (-80.19, 25.77), (-80.30, 25.40)
FIX, BR, PBMX, NSB = (-79.0, 29.25), (-80.608, 28.235), (-80.417, 28.983), (-80.927, 29.026)
GULF, GBI, DEEP91 = (-84.6, 26.2), (-78.45, 26.72), (-79.98, 26.18)
T2_PART = (-77.95, 26.55)
V_WIDE, V_ROUTE, V_KEYS = (-81.0, 26.9, 12.5), (-78.9, 26.5, 4.6), (-79.7, 25.9, 7.5)
V_FIX, V_PBM, V_FLL = (-79.4, 28.6, 12.0), (-80.6, 28.62, 2.6), (-80.0, 26.2, 3.0)

# ------------------------------------------------------------------ shot constructors
CROP = {"B1": (0.0, 0.05, 0.955, 0.97), "B5": (0.03, 0.03, 0.965, 0.93), "C1": (0.05, 0.03, 0.95, 0.965), "I17": (0.02, 0.02, 0.98, 0.98), "F6": (0.0, 0.0, 0.93, 1.0)}
TB1 = "TBF-1 AVENGERS OFF FORT LAUDERDALE, 1943  ·  SAME TYPE, NOT FLIGHT 19"
TB3 = "FIVE TBF-1 AVENGERS, 1942  ·  SAME TYPE, NOT FLIGHT 19"
TB4 = "TBM-3 AVENGERS OF VT-6 (USS HANCOCK), 1945"
TB5 = "TBM AVENGERS, LATE 1940s  ·  SAME TYPE"
TB6 = "A PBM-5 MARINER, c. 1945  ·  SAME TYPE AS TRAINING 49"
TB7 = "PBM MARINERS AT NAS BANANA RIVER, 1943"
TB8 = "A PBM AT NAS BANANA RIVER, 1943"
TC1 = "LT. CHARLES C. TAYLOR, 1941  ·  NHHC NH 84038"
TD1 = "USS SOLOMONS (CVE-67), 1943"
TSAT = "NASA SATELLITE IMAGE (MODERN)"
TF5 = "FLORIDA AT NIGHT, 2016 (MODERN LIGHTS)  ·  NASA"
TCHART = "NOAA NAUTICAL CHART (MODERN)"
DT = {"A1": "BOARD OF INVESTIGATION  ·  RECORD OF PROCEEDINGS, 10 DEC 1945  ·  NARA", "A2": "NAS FORT LAUDERDALE FORECAST, 11 A.M., 5 DEC 1945  ·  NARA",
      "A3": "WINDS ALOFT, 1 P.M., 5 DEC 1945  ·  NARA", "A4": "NAVIGATION PROBLEM No. 1  ·  BOARD ENCLOSURE 1  ·  NARA", "I9": "NAVIGATION PROBLEM No. 1  ·  BOARD ENCLOSURE 1  ·  NARA",
      "I13": "ACCIDENT CARD, ENS. J. T. BOSSI (FT-3)  ·  NHHC",
      "A13": "NAS FORT LAUDERDALE ROUGH CRASH LOG  ·  NARA", "A14": "NAS FORT LAUDERDALE ROUGH CRASH LOG  ·  NARA", "A15": "NAS FORT LAUDERDALE ROUGH CRASH LOG  ·  NARA",
      "I5": "NAS FORT LAUDERDALE ROUGH CRASH LOG  ·  NARA", "A16": "COAST GUARD RADIO STATION PENSACOLA  ·  LOG, 5 DEC 1945  ·  NARA",
      "A17": "COAST GUARD RADIO STATION PENSACOLA  ·  LOG, 5-6 DEC 1945  ·  NARA", "A18": "TESTIMONY OF LT. ROBERT F. COX  ·  BOARD RECORD  ·  NARA",
      "A19": "TESTIMONY OF LT. ROBERT F. COX  ·  BOARD RECORD  ·  NARA", "A29": "ENDORSEMENT, REAR ADM. R. E. DAVISON, 24 JAN 1946  ·  NARA",
      "A30": "ENDORSEMENT, REAR ADM. F. D. WAGNER, 15 FEB 1946  ·  NARA", "A31": "CHIEF OF NAVAL OPERATIONS, 28 DEC 1945  ·  NARA",
      "I8": "NARA MICROFILM M1657, TITLE CARD (2001)"}
for _r in ("A6", "A7", "A8", "A9", "A10", "A11", "A12"): DT[_r] = "AIR SEA RESCUE TASK UNIT 4, PORT EVERGLADES  ·  RADIO LOG, 5 DEC 1945  ·  NARA"
for _r in ("A5", "A20", "A21", "A22", "A23"): DT[_r] = "BOARD OF INVESTIGATION  ·  FINDINGS OF FACT  ·  NARA"
for _r in ("A24", "A25", "A26", "A27", "A28"): DT[_r] = "BOARD OF INVESTIGATION  ·  OPINIONS  ·  NARA"
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag, dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT.get(rid)))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag))
LAST = "1904+lasttransmissions+t28noanswer"                    # the crash-log line, 7:04 p.m.

SHOTS = [
 (0, KB("B3", z=(1.0, 1.12), c0=(0.5, 0.45), tag=TB3)),                                  # frame 1: five Avengers
 ((0, "navy"), KB("F2", z=(1.0, 1.1), tag=TSAT)),
 ((0, "nobody"), KB("E2", z=(1.05, 1.15), dim=0.1)),
 (1, TCARD("7:04 PM", "Wednesday, December 5, 1945", "E1")),
 (2, KB("B1", z=(1.0, 1.1), tag=TB1)),
 ((2, "crash|log"), DOC("A13", [("0", (2, "crash|log")), (LAST, 3)])),
 (4, KB("B3", z=(1.15, 1.3), c0=(0.45, 0.62), tag=TB3)),
 ((4, "eighty|80"), KB("E3", z=(1.0, 1.1), dim=0.1)),
 (5, KBP("I8")),
 (6, DOC("A6", [("0+1+2", (6, "radio|navy")), ("9+10", (6, "line"))])),
 (7, NMAP(V_WIDE, ops=[("pin", *FLL, "FORT LAUDERDALE", 0.1), ("label", -77.6, 29.0, "?", 0.5, 130)])),
 ((7, "knew"), KB("F5", z=(1.0, 1.08), tag=TF5)),
 ((7, "famous"), KB("E3", z=(1.1, 1.2))),
 (8, KB("F3", z=(1.0, 1.08), tag=TSAT)),
 ((8, "showers"), DOC("A2", [("14+15+16", (8, "showers")), ("30+35+36", (8, "flying"))])),
 (9, KB("E3", z=(1.0, 1.1))),
 (10, DOC("A3", [("37+38+39+42+43+44", (10, "thirty|30"))])),
 ((10, "flying"), NMAP(V_ROUTE, ops=[("pin", *FLL, "FORT LAUDERDALE", 0.0), ("arrow", (-80.0, 25.55), (-78.3, 26.25), "WIND FROM THE WSW · 30-52 KNOTS ALOFT", 0.3)])),
 (12, KB("I17", z=(1.0, 1.08), c0=(0.5, 0.40), tag=TC1)),
 ((12, "hours"), DOC("A20", [("40+41+42", (12, "hours"))])),
 ((12, "combat"), KB("B4", z=(1.0, 1.1), tag=TB4)),
 (13, KB("I17", z=(1.25, 1.4), c0=(0.5, 0.27), tag=TC1)),
 (14, DOC("A20", [("12+13+14+15+16+17", 14)])),
 ((14, "nine|9"), DOC("A20", [("23+24+25+26+27+28+29+30+31+32+33", (14, "nine|9"))])),
 (15, KB("B5", z=(1.0, 1.1), tag=TB5)),
 ((15, "navigation"), KBP("I9", rot=1.0)),
 ((15, "triangle"), NMAP(V_ROUTE, ops=[("pin", *FLL, "FORT LAUDERDALE", 0.0), ("route", [FLL, HC, T1, T2, END3, FLL], 0.3, 3.0)])),
 (16, NMAP(V_ROUTE, ops=[("pin", *FLL, "FORT LAUDERDALE", -9), ("route", [FLL, HC], 0.0, 0.8), ("pin", *HC, "HENS AND CHICKENS SHOAL · BOMBING", 0.8),
                         ("route", [HC, T1], 1.4, 0.8), ("route", [T1, T2], 2.2, 0.8), ("label", *GBI, "GRAND BAHAMA", 2.6, 30), ("route", [T2, END3], 3.2, 1.0)])),
 (17, KB("B2", z=(1.0, 1.1), c0=(0.5, 0.55), tag=TB1)),
 ((17, "clock"), KB("B2", z=(1.6, 1.8), c0=(0.37, 0.45), tag=TB1)),
 (19, TCARD("2:10 PM", "Wednesday, December 5, 1945", "B1")),
 ((19, "five"), KB("B1", z=(1.0, 1.12), tag=TB1)),
 ((19, "student"), DOC("A20", [("36+37+38+39", (19, "student"))])),
 (20, NMAP(V_ROUTE, ops=[("pin", *FLL, "", -9), ("route", [FLL, HC], 0.1, 1.2), ("pin", *HC, "~3 PM · PRACTICE BOMBS", 1.3)])),
 (21, NMAP(V_ROUTE, ops=[("pin", *FLL, "", -9), ("route", [FLL, HC], -9, 0.01), ("route", [HC, T1, T2_PART], 0.1, 1.6), ("label", T2_PART[0] + 0.5, T2_PART[1], "?", 1.8, 90)])),
 (22, TCARD("3:40 PM", "Lt. Robert Cox, near the base", "B4")),
 (23, DOC("A18", [("3+4+5", 23), ("6+7", (23, "compass"))])),
 (24, DOC("A18", [((496, 1440, 2610, 1562), 24)])),
 (25, DOC("A18", [("10+11", 25)])),
 (26, KB("I17", z=(1.0, 1.1), dim=0.1, tag=TC1)),
 (27, DOC("A18", [("14+15", 27), ("16+17", (27, "sure"))])),
 (28, NMAP(V_KEYS, ops=[("pin", *FLL, "FORT LAUDERDALE", -9), ("pin", *KEYS, "THE FLORIDA KEYS · WHERE HE THOUGHT HE WAS", 0.3, -40, 50),
                        ("pin", *T2_PART, "THE BAHAMAS · WHERE HE WAS", 2.2)])),
 (29, DOC("A18", [("19+20", 29)])),
 (30, DOC("A18", [("21+22", 30)])),
 (31, KB("E3", z=(1.0, 1.08), dim=0.25)),
 (32, KB("E2", z=(1.0, 1.1), dim=0.15)),
 ((32, "bestseller"), KB("E1", z=(1.0, 1.08), dim=0.1)),
 (33, NMAP(V_KEYS, ops=[("pin", *FLL, "", -9), ("arrow", FLL, MIAMI_S, "COX: SOUTH", 0.2), ("arrow", (-78.1, 26.8), (-78.0, 27.8), "TAYLOR: NORTH?", 1.4)])),
 (34, DOC("A18", [((494, 3650, 2742, 3780), 34)])),
 (35, DOC("A6", [("0+1+2", 35)])),
 (36, DOC("A6", [("6+7+8+9+10", 36)])),
 (37, DOC("A6", [("25+26+27+28+29", 37)])),
 (38, DOC("A6", [("30+31+32+33", 38)])),
 (39, DOC("A6", [("39+40+41+42", 39), ("43+44+45+46", (39, "far"))])),
 (40, KB("B3", z=(1.1, 1.2), tag=TB3)),
 (41, DOC("A6", [("47+48+49+50", 41)])),
 (42, NMAP(V_KEYS, ops=[("pin", *FLL, "FLORIDA", -9), ("arrow", (-77.9, 26.8), (-80.0, 26.8), "270° = DUE WEST", 0.2)])),
 (43, KB("B1", z=(1.15, 1.25), tag=TB1)),
 (44, DOC("A7", [("19+20+21+22", 44)])),
 (45, NMAP(V_WIDE, ops=[("label", *GULF, "GULF OF MEXICO", 0.2, 40), ("pin", *FLL, "FORT LAUDERDALE", -9), ("pin", *T2_PART, "THE FLIGHT", -9)])),
 (46, DOC("A25", [("0+1+2", 46)])),
 (47, DOC("A22", [("0+1+2", (47, "four|4|direction"))])),
 (48, DOC("A7", [("0+1+2+3+4", 48)])),
 (49, KB("B5", z=(1.05, 1.18), tag=TB5)),
 (50, DOC("A16", [("2", 50), ("24", (50, "all"))])),
 (51, DOC("A7", [("46+47+48", 51)])),
 (52, DOC("A16", [("27+28+29", 52)])),
 (53, KB("B2", z=(1.6, 1.75), c0=(0.37, 0.45), tag=TB1)),
 (54, DOC("A8", [("5+6+7+8", (54, "lauderdale|ready"))])),
 (55, DOC("A19", [("3+4+5", 55), ("6+7", (55, "very|definitely"))])),
 (56, DOC("A8", [("9+10+11", 56)])),
 (57, DOC("A8", [("12+13+14", 57)])),
 (58, NMAP(V_KEYS, ops=[("pin", *FLL, "FLORIDA", -9), ("arrow", (-77.6, 27.6), (-79.6, 27.6), "WEST", 0.1)])),
 (59, DOC("A16", [("42", (59, "pensacola|again")), ("43", (60, "gallons|ten"))])),
 (61, KB("E3", z=(1.0, 1.12))),
 (62, TCARD("5:29 PM", "Sunset at Fort Lauderdale", "E2")),
 (63, KB("E2", z=(1.0, 1.1), dim=0.15)),
 (64, DOC("A8", [("24+25+26", 64)])),
 (65, DOC("A8", [("15+16+17+18", 65), ("31+32+33+34", (65, "rescue"))])),
 (66, DOC("A25", [("3+4+5", 66)])),
 (67, KB("F1", z=(1.0, 1.08), tag=TSAT)),
 (68, DOC("A22", [("0+1+2", 68)])),
 (69, NMAP(V_FIX, ops=[("pin", *FLL, "FORT LAUDERDALE", -9), ("circle", *FIX, 100, "5:50 PM · WITHIN 100 MILES", 0.3)])),
 (70, NMAP(V_FIX, ops=[("pin", *FLL, "HOME", -9), ("circle", *FIX, 100, "", -9), ("pin", *FIX, "29°15'N 79°00'W", 0.1), ("route", [FLL, FIX], 0.6, 1.2),
                       ("label", -80.1, 27.7, "231 MILES", 1.6, 36)])),
 (71, DOC("A29", [("21+22+23", (71, "navy|review"))])),
 (72, DOC("A22", [("6+7", 72), ("8+9", (72, "thirty|36|teletype"))])),
 (73, DOC("A25", [("16+17+18", 73)])),
 (74, KB("B1", z=(1.1, 1.2), dim=0.2, tag=TB1)),
 (75, DOC("A9", [("14+15", 75)])),
 (76, DOC("A9", [("16+17", 76)])),
 (77, DOC("A16", [("65", 77), ("68+69", (77, "over|gulf"))])),
 (78, DOC("A16", [("70+71+72", 78)])),
 (79, NMAP(V_WIDE, ops=[("label", *GULF, "WHERE HE THINKS HE IS", 0.1, 36), ("arrow", (-84.5, 27.3), (-82.3, 27.3), "EAST = LAND", 0.5)])),
 (80, NMAP(V_FIX, ops=[("circle", *FIX, 100, "", -9), ("arrow", FIX, (-76.6, 29.25), "EAST = OPEN ATLANTIC", 0.2)])),
 (81, KB("B3", z=(1.2, 1.3), c0=(0.5, 0.3), tag=TB3)),
 (82, DOC("A26", [("15+16+17", 82)])),
 (83, DOC("A26", [("18", 83)])),
 (84, DOC("A9", [("35+36", 84)])),
 (85, KB("B7", z=(1.0, 1.1), tag=TB7)),
 ((85, "thirteen|13"), KB("B8", z=(1.0, 1.12), c0=(0.55, 0.45), tag=TB8)),
 (86, DOC("A9", [("42+43", 86)])),
 (87, DOC("A14", [("56", 87), ("61", (87, "bossi|bossy|joseph"))])),
 ((87, "twenty|20"), KBP("I13", h=760, rot=1.5)),
 (88, TCARD("7:04 PM", "The last transmission", "E1")),
 ((88, "crash|log"), DOC("A13", [(LAST, (88, "last"))])),
 (89, DOC("A17", [("39", 89)])),
 ((89, "until|almost"), KB("E1", z=(1.0, 1.08), dim=0.3)),
 (91, DOC("A26", [("19+20", 91), ("21+22", (91, "rough"))])),
 (92, KB("F5", z=(1.0, 1.1), tag=TF5)),
 (93, KB("B6", z=(1.0, 1.12), tag=TB6)),
 ((93, "thirteen|13"), KB("B6", z=(1.35, 1.5), c0=(0.32, 0.5), tag=TB6)),
 (94, KB("B9", z=(1.0, 1.1), tag=TB8)),
 ((94, "volunteered"), DOC("A28", [("19+20+21+22", (94, "volunteered"))])),
 (95, DOC("A22", [("24+25+26", 95)])),
 (96, TCARD("7:50 PM", "Off New Smyrna Beach", "E2")),
 ((96, "tanker|gaines"), DOC("A10", [("35+36+37+38", (96, "tanker|gaines"))])),
 (97, KB("D1", z=(1.0, 1.1), tag=TD1)),
 ((97, "exact"), NMAP(V_PBM, ops=[("pin", *BR, "NAS BANANA RIVER", -9), ("pin", *NSB, "NEW SMYRNA BEACH", -9), ("route", [BR, PBMX], 0.0, 1.0),
                                  ("pin", *PBMX, "7:50 PM · FLAMES 100 FT HIGH", 1.0, 26, 40)])),
 (98, DOC("A10", [("44+45+46+47+48+49", 98)])),
 (99, KB("B6", z=(1.1, 1.2), c0=(0.45, 0.5), dim=0.3, tag=TB6)),
 (100, DOC("A28", [("26+27+28", (100, "board|exploded"))])),
 (101, COUNTER([(101, "27")], "MEN  ·  6 PLANES  ·  ONE NIGHT", "B3", red=True)),
 (102, KBP("I5")),
 (103, COUNTER([((103, "two|248"), "248")], "NAVY PLANES ORDERED UP  ·  AP, 7 DEC 1945", "B1")),
 ((103, "eighteen|18"), KB("D2", z=(1.0, 1.1), tag=TD1)),
 (104, DOC("A14", [("14", 104)])),
 ((104, "two|raft"), DOC("A15", [("26", (104, "two|raft")), ((960, 2650, 2640, 2830), (104, "false"))])),
 (105, DOC("A15", [("67", (105, "search|secured"))])),
 (106, KB("I17", z=(1.0, 1.08), dim=0.2, tag=TC1)),
 (107, DOC("A1", [("0+1+2+3", 107)])),
 (108, DOC("A26", [("25+26", 108), ("30+31", (108, "radio")), ("32+33+34", (108, "switch")), ("35+36", (108, "teletype|broken"))])),
 (109, DOC("A27", [("37+38", (109, "temporary|confusion"))])),
 (110, DOC("A30", [("10", (110, "hopelessly|writes")), ("11", (110, "akin|something|mental"))])),
 (111, KB("I17", z=(1.0, 1.08), dim=0.15, tag=TC1)),
 (112, KB("I17", z=(1.05, 1.12), c0=(0.5, 0.35), dim=0.4, tag=TC1)),
 (113, KB("I17", z=(1.2, 1.35), c0=(0.5, 0.28), tag=TC1)),
 (114, KB("B2", z=(1.05, 1.15), dim=0.3, tag=TB1)),
 (115, KB("B4", z=(1.0, 1.1), tag=TB4)),
 (116, KBP("I8")),
 (117, KB("E1", z=(1.0, 1.1))),
 (118, KB("E3", z=(1.0, 1.15), dim=0.2)),
 (119, KB("E3", z=(1.2, 1.3), c0=(0.4, 0.6), dim=0.15)),
 (120, DOC("A19", [("30+31+32", (120, "covered|white|whitecaps"))])),
 (121, KB("F1", z=(1.0, 1.1), tag=TSAT)),
 ((121, "years"), KB("E3", z=(1.05, 1.15), dim=0.1)),
 (122, KB("E3", z=(1.0, 1.1), dim=0.1)),
 (123, KB("B3", z=(1.0, 1.1), dim=0.1, tag=TB3)),
 (124, KB("F6", z=(1.0, 1.08), tag=TCHART)),
 ((124, "noaa|noah"), KB("F1", z=(1.1, 1.2), c0=(0.55, 0.5), tag=TSAT)),
 (125, NMAP(V_FLL, ops=[("pin", *FLL, "FORT LAUDERDALE", -9), ("pin", *DEEP91, "MAY 1991 · 5 AVENGERS · 600-750 FT DOWN", 0.4)])),
 ((125, "shows|twenty|28"), KB("B4", z=(1.05, 1.18), c0=(0.35, 0.55), tag=TB4)),
 (126, KB("B1", z=(1.1, 1.2), tag=TB1)),
 (127, KB("B5", z=(1.0, 1.1), dim=0.2, tag=TB5)),
 (128, KB("B4", z=(1.1, 1.2), tag=TB4)),
 (129, KB("F4", z=(1.0, 1.1), tag=TSAT)),
 (130, KB("F5", z=(1.0, 1.08), tag=TF5)),
 (131, NMAP(V_FIX, ops=[("pin", *FLL, "HOME", -9), ("circle", *FIX, 100, "200 MILES ACROSS", 0.2), ("label", -77.3, 27.6, "?", 1.0, 110)])),
 (132, KB("E1", z=(1.0, 1.1), dim=0.1)),
 (133, KB("B2", z=(1.6, 1.75), c0=(0.37, 0.45), tag=TB1)),
 (134, KB("B7", z=(1.05, 1.15), tag=TB7)),
 (135, DOC("A13", [(LAST, (135, "one|line"))])),
 (136, KB("B3", z=(1.0, 1.12), tag=TB3)),
 ((136, "circle"), NMAP(V_FIX, ops=[("pin", *FLL, "HOME", -9), ("circle", *FIX, 100, "", 0.0)])),
 (137, ("names", {})),
 (139, ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "lower", "FLIGHT 19  ·  FIVE NAVY AVENGERS  ·  FOURTEEN MEN"),
 (0, "navy", "typecenter", "BY 6 P.M., THE NAVY KNEW"),
 (0, "nobody", "typecenter_red", "NOBODY TOLD THEM"),
 (4, "eighty|80", "typecenter", "NOT ONE PIECE FOUND"),
 (5, "bermuda", "under", "“THE BERMUDA TRIANGLE”: A NAME FIRST USED IN 1964"),
 (7, "where", "under", "WHERE THEY REALLY WERE"),
 (7, "knew", "under", "WHAT THE NAVY KNEW BY 6 P.M."),
 (7, "famous", "under", "AND WHICH “LAST WORDS” WERE MADE UP IN 1962"),
 (8, 0.0, "badge", "11:00 AM"),
 (8, 0.2, "brand", None),
 (9, 0.0, "under", "MYTH: A CALM, PERFECT DAY"),
 (9, "forecast", "stamp", ("SHOWERS · ROUGH SEA", 1240, 400)),
 (11, 0.0, "typecenter", "REMEMBER THE WIND"),
 (12, 0.2, "nameplate", ("LT. CHARLES C. TAYLOR", "28  ·  USNR  ·  FLIGHT LEADER AND INSTRUCTOR")),
 (13, 0.2, "under", "AT NAS FORT LAUDERDALE SINCE NOV 21  ·  FIRST TIME LEADING THIS ROUTE"),
 (15, 0.0, "under", "MYTH: “THE LOST PATROL”"),
 (15, "training", "stamp", ("A TRAINING FLIGHT", 1260, 380)),
 (15, "back|five", "under", "ABOUT 360 MILES  ·  BACK BY 5:23 P.M."),
 (17, 0.2, "under", "FULL TANKS  ·  LIFE RAFTS"),
 (17, "clock", "typecenter", "NO COCKPIT CLOCKS"),
 (18, 0.0, "typecenter", "REMEMBER THE CLOCKS"),
 (19, "five", "under", "5 AVENGERS  ·  5 PILOTS, 9 CREW  ·  6 NAVY, 8 MARINES"),
 (20, 0.0, "badge", "~3:00 PM"),
 (22, 0.0, "badge", "3:40 PM"),
 (26, 0.0, "badge", "~4:00 PM"),
 (26, 0.3, "under", "AS LT. COX TOLD THE BOARD, UNDER OATH"),
 (31, 0.0, "quote", ("“I'm coming to meet you anyhow.”", "LT. ROBERT COX, AS HE TOLD THE BOARD")),
 (32, 0.0, "under", "MYTH: “DON'T COME AFTER ME” WAS MADE UP"),
 (32, "real", "stamp", ("IT'S REAL", 1300, 420)),
 (32, "bestseller", "typecenter", "1974: A FEW WORDS ADDED"),
 (35, 0.0, "badge", "4:21 PM"),
 (37, 0.0, "badge", "4:25 PM"),
 (38, 0.0, "badge", "4:26 PM"),
 (39, 0.0, "badge", "4:28 PM"),
 (40, 0.0, "badge", "4:31 PM"),
 (40, 0.2, "under", "WHAT ONE OF THE STUDENTS THOUGHT"),
 (42, "remember", "typecenter", "REMEMBER THAT STUDENT"),
 (43, 0.0, "typecenter", "WHY DON'T THEY TURN WEST?"),
 (44, 0.0, "badge", "4:45 PM"),
 (47, "four|4|direction", "badge", "4:47 PM"),
 (49, 0.0, "typecenter", "REMEMBER THE READY PLANE"),
 (50, 0.0, "badge", "5:04 PM"),
 (51, 0.0, "badge", "5:07 PM"),
 (52, 0.0, "badge", "5:09 PM"),
 (53, 0.2, "under", "NO COCKPIT CLOCKS IN ANY OF THE FIVE PLANES"),
 (56, 0.0, "badge", "5:15 PM"),
 (57, 0.0, "badge", "5:16 PM"),
 (58, 0.0, "typecenter", "WEST, AT LAST"),
 (59, 0.0, "badge", "5:24 PM"),
 (61, 0.2, "under", "A DITCHING, ALL TOGETHER, IN A ROUGH SEA"),
 (63, 0.0, "under", "MYTH: “TEN GALLONS” WAS THE LAST MESSAGE"),
 (63, "log", "stamp", ("5:24 P.M.", 1300, 400)),
 (63, "hour", "typecenter", "1 HOUR 40 MINUTES STILL TO COME"),
 (64, 0.0, "badge", "5:30 PM"),
 (67, 0.0, "typecenter", "WHAT THE NAVY KNEW"),
 (69, 0.0, "badge", "5:50 PM"),
 (72, 0.0, "badge", "6:10 PM"),
 (72, "thirty|36|teletype", "badge", "6:36 PM"),
 (74, 0.0, "typecenter_red", "THE MEN IN THE AIR NEVER HEARD IT"),
 (75, 0.0, "badge", "6:04 PM"),
 (81, 0.0, "under", "4:31 P.M.: “IF WE WENT 270 WE COULD HIT LAND”"),
 (82, 0.0, "badge", "6:06 PM"),
 (84, 0.0, "badge", "6:24 PM"),
 (85, "thirteen|13", "under", "13 MEN WILL TAKE OFF IN ONE OF THEM"),
 (86, 0.0, "badge", "6:44 PM"),
 (89, 0.0, "badge", "7:46-9:56 PM"),
 (90, 0.0, "typecenter", "NO REPLY"),
 (92, 0.2, "under", "NO WRECKAGE  ·  NO RAFT  ·  NONE OF THE 14 MEN  ·  1945 TO TODAY"),
 (93, 0.0, "badge", "7:27 PM"),
 (93, 0.3, "under", "PBM-5 MARINER, BuNo 59225  ·  “TRAINING 49”  ·  13 MEN"),
 (94, 0.1, "nameplate", ("LT. (JG) WALTER G. JEFFREY", "PATROL PLANE COMMANDER  ·  1,917.8 HOURS")),
 (95, 0.0, "badge", "7:30 PM"),
 (97, 0.2, "under", "ITS RADAR SAW THE PLANE VANISH AT THAT SPOT"),
 (99, 0.0, "under", "MYTH: THE RESCUE PLANE VANISHED WITHOUT A TRACE"),
 (99, "flames", "list", ["FLAMES", "OIL", "RADAR"]),
 (102, 0.0, "badge", "THU 6 DEC"),
 (104, 0.0, "badge", "FRI 7 DEC"),
 (104, "two|raft", "badge", "SUN 9 DEC"),
 (105, 0.0, "badge", "MON 10 DEC"),
 (105, "secured", "subpop", None),
 (106, 0.0, "typecenter", "ONE MAN BLAMED"),
 (107, 0.0, "badge", "10 DEC 1945"),
 (110, 0.0, "badge", "15 FEB 1946"),
 (111, 0.2, "under", "HIS MOTHER, KATHERINE TAYLOR, A SCHOOLTEACHER IN TEXAS"),
 (112, 0.0, "list", ["A $1,000 REWARD", "200+ LETTERS", "A NEW NAVY REVIEW BOARD"]),
 (113, 0.0, "typecenter", "1947: CAUSE UNKNOWN"),
 (114, 0.0, "under", "MYTH: “GUILTY OF A MENTAL ABERRATION”"),
 (114, "trial", "list", ["NOT A TRIAL", "NOT THE BOARD'S WORDS", "CLEARED IN 1947"]),
 (115, 0.2, "under", "1991: “WE FOUND THEM”"),
 (116, 0.2, "under", "EVEN NARA'S 2001 MICROFILM TITLE USES THE NAME"),
 (117, 0.2, "under", "1950  ·  AP: “SEA'S PUZZLES STILL BAFFLE MEN IN PUSHBUTTON AGE”"),
 (118, 0.0, "under", "1962  ·  A MAGAZINE STORY"),
 (118, "entering|white", "quote", ("“We are entering white water...\nWe're completely lost.”", "INVENTED IN 1962  ·  NOT IN ANY LOG OR TESTIMONY")),
 (119, 0.0, "stamp", ("NOT IN THE RECORD", 1260, 400)),
 (119, "kusche|larry|kooshee", "under", "LARRY KUSCHE: “FICTIONALIZED, DRAMATIZED MESSAGES”"),
 (121, 0.0, "typecenter", "1964: “THE BERMUDA TRIANGLE”"),
 (121, "years", "under", "VINCENT GADDIS, ARGOSY  ·  19 YEARS AFTER FLIGHT 19"),
 (122, 0.0, "quote", ("“Don't come after me.”", "THE RECORD, 1945")),
 (122, "adds", "quote", ("“...they look like they are from outer space.”", "ADDED IN A 1974 BESTSELLER  ·  NOT IN THE RECORD")),
 (123, 0.2, "under", "1977: A HOLLYWOOD FILM  ·  FICTION"),
 (124, 0.0, "under", "NOT AN OFFICIAL NAME  ·  U.S. BOARD ON GEOGRAPHIC NAMES"),
 (124, "noaa|noah", "under", "NOAA: NO EVIDENCE OF MORE DISAPPEARANCES THERE"),
 (126, 0.0, "typecenter", "“THE LOST PATROL, FOUND”"),
 (127, "quite", "quote", ("“...quite certain that the five aircraft we found\nare not those of Flight 19.”", "GRAHAM HAWKES, 4 JUNE 1991")),
 (128, 0.0, "list", ["WRONG NUMBERS", "OLDER PLANES", "100+ AVENGERS LOST OFF FLORIDA"]),
 (129, 0.2, "under", "2022  ·  DIVERS LOOKING FOR TRAINING 49 FIND A PIECE OF CHALLENGER"),
 (130, 0.0, "typecenter", "WHAT NOBODY KNOWS"),
 (132, 0.0, "under", "WHEN  ·  TOGETHER OR ONE BY ONE"),
 (133, 0.2, "under", "THE COMPASSES: ONLY HIS WORD"),
 (134, 0.0, "under", "A BROADCAST OF THE FIX?  THE READY PLANE?"),
 (136, 0.0, "under", "THEIR WORDS  ·  THEIR HEADINGS  ·  THEIR FUEL"),
 (138, 0.0, "under", "WHERE DO YOU THINK FLIGHT 19 WENT DOWN?  TELL ME BELOW"),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

NAMES19 = ["Lt. Charles C. Taylor, USNR", "ARM3c Walter R. Parpart, USNR", "AOM3c George F. Devlin, USNR*", "Capt. Edward J. Powers Jr., USMC",
           "SSgt. Howell O. Thompson, USMCR", "SSgt. George R. Paonessa, USMC", "Capt. George W. Stivers Jr., USMC", "Pvt. Robert P. Gruebel, USMCR",
           "Sgt. Robert F. Gallivan, USMC", "2nd Lt. Forrest J. Gerber, USMCR", "PFC William E. Lightfoot, USMCR", "Ens. Joseph T. Bossi, USNR",
           "S1c Herman A. Thelander, USNR", "S1c Burt E. Baluk Jr., USNR"]
NAMES49 = ["Lt.(jg) Walter G. Jeffrey, USN", "Lt.(jg) Harry G. Cone, USNR", "Ens. Roger M. Allen, USNR", "Ens. Lloyd A. Eliason, USNR",
           "Ens. Charles D. Arceneaux, USNR", "AMM1c Donald E. Peterson, USN", "S1c Wiley D. Cargill, USNR", "ARM3c Robert C. Cameron, USNR",
           "ARM3c James F. Jordan, USNR", "S1c Philip B. Neeman, USNR", "AOM3c John T. Menendez, USN", "AOM3c James F. Osterheld, USNR",
           "S1c Alfred J. Zywicki, USNR"]

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

SLOT = {"lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center"}
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
        if kind == "badge": continue                                   # badges run across shots (draw_badge)
        if t < t0 or t >= shot_t1 or t0 < shot_t0 - 0.2: continue
        if NO_BOTTOM and SLOT.get(kind) == "bottom": continue
        if t >= ov_end(j, shot_t1): continue
        if kind == "lower": lower(c, a, t, t0)
        elif kind == "under": under(c, a, t, t0)
        elif kind in ("typecenter", "typecenter_red"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 110, W, H / 2 + 110), fill=(0, 0, 0, 185)); c.alpha_composite(lay)
            L.typewriter(c, a, t, t0, W / 2, H / 2, size=96 if len(a) < 26 else 74, fill=RED if kind.endswith("red") else BONE, cps=16, anchor="mm", cursor=False)
        elif kind == "list":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay); sz = 74 if max(len(s) for s in a) < 24 else 58
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W / 2, H / 2 - (len(a) - 1) * 60 + i * 120, size=sz, cps=20, anchor="mm", cursor=False)
        elif kind == "stamp": L.stamp(c, a[0], a[1], a[2], t, t0, size=100)
        elif kind == "quote":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay); qs = a[0].split("\n")
            for i, q in enumerate(qs):
                L.text(c, q, W / 2, H / 2 - 40 - (len(qs) - 1) * 42 + i * 84, 50 if NO_BOTTOM and len(q) > 44 else 60, BONE, SER, alpha=ease((t - t0 - 0.25 * i) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, W / 2, H / 2 + 60 + (len(qs) - 1) * 42, size=34, fill=STEEL, cps=34, anchor="mm", cursor=False)
        else: ov_extra(c, kind, a, t, t0)

BADGES = sorted((OVT[j], OV[j][3]) for j in range(len(OV)) if OV[j][2] == "badge")
def draw_badge(c, t):
    """the clock, top-left: shows for 9 s from its line (or until the next one), across shot cuts"""
    cur = None
    for k, (tm, s) in enumerate(BADGES):
        if t >= tm: cur = (tm, s, BADGES[k + 1][0] if k + 1 < len(BADGES) else 1e9)
    if not cur: return
    tm, s, nxt = cur; end = min(tm + 9.0, nxt)
    if t >= end: return
    al = ease((t - tm) / 0.2) * ease((end - t) / 0.4); f = L.font(TYPE, 40); w = f.getlength(s)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    dd.rectangle((36, 34, 36 + w + 46, 98), fill=(0, 0, 0, int(205 * al))); dd.rectangle((36, 34, 45, 98), fill=RED + (int(255 * al),))
    dd.text((66, 66), s, font=f, fill=BONE + (int(255 * al),), anchor="lm"); c.alpha_composite(lay)

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
            L.text(c, "FILE 08  ·  FLIGHT 19  ·  DECEMBER 1945", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
    elif kind == "subpop":                                     # mid-video subscribe nudge, top-left, 4 s
        u = t - t0
        if u < 4.0:
            k = ease(u / 0.4) * ease((4.0 - u) / 0.4); x = 40 - (1 - k) * 640
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x, 120, x + 600, 192), 36, fill=RED + (int(235 * k),))
            c.alpha_composite(lay); L.text(c, "SUBSCRIBE FOR THE NEXT FILE", x + 300, 157, 34, BONE, TYPE, alpha=k)

def doc_frame(a, t, t0, t1):
    """a Board / log page, paper-toned; the camera follows each spoken line, which gets a spotlight and a red underline"""
    rid = a["rid"]; src, k = page_img(rid); rows = ocr(rid); mk = []
    for q, key in a["marks"]:
        b = ob(rid, q)
        if b: mk.append((tuple(v * k for v in b), AT(key)))
    if rows:
        bx0 = np.percentile([r["box"][0] for r in rows], 10) * k; bx1 = np.percentile([r["box"][2] for r in rows], 90) * k
    else: bx0, bx1 = 0.08 * src.width, 0.92 * src.width
    u = clamp01((t - t0) / max(t1 - t0, 1e-6))
    s = W * 0.84 / max(bx1 - bx0, 1) * a.get("zoom", 1.0) * (1.0 + 0.05 * u)
    cx = (bx0 + bx1) / 2; cy = (mk[0][0][1] + mk[0][0][3]) / 2 if mk else src.height * 0.4; act = None
    for b, tm in mk:
        cy += ((b[1] + b[3]) / 2 - cy) * ease((t - tm + 0.15) / 0.6)
        if t >= tm: act = (b, tm)
    cx = min(max(cx, W / 2 / s), src.width - W / 2 / s) if src.width * s > W else src.width / 2
    cy = min(max(cy, H / 2 / s), src.height - H / 2 / s) if src.height * s > H else src.height / 2
    c = view(src, cx, cy, s)
    if act:
        b, tm = act; sx0, sy0, sx1, sy1 = (b[0] - cx) * s + W / 2 - 18, (b[1] - cy) * s + H / 2 - 12, (b[2] - cx) * s + W / 2 + 18, (b[3] - cy) * s + H / 2 + 12
        spotlight(c, (sx0, sy0, sx1, sy1), ease((t - tm) / 0.35))
        uu = ease((t - tm - 0.1) / 0.3); ImageDraw.Draw(c).rectangle((sx0 + 10, sy1 + 4, sx0 + 10 + (sx1 - sx0 - 20) * uu, sy1 + 11), fill=RED)
    c = L.vignette(c, 0.45); tag(c, a.get("tag") or DT.get(rid)); return c

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

def names_frame(a, t, t0, t1):
    c = blur_bg("E1", None).copy(); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
    for x, head, sub, names in ((500, "FLIGHT 19", "FIVE TBM AVENGERS  ·  14 MEN", NAMES19), (1420, "TRAINING 49", "PBM-5 MARINER  ·  13 MEN", NAMES49)):
        L.text(c, head, x, 96, 64, BONE, COND, alpha=ease((t - t0) / 0.4)); L.text(c, sub, x, 150, 26, STEEL, TYPE, alpha=ease((t - t0 - 0.2) / 0.4))
        for i, s in enumerate(names): L.typewriter(c, s, t, t0 + 0.4 + i * 0.16, x, 212 + i * 48, size=30, cps=70, anchor="mm", cursor=False)
    L.typewriter(c, "MISSING SINCE 5 DECEMBER 1945  ·  NAMES AND RANKS AS IN THE BOARD RECORD  ·  *ENLISTED AS “ROBERT F. HARMON”", t, t0 + 2.6, W / 2, 892, size=22, fill=STEEL, cps=80, anchor="mm", cursor=False)
    return c

def frame(t):
    k, (key, (kind, a)), t0, t1 = shot_at(t)
    if kind == "kb":
        src = tone(a["rid"], a["crop"]); c = L.vignette(L.kenburns(src, t, t0, t1, max(a["z"][0], 1.01), max(a["z"][1], 1.01), a["c0"], a["c1"])); tag(c, a.get("tag"))
        if a.get("dim"): c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * a["dim"]))))
    elif kind == "kbp":
        c = blur_bg(a["rid"], a["crop"]).copy(); u = ease(clamp01((t - t0) / max(t1 - t0, 1e-6)))
        card = pcard_h(a["rid"], a["crop"], a["h"], a["rot"]); k2 = 1.0 + 0.05 * u
        card = card.resize((int(card.width * k2), int(card.height * k2)), Image.BICUBIC)
        L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag"))
    elif kind == "tcard": c = tcard_frame(a, t, t0, t1)
    elif kind == "nmap": c = MS.map_panel(a, t, t0, t1)
    elif kind == "doc": c = doc_frame(a, t, t0, t1)
    elif kind == "counter": c = counter_frame(a, t, t0, t1)
    elif kind == "names": c = names_frame(a, t, t0, t1)
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 120, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 230, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 320, t, t0, width=7)
        L.typewriter(c, ("NEXT FILE:  " + NEXT) if NEXT else "SUBSCRIBE FOR THE NEXT FILE", t, t0 + 0.2, W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
        if t > VO_END:
            d = ImageDraw.Draw(c)
            for x in (110, 1170): d.rectangle((x, 520, x + 640, 880), outline=STEEL + (255,), width=3)
            d.ellipse((835, 575, 1085, 825), outline=STEEL + (255,), width=3)
    else:
        c = Image.new("RGBA", (W, H), INK + (255,))
    draw_ov(c, t, t0, t1)
    if kind not in ("tcard", "names", "end"): draw_badge(c, t)
    return c

# ------------------------------------------------------------------ audio
def load(p, sr=48000):
    a, s = sf.read(p, dtype="float32", always_2d=True); a = a.mean(1)
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    return a
def tl(i, off=0.0): return T[i] + off
RADIO = {"A6", "A7", "A8", "A9", "A10", "A16", "A17"}
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
    # music beds (Kevin MacLeod, CC BY), about 19-22 dB under the voice
    music("Thunder Dreams.mp3", 0.0, tl(8), -20); music("Floating Cities.mp3", tl(8), tl(22), -21); music("Rising Tide.mp3", tl(22), tl(47), -21)
    music("Man Down.mp3", tl(47), tl(67), -21); music("Thunder Dreams.mp3", tl(67), tl(86), -20); music("Rising Tide.mp3", tl(86), tl(102), -21)
    music("Promises to Keep.mp3", tl(102), tl(116), -21); music("Floating Cities.mp3", tl(116), tl(130), -21); music("Thunder Dreams.mp3", tl(130), DUR, -20)
    loop("radio_static_crackles", tl(22), tl(35), -36); loop("radio_static_crackles", tl(35), tl(59), -37); loop("radio_static_crackles", tl(75), tl(90), -36)
    loop("waves_rough_sea_loop", tl(59), tl(63), -31); loop("waves_windy_sea_loop", tl(90), tl(93), -30); loop("wind_deep_cinematic_hum", tl(130), tl(137), -31)
    for i, (key, (kind, a)) in enumerate(SHOTS):
        t0 = SHOT_T[i]
        if kind == "tcard":
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "kbp": sfx("paper_slide", t0, -19); sfx("camera_vintage_shutter", t0 + 0.12, -25)
        elif kind == "nmap":
            sfx("paper_page_turn", t0, -22)
            for op in a["ops"]:
                if op[0] == "pin" and op[4] >= 0: sfx("camera_classic_click", t0 + op[4], -22)
        elif kind == "doc":
            sfx("paper_slide", t0, -21)
            for q, k2 in a["marks"]:
                sfx("typewriter_soft_click", AT(k2), -22, maxlen=0.6)
                if a["rid"] in RADIO: sfx("radio_static_fx", AT(k2) - 0.05, -31, maxlen=0.9)
        elif kind == "counter":
            for k2, s in a["steps"]: sfx("hit_short_bass", AT(k2), -18, maxlen=1.2); sfx("clock_tick_single", AT(k2), -16)
        elif kind == "kb": sfx("whoosh_fast_transition", t0 - 0.1, -32)
    for j, (ln, off, kind, a) in enumerate(OV):
        if kind == "stamp": sfx("hit_horror_drum", OVT[j], -14)
        if kind in ("typecenter", "typecenter_red", "list"): sfx("typewriter_typing_old", OVT[j], -26)
        if kind == "nameplate": sfx("typewriter_typing_old", OVT[j], -24, maxlen=1.2)
        if kind == "brand": sfx("hit_cinematic_deep_impact", OVT[j], -16)
        if kind == "subpop": sfx("whoosh_fast_transition", OVT[j], -24)
        if kind == "badge": sfx("clock_tick_single", OVT[j], -20)
    sfx("hit_cinematic_deep_impact", 0.0, -12)                                   # the cold open starts on a hit
    EV = [(0, 0.0, "radio_static_fx", -26), (3, "no", "hit_deep_heartbeat_impact", -16), (19, "take|off", "whoosh_ghostly", -26), (24, 0.0, "radio_static_crackles", -26),
          (30, "come", "hit_short_bass", -18), (33, "fails", "radio_static_fx", -22), (54, "held|ground", "hit_short_bass", -18), (60, "together", "hit_glass_suspense", -20),
          (62, "sun|sets", "sweep_horror_long", -26), (69, "cross", "hit_glass_suspense", -20), (72, "phoned", "telephone_old_ring", -27), (72, "teletype", "typewriter_typing_old", -22),
          (73, "never|broadcasts", "hit_cinematic_deep_impact", -14), (76, "east", "hit_short_bass", -18), (88, "no", "hit_deep_heartbeat_impact", -15),
          (89, "calling", "radio_static_crackles", -24), (96, "flames|burst", "hit_big_cinematic_impact", -14), (97, "disappeared", "hit_glass_suspense", -20),
          (109, "confusion|temporary", "hit_horror_drum", -18), (113, "unknown", "hit_cinematic_deep_impact", -16), (118, "white", "whoosh_ghostly", -24),
          (126, "found", "reporters_camera_flashes", -27), (135, "no", "hit_deep_heartbeat_impact", -15), (138, 0.2, "typewriter_return_bell", -18)]
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
SEGP = "cseg_" if COLOR else "seg_"
def final(n, name=None):
    name = name or "TheLastHours_08_Flight19.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "7:04 PM: no answer"), (8, "11 AM: the forecast"), (20, "3:40 PM: “I don't know where we are”"), (35, "4:21 PM: “Am lost”"),
      (47, "The ready plane stays on the ground"), (59, "5:24 PM: ten gallons"), (67, "5:50 PM: what the Navy knew"), (75, "6:04 PM: the turn east"),
      (86, "7:04 PM: the last call"), (93, "7:27 PM: Training 49"), (102, "The search"), (107, "The verdict"), (116, "How the legend was made"),
      (125, "1991: “We found them”"), (130, "What nobody knows")]

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
    elif m == "boxes":                                                           # which OCR text each DOC spotlight lands on
        for key, (kind, a) in SHOTS:
            if kind != "doc": continue
            for q, k2 in a["marks"]:
                b = ob(a["rid"], q); rows = ocr(a["rid"])
                txt = " / ".join(r["text"][:40] for r in rows if b and r["box"][1] >= b[1] - 2 and r["box"][3] <= b[3] + 2)
                print(a["rid"], q if isinstance(q, str) else "manual", "->", "NONE" if b is None else [int(v) for v in b], "|", txt[:150])
    elif m == "keys":                                                            # word keys whisper did not hear (they fall back to line start + 0.3 s)
        keys = [s[0] for s in SHOTS] + [(ln, off) for ln, off, _, _ in OV]
        for s in SHOTS:
            if s[1][0] == "counter": keys += [k for k, _ in s[1][1]["steps"]]
            if s[1][0] == "doc": keys += [k for _, k in s[1][1]["marks"]]
        for k in keys:
            if isinstance(k, tuple) and isinstance(k[1], str) and wt(k[0], k[1]) is None: print("MISSING", k, "|", LINES[k[0]][:80])
        gaps = [(SHOT_T[i + 1] - SHOT_T[i], i) for i in range(len(SHOTS) - 1)]
        print("shots", len(SHOTS), "longest", sorted(gaps)[-6:], "shortest", sorted(gaps)[:4])
    elif m == "chapters":
        for i, (ln, name) in enumerate(CH):
            t = 0 if i == 0 else T[ln] - 0.12; print(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    elif m == "times":
        for i in range(len(LINES)): print(f"{i:3d} {T[i]:7.2f} {LINES[i][:70]}")
        print("VO_END", VO_END, "DUR", DUR, "shots", len(SHOTS))
    elif m == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "segfrom":                                                         # re-render only the tail: frames from a fixed start to the (new) end into seg_<i>
        f0, i = int(sys.argv[2]), int(sys.argv[3])
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "3", "-pix_fmt", "yuv420p", B + f"{SEGP}{i}.mp4"], stdin=subprocess.PIPE)
        for f in range(f0, NF): p.stdin.write(frame(f / FPS).convert("RGB").tobytes())
        p.stdin.close(); p.wait(); print("segfrom done", f0, NF, flush=True)
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
