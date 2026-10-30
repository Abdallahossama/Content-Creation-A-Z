"""Build render_indy.py from render_alcatraz46.py (the File Keeper engine: animated stamp, case tab, spoken mid ask, CASE CLOSED end card),
file-15 blocks swapped in (docstring, paths, tags, crops, SHOTS, OV, CAPFIX, music/SFX, chapters, end-card line).
  uv run --no-project python _build_render.py"""
SRC = "D:/why habibi/_newchannel/14_battle_of_alcatraz/render_alcatraz46.py"
DST = "D:/why habibi/_newchannel/15_uss_indianapolis/render_indy.py"
s = open(SRC, encoding="utf-8").read()
def swap(a, b, new):
    """replace s[index(a) : index(b)] (b exclusive) with new"""
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

swap('"""The Last Hours #14', "import sys, os", '''"""The Last Hours #15: USS Indianapolis, Monday 30 July 1945 (about 12:05 a.m. ship's time: two torpedoes from I-58; sunk in about
twelve minutes), the four days nobody reported her missing, the broken antenna that found the survivors (Thursday 2 August), the rescue,
the court-martial of Captain McVay and the long fight to clear his name. The File Keeper, colour grade, 1920x1080, burned-in captions, film finish.
Real images only: U.S. Navy / NHHC and National Archives photos and documents (court of inquiry, McVay's action report, routing orders,
ULTRA extracts, dispatches, deck logs), the Navy's 1945 rescue film (safe seconds only), Pexels sea textures labelled ILLUSTRATIVE.
Never shown: bodies, wounds, burns, sharks, any woman. Owner rules: research/research.md (do-not-say), assets.md section X.
  uv run --no-project --with pillow --with numpy --with soundfile python render_indy.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
''')
rep('ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"', 'ROOT = "D:/why habibi/_newchannel/15_uss_indianapolis/"')
rep('ROOT + "vo/alcatraz46_vo_chatterbox.wav"', 'ROOT + "vo/indy_vo_chatterbox.wav"')
rep('def isdoc(rid): return rid[0] == "A" and rid not in ("A7", "A8", "A9", "A10")      # A7-A10 are museum objects: graded like photos',
    'def isdoc(rid): return re.fullmatch(r"A\\d+p\\d+|A9|A10|A11|A35", rid) is not None    # pages, charts and the war diary stay paper-toned; A13-A33 are photos')
rep('# (no Natural-Earth map in this file: the bay is shown on the real USGS sheet and the NPS plan)', '''# Natural-Earth maps (mshorts VMap): (lon centre, lat centre, degrees wide)
V_PHIL, V_SINK, V_RESC = (135.0, 11.5, 26.0), (134.5, 12.2, 5.5), (133.9, 11.8, 3.4)
GUAM, LEYTE, TINIAN, PELELIU, SAMAR = (144.66, 13.45), (125.33, 10.9), (145.63, 15.0), (134.24, 7.0), (125.72, 11.05)
SINK, I58, GWINN, G150, DOYLE, MCVAY = (134.8, 12.03), (134.27, 12.52), (133.5, 11.5), (133.78, 11.9), (133.58, 11.75), (133.35, 11.58)
ROUTE = [GUAM, (144.0, 13.08), (143.0, 13.23), (138.0, 12.5), (132.5, 11.73), (128.08, 11.1), (126.0, 10.62), (125.67, 10.69), LEYTE]   # Route Peddie (routing instructions, 28 Jul 1945)
TO_SINK = [GUAM, (144.0, 13.08), (143.0, 13.23), (138.0, 12.5), SINK]''')

swap("CROP = {", "def KB(rid", r'''CROP = {"A16": (0.06, 0.0, 0.94, 1.0), "A25": (0.495, 0.245, 0.77, 0.69), "A28": (0.27, 0.18, 0.97, 0.80), "A23": (0.0, 0.0, 1.0, 0.92),
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
''')
rep('def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))',
    'def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid)))')
swap("CROPV = {", "def VID(rid", '''CROPV = {"A34a": (0.03, 0.03, 0.97, 0.97), "A34b": (0.03, 0.03, 0.97, 0.97)}
LIFT = {"A34a": 1.25, "A34b": 1.2, "F4": 0.8}
''')
swap("SHOTS = [", "def OT(ln, off)", open("D:/why habibi/_newchannel/15_uss_indianapolis/shots_indy.py", encoding="utf-8").read())
rep('BP.LABEL["alcatraz46"]', 'BP.LABEL["indy"]', 2)
rep('BP.NEXT["alcatraz46"]', 'BP.NEXT["indy"]')
rep('sh = tone("F13")', 'sh = tone("A13")')
rep('wt(67, "like"), wt(67, "subscrib")', 'wt(ENDL, "like"), wt(ENDL, "subscrib")', 2)
swap("CAPFIX = {", "def capfix(i, w):", '''CAPFIX = {"Lighty": "Leyte", "Leighty": "Leyte", "Laity": "Leyte", "Layte": "Leyte", "Pelelu": "Peleliu", "Pelilu": "Peleliu", "Pellalu": "Peleliu", "Peleleu": "Peleliu",
          "McVeigh": "McVay", "McVey": "McVay", "Mcvay": "McVay", "Gwyn": "Gwinn", "Gwen": "Gwinn", "Gwin": "Gwinn", "Hashimodo": "Hashimoto", "Tinnian": "Tinian",
          "Farallone": "Farallon", "Faralon": "Farallon", "Haynes'": "Haynes", "Hayes": "Haynes", "Doil": "Doyle", "SOS": "S.O.S.", "S.O.S": "S.O.S.", "LST": "LST-779",
          "I58": "I-58", "I-58.": "I-58.", "11.18": "11:18", "11.25": "11:25", "10.42": "10:42", "5.05": "5:05", "10.30": "10:30", "11.30": "11:30", "9.10": "9:10"}  # whisper spellings -> the record's
''')
swap('    music("Thunder Dreams.mp3", 0.0, tl(5)', "    for i, (key, (kind, a)) in enumerate(SHOTS):", '''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(17), -17); music("Industrial Cinematic.mp3", tl(17), tl(24), -17)
    music("Man Down.mp3", tl(24), tl(33), -17); music("Thunder Dreams.mp3", tl(33), tl(47), -17); music("Rising Tide.mp3", tl(47), tl(56), -17)
    music("Industrial Cinematic.mp3", tl(56), tl(71), -17); music("Man Down.mp3", tl(71), tl(82), -18); music("Promises to Keep.mp3", tl(82), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("waves_rough_sea_loop", tl(24), tl(33), -31); loop("waves_rough_sea_loop", tl(40), tl(52), -33)
    loop("wind_deep_cinematic_hum", tl(17), tl(24), -31); loop("waves_rough_sea_loop", tl(62), tl(70), -34)
''')
swap("    EV = [", "    for ln, off, name, db in EV:", '''    EV = [(0, "planes|eight", "sweep_horror_long", -24), (0, "dying", "heartbeat_single", -18), (0, "missing", "hit_short_bass", -18),
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
''')
rep('name = name or "TheLastHours_14_BattleOfAlcatraz.mp4"', 'name = name or "TheLastHours_15_USS_Indianapolis.mp4"')
swap("CH = [", 'if __name__ == "__main__":', '''CH = [(0, "Nobody came"), (5, "The cargo"), (11, "Zigzag at discretion"), (17, "Under the moon"), (24, "Twelve minutes"),
      (33, "Nobody missed her"), (40, "Four days"), (47, "The sharks: myth vs record"), (52, "The antenna"), (62, "Three bounces"),
      (71, "316"), (74, "The witness"), (82, "The long fight"), (87, "What the record shows")]

''')
rep("NEXT = os.environ.get(\"LH_NEXT\", \"\")", "NEXT = os.environ.get(\"LH_NEXT\", \"\")\nENDL = 90                                                # the File Keeper sign-off line (the end card runs under it)")
open(DST, "w", encoding="utf-8").write(s); print("wrote", DST, len(s.splitlines()), "lines")
