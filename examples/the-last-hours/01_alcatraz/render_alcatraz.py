"""The Last Hours #1: "The Night 3 Men Vanished From Alcatraz" (Case File style, 1920x1080).
Every shot starts on a narration line (index into vo_lines.txt without '##'); line times come from vo/vo.log
(Chatterbox prints each line's length; pauses are 0.35 s, 0.9 s before a '##').
  python render_alcatraz.py qa <t> <t> ...      contact sheet of frames
  python render_alcatraz.py seg <i> <n>         render segment i of n (video only)
  python render_alcatraz.py audio               mix VO + music + SFX -> build/mix.wav
  python render_alcatraz.py final <n>           concat segments + audio -> export/
  python render_alcatraz.py all <n>"""
import sys, os, re, json, math, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease, clamp01
Image.MAX_IMAGE_PIXELS = None

ROOT = "D:/why habibi/_newchannel/01_alcatraz/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)
SFXD = "D:/why habibi/_newchannel/sfx/"; KSFX = "D:/why habibi/_style_kit/sfx/"; MUS = "D:/why habibi/_music_library/"
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
WORDS = []
if os.path.exists(ROOT + "vo/vo_words2.json"):
    WORDS = [w for sg in json.load(open(ROOT + "vo/vo_words2.json", encoding="utf-8")) for w in sg["words"]]
def wt(line, word, off=0.0):
    """time (video clock) the narrator says `word` inside script line `line`; falls back to the line start"""
    a = T[line] - 0.3; b = (T[line + 1] if line + 1 < len(T) else VO_END) + 0.3
    for w in WORDS:
        t = w["s"] + LEAD
        if a <= t <= b and re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(word.lower()): return t + off
    return T[line] + 0.4 + off

# ------------------------------------------------------------------ assets
PH = json.load(open(M + "docs/phrases.json"))
PH["p115"]["dummy"] = [250, 289, 565, 301]
PH["a25"] = {"stride": [312, 334, 770, 353], "run": [308, 356, 640, 376]}; PH["p116"]["lock"] = [300, 397, 540, 421]
DOCS = {"p115": M + "docs/fbi_part06_p115.png", "p113": M + "docs/fbi_part06_p113.png", "p116": M + "docs/fbi_part06_p116.png",
        "p48": M + "docs/fbi_part05_p48.png", "p44": M + "docs/fbi_part05_p44.png", "p43": M + "docs/fbi_part05_p43.png",
        "p32": M + "docs/fbi_part01_p32.png", "p68": M + "docs/fbi_part01_p68.png", "p87": M + "docs/fbi_part01_p87.png",
        "p92": M + "docs/fbi_part01_p92.png", "a24": M + "album/a-24.pgm", "a25": M + "album/a-25.pgm", "a14": M + "album/a-14.pgm"}
NPSCROP = (0, 0, 1, 0.955)                                   # NPS scans carry a credit strip at the bottom
def P(name): return M + name
IMG = {}
def tone(path, crop=None):
    k = (path, crop)
    if k not in IMG: IMG[k] = L.bw(path, crop)
    return IMG[k]

MAPI = None
def mapimg():
    global MAPI
    if MAPI is None:
        im = Image.open(M + "usgs_bay.png").convert("RGB"); a = np.asarray(im, np.float32) / 255
        lum = a @ np.array([0.3, 0.59, 0.11], np.float32); a = lum[..., None] + (a - lum[..., None]) * 0.35      # faded colour
        a = a * np.array([0.95, 0.93, 0.86], np.float32)                                                      # aged paper
        MAPI = Image.fromarray((a.clip(0, 1) * 255).astype(np.uint8))
    return MAPI
# map points (pixels in usgs_bay.png, 4300x2900)
ALC = (2672, 1850); ALC_NE = (2712, 1828); ANGEL = (2400, 560); BLUNT = (2800, 880); GG = (1090, 2060); HORSE = (1140, 1640)
FTPOINT = (1128, 2420); FTMASON = (2440, 2470); WHIRL = (2930, 1830); PADDLE = (2740, 960); WEST = (-300, 2000)

# ------------------------------------------------------------------ video proxies (B&W, 1080p, 30 fps)
class Vid:
    def __init__(self, name, start, speed, t0):
        self.path = M + f"video/proxy/{name}.mp4"; self.start, self.speed, self.t0 = start, speed, t0; self.p = None; self.n = -1; self.last = None
        self.len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", self.path], capture_output=True, text=True).stdout or 10)
    def frame(self, t):
        want = int(((t - self.t0) * self.speed) * FPS)
        if self.p is None or want < self.n:
            if self.p: self.p.kill()
            ss = self.start + want / FPS
            vf = f"setpts={1 / self.speed:.4f}*PTS,fps=30" if self.speed != 1 else "fps=30"
            self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-stream_loop", "-1", "-ss", f"{ss % max(self.len - 0.2, 1):.3f}", "-i", self.path, "-vf", vf,
                                       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE); self.n = want - 1
        while self.n < want:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            self.last = buf; self.n += 1
        return Image.frombytes("RGB", (W, H), self.last).convert("RGBA") if self.last else Image.new("RGBA", (W, H), INK + (255,))
VIDS = {}

# ------------------------------------------------------------------ shot constructors
def KB(path, crop=None, z=(1.03, 1.13), c0=(0.5, 0.5), c1=None, nps=False): return ("kb", dict(path=P(path), crop=NPSCROP if nps and crop is None else crop, z=z, c0=c0, c1=c1 or c0))
def VID(name, start=0.0, speed=1.0): return ("vid", dict(name=name, start=start, speed=speed))
def CARD(big, sub): return ("card", dict(big=big, sub=sub))
def DOC(key, focus, z=(0.9, 1.25), marks=()): return ("doc", dict(key=key, focus=focus, z=z, marks=marks))
def MAP(c0, c1, ops=()): return ("map", dict(c0=c0, c1=c1, ops=ops))
def PRINTS(items, bg=None): return ("prints", dict(items=items, bg=bg))
def BLACK(): return ("black", {})
def TITLE(): return ("title", {})
MUGS = [("A1_fbi_morris.jpg", None), ("mug_john_anglin.jpg", (0, 0, 1, 0.78)), ("mug_clarence_anglin.jpg", None)]
def three_mugs(label=True, w=380):
    names = ["FRANK MORRIS", "JOHN ANGLIN", "CLARENCE ANGLIN"]
    return PRINTS([(p, c, w, W / 2 + (k - 1) * 540, H / 2 - 50, (-2, 1.5, -1)[k], 0.15 + 0.35 * k, names[k] if label else None) for k, (p, c) in enumerate(MUGS)])

SHOTS = [
 (0, ("coldopen", {})),
 (1, KB("F11_nps_broadway_1963.jpg", nps=True, z=(1.05, 1.2), c0=(0.5, 0.55))),
 (2, DOC("p115", (200, 262, 620, 322), z=(1.15, 1.45), marks=[("dummy", 0.3)])),
 (3, KB("B2_fbi_dummy_in_bed.jpg", z=(1.0, 1.18), c0=(0.45, 0.45), c1=(0.42, 0.38))),
 (4, DOC("p115", (330, 330, 620, 380), z=(1.1, 1.5), marks=[("crumbled", 0.5)])),
 (5, KB("B3_fbi_dummy_head.jpg", z=(1.0, 1.25), c0=(0.4, 0.5))),
 (6, VID("H1", 0.5, 0.6)),
 (8, PRINTS([("E4_page_p32", None, 760, W / 2 - 160, H / 2, -2, 0.1, None), ("E4_page_p68", None, 760, W / 2 + 200, H / 2 + 20, 2.5, 0.6, None)])),
 (9, BLACK()),
 (10, TITLE()),
 (11, MAP((2600, 1700, 3600), (2672, 1900, 1900), ops=[("ring", ALC, 0.6), ("measure", ALC, FTMASON, 1.8, "1.25 MILES")])),
 (12, KB("F3_nps_aerial_1950a.jpg", nps=True, z=(1.05, 1.2))),
 (13, VID("H18", 2.0, 0.7)),
 (14, BLACK()),
 (18, three_mugs()),
 (19, KB("A1_fbi_morris.jpg", z=(1.0, 1.12), c0=(0.5, 0.42))),
 (21, PRINTS([("mug_john_anglin.jpg", (0, 0, 1, 0.78), 460, W / 2 - 300, H / 2 - 40, -2, 0.1, "JOHN ANGLIN  ·  AZ-1476"),
              ("mug_clarence_anglin.jpg", None, 460, W / 2 + 300, H / 2 - 40, 1.5, 0.6, "CLARENCE ANGLIN  ·  AZ-1485")])),
 (22, KB("A9_wanted_clarence_anglin_nps.jpg", nps=True, z=(1.0, 1.15), c0=(0.5, 0.45))),
 (23, KB("F12_nps_prisoners_cells.jpg", nps=True)),
 (24, BLACK()),
 (25, KB("C3_nps_cell138.jpg", nps=True, z=(1.02, 1.15))),
 (27, CARD("DEC 1961", "Six months before")),
 (28, KB("C4_fbi_vent.jpg", z=(1.0, 1.3), c0=(0.45, 0.5))),
 (29, KB("C2_nps_utility_corridor.jpg", nps=True, z=(1.02, 1.15))),
 (30, VID("H9", 1.0, 0.8)),
 (31, KB("E3_nps_tools.jpg", nps=True, z=(1.3, 1.6), c0=(0.55, 0.62), c1=(0.6, 0.6))),
 (32, KB("E3_nps_tools.jpg", nps=True, z=(1.4, 1.7), c0=(0.55, 0.25), c1=(0.5, 0.22))),
 (33, KB("cell_vent.jpg", z=(1.1, 1.35), c0=(0.3, 0.32))),
 (34, PRINTS([("false_grid.jpg", None, 900, W / 2, H / 2, -1.5, 0.1, "FAKE GRILLE  ·  CARDBOARD, PAINT  ·  NPS")])),
 (35, KB("C1_nps_cell152.jpg", nps=True, z=(1.0, 1.15), c0=(0.45, 0.6))),
 (37, KB("D3_fbi_catwalk.jpg", z=(1.0, 1.15))),
 (38, KB("D2_fbi_workshop.jpg", z=(1.0, 1.2))),
 (40, BLACK()),
 (41, KB("E2_fbi_life_vest.jpg", z=(1.0, 1.15))),
 (43, BLACK()),
 (44, PRINTS([("E1_fbi_paddle.jpg", None, 760, W / 2 - 330, H / 2 - 20, -2, 0.1, "PADDLE  ·  FBI"), ("E2_fbi_life_vest.jpg", None, 760, W / 2 + 330, H / 2 + 10, 2, 0.8, "LIFE VEST  ·  FBI")])),
 (46, KB("D4_fbi_roof_vent.jpg", z=(1.0, 1.2), c0=(0.45, 0.55))),
 (47, BLACK()),
 (48, KB("B4_fbi_fake_heads.jpg", z=(1.0, 1.12))),
 (50, KB("B3_fbi_dummy_head.jpg", z=(1.05, 1.2), c0=(0.35, 0.55))),
 (51, KB("dummy_head_morris.jpg", z=(1.0, 1.25), c0=(0.6, 0.3))),
 (52, KB("B5_nps_dummy_morris.jpg", nps=True, z=(1.0, 1.15))),
 (53, KB("B2_fbi_dummy_in_bed.jpg", z=(1.1, 1.25), c0=(0.42, 0.4))),
 (54, CARD("5:30 PM", "Monday, June 11, 1962  ·  Lockup")),
 (55, KB("F10_nps_locking_doors_1960.jpg", nps=True, z=(1.0, 1.15))),
 (56, KB("F12_nps_prisoners_cells.jpg", nps=True, z=(1.1, 1.2), c0=(0.6, 0.5))),
 (57, KB("F11_nps_broadway_1963.jpg", nps=True, z=(1.1, 1.25))),
 (58, VID("H8", 0.5, 0.8)),
 (59, CARD("8:31 PM", "Sunset")),
 (60, VID("H14", 3.0, 0.8)),
 (61, VID("H21", 1.0, 0.8)),
 (63, CARD("9:30 PM", "Lights out  ·  Bed check")),
 (64, three_mugs(label=False)),
 (65, VID("H8", 6.0, 0.6)),
 (66, DOC("p68", (380, 720, 680, 790), marks=[("thirty", 0.6)])),
 (67, KB("F2_habs_cellhouse_1986.jpg", z=(1.0, 1.2), c0=(0.5, 0.6), c1=(0.5, 0.35))),
 (68, KB("F9_nps_cellblock_west.jpg", nps=True, z=(1.0, 1.15))),
 (70, CARD("9:37 PM", "The fourth man")),
 (71, KB("cell_vent.jpg", z=(1.0, 1.15), c0=(0.35, 0.4))),
 (73, PRINTS([("A1_fbi_morris.jpg", None, 420, W / 2 - 260, H / 2 - 40, -2, 0.1, "MORRIS"), ("mug_john_anglin.jpg", (0, 0, 1, 0.78), 420, W / 2 + 260, H / 2 - 40, 1.5, 0.6, "ANGLIN")])),
 (74, BLACK()),
 (75, KB("C2_nps_utility_corridor.jpg", nps=True, z=(1.15, 1.3), c0=(0.55, 0.45))),
 (76, ("cta", {})),
 (80, CARD("10:00 PM", "The roof")),
 (81, KB("D2_fbi_workshop.jpg", z=(1.15, 1.3), c0=(0.55, 0.45))),
 (82, KB("D4_fbi_roof_vent.jpg", z=(1.1, 1.3), c0=(0.4, 0.5))),
 (83, DOC("a24", (130, 120, 1000, 1350), z=(0.95, 1.1))),
 (84, DOC("a25", (300, 300, 1060, 390), z=(1.0, 1.12), marks=[("stride", 0.5), ("run", 0.3, 85)])),
 (86, KB("D7_nps_bakery.jpg", nps=True, z=(1.0, 1.15))),
 (87, KB("F9_nps_cellblock_west.jpg", nps=True, z=(1.2, 1.4), c0=(0.3, 0.4), c1=(0.3, 0.7))),
 (88, VID("H25", 1.0, 0.7)),
 (89, KB("D6_nps_press_diagram.jpg", nps=True, z=(1.0, 1.25), c0=(0.3, 0.3))),
 (90, MAP((2672, 1860, 1200), (2700, 1830, 700), ops=[("ring", ALC, 0.3), ("label", ALC_NE, "NE SHORE", 0.6)])),
 (91, MAP((2672, 1900, 2600), (2300, 1950, 3000), ops=[("ring", ALC, 0.0)])),
 (92, MAP((2300, 1950, 3000), (1900, 2000, 3600), ops=[("ebb", 0.0)])),
 (93, VID("H23", 0.5, 0.7)),
 (94, KB("E3_nps_tools.jpg", nps=True, z=(1.0, 1.1))),
 (95, CARD("10:30 PM", "The noise")),
 (96, VID("H8", 10.0, 0.6)),
 (97, DOC("p113", (200, 260, 560, 320), z=(1.0, 1.35), marks=[("oil", 0.8)])),
 (98, BLACK()),
 (100, KB("F15_nps_metal_detector.jpg", nps=True, z=(1.0, 1.15))),
 (101, KB("F11_nps_broadway_1963.jpg", nps=True, z=(1.2, 1.35), c0=(0.5, 0.5))),
 (102, BLACK()),
 (103, KB("B2_fbi_dummy_in_bed.jpg", z=(1.0, 1.12))),
 (105, CARD("11:15 PM", "Count")),
 (106, PRINTS([("B2_fbi_dummy_in_bed.jpg", None, 520, W / 2 - 560, H / 2, -2, 0.0, None), ("B3_fbi_dummy_head.jpg", None, 470, W / 2, H / 2 - 10, 1, 0.3, None),
               ("B4_fbi_fake_heads.jpg", None, 560, W / 2 + 560, H / 2 + 10, -1.5, 0.6, None)])),
 (107, MAP((2400, 1950, 3300), (1800, 2000, 3900), ops=[("ebb", 0.0), ("label", (1700, 1900), "11:46 PM  ·  MAX EBB 2.7 KNOTS", 0.5)])),
 (108, VID("H19", 2.0, 0.6)),
 (109, VID("H18", 10.0, 0.6)),
 (110, MAP((2000, 1700, 3800), (2000, 1700, 3800), ops=[("note", "Illustration of the TU Delft / Deltares tide model, 2014")])),
 (111, MAP((2000, 1700, 3800), (1900, 1750, 3900), ops=[("boats", "all")])),
 (112, MAP((1900, 1750, 3900), (1700, 1850, 3600), ops=[("boats", "early")])),
 (113, MAP((1700, 1850, 3600), (1500, 1700, 2600), ops=[("boats", "late"), ("label", HORSE, "MARIN SHORE", 1.2)])),
 (114, MAP((1700, 1500, 3400), (2300, 1200, 3000), ops=[("boats", "debris"), ("label", BLUNT, "ANGEL ISLAND", 0.8)])),
 (115, MAP((2300, 1200, 3000), (2100, 1500, 3800), ops=[("boats", "all_static")])),
 (116, VID("H19", 14.0, 0.6)),
 (117, KB("cell_vent.jpg", z=(1.15, 1.3), c0=(0.3, 0.35))),
 (118, KB("D3_fbi_catwalk.jpg", z=(1.1, 1.25), c0=(0.5, 0.4))),
 (119, KB("D4_fbi_roof_vent.jpg", z=(1.0, 1.08))),
 (120, BLACK()),
 (121, KB("C3_nps_cell138.jpg", nps=True, z=(1.2, 1.3), c0=(0.5, 0.6))),
 (122, CARD("2:43 AM", "Moonset")),
 (123, MAP((2400, 1900, 3600), (2400, 1900, 3400), ops=[("flood", 0.3), ("label", (2300, 1500), "2:55 AM  ·  LOW WATER, TIDE TURNS", 0.4)])),
 (124, CARD("5:46 AM", "Sunrise")),
 (125, VID("H2", 0.5, 0.6)),
 (126, CARD("7:15 AM", "Morning count")),
 (127, three_mugs(label=False)),
 (128, DOC("p115", (180, 270, 640, 320), z=(1.1, 1.3), marks=[("dummy", 1.5)])),
 (129, KB("B2_fbi_dummy_in_bed.jpg", z=(1.05, 1.25), c0=(0.45, 0.42))),
 (130, DOC("p115", (330, 330, 620, 380), z=(1.2, 1.5), marks=[("crumbled", 0.2), ("rolled", 1.6)])),
 (131, KB("C1_nps_cell152.jpg", nps=True, z=(1.0, 1.12))),
 (132, KB("F11_nps_broadway_1963.jpg", nps=True, z=(1.3, 1.4))),
 (133, KB("F7_nps_east_side.jpg", nps=True, z=(1.0, 1.12))),
 (134, KB("C2_nps_utility_corridor.jpg", nps=True, z=(1.05, 1.25), c0=(0.45, 0.55))),
 (135, KB("cell_vent.jpg", z=(1.0, 1.1))),
 (136, DOC("p116", (260, 380, 600, 440), z=(1.1, 1.4), marks=[("planned", 1.2)])),
 (137, CARD("JUNE 12", "The manhunt")),
 (138, VID("H30", 2.0, 0.8)),
 (139, MAP((2600, 1300, 3400), (2450, 800, 2200), ops=[("ring", ANGEL, 0.2), ("label", (2400, 420), "ANGEL ISLAND", 0.5)])),
 (140, MAP((2600, 1000, 1800), (2720, 960, 1300), ops=[("pin", PADDLE, 0.3, "PADDLE  ·  JUNE 12")])),
 (141, MAP((2700, 1700, 2200), (2850, 1830, 1500), ops=[("pin", WHIRL, 0.5, "PACKETS  ·  JUNE 14"), ("ring", ALC, 0.0)])),
 (142, DOC("p44", (60, 780, 640, 850), z=(1.0, 1.3), marks=[("whirlpool", 0.4)])),
 (143, BLACK()),
 (144, VID("H18", 18.0, 0.7)),
 (145, DOC("p92", (60, 940, 520, 1010), z=(1.0, 1.3), marks=[("olympic", 0.4)])),
 (146, DOC("p43", (180, 690, 640, 760), z=(1.0, 1.3), marks=[("cronkhite", 1.0)])),
 (147, KB("E2_fbi_life_vest.jpg", z=(1.05, 1.2))),
 (148, BLACK()),
 (150, DOC("p87", (700, 890, 1080, 950), z=(1.0, 1.3), marks=[("haha", 0.6)])),
 (152, VID("H19", 20.0, 0.6)),
 (155, BLACK()),
 (157, CARD("MAR 21, 1963", "Alcatraz closes")),
 (158, KB("F11_nps_broadway_1963.jpg", nps=True, z=(1.0, 1.1))),
 (159, PRINTS([("E4_page_p32", None, 700, W / 2 - 300, H / 2, -2, 0.0, None), ("E4_page_p48", None, 700, W / 2, H / 2 + 10, 1.5, 0.4, None),
               ("E4_page_p115", None, 700, W / 2 + 300, H / 2 - 10, -1, 0.8, None)])),
 (162, CARD("DEC 31, 1979", "The FBI closes its file")),
 (163, PRINTS([("A8_wanted_john_anglin_nps.jpg", NPSCROP, 760, W / 2 - 330, H / 2, -2, 0.0, None), ("A9_wanted_clarence_anglin_nps.jpg", NPSCROP, 760, W / 2 + 330, H / 2, 2, 0.3, None)])),
 (164, MAP((2300, 2100, 3000), (1900, 2250, 2800), ops=[("swim", 0.2), ("label", FTPOINT, "FORT POINT", 1.6)])),
 (167, CARD("2013", "The letter")),
 (168, ("letter", {})),
 (173, BLACK()),
 (175, CARD("2015", "The photo")),
 (176, BLACK()),
 (177, KB("B5_nps_dummy_morris.jpg", nps=True, z=(1.0, 1.15))),
 (178, KB("B6_nps_head_exhibit.jpg", z=(1.0, 1.15))),
 (179, PRINTS([("A10_usms_age_morris.jpg", None, 380, W / 2 - 520, H / 2 - 30, -2, 0.0, "MORRIS"), ("A11_usms_age_john.jpg", None, 380, W / 2, H / 2 - 30, 1, 0.4, "JOHN"),
               ("A12_usms_age_clarence.jpg", None, 380, W / 2 + 520, H / 2 - 30, -1.5, 0.8, "CLARENCE")])),
 (180, VID("H1", 4.0, 0.5)),
 (181, PRINTS([("A10_usms_age_morris.jpg", None, 380, W / 2 - 520, H / 2 - 30, -2, 0.0, None), ("A11_usms_age_john.jpg", None, 380, W / 2, H / 2 - 30, 1, 0.0, None),
               ("A12_usms_age_clarence.jpg", None, 380, W / 2 + 520, H / 2 - 30, -1.5, 0.0, None)])),
 (182, KB("A10_usms_age_morris.jpg", z=(1.0, 1.12), c0=(0.5, 0.4))),
 (183, VID("H1", 1.0, 0.5)),
 (184, KB("E3_nps_tools.jpg", nps=True, z=(1.0, 1.1))),
 (185, KB("D4_fbi_roof_vent.jpg", z=(1.0, 1.1))),
 (186, BLACK()),
 (187, VID("H18", 22.0, 0.6)),
 (188, VID("H2", 2.0, 0.5)),
 (189, ("end", {})),
]
SHOT_LINES = [s[0] for s in SHOTS]

# overlays: (line, offset, kind, args)
OV = [
 (0, 0, "none", ()),
 (6, 0.2, "lower", "ALCATRAZ ISLAND  ·  SAN FRANCISCO BAY"),
 (7, 0.3, "big", "\u201cNO ONE EVER ESCAPED\u201d"),
 (8, 0.2, "lower", "FBI FILE 76-26295  ·  'ALCATRAZ ESCAPE'"),
 (9, 0.0, "typecenter", "HOUR BY HOUR"),
 (13, 0.4, "lower", "WATER  ·  ABOUT 50°F"),
 (14, 0.0, "typecenter", "14 ATTEMPTS  ·  36 MEN"),
 (15, 0.0, "list", ["23 CAUGHT", "6 SHOT AND KILLED", "2 DROWNED"]),
 (16, 0.0, "typecenter_red", "5 NEVER FOUND"),
 (17, 0.1, "under", "2 OF THEM: ROE AND COLE, 1937"),
 (19, 0.3, "lower", "FRANK LEE MORRIS  ·  AZ-1441  ·  FBI"),
 (22, 0.3, "lower", "FBI WANTED POSTER  ·  CLARENCE ANGLIN"),
 (24, 0.0, "list", ["JAN 1960  ·  MORRIS", "1960  ·  JOHN ANGLIN", "EARLY 1961  ·  CLARENCE ANGLIN"]),
 (25, 0.3, "lower", "CELL 138  ·  MORRIS   |   NEXT DOOR: ALLEN WEST"),
 (28, 0.3, "lower", "THE AIR VENT  ·  FBI PHOTO"),
 (29, 0.3, "lower", "UTILITY CORRIDOR BEHIND CELL 152  ·  1962"),
 (31, 0.3, "lower", "TOOLS FOUND AFTER THE ESCAPE  ·  NPS"),
 (32, 0.4, "lower", "DRILL MOTOR: PRISON VACUUM CLEANER"),
 (35, 0.3, "lower", "CELL 152  ·  HOW THE HOLE WAS HIDDEN  ·  1962"),
 (36, 0.3, "under", "ACCORDION COVER STORY  ·  NOT IN THE FBI SUMMARY"),
 (38, 0.3, "lower", "THE WORKSHOP ON TOP OF CELL BLOCK B  ·  FBI"),
 (39, 0.2, "lower", "LOOKOUT: CARDBOARD PERISCOPE"),
 (40, 0.0, "typecenter", "THE BOAT"),
 (41, 0.2, "lower", "50+ RAINCOATS"),
 (42, 0.3, "lower", "SEAMS SEALED ON HOT-WATER PIPES"),
 (43, 0.0, "list", ["POPULAR MECHANICS", "SPORTS ILLUSTRATED"]),
 (44, 0.2, "under", "RAFT 6 × 14 FT  ·  3 VESTS  ·  PADDLES"),
 (45, 0.2, "under", "CONCERTINA  →  BELLOWS"),
 (46, 0.3, "lower", "ROOF VENTILATOR  ·  'BOLT' MADE OF SOAP  ·  FBI"),
 (47, 0.0, "typecenter", "THE HEADS"),
 (48, 0.2, "lower", "THE DUMMY HEADS  ·  FBI"),
 (49, 0.2, "stamp", ("FBI LAB", 1500, 260)),
 (50, 0.2, "list_side", ["PORTLAND CEMENT", "SAND", "WHITE CEMENT PAINT"]),
 (51, 0.3, "lower", "HAIR: HUMAN"),
 (52, 0.3, "lower", "CLARENCE'S: SOAP OVER COTTON RAGS"),
 (56, 0.3, "lower", "ABOUT 260 OTHER INMATES"),
 (61, 0.4, "lower", "MOON ABOUT 2/3 FULL  ·  COMPUTED"),
 (64, 0.4, "under", "LAST SEEN BY A GUARD: 9:30 PM"),
 (65, 0.3, "quote", ("\u201cAny small noise thereafter sounds like an explosion.\u201d", "NIGHT OFFICER  ·  FBI INTERVIEW")),
 (67, 0.3, "lower", "CELL HOUSE  ·  HABS / LIBRARY OF CONGRESS"),
 (68, 0.3, "under", "ONE INMATE'S ACCOUNT  ·  FBI TELETYPE"),
 (72, 0.3, "lower", "WEST'S VENT WON'T COME FREE"),
 (74, 0.0, "typecenter", "THEY NEVER COME BACK"),
 (75, 0.3, "under", "WEST'S ACCOUNT TO THE FBI"),
 (83, 0.2, "lower", "FBI PHOTO 1-10  ·  TENNIS-SHOE PRINT  ·  JUNE 12, 1962"),
 (84, 0.3, "under", "STRIDE: 4 FT 1⅛ IN"),
 (86, 0.3, "lower", "THE BAKERY  ·  ITS OVEN STACK RAN UP THE OUTSIDE WALL"),
 (87, 0.2, "under", "≈ 45 FT DOWN"),
 (88, 0.3, "lower", "12-FT FENCE  ·  BARBED WIRE"),
 (89, 0.3, "under", "TOWERS 2 AND 3: NOT MANNED AT NIGHT  ·  FBI"),
 (90, 0.4, "under", "FBI ESTIMATE: AROUND 10 PM"),
 (91, 0.2, "lower", "10:00 PM  ·  SLACK TIDE"),
 (94, 0.3, "lower", "EXTENSION CORD: ON THE ROOF, AND ON THE BEACH"),
 (98, 0.0, "typecenter", "+ 2 MINUTES"),
 (99, 0.0, "typecenter", "+ 5 MINUTES"),
 (100, 0.3, "lower", "CONTROL CENTER  ·  LISTENING SYSTEM"),
 (101, 0.3, "under", "SEARCH: ABOUT 45 MINUTES"),
 (102, 0.0, "typecenter", "\u201cEVERYTHING APPEARED TO BE NORMAL\u201d"),
 (108, 0.3, "lower", "WATER  ·  ABOUT 50°F"),
 (109, 0.3, "under", "NOBODY SAW THEM LAUNCH"),
 (115, 0.3, "under", "A MODEL, NOT PROOF"),
 (116, 0.4, "lower", "COLD WATER: EXHAUSTION IN 1–2 HOURS (SURVIVAL TABLES)"),
 (117, 0.3, "under", "WEST'S ACCOUNT TO THE FBI"),
 (120, 0.0, "list", ["RAFT: GONE", "3 VESTS: GONE"]),
 (125, 0.3, "under", "WHATEVER HAPPENED HAS ALREADY HAPPENED"),
 (127, 0.3, "under", "3 MEN DON'T STAND UP"),
 (131, 0.2, "list_side", ["CELL 150  ·  DUMMY", "CELL 152  ·  DUMMY", "CELL 138  ·  DUMMY"]),
 (132, 0.2, "stamp", ("ESCAPE ALARM", 1400, 300)),
 (133, 0.3, "lower", "WARDEN OLIN BLACKWELL  ·  ON VACATION"),
 (134, 0.3, "lower", "VENTS KICKED OUT INTO THE CORRIDOR"),
 (137, 0.0, "none", ()),
 (138, 0.3, "lower", "COAST GUARD  ·  HELICOPTER  ·  FBI"),
 (139, 0.3, "under", "100+ SOLDIERS  ·  NOTHING FOUND"),
 (143, 0.0, "list", ["PHOTOGRAPHS", "NAMES", "ADDRESSES"]),
 (144, 0.3, "lower", "OLYMPIC CLUB SWIMMERS  ·  53 MINUTES"),
 (146, 0.0, "under", "JUNE 15  ·  ~3:30 PM  ·  CRONKHITE BEACH"),
 (147, 0.3, "lower", "LIFE VEST  ·  RAINCOAT RUBBER  ·  FBI"),
 (148, 0.0, "quote", ("\u201cInmates had no access to raincoats.\u201d", "OFFICIALS TO REPORTERS  ·  JUNE 1962")),
 (149, 0.2, "stamp", ("50+ RAINCOATS", 1350, 760)),
 (151, 0.2, "stamp", ("FAKE", 1450, 300)),
 (152, 0.3, "lower", "JULY 17, 1962  ·  NORWEGIAN FREIGHTER  ·  ~20 MILES OUT"),
 (154, 0.3, "under", "NEVER RECOVERED"),
 (155, 0.0, "list", ["RAFT: NEVER FOUND", "NO CAR STOLEN", "NO ROBBERY TIED TO THEM"]),
 (158, 0.3, "lower", "CLOSING DAY  ·  MARCH 21, 1963  ·  NPS"),
 (160, 0.0, "list_side", ["STRONG CURRENTS", "COLD WATER", "NO CRIMES", "NO MONEY", "NO CREDIBLE SIGHTING"]),
 (161, 0.2, "stamp", ("PRESUMED DROWNED", 1300, 860)),
 (163, 0.4, "stamp", ("STILL OPEN", 1500, 830)),
 (164, 0.3, "lower", "JOHN PAUL SCOTT  ·  DECEMBER 1962"),
 (166, 0.2, "under", "POSSIBLE. BARELY."),
 (173, 0.0, "list", ["FINGERPRINTS", "DNA", "HANDWRITING"]),
 (174, 0.0, "stamp", ("INCONCLUSIVE", W / 2, H / 2 + 220)),
 (176, 0.0, "quote", ("\u201cNot the Anglins.\u201d", "US MARSHALS SERVICE  ·  2016")),
 (177, 0.3, "lower", "2018  ·  FBI LAB SCANS THE REAL HEADS"),
 (178, 0.3, "under", "BEFORE 2018: MOVIE PROPS IN THE CELLS"),
 (179, 0.3, "lower", "US MARSHALS AGE-PROGRESSED IMAGES  ·  2022"),
 (180, 0.3, "lower", "BUREAU OF PRISONS: MISSING, PRESUMED DROWNED"),
 (181, 0.3, "stamp", ("WANTED: ESCAPE", W / 2, H - 170)),
 (182, 0.3, "lower", "FRANK MORRIS  ·  BORN SEPT 1, 1926"),
 (186, 0.0, "typecenter", "10:30 PM  ·  NOTHING FOUND"),
 (187, 0.4, "under", "DID ANYONE REACH THE SHORE?"),
]

# ------------------------------------------------------------------ drawing helpers
def shot_at(t):
    k = 0
    for j, ln in enumerate(SHOT_LINES):
        if T[ln] - 0.12 <= t: k = j
    t0 = T[SHOTS[k][0]] - 0.12; t1 = (T[SHOTS[k + 1][0]] - 0.12) if k + 1 < len(SHOTS) else DUR
    return k, SHOTS[k], t0, t1

def page_img(key):
    if key.startswith("E4_page_"): key = key[8:]
    k = ("doc", key)
    if k not in IMG:
        im = Image.open(DOCS[key]).convert("RGB")
        IMG[k] = L.bw(DOCS[key]) if False else Image.fromarray((np.asarray(im.convert("L"), np.float32)[..., None] / 255 * np.array([236, 230, 214], np.float32)).astype(np.uint8))
    return IMG[k]

def view(src, cx, cy, s):
    """screen = src scaled by s, centred on (cx, cy); outside = black"""
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
    """dim the page except the quoted phrase (soft edges)"""
    if k <= 0: return
    m = Image.new("L", (W, H), 255); ImageDraw.Draw(m).rectangle([int(v) for v in box], fill=0); m = m.filter(ImageFilter.GaussianBlur(10))
    lay = Image.new("RGBA", (W, H), (8, 8, 9, 0)); lay.putalpha(m.point(lambda v: int(v * 0.62 * k))); c.alpha_composite(lay)
MARK_WORD = {("p115", "dummy"): "dead", ("p115", "crumbled"): "crumbled", ("p115", "rolled"): "rolled", ("p68", "thirty"): "bed", ("a25", "stride"): "feet",
             ("a25", "run"): "apparently", ("p113", "oil"): "oil", ("p116", "planned"): "planned", ("p43", "cronkhite"): "beach", ("p87", "haha"): "ha"}
def mark_time(mk, shot_line):
    line = mk[2] if len(mk) > 2 else shot_line
    for (key, name), word in MARK_WORD.items():
        if name == mk[0]: return wt(line, word)
    return T[line] + mk[1]

def arrow(d, pts, col, width=6, head=22):
    d.line(pts, fill=col, width=width, joint="curve")
    (x0, y0), (x1, y1) = pts[-2], pts[-1]; a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1, y1), (x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45)), (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45))], fill=col)

def bez(p0, p1, p2, n=40): return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in np.linspace(0, 1, n)]
PATHS = {"early": bez(ALC, (1900, 2150), WEST), "late": bez(ALC, (1700, 1800), HORSE), "debris": bez(ALC, (2900, 1300), BLUNT)}
def boat_dots(group, u):
    rng = np.random.default_rng({"early": 1, "late": 2, "debris": 3}[group]); path = np.array(PATHS[group]); out = []
    for k in range(14):
        lag = rng.uniform(0, 0.35); j = rng.normal(0, 40, 2); v = clamp01((u - lag) / 0.65)
        idx = v * (len(path) - 1); i0 = int(idx); f = idx - i0; i1 = min(i0 + 1, len(path) - 1)
        out.append(tuple(path[i0] * (1 - f) + path[i1] * f + j * math.sin(math.pi * v)))
    return out

def draw_map_ops(c, ops, t, t0, t1, tomap):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for op in ops:
        kind = op[0]
        if kind == "ring":
            if t < t0 + op[2]: continue
            x, y = tomap(*op[1]); k = ease((t - t0 - op[2]) / 0.35); r = 62 * (1.3 - 0.3 * k)
            d.ellipse((x - r, y - r, x + r, y + r), outline=RED + (int(255 * k),), width=6)
        elif kind == "measure":
            if t < t0 + op[3]: continue
            (x0, y0), (x1, y1) = tomap(*op[1]), tomap(*op[2]); u = ease((t - t0 - op[3]) / 0.8)
            d.line([(x0, y0), (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u)], fill=RED + (255,), width=5)
            if u >= 1: L.typewriter(lay, op[4], t, t0 + op[3] + 0.8, (x0 + x1) / 2 + 30, (y0 + y1) / 2, size=44, cps=24, cursor=False)
        elif kind == "label":
            x, y = tomap(*op[1]); L.typewriter(lay, op[2], t, t0 + op[3], x + 40, y, size=40, cps=26, cursor=False)
        elif kind == "pin":
            if t < t0 + op[2]: continue
            x, y = tomap(*op[1]); d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=RED + (255,), outline=BONE + (255,), width=4)
            L.typewriter(lay, op[3], t, t0 + op[2] + 0.2, x + 34, y, size=40, cps=26, cursor=False)
        elif kind in ("ebb", "flood"):
            for k in range(7):
                ph = ((t - t0) * 0.35 + k / 7) % 1.0; a0 = ALC if kind == "ebb" else GG; a1 = GG if kind == "ebb" else ALC
                mid = ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2 + (k - 3) * 90)
                p = bez((a0[0], a0[1] + (k - 3) * 60), mid, (a1[0], a1[1] + (k - 3) * 40), 30)
                i0 = int(ph * 20); seg = [tomap(*q) for q in p[i0:i0 + 9]]
                if len(seg) > 2: arrow(d, seg, RED + (int(230 * math.sin(math.pi * ph)),), width=5, head=18)
        elif kind == "boats":
            groups = ["early", "late", "debris"] if op[1] in ("all", "all_static") else [op[1]]
            u = 1.0 if op[1] == "all_static" else clamp01((t - t0 - 0.3) / max(t1 - t0 - 0.6, 1.0))
            for g in groups:
                for x, y in boat_dots(g, u if op[1] != "all" else 0.12 + 0.2 * clamp01((t - t0) / 3)):
                    sx, sy = tomap(x, y); d.ellipse((sx - 7, sy - 7, sx + 7, sy + 7), fill=RED + (235,))
        elif kind == "swim":
            if t < t0 + op[1]: continue
            pts = [tomap(*q) for q in bez(ALC, (1900, 2350), FTPOINT, 50)]; n = max(2, int(len(pts) * ease((t - t0 - op[1]) / 2.0)))
            for i in range(0, n - 1, 2): d.line([pts[i], pts[i + 1]], fill=RED + (255,), width=6)
        elif kind == "note":
            L.typewriter(lay, op[1], t, t0 + 0.2, 80, H - 70, size=30, fill=STEEL, cps=40, cursor=False)
    c.alpha_composite(lay)

def lower(c, s, t, t0):
    if t < t0: return
    lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); g = np.linspace(0, 1, 200)[:, None] ** 1.5 * 190
    lay.putalpha(Image.fromarray(np.repeat(g, W, 1).astype(np.uint8))); c.alpha_composite(lay, (0, H - 200))
    L.typewriter(c, s, t, t0, 90, H - 110, size=38, cps=34, cursor=False)
    L.rule(c, 90, 90 + min(len(s), 40) * 23, H - 76, t, t0 + 0.2, width=5)
def under(c, s, t, t0):
    if t < t0: return
    lay = Image.new("RGBA", (W, 170), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, 0, W, 170), fill=(0, 0, 0, 120))
    c.alpha_composite(lay, (0, H - 170)); L.typewriter(c, s, t, t0, W / 2, H - 92, size=50, cps=30, anchor="mm", cursor=False)

SLOT = {"lower": "bottom", "under": "bottom", "big": "bottom", "typecenter": "center", "typecenter_red": "center", "list": "center", "quote": "center", "list_side": "side"}
def ov_end(j, shot_t1):
    sl = SLOT.get(OV[j][2])
    if not sl: return shot_t1
    for ln2, off2, kind2, _ in OV[j + 1:]:
        if SLOT.get(kind2) == sl or (sl == "bottom" and kind2 in ("list", "typecenter")) : return min(T[ln2] + off2 - 0.05, shot_t1)
    return shot_t1
def draw_ov(c, k, t, shot_t1):
    for j, (ln, off, kind, a) in enumerate(OV):
        t0 = T[ln] + off
        if t < t0 or t >= shot_t1 or ln < SHOTS[k][0]: continue
        if t >= ov_end(j, shot_t1): continue
        if kind == "lower": lower(c, a, t, t0)
        elif kind == "under": under(c, a, t, t0)
        elif kind == "big": L.text(c, a, W / 2, H - 190, 110, BONE, COND, alpha=ease((t - t0) / 0.3))
        elif kind in ("typecenter", "typecenter_red"):
            L.typewriter(c, a, t, t0, W / 2, H / 2, size=96, fill=RED if kind.endswith("red") else BONE, cps=16, anchor="mm", cursor=False)
        elif kind == "list":
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.9, W / 2, H / 2 - (len(a) - 1) * 60 + i * 120, size=78, cps=20, anchor="mm", cursor=False)
        elif kind == "list_side":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip((np.linspace(0, 1, W) - 0.45) * 2.2, 0, 1)[None, :] * 200
            lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.7, 1180, 300 + i * 95, size=52, cps=24, anchor="lm", cursor=False)
        elif kind == "stamp": L.stamp(c, a[0], a[1], a[2], t, t0, size=100)
        elif kind == "quote":
            L.text(c, a[0], W / 2, H / 2 - 30, 70, BONE, SER, alpha=ease((t - t0) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, W / 2, H / 2 + 70, size=34, fill=STEEL, cps=34, anchor="mm", cursor=False)

PC = {}
def pcard(path, crop, w, rot):
    k = (path, crop, w, rot)
    if k not in PC:
        src = page_img(path) if path.startswith("E4_page_") else tone(P(path), crop)
        PC[k] = L.print_card(src, w, rot=rot)
    return PC[k]

def frame(t):
    k, (ln, (kind, a)), t0, t1 = shot_at(t)
    if kind == "kb":
        src = tone(a["path"], a["crop"]); c = L.vignette(L.kenburns(src, t, t0, t1, a["z"][0], a["z"][1], a["c0"], a["c1"]))
    elif kind == "vid":
        key = (k, a["name"])
        if key not in VIDS:
            for v in VIDS.values():
                if v.p: v.p.kill()
            VIDS.clear(); VIDS[key] = Vid(a["name"], a["start"], a["speed"], t0)
        c = L.vignette(VIDS[key].frame(t))
    elif kind == "coldopen":
        pg = page_img("p115"); bg = view(pg, 380, 330, 2.6).filter(ImageFilter.GaussianBlur(1.2))
        c = Image.alpha_composite(bg, Image.new("RGBA", (W, H), (0, 0, 0, 150)))
        u = clamp01((t - t0) / max(t1 - t0, 1)); hd = pcard("B3_fbi_dummy_head.jpg", None, int(560 + 50 * u), 3)
        c.alpha_composite(hd, (int(W * 0.66 - hd.width / 2), int(H / 2 - hd.height / 2)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.clip(1.25 - np.linspace(0, 1, W) * 1.9, 0, 1)[None, :] * 235
        lay.putalpha(Image.fromarray(np.repeat(g, H, 0).astype(np.uint8))); c.alpha_composite(lay)
        L.typewriter(c, "7:20 AM", t, t0 + 0.05, 120, H / 2 - 60, size=170, cps=12, anchor="lm", cursor=False)
        L.text(c, "June 12, 1962  ·  Alcatraz", 125, H / 2 + 70, 52, BONE, SER, anchor="lm", alpha=ease((t - t0 - 0.7) / 0.4))
        L.rule(c, 125, 545, H / 2 + 120, t, t0 + 0.9)
    elif kind == "card":
        c = Image.new("RGBA", (W, H), INK + (255,)); big = a["big"]
        L.typewriter(c, big, t, t0 + 0.05, W / 2, H / 2 - 50, size=210, cps=12, anchor="mm", cursor=False)
        t2 = t0 + 0.05 + len(big) / 12
        L.text(c, a["sub"], W / 2, H / 2 + 120, 58, STEEL, SER, alpha=ease((t - t2) / 0.4)); L.rule(c, W / 2 - 280, W / 2 + 280, H / 2 + 185, t, t2 + 0.15)
    elif kind == "doc":
        src = page_img(a["key"]); fx0, fy0, fx1, fy1 = a["focus"]; u = ease((t - t0) / max(t1 - t0, 0.5))
        s_fit = min(W * 0.78 / (fx1 - fx0), H * 0.6 / (fy1 - fy0)); s = s_fit * (a["z"][0] + (a["z"][1] - a["z"][0]) * u)
        cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
        act = None
        for mk in a["marks"]:
            tm = mark_time(mk, ln)
            if t >= tm: act = (PH[a["key"]][mk[0]], tm)
        if act:                                                            # glide toward the quoted line
            b, tm = act; v = ease((t - tm) / 0.6); cx += ((b[0] + b[2]) / 2 - cx) * 0.55 * v; cy += ((b[1] + b[3]) / 2 - cy) * 0.8 * v
        c = view(src, cx, cy, s)
        if act:
            b, tm = act; sx0, sy0, sx1, sy1 = (b[0] - cx) * s + W / 2 - 18, (b[1] - cy) * s + H / 2 - 12, (b[2] - cx) * s + W / 2 + 18, (b[3] - cy) * s + H / 2 + 12
            spotlight(c, (sx0, sy0, sx1, sy1), ease((t - tm) / 0.35))
            uu = ease((t - tm - 0.1) / 0.3); ImageDraw.Draw(c).rectangle((sx0 + 10, sy1 + 4, sx0 + 10 + (sx1 - sx0 - 20) * uu, sy1 + 11), fill=RED)
        c = L.vignette(c, 0.45)
    elif kind == "map":
        (x0, y0, w0), (x1, y1, w1) = a["c0"], a["c1"]; u = ease((t - t0) / max(t1 - t0, 0.5))
        cx, cy, ww = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, w0 * (w1 / w0) ** u; s = W / ww
        c = view(mapimg(), cx, cy, s); tomap = lambda x, y: ((x - cx) * s + W / 2, (y - cy) * s + H / 2)
        draw_map_ops(c, a["ops"], t, t0, t1, tomap); c = L.vignette(c, 0.4)
    elif kind == "prints":
        c = Image.new("RGBA", (W, H), INK + (255,))
        for path, crop, w, x, y, rot, d, label in a["items"]:
            L.drop(c, pcard(path, crop, w, rot), x, y, t, t0 + d)
            if label: L.typewriter(c, label, t, t0 + d + 0.35, x, y + pcard(path, crop, w, rot).height / 2 + 30, size=34, cps=30, anchor="mm", cursor=False)
    elif kind == "title":
        c = Image.new("RGBA", (W, H), INK + (255,)); u = ease((t - t0) / 0.6)
        L.text(c, "the", W / 2, H / 2 - 170, 80, STEEL, SER, alpha=u); L.text(c, "LAST HOURS", W / 2, H / 2 - 10, 240, BONE, COND, alpha=u)
        L.rule(c, W / 2 - 320, W / 2 + 320, H / 2 + 135, t, t0 + 0.4, width=9)
        L.typewriter(c, "FILE 01  ·  ALCATRAZ  ·  JUNE 11, 1962", t, t0 + 0.9, W / 2, H / 2 + 230, size=40, fill=STEEL, cps=30, anchor="mm", cursor=False)
    elif kind == "cta":
        c = L.vignette(L.kenburns(tone(P("A9_wanted_clarence_anglin_nps.jpg"), NPSCROP), t, t0, t1, 1.1, 1.18)); c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 165)))
        L.typewriter(c, "EVERYTHING HERE IS FROM THE REAL FILES", t, T[77], W / 2, H / 2 - 60, size=56, cps=30, anchor="mm", cursor=False)
        L.typewriter(c, "LIKE  ·  SUBSCRIBE", t, T[78] + 0.8, W / 2, H / 2 + 60, size=70, fill=RED, cps=14, anchor="mm", cursor=False)
    elif kind == "letter":
        c = Image.new("RGBA", (W, H), INK + (255,)); paper = (226, 220, 204)
        ImageDraw.Draw(c).rectangle((W / 2 - 660, 90, W / 2 + 660, H - 90), fill=paper)
        rows = [(168, "SIGNED: JOHN ANGLIN"), (169, "\u201cI'm 83 years old and in bad shape. I have cancer.\u201d"), (170, "\u201cAll three made it that night. But barely.\u201d"),
                (171, "Frank: died 2008.  Clarence: died 2011."), (172, "Offer: surrender for < 1 year in jail + medical care.")]
        for i, (li, s) in enumerate(rows):
            L.typewriter(c, s, t, T[li] + 0.1, W / 2 - 600, 210 + i * 140, size=36, fill=(40, 36, 30), cps=32, anchor="lm", cursor=False)
        L.typewriter(c, "Letter received by SFPD, 2013 (made public 2018)  ·  as reported by CBS", t, t0 + 0.3, W / 2, H - 50, size=26, fill=STEEL, cps=50, anchor="mm", cursor=False)
    elif kind == "end":
        c = L.vignette(L.kenburns(Image.new("RGB", (W, H), INK), t, t0, t1))
        L.text(c, "the", W / 2, 150, 60, STEEL, SER); L.text(c, "LAST HOURS", W / 2, 260, 150, BONE, COND); L.rule(c, W / 2 - 220, W / 2 + 220, 350, t, t0, width=7)
        L.typewriter(c, "NEXT FILE?  D.B. COOPER  ·  FLIGHT 19", t, T[190], W / 2, 450, size=46, fill=BONE, cps=26, anchor="mm", cursor=False)
        if t > VO_END:                                                     # end-screen slots (YouTube elements go on top)
            d = ImageDraw.Draw(c); d.rectangle((1050, 560, 1770, 965), outline=STEEL + (255,), width=3); d.ellipse((330, 600, 650, 920), outline=STEEL + (255,), width=3)
    else:
        c = Image.new("RGBA", (W, H), INK + (255,))
    draw_ov(c, k, t, t1)
    if t1 - t < 0.10 and kind not in ("card",): c = L.fade_black(c, (0.10 - (t1 - t)) / 0.10 * 0.0)
    return c

# ------------------------------------------------------------------ audio
def load(p, sr=48000):
    a, s = sf.read(p, dtype="float32", always_2d=True); a = a.mean(1)
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    return a
def audio():
    sr = 48000; N = int(DUR * sr); vo = load(ROOT + "vo/alcatraz_vo_chatterbox.wav"); y = np.zeros(N, np.float32)
    s0 = int(LEAD * sr); y[s0:s0 + len(vo)] += vo[: N - s0]
    vr = np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)); bed = np.zeros(N, np.float32)
    def put(a, t, db, fade=0.02):
        i = int(t * sr); a = a[: max(0, N - i)] * 10 ** (db / 20)
        if len(a) == 0: return
        f = int(fade * sr)
        if f > 1: a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        bed[i:i + len(a)] += a
    def sfx(name, t, db, maxlen=None):
        p = SFXD + name + ".mp3" if os.path.exists(SFXD + name + ".mp3") else KSFX + name + ".wav"; a = load(p); a = a / (np.max(np.abs(a)) + 1e-9) * vr * 3.2
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
    # music beds (Kevin MacLeod, CC BY) ≤ -22 dB under the voice
    music("Thunder Dreams.mp3", tl(10), tl(54), -24); music("Man Down.mp3", tl(54), tl(95), -25)
    music("Thunder Dreams.mp3", tl(95), tl(137), -25); music("Rising Tide.mp3", tl(137), tl(157), -27); music("Man Down.mp3", tl(157), tl(188), -25)
    music("Thunder Dreams.mp3", tl(188), DUR, -22)
    loop("roomtone_dark_cinematic", 0, tl(10), -20); loop("heartbeat_slow", tl(2), tl(6), -24)
    loop("roomtone_dark_cinematic", tl(54), tl(137), -30); loop("ambience_cinematic_suspense", tl(95), tl(126), -31)
    HITS = [("hit_deep_heartbeat_impact", -17), ("hit_short_bass", -19), ("hit_glass_suspense", -21), ("hit_cinematic_deep_impact", -20)]
    SWIPES = [("highlighter", -18), ("whoosh_fast_transition", -22), ("paper_slide", -20)]; MK = [0]
    for i, (ln, (kind, a)) in enumerate(SHOTS):
        t0 = T[ln] - 0.12
        if kind == "card":
            for j in range(len(a["big"])):
                if a["big"][j] != " ": sfx("typewriter_single_hit", t0 + 0.05 + j / 12, -20)
            sfx("clock_tick_single", t0, -16); sfx("whoosh_tunnel_reverb", t0 - 0.4, -26)
        elif kind == "doc": sfx("paper_slide", t0, -18); sfx("typewriter_soft_click", t0 + 0.2, -24)
        elif kind == "prints":
            for it in a["items"]: sfx("paper_slide", t0 + it[6], -17); sfx("camera_vintage_shutter", t0 + it[6] + 0.15, -24)
        elif kind == "vid" and a["name"] in ("H18", "H19", "H21", "H23"): loop("waves_rough_sea_loop", t0, T[SHOTS[i + 1][0]] if i + 1 < len(SHOTS) else DUR, -28)
        elif kind == "map": sfx("paper_page_turn", t0, -22)
        elif kind == "title": sfx("hit_cinematic_deep_impact", t0, -12); sfx("typewriter_return_bell", t0 + 2.0, -20)
        elif kind == "kb": sfx("whoosh_fast_transition", t0 - 0.1, -32)
        for mk in a.get("marks", ()):                                 # highlight sounds, varied: a soft hit on the dim, a swipe on the underline
            tm = mark_time(mk, ln); MK[0] += 1; h = HITS[MK[0] % len(HITS)]; w = SWIPES[MK[0] % len(SWIPES)]
            sfx(h[0], tm, h[1], maxlen=1.8); sfx(w[0], tm + 0.1, w[1], maxlen=0.9)
        if kind == "map":
            for op in a["ops"]:
                if op[0] == "ring": sfx("camera_lens_autofocus", t0 + op[2], -26, maxlen=1.0); sfx("typewriter_soft_click", t0 + op[2] + 0.3, -22)
                if op[0] == "pin": sfx("camera_classic_click", t0 + op[2], -22)
    for ln, off, kind, a in OV:
        if kind == "stamp": sfx("hit_horror_drum", T[ln] + off, -14)
        if kind in ("typecenter", "typecenter_red", "list", "list_side"): sfx("typewriter_typing_old", T[ln] + off, -26)
    sfx("hit_cinematic_deep_impact", 0.0, -14)
    for j in range(7): sfx("typewriter_single_hit", 0.05 + j / 12, -20)
    EV = [(1, 0.2, "footsteps_tunnel_loop", -24), (5, 0.6, "hit_cinematic_deep_impact", -12), (5, 0.5, "metal_tool_drop", -18), (9, 0, "clock_pendulum_ticking", -20),
          (32, 0.6, "drill_on_off", -22), (31, 0.4, "metal_tool_falling", -24), (38, 0.2, "papers_moving", -24), (46, 0.5, "gear_metallic_lock", -20),
          (55, 0.3, "prison_metal_door_close", -12), (55, 1.0, "locking_door_with_keys", -18), (57, 0.2, "keys_moving", -22), (59, 0.4, "waves_with_birds", -26),
          (63, 0.9, "light_switch", -12), (63, 1.2, "prison_metal_door_close", -18), (67, 1.2, "footsteps_stones_loop", -22), (74, 0, "clock_wall_tick", -20),
          (82, 0.6, "heavy_sliding_door", -18), (84, 0.4, "heartbeat_horror_drum", -16), (87, 0.3, "metal_tool_falling", -20), (88, 0.3, "wind_ambience", -24),
          (91, 0.3, "waves_harbor_rocks", -24), (97, 1.4, "factory_metal_hard_hit", -10), (98, 0.1, "factory_metal_hard_hit", -12), (99, 0.1, "factory_metal_hard_hit", -12),
          (99, 1.0, "telephone_old_ring", -20), (100, 0.4, "radio_static_crackles", -22), (101, 0.2, "footsteps_tunnel_loop", -24), (106, 0.2, "clock_ticking_closeup", -22),
          (107, 0.4, "waves_rough_sea_loop", -22), (110, 0.4, "radio_static_fx", -24), (119, 0.3, "wind_scary", -22), (122, 0.6, "wind_deep_cinematic_hum", -26),
          (124, 0.6, "waves_with_birds", -24), (126, 0.6, "clock_bells_hour", -20), (127, 0.4, "heartbeat_slow", -20), (130, 1.4, "hit_cinematic_deep_impact", -12),
          (132, 0.0, "siren_vintage_manual", -18), (132, 0.2, "alarm_vintage_warning", -24), (133, 0.6, "telephone_vintage_ring", -22), (135, 0.6, "keys_moving", -22),
          (138, 0.2, "helicopter_far_away", -18), (138, 0.8, "motorboat_sea", -24), (140, 0.4, "sea_water_splash", -20), (141, 0.6, "water_splash", -22),
          (144, 0.4, "sea_swimming_loop", -22), (147, 0.4, "waves_rocky_shore", -24), (150, 0.4, "paper_big_page_turn", -18), (152, 0.4, "ship_engine_loop", -22),
          (152, 1.4, "ship_hull_creak", -22), (157, 0.4, "prison_metal_door_close", -14), (159, 0.3, "typewriter_typing_old", -22), (162, 0.6, "newspaper_drop", -18),
          (167, 0.4, "paper_signing", -20), (173, 0.3, "camera_classic_click", -18), (179, 0.3, "camera_old_shutter_click", -18), (182, 0.6, "heartbeat_single", -14),
          (186, 0.3, "factory_metal_hard_hit", -14), (187, 0.3, "waves_rough_sea_loop", -24), (189, 0.2, "typewriter_return_bell", -18)]
    for ln, off, name, db in EV: sfx(name, T[ln] + off, db)
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
def final(n):
    with open(B + "segs.txt", "w") as f:
        for i in range(n): f.write(f"file 'seg_{i}.mp4'\n")
    os.makedirs(ROOT + "export", exist_ok=True); out = ROOT + "export/TheLastHours_01_Alcatraz_v3.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True); print(out)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "qa":
        ts = [float(x) for x in sys.argv[2:]]; tiles = [frame(t).convert("RGB").resize((480, 270)) for t in ts]
        S = Image.new("RGB", (4 * 490, ((len(tiles) + 3) // 4) * 300), (20, 20, 20))
        for i, (im, t) in enumerate(zip(tiles, ts)): S.paste(im, ((i % 4) * 490, (i // 4) * 300)); ImageDraw.Draw(S).text(((i % 4) * 490 + 6, (i // 4) * 300 + 274), f"{t:.1f}", fill=(255, 220, 90))
        S.save(B + "qa.png"); print(B + "qa.png")
    elif m == "times":
        for i in range(0, len(LINES), 1): print(f"{i:3d} {T[i]:7.2f} {LINES[i][:70]}")
        print("VO_END", VO_END, "DUR", DUR)
    elif m == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif m == "audio": audio()
    elif m == "final": final(int(sys.argv[2]))
    elif m == "all":
        n = int(sys.argv[2]); env = dict(os.environ, PYTHONUTF8="1")
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), "seg", str(i), str(n)], env=env) for i in range(n)]
        for p in ps: p.wait()
        audio(); final(n)
