ROOT = "D:/why habibi/_newchannel/29_dreamworks_revenge/"
VO = "dw_vo_chatterbox.wav"
ENDL = 211
SHOTS = ROOT + "shots_dw.py"
DOCS = ()
ENDBG = "C6"
NAME = "TheLastHours_29_DreamWorks_Disney_Said_No.mp4"
DOC = '''"""The Last Hours #29: DreamWorks, the studio built out of a grudge (Easter Sunday 3 Apr 1994, Frank Wells dies -> Eisner says no ->
DreamWorks SKG 12 Oct 1994 -> Shrek and the first Best Animated Feature Oscar -> 2014-15 crash -> Comcast, $3.8B, 2016).
Owner 27 Nov 2026: our own English version of an Omar Qany topic for US viewers, friend tone + NOAH host avatar (sparing).
Real images only: Wikimedia Commons (PD / CC BY / CC BY-SA, credits in CREDITS.md), White House (PD); Pexels labelled ILLUSTRATIVE.
Never shown: film clips, posters, characters, studio logos or signs, any woman. Facts: research/research.md.
  uv run --no-project --with pillow --with numpy --with soundfile python render_dw29.py times | qa [t..] | seg i n | audio | final n | all n | chapters | prep"""
'''
TBLOCK = r'''CROP = {"C6": (0.0, 0.3, 1.0, 1.0), "C9": (0.0, 0.22, 1.0, 1.0), "B6": (0.0, 0.0, 0.85, 1.0)}
ILL = "ILLUSTRATIVE  ·  PEXELS"
TB = {"B1": "JEFFREY KATZENBERG, 2014  ·  WTTC (CC BY 2.0)", "B3": "JEFFREY KATZENBERG, 2014  ·  WIKIMEDIA COMMONS", "B4": "JEFFREY KATZENBERG, 2022  ·  WIKIMEDIA COMMONS",
      "B5": "JEFFREY KATZENBERG, 2007  ·  WIKIMEDIA COMMONS", "B6": "OBAMA AND KATZENBERG, WHITE HOUSE, 2014  ·  WHITE HOUSE (PD)",
      "B7": "NATIONAL MEDAL OF ARTS, 2014  ·  WHITE HOUSE (PD)", "B8": "NATIONAL MEDAL OF ARTS, 2014  ·  WHITE HOUSE (PD)",
      "B9": "STEVEN SPIELBERG, 1999  ·  U.S. DEPT. OF DEFENSE (PD)", "B10": "STEVEN SPIELBERG, 2017  ·  GAGE SKIDMORE (CC BY-SA)", "B11": "STEVEN SPIELBERG, 2011  ·  WIKIMEDIA COMMONS",
      "B13": "DAVID GEFFEN, 1973  ·  WIKIMEDIA COMMONS", "B14": "MICHAEL EISNER, c. 1977  ·  WIKIMEDIA COMMONS (PD)", "B15": "MICHAEL EISNER, 2010  ·  WIKIMEDIA COMMONS",
      "B16": "PAUL ALLEN, 2013  ·  WIKIMEDIA COMMONS", "B17": "PAUL ALLEN, 2011  ·  WIKIMEDIA COMMONS", "B18": "JERRY SEINFELD, 1997  ·  WIKIMEDIA COMMONS",
      "B19": "CHRIS MELEDANDRI, 2023  ·  WIKIMEDIA COMMONS", "B20": "JOHN LASSETER, 2011  ·  WIKIMEDIA COMMONS", "B21": "JOHN LASSETER, 2002  ·  WIKIMEDIA COMMONS",
      "C1": "PDI/DREAMWORKS, REDWOOD CITY, 2010  ·  WIKIMEDIA COMMONS", "C2": "PDI/DREAMWORKS, REDWOOD CITY  ·  WIKIMEDIA COMMONS", "C3": "PDI/DREAMWORKS, REDWOOD CITY  ·  WIKIMEDIA COMMONS",
      "C5": "PACIFIC SHORES CENTER, REDWOOD CITY  ·  WIKIMEDIA COMMONS", "C6": "DREAMWORKS ANIMATION, GLENDALE, 2014  ·  WIKIMEDIA COMMONS",
      "C7": "WALT DISNEY STUDIOS, BURBANK  ·  WIKIMEDIA COMMONS", "C9": "DISNEY / ABC BUILDING, BURBANK  ·  WIKIMEDIA COMMONS",
      "C10": "WALT DISNEY'S OFFICE, RESTORED  ·  WIKIMEDIA COMMONS", "C11": "BURBANK FROM THE AIR, 2014  ·  WIKIMEDIA COMMONS",
      "C12": "COMCAST CENTER, PHILADELPHIA  ·  WIKIMEDIA COMMONS", "C13": "COMCAST CENTER, PHILADELPHIA, 2007  ·  WIKIMEDIA COMMONS",
      "C14": "CENTER CITY, PHILADELPHIA, 2024  ·  WIKIMEDIA COMMONS", "C15": "COMCAST CENTERS, PHILADELPHIA, 2025  ·  WIKIMEDIA COMMONS",
      "C17": "UNIVERSAL STUDIOS BACKLOT, 2008  ·  WIKIMEDIA COMMONS", "C18": "UNIVERSAL STUDIOS BACKLOT, 2011  ·  WIKIMEDIA COMMONS",
      "C19": "NEW YORK STOCK EXCHANGE  ·  WIKIMEDIA COMMONS", "C20": "NEW YORK STOCK EXCHANGE, 2015  ·  WIKIMEDIA COMMONS",
      "M1": "LAMOILLE CANYON, RUBY MOUNTAINS  ·  BLM (PD)", "M2": "RUBY MOUNTAINS IN WINTER  ·  WIKIMEDIA COMMONS", "M3": "RUBY MOUNTAINS, NEVADA  ·  WIKIMEDIA COMMONS",
      "M4": "LAMOILLE CANYON FROM THE AIR  ·  WIKIMEDIA COMMONS", "M5": "LAMOILLE CANYON FROM THE AIR  ·  WIKIMEDIA COMMONS",
      "M6": "RUBY MOUNTAINS, APRIL 2009  ·  WIKIMEDIA COMMONS", "M8": "NEVADA FROM THE ISS, 2008  ·  NASA (PD)", "M10": "THE RUBY MOUNTAINS, NEVADA  ·  WIKIMEDIA COMMONS"}
for _r in ["E%d" % i for i in range(1, 30)]: TB[_r] = ILL
def DT(rid):
    m = re.match(r"(A\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD")
'''
LIFT = {"E16": 0.7, "E15": 0.75, "E3": 0.75, "E19": 0.7, "E26": 0.7}
CAPFIX = {"Far-kwahd": "Farquaad", "Farquad": "Farquaad", "Styg": "Steig", "Stig": "Steig", "Kwib-ee": "Quibi", "Quibie": "Quibi", "Kwibi": "Quibi",
          "Mel-eh-dan-dree": "Meledandri", "Meladandri": "Meledandri", "Katzenburg": "Katzenberg", "Geffin": "Geffen", "Ants": "Antz",
          "Awesomeness T V": "AwesomenessTV", "Lassiter": "Lasseter", "Eisener": "Eisner", "Ice-ner": "Eisner", "Wall-E": "WALL-E", "Farbwad": "Farquaad", "Farkwad": "Farquaad", "Farquad": "Farquaad"}
MUSIC = '''    music("Darkling.mp3", 0.0, tl(10), -12, later=(tl(9), -16)); music("Marty Gots a Plan.mp3", tl(10), tl(28), -18)
    music("Inspired.mp3", tl(28), tl(49), -19); music("Late Night Radio.mp3", tl(49), tl(63), -19); music("Dream Culture.mp3", tl(63), tl(71), -19)
    music("Son Of A Rocket.mp3", tl(71), tl(91), -19); music("Overcast.mp3", tl(91), tl(98), -19); music("Vibing Over Venus.mp3", tl(98), tl(108), -18)
    music("Marty Gots a Plan.mp3", tl(108), tl(121), -19); music("Inspired.mp3", tl(121), tl(134), -19); music("Daily Beetle.mp3", tl(134), tl(150), -19)
    music("Overcast.mp3", tl(150), tl(165), -19); music("Eternity.mp3", tl(165), tl(174), -19); music("Industrial Cinematic.mp3", tl(174), tl(184), -18)
    music("Stay the Course.mp3", tl(184), tl(196), -18); music("Wallpaper.mp3", tl(196), tl(205), -19); music("Promises to Keep.mp3", tl(205), DUR, -17)
    loop("roomtone_dark_cinematic", 0.0, tl(10), -30)
'''
EV = [(1, 0.0, "clock_tick_single", -20), (3, "down", "hit_big_cinematic_impact", -16), (8, "billion", "hit_cinematic_deep_impact", -16),
      (10, 0.0, "clock_tick_single", -20), (20, "no", "hit_short_bass", -17), (25, 0.0, "paper_slide", -22), (32, 0.0, "clock_tick_single", -20),
      (35, "five", "hit_short_bass", -18), (46, "sued", "metal_hammer_hit", -19), (48, "two", "hit_cinematic_deep_impact", -17), (60, "october", "whoosh_fast_transition", -20),
      (68, "flop", "hit_short_bass", -18), (89, "shrek", "hit_big_cinematic_impact", -15), (94, "sinks", "sweep_terror_darkness", -25),
      (99, "hundred", "hit_short_bass", -18), (103, "three", "hit_cinematic_deep_impact", -17), (111, "eight", "hit_short_bass", -18),
      (120, "nine", "hit_cinematic_deep_impact", -17), (161, "eighty", "hit_short_bass", -18), (172, "billion", "hit_short_bass", -18),
      (176, "hard", "sweep_terror_darkness", -25), (181, "five", "hit_cinematic_deep_impact", -16), (183, "shut", "metal_hammer_hit", -18),
      (184, 0.0, "clock_tick_single", -20), (186, "billion", "hit_big_cinematic_impact", -15), (200, "shutting", "hit_short_bass", -18),
      (ENDL, -0.55, "metal_hammer_hit", -16)]
CH = [(0, "Easter Sunday, 1994"), (10, "Disney says no"), (28, "DreamWorks SKG"), (41, "The lawsuit"), (49, "Antz vs. A Bug's Life"),
      (63, "Prince of Egypt and El Dorado"), (71, "Shrek"), (91, "The wobble"), (98, "Shrek 2 and the IPO"), (108, "The 8% problem"),
      (121, "Bee Movie, Panda, Dragon"), (134, "Katzenberg's bets"), (150, "The market changes"), (165, "Obama at DreamWorks"),
      (174, "The crash"), (184, "Comcast: $3.8 billion"), (196, "After"), (205, "What the files can tell you")]
