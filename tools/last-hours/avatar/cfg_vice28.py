ROOT = "D:/why habibi/_newchannel/28_vice_city_real/"
VO = "vice_vo_chatterbox.wav"
ENDL = 231
SHOTS = ROOT + "shots_vice.py"
DOCS = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8")
ENDBG = "C1"
NAME = "TheLastHours_28_Vice_City_Was_Real.mp4"
DOC = '''"""The Last Hours #28: Vice City Was Real, Miami 1979-1986 (Dadeland Wed 11 Jul 1979 2:30 PM -> the FBI Miami shootout Fri 11 Apr
1986 ~9:35 AM -> GTA Vice City 2002 / GTA VI 2026). Friend tone (owner 26 Nov: Omar Qany GTA reference) + the NOAH host avatar
(owner 27 Nov: cutaways on aside lines, sparing; corner pops; Noah end screen). Real images only: White House / Reagan Library papers,
NARA, USCG, HABS, Florida Memory / Florida Keys Public Libraries (CC BY), Wikimedia Commons; Pexels clips labelled ILLUSTRATIVE.
Never shown: bodies, crime-scene photos, any woman, film/TV/game images. Facts: research/research.md.
  uv run --no-project --with pillow --with numpy --with soundfile python render_vice28.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
'''
TBLOCK = r'''CROP = {"E3": (0.0, 0.0, 1.0, 0.65), "B6": (0.0, 0.15, 1.0, 0.45), "B8": (0.15, 0.0, 1.0, 1.0), "B10": (0.0, 0.0, 0.92, 1.0),
        "C4": (0.0, 0.0, 1.0, 0.7), "C14": (0.0, 0.0, 0.95, 1.0), "C16": (0.45, 0.0, 1.0, 1.0), "C26": (0.0, 0.0, 0.7, 1.0)}
ILL = "ILLUSTRATIVE  ·  PEXELS"
TB = {"B1": "SPECIAL AGENTS JERRY DOVE AND BENJAMIN GROGAN  ·  FBI", "B2": "PRESIDENT RONALD REAGAN, 1981  ·  WHITE HOUSE",
      "B3": "VICE PRESIDENT GEORGE H. W. BUSH  ·  WHITE HOUSE", "B4": "REAGAN AND BUSH, 16 JUL 1981  ·  NARA",
      "B5": "REAGAN AND BUSH, OVAL OFFICE, 1982  ·  WHITE HOUSE", "B6": "REAGAN AND THE SOUTH FLORIDA TASK FORCE, 17 NOV 1982  ·  WHITE HOUSE",
      "B7": "PRESIDENT JIMMY CARTER  ·  WHITE HOUSE", "B8": "FIDEL CASTRO, WASHINGTON, 1959  ·  LIBRARY OF CONGRESS",
      "B9": "ARRIVING AT KEY WEST, 1980  ·  U.S. COAST GUARD", "B10": "KEY WEST, 1980  ·  FLORIDA KEYS PUBLIC LIBRARIES (CC BY)",
      "B11": "LITTLE HAVANA, MIAMI, c. 1980  ·  FLORIDA MEMORY",
      "C1": "DOWNTOWN MIAMI, MAY 1984  ·  FLORIDA MEMORY", "C2": "MIAMI, 1986  ·  METRO-DADE TRANSIT", "C3": "DOWNTOWN MIAMI, 1980s  ·  METRO-DADE",
      "C4": "DOWNTOWN MIAMI, 1980s  ·  METRO-DADE", "C5": "BAYFRONT, MIAMI, JUNE 1985  ·  FLORIDA MEMORY",
      "C6": "OCEAN DRIVE, MIAMI BEACH, 1980  ·  HABS / LIBRARY OF CONGRESS", "C7": "CARDOZO HOTEL, OCEAN DRIVE  ·  HABS", "C8": "COLLINS AVENUE  ·  HABS",
      "C9": "HENROSA HOTEL, COLLINS AVENUE  ·  HABS", "C10": "MIAMI BEACH, 1980  ·  HABS", "C11": "ESPAÑOLA WAY, MIAMI BEACH, 1980  ·  HABS",
      "C12": "KEY WEST, 1980  ·  FLORIDA KEYS PUBLIC LIBRARIES (CC BY)", "C13": "KEY WEST, 1980  ·  FLORIDA KEYS PUBLIC LIBRARIES (CC BY)",
      "C14": "KEY WEST, 1980  ·  FLORIDA KEYS PUBLIC LIBRARIES (CC BY)", "C15": "IMPOUNDED BOATLIFT BOATS, KEY WEST, 1980  ·  FKPL (CC BY)",
      "C16": "KEY WEST, 1980  ·  FLORIDA KEYS PUBLIC LIBRARIES (CC BY)", "C17": "KEY WEST, 1980  ·  FLORIDA KEYS PUBLIC LIBRARIES (CC BY)",
      "C18": "USCGC DILIGENCE, KEY WEST, 1980  ·  FKPL (CC BY)", "C19": "USCGC VALIANT, KEY WEST, 1980  ·  FKPL (CC BY)", "C20": "KEY WEST, EARLY 1980s  ·  FKPL (CC BY)",
      "C21": "DADELAND, KENDALL, TODAY  ·  WIKIMEDIA COMMONS", "C22": "DADELAND, KENDALL, TODAY  ·  WIKIMEDIA COMMONS",
      "C23": "THE MIAMI RIVER, TODAY  ·  WIKIMEDIA COMMONS", "C24": "MOUTH OF THE MIAMI RIVER  ·  WIKIMEDIA COMMONS", "C25": "THE MIAMI RIVER  ·  WIKIMEDIA COMMONS",
      "C26": "OVERTOWN, TODAY  ·  WIKIMEDIA COMMONS", "C27": "SW 82ND AVENUE, PINECREST, TODAY  ·  WIKIMEDIA COMMONS",
      "C28": "THE MEMORIAL ON SW 82ND AVENUE  ·  AQUARIUSPL (CC BY-SA)", "C29": "THE MEMORIAL ON SW 82ND AVENUE  ·  AQUARIUSPL (CC BY-SA)",
      "C30": "SW 82ND AVENUE TODAY  ·  AQUARIUSPL (CC BY-SA)", "C31": "A RUGER MINI-14  ·  WIKIMEDIA COMMONS", "C32": "SMITH & WESSON 1006, 10 MM  ·  WIKIMEDIA COMMONS",
      "C33": "SMITH & WESSON 4006, .40 S&W  ·  WIKIMEDIA COMMONS", "M1": "THE CARIBBEAN  ·  CIA", "M2": "THE CARIBBEAN  ·  CIA",
      "M3": "CUBA  ·  CIA", "M4": "CUBA AND THE FLORIDA KEYS, 1964  ·  CIA / LIBRARY OF CONGRESS", "M5": "THE FLORIDA STRAITS  ·  NOAA",
      "M6": "THE CARS ON SW 82ND AVENUE (DIAGRAM)  ·  WIKIMEDIA COMMONS",
      "A1": "TASK FORCE MEETING, 27 JAN 1982  ·  REAGAN LIBRARY", "A2": "VP BUSH PRESS RELEASE, 16 FEB 1982  ·  REAGAN LIBRARY",
      "A3": "TASK FORCE FACT SHEET, 1982  ·  REAGAN LIBRARY", "A4": "BANK SECRECY ACT REQUEST, 1982  ·  REAGAN LIBRARY",
      "A5": "COAST GUARD REQUEST, 1982  ·  REAGAN LIBRARY", "A6": "FLORIDA CRIME FACT SHEET, 1982  ·  REAGAN LIBRARY",
      "A7": "DOD SUPPORT FACT SHEET, 1982  ·  REAGAN LIBRARY", "A8": "PUBLIC LAW 99-570, 1986  ·  U.S. CONGRESS"}
for _r in ["E%d" % i for i in range(1, 31)]: TB[_r] = ILL
def DT(rid):
    m = re.match(r"(A\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD")
'''
LIFT = {"E19": 0.55, "E20": 0.8, "E10": 0.8, "E11": 0.8, "E5": 0.85}
CAPFIX = {"Pah-nesso": "Panesso", "Hee-meh-nez": "Jimenez", "Mah-ree-el": "Mariel", "Mah-ree-eh-lee-tos": "Marielitos", "Yer-ko-vich": "Yerkovich",
          "Man-ow-zee": "Manauzzi", "Mih-reh-less": "Mireles", "May-tix": "Matix", "Ko-yah-so": "Collazo", "Bree-el": "Briel", "Lee-oh-nee-da": "Leonida",
          "How-zer": "Houser", "Kah-tahn": "Kattan", "Gro-gan": "Grogan", "Opa-Locka": "Opa-locka", "Opalocka": "Opa-locka", "Matics": "Matix", "Mattix": "Matix", "Dubs": "Dove", "Dadd": "Dade", "Warwacken": "war wagon", (46, "countries"): "country's", (192, "aid"): "eight", "Cop": "Cops"}
MUSIC = '''    music("I Can Feel it Coming.mp3", 0.0, tl(11), -12, later=(tl(10), -16)); music("Stay the Course.mp3", tl(11), tl(30), -18)
    music("Late Night Radio.mp3", tl(30), tl(50), -19); music("Stay the Course.mp3", tl(50), tl(68), -19); music("Floating Cities.mp3", tl(68), tl(86), -19)
    music("Man Down.mp3", tl(86), tl(93), -18); music("Industrial Cinematic.mp3", tl(93), tl(110), -18); music("Rising Tide.mp3", tl(110), tl(128), -18)
    music("Late Night Radio.mp3", tl(128), tl(146), -18); music("I Can Feel it Coming.mp3", tl(146), tl(162), -18); music("Thunder Dreams.mp3", tl(162), tl(194), -18)
    music("Rising Tide.mp3", tl(194), tl(207), -19); music("Late Night Radio.mp3", tl(207), tl(223), -18); music("Promises to Keep.mp3", tl(223), DUR, -17)
    loop("roomtone_dark_cinematic", 0.0, tl(11), -30); loop("waves_rocky_shore", tl(35), tl(38), -30); loop("waves_harbor_rocks", tl(73), tl(79), -31)
'''
EV = [(1, 0.0, "hit_big_cinematic_impact", -15), (2, 0.0, "clock_tick_single", -20), (5, "cowboys", "hit_short_bass", -18), (6, "room", "sweep_terror_darkness", -24),
      (7, "deadliest", "hit_cinematic_deep_impact", -16), (9, "copied", "hit_horror_drum", -18), (15, "fire", "hit_big_cinematic_impact", -16), (20, "wagon", "hit_short_bass", -18),
      (25, "prosecuted", "hit_short_bass", -18), (38, "seventy", "hit_cinematic_deep_impact", -17), (44, "billion", "hit_big_cinematic_impact", -15),
      (46, "entire", "hit_short_bass", -18), (54, "twelve", "hit_short_bass", -18), (61, "ninety", "hit_short_bass", -18), (68, 0.0, "clock_tick_single", -20),
      (76, "eighty", "hit_cinematic_deep_impact", -17), (89, "burning", "sweep_terror_darkness", -24), (98, "six", "hit_big_cinematic_impact", -14),
      (100, "room", "heartbeat_single", -16), (104, "paradise", "newspaper_drop", -20), (111, 0.0, "paper_slide", -22), (123, "steal", "hit_short_bass", -18),
      (124, "drowned", "sweep_horror_long", -26), (131, 0.0, "whoosh_fast_transition", -20), (162, 0.0, "clock_tick_single", -20), (170, 0.0, "clock_tick_single", -20),
      (175, "ram", "metal_hammer_hit", -18), (176, "shooting", "hit_big_cinematic_impact", -15), (184, "killed", "hit_cinematic_deep_impact", -16),
      (190, "hundred", "hit_cinematic_deep_impact", -16), (198, "everything", "hit_short_bass", -18), (219, "ninety", "hit_big_cinematic_impact", -16),
      (229, "real", "hit_cinematic_deep_impact", -15), (ENDL, -0.55, "metal_hammer_hit", -16)]
CH = [(0, "2:30 PM, a shopping mall in Miami"), (11, "Dadeland, 11 July 1979"), (30, "How Miami got here"), (50, "Too much cash"), (68, "Mariel, 1980"),
      (86, "One more fire"), (93, "1981: the record year"), (110, "Washington steps in"), (120, "The Miami River Cops"), (128, "Scarface and Miami Vice"),
      (146, "Platt and Matix"), (162, "Friday, 11 April 1986"), (194, "What the FBI changed"), (207, "Miami after"), (212, "Vice City and GTA VI"), (223, "What the files can tell you")]
