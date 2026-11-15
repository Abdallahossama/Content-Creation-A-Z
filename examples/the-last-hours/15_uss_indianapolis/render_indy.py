"""The Last Hours #15: USS Indianapolis, Monday 30 July 1945 (about 12:05 a.m. ship's time: two torpedoes from I-58; sunk in about
twelve minutes), the four days nobody reported her missing, the broken antenna that found the survivors (Thursday 2 August), the rescue,
the court-martial of Captain McVay and the long fight to clear his name. The File Keeper, colour grade, 1920x1080, burned-in captions, film finish.
Real images only: U.S. Navy / NHHC and National Archives photos and documents (court of inquiry, McVay's action report, routing orders,
ULTRA extracts, dispatches, deck logs), the Navy's 1945 rescue film (safe seconds only), Pexels sea textures labelled ILLUSTRATIVE.
Never shown: bodies, wounds, burns, sharks, any woman. Owner rules: research/research.md (do-not-say), assets.md section X.
  uv run --no-project --with pillow --with numpy --with soundfile python render_indy.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
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

ROOT = "D:/why habibi/_newchannel/15_uss_indianapolis/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 5.0                                   # the File Keeper end card runs under the sign-off
NEXT = os.environ.get("LH_NEXT", "")
ENDL = 90                                                # the File Keeper sign-off line (the end card runs under it)                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/indy_vo_chatterbox.wav")
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
def isdoc(rid): return re.fullmatch(r"A\d+p\d+|A9|A10|A11|A35", rid) is not None    # pages, charts and the war diary stay paper-toned; A13-A33 are photos
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
V_PHIL, V_SINK, V_RESC = (135.0, 11.5, 26.0), (134.5, 12.2, 5.5), (133.9, 11.8, 3.4)
GUAM, LEYTE, TINIAN, PELELIU, SAMAR = (144.66, 13.45), (125.33, 10.9), (145.63, 15.0), (134.24, 7.0), (125.72, 11.05)
SINK, I58, GWINN, G150, DOYLE, MCVAY = (134.8, 12.03), (134.27, 12.52), (133.5, 11.5), (133.78, 11.9), (133.58, 11.75), (133.35, 11.58)
ROUTE = [GUAM, (144.0, 13.08), (143.0, 13.23), (138.0, 12.5), (132.5, 11.73), (128.08, 11.1), (126.0, 10.62), (125.67, 10.69), LEYTE]   # Route Peddie (routing instructions, 28 Jul 1945)
TO_SINK = [GUAM, (144.0, 13.08), (143.0, 13.23), (138.0, 12.5), SINK]

# ------------------------------------------------------------------ shot constructors
CROP = {"A16": (0.06, 0.0, 0.94, 1.0), "A25": (0.495, 0.245, 0.77, 0.69), "A28": (0.27, 0.18, 0.97, 0.80), "A23": (0.0, 0.0, 1.0, 0.92),
        "A11": (0.0, 0.0, 0.5, 1.0), "A9": (0.04, 0.05, 0.97, 0.9)}      # A16: black scan bars; A25 and A28: the photo inside the Navy photo card
NAVY = "U.S. NAVY"; NHHC = "U.S. NAVY / NHHC"; NARA = "NATIONAL ARCHIVES"
TB = {"A9": "HASHIMOTO'S OWN SKETCH OF THE ATTACK, 29 JULY  ·  NIDS TOKYO / NHHC", "A10": "ROUTE PEDDIE, COURT OF INQUIRY EXHIBIT  ·  NHHC",
      "A11": "USS CECIL J. DOYLE, WAR DIARY, AUGUST 1945  ·  U.S. NAVY", "A13": f"USS INDIANAPOLIS OFF MARE ISLAND, 10 JULY 1945  ·  {NARA}",
      "A14": f"USS INDIANAPOLIS AT SEA, 1943-44  ·  {NHHC}", "A15": f"HER CREW IN THE WELL DECK, 1945  ·  {NHHC}",
      "A16": f"THE LITTLE BOY UNIT, TINIAN, AUGUST 1945  ·  {NARA}", "A17": f"LITTLE BOY ON TINIAN  ·  U.S. ARMY / {NARA}",
      "A18": f"LITTLE BOY LOADED INTO ENOLA GAY, 5 AUGUST 1945  ·  {NARA}", "A19": f"I-58 (LEFT) AT KURE, OCTOBER 1945  ·  {NAVY}",
      "A20": "I-58 AT SASEBO, JANUARY 1946  ·  U.S. MARINE CORPS", "A21": f"I-58 OFF SASEBO, APRIL 1946  ·  {NHHC}",
      "A22": "I-58'S FORWARD TORPEDO ROOM, 1946  ·  U.S. MARINE CORPS", "A23": f"CAPTAIN McVAY WITH WAR CORRESPONDENTS, GUAM, AUGUST 1945  ·  {NARA}",
      "A24": f"LT (JG) WILBUR GWINN AND HIS VENTURA, AUGUST 1945  ·  {NARA}", "A25": f"LT ADRIAN MARKS AND HIS PBY, 6 AUGUST 1945  ·  {NARA}",
      "A27": f"BUILDING 57, WASHINGTON NAVY YARD (PHOTO 1983)  ·  {NHHC}", "A28": f"SURVIVORS TAKEN TO HOSPITAL, PELELIU, AUGUST 1945  ·  {NARA}",
      "A29": f"TWO SURVIVORS, PELELIU, AUGUST 1945  ·  {NARA}", "A30": f"A SURVIVOR IS FED BY A CORPSMAN, PELELIU, 1945  ·  {NARA}",
      "A31": f"USS CECIL J. DOYLE, 1945  ·  {NAVY}", "A32": f"PV-1 VENTURAS LIKE GWINN'S (NOT HIS)  ·  {NAVY}", "A33": f"USS RINGNESS  ·  {NHHC}",
      "A34a": "THE NAVY'S RESCUE FILM, AUGUST 1945  ·  NATIONAL ARCHIVES 428-NPC-12522", "A34b": "SURVIVORS ABOARD A RESCUE SHIP, 1945  ·  NATIONAL ARCHIVES 428-NPC-12522",
      "A35": "HER TRACK FROM GUAM, NAVY CHART  ·  U.S. NAVY",
      "A1": "COURT OF INQUIRY, GUAM, AUGUST 1945  ·  NHHC / NARA RG 38", "A2": "CAPTAIN McVAY'S ACTION REPORT, 26 AUGUST 1945  ·  NHHC",
      "A3": "ROUTING INSTRUCTIONS, PORT DIRECTOR GUAM, 28 JULY 1945  ·  NHHC / NARA RG 38", "A4": "ULTRA EXTRACTS, JULY-AUGUST 1945  ·  NHHC ARCHIVES",
      "A5": "CASUALTY SUMMATION, AUGUST 1945  ·  NHHC", "A6": "PACIFIC DISPATCHES, 2-3 AUGUST 1945  ·  NHHC / NARA RG 38",
      "A7": "DECK LOG OF USS LST-779, 29 JULY 1945  ·  NHHC / NARA RG 24", "A8": "SECRETARY OF THE NAVY, 11 JULY 2001  ·  NHHC",
      "A12": "“A GRAVE MISFORTUNE”, NHHC, 2018", "A12p148": "DISPATCH OF 2 AUGUST 1945, AS PRINTED IN “A GRAVE MISFORTUNE” (NHHC, 2018)",
      "A4p11": "THE DECODED I-58 REPORT, ULTRA, 30 JULY 1945  ·  NHHC ARCHIVES", "A1p4": "COURT OF INQUIRY: GWINN'S MESSAGE, 2 AUGUST 1945  ·  NHHC / NARA RG 38"}
ILL = "ILLUSTRATIVE  ·  PEXELS"
for _r in ("F1", "F2", "F3", "F4"): TB[_r] = ILL
TB["F5"] = "SAN FRANCISCO TODAY  ·  ILLUSTRATIVE, PEXELS"
def DT(rid):
    m = re.match(r"(A\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD, 1945")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None, x=0.5): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid), x=x))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {"A34a": (0.03, 0.03, 0.97, 0.97), "A34b": (0.03, 0.03, 0.97, 0.97)}
LIFT = {"A34a": 1.25, "A34b": 1.2, "F4": 0.8}
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C10", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

PG = dict(zig="A3p1", subs="A3p2", ultra="A4p3", lst="A7p3", msg="A2p2", decrypt="A4p11", rule="A1p7", causes="A2p3", sighted="A1p4",
          advise="A12p148", cas="A5p1", eng="A8p1")                                 # document pages (set from the OCR search, ocr_find.py)
V_EPAC = (-141.0, 29.5, 46.0); V_AREA = (134.4, 11.9, 2.8); FARALLON, DIAMOND = (-123.0, 37.7), (-157.8, 21.26)
SHOTS = [
 # COLD OPEN
 (0, KB("A13", z=(1.05, 1.15), c0=(0.5, 0.5))),                                   # frame 1: her last portrait, 10 July 1945
 ((0, "planes|eight"), VID("A34a", at=52.0)),
 ((0, "dying|men"), VID("F4", at=3.0, dim=0.1)),
 ((0, "nobody|reported"), KB("F3", z=(1.04, 1.14))),
 (1, TCARD("12:05 AM", "Monday, 30 July 1945  ·  ship's time  ·  the Philippine Sea", "A13")),
 (2, KB("A14", z=(1.03, 1.12), c0=(0.55, 0.5))),
 ((2, "12|twelve"), COUNTER([((2, "12|twelve"), "12 MIN")], "FROM THE HIT TO GONE  ·  ABOUT", "A14", size=360)),
 (3, COUNTER([((3, "1195|eleven"), "1,195"), ((3, "316|three"), "316")], "ABOARD  ·  CAME HOME", "A15", size=380)),
 (4, KB("A15", z=(1.04, 1.14))),
 ((4, "sentence|paperwork"), KBP(PG["zig"], h=900)),
 ((4, "sharks"), VID("A34a", at=14.0)),
 ((4, "court"), KBP("A27", h=600, rot=-1.0)),
 # THE CARGO
 (5, VID("F5", at=2.0)),
 ((5, "hunters|francisco"), KB("A13", z=(1.12, 1.25), c0=(0.6, 0.45))),
 (6, KB("A13", z=(1.25, 1.4), c0=(0.62, 0.42), dim=0.1)),
 ((6, "canister|welded"), KBP("A17", h=640, rot=1.0)),
 ((6, "army|officers"), KB("A15", z=(1.1, 1.22), c0=(0.35, 0.45))),
 (7, VID("F5", at=12.0)),
 ((7, "hours|earlier|desert"), TCARD("16 JUL 1945", "The first atomic test, New Mexico  ·  hours before she sails", "A14")),
 (8, NMAP(V_EPAC, ops=[("pin", *FARALLON, "FARALLON ISLANDS · 16 JUL", 0.1, -420, 0), ("route", [FARALLON, DIAMOND], 0.5, 2.0), ("pin", *DIAMOND, "DIAMOND HEAD · 19 JUL", 2.4), ("label", -140.0, 33.5, "SAN FRANCISCO TO HAWAII", 1.0, 34)])),
 ((8, "74|seventy"), COUNTER([((8, "74|seventy"), "74½ HRS")], "SAN FRANCISCO TO HAWAII  ·  A RECORD", "A14", size=330)),
 (9, KB("A16", z=(1.03, 1.12))),
 ((9, "uranium|including"), KBP("A17", h=640, rot=-1.0)),
 (10, KBP("A18", h=600, rot=1.0, x=0.76)),
 # ZIGZAG AT DISCRETION
 (11, NMAP(V_PHIL, ops=[("pin", *GUAM, "GUAM", -9), ("pin", *LEYTE, "LEYTE", 0.4), ("route", ROUTE, 0.9, 2.6), ("label", 135.0, 9.2, "ROUTE PEDDIE  ·  ALONE", 3.2, 34)])),
 ((11, "alone"), KB("A14", z=(1.06, 1.16), c0=(0.6, 0.5))),
 (12, DOC(PG["subs"], [("33+34", (12, "submarine|reports"))])),
 ((12, "zigzag"), DOC(PG["zig"], [("69+70", (12, "zigzag"))])),
 (13, KBP("A27", h=600, rot=1.0)),
 (14, KB("A23", z=(1.05, 1.15), c0=(0.33, 0.4))),
 ((14, "codebreakers"), DOC(PG["ultra"], [("92", (14, "submarine|japanese"))])),
 ((14, "ship|captains"), KB("A19", z=(1.04, 1.14))),
 (15, DOC(PG["lst"], [("7", (15, "landing|ship"))])),
 ((15, "last"), KB("A13", z=(1.2, 1.3), c0=(0.45, 0.55))),
 (16, KBP("A10", h=720, rot=-1.0)),
 # UNDER THE MOON
 (17, VID("F4", at=8.0, dim=0.1)),
 ((17, "testify|visibility"), KBP("A23", crop=(0.12, 0.0, 0.62, 0.70), h=760, rot=-1.0, x=0.27)),
 (18, TCARD("~10:30 PM", "The moon rises, three-quarters full", "A13")),
 (19, KB("A14", z=(1.08, 1.18), c0=(0.5, 0.55))),
 ((19, "asleep|mcvay"), KBP("A23", crop=(0.12, 0.0, 0.62, 0.70), h=760, rot=1.0, x=0.27)),
 (20, NMAP(V_PHIL, ops=[("pin", *GUAM, "GUAM", -9), ("route", TO_SINK, 0.0, 2.5), ("pin", *I58, "I-58 SURFACES", 2.0), ("pin", *LEYTE, "LEYTE", -9)])),
 ((20, "hashimoto|commander"), KB("A20", z=(1.04, 1.14))),
 ((20, "dark|shape"), KB("A13", z=(1.04, 1.1), dim=0.45)),
 (21, KBP("A22", h=560, rot=-1.0)),
 ((21, "27|twenty"), COUNTER([((21, "27|twenty"), "27 MIN")], "FROM SIGHTING TO FIRING  ·  HASHIMOTO'S TESTIMONY", "A20", size=360)),
 (22, KBP("A21", h=600, rot=1.0)),
 (23, KBP("A9", h=600, rot=-1.0)),
 ((23, "six|fires"), COUNTER([((23, "six"), "6")], "TORPEDOES  ·  FROM ABOUT 1,600 YARDS, 3 SECONDS APART", "A22", size=420)),
 # TWELVE MINUTES
 (24, TCARD("12:05 AM", "Monday 30 July  ·  ship's time (about)", "A13")),
 ((24, "starboard|hit"), NMAP(V_PHIL, ops=[("pin", *GUAM, "GUAM", -9), ("route", TO_SINK, 0.0, 0.01), ("pin", *SINK, "HIT  ·  ABOUT 12:05 AM", 0.2), ("pin", *LEYTE, "LEYTE", -9)])),
 (25, KBP("A15", h=540, rot=1.0, x=0.74)),
 (26, KB("A13", z=(1.15, 1.3), c0=(0.3, 0.5), dim=0.2)),
 ((26, "phones|dead"), KB("A14", z=(1.15, 1.25), c0=(0.35, 0.4), dim=0.2)),
 (27, DOC(PG["msg"], [("44", (27, "hit|torpedoes")), ("47", (27, "immediate"))])),
 (28, VID("F4", at=14.0, dim=0.2)),
 ((28, "never|left"), KB("A13", z=(1.04, 1.1), dim=0.5)),
 (29, KB("A15", z=(1.1, 1.22), c0=(0.6, 0.5), dim=0.15)),
 ((29, "answers|abandon"), KBP("A23", crop=(0.12, 0.0, 0.62, 0.70), h=760, rot=-1.0, x=0.27)),
 (30, KB("A14", z=(1.04, 1.18), c0=(0.5, 0.5), dim=0.25)),
 ((30, "pulled|propellers"), VID("F4", at=20.0, dim=0.25)),
 (31, COUNTER([((31, "12|twelve"), "~12 MIN")], "AND SHE WAS GONE  ·  DOWN BY THE BOW", "A13", size=360)),
 (32, KB("F3", z=(1.04, 1.14))),
 ((32, "around|eight"), COUNTER([((32, "around|eight"), "~800")], "IN THE SEA  ·  MOST WITH ONLY A LIFE JACKET", "F3", size=400)),
 # NOBODY MISSED HER
 (33, KB("A19", z=(1.04, 1.14), c0=(0.3, 0.6))),
 (34, DOC(PG["decrypt"], [("17", (34, "report|codebreakers")), ("19", (34, "attacked|sank"))])),
 ((34, "japanese|claims"), KBP("A21", h=600, rot=-1.0)),
 (35, NMAP(V_PHIL, ops=[("pin", *GUAM, "GUAM", -9), ("route", TO_SINK, 0.0, 0.01), ("pin", *SINK, "", -9), ("pin", *LEYTE, "LEYTE  ·  DUE 11 AM", 0.3)])),
 (36, KB("A14", z=(1.1, 1.2), dim=0.5)),
 (37, DOC(PG["rule"], [("14", (37, "arrival|reports"))])),
 (38, KBP("A10", h=720, rot=1.0)),
 ((38, "radio|test"), KBP("A35", h=740, rot=-1.0)),
 (39, KBP("A35", h=880)),
 # FOUR DAYS
 (40, KB("F3", z=(1.04, 1.14))),
 ((40, "groups|see"), VID("A34a", at=16.0)),
 (41, VID("A34a", at=24.0)),
 ((41, "spam|malted"), KB("A29", z=(1.08, 1.18), c0=(0.5, 0.45), dim=0.2)),
 (42, DOC(PG["causes"], [("30", (42, "300|three"))])),
 ((43, "64|sixty"), COUNTER([((43, "64|sixty"), "64 HRS")], "WHAT A KAPOK JACKET WAS MEANT TO LAST", "F3", size=360)),
 ((43, "two|days"), VID("F4", at=4.0, dim=0.15)),
 (44, KB("A29", z=(1.04, 1.14), dim=0.15)),
 (45, KB("F3", z=(1.06, 1.18))),
 ((45, "things|aren"), KB("A13", z=(1.04, 1.1), dim=0.55)),
 ((45, "swim|never"), VID("F4", at=22.0, dim=0.2)),
 (46, VID("A34a", at=50.0)),
 ((46, "count|eight"), KB("A32", z=(1.04, 1.14), tag="PATROL PLANES OF THE TIME (NOT THOSE THAT FLEW OVER)  ·  U.S. NAVY")),
 ((46, "radar|nobody"), VID("A34a", at=57.0)),
 # THE SHARKS: MYTH vs RECORD
 (47, KB("F3", z=(1.06, 1.14), c0=(0.5, 0.4))),
 (48, VID("A34a", at=24.0)),
 (49, KB("A14", z=(1.04, 1.14), dim=0.15)),
 (50, KB("F3", z=(1.04, 1.12), dim=0.2)),
 (51, DOC(PG["causes"], [("48", (51, "wounds|exhaustion")), ("50", (51, "drinking|salt")), ("52", (51, "sharks|list"))])),
 ((51, "how|many"), KB("F2", z=(1.05, 1.12), dim=0.3)),
 # THE ANTENNA
 (52, NMAP(V_PHIL, ops=[("pin", *PELELIU, "PELELIU", -9), ("route", [PELELIU, GWINN], 0.8, 2.2), ("pin", *GWINN, "", 3.0)])),
 ((52, "gwinn|lieutenant"), KBP("A24", h=860, rot=1.0, x=0.62)),
 (53, KB("F1", z=(1.04, 1.14))),
 ((53, "nobody|knows"), KB("A14", z=(1.1, 1.2), dim=0.55)),
 (54, KBP("A24", h=860, rot=-1.0)),
 ((54, "tunnel|tail"), KB("A32", z=(1.2, 1.35), c0=(0.7, 0.55))),
 ((54, "and"), KB("F1", z=(1.2, 1.4))),
 (55, ("midask", dict(bg="A24", ln=55))),                          # the spoken mid-video ask (cliffhanger: he looks down)
 (56, DOC(PG["sighted"], [("38+39", (56, "right|over")), ("40+41", (56, "follows|900"))])),
 (57, VID("A34a", at=14.0)),
 (58, DOC(PG["sighted"], [("42", (58, "radios|11")), ("43+44", (58, "sighted"))])),
 (59, COUNTER([((59, "150|hundred"), "150")], "SURVIVORS IN THE WATER  ·  GWINN'S SECOND MESSAGE", "A24", size=420)),
 (60, KBP("A24", h=860, rot=1.0, x=0.74)),
 (61, DOC(PG["advise"], [("6", (61, "arrived|leyte"))])),
 # THREE BOUNCES
 (62, KB("A25", z=(1.04, 1.14))),
 ((62, "sharks|bothering"), VID("A34a", at=27.0)),
 ((62, "midnight|ship"), KBP("A31", h=440, rot=-1.0)),
 (63, TCARD("5:05 PM", "Marks lands on the open sea  ·  12-foot swells", "A25")),
 ((63, "words|bounces"), KBP("A25", crop=(0.49, 0.25, 0.79, 0.70), h=720, rot=1.0, x=0.76)),
 (64, KB("A25", z=(1.25, 1.4), c0=(0.55, 0.6), dim=0.15)),
 (65, VID("A34a", at=36.0)),
 ((65, "hull|full"), COUNTER([((65, "56|fifty"), "56")], "MEN TAKEN ABOARD MARKS'S PBY", "A25", size=420)),
 (66, VID("A34b", at=1.0)),
 (67, TCARD("10:42 PM", "The Cecil J. Doyle points her searchlight at the sky", "A31")),
 ((67, "searchlight|straight"), KBP("A31", h=440, rot=1.0)),
 ((67, "waters|submarine"), KB("A11", z=(1.05, 1.15), c0=(0.5, 0.45))),
 (68, VID("A34a", at=74.0)),
 ((68, "pull|men"), KB("A30", z=(1.04, 1.14))),
 (69, KBP("A31", h=440, rot=-1.0)),
 ((69, "radar|ship"), KB("A33", z=(1.04, 1.14))),
 ((69, "never|sighted"), KBP("A23", crop=(0.12, 0.0, 0.62, 0.70), h=760, rot=1.0, x=0.27)),
 (70, TCARD("NOON", "Friday 3 August  ·  the last survivors are out of the water", "A33")),
 ((70, "almost|half"), COUNTER([((70, "four|almost"), "~4½ DAYS")], "IN THE WATER", "A29", size=330)),
 # 316
 (71, COUNTER([((71, "1|1195|eleven"), "1,195"), ((71, "316|three"), "316")], "SAILED  ·  CAME HOME", "A15", size=400)),
 (72, DOC(PG["cas"], [("2", (72, "1196|eleven"))])),
 ((72, "historians|sailor"), KB("A15", z=(1.12, 1.25), c0=(0.4, 0.5), dim=0.2)),
 (73, KB("A30", z=(1.04, 1.14))),
 ((73, "cargo|hiroshima"), KBP("A18", h=600, rot=-1.0)),
 # THE WITNESS
 (74, DOC(PG["zig"], [("69+70", (74, "zigzag"))])),
 (75, KBP("A27", h=600, rot=-1.0)),
 ((75, "charge"), TCARD("CHARGE I", "Hazarding his ship by failing to zigzag", "A27")),
 (76, KB("A20", z=(1.06, 1.18), dim=0.2)),
 ((76, "hashimoto|commander"), KB("A19", z=(1.06, 1.16), c0=(0.3, 0.6), dim=0.2)),
 (77, KBP("A27", h=560, rot=1.0)),
 (78, KBP("A22", h=520, rot=-1.0, x=0.76)),
 (79, KBP("A21", h=600, rot=1.0)),
 (80, TCARD("19 DEC 1945", "Not guilty: the abandon-ship order  ·  guilty: no zigzag", "A27")),
 ((80, "never|convicted"), KBP("A23", crop=(0.12, 0.0, 0.62, 0.70), h=760, rot=-1.0, x=0.27)),
 (81, KB("A23", z=(1.12, 1.25), c0=(0.33, 0.35))),
 # THE LONG FIGHT
 (82, KB("A13", z=(1.03, 1.1), dim=0.55)),
 (83, KB("A15", z=(1.04, 1.12), dim=0.35)),
 (84, COUNTER([((84, "154|hundred"), "154"), ((84, "80|eighty"), "80+")], "SURVIVORS ASKED  ·  WROTE BACK", "A15", size=380)),
 ((84, "senate|testified"), KBP("A27", h=600, rot=1.0)),
 (85, DOC(PG["eng"], [("38+39+40", (85, "record|exonerated"))])),
 ((85, "conviction"), KBP("A23", crop=(0.12, 0.0, 0.62, 0.70), h=760, rot=1.0, x=0.27)),
 (86, KB("A13", z=(1.04, 1.12), dim=0.25)),
 ((86, "west"), NMAP(V_PHIL, ops=[("pin", *GUAM, "GUAM", -9), ("pin", *LEYTE, "LEYTE", -9), ("pin", *SINK, "1945 ESTIMATE", -9), ("arrow", SINK, (133.2, 11.9), "THE WRECK: WEST", 0.3)])),
 ((86, "landing|log"), DOC(PG["lst"], [("7", (86, "landing|log"))])),
 # WHAT THE RECORD SHOWS + ASKS
 (87, KB("A13", z=(1.03, 1.1), dim=0.3)),
 (88, COUNTER([((88, "two|torpedoes"), "2 TORPEDOES"), ((88, "rule|paperwork"), "1 RULE"), ((88, "antenna|broken"), "1 ANTENNA")],
              "USS INDIANAPOLIS  ·  30 JULY - 3 AUGUST 1945", "A13", size=300)),
 (89, KB("A23", z=(1.04, 1.12), c0=(0.35, 0.4))),
 ((ENDL, -0.7), ("end", {})),                                    # the File Keeper end card under the sign-off
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "hookleft", ("4 DAYS IN THE SEA.", "8 PLANES FLEW OVER.")),          # from frame 1 (LEAD = 0.8 s)
 (0, "missing", "under", "NOBODY REPORTED HER MISSING  ·  WHY?"),
 (1, 0.0, "badge", "MON 30 JUL 1945"),
 (2, 0.3, "under", "USS INDIANAPOLIS  ·  HEAVY CRUISER, 610 FEET"),
 (4, 0.2, "under", "THE CARGO  ·  THE RULE  ·  THE SHARKS  ·  THE TRIAL"),
 (5, 0.0, "brand", None),                                          # the File Keeper stamp, over moving footage, voice keeps going
 (5, 0.2, "badge", "SUN 15 JUL 1945"),
 (7, 0.0, "badge", "MON 16 JUL  ·  8:00 AM"),
 (9, 0.0, "badge", "THU 26 JUL 1945"),
 (9, "uranium|including", "under", "PARTS OF LITTLE BOY, INCLUDING ITS URANIUM"),
 (10, 0.3, "listL", ("REMEMBER", "THE CARGO")),
 (11, 0.0, "badge", "SAT 28 JUL  ·  9:00 AM"),
 (13, 0.2, "typecenter_red", "4 MONTHS LATER: A TRIAL"),
 (14, 0.3, "nameplate", ("CHARLES B. McVAY III", "CAPTAIN, USS INDIANAPOLIS")),
 (15, 0.0, "badge", "SUN 29 JUL  ·  AFTERNOON"),
 (16, 0.2, "under", "LST-779'S LOG  ·  REMEMBER IT"),
 (17, 0.0, "badge", "SUN 29 JUL  ·  AFTER DARK"),
 (17, "testify|visibility", "quoteR", ("“The visibility was poor.”", "CAPTAIN McVAY, AT HIS COURT-MARTIAL")),
 (19, 0.2, "listR", ("17 KNOTS", "NO ZIGZAG")),
 (20, 0.0, "badge", "SUN 29 JUL  ·  11:35 PM"),
 (20, "hashimoto|commander", "nameplate", ("MOCHITSURA HASHIMOTO", "COMMANDER, I-58  ·  NO SAFE PHOTO OF HIM")),
 (22, 0.2, "under", "KAITEN: MANNED SUICIDE TORPEDOES  ·  NOT USED"),
 (24, 0.0, "badge", "MON 30 JUL  ·  ~12:05 AM"),
 (25, 0.0, "listL", ("NEW YORK:", "SUNDAY, 10:35 AM")),
 (28, 0.2, "typecenter_red", "S.O.S.  ·  S.O.S.  ·  S.O.S."),
 (29, "answers|abandon", "quoteR", ("“Pass the word to abandon ship.”", "CAPTAIN McVAY")),
 (33, 0.2, "under", "HASHIMOTO SURFACES: NOTHING IN SIGHT"),
 (35, 0.0, "badge", "TUE 31 JUL  ·  11:00 AM"),
 (36, 0.2, "typecenter_red", "NOT REPORTED"),
 (38, 0.2, "under", "THE OFFICER WHO KNEW: NO ACTION"),
 (38, "radio|test", "under", "RADIO TEST: “UNABLE TO CONTACT INDIANAPOLIS”"),
 (39, 0.2, "under", "ON THE PLOTTING BOARDS: ARRIVED"),
 (40, 0.0, "badge", "MON 30 JUL - THU 2 AUG"),
 (40, 0.3, "under", "STRUNG OUT OVER ABOUT 20 MILES"),
 (41, 0.3, "under", "McVAY'S GROUP: 3 RAFTS, 1 FLOATER NET, 9 MEN"),
 (44, 0.2, "under", "NO PHOTOGRAPHS OF THE WOUNDED ARE SHOWN"),
 (45, "things|aren", "under", "HALLUCINATIONS: THE SHIP, JUST UNDER THE SURFACE"),
 (46, "count|eight", "typecenter", "ABOUT 8 PLANES  ·  NONE SAW THEM"),
 (47, 0.2, "typecenter", "MYTH vs RECORD: THE SHARKS"),
 (48, 0.3, "list", ("JAWS (1975):", "1,100 IN THE WATER", "316 CAME OUT", "SHARKS TOOK THE REST")),
 (49, 0.2, "list", ("THE RECORD:", "ABOUT 800 IN THE WATER", "SHARKS: THERE FROM EARLY ON", "HOW MANY THEY KILLED: NO COUNT")),
 (50, 0.3, "quote", ("“…I did not see a man" + chr(10) + "attacked by a shark.”", "DR. LEWIS HAYNES  ·  110 HOURS IN THE WATER")),
 (52, 0.0, "badge", "THU 2 AUG  ·  9:10 AM"),
 (52, "gwinn|lieutenant", "nameplate", ("WILBUR “CHUCK” GWINN", "LT (JG), U.S. NAVAL RESERVE  ·  PV-1 VENTURA PILOT")),
 (54, 0.0, "badge", "THU 2 AUG  ·  ~11:00 AM"),
 (57, 0.0, "badge", "THU 2 AUG  ·  11:18 AM"),
 (58, 0.0, "badge", "THU 2 AUG  ·  11:25 AM"),
 (60, "antenna|broke", "listL", ("FOUND", "BY ACCIDENT")),
 (62, 0.3, "nameplate", ("ADRIAN MARKS", "LIEUTENANT, U.S. NAVAL RESERVE  ·  PBY PILOT")),
 (63, "words|bounces", "quoteL", ("“The plane landed in three bounces," + chr(10) + "the first bounce being" + chr(10) + "about 15 feet high.”", "LT ADRIAN MARKS, 6 AUGUST 1945")),
 (64, 0.2, "under", "THE HOLES: PLUGGED WITH PENCILS AND COTTON"),
 (66, 0.2, "quote", ("“Their first one was" + chr(10) + "to ask for water.”", "LT ADRIAN MARKS")),
 (67, "moon", "under", "NO MOON THAT NIGHT"),
 (69, "never|sighted", "quoteR", ("“We were never sighted by a plane.”", "CAPTAIN McVAY, 1945")),
 (71, "home", "subpop", None),                                     # the File Keeper case tab, right after the payoff
 (72, "historians|sailor", "under", "2018: HE HAD LEFT THE SHIP BEFORE SHE SAILED"),
 (73, 0.0, "badge", "MON 6 AUG 1945"),
 (73, "cargo|hiroshima", "under", "THE CARGO SHE DELIVERED  ·  HIROSHIMA"),
 (75, 0.0, "badge", "MON 3 DEC 1945"),
 (76, 0.0, "badge", "THU 13 DEC 1945"),
 (76, "witness|united", "under", "A WITNESS FOR THE PROSECUTION"),
 (77, 0.2, "quote", ("“Would it have made any difference to you" + chr(10) + "if the target had been zigzagging?”", "THE DEFENSE, 13 DECEMBER 1945")),
 (78, 0.2, "quoteL", ("“It would have involved" + chr(10) + "no change in the method" + chr(10) + "of firing the torpedoes," + chr(10) + "but some changes in maneuvering.”", "COMMANDER HASHIMOTO, THROUGH AN INTERPRETER")),
 (79, 0.2, "under", "AN AMERICAN SUBMARINE CAPTAIN, UNDER OATH"),
 (80, "never|convicted", "listR", ("NEVER CONVICTED", "OF LOSING", "HIS SHIP")),
 (81, 0.2, "under", "20 FEB 1946: SENTENCE REMITTED, BACK TO DUTY"),
 (82, 0.2, "typecenter", "NOVEMBER 1968"),
 (83, 0.2, "under", "HUNTER SCOTT, 11  ·  PENSACOLA, FLORIDA"),
 (84, "senate|testified", "under", "14 SEP 1999  ·  U.S. SENATE ARMED SERVICES COMMITTEE"),
 (85, "conviction", "listR", ("THE CONVICTION", "STILL STANDS")),
 (86, 0.0, "badge", "AUGUST 2017"),
 (86, "18|eighteen", "under", "MORE THAN 18,000 FEET DOWN"),
 (87, 0.0, "typecenter", "WHAT THE RECORD SHOWS"),
 (89, 0.2, "under", "SHOULD McVAY HAVE BEEN TRIED?  TELL ME BELOW"),
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

SLOT = {"hookleft": "center", "lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "listL": "center", "quoteL": "center", "quoteR": "center", "listR": "center"}
OVT = [OT(ln, off) for ln, off, _, _ in OV]
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    end = shot_t1                                  # the EARLIEST later overlay in the slot wins, whatever its list order
    for j2 in range(len(OV)):
        if OVT[j2] <= OVT[j] or j2 == j: continue
        k2 = OV[j2][2]
        if SLOT.get(k2) == sl or (sl == "bottom" and k2 in ("list", "typecenter", "typecenter_red", "quote", "listL", "quoteL", "quoteR", "listR")):
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
        elif kind in ("list", "listL", "listR"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay); sz = 74 if max(len(s) for s in a) < 24 else 58
            if kind in ("listL", "listR"): sz = min(sz, 52)
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W * {"listL": 0.29, "listR": 0.71}.get(kind, 0.5), H / 2 - (len(a) - 1) * 60 + i * 120, size=sz, cps=20, anchor="mm", cursor=False)
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
        if t - t0 < BA.STAMP_LEN: c.alpha_composite(BA.stamp_frame(t - t0, BP.LABEL["indy"]))
    elif kind == "hookleft":                                   # frame-1 hook text in thumbnail blocks, left, off the face
        f = L.font(COND, 132); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i, s in enumerate(a):
            y = H / 2 - 130 + i * 180; w = f.getlength(s)
            d.rectangle((80, y - 82, 80 + w + 56, y + 82), fill=((0, 0, 0, 230) if i == 0 else (255, 204, 0, 255)))
            d.text((108, y), s, font=f, fill=(BONE + (255,)) if i == 0 else (10, 10, 10, 255), anchor="lm")
        c.alpha_composite(lay)
    elif kind == "subpop":                                     # the File Keeper case tab (no ask: the spoken mid ask does that)
        if t - t0 < BA.PILL_LEN: c.alpha_composite(BA.chip_frame(t - t0, BP.LABEL["indy"]), (0, BP.PILL_Y))

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
CAPFIX = {"Lighty": "Leyte", "Leighty": "Leyte", "Laity": "Leyte", "Layte": "Leyte", "Pelelu": "Peleliu", "Pelilu": "Peleliu", "Pellalu": "Peleliu", "Peleleu": "Peleliu",
          "McVeigh": "McVay", "McVey": "McVay", "Mcvay": "McVay", "Gwyn": "Gwinn", "Gwen": "Gwinn", "Gwin": "Gwinn", "Hashimodo": "Hashimoto", "Tinnian": "Tinian",
          "Farallone": "Farallon", "Faralon": "Farallon", "Haynes'": "Haynes", "Hayes": "Haynes", "Doil": "Doyle", "SOS": "S.O.S.", "S.O.S": "S.O.S.", "LST": "LST-779",
          "I58": "I-58", "I-58.": "I-58.", "11.18": "11:18", "11.25": "11:25", "10.42": "10:42", "5.05": "5:05", "10.30": "10:30", "11.30": "11:30", "9.10": "9:10", (61, "arrived."): "arrived", (61, "Late."): "Leyte.", (61, "Advise."): "Advise."}  # whisper spellings -> the record's
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
            sh = tone("A13"); k = max(W / sh.width, H / sh.height); sh = sh.resize((int(sh.width * k) + 1, int(sh.height * k) + 1), Image.LANCZOS)
            sh = sh.crop(((sh.width - W) // 2, (sh.height - H) // 2, (sh.width - W) // 2 + W, (sh.height - H) // 2 + H)).convert("RGB")
            BG["end"] = (sh, Image.blend(sh.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62))
        wl, wsb = wt(ENDL, "like"), wt(ENDL, "subscrib")
        c = BP.end_frame(BG["end"][0], BG["end"][1], t - t0, BP.NEXT["indy"], caps=[], t_like=(wl - t0) if wl else None, t_sub=(wsb - t0) if wsb else None)
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
    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(17), -17); music("Industrial Cinematic.mp3", tl(17), tl(24), -17)
    music("Man Down.mp3", tl(24), tl(33), -17); music("Thunder Dreams.mp3", tl(33), tl(47), -17); music("Rising Tide.mp3", tl(47), tl(56), -17)
    music("Industrial Cinematic.mp3", tl(56), tl(71), -17); music("Man Down.mp3", tl(71), tl(82), -18); music("Promises to Keep.mp3", tl(82), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("waves_rough_sea_loop", tl(24), tl(33), -31); loop("waves_rough_sea_loop", tl(40), tl(52), -33)
    loop("wind_deep_cinematic_hum", tl(17), tl(24), -31); loop("waves_rough_sea_loop", tl(62), tl(70), -34)
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
    EV = [(0, "planes|eight", "sweep_horror_long", -24), (0, "dying", "heartbeat_single", -18), (0, "missing", "hit_short_bass", -18),
          (2, "torpedoes", "hit_big_cinematic_impact", -20), (6, "welded", "metal_hammer_hit", -24), (7, "sails", "ship_engine_loop", -30),
          (9, "ashore", "hit_cinematic_deep_impact", -20), (11, "alone", "wind_scary", -28), (14, "codebreakers", "radio_static_fx", -28),
          (20, "surface", "bass_suspense_mystery", -24), (21, "dives", "water_splash", -26), (23, "fires|six", "whoosh_metal_hit", -22),
          (24, "hit", "hit_big_cinematic_impact", -16), (26, "blaze", "thunder_deep_rumble", -22), (27, "message", "radio_static_crackles", -28),
          (28, "keys", "radio_static_crackles", -24), (31, "bow", "hit_cinematic_deep_impact", -18), (34, "codebreakers", "radio_static_fx", -28),
          (36, "nobody", "hit_short_bass", -18), (37, "arrival", "typewriter_soft_click", -22), (46, "planes", "sweep_horror_long", -22),
          (52, "takes", "wind_ambience", -30), (54, "looks|down", "hit_short_bass", -16), (57, "heads", "hit_cinematic_deep_impact", -18),
          (58, "radios", "radio_static_crackles", -26), (63, "bounces", "jump_in_water", -20), (67, "searchlight", "light_switch", -24),
          (69, "radar", "bass_suspense_mystery", -24), (73, "hiroshima", "hit_deep_heartbeat_impact", -20), (75, "trial", "hit_horror_drum", -20),
          (80, "guilty", "hit_horror_drum", -18), (86, "wreck", "water_splash", -26), (87, 0.0, "hit_cinematic_deep_impact", -15),
          (ENDL, -0.55, "metal_hammer_hit", -16), (ENDL, -0.3, "hit_cinematic_deep_impact", -14)]
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
    name = name or "TheLastHours_15_USS_Indianapolis.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "Nobody came"), (5, "The cargo"), (11, "Zigzag at discretion"), (17, "Under the moon"), (24, "Twelve minutes"),
      (33, "Nobody missed her"), (40, "Four days"), (47, "The sharks: myth vs record"), (52, "The antenna"), (62, "Three bounces"),
      (71, "316"), (74, "The witness"), (82, "The long fight"), (87, "What the record shows")]

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

