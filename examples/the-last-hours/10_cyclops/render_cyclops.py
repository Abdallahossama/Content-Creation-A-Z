"""The Last Hours #9: USS Cyclops, March 1918 (Case File style, colour grade, 1920x1080). Built on render_flight19.py
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

ROOT = "D:/why habibi/_newchannel/10_cyclops/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 20.0
NEXT = os.environ.get("LH_NEXT", "")                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/cyclops_vo_chatterbox.wav")
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
def isdoc(rid): return rid[0] == "A" or rid in ("C1", "C2", "D6")
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
RIO, BAHIA, BARB, NORFOLK = (-43.17, -22.9), (-38.51, -12.97), (-59.62, 13.1), (-76.29, 36.85)
CAPEH, BALT, STTH, HAWES = (-76.0, 36.93), (-76.62, 39.28), (-64.93, 18.33), (-74.70, 37.43)
SOUTH_OF_BARB = (-59.75, 11.4)
V_ATL, V_LAST, V_BARB = (-55.0, 7.0, 128.0), (-67.0, 26.0, 68.0), (-59.6, 12.6, 6.0)
V_CHES, V_SIS = (-75.6, 37.6, 6.5), (-70.0, 27.5, 46.0)

# ------------------------------------------------------------------ shot constructors
CROP = {"A6": (0.03, 0.035, 0.52, 0.50), "A7": (0.0, 0.0, 1.0, 1.0), "B1": (0.04, 0.05, 0.95, 0.93), "B7": (0.05, 0.08, 0.95, 0.92),
        "B8": (0.0, 0.0, 1.0, 0.92), "C1": (0.715, 0.06, 0.965, 0.74), "C2": (0.70, 0.06, 0.96, 0.58), "D2": (0.03, 0.03, 0.97, 0.80),
        "D6": (0.10, 0.08, 0.92, 0.88), "F9": (0.33, 0.0, 1.0, 1.0)}
TB1 = "USS CYCLOPS, 1910s  ·  HARRIS & EWING, LIBRARY OF CONGRESS"
TB2 = "USS CYCLOPS IN THE HUDSON RIVER, 3 OCT 1911  ·  NHHC"
TB3 = "USS CYCLOPS, 3 OCT 1911  ·  NATIONAL ARCHIVES"
TB4 = "USS CYCLOPS, c. 1913  ·  NHHC"
TB5 = "CYCLOPS'S COALING GEAR  ·  SEA POWER, MAY 1917  ·  NHHC"
TB6 = "“COALING SHIP FROM USS CYCLOPS”, 1914 POSTCARD  ·  NHHC"
TB7 = "USS CYCLOPS  ·  BAIN NEWS SERVICE, LIBRARY OF CONGRESS"
TD1 = "USS JUPITER, CYCLOPS'S SISTER, 1913  ·  NHHC"
TD4 = "USS JASON, A SIMILAR COLLIER, 1910s  ·  LIBRARY OF CONGRESS"
TSAT = "NASA SATELLITE IMAGE (MODERN)"
TF3 = "THE ATLANTIC COAST AT NIGHT, 2016 (MODERN LIGHTS)  ·  NASA"
DT = {"A1": "WORLEY'S NAVY MEDICAL FORM, 30 MAR 1917  ·  NATIONAL ARCHIVES", "A2": "WORLEY'S FITNESS REPORT, JAN-JUN 1917  ·  NATIONAL ARCHIVES",
      "A3": "WORLEY'S NAVAL RESERVE CARD, 1917  ·  NATIONAL ARCHIVES", "A4": "NAVAL EXAMINING BOARD, MARCH 1917  ·  NATIONAL ARCHIVES",
      "A5": "THE LAST MESSAGE, AS PRINTED BY SECRETARY DANIELS, 1922", "A6": "U.S. WEATHER BUREAU MAP, 10 MARCH 1918  ·  POPULAR SCIENCE, 1929",
      "A7": "CYCLOPS STABILITY CURVES, 1910  ·  NATIONAL ARCHIVES", "C1": "NAVY DEPARTMENT PHOTO CARD  ·  NATIONAL ARCHIVES",
      "C2": "NAVY DEPARTMENT PHOTO CARD  ·  NATIONAL ARCHIVES", "D6": "U-151 AT SEA, 1918  ·  U.S. NAVY"}
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag, dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT.get(rid)))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag))
CABLE = "11+12+13+14+15+16+17+18+19+20+21"   # the Daniels page: the cable block

SHOTS = [
 (0, KB("B1", z=(1.0, 1.1), c0=(0.5, 0.52), tag=TB1)),                                    # frame 1: the ship, broadside
 ((0, "nobody"), KB("E3", z=(1.05, 1.15), dim=0.1)),
 (1, TCARD("11:45 AM", "Monday, March 4, 1918", "B2")),
 (2, KB("F6", z=(1.0, 1.12), c0=(0.62, 0.5), tag=TSAT)),
 (3, DOC("A5", [(CABLE, 3)])),
 (4, KB("B3", z=(1.0, 1.1), tag=TB3)),
 ((4, "south"), NMAP(V_LAST, ops=[("pin", *BARB, "BARBADOS", -9), ("arrow", BARB, (-59.8, 9.5), "SOUTH", 0.0), ("pin", *BALT, "BALTIMORE · NORTH", 0.9)])),
 (5, KB("B7", z=(1.0, 1.1), tag=TB7)),
 (6, KBP("A2")),
 ((6, "stability"), KBP("A7", h=620)),
 (7, KB("B5", z=(1.1, 1.22), tag=TB5)),
 ((7, "captain"), KBP("A1")),
 ((7, "nobody"), KB("E3", z=(1.0, 1.1))),
 (8, TCARD("5:30 PM", "Sunday, March 3, 1918", "B2")),
 ((8, "collier|navy"), KB("F6", z=(1.05, 1.18), c0=(0.62, 0.5), tag=TSAT)),
 (9, NMAP(V_ATL, ops=[("pin", *RIO, "RIO DE JANEIRO", -9), ("pin", *BARB, "BARBADOS · NOT ON THE SCHEDULE", 0.2), ("pin", *BALT, "BALTIMORE", -9)])),
 (10, KB("B2", z=(1.0, 1.1), tag=TB2)),
 ((10, "five|542"), KB("B3", z=(1.15, 1.25), c0=(0.45, 0.55), tag=TB3)),
 (11, KB("B4", z=(1.0, 1.12), tag=TB4)),
 (12, KB("B5", z=(1.0, 1.1), dim=0.2, tag=TB5)),
 (13, KB("B6", z=(1.0, 1.12), tag=TB6)),
 ((13, "crew"), KB("B3", z=(1.1, 1.2), dim=0.3, tag=TB3)),
 (14, KB("B7", z=(1.1, 1.2), tag=TB7)),
 (15, KB("B6", z=(1.2, 1.3), c0=(0.4, 0.6), tag=TB6)),
 ((15, "seven|775"), COUNTER([((15, "seven|775"), "$775")], "FOR MEAT, FLOUR AND VEGETABLES  ·  THE CONSUL'S CABLE", "B1")),
 (16, KB("B5", z=(1.2, 1.3), c0=(0.4, 0.5), dim=0.15, tag=TB5)),
 (17, KB("B5", z=(1.45, 1.55), c0=(0.7, 0.4), dim=0.2, tag=TB5)),
 (18, DOC("A5", [(CABLE, (18, "files|cable"))])),
 (19, KB("B1", z=(1.2, 1.35), c0=(0.55, 0.45), tag=TB1)),
 (20, KB("F6", z=(1.2, 1.35), c0=(0.6, 0.5), tag=TSAT)),
 (21, KB("B2", z=(1.1, 1.2), tag=TB2)),
 ((21, "backs"), NMAP(V_BARB, ops=[("pin", *BARB, "CARLISLE BAY", -9), ("arrow", BARB, SOUTH_OF_BARB, "STEAMED SOUTH", 1.2)])),
 (22, NMAP(V_LAST, ops=[("pin", *BARB, "BARBADOS", -9), ("pin", *BALT, "BALTIMORE · NORTH", 0.2)])),
 (23, KBP("A1")),
 (24, KB("B2", z=(1.2, 1.3), c0=(0.5, 0.5), dim=0.3, tag=TB2)),
 (25, NMAP(V_ATL, ops=[("pin", *NORFOLK, "NORFOLK · 8 JAN 1918", 0.1), ("route", [NORFOLK, (-50.0, 5.0), BAHIA, RIO], 0.6, 2.4), ("pin", *RIO, "RIO", 3.0)])),
 (26, KB("B3", z=(1.0, 1.1), tag=TB3)),
 (27, KB("B2", z=(1.0, 1.1), tag=TB2)),
 ((27, "captain|son"), KB("E3", z=(1.0, 1.1), dim=0.25)),
 (28, KB("B2", z=(1.25, 1.4), c0=(0.35, 0.5), tag=TB2)),
 (29, KB("B7", z=(1.0, 1.12), dim=0.25, tag=TB7)),
 (30, KB("B4", z=(1.2, 1.35), c0=(0.62, 0.42), tag=TB4)),
 (31, KB("B4", z=(1.5, 1.6), c0=(0.7, 0.4), dim=0.2, tag=TB4)),
 (32, KB("F7", z=(1.0, 1.1), tag=TSAT)),
 ((32, "survey"), KB("B5", z=(1.0, 1.1), dim=0.15, tag=TB5)),
 (33, KB("B3", z=(1.2, 1.3), c0=(0.6, 0.5), tag=TB3)),
 (34, COUNTER([((34, "ten|10"), "10,835")], "TONS OF MANGANESE ORE  ·  STOWED ON TIMBER IN THE HOLD", "B5", size=360)),
 (35, KB("B3", z=(1.0, 1.1), dim=0.25, tag=TB3)),
 (36, NMAP(V_ATL, ops=[("pin", *RIO, "RIO · 16 FEB", -9), ("pin", *BAHIA, "BAHIA", 0.3), ("route", [RIO, BAHIA, BARB], 0.5, 2.2), ("pin", *BARB, "BARBADOS · 3 MAR", 2.8)])),
 (37, KBP("A1", h=820, rot=1.5)),
 (38, DOC("A1", [((140, 690, 1112, 748), (38, "where")), ("23+24", (38, "date|december"))])),
 (39, KB("E3", z=(1.05, 1.15), dim=0.2)),
 ((39, "germany"), KB("B7", z=(1.05, 1.15), dim=0.3, tag=TB7)),
 (40, KB("B7", z=(1.15, 1.25), dim=0.3, tag=TB7)),
 (41, KB("B3", z=(1.0, 1.08), dim=0.35, tag=TB3)),
 (42, KB("B2", z=(1.0, 1.1), dim=0.25, tag=TB2)),
 (43, DOC("A2", [("13+14+15+16", 43), ("23+24", (43, "intemperance|temperance")), ("32+33+34+35+36+37+38", (43, "keep|highly"))])),
 (44, KB("B1", z=(1.05, 1.15), tag=TB1)),
 (45, NMAP(V_LAST, ops=[("pin", *BARB, "BARBADOS", -9), ("pin", *CAPEH, "MOUTH OF CHESAPEAKE BAY", 0.2), ("route", [BARB, CAPEH], 0.6, 2.0),
                        ("label", -71.0, 24.0, "~1,930 MILES  ·  ABOUT 9 DAYS", 2.4, 34)])),
 (46, KB("B1", z=(1.4, 1.6), c0=(0.62, 0.3), tag=TB1)),
 (47, KB("E3", z=(1.0, 1.12))),
 (48, KB("E3", z=(1.2, 1.3), c0=(0.4, 0.6))),
 (49, KBP("A6", h=900)),
 ((49, "those|nights"), KB("F3", z=(1.0, 1.08), tag=TF3)),
 (50, NMAP(V_CHES, ops=[("pin", *BALT, "BALTIMORE · DUE 13 MARCH", 0.1), ("pin", *CAPEH, "CAPE HENRY", -9)])),
 (51, KB("B7", z=(1.0, 1.1), tag=TB7)),
 (52, KB("C3", z=(1.0, 1.08), c0=(0.5, 0.35), tag="EARNEST R. CRAMMER, SEAMAN  ·  LOST ON CYCLOPS  ·  NHHC")),
 (53, KB("E3", z=(1.0, 1.1), dim=0.3)),
 (54, KBP("A6", h=900, rot=1.5)),
 (55, KB("B2", z=(1.05, 1.15), dim=0.2, tag=TB2)),
 (56, KB("E3", z=(1.0, 1.08), dim=0.1)),
 (57, KB("B7", z=(1.05, 1.15), dim=0.3, tag=TB7)),
 (58, KB("E3", z=(1.1, 1.2), c0=(0.6, 0.4), dim=0.1)),
 ((58, "bottle|august"), KB("F5", z=(1.0, 1.1), tag=TSAT)),
 (60, KBP("D6", h=900)),
 (61, KB("B1", z=(1.0, 1.08), dim=0.2, tag=TB1)),
 ((61, "admiral|german"), KB("B3", z=(1.05, 1.15), dim=0.35, tag=TB3)),
 (62, KBP("C2", h=880)),
 (63, KB("B4", z=(1.0, 1.1), dim=0.25, tag=TB4)),
 (64, KB("B6", z=(1.1, 1.2), dim=0.2, tag=TB6)),
 (65, COUNTER([((65, "five|5"), "$5,000")], "EACH MAN ABOARD DEEMED INSURED  ·  SENATE, DEC 1919", "B3")),
 (66, KB("B1", z=(1.0, 1.1), tag=TB1)),
 (67, KB("E3", z=(1.0, 1.08), dim=0.1)),
 (68, KB("B5", z=(1.0, 1.1), tag=TB5)),
 ((68, "nervig|plates"), KB("B2", z=(1.1, 1.2), c0=(0.5, 0.6), tag=TB2)),
 ((68, "years|similar"), KB("D4", z=(1.0, 1.1), tag=TD4)),
 (69, KB("B2", z=(1.0, 1.1), tag=TB2)),
 ((69, "fifty|56"), COUNTER([((69, "fifty|56"), "56°")], "HER ROLL IN 1916, NEARLY EMPTY  ·  AS A NAVY OFFICER ABOARD SAW IT", "B2")),
 (70, KB("E3", z=(1.1, 1.2), dim=0.2)),
 (71, KBP("A6", h=900)),
 (72, KB("B3", z=(1.0, 1.1), tag=TB3)),
 (73, KB("D1", z=(1.0, 1.1), tag=TD1)),
 (74, KB("D2", z=(1.05, 1.15), tag=TD1)),
 ((74, "virgin|sailed"), NMAP(V_SIS, ops=[("pin", *STTH, "ST. THOMAS · 23 NOV + 10 DEC 1941", 0.1), ("pin", *CAPEH, "CHESAPEAKE BAY", -9),
                                         ("route", [STTH, CAPEH], 0.6, 1.8)])),
 (75, KB("D1", z=(1.15, 1.25), c0=(0.6, 0.5), tag=TD1)),
 (76, NMAP(V_CHES, ops=[("pin", *CAPEH, "CAPE HENRY", -9), ("pin", *HAWES, "1968 · AN OLD WRECK · 180 FT DOWN", 0.4)])),
 (77, KB("B4", z=(1.05, 1.15), dim=0.35, tag=TB4)),
 (78, KB("B2", z=(1.1, 1.2), dim=0.35, tag=TB2)),
 (79, KB("F2", z=(1.0, 1.08), tag=TSAT)),
 (80, KB("B1", z=(1.1, 1.2), c0=(0.45, 0.5), dim=0.2, tag=TB1)),
 ((80, "frigate|historians"), KB("E3", z=(1.0, 1.1), dim=0.15)),
 (81, KB("F3", z=(1.0, 1.08), tag=TF3)),
 (82, NMAP(V_LAST, ops=[("pin", *BARB, "BARBADOS", -9), ("pin", *BALT, "BALTIMORE", -9), ("label", -68.0, 27.0, "?", 0.3, 130)])),
 (83, KB("F6", z=(1.0, 1.1), c0=(0.62, 0.5), tag=TSAT)),
 (84, COUNTER([((84, "two|293"), "293"), ((84, "three|312"), "312")], "RECORDS DIFFER ON HOW MANY WERE ABOARD", "B3")),
 (85, DOC("A5", [(CABLE, (85, "stamped|cable|coal"))])),
 (86, KB("B1", z=(1.0, 1.15), tag=TB1)),
 (87, ("crew", {})),
 ((88, "tell"), ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "lower", "USS CYCLOPS  ·  306 PEOPLE ABOARD, BY THE NAVY'S COUNT"),
 (0, "coal", "typecenter", "THE LAST MESSAGE: COAL"),
 (0, "nobody", "typecenter_red", "NEVER FOUND"),
 (4, "witness|remembered", "under", "AS THE U.S. CONSUL'S SON REMEMBERED IT, 1929"),
 (6, 0.2, "under", "FORGET THE BERMUDA TRIANGLE"),
 (7, "carrying", "under", "WHAT SHE WAS CARRYING"),
 (7, "captain", "under", "WHO HER CAPTAIN REALLY WAS"),
 (7, "nobody", "under", "AND WHY NOBODY CAN SAY WHAT HAPPENED"),
 (8, 0.0, "badge", "3 MAR 1918"),
 (8, "collier|navy", "brand", None),
 (10, "five|542", "under", "542 FT  ·  ABOUT 1½ FOOTBALL FIELDS"),
 (11, 0.3, "under", "ABOUT 10,800 TONS OF MANGANESE ORE  ·  FROM RIO DE JANEIRO"),
 (12, "remember", "typecenter", "REMEMBER THE ORE"),
 (13, "crew", "list", ["HER CREW", "DOZENS OF SAILORS GOING HOME", "5 PRISONERS", "THE U.S. CONSUL GENERAL FROM RIO"]),
 (14, 0.2, "under", "THE AMERICAN CONSUL IN BARBADOS: LIVINGSTON"),
 (16, "reckoning|probably", "under", "“PROBABLY HAD MORE THAN FIFTEEN HUNDRED TONS”  ·  THE CONSUL"),
 (17, 0.0, "typecenter", "REMEMBER THE COAL"),
 (18, 0.0, "badge", "4 MAR 1918  ·  11:45 AM"),
 (19, 0.2, "typecenter_red", "THE LAST WORD"),
 (20, 0.2, "under", "THE CAPTAIN + 2 OTHERS  ·  THE U.S. CONSULATE"),
 (21, 0.0, "badge", "~5:00 PM"),
 (22, 0.3, "under", "NOBODY ON THE BEACH THOUGHT ANYTHING OF IT"),
 (23, 0.2, "nameplate", ("LT. CMDR. GEORGE W. WORLEY", "51 BY HIS OWN PAPERS  ·  HER MASTER SINCE 1910")),
 (24, 0.0, "typecenter", "WHO WAS HE?"),
 (25, 0.0, "badge", "8 JAN 1918"),
 (26, 0.2, "nameplate", ("LT. (JG) CONRAD NERVIG", "WATCH OFFICER  ·  LEFT THE SHIP AT RIO")),
 (27, "son|captain", "quote", ("“Son, she'll last as long as we do.”", "WORLEY TO NERVIG, AS NERVIG REMEMBERED IT")),
 (28, 0.2, "under", "DAY 5: THE SECOND-IN-COMMAND, UNDER ARREST"),
 (29, "long|woolen", "list", ["LONG WOOLEN UNDERWEAR", "A DERBY HAT", "A CANE"]),
 (30, "head|cylinder", "under", "THE STARBOARD ENGINE: A CYLINDER HEAD BLOWS OFF"),
 (31, 0.0, "typecenter", "REMEMBER THE ENGINE"),
 (32, 0.0, "badge", "RIO  ·  LATE JAN 1918"),
 (32, "satisfactory|survey", "under", "SURVEY BOARD: “NOT IN SATISFACTORY CONDITION”"),
 (33, 0.2, "under", "NERVIG LEFT FOR ANOTHER SHIP AT RIO"),
 (35, 0.0, "under", "+ 4,000 TONS OF WATER, MOSTLY IN THE DOUBLE BOTTOM"),
 (36, 0.0, "badge", "16 FEB 1918"),
 (37, 0.0, "typecenter", "WHO WAS GEORGE WORLEY?"),
 (38, 0.0, "badge", "30 MAR 1917"),
 (39, "germany", "under", "NAVY INVESTIGATORS: BORN IN GERMANY, UNDER ANOTHER NAME"),
 (40, "damned|dutchman", "quote", ("“Master alluded to by others as damned Dutchman.”", "THE U.S. CONSUL, BARBADOS  ·  APRIL 1918")),
 (41, 0.0, "quote", ("“...I fear fate worse than sinking...”", "“...POSSIBLY BASED ON INSTINCTIVE DISLIKE”  ·  THE SAME CABLE")),
 (42, 0.0, "under", "MYTH: A DRUNK AND A TRAITOR"),
 (44, 0.2, "under", "NAVY INTELLIGENCE: NO EVIDENCE HE WAS DISLOYAL"),
 (45, 0.0, "badge", "4 MAR 1918"),
 (46, 0.2, "under", "WIRELESS ABOARD  ·  NO MESSAGE EVER CAME"),
 (47, 0.0, "badge", "9 MAR 1918"),
 (47, "molasses|amolco", "under", "THE AMOLCO  ·  MOLASSES  ·  BOUND FOR BOSTON"),
 (48, 0.0, "list", ["BOATS SMASHED", "BRIDGE WRECKED", "RADIO ROOM FLOODED"]),
 (49, "those|nights", "under", "THE MOON: ALMOST NEW"),
 (50, 0.0, "badge", "13 MAR 1918"),
 (50, "doesn", "typecenter_red", "SHE NEVER ARRIVED"),
 (51, "twenty|23", "under", "23 MARCH 1918: RECORDED “MISSING”"),
 (52, 0.0, "badge", "14 APR 1918"),
 (53, 0.0, "quote", ("“...there has been no bad weather nor fighting\nin the ship's zone.”", "NAVY TELEGRAM TO THE FAMILIES  ·  14 APRIL 1918")),
 (54, 0.2, "under", "8 MARCH: A FRONT  ·  9-10 MARCH: A GALE OFF VIRGINIA"),
 (55, 0.2, "under", "“THE WHOLE THING IS AN ENIGMA”  ·  A NAVY OFFICIAL, APRIL 1918"),
 (56, 0.0, "typecenter", "THE RUMORS"),
 (57, 0.0, "list", ["SAILED TO GERMANY", "SEEN IN THE KIEL CANAL", "CREW IN A GERMAN CAMP", "A SPY IN THE COAL"]),
 (58, 0.0, "under", "1918: “DID GIANT SQUIDS DEVOUR THE CYCLOPS?”"),
 (58, "bottle|august", "under", "AUG 1918  ·  A NOTE IN A BOTTLE  ·  A HOAX"),
 (59, "unfounded|every", "stamp", ("ALL UNFOUNDED", 1240, 400)),
 (60, 0.3, "under", "U-151 LEFT GERMANY 14 APRIL 1918  ·  REACHED U.S. WATERS 15 MAY"),
 (61, 0.0, "badge", "14 DEC 1918"),
 (61, "admiral|german", "quote", ("“...no information concerning her fate\nwas to be had in Germany.”", "ADMIRAL GOETTE, KIEL  ·  14 DECEMBER 1918")),
 (62, 0.0, "badge", "14 JUN 1918"),
 (63, 0.2, "under", "ANDREW T. ASKIN  ·  MESS ATTENDANT, 22  ·  STEELTON, PA."),
 (64, 0.0, "list", ["BACK PAY: HELD UP", "UNDER 1/3 INSURED"]),
 (66, 0.2, "typecenter", "THE NAVY'S DEADLIEST LOSS OF WWI"),
 (66, "war|one", "subpop", None),
 (67, "three|3", "typecenter", "3 EXPLANATIONS"),
 (68, 0.0, "under", "1  ·  SHE BROKE IN TWO"),
 (69, 0.0, "under", "2  ·  SHE ROLLED OVER"),
 (70, 0.0, "under", "THEORY: A SHIFTING LOAD + LOOSE WATER"),
 (71, 0.0, "under", "3  ·  THE STORM OF 9-10 MARCH"),
 (72, 0.2, "under", "A NAVY REPORT: “SUDDEN SHIFTING OF CARGO”"),
 (72, "conjecture|secretary", "stamp", ("“ALL CONJECTURE”", 1260, 400)),
 (73, "again|twice", "typecenter", "IT HAPPENED AGAIN. TWICE."),
 (75, 0.2, "under", "NEITHER SEEN AGAIN  ·  NO U-BOAT CLAIM"),
 (76, 0.0, "badge", "1968"),
 (77, 0.0, "quote", ("“...a very old cargo ship\nwith two cradled booms forward.”", "DEAN HAWES, NAVY DIVER")),
 (78, 0.0, "quote", ("“I cannot say that the ship I saw\nwas definitely the Cyclops.”", "DEAN HAWES")),
 (79, 0.0, "under", "MYTH: LOST IN THE BERMUDA TRIANGLE"),
 (79, "name|nineteen", "stamp", ("NAMED IN 1964", 1240, 400)),
 (80, 0.0, "under", "MYTH: THE NAVY'S BIGGEST LOSS OUTSIDE COMBAT"),
 (80, "frigate|historians", "list", ["1800  ·  THE FRIGATE INSURGENT", "1944  ·  THE DESTROYER SPENCE"]),
 (81, 0.0, "typecenter", "WHAT NOBODY KNOWS"),
 (82, 0.0, "under", "WHERE  ·  WHEN  ·  HOW"),
 (83, 0.2, "under", "WHY BARBADOS?  WHY SOUTH?"),
 (86, 0.3, "under", "NEVER A SINGLE PLANK"),
 (88, 0.0, "under", "WHY DO YOU THINK SHE STEAMED SOUTH?  TELL ME BELOW"),
]
def OT(ln, off): return T[ln] + off if isinstance(off, (int, float)) else (wt(ln, off) or T[ln] + 0.3)

CREW = [("C3", None, "EARNEST R. CRAMMER", "SEAMAN"), ("C1", CROP["C1"], "GORDON DEWEES", "SEAMAN"),
        ("C2", CROP["C2"], "CHAS. S. ASHBEE", "SEAMAN"), ("C4", None, "ROY S. MERRIAM", "COXSWAIN")]

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
            L.text(c, "FILE 09  ·  USS CYCLOPS  ·  MARCH 1918", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
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

def crew_frame(a, t, t0, t1):
    """four of the men lost with her (Navy Department / NHHC photos), as prints on the blurred ship"""
    c = blur_bg("B1", CROP.get("B1")).copy(); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    for i, (rid, crop, name, rate) in enumerate(CREW):
        x = 270 + i * 460; card = pcard_h(rid, crop, 520, (-2, 1.5, -1, 2)[i]); L.drop(c, card, x, H / 2 - 60, t, t0 + 0.2 + i * 0.35)
        L.typewriter(c, name, t, t0 + 0.5 + i * 0.35, x, H / 2 + 260, size=34, cps=40, anchor="mm", cursor=False)
        L.typewriter(c, rate, t, t0 + 0.7 + i * 0.35, x, H / 2 + 302, size=26, fill=STEEL, cps=40, anchor="mm", cursor=False)
    L.typewriter(c, "LOST WITH USS CYCLOPS, 1918  ·  306 ABOARD BY THE NAVY'S COUNT  ·  NAVY DEPARTMENT / NHHC PHOTOS", t, t0 + 2.0, W / 2, 1010, size=22, fill=STEEL, cps=80, anchor="mm", cursor=False)
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
    elif kind == "crew": c = crew_frame(a, t, t0, t1)
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
    if kind not in ("tcard", "crew", "end"): draw_badge(c, t)
    return c

# ------------------------------------------------------------------ audio
def load(p, sr=48000):
    a, s = sf.read(p, dtype="float32", always_2d=True); a = a.mean(1)
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    return a
def tl(i, off=0.0): return T[i] + off
RADIO = set()
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
    music("Thunder Dreams.mp3", 0.0, tl(8), -20); music("Floating Cities.mp3", tl(8), tl(25), -21); music("Rising Tide.mp3", tl(25), tl(45), -21)
    music("Man Down.mp3", tl(45), tl(56), -21); music("Thunder Dreams.mp3", tl(56), tl(67), -20); music("Promises to Keep.mp3", tl(67), tl(81), -21)
    music("Thunder Dreams.mp3", tl(81), DUR, -20)
    loop("waves_harbor_rocks", tl(8), tl(10), -31); loop("ship_hull_creak", tl(27), tl(28), -30); loop("waves_rough_sea_loop", tl(47), tl(50), -30)
    loop("wind_scary", tl(49), tl(50), -32); loop("waves_windy_sea_loop", tl(53), tl(55), -32); loop("wind_deep_cinematic_hum", tl(81), tl(87), -31)
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
    EV = [(0, 0.0, "ship_hull_creak", -28), (3, 0.0, "typewriter_typing_old", -22), (4, "whistle", "ship_engine_loop", -30), (5, 0.2, "hit_deep_heartbeat_impact", -15),
          (18, "cable", "typewriter_typing_old", -22), (19, 0.0, "hit_cinematic_deep_impact", -15), (21, "whistle", "whoosh_ghostly", -26), (30, "blows", "metal_hammer_hit", -20),
          (38, "where", "paper_writing_pencil", -24), (39, "germany", "hit_short_bass", -18), (46, "radio|wireless", "radio_static_fx", -26), (47, "storm", "thunder_deep_rumble", -20),
          (50, "doesn", "hit_deep_heartbeat_impact", -15), (53, 0.0, "typewriter_typing_old", -22), (60, "left|germany", "hit_glass_suspense", -20),
          (62, "june|fourteenth", "hit_cinematic_deep_impact", -16), (73, "twice", "hit_horror_drum", -18), (77, "cargo|booms", "sea_water_splash", -26),
          (85, "stamped|cable", "typewriter_return_bell", -20), (88, 0.2, "typewriter_return_bell", -18)]
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
    name = name or "TheLastHours_09_Cyclops.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "The last message: coal"), (8, "Sunday, 5:30 PM: Barbados"), (18, "Monday: the last word, and south"), (25, "January: the voyage down"),
      (32, "Rio: the ore"), (37, "Who was George Worley?"), (45, "March 4-13: silence and a storm"), (51, "The telegram"), (56, "Spies, squids and U-boats"),
      (62, "June 14, 1918"), (67, "Three explanations"), (73, "It happened again. Twice."), (79, "Myths"), (81, "What nobody knows")]

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
