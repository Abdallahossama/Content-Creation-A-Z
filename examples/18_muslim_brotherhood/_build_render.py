"""Build render_mb18.py from render_alcatraz46.py (the File Keeper engine: animated stamp, case tab, spoken mid ask, CASE CLOSED end card),
file-18 blocks swapped in (docstring, paths, tags, crops, maps, SHOTS, OV, CAPFIX, music/SFX, chapters, end-card line).
  uv run --no-project python _build_render.py"""
SRC = "D:/why habibi/_newchannel/14_battle_of_alcatraz/render_alcatraz46.py"
DST = "D:/why habibi/_newchannel/18_muslim_brotherhood/render_mb18.py"
s = open(SRC, encoding="utf-8").read()
def swap(a, b, new):
    """replace s[index(a) : index(b)] (b exclusive) with new"""
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

swap('"""The Last Hours #14', "import sys, os", '''"""The Last Hours #18: Hassan al-Banna's last hours, Cairo, Saturday 12 February 1949 (about 8:30 p.m.: two men open fire as he gets into a
taxi outside the Young Men's Muslim Association; just after midnight he dies at Qasr al-Aini hospital), told as the story of who the Muslim
Brotherhood were: six workmen in a canal town (1928), hundreds of thousands of members and a secret wing (1940s), the 1948 killings, the trial
that traced the getaway car to the Interior Ministry (1954), and why the name is in a US Senate race (2026). The File Keeper, 1920x1080.
Real images only: PD-Egypt photographs, Library of Congress (Matson), Nationaal Archief (CC0), KITLV and Wellcome (CC BY 4.0), US government
(PD), Universal Newsreel (PD), 1948-49 US newspapers, Pexels textures labelled ILLUSTRATIVE. Never shown: the shooting, any body, any woman.
Owner rules: research/research.md (do-not-say list 11), research/assets.md.
  uv run --no-project --with pillow --with numpy --with soundfile python render_mb18.py times | qa [t..] | boxes | keys | seg i n | audio | final n | all n | chapters | prep"""
''')
rep('ROOT = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"', 'ROOT = "D:/why habibi/_newchannel/18_muslim_brotherhood/"')
rep('ROOT + "vo/alcatraz46_vo_chatterbox.wav"', 'ROOT + "vo/mb_vo_chatterbox.wav"')
rep('def isdoc(rid): return rid[0] == "A" and rid not in ("A7", "A8", "A9", "A10")      # A7-A10 are museum objects: graded like photos',
    'def isdoc(rid): return re.fullmatch(r"N\\d+[ab]?|A9", rid) is not None                    # the newspaper pages and the 1947 clipping stay paper-toned')
rep('# (no Natural-Earth map in this file: the bay is shown on the real USGS sheet and the NPS plan)', '''# Natural-Earth maps (mshorts VMap): (lon centre, lat centre, degrees wide)
V_EGYPT, V_REGION, V_MIDEAST = (31.4, 30.6, 4.4), (33.2, 30.9, 8.0), (34.0, 31.6, 13.0)''')

swap("CROP = {", "def KB(rid", r'''CROP = {"A21": (0.0, 0.12, 0.64, 0.95), "A5": (0.0, 0.17, 1.0, 1.0), "A24": (0.0, 0.0, 1.0, 0.86), "A13": (0.05, 0.08, 0.95, 0.92), "A15": (0.07, 0.04, 0.95, 0.96),
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
''')
rep('def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop, h=h, rot=rot, tag=tag or (DT(rid) if rid[0] == "A" else TB.get(rid))))',
    'def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid)))')
swap("CROPV = {", "def VID(rid", '''CROPV = {}
LIFT = {"T3": 0.4, "T4": 0.45, "T5": 0.55}                     # gamma: below 1 lifts the night clips (QA 31 Oct: they read as black)                     # gamma: below 1 lifts the dark clips (LESSONS 34)
''')
swap("SHOTS = [", "def OT(ln, off)", open("D:/why habibi/_newchannel/18_muslim_brotherhood/shots_mb18.py", encoding="utf-8").read())
rep('BP.LABEL["alcatraz46"]', 'BP.LABEL["mb18"]', 2)
rep('BP.NEXT["alcatraz46"]', 'BP.NEXT["mb18"]')
rep('sh = tone("F13")', 'sh = tone("A21")')
rep('wt(67, "like"), wt(67, "subscrib")', 'wt(ENDL, "like"), wt(ENDL, "subscrib")', 2)
swap("CAPFIX = {", "def capfix(i, w):", '''CAPFIX = {"Bana": "Banna", "Banner": "Banna", "Ismailiya": "Ismailia", "Nokrashi": "Nuqrashi", "Nukrashi": "Nuqrashi", "Nookrahshee": "Nuqrashi",
          "Kasr": "Qasr", "Ainy": "Aini", "Mageed": "Magid", "Majid": "Magid", "Kareem": "Karim", "Mansoor": "Mansour", "Ebeyd": "Ebeid", "Obeid": "Ebeid",
          "Kutb": "Qutb", "Qotb": "Qutb", "Nazlee": "Nazli", "Nazly": "Nazli", "Mahmudiya": "Mahmudiyya", "Mahmoudiya": "Mahmudiyya", "El-Syed": "El-Sayed",
          "El-Said": "El-Sayed", "Elsayed": "El-Sayed", "Politifact": "PolitiFact", "piasters": "piastres", (29, "Anna"): "Banna", (4, "gunman"): "gunmen", "5pm": "5 p.m.", (9, "Ismaili"): "Ismailia", (9, "Liya"): "", "Kutb": "Qutb", "8.30": "8:30", "8.45": "8:45", "7.45": "7:45", "5.40": "5:40"}  # whisper spellings -> the record's
''')
swap('    music("Thunder Dreams.mp3", 0.0, tl(5)', "    for i, (key, (kind, a)) in enumerate(SHOTS):", '''    music("Thunder Dreams.mp3", 0.0, tl(5), -11, later=(tl(4), -15)); music("Rising Tide.mp3", tl(5), tl(16), -17); music("Industrial Cinematic.mp3", tl(16), tl(29), -17)
    music("Man Down.mp3", tl(29), tl(38), -17); music("Thunder Dreams.mp3", tl(39), tl(49), -17); music("Rising Tide.mp3", tl(49), tl(54), -17)
    music("Man Down.mp3", tl(54), tl(58), -18); music("Industrial Cinematic.mp3", tl(58), tl(66), -18); music("Promises to Keep.mp3", tl(66), DUR, -16)
    loop("roomtone_dark_cinematic", 0.0, tl(5), -30); loop("wind_deep_cinematic_hum", tl(29), tl(38), -31); loop("roomtone_dark_cinematic", tl(39), tl(49), -31)
''')
swap("    EV = [", "    for ln, off, name, db in EV:", '''    EV = [(0, "night", "sweep_horror_long", -24), (0, "shot", "hit_short_bass", -18), (0, "how", "hit_cinematic_deep_impact", -18),
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
''')
rep('name = name or "TheLastHours_14_BattleOfAlcatraz.mp4"', 'name = name or "TheLastHours_18_MuslimBrotherhood_Banna.mp4"')
swap("CH = [", 'if __name__ == "__main__":', '''CH = [(0, "8:30 PM, Cairo"), (5, "A teacher in a canal town"), (16, "Hundreds of thousands, and a secret wing"), (29, "The last hours"),
      (39, "Car 9979"), (49, "The trial"), (54, "After the file"), (58, "Why this name is in the news"), (66, "What the record shows")]

''')
rep("NEXT = os.environ.get(\"LH_NEXT\", \"\")", "NEXT = os.environ.get(\"LH_NEXT\", \"\")\nENDL = 70                                                # the File Keeper sign-off line (the end card runs under it)")
open(DST, "w", encoding="utf-8").write(s); print("wrote", DST, len(s.splitlines()), "lines")
