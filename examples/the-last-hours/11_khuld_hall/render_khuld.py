"""The Last Hours #10: the al-Khuld Hall purge, Baghdad, July-August 1979 (Case File style, colour grade, 1920x1080).
Built on render_cyclops.py + moving footage (vidclip.py: "vid" full frame, "vidp" low-res clip as a print).
No footage of the 1979 meeting is used (copyright: research.md section 18). Documents: FBIS / FBI scans (OCR rows) and the
State Department cables as printed by NARA's AAD (exact line boxes from the PDF text, cables_to_pages.py; FRUS: frus_pages.py).
  uv run --no-project --with pillow --with numpy --with soundfile python render_khuld.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
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

ROOT = "D:/why habibi/_newchannel/11_khuld_hall/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 20.0
NEXT = os.environ.get("LH_NEXT", "")                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/khuld_vo_chatterbox.wav")
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
BAGHDAD, DAMASCUS, KIRKUK, TIKRIT = (44.37, 33.31), (36.29, 33.51), (44.39, 35.47), (43.68, 34.60)
V_ME, V_IRAQ = (40.4, 33.4, 14.0), (44.0, 34.2, 7.5)

# ------------------------------------------------------------------ shot constructors
CROP = {"A7": (0.0, 0.12, 1.0, 1.0), "B3": (0.0, 0.0, 1.0, 1.0), "B7": (0.0, 0.0, 1.0, 1.0)}
TB = {"B1": "HAFEZ AL-ASSAD AND JIMMY CARTER, GENEVA, 1977  ·  WHITE HOUSE PHOTO",
      "B3": "TARIQ AZIZ (RIGHT) WITH PRESIDENT REAGAN, 1984  ·  WHITE HOUSE PHOTO", "B4": "SADDAM HUSSEIN AFTER HIS CAPTURE, DEC 2003  ·  U.S. DOD",
      "B5": "SADDAM HUSSEIN AFTER HIS CAPTURE, DEC 2003  ·  U.S. DOD", "B6": "THE CAPTURE ANNOUNCED, 14 DEC 2003  ·  USAF",
      "B7": "SADDAM HUSSEIN IN COURT, 1 JUL 2004  ·  USAF PHOTO", "B8": "ALI HASSAN AL-MAJID, 2004  ·  USAF PHOTO",
      "B10": "SADDAM ON THE U.S. MOST-WANTED CARDS, 2003", "C1": "THE REPUBLICAN PALACE, BAGHDAD, 2000s  ·  BRIAN1975, CC BY-SA 3.0",
      "C2": "THE REPUBLICAN PALACE FROM THE AIR, 2007  ·  JIM GORDON, CC BY 2.0", "C3": "A SADDAM-ERA PALACE DINING ROOM, 2000s  ·  BRIAN1975, CC BY-SA 3.0",
      "C4": "A SADDAM-ERA PALACE HALL, APRIL 2003 (NOT AL-KHULD HALL)  ·  U.S. DOD", "C5": "AL-FAW PALACE, BAGHDAD, 2006  ·  USAF",
      "C6": "A SADDAM-ERA PALACE, CAMP VICTORY, 2011  ·  U.S. ARMY", "C7": "A THRONE IN AL-FAW PALACE, 2011  ·  U.S. ARMY",
      "C9": "BAGHDAD FROM THE AIR, 2004  ·  USMC", "C10": "SADDAM'S STATUE FALLS, FIRDOS SQUARE, 9 APR 2003  ·  U.S. DOD",
      "C11": "BAGHDAD AND THE TIGRIS FROM SPACE, 2002  ·  NASA", "F6": "AN IRAQI TILE MURAL OF SADDAM  ·  B. MOSS, CC BY 2.0",
      "F7": "A SADDAM MURAL, VICTORY OVER AMERICA PALACE, 2009  ·  CC BY-SA 3.0", "F9": "THE HOLE WHERE SADDAM WAS FOUND, DEC 2003  ·  U.S. ARMY",
      "B9": "ALI HASSAN AL-MAJID (RIGHT), “CHEMICAL ALI”, AT HIS HEARING, 2004  ·  U.S. DOD", "C8": "SADDAM'S SWORDS OF VICTORY ARCH, BAGHDAD, 2003  ·  USAF",
      "C13": "BAGHDAD, U.S. GOVERNMENT CITY MAP, 2003  ·  NIMA", "F1": "THE BA'ATH PARTY HEADQUARTERS IN RUINS, BAGHDAD, 2007  ·  J. GORDON, CC BY 2.0",
      "F2": "INSIDE THE RUINED BA'ATH PARTY HEADQUARTERS, 2003  ·  J. GORDON, CC BY 2.0", "F5": "SADDAM'S GIANT BUSTS, TAKEN DOWN, 2004  ·  U.S. ARMY",
      "F6": "AN IRAQI TILE MURAL OF SADDAM  ·  B. MOSS, CC BY 2.0", "D10": "PRESIDENT BUSH ADDRESSES THE NATION ON IRAQ, 17 MAR 2003  ·  WHITE HOUSE",
      "D1": "BAGHDAD'S VICTORY ARCH, 2005  ·  U.S. ARMY VIDEO", "D3": "A SADDAM PALACE, 2009  ·  U.S. AIR FORCE VIDEO",
      "D4": "AL-FAW PALACE, 2008  ·  U.S. ARMY VIDEO", "D5": "A SADDAM-ERA PRISON, 2005  ·  U.S. ARMY VIDEO",
      "D7": "THE TIGRIS IN BAGHDAD, 2010  ·  U.S. ARMY VIDEO", "D8": "BAGHDAD AT NIGHT, 2017  ·  M. AL-JAMALIY, CC BY 3.0",
      "H1": "SADDAM'S CAPTURE, DEC 2003  ·  U.S. DOD FOOTAGE, NATIONAL ARCHIVES"}
ILL = "ILLUSTRATIVE  ·  PEXELS"
for _r in ("E2", "E7", "E10", "E11", "E12", "E13", "E14"): TB[_r] = ILL
def DT(rid):
    n = re.match(r"A(\d+)", rid).group(1)
    cab = {"12": "1522, 16 JUL", "13": "1543, 19 JUL", "14": "1583, 24 JUL", "15": "1591, 25 JUL", "16": "1593, 25 JUL", "17": "1602, 27 JUL",
           "18": "1603, 27 JUL", "19": "1621, 30 JUL", "20": "1626, 30 JUL", "21": "1640, 31 JUL", "23": "1754, 15 AUG", "25": "1935, 12 SEP"}
    if n in cab: return f"U.S. INTERESTS SECTION BAGHDAD, CABLE {cab[n]} 1979  ·  NATIONAL ARCHIVES"
    return {"1": "FBIS, 17 JUL 1979: IRAQI NEWS AGENCY, U.S. GOVERNMENT TRANSLATION", "2": "FBIS, 30 JUL 1979: IRAQ'S OFFICIAL STATEMENT, U.S. TRANSLATION",
            "3": "FBIS, 30 JUL 1979: IRAQ'S OFFICIAL STATEMENT, U.S. TRANSLATION", "4": "FBIS, 30 JUL 1979: IRAQ'S OFFICIAL STATEMENT, U.S. TRANSLATION",
            "5": "FBIS, 8 AUG 1979: THE VERDICTS (IRAQI NEWS AGENCY)", "6": "FBIS, 9 AUG 1979: BAGHDAD RADIO ON THE EXECUTIONS",
            "22": "STATE DEPARTMENT INTELLIGENCE SUMMARY, 10 AUG 1979  ·  NATIONAL ARCHIVES", "24": "STATE DEPARTMENT CABLE 224206, 26 AUG 1979  ·  NATIONAL ARCHIVES",
            "26": "CIA, IRAQ: A HANDBOOK, DECEMBER 1982", "27": "FRUS 1977-80, VOL. XVIII, DOC. 138: BAGHDAD 1528, 17 JUL 1979 (PUBLISHED TEXT)",
            "28": "FRUS 1977-80, VOL. XVIII, DOC. 139: BAGHDAD 231, 4 FEB 1980 (PUBLISHED TEXT)"}.get(n, "FBI, INTERVIEW SESSION 8 WITH SADDAM HUSSEIN, 20 FEB 2004")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {"E12": (0.15, 0.45, 0.85, 1.0)}                                             # the Pexels auditorium is a cinema: rows of seats only, never the screen
LIFT = {"E12": 0.55, "E6": 0.7, "E19": 0.7, "E20": 0.75, "D8": 0.8}                 # gamma for dark clips (LESSONS 34: dark reads as black on a phone)
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag or "SADDAM HUSSEIN, 2004 (USAF), IN A SADDAM-ERA HALL, 2003 (DOD)  ·  COMPOSITE"))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C6", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

SHOTS = [
 (0, GHOST("C4", "B7", (0.10, 0.34, 0.44, 0.88))),                                  # frame 1: Saddam ghosted into an empty Saddam-era hall (= thumbnail A)
 ((0, "name|read"), VID("E11", speed=0.5)),
 ((0, "seventeen|17"), COUNTER([((0, "seventeen|17"), "17 DAYS")], "FROM THE MEETING TO THE FIRING SQUADS", "C6", size=300)),
 ((0, "nobody"), KB("C8", z=(1.05, 1.15), dim=0.2)),
 (1, TCARD("22 JULY 1979", "Sunday  ·  Baghdad", "C11")),
 ((1, "saddam"), KB("B10", z=(1.3, 1.45), c0=(0.42, 0.45))),
 (2, VID("E10", at=14.0, z=(1.1, 1.18), speed=0.8)),
 ((2, "each"), VID("D3", at=66.0, z=(1.05, 1.1))),
 ((2, "guards"), KB("C4", z=(1.2, 1.3), c0=(0.62, 0.5))),
 (3, VID("E1", at=2.0, z=(1.15, 1.2), c=(0.5, 0.62), dim=0.2)),
 (4, VID("E7", z=(1.0, 1.08))),
 ((4, "tariq"), KB("B3", z=(1.35, 1.5), c0=(0.72, 0.42))),
 ((4, "ali"), KB("B8", z=(1.25, 1.4), c0=(0.68, 0.42))),
 ((4, "chemical"), KB("B9", z=(1.15, 1.25), c0=(0.72, 0.45))),
 (5, VID("E15", z=(1.0, 1.06))),
 (6, VID("E1", at=5.0, z=(1.18, 1.22), c=(0.5, 0.62))),
 ((6, "people"), DOC("A9", [("sixty-six", (6, "people"))])),
 (7, DOC("A16p1", [("12", 7), ("22", (7, "washington"))])),
 ((7, "two|2004|thousand"), VID("H1", at=86.0, z=(1.15, 1.22), c=(0.46, 0.42))),
 (8, VID("E8", z=(1.0, 1.06))),
 ((8, "admitted"), KB("B5", z=(1.05, 1.15), c0=(0.5, 0.35))),
 ((8, "question"), VID("D3", at=133.0, z=(1.05, 1.1))),
 (9, TCARD("8:40 PM", "Monday, July 16, 1979", "C2")),
 ((9, "farewell|speech"), DOC("A1", [((455, 1190, 2870, 1505), (9, "farewell|speech"))])),
 (10, KB("C1", z=(1.0, 1.1))),
 ((10, "officially"), DOC("A1", [((455, 1795, 2870, 1945), (10, "officially"))])),
 (11, VID("E16", z=(1.0, 1.05))),
 ((11, "saddam"), KB("B10", z=(1.3, 1.45), c0=(0.42, 0.45))),
 (12, DOC("A27p1", [("2+3", 12)])),
 (13, DOC("A13p1", [("28+29+30", 13)])),
 (14, VID("E20", z=(1.0, 1.06))),
 (15, TCARD("12 JULY", "Thursday, 1979  ·  the ruling council", "C3")),
 ((15, "command|council"), KB("C3", z=(1.0, 1.12))),
 (16, VID("E11", at=0.5, speed=0.45, z=(1.1, 1.2))),
 ((16, "dangerous"), VID("E10", at=10.0, speed=0.8, dim=0.2)),
 (17, DOC("A18p2", [("12+13+14", 17)])),
 (18, DOC("A18p2", [("10+11", 18), ("15+16", (18, "chosen|mashhadi"))])),
 (19, DOC("A18p2", [("17+18+19", 19)])),
 (20, DOC("A12p2", [("24", 20), ("28+29+30", (20, "reasons"))])),
 (21, KB("B7", z=(1.45, 1.6), c0=(0.3, 0.52), dim=0.2)),
 (22, VID("E13", z=(1.0, 1.08))),
 ((22, "remember"), VID("E13", at=12.0, z=(1.2, 1.3), c=(0.45, 0.5))),
 (23, NMAP(V_ME, ops=[("pin", *BAGHDAD, "BAGHDAD", -9), ("pin", *DAMASCUS, "DAMASCUS", 0.6), ("route", [DAMASCUS, BAGHDAD], 1.0, 1.2),
                      ("label", 40.3, 32.4, "ABOUT 470 MILES", 2.2, 34)])),
 ((23, "charter"), KB("B1", z=(1.0, 1.1))),
 (24, NMAP(V_ME, ops=[("pin", *DAMASCUS, "SYRIA", -9), ("pin", *BAGHDAD, "IRAQ", -9)], z=(1.05, 1.12))),
 (25, DOC("A18p2", [("32+33", 25)])),
 (26, DOC("A18p2", [("33+34+35", 26)])),
 ((26, "reportedly"), VID("E6", at=8.0)),
 (27, KB("C11", z=(1.0, 1.15), c0=(0.5, 0.5), c1=(0.45, 0.5))),
 ((27, "khuld"), KB("C13", z=(1.6, 1.9), c0=(0.42, 0.55), c1=(0.40, 0.58))),
 (28, KBP("A2", h=920)),
 (29, DOC("A3", [((262, 2688, 2525, 2795), 29), ("Khuld Hall", (29, "khuld"))])),
 (30, DOC("A3", [("heard the confessions", 30)])),
 (31, KBP("A8", h=920)),
 (32, DOC("A9", [("sixty-six", 32)])),
 (33, DOC("A10", [((148, 1163, 1085, 1212), 33), ("shouted their innocence", (33, "named|shouted"))])),
 (34, DOC("A9", [("one by one", (34, "one")), ("Himaya", (34, "himaya|guards"))])),
 (35, DOC("A10", [("ordered at least one", 35)])),
 (36, DOC("A10", [("three things", 36), ("smoking a cigar", (36, "cigar"))])),
 ((36, "tariq"), KB("B3", z=(1.35, 1.5), c0=(0.72, 0.42))),
 ((36, "majid"), KB("B8", z=(1.25, 1.4), c0=(0.68, 0.42))),
 (37, DOC("A9", [("crying", 37)])),
 ((37, "director"), VID("E13", at=10.0, z=(1.15, 1.22))),
 (38, VID("E9", z=(1.0, 1.06))),
 ((38, "every"), KB("F2", z=(1.05, 1.15), dim=0.12)),
 (39, KB("C3", z=(1.05, 1.15), dim=0.1)),
 (40, DOC("A8", [("given to all", 40)])),
 ((40, "copies|ambassadors"), DOC("A11", [((160, 600, 1095, 662), (40, "copies|ambassadors"))])),
 (41, VID("E7", at=4.0, z=(1.1, 1.2))),
 (42, KB("C6", z=(1.0, 1.1))),
 ((42, "sixty|68"), COUNTER([((42, "sixty|68"), "68")], "THE NUMBER PUT ON TRIAL  ·  NOT THE NUMBER READ OUT", "C6")),
 (43, VID("D7", at=60.0, z=(1.02, 1.08))),
 ((43, "interests|section"), DOC("A14p1", [("11", (43, "interests|section")), ("17", (43, "peck|edward"))])),
 (44, TCARD("1:29 PM", "Tuesday, July 24, 1979", "C2")),
 (45, DOC("A14p1", [("22+23+24+25", 45), ("26+27", (45, "thirty|35"))])),
 (46, KB("C1", z=(1.1, 1.2), c0=(0.5, 0.45))),
 (47, DOC("A14p1", [("28", 47)])),
 (48, TCARD("5:35 PM", "Wednesday, July 25, 1979", "C5")),
 ((48, "secret|cable"), DOC("A16p1", [("12", (48, "secret|cable")), ("22", (48, "action|night"))])),
 (49, DOC("A16p2", [("1+2", 49)])),
 (50, DOC("A16p2", [("18", 50)])),
 (51, DOC("A17p1", [("38+39+40", 51)])),
 (52, VIDP("D5", at=255.0, h=600, bg="C6")),
 ((52, "over|two"), DOC("A20p1", [("42+43", (52, "over|two"))])),
 (53, DOC("A21p2", [("10", 53)])),
 ((53, "normal"), VID("D7", at=70.0, z=(1.02, 1.08))),
 (54, TCARD("8:40 PM", "Saturday, July 28, 1979", "C2")),
 ((54, "government"), KBP("A2", h=920, rot=1.5)),
 (55, DOC("A2", [((245, 690, 2370, 830), 55)])),
 (56, DOC("A2", [((245, 1008, 2420, 1066), 56), ((245, 1062, 2420, 1178), (56, "mashhadi|mash"))])),
 (57, DOC("A2", [("foreign side", 57), ("national interest", (57, "national|interest"))])),
 (58, NMAP(V_ME, ops=[("pin", *BAGHDAD, "BAGHDAD", -9), ("pin", *DAMASCUS, "SYRIA?", 0.3)], z=(1.0, 1.08))),
 (59, VID("E10", at=12.0, z=(1.05, 1.12), dim=0.15)),
 (60, DOC("A19p3", [("22+23", 60)])),
 (61, TCARD("1 AUGUST", "Wednesday, 1979  ·  Ramadan", "C5")),
 ((61, "ramadan|holy"), KB("C9", z=(1.0, 1.1))),
 (62, COUNTER([(62, "6 DAYS")], "THE SPECIAL COURT SITS  ·  1-6 AUGUST 1979", "C2", size=300)),
 (63, TCARD("8:30 PM", "Tuesday, August 7, 1979", "C3")),
 ((63, "announces|verdicts"), KBP("A5", h=920)),
 (64, KB("F6", z=(1.05, 1.15), c0=(0.6, 0.45), dim=0.35)),
 (65, DOC("A5", [("property", 65), ("no case", (65, "case|left"))])),
 (66, TCARD("8 AUGUST", "Wednesday, 1979", "C5")),
 ((66, "moon|night"), VID("E20", z=(1.0, 1.06))),
 (67, KB("C6", z=(1.15, 1.25), c0=(0.5, 0.55), dim=0.35)),
 (68, DOC("A22p4", [("1+2", (68, "americans|syria"))])),
 (69, KBP("A6", h=920)),
 (70, DOC("A6", [("own weapons", 70)])),
 (71, DOC("A6", [("each division", 71)])),
 (72, DOC("A6", [("attended by", 72)])),
 (73, VID("E16", at=2.0, z=(1.08, 1.14))),
 (74, KBP("A28p1", h=900)),
 (75, DOC("A28p1", [("8+9+10+11", 75)])),
 (76, KB("F7", z=(1.0, 1.12))),
 (77, KB("C7", z=(1.0, 1.12))),
 ((77, "americans|translate"), VID("D3", at=45.0, z=(1.05, 1.12))),
 (78, VID("D1", at=6.0, z=(1.05, 1.1))),
 (79, DOC("A23p1", [("38+39", 79)])),
 (80, DOC("A25p2", [("4+5+6+7", (80, "probably"))])),
 (81, VID("E11", at=1.0, speed=0.5, z=(1.15, 1.25), dim=0.25)),
 (82, NMAP(V_ME, ops=[("pin", *DAMASCUS, "DAMASCUS", -9), ("pin", *BAGHDAD, "BAGHDAD", -9), ("label", 40.3, 34.6, "?", 0.3, 130)])),
 (83, VID("E8", at=4.0, z=(1.05, 1.12), dim=0.1)),
 (84, DOC("A24p2", [("23+27", 84)])),
 (85, KB("B1", z=(1.2, 1.35), c0=(0.5, 0.4))),
 (86, VID("D10", at=90.0, z=(1.02, 1.08))),
 ((86, "years"), KB("C10", z=(1.0, 1.1))),
 ((86, "december"), VID("H1", at=46.0, z=(1.15, 1.2), c=(0.45, 0.42))),
 ((86, "hole|hiding"), KB("F9", z=(1.0, 1.1))),
 (87, TCARD("20 FEB 2004", "Friday  ·  Baghdad  ·  FBI session 8", "B7")),
 ((87, "piro|sits"), KBP("A7", h=900, rot=1.5)),
 (88, VID("H1", at=120.0, z=(1.15, 1.22), c=(0.46, 0.42))),
 (89, DOC("A9", [("secrets of", 89)])),
 (90, DOC("A11", [("rarely smokes", 90)])),
 ((90, "unless"), KB("B4", z=(1.1, 1.2), c0=(0.5, 0.35))),
 (91, DOC("A9", [("human being", (91, "human|being"))])),
 ((91, "felt"), DOC("A8", [("back-stabbed", (91, "felt"))])),
 (92, KB("B3", z=(1.5, 1.7), c0=(0.72, 0.4))),
 (93, DOC("A11", [("all scared", (93, "scared|were"))])),
 (94, KB("C5", z=(1.0, 1.1))),
 (95, COUNTER([((95, "fifty|50"), "~50"), ((95, "sixty|66"), "~66"), ((95, "eight|68"), "68")], "HOW MANY NAMES?  AL-AHRAM  ·  THE FBI AGENT  ·  PUT ON TRIAL", "C9")),
 (96, VID("E8", at=2.0, z=(1.08, 1.15))),
 (97, NMAP(V_ME, ops=[("pin", *BAGHDAD, "BAGHDAD", -9), ("route", [BAGHDAD, DAMASCUS], 0.4, 1.4), ("pin", *DAMASCUS, "SYRIA?", 1.6)], z=(1.0, 1.06))),
 ((97, "khuld|hall"), KB("F1", z=(1.0, 1.1), dim=0.1)),
 (98, DOC("A10", [("inform the Party", 98)])),
 (99, VID("E2", at=8.6, z=(1.0, 1.1))),
 (100, KB("F5", z=(1.05, 1.15), c0=(0.6, 0.45), dim=0.15)),
 ((101, 0.0), ("end", {})),
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "typecenter", "ABOUT 66 NAMES"),                                # from frame 1 (LEAD = 0.8 s)
 (0, "nobody", "under", "THE CRIME WAS NEVER PROVEN"),
 (1, 0.0, "badge", "SUN 22 JUL 1979"),
 (2, "guards", "under", "ONE BY ONE, WALKED OUT OF THE HALL"),
 (3, 0.0, "under", "AS DESCRIBED BY THE FBI AGENT WHO WATCHED THE TAPE"),
 (1, "saddam", "nameplate", ("SADDAM HUSSEIN", "PRESIDENT OF IRAQ FOR 6 DAYS  ·  CARD: U.S. MOST-WANTED DECK, 2003")),
 (4, "tariq", "nameplate", ("TARIQ AZIZ", "IN THE HALL  ·  LATER IRAQ'S FOREIGN MINISTER  ·  PHOTO 1984")),
 (4, "ali", "nameplate", ("ALI HASSAN AL-MAJID", "IN THE HALL  ·  LATER CALLED “CHEMICAL ALI”  ·  PHOTO 2004")),
 (6, 0.0, "typecenter", "WE WON'T SHOW YOU THE FILM"),
 (8, "saw", "under", "WHAT THE AMERICANS SAW"),
 (8, "admitted", "under", "WHAT SADDAM ADMITTED"),
 (8, "question", "under", "AND THE QUESTION NOBODY CAN ANSWER"),
 (9, 0.0, "badge", "MON 16 JUL 1979  ·  8:40 PM"),
 (10, 0.2, "under", "AHMED HASSAN AL-BAKR  ·  PRESIDENT SINCE 1968"),
 (11, 0.0, "badge", "16 JUL  ·  9:09 PM"),
 (14, 0.0, "brand", None),                                          # the 2 s channel stamp, over moving footage, voice keeps going
 (15, 0.0, "badge", "THU 12 JUL 1979"),
 (16, 0.2, "nameplate", ("MUHYI ABD AL-HUSSEIN MASHHADI", "SECRETARY OF THE RULING COUNCIL  ·  NO SAFE PHOTO OF HIM EXISTS")),
 (16, "vote", "typecenter", "A VOTE"),
 (21, 0.0, "under", "“THIS INFORMATION IS NOT CORRECT”  ·  SADDAM TO THE FBI, 2004"),
 (22, "remember", "typecenter", "REMEMBER THE TAPE"),
 (24, "remember", "typecenter", "REMEMBER SYRIA"),
 (25, 0.0, "badge", "FRI 20 JUL 1979"),
 (27, 0.3, "under", "AL-KHULD HALL  ·  WEST BANK OF THE TIGRIS"),
 (27, "khuld", "badge", "SUN 22 JUL 1979"),
 (38, 0.2, "under", "AL-AHRAM, CAIRO  ·  5 AUGUST 1979"),
 (38, "every", "quote", ("“...the person stood up in fear...”", "AL-AHRAM, CAIRO, 5 AUG 1979  ·  AS TRANSLATED BY THE U.S. GOVERNMENT")),
 (39, "session", "quote", ("“This session is also being videotaped.”", "SADDAM, AS QUOTED BY AL-AHRAM")),
 (41, 0.0, "under", "MYTH OR RECORD"),
 (41, "real", "stamp", ("RECORD", 1260, 400)),
 (42, 0.0, "under", "MYTH: SHOT IN THE COURTYARD THAT DAY"),
 (42, "courtyard", "stamp", ("17 DAYS LATER", 1240, 400)),
 (43, 0.2, "under", "NO U.S. EMBASSY SINCE 1967  ·  A SMALL INTERESTS SECTION"),
 (44, 0.0, "badge", "TUE 24 JUL  ·  1:29 PM"),
 (46, 0.2, "under", "ADNAN HUSSEIN  ·  DEPUTY PRIME MINISTER"),
 (48, 0.0, "badge", "WED 25 JUL  ·  5:35 PM"),
 (52, 0.2, "under", "OVER 2,000 HELD  ·  A SECOND-HAND REPORT"),
 (54, 0.0, "badge", "SAT 28 JUL  ·  8:40 PM"),
 (58, "never", "stamp", ("NEVER NAMED", 1240, 400)),
 (59, 0.2, "under", "A SPECIAL COURT OF 7  ·  CHAIRMAN: NA'IM HADDAD"),
 (61, 0.0, "badge", "WED 1 AUG 1979"),
 (63, 0.0, "badge", "TUE 7 AUG  ·  8:30 PM"),
 (64, 0.0, "list", ["22  ·  DEATH BY FIRING SQUAD", "33  ·  PRISON", "13  ·  ACQUITTED"]),
 (66, 0.0, "badge", "WED 8 AUG 1979"),
 (67, "twenty|21", "typecenter_red", "21 SHOT"),
 (68, 0.2, "under", "AHMAD DHANNUN KARIM  ·  SENTENCED IN HIS ABSENCE"),
 (69, 0.0, "badge", "8 AUG  ·  6:00 PM"),
 (73, 0.0, "typecenter", "ONE MAN FROM EVERY BRANCH"),
 (74, 0.0, "badge", "4 FEB 1980"),
 (76, 0.2, "under", "8 AUG 1979  ·  A MASS RALLY IN BAGHDAD"),
 (77, "forget", "under", "“FORGET ABOUT THE LAW”  ·  U.S. INTERESTS SECTION, 16 AUG 1979"),
 (78, 0.2, "under", "THE AMNESTY, 16 AUG 1979  ·  NOT FOR THE SPECIAL COURT'S PRISONERS"),
 (76, 0.5, "subpop", None),                                        # silent ask at ~77%, right after the payoff (LESSONS 37)
 (81, 0.0, "typecenter", "THE ACT OF ASKING"),
 (82, 0.0, "under", "MYTH OR RECORD: A SYRIAN PLOT?"),
 (83, 0.2, "quote", ("“...it is possible that there was no foreign" + chr(10) + "involvement in the alleged plot...”", "STATE DEPARTMENT INTELLIGENCE SUMMARY, 31 JULY 1979")),
 (85, "never|proven", "stamp", ("NEVER PROVEN", 1240, 400)),
 (86, "december", "badge", "13 DEC 2003"),
 (87, 0.0, "badge", "FRI 20 FEB 2004"),
 (94, 0.0, "typecenter", "WHAT NOBODY KNOWS"),
 (96, 0.2, "under", "BAGHDAD CABLE 1711, 9 AUG 1979  ·  TEXT WITHHELD"),
 (97, "khuld|hall", "under", "AL-KHULD HALL TODAY: UNCONFIRMED"),
 (99, 0.0, "typecenter", "EVERY MEMBER GOT A COPY"),
 (100, 0.0, "under", "WAS THERE EVER A PLOT?  TELL ME BELOW"),
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
            L.text(c, "FILE 10  ·  AL-KHULD HALL  ·  JULY 1979", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
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
CAPFIX = {"Al": "al", "Muhi": "Muhyi", "Abdul": "Abd al-", "Mashahadi": "Mashhadi", "Majub": "Mahjub", "Tannoun": "Dhannun", "backstabbed": "back-stabbed",
          (9, "Ahmad"): "Ahmed", (34, "high"): "Himaya", (34, "maya"): "", (43, "U"): "U.S.", (43, ".S."): "", (43, "interest"): "interests",
          (67, "were"): "are"}                                                 # whisper spellings -> the record's (core word; punctuation kept; "" drops it)
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
        c = L.vignette(L.kenburns(blur_bg("C6", None), t, t0, t1))
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
RADIO = {"A1", "A6"}
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
    music("Thunder Dreams.mp3", 0.0, tl(9), -20); music("Industrial Cinematic.mp3", tl(9), tl(28), -21); music("Man Down.mp3", tl(28), tl(43), -21)
    music("Rising Tide.mp3", tl(43), tl(61), -21); music("Thunder Dreams.mp3", tl(61), tl(76), -20); music("Promises to Keep.mp3", tl(76), tl(94), -21)
    music("Thunder Dreams.mp3", tl(94), DUR, -20)
    loop("roomtone_dark_cinematic", 0.0, tl(9), -30); loop("wind_cold_interior", tl(28), tl(43), -33); loop("ambience_cinematic_suspense", tl(66), tl(76), -31)
    loop("wind_deep_cinematic_hum", tl(94), tl(101), -31)
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
    EV = [(2, "guards", "footsteps_tunnel_loop", -27), (3, 0.0, "heavy_sliding_door", -26), (6, 0.0, "radio_static_crackles", -28),
          (7, 0.0, "typewriter_typing_old", -22), (11, 0.0, "radio_static_fx", -28), (16, "vote", "hit_short_bass", -18),
          (19, "picked", "prison_metal_door_close", -24), (25, "broke", "hit_glass_suspense", -20), (27, "khuld", "hit_cinematic_deep_impact", -15),
          (34, "himaya|guards", "footsteps_tunnel_loop", -27), (37, "cry", "heartbeat_single", -18), (45, 0.0, "typewriter_typing_old", -22),
          (48, "secret|cable", "typewriter_return_bell", -20), (55, "plot", "hit_short_bass", -18), (64, 0.0, "hit_horror_drum", -16),
          (67, "shot", "hit_deep_heartbeat_impact", -14), (69, 0.0, "radio_static_fx", -26), (75, "questions", "typewriter_return_bell", -20),
          (81, 0.0, "hit_cinematic_deep_impact", -15), (86, "december", "helicopter_far_away", -28), (93, "scared", "hit_deep_heartbeat_impact", -14),
          (101, 0.2, "typewriter_return_bell", -18)]
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
    name = name or "TheLastHours_10_KhuldHall.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "Sunday: the names"), (9, "Monday, July 16: the new president"), (15, "July 12: one man asks for a vote"), (25, "July 20: the tape"),
      (28, "July 22: al-Khuld Hall"), (43, "The Americans find out"), (54, "July 28: \"a plot\""), (61, "The court"), (66, "August 8"),
      (76, "After"), (82, "Myth: a Syrian plot?"), (86, "2004: the FBI asks"), (94, "What nobody knows")]

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

