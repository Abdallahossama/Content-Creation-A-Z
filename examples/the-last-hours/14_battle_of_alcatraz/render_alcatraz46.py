"""The Last Hours #14: the Battle of Alcatraz, Thursday 2 - Saturday 4 May 1946 (the gun cage, cells 403/402, key 107, the siege,
the grenades on the roof, the trial). Case File style, colour grade, 1920x1080, burned-in captions, film finish. Built on render_goering.py.
Real images only: NPS Golden Gate NRA museum photos and the 1946 BOP report, NARA warden's notebook cards, HABS (Library of Congress),
the US Attorney's brief, 1946 newspapers, Universal newsreel outtakes (safe seconds only), Pexels textures labelled ILLUSTRATIVE.
Never shown: the dead, the morgue, the wounded, any woman. Owner rules: research/research.md (do-not-say), assets.md section H.
  uv run --no-project --with pillow --with numpy --with soundfile python render_alcatraz46.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
import vidclip as VC
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
sys.path.insert(0, "D:/why habibi/_newchannel/_cta"); import brand_patch as BP; import brand_anim as BA     # The File Keeper (docs/09)
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 5.0                                   # the File Keeper end card runs under the sign-off
NEXT = os.environ.get("LH_NEXT", "")                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/alcatraz46_vo_chatterbox.wav")
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
def isdoc(rid): return rid[0] == "A" and rid not in ("A7", "A8", "A9", "A10")      # A7-A10 are museum objects: graded like photos
def grade_im(im):
    a = np.asarray(im.convert("RGB"), np.float32) / 255; a = np.clip((a - 0.5) * 1.10 + 0.5, 0, 1)
    g = a.mean(2, keepdims=True); a = np.clip(g + (a - g) * 1.15, 0, 1)
    a = a + (1 - g) * 0.10 * np.array([-0.6, 0.15, 0.35], np.float32) + g * 0.06 * np.array([0.5, 0.15, -0.4], np.float32)   # teal shadows, warm highlights
    return Image.fromarray((np.clip(a * 0.94, 0, 1) * 255).astype(np.uint8))
def colour(path, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(tuple(int(v * s) for v, s in zip(crop, (im.width, im.height, im.width, im.height))))
    return grade_im(im)
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

# (no Natural-Earth map in this file: the bay is shown on the real USGS sheet and the NPS plan)

# ------------------------------------------------------------------ shot constructors
CROP = {"B1": (0.07, 0.04, 0.93, 0.96), "B11": (0.02, 0.03, 0.98, 0.93), "C14": (0.04, 0.03, 0.96, 0.95), "C15": (0.04, 0.03, 0.96, 0.95),
        "C16": (0.01, 0.02, 0.99, 0.92), "C17": (0.02, 0.02, 0.98, 0.92), "C18": (0.04, 0.03, 0.96, 0.94), "C19": (0.05, 0.03, 0.95, 0.94),
        "C21": (0.04, 0.03, 0.96, 0.93), "C11": (0.02, 0.02, 0.98, 0.94), "C12": (0.06, 0.03, 0.94, 0.93),
        "C3": (0.02, 0.03, 0.94, 0.97), "C4": (0.03, 0.06, 0.95, 0.97), "C5": (0.03, 0.06, 0.95, 0.97), "C6": (0.02, 0.03, 0.94, 0.97),
        "C7": (0.03, 0.06, 0.95, 0.97), "C8": (0.02, 0.03, 0.94, 0.97), "C9": (0.03, 0.04, 0.94, 0.97), "C10": (0.03, 0.03, 0.94, 0.97)}   # HABS: black edge + catalogue number                                # NPS prints: trim the white border + caption strip (cover-fit picks the band)
NPS = "NPS, GOLDEN GATE NRA"; HABS = "HABS, LIBRARY OF CONGRESS"; NARA = "NATIONAL ARCHIVES"
TB = {"B1": f"BERNARD COY, ALCATRAZ No. 415  ·  {NPS}", "B2": f"JOSEPH CRETZER  ·  {NPS}",
      "B3": f"WARDEN'S NOTEBOOK: BERNARD COY, AZ 415  ·  {NARA}", "B4": f"WARDEN'S NOTEBOOK: JOSEPH CRETZER, AZ 548  ·  {NARA}",
      "B5": f"WARDEN'S NOTEBOOK: MARVIN HUBBARD, AZ 645  ·  {NARA}", "B6": f"WARDEN'S NOTEBOOK: SAM SHOCKLEY, AZ 462  ·  {NARA}",
      "B7": f"WARDEN'S NOTEBOOK: MIRAN THOMPSON, AZ 729  ·  {NARA}", "B8": f"WARDEN'S NOTEBOOK: CLARENCE CARNES, AZ 714  ·  {NARA}",
      "B9": f"CARNES, SHOCKLEY AND THOMPSON ON THE WAY TO COURT  ·  {NPS}", "B10": f"WARDEN JOHNSTON AND DIRECTOR BENNETT MEET THE PRESS, MAY 1946  ·  {NPS}",
      "B11": f"ALCATRAZ OFFICERS, WARDEN JOHNSTON AT CENTRE  ·  {NPS}", "B12": f"OFFICERS ON THE BAY PATROL, 1946  ·  {NPS}",
      "B13": f"CLARENCE CARNES BACK IN THE CELL HOUSE, 1980  ·  {NPS}",
      "C1": f"SMOKE FROM THE CELL HOUSE, MAY 1946  ·  {NPS}", "C2": f"THE GUN-GALLERY BARS COY PRIED APART  ·  {NPS}",
      "C3": f"D BLOCK, THE ISOLATION CELLS  ·  {HABS}", "C4": f"D BLOCK DOOR OPENERS  ·  {HABS}",
      "C5": f"“BROADWAY”, BETWEEN C AND B BLOCKS  ·  {HABS}", "C6": f"C BLOCK CELLS  ·  {HABS}", "C7": f"C BLOCK: THE LEVER BOX  ·  {HABS}",
      "C8": f"THE PRISONERS' DINING ROOM  ·  {HABS}", "C9": f"THE RECREATION YARD  ·  {HABS}", "C10": f"THE GUARD TOWER OVER THE YARD  ·  {HABS}",
      "C11": f"THE RECREATION YARD FROM THE AIR  ·  {NPS}", "C12": f"A TOWER GUARD'S RIFLES, c. 1940  ·  {NPS}",
      "C14": f"ALCATRAZ FROM THE AIR, 1950  ·  {NPS}", "C15": f"ALCATRAZ FROM THE AIR, 1950  ·  {NPS}", "C16": f"THE EAST SIDE AND THE DOCK  ·  {NPS}",
      "C17": f"THE CELL HOUSE, WEST SIDE  ·  {NPS}", "C18": f"LOCKING THE CELL DOORS AT THE LEVER BOX, 1960  ·  {NPS}",
      "C19": f"“BROADWAY”, 1963  ·  {NPS}", "C20": f"B AND C BLOCKS FROM THE GUARD STATION  ·  {HABS}",
      "C21": f"THE UTILITY CORRIDOR BEHIND THE CELLS, 1962  ·  {NPS}", "C22": "D BLOCK, NEWLY BUILT, 1911  ·  PUBLIC DOMAIN",
      "D1a": "ALCATRAZ FROM THE BAY, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES", "D1b": "BOATS AROUND THE ISLAND, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES",
      "D1c": "THE CELL HOUSE WALL, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES", "D1d": "ALCATRAZ, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES",
      "D2a": "ALCATRAZ FROM THE WATER, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES", "D2b": "THE CELL HOUSE, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES",
      "D2c": "THE LIGHTHOUSE AND THE FLAG, MAY 1946  ·  UNIVERSAL NEWSREEL / NATIONAL ARCHIVES",
      "E1": "PLAN OF THE CELL HOUSE, 1949  ·  NPS", "E2": "D BLOCK MODERNIZATION PLAN, 1940  ·  NATIONAL ARCHIVES",
      "E3": "THE DOCK AND POWER-HOUSE TOWERS, PLAN  ·  NATIONAL ARCHIVES", "E4": "ALCATRAZ ISLAND  ·  NPS MAP",
      "E5": "SAN FRANCISCO NORTH, 1950  ·  USGS", "E7": "SAN FRANCISCO BAY  ·  USGS"}
ILL = "ILLUSTRATIVE  ·  PEXELS"
for _r in ("D3", "D4", "D5", "D6", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15"): TB[_r] = ILL
TB["F5"] = "OLD KEYS (NOT KEY 107)  ·  ILLUSTRATIVE, PEXELS"; TB["F9"] = "A SMOKE GRENADE  ·  ILLUSTRATIVE, PEXELS"
TB["F15"] = "SPENT CARTRIDGES  ·  ILLUSTRATIVE, PEXELS"; TB["F8"] = "A BULLET-PITTED WALL (NOT ALCATRAZ)  ·  ILLUSTRATIVE, PEXELS"
def DT(rid):
    n = re.match(r"A(\d+)", rid).group(1)
    return {"1": "“THE ALCATRAZ REVOLT”, U.S. BUREAU OF PRISONS, JULY 1946  ·  NPS", "2": "“A TRIBUTE TO WILLIAM A. MILLER AND HAROLD P. STITES”, 1946  ·  NPS",
            "3": "“THE ALCATRAZ REVOLT”, BUREAU OF PRISONS REPORT, 1946  ·  NPS", "4": "THE ISLAND, BUREAU OF PRISONS REPORT, 1946  ·  NPS",
            "5": "“DETAIL AT GUN GALLERY”, BUREAU OF PRISONS REPORT, 1946  ·  NPS", "6": "UNITED PRESS TO WARDEN JOHNSTON, 2 MAY 1946  ·  NPS",
            "7": "THE BAR SPREADER, 1946  ·  NPS MUSEUM COLLECTION", "8": "BULLETS RECOVERED AFTER THE BATTLE  ·  NPS MUSEUM COLLECTION",
            "9": "AN ALCATRAZ THOMPSON GUN, MODEL 1928  ·  NPS MUSEUM COLLECTION", "10": "CELL-LOCKING INSTRUCTIONS, c. 1934  ·  NPS MUSEUM COLLECTION",
            "11": "BRIEF FOR THE UNITED STATES, SHOCKLEY v. UNITED STATES, 1947  ·  PUBLIC.RESOURCE.ORG", "12": "MONROE MORNING WORLD, SUN 5 MAY 1946",
            "13": "NEW CASTLE NEWS, FRI 3 MAY 1946", "14": "EAST LIVERPOOL REVIEW, FRI 3 MAY 1946", "15": "CIRCLEVILLE HERALD, SAT 4 MAY 1946",
            "16": "DIXON EVENING TELEGRAPH, SAT 4 MAY 1946", "17": "GETTYSBURG TIMES, FRI 3 MAY 1946"}.get(n, "THE RECORD, 1946")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {"D1a": (0.0, 0.04, 1.0, 0.8), "D1b": (0.0, 0.04, 1.0, 0.8), "D1c": (0.0, 0.04, 1.0, 0.8), "D1d": (0.0, 0.04, 1.0, 0.8),   # newsreel: no burnt-in timecode
         "D2a": (0.07, 0.07, 0.93, 0.78), "D2b": (0.07, 0.07, 0.93, 0.78), "D2c": (0.07, 0.07, 0.93, 0.78)}   # D2a cut to 0-10.4 s (onlookers incl. a woman at ~13 s: never shown)
LIFT = {"D1a": 1.5, "D1b": 1.6, "D1c": 1.4, "D1d": 1.5}                 # washed-out 1946 aerials: deepen the midtones
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C10", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

SHOTS = [
 # COLD OPEN
 (0, KB("C1", z=(1.05, 1.15), c0=(0.55, 0.45))),                                  # frame 1: smoke bursting from the cell house, May 1946
 ((0, "ask"), KB("F5", z=(1.06, 1.18), c0=(0.5, 0.42))),
 ((0, "five|die"), KBP("A12", crop=(0.0, 0.0, 1.0, 0.2), h=430)),
 ((0, "never"), KB("C2", z=(1.06, 1.18), c0=(0.62, 0.48))),
 (1, TCARD("2:00 PM", "Thursday, 2 May 1946  ·  Alcatraz", "C14")),
 (2, VID("D1a", at=19.0)),
 ((2, "prisoners"), KB("C5", z=(1.03, 1.13))),
 (3, KB("C2", z=(1.1, 1.22), c0=(0.62, 0.48))),
 ((3, "nine|held"), KB("C6", z=(1.04, 1.14))),
 ((3, "marines|friday"), VID("D1c", at=4.0)),
 (4, KBP("A5", h=900)),
 ((4, "key"), KB("F5", z=(1.1, 1.2), c0=(0.5, 0.42))),
 ((4, "happened|six"), KB("C17", z=(1.03, 1.12))),
 # THE SIX
 (5, VID("D2b", at=6.0)),
 ((5, "nobody"), KB("C14", z=(1.04, 1.14), dim=0.2)),
 (6, KBP("B1", h=760)),
 ((6, "view|gallery"), KB("C17", z=(1.05, 1.15))),
 (7, KB("B3", z=(1.12, 1.3), c0=(0.72, 0.2))),
 (8, KBP("B2", h=760)),
 ((8, "shockley"), KB("B6", z=(1.12, 1.3), c0=(0.72, 0.2))),
 ((8, "hostage|took"), KB("B4", z=(1.12, 1.3), c0=(0.72, 0.2))),
 (9, KB("B5", z=(1.12, 1.3), c0=(0.72, 0.2))),
 ((9, "miran|thompson"), KB("B7", z=(1.12, 1.3), c0=(0.72, 0.2))),
 ((9, "clarence"), KB("B8", z=(1.12, 1.3), c0=(0.72, 0.2))),
 # THE GUN CAGE
 (10, KB("B7", z=(1.3, 1.45), c0=(0.74, 0.18), dim=0.15)),
 (11, KB("C8", z=(1.03, 1.13))),
 (12, KB("C19", z=(1.04, 1.14), c0=(0.5, 0.6))),
 (13, KB("E1", z=(1.15, 1.35), c0=(0.3, 0.5))),
 ((13, "burch"), KBP("A5", h=900)),
 ((13, "armored|doors"), KB("C20", z=(1.03, 1.12))),
 (14, KB("C5", z=(1.08, 1.18), dim=0.2)),
 (15, KB("C2", z=(1.04, 1.16), c0=(0.62, 0.48))),
 ((15, "stolen|made"), KB("A7", z=(1.04, 1.14))),
 ((15, "pushed"), COUNTER([((15, "five|5"), "5 IN"), ((15, "seven|7"), "7 IN")], "THE GAP BETWEEN TWO GUN-GALLERY BARS", "C2", size=330)),
 (16, KB("C12", z=(1.04, 1.14))),
 ((16, "only|two"), KB("C2", z=(1.12, 1.24), c0=(0.62, 0.48), dim=0.25)),
 (17, KB("C3", z=(1.03, 1.13))),
 ((17, "kretzer|cretzer|out"), KB("C4", z=(1.04, 1.14))),
 # KEY 107
 (18, TCARD("2:15 PM", "A kitchen supervisor walks in", "C8")),
 ((18, "coy|up"), KB("C17", z=(1.1, 1.2), c0=(0.45, 0.5))),
 (19, KB("C6", z=(1.06, 1.16))),
 ((19, "four|403"), DOC("A11", [("No. 403", (19, "four|403"))])),
 (20, KB("C9", z=(1.03, 1.13))),
 ((20, "number|key"), COUNTER([((20, "107|seven"), "107")], "THE KEY TO THE YARD DOOR", "C9", size=420)),
 (21, DOC("A11", [("Key No. 107", (21, "which|key")), ("told him, 107", (21, "miller|told")), ("for the 107 key", (22, "hidden|key"))])),
 ((22, "convicts|never"), KB("F5", z=(1.04, 1.16), c0=(0.5, 0.42))),
 (23, KB("C10", z=(1.04, 1.14))),
 # THE TWO CELLS
 (24, KB("C6", z=(1.1, 1.2), dim=0.25)),
 (25, KBP("B2", h=760)),
 (26, KB("F15", z=(1.04, 1.14))),
 ((26, "miller|william"), KBP("A2", h=900)),
 (27, TCARD("“ON THIS DATE…”", "William Miller's sworn statement, dictated by telephone", "C6")),
 # SIEGE NIGHT
 (28, TCARD("3:23 PM", "“Serious trouble.”", "C16")),
 (29, KB("A9", z=(1.04, 1.14))),
 ((29, "didn|rifle"), KB("C12", z=(1.08, 1.18))),
 (30, VID("D1b", at=1.0)),
 (31, KB("B12", z=(1.04, 1.14))),
 (32, KB("E7", z=(1.3, 1.6), c0=(0.6, 0.6), c1=(0.62, 0.62))),
 (33, VID("D2a", at=2.0)),
 ((33, "stairs|steep"), KB("C9", z=(1.06, 1.16))),
 (34, KBP("A2", h=900)),
 ((34, "gallery|went"), KB("C20", z=(1.08, 1.18), dim=0.2)),
 (35, VID("D5", at=4.0)),
 ((35, "searchlights|lit"), KB("F11", z=(1.03, 1.13))),
 (36, VID("D6", at=2.0, dim=0.2)),
 (37, KB("C16", z=(1.04, 1.14), dim=0.3)),
 (38, KB("C6", z=(1.12, 1.24), dim=0.35)),
 (39, KB("C21", z=(1.04, 1.14), c0=(0.5, 0.35))),
 ((39, "other|three"), KB("C3", z=(1.06, 1.16), dim=0.2)),
 # GRENADES ON THE ROOF
 (40, TCARD("FRI 3 MAY", "Officer William Miller dies", "C17")),
 (41, KBP("A14", crop=(0.0, 0.025, 1.0, 0.144), h=260)),
 ((41, "marine|firing"), KB("C17", z=(1.04, 1.14), dim=0.15)),
 (42, ("midask", dict(bg="C17", ln=42))),                          # the spoken mid-video ask (cliffhanger)
 (43, VID("D1c", at=12.0)),
 ((43, "drilled|lowered"), KBP("A15", crop=(0.738, 0.235, 0.87, 0.40), h=880)),
 ((43, "150|hundred"), COUNTER([((43, "hundred|150"), "~150")], "GRENADES INTO THE CELL HOUSE  ·  THE MARINE MAJOR'S COUNT", "C1", size=360)),
 (44, KB("C1", z=(1.1, 1.24), c0=(0.55, 0.45))),
 ((44, "shoulder|sore"), KB("F9", z=(1.04, 1.14), c0=(0.5, 0.42))),
 (45, VID("D1c", at=24.0)),
 (46, DOC("A6", [("31", (46, "thousands|watched")), ("COY STARTED", (46, "reporters"))])),
 ((46, "aquatic|pier"), KB("F6", z=(1.03, 1.13))),
 (47, VID("D1d", at=2.0)),
 (48, KB("B11", z=(1.06, 1.18), c0=(0.5, 0.45))),
 (49, KB("C3", z=(1.1, 1.2), dim=0.55)),
 # THE CORRIDOR
 (50, KB("C21", z=(1.08, 1.2), c0=(0.5, 0.35))),
 (51, KBP("A12", crop=(0.0, 0.0, 1.0, 0.2), h=430)),
 (52, TCARD("12:10 PM", "“No prisoner escaped.”", "C14")),
 (53, KB("B10", z=(1.04, 1.14))),
 ((53, "cells|shouted"), KB("C5", z=(1.06, 1.16), dim=0.2)),
 (54, KB("C2", z=(1.04, 1.12), c0=(0.62, 0.48), dim=0.4)),
 # THE TRIAL
 (55, KBP("B9", h=880)),
 (56, DOC("A11", [("Shockley", (56, "trial|month"))], zoom=1.1)),
 (57, KB("B8", z=(1.3, 1.45), c0=(0.74, 0.18))),
 (58, TCARD("3 DEC 1948", "Shockley and Thompson  ·  San Quentin", "B9")),
 (59, KB("A8", z=(1.04, 1.14))),
 (60, KBP("A2", h=900)),
 # CARNES AND 1962
 (61, KB("B13", z=(1.04, 1.14))),
 (62, TCARD("11 JUN 1962", "Three men  ·  a utility corridor  ·  the roof", "C21")),
 ((62, "roof|over"), KB("C15", z=(1.04, 1.14))),
 (63, KB("C14", z=(1.06, 1.16))),
 # WHAT THE RECORD SHOWS + ASKS
 (64, KB("C5", z=(1.04, 1.12), dim=0.3)),
 (65, COUNTER([((65, "six"), "6 MEN"), ((65, "two|guns"), "2 GUNS"), ((65, "nine"), "9 OFFICERS"), ((65, "five|dead"), "5 DEAD"), ((65, "one|key"), "1 KEY")],
              "THE BATTLE OF ALCATRAZ  ·  2-4 MAY 1946", "C1", size=300)),
 (66, KB("F5", z=(1.06, 1.16), c0=(0.5, 0.42))),
 ((67, -0.7), ("end", {})),                                     # the File Keeper end card under the sign-off
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "hookleft", ("6 ARMED CONVICTS.", "1 HIDDEN KEY.")),                    # from frame 1 (LEAD = 0.8 s)
 (0, "never", "under", "THEY NEVER GOT THE KEY  ·  HOW?"),
 (1, 0.0, "badge", "THU 2 MAY 1946"),
 (2, 0.3, "under", "16 YEARS BEFORE THE 1962 ESCAPE"),
 (3, "two|guns", "typecenter", "2 GUNS  ·  9 HOSTAGES"),
 (4, 0.2, "under", "THE GUN CAGE  ·  KEY 107  ·  ALL SIX MEN"),
 (5, 0.0, "brand", None),                                          # the 2 s channel stamp, over moving footage, voice keeps going
 (6, 0.3, "nameplate", ("BERNARD COY", "BANK ROBBER  ·  ALCATRAZ No. 415  ·  THE CELL-HOUSE ORDERLY")),
 (7, 0.2, "quote", ("“Do you get a thrill out of" + chr(10) + "criminal activities?”", "THE JUDGE, 1937")),
 (7, "said|hardened", "typecenter", "“NO, I'M JUST HARDENED TO IT.”"),
 (8, 0.3, "nameplate", ("JOSEPH CRETZER", "BANK ROBBER  ·  TRIED TO ESCAPE IN 1941")),
 (8, "shockley", "under", "SAM SHOCKLEY  ·  WITH CRETZER IN THE 1941 ATTEMPT"),
 (9, 0.2, "under", "MARVIN HUBBARD  ·  KIDNAPPER"),
 (9, "miran|thompson", "under", "MIRAN THOMPSON  ·  8 ESCAPES ON HIS RECORD"),
 (9, "clarence", "under", "CLARENCE CARNES  ·  19, THE YOUNGEST"),
 (11, 0.0, "badge", "THU 2 MAY  ·  1:00 PM"),
 (11, "sick", "under", "“SICK ALL OVER”"),
 (12, 0.0, "badge", "THU 2 MAY  ·  1:30 PM"),
 (13, "burch", "under", "OFFICER BERT BURCH  ·  NO SAFE PHOTO"),
 (14, 0.0, "badge", "THU 2 MAY  ·  ABOUT 2:00 PM"),
 (15, "tool|stolen", "under", "THE BAR SPREADER: A BOLT, A NUT AND A PIPE"),
 (16, "only|two", "typecenter_red", "THE ONLY 2 GUNS THEY WOULD EVER HAVE"),
 (17, "kretzer|cretzer|out", "under", "JOSEPH CRETZER, FREED FROM D BLOCK"),
 (19, 0.0, "typecenter", "9 OFFICERS  ·  2 CELLS"),
 (21, 0.2, "under", "OFFICER WILLIAM MILLER  ·  NO SAFE PHOTO"),
 (22, "never|found", "stamp", ("NEVER FOUND", 1240, 400)),
 (23, 0.0, "typecenter_red", "THE SIREN"),
 (24, 0.0, "badge", "THU 2 MAY  ·  ABOUT 3:00 PM"),
 (24, 0.3, "under", "OUTSIDE CELL 403"),
 (25, 0.4, "quote", ("“You mean they will get killed," + chr(10) + "don't you?”", "JOSEPH CRETZER, AS THE COURT RECORDED IT")),
 (26, "miller|william", "under", "WILLIAM MILLER DIED THE NEXT MORNING"),
 (29, "didn", "stamp", ("A RIFLE", 1240, 400)),
 (30, 0.0, "badge", "THU 2 MAY  ·  3:30 PM"),
 (31, 0.0, "badge", "THU 2 MAY  ·  4:15 PM"),
 (31, "cornered", "quote", ("“Cornered, but not subdued.”", "WARDEN JAMES A. JOHNSTON, TO THE S.F. POLICE CHIEF")),
 (32, 0.2, "under", "U.S. MARINES FROM TREASURE ISLAND"),
 (33, 0.0, "badge", "THU 2 MAY  ·  6:30 PM"),
 (34, 0.2, "under", "OFFICER HAROLD STITES  ·  HE STOPPED A 1938 ESCAPE"),
 (35, 0.0, "badge", "THU 2 MAY  ·  7:01 PM"),
 (36, 0.0, "badge", "THU 2 MAY  ·  9:00 PM"),
 (36, 0.2, "typecenter", "7 HOURS IN"),
 (38, 0.2, "under", "OFFICER ROBERT BAKER  ·  HE PLAYED DEAD FOR HOURS"),
 (39, 0.2, "under", "COY, CRETZER, HUBBARD: THE CORRIDOR BEHIND C BLOCK"),
 (40, 0.0, "badge", "FRI 3 MAY 1946"),
 (41, 0.2, "under", "UP AND AP, 3 MAY 1946: “MORTARS”  ·  MYTH OR RECORD?"),
 (43, 0.3, "nameplate", ("CHARLES BUCKNER", "U.S. MARINE WARRANT OFFICER  ·  ON THE CELL-HOUSE ROOF")),
 (44, "noon", "badge", "FRI 3 MAY  ·  NOON"),
 (45, 0.2, "under", "SENT ON GENERAL JOSEPH STILWELL'S AUTHORITY"),
 (46, "telescope|ten", "under", "10 CENTS A LOOK, AQUATIC PARK PIER"),
 (48, 0.2, "nameplate", ("JAMES A. JOHNSTON", "WARDEN OF ALCATRAZ  ·  AGE 71")),
 (48, "deal|make", "quote", ("“We'll make a deal when you throw" + chr(10) + "out your guns and ammunition.”", "WARDEN JOHNSTON")),
 (50, 0.0, "badge", "SAT 4 MAY 1946"),
 (51, "dead", "under", "NO PHOTOGRAPHS OF THE DEAD ARE SHOWN"),
 (52, 0.0, "badge", "SAT 4 MAY  ·  12:10 PM"),
 (53, "saltwater|hey", "typecenter", "“HEY, SALTWATER JOHNSTON.”"),
 (54, 0.0, "list", ("2 GUNS", "9 OFFICERS IN 2 CELLS", "1 KEY THEY NEVER HAD", "0 REACHED THE YARD")),
 (54, "yard|reached", "subpop", None),                              # silent ask right after the payoff (LESSONS 37)
 (55, 0.2, "under", "SHOCKLEY AND THOMPSON FIRED NO SHOT"),
 (56, 0.2, "under", "A MONTH OF TRIAL  ·  NEARLY 2,200 PAGES"),
 (57, "spared", "typecenter", "CARNES: SPARED"),
 (58, 0.0, "badge", "FRI 3 DEC 1948"),
 (59, 0.2, "under", "CORONER'S JURY: THE OFFICERS' DEATHS WERE MURDER"),
 (60, 0.2, "under", "NATIONAL LAW ENFORCEMENT OFFICERS MEMORIAL"),
 (61, 0.3, "under", "CLARENCE CARNES, 1980"),
 (62, 0.0, "badge", "MON 11 JUN 1962"),
 (63, 0.2, "under", "“WHAT THE FBI FOUND WHEN 3 MEN VANISHED FROM ALCATRAZ”"),
 (64, 0.0, "typecenter", "WHAT THE RECORD SHOWS"),
 (66, 0.2, "under", "KEY 107: COULD THEY HAVE MADE IT?  TELL ME BELOW"),
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
    lay = Image.new("RGBA", (W, 104), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, 0, W, 104), fill=(0, 0, 0, 190))
    c.alpha_composite(lay, (0, 796)); L.typewriter(c, s, t, t0, W / 2, 848, size=46 if len(s) < 48 else 38, cps=30, anchor="mm", cursor=False)

SLOT = {"hookleft": "center", "lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center"}
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
        if kind == "subpop":                                           # the case tab runs its full length across shot cuts
            if t0 <= t < t0 + BA.PILL_LEN: ov_extra(c, kind, a, t, t0)
            continue
        if kind == "brand":                                            # so does the stamp
            if t0 <= t < t0 + BA.STAMP_LEN: ov_extra(c, kind, a, t, t0)
            continue
        if t < t0 or t >= shot_t1 or t0 < shot_t0 - 0.2: continue
        if NO_BOTTOM and SLOT.get(kind) == "bottom": continue
        if t >= ov_end(j, shot_t1): continue
        if kind == "lower": lower(c, a, t, t0)
        elif kind == "under": under(c, a, t, t0)
        elif kind in ("typecenter", "typecenter_red"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 110, W, H / 2 + 110), fill=(0, 0, 0, 185)); c.alpha_composite(lay)
            if t0 <= 0.05:                                             # frame 1: the hook text is already there (LESSONS 1)
                L.text(c, a, W / 2, H / 2, 96 if len(a) < 26 else 74, RED if kind.endswith("red") else BONE, TYPE)
            else:
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
        lay = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); g = np.clip(np.linspace(0, 1, 420) * 1.6, 0, 1)[:, None] ** 1.2 * 240
        lay.putalpha(Image.fromarray(np.repeat(g, W, 1).astype(np.uint8))); c.alpha_composite(lay, (0, H - 420))
        L.typewriter(c, a[0], t, t0, 90, 772, size=90, fill=BONE, cps=18, anchor="lm", fnt=COND, cursor=False)
        L.rule(c, 92, 92 + len(a[0]) * 41, 824, t, t0 + 0.4, width=6)
        L.typewriter(c, a[1], t, t0 + 0.6, 92, 866, size=30, fill=STEEL, cps=40, anchor="lm", cursor=False)
    elif kind == "brand":                                      # the animated File Keeper stamp (band sweep, mark, letters, file line)
        if t - t0 < BA.STAMP_LEN: c.alpha_composite(BA.stamp_frame(t - t0, BP.LABEL["alcatraz46"]))
    elif kind == "hookleft":                                   # frame-1 hook text in thumbnail blocks, left, off the face
        f = L.font(COND, 132); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i, s in enumerate(a):
            y = H / 2 - 130 + i * 180; w = f.getlength(s)
            d.rectangle((80, y - 82, 80 + w + 56, y + 82), fill=((0, 0, 0, 230) if i == 0 else (255, 204, 0, 255)))
            d.text((108, y), s, font=f, fill=(BONE + (255,)) if i == 0 else (10, 10, 10, 255), anchor="lm")
        c.alpha_composite(lay)
    elif kind == "subpop":                                     # the File Keeper case tab (no ask: the spoken mid ask does that)
        if t - t0 < BA.PILL_LEN: c.alpha_composite(BA.chip_frame(t - t0, BP.LABEL["alcatraz46"]), (0, BP.PILL_Y))

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


# ------------------------------------------------------------------ burned-in captions (word-synced; the current word in yellow)
CAPFIX = {"Khoi": "Coy", "Koi": "Coy", "Kratzer": "Cretzer", "Kratz's": "Cretzer's", "Krezza": "Cretzer", "Mirren": "Miran", "Moran": "Miran", "Thomson": "Thompson", "Burt": "Bert", "Burj": "Burch", "armoured": "armored", (15, "pots"): "parts", (41, "describes"): "described", "Coy's": "Coy's", "Kretzer": "Cretzer", "Kretzer's": "Cretzer's", "Cretser": "Cretzer", "Kanns": "Carnes",
          "Khan's": "Carnes,", "Karns": "Carnes", "Kahns": "Carnes", "Karnes": "Carnes", "Birch": "Burch", "Stights": "Stites", "Steits": "Stites",
          "Stillwell": "Stilwell", "sellhouse": "cellhouse", "Sellhouse": "Cellhouse", "1.30": "1:30", "3.23": "3:23", "4.15": "4:15", "6.30": "6:30",
          "7.01": "7:01", "12.10": "12:10", "2.15": "2:15", (67, "everyone"): "every one", (67, "everyone."): "every one."}  # whisper spellings -> the record's
def capfix(i, w):
    m = re.match(r"^(.*?)([.,?!;:]*)$", w); core, pun = m.group(1), m.group(2)
    if (i, w) in CAPFIX: return CAPFIX[(i, w)]
    if (i, core) in CAPFIX: r = CAPFIX[(i, core)]; return r + pun if r else ""
    if core in CAPFIX: return CAPFIX[core] + pun
    return w
CAP_Y, CAP_F = 996, None
def _caps():
    out = []
    for i in range(len(LINES)):
        ws = [(T[i] + rel, capfix(i, w.strip())) for rel, w in WORDS.get(i, []) if w.strip()]
        ws = [(tm, w) for tm, w in ws if w]; mg = []
        for tm, w in ws:                                                              # "al" + "-Bakr" -> "al-Bakr"
            if mg and (w.startswith("-") or mg[-1][1].endswith("-")): mg[-1] = (mg[-1][0], mg[-1][1].rstrip("-") + "-" + w.lstrip("-"))
            elif mg and len(w) > 1 and w[0] in ".," and w[1].isalnum():                     # "8" + ".30" -> "8:30", "a" + ".m." -> "a.m.", "9" + ",998"
                mg[-1] = (mg[-1][0], re.sub(r"^(\d{1,2})\.(\d\d)", r"\1:\2", mg[-1][1] + w))
            else: mg.append((tm, w))
        ws = mg
        ch = []
        for k, (tm, w) in enumerate(ws):
            ch.append((tm, w)); txt = " ".join(x for _, x in ch)
            if len(ch) >= 6 or len(txt) >= 30 or w[-1] in ".,?!;:" or k == len(ws) - 1:
                out.append(ch); ch = []
    caps = []
    for j, chk in enumerate(out):
        t0 = chk[0][0] - 0.05; t1 = out[j + 1][0][0] - 0.05 if j + 1 < len(out) else VO_END
        caps.append((t0, min(t1, chk[-1][0] + 2.2), chk))
    return caps
CAPS = _caps() if WORDS else []
def draw_caps(c, t):
    global CAP_F
    if NO_BOTTOM or not CAPS or t > VO_END + 0.2: return
    cur = None
    for t0, t1, chk in CAPS:
        if t0 <= t < t1: cur = chk; break
    if not cur: return
    if CAP_F is None: CAP_F = L.font(COND, 62)
    words = [w for _, w in cur]; sp = CAP_F.getlength(" "); ws = [CAP_F.getlength(w) for w in words]
    gaps = [0 if w.endswith("-") else sp for w in words]; tw = sum(ws) + sum(gaps[:-1])
    x = W / 2 - tw / 2; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x - 26, CAP_Y - 44, x + tw + 26, CAP_Y + 42), 14, fill=(0, 0, 0, 120))
    for k, ((tm, w), wl) in enumerate(zip(cur, ws)):
        nxt = cur[k + 1][0] if k + 1 < len(cur) else tm + 0.6
        col = (255, 204, 0) if tm <= t < nxt else (255, 255, 255)                # only the word being spoken
        d.text((x, CAP_Y), w, font=CAP_F, fill=col + (255,), anchor="lm", stroke_width=5, stroke_fill=(0, 0, 0, 255)); x += wl + gaps[k]
    c.alpha_composite(lay)

# ------------------------------------------------------------------ one archive-film finish on every frame (under the text layers)
FILM = os.environ.get("LH_FILM", "1") == "1"
def _film_lut():
    x = np.arange(256) / 255.0; sc = x + 0.22 * (x - 0.5) * (1 - np.abs(2 * x - 1))      # gentle S-curve
    sc = 0.035 + sc * 0.93                                                                # lifted blacks, soft whites (print look)
    r = np.clip(sc + 0.035 * sc ** 2, 0, 1); g = np.clip(sc + 0.008, 0, 1); b = np.clip(sc * 0.92 + 0.05 * (1 - sc), 0, 1)   # warm highs, teal lows
    return [int(v * 255) for v in r] + [int(v * 255) for v in g] + [int(v * 255) for v in b]
_LUT = _film_lut(); _GRAIN = []
def film(c, t):
    if not FILM: return c
    from PIL import ImageEnhance
    im = ImageEnhance.Color(c.convert("RGB")).enhance(0.86).point(_LUT)
    if not _GRAIN:
        rng = np.random.default_rng(7)
        for _ in range(12):                                                               # fine grain, half-res and scaled up so it reads as film
            n = rng.normal(0, 6.5, (H // 2, W // 2)).astype(np.float32)
            _GRAIN.append(np.asarray(Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.int16) - 128)
    a = np.asarray(im, np.int16) + _GRAIN[int(t * FPS) % len(_GRAIN)][..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def VFILE(rid):
    for f in sorted(glob.glob(M + rid + "_*")):
        if kind_v(f): return f
    return None
def kind_v(f):
    if not os.path.isfile(f): return False
    h = open(f, "rb").read(12); return h[4:8] == b"ftyp" or h[:4] == b"\x1a\x45\xdf\xa3"
CLIPS = {}
def lifted(g):
    if not g: return grade_im
    lut = [int(255 * (i / 255) ** g) for i in range(256)] * 3
    return lambda im: grade_im(im.convert("RGB").point(lut))
def clip_for(a, t0, t1):
    """one ffmpeg reader per shot; readers of other shots are closed (frames come in order inside a segment)"""
    k = (a["rid"], a["at"], round(t0, 3))
    if k not in CLIPS:
        for k2 in list(CLIPS): CLIPS.pop(k2).close()
        f = VFILE(a["rid"]); need = max(t1 - t0, 0.5)
        _, _, ln = VC.probe(f); avail = max(ln - a["at"] - 0.1, 0.5)
        sp = min(a["speed"], max(0.35, avail / need))                        # slow a short clip down to fill its shot (never the voice)
        CLIPS[k] = VC.Clip(f, src_in=a["at"], speed=sp, crop=a.get("crop"), look=a.get("look", "grade"), z0=max(a["z"][0], 1.0),
                           z1=max(a["z"][1], 1.0), c=a["c"], dur=need, grade=lifted(a.get("lift")))
    return CLIPS[k]
GH = {}
def ghost_frame(a, t, t0, t1):
    c = L.vignette(L.kenburns(tone(a["bg"]), t, t0, t1, a["z"][0] + 0.01, a["z"][1], (0.45, 0.5), (0.45, 0.5)))
    if "fg" not in GH:
        m = tone(a["fg"], a["crop"]).convert("RGB"); k = 980 / m.height; m = m.resize((int(m.width * k), 980), Image.LANCZOS)
        yy, xx = np.mgrid[0:m.height, 0:m.width].astype(np.float32)
        al = np.clip(xx / 300, 0, 1) * np.clip((m.height - 1 - yy) / 220, 0, 1) * np.clip(yy / 80, 0, 1) * 0.92
        m = m.convert("RGBA"); m.putalpha(Image.fromarray((al * 255).astype(np.uint8))); GH["fg"] = m
    m = GH["fg"]; u = clamp01((t - t0) / max(t1 - t0, 1e-6)); c.alpha_composite(m, (int(W - m.width + 30 - 20 * u), int(H - m.height + 20)))
    tag(c, a.get("tag")); return c
def vid_frame(a, t, t0, t1):
    c = L.vignette(clip_for(a, t0, t1).at(t - t0)); tag(c, a.get("tag"))
    if a.get("dim"): c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * a["dim"]))))
    return c
def vidp_frame(a, t, t0, t1):
    """a low-resolution clip as a print on the blurred room photo (never blown up full frame)"""
    c = blur_bg(a["bg"], CROP.get(a["bg"])).copy()
    im = clip_for(dict(a, look="grade", z=(1.0, 1.0), c=(0.5, 0.5)), t0, t1).at(t - t0).convert("RGB")
    h = a["h"]; im = im.resize((int(h * 16 / 9), h), Image.BICUBIC); card = L.print_card(im, im.width, rot=-1.2)
    L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag")); return c

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
    elif kind == "ghost": c = ghost_frame(a, t, t0, t1)
    elif kind == "vid": c = vid_frame(a, t, t0, t1)
    elif kind == "vidp": c = vidp_frame(a, t, t0, t1)
    elif kind == "tcard": c = tcard_frame(a, t, t0, t1)
    elif kind == "nmap": c = MS.map_panel(a, t, t0, t1)
    elif kind == "doc": c = doc_frame(a, t, t0, t1)
    elif kind == "counter": c = counter_frame(a, t, t0, t1)
    elif kind == "midask":                                     # frozen-feel blurred photo + the File Keeper ask, buttons on the words
        ln = a["ln"]; c = blur_bg(a["bg"], CROP.get(a["bg"])).copy(); wk = lambda w: (wt(ln, w) - t0) if wt(ln, w) is not None else None
        BA.mid_overlay(c, t - t0, t1 - t0, wk("like"), wk("subscrib"), wk("comment"))
    elif kind == "end":                                        # the File Keeper end card under the sign-off
        if "end" not in BG:
            sh = tone("F13"); k = max(W / sh.width, H / sh.height); sh = sh.resize((int(sh.width * k) + 1, int(sh.height * k) + 1), Image.LANCZOS)
            sh = sh.crop(((sh.width - W) // 2, (sh.height - H) // 2, (sh.width - W) // 2 + W, (sh.height - H) // 2 + H)).convert("RGB")
            BG["end"] = (sh, Image.blend(sh.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62))
        wl, wsb = wt(67, "like"), wt(67, "subscrib")
        c = BP.end_frame(BG["end"][0], BG["end"][1], t - t0, BP.NEXT["alcatraz46"], caps=[], t_like=(wl - t0) if wl else None, t_sub=(wsb - t0) if wsb else None)
    else:
        c = Image.new("RGBA", (W, H), INK + (255,))
    c = film(c, t)
    draw_ov(c, t, t0, t1)
    if kind not in ("tcard", "end"): draw_badge(c, t)
    draw_caps(c, t)
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
    def music(file, t0, t1, db, later=None):
        a = load(MUS + file); n = int((t1 - t0) * sr)
        while len(a) < n: a = np.concatenate([a, load(MUS + file)])
        a = a[:n] / (np.sqrt(np.mean(a[:n] ** 2)) + 1e-9) * vr
        if later:                                                              # (time, dB): ease down to a second level over 3 s
            ts, db2 = later; i = max(0, min(n, int((ts - t0) * sr))); r = min(int(3.0 * sr), n - i); g = np.ones(n, np.float32)
            k = 10 ** ((db2 - db) / 20); g[i:i + r] = np.linspace(1, k, r); g[i + r:] = k; a = a * g
        put(a, t0, db, fade=2.5)
    def loop(name, t0, t1, db):
        a = load(SFXD + name + ".mp3"); n = int((t1 - t0) * sr)
        while len(a) < n: a = np.concatenate([a, a])
        a = a[:n] / (np.sqrt(np.mean(a[:n] ** 2)) + 1e-9) * vr; put(a, t0, db, fade=1.5)
    # music beds (Kevin MacLeod, CC BY), about 19-22 dB under the voice
    # owner 25 Oct: "make the music more listened, a little louder, and much shown at the beginning": strong in the cold open, ~4 dB up after
    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Industrial Cinematic.mp3", tl(5), tl(18), -17); music("Man Down.mp3", tl(18), tl(28), -17)
    music("Rising Tide.mp3", tl(28), tl(40), -17); music("Thunder Dreams.mp3", tl(40), tl(50), -17); music("Industrial Cinematic.mp3", tl(50), tl(55), -17)
    music("Man Down.mp3", tl(55), tl(64), -18); music("Promises to Keep.mp3", tl(64), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("ambience_cinematic_suspense", tl(18), tl(28), -31); loop("waves_rough_sea_loop", tl(28), tl(40), -33)
    loop("wind_deep_cinematic_hum", tl(50), tl(55), -31)
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
        elif kind in ("kb", "vid", "vidp"): sfx("whoosh_fast_transition", t0 - 0.1, -32)
        elif kind == "midask":
            t1 = SHOT_T[i + 1]; wk = lambda w: (wt(a["ln"], w) - t0) if wt(a["ln"], w) is not None else None
            for tt, nm, db, ml in BA.mid_sfx(t1 - t0, wk("like"), wk("subscrib"), wk("comment")): sfx(nm, t0 + tt, db, maxlen=ml)
        elif kind == "end":
            wl, wsb = wt(67, "like"), wt(67, "subscrib")
            for tt, nm, db, ml in BA.end_sfx((wl - t0) if wl else None, (wsb - t0) if wsb else None): sfx(nm, t0 + tt, db, maxlen=ml)
    for j, (ln, off, kind, a) in enumerate(OV):
        if kind == "stamp": sfx("hit_horror_drum", OVT[j], -14)
        if kind in ("typecenter", "typecenter_red", "list"): sfx("typewriter_typing_old", OVT[j], -26)
        if kind == "nameplate": sfx("typewriter_typing_old", OVT[j], -24, maxlen=1.2)
        if kind == "brand":
            for tt, nm, db, ml in BA.STAMP_SFX: sfx(nm, OVT[j] + tt, db, maxlen=ml)
        if kind == "subpop":
            for tt, nm, db, ml in BA.CHIP_SFX: sfx(nm, OVT[j] + tt, db, maxlen=ml)
        if kind == "badge": sfx("clock_tick_single", OVT[j], -20)
    sfx("hit_cinematic_deep_impact", 0.0, -12)                                   # the cold open starts on a hit
    EV = [(0, "key", "keys_moving", -20), (0, "five|die", "heartbeat_single", -18), (0, "never", "hit_short_bass", -18),
          (3, "grenades|dropping", "hit_big_cinematic_impact", -20), (6, 0.0, "prison_metal_door_close", -26), (8, "hostage|took", "keys_dropping", -24),
          (12, "walked", "footsteps_tunnel_loop", -30), (14, "door|stepped", "heavy_sliding_door", -26), (15, "climbed", "metal_tool_drop", -24),
          (16, "hit", "metal_hammer_hit", -22), (17, "keys", "keys_moving", -22), (19, "locked", "locking_door_with_keys", -22),
          (20, "107|seven", "door_key_in_lock", -20), (22, "never|found", "hit_short_bass", -18), (23, "siren", "siren_vintage_manual", -24),
          (26, "fired", "hit_horror_drum", -18), (28, 0.0, "telephone_old_ring", -24), (30, 0.0, "motorboat_sea", -26),
          (31, "phoned", "telephone_vintage_ring", -26), (35, "searchlights|flares", "whoosh_ghostly", -26), (36, 0.0, "thunder_deep_rumble", -26),
          (43, "drilled", "drill_on_off", -26), (43, "lowered|grenades", "hit_big_cinematic_impact", -18), (44, "rifle|grenades", "hit_cinematic_deep_impact", -18),
          (46, "reporters", "reporters_camera_flashes", -26), (47, "phoned", "telephone_old_ring", -24), (50, 0.0, "heavy_sliding_door", -24),
          (51, "rifle|pistol", "metal_tool_falling", -24), (53, "walked", "reporters_camera_flashes", -28), (58, "executed|quentin", "hit_deep_heartbeat_impact", -20),
          (62, "roof", "wind_scary", -28), (64, 0.0, "hit_cinematic_deep_impact", -15), (67, -0.55, "metal_hammer_hit", -16), (67, -0.3, "hit_cinematic_deep_impact", -14)]
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
    name = name or "TheLastHours_14_BattleOfAlcatraz.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "One key, six convicts"), (5, "The six"), (10, "The gun cage"), (18, "Key 107"), (24, "Two cells"),
      (28, "The siege night"), (40, "Grenades on the roof"), (50, "The corridor"), (55, "The trial"), (61, "Carnes and 1962"),
      (64, "What the record shows")]

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
        for g, i in sorted(gaps)[:8] + sorted(gaps)[-8:]: print(f"  {g:5.2f}s  #{i} {SHOTS[i][0]} {SHOTS[i][1][0]} {SHOTS[i][1][1].get('rid', '') if isinstance(SHOTS[i][1][1], dict) else ''}")
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

