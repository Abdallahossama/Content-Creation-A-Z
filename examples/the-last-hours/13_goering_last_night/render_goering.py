"""The Last Hours #13: Hermann Göring's last night, Nuremberg prison, Tuesday 15 October 1946 (10:45 p.m.), and the hangings of
Wednesday 16 October (1:11-2:57 a.m.). Case File style, colour grade, 1920x1080, burned-in captions, film finish. Built on render_gaddafi.py.
Real images only: U.S. Army / National Archives photos and documents (238-NT, RG 242 Board of Proceedings), the IMT record, 1946 newspapers,
public-domain newsreels (United News, Universal), Pexels textures labelled ILLUSTRATIVE. Never shown: the executions, the gallows, the dead,
any woman. Owner rules: research.md sections 12-13 (do-not-say, YouTube safety).
  uv run --no-project --with pillow --with numpy --with soundfile python render_goering.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
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

ROOT = "D:/why habibi/_newchannel/13_goering_last_night/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 20.0
NEXT = os.environ.get("LH_NEXT", "")                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/goering_vo_chatterbox.wav")
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
NUREMBERG, MUNICH = (11.08, 49.45), (11.58, 48.14)
V_DE, V_BAV = (11.0, 49.2, 8.0), (11.3, 48.85, 3.4)

# ------------------------------------------------------------------ shot constructors
CROP = {"C13": (0.0, 0.18, 1.0, 0.74), "C12": (0.0, 0.2, 1.0, 0.76), "C11": (0.0, 0.18, 1.0, 0.74), "C16": (0.0, 0.2, 1.0, 0.76),
        "C17": (0.0, 0.2, 1.0, 0.76), "C4": (0.0, 0.25, 1.0, 0.8), "C5": (0.0, 0.2, 1.0, 0.76), "B1": (0.0, 0.12, 1.0, 0.68),
        "B2": (0.0, 0.12, 1.0, 0.68), "B3": (0.0, 0.1, 1.0, 0.66), "B5": (0.0, 0.12, 1.0, 0.68), "B6": (0.0, 0.1, 1.0, 0.66),
        "B9": (0.0, 0.14, 1.0, 0.7), "B10": (0.0, 0.14, 1.0, 0.7), "B12": (0.0, 0.14, 1.0, 0.7), "B17": (0.0, 0.08, 1.0, 0.64),
        "B18": (0.0, 0.08, 1.0, 0.64), "B20": (0.0, 0.2, 1.0, 0.76), "C23": (0.0, 0.15, 1.0, 0.72),
        "F2": (0.0, 0.2, 1.0, 0.76), "F5": (0.0, 0.25, 1.0, 0.75), "F6": (0.0, 0.25, 1.0, 0.75), "F9": (0.0, 0.2, 1.0, 0.76)}   # portrait photos: a 16:9 band
NA = "U.S. ARMY, NATIONAL ARCHIVES"
TB = {"B1": f"GÖRING ON THE WITNESS STAND, NUREMBERG, 1946  ·  {NA}", "B2": f"GÖRING IN THE DOCK, 1946  ·  {NA}",
      "B3": f"GÖRING IN HIS CELL, NUREMBERG PRISON  ·  {NA}", "B4": f"GÖRING IN THE WITNESS BOX, 1946  ·  {NA}",
      "B5": f"GÖRING ON THE WITNESS STAND, 1946  ·  {NA}", "B6": f"GÖRING IN HIS CELL  ·  {NA}", "B7": f"GÖRING READING ON HIS COT  ·  {NA}",
      "B8": f"“A MUCH THINNER GOERING HAVING SUPPER IN HIS CELL”  ·  {NA}", "B9": f"GÖRING WRITING A LETTER IN HIS CELL  ·  {NA}",
      "B10": f"GÖRING AND HESS IN THE DOCK  ·  {NA}", "B11": f"GÖRING, HANS FRANK AND THE PRISON PSYCHOLOGIST, DR. GILBERT  ·  {NA}",
      "B12": f"GÖRING ENTERS THE COURTROOM  ·  {NA}", "B13": f"GÖRING AND HIS LAWYER, THROUGH THE SCREEN  ·  {NA}",
      "B14": f"GÖRING'S CELL DOOR, LAUNDRY DAY  ·  {NA}", "B15": f"FRONT ROW: GÖRING, HESS, RIBBENTROP, KEITEL  ·  {NA}",
      "B16": "THE DEFENDANTS' DOCK  ·  RAY D'ADDARIO, U.S. ARMY / NATIONAL ARCHIVES", "B17": "GÖRING AFTER HIS SURRENDER, MAY 1945  ·  U.S. ARMY AIR FORCES",
      "B18": f"COL. BURTON C. ANDRUS, PRISON COMMANDANT  ·  {NA}", "B19": f"COL. ANDRUS AT HIS DESK  ·  {NA}",
      "B20": f"ANDRUS ON THE COVERED WALK FROM THE PRISON TO THE COURT  ·  {NA}", "B21": f"CHAPLAIN HENRY F. GERECKE, THE PRISON CHAPEL  ·  {NA}",
      "B22": f"CHAPLAIN GERECKE  ·  {NA}", "B23": f"DR. GUSTAVE GILBERT, PRISON PSYCHOLOGIST, WITH THE DEFENDANTS  ·  {NA}",
      "B24": f"GILBERT WITH THE DEFENDANTS DURING A RECESS  ·  {NA}",
      "C1": f"THE PALACE OF JUSTICE IN A RUINED CITY  ·  {NA}", "C2": f"NUREMBERG FROM THE AIR, 1945-46  ·  {NA}",
      "C3": f"THE COURTHOUSE ON FÜRTHER STRASSE  ·  {NA}", "C4": f"A TANK AT THE PALACE OF JUSTICE  ·  {NA}",
      "C5": f"ON GUARD FOR THE VERDICT DAYS, 30 SEP - 1 OCT 1946  ·  {NA}", "C6": f"THE GATE ON THE VERDICT DAYS, 1946  ·  {NA}",
      "C7": f"THE PRISON WHERE THE 21 WERE HELD  ·  {NA}", "C8": f"THE PRISON YARD  ·  {NA}",
      "C9": f"THE CELL BLOCK: CELLS OF GÖRING AND HESS AT FAR RIGHT  ·  {NA}", "C10": f"THE CELL BLOCK, A GUARD AT EVERY DOOR  ·  {NA}",
      "C11": f"A GUARD AT RUDOLF HESS'S DOOR  ·  {NA}", "C12": f"“TO THWART ANY ATTEMPT AT SUICIDE”  ·  {NA}",
      "C13": f"“WATCHFUL EYES AT GOERING CELL”  ·  {NA}", "C14": f"A DEFENDANT'S CELL  ·  {NA}", "C15": f"A DEFENDANT'S CELL  ·  {NA}",
      "C16": f"A CELL DOOR AND ITS PEEP HOLE  ·  {NA}", "C17": f"GÖRING'S TABLE, BUILT TO GIVE WAY  ·  {NA}",
      "C18": f"“LUNCH FOR GOERING”  ·  {NA}", "C19": f"THE PRISONERS' GLASSES, HANDED BACK EACH MORNING  ·  {NA}",
      "C20": f"THE DOCK, WATCHED BY A GUARD  ·  {NA}", "C21": "NUREMBERG IN RUINS, 1945  ·  U.S. ARMY AIR FORCES",
      "C22": "NUREMBERG BOMBED, FEB 1945  ·  U.S. ARMY AIR FORCES", "C23": "OSTFRIEDHOF CREMATORIUM, MUNICH (PHOTO 2009)  ·  RUFUS46, CC BY-SA 3.0",
      "E1": "PLAN OF NUREMBERG, c. 1930  ·  STADT NÜRNBERG / BnF", "E2": "CIA MAP OF GERMANY  ·  NATIONAL ARCHIVES",
      "E3": "NUREMBERG DAMAGE MAP, 12 FEB 1945  ·  STADT NÜRNBERG",
      "D1": "GÖRING TESTIFIES, MARCH 1946  ·  UNITED NEWS, NATIONAL ARCHIVES", "D5a": "VERDICT WEEK, OCT 1946  ·  UNIVERSAL NEWSREEL",
      "D5b": "THE COURTROOM, OCT 1946  ·  UNIVERSAL NEWSREEL", "D5c": "THE DOCK, OCT 1946  ·  UNIVERSAL NEWSREEL",
      "D6": "GÖRING JUST AFTER HIS SURRENDER, MAY 1945  ·  NATIONAL ARCHIVES"}
ILL = "ILLUSTRATIVE  ·  PEXELS"
for _r in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11"): TB[_r] = ILL
TB["F5"] = "CARTRIDGES LIKE THE ONE FOUND  ·  ILLUSTRATIVE, PEXELS"; TB["F2"] = "A PRISON CORRIDOR (NOT NUREMBERG)  ·  ILLUSTRATIVE, PEXELS"
def DT(rid):
    n = re.match(r"A(\d+)", rid).group(1)
    return {"1": "U.S. ARMY BOARD OF PROCEEDINGS: THE SUICIDE OF HERMANN GÖRING, 1946  ·  NATIONAL ARCHIVES",
            "2": "THE BOARD'S EXHIBIT LIST, 1946  ·  NATIONAL ARCHIVES", "3": "EXHIBIT “A”: THE CAPSULE, 1946  ·  NATIONAL ARCHIVES",
            "4": "THE CASE AND THE GLASS VIAL, ARMY LABORATORY PHOTO, 1946  ·  NATIONAL ARCHIVES",
            "5": "GÖRING TO THE COMMANDANT, 11 OCT 1946: THE ARMY'S ENGLISH COPY  ·  NATIONAL ARCHIVES",
            "6": "THE BOARD'S PLAN OF THE COURT ROOMS, 1946  ·  NATIONAL ARCHIVES", "7": "FOUR-POWER COMMISSION, TOP SECRET, 19 OCT 1946  ·  NATIONAL ARCHIVES",
            "8": "COL. ANDRUS, “DELIVERY TIME OF CONVICTS”, 17 OCT 1946  ·  NATIONAL ARCHIVES",
            "10": "THE SENTENCE, 1 OCT 1946  ·  TRIAL OF THE MAJOR WAR CRIMINALS, VOL. XXII", "11": "THE JUDGMENT, 1 OCT 1946  ·  TRIAL OF THE MAJOR WAR CRIMINALS, VOL. I",
            "12": "THE CUMBERLAND NEWS, WED 16 OCT 1946", "13": "GETTYSBURG TIMES, WED 16 OCT 1946"}.get(n, "U.S. ARMY RECORD  ·  NATIONAL ARCHIVES")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {}
LIFT = {}
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C10", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

SHOTS = [
 # COLD OPEN
 (0, KB("C13", z=(1.06, 1.16), c0=(0.5, 0.45))),                                  # frame 1: the guard at "H. GOERING"'s door
 ((0, "twenty|24"), KB("C12", z=(1.04, 1.14))),
 ((0, "about|two"), KB("B3", z=(1.08, 1.2), c0=(0.5, 0.4))),
 (1, TCARD("10:45 PM", "Tuesday, 15 October 1946  ·  Nuremberg prison", "C9")),
 (2, DOC("A10", [("death by hanging", (2, "sentenced|hang"))])),
 ((2, "hangings|set"), KB("C7", z=(1.0, 1.1))),
 (3, KB("C11", z=(1.05, 1.15))),
 ((3, "light"), KB("C14", z=(1.02, 1.12))),
 ((3, "hands|sleep"), KB("C16", z=(1.05, 1.15))),
 (4, KB("A4", z=(1.05, 1.25), c0=(0.5, 0.5), tag=None)),
 (5, KBP("A5", h=900)),
 ((5, "army|decided"), KBP("A1", h=900)),
 ((5, "four|claimed"), KB("B1", z=(1.05, 1.15), c0=(0.5, 0.45))),
 # WHO HE WAS / SENTENCED
 (6, VIDP("D6", at=2.0, h=600, bg="C21")),
 (7, KB("B17", z=(1.03, 1.12), c0=(0.5, 0.4))),
 ((7, "why|germany"), KB("C22", z=(1.0, 1.1), dim=0.35)),
 (8, VID("D1", at=83.0, crop=(0.0, 0.0, 1.0, 0.6), z=(1.0, 1.05))),                # witness box 1946 (seg 83-97 s; reporters cut off)
 (9, DOC("A11", [("enormity", (9, "unique|enormity"))])),
 (10, VIDP("D5c", at=18.0, h=600, bg="C1")),
 ((10, "sentences|death"), KB("B2", z=(1.06, 1.18), c0=(0.5, 0.4))),
 (11, KB("B15", z=(1.0, 1.1))),
 ((11, "shot"), DOC("A5", [("method of execution to shooting", (11, "shot"))])),
 (12, KB("C6", z=(1.0, 1.1))),
 (13, KB("B9", z=(1.05, 1.16), c0=(0.5, 0.45))),
 ((13, "remember"), DOC("A5", [((520, 650, 1400, 725), (13, "friday|eleventh"))], zoom=1.25)),
 # THE WATCHED MEN
 (14, KB("B18", z=(1.04, 1.14), c0=(0.5, 0.4))),
 (15, KB("C7", z=(1.05, 1.15), dim=0.2)),
 ((15, "less|weeks"), KB("C15", z=(1.03, 1.12), dim=0.15)),
 (16, KB("C9", z=(1.0, 1.12), c0=(0.6, 0.5))),
 (17, COUNTER([((17, "thirty|30"), "30 SEC")], "HOW OFTEN THE GUARD LOOKED IN", "C11", size=330)),
 (18, KB("C17", z=(1.04, 1.14))),
 ((18, "razors"), KB("C19", z=(1.0, 1.1))),
 (19, KB("C8", z=(1.0, 1.1))),
 ((19, "associated|count"), COUNTER([((19, "associated|count"), "~100")], "TIMES GÖRING WAS SEARCHED  ·  ASSOCIATED PRESS, 1946", "C10", size=330)),
 (20, KB("B19", z=(1.03, 1.13))),
 # THE LAST EVENING
 (21, KB("C10", z=(1.02, 1.12))),
 (22, TCARD("OCT 16", "In the papers since October 1st", "C5")),
 (23, KB("C8", z=(1.08, 1.18), c0=(0.45, 0.55))),
 (24, KB("B7", z=(1.04, 1.14))),
 (25, KB("C2", z=(1.0, 1.1), dim=0.35)),
 (26, KB("B21", z=(1.03, 1.13))),
 (27, KB("B22", z=(1.04, 1.14))),
 (28, KB("C15", z=(1.04, 1.12), dim=0.45)),
 (29, KB("C14", z=(1.06, 1.14), dim=0.4)),
 (30, KB("C1", z=(1.04, 1.16), c0=(0.5, 0.5))),
 ((30, "gymnasium|army"), KB("C8", z=(1.1, 1.2), c0=(0.6, 0.5), dim=0.2)),
 (31, KB("C7", z=(1.06, 1.16), dim=0.15)),
 ((31, "hold"), KB("F7", z=(1.04, 1.14))),
 # 10:45 PM
 (32, KB("C12", z=(1.08, 1.2))),
 ((32, "hatch"), KB("F4", z=(1.05, 1.15))),
 (33, KB("C16", z=(1.08, 1.2), dim=0.25)),
 (34, KB("C13", z=(1.14, 1.3), c0=(0.5, 0.45))),
 (35, KB("C10", z=(1.06, 1.14), dim=0.2)),
 (36, KB("C14", z=(1.1, 1.22), dim=0.45)),
 (37, TCARD("10:45 PM", "Hermann Göring is dead", "B3")),
 (38, KB("A4", z=(1.15, 1.35), c0=(0.55, 0.5))),
 (39, KB("A3", z=(1.05, 1.2), c0=(0.5, 0.45))),
 ((39, "rifle|cartridge"), KB("F5", z=(1.05, 1.15))),
 (40, DOC("A7", [("last letters", (40, "envelope|pencil")), ("Governor of the Prison", (40, "andrus|colonel"))])),
 (41, KB("B20", z=(1.04, 1.14))),
 (42, KBP("A12", crop=(0.0, 0.0, 1.0, 0.22), h=520)),
 # THE NOTE
 (43, DOC("A5", [((520, 650, 1400, 725), (43, "friday|eleventh"))], zoom=1.2)),
 (44, DOC("A5", [((520, 935, 2880, 1068), (44, "always|capsule"))])),
 (45, DOC("A5", [((520, 1000, 2880, 1068), (45, "three")), ((520, 1068, 2880, 1200), (45, "first|clothes"))])),
 (46, DOC("A5", [((520, 1333, 2880, 1466), (46, "court|sessions"))])),
 ((46, "riding|boots"), KB("B4", z=(1.04, 1.12), c0=(0.5, 0.6))),
 (47, DOC("A5", [((520, 1400, 2880, 1532), (47, "suitcase|third"))])),
 (48, DOC("A5", [((520, 1532, 2880, 1598), (48, "none|charged")), ((520, 1598, 2880, 1665), (48, "practically|impossible"))])),
 (49, KBP("A1", h=900)),
 (50, DOC("A2", [("Capsule", (50, "body|navel"))])),
 ((50, "toilet|rim"), KB("C15", z=(1.05, 1.15), dim=0.2)),
 (51, KB("C9", z=(1.04, 1.14))),
 (52, KB("B3", z=(1.1, 1.24), c0=(0.5, 0.4))),
 # FOUR CLAIMS
 (53, TCARD("1951", "A bar of soap", "B16")),
 (54, KB("B16", z=(1.02, 1.12))),
 (55, TCARD("1985", "A lieutenant and a gold watch", "C18")),
 ((55, "watch|gold"), KB("F7", z=(1.06, 1.16))),
 (56, TCARD("2005", "A fountain pen", "C11")),
 ((56, "medicine|carried"), KB("B13", z=(1.03, 1.12))),
 (57, KB("C20", z=(1.03, 1.13))),
 (58, TCARD("2026", "Six men knew?", "C10")),
 (59, KB("B16", z=(1.08, 1.16), dim=0.5)),
 (60, KB("B1", z=(1.06, 1.18), c0=(0.5, 0.4))),
 # 1:11 AM
 (61, KB("C8", z=(1.0, 1.12), dim=0.25)),
 (62, TCARD("1:11 AM", "Wednesday, 16 October 1946", "C7")),
 ((62, "joachim|ribbentrop"), KB("B15", z=(1.1, 1.2), c0=(0.62, 0.5))),
 (63, KB("C6", z=(1.03, 1.12))),
 (64, DOC("A8", [("18+19", (64, "one")), ("36+37", (64, "ten|brought"))])),
 (65, COUNTER([((65, "two|2"), "2:45 AM"), ((65, "hundred|103"), "103 MIN")], "THE TENTH MAN  ·  THE HANGMAN'S COUNT (TIME, 1946)", "C7", size=300)),
 (66, DOC("A8", [("38+40", (66, "two|fifty|54"))], zoom=1.15)),
 (67, KBP("A13", crop=(0.0, 0.0, 1.0, 0.2), h=380)),
 (68, KB("F11", z=(1.04, 1.14))),
 # MUNICH
 (69, NMAP(V_DE, [("pin", *NUREMBERG, "NUREMBERG", 0.2), ("route", [NUREMBERG, (11.4, 48.8), MUNICH], 0.8, 2.2), ("pin", *MUNICH, "MUNICH", 3.0), ("label", 11.9, 48.85, "ABOUT 95 MILES", 2.2, 28)], z=(1.25, 1.4), c0=(0.52, 0.56))),
 (70, KB("C23", z=(1.03, 1.12))),
 (71, KB("C21", z=(1.0, 1.1), dim=0.45)),
 (72, DOC("A7", [("TOP SECRET", (72, "sealed|control"))], zoom=1.1)),
 (73, KB("B18", z=(1.08, 1.18), c0=(0.5, 0.35), dim=0.15)),
 (74, KB("C14", z=(1.04, 1.12), dim=0.45)),
 ((74, "new|year"), TCARD("1 JAN 1958", "Dr. Douglas Kelley  ·  Berkeley, California", "C15")),
 # WHAT THE RECORD SHOWS + ASKS
 (75, KB("B3", z=(1.04, 1.12), c0=(0.5, 0.4))),
 (76, COUNTER([((76, "10|ten"), "10:45 PM"), ((76, "two|half"), "1:11 AM")], "HIS DEATH  →  THE FIRST MAN IN THE GYMNASIUM", "C9", size=300)),
 (77, KBP("A5", h=900)),
 (78, KB("B16", z=(1.04, 1.12), dim=0.3)),
 (79, KB("C13", z=(1.04, 1.12), c0=(0.5, 0.45))),
 (80, KB("C9", z=(1.04, 1.14), dim=0.3)),
 ((81, 0.0), ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "hookleft", ("100 SEARCHES.", "24 HOURS A DAY.")),                      # from frame 1 (LEAD = 0.8 s)
 (0, "about|two", "under", "DEAD 2 HOURS BEFORE HIS HANGING  ·  HOW?"),
 (2, 0.0, "badge", "TUE 1 OCT 1946"),
 (3, 0.2, "under", "A GUARD AT EVERY DOOR, DAY AND NIGHT"),
 (4, 0.2, "under", "THE ARMY'S OWN PHOTO, 1946"),
 (6, 0.0, "brand", None),                                          # the 2 s channel stamp, over moving footage, voice keeps going
 (6, 0.4, "nameplate", ("HERMANN GÖRING", "HITLER'S CHOSEN SUCCESSOR  ·  HEAD OF THE LUFTWAFFE")),
 (7, 0.0, "badge", "WED 25 JUL 1945"),
 (7, "why|germany", "quote", ("“Why did Germany declare war" + chr(10) + "on the United States?”", "MAJ. KENNETH HECHLER, U.S. ARMY HISTORIAN, 1945")),
 (8, 0.2, "typecenter", "“I WAS ASTONISHED.”"),
 (9, 0.0, "badge", "TUE 1 OCT 1946"),
 (11, 0.0, "typecenter", "11 SENTENCED TO HANG"),
 (12, 0.0, "badge", "THU 10 OCT 1946"),
 (13, "remember", "typecenter_red", "REMEMBER: FRI 11 OCT"),
 (14, 0.2, "nameplate", ("COL. BURTON C. ANDRUS", "COMMANDANT, NUREMBERG PRISON")),
 (15, 0.0, "badge", "OCT 1945"),
 (15, 0.3, "under", "LEONARDO CONTI  ·  6 OCT 1945  ·  NO PHOTO SHOWN"),
 (15, "less|weeks", "under", "ROBERT LEY  ·  OCT 1945  ·  NO PHOTO SHOWN"),
 (18, 0.2, "under", "THE TABLES WERE BUILT TO GIVE WAY"),
 (20, 0.0, "quote", ("“Just about impossible.”", "COL. ANDRUS, BEFORE THE NIGHT")),
 (21, 0.0, "badge", "MON 14 OCT 1946"),
 (23, 0.0, "badge", "TUE 15 OCT 1946"),
 (24, 0.2, "quote", ("“I have no fear, and will to the last" + chr(10) + "try to show dignity.”", "GÖRING, AS REPORTED BY THE DAILY TELEGRAPH, 16 OCT 1946")),
 (25, 0.0, "badge", "15 OCT  ·  5:26 PM"),
 (26, 0.0, "badge", "15 OCT  ·  8:00 PM"),
 (26, 0.3, "nameplate", ("HENRY F. GERECKE", "U.S. ARMY CHAPLAIN")),
 (27, "refuses", "stamp", ("REFUSED", 1260, 400)),
 (28, 0.0, "badge", "15 OCT  ·  9:00 PM"),
 (29, 0.0, "badge", "15 OCT  ·  ABOUT 10:00 PM"),
 (30, 0.4, "under", "THE PRISON GYMNASIUM: 35 YARDS FROM THE CELL BLOCK"),
 (31, "hold|back", "typecenter_red", "REMEMBER: 1:11 AM"),
 (32, 0.0, "badge", "15 OCT  ·  10:44 PM"),
 (33, 0.2, "under", "“NOT OBSERVED TO GO TO HIS MOUTH”  ·  AP, 1946"),
 (34, 0.2, "under", "“AN ODD NOISE”  ·  “TWITCH”  ·  COL. ANDRUS'S STATEMENT"),
 (38, 0.2, "under", "“PIECES OF GLASS IN HIS MOUTH”  ·  COL. ANDRUS"),
 (39, 0.3, "under", "A CASE MADE FROM A CARTRIDGE  ·  BRASS OR COPPER: REPORTS DIFFER"),
 (42, 0.0, "badge", "WED 16 OCT 1946"),
 (42, "baffled|completely", "quote", ("“I am completely baffled by it.”", "COL. ANDRUS, 16 OCT 1946")),
 (43, 0.0, "badge", "FRI 11 OCT 1946"),
 (49, 0.0, "badge", "SAT 26 OCT 1946"),
 (50, 0.0, "under", "THE COMMISSION'S GUESSES, NOT FACTS"),
 (51, 0.0, "typecenter", "NO GUARD TO BLAME"),
 (53, 0.0, "under", "MYTH OR RECORD: CLAIM 1"),
 (54, "only|evidence", "stamp", ("NEVER PROVED", 1240, 400)),
 (55, 0.3, "under", "MYTH OR RECORD: CLAIM 2  ·  BEN SWEARINGEN'S BOOK, 1985"),
 (56, 0.3, "under", "MYTH OR RECORD: CLAIM 3  ·  LOS ANGELES TIMES, 2005"),
 (57, "nothing|checked", "stamp", ("UNVERIFIED", 1240, 400)),
 (58, 0.3, "under", "MYTH OR RECORD: CLAIM 4  ·  PAUL HOOLEY'S BOOK, 2026"),
 (59, 0.0, "list", ("A BAR OF SOAP", "A LIEUTENANT", "A FOUNTAIN PEN", "SIX MEN")),
 (60, 0.2, "stamp", ("NONE PROVED", 1240, 400)),
 (60, 1.8, "subpop", None),                                         # silent ask at ~72%, right after the payoff (LESSONS 37)
 (62, 0.0, "badge", "WED 16 OCT  ·  1:11 AM"),
 (62, "joachim|ribbentrop", "under", "JOACHIM VON RIBBENTROP, FRONT ROW, THIRD FROM LEFT"),
 (63, 0.2, "under", "8 REPORTERS: 2 FROM EACH OF THE 4 POWERS, CHOSEN BY LOT"),
 (65, 0.0, "badge", "16 OCT  ·  2:45 AM"),
 (66, 0.0, "badge", "16 OCT  ·  2:54 AM"),
 (66, "stretcher|carry", "under", "COL. ANDRUS'S MEMO, 17 OCT 1946  ·  NO PHOTOGRAPHS SHOWN"),
 (68, 0.0, "badge", "16 OCT  ·  3:00 AM"),
 (69, 0.0, "badge", "WED 16 OCT 1946"),
 (70, 0.0, "badge", "THU 17 OCT 1946"),
 (70, "creek|small", "under", "A SMALL CREEK IN MUNICH  ·  STARS AND STRIPES, 1947"),
 (73, 0.0, "badge", "DEC 1946"),
 (74, 0.0, "badge", "1 JAN 1958"),
 (74, 0.3, "under", "DR. DOUGLAS KELLEY, ARMY PSYCHIATRIST  ·  NO SAFE PHOTO"),
 (75, 0.0, "typecenter", "WHAT THE RECORD SHOWS"),
 (78, "proved|right", "stamp", ("NONE PROVED", 1240, 400)),
 (79, 0.2, "under", "HID IT 17 MONTHS, OR HANDED IT?  TELL ME BELOW"),
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
        if kind == "subpop":                                           # the silent subscribe ask runs its full 4 s across shot cuts
            if t0 <= t < t0 + 4.0: ov_extra(c, kind, a, t, t0)
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
    elif kind == "brand":                                      # 2 s channel stamp over moving footage: no spoken ident, no pause
        u = t - t0
        if u < 2.2:
            al = ease(u / 0.35) * ease((2.2 - u) / 0.35)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, H / 2 - 150, W, H / 2 + 150), fill=(0, 0, 0, int(150 * al))); c.alpha_composite(lay)
            L.text(c, "the", W / 2, H / 2 - 95, 52, STEEL, SER, alpha=al); L.text(c, "LAST HOURS", W / 2, H / 2 + 5, 150, BONE, COND, alpha=al)
            L.text(c, "FILE 13  ·  NUREMBERG  ·  OCTOBER 1946", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
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
CAPFIX = {"Goering": "Göring", "Goering's": "Göring's", "Goring": "Göring", "Goring's": "Göring's", "Gurring": "Göring", "Gowering": "Göring",
          "Gharing": "Göring", "Garing": "Göring", "Herman": "Hermann", "Erman": "Hermann", "Andris": "Andrus", "Andress": "Andrus", "Andras": "Andrus",
          "Lye": "Ley", "Geraki": "Gerecke", "Gheriki": "Gerecke", "Gerecky": "Gerecke", "Kelly": "Kelley", "10.45": "10:45", "5.26": "5:26",
          "1.11": "1:11", "2.57": "2:57", "2.45": "2:45", "2.54": "2:54", (82, "everyone"): "every one", "gowering": "Göring", "goering": "Göring", "goring": "Göring", "gurring": "Göring", (34, "Twitch"): "twitch", (62, "Your"): "", (62, "Kim"): "Joachim"}  # whisper spellings -> the record's (core word; punctuation kept; "" drops it)
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
        c = L.vignette(L.kenburns(blur_bg("C9", None), t, t0, t1))
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
    music("Thunder Dreams.mp3", 0.0, tl(6), -11, later=(tl(4), -15)); music("Industrial Cinematic.mp3", tl(6), tl(21), -17); music("Man Down.mp3", tl(21), tl(32), -17)
    music("Rising Tide.mp3", tl(32), tl(43), -17); music("Thunder Dreams.mp3", tl(43), tl(53), -18); music("Industrial Cinematic.mp3", tl(53), tl(61), -17)
    music("Man Down.mp3", tl(61), tl(75), -18); music("Promises to Keep.mp3", tl(75), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(6), -30); loop("ambience_cinematic_suspense", tl(28), tl(37), -31); loop("wind_cold_interior", tl(61), tl(69), -33)
    loop("wind_deep_cinematic_hum", tl(69), tl(75), -31)
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
    EV = [(0, "dead|about", "heartbeat_single", -18), (4, "glass", "hit_short_bass", -18), (8, 0.0, "typewriter_return_bell", -22),
          (10, "death|hanging", "hit_deep_heartbeat_impact", -20), (15, 0.0, "heavy_sliding_door", -26), (17, "thirty|30", "clock_tick_single", -16),
          (19, "hundred|100", "hit_short_bass", -18), (28, 0.0, "heavy_sliding_door", -28), (31, "basketball", "hit_short_bass", -22),
          (34, "noise|odd", "heartbeat_single", -16), (37, 0.0, "hit_cinematic_deep_impact", -14), (38, "glass", "hit_short_bass", -18),
          (44, 0.0, "paper_big_page_turn", -20), (45, "three", "hit_short_bass", -20), (52, "only|answer", "hit_cinematic_deep_impact", -16),
          (61, 0.0, "heavy_sliding_door", -24), (62, "eleven|one", "clock_tick_single", -14), (65, "two|fifty", "clock_tick_single", -14),
          (66, "stretcher", "hit_deep_heartbeat_impact", -20), (71, 0.0, "wind_cold_interior", -30), (75, 0.0, "hit_cinematic_deep_impact", -15),
          (82, 1.0, "typewriter_return_bell", -18)]
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
    name = name or "TheLastHours_13_GoeringLastNight.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "A hundred searches"), (6, "Sentenced to hang"), (14, "The watched men"), (21, "The last evening"),
      (32, "10:45 p.m."), (43, "His own note"), (53, "Four men, four answers"), (61, "1:11 a.m."), (69, "A creek in Munich"),
      (75, "What the record shows")]

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

