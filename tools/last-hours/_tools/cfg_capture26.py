ROOT = "D:/why habibi/_newchannel/26_saddam_capture/"
VO = "capture_vo_chatterbox.wav"
ENDL = 83
SHOTS = ROOT + "shots_capture.py"
DOCS = ("A1", "A2", "A3")
ENDBG = "B1"
NAME = "TheLastHours_26_Saddam_Capture.mp4"
DOC = '''"""The Last Hours #26: the capture of Saddam Hussein, Operation Red Dawn, ad-Dawr near Tikrit, Saturday 13 December 2003
(about 10:50 a.m. the tip; about 6 p.m. 600 soldiers move out; about 8 p.m. two empty farmhouses; 8:26 p.m. two hands come up out of
the hole; 12:20 a.m. the first interrogation report; Sunday 3 p.m. "We got him"; the rumours; the FBI room, 1959). The File Keeper,
colour grade, 1920x1080, burned-in captions, film finish. Real images only: US Army / DoD / White House (PD), CENTCOM FOIA and FBI
documents (PD), CIA/NIMA maps (PD), file 11's vetted Baghdad set, Pexels textures labelled ILLUSTRATIVE. Never shown: the sons' bodies,
the execution, the mouth-exam frame, blood, any woman. Owner rules: research/research.md (content flags), research/assets.md.
  uv run --no-project --with pillow --with numpy --with soundfile python render_capture26.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
'''
TBLOCK = r'''CROP = {}
DOD, ARMY, ILL = "U.S. DEPARTMENT OF DEFENSE", "U.S. ARMY", "ILLUSTRATIVE  ·  PEXELS"
TB = {"B1": f"THE LID OVER THE HOLE, AD-DAWR, 17 DEC 2003  ·  {ARMY}", "B2": f"THE HUT'S KITCHEN, AD-DAWR, 17 DEC 2003  ·  {ARMY}",
      "B3": f"SADDAM HUSSEIN AFTER HIS CAPTURE, DEC 2003  ·  {DOD}", "B4": f"AFTER HIS BEARD WAS SHAVED, DEC 2003  ·  {DOD}",
      "B6": f"SANCHEZ AND BREMER, BAGHDAD, 14 DEC 2003  ·  {DOD}", "B7": "PRESIDENT BUSH, CABINET ROOM, 14 DEC 2003  ·  THE WHITE HOUSE",
      "B8": f"RUMSFELD AND GEN. PACE, THE PENTAGON, 16 DEC 2003  ·  {DOD}", "B9": f"BEFORE THE INVESTIGATING JUDGE, 1 JUL 2004  ·  {DOD}",
      "B10": "THE MOST-WANTED DECK, 2003: THE ACE OF SPADES  ·  DOD", "B11": f"FIRDOS SQUARE, BAGHDAD, 9 APR 2003  ·  {DOD}",
      "B12": "SADDAM'S PALACE, TIKRIT, 2003  ·  PD", "M1": "IRAQ, JAN 2003  ·  CIA", "M2": "IRAQ, COUNTRY PROFILE, 2003  ·  CIA", "M3": "TIKRIT, c. 2003  ·  NIMA",
      "A1": "FBI INTERVIEW SESSION 1, 7 FEB 2004  ·  FBI / NSA ARCHIVE", "A2": "FBI INTERVIEW SESSION 2, 8 FEB 2004  ·  FBI / NSA ARCHIVE",
      "A3": "FBI CASUAL CONVERSATION, 11 JUN 2004  ·  FBI / NSA ARCHIVE", "A4p4": "TACTICAL INTERROGATION REPORT 001-03, 13-14 DEC 2003  ·  CENTCOM FOIA",
      "A4p6": "TACTICAL INTERROGATION REPORT 001-03, 13-14 DEC 2003  ·  CENTCOM FOIA", "A5p1": "FRAGO 1217, CJTF-7, 14 DEC 2003  ·  CENTCOM FOIA",
      "A5p2": "FRAGO 1217, CJTF-7, 14 DEC 2003  ·  CENTCOM FOIA", "A6p1": "FRAGO 1239, CJTF-7, 18 DEC 2003  ·  CENTCOM FOIA",
      "A7p1": "CENTCOM CAG INFORMATION PAPER, 16 DEC 2003  ·  CENTCOM FOIA", "A10p1": "DOD MEMO, “REWARD FOR SADDAM HUSSEIN AND SONS”, 20 MAR 2003",
      "R1": f"FIRDOS SQUARE, BAGHDAD, 9 APR 2003  ·  {DOD}", "R2": "BAGHDAD AND THE TIGRIS FROM SPACE, 2002  ·  NASA",
      "R3": "THE REPUBLICAN PALACE, BAGHDAD, c. 2003-05  ·  PD", "R4": f"OVER BAGHDAD, 2004  ·  {DOD}", "R5": f"US TANKS UNDER THE VICTORY ARCH, BAGHDAD, NOV 2003  ·  {DOD}",
      "R6": "THE TIGRIS IN BAGHDAD, 2010  ·  DVIDS", "R7": "A CONVOY IN BAGHDAD, 2005  ·  DVIDS", "R9": f"AN EMPTY PALACE, BAGHDAD, 17 APR 2003  ·  {DOD}",
      "R10": "PRESIDENT BUSH ADDRESSES THE NATION, 2003  ·  THE WHITE HOUSE / NARA", "R11": f"AL-FAW PALACE, BAGHDAD  ·  {DOD}",
      "R15": f"THE REPUBLICAN PALACE FROM THE AIR  ·  {DOD}", "R16": f"A PALACE DINING ROOM, BAGHDAD, 2003  ·  {DOD}"}
for _r in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "R12", "R13"): TB[_r] = ILL
def DT(rid):
    m = re.match(r"(A\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD, 2003")
'''
LIFT = {"E4": 0.7, "E10": 0.7, "E5": 0.8, "E6": 0.8}
CAPFIX = {"Odierno": "Odierno", "Oh-dee-air-no": "Odierno", "Odiyerno": "Odierno", "Musslit": "al-Musslit", "Muslit": "al-Musslit", "Dour": "ad-Dawr",
          "Adour": "ad-Dawr", "Addour": "ad-Dawr", "ad-dour": "ad-Dawr", "Tikreet": "Tikrit", "Uday,": "Uday", "Koo-say": "Qusay", "Qusai": "Qusay",
          "Sentcom": "CENTCOM", "Centcom": "CENTCOM", "Peero": "Piro", "Pirro": "Piro", "Firdaus": "Firdos", "Firdoss": "Firdos", "8.26": "8:26", "10.50": "10:50",
          "12.20": "12:20", "2.10": "2:10", "'clock": "o'clock", (23, "o"): "", (53, "o"): "", (79, "o"): "",
          (1, "erupts."): "Iraq.", (1, "Tikrit"): "Tikrit,", (5, "Fia"): "Firdos", (5, "Dus"): "", (17, "at"): "", (17, "Dao,"): "ad-Dawr,", (22, "855."): "8:55.",
          (49, "lion"): "line", (60, "Al"): "al", (60, "Arabihe"): "Arabiya", (74, "You'd"): "He'd", (43, "believe"): "believed"}
MUSIC = '''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(15), -17); music("Industrial Cinematic.mp3", tl(15), tl(25), -17)
    music("Man Down.mp3", tl(25), tl(35), -17); music("Thunder Dreams.mp3", tl(35), tl(45), -17); music("Industrial Cinematic.mp3", tl(45), tl(53), -17)
    music("Rising Tide.mp3", tl(53), tl(59), -17); music("Man Down.mp3", tl(59), tl(68), -18); music("Rising Tide.mp3", tl(68), tl(78), -17)
    music("Promises to Keep.mp3", tl(78), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("wind_deep_cinematic_hum", tl(19), tl(25), -31); loop("wind_ambience", tl(25), tl(30), -30)
    loop("wind_scary", tl(45), tl(49), -32)
'''
EV = [(0, "minutes", "hit_short_bass", -20), (0, "foam", "hit_cinematic_deep_impact", -18), (1, 0.0, "clock_tick_single", -20),
      (2, "hands", "hit_deep_heartbeat_impact", -16), (3, "saddam", "hit_big_cinematic_impact", -16), (5, "falls", "hit_cinematic_deep_impact", -18),
      (9, "million", "hit_short_bass", -18), (10, "killed", "sweep_terror_darkness", -24), (13, "name", "hit_horror_drum", -18),
      (15, 0.0, "clock_tick_single", -20), (18, "wolverine", "hit_short_bass", -18), (20, 0.0, "clock_tick_single", -20),
      (22, "eight|fifty", "bass_suspense_mystery", -24), (23, 0.0, "clock_tick_single", -20), (24, "initially", "hit_short_bass", -18),
      (27, "foam", "heartbeat_single", -16), (28, "hole", "hit_cinematic_deep_impact", -16), (29, 0.0, "clock_tick_single", -20),
      (29, "hands", "hit_big_cinematic_impact", -14), (30, "recording", "sweep_horror_long", -24), (35, "shot", "hit_short_bass", -18),
      (37, 0.0, "camera_classic_click", -24), (41, "helicopter", "whoosh_fast_transition", -22), (45, 0.0, "clock_tick_single", -20),
      (47, "water", "heartbeat_single", -16), (50, 0.0, "clock_tick_single", -20), (52, "absolutely", "metal_hammer_hit", -20),
      (53, 0.0, "clock_bells_hour", -24), (54, "got", "hit_big_cinematic_impact", -14), (54, "gentlemen", "reporters_camera_flashes", -26),
      (59, "wasn't", "hit_short_bass", -18), (60, "double", "bass_suspense_mystery", -24), (62, "believe", "hit_horror_drum", -18),
      (66, "never", "hit_short_bass", -18), (71, "grandchildren", "hit_cinematic_deep_impact", -16), (73, "fifty-nine|1959", "hit_big_cinematic_impact", -15),
      (77, "executed", "sweep_terror_darkness", -26), (78, 0.0, "hit_cinematic_deep_impact", -15),
      (ENDL, -0.55, "metal_hammer_hit", -16), (ENDL, -0.3, "hit_cinematic_deep_impact", -14)]
CH = [(0, "8:26 PM, a farm near Tikrit"), (5, "248 days on the run"), (11, "The driver"), (15, "10:50 AM: the tip"), (20, "In the dark"),
      (25, "Under the rug"), (30, "What did he say?"), (35, "The cash and the hole"), (41, "The night"), (45, "Would you like some water?"),
      (50, "We got him"), (59, "Some did not believe it"), (66, "The reward"), (68, "The FBI room"), (78, "What the record kept")]
