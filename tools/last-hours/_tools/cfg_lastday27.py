ROOT = "D:/why habibi/_newchannel/27_saddam_last_day/"
VO = "lastday_vo_chatterbox.wav"
ENDL = 85
SHOTS = ROOT + "shots_lastday.py"
DOCS = ()
ENDBG = "C8"
NAME = "TheLastHours_27_Saddam_LastDay.mp4"
DOC = '''"""The Last Hours #27: Saddam Hussein's last day, Baghdad, Friday 29 - Sunday 31 December 2006 (about 11:55 p.m. Maliki signs; 1:30 a.m.
fourteen phones ring; LZ Washington, the phones taken; Camp Cropper to Kadhimiya by Black Hawk; 5:30 a.m. Iraq takes full custody; the small
room; 6 a.m. the corridor, the Koran; about 6:10 a.m. the sentence carried out (one line, no images); two videos; the coffin north to Awja),
framed by the Dujail case (8 July 1982; Decree 778, 16 June 1984). The File Keeper, colour grade, 1920x1080, burned-in captions, film finish.
Real images only: DoD / US Army / White House (PD), CIA / NIMA / MND-B maps (PD), file 11's vetted Baghdad set, Pexels textures labelled
ILLUSTRATIVE. Never shown: the execution, the gallows, the rope, either video or stills from them, the body, any woman.
  uv run --no-project --with pillow --with numpy --with soundfile python render_lastday27.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
'''
TBLOCK = r'''CROP = {"C13": (0.0, 0.0, 1.0, 0.55), "C16": (0.0, 0.0, 0.7, 1.0)}             # C13: city + domes only, never the pilgrims on the bridge; C16: no pedestrians
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
'''
LIFT = {"E7": 0.8, "E14": 0.7, "E17": 0.9, "E8": 0.85}
CAPFIX = {"Dujayl": "Dujail", "Doojail": "Dujail", "Doo-jail": "Dujail", "Kadhimiyah": "Kadhimiya", "Khadimiya": "Kadhimiya", "Kazimiya": "Kadhimiya",
          "Faroun": "al-Faroon", "Farun": "al-Faroon", "Bander": "al-Bandar", "Bandar": "al-Bandar", "Maleki": "al-Maliki", "Talibani": "Talabani",
          "Moqtada": "Muqtada", "Mukhtada": "Muqtada", "Awjah": "Awja", "Owja": "Awja", "Ouja": "Awja", "Tikreet": "Tikrit", "Eid,": "Eid,",
          "1.30": "1:30", "3.30": "3:30", "5.30": "5:30", "6.10": "6:10", "Quran": "Koran", "keeper": "Keeper",
          (28, "Aridsina"): "At a dinner", (59, "knocked."): "not.", (29, "Noor"): "Nouri", (29, "Rai"): "", (46, "Munqif"): "Munqith",
          (46, "-Farooon,"): "-Faroon,", (69, "government."): "government's.", (42, "stepped"): "step", (28, "According"): "according"}
MUSIC = '''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(12), -17); music("Industrial Cinematic.mp3", tl(12), tl(22), -17)
    music("Man Down.mp3", tl(22), tl(30), -17); music("Thunder Dreams.mp3", tl(30), tl(36), -17); music("Industrial Cinematic.mp3", tl(36), tl(43), -17)
    music("Rising Tide.mp3", tl(43), tl(50), -18); music("Man Down.mp3", tl(50), tl(60), -18); music("Rising Tide.mp3", tl(68), tl(79), -17)
    music("Promises to Keep.mp3", tl(79), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("wind_deep_cinematic_hum", tl(30), tl(36), -31); loop("roomtone_dark_cinematic", tl(60), tl(68), -30)
    loop("wind_ambience", tl(74), tl(79), -31)
'''
EV = [(0, "rings", "clock_tick_single", -20), (0, "execution", "hit_cinematic_deep_impact", -18), (1, 0.0, "clock_tick_single", -20),
      (2, "saddam", "hit_big_cinematic_impact", -16), (6, "kill", "hit_short_bass", -18), (9, "death", "hit_horror_drum", -18),
      (10, "worse", "bass_suspense_mystery", -24), (11, "back", "hit_cinematic_deep_impact", -16), (16, "hanging", "hit_big_cinematic_impact", -16),
      (17, 0.0, "clock_tick_single", -20), (19, "four", "hit_short_bass", -16), (22, 0.0, "clock_tick_single", -20),
      (29, "midnight", "clock_bells_hour", -24), (29, "hanging", "hit_cinematic_deep_impact", -16), (30, 0.0, "clock_tick_single", -20),
      (33, "phones", "metal_tool_drop", -22), (35, "end", "hit_short_bass", -18), (38, "black", "whoosh_fast_transition", -22),
      (41, 0.0, "clock_tick_single", -20), (41, "custody", "hit_big_cinematic_impact", -16), (47, "shouts", "hit_short_bass", -18),
      (50, 0.0, "clock_tick_single", -20), (53, "koran", "heartbeat_single", -16), (56, "changed", "sweep_horror_long", -24),
      (58, "phones", "hit_horror_drum", -18), (65, 0.0, "clock_tick_single", -22), (68, 0.0, "hit_cinematic_deep_impact", -18),
      (73, "revenge", "hit_short_bass", -18), (75, "coffin", "sweep_terror_darkness", -26), (78, "sure", "hit_short_bass", -18),
      (79, 0.0, "hit_cinematic_deep_impact", -15), (85, -0.55, "metal_hammer_hit", -16), (85, -0.3, "hit_cinematic_deep_impact", -14)]
CH = [(0, "1:30 AM, Baghdad"), (5, "Dujail, 1982"), (12, "The court"), (17, "30 days. They took four"), (22, "Friday: who will do it?"),
      (30, "Fourteen phones"), (36, "Camp Cropper"), (43, "The small room"), (50, "The Koran"), (56, "Two phones raised"),
      (60, "6:10 AM"), (68, "Two videos"), (74, "The coffin goes north"), (79, "What the record keeps")]
