"""The Last Hours #2: Franklin's lost expedition (Case File style, 1920x1080). Built on render_alcatraz.py.
Every shot starts on a narration line (index into vo_lines.txt without '##'), optionally at a spoken word.
  python render_franklin.py times | qa <t..> | seg <i> <n> | audio | final <n> | all <n>"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []   # 16:9 panels, no province lines in the Arctic
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/03_franklin/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 20.0

# ------------------------------------------------------------------ narration timing
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES, PAUSE = [], []
for l in RAW:
    if l == "##":
        if PAUSE: PAUSE[-1] = 0.9
    else: LINES.append(l); PAUSE.append(0.35)
DURS = {}
if os.path.exists(ROOT + "vo/vo.log"):
    for m in re.finditer(r"^(\d+)/(\d+)\s+([\d.]+)s audio", open(ROOT + "vo/vo.log", encoding="utf-8", errors="ignore").read(), re.M):
        DURS[int(m.group(1)) - 1] = float(m.group(3))
T = []; t = LEAD
for i, l in enumerate(LINES):
    T.append(t); t += DURS.get(i, 0.37 * len(l.split()) + 0.2) + PAUSE[i]
VO_END = t; DUR = VO_END + TAIL; NF = int(DUR * FPS)
def tl(i, off=0.0): return T[i] + off
WORDS = {}                                     # line -> [(seconds after the line starts, word)] (whisper, one slice per line)
if os.path.exists(ROOT + "vo/vo_words.json"):
    for sg in json.load(open(ROOT + "vo/vo_words.json", encoding="utf-8")):
        WORDS[sg["line"]] = [(w["s"] - sg["start"], w["w"]) for w in sg["words"]]
def wt(line, word, off=0.0):
    """video-clock time the narrator says `word` (prefix match, 'a|b' = either) inside script line `line`; None if not heard"""
    for rel, w in WORDS.get(line, []):
        if any(re.sub(r"[^a-z0-9]", "", w.lower()).startswith(x) for x in word.lower().split("|")): return T[line] + rel + off
    return None

# ------------------------------------------------------------------ assets
def P(rid):
    fs = glob.glob(M + rid + "_*")
    ok = [f for f in fs if open(f, "rb").read(3) == b"\xff\xd8\xff" or open(f, "rb").read(4) == b"\x89PNG"]
    return ok[0] if ok else None
FALLBACK = "G6"
IMG = {}
def prep():
    """rotated plates are saved once, before the parallel render starts"""
    for ln, (kind, a) in SHOTS:
        if kind == "kb" and a["rot"] and not os.path.exists(B + f"_rot_{a['rid']}_{a['rot']}.png"):
            Image.open(P(a["rid"])).convert("RGB").rotate(a["rot"], expand=True).save(B + f"_rot_{a['rid']}_{a['rot']}.png")
def tone(rid, crop=None, rot=0):
    k = (rid, crop, rot)
    if k not in IMG:
        p = (B + f"_rot_{rid}_{rot}.png") if rot else (P(rid) or P(FALLBACK))
        IMG[k] = L.bw(p, crop)
    return IMG[k]

NOTE = "B2"                                                     # 1859 lithographed facsimile of the Victory Point record
DOCROT = {"note": 0, "note_cw": -90, "note_180": 180}
PH = {
 "note": {"allwell": (1140, 1060, 1550, 1170), "date": (210, 450, 680, 540), "wrong": (560, 570, 900, 660), "franklin": (150, 950, 1560, 1075),
          "monday": (210, 2430, 1560, 2580), "signs": (880, 2560, 1560, 2700), "whoever": (200, 1170, 1500, 1340)},
 "note_cw": {"deserted": (1300, 90, 2070, 140), "beset": (420, 138, 1100, 192), "souls": (1790, 138, 2090, 196), "crozier": (400, 188, 1250, 242),
             "irving": (400, 238, 1600, 292), "died": (1180, 1572, 2210, 1645), "lategore": (300, 1525, 760, 1578)},
 "note_180": {"start": (100, 2620, 700, 2780), "losses": (250, 2480, 1700, 2600), "fitzjames": (850, 2620, 1520, 2750), "crozier": (150, 2540, 460, 2680)},
}
MARK_WORD = {("note", "allwell"): "all", ("note", "wrong"): "1846|eighteen", ("note", "whoever"): "whoever",("note", "monday"): "monday", ("note", "signs"): "gore",
             ("note_cw", "deserted"): "deserted", ("note_cw", "beset"): "beset", ("note_cw", "souls"): "souls", ("note_cw", "crozier"): "crozier",
             ("note_cw", "died"): "died", ("note_cw", "lategore"): "commander", ("note_180", "start"): "start", ("note_180", "losses"): "nine",
             ("note_180", "crozier"): "crozier", ("note_180", "fitzjames"): "fitzjames"}
def page_img(key):
    k = ("doc", key)
    if k not in IMG:
        im = Image.open(P(NOTE)).convert("L")
        if DOCROT[key]: im = im.rotate(DOCROT[key], expand=True)
        a = np.asarray(im, np.float32); lo, hi = np.percentile(a, 1), np.percentile(a, 99.5); a = np.clip((a - lo) / (hi - lo), 0, 1)
        IMG[k] = Image.fromarray((a[..., None] * np.array([236, 230, 214], np.float32)).astype(np.uint8))
    return IMG[k]

# map points (lon, lat)
GREEN, DISKO, MELV, LANC, BEECH = (0.28, 51.45), (-53.4, 69.0), (-63.0, 75.2), (-84.0, 74.3), (-91.654, 74.724)
WELL77, CORNW, PEEL, BESET = (-92.8, 77.0), (-98.2, 75.2), (-96.6, 72.8), (-98.383, 70.083)
VICT, SHIPS48, BACKR, EREBUS14, TERRORB, EREBAY = (-98.683, 69.628), (-98.95, 69.856), (-96.2, 67.4), (-98.70, 68.23), (-98.95, 68.87), (-98.85, 69.05)
SOUTHC = (-97.6, 68.55)
V_PASS, V_NATL, V_ARCH, V_KWI, V_SOUTH = (-95.0, 68.0, 150.0), (-35.0, 66.0, 125.0), (-92.0, 74.0, 56.0), (-98.2, 69.6, 8.0), (-97.6, 68.5, 13.0)

# ------------------------------------------------------------------ shot constructors
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, rot=0): return ("kb", dict(rid=rid, crop=crop, z=z, c0=c0, c1=c1 or c0, rot=rot))
def CARD(big, sub): return ("card", dict(big=big, sub=sub))
def DOC(key, focus, z=(0.9, 1.2), marks=()): return ("doc", dict(key=key, focus=focus, z=z, marks=marks))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def PRINTS(items, bg=None): return ("prints", dict(items=items, bg=bg))
def FACES(): return ("faces", {})
def BLACK(): return ("black", {})
OFFICERS = [f"A{i}" for i in range(1, 15)]
D1_SHIPS, D1_CAB, D1_PORT = (0.12, 0.30, 0.88, 0.62), (0.03, 0.74, 0.97, 0.985), (0.30, 0.03, 0.70, 0.29)
C9_HEAD, D12_TOP, D12_MID = (0.0, 0.0, 1.0, 0.33), (0.04, 0.03, 0.96, 0.36), (0.04, 0.36, 0.96, 0.72)
D15_TOP, D16_ALL, NOTE_ALL = (0.06, 0.05, 0.94, 0.47), (0.08, 0.05, 0.92, 0.95), (0, 0, 1736, 2792)
LMARGIN = (400, 85, 2780, 300)
def pr(rid, x, label=None, d=0.1, w=430, rot=-2, y=None): return (rid, None, w, x, (y or H / 2 - 40), rot, d, label)

SHOTS = [
 (0, ("coldopen", {})),
 (1, KB("G9", z=(1.04, 1.16), c0=(0.5, 0.6))),
 (2, DOC("note", PH["note"]["allwell"], z=(1.0, 1.25), marks=[("allwell", 0.3)])),
 (3, DOC("note", NOTE_ALL, z=(1.5, 1.7))),
 (4, DOC("note_cw", (1200, 80, 2300, 210), z=(1.0, 1.2), marks=[("deserted", 0.3), ("souls", 2.0)])),
 (5, DOC("note_cw", PH["note_cw"]["died"], z=(1.0, 1.2), marks=[("died", 0.3)])),
 (6, DOC("note_180", (80, 2500, 760, 2790), z=(1.0, 1.2), marks=[("start", 1.5)])),
 (7, BLACK()),
 (8, FACES()),
 (9, PRINTS([pr("B1", W / 2, None, 0.1, 470, -1.5, H / 2 - 10)])),
 (10, KB("G8", z=(1.05, 1.15))),
 (11, KB("G6", z=(1.02, 1.12))),
 (12, ("title", {})),
 (13, KB("D1", crop=D1_SHIPS, z=(1.05, 1.18))),
 (14, KB("D2", z=(1.0, 1.12), c0=(0.55, 0.5))),
 (15, KB("G7", z=(1.0, 1.12), c0=(0.45, 0.4))),
 (16, NMAP(V_PASS, ops=[("route", [(-60, 66), (-75, 73.5), (-95, 74.5), (-105, 71), (-125, 70.5), (-145, 71.2), (-168, 66)], 0.4, 4.0),
                        ("label", -45, 60, "ATLANTIC", 0.2, 34), ("label", -150, 53, "PACIFIC", 0.6, 34)])),
 (17, KB("C3", z=(1.0, 1.12))),
 (18, KB("C2", z=(1.0, 1.15), c0=(0.5, 0.5))),
 (19, KB("A1", z=(1.0, 1.12), c0=(0.5, 0.42))),
 (20, PRINTS([pr("A2", W / 2 - 300, "FRANCIS CROZIER  ·  TERROR", 0.1), pr("A3", W / 2 + 300, "JAMES FITZJAMES  ·  EREBUS", 0.9, rot=2)])),
 (21, PRINTS([pr("A5", W / 2 - 560, None, 0.1, 380), pr("A8", W / 2, None, 0.6, 380, 1.5), pr("A6", W / 2 + 560, None, 1.1, 380, -1)])),
 (22, FACES()),
 (23, NMAP(V_NATL, ops=[("route", [GREEN, (-20, 58), (-45, 60), DISKO], 0.2, 2.5), ("pin", *DISKO, "DISKO BAY, GREENLAND", 2.4)])),
 (24, KB("D1", crop=D1_CAB, z=(1.0, 1.1))),
 (25, KB("G3", z=(1.02, 1.12))),
 (26, CARD("134 - 5", "Sent home sick from Greenland")),
 (27, CARD("129", "Sail on into the Arctic")),
 (29, NMAP(V_NATL, ops=[("route", [DISKO, (-58, 72.5), MELV], 0.2, 1.8), ("pin", *MELV, "LAST SEEN · LATE JULY 1845", 1.8)])),
 (30, KB("G3", z=(1.1, 1.2), c0=(0.6, 0.5))),
 (31, KB("D17", crop=(0.05, 0.12, 0.95, 0.62), z=(1.0, 1.1))),
 (32, NMAP(V_ARCH, ops=[("route", [LANC, (-88, 74.4), BEECH], 0.2, 2.2), ("label", -84, 72.6, "LANCASTER SOUND", 0.6, 28)])),
 (33, NMAP(V_ARCH, ops=[("route", [BEECH, (-91.8, 75.3), WELL77, (-96.5, 76.5), CORNW, BEECH], 0.2, 3.5), ("label", -95.2, 75.0, "CORNWALLIS IS.", 0.5, 26)])),
 (34, KB("D7", z=(1.0, 1.12))),
 (35, KB("D6", z=(1.02, 1.18), c0=(0.5, 0.55))),
 (38, KB("E5", crop=(0.1, 0.18, 0.9, 0.82), z=(1.0, 1.12))),
 (39, ("letter", {})),
 (40, KB("E1", z=(1.0, 1.12))),
 (41, BLACK()),
 (42, NMAP(V_ARCH, ops=[("pin", *BEECH, "BEECHEY ISLAND", 0.0), ("route", [BEECH, (-94.5, 74.2), PEEL, (-97.2, 71.3), BESET], 0.3, 3.0)])),
 (43, NMAP(V_KWI, ops=[("pin", *BESET, "BESET · SEPT 12, 1846", 0.3)], c0=(0.5, 0.45))),
 (44, KB("G1", z=(1.02, 1.12))),
 (45, KB("D4", z=(1.0, 1.15), c0=(0.45, 0.6))),
 (46, KB("D5", crop=(0.08, 0.12, 0.92, 0.58), z=(1.0, 1.12))),
 (47, KB("G4", z=(1.02, 1.12))),
 (48, CARD("MAY 24, 1847", "A Monday")),
 (49, PRINTS([pr("A4", W / 2 - 300, "LT. GRAHAM GORE", 0.1), pr("A7", W / 2 + 300, "CHARLES DES VOEUX, MATE", 0.7, rot=2)])),
 (50, KB("G2", z=(1.02, 1.15))),
 (51, DOC("note", (200, 1160, 1500, 2350), z=(0.95, 1.05), marks=[("whoever", 0.5)])),
 (52, DOC("note", (210, 440, 1560, 560), z=(0.95, 1.1))),
 (53, DOC("note", (160, 560, 1600, 900), z=(1.0, 1.15), marks=[("wrong", 2.5)])),
 (54, DOC("note", PH["note"]["allwell"], z=(1.1, 1.3), marks=[("allwell", 0.6)])),
 (55, DOC("note", (200, 2420, 1600, 2720), z=(1.0, 1.12), marks=[("signs", 0.2)])),
 (56, CARD("MAY 28, 1847", "All well")),
 (57, KB("A1", z=(1.1, 1.22), c0=(0.5, 0.4))),
 (58, CARD("JUNE 11, 1847", "Sir John Franklin dies. Age 61")),
 (59, KB("G6", z=(1.05, 1.15))),
 (61, FACES()),
 (62, CARD("24 DEAD", "9 officers  ·  15 men")),
 (63, KB("A4", z=(1.0, 1.12), c0=(0.5, 0.42))),
 (64, DOC("note_cw", PH["note_cw"]["lategore"], z=(1.0, 1.2), marks=[("lategore", 0.8)])),
 (65, KB("D5", crop=(0.08, 0.12, 0.92, 0.58), z=(1.12, 1.25))),
 (66, KB("G5", z=(1.02, 1.12))),
 (67, ("cta", {})),
 (70, BLACK()),
 (71, CARD("APRIL 22, 1848", "The ships are deserted")),
 (72, KB("D4", z=(1.15, 1.3), c0=(0.5, 0.6))),
 (73, KB("G2", z=(1.1, 1.2))),
 (74, NMAP(V_KWI, ops=[("pin", *SHIPS48, "SHIPS LEFT HERE", 0.0, -330, 0), ("route", [SHIPS48, VICT], 0.4, 2.0)], c0=(0.5, 0.45))),
 (75, NMAP(V_KWI, ops=[("pin", *SHIPS48, "", -9), ("route", [SHIPS48, VICT], -9, 0.1), ("pin", *VICT, "VICTORY POINT", 0.2)], c0=(0.5, 0.45))),
 (76, KB("G9", z=(1.05, 1.15), c0=(0.4, 0.5))),
 (77, KB("A3", z=(1.0, 1.12), c0=(0.5, 0.42))),
 (78, DOC("note", NOTE_ALL, z=(1.55, 1.75))),
 (79, DOC("note_cw", (400, 70, 2100, 260), z=(1.0, 1.12), marks=[("deserted", 0.3), ("beset", 2.0)])),
 (80, DOC("note_cw", (400, 130, 2100, 250), z=(1.0, 1.12), marks=[("souls", 0.3), ("crozier", 1.8)])),
 (81, DOC("note_cw", PH["note_cw"]["died"], z=(1.0, 1.2), marks=[("died", 0.3)])),
 (82, DOC("note_180", (100, 2500, 800, 2790), z=(1.0, 1.2), marks=[("crozier", 0.2)])),
 (83, DOC("note_180", (80, 2580, 760, 2790), z=(1.0, 1.25), marks=[("start", 1.5)])),
 (84, DOC("note_180", PH["note_180"]["start"], z=(1.3, 1.6))),
 (85, NMAP(V_SOUTH, ops=[("pin", *VICT, "VICTORY POINT", 0.0), ("pin", *BACKR, "BACK'S FISH RIVER", 0.6)])),
 (86, NMAP(V_SOUTH, ops=[("pin", *VICT, "", -9), ("pin", *BACKR, "BACK'S FISH RIVER", -9),
                         ("route", [VICT, (-98.9, 69.2), (-98.6, 68.7), (-97.6, 68.3), (-96.8, 67.9), BACKR, (-97.6, 66.8)], 0.3, 4.0)])),
 (87, KB("G8", z=(1.02, 1.12))),
 (88, KB("D16", crop=D16_ALL, z=(1.0, 1.12))),
 (89, DOC("note", NOTE_ALL, z=(1.5, 1.62))),
 (90, KB("D17", crop=(0.05, 0.12, 0.95, 0.62), z=(1.05, 1.15))),
 (91, BLACK()),
 (92, KB("G6", z=(1.0, 1.1))),
 (93, KB("D9", z=(1.0, 1.12))),
 (94, KB("C1", z=(1.0, 1.25), c0=(0.5, 0.18), c1=(0.5, 0.3))),
 (95, CARD("MARCH 31, 1854", "Declared dead. Pay stops")),
 (96, KB("E4", z=(1.0, 1.12), c0=(0.5, 0.3))),
 (97, KB("G5", z=(1.0, 1.12))),
 (98, KB("G2", z=(1.0, 1.12))),
 (99, KB("G1", z=(1.0, 1.1))),
 (100, NMAP(V_SOUTH, ops=[("pin", *BACKR, "~30 BODIES (INUIT ACCOUNT)", 0.4)])),
 (101, KB("G6", z=(1.08, 1.15))),
 (102, BLACK()),
 (103, KB("C9", crop=C9_HEAD, z=(1.0, 1.12))),
 (104, KB("C8", crop=(0.05, 0.02, 0.95, 0.5), z=(1.0, 1.12))),
 (105, KB("D13", z=(1.0, 1.12))),
 (106, KB("D14", crop=(0.06, 0.08, 0.93, 0.92), rot=-90, z=(1.02, 1.14))),
 (107, CARD("MAY 6, 1859", "11:15 a.m.")),
 (108, KB("D15", crop=D15_TOP, z=(1.0, 1.12))),
 (109, DOC("note", PH["note"]["allwell"], z=(0.8, 1.0), marks=[("allwell", 0.8)])),
 (110, DOC("note", NOTE_ALL, z=(1.5, 1.62))),
 (111, KB("D16", crop=D16_ALL, z=(1.1, 1.2), c0=(0.5, 0.6))),
 (112, KB("E3", z=(1.0, 1.1), c0=(0.5, 0.35))),
 (113, CARD("MAY 24, 1859", "Just after midnight")),
 (114, KB("G9", z=(1.05, 1.15), c0=(0.5, 0.7))),
 (116, KB("G8", z=(1.05, 1.12))),
 (117, KB("G4", z=(1.05, 1.15))),
 (118, CARD("2026", "DNA: it was Peglar")),
 (119, NMAP(V_KWI, ops=[("pin", *EREBAY, "THE BOAT · EREBUS BAY · ~3 P.M.", 0.3, -650, 0)], c0=(0.5, 0.6))),
 (120, KB("D16", crop=D16_ALL, z=(1.0, 1.1))),
 (121, CARD("1,400 LB", "Boat and sledge")),
 (122, BLACK()),
 (123, KB("D16", crop=(0.08, 0.05, 0.55, 0.6), z=(1.0, 1.15))),
 (124, KB("D12", crop=D12_MID, z=(1.0, 1.12))),
 (125, CARD("40 LB", "of chocolate. No meat. No bread.")),
 (126, NMAP(V_KWI, ops=[("pin", *EREBAY, "THE BOAT", -9, -200, 0), ("arrow", EREBAY, SHIPS48, "NORTHEAST: TOWARD THE SHIPS", 0.3)], c0=(0.5, 0.55))),
 (127, KB("D17", crop=(0.05, 0.12, 0.95, 0.62), z=(1.1, 1.2))),
 (128, KB("G5", z=(1.05, 1.15))),
 (129, KB("G8", z=(1.05, 1.15))),
 (131, KB("G4", z=(1.05, 1.18))),
 (132, BLACK()),
 (133, KB("D16", crop=(0.4, 0.55, 0.95, 0.95), z=(1.0, 1.15))),
 (134, KB("E7", z=(1.0, 1.12))),
 (135, KB("G1", z=(1.05, 1.15))),
 (136, BLACK()),
 (137, KB("G9", z=(1.0, 1.1))),
 (138, KB("E4", z=(1.05, 1.15), c0=(0.5, 0.3))),
 (139, KB("F2", z=(1.0, 1.15))),
 (140, CARD("SEPT 2, 2014", "Wilmot and Crampton Bay")),
 (141, KB("F1", z=(1.0, 1.15), c0=(0.5, 0.5))),
 (142, CARD("36 FT", "Depth of the wreck")),
 (143, NMAP(V_SOUTH, ops=[("circle", *EREBUS14, 6, "HMS EREBUS · 2014", 0.2)])),
 (145, NMAP(V_SOUTH, ops=[("circle", *EREBUS14, 6, "", -9), ("circle", *TERRORB, 6, "HMS TERROR · 2016", 0.8)])),
 (146, CARD("SEPT 2016", "HMS Terror")),
 (147, KB("C2", z=(1.0, 1.15), c0=(0.4, 0.5))),
 (149, KB("C2", z=(1.3, 1.5), c0=(0.35, 0.55))),
 (151, KB("G6", z=(1.05, 1.15))),
 (152, KB("G9", z=(1.0, 1.12), c0=(0.5, 0.65))),
 (153, FACES()),
 (154, KB("G3", z=(1.0, 1.1))),
 (155, KB("A3", z=(1.0, 1.12), c0=(0.5, 0.42))),
 (156, NMAP(V_KWI, ops=[("pin", *EREBAY, "EREBUS BAY", 0.3)], c0=(0.5, 0.6))),
 (157, KB("A3", z=(1.15, 1.25), c0=(0.5, 0.4))),
 (158, BLACK()),
 (159, CARD("6 OF 129", "Have their names back")),
 (160, CARD("123", "Still don't")),
 (161, PRINTS([pr("B1", W / 2, None, 0.1, 470, 1.5, H / 2 - 10)])),
 (162, FACES()),
 (163, DOC("note", PH["note"]["allwell"], z=(1.0, 1.2), marks=[("allwell", 0.8)])),
 (164, DOC("note_cw", (1200, 80, 2300, 210), z=(1.0, 1.15), marks=[("souls", 1.0, "hundred")])),
 (165, KB("A1", z=(1.1, 1.2), c0=(0.5, 0.42))),
 (166, KB("G8", z=(1.0, 1.1))),
 (167, KB("G9", z=(1.05, 1.15))),
 (168, KB("C2", z=(1.45, 1.6), c0=(0.35, 0.55))),
 (169, DOC("note_180", (80, 2580, 760, 2790), z=(1.0, 1.15), marks=[("start", 0.6)])),
 (170, ("end", {})),
]
SHOT_LINES = [s[0] for s in SHOTS]

# overlays: (line, offset, kind, args)  (one text per screen slot: bottom / center / side)
OV = [
 (2, 0.2, "lower", "THE VICTORY POINT RECORD  ·  1847 / 1848"),
 (4, 0.0, "lower", "\u201cTERROR AND EREBUS WERE DESERTED ON THE 22ND APRIL\u201d"),
 (5, 0.0, "lower", "\u201cSIR JOHN FRANKLIN DIED ON THE 11TH OF JUNE 1847\u201d"),
 (6, 0.0, "lower", "\u201cAND START ON TOMORROW 26TH FOR BACKS FISH RIVER\u201d"),
 (8, 0.3, "under", "129 MEN  ·  NONE CAME HOME"),
 (9, 0.3, "lower", "FACSIMILE WITH THE RUST STAINS  ·  McCLINTOCK, 1869"),
 (13, 0.3, "lower", "DEPARTURE  ·  ILLUSTRATED LONDON NEWS, MAY 24, 1845"),
 (14, 0.2, "lower", "HMS EREBUS & HMS TERROR  ·  ENGRAVING, 1845"),
 (15, 0.0, "typecenter", "134 MEN"),
 (17, 0.3, "lower", "THE ARCTIC AS KNOWN IN 1845"),
 (18, 0.3, "lower", "ADMIRALTY PLAN, MARCH 1845  ·  THE NEW SCREW PROPELLER"),
 (19, 0.3, "lower", "SIR JOHN FRANKLIN  ·  DAGUERREOTYPE, MAY 1845"),
 (21, 0.4, "under", "DAGUERREOTYPES, 1845  ·  STUDIO OF RICHARD BEARD"),
 (24, 0.3, "lower", "OFFICERS' CABINS  ·  ILLUSTRATED LONDON NEWS, 1845"),
 (25, 0.3, "under", "JOHN GREGORY  ·  ENGINEER  ·  LETTER OF JULY 9, 1845"),
 (31, 0.3, "lower", "ENGRAVING, 1859"),
 (34, 0.3, "lower", "BEECHEY ISLAND  ·  WINTER QUARTERS 1845–46  ·  ENGRAVING"),
 (35, 0.2, "lower", "JOHN TORRINGTON  ·  TERROR  ·  DIED JAN 1, 1846  ·  AGE 20"),
 (36, 0.2, "lower", "JOHN HARTNELL  ·  EREBUS  ·  DIED JAN 4, 1846  ·  AGE 25"),
 (37, 0.2, "lower", "WILLIAM BRAINE  ·  ROYAL MARINES  ·  DIED APR 3, 1846  ·  AGE 32"),
 (38, 0.3, "lower", "BEECHEY ISLAND  ·  PHOTOGRAPH, 1904"),
 (40, 0.3, "lower", "FRANKLIN SEARCH SHIPS  ·  PHOTOGRAPH, 1852"),
 (41, 0.0, "typecenter", "NO NOTE."),
 (45, 0.3, "lower", "EREBUS AND TERROR IN THE ICE  ·  ENGRAVING, 1860"),
 (51, 0.2, "lower", "\u201cWHOEVER FINDS THIS PAPER...\u201d  ·  IN 6 LANGUAGES"),
 (53, 0.3, "under", "IT WAS 1845–46"),
 (57, 0.2, "typecenter", "+ 14 DAYS"),
 (60, 0.2, "stamp", ("GRAVE NEVER FOUND", W / 2, H - 200)),
 (64, 0.2, "lower", "\u201cTHE LATE COMMANDER GORE\u201d"),
 (65, 0.3, "under", "TRAPPED: 588 DAYS"),
 (66, 0.3, "under", "McCLINTOCK: PROVISIONED ONLY UP TO JULY 1848"),
 (72, 0.0, "typecenter", "105 MEN"),
 (74, 0.2, "under", "~17 MILES"),
 (77, 0.3, "lower", "CAPTAIN JAMES FITZJAMES  ·  1845"),
 (84, 0.3, "under", "LT. HOBSON'S OPINION, 1859"),
 (88, 0.0, "list_side", ["CLOTHES", "TOOLS", "STOVES", "OARS"]),
 (88, 0.0, "lower", "ITEMS FOUND IN 1859  ·  ILLUSTRATED LONDON NEWS"),
 (90, 0.3, "under", "THE LAST RECORD EVER FOUND"),
 (93, 0.3, "lower", "SEARCH SQUADRON, 1850  ·  ENGRAVING"),
 (93, 1.2, "typecenter", "32 SEARCH EXPEDITIONS"),
 (94, 0.3, "lower", "ADMIRALTY REWARD POSTER  ·  MARCH 7, 1850"),
 (96, 0.3, "lower", "DR. JOHN RAE  ·  HUDSON'S BAY COMPANY"),
 (98, 0.3, "under", "INUIT TESTIMONY  ·  RECORDED BY RAE, 1854"),
 (102, 0.0, "quote", ("\u201c...driven to the last dread alternative as a means of sustaining life.\u201d", "JOHN RAE  ·  REPORT, 1854")),
 (103, 0.3, "lower", "RAE'S REPORT IN PRINT  ·  ILLUSTRATED LONDON NEWS, 1854"),
 (105, 0.3, "lower", "THE FOX  ·  ENGRAVING, 1859"),
 (106, 0.3, "lower", "A SLEDGE PARTY FROM THE FOX AT A CAIRN  ·  ENGRAVING, 1859"),
 (108, 0.3, "lower", "A SEARCH PARTY AT A CAIRN  ·  ILLUSTRATED LONDON NEWS, 1859"),
 (110, 0.3, "under", "APRIL 1848 → MAY 1859"),
 (111, 0.3, "lower", "OBJECTS FOUND IN 1859  ·  ILLUSTRATED LONDON NEWS"),
 (112, 0.4, "quote", ("\u201cA sad tale was never told in fewer words.\u201d", "F. L. McCLINTOCK  ·  1859")),
 (116, 0.3, "under", "HARRY PEGLAR  ·  CAPTAIN OF THE FORETOP"),
 (117, 0.0, "list", ["PEGLAR?", "OR A STEWARD WITH HIS PAPERS?"]),
 (120, 0.3, "under", "28 FT  ·  ON A HEAVY SLEDGE"),
 (122, 0.0, "typecenter", "2 SKELETONS"),
 (123, 0.3, "lower", "RELICS FROM THE BOAT  ·  ILLUSTRATED LONDON NEWS, 1859"),
 (124, 0.2, "lower", "SILVER FROM THE EXPEDITION  ·  ILLUSTRATED LONDON NEWS, 1854"),
 (124, 0.0, "list_side", ["SILVER FORKS & SPOONS", "5 WATCHES", "A NOVEL", "SOAP", "A TOOTHBRUSH"]),
 (127, 0.4, "under", "McCLINTOCK: TURNING BACK?  ·  NOBODY KNOWS"),
 (129, 0.3, "quote", ("\u201c...fell down and died as they walked along.\u201d", "AN INUK, TO McCLINTOCK'S INTERPRETER  ·  1859")),
 (131, 0.3, "under", "INUIT ACCOUNTS"),
 (132, 0.0, "typecenter", "WHAT KILLED THEM?"),
 (133, 0.3, "under", "THEORY: LEAD FROM TIN-CAN SOLDER"),
 (134, 0.3, "lower", "1980s  ·  HIGH LEAD IN THE BEECHEY ISLAND MEN"),
 (135, 0.3, "under", "2014–2018 STUDIES: PROBABLY NOT THE MAIN KILLER"),
 (136, 0.0, "list", ["HUNGER", "COLD", "DISEASE", "SCURVY"]),
 (137, 0.3, "under", "1997 STUDY  ·  CUT MARKS ON ABOUT 1 IN 4 BONES"),
 (138, 0.4, "stamp", ("RAE WAS RIGHT", 1400, 820)),
 (139, 0.3, "lower", "THE CENTRAL CANADIAN ARCTIC FROM SPACE  ·  NASA, 2016"),
 (141, 0.3, "under", "RYAN HARRIS  ·  PARKS CANADA"),
 (144, 0.3, "under", "WHERE INUIT ACCOUNTS POINTED"),
 (145, 0.3, "lower", "SAMMY KOGVIK'S TIP"),
 (147, 0.3, "lower", "2019  ·  PARKS CANADA ROV  ·  SHIP PLAN, 1845"),
 (148, 0.0, "list_side", ["PLATES ON THE SHELVES", "BEDS", "DESKS"]),
 (149, 0.3, "typecenter", "1 CLOSED DOOR"),
 (150, 0.2, "under", "THE CAPTAIN'S SLEEPING CABIN"),
 (151, 0.3, "under", "PAPERS MAY SURVIVE  ·  PARKS CANADA"),
 (154, 0.2, "under", "JOHN GREGORY  ·  ENGINEER  ·  IDENTIFIED 2021"),
 (155, 0.3, "lower", "JAMES FITZJAMES  ·  IDENTIFIED 2024"),
 (158, 0.0, "list", ["WILLIAM ORREN", "DAVID YOUNG", "JOHN BRIDGENS", "HARRY PEGLAR"]),
 (165, 0.4, "stamp", ("GRAVE: NOT FOUND", 1420, 830)),
 (166, 0.3, "under", "THE LAST MAN: UNKNOWN"),
 (167, 0.3, "under", "INUIT ACCOUNTS  ·  NEVER PROVEN"),
 (168, 0.3, "typecenter", "THE CLOSED DOOR"),
]

# ------------------------------------------------------------------ drawing helpers
def shot_at(t):
    k = 0
    for j, ln in enumerate(SHOT_LINES):
        if T[ln] - 0.12 <= t: k = j
    t0 = T[SHOTS[k][0]] - 0.12; t1 = (T[SHOTS[k + 1][0]] - 0.12) if k + 1 < len(SHOTS) else DUR
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

def mark_time(key, mk, shot_line):
    """a mark lands on its spoken word (mk[2] if given, else MARK_WORD); mk[1] = fallback offset from the line start"""
    word = mk[2] if len(mk) > 2 else MARK_WORD.get((key, mk[0]))
    tm = wt(shot_line, word) if word else None
    return tm if tm is not None else T[shot_line] + mk[1]

def lower(c, s, t, t0):
    if t < t0: return
    lay = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); g = np.clip(np.linspace(0, 1, 260) * 1.7, 0, 1)[:, None] ** 1.3 * 238
    lay.putalpha(Image.fromarray(np.repeat(g, W, 1).astype(np.uint8))); c.alpha_composite(lay, (0, H - 260))
    L.typewriter(c, s, t, t0, 90, H - 110, size=38, cps=34, cursor=False)
    L.rule(c, 90, 90 + min(len(s), 40) * 23, H - 76, t, t0 + 0.2, width=5)
def under(c, s, t, t0):
    if t < t0: return
    lay = Image.new("RGBA", (W, 170), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, 0, W, 170), fill=(0, 0, 0, 190))
    c.alpha_composite(lay, (0, H - 170)); L.typewriter(c, s, t, t0, W / 2, H - 92, size=50, cps=30, anchor="mm", cursor=False)

SLOT = {"lower": "bottom", "under": "bottom", "big": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "list_side": "side"}
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    for ln2, off2, kind2, _ in OV[j + 1:]:
        if SLOT.get(kind2) == sl or (sl == "bottom" and kind2 in ("list", "typecenter")): return min(T[ln2] + off2 - 0.05, shot_t1)
    return shot_t1
def draw_ov(c, k, t, shot_t1):
    for j, (ln, off, kind, a) in enumerate(OV):
        t0 = T[ln] + off
        if t < t0 or t >= shot_t1 or ln < SHOTS[k][0]: continue
        if t >= ov_end(j, shot_t1): continue
        if kind == "lower": lower(c, a, t, t0)
        elif kind == "under": under(c, a, t, t0)
        elif kind in ("typecenter", "typecenter_red"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 110, W, H / 2 + 110), fill=(0, 0, 0, 185)); c.alpha_composite(lay)
            L.typewriter(c, a, t, t0, W / 2, H / 2, size=96, fill=RED if kind.endswith("red") else BONE, cps=16, anchor="mm", cursor=False)
        elif kind == "list":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay)
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W / 2, H / 2 - (len(a) - 1) * 60 + i * 120, size=74, cps=20, anchor="mm", cursor=False)
        elif kind == "list_side":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip((np.linspace(0, 1, W) - 0.45) * 3.0, 0, 1)[None, :] * 240
            lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.6, 1180, 260 + i * 95, size=50, cps=24, anchor="lm", cursor=False)
        elif kind == "stamp": L.stamp(c, a[0], a[1], a[2], t, t0, size=100)
        elif kind == "quote":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay)
            L.text(c, a[0], W / 2, H / 2 - 30, 62 if len(a[0]) > 50 else 70, BONE, SER, alpha=ease((t - t0) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, W / 2, H / 2 + 70, size=34, fill=STEEL, cps=34, anchor="mm", cursor=False)

PC = {}
def pcard(rid, crop, w, rot):
    k = (rid, crop, w, rot)
    if k not in PC: PC[k] = L.print_card(tone(rid, crop), w, rot=rot)
    return PC[k]

def faces(c, t, t0):
    for i, rid in enumerate(OFFICERS):
        col, row = i % 7, i // 7; x = 150 + col * 270; y = 300 + row * 470
        L.drop(c, pcard(rid, None, 230, (-2, 1.5, -1, 2, -1.5, 1, -2)[col]), x, y, t, t0 + 0.08 * i)


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
    k, (ln, (kind, a)), t0, t1 = shot_at(t)
    if kind == "kb":
        src = tone(a["rid"], a["crop"], a["rot"]); c = L.vignette(L.kenburns(src, t, t0, t1, a["z"][0], a["z"][1], a["c0"], a["c1"]))
    elif kind == "coldopen":
        pg = page_img("note"); bg = view(pg, 900, 1100, 1.15).filter(ImageFilter.GaussianBlur(1.5))
        c = Image.alpha_composite(bg, Image.new("RGBA", (W, H), (0, 0, 0, 150)))
        u = clamp01((t - t0) / max(t1 - t0, 1)); card = L.print_card(page_img("note"), int(520 + 40 * u), rot=3)
        c.alpha_composite(card, (int(W * 0.68 - card.width / 2), int(H / 2 - card.height / 2)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip(1.25 - np.linspace(0, 1, W) * 1.9, 0, 1)[None, :] * 235
        lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
        L.typewriter(c, "APRIL 25, 1848", t, t0 + 0.05, 110, H / 2 - 60, size=120, cps=12, anchor="lm", cursor=False)
        L.text(c, "Victory Point  ·  King William Island", 115, H / 2 + 60, 50, BONE, SER, anchor="lm", alpha=ease((t - t0 - 1.2) / 0.4))
        L.rule(c, 115, 640, H / 2 + 110, t, t0 + 1.4)
    elif kind == "card":
        c = ambient(k); big = a["big"]
        L.typewriter(c, big, t, t0 + 0.05, W / 2, H / 2 - 50, size=200 if len(big) < 10 else 150, cps=12, anchor="mm", cursor=False)
        t2 = t0 + 0.05 + len(big) / 12
        L.text(c, a["sub"], W / 2, H / 2 + 120, 58, STEEL, SER, alpha=ease((t - t2) / 0.4)); L.rule(c, W / 2 - 280, W / 2 + 280, H / 2 + 185, t, t2 + 0.15)
    elif kind == "doc":
        key = a["key"]; src = page_img(key); fx0, fy0, fx1, fy1 = a["focus"]; u = ease((t - t0) / max(t1 - t0, 0.5))
        s_fit = min(W * 0.8 / (fx1 - fx0), H * 0.62 / (fy1 - fy0)); s = s_fit * (a["z"][0] + (a["z"][1] - a["z"][0]) * u)
        cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2; act = None
        for mk in a["marks"]:
            tm = mark_time(key, mk, ln)
            if t >= tm: act = (PH[key][mk[0]], tm)
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
        c = ambient(k)
        for rid, crop, w, x, y, rot, d, label in a["items"]:
            L.drop(c, pcard(rid, crop, w, rot), x, y, t, t0 + d)
            if label: L.typewriter(c, label, t, t0 + d + 0.35, x, y + pcard(rid, crop, w, rot).height / 2 + 30, size=32, cps=30, anchor="mm", cursor=False)
    elif kind == "faces":
        c = ambient(k); faces(c, t, t0)
    elif kind == "letter":
        c = ambient(k); paper = (226, 220, 204)
        ImageDraw.Draw(c).rectangle((W / 2 - 520, 110, W / 2 + 520, H - 110), fill=paper)
        rows = ["SACRED", "TO THE MEMORY OF", "JOHN TORRINGTON", "WHO DEPARTED THIS LIFE", "JANUARY 1ST, AD 1846", "ON BOARD OF", "H.M. SHIP TERROR", "AGED 20 YEARS"]
        for i, s in enumerate(rows):
            L.typewriter(c, s, t, t0 + 0.1 + i * 0.25, W / 2, 190 + i * 95, size=46, fill=(40, 36, 30), cps=40, anchor="mm", cursor=False)
        L.typewriter(c, "Headboard inscription, Beechey Island (1846)  ·  as recorded by Royal Museums Greenwich", t, t0 + 0.3, W / 2, H - 55, size=26, fill=STEEL, cps=50, anchor="mm", cursor=False)
    elif kind == "title":
        c = ambient(k); u = ease((t - t0) / 0.6)
        L.text(c, "the", W / 2, H / 2 - 170, 80, STEEL, SER, alpha=u); L.text(c, "LAST HOURS", W / 2, H / 2 - 10, 240, BONE, COND, alpha=u)
        L.rule(c, W / 2 - 320, W / 2 + 320, H / 2 + 135, t, t0 + 0.4, width=9)
        L.typewriter(c, "FILE 02  ·  FRANKLIN  ·  1845–1848", t, t0 + 0.9, W / 2, H / 2 + 230, size=40, fill=STEEL, cps=30, anchor="mm", cursor=False)
    elif kind == "cta":
        c = L.vignette(L.kenburns(tone("D4"), t, t0, t1, 1.1, 1.18)); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 165)))
        pass  # spoken ask cut 23 Oct (LESSONS 21): L.typewriter(c, "EVERYTHING HERE IS FROM
        pass  # spoken ask cut 23 Oct (LESSONS 21): L.typewriter(c, "LIKE  ·  SUBSCRIBE", t,
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 150, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 260, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 350, t, t0, width=7)
        L.typewriter(c, "NEXT FILE:  D.B. COOPER", t, T[171], W / 2, 450, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
        if t > VO_END:
            d = ImageDraw.Draw(c); d.rectangle((1050, 560, 1770, 965), outline=STEEL + (255,), width=3); d.ellipse((330, 600, 650, 920), outline=STEEL + (255,), width=3)
    else:
        c = ambient(k)
    draw_ov(c, k, t, t1)
    return c

# ------------------------------------------------------------------ audio
def load(p, sr=48000):
    a, s = sf.read(p, dtype="float32", always_2d=True); a = a.mean(1)
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    return a
def audio():
    sr = 48000; N = int(DUR * sr); vo = load(ROOT + "vo/franklin_vo_chatterbox.wav"); y = np.zeros(N, np.float32)
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
    music("Thunder Dreams.mp3", tl(12), tl(42), -24); music("Man Down.mp3", tl(42), tl(67), -25); music("Thunder Dreams.mp3", tl(70), tl(105), -25)
    music("Rising Tide.mp3", tl(105), tl(139), -26); music("Man Down.mp3", tl(139), tl(161), -25); music("Thunder Dreams.mp3", tl(161), DUR, -22)
    loop("wind_cold_interior", 0, tl(12), -22); loop("wind_deep_cinematic_hum", tl(42), tl(67), -30); loop("wind_ambience", tl(71), tl(92), -30)
    loop("roomtone_dark_cinematic", tl(91), tl(105), -30); loop("wind_scary", tl(113), tl(132), -32)
    HITS = [("hit_deep_heartbeat_impact", -17), ("hit_short_bass", -19), ("hit_glass_suspense", -21), ("hit_cinematic_deep_impact", -20)]
    SWIPES = [("whoosh_fast_transition", -22), ("paper_slide", -20), ("whoosh_ghostly", -24)]; MK = [0]
    for i, (ln, (kind, a)) in enumerate(SHOTS):
        t0 = T[ln] - 0.12
        if kind == "card":
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "doc": sfx("paper_slide", t0, -18); sfx("typewriter_soft_click", t0 + 0.2, -24)
        elif kind == "prints":
            for it in a["items"]: sfx("paper_slide", t0 + it[6], -17); sfx("camera_vintage_shutter", t0 + it[6] + 0.15, -24)
        elif kind == "faces":
            for j in range(0, 14, 3): sfx("camera_old_shutter_click", t0 + 0.08 * j, -24)
        elif kind == "nmap": sfx("paper_page_turn", t0, -22)
        elif kind == "title": sfx("hit_cinematic_deep_impact", t0, -12); sfx("typewriter_return_bell", t0 + 2.0, -20)
        elif kind == "kb": sfx("whoosh_fast_transition", t0 - 0.1, -32)
        for mk in a.get("marks", ()):
            tm = mark_time(a["key"], mk, ln); MK[0] += 1; h = HITS[MK[0] % len(HITS)]; w = SWIPES[MK[0] % len(SWIPES)]
            sfx(h[0], tm, h[1], maxlen=1.8); sfx(w[0], tm + 0.1, w[1], maxlen=0.9)
        if kind == "nmap":
            for op in a["ops"]:
                if op[0] == "pin" and op[4] >= 0: sfx("camera_classic_click", t0 + op[4], -22)
                if op[0] == "circle" and op[5] >= 0: sfx("camera_lens_autofocus", t0 + op[5], -26, maxlen=1.0)
    for ln, off, kind, a in OV:
        if kind == "stamp": sfx("hit_horror_drum", T[ln] + off, -14)
        if kind in ("typecenter", "typecenter_red", "list", "list_side"): sfx("typewriter_typing_old", T[ln] + off, -26)
    sfx("hit_cinematic_deep_impact", 0.0, -14)
    for j in range(len("APRIL 25, 1848")): sfx("typewriter_single_hit", 0.05 + j / 12, -20)
    EV = [(1, 0.3, "metal_tool_drop", -26), (13, 0.2, "ship_hull_creak", -22), (14, 0.3, "waves_windy_sea_loop", -26), (23, 0.3, "waves_with_birds", -28),
          (25, 0.3, "paper_writing_pencil", -24), (30, 0.3, "waves_rough_sea_loop", -28), (35, 0.2, "heartbeat_single", -18), (36, 0.2, "heartbeat_single", -20),
          (37, 0.2, "heartbeat_single", -22), (44, 0.3, "ship_hull_creak", -18), (45, 0.4, "wind_scary", -24), (46, 0.6, "ship_hull_creak", -22),
          (50, 0.3, "footsteps_stones_loop", -26), (55, 0.4, "paper_signing", -20), (57, 0.4, "clock_bells_hour", -22), (59, 0.3, "wind_cold_interior", -24),
          (62, 0.2, "heartbeat_slow", -22), (72, 0.3, "footsteps_stones_loop", -24), (74, 0.4, "wind_ambience", -26), (83, 0.6, "paper_writing_pencil", -22),
          (87, 0.2, "footsteps_stones_loop", -24), (89, 0.3, "metal_tool_drop", -24), (91, 0.0, "wind_deep_cinematic_hum", -26), (94, 0.4, "paper_big_page_turn", -20),
          (95, 0.3, "newspaper_drop", -18), (103, 0.4, "newspaper_drop", -20), (105, 0.4, "ship_engine_loop", -28), (106, 0.3, "footsteps_stones_loop", -26),
          (108, 0.6, "metal_tool_falling", -24), (113, 0.3, "wind_scary", -24), (119, 0.3, "waves_rocky_shore", -26), (122, 0.2, "heartbeat_horror_drum", -18),
          (123, 0.3, "metal_hammer_hit", -24), (126, 0.4, "wind_cold_interior", -26), (132, 0.0, "heartbeat_single", -16), (140, 0.4, "radio_static_fx", -26),
          (142, 0.2, "sweep_horror_long", -22), (146, 0.4, "sweep_terror_darkness", -24), (149, 0.6, "door_key_in_lock", -18), (150, 0.4, "heartbeat_slow", -22),
          (159, 0.3, "typewriter_return_bell", -20), (165, 0.6, "clock_wall_tick", -22), (168, 0.4, "door_key_in_lock", -20), (170, 0.2, "typewriter_return_bell", -18)]
    for ln, off, name, db in EV: sfx(name, T[ln] + off, db, maxlen=4.0)
    y += bed; pk = np.max(np.abs(y)); y = y / max(pk, 1e-6) * 0.9
    sf.write(B + "mix_raw.wav", y, sr, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(B + "mix_raw.wav", B + "mix.wav", target=-14, tp=-1); print("audio", AM.measure(B + "mix.wav"))

def seg(i, n):
    a, b = NF * i // n, NF * (i + 1) // n
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", B + f"seg_{i}.mp4"], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(frame(f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("seg done", i, flush=True)
def final(n, name="TheLastHours_02_Franklin.mp4"):
    with open(B + "segs.txt", "w") as f:
        for i in range(n): f.write(f"file 'seg_{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "qa":
        prep()
        ts = [float(x) for x in sys.argv[2:]] or [T[s[0]] + 1.2 for s in SHOTS]
        tiles = [frame(t).convert("RGB").resize((384, 216)) for t in ts]; cols = 5
        S = Image.new("RGB", (cols * 394, ((len(tiles) + cols - 1) // cols) * 236), (20, 20, 20))
        for i, (im, tt) in enumerate(zip(tiles, ts)):
            S.paste(im, ((i % cols) * 394, (i // cols) * 236)); ImageDraw.Draw(S).text(((i % cols) * 394 + 6, (i // cols) * 236 + 218), f"{tt:.1f}", fill=(255, 220, 90))
        out = B + ("qa.png" if len(sys.argv) > 2 else "qa_all.png"); S.save(out); print(out)
    elif m == "chapters":
        CH = [(0, "April 1848: a note in a tin"), (13, "May 1845: two ships leave England"), (32, "Beechey Island: three graves, no note"),
              (42, "September 1846: locked in the ice"), (48, "May 1847: “All well”"), (57, "Franklin dies"), (71, "April 1848: they walk"),
              (91, "Silence, and what the Inuit told Rae"), (105, "1859: the note is found"), (113, "The skeleton and the boat"),
              (132, "What killed them?"), (139, "The wrecks, and the closed door"), (152, "DNA: six names back"), (161, "What the records can't tell us")]
        for i, (ln, name) in enumerate(CH):
            t = 0 if i == 0 else T[ln] - 0.12; print(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    elif m == "times":
        for i in range(len(LINES)): print(f"{i:3d} {T[i]:7.2f} {LINES[i][:70]}")
        print("VO_END", VO_END, "DUR", DUR)
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
