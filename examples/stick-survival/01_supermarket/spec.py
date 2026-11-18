"""Survival Diaries #1 - Zombie Outbreak: 30 Days Trapped in a Supermarket (stick figures, no AI images).
  uv run --no-project --python 3.11 --with pycairo --with numpy --with pillow --with soundfile python spec.py times|keys|qa|frame t|all 4"""
import sys, os, math
sys.path.insert(0, "F:/stick-survival/tools")
import stickvid as BV
from stickvid import STICK
from stickkit import Actor as A, ease, cl, draw_prop, lerp

ROOT = "F:/stick-survival/videos/01_supermarket/"
NAME = "SurvivalDiaries_01_Supermarket_30_Days.mp4"
LEAD, TAIL = 0.5, 13.0

def S(bg, actors=(), props=(), **kw): return STICK(bg=bg, actors=list(actors), props=list(props), **kw)
def DAY(n): return S("black", day=f"DAY {n}", daybig=True, vig=0.0, sfx=[(0.0, "hit_horror_drum", -16), (0.05, "marker_write", -20)])
def shut(t0, t1): return lambda u: ease((u - t0) / max(1e-3, t1 - t0))
def wr(t0, t1): return lambda u: cl((u - t0) / max(1e-3, t1 - t0))
def labels(*items):
    def fx(c, u, d):
        for (x, y, txt, t0) in items:
            if u >= t0: draw_prop(c, "bigtext", x, y, min(1.0, 0.6 + (u - t0) * 2), text=txt, size=70)
    return fx
def arc_fob(c, u, d):
    k = cl(u / 1.4); x = lerp(1000, 1850, k); y = 480 - math.sin(k * math.pi) * 260 + k * 300
    if k < 1: draw_prop(c, "keyfob", x, y, 1.6)
ZB = ["zombie", "zombie2", "zombie3"]
def hatch(c, u, d):
    c.rectangle(0, 430, 1080, 34); c.rectangle(1240, 430, 680, 34); c.set_source_rgb(0.33, 0.31, 0.29); c.fill()

SHOTS = [
    # ---------------- cold open
    (0, S("front", [A("me", 960, act="scared", face="scared", f=-1)], bgargs=dict(shutters=shut(0.3, 2.6), crowd=8), day="3:12 A.M.",
          sfx=[(0.3, "heavy_sliding_door", -14), (2.4, "gear_metallic_lock", -14)], cam=((1.0, 960, 540), (1.12, 960, 520)))),
    (1, S("lot", props=[dict(kind="minivan", x=1350, y=900), dict(kind="crowd", x=820, y=930, n=16, w=900, act="zidle")], cam=((1.0, 960, 560), (1.25, 900, 680)),
          sfx=[(0.0, "ambience_horror", -16)])),
    (2, S("aisle", [A("me", 960, act="worried", face="worried")], dark=0.55, cam=((1.0, 960, 540), (1.7, 960, 560)), sfx=[(0.0, "heartbeat_slow", -16)])),
    (3, S("black", day="DAY 30", daybig=True, vig=0.0, sfx=[(0.0, "marker_write", -18)])),
    ((3, "seventeen|17"), S("black", day="DAY 17", daybig=True, vig=0.0, shake=(0.0, 0.5, 8), sfx=[(0.0, "hit_cinematic_deep_impact", -12), (0.4, "heartbeat_horror_drum", -16)])),
    # ---------------- day 1
    (4, DAY(1)),
    (5, S("aisle", [A("me", 0, path=[(0, 420), (6, 1200)], act="walk", face="neutral")], props=[dict(kind="cart", x=0, y=905, path=[(0, 600), (6, 1380)])], day="DAY 1",
          sfx=[(0.0, "footsteps", -26)])),
    (6, S("backroom", [A("me", 760, act="radio", face="worried")], shake=(0.5, 3.0, 2), day="DAY 1", sfx=[(0.0, "radio_static_crackles", -16), (0.8, "siren_manual_fire_alert", -26)])),
    (7, S("front", [A("me", 520, act="stand", face=[(0, "neutral"), (1.6, "scared")], f=1), A("zombie", 0, path=[(0, 1500), (4, 1150)], act="zwalk", f=-1)],
          bgargs=dict(shutters=0.0, crowd=4), day="DAY 1", sfx=[(0.2, "door", -18), (1.6, "hit_horror_drum", -16)])),
    (8, S("aisle", [A("walt", 980, act=[(0, "idle"), (0.6, "scared")], face=[(0, "neutral"), (0.6, "scared")]), A("zombie", 0, path=[(0, 1400), (0.8, 1150)], act="zwalk", f=-1),
                    A("me", 520, act="scared", face="scared")], shake=(0.6, 1.4, 6), day="DAY 1", sfx=[(0.6, "hit_big_cinematic_impact", -14)])),
    (9, S("front", [A("rick", 0, path=[(0, 700), (1.2, 380)], act="run", face="scared", f=-1), A("me", 1000, act="scared", face="scared")], bgargs=dict(shutters=0.0, crowd=10), day="DAY 1",
          props=[dict(kind="bigtext", x=300, y=640, text="!", size=90)], sfx=[(1.2, "alarm_facility", -18)])),
    ((9, "shutters"), S("front", [A("rick", 380, act="worried", face="scared"), A("me", 1000, act="scared", face="scared")], bgargs=dict(shutters=shut(0.0, 1.8), crowd=12), day="DAY 1",
          sfx=[(0.0, "heavy_sliding_door", -12), (1.8, "factory_metal_hard_hit", -14)])),
    (10, S("front", [A("rick", 520, face="worried"), A("walt", 760, face="worried", bandage=True), A("marcus", 1000, face="neutral", f=-1), A("dex", 1240, face="smirk", f=-1), A("me", 1470, face="worried", f=-1)],
           bgargs=dict(shutters=1.0), day="DAY 1")),
    (11, S("front", [A("rick", 380, face="neutral"), A("walt", 700, face="smile"), A("marcus", 1020, face="neutral", f=-1), A("dex", 1320, face="smirk", f=-1), A("me", 1620, face="neutral", f=-1)],
           bgargs=dict(shutters=1.0), fx=labels((380, 360, "RICK", 0.1), (700, 360, "WALT", 0.9), (1020, 360, "MARCUS", 1.6), (1320, 360, "DEX", 3.0), (1620, 360, "ME", 4.2)),
           cam=((1.15, 700, 560), (1.15, 1250, 560)), sfx=[(0.1, "pop", -20), (0.9, "pop", -20), (1.6, "pop", -20), (3.0, "pop", -20), (4.2, "pop", -20)])),
    (12, S("front", [A("me", 700, face="sad", f=1, act="idle"), A("marcus", 1200, face="worried", f=-1)], bgargs=dict(shutters=0.45, crowd=18, seed=9), dark=0.25, day="DAY 1",
           cam=((1.0, 960, 540), (1.15, 960, 470)), sfx=[(0.0, "helicopter_far_away", -24)])),
    # ---------------- day 2
    (13, DAY(2)),
    (14, S("aisle", [A("walt", 860, face="smile", bandage=True, act="idle"), A("me", 1220, face="worried", f=-1)], day="DAY 2", cam=((1.25, 900, 600), (1.4, 880, 580)))),
    (15, S("aisle", [A("walt", 860, face="smile", act="carry", hold="bread", bandage=True), A("rick", 1250, face="smile", f=-1), A("dex", 520, face="smirk")], day="DAY 2")),
    (16, S("storeroom", [A("marcus", 760, act="think", face="neutral")], bgargs=dict(cans=1.0, water=1.0), day="DAY 2", sfx=[(0.2, "paper_writing_pencil", -22)])),
    (17, S("storeroom", [A("marcus", 760, act="point", face="smile")], bgargs=dict(cans=1.0, water=1.0), day="DAY 2",
           fx=labels((960, 260, "4,000 CANS", 0.0), (960, 360, "600 WATERS", 1.6)), sfx=[(0.0, "pop", -18), (1.6, "pop", -18)])),
    (18, S("backroom", [A("rick", 900, act="talk", face="smile", talk=True), A("dex", 1250, face="smirk", f=-1)], day="DAY 2", fx=labels((960, 200, "3 DAYS. TOPS.", 0.6)))),
    (19, S("backroom", [A("me", 1300, act="write", face="neutral", hold="marker", f=-1)], bgargs=dict(wall_text="DAY 2", write_u=wr(0.4, 1.6), wx=1050, size=120), day="DAY 2",
           sfx=[(0.4, "marker_write", -18)], cam=((1.0, 960, 540), (1.25, 1150, 420)))),
    # ---------------- day 3
    (20, DAY(3)),
    (21, S("backroom", [A("marcus", 520, face="worried"), A("me", 800, face="worried")], props=[dict(kind="door", x=1300, y=905, sign="WC")], bgargs=dict(radio=False), day="DAY 3",
           sfx=[(0.5, "creak", -22)])),
    (22, S("backroom", [A("marcus", 980, act=[(0, "stand"), (1.0, "scared")], face=[(0, "neutral"), (1.0, "scared")]), A("zwalt", 1300, act="zwalk", f=-1, z=-1)],
           props=[dict(kind="door", x=1300, y=905, open=1.0, sign="WC", z=-2)], bgargs=dict(radio=False), day="DAY 3", shake=(1.0, 1.6, 9),
           sfx=[(0.0, "door", -18), (1.0, "hit_horror_drum", -12), (1.05, "sweep_terror_darkness", -18)])),
    (23, S("black", sfx=[(0.6, "metal_hammer_hit", -14)])),
    ((23, "Marcus"), S("backroom", [A("marcus", 900, act="worried", face="shock", hold="flashlight")], bgargs=dict(radio=False), dark=0.35, day="DAY 3", cam=((1.4, 900, 560), (1.5, 900, 540)))),
    (24, S("aisle", [A("rick", 520, act="hug_knees", face="worried"), A("dex", 800, act="sit", face="angry"), A("marcus", 1100, act="sit", face="worried", f=-1), A("me", 1400, act="hug_knees", face="scared", f=-1)],
           dark=0.7, day="DAY 3", sfx=[(0.0, "roomtone_dark_cinematic", -20)])),
    (25, S("black", props=[dict(kind="bigtext", x=960, y=470, text="BITE OR SCRATCH", size=110, col="#e74c3c"), dict(kind="bigtext", x=960, y=640, text="= ABOUT 1 DAY", size=110)],
           sfx=[(0.0, "hit_short_bass", -14)])),
    # ---------------- day 5
    (26, DAY(5)),
    (27, S("backroom", [A("rick", 700, act="radio", face="sad"), A("me", 1100, face="worried", f=-1)], day="DAY 5", sfx=[(0.0, "radio_static_fx", -16)], cam=((1.0, 900, 560), (1.2, 800, 560)))),
    (28, S("front", [A("marcus", 760, act="point", face="angry"), A("me", 1100, face="neutral", f=-1), A("dex", 1350, face="smirk", f=-1)], bgargs=dict(shutters=1.0), day="DAY 5")),
    (29, S("front", [A("me", 0, path=[(0, 1650), (3, 900)], act="push", face="angry", f=-1)], props=[dict(kind="cart", x=0, y=905, path=[(0, 1520), (3, 770)], f=-1),
           dict(kind="cart", x=520, y=905), dict(kind="cart", x=650, y=905)], bgargs=dict(shutters=0.25, crowd=8), day="DAY 5", sfx=[(0.0, "car_pass", -26)])),
    (30, S("front", [A("me", 0, path=[(0, 1700), (3, 1250)], act="carry", face="tired", f=-1, hold="sack")], bgargs=dict(shutters=0.25, barricade=True), day="DAY 5",
           sfx=[(2.8, "impact_soft", -16)])),
    (31, S("storeroom", [A("dex", 700, act="point", face="smile")], props=[dict(kind="ladder", x=1150, y=905)], bgargs=dict(cans=0.8, water=0.8), day="DAY 5",
           cam=((1.0, 960, 540), (1.15, 1100, 380)), sfx=[(0.3, "metal_tool_drop", -20)])),
    (32, S("roof", [A("me", 700, face="worried", y=890), A("dex", 1000, face="neutral", y=890, f=-1)], bgargs=dict(sky="dawn"), day="DAY 5", cam=((1.0, 960, 540), (1.0, 960, 540)),
           sfx=[(0.0, "wind_ambience", -18)])),
    ((32, "Except"), S("lot", props=[dict(kind="crowd", x=960, y=930, n=22, w=1700)], cam=((1.3, 960, 700), (1.0, 960, 540)), sfx=[(0.0, "whoosh_ghostly", -16)])),
    # ---------------- day 8
    (33, DAY(8)),
    (34, S("aisle", [A("me", 960, face="neutral", act="idle")], day="DAY 8")),
    ((34, "out"), S("aisle", [A("me", 960, face="scared", act="worried")], dark=0.85, day="DAY 8", sfx=[(0.0, "light_switch", -12), (0.2, "hit_short_bass", -16)])),
    (35, S("aisle", [A("me", 0, path=[(0, 500), (4, 1400)], act="walk", face="worried", hold="flashlight")], dark=0.5, torch=lambda u: (lerp(600, 1500, cl(u / 4)), 560), day="DAY 8")),
    (36, S("aisle", [A("me", 700, act="carry", face="smile", hold="steak"), A("walt", 1200, face="smile", f=-1)], props=[dict(kind="grill", x=960, y=905)], dark=0.35, day="DAY 8",
           sfx=[(0.3, "water_splash", -30)])),
    (37, S("aisle", [A("rick", 500, act="eat", face="smile"), A("dex", 760, act="sit", face="smile"), A("marcus", 1160, act="eat", face="smile", f=-1), A("me", 1420, act="cheer", face="happy", f=-1)],
           props=[dict(kind="grill", x=960, y=905)], dark=0.3, day="DAY 8")),
    (38, S("lot", props=[dict(kind="crowd", x=0, y=930, n=14, w=700, path=[(0, 300), (5, 1100)])], day="DAY 8", sfx=[(0.0, "footsteps_stones_loop", -22)])),
    (39, S("lot", props=[dict(kind="crowd", x=960, y=930, n=40, w=1800, seed=8)], cam=((1.35, 960, 640), (1.0, 960, 540)), fx=labels((960, 220, "40+", 0.3)),
           sfx=[(0.0, "ambience_horror", -14), (0.3, "hit_short_bass", -14)])),
    (40, S("aisle", [A("me", 800, face="worried", act="idle"), A("marcus", 1150, face="worried", f=-1)], props=[dict(kind="grill", x=960, y=905)], dark=0.6, day="DAY 8")),
    # ---------------- day 11
    (41, DAY(11)),
    (42, S("backroom", [A("rick", 700, act="point", face="angry")], bgargs=dict(wall_text="RULES", write_u=1.0, wx=1000, size=110), day="DAY 11", sfx=[(0.0, "marker_squeak", -18)])),
    (43, S("backroom", [A("rick", 700, act="point", face="neutral")], bgargs=dict(wall_text="RULES\n1 CAN / DAY\n2 WATERS", write_u=wr(0.0, 3.0), wx=1000, size=90), day="DAY 11",
           sfx=[(0.2, "marker_write", -18)])),
    (44, S("backroom", [A("rick", 700, act="point", face="angry")], bgargs=dict(wall_text="RULES\n1 CAN / DAY\n2 WATERS\nNO DOORS ALONE", write_u=1.0, wx=1000, size=90), day="DAY 11",
           sfx=[(0.0, "marker_squeak", -18)])),
    (45, S("backroom", [A("dex", 760, act="talk", face="angry", talk=True), A("rick", 1160, act="point", face="angry", f=-1)], bgargs=dict(radio=False), day="DAY 11", shake=(0.4, 0.8, 3),
           cam=((1.2, 960, 560), (1.3, 960, 540)))),
    (46, S("storeroom", [A("me", 900, act="think", face="worried")], bgargs=dict(cans=0.75, water=0.9), day="DAY 11", cam=((1.0, 960, 540), (1.2, 700, 620)))),
    (47, S("storeroom", [A("me", 900, act="worried", face="sad")], bgargs=dict(cans=0.7, water=0.9), dark=0.3, day="DAY 11", cam=((1.4, 900, 520), (1.8, 900, 470)))),
    # ---------------- day 14
    (48, DAY(14)),
    (49, S("backroom", [A("rick", 520, face="worried"), A("me", 760, act="radio", face="shock"), A("marcus", 1100, face="worried", f=-1), A("dex", 1350, face="neutral", f=-1)], day="DAY 14",
           sfx=[(0.0, "radio_static_fx", -14)])),
    (50, S("map", bgargs=dict(route=wr(0.4, 3.5)), sfx=[(0.0, "paper_page_turn", -16), (0.4, "marker_squeak", -18)])),
    (51, S("bridge", props=[dict(kind="boat", x=0, y=900, path=[(0, 1300), (6, 1500)])], day="DAY 14", sfx=[(0.0, "motorboat_sea", -18)])),
    (52, S("backroom", [A("rick", 760, act="point", face="angry"), A("dex", 1160, act="talk", face="angry", f=-1, talk=True)], bgargs=dict(radio=False), day="DAY 14")),
    ((52, "Dex"), S("backroom", [A("rick", 760, face="angry"), A("dex", 1160, act="point", face="angry", f=-1)], bgargs=dict(radio=False), day="DAY 14", cam=((1.3, 1100, 520), (1.35, 1100, 520)))),
    (53, S("backroom", [A("marcus", 960, act="talk", face="neutral", talk=True)], bgargs=dict(radio=False), day="DAY 14")),
    (54, S("backroom", [A("me", 960, act="carry", face="worried", hold="map")], bgargs=dict(radio=False), day="DAY 14", cam=((1.2, 960, 560), (1.45, 960, 520)))),
    # ---------------- day 17
    (55, S("black", day="DAY 17", daybig=True, vig=0.0, shake=(0.0, 0.4, 8), sfx=[(0.0, "hit_cinematic_deep_impact", -12), (0.1, "heartbeat_horror_drum", -14)])),
    (56, S("aisle", [], dark=0.75, cam=((1.0, 960, 540), (1.3, 960, 600)), day="DAY 17", sfx=[(0.0, "wind_scary", -18)])),
    (57, S("storeroom", [A("me", 900, act=[(0, "lie"), (1.6, "crouch")], face=[(0, "sleep"), (1.6, "scared")], y=880)], bgargs=dict(cans=0.6, water=0.5), dark=0.6, day="DAY 17",
           sfx=[(0.0, "wind_cold_interior", -16), (0.0, "clock_tick_single", -20)])),
    (58, S("backroom", [A("me", 700, face="scared", act="scared")], props=[dict(kind="door", x=1300, y=905, open=0.9, inside="#2b3a55")], bgargs=dict(radio=False), dark=0.45, day="DAY 17",
           sfx=[(0.0, "creak", -14), (0.0, "wind_scary", -18)])),
    (59, S("storeroom", [A("me", 900, act="scared", face="shock")], bgargs=dict(cans=0.45, water=0.0), dark=0.3, day="DAY 17", fx=labels((960, 250, "HALF THE FOOD", 0.9), (960, 350, "ALL THE WATER", 2.0)),
           sfx=[(0.9, "hit_short_bass", -14), (2.0, "hit_short_bass", -12)])),
    (60, S("backroom", [], props=[dict(kind="door", x=1300, y=905, open=1.0, inside="#2b3a55")], bgargs=dict(radio=False), dark=0.45, day="DAY 17", cam=((1.0, 1100, 540), (1.35, 1300, 600)),
           sfx=[(0.0, "wind_scary", -16)])),
    (61, S("aisle", [A(ZB[i % 3], 400 + i * 260, act="zwalk", f=-1 if i % 2 else 1, z=i) for i in range(5)], dark=0.6, day="DAY 17",
           sfx=[(0.0, "hit_glass_suspense", -14), (0.2, "ambience_horror", -16)])),
    (62, S("aisle", [A("me", 0, path=[(0, 1500), (3.5, 200)], act="run", face="scared", f=-1, hold="flashlight"), A("zombie", 0, path=[(0, 1900), (3.5, 650)], act="zwalk", f=-1)],
           dark=0.55, torch=lambda u: (lerp(1400, 300, cl(u / 3.5)), 560), shake=(0.0, 4.0, 3), day="DAY 17",
           sfx=[(0.0, "footsteps", -14), (0.0, "heartbeat_horror_drum", -14)])),
    (63, S("storeroom", [A("marcus", 1210, act="crouch", face="angry", y=430, f=-1, s=1.0), A("me", 1150, act="climb", face="scared", y=905, s=1.0)], props=[dict(kind="ladder", x=1150, y=905, h=480)],
           bgargs=dict(cans=0.3, water=0.0), dark=0.45, day="DAY 17", fx=hatch, sfx=[(0.3, "metal_tool_falling", -16)])),
    (64, S("aisle", [A("rick", 960, act="scared", face="scared")] + [A(ZB[i % 3], 960 + d, act="zwalk", f=-1 if d > 0 else 1, z=1) for i, d in enumerate([-420, -260, 280, 450])],
           dark=0.65, cam=((1.5, 960, 560), (1.0, 960, 540)), day="DAY 17", sfx=[(0.0, "hit_cinematic_deep_impact", -12), (0.4, "sweep_horror_long", -18)])),
    # ---------------- day 18
    (65, DAY(18)),
    (66, S("roof", [A("me", 760, act="hug_knees", face="sad", y=890), A("marcus", 1060, act="sit", face="tired", y=890, f=-1)], bgargs=dict(sky="day"), day="DAY 18", sfx=[(0.0, "wind_ambience", -20)])),
    (67, S("roof", [A("me", 560, act="sit", face="worried", y=890), A("marcus", 1360, act="sit", face="worried", y=890, f=-1)],
           props=[dict(kind="bottle", x=880 + i * 40, y=880) for i in range(3)] + [dict(kind="can", x=820 + i * 32, y=930) for i in range(12)], bgargs=dict(sky="day"), day="DAY 18",
           fx=labels((960, 250, "2 PEOPLE", 0.0), (960, 350, "3 WATERS", 1.0), (960, 450, "12 CANS", 2.0)), sfx=[(0.0, "pop", -20), (1.0, "pop", -20), (2.0, "pop", -20)])),
    (68, S("aisle", [A(ZB[i % 3], 250 + i * 200, act="zidle", f=1 if i % 2 else -1, s=1.15) for i in range(8)], dark=0.55, day="DAY 18", cam=((1.0, 960, 540), (1.1, 960, 600)),
           sfx=[(0.0, "ambience_horror", -16)])),
    (69, S("roof", [A("marcus", 900, act="talk", face="smile", talk=True, y=890), A("me", 1250, face="smile", y=890, f=-1)], bgargs=dict(sky="day"), day="DAY 18")),
    (70, S("roof", [A("me", 760, act="crouch", face="neutral", y=890), A("marcus", 1160, act="crouch", face="neutral", y=890, f=-1)], props=[dict(kind="map", x=960, y=920)], bgargs=dict(sky="day"),
           day="DAY 18", sfx=[(0.0, "paper_page_turn", -18)])),
    # ---------------- day 20
    (71, DAY(20)),
    (72, S("roof", [A("me", 800, act="eat", face="tired", y=890, hold="can"), A("marcus", 1150, act="sit", face="tired", y=890, f=-1)], bgargs=dict(sky="day"), day="DAY 20")),
    (73, S("roof", [A("me", 800, act="eat", face="sad", y=890, hold="bottle")], bgargs=dict(sky="day"), day="DAY 20", fx=labels((960, 260, "1/2 CAN A DAY", 0.0), (960, 360, "1 CAP OF WATER / 2 HRS", 1.8)),
           sfx=[(0.0, "pop", -20), (1.8, "pop", -20)])),
    (74, S("roof", [A("me", 650, act="cheer", face="happy", y=890), A("marcus", 1500, act="cheer", face="smile", y=890, f=-1)], props=[dict(kind="pool", x=1050, y=920)], bgargs=dict(sky="rain"),
           day="DAY 20", sfx=[(0.0, "thunder_deep_rumble", -16)])),
    (75, S("roof", [A("me", 960, act="shrug", face="sad", y=890, baggy=1.7)], bgargs=dict(sky="day"), day="DAY 20", cam=((1.2, 960, 560), (1.3, 960, 540)))),
    (76, S("roof", [A("me", 760, act="lie", face="worried", y=900), A("marcus", 1160, act="lie", face="tired", y=900, f=-1)], bgargs=dict(sky="night"), day="DAY 20",
           sfx=[(0.0, "footsteps_tunnel_loop", -22)])),
    # ---------------- day 23
    (77, DAY(23)),
    (78, S("roof", [A("marcus", 960, act="cheer", face="happy", y=890)], bgargs=dict(sky="day"), day="DAY 23", props=[dict(kind="bigtext", x=1090, y=330, text="!", size=120)], sfx=[(0.0, "bell", -18)])),
    (79, S("aisle", [A(ZB[i % 3], 300 + i * 330, act="zidle", f=1, s=1.15, flip_at=None) for i in range(5)], dark=0.5, day="DAY 23", fx=labels((960, 250, "THEY FOLLOW SOUND", 0.3)),
           sfx=[(0.3, "hit_short_bass", -14)])),
    (80, S("roof", [A("marcus", 900, act=[(0, "stand"), (0.4, "throw")], face="angry", y=890), A("me", 600, face="worried", y=890)], bgargs=dict(sky="day"), fx=arc_fob, day="DAY 23",
           sfx=[(0.4, "whoosh_fast", -16)])),
    (81, S("lot", props=[dict(kind="minivan", x=1300, y=900, alarm=True, night=False), dict(kind="keyfob", x=1050, y=920, s=1.5)], bgargs=dict(night=False), day="DAY 23",
           sfx=[(0.0, "keys_dropping", -16), (0.5, "alarm_vintage_warning", -14)])),
    (82, S("lot", props=[dict(kind="minivan", x=1500, y=900, alarm=True), dict(kind="crowd", x=0, y=930, n=24, w=900, path=[(0, 300), (6, 1000)])], bgargs=dict(night=False), day="DAY 23",
           sfx=[(0.0, "alarm_vintage_warning", -20)])),
    (83, S("black", props=[dict(kind="bigtext", x=960, y=600, text="10 MINUTES", size=170, col="#f1c40f")], sfx=[(0.0, "clock_ticking_closeup", -14)])),
    (84, S("aisle", [A("me", 0, path=[(0, 200), (4, 1700)], act="run", face="angry", hold="backpack"), A("marcus", 0, path=[(0, -100), (4, 1400)], act="run", face="angry", hold="bottle")],
           day="DAY 23", sfx=[(0.0, "footsteps", -14), (0.0, "riser", -18)])),
    (85, S("roof", [A("me", 760, act="cheer", face="happy", y=890), A("marcus", 1160, act="cheer", face="happy", y=890, f=-1)],
           props=[dict(kind="backpack", x=960, y=920), dict(kind="can", x=1040, y=920), dict(kind="bottle", x=880, y=920)], bgargs=dict(sky="day"), day="DAY 23")),
    # ---------------- day 26
    (86, DAY(26)),
    (87, S("roof", [A("me", 760, act="radio", face="shock", y=890, hold=None), A("marcus", 1160, face="worried", y=890, f=-1)], props=[dict(kind="radio", x=960, y=920)], bgargs=dict(sky="day"),
           day="DAY 26", sfx=[(0.0, "radio_static_crackles", -16)])),
    (88, S("bridge", props=[dict(kind="boat", x=1300, y=900)], fx=labels((960, 220, "LAST BOAT: DAY 30", 0.4)), day="DAY 26", sfx=[(0.0, "ship_hull_creak", -18), (0.4, "hit_short_bass", -14)])),
    (89, S("street", props=[dict(kind="crowd", x=960, y=930, n=26, w=1800, seed=12)], fx=labels((960, 200, "12 MILES", 0.2)), day="DAY 26", sfx=[(0.0, "wind_scary", -18)])),
    (90, S("roof", [A("marcus", 900, act="talk", face="angry", talk=True, y=890), A("me", 1250, face="worried", y=890, f=-1)], bgargs=dict(sky="dawn"), day="DAY 26",
           cam=((1.2, 1000, 560), (1.3, 1000, 540)))),
    # ---------------- day 29
    (91, DAY(29)),
    (92, S("roof", [A("marcus", 0, path=[(0, 400), (4, 1100)], act="walk", face="neutral", y=890), A("me", 0, path=[(0, 150), (4, 850)], act="walk", face="neutral", y=890)], bgargs=dict(sky="night"),
           day="DAY 29", dark=0.2)),
    (93, S("roof", [A("marcus", 900, act="point", face="neutral", y=890, hold="keyfob"), A("me", 1250, face="neutral", y=890, f=-1, hold="keyfob")], bgargs=dict(sky="night"), day="DAY 29")),
    (94, S("backroom", [A("me", 1250, act="write", face="sad", hold="marker", f=-1)], bgargs=dict(radio=False, tally=29), dark=0.3, day="DAY 29")),
    (95, S("backroom", [A("me", 1600, act="write", face="sad", hold="marker", f=-1)], bgargs=dict(radio=False, wall_text="DAY 29.\nIF YOU FIND THIS,\nWE WENT NORTH.", write_u=wr(0.0, 3.5), wx=500, size=96),
           dark=0.2, cam=((1.0, 960, 540), (1.1, 900, 420)), sfx=[(0.0, "marker_write", -16)])),
    # ---------------- day 30
    (96, DAY(30)),
    (97, S("street", [A("marcus", 0, path=[(0, 300), (5, 1100)], act="walk", face="neutral", hold="backpack"), A("me", 0, path=[(0, 80), (5, 880)], act="walk", face="worried", hold="backpack")],
           day="DAY 30", sfx=[(0.0, "footsteps_stones_loop", -22)])),
    (98, S("lot", props=[dict(kind="minivan", x=1400, y=900, alarm=True), dict(kind="crowd", x=0, y=930, n=18, w=700, path=[(0, 500), (5, 1100)])], day="DAY 30",
           sfx=[(0.0, "alarm_vintage_warning", -18)])),
    (99, S("street", [A("marcus", 0, path=[(0, 200), (4, 700)], act="walk", face="neutral"), A("me", 0, path=[(0, 0), (4, 500)], act="walk", face="neutral")],
           props=[dict(kind="crowd", x=1450, y=930, n=10, w=600, face=1, act="zidle")], day="DAY 30", sfx=[(0.0, "keys_moving", -18), (0.8, "alarm_facility", -24)])),
    (100, S("bridge", [A("marcus", 0, path=[(0, -100), (4, 420)], act="walk", face="happy", y=860), A("me", 0, path=[(0, -300), (4, 220)], act="walk", face="happy", y=860)],
            props=[dict(kind="boat", x=1300, y=900)], day="DAY 30", sfx=[(0.0, "waves_with_birds", -18)])),
    (101, S("bridge", props=[dict(kind="boat", x=1300, y=900)], cam=((1.0, 960, 540), (1.5, 1300, 760)), day="DAY 30", sfx=[(0.0, "ship_engine_loop", -20)])),
    (102, S("bridge", [A("dex", 640, face="smirk", y=860), A("me", 140, face="shock", y=860, s=1.1), A("marcus", 300, face="angry", y=860, s=1.1)],
            props=[dict(kind="cart", x=820, y=860)] + [dict(kind="can", x=760 + i * 26, y=760) for i in range(5)], day="DAY 30", sfx=[(0.0, "hit_horror_drum", -14)])),
    ((103, "smiled"), S("bridge", [A("dex", 640, face="smirk", y=860)], props=[dict(kind="cart", x=820, y=860), dict(kind="boat", x=1400, y=900)], cam=((1.6, 640, 640), (1.7, 640, 620)), day="DAY 30")),
    ((103, "pointed"), S("bridge", [A("dex", 640, act="point", face="smirk", y=860)], props=[dict(kind="cart", x=820, y=860), dict(kind="boat", x=1400, y=900)],
            cam=((1.6, 640, 640), (1.0, 960, 540)), day="DAY 30", sfx=[(0.0, "whoosh_long", -18)])),
    (104, S("bridge", props=[dict(kind="boat", x=1300, y=900), dict(kind="crowd", x=1300, y=840, n=9, w=380, who=["man", "soldier", "rick"], act="stand", expr="neutral")],
            cam=((1.0, 960, 540), (1.7, 1300, 760)), day="DAY 30", sfx=[(0.0, "hit_big_cinematic_impact", -12)])),
    (105, S("bridge", [A("me", 300, face="shock", y=860), A("marcus", 480, face="worried", y=860)], props=[dict(kind="boat", x=1300, y=900)], dark=0.45,
            fx=labels((960, 300, "TO BE CONTINUED...", 0.4)), sfx=[(0.4, "riser_cinematic_trailer", -16)])),
    (106, S("black", props=[dict(kind="bigtext", x=960, y=560, text="PART 2", size=200, col="#e74c3c")], sfx=[(0.0, "hit_horror_drum", -14)])),
    (107, S("roof", [A("me", 760, act="cheer", face="happy", y=890), A("marcus", 1160, act="cheer", face="smile", y=890, f=-1)], bgargs=dict(sky="dawn"),
            fx=labels((960, 230, "SUBSCRIBE", 0.2)), sfx=[(0.2, "pop", -16)])),
    (108, S("roof", [A("me", 240, act="think", face="neutral", y=890, s=1.0)], bgargs=dict(sky="night"), dark=0.35,
            fx=labels((960, 150, "WHERE SHOULD I SURVIVE NEXT?", 0.2)), vig=0.5)),
]

OV = []
MUSIC = [("SCP-x5x.mp3", 0.0, 4, -16), ("Stay the Course.mp3", 4, 20, -19), ("SCP-x5x.mp3", 20, 33, -19), ("I Can Feel it Coming.mp3", 33, 55, -20),
         ("Shadowlands 2 - Bridge.mp3", 55, 65, -18), ("Man Down.mp3", 65, 77, -20), ("Darkling.mp3", 77, 86, -19), ("I Can Feel it Coming.mp3", 86, 96, -20),
         ("Darkling.mp3", 96, 105, -18), ("SCP-x5x.mp3", 105, None, -17)]
EV = []
CAPFIX = {}
CH = [(0, "3:12 a.m."), (4, "Day 1: the shutters"), (13, "Day 2: what we had"), (20, "Day 3: the bathroom"), (26, "Day 5: barricades"), (33, "Day 8: the feast"),
      (41, "Day 11: the rules"), (48, "Day 14: the radio"), (55, "Day 17"), (65, "Day 18: the roof"), (71, "Day 20: rationing"), (77, "Day 23: they follow sound"),
      (86, "Day 26: the last boat"), (91, "Day 29: the plan"), (96, "Day 30: the bridge")]

if __name__ == "__main__":
    BV.run(dict(globals(), __file__=__file__))
