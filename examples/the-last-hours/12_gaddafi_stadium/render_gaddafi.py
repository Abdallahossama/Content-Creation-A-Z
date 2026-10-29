"""The Last Hours #11: the Benghazi basketball-stadium hanging, Tuesday 5 June 1984 (Muammar Gaddafi's Libya). Case File style,
colour grade, 1920x1080, burned-in captions, film finish. Built on render_khuld.py (file 10).
No frame of the 1984 Libyan TV broadcast is used, ever (copyright and our rules: research.md section 18); the stadium is told with
Libyan radio's own words (FBIS), US government pages and labelled illustrative footage. The 2009 UN scene uses the UN's own
public-domain official record (A/64/PV.3), not UN footage.
  uv run --no-project --with pillow --with numpy --with soundfile python render_gaddafi.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
import sys, os, re, json, math, glob, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween")
import lastkit as L
import vidclip as VC
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
import mshorts as MS                                   # dark Natural-Earth maps (VMap / map_panel)
MS.PW, MS.PH = W, H; MS._VIG.clear(); MS._STATES = []  # no state lines
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/12_gaddafi_stadium/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 20.0
NEXT = os.environ.get("LH_NEXT", "")                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/gaddafi_vo_chatterbox.wav")
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
def isdoc(rid): return rid[0] == "A"
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

# map points (lon, lat)
TRIPOLI, BENGHAZI, NALUT, TOBRUK, JALU, ZUWARAH, RASAJDIR = (13.19, 32.89), (20.07, 32.12), (10.98, 31.87), (23.96, 32.08), (21.55, 29.03), (12.08, 32.93), (11.57, 33.15)
V_LIBYA, V_WEST = (17.5, 31.0, 17.0), (12.3, 32.6, 5.5)

# ------------------------------------------------------------------ shot constructors
CROP = {"B1": (0.30, 0.0, 0.98, 1.0), "B13": (0.15, 0.0, 1.0, 1.0), "C3": (0.03, 0.03, 0.97, 0.97),
        "C9": (0.52, 0.12, 0.95, 0.88), "C19": (0.0, 0.0, 1.0, 0.72)}   # C9, C19: only the men on the tank / no street crowd
TB = {"B1": "MUAMMAR GADDAFI, AU SUMMIT, ADDIS ABABA, FEB 2009  ·  U.S. NAVY", "B2": "GADDAFI, AU SUMMIT, ADDIS ABABA, FEB 2009  ·  U.S. NAVY",
      "B3": "GADDAFI AT THE AFRICAN UNION SUMMIT, ADDIS ABABA, FEB 2009 (NOT NEW YORK)  ·  U.S. NAVY",
      "B5": "GADDAFI IN BRUSSELS, 2004  ·  © EUROPEAN COMMUNITIES, CC BY 4.0", "B6": "GADDAFI IN TRIPOLI, 2010  ·  © EUROPEAN UNION, CC BY 4.0",
      "B7": "GADDAFI IN TRIPOLI, 2008  ·  KREMLIN.RU, CC BY 4.0", "B12": "GADDAFI IN BELGRADE, 1970  ·  STEVAN KRAGUJEVIĆ, CC BY-SA 3.0",
      "B13": "GADDAFI IN ABUJA, 2006  ·  AGÊNCIA BRASIL, CC BY 3.0 BR",
      "C1": "BENGHAZI WATERFRONT, 2009  ·  JAW101IE, PD", "C2": "BENGHAZI AT NIGHT  ·  DENNIXO, CC BY-SA 3.0", "C3": "BENGHAZI AT NIGHT  ·  DENNIXO, CC BY-SA 3.0",
      "C5": "SIDI KHREBISH LIGHTHOUSE, BENGHAZI, 2014  ·  AL-MUJBIRI, CC BY-SA 3.0", "C7": "BENGHAZI, OLD CATHEDRAL DOMES AT MIDNIGHT, 2024  ·  MO ELFATY, CC BY-SA 4.0",
      "C9": "BENGHAZI, 25 FEB 2011  ·  AL JAZEERA ENGLISH, CC BY-SA 2.0", "C10": "BENGHAZI AT NIGHT FROM THE ISS, 2025  ·  NASA",
      "C11": "BENGHAZI FROM THE ISS, 2026  ·  NASA", "C12": "BENGHAZI FROM THE ISS, 2016  ·  NASA",
      "C14": "INSIDE BAB AL-AZIZIYA, AUG 2011  ·  “FREE LIBYAN”, CC BY 3.0", "C15": "BAB AL-AZIZIYA, AUG 2011  ·  “FREE LIBYAN”, CC BY 3.0",
      "C17": "REBELS AT THE GATE OF BAB AL-AZIZIYA, AUG 2011  ·  MAGHAREBIA, CC BY 2.0", "C19": "GREEN SQUARE, TRIPOLI, 2006  ·  JAW101IE, PD",
      "C21": "TRIPOLI, 1986  ·  ANDRÉ RAYMOND / MMSH, LICENCE OUVERTE", "C22": "TRIPOLI, 1986  ·  ANDRÉ RAYMOND / MMSH, LICENCE OUVERTE",
      "C23": "TRIPOLI, 1986  ·  ANDRÉ RAYMOND / MMSH, LICENCE OUVERTE", "C24": "TRIPOLI, 2011  ·  BEN SUTHERLAND, CC BY 2.0",
      "C26": "TRIPOLI AT NIGHT FROM THE ISS, 2025  ·  NASA", "C27": "CIA MAP OF LIBYA, 1981  ·  NATIONAL ARCHIVES", "C29": "CIA MAP OF LIBYA, 1993  ·  LIBRARY OF CONGRESS",
      "C30": "U.S. ARMY MAP OF EASTERN LIBYA, 1973", "C33": "LIBYA FROM SPACE, 2015  ·  NASA", "C4": "BENGHAZI, 2022  ·  AHMAD MOHAMAD Z, CC BY-SA 4.0", "C34": "5 ST JAMES'S SQUARE, LONDON: LIBYA'S EMBASSY IN 1984  ·  PAASIKIVI, CC BY-SA 4.0",
      "C35": "THE MEMORIAL, ST JAMES'S SQUARE, LONDON  ·  PAASIKIVI, CC BY-SA 4.0",
      "F3": "RAF LAKENHEATH, 14 APR 1986: F-111s ARMED FOR LIBYA  ·  USAF", "F4": "AN F-111 TAKES OFF FOR LIBYA, 14 APR 1986  ·  USAF",
      "F7": "AN F-14 OFF LIBYA, 15 APR 1986  ·  U.S. NAVY",
      "D1": "REAGAN'S ADDRESS ON THE LIBYA STRIKE, 14 APR 1986  ·  WHITE HOUSE TV, NATIONAL ARCHIVES",
      "G1": "ILLUSTRATIVE  ·  PEXELS", "G2": "ILLUSTRATIVE  ·  PEXELS", "G3": "ILLUSTRATIVE  ·  PEXELS"}
ILL = "ILLUSTRATIVE  ·  PEXELS"
for _r in ("E1", "E2", "E3", "E4", "E5", "E7", "E8", "E9", "E10", "E11", "E13", "E15", "E16", "E18", "E19", "E21", "E22", "E23", "E24"): TB[_r] = ILL
TB["E12"] = "THE MEDITERRANEAN AT DUSK  ·  ILLUSTRATIVE, PEXELS"; TB["E20"] = "AN ABANDONED SPORTS HALL (NOT LIBYA)  ·  ILLUSTRATIVE, PEXELS"
def DT(rid):
    n = re.match(r"A(\d+)", rid).group(1)
    fb = {"1": "8 MAY", "2": "8 MAY", "3": "8 MAY", "4": "9 MAY", "5": "9 MAY", "6": "10 MAY", "7": "14 MAY", "8": "16 MAY", "9": "17 MAY", "10": "20 APR",
          "11": "4 JUN", "12": "5 JUN", "13": "6 JUN", "14": "6 JUN", "15": "8 JUN", "16": "11 JUN", "17": "12 JUN"}
    if n in fb: return f"FBIS DAILY REPORT, {fb[n]} 1984: LIBYAN RADIO, U.S. GOVERNMENT TRANSLATION"
    return {"18": "STATE DEPARTMENT, COUNTRY REPORTS ON HUMAN RIGHTS FOR 1984, P. 1314", "19": "STATE DEPARTMENT, COUNTRY REPORTS FOR 1984, P. 1315 (FEB 1985)",
            "20": "STATE DEPARTMENT, COUNTRY REPORTS FOR 1984, P. 1316 (FEB 1985)", "21": "STATE DEPARTMENT, COUNTRY REPORTS FOR 1984, P. 1317 (FEB 1985)",
            "22": "LIBRARY OF CONGRESS, LIBYA: A COUNTRY STUDY (1989), P. 203", "23": "LIBRARY OF CONGRESS, LIBYA: A COUNTRY STUDY (1989), P. 205",
            "24": "LIBRARY OF CONGRESS, LIBYA: A COUNTRY STUDY (1989), P. 290", "26": "CIA, NATIONAL INTELLIGENCE DAILY, 9 MAY 1984 (TOP SECRET, DECLASSIFIED)",
            "27": "CIA, NATIONAL INTELLIGENCE DAILY, 10 MAY 1984 (DECLASSIFIED)", "28": "CIA, NATIONAL INTELLIGENCE DAILY, 12 MAY 1984 (DECLASSIFIED)",
            "31": "U.S. WARNING MEETING OF 24 MAY 1984 (NIC 03109-84, DECLASSIFIED)", "40": "CIA, “LIBYA: QADHAFI'S POLITICAL POSITION”, 17 JUL 1986 (DECLASSIFIED)",
            "41": "CIA CHART, “QADHAFI'S ADVISERS, HENCHMEN, ENEMIES”, AUG 1986", "43": "CIA, “LIBYAN OPPOSITION GROUPS”, MAY 1987 (DECLASSIFIED)",
            "90": "UNITED NATIONS GENERAL ASSEMBLY, OFFICIAL RECORD A/64/PV.3, 23 SEP 2009"}.get(n, "DECLASSIFIED U.S. GOVERNMENT RECORD")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {"E4": (0.15, 0.0, 1.0, 1.0), "E9": (0.0, 0.25, 0.75, 1.0), "E2": (0.15, 0.1, 0.85, 0.9)}   # E4: two tiny unidentifiable figures far left; E9: no typed text
LIFT = {"E11": 0.6, "E13": 0.75, "E12": 0.6, "E4": 0.8, "E23": 0.75, "E16": 0.8}                    # gamma for dark clips (LESSONS 34)
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag or "GADDAFI, 2009 (U.S. NAVY), OVER AN EMPTY ARENA (PEXELS)  ·  COMPOSITE"))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C6", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

def _june_pins():
    return [("pin", *NALUT, "NALUT  ·  3 JUN", 0.0, 22, 34), ("pin", *TRIPOLI, "TRIPOLI  ·  5 JUN", 0.35, 22, -30), ("pin", *BENGHAZI, "BENGHAZI  ·  5 JUN", 0.7),
            ("pin", *TOBRUK, "TOBRUK  ·  7 JUN", 1.05, -150, -34), ("pin", *JALU, "JALU  ·  7 JUN", 1.4), ("pin", *ZUWARAH, "ZUWARAH  ·  10 JUN", 1.75, -40, -44),
            ("label", 17.4, 27.6, "+ “TANZIM”, 4 JUN: PLACE NOT IDENTIFIED", 2.1, 26)]

SHOTS = [
 (0, GHOST("G1", "B1", CROP["B1"])),                                              # frame 1: Gaddafi ghosted over empty arena seats (= thumbnail A)
 ((0, "knees"), VID("E19", z=(1.05, 1.12), dim=0.15)),
 ((0, "eight"), COUNTER([((0, "eight"), "8 DAYS")], "3-10 JUNE 1984  ·  EIGHT MEN EXECUTED IN PUBLIC", "C26", size=300)),
 ((0, "nobody"), VID("E4", at=1.0, z=(1.0, 1.06))),
 (1, TCARD("23 SEP 2009", "Wednesday  ·  the United Nations, New York", "B2")),
 ((1, "fifteen|15"), COUNTER([((1, "fifteen|15"), "15 MIN"), ((1, "hour|half"), "96 MIN")], "THE TIME HE WAS GIVEN  ·  THE TIME HE TOOK (VOA)", "B3", size=300)),
 (2, KB("B3", z=(1.05, 1.18), c0=(0.5, 0.35))),
 ((2, "charter"), DOC("A90p15", [("of which I have a copy", (2, "charter"))])),
 ((2, "security"), DOC("A90p19", [("2+3", (2, "security"))])),
 (3, KB("B1", crop=(0.25, 0.0, 1.0, 1.0), z=(1.05, 1.18), c0=(0.6, 0.45))),
 ((3, "own|country"), KB("C10", z=(1.0, 1.12))),
 (4, TCARD("5 JUNE 1984", "Tuesday  ·  Benghazi  ·  6 Ramadan", "C7")),
 ((4, "ramadan"), KB("C1", z=(1.0, 1.1), dim=0.1)),
 (5, VID("E22", z=(1.0, 1.05))),
 ((5, "stadium|basketball"), VID("E18", at=8.0, z=(1.0, 1.08))),
 (6, VID("E19", at=3.0, z=(1.15, 1.25), c=(0.62, 0.35), dim=0.2)),
 ((6, "america"), KB("C27", z=(1.1, 1.25), c0=(0.5, 0.45))),
 (7, DOC("A14", [("ash-Shuwayri", (7, "radio|agent"))])),
 ((7, "eight"), KB("C33", z=(1.05, 1.2), dim=0.2)),
 (8, VID("E21", z=(1.0, 1.06))),
 ((8, "radio"), VID("E7", z=(1.0, 1.08))),
 ((8, "washington"), VID("E9", at=20.0, z=(1.05, 1.12))),
 (9, KBP("A28", h=900)),
 ((9, "americans|knew"), VID("D2", at=20.0, z=(1.05, 1.1), tag="PRESIDENT REAGAN, 9 APR 1986  ·  WHITE HOUSE TV, NATIONAL ARCHIVES")),
 ((9, "question"), KB("B5", z=(1.05, 1.15), c0=(0.5, 0.4))),
 (10, KB("B12", z=(1.05, 1.15), c0=(0.5, 0.4))),
 ((10, "title|official"), KB("B13", z=(1.05, 1.15), c0=(0.55, 0.4))),
 (11, DOC("A18", [("decisionmaker", 11)])),
 (12, TCARD("16 APRIL 1984", "Monday  ·  Tripoli University", "C21")),
 ((12, "hanged|two"), DOC("A10", [("Hanged", (12, "hanged|two"))])),
 (13, KB("B7", z=(1.05, 1.18), c0=(0.45, 0.4), dim=0.1)),
 (14, KB("C34", z=(1.0, 1.1))),
 ((14, "shots|ten"), VID("E15", z=(1.0, 1.05))),
 (15, KB("C35", z=(1.0, 1.1))),
 (16, DOC("A43", [("46+47", 16)])),
 (17, DOC("A41", [("117+118", (17, "group|national"))])),
 (18, NMAP(V_WEST, ops=[("pin", *TRIPOLI, "TRIPOLI", -9), ("pin", *RASAJDIR, "TUNISIAN BORDER", 0.8, 22, -34)])),
 ((18, "three|stop"), VID("E11", at=4.0, z=(1.0, 1.06))),
 (19, DOC("A3", [("Huwaf", (19, "killed|one")), ("passport", (19, "sudanese|passport"))])),
 (20, KB("C24", z=(1.0, 1.1))),
 (21, TCARD("8:30 AM", "Tuesday, May 8, 1984  ·  Tripoli", "C22")),
 (22, KB("C14", z=(1.0, 1.1))),
 ((22, "barracks|home"), DOC("A1", [("Shooting in Tripoli", (22, "barracks|home"))])),
 (23, DOC("A5", [("artillery", 23), ("four hours", (23, "fighting|four"))])),
 (24, KB("C24", z=(1.1, 1.22), c0=(0.55, 0.5))),
 ((24, "shops|shutters"), KB("C23", z=(1.0, 1.1))),
 (25, DOC("A5", [("1130 GMT", 25)])),
 (26, KB("C19", z=(1.0, 1.1))),
 (27, KB("C15", z=(1.0, 1.1), dim=0.15)),
 (28, VID("E12", at=2.0, z=(1.0, 1.06))),
 ((28, "machine|gun"), KB("B2", z=(1.1, 1.22), c0=(0.5, 0.35), dim=0.1)),
 (29, VID("E2", z=(1.0, 1.06))),
 (30, KB("B5", z=(1.15, 1.28), c0=(0.5, 0.35))),
 ((30, "countries|pay"), KB("C21", z=(1.05, 1.15), dim=0.1)),
 (31, TCARD("9 MAY 1984", "Wednesday  ·  Washington  ·  TOP SECRET", "C27")),
 (32, DOC("A26", [("Firefight", 32), ("small group", 33), ("no chance", 34)])),
 (35, DOC("A27", [("strengthened", 35)])),
 (36, VID("E9", at=60.0, z=(1.05, 1.12))),
 ((36, "library|study"), DOC("A22", [("28+29", (36, "library|study"))])),
 (37, COUNTER([((37, "248|200|two"), "200")], "ARRESTED IN 48 HOURS  ·  A LIBYAN SOURCE TO LE MONDE", "C22")),
 ((37, "soldiers"), KB("C23", crop=(0.1, 0.1, 0.9, 0.9), z=(1.0, 1.08))),
 (38, DOC("A24", [("26", 38)])),
 (39, DOC("A7", [("70", 39), ("stray dogs", 40)])),
 (41, KBP("A36", h=900)),
 (42, NMAP(V_LIBYA, ops=[("pin", *TRIPOLI, "TRIPOLI", -9), ("route", [TRIPOLI, BENGHAZI], 0.6, 1.6), ("pin", *BENGHAZI, "BENGHAZI", 2.2),
                        ("label", 16.6, 33.5, "ABOUT 400 MILES", 2.4, 34)])),
 (43, DOC("A8", [("Barkah", 43), ("24+26", 44)])),
 (45, DOC("A9", [("Immediate execution", (45, "immediate|reads"))])),
 (46, KB("C2", z=(1.0, 1.1))),
 (47, TCARD("24 MAY 1984", "Thursday  ·  a U.S. warning meeting", "C29")),
 (48, DOC("A31", [("lash out", (48, "concerned|lash|qadhafi|gaddafi"))])),
 (49, COUNTER([((49, "ten|10"), "10 DAYS")], "FROM THE WARNING TO THE FIRST HANGING", "C29")),
 (50, TCARD("1 RAMADAN", "Thursday, May 31, 1984", "C5")),
 (51, NMAP(V_WEST, ops=[("pin", *TRIPOLI, "TRIPOLI", -9), ("pin", *NALUT, "NALUT", 0.6)])),
 ((51, "hanged|two"), DOC("A11", [("hanging", (51, "hanged|two"))])),
 ((51, "radio"), VID("E7", at=4.0, z=(1.05, 1.12))),
 (52, DOC("A12", [("Tanzim", 52)])),
 (53, DOC("A13", [("Zardi", (53, "tripoli|local"))])),
 (54, KB("C10", z=(1.1, 1.25), c0=(0.5, 0.5))),
 (55, DOC("A12", [("recruited", (55, "recruited|american")), ("fuel", (55, "destroy|markets"))])),
 (56, VID("E23", z=(1.0, 1.06))),
 (57, KB("C12", z=(1.0, 1.12))),
 (58, KB("C30", z=(1.1, 1.25), c0=(0.45, 0.5))),
 (59, VID("E11", at=18.0, z=(1.0, 1.06))),
 (60, KB("C3", z=(1.0, 1.1), dim=0.35)),
 (61, TCARD("5 JUNE 1984", "Tuesday  ·  Benghazi  ·  the sixth day of Ramadan", "C11")),
 (62, VID("E23", at=2.0, z=(1.1, 1.16))),
 ((62, "stadium|basketball"), VID("E18", at=30.0, z=(1.0, 1.06))),
 (63, VID("E4", at=4.0, z=(1.05, 1.1))),
 (64, VID("E20", z=(1.0, 1.06), dim=0.2)),
 (65, VID("E3", at=5.0, z=(1.05, 1.1))),
 (66, VID("E21", at=6.0, z=(1.05, 1.1))),
 (67, VID("E1", at=9.5, speed=0.5, z=(1.0, 1.06), dim=0.15)),
 (68, VID("E2", at=5.0, z=(1.1, 1.18))),
 (69, KB("C5", z=(1.0, 1.1), dim=0.3)),
 (70, TCARD("7:30 AM", "Wednesday, June 6, 1984  ·  Tripoli radio", "C26")),
 ((70, "official|version"), DOC("A13", [("78+80", 71), ("88+89+91", 72), ("93+95+97", (72, "members|carried")), ("Michigan", 73),
                                         ])),
 (74, KB("C2", z=(1.1, 1.2), c0=(0.55, 0.5))),
 (75, DOC("A15", [("57", (75, "tobruk")), ("Jalu", (75, "jalu"))])),
 (76, DOC("A16", [("Zuwarah", 76)])),
 (77, NMAP(V_LIBYA, ops=_june_pins())),
 (78, TCARD("11 JUNE 1984", "Monday  ·  late night  ·  live on the radio", "B6")),
 ((78, "anniversary|bases"), VID("E8", z=(1.0, 1.06))),
 (79, DOC("A17", [("15", 79), ("17", (79, "trained|this")), ("heart of America", (80, "capable|exporting"))])),
 (81, DOC("A90p19", [("2+3", (81, "terror|called|security"))])),
 (82, DOC("A19", [("37", 82)])),
 (83, KBP("A21", h=920)),
 (84, DOC("A19", [("unprecedented", 84)])),
 (85, DOC("A20", [("gruesome", 85)])),
 (86, DOC("A18", [("absence of a", (86, "embassy|admits"))])),
 (87, DOC("A23", [("12", 87)])),
 (88, KB("F4", z=(1.0, 1.1))),
 ((88, "cited|berlin"), KB("F7", z=(1.0, 1.1))),
 (89, VID("D1", at=30.0, z=(1.0, 1.06))),
 (90, KBP("A40", h=900)),
 (91, DOC("A40", [("17+18+19", 91)])),
 (92, DOC("A10", [("Students", (92, "students|tripoli"))])),
 (93, DOC("A16", [("76+78", (93, "charge|libyan"))])),
 (94, VID("E10", at=8.0, z=(1.0, 1.06))),
 ((94, "twenty|27"), COUNTER([((94, "twenty|27"), "27 YEARS")], "1984 → 2011  ·  FOUR TAPES, KEPT BY HIS FAMILY", "C9", size=300)),
 (95, KB("C9", z=(1.0, 1.1))),
 (96, VID("E1", at=10.0, z=(1.0, 1.06))),
 (97, KB("C17", z=(1.0, 1.1))),
 (98, KB("B6", z=(1.05, 1.15), c0=(0.62, 0.35), dim=0.25)),
 ((98, "9"), COUNTER([((98, "9"), "9,998 DAYS")], "FROM THE STADIUM TO SIRTE", "C12", size=260)),
 (99, DOC("A41", [("117+118", (99, "magariaf|exile|mohammed"))])),
 (100, VID("E20", at=1.0, z=(1.05, 1.1))),
 (101, KBP("A14", h=900)),
 (102, KB("C1", z=(1.0, 1.1), dim=0.3)),
 (103, DOC("A14b", [("Michigan", (103, "radio|trained|agent"))])),
 ((103, "cousin|peaceful"), KB("C3", crop=(0.2, 0.15, 0.85, 0.85), z=(1.0, 1.08), dim=0.25)),
 (104, VID("E12", at=8.0, z=(1.05, 1.1), dim=0.2)),
 (105, KB("C11", z=(1.05, 1.18))),
 (106, KB("C4", z=(1.0, 1.1), dim=0.2)),
 ((107, 0.0), ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "hookleft", ("8 MEN.", "8 DAYS.")),                               # from frame 1 (LEAD = 0.8 s)
 (0, "nobody", "under", "THE CHARGE WAS NEVER PROVEN"),
 (1, 0.0, "badge", "WED 23 SEP 2009"),
 (2, "security", "under", "“THE TERROR COUNCIL”  ·  UN OFFICIAL RECORD"),
 (3, 0.2, "nameplate", ("MUAMMAR GADDAFI", "RULED LIBYA 1969-2011  ·  PHOTO 2009, U.S. NAVY")),
 (4, 0.0, "badge", "TUE 5 JUN 1984"),
 (5, 0.2, "under", "AS DESCRIBED BY THE GUARDIAN AND HIS FAMILY, 2011  ·  ILLUSTRATIVE"),
 (6, 0.2, "under", "NO SAFE PHOTO OF HIM EXISTS"),
 (8, 0.0, "typecenter", "WE WON'T SHOW YOU THE FILM"),
 (9, "americans|knew", "under", "WHAT THE AMERICANS KNEW"),
 (9, "radio|admitted", "under", "WHAT GADDAFI'S RADIO ADMITTED"),
 (9, "question", "under", "AND THE QUESTION NOBODY HAS ANSWERED"),
 (12, 0.0, "badge", "MON 16 APR 1984"),
 (13, 0.2, "under", "THE GALLOWS, BY GADDAFI'S PORTRAIT  ·  THE WASHINGTON POST, 1984"),
 (14, 0.0, "badge", "TUE 17 APR  ·  10:00 AM  ·  LONDON"),
 (15, 0.2, "under", "11 DEMONSTRATORS WOUNDED  ·  A POLICEWOMAN KILLED  ·  HANSARD"),
 (17, "magariaf|leader", "under", "MUHAMMAD AL-MAGARIAF  ·  NFSL LEADER  ·  NO SAFE PHOTO OF HIM"),
 (18, 0.0, "badge", "SUN 6 MAY 1984"),
 (20, 0.2, "under", "GADDAFI'S VERSION, AS TOLD TO LE MONDE"),
 (21, 0.0, "badge", "TUE 8 MAY  ·  8:30 AM"),
 (22, 0.2, "under", "BAB AL-AZIZIYA  ·  GADDAFI'S HOME AND HEADQUARTERS  ·  PHOTO 2011"),
 (24, 0.0, "brand", None),                                          # the 2 s channel stamp, over moving footage, voice keeps going
 (25, 0.0, "badge", "8 MAY  ·  1:30-2:30 PM"),
 (26, 0.0, "badge", "8 MAY  ·  4:30 PM"),
 (26, 0.2, "under", "GREEN SQUARE, TRIPOLI  ·  PHOTO 2006"),
 (27, "nobody", "stamp", ("UNKNOWN", 1240, 400)),
 (28, 0.0, "badge", "8 MAY  ·  6:30 PM"),
 (29, 0.0, "badge", "8 MAY  ·  9:45 PM"),
 (29, 0.2, "under", "LIBYAN TV SHOWED THE BODIES  ·  WE DON'T"),
 (31, 0.0, "badge", "WED 9 MAY 1984"),
 (36, 0.0, "under", "MYTH OR RECORD"),
 (36, "daily|briefs|news", "stamp", ("DISPUTED", 1260, 400)),
 (39, 0.0, "badge", "SAT 12 MAY 1984"),
 (41, 0.0, "typecenter", "“STRAY DOGS”"),
 (42, 0.0, "badge", "TUE 15 MAY  ·  NIGHT"),
 (43, 0.2, "under", "AL-BIRKAH PEOPLE'S CONGRESS, BENGHAZI"),
 (45, 0.0, "badge", "WED 16 MAY 1984"),
 (46, 0.0, "typecenter", "REMEMBER: MAY 15"),
 (74, "fifteenth|15", "typecenter", "MAY 15"),
 (47, 0.0, "badge", "THU 24 MAY 1984"),
 (50, 0.0, "badge", "THU 31 MAY  ·  1 RAMADAN"),
 (51, 0.0, "badge", "SUN 3 JUN 1984"),
 (52, 0.0, "badge", "MON 4 JUN 1984"),
 (53, 0.0, "badge", "TUE 5 JUN  ·  10:00 AM"),
 (54, 0.2, "under", "BENGHAZI  ·  ABOUT 400 MILES EAST"),
 (56, 0.0, "typecenter", "WHO WAS HE?"),
 (57, 0.2, "nameplate", ("AL-SADIQ HAMID AL-SHUWEHDI", "30  ·  AERONAUTICAL ENGINEER  ·  NO SAFE PHOTO OF HIM EXISTS")),
 (58, 0.2, "under", "HIS COUSIN, TO THE DAILY TELEGRAPH, 2011"),
 (60, "liked|everybody", "quote", ("“He liked everybody, and everybody liked him.”", "HIS COUSIN, TO THE DAILY TELEGRAPH, 2011")),
 (61, 0.0, "badge", "TUE 5 JUN 1984  ·  BENGHAZI"),
 (62, 0.2, "under", "AS DESCRIBED BY THE GUARDIAN AND HIS FAMILY  ·  ILLUSTRATIVE"),
 (64, 0.0, "quote", ("“...a terrorist from the Muslim Brotherhood," + chr(10) + "an agent of America.”", "THE COURT'S WORDS, AS REPORTED BY THE GUARDIAN, 2011")),
 (66, 0.0, "typecenter", "WE WON'T SHOW IT"),
 (68, 0.2, "under", "“MANY LIBYANS SAW THE ORIGINAL LIVE BROADCAST”  ·  HUMAN RIGHTS WATCH"),
 (70, 0.0, "badge", "WED 6 JUN  ·  7:30 AM"),
 (75, 0.0, "badge", "THU 7 JUN 1984"),
 (76, 0.0, "badge", "SUN 10 JUN 1984"),
 (77, 0.0, "typecenter_red", "8 IN 8 DAYS"),
 (78, 0.0, "badge", "MON 11 JUN  ·  11:42 PM"),
 (81, 0.0, "badge", "NEW YORK  ·  23 SEP 2009"),
 (81, 0.6, "subpop", None),                                        # silent ask at ~70%, right after the payoff (LESSONS 37)
 (82, 0.0, "badge", "WED 13 JUN 1984"),
 (83, 0.0, "badge", "FEB 1985"),
 (88, 0.0, "badge", "14 APR 1986"),
 (89, 0.2, "under", "PRESIDENT REAGAN, 14 APRIL 1986"),
 (90, 0.0, "badge", "17 JUL 1986"),
 (92, 0.0, "under", "MYTH OR RECORD: THE FIRST?"),
 (92, "no", "stamp", ("NOT THE FIRST", 1240, 400)),
 (93, 0.0, "under", "MYTH OR RECORD: A CIA AGENT?"),
 (93, "evidence", "stamp", ("NO EVIDENCE SHOWN", 1200, 400)),
 (95, 0.0, "badge", "FEB 2011"),
 (97, 0.0, "badge", "23 AUG 2011"),
 (98, 0.0, "badge", "THU 20 OCT 2011"),
 (100, 0.0, "typecenter", "WHAT NOBODY KNOWS"),
 (102, "amnesty", "quote", ("“...executed within an hour of their arrest.”", "AMNESTY INTERNATIONAL REPORT, 1985")),
 (104, 0.2, "quote", ("“He knew he was risking his life.”", "ASHOUR SHAMIS, WHO HELPED PLAN THE ATTACK, TO THE GUARDIAN, 2011")),
 (105, 0.0, "typecenter", "NOT IN ONE U.S. FILE WE READ"),
 (106, 0.0, "under", "A PLOTTER, OR AN EXAMPLE?  TELL ME BELOW"),
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
    elif kind == "brand":                                      # 2 s channel stamp over moving footage: no spoken ident, no pause
        u = t - t0
        if u < 2.2:
            al = ease(u / 0.35) * ease((2.2 - u) / 0.35)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 150, W, H / 2 + 150), fill=(0, 0, 0, int(150 * al))); c.alpha_composite(lay)
            L.text(c, "the", W / 2, H / 2 - 95, 52, STEEL, SER, alpha=al); L.text(c, "LAST HOURS", W / 2, H / 2 + 5, 150, BONE, COND, alpha=al)
            L.text(c, "FILE 11  ·  BENGHAZI  ·  JUNE 1984", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
    elif kind == "hookleft":                                   # frame-1 hook text in thumbnail blocks, left, off the face
        f = L.font(COND, 132); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i, s in enumerate(a):
            y = H / 2 - 130 + i * 180; w = f.getlength(s)
            d.rectangle((80, y - 82, 80 + w + 56, y + 82), fill=((0, 0, 0, 230) if i == 0 else (255, 204, 0, 255)))
            d.text((108, y), s, font=f, fill=(BONE + (255,)) if i == 0 else (10, 10, 10, 255), anchor="lm")
        c.alpha_composite(lay)
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


# ------------------------------------------------------------------ burned-in captions (word-synced; the current word in yellow)
CAPFIX = {"Gadhafi": "Gaddafi", "Qaddafi": "Gaddafi", "Qadhafi": "Gaddafi", "Qadhafi's": "Gaddafi's", "Qaddafi's": "Gaddafi's", "Al": "al",
          (17, "-Mughal"): "-Magariaf", (17, "Yaf"): "", (99, "-Magaryaf"): "-Magariaf", (99, "Muhammad"): "Mohammed",
          (19, "Ahmad"): "Ahmed", (19, "R"): "", (19, "Waas"): "Ahwas", (71, "Bayan"): "-Bayan", (71, "Awawal"): "-Awwal",
          (76, "Zuawara"): "Zuwarah", (2, "terror"): "Terror", (2, "council"): "Council", (81, "terror"): "Terror", (81, "council"): "Council",
          (84, "it"): "It", (1, "You"): "", (37, "248"): "200 in 48", (59, "3"): "three", (59, "-1"): "one", (45, "immediate"): "Immediate", (19, "exiles"): "exiles'"}  # whisper spellings -> the record's (core word; punctuation kept; "" drops it)
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
    elif kind == "end":
        c = L.vignette(L.kenburns(blur_bg("C11", None), t, t0, t1))
        L.text(c, "the", W / 2, 120, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 230, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 320, t, t0, width=7)
        L.typewriter(c, ("NEXT FILE:  " + NEXT) if NEXT else "SUBSCRIBE FOR THE NEXT FILE", t, t0 + 0.2, W / 2, 410, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
        if t > VO_END:
            d = ImageDraw.Draw(c)
            for x in (110, 1170): d.rectangle((x, 520, x + 640, 880), outline=STEEL + (255,), width=3)
            d.ellipse((835, 575, 1085, 825), outline=STEEL + (255,), width=3)
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
RADIO = {"A3", "A7", "A11", "A12", "A13", "A15", "A16", "A17"}
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
    music("Thunder Dreams.mp3", 0.0, tl(10), -11, later=(tl(4), -15)); music("Industrial Cinematic.mp3", tl(10), tl(31), -17); music("Man Down.mp3", tl(31), tl(51), -17)
    music("Rising Tide.mp3", tl(51), tl(61), -17); music("Thunder Dreams.mp3", tl(61), tl(75), -18); music("Promises to Keep.mp3", tl(75), tl(94), -17)
    music("Thunder Dreams.mp3", tl(94), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(10), -30); loop("ambience_cinematic_suspense", tl(21), tl(31), -31); loop("wind_cold_interior", tl(61), tl(70), -33)
    loop("wind_deep_cinematic_hum", tl(100), tl(107), -31)
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
    for j, (ln, off, kind, a) in enumerate(OV):
        if kind == "stamp": sfx("hit_horror_drum", OVT[j], -14)
        if kind in ("typecenter", "typecenter_red", "list"): sfx("typewriter_typing_old", OVT[j], -26)
        if kind == "nameplate": sfx("typewriter_typing_old", OVT[j], -24, maxlen=1.2)
        if kind == "brand": sfx("hit_cinematic_deep_impact", OVT[j], -16)
        if kind == "subpop": sfx("whoosh_fast_transition", OVT[j], -24)
        if kind == "badge": sfx("clock_tick_single", OVT[j], -20)
    sfx("hit_cinematic_deep_impact", 0.0, -12)                                   # the cold open starts on a hit
    EV = [(0, "knees", "heartbeat_single", -18), (2, "tossed|shoulder", "paper_big_page_turn", -20), (8, 0.0, "radio_static_crackles", -28),
          (14, "shots|ten", "hit_short_bass", -19), (18, "three|stop", "siren_vintage_manual", -34), (21, 0.0, "hit_cinematic_deep_impact", -16),
          (26, "sirens", "siren_vintage_manual", -30), (29, 0.0, "radio_static_fx", -26), (31, 0.0, "typewriter_typing_old", -22),
          (39, 0.0, "radio_static_fx", -28), (45, "immediate|reads", "hit_short_bass", -18), (49, "ten|10", "hit_horror_drum", -16),
          (51, "radio", "radio_static_fx", -26), (59, "secret|police", "heavy_sliding_door", -24), (61, 0.0, "hit_cinematic_deep_impact", -15),
          (66, "hanged", "hit_deep_heartbeat_impact", -20), (70, 0.0, "radio_static_fx", -26), (77, 0.0, "hit_horror_drum", -16),
          (80, "heart", "hit_cinematic_deep_impact", -15), (81, "terror|called", "paper_big_page_turn", -20), (88, 0.0, "helicopter_far_away", -30),
          (94, 0.0, "radio_static_crackles", -30), (98, "9998|nine", "hit_short_bass", -18), (100, 0.0, "hit_cinematic_deep_impact", -15),
          (106, 0.2, "typewriter_return_bell", -18)]
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
    name = name or "TheLastHours_11_GaddafiStadium.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "The stadium, and the UN"), (10, "Gaddafi's Libya: two students, and London"), (18, "May 6: the border"),
      (21, "May 8: Bab al-Aziziya"), (31, "Washington: \"Firefight in Tripoli\""), (37, "The arrests"), (42, "May 15: Benghazi votes"),
      (47, "A warning"), (51, "June 3-5: the radio bulletins"), (56, "Who was he?"), (61, "June 5: the stadium"), (70, "June 6: the official version"),
      (75, "Eight in eight days"), (78, "\"The heart of America\""), (83, "Washington's verdict"), (92, "Myths"), (94, "2011"),
      (100, "What nobody knows")]

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

