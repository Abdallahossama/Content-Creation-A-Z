"""Ep 4 (documentary) beat list: moving real maps (mapcam), sourced receipts, doc-mode cards. Every cue is keyed to a
word in the voiceover. Layout: lower-thirds and labels stay above the caption band (bottom edge <= 800)."""
from ep04_fx import *
from ep04_map import *
import docfx as DX
import marker as MK
from mapkit import Map

def P(phrase, after=None):
    """timeline time of `phrase` (optionally the first occurrence after another phrase)"""
    return T(find(phrase, find(after) if after else 0.0))
def PE(phrase, after=None):
    return T(find_end(phrase, find(after) if after else 0.0))
def cut_before(phrase):
    """timeline time where the pause before `phrase` starts (the previous word's end)"""
    s = find(phrase); prev = max([t["e"] for t in TOK if t["e"] <= s + 1e-6] or [0.0]); return T(prev) + 0.05

BEATS, CUES = [], []
def beat(t0, bg, ovs=(), punch=(), shakes=(), name=""): BEATS.append(Beat(t0, bg, ovs, punch, shakes, name))
def cue(t, name, g=1.0): CUES.append((t, name, g))
ph3 = MEDIA + "photos/"
LAND_T, LAND_S = (70, 55, 35), (236, 224, 196)
def country(t, lon, lat, t_in, size=34): return Label(t, lon, lat, t_in, size=size, color=LAND_T, stroke=LAND_S, sw=3)
def sea(t, lon, lat, t_in, size=30): return Label(t, lon, lat, t_in, size=size, color=(200, 215, 240), stroke=(8, 14, 34), sw=3)

# ---------------------------------------------------------------- COLD OPEN
t0 = 0.0
beat(t0, DocPhotoBG(ph3 + "pexels-8266768.jpg", focus=(0.5, 0.5), grade=False, z=(1.0, 1.08), dark=0.75),
     [DX.Counter(4.36, 0.3, label="a gallon, today", fmt="${:.2f}", start=3.08, x=1320, y=330, size=190, dur=1.6),
      DX.LowerThird("a year ago: $3.08", P("more than last year.") - 0.2, sub="US average, regular · AAA, 12 Oct 2026", x=1000, y=560)],
     name="cold_gas")
cue(0.0, "room_tone", 0.4)

t1 = P("But why does a strip")
cam = Cam([(t1, 52, 22, 70), (P("Here's the strip.") + 0.3, 56.3, 26.3, 5.0, "fly"), (P("And here's the other one") - 0.1, 56.3, 26.3, 5.0),
           (PE("opposite corner of Arabia.") + 0.2, 43.4, 12.7, 5.0, "fly"), (P("This year, one of them") + 0.3, 50.0, 19.5, 21.0),
           (cut_before("This is Ask Habibi.") + 1.4, 49.5, 19.5, 20.0)])
beat(t1, MapBG(BASES, cam, [
    Pulse(*HORMUZ, P("Here's the strip.") + 0.8, ring=80), Label("Strait of Hormuz", *HORMUZ, P("Here's the strip.") + 1.0, size=40, dy=-90),
    country("Iran", 57.6, 27.6, P("between Iran") , 38), country("Oman", 57.3, 22.8, P("and Oman.") , 34),
    Pulse(*BAB, P("here's the other one") + 1.6, ring=80), Label("Bab el-Mandeb", *BAB, P("opposite corner") , size=40, dy=80),
    Barrier(*HORMUZ, P("closed by a war."), angle=-35, length=90, width=14),
    Label("closed", *HORMUZ, P("closed by a war.") + 0.3, size=44, color=RED, stroke=(255, 255, 255), dy=-150),
    Area(PERIM_RING, P("lost an island."), color=RED), HandCircle(*MAYUN, P("lost an island.") + 0.2, rx=60, ry=50),
    Label("an island, taken", *MAYUN, P("lost an island.") + 0.5, size=40, color=RED, stroke=(255, 255, 255), dy=95)]),
     name="map_open")
cue(t1, "whoosh_long", 0.5); cue(P("closed by a war."), "impact_soft", 0.6); cue(P("lost an island."), "impact_soft", 0.6)

# ---------------------------------------------------------------- TITLE + CHAPTER 1 card
tt = P("This is Ask Habibi.")
wb = BASES[0]; x0, y0 = wb.px(10, 48); x1, y1 = wb.px(90, 3)
title_bg = wb.img.crop((int(x0), int(y0), int(x1), int(y1))).resize((1920, 1080))
bat = MK.sticker(MK.BATATA + "Batata_deadpan.png", 200, border=10, rot=0)
beat(tt, DX.TitleCard("The two doors", "Ask Habibi · a documentary", title_bg, batata=bat), name="title")
cue(tt, "impact_soft", 0.8)

t_c1 = P("Oil, it turns out") - 1.9
cam = Cam([(t_c1, 56.2, 26.4, 6.5), (P("Iran on one side."), 56.3, 26.35, 3.3), (P("Every tanker leaving"), 52.5, 27.3, 9.5),
           (P("a chokepoint.") - 0.4, 56.3, 26.35, 3.6), (P("In 2024, about") - 0.2, 56.3, 26.35, 3.4)])
ports = [("Basra", 47.78, 30.51, "from Iraq,"), ("Kuwait", 47.98, 29.37, "Kuwait,"), ("Ras Tanura", 50.16, 26.64, "Saudi Arabia,"),
         ("Ras Laffan", 51.53, 25.91, "Qatar,"), ("Jebel Ali", 55.03, 25.01, "the Emirates"), ("Kharg", 50.32, 29.24, "Iran itself,")]
items = [country("Iran", 57.2, 27.35, P("Iran on one side."), 40), country("Oman", 56.25, 25.75, P("Oman's mountains"), 36)]
for name_, lon, lat, w in ports:
    tw = P(w, "Every tanker leaving"); items += [Dot(lon, lat, tw, color=YEL), Label(name_, lon, lat, tw + 0.1, size=26, dy=-30)]
items += [Flow([(50.5, 27.4), (53.5, 26.7), (56.0, 26.55), (56.6, 26.3), (57.4, 25.5)], P("has to squeeze through"), color=YEL, n=6),
          HandCircle(*HORMUZ, P("a chokepoint.") , rx=150, ry=110, color=YEL),
          Label("chokepoint", 57.55, 25.55, P("a chokepoint.") + 0.3, size=54, color=YEL, stroke=(8, 14, 34))]
beat(t_c1, MapBG(BASES, cam, items), [DX.ChapterCard(1, "The door", t_c1, P("Oil, it turns out") + 0.4)], name="ch1_door")
cue(t_c1, "riser_short", 0.5)

t0 = P("In 2024, about")
beat(t0, Receipt("eia_hormuz_2025",
                 [dict(t=t0, at="20 million barrels per day", s=1.25), dict(t=P("liquefied natural gas"), at="liquefied natural gas", s=1.3)],
                 [dict(phrase="20 million barrels per day", t=P("20 million") + 0.1), dict(phrase="20% of global petroleum liquids consumption", t=P("a fifth of all the oil")),
                  dict(phrase="liquefied natural gas", t=P("liquefied natural gas") + 0.1)], tag="U.S. Energy Information Administration · 16 Jun 2025"),
     [DX.Counter(20_000_000, t0 + 0.4, label="barrels a day through Hormuz, 2024", x=1180, y=230, size=110, dur=1.6, t_out=P("liquefied natural gas"))],
     name="r_eia")
cue(t0, "paper_slide", 0.6)

t0 = P("Most of it goes east.")
cam = Cam([(t0, 57.5, 25.0, 9), (P("84% of the crude") + 0.5, 62.0, 22.5, 16), (P("And if the door closes,") , 62.0, 22.5, 16),
           (P("only two ways around it") , 51.0, 24.8, 11)])
beat(t0, MapBG(BASES, cam, [
    Flow(HORMUZ_OUT, t0, color=YEL, n=9, size=18), Label("to Asia: 84%", 67.0, 20.5, P("84% of the crude") , size=48, color=YEL, dx=-120),
    Barrier(*HORMUZ, P("if the door closes,") , angle=-35, length=80, width=12),
    Route(EAST_WEST, P("pipelines in Saudi Arabia"), dur=1.4, color=YEL, width=7), Route(UAE_BYPASS, P("and the UAE.") , dur=0.8, color=YEL, width=7),
    Label("Saudi pipeline", 44.5, 25.0, P("pipelines in Saudi Arabia") + 1.0, size=30, color=YEL, dy=-36),
    Label("UAE pipeline", 55.2, 24.2, P("and the UAE.") + 0.6, size=28, color=YEL, dy=40)]),
     [DX.SourceTag("EIA, 2024 data", t0 + 0.3)], name="ch1_asia")

# ---------------------------------------------------------------- CHAPTER 2: the closing
t_c2 = P("On February 28th") - 2.1
cam = Cam([(t_c2, 56.3, 26.4, 4.6), (P("The United States answered"), 55.2, 26.6, 6.5), (P("In April, there was") , 55.0, 26.2, 6.0)])
beat(t_c2, MapBG(BASES, cam, [
    Barrier(*HORMUZ, P("largely blocked."), angle=-35, length=110, width=14),
    Route([(50.6, 28.5), (51.8, 27.55), (53.0, 26.8), (54.5, 26.3), (55.7, 26.42), (56.65, 26.72), (57.4, 25.75), (58.4, 25.35), (60.0, 25.0)],
          P("a blockade of its own,"), dur=1.4, color=(90, 160, 255), width=6, dash=(18, 10)),
    Label("US blockade of Iranian ports", 53.4, 26.25, P("against Iranian ports.") , size=32, color=(150, 200, 255))]),
    [DX.ChapterCard(2, "The closing", t_c2, P("On February 28th") + 0.4),
     DX.LowerThird("28 Feb 2026", P("On February 28th") + 0.3, sub="US and Israel attack Iran", t_out=P("Since then, Iran"))], name="ch2_closing")
cue(t_c2, "riser_short", 0.5)

t0 = P("In April, there was")
rng = np.random.default_rng(4); ships = []
for k in range(16):
    sx, sy = 52.6 + rng.uniform(0, 2.6), 26.0 + rng.uniform(0, 1.3)
    out = k < 4
    path = [(sx, sy), (55.8, 26.55), (56.5, 26.35)] + ([(57.4, 25.4), (58.6, 24.6)] if out else [])
    ships.append(Ship(path, P("Dozens of ships rushed") + rng.uniform(0, 0.6), P("made it out") + (1.4 if out else 0.2), color=WHITE, size=15, trail=False))
beat(t0, MapBG(BASES, Cam([(t0, 55.6, 26.2, 5.2), (P("made it out"), 56.3, 25.9, 5.6)]), ships + [
    Barrier(*HORMUZ, P("reversed the next day."), angle=-35, length=110, width=14),
    Label("at least 13 tankers got out", 58.4, 24.4, P("At least 13 tankers") + 0.3, size=34, color=YEL)]),
    [DX.LowerThird("17 Apr 2026", P("Iran announced the strait") , sub="a ceasefire, and a one-day reopening · CSIS"),
     DX.SourceTag("CSIS · 22 Apr 2026", t0 + 0.4)], name="ch2_april")

t0 = P("Both sides have attacked")
hits = [(56.1, 26.45), (56.6, 26.2), (57.0, 25.7), (56.4, 25.95), (55.6, 26.4), (57.4, 25.2), (56.9, 25.1), (58.1, 24.3), (56.2, 26.0)]
tn = P("nine ships were struck")
beat(t0, MapBG(BASES, Cam([(t0, 56.6, 25.9, 4.8), (PE("most of them oil tankers."), 56.8, 25.6, 4.4)]),
     [Pulse(x, y, tn + 0.18 * k, color=RED, r=7, ring=34, period=1.3) for k, (x, y) in enumerate(hits)]),
     [DX.LowerThird("1–6 Oct 2026", tn, sub="9 ships struck in or near the strait (IMO, via USNI News)"),
      DX.SourceTag("USNI News · 9 Oct 2026", t0 + 0.3)], name="ch2_strikes")
cue(tn, "impact_soft", 0.5)

t0 = P("And yet, the oil hasn't stopped.")
toff, tsts = P("switched off,"), P("pass the oil to other ships")
shuttle = Ship([(54.6, 26.3), (55.8, 26.55), (56.5, 26.3), (57.3, 25.5), (58.6, 24.5), (59.6, 23.9)], P("Ships cross the strait"), tsts + 0.4,
               color=YEL, size=16, dark=(toff - 0.1, tsts - 0.2))
waiting = Ship([(60.6, 23.4), (59.95, 23.75)], t0 + 0.5, tsts + 0.6, color=WHITE, size=18)
beat(t0, MapBG(BASES, Cam([(t0, 56.3, 26.1, 4.2), (tsts, 58.6, 24.6, 5.4), (PE("call it a shuttle.") , 58.4, 24.8, 6.0)]), [
    shuttle, waiting, Label("transponder off", 56.6, 25.9, toff, size=32, color=YEL, dy=-46, t_out=tsts),
    Label("ship-to-ship transfer", 59.8, 23.7, tsts + 0.4, size=32, color=WHITE, dy=-56),
    Label("the shuttle", 59.8, 23.7, P("call it a shuttle.") , size=46, color=YEL, dy=60)]),
    [DX.SourceTag("Lloyd's List, via USNI News · 9 Oct 2026", t0 + 0.3)], name="ch2_shuttle")

t0 = cut_before("In September, Lloyd's")
beat(t0, MapBG(BASES, Cam([(t0, 56.0, 26.0, 7.0), (P("the most since the war began.") , 56.0, 26.0, 6.4)]), []),
     [DX.Counter(477, P("477 crossings") - 0.3, label="crossings in September, by ships not linked to Iran", x=960, y=300, size=200, dur=1.2,
                 t_out=P("Its editor's verdict") - 0.1),
      DX.PullQuote("not a sustainable new normal.", "Richard Meade, editor, Lloyd's List (via USNI News, 9 Oct 2026)", P("Its editor's verdict"), y=340)],
     name="ch2_477")

# ---------------------------------------------------------------- CHAPTER 3: the back door
t_c3 = P("Saudi Arabia had a plan") - 2.1
cam = Cam([(t_c3, 49.0, 25.6, 6.0), (P("A pipeline straight across"), 49.0, 25.6, 6.0), (P("port of Yanbu."), 39.6, 24.3, 6.0),
           (P("Normally it carries"), 43.8, 24.9, 11.0)])
beat(t_c3, MapBG(BASES, cam, [
    Dot(*ABQAIQ, P("from the Gulf"), color=YEL), Label("Abqaiq", *ABQAIQ, P("from the Gulf") + 0.1, size=30, dy=-34),
    Route(EAST_WEST, P("A pipeline straight across"), dur=2.6, color=YEL, width=8),
    Dot(*YANBU, P("port of Yanbu.") - 0.2, color=YEL), Label("Yanbu", *YANBU, P("port of Yanbu."), size=36, dy=-40)]),
    [DX.ChapterCard(3, "The back door", t_c3, P("Saudi Arabia had a plan") + 0.4),
     DX.Counter(5, P("about five million") , label="million barrels a day, normally", fmt="{:.0f}", x=960, y=250, size=150, dur=0.6, t_out=P("In March, it hit")),
     DX.Counter(7, P("In March, it hit"), label="March 2026 · Fortune", fmt="{:.0f}", start=5, x=960, y=250, size=150, dur=0.6, t_out=P("a drone attack")),
     DX.Counter(0, P("a drone attack"), label="September: drone attack", fmt="{:.0f}", start=7, x=960, y=250, size=150, dur=0.5, color=RED, t_out=P("By early October,")),
     DX.Counter(5.8, P("By early October,"), label="early October · Al Jazeera, 6 Oct 2026", fmt="{:.1f}", start=0, x=960, y=250, size=150, dur=0.8,
                t_out=P("But a back door"))], name="ch3_pipeline")
cue(t_c3, "riser_short", 0.5); cue(P("a drone attack"), "impact_soft", 0.6)

t0 = P("But a back door")
conv = [Ship(RED_SEA_SOUTH[:6], P("sail south.") - 0.4 + 0.5 * k, P("Toward the second door.") + 1.0 + 0.5 * k, color=WHITE, size=13) for k in range(3)]
beat(t0, MapBG(BASES, Cam([(t0, 39.0, 23.0, 7.0), (P("Through the Red Sea."), 40.5, 18.5, 8.0), (PE("Toward the second door.") + 0.4, 42.8, 14.0, 6.0)]),
     [Dot(*YANBU, t0, color=YEL), Label("Yanbu", *YANBU, t0, size=34, dy=-40), sea("Red Sea", 39.2, 19.6, P("Through the Red Sea."), 34)] + conv),
     name="ch3_redsea")

# ---------------------------------------------------------------- CHAPTER 4: the second door
t_c4 = P("This is Bab el-Mandeb.") - 2.1
lanes = [[(43.05, 13.15), (43.28, 12.72), (43.36, 12.52), (43.55, 12.3)], [(43.09, 13.17), (43.32, 12.74), (43.40, 12.54), (43.59, 12.32)]]
beat(t_c4, MapBG(BASES, Cam([(t_c4, 43.2, 13.0, 4.0), (P("Eighteen miles wide"), 43.35, 12.68, 1.9), (P("It has been here before."), 43.35, 12.68, 1.9)]), [
    Label("Bab el-Mandeb", 43.35, 12.95, P("This is Bab el-Mandeb."), size=46, dy=-60),
    country("Yemen", 43.62, 12.95, P("This is Bab el-Mandeb.") + 0.5, 36), country("Djibouti", 43.12, 12.2, P("This is Bab el-Mandeb.") + 0.8, 30),
    Label("18 miles at its narrowest", 43.05, 12.45, P("Eighteen miles wide"), size=34, color=YEL),
    Route(lanes[0], P("two lanes,"), dur=1.0, color=WHITE, width=4, dash=(16, 10), glow=False),
    Route(lanes[1], P("two lanes,") + 0.2, dur=1.0, color=WHITE, width=4, dash=(16, 10), glow=False),
    Label("2 lanes, ~2 miles each", 43.62, 12.42, P("each about two miles wide.") , size=30, color=WHITE)]),
    [DX.ChapterCard(4, "The second door", t_c4, P("This is Bab el-Mandeb.") + 0.4), DX.SourceTag("EIA · 27 Aug 2019", P("Eighteen miles wide"))],
    name="ch4_bab")
cue(t_c4, "riser_short", 0.5)

t0 = P("It has been here before.")
tcape = P("Tankers went the long way,")
beat(t0, MapBG(BASES, Cam([(t0, 42.0, 15.0, 12.0), (P("Oil through this strait"), 42.5, 14.0, 11.0), (tcape, 25.0, -4.0, 70.0, "fly"),
                          (PE("around Africa.") + 0.3, 22.0, -6.0, 72.0)]), [
    Route(CAPE, tcape + 0.4, dur=2.2, color=WHITE, width=5, dash=(18, 12)),
    Label("around Africa", 14.0, -30.0, tcape + 1.6, size=40, color=WHITE)]),
    [DX.LowerThird("Nov 2023 – mid 2025", P("Starting in November 2023,"), sub="Houthis attack 100+ commercial ships (Al Jazeera)", t_out=P("Oil through this strait")),
     DX.Counter(4.0, P("Oil through this strait"), label="million barrels a day · 2023 → Jan–Aug 2024 · EIA", fmt="{:.1f}", start=8.7, x=1260, y=300,
                size=150, dur=1.6, t_out=tcape)], name="ch4_history")

t0 = P("Then, in September 2026,")
HANISH_R = None
for nm, r, b in Map(42.0, 44.0, 12.0, 15.0, 10, 10)._rings():
    if nm == "Yemen" and abs(b[0] - 42.686) < 0.01 and abs(b[1] - 13.664) < 0.01: HANISH_R = r
tm = P("Mayun Island.")
beat(t0, MapBG(BASES, Cam([(t0, 43.35, 12.7, 2.0), (tm, 43.42, 12.655, 0.42), (P("They also took the Hanish"), 43.42, 12.655, 0.42),
                          (P("to the north.") , 42.95, 13.3, 2.0), (P("The Houthis say ships") , 43.0, 13.2, 2.4)]), [
    Area(PERIM_RING, tm, color=RED), HandArrow(*MAYUN, tm + 0.3, frm=(-330, -200), color=RED),
    Label("Mayun (Perim)", *MAYUN, tm + 0.4, size=46, color=WHITE, dy=-150, dx=-160),
    Label("channel", 43.33, 12.66, P("splits it in two.") , size=30, color=YEL), Label("channel", 43.465, 12.67, P("splits it in two.") + 0.2, size=26, color=YEL),
    Area(HANISH_R, P("They also took the Hanish"), color=RED), Label("Hanish islands", 42.74, 13.72, P("They also took the Hanish") + 0.3, size=34, dy=-50)]),
    [DX.LowerThird("11–12 Sep 2026", tm + 0.6, sub="seized by the Houthis · government forces reportedly withdrew (AP, Al Jazeera)", t_out=P("They also took the Hanish"))],
    name="ch4_mayun")
cue(tm, "impact_soft", 0.7)

t0 = P("The Houthis say ships")
beat(t0, Receipt("aljazeera_mayun_2026_09_12",
                 [dict(t=t0, at="except for vessels linked to Saudi Arabia", s=1.3),
                  dict(t=P("But one security analyst"), at="real capability to shut down any maritime traffic", s=1.3)],
                 [dict(phrase="except for vessels linked to Saudi Arabia", t=P("except the ones linked")),
                  dict(phrase="real capability to shut down any maritime traffic", t=P("the real capability") - 0.1)],
                 tag="Al Jazeera · 12 Sep 2026"),
     [DX.LowerThird("Wolfgang Pusztai", P("But one security analyst") + 0.4, sub="security and defence analyst, to Al Jazeera")], name="r_aljazeera")
cue(t0, "paper_slide", 0.6)

t0 = P("And in October, the fighting")
beat(t0, MapBG(BASES, Cam([(t0, 45.5, 20.0, 16.0), (P("Missiles hit Riyadh's"), 46.0, 22.0, 11.0), (P("Saudi-backed forces launched"), 45.5, 18.5, 13.0)]), [
    Pulse(*RIYADH_AIRPORT, P("Missiles hit Riyadh's"), color=RED, r=9, ring=50), Label("Riyadh airport", *RIYADH_AIRPORT, P("Missiles hit Riyadh's") + 0.3, size=32, dy=-48),
    country("Saudi Arabia", 44.0, 23.5, t0 + 0.3, 40), country("Yemen", 47.3, 15.6, P("Saudi-backed forces launched"), 36),
    Label("counteroffensive", 44.6, 14.9, P("a counteroffensive in Yemen,"), size=32, color=YEL)]),
    [DX.LowerThird("October 2026", P("Missiles hit Riyadh's") + 0.4, sub="missile strikes on Riyadh airport; deaths reported (Al Jazeera, NBC)", t_out=P("Saudi-backed forces")),
     DX.LowerThird("11 Oct 2026", P("the American president said"), sub="Trump: the US \"could join\" (NBC News)")], name="ch4_october")

# ---------------------------------------------------------------- CHAPTER 5: your tank
t_c5 = P("So, why do two tiny") - 2.1
beat(t_c5, MapBG(BASES, Cam([(t_c5, 50.5, 19.5, 21.0), (P("Threaten that one too,"), 49.5, 19.0, 22.0)]), [
    Pulse(*HORMUZ, t_c5, ring=70), Pulse(*BAB, t_c5, ring=70),
    Flow(HORMUZ_OUT, t_c5, color=YEL, n=8, t_out=P("Close one,")),
    Barrier(*HORMUZ, P("Close one,"), angle=-35, length=70, width=12),
    Flow(EAST_WEST + RED_SEA_SOUTH, P("everything squeezes through"), color=YEL, n=12, size=14),
    Barrier(*BAB, P("Threaten that one too,"), angle=60, length=70, width=12, color=(255, 140, 40))]),
    [DX.ChapterCard(5, "Your tank", t_c5, P("So, why do two tiny") + 0.4)], name="ch5_doors")
cue(t_c5, "riser_short", 0.5)

t0 = P("Most of that oil goes to Asia.")
beat(t0, DocPhotoBG(ph3 + "pexels-8266768.jpg", focus=(0.5, 0.5), grade=False, z=(1.04, 1.1), dark=0.7),
     [DX.Counter(4.36, P("That's why your gallon"), label="a gallon in America, today", fmt="${:.2f}", start=3.08, x=1300, y=330, size=180, dur=1.4),
      DX.SourceTag("AAA national average · 12 Oct 2026", t0 + 0.3)], name="ch5_gas")

t0 = P("And it isn't only oil.")
beat(t0, DocPhotoBG(ph3 + "pexels-35757999.jpg", focus=(0.5, 0.5), grade=False, z=(1.0, 1.06), dark=0.8),
     [DX.LowerThird("~1/5 of the world's LNG trade", t0 + 0.4, sub="went through Hormuz in 2024 (EIA)")], name="ch5_lng")
t0 = P("Researchers at CSIS")
beat(t0, Receipt("csis_2026_04_22", [dict(t=t0, at="risen sharply", s=1.35)], [dict(phrase="risen sharply", t=P("rising sharply."))],
                 tag="CSIS · 22 Apr 2026"), [DX.LowerThird("heating. electricity.", P("That's heating."))], name="r_csis")
cue(t0, "paper_slide", 0.6)

t0 = cut_before("Here's what to watch next.")
w1, w2, w3 = P("Whether Iran reopens"), P("Whether the Houthis keep"), P("And whether anyone joins")
class Line3(DX.DOv):
    def __init__(self, text, t_in, y): self.t_in, self.t_out, self.y = t_in, None, y; self.im = DX.text_img(text, 58, WHITE)
    def draw(self, c, tl):
        a = self.fade(tl, 0.35, 0); DX.scrim(c, (220, self.y - 26, 260 + self.im.width + 40, self.y + self.im.height + 26), int(150 * a), 22)
        MK.place(c, DX._alpha(self.im, a), 260, self.y, "lt")
beat(t0, MapBG(BASES, Cam([(t0, 49.5, 19.5, 22.0), (PE("joins the fight."), 49.0, 19.5, 20.0)]),
     [Pulse(*HORMUZ, w1, ring=60), Pulse(*BAB, w2, ring=60)], vig=0.6),
     [Line3("1.  Does Iran reopen Hormuz?", w1, 200), Line3("2.  Do the Houthis keep Mayun?", w2, 330), Line3("3.  Does anyone join the fight?", w3, 460),
      DX.Stamp("as of 13 Oct 2026", P("This is how things stand"), x=1440, y=640)], name="ch5_watch")
cue(P("This is how things stand"), "impact_soft", 0.5)

t0 = P("If this helped you")
beat(t0, DocPhotoBG(ph3 + "pexels-36563588.jpg", focus=(0.5, 0.5), grade=False, z=(1.0, 1.06), dark=0.85),
     [DX.LowerThird("subscribe", P("subscribe.") , sub="next time: back to the midnight questions"),
      Sticker("deadpan", 260, 1730, 860, P("Next time, back") , rot=6)], name="cta")

beat(T_END_SCREEN, PhotoBG(KIT + "brand/end_screen_1920x1080.png", grade=False, z=(1.0, 1.0)), name="end_screen")

for b in BEATS:                                    # base-map labels in every map shot, unless the shot names that place itself
    if isinstance(b.bg, MapBG):
        own = {getattr(o, "text", None) for o in b.bg.items}
        b.bg.items = [l for l in BASE_LABELS if l.text not in own] + b.bg.items
STILL_IN_CAPTION_ZONE = caption_safe(BEATS)
for a, b in zip(BEATS, BEATS[1:]): a.t1 = b.t0
BEATS[-1].t1 = T_END
for b in BEATS:                                    # quiet, documentary sound design
    if isinstance(b.bg, Receipt):
        for m in b.bg.marks: cue(m["t"], "highlighter", 0.35)
    for o in b.ovs:
        k = type(o).__name__
        if k in ("LowerThird",): cue(o.t_in, "swoosh_in", 0.25)
        elif k in ("Counter",): cue(o.t_in, "pop", 0.25)
        elif k == "Sticker": cue(o.t_in, "sticker_slap", 0.4)
CUES.sort()

if __name__ == "__main__":
    print(len(BEATS), "beats,", len(CUES), "sfx cues, ends", round(T_END, 2), "| still in caption zone:", STILL_IN_CAPTION_ZONE)
    for i, b in enumerate(BEATS):
        print(f"{i:02d} {b.t0:7.2f}-{b.t1:7.2f} ({b.t1 - b.t0:5.2f}s) {b.name:14s} {type(b.bg).__name__:10s} {len(b.ovs)} ov")
    bad = [(i, b.name) for i, b in enumerate(BEATS) if b.t1 <= b.t0]
    assert not bad, f"non-positive beats: {bad}"
