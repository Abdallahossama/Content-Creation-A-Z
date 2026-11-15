"""Build render_gaddafi17.py from render_alcatraz46.py (the File Keeper engine: animated stamp, case tab, spoken mid ask, CASE CLOSED end card),
file-17 blocks swapped in (docstring, paths, tags, crops, maps, SHOTS, OV, CAPFIX, music/SFX, chapters, end-card line).
  uv run --no-project python _build_render.py"""
SRC = "D:/why habibi/_newchannel/14_battle_of_alcatraz/render_alcatraz46.py"
DST = "D:/why habibi/_newchannel/17_gaddafi_last_day/render_gaddafi17.py"
s = open(SRC, encoding="utf-8").read()
def swap(a, b, new):
    """replace s[index(a) : index(b)] (b exclusive) with new"""
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

swap('"""The Last Hours #14', "import sys, os", '''"""The Last Hours #17: Gaddafi's last day, Sirte, Libya, Thursday 20 October 2011 (about 8:00 a.m. the convoy leaves late, in daylight;
about 8:30 a.m. NATO aircraft strike it; the drainage pipes; about 11 a.m. taken alive by Misrata fighters; dead by the time the ambulance
reaches Misrata), framed by the crown he claimed ("king of kings", 2008; one African army "to confront NATO", 2010). The File Keeper,
colour grade, 1920x1080, burned-in captions, film finish. Real images only: US Navy / USAF / DVIDS / White House / VOA / NASA (PD),
European Commission AV (CC BY 4.0) and Al Jazeera Creative Commons (CC BY 3.0) footage of Gaddafi and the 2011 war (men-only seconds),
Pexels textures labelled ILLUSTRATIVE. Never shown: the capture, any body, wound or morgue image, any woman (incl. his female guards).
Owner rules: research/research.md (content flags), research/assets.md (men-only windows).
  uv run --no-project --with pillow --with numpy --with soundfile python render_gaddafi17.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
''')
rep('ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"', 'ROOT = "D:/why habibi/_newchannel/17_gaddafi_last_day/"')
rep('ROOT + "vo/alcatraz46_vo_chatterbox.wav"', 'ROOT + "vo/gaddafi_vo_chatterbox.wav"')
rep('def isdoc(rid): return rid[0] == "A" and rid not in ("A7", "A8", "A9", "A10")      # A7-A10 are museum objects: graded like photos',
    'def isdoc(rid): return re.fullmatch(r"A90p\\d+", rid) is not None                     # only the UN verbatim pages stay paper-toned')
rep('# (no Natural-Earth map in this file: the bay is shown on the real USGS sheet and the NPS plan)', '''# Natural-Earth maps (mshorts VMap): (lon centre, lat centre, degrees wide)
V_GULF, V_SIRTE, V_AFRICA = (16.8, 31.9, 8.5), (16.55, 31.2, 0.45), (17.0, 3.0, 78.0)''')

swap("CROP = {", "def KB(rid", r'''CROP = {}
USN, VOA, NASA, ILL = "U.S. NAVY", "VOICE OF AMERICA", "NASA", "ILLUSTRATIVE  ·  PEXELS"
EC04, EC00, EU10 = "© EUROPEAN COMMUNITIES, 2004, CC BY 4.0", "© EUROPEAN COMMUNITIES, 2000, CC BY 4.0", "© EUROPEAN UNION, 2010, CC BY 4.0"
LIKE = "AN MQ-1 LIKE THE ONE REPORTED, NOT THE ACTUAL DRONE  ·  U.S. AIR FORCE"
TB = {"B1": f"MUAMMAR GADDAFI, AU SUMMIT, ADDIS ABABA, FEB 2009  ·  {USN}", "B2": f"GADDAFI, AU SUMMIT, ADDIS ABABA, FEB 2009  ·  {USN}",
      "B3": f"CHAIRMAN OF THE AFRICAN UNION, ADDIS ABABA, FEB 2009  ·  {USN}", "B4": f"TANZANIA'S KIKWETE EMBRACES GADDAFI, AU SUMMIT, FEB 2009  ·  {USN}",
      "B5": "GADDAFI IN BRUSSELS, 2004  ·  © EUROPEAN COMMUNITIES, CC BY 4.0", "B6": "GADDAFI IN TRIPOLI, NOV 2010  ·  HAMZA TURKIA, © EUROPEAN UNION, CC BY 4.0",
      "B7": "GADDAFI IN TRIPOLI, 2008  ·  KREMLIN.RU, CC BY 4.0", "B13": "GADDAFI IN ABUJA, 2006  ·  RICARDO STUCKERT/PR, AGÊNCIA BRASIL, CC BY 3.0 BR",
      "C14": "INSIDE BAB AL-AZIZIYA, TRIPOLI, AUG 2011  ·  “FREE LIBYAN”, CC BY 3.0", "C15": "BAB AL-AZIZIYA, TRIPOLI, AUG 2011  ·  “FREE LIBYAN”, CC BY 3.0",
      "C16": "GRAFFITI AT BAB AL-AZIZIYA, 29 AUG 2011  ·  PANORAMIO, CC BY 3.0", "C17": "REBELS AT THE GATE OF BAB AL-AZIZIYA, AUG 2011  ·  MAGHAREBIA, CC BY 2.0",
      "C18": "THE “FIST” SCULPTURE, TAKEN TO MISRATA, NOV 2011  ·  U.S. STATE DEPARTMENT", "C19": "GREEN SQUARE, TRIPOLI, 2006  ·  JAW101IE, PD",
      "C24": "TRIPOLI, NOV 2011  ·  BEN SUTHERLAND, CC BY 2.0",
      "A8": LIKE, "A10": LIKE, "V2b": LIKE, "V3b": LIKE,
      "A19": f"FIGHTERS NEAR BANI WALID, SEP 2011  ·  {VOA}", "A20": f"AMBULANCES ON THE BANI WALID ROAD, SEP 2011  ·  {VOA}",
      "A21": f"SHELL CASINGS ON A LIBYAN ROAD, SEP 2011  ·  {VOA}", "A4": f"USS BARRY FIRES TOMAHAWKS AT LIBYA, 19 MAR 2011  ·  {USN}", "A6": f"A TOMAHAWK LAUNCH, 19 MAR 2011  ·  {USN}",                # A17-A22: the files hold other VOA frames than assets.md says: tag by what is SEEN
      "A23": "SIRTE, AFTER THE BATTLE  ·  MEHDI KHOSHNEJAD / PEXELS", "A24": "THE GULF OF SIDRA, THURSDAY 20 OCT 2011  ·  NASA WORLDVIEW, MODIS TERRA",
      "A25": f"THE GULF OF SIRTE FROM THE SPACE STATION, MAR 2011  ·  {NASA}", "A26": f"THE GULF OF SIRTE FROM THE SPACE STATION, MAR 2011  ·  {NASA}",
      "A38": "THE AFRICAN UNION FLAG OF HIS CHAIRMANSHIP, 2009", "A90p15": "UN GENERAL ASSEMBLY, VERBATIM RECORD, 23 SEP 2009  ·  UNITED NATIONS",
      "A30": "USS STOUT FIRES TOMAHAWKS AT LIBYA, MAR 2011  ·  DVIDS, PD", "A31": "USS STOUT FIRES TOMAHAWKS AT LIBYA, MAR 2011  ·  DVIDS, PD",
      "A54": "ILLUSTRATIVE, NOT THE ACTUAL PIPES  ·  PEXELS", "D5": "PRESIDENT OBAMA, ROSE GARDEN, 20 OCT 2011  ·  THE WHITE HOUSE",
      "V9e": f"GADDAFI, CAIRO, APRIL 2000  ·  {EC00}", "V10a": f"TRIPOLI, NOV 2010, HIS LAST SUMMIT  ·  {EU10}",
      "V11a": "REBEL CONVOY ON THE COAST ROAD, MARCH 2011  ·  AL JAZEERA, CC BY 3.0", "V12a": "REBEL FIGHTERS, RAS LANUF, MARCH 2011  ·  AL JAZEERA, CC BY 3.0"}
for _r in ("A47", "A48", "A49", "A50", "A51", "A52", "A53", "E11", "E16"): TB[_r] = ILL
def DT(rid):
    m = re.match(r"(A\d+)", rid); return TB.get(rid) or TB.get(m.group(1) if m else rid, "THE RECORD, 2011")
''')
rep('def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))',
    'def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid)))')
swap("CROPV = {", "def VID(rid", '''CROPV = {}
LIFT = {"E11": 0.6, "E16": 0.8}                     # gamma: below 1 lifts the dark clips (LESSONS 34)
''')
swap("SHOTS = [", "def OT(ln, off)", open("D:/why habibi/_newchannel/17_gaddafi_last_day/shots_gaddafi.py", encoding="utf-8").read())
rep('BP.LABEL["alcatraz46"]', 'BP.LABEL["gaddafi17"]', 2)
rep('BP.NEXT["alcatraz46"]', 'BP.NEXT["gaddafi17"]')
rep('sh = tone("F13")', 'sh = tone("A24")')
rep('wt(67, "like"), wt(67, "subscrib")', 'wt(ENDL, "like"), wt(ENDL, "subscrib")', 2)
swap("CAPFIX = {", "def capfix(i, w):", '''CAPFIX = {"Qaddafi": "Gaddafi", "Gadhafi": "Gaddafi", "Kadafi": "Gaddafi", "Sirt": "Sirte", "Sert": "Sirte", "Surt": "Sirte",
          "Sirt,": "Sirte,", "Sirt.": "Sirte.", "Mutasim": "Mutassim", "Mutassem": "Mutassim", "Moutassim": "Mutassim", "Dow": "Dhao", "Dow,": "Dhao,", "Dhow": "Dhao",
          "Mansoor": "Mansour", "Misurata": "Misrata", "Misratah": "Misrata", "defence": "defense", (24, "Now"): "Now,", (24, "The"): "the", (24, "Crown"): "crown", "2.07": "2:07", "8.30": "8:30", "3.30": "3:30"}  # whisper spellings -> the record's
''')
swap('    music("Thunder Dreams.mp3", 0.0, tl(5)', "    for i, (key, (kind, a)) in enumerate(SHOTS):", '''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(11), -17); music("Industrial Cinematic.mp3", tl(11), tl(15), -17)
    music("Man Down.mp3", tl(15), tl(24), -17); music("Thunder Dreams.mp3", tl(24), tl(29), -17); music("Industrial Cinematic.mp3", tl(29), tl(36), -17)
    music("Man Down.mp3", tl(36), tl(43), -18); music("Rising Tide.mp3", tl(43), tl(51), -17); music("Man Down.mp3", tl(51), tl(56), -18)
    music("Promises to Keep.mp3", tl(56), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("wind_deep_cinematic_hum", tl(11), tl(15), -31); loop("wind_ambience", tl(29), tl(36), -30)
    loop("wind_scary", tl(51), tl(53), -32)
''')
swap("    EV = [", "    for ln, off, name, db in EV:", '''    EV = [(0, "kings", "sweep_horror_long", -24), (0, "nato", "hit_short_bass", -20), (0, "morning", "hit_cinematic_deep_impact", -18),
          (1, 0.0, "clock_tick_single", -20), (2, "convoy", "whoosh_metal_hit", -22), (3, "dead", "hit_deep_heartbeat_impact", -18),
          (5, "fell", "hit_cinematic_deep_impact", -20), (8, "district", "bass_suspense_mystery", -24), (9, "killed", "hit_short_bass", -18),
          (11, 0.0, "clock_ticking_closeup", -26), (13, 0.0, "clock_tick_single", -20), (15, 0.0, "clock_tick_single", -20),
          (15, "strike", "hit_big_cinematic_impact", -16), (16, "missile", "whoosh_fast_transition", -20), (16, "airbags", "hit_cinematic_deep_impact", -16),
          (17, "predator", "bass_suspense_mystery", -24), (21, "second", "hit_big_cinematic_impact", -18), (23, "never", "hit_short_bass", -18),
          (24, "crown", "riser_cinematic_trailer", -24), (25, "kings", "hit_horror_drum", -20), (27, "million", "hit_cinematic_deep_impact", -18),
          (28, "stopped", "hit_big_cinematic_impact", -16), (30, "helmet", "metal_tool_drop", -22), (32, "fire", "hit_short_bass", -18),
          (33, "grenade", "metal_hammer_hit", -20), (33, "feet", "heartbeat_single", -16), (35, "blast", "hit_big_cinematic_impact", -14),
          (37, 0.0, "clock_tick_single", -20), (37, "alive", "hit_horror_drum", -18), (42, "dead", "hit_deep_heartbeat_impact", -16),
          (43, "killed", "sweep_terror_darkness", -24), (45, "alive", "hit_cinematic_deep_impact", -16), (46, "never", "hit_short_bass", -18),
          (47, "killed", "reporters_camera_flashes", -26), (49, "garden", "camera_classic_click", -24), (52, "buried", "wind_scary", -26),
          (53, 0.0, "clock_bells_hour", -24), (55, "trial", "hit_horror_drum", -18), (56, 0.0, "hit_cinematic_deep_impact", -15),
          (ENDL, -0.55, "metal_hammer_hit", -16), (ENDL, -0.3, "hit_cinematic_deep_impact", -14)]
    EV = [e for e in EV if os.path.exists(SFXD + e[2] + ".mp3")]
''')
rep('name = name or "TheLastHours_14_BattleOfAlcatraz.mp4"', 'name = name or "TheLastHours_17_Gaddafi_LastDay.mp4"')
swap("CH = [", 'if __name__ == "__main__":', '''CH = [(0, "One morning in Sirte"), (5, "The last hideout"), (11, "The convoy leaves late"), (15, "8:30 AM: the strike"),
      (20, "He never came back"), (24, "The king of kings"), (29, "The drainage pipes"), (36, "Taken alive"), (43, "Who killed him?"),
      (47, "That afternoon"), (51, "The secret grave"), (56, "What the record shows")]

''')
rep("NEXT = os.environ.get(\"LH_NEXT\", \"\")", "NEXT = os.environ.get(\"LH_NEXT\", \"\")\nENDL = 60                                                # the File Keeper sign-off line (the end card runs under it)")
exec(open("D:/why habibi/_newchannel/17_gaddafi_last_day/build/post_patch.py", encoding="utf-8").read())   # owner 31 Oct: print cards, no text on faces
open(DST, "w", encoding="utf-8").write(s); print("wrote", DST, len(s.splitlines()), "lines")
