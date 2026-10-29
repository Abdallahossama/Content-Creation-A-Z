"""Build render_alcatraz46.py from render_goering.py: same engine (subpop across cuts, badges, DOC spotlights, film finish),
file-14 blocks swapped in (docstring, paths, tags, SHOTS, OV, CAPFIX, music/SFX, chapters).  uv run --no-project python _build_render.py"""
SRC = "D:/why habibi/_newchannel/13_goering_last_night/render_goering.py"
DST = "D:/why habibi/_newchannel/14_battle_of_alcatraz/render_alcatraz46.py"
G = open(SRC, encoding="utf-8").read().split("\n")
def blk(a, b): return "\n".join(G[a - 1:b])            # 1-indexed, inclusive

DOC = '''"""The Last Hours #14: the Battle of Alcatraz, Thursday 2 - Saturday 4 May 1946 (the gun cage, cells 403/402, key 107, the siege,
the grenades on the roof, the trial). Case File style, colour grade, 1920x1080, burned-in captions, film finish. Built on render_goering.py.
Real images only: NPS Golden Gate NRA museum photos and the 1946 BOP report, NARA warden's notebook cards, HABS (Library of Congress),
the US Attorney's brief, 1946 newspapers, Universal newsreel outtakes (safe seconds only), Pexels textures labelled ILLUSTRATIVE.
Never shown: the dead, the morgue, the wounded, any woman. Owner rules: research/research.md (do-not-say), assets.md section H.
  uv run --no-project --with pillow --with numpy --with soundfile python render_alcatraz46.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""'''

PATHS = '''ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"; M = ROOT + "media/"; B = ROOT + "build/"; os.makedirs(B, exist_ok=True)'''
VOF = '''VOF = os.environ.get("LH_VOF", ROOT + "vo/alcatraz46_vo_chatterbox.wav")'''
ISDOC = '''def isdoc(rid): return rid[0] == "A" and rid not in ("A7", "A8", "A9", "A10")      # A7-A10 are museum objects: graded like photos'''
MAPS = '''# (no Natural-Earth map in this file: the bay is shown on the real USGS sheet and the NPS plan)'''

TAGS = r'''CROP = {}                                                         # portrait photos: a 16:9 band (set after the contact sheet)
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
            "5": "“DETAIL AT GUN GALLERY”, BUREAU OF PRISONS REPORT, 1946  ·  NPS", "6": "UNITED PRESS TO WARDEN JOHNSTON, 4 MAY 1946  ·  NPS",
            "7": "THE BAR SPREADER, 1946  ·  NPS MUSEUM COLLECTION", "8": "BULLETS RECOVERED AFTER THE BATTLE  ·  NPS MUSEUM COLLECTION",
            "9": "AN ALCATRAZ THOMPSON GUN, MODEL 1928  ·  NPS MUSEUM COLLECTION", "10": "CELL-LOCKING INSTRUCTIONS, c. 1934  ·  NPS MUSEUM COLLECTION",
            "11": "BRIEF FOR THE UNITED STATES, SHOCKLEY v. UNITED STATES, 1947  ·  PUBLIC.RESOURCE.ORG", "12": "MONROE MORNING WORLD, SUN 5 MAY 1946",
            "13": "NEW CASTLE NEWS, FRI 3 MAY 1946", "14": "EAST LIVERPOOL REVIEW, FRI 3 MAY 1946", "15": "CIRCLEVILLE HERALD, SAT 4 MAY 1946",
            "16": "DIXON EVENING TELEGRAPH, SAT 4 MAY 1946", "17": "GETTYSBURG TIMES, FRI 3 MAY 1946"}.get(n, "THE RECORD, 1946")'''

SHOTS = r'''SHOTS = [
 # COLD OPEN
 (0, KB("C1", z=(1.05, 1.15), c0=(0.55, 0.45))),                                  # frame 1: smoke bursting from the cell house, May 1946
 ((0, "ask"), KB("F5", z=(1.06, 1.18))),
 ((0, "five|die"), KBP("A12", crop=(0.0, 0.0, 1.0, 0.2), h=430)),
 ((0, "never"), KB("C2", z=(1.06, 1.18), c0=(0.5, 0.45))),
 (1, TCARD("2:00 PM", "Thursday, 2 May 1946  ·  Alcatraz", "C14")),
 (2, VID("D1a", at=2.0, crop=(0.0, 0.0, 1.0, 0.9))),
 ((2, "six|prisoners"), KB("C5", z=(1.03, 1.13))),
 (3, KB("C2", z=(1.1, 1.22), c0=(0.5, 0.45))),
 ((3, "nine|held"), KB("C6", z=(1.04, 1.14))),
 ((3, "marines|friday"), VID("D1c", at=4.0, crop=(0.0, 0.0, 1.0, 0.9))),
 (4, KBP("A5", h=900)),
 ((4, "key"), KB("F5", z=(1.1, 1.2), c0=(0.5, 0.5))),
 ((4, "happened|six"), KB("C17", z=(1.03, 1.12))),
 # THE SIX
 (5, VID("D2b", at=6.0, crop=(0.0, 0.0, 1.0, 0.9))),
 ((5, "nobody"), KB("C14", z=(1.04, 1.14), dim=0.2)),
 (6, KB("B1", z=(1.04, 1.14), c0=(0.5, 0.4))),
 ((6, "view|gallery"), KB("C17", z=(1.05, 1.15))),
 (7, KB("B3", z=(1.1, 1.24), c0=(0.5, 0.35))),
 (8, KB("B2", z=(1.04, 1.14), c0=(0.5, 0.4))),
 ((8, "shockley"), KB("B6", z=(1.08, 1.2), c0=(0.5, 0.35))),
 ((8, "hostage|took"), KB("B4", z=(1.12, 1.26), c0=(0.5, 0.3))),
 (9, KB("B5", z=(1.08, 1.2), c0=(0.5, 0.35))),
 ((9, "miran|thompson"), KB("B7", z=(1.08, 1.2), c0=(0.5, 0.35))),
 ((9, "clarence"), KB("B8", z=(1.08, 1.2), c0=(0.5, 0.35))),
 # THE GUN CAGE
 (10, KB("B7", z=(1.14, 1.3), c0=(0.5, 0.3), dim=0.15)),
 (11, KB("C8", z=(1.03, 1.13))),
 (12, KB("C19", z=(1.04, 1.14))),
 (13, KB("E1", z=(1.15, 1.35), c0=(0.3, 0.5))),
 ((13, "burch"), KBP("A5", h=900)),
 ((13, "armored|doors"), KB("C20", z=(1.03, 1.12))),
 (14, KB("C5", z=(1.08, 1.18), dim=0.2)),
 (15, KB("C2", z=(1.04, 1.16), c0=(0.5, 0.45))),
 ((15, "tool|stolen"), KB("A7", z=(1.04, 1.14))),
 ((15, "pushed|bars"), COUNTER([((15, "five|5"), "5 IN"), ((15, "seven|7"), "7 IN")], "THE GAP BETWEEN TWO GUN-GALLERY BARS", "C2", size=330)),
 (16, KB("C12", z=(1.04, 1.14))),
 ((16, "only|two"), KB("C2", z=(1.12, 1.24), c0=(0.5, 0.4), dim=0.25)),
 (17, KB("C3", z=(1.03, 1.13))),
 ((17, "cretzer"), KB("C4", z=(1.04, 1.14))),
 # KEY 107
 (18, TCARD("2:15 PM", "A kitchen supervisor walks in", "C8")),
 ((18, "coy|up"), KB("C17", z=(1.1, 1.2), c0=(0.45, 0.5))),
 (19, KB("C6", z=(1.06, 1.16))),
 ((19, "four|403"), DOC("A11", [("403", (19, "four|403"))])),
 (20, KB("C9", z=(1.03, 1.13))),
 ((20, "key|number"), COUNTER([((20, "one|107"), "107")], "THE KEY TO THE YARD DOOR", "C9", size=420)),
 (21, KB("C18", z=(1.04, 1.14))),
 (22, KB("F5", z=(1.04, 1.16), c0=(0.5, 0.45))),
 (23, KB("C10", z=(1.04, 1.14))),
 # THE TWO CELLS
 (24, KB("C6", z=(1.1, 1.2), dim=0.25)),
 (25, KB("B2", z=(1.1, 1.24), c0=(0.5, 0.4))),
 (26, KB("F15", z=(1.04, 1.14))),
 ((26, "miller|william"), KBP("A2", h=900)),
 (27, DOC("A11", [("Miller", (27, "statement|sworn")), ("telephone", (27, "telephone|dictated"))])),
 # SIEGE NIGHT
 (28, TCARD("3:23 PM", "“Serious trouble.”", "C16")),
 (29, KB("A9", z=(1.04, 1.14))),
 ((29, "didn|rifle"), KB("C12", z=(1.08, 1.18))),
 (30, VID("D1b", at=1.0, crop=(0.0, 0.0, 1.0, 0.9))),
 (31, KB("B12", z=(1.04, 1.14))),
 (32, KB("E5", z=(1.6, 1.9), c0=(0.55, 0.45))),
 (33, VID("D2a", at=2.0, crop=(0.0, 0.0, 1.0, 0.9))),
 ((33, "stairs|steep"), KB("C9", z=(1.06, 1.16))),
 (34, KBP("A2", h=900)),
 ((34, "gallery|went"), KB("C20", z=(1.08, 1.18), dim=0.2)),
 (35, VID("D5", at=4.0)),
 ((35, "searchlights|lit"), KB("F11", z=(1.03, 1.13))),
 (36, VID("D6", at=2.0, dim=0.2)),
 (37, KB("C16", z=(1.04, 1.14), dim=0.3)),
 (38, KB("C6", z=(1.12, 1.24), dim=0.35)),
 (39, KB("C21", z=(1.04, 1.14))),
 ((39, "other|three"), KB("C3", z=(1.06, 1.16), dim=0.2)),
 # GRENADES ON THE ROOF
 (40, TCARD("FRI 3 MAY", "Officer William Miller dies", "C17")),
 (41, KBP("A13", crop=(0.0, 0.0, 1.0, 0.22), h=420)),
 ((41, "marine|firing"), KB("C17", z=(1.04, 1.14), dim=0.15)),
 (42, VID("D1c", at=12.0, crop=(0.0, 0.0, 1.0, 0.9))),
 ((42, "hundred|150"), COUNTER([((42, "hundred|150"), "~150")], "GRENADES INTO THE CELL HOUSE  ·  THE MARINE MAJOR'S COUNT", "C1", size=360)),
 (43, KB("C1", z=(1.1, 1.24), c0=(0.55, 0.45))),
 ((43, "shoulder|sore"), KB("F9", z=(1.04, 1.14))),
 (44, KB("A9", z=(1.1, 1.22), dim=0.2)),
 (45, VID("D1d", at=2.0, crop=(0.0, 0.0, 1.0, 0.9))),
 ((45, "aquatic|telescope"), KB("F6", z=(1.03, 1.13))),
 (46, KB("C16", z=(1.08, 1.18))),
 (47, KB("B11", z=(1.06, 1.18), c0=(0.5, 0.45))),
 (48, KB("C3", z=(1.1, 1.2), dim=0.55)),
 # THE CORRIDOR
 (49, KB("C21", z=(1.08, 1.2))),
 (50, KBP("A12", crop=(0.0, 0.0, 1.0, 0.2), h=430)),
 (51, TCARD("12:10 PM", "“No prisoner escaped.”", "C14")),
 (52, KB("B10", z=(1.04, 1.14))),
 ((52, "cells|shouted"), KB("C5", z=(1.06, 1.16), dim=0.2)),
 (53, KB("C2", z=(1.04, 1.12), dim=0.4)),
 # THE TRIAL
 (54, KB("B9", z=(1.04, 1.14))),
 (55, DOC("A11", [("Shockley", (55, "trial|month"))], zoom=1.1)),
 (56, KB("B8", z=(1.12, 1.26), c0=(0.5, 0.3))),
 (57, TCARD("3 DEC 1948", "Shockley and Thompson  ·  San Quentin", "B9")),
 (58, KB("A8", z=(1.04, 1.14))),
 (59, KBP("A2", h=900)),
 # CARNES AND 1962
 (60, KB("B13", z=(1.04, 1.14))),
 (61, TCARD("11 JUN 1962", "Three men  ·  a utility corridor  ·  the roof", "C21")),
 ((61, "roof|over"), KB("C15", z=(1.04, 1.14))),
 (62, KB("C14", z=(1.06, 1.16))),
 # WHAT THE RECORD SHOWS + ASKS
 (63, KB("C5", z=(1.04, 1.12), dim=0.3)),
 (64, COUNTER([((64, "six"), "6 MEN"), ((64, "two|guns"), "2 GUNS"), ((64, "nine"), "9 OFFICERS"), ((64, "five|dead"), "5 DEAD"), ((64, "one|key"), "1 KEY")],
              "THE BATTLE OF ALCATRAZ  ·  2-4 MAY 1946", "C1", size=300)),
 (65, KB("F5", z=(1.06, 1.16), c0=(0.5, 0.45))),
 (66, KB("F13", z=(1.03, 1.12))),
 ((67, 0.0), ("end", {})),
]'''

OV = r'''OV = [
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
 (17, "cretzer", "under", "JOSEPH CRETZER, FREED FROM D BLOCK"),
 (19, 0.0, "typecenter", "9 OFFICERS  ·  2 CELLS"),
 (21, 0.2, "under", "OFFICER WILLIAM MILLER  ·  NO SAFE PHOTO"),
 (22, "never|found", "stamp", ("NEVER FOUND", 1240, 400)),
 (23, 0.0, "typecenter_red", "THE SIREN"),
 (24, 0.0, "badge", "THU 2 MAY  ·  ABOUT 3:00 PM"),
 (24, 0.3, "under", "OUTSIDE CELL 403"),
 (25, 0.4, "quote", ("“You mean they will get killed," + chr(10) + "don't you?”", "JOSEPH CRETZER, AS THE COURT RECORDED IT")),
 (26, "miller|william", "under", "WILLIAM MILLER DIED THE NEXT MORNING"),
 (27, 0.2, "under", "MILLER'S STATEMENT, DICTATED BY TELEPHONE"),
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
 (41, 0.2, "under", "MYTH OR RECORD: “MORTARS”"),
 (42, 0.3, "nameplate", ("CHARLES BUCKNER", "U.S. MARINE WARRANT OFFICER  ·  ON THE CELL-HOUSE ROOF")),
 (43, "noon", "badge", "FRI 3 MAY  ·  NOON"),
 (44, 0.2, "under", "SENT ON GENERAL JOSEPH STILWELL'S AUTHORITY"),
 (45, "telescope|ten", "under", "10 CENTS A LOOK, AQUATIC PARK PIER"),
 (47, 0.2, "nameplate", ("JAMES A. JOHNSTON", "WARDEN OF ALCATRAZ  ·  AGE 71")),
 (47, "deal|make", "quote", ("“We'll make a deal when you throw" + chr(10) + "out your guns and ammunition.”", "WARDEN JOHNSTON")),
 (49, 0.0, "badge", "SAT 4 MAY 1946"),
 (50, "dead", "under", "NO PHOTOGRAPHS OF THE DEAD ARE SHOWN"),
 (51, 0.0, "badge", "SAT 4 MAY  ·  12:10 PM"),
 (52, "saltwater|hey", "typecenter", "“HEY, SALTWATER JOHNSTON.”"),
 (53, 0.0, "list", ("2 GUNS", "9 OFFICERS IN 2 CELLS", "1 KEY THEY NEVER HAD", "0 REACHED THE YARD")),
 (53, "yard|reached", "subpop", None),                              # silent ask right after the payoff (LESSONS 37)
 (54, 0.2, "under", "SHOCKLEY AND THOMPSON FIRED NO SHOT"),
 (55, 0.2, "under", "A MONTH OF TRIAL  ·  NEARLY 2,200 PAGES"),
 (56, "spared", "typecenter", "CARNES: SPARED"),
 (57, 0.0, "badge", "FRI 3 DEC 1948"),
 (58, 0.2, "under", "CORONER'S JURY: THE OFFICERS' DEATHS WERE MURDER"),
 (59, 0.2, "under", "NATIONAL LAW ENFORCEMENT OFFICERS MEMORIAL"),
 (60, 0.3, "under", "CLARENCE CARNES, 1980"),
 (61, 0.0, "badge", "MON 11 JUN 1962"),
 (62, 0.2, "under", "“WHAT THE FBI FOUND WHEN 3 MEN VANISHED FROM ALCATRAZ”"),
 (63, 0.0, "typecenter", "WHAT THE RECORD SHOWS"),
 (65, 0.2, "under", "KEY 107: COULD THEY HAVE MADE IT?  TELL ME BELOW"),
]'''

BRAND = '''            L.text(c, "FILE 14  ·  ALCATRAZ  ·  MAY 1946", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)'''

CAPFIX = r'''CAPFIX = {"Khoi": "Coy", "Koi": "Coy", "Coy's": "Coy's", "Kretzer": "Cretzer", "Kretzer's": "Cretzer's", "Cretser": "Cretzer", "Kanns": "Carnes",
          "Khan's": "Carnes,", "Karns": "Carnes", "Kahns": "Carnes", "Karnes": "Carnes", "Birch": "Burch", "Stights": "Stites", "Steits": "Stites",
          "Stillwell": "Stilwell", "sellhouse": "cellhouse", "Sellhouse": "Cellhouse", "1.30": "1:30", "3.23": "3:23", "4.15": "4:15", "6.30": "6:30",
          "7.01": "7:01", "12.10": "12:10", "2.15": "2:15", (68, "everyone"): "every one", (68, "everyone."): "every one."}  # whisper spellings -> the record's'''

ENDBG = '''        c = L.vignette(L.kenburns(blur_bg("C14", None), t, t0, t1))'''

MUSIC = r'''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Industrial Cinematic.mp3", tl(5), tl(18), -17); music("Man Down.mp3", tl(18), tl(28), -17)
    music("Rising Tide.mp3", tl(28), tl(40), -17); music("Thunder Dreams.mp3", tl(40), tl(49), -17); music("Industrial Cinematic.mp3", tl(49), tl(54), -17)
    music("Man Down.mp3", tl(54), tl(63), -18); music("Promises to Keep.mp3", tl(63), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("ambience_cinematic_suspense", tl(18), tl(28), -31); loop("waves_rough_sea_loop", tl(28), tl(40), -33)
    loop("wind_deep_cinematic_hum", tl(49), tl(54), -31)'''

EV = r'''    sfx("hit_cinematic_deep_impact", 0.0, -12)                                   # the cold open starts on a hit
    EV = [(0, "key", "keys_moving", -20), (0, "five|die", "heartbeat_single", -18), (0, "never", "hit_short_bass", -18),
          (3, "grenades|dropping", "hit_big_cinematic_impact", -20), (6, 0.0, "prison_metal_door_close", -26), (8, "hostage|took", "keys_dropping", -24),
          (12, "walked", "footsteps_tunnel_loop", -30), (14, "door|stepped", "heavy_sliding_door", -26), (15, "climbed", "metal_tool_drop", -24),
          (16, "hit", "metal_hammer_hit", -22), (17, "keys", "keys_moving", -22), (19, "locked", "locking_door_with_keys", -22),
          (20, "one|107", "door_key_in_lock", -20), (22, "never|found", "hit_short_bass", -18), (23, "siren", "siren_vintage_manual", -24),
          (26, "fired", "hit_horror_drum", -18), (28, 0.0, "telephone_old_ring", -24), (30, 0.0, "motorboat_sea", -26),
          (31, "phoned", "telephone_vintage_ring", -26), (35, "searchlights|flares", "whoosh_ghostly", -26), (36, 0.0, "thunder_deep_rumble", -26),
          (42, "drilled", "drill_on_off", -26), (42, "lowered|grenades", "hit_big_cinematic_impact", -18), (43, "rifle|grenades", "hit_cinematic_deep_impact", -18),
          (45, "reporters", "reporters_camera_flashes", -26), (46, "phoned", "telephone_old_ring", -24), (49, 0.0, "heavy_sliding_door", -24),
          (50, "rifle|pistol", "metal_tool_falling", -24), (52, "walked", "reporters_camera_flashes", -28), (57, "executed|quentin", "hit_deep_heartbeat_impact", -20),
          (61, "roof", "wind_scary", -28), (63, 0.0, "hit_cinematic_deep_impact", -15), (68, 1.0, "typewriter_return_bell", -18)]'''
NAME = '''    name = name or "TheLastHours_14_BattleOfAlcatraz.mp4"'''
CH = r'''CH = [(0, "One key, six convicts"), (5, "The six"), (10, "The gun cage"), (18, "Key 107"), (24, "Two cells"),
      (28, "The siege night"), (40, "Grenades on the roof"), (49, "The corridor"), (54, "The trial"), (60, "Carnes and 1962"),
      (63, "What the record shows")]'''

out = [DOC, blk(7, 17), PATHS, blk(19, 25), VOF, blk(27, 62), ISDOC, blk(64, 114), MAPS, blk(118, 119), TAGS, blk(168, 180),
       SHOTS, blk(299, 301), OV, blk(371, 500), BRAND, blk(502, 564), CAPFIX, blk(569, 697), ENDBG, blk(699, 750), MUSIC, blk(756, 781), EV,
       blk(791, 804), NAME, blk(806, 811), CH, blk(815, 867)]
s = "\n".join(out)
for a, b in (("{rid:4}", "{rid:4}"),): s = s.replace(a, b)
open(DST, "w", encoding="utf-8").write(s); print("wrote", DST, len(s.split(chr(10))), "lines")
