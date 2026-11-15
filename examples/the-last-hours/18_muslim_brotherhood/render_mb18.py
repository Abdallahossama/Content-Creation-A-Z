"""The Last Hours #18: Hassan al-Banna's last hours, Cairo, Saturday 12 February 1949 (about 8:30 p.m.: two men open fire as he gets into a
taxi outside the Young Men's Muslim Association; just after midnight he dies at Qasr al-Aini hospital), told as the story of who the Muslim
Brotherhood were: six workmen in a canal town (1928), hundreds of thousands of members and a secret wing (1940s), the 1948 killings, the trial
that traced the getaway car to the Interior Ministry (1954), and why the name is in a US Senate race (2026). The File Keeper, 1920x1080.
Real images only: PD-Egypt photographs, Library of Congress (Matson), Nationaal Archief (CC0), KITLV and Wellcome (CC BY 4.0), US government
(PD), Universal Newsreel (PD), 1948-49 US newspapers, Pexels textures labelled ILLUSTRATIVE. Never shown: the shooting, any body, any woman.
Owner rules: research/research.md (do-not-say list 11), research/assets.md.
  uv run --no-project --with pillow --with numpy --with soundfile python render_mb18.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
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

ROOT = "D:/why habibi/_newchannel/18_muslim_brotherhood/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; MUS = "D:/why habibi/_music_library/"
LEAD = 0.8; TAIL = 5.0                                   # the File Keeper end card runs under the sign-off
NEXT = os.environ.get("LH_NEXT", "")
ENDL = 70                                                # the File Keeper sign-off line (the end card runs under it)                     # the next file named on the end card (empty: subscribe line)

# ------------------------------------------------------------------ narration timing (exact-zero gaps)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
VOF = os.environ.get("LH_VOF", ROOT + "vo/mb_vo_chatterbox.wav")
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
def isdoc(rid): return re.fullmatch(r"N\d+[ab]?|A9", rid) is not None                    # the newspaper pages and the 1947 clipping stay paper-toned
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
V_EGYPT, V_REGION, V_MIDEAST = (31.4, 30.6, 4.4), (33.2, 30.9, 8.0), (34.0, 31.6, 13.0)

# ------------------------------------------------------------------ shot constructors
CROP = {"A21": (0.0, 0.12, 0.64, 0.95), "A5": (0.0, 0.17, 1.0, 1.0), "A24": (0.0, 0.0, 1.0, 0.86), "A13": (0.05, 0.08, 0.95, 0.92), "A15": (0.07, 0.04, 0.95, 0.96),
        "A16": (0.05, 0.05, 0.95, 0.95), "A17": (0.05, 0.05, 0.95, 0.95), "A50": (0.525, 0.03, 0.82, 0.75)}      # A5: burned-in caption; A24: watermark; Matson plate borders
PDE, MAT, NA, ILL = "PD-EGYPT", "LIBRARY OF CONGRESS, MATSON COLLECTION", "NATIONAAL ARCHIEF, CC0", "ILLUSTRATIVE  ·  PEXELS"
TB = {"A1": f"HASSAN AL-BANNA  ·  {PDE}", "A2": f"HASSAN AL-BANNA, FROM AL-ZIRIKLI'S “AL-A'LAM” (1958)  ·  {PDE}",
      "A3": f"BANNA AT A RECEPTION, CONTINENTAL HOTEL, CAIRO, 1947  ·  ELTAHER COLLECTION, {PDE}", "A4": f"BANNA AMONG FOLLOWERS  ·  {PDE}",
      "A5": f"BANNA WITH FOLLOWERS, 1935  ·  {PDE}", "A6": f"A GATHERING WITH BANNA  ·  {PDE}", "A7": f"MAKRAM EBEID WITH BANNA, 1945  ·  AL-AHRAM, {PDE}",
      "A8": f"BROTHERHOOD ROVER SCOUTS, 1940s  ·  {PDE}", "A9": f"A 1947 PRESS CLIPPING: THE SCOUTS IN THE CHOLERA CAMPAIGN  ·  {PDE}",
      "A10": f"SUEZ CANAL COMPANY OFFICE, ISMAILIA (POSTCARD)  ·  CAIRO POSTCARD TRUST / AUC, {PDE}", "A11": "CANAL COMPANY OFFICE, ISMAILIA  ·  KITLV / LEIDEN UNIVERSITY LIBRARIES, CC BY 4.0",
      "A13": f"A SHIP ON THE CANAL AT ISMAILIA, 1930s  ·  {MAT}", "A15": f"DREDGERS ON THE CANAL BANK, ISMAILIA  ·  {MAT}",
      "A16": f"ISMAILIA FROM THE AIR, 1932  ·  {MAT}", "A17": f"ISMAILIA'S WATERFRONT FROM THE AIR, 1932  ·  {MAT}",
      "A19": "ISMAILIA  ·  KITLV / LEIDEN UNIVERSITY LIBRARIES, CC BY 4.0", "A21": f"A CAIRO STREET, APRIL 1946  ·  WILLEM VAN DE POLL / {NA}",
      "A22": f"CAIRO AFTER STUDENT RIOTS, NOVEMBER 1946  ·  ANEFO / {NA}", "A24": f"A CONFERENCE AT THE YMMA HEADQUARTERS, CAIRO, 1930  ·  ELTAHER COLLECTION, {PDE}",
      "A25": "QASR AL-AINI HOSPITAL, 19TH-CENTURY PRINT  ·  WELLCOME COLLECTION, CC BY 4.0", "A26": f"KING FAROUK  ·  RIAD SHEHATA / {MAT}",
      "A27": "PRESIDENT ROOSEVELT AND KING FAROUK, 13 FEB 1945  ·  US NATIONAL ARCHIVES", "A28": f"KING FAROUK WITH HIS MINISTERS  ·  RIAD SHEHATA / BIBLIOTHECA ALEXANDRINA, {PDE}",
      "A29": f"KING FAROUK  ·  {PDE}", "A30": f"MAHMOUD AL-NUQRASHI, 1924  ·  AL-MUSAWWAR, {PDE}", "A32": f"IBRAHIM ABDEL HADI, 30 DEC 1948  ·  ANEFO / {NA}",
      "A35": f"GAMAL ABDEL NASSER  ·  BIBLIOTHECA ALEXANDRINA, {PDE}", "A36": f"SAYYID QUTB  ·  {PDE}", "A37": f"QUTB AT HIS TRIAL, 1966  ·  {PDE}",
      "A39": f"UMAR AL-TILMISANI  ·  {PDE}", "A42": f"ANWAR SADAT, 1981  ·  ANEFO / {NA}", "A45": "PRESIDENT MORSI AND US DEFENSE SECRETARY PANETTA, 31 JUL 2012  ·  US DOD",
      "A46": "MOHAMED MORSI, MAY 2013  ·  WILSON DIAS / AGÊNCIA BRASIL, CC BY 3.0 BR", "A50": "ABDUL EL-SAYED AT A SENATE HEARING, JULY 2024  ·  U.S. SENATE", "A50c": "ABDUL EL-SAYED, SENATE HEARING, JULY 2024 (BACKGROUND REMOVED)  ·  U.S. SENATE",
      "A51": "MICHIGAN STATE CAPITOL, LANSING  ·  CAROL M. HIGHSMITH / LIBRARY OF CONGRESS", "A52": "THE U.S. CAPITOL AT DAWN  ·  ARCHITECT OF THE CAPITOL",
      "A53": "THE U.S. CAPITOL  ·  ARCHITECT OF THE CAPITOL", "A54": "U.S. STATE DEPARTMENT, 2024  ·  U.S. DEPARTMENT OF STATE",
      "A55": "U.S. TREASURY  ·  CAROL M. HIGHSMITH / LIBRARY OF CONGRESS", "H1": "THE MUSLIM BROTHERHOOD'S EMBLEM  ·  SHOWN AS A HISTORICAL RECORD",
      "N1a": "WILMINGTON NEWS-JOURNAL (OHIO), TUE 28 DEC 1948, P. 1  ·  AP", "N1b": "WILMINGTON NEWS-JOURNAL, 28 DEC 1948  ·  AP",
      "N2a": "MONROE MORNING WORLD (LOUISIANA), SUN 13 FEB 1949  ·  AP", "V2b": "NASSER, ALEXANDRIA, JULY 1956  ·  UNIVERSAL NEWSREEL",
      "V2c": "ALEXANDRIA, JULY 1956  ·  UNIVERSAL NEWSREEL"}
for _r in ("T1", "T2", "T3", "T4", "T5", "T6"): TB[_r] = ILL
def DT(rid):
    m = re.match(r"([AN]\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD, 1949")
def KB(rid, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, tag=None, dim=0.0): return ("kb", dict(rid=rid, crop=crop or CROP.get(rid), z=z, c0=c0, c1=c1 or c0, tag=tag or TB.get(rid), dim=dim))
def KBP(rid, crop=None, h=880, rot=-1.5, tag=None, x=0.5): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid), x=x))
def TCARD(big, sub, bg): return ("tcard", dict(big=big, sub=sub, bg=bg))
def NMAP(view, ops=(), z=(1.0, 1.06), c0=(0.5, 0.5), c1=None): return ("nmap", dict(view=view, ops=list(ops), z=z, c0=c0, c1=c1 or c0))
def COUNTER(steps, sub, bg, red=False, size=420): return ("counter", dict(steps=steps, sub=sub, bg=bg, red=red, size=size))
def DOC(rid, marks, zoom=1.0, tag=None): return ("doc", dict(rid=rid, marks=marks, zoom=zoom, tag=tag or DT(rid)))
CROPV = {}
LIFT = {"T3": 0.4, "T4": 0.45, "T5": 0.55}                     # gamma: below 1 lifts the night clips (QA 31 Oct: they read as black)                     # gamma: below 1 lifts the dark clips (LESSONS 34)
def VID(rid, at=0.0, speed=1.0, look="grade", z=(1.0, 1.06), c=(0.5, 0.5), crop=None, tag=None, dim=0.0):
    return ("vid", dict(rid=rid, at=at, speed=speed, look=look, z=z, c=c, crop=crop or CROPV.get(rid), tag=tag or TB.get(rid), dim=dim, lift=LIFT.get(rid)))
def GHOST(bg, fg, crop, z=(1.0, 1.08), tag=None): return ("ghost", dict(bg=bg, fg=fg, crop=crop, z=z, tag=tag))
def VIDP(rid, at=0.0, speed=1.0, h=560, bg="C10", tag=None): return ("vidp", dict(rid=rid, at=at, speed=speed, h=h, bg=bg, tag=tag or TB.get(rid)))

MAHMUDIYYA, CAIRO, ISMAILIA = (30.53, 31.18), (31.24, 30.05), (32.27, 30.60)
PALESTINE, BEIRUT, AMMAN = (34.9, 31.6), (35.50, 33.89), (35.93, 31.95)
SHOTS = [
 # COLD OPEN
 (0, KBP("A2", h=900, rot=0.0, x=0.79)),
 ((0, "night|lose"), KB("T6", z=(1.2, 1.3), c0=(0.35, 0.45))),
 ((0, "police|chief"), KB("A21", z=(1.04, 1.14), dim=0.2)),
 (1, TCARD("8:30 PM", "Saturday, 12 February 1949  ·  Cairo", "A21")),
 (2, KB("T6", z=(1.1, 1.25), c0=(0.5, 0.55))),
 ((2, "owner|hassan"), KBP("A1", h=900, rot=-1.0)),
 ((2, "ambulance|building"), KBP("A24", h=640, rot=1.2)),
 (3, KBP("A8", h=560)),
 ((3, "week|this"), KB("A52", z=(1.04, 1.12))),
 ((3, "candidate|abdul|sayed"), KBP("A50c", h=780, rot=-1.2)),
 (4, KB("A21", z=(1.06, 1.16), c0=(0.55, 0.55), dim=0.3)),                   # no text over the newspaper (the under band runs here)
 ((4, "record|claim"), KB("A51", z=(1.04, 1.12))),
 # 9 A.M. -> THE BEGINNING
 (5, TCARD("9:00 AM", "Saturday, 12 February 1949  ·  the Prime Minister's house", "A32")),
 ((5, "prime|minister"), KB("A32", z=(1.04, 1.14), c0=(0.5, 0.35))),
 (6, KBP("A1", h=900, rot=1.0)),
 (7, NMAP(V_EGYPT, ops=[("pin", *MAHMUDIYYA, "MAHMUDIYYA  ·  1906", 0.2), ("pin", *CAIRO, "CAIRO", -9)])),
 (8, KBP("A6", h=760)),
 (9, NMAP(V_EGYPT, ops=[("pin", *CAIRO, "CAIRO", -9), ("route", [CAIRO, (31.8, 30.45), ISMAILIA], 0.4, 1.6), ("pin", *ISMAILIA, "ISMAILIA  ·  1927", 1.8)])),
 ((9, "account|exactly"), KB("A16", z=(1.04, 1.14))),
 (10, KB("A13", z=(1.04, 1.12))),
 ((10, "company"), KBP("A10", h=620)),
 ((10, "british|bases"), KB("A15", z=(1.04, 1.12))),
 ((10, "signs|language"), KB("A19", z=(1.04, 1.14))),
 (11, KBP("A5", h=560)),
 (12, KB("A17", z=(1.04, 1.12), dim=0.45)),
 (13, KBP("A6", h=760, x=0.74)),
 (14, KBP("H1", h=500, rot=0.0)),
 (15, KB("A11", z=(1.04, 1.14))),
 ((15, "five|500"), COUNTER([((15, "five|500"), "£E500")], "FROM THE SUEZ CANAL COMPANY  ·  FOR THE FIRST MOSQUE", "A10", size=380)),
 # 1 P.M. -> HOW BIG IT GOT, AND THE SECRET WING
 (16, TCARD("1:00 PM", "A messenger finds him at lunch  ·  meeting at five", "A21")),
 ((16, "telephone"), KBP("A2", h=900, rot=1.2)),
 (17, KBP("A8", h=620, rot=1.5)),
 (18, KBP("A9", h=880)),
 ((18, "fifteen|15"), COUNTER([((18, "fifteen|15"), "15"), ((18, "thousand|1,000|1000"), "1,000+"), ((18, "hundreds"), "100,000s")],
                            "BRANCHES 1933 → 1944  ·  MEMBERS: ESTIMATES OF THE TIME", "A19", size=360)),
 (19, KBP("A28", h=560, x=0.74)),
 (20, KB("A21", z=(1.12, 1.22), c0=(0.5, 0.6), dim=0.2)),
 ((20, "revolver|test"), VID("T3", at=8.0)),
 (21, NMAP(V_REGION, ops=[("pin", *CAIRO, "CAIRO", -9), ("arrow", CAIRO, PALESTINE, "VOLUNTEERS  ·  1948", 0.3)])),
 ((21, "killings|home"), KB("A22", z=(1.04, 1.12), dim=0.2)),
 (22, KBP("A3", h=560)),
 ((22, "people|close|feared"), KBP("A2", h=900, rot=-1.0)),
 (23, VID("T2", at=2.0)),
 (24, TCARD("11:00 PM", "Wednesday, 8 December 1948  ·  the radio", "A28")),
 ((24, "radio|announces"), VID("T1", at=1.0)),
 ((24, "except|one"), KBP("A1", h=900)),
 (25, KBP("A2", h=900, rot=1.5)),
 (26, KBP("A30", h=860)),
 ((26, "opens|fire|uniform"), KBP("N1a", h=520, rot=-1.0)),
 ((26, "gunman|student"), KBP("N1b", h=960, rot=1.5)),
 (27, KB("A21", z=(1.08, 1.18), dim=0.25)),
 (28, VID("T2", at=3.0)),
 # THE LAST HOURS
 (29, TCARD("5:00 PM", "The Young Men's Muslim Association  ·  Queen Nazli Street", "A24")),
 ((29, "brother|mansour"), KBP("A24", h=640)),
 (30, KBP("A1", h=900, x=0.74)),
 (31, KBP("A3", h=560, x=0.74)),
 ((31, "nobody|moves"), KBP("A24", h=640)),
 (32, VID("T5", at=1.0, crop=(0.0, 0.25, 1.0, 0.565))),
 (33, TCARD("7:45 PM", "A police colonel gives his driver an order", "A21")),
 ((33, "colonel"), KB("A21", z=(1.15, 1.25), c0=(0.4, 0.5), dim=0.45)),
 ((33, "wait|building"), VID("T4", at=3.0)),
 (34, KB("T6", z=(1.04, 1.14))),
 (35, KB("A21", z=(1.05, 1.2), c0=(0.5, 0.55), dim=0.3)),
 ((35, "what|time"), VID("T3", at=20.0)),
 (36, COUNTER([((36, "moon"), "99%")], "THE MOON OVER CAIRO THAT NIGHT  ·  COMPUTED", "A21", size=420)),
 (37, TCARD("8:30 PM", "Queen Nazli Street  ·  two men open fire", "A21")),
 (38, ("midask", dict(bg="A21", ln=38))),                          # the spoken mid-video ask (cliffhanger: the shots)
 (39, VID("T3", at=5.0)),
 ((39, "shouts|number"), COUNTER([((39, "nine|9"), "9979")], "THE GETAWAY CAR  ·  SHOUTED BY A BOY NOBODY EVER FOUND", "A21", size=420)),
 (40, KBP("A24", h=640)),
 (41, KBP("A24", h=640, rot=1.5)),
 ((41, "told|shot"), KB("A21", z=(1.1, 1.2), c0=(0.6, 0.5), dim=0.3)),
 (42, TCARD("8:45 PM", "The meter still running  ·  16 piastres", "T6")),
 (43, KB("A25", z=(1.04, 1.12))),
 (44, COUNTER([((44, "copies|already"), "~5,000")], "COPIES ALREADY ON THE STREET  ·  AS ONE INVESTIGATION TELLS IT", "A9", size=380)),
 (45, TCARD("MIDNIGHT", "Sunday, 13 February 1949  ·  Hassan al-Banna dies, aged 42", "A1")),
 (46, KBP("N2a", h=960, rot=-1.2)),
 (47, KB("A21", z=(1.15, 1.25), c0=(0.4, 0.5), dim=0.25)),
 (48, KBP("A7", h=760)),
 # WHO GAVE THE ORDER: THE TRIAL
 (49, KB("A26", z=(1.04, 1.14), c0=(0.5, 0.3))),
 ((49, "army|overthrows"), KBP("A35", h=860)),
 (50, COUNTER([((50, "nine|9979|car"), "9979")], "RENTED BY THE INTERIOR MINISTRY  ·  FOR ITS CHIEF OF CRIMINAL INVESTIGATION", "A28", size=420)),
 (51, KBP("A28", h=560, x=0.74)),
 (52, KBP("A29", h=860, x=0.74)),
 (53, KB("A27", z=(1.04, 1.12), dim=0.35)),
 # AFTER THE FILE
 (54, VID("V2b", at=0.2)),
 (55, KBP("A36", h=760)),
 (56, KB("A42", z=(1.04, 1.12))),
 ((56, "eighty|88"), COUNTER([((56, "eighty|88"), "88 SEATS")], "PARLIAMENT, 2005  ·  AS INDEPENDENTS", "A39", size=330)),
 (57, KBP("A46", h=860)),
 ((57, "army|removes"), KB("A45", z=(1.04, 1.12))),
 # 2026
 (58, KB("A52", z=(1.03, 1.1))),
 (59, KB("A55", z=(1.04, 1.12))),
 ((59, "lebanon|jordan"), NMAP(V_MIDEAST, ops=[("pin", *BEIRUT, "LEBANON", 0.1), ("pin", *AMMAN, "JORDAN", 0.4), ("pin", *CAIRO, "EGYPT", 0.7)])),
 ((59, "said|fight"), KB("A54", z=(1.04, 1.12))),
 (60, KB("A51", z=(1.04, 1.12))),
 ((60, "abdul|el-sayed|sayed"), KBP("A50c", h=780, rot=-1.2)),
 (61, KB("A53", z=(1.04, 1.12), dim=0.3)),
 ((61, "pointed|donations"), KB("A51", z=(1.1, 1.18), dim=0.35)),
 (62, KB("A52", z=(1.1, 1.18), dim=0.35)),
 (63, KBP("A50c", h=860, rot=1.0, x=0.74)),
 (64, KB("A53", z=(1.1, 1.18), dim=0.4)),
 (65, KB("A51", z=(1.08, 1.14), dim=0.2)),
 # WHAT THE RECORD SHOWS + ASKS
 (66, KB("A21", z=(1.03, 1.1), dim=0.3)),
 (67, KB("A17", z=(1.04, 1.12))),
 ((67, "hundreds"), KBP("A8", h=560)),
 ((67, "prime|minister"), KBP("A30", h=860)),
 ((67, "founder"), KBP("A2", h=900)),
 ((67, "interior|ministry|getaway"), KB("A21", z=(1.1, 1.2), dim=0.3)),
 (68, KBP("H1", h=520, rot=0.0)),
 (69, KBP("A2", h=900, rot=0.5)),
 ((ENDL, -0.7), ("end", {})),                                    # the File Keeper end card under the sign-off
]
SHOTS.sort(key=lambda s: KT(s[0]))
SHOT_T = [KT(s[0]) for s in SHOTS]; SHOT_T[0] = 0.0          # the cold open owns frame 1

OV = [
 (0, -0.8, "hookleft", ("1928: HE FOUNDED IT.", "1949: SHOT IN CAIRO.")),   # from frame 1 (LEAD = 0.8 s)
 (0, "how", "under", "THE GETAWAY CAR WAS RENTED FOR A POLICE CHIEF  ·  HOW?"),
 (1, 0.0, "badge", "SAT 12 FEB 1949"),
 (2, 0.3, "under", "ILLUSTRATIVE  ·  16 PIASTRES ON THE METER"),
 (2, "owner|hassan", "nameplate", ("HASSAN AL-BANNA", "42  ·  FOUNDER OF THE MUSLIM BROTHERHOOD")),
 (3, "candidate|abdul|sayed", "nameplate", ("ABDUL EL-SAYED", "DEMOCRATIC NOMINEE, U.S. SENATE, MICHIGAN")),
 (3, "says|none", "under", "HE SAYS HE HAS NO TIES TO THE GROUP"),
 (4, 0.2, "under", "WHO FIRED  ·  WHOSE CAR  ·  THE NUMBER  ·  THE CLAIM"),
 (5, 0.0, "brand", None),                                          # the File Keeper stamp, over moving footage, voice keeps going
 (5, "prime|minister", "nameplate", ("IBRAHIM ABDEL HADI", "PRIME MINISTER SINCE 28 DEC 1948")),
 (6, 0.3, "under", "GO BACK TO 1906"),
 (7, "father|watches", "under", "HIS FATHER: IMAM, TEACHER, WATCH REPAIRER"),
 (8, 0.3, "under", "DAR AL-ULUM, CAIRO  ·  A COLLEGE FOR TEACHERS"),
 (10, "signs|language", "under", "“THE LANGUAGE OF THE OCCUPATION”  ·  HIS MEMOIR"),
 (12, 0.2, "badge", "MARCH 1928"),
 (12, "carpenter", "list", ("SIX MEN:", "A CARPENTER  ·  A BARBER", "AN IRONER  ·  A DRIVER", "A GARDENER  ·  A BICYCLE REPAIRMAN")),
 (13, "nothing|offer", "quoteL", ("“We have nothing to offer except our blood, our lives," + chr(10) + "our faith… and these few coins.”", "THE SIX, AS BANNA TELLS IT IN HIS MEMOIR")),
 (14, "brothers|muslim", "under", "“WE ARE THE MUSLIM BROTHERS”  ·  THE EMBLEM CAME LATER"),
 (16, 0.0, "badge", "SAT 12 FEB  ·  1:00 PM"),
 (16, "telephone", "under", "HIS PHONE LINE HAD BEEN CUT  ·  FAMILY ACCOUNT"),
 (19, "danger|serious", "quoteL", ("“the most serious danger to public security”", "BRITISH INTELLIGENCE, 1941")),
 (20, "special|apparatus", "typecenter_red", "THE SPECIAL APPARATUS"),
 (22, 0.0, "badge", "MON 22 MAR 1948"),
 (22, 0.3, "under", "JUDGE AHMED AL-KHAZINDAR  ·  SHOT OUTSIDE HIS HOME"),
 (23, 0.0, "badge", "NOVEMBER 1948"),
 (23, 0.3, "under", "THE JEEP CASE  ·  CAIRO"),
 (24, 0.0, "badge", "WED 8 DEC 1948  ·  11:00 PM"),
 (25, 0.3, "under", "BANNA, AS THE HISTORIAN RICHARD MITCHELL RECORDS IT"),
 (26, 0.0, "badge", "TUE 28 DEC 1948  ·  ~10 AM"),
 (26, 0.3, "nameplate", ("MAHMOUD AL-NUQRASHI", "PRIME MINISTER OF EGYPT")),
 (27, 0.3, "under", "AT NUQRASHI'S FUNERAL, CAIRO"),
 (28, 0.0, "badge", "JANUARY 1949"),
 (28, "neither|brothers", "quote", ("“Neither Brothers nor Muslims.”", "BANNA, ON THE COURTHOUSE BOMBERS")),
 (29, 0.0, "badge", "SAT 12 FEB  ·  5:00 PM"),
 (29, "brother|mansour", "under", "WITH HIS BROTHER-IN-LAW, ABDEL KARIM MANSOUR"),
 (30, "lives|hands", "quoteL", ("“Our lives are in God's hands.”", "BANNA, AS HIS FAMILY TELLS IT")),
 (31, "names|weapons", "listL", ("THE GOVERNMENT WANTS:", "NAMES  ·  WEAPONS  ·  THE SECRET RADIO", "BANNA WANTS:", "HIS MEN RELEASED FIRST")),
 (32, 0.0, "badge", "5:40 PM  ·  SUNSET"),
 (33, 0.0, "badge", "SAT 12 FEB  ·  7:45 PM"),
 (33, "wait|building", "quote", ("“If two men in traditional clothes get in," + chr(10) + "bring them to me, at the Eden Hotel.”", "THE COLONEL'S ORDER, IN HIS DRIVER'S CONFESSION")),
 (33, "colonel", "nameplate", ("COL. MAHMOUD ABDEL MAGID", "HEAD OF CRIMINAL INVESTIGATION  ·  NO SAFE PHOTO")),
 (34, 0.0, "badge", "~8:00 PM"),
 (34, 0.3, "under", "ILLUSTRATIVE"),
 (35, "comment|everything", "quote", ("“You comment on everything.”", "BANNA, AS HIS BROTHER-IN-LAW REMEMBERED IT")),
 (37, 0.0, "badge", "~8:30 PM"),
 (40, 0.3, "under", "BACK INTO THE YMMA, CALLING FOR AN AMBULANCE"),
 (41, "asked|word", "typecenter_red", "“DEAD?”"),
 (42, 0.0, "badge", "8:45 PM"),
 (43, 0.3, "under", "QASR AL-AINI HOSPITAL  ·  19TH-CENTURY PRINT"),
 (43, "family|bleed", "under", "THE FAMILY'S CLAIM  ·  NO COURT EVER RULED ON IT"),
 (46, 0.0, "badge", "SUN 13 FEB  ·  1:00 AM"),
 (47, 0.3, "under", "THE FATHER'S ACCOUNT  ·  NO IMAGES"),
 (48, 0.3, "nameplate", ("MAKRAM EBEID", "COPTIC CHRISTIAN POLITICIAN  ·  HERE WITH BANNA, 1945")),
 (49, 0.0, "badge", "JULY 1952"),
 (51, 0.0, "badge", "MON 2 AUG 1954"),
 (51, "gunman|corporal", "listL", ("THE VERDICT:", "THE GUNMAN, A POLICE CORPORAL: LIFE", "THE COLONEL: 15 YEARS", "HIS DRIVER: 15 YEARS")),
 (52, "account|king", "quoteL", ("“…for the account of the King and the government.”", "CAIRO CRIMINAL COURT, 1954")),
 (53, 0.2, "typecenter", "FREED: 1955  ·  1960  ·  1967"),
 (54, 0.0, "badge", "26 OCT 1954"),
 (54, "staged", "under", "THE BROTHERHOOD SAYS IT WAS STAGED"),
 (55, 0.0, "badge", "MON 29 AUG 1966"),
 (55, 0.3, "nameplate", ("SAYYID QUTB", "AUTHOR OF “MILESTONES”")),
 (57, 0.0, "badge", "2012 - 2013"),
 (57, 0.3, "nameplate", ("MOHAMED MORSI", "PRESIDENT OF EGYPT, 2012-2013")),
 (58, 0.2, "typecenter", "2026"),
 (59, 0.0, "badge", "TUE 13 JAN 2026"),
 (60, "abdul|el-sayed|sayed", "nameplate", ("ABDUL EL-SAYED", "DEMOCRATIC NOMINEE, U.S. SENATE, MICHIGAN")),
 (61, "pledged|support", "quote", ("“…pledged his support to the Muslim Brotherhood.”", "MIKE ROGERS, REPUBLICAN NOMINEE, 5 AUG 2026")),
 (61, "politifact|cherry", "under", "POLITIFACT: “CHERRY-PICKING”"),
 (62, "jihadist|member", "quote", ("“…a jihadist Muslim Brotherhood member…”", "PRESIDENT TRUMP, PORT HURON, MICHIGAN, 25 OCT 2026")),
 (63, "never|member", "quoteL", ("“I have never been a member of the Muslim Brotherhood." + chr(10) + "I never will be.”", "ABDUL EL-SAYED, FOX NEWS, 23 OCT 2026")),
 (64, 0.2, "typecenter", "POLITIFACT: “PANTS ON FIRE”"),
 (64, "associated|press", "under", "AP: “NO EVIDENCE” OF ANY AFFILIATION"),
 (65, 0.0, "badge", "TUE 3 NOV 2026"),
 (66, 0.0, "typecenter", "WHAT THE RECORD SHOWS"),
 (69, 0.2, "under", "WHO GAVE THE ORDER?  TELL ME BELOW"),
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

SLOT = {"hookleft": "center", "lower": "bottom", "under": "bottom", "nameplate": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "listL": "center", "quoteL": "center"}
OVT = [OT(ln, off) for ln, off, _, _ in OV]
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    end = shot_t1                                  # the EARLIEST later overlay in the slot wins, whatever its list order
    for j2 in range(len(OV)):
        if OVT[j2] <= OVT[j] or j2 == j: continue
        k2 = OV[j2][2]
        if SLOT.get(k2) == sl or (sl == "bottom" and k2 in ("list", "typecenter", "typecenter_red", "quote", "listL", "quoteL")):
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
        elif kind in ("quote", "quoteL"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay); qs = a[0].split("\n"); qx = W * (0.30 if kind == "quoteL" else 0.5)
            for i, q in enumerate(qs):
                L.text(c, q, qx, H / 2 - 40 - (len(qs) - 1) * 42 + i * 84, 44 if kind == "quoteL" else (50 if NO_BOTTOM and len(q) > 44 else 60), BONE, SER, alpha=ease((t - t0 - 0.25 * i) / 0.4))
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
        if t - t0 < BA.STAMP_LEN: c.alpha_composite(BA.stamp_frame(t - t0, BP.LABEL["mb18"]))
    elif kind == "hookleft":                                   # frame-1 hook text in thumbnail blocks, left, off the face
        f = L.font(COND, 132); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i, s in enumerate(a):
            y = H / 2 - 130 + i * 180; w = f.getlength(s)
            d.rectangle((80, y - 82, 80 + w + 56, y + 82), fill=((0, 0, 0, 230) if i == 0 else (255, 204, 0, 255)))
            d.text((108, y), s, font=f, fill=(BONE + (255,)) if i == 0 else (10, 10, 10, 255), anchor="lm")
        c.alpha_composite(lay)
    elif kind == "subpop":                                     # the File Keeper case tab (no ask: the spoken mid ask does that)
        if t - t0 < BA.PILL_LEN: c.alpha_composite(BA.chip_frame(t - t0, BP.LABEL["mb18"]), (0, BP.PILL_Y))

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
CAPFIX = {"Bana": "Banna", "Banner": "Banna", "Ismailiya": "Ismailia", "Nokrashi": "Nuqrashi", "Nukrashi": "Nuqrashi", "Nookrahshee": "Nuqrashi",
          "Kasr": "Qasr", "Ainy": "Aini", "Mageed": "Magid", "Majid": "Magid", "Kareem": "Karim", "Mansoor": "Mansour", "Ebeyd": "Ebeid", "Obeid": "Ebeid",
          "Kutb": "Qutb", "Qotb": "Qutb", "Nazlee": "Nazli", "Nazly": "Nazli", "Mahmudiya": "Mahmudiyya", "Mahmoudiya": "Mahmudiyya", "El-Syed": "El-Sayed",
          "El-Said": "El-Sayed", "Elsayed": "El-Sayed", "Politifact": "PolitiFact", "piasters": "piastres", (29, "Anna"): "Banna", (4, "gunman"): "gunmen", "5pm": "5 p.m.", (9, "Ismaili"): "Ismailia", (9, "Liya"): "", "Kutb": "Qutb", "8.30": "8:30", "8.45": "8:45", "7.45": "7:45", "5.40": "5:40"}  # whisper spellings -> the record's
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
            sh = tone("A21"); k = max(W / sh.width, H / sh.height); sh = sh.resize((int(sh.width * k) + 1, int(sh.height * k) + 1), Image.LANCZOS)
            sh = sh.crop(((sh.width - W) // 2, (sh.height - H) // 2, (sh.width - W) // 2 + W, (sh.height - H) // 2 + H)).convert("RGB")
            BG["end"] = (sh, Image.blend(sh.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62))
        wl, wsb = wt(ENDL, "like"), wt(ENDL, "subscrib")
        c = BP.end_frame(BG["end"][0], BG["end"][1], t - t0, BP.NEXT["mb18"], caps=[], t_like=(wl - t0) if wl else None, t_sub=(wsb - t0) if wsb else None)
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
    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(16), -17); music("Industrial Cinematic.mp3", tl(16), tl(29), -17)
    music("Man Down.mp3", tl(29), tl(38), -17); music("Thunder Dreams.mp3", tl(39), tl(49), -17); music("Rising Tide.mp3", tl(49), tl(54), -17)
    music("Man Down.mp3", tl(54), tl(58), -18); music("Industrial Cinematic.mp3", tl(58), tl(66), -18); music("Promises to Keep.mp3", tl(66), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("wind_deep_cinematic_hum", tl(29), tl(38), -31); loop("roomtone_dark_cinematic", tl(39), tl(49), -31)
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
    EV = [(0, "night", "sweep_horror_long", -24), (0, "shot", "hit_short_bass", -18), (0, "how", "hit_cinematic_deep_impact", -18),
          (1, 0.0, "clock_tick_single", -20), (2, "ticking", "clock_ticking_closeup", -26), (2, "ambulance", "hit_deep_heartbeat_impact", -20),
          (5, 0.0, "clock_tick_single", -20), (6, "beginning", "whoosh_ghostly", -24), (12, "carpenter", "typewriter_soft_click", -24),
          (14, "oath", "hit_cinematic_deep_impact", -20), (16, 0.0, "clock_tick_single", -20), (20, "secret", "bass_suspense_mystery", -24),
          (22, "shot", "hit_short_bass", -18), (23, "jeep", "metal_tool_drop", -22), (24, "radio", "radio_static_crackles", -26),
          (26, "fire", "hit_big_cinematic_impact", -16), (28, "bomb", "hit_cinematic_deep_impact", -18), (29, 0.0, "clock_tick_single", -20),
          (32, "sunset", "wind_ambience", -30), (33, 0.0, "clock_ticking_closeup", -26), (33, "order", "hit_short_bass", -18),
          (35, "dark", "sweep_terror_darkness", -26), (37, "fire", "hit_big_cinematic_impact", -14), (39, "number", "heartbeat_single", -18),
          (41, "phone", "telephone_old_ring", -26), (41, "dead", "hit_horror_drum", -16), (42, 0.0, "clock_tick_single", -20),
          (44, "presses", "newspaper_drop", -22), (45, "dies", "hit_deep_heartbeat_impact", -16), (46, 0.0, "clock_bells_hour", -26),
          (49, "overthrows", "hit_cinematic_deep_impact", -18), (50, "interior", "hit_horror_drum", -16), (51, "verdict", "paper_signing", -22),
          (52, "king", "hit_short_bass", -18), (55, "hanged", "hit_horror_drum", -18), (58, 0.0, "whoosh_fast_transition", -22),
          (62, "jihadist", "hit_short_bass", -20), (64, "fire", "typewriter_hit", -22), (66, 0.0, "hit_cinematic_deep_impact", -15),
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
    name = name or "TheLastHours_18_MuslimBrotherhood_Banna.mp4"
    with open(B + SEGP + "list.txt", "w") as f:
        for i in range(n): f.write(f"file '{SEGP}{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/" + name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + SEGP + "list.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

CH = [(0, "8:30 PM, Cairo"), (5, "A teacher in a canal town"), (16, "Hundreds of thousands, and a secret wing"), (29, "The last hours"),
      (39, "Car 9979"), (49, "The trial"), (54, "After the file"), (58, "Why this name is in the news"), (66, "What the record shows")]

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

