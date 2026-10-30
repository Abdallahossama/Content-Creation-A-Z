"""Build render_coleroe.py from render_alcatraz46.py (the File Keeper engine: animated stamp, case tab, spoken mid ask, CASE CLOSED end card),
file-16 blocks swapped in (docstring, paths, tags, crops, SHOTS, OV, CAPFIX, music/SFX, chapters, end-card line). The two NARA cards are
documents in COLOUR (the red "ESCAPED DECEMBER 16, 1937" stamp).   uv run --no-project python _build_render.py"""
SRC = "D:/why habibi/_newchannel/14_battle_of_alcatraz/render_alcatraz46.py"
DST = "D:/why habibi/_newchannel/16_cole_roe_1937/render_coleroe.py"
s = open(SRC, encoding="utf-8").read()
def swap(a, b, new):
    """replace s[index(a) : index(b)] (b exclusive) with new"""
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

swap('"""The Last Hours #14', "import sys, os", '''"""The Last Hours #16: the fog escape, Alcatraz, Thursday 16 December 1937 (counted at 1:00 p.m., gone at 1:30 p.m.): Theodore Cole and
Ralph Roe, the Model Industries Building, the outgoing tide, the search, the warden's change of mind, the FBI hunt 1937-1941, the 1941
"alive in South America" story, and the open file. The File Keeper, colour grade, 1920x1080, burned-in captions, film finish.
Real images only: NARA warden's notebook cards, NPS / GGNRA photos and drawings, HABS (Library of Congress), the FBI's 1932 aerial,
1937-1941 newspapers (Utah Digital Newspapers, NoC-US; Internet Archive), the U.S. Weather Bureau map; Pexels textures labelled ILLUSTRATIVE.
Never shown: bodies, drowning, any woman (newspaper pages cropped to the articles). Owner rules: research/research.md (do-not-say), assets.md section H.
  uv run --no-project --with pillow --with numpy --with soundfile python render_coleroe.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
''')
rep('ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"', 'ROOT = "D:/why habibi/_newchannel/16_cole_roe_1937/"')
rep('ROOT + "vo/alcatraz46_vo_chatterbox.wav"', 'ROOT + "vo/coleroe_vo_chatterbox.wav"')
rep('def isdoc(rid): return rid[0] == "A" and rid not in ("A7", "A8", "A9", "A10")      # A7-A10 are museum objects: graded like photos',
    'def isdoc(rid): return re.fullmatch(r"A\\d+(c|p\\d+)", rid) is not None             # newspaper crops and pages stay paper-toned; the cards and photos are graded\n'
    'COLORDOC = {"A1", "A2", "G19"}                                               # NARA cards shown as documents IN COLOUR (the red stamp)')
rep('''        im = Image.open(ORIG(rid)).convert("L"); s = min(1.0, 3200 / im.height)
        if s < 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        a = np.asarray(im, np.float32)''', '''        im = Image.open(ORIG(rid)).convert("RGB" if rid in COLORDOC else "L"); s = min(1.0, 3200 / im.height)
        if s < 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        if rid in COLORDOC: IMG[k] = (grade_im(im), s); return IMG[k]
        a = np.asarray(im, np.float32)''')
swap("CROP = {", "def KB(rid", r'''CROP = {"G2": (0.02, 0.02, 0.98, 0.94), "G12": (0.04, 0.03, 0.96, 0.93), "G13": (0.02, 0.03, 0.96, 0.97), "G14": (0.02, 0.02, 0.96, 0.97),
        "C3": (0.02, 0.02, 0.97, 0.97)}                                   # NPS prints and HABS: the white border, black edge and catalogue number
NPS = "NPS, GOLDEN GATE NRA"; HABS = "HABS, LIBRARY OF CONGRESS"; NARA = "NATIONAL ARCHIVES"
TB = {"A1": f"WARDEN'S NOTEBOOK: THEODORE COLE, AZ 258  ·  {NARA}", "A2": f"WARDEN'S NOTEBOOK: RALPH ROE, AZ 260  ·  {NARA}",
      "A3": f"THEODORE COLE, ALCATRAZ 258  ·  {NPS}", "A4p1": "SALT LAKE TELEGRAM, FRI 17 DEC 1937  ·  UTAH DIGITAL NEWSPAPERS",
      "A5p1": "SALT LAKE TELEGRAM, SAT 18 DEC 1937  ·  UTAH DIGITAL NEWSPAPERS", "A6p1": "SALT LAKE TELEGRAM, MON 20 DEC 1937  ·  UTAH DIGITAL NEWSPAPERS",
      "A7c": "PROVO EVENING HERALD, MON 20 DEC 1937  ·  UTAH DIGITAL NEWSPAPERS", "A8c": "OGDEN STANDARD-EXAMINER, FRI 17 DEC 1937  ·  UTAH DIGITAL NEWSPAPERS",
      "A9c": "SALT LAKE TRIBUNE, SAT 12 AUG 1939  ·  UTAH DIGITAL NEWSPAPERS", "A10c": "PROVO DAILY HERALD, FRI 18 AUG 1939  ·  UTAH DIGITAL NEWSPAPERS",
      "A11c": "PROVO DAILY HERALD, THU 4 APR 1940  ·  UTAH DIGITAL NEWSPAPERS", "A12c": "OGDEN STANDARD-EXAMINER, WED 30 APR 1941  ·  UTAH DIGITAL NEWSPAPERS",
      "A13c": "THE CIRCLEVILLE HERALD, FRI 17 DEC 1937  ·  INTERNET ARCHIVE", "A14c": "SANTA ANA REGISTER, SAT 18 DEC 1937  ·  INTERNET ARCHIVE",
      "A17p1": "U.S. WEATHER BUREAU, DAILY WEATHER MAP, 16 DEC 1937  ·  NOAA CENTRAL LIBRARY",
      "C1": f"THE NORTH END AND THE MODEL INDUSTRIES BUILDING, c. 1930  ·  NPS", "C2": f"THE 1933 WARNING SIGN, TODAY  ·  NPS",
      "C3": f"THE NORTH END OF THE ISLAND  ·  {HABS}", "C4": f"A PRISON SHOP, DRAWN BY AN INMATE, 1944  ·  {NPS}", "C5": f"THE MACHINE SHOP, DRAWN BY AN INMATE, 1944  ·  {NPS}",
      "D1": "FOG THROUGH THE GOLDEN GATE, TODAY  ·  ILLUSTRATIVE, PEXELS",
      "G1": "ALCATRAZ FROM THE AIR, BEFORE 1934  ·  FBI", "G2": f"THE DOCK FROM THE WATER, 1938  ·  {NPS}", "G3": f"ALCATRAZ AND ANGEL ISLAND  ·  {NPS}",
      "G4": f"THE EAST SIDE OF THE ISLAND  ·  {NPS}", "G5": f"ALCATRAZ FROM THE AIR, 1950  ·  {NPS}", "G6": f"PRISONERS GOING BACK TO THEIR CELLS  ·  {NPS}",
      "G7": f"THE CELL HOUSE  ·  {HABS}", "G8": "FRANK MORRIS, 1962  ·  FBI", "G9": f"ALCATRAZ OFFICERS WITH WARDEN JOHNSTON, 1930s  ·  {NPS}",
      "G10": f"WARDEN JOHNSTON (CENTRE) WITH THE PRESS, 1946  ·  {NPS}", "G11": f"JOSEPH CRETZER  ·  {NPS}", "G12": f"A TOWER GUARD'S RIFLES, c. 1940  ·  {NPS}",
      "G13": f"THE RECREATION YARD  ·  {HABS}", "G14": f"A GUARD TOWER  ·  {HABS}", "G18": "ALCATRAZ ISLAND  ·  NPS MAP",
      "G19": f"WARDEN'S NOTEBOOK: JOSEPH CRETZER  ·  {NARA}"}
ILL = "ILLUSTRATIVE  ·  PEXELS"
for _r in ("F1", "F2", "F3", "F4", "F5", "F6", "G15", "G16", "G17", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"): TB[_r] = ILL
TB["F5"] = "ANGEL ISLAND, THE NEAREST LAND TO THE NORTH  ·  ILLUSTRATIVE, PEXELS"; TB["G16"] = TB["G17"] = "ALCATRAZ TODAY  ·  ILLUSTRATIVE, PEXELS"
TB["V1"] = "ALCATRAZ IN FOG, TODAY  ·  ILLUSTRATIVE, PEXELS"; TB["V8"] = "THE GOLDEN GATE, TODAY  ·  ILLUSTRATIVE, PEXELS"; TB["G15"] = "THE GOLDEN GATE IN FOG, TODAY  ·  ILLUSTRATIVE, PEXELS"
def DT(rid): return TB.get(rid, "THE RECORD, 1937")
''')
rep('def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))',
    'def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid)))')
swap("CROPV = {", "def VID(rid", '''CROPV = {"D1": (0.12, 0.0, 0.62, 0.5)}                                   # D1: only the sky and the bridge tower (visitors stand on the hill below)
LIFT = {"V3": 0.8, "V4": 0.8}
''')
swap("SHOTS = [", "def OT(ln, off)", open("D:/why habibi/_newchannel/16_cole_roe_1937/shots_coleroe.py", encoding="utf-8").read())
rep('BP.LABEL["alcatraz46"]', 'BP.LABEL["coleroe"]', 2)
rep('BP.NEXT["alcatraz46"]', 'BP.NEXT["coleroe"]')
rep('sh = tone("F13")', 'sh = tone("G17")')
rep('wt(67, "like"), wt(67, "subscrib")', 'wt(ENDL, "like"), wt(ENDL, "subscrib")', 2)
swap("CAPFIX = {", "def capfix(i, w):", '''CAPFIX = {"Noah's": "NOAA's", "Noahs": "NOAA's", "Kretzer": "Cretzer", "Kretzer's": "Cretzer's", "Cretser": "Cretzer", "Kratzer": "Cretzer", "Johnson": "Johnston",
          "Leavenwerth": "Leavenworth", "Rowe": "Roe", "Row": "Roe", "Roe's": "Roe's", "Rowe's": "Roe's", "F.B.I.": "FBI", "F.B.I.'s": "FBI's", "PM": "p.m.", "PM,": "p.m.,",
          "1.30": "1:30", "4.52": "4:52", "1.00": "1:00", "Alcatraz,": "Alcatraz,", "Tulsa,": "Tulsa,"}  # whisper spellings -> the record's
''')
swap('    music("Thunder Dreams.mp3", 0.0, tl(5)', "    for i, (key, (kind, a)) in enumerate(SHOTS):", '''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Industrial Cinematic.mp3", tl(5), tl(18), -17); music("Man Down.mp3", tl(18), tl(29), -17)
    music("Rising Tide.mp3", tl(29), tl(42), -17); music("Thunder Dreams.mp3", tl(42), tl(53), -17); music("Industrial Cinematic.mp3", tl(53), tl(61), -17)
    music("Man Down.mp3", tl(61), tl(66), -18); music("Promises to Keep.mp3", tl(66), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("ambience_cinematic_suspense", tl(18), tl(24), -31); loop("waves_rough_sea_loop", tl(23), tl(36), -32)
    loop("wind_deep_cinematic_hum", tl(36), tl(42), -31)
''')
swap("    EV = [", "    for ln, off, name, db in EV:", '''    EV = [(0, "counted", "clock_tick_single", -18), (0, "fog", "whoosh_ghostly", -24), (0, "dead|alive", "hit_short_bass", -18),
          (2, "counted", "prison_metal_door_close", -26), (3, "gone", "hit_cinematic_deep_impact", -18), (6, "shot", "hit_horror_drum", -22),
          (10, "nailed", "metal_hammer_hit", -24), (12, "laundry", "papers_moving", -26), (16, "sawed|bars", "metal_tool_drop", -26),
          (18, "count", "keys_moving", -24), (19, "cut", "metal_hammer_hit", -22), (21, "gate|force", "gear_metallic_lock", -22),
          (21, "drop", "jump_in_water", -26), (23, "water", "jump_in_water", -20), (25, "draining", "waves_windy_sea_loop", -30),
          (29, "gone", "siren_vintage_manual", -24), (31, "radio", "radio_static_crackles", -26), (32, "foghorns|blaring", "ship_engine_loop", -28),
          (39, "front|pages", "newspaper_drop", -22), (41, "mystery|boat", "motorboat_sea", -26), (42, "changed|mind", "hit_short_bass", -16),
          (46, "fingerprints", "typewriter_typing_old", -26), (47, "tool", "metal_tool_falling", -24), (53, "shot", "hit_horror_drum", -18),
          (55, "swarm|highways", "siren_manual_fire_alert", -30), (57, "chronicle", "newspaper_drop", -22), (59, "postcard", "paper_slide", -22),
          (63, "stamped|red", "hit_big_cinematic_impact", -18), (64, "swam", "water_splash", -24), (66, 0.0, "hit_cinematic_deep_impact", -15),
          (ENDL, -0.55, "metal_hammer_hit", -16), (ENDL, -0.3, "hit_cinematic_deep_impact", -14)]
    EV = [e for e in EV if os.path.exists(SFXD + e[2] + ".mp3")]
''')
rep('name = name or "TheLastHours_14_BattleOfAlcatraz.mp4"', 'name = name or "TheLastHours_16_ColeRoe_FogEscape.mp4"')
swap("CH = [", 'if __name__ == "__main__":', '''CH = [(0, "Counted at one"), (5, "The same Rock"), (8, "Two Oklahoma files"), (14, "The shop at the tip"), (18, "1:00 p.m."),
      (24, "The tide turns"), (29, "1:30 p.m."), (36, "One in a thousand"), (42, "The warden changes his mind"), (49, "Number two, number three"),
      (53, "The cab in Tulsa"), (57, "Business was good"), (61, "The open file"), (66, "What the record shows")]

''')
rep("NEXT = os.environ.get(\"LH_NEXT\", \"\")", "NEXT = os.environ.get(\"LH_NEXT\", \"\")\nENDL = 69                                                # the File Keeper sign-off line (the end card runs under it)")
open(DST, "w", encoding="utf-8").write(s); print("wrote", DST, len(s.splitlines()), "lines")
