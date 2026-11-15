"""The Last Hours #27: Saddam Hussein's last day, Baghdad, Friday 29 - Sunday 31 December 2006 (about 11:55 p.m. Maliki signs; 1:30 a.m.
fourteen phones ring; LZ Washington, the phones taken; Camp Cropper to Kadhimiya by Black Hawk; 5:30 a.m. Iraq takes full custody; the small
room; 6 a.m. the corridor, the Koran; about 6:10 a.m. the sentence carried out (one line, no images); two videos; the coffin north to Awja),
framed by the Dujail case (8 July 1982; Decree 778, 16 June 1984). The File Keeper, colour grade, 1920x1080, burned-in captions, film finish.
Real images only: DoD / US Army / White House (PD), CIA / NIMA / MND-B maps (PD), file 11's vetted Baghdad set, Pexels textures labelled
ILLUSTRATIVE. Never shown: the execution, the gallows, the rope, either video or stills from them, the body, any woman.
  uv run --no-project --with pillow --with numpy --with soundfile python render_lastday27.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
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

ROOT = "D:/why habibi/_newchannel/27_saddam_last_day/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 5.0                                   # the File Keeper end card runs under the sign-off
NEXT = os.environ.get("LH_NEXT", "")
ENDL = 85                                                # the File Keeper sign-off line (the end card runs under it)                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/lastday_vo_chatterbox.wav")
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
def isdoc(rid): return re.fullmatch(r"A\d+p\d+", rid) is not None or rid in ()     # document pages stay paper-toned
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

# Natural-Earth maps (mshorts VMap): (lon centre, lat centre, degrees wide)
V_GULF, V_SIRTE, V_AFRICA = (16.8, 31.9, 8.5), (16.55, 31.2, 0.45), (17.0, 3.0, 78.0)

# ------------------------------------------------------------------ shot constructors
CROP = {"C13": (0.0, 0.0, 1.0, 0.55), "C16": (0.0, 0.0, 0.7, 1.0)}             # C13: city + domes only, never the pilgrims on the bridge; C16: no pedestrians
DOD, ARMY, ILL = "U.S. DEPARTMENT OF DEFENSE", "U.S. ARMY", "ILLUSTRATIVE  ·  PEXELS"
TB = {"B1": f"SADDAM HUSSEIN AT HIS FIRST HEARING, BAGHDAD, 1 JUL 2004  ·  {DOD}", "B3": f"THE HEARING ROOM, 1 JUL 2004  ·  {DOD}",
      "B5": f"SADDAM HUSSEIN, DEC 2003  ·  {DOD}", "B7": f"SADDAM HUSSEIN AFTER HIS CAPTURE, DEC 2003  ·  {DOD}",
      "B8": f"MOWAFFAK AL-RUBAIE, IRAQ'S NATIONAL SECURITY ADVISER, 2006  ·  {DOD}", "B9": "NOURI AL-MALIKI, BAGHDAD, 13 JUN 2006  ·  THE WHITE HOUSE",
      "B10": "NOURI AL-MALIKI, 30 NOV 2006  ·  THE WHITE HOUSE", "B11": "ZALMAY KHALILZAD, US AMBASSADOR TO IRAQ, 2005  ·  U.S. AIR FORCE",
      "B12": f"MAJ. GEN. WILLIAM CALDWELL, BAGHDAD, 2007  ·  {ARMY}", "B13": "PRESIDENT BUSH, CRAWFORD, TEXAS, AUG 2006  ·  THE WHITE HOUSE",
      "B14": "PRESIDENT BUSH AND STEPHEN HADLEY, THE WHITE HOUSE, 2006  ·  THE WHITE HOUSE", "B16": "CHIEF JUDGE RAOUF ABDEL RAHMAN, IHT, MAY 2006  ·  FORCE2006, CC BY-SA 4.0",
      "C1": f"CAMP CROPPER, BAGHDAD, 2010  ·  {ARMY}", "C2": f"CAMP CROPPER, BAGHDAD, 2010  ·  {ARMY}", "C5": f"CAMP CROPPER, BAGHDAD, 2010  ·  {ARMY}",
      "C7": f"CAMP CROPPER, BAGHDAD, 2010  ·  {ARMY}", "C8": f"A BLACK HAWK OVER BAGHDAD AT SUNSET, 2005  ·  {ARMY}",
      "C9": f"BOARDING A BLACK HAWK AT NIGHT, BAGHDAD, 2009  ·  {ARMY}", "C10": f"A BLACK HAWK OVER BAGHDAD, 2009  ·  {ARMY}",
      "C13": f"KADHIMIYA, BAGHDAD, FROM THE AIR, 2008  ·  {DOD}", "C14": "THE REPUBLICAN PALACE, BAGHDAD, 2007  ·  JIM.GORDON, CC BY 2.0",
      "C16": "THE REPUBLICAN PALACE, GREEN ZONE, 2010  ·  JIM.GORDON, CC BY 2.0", "C19": "THE TIGRIS THROUGH BAGHDAD, 2016  ·  DOD PHOTO, PO2 D. A. PINEIRO",
      "C20": "SADDAM'S PALACE ABOVE THE TIGRIS, TIKRIT, 2003  ·  LOOPER5920, PD", "C21": f"AWJA, NEAR TIKRIT, 2006  ·  {ARMY}",
      "C22": f"DUJAIL, 2008  ·  {ARMY}", "C23": "THE GATES OF TIKRIT, 2004  ·  J. A. BACKOWSKI II, CC BY-SA 4.0", "C25": "A SADDAM MURAL, BAGHDAD, 2009  ·  ROBERTJALBERTS, CC BY-SA 3.0",
      "C26": "A SMASHED SADDAM PORTRAIT, BAGHDAD, 2003-04  ·  PETER RIMAR, PD", "A3": "DISTRICTS OF BAGHDAD  ·  PD",
      "R16": "ILLUSTRATIVE  ·  A SADDAM-ERA ROOM, NOT THE ACTUAL ROOM"}
for _r in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18"): TB[_r] = ILL
def DT(rid):
    m = re.match(r"(A\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD, 2006")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None, x=0.5): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid), x=x))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {}
LIFT = {'E7': 0.8, 'E14': 0.7, 'E17': 0.9, 'E8': 0.85}                     # gamma: below 1 lifts the dark clips (LESSONS 34)
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C10", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

BAGHDAD, DUJAIL, KADH, CROPPER = (44.366, 33.315), (44.24, 33.84), (44.338, 33.38), (44.23, 33.27)            # research/research.md (±2 km)
TIKRIT, AWJA, SPEICHER = (43.679, 34.607), (43.67, 34.53), (43.53, 34.67)
V_IRAQ, V_BAGHDAD = (43.9, 34.0, 6.0), (44.3, 33.35, 0.55)
SHOTS = [
 # COLD OPEN
 (0, VID("E13", at=0.0)),                                                                            # frame 1: a clock turning past midnight
 ((0, "voice|prime"), VID("E7", at=2.0, dim=0.15)),
 ((0, "execution"), KBP("B1", crop=(0.0, 0.0, 1.0, 0.92), h=860, rot=-1.0)),
 ((0, "nobody|room"), KB("C14", z=(1.04, 1.14), dim=0.25)),
 (1, TCARD("1:30 AM", "Saturday, 30 December 2006", "A3")),
 (2, KBP("B1", crop=(0.0, 0.0, 1.0, 0.92), h=880, rot=1.0)),
 (3, KB("C1", z=(1.03, 1.12))),
 ((3, "hand|over"), VID("E2", at=2.0)),
 (4, KB("C13", z=(1.04, 1.14))),
 ((4, "carried|hands"), VID("E16", at=3.0)),
 ((4, "videos"), VID("E18", at=0.0)),
 # DUJAIL, 1982
 (5, VID("E17", at=0.0)),
 (6, NMAP(V_IRAQ, ops=[("pin", *BAGHDAD, "BAGHDAD", 0.1), ("pin", *DUJAIL, "DUJAIL  ·  8 JULY 1982", 0.6)])),
 ((6, "survives"), KB("C22", z=(1.03, 1.12))),
 (7, KB("C22", z=(1.12, 1.25), c0=(0.55, 0.5), dim=0.15)),
 (8, KB("C25", z=(1.03, 1.12))),
 ((8, "hundred|forty"), COUNTER([((8, "hundred|forty"), "148")], "MEN AND BOYS FROM DUJAIL, REFERRED TO THE REVOLUTIONARY COURT  ·  MAY 1984", "C22", size=420)),
 (9, TCARD("DECREE 778", "16 June 1984", "C25")),
 (10, COUNTER([((10, "forty-six|46"), "46 OF 148")], "ALREADY DEAD IN CUSTODY BEFORE THEY REACHED COURT  ·  HRW, FROM THE TRIAL FILE", "C22", size=360)),
 (11, KB("C26", z=(1.04, 1.14), dim=0.2)),
 # THE COURT
 (12, KBP("B7", crop=(0.0, 0.0, 0.93, 0.93), h=860, rot=-1.0)),
 (13, KB("C2", z=(1.03, 1.12))),
 ((13, "airport"), NMAP(V_BAGHDAD, ops=[("pin", *CROPPER, "CAMP CROPPER  ·  NEAR THE AIRPORT", 0.2)])),
 (14, KB("B3", z=(1.03, 1.12), c0=(0.35, 0.5))),
 ((14, "dujail"), KBP("B1", crop=(0.0, 0.0, 1.0, 0.92), h=840, rot=1.0)),
 (15, KBP("B11", h=780, rot=-1.0)),
 (16, KBP("B16", h=860, rot=1.0)),
 ((16, "humanity|hanging"), KB("B3", z=(1.12, 1.25), c0=(0.3, 0.55))),
 # THE APPEAL
 (17, TCARD("TUE 26 DEC", "The appeal is rejected", "C14")),
 (18, KB("C26", z=(1.05, 1.15), dim=0.2)),
 (19, COUNTER([((19, "four"), "30 → 4")], "DAYS ALLOWED  ·  DAYS TAKEN", "C14", size=380)),
 (20, VID("E18", at=4.0)),
 (21, KB("C5", z=(1.04, 1.12), dim=0.2)),
 # FRIDAY
 (22, TCARD("FRI 29 DEC", "The Iraqi government wants it done", "C14")),
 (23, KB("C1", z=(1.05, 1.15), c0=(0.6, 0.5))),
 (24, KB("C16", z=(1.03, 1.1))),
 (25, KB("B14", z=(1.03, 1.1), dim=0.15)),
 (26, KBP("B8", h=820, rot=-1.0)),
 (27, VID("E3", at=2.0)),
 (28, KB("C14", z=(1.1, 1.2), c0=(0.5, 0.45), dim=0.3)),
 (29, VID("E13", at=1.5)),
 ((29, "maliki"), KBP("B9", h=840, rot=1.0)),
 # 1:30 AM
 (30, TCARD("1:30 AM", "Fourteen phones ring", "A3")),
 ((30, "fourteen|phones"), VID("E7", at=8.0)),
 (31, KB("B3", z=(1.25, 1.4), c0=(0.7, 0.5), dim=0.2)),
 (32, NMAP(V_BAGHDAD, ops=[("pin", *BAGHDAD, "LZ WASHINGTON  ·  GREEN ZONE", 0.2), ("pin", *CROPPER, "CAMP CROPPER", 0.8), ("pin", *KADH, "KADHIMIYA", 1.4)])),
 ((32, "washington"), KB("C14", z=(1.04, 1.14))),
 (33, VID("E11", at=2.0)),
 (34, KB("C9", z=(1.03, 1.12))),
 (35, VID("E12", at=3.0)),
 # CAMP CROPPER
 (36, KB("C7", z=(1.03, 1.12))),
 (37, VID("E8", at=4.0)),
 (38, KB("C9", z=(1.15, 1.28), c0=(0.55, 0.55))),
 ((38, "ten|miles"), NMAP(V_BAGHDAD, ops=[("pin", *CROPPER, "CAMP CROPPER", 0.1), ("route", [CROPPER, (44.29, 33.33), KADH], 0.4, 1.6), ("pin", *KADH, "KADHIMIYA  ·  ~10 MILES", 1.8)])),
 (39, KB("C13", z=(1.03, 1.12))),
 ((39, "justice"), KB("C10", z=(1.04, 1.12))),
 (40, VID("E15", at=3.0)),
 (41, TCARD("5:30 AM", "Iraq takes full custody", "C13")),
 (42, COUNTER([((42, "thousand|1,113"), "1,113 DAYS")], "IN AMERICAN HANDS  ·  13 DEC 2003 → 30 DEC 2006", "C8", size=340)),
 # THE SMALL ROOM
 (43, KB("R16", z=(1.04, 1.12), dim=0.35)),
 (44, KBP("B1", crop=(0.0, 0.0, 1.0, 0.92), h=860, rot=-1.0)),
 (45, KB("B3", z=(1.2, 1.35), c0=(0.68, 0.45), dim=0.15)),
 (46, KBP("B11", h=760, rot=1.0)),
 (47, KB("B3", z=(1.03, 1.12), c0=(0.4, 0.5))),
 (48, KBP("B1", crop=(0.0, 0.0, 1.0, 0.92), h=840, rot=1.0)),
 (49, KB("C19", z=(1.03, 1.1), dim=0.35)),
 # THE KORAN
 (50, TCARD("6:00 AM", "A corridor of witnesses", "C13")),
 (51, KBP("B8", h=820, rot=-1.0)),
 (52, KBP("B1", crop=(0.0, 0.0, 1.0, 0.92), h=860, rot=1.0)),
 (53, VID("E16", at=6.0)),
 (54, VID("E16", at=14.0)),
 (55, VID("E8", at=12.0)),
 # SOMETHING CHANGED
 (56, VID("E17", at=0.5)),
 (57, KB("C26", z=(1.1, 1.22), dim=0.3)),
 (58, VID("E18", at=6.0)),
 (59, VID("E11", at=8.0)),
 # 6:10 AM: one line, no images of the act
 (60, VID("E14", at=0.5)),
 (61, VID("E8", at=18.0)),
 (62, VID("E18", at=8.0)),
 (63, VID("E14", at=2.5)),
 (64, VID("E17", at=1.0)),
 (65, TCARD("~6:10 AM", "Saturday, 30 December 2006", "C13")),
 (66, KB("B13", z=(1.03, 1.1), dim=0.2)),
 (67, VID("E9", at=2.0)),
 ((67, "eid|holiday"), VID("E10", at=3.0)),
 # TWO VIDEOS
 (68, VID("E18", at=0.0)),
 (69, VID("E18", at=2.0, dim=0.3)),
 (70, VID("E7", at=12.0)),
 (71, KB("B12", z=(1.03, 1.12), c0=(0.55, 0.45))),
 (72, KB("B14", z=(1.05, 1.15), c0=(0.6, 0.6))),
 (73, KB("B13", z=(1.1, 1.2), c0=(0.5, 0.6))),
 # AWJA
 (74, VID("E2", at=8.0)),
 (75, VID("E4", at=10.0)),
 ((75, "hundred|ten"), NMAP(V_IRAQ, ops=[("pin", *BAGHDAD, "BAGHDAD", 0.1), ("route", [BAGHDAD, (44.0, 34.0), SPEICHER], 0.4, 1.8), ("pin", *SPEICHER, "CAMP SPEICHER  ·  110 MILES", 2.0), ("pin", *AWJA, "AWJA", 2.6)])),
 (76, KB("C21", z=(1.03, 1.12))),
 ((76, "hall|hometown"), KB("C20", z=(1.03, 1.12))),
 (77, KB("C23", z=(1.03, 1.1), dim=0.2)),
 (78, VID("E15", at=8.0)),
 # WHAT THE RECORD KEEPS
 (79, KB("C13", z=(1.03, 1.1), dim=0.3)),
 (80, KB("C22", z=(1.04, 1.12), dim=0.2)),
 (81, VID("E8", at=1.0)),
 ((81, "fourteen|phones"), VID("E11", at=10.0)),
 (82, VID("E16", at=10.0)),
 (83, VID("E18", at=3.0)),
 (84, VID("E14", at=4.0)),
 (85, KB("C8", z=(1.03, 1.1))),
 ((ENDL, -0.7), ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "hookleft", ("1:30 AM. A PHONE RINGS.", "BE THERE AT 3:30.")),
 (0, "nobody|room", "under", "WHAT HAPPENED IN THAT ROOM?"),
 (1, 0.0, "badge", "SAT 30 DEC 2006"),
 (1, "york", "under", "NEW YORK: 5:30 PM, FRIDAY"),
 (3, 0.3, "under", "HELD BY US FORCES  ·  CAMP CROPPER"),
 (4, 0.2, "under", "WHY SO FAST  ·  WHO WAS THERE  ·  WHAT HE CARRIED  ·  TWO VIDEOS"),
 (4, "videos", "under", "NO IMAGES OF THE EXECUTION ARE SHOWN IN THIS FILE"),
 (5, 0.0, "brand", None),
 (6, 0.0, "badge", "THU 8 JUL 1982"),
 (7, 0.3, "under", "THE PROSECUTION'S CASE  ·  AS SUMMARISED BY HUMAN RIGHTS WATCH"),
 (8, 0.0, "badge", "SUN 27 MAY 1984"),
 (9, 0.0, "badge", "THU 14 JUN 1984"),
 (12, 0.0, "badge", "SAT 13 DEC 2003"),
 (14, 0.0, "badge", "WED 19 OCT 2005"),
 (15, 0.3, "under", "ZALMAY KHALILZAD, US AMBASSADOR"),
 (16, 0.0, "badge", "SUN 5 NOV 2006"),
 (16, "verdict", "nameplate", ("JUDGE RAOUF ABDEL RAHMAN", "CHIEF JUDGE, IRAQI HIGH TRIBUNAL")),
 (17, 0.0, "badge", "TUE 26 DEC 2006"),
 (18, "exceed|thirty", "quote", ("“It cannot exceed 30 days.”", "JUDGE AREF SHAHEEN, IHT APPEALS CHAMBER, 26 DEC 2006")),
 (20, 0.0, "badge", "WED 27 DEC 2006"),
 (21, 0.0, "badge", "THU 28 DEC 2006"),
 (22, 0.0, "badge", "FRI 29 DEC 2006"),
 (23, "legal|physical", "quote", ("“…legal custody … physical custody of him" + chr(10) + "until before the execution…”", "U.S. DEPARTMENT OF DEFENSE, 29 DEC 2006")),
 (24, "talabani", "nameplate", ("JALAL TALABANI", "PRESIDENT OF IRAQ  ·  NO PHOTO USED")),
 (25, 0.3, "under", "U.S. DISTRICT COURT, WASHINGTON  ·  STAY DENIED"),
 (26, "adviser|security", "nameplate", ("MOWAFFAK AL-RUBAIE", "IRAQ'S NATIONAL SECURITY ADVISER")),
 (26, "responsibility", "under", "US DIPLOMATIC CABLE 07BAGHDAD146  ·  LATER PUBLISHED BY WIKILEAKS"),
 (28, "execute|you", "quote", ("“Who is going to execute him, anyway, you or us?”", "AS ONE IRAQI PARTICIPANT RECALLED IT  ·  THE NEW YORK TIMES")),
 (29, 0.2, "badge", "FRI 29 DEC  ·  ~11:55 PM"),
 (29, "maliki", "nameplate", ("NOURI AL-MALIKI", "PRIME MINISTER OF IRAQ")),
 (30, 0.0, "badge", "SAT 30 DEC  ·  1:30 AM"),
 (31, "haddad", "nameplate", ("JUDGE MUNIR HADDAD", "IRAQI HIGH TRIBUNAL  ·  NO PHOTO USED")),
 (31, "come", "quote", ("“Come to the prime minister's office at 3:30…”", "THE CALL, AS JUDGE HADDAD RECALLED IT  ·  THE WASHINGTON POST")),
 (32, 0.0, "badge", "~3:30 AM"),
 (33, "phones", "typecenter_red", "EVERY PHONE TAKEN"),
 (34, 0.2, "under", "2 HELICOPTERS  ·  7 MEN IN EACH"),
 (35, "end", "typecenter", "THAT SHOULD HAVE BEEN THE END OF IT"),
 (36, 0.3, "under", "CAMP CROPPER  ·  US DETENTION CENTER"),
 (37, 0.3, "list", ("A LONG BLACK COAT", "A WHITE SHIRT", "A WOOL CAP, A SCARF")),
 (37, 0.2, "under", "ILLUSTRATIVE"),
 (39, "justice", "under", "THE FORMER MILITARY INTELLIGENCE HQ  ·  “CAMP JUSTICE”"),
 (40, 0.3, "under", "“VIDEO PERSONNEL AND PSD”  ·  US DIPLOMATIC CABLE"),
 (41, 0.0, "badge", "SAT 30 DEC  ·  5:30 AM"),
 (43, 0.3, "list", ("A DESK", "A FEW CHAIRS", "A REFRIGERATOR")),
 (43, 0.2, "under", "ILLUSTRATIVE  ·  NOT THE ACTUAL ROOM"),
 (45, "normal|afraid", "quote", ("“He seemed normal, not confused nor afraid.”", "JUDGE MUNIR HADDAD  ·  THE WASHINGTON POST")),
 (46, "faroon", "nameplate", ("MUNQITH AL-FAROON", "DEPUTY PROSECUTOR  ·  NO PHOTO USED")),
 (46, "shaking", "under", "HIS ACCOUNT TO THE US AMBASSADOR  ·  CABLE 07BAGHDAD146"),
 (48, "voice|higher", "quote", ("“My voice was higher than his.”", "JUDGE MUNIR HADDAD")),
 (50, 0.0, "badge", "SAT 30 DEC  ·  6:00 AM"),
 (52, "afraid|path", "quote", ("“I am not afraid. I have chosen this path.”", "SADDAM HUSSEIN, AS JUDGE HADDAD RECALLED IT")),
 (53, 0.3, "under", "ILLUSTRATIVE  ·  NOT HIS KORAN"),
 (54, "bandar", "nameplate", ("AWAD AL-BANDAR", "THE JUDGE WHO SENTENCED DUJAIL, 1984")),
 (55, "keep", "quote", ("“Keep it until you meet with any of my family members.”", "SADDAM HUSSEIN  ·  THE WASHINGTON POST")),
 (56, 0.2, "typecenter_red", "THEN SOMETHING CHANGED"),
 (58, "pictures|phones", "typecenter_red", "TWO PHONES, RAISED"),
 (59, 0.2, "typecenter", "SOMEBODY HAD NOT"),
 (62, "real|men", "quote", ("“Is this how real men behave?”", "SADDAM HUSSEIN, ON THE PHONE VIDEO  ·  THE NEW YORK TIMES")),
 (63, "facing", "quote", ("“The man is facing execution. Please don't.”", "THE DEPUTY PROSECUTOR  ·  THE WASHINGTON POST")),
 (65, 0.0, "badge", "SAT 30 DEC  ·  ~6:10 AM"),
 (66, 0.0, "badge", "10:10 PM FRIDAY IN NEW YORK"),
 (67, 0.0, "badge", "SUNRISE 7:05 AM"),
 (68, 0.2, "typecenter", "TWO VIDEOS"),
 (69, 0.3, "under", "NOT SHOWN  ·  NO STILLS FROM EITHER VIDEO"),
 (71, "caldwell", "nameplate", ("MAJ. GEN. WILLIAM CALDWELL", "US MILITARY SPOKESMAN, BAGHDAD")),
 (71, "differently", "quote", ("“We, as a coalition force," + chr(10) + "would have done it differently.”", "MAJ. GEN. WILLIAM CALDWELL, 3 JAN 2007")),
 (72, "dignified", "quote", ("“…a more dignified way.”", "PRESIDENT BUSH, 4 JAN 2007")),
 (73, "revenge", "quote", ("“…kind of a revenge killing.”", "PRESIDENT BUSH, 16 JAN 2007")),
 (73, 0.3, "subpop", None),                                        # the File Keeper case tab (~80%)
 (74, 0.0, "badge", "SAT 30 - SUN 31 DEC"),
 (75, 0.3, "under", "ILLUSTRATIVE"),
 (76, 0.0, "badge", "SUN 31 DEC  ·  BEFORE DAWN"),
 (77, 0.0, "badge", "MON 15 JAN 2007"),
 (78, 0.2, "typecenter", "HIS GRAVE: UNKNOWN TODAY"),
 (79, 0.0, "typecenter", "WHAT THE RECORD KEEPS"),
 (80, 0.3, "list", ("DECREE 778  ·  1984", "148 NAMES")),
 (81, 0.3, "list", ("~11:55 PM  ·  A SIGNATURE", "1:30 AM  ·  14 PHONES")),
 (83, 0.2, "typecenter", "ONE WENT QUIET. ONE DIDN'T."),
 (84, 0.2, "listL", ("30 DAYS ALLOWED.", "4 TAKEN.", "TELL ME WHAT YOU THINK")),
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

SLOT = {"hookleft": "center", "lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "listL": "center", "quoteL": "center", "quoteR": "center"}
OVT = [OT(ln, off) for ln, off, _, _ in OV]
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    end = shot_t1                                  # the EARLIEST later overlay in the slot wins, whatever its list order
    for j2 in range(len(OV)):
        if OVT[j2] <= OVT[j] or j2 == j: continue
        k2 = OV[j2][2]
        if SLOT.get(k2) == sl or (sl == "bottom" and k2 in ("list", "typecenter", "typecenter_red", "quote", "listL", "quoteL", "quoteR")):
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
        elif kind in ("list", "listL"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay); sz = 74 if max(len(s) for s in a) < 24 else 58
            if kind == "listL": sz = min(sz, 52)
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W * (0.29 if kind == "listL" else 0.5), H / 2 - (len(a) - 1) * 60 + i * 120, size=sz, cps=20, anchor="mm", cursor=False)
        elif kind == "stamp": L.stamp(c, a[0], a[1], a[2], t, t0, size=100)
        elif kind in ("quote", "quoteL", "quoteR"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay); qs = a[0].split("\n"); qx = W * {"quoteL": 0.30, "quoteR": 0.74}.get(kind, 0.5)
            for i, q in enumerate(qs):
                L.text(c, q, qx, H / 2 - 40 - (len(qs) - 1) * 42 + i * 84, 44 if kind in ("quoteL", "quoteR") else (50 if NO_BOTTOM and len(q) > 44 else 60), BONE, SER, alpha=ease((t - t0 - 0.25 * i) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, qx, H / 2 + 60 + (len(qs) - 1) * 42, size=34, fill=STEEL, cps=34, anchor="mm", cursor=False)
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
        if t - t0 < BA.STAMP_LEN: c.alpha_composite(BA.stamp_frame(t - t0, BP.LABEL["lastday27"]))
    elif kind == "hookleft":                                   # frame-1 hook text in thumbnail blocks, left, off the face
        f = L.font(COND, 132); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i, s in enumerate(a):
            y = H / 2 - 130 + i * 180; w = f.getlength(s)
            d.rectangle((80, y - 82, 80 + w + 56, y + 82), fill=((0, 0, 0, 230) if i == 0 else (255, 204, 0, 255)))
            d.text((108, y), s, font=f, fill=(BONE + (255,)) if i == 0 else (10, 10, 10, 255), anchor="lm")
        c.alpha_composite(lay)
    elif kind == "subpop":                                     # the File Keeper case tab (no ask: the spoken mid ask does that)
        if t - t0 < BA.PILL_LEN: c.alpha_composite(BA.chip_frame(t - t0, BP.LABEL["lastday27"]), (0, BP.PILL_Y))

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
CAPFIX = {'Dujayl': 'Dujail', 'Doojail': 'Dujail', 'Doo-jail': 'Dujail', 'Kadhimiyah': 'Kadhimiya', 'Khadimiya': 'Kadhimiya', 'Kazimiya': 'Kadhimiya', 'Faroun': 'al-Faroon', 'Farun': 'al-Faroon', 'Bander': 'al-Bandar', 'Bandar': 'al-Bandar', 'Maleki': 'al-Maliki', 'Talibani': 'Talabani', 'Moqtada': 'Muqtada', 'Mukhtada': 'Muqtada', 'Awjah': 'Awja', 'Owja': 'Awja', 'Ouja': 'Awja', 'Tikreet': 'Tikrit', 'Eid,': 'Eid,', '1.30': '1:30', '3.30': '3:30', '5.30': '5:30', '6.10': '6:10', 'Quran': 'Koran', 'keeper': 'Keeper', (28, 'Aridsina'): 'At a dinner', (59, 'knocked.'): 'not.', (29, 'Noor'): 'Nouri', (29, 'Rai'): '', (46, 'Munqif'): 'Munqith', (46, '-Farooon,'): '-Faroon,', (69, 'government.'): "government's.", (42, 'stepped'): 'step', (28, 'According'): 'according'}
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
        L.drop(c, card, W * a.get("x", 0.5), H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag"))
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
            sh = tone("C8"); k = max(W / sh.width, H / sh.height); sh = sh.resize((int(sh.width * k) + 1, int(sh.height * k) + 1), Image.LANCZOS)
            sh = sh.crop(((sh.width - W) // 2, (sh.height - H) // 2, (sh.width - W) // 2 + W, (sh.height - H) // 2 + H)).convert("RGB")
            BG["end"] = (sh, Image.blend(sh.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62))
        wl, wsb = wt(ENDL, "like"), wt(ENDL, "subscrib")
        c = BP.end_frame(BG["end"][0], BG["end"][1], t - t0, BP.NEXT["lastday27"], caps=[], t_like=(wl - t0) if wl else None, t_sub=(wsb - t0) if wsb else None)
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
    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(12), -17); music("Industrial Cinematic.mp3", tl(12), tl(22), -17)
    music("Man Down.mp3", tl(22), tl(30), -17); music("Thunder Dreams.mp3", tl(30), tl(36), -17); music("Industrial Cinematic.mp3", tl(36), tl(43), -17)
    music("Rising Tide.mp3", tl(43), tl(50), -18); music("Man Down.mp3", tl(50), tl(60), -18); music("Rising Tide.mp3", tl(68), tl(79), -17)
    music("Promises to Keep.mp3", tl(79), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("wind_deep_cinematic_hum", tl(30), tl(36), -31); loop("roomtone_dark_cinematic", tl(60), tl(68), -30)
    loop("wind_ambience", tl(74), tl(79), -31)
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
            wl, wsb = wt(ENDL, "like"), wt(ENDL, "subscrib")
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
    EV = [(0, 'rings', 'clock_tick_single', -20), (0, 'execution', 'hit_cinematic_deep_impact', -18), (1, 0.0, 'clock_tick_single', -20), (2, 'saddam', 'hit_big_cinematic_impact', -16), (6, 'kill', 'hit_short_bass', -18), (9, 'death', 'hit_horror_drum', -18), (10, 'worse', 'bass_suspense_mystery', -24), (11, 'back', 'hit_cinematic_deep_impact', -16), (16, 'hanging', 'hit_big_cinematic_impact', -16), (17, 0.0, 'clock_tick_single', -20), (19, 'four', 'hit_short_bass', -16), (22, 0.0, 'clock_tick_single', -20), (29, 'midnight', 'clock_bells_hour', -24), (29, 'hanging', 'hit_cinematic_deep_impact', -16), (30, 0.0, 'clock_tick_single', -20), (33, 'phones', 'metal_tool_drop', -22), (35, 'end', 'hit_short_bass', -18), (38, 'black', 'whoosh_fast_transition', -22), (41, 0.0, 'clock_tick_single', -20), (41, 'custody', 'hit_big_cinematic_impact', -16), (47, 'shouts', 'hit_short_bass', -18), (50, 0.0, 'clock_tick_single', -20), (53, 'koran', 'heartbeat_single', -16), (56, 'changed', 'sweep_horror_long', -24), (58, 'phones', 'hit_horror_drum', -18), (65, 0.0, 'clock_tick_single', -22), (68, 0.0, 'hit_cinematic_deep_impact', -18), (73, 'revenge', 'hit_short_bass', -18), (75, 'coffin', 'sweep_terror_darkness', -26), (78, 'sure', 'hit_short_bass', -18), (79, 0.0, 'hit_cinematic_deep_impact', -15), (85, -0.55, 'metal_hammer_hit', -16), (85, -0.3, 'hit_cinematic_deep_impact', -14)]
    EV = [e for e in EV if os.path.exists(SFXD + e[2] + ".mp3")]
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
    name = name or "TheLastHours_27_Saddam_LastDay.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, '1:30 AM, Baghdad'), (5, 'Dujail, 1982'), (12, 'The court'), (17, '30 days. They took four'), (22, 'Friday: who will do it?'), (30, 'Fourteen phones'), (36, 'Camp Cropper'), (43, 'The small room'), (50, 'The Koran'), (56, 'Two phones raised'), (60, '6:10 AM'), (68, 'Two videos'), (74, 'The coffin goes north'), (79, 'What the record keeps')]

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

