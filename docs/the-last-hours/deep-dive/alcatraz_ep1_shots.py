"""Deep Dive into Alcatraz, Episode 1: The Plan. Shots keyed to VO line numbers (vo/vo_tts.txt without '##').
Images: File 01's vetted set (FBI / NPS / Wikimedia PD, Pexels proxies)."""
M = "D:/why habibi/_newchannel/01_alcatraz/media/"
NAME = "DeepDive_Alcatraz_Ep1.mp4"
CAP_Y = 1560
TAIL = 2.4
SHOTS = [
 dict(line=0, img="C4_fbi_vent.jpg", label="REAL PHOTO", label2="FBI, JUNE 1962", z0=1.0, z1=1.12, flash=False),
 dict(line=1, img="E3_nps_tools.jpg", label="THE TOOLS", label2="NPS / GOLDEN GATE NRA", z0=1.0, z1=1.1),
 dict(line=2, kind="title", img="C2_nps_utility_corridor.jpg", lines=["A DEEP DIVE", "INTO ALCATRAZ", "EPISODE 1"], colour=False),
 dict(line=3, img="F3_nps_aerial_1950a.jpg", label="ALCATRAZ", label2="SAN FRANCISCO BAY, c. 1950", z0=1.0, z1=1.15),
 dict(line=4, img="F11_nps_broadway_1963.jpg", full=True, z0=1.05, z1=1.15, cy=0.45),
 dict(line=5, img="mug_frank_morris.jpg", label="FRANK MORRIS", w=760, ar=0.78, z0=1.0, z1=1.06, cy=0.4),
 dict(line=6, kind="pair", imgs=[("mug_john_anglin.jpg", "JOHN ANGLIN"), ("mug_clarence_anglin.jpg", "CLARENCE ANGLIN")]),
 dict(line=7, img="F12_nps_prisoners_cells.jpg", full=True, z0=1.05, z1=1.14),
 dict(line=8, img="cell_vent.jpg", label="THE VENT", z0=1.0, z1=1.12),
 dict(line=9, img="C2_nps_utility_corridor.jpg", label="THE UTILITY CORRIDOR", lsize=48, colour=True, z0=1.0, z1=1.1),
 dict(line=10, kind="hour", big="DEC 1961", sub="THE SAW BLADES"),
 dict(line=11, img="E3_nps_tools.jpg", label="SHARPENED SPOONS", z0=1.25, z1=1.45, cx=0.55, cy=0.55),
 dict(line=12, img="D2_fbi_workshop.jpg", label="REAL PHOTO", label2="WHAT THE FBI FOUND, 1962", z0=1.0, z1=1.1),
 dict(line=13, img="false_grid.jpg", label="THE FAKE GRILLE", colour=True, z0=1.0, z1=1.08),
 dict(line=14, vid="video/proxy/H8.mp4", full=True, z0=1.1, z1=1.15),
 dict(line=15, img="D3_fbi_catwalk.jpg", label="30 FEET UP", z0=1.0, z1=1.12),
 dict(line=16, img="D2_fbi_workshop.jpg", label="THE WORKSHOP", z0=1.15, z1=1.3, cx=0.4),
 dict(line=17, kind="hour", big="PERISCOPE", sub="MADE OF CARDBOARD"),
 dict(line=18, img="E2_fbi_life_vest.jpg", label="REAL PHOTO", label2="A LIFE VEST, RAINCOAT RUBBER", z0=1.0, z1=1.1),
 dict(line=19, img="E2_fbi_life_vest.jpg", label="50+ RAINCOATS", z0=1.25, z1=1.4, cx=0.45),
 dict(line=20, kind="hour", big="POPULAR", sub="MECHANICS"),
 dict(line=21, img="E1_fbi_paddle.jpg", label="THE PADDLE", label2="FOUND OFF ANGEL ISLAND", z0=1.0, z1=1.12),
 dict(line=22, img="D4_fbi_roof_vent.jpg", label="THE ROOF VENT", z0=1.0, z1=1.1),
 dict(line=23, img="F10_nps_locking_doors_1960.jpg", label="THE COUNT", colour=True, z0=1.0, z1=1.1),
 dict(line=24, img="B4_fbi_fake_heads.jpg", label="REAL PHOTO", z0=1.0, z1=1.12),
 dict(line=25, img="B3_fbi_dummy_head.jpg", label="SOAP AND TOILET PAPER?", lsize=48, z0=1.0, z1=1.1),
 dict(line=26, img="B5_nps_dummy_morris.jpg", label="CEMENT. REAL HAIR.", colour=True, z0=1.0, z1=1.15),
 dict(line=27, kind="hour", big="9:30 PM", sub="JUNE 11, 1962"),
 dict(line=28, img="B2_fbi_dummy_in_bed.jpg", label="REAL PHOTO", label2="CELL 150, THE NEXT MORNING", z0=1.0, z1=1.12),
 dict(line=29, img="D7_nps_bakery.jpg", label="THE BAKERY STACK", z0=1.0, z1=1.1),
 dict(line=30, vid="video/proxy/H18.mp4", full=True, z0=1.0, z1=1.05),
 dict(line=31, kind="hour", big="7:20 AM", sub="JUNE 12, 1962"),
 dict(line=32, img="B3_fbi_dummy_head.jpg", label="REAL PHOTO", z0=1.15, z1=1.3),
 dict(line=33, kind="pair", imgs=[("A1_fbi_morris.jpg", "MORRIS"), ("A2_fbi_john_anglin.jpg", "J. ANGLIN")]),
 dict(line=34, kind="hour", big="EPISODE 2", sub="THE FOURTH MAN"),
 dict(line=35, kind="end", img="D:/why habibi/_newchannel/01_alcatraz/export/thumbs_colour/B_IT_WAS_A_DUMMY_upload.jpg",
      label="THE FULL FILE", lines=["What the FBI Found When", "3 Men Vanished From Alcatraz", "on The Last Hours"]),
]
MUSIC = [("Shadowlands 2 - Bridge.mp3", 0.0, 9999, -21, 0.0)]          # (file, t0, t1, gain dB, offset s); t1 clipped to DUR
SFX_EV = [(0, None, "hit_cinematic_deep_impact", -18), (2, None, "whoosh_tunnel_reverb", -20), (12, "drill", "drill_on_off", -26),
          (24, "heads", "hit_deep_heartbeat_impact", -16), (27, None, "light_switch", -18), (31, None, "clock_tick_single", -18),
          (32, "rolls", "hit_big_cinematic_impact", -15), (30, None, "waves_rocky_shore", -28)]
