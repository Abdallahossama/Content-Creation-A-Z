"""The Bill, Explained #2 - Why Your Power Bill Jumped $43 (It's Partly AI).
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe spec.py times|keys|qa|all 4"""
import sys, os
sys.path.insert(0, "D:/the-bill-explained/tools")
import billvid as BV
from billvid import VID, KB, RECEIPT, BARS, LINE, BIG, CHAPTER, MAP, END, RED, BLUE, INK

ROOT = "D:/the-bill-explained/videos/02_ai_power/"
NAME = "TheBillExplained_02_AI_Power.mp4"
LEAD, TAIL = 0.6, 13.0
VOF = os.environ.get("BV_VOF", "vo/vo.wav")
EIA = "EIA Electric Power Monthly, Aug 2026"
PJM_STATES = ["Delaware", "Illinois", "Indiana", "Kentucky", "Maryland", "Michigan", "New Jersey", "North Carolina", "Ohio",
              "Pennsylvania", "Tennessee", "Virginia", "West Virginia", "District of Columbia"]
PX = "Pexels"

SHOTS = [
    # cold open
    (0, VID("D3", at=2, speed=0.8, z=(1.0, 1.12), tags=(((0, "$43|forty"), "+$43/mo", 1450, 300),))),
    ((1, "lights|AI"), VID("A1", at=1, z=(1.0, 1.08))),
    ((1, "nobody"), VID("A2", at=0, speed=0.7, z=(1.05, 1.12))),
    (2, VID("A4", at=6, z=(1.0, 1.08))),
    (3, RECEIPT("Your electric bill", [((3, "$113|hundred"), "2020, PER MONTH", "$113"), ((3, "today"), "2026, PER MONTH", "$157")], total=((3, "$157|fifty"), "DIFFERENCE", "+$43"),
                bg=("D3", None), sub="EIA average prices, 863 kWh/month", src="EIA; our math")),
    (4, CHAPTER("THE BILL, EXPLAINED  #2", "The hidden AI charge", bg=("A1", None))),
    # what you pay
    (5, VID("D1", at=4, z=(1.0, 1.08))),
    (6, BARS("Average US home price, cents per kWh", [((6, "eighteen|18"), "Aug 2026", 18.16, RED), (7, "2020", 13.15, BLUE)], fmt="{:.1f}", unit="c", maxv=22, src=EIA)),
    (8, VID("D11", at=0, z=(1.0, 1.06))),
    (9, BIG("+$522", "a year, vs. 2020 prices (typical home)", count=(0, 522, 1.0), fmt="+${:,.0f}", col=RED, bg=("D13", None))),
    ((10, "gas"), VID("B6", at=1, z=(1.0, 1.08))),
    ((10, "storms"), VID("E12", at=2, z=(1.0, 1.06))),
    (11, VID("A5", at=3, speed=0.8, z=(1.0, 1.1))),
    (12, KB("P5", z=(1.05, 1.25), c0=(.5, .5), c1=(.35, .45))),
    # line 1: the appetite
    (13, CHAPTER("LINE 1", "The appetite", bg=("A4", None))),
    (14, VID("A1", at=6, z=(1.0, 1.1))),
    (15, VID("A10", at=10, z=(1.0, 1.06))),
    ((15, "needs"), VID("B13", at=1, z=(1.0, 1.08))),
    (16, BARS("Data centers' share of US electricity", [(16, "2023", 4.4, BLUE), (17, "2030 (projected)", 11.8, RED)], fmt="{:.1f}", unit="%", maxv=15,
              src="LBNL / DOE (2024); LBNL 2025 Update (Jun 2026)")),
    (18, BIG("~3x", "more of America's power in seven years", col=RED)),
    (19, VID("A2", at=3, z=(1.1, 1.0))),
    (20, BIG("80,000", "homes = one 100-megawatt data center", count=(0, 80000, 1.0), fmt="{:,.0f}", bg=("D1", None))),
    (21, VID("C8", at=12, z=(1.0, 1.06))),
    (22, MAP((-98, 36, 34), [("pin", -99.73, 32.45, "Abilene, TX: ~618 MW", (22, "abilene"))], title="Giant AI campuses", src="Epoch AI; Oracle, Sep 2026")),
    (23, MAP((-95, 33, 30), [("pin", -99.73, 32.45, "Abilene, TX", (23, 0.0)), ("pin", -91.75, 32.4, "Hyperion, LA: 2-5 GW", (23, "hyperion|louisiana"))],
             title="Giant AI campuses", src="TechCrunch; Louisiana PSC")),
    (24, VID("D4", at=6, z=(1.0, 1.08))),
    (25, VID("C1", at=2, z=(1.0, 1.06))),
    # line 2: the standby charge
    (26, CHAPTER("LINE 2", "The standby charge", bg=("C5", None))),
    (27, VID("B2", at=8, z=(1.0, 1.06))),
    (28, MAP((-82, 39, 24), [("states", PJM_STATES, (28, "PJM|grid"))], title="The PJM grid: 13 states + D.C.", src="PJM")),
    (29, VID("B1", at=10, z=(1.0, 1.06))),
    (30, KB("P6", z=(1.0, 1.15))),
    (31, BARS("PJM standby auction, total cost", [(31, "2024/25", 2.2, BLUE), ((33, "$14|fourteen|14"), "2025/26", 14.7, RED), ((33, "$16|sixteen|16"), "2026/27", 16.1, RED)],
              fmt="${:.1f}", unit="B", maxv=19, src="PJM; IEEFA; Utility Dive")),
    (32, VID("A1", at=10, z=(1.08, 1.0))),
    (34, BIG("9x", "jump in the price per megawatt, one auction", col=RED)),
    (35, VID("A4", at=18, z=(1.0, 1.08))),
    (36, RECEIPT("Why the auction jumped", [((36, "data"), "DATA CENTERS' SHARE", "63%")], total=((36, "$9|nine"), "COST OF THAT SHARE", "$9.3B"),
                 bg=("A2", None), src="PJM Independent Market Monitor")),
    (37, VID("C2", at=1, z=(1.0, 1.06))),
    (38, VID("D8", at=2, z=(1.0, 1.08))),
    (39, MAP((-75.6, 40.15, 7), [("states", ["New Jersey"], (39, "new jersey|jersey"))], title="New Jersey, June 2025: +17-20%", src="NJ BPU; CBS News")),
    (40, BIG("+$26", "a month, one big New Jersey utility", count=(0, 26, 0.8), fmt="+${:.0f}", col=RED, bg=("D3", None))),
    (41, VID("C3", at=3, z=(1.0, 1.06))),
    (42, MAP((-77, 39, 6), [("states", ["Maryland"], (42, "maryland"))], title="Maryland: +$10-21 a month", src="Maryland Office of People's Counsel")),
    (43, VID("A5", at=10, z=(1.06, 1.0))),
    # line 3: the wires
    (44, CHAPTER("LINE 3", "The wires", bg=("C3", None))),
    (45, VID("C8", at=30, z=(1.0, 1.08))),
    (46, VID("E8", at=2, z=(1.0, 1.06))),
    (47, BIG("$18.6B", "in rate increases requested, Jan-Jun 2026", count=(0, 18.6, 1.0), fmt="${:.1f}B", bg=("C1", None))),
    ((48, "storms"), VID("E11", at=6, z=(1.0, 1.06))),
    (49, KB("P1", z=(1.0, 1.15), credit="Ashburn, VA data centers · CC0")),
    # line 4: the fuel
    (50, CHAPTER("LINE 4", "The fuel", bg=("B6", None))),
    (51, VID("B11", at=4, z=(1.0, 1.06))),
    (52, BIG("+60%", "natural gas price, 2025 vs. 2024", col=RED, bg=("B9", None))),
    (53, VID("B9", at=6, z=(1.0, 1.06))),
    (54, MAP((-110, 40, 70), [("states", ["Maine", "New Hampshire", "Hawaii"], (54, "maine"))], title="Big jumps, few data centers", src="EIA via electricrates.org")),
    # line 5: who pays
    (55, CHAPTER("LINE 5", "Who should pay", bg=("D6", None))),
    (56, VID("D6", at=4, z=(1.0, 1.08))),
    (57, RECEIPT("New rules for big data centers", [((57, "ohio"), "OHIO (AEP)", "PAY 85%"), ((57, "virginia"), "VIRGINIA (DOMINION)", "PAY 60-85%")],
                 bg=("A4", None), sub="of the power they reserve, used or not", src="PUCO Jul 2025; Virginia SCC Nov 2025")),
    (58, RECEIPT("Oregon utility, new rates", [((58, "data"), "DATA CENTERS", "+29%"), ((58, "homes"), "HOMES", "-1.3%")], bg=("E6", None),
                 sub="Portland General Electric, Jul 2026", src="Portland General Electric, Jul 2026")),
    (59, VID("E6", at=10, z=(1.0, 1.06))),
    (60, VID("E4", at=2, z=(1.0, 1.06))),
    # how much is AI
    (61, VID("D3", at=10, z=(1.06, 1.0))),
    (62, BARS("Data centers' effect on wholesale prices", [((62, "seven|7"), "US, by 2025", 6.9, BLUE), ((62, "fifteen|15"), "N. Virginia", 15.0, RED)], fmt="+{:.1f}", unit="%", maxv=18,
              src="Dallas Fed WP 2606 (rev. Oct 2026)")),
    (63, BIG("$2-5", "a month for a typical home (our rough estimate)", col=INK)),
    (64, BIG("$10-25", "a month on many PJM bills (standby charge)", col=RED, bg=("D8", None))),
    (65, BARS("Average US price, cents per kWh", [(65, "2026", 18.2, BLUE), ((65, "eighteen|18"), "2027 (forecast)", 18.7, RED)], fmt="{:.1f}", unit="c", maxv=22, src="EIA STEO, Nov 2026")),
    # the full bill
    (66, RECEIPT("Your power bill, explained", [(67, "1  THE APPETITE", "~3X DEMAND"), (68, "2  THE STANDBY", "$2B > $16B"), (69, "3  THE WIRES", "UPGRADES"),
                                                (70, "4  THE FUEL", "GAS +60%"), (71, "5  WHO PAYS", "UNDECIDED")], total=(72, "TOTAL PER MONTH", "$157"), bg=("D3", None), src=EIA)),
    (73, END()),
]

OV = [
    ((22, "618|six"), "label", dict(text="OpenAI / Oracle, Abilene TX", x=110, y=920, dur=3.0)),
    ((37, "cap"), "label", dict(text="All hit the price cap (~$325-333/MW-day)", x=110, y=90, dur=4.5)),
    ((48, "storms"), "label", dict(text="Not only data centers", x=110, y=90, dur=3.5)),
    ((49, "ordered"), "label", dict(text="Virginia SCC, Aug 2026", x=110, y=90, dur=3.5)),
    ((53, "nothing"), "label", dict(text="Not AI", x=110, y=90, dur=3.0)),
    ((59, "share"), "label", dict(text="Berkeley Lab / Brattle, 2026", x=110, y=90, dur=4.0)),
]

MUSIC = [("Industrial Cinematic.mp3", 0.0, 5, -12), ("Floating Cities.mp3", 5, 26, -18), ("Industrial Cinematic.mp3", 26, 44, -18),
         ("Daily Beetle.mp3", 44, 61, -19), ("Floating Cities.mp3", 61, 73, -18), ("Stay the Course.mp3", 73, None, -14)]
EV = [((1, "nobody"), "impact_soft", -14), ((34, "nine|9"), "impact_soft", -14)]
CAPFIX = {"Pjm": "PJM", (17, "12th"): "12%", (17, "ascent"): "", (44, "is."): "", (50, "Google."): "", (7, "and"): "In"}
CH = [(0, "The hidden AI charge"), (5, "What you pay"), (13, "Line 1: the appetite"), (26, "Line 2: the standby charge"),
      (38, "Where it lands: New Jersey, Maryland"), (44, "Line 3: the wires"), (50, "Line 4: the fuel"), (55, "Line 5: who should pay"),
      (61, "How much of your bill is AI?"), (66, "The full bill")]

if __name__ == "__main__":
    BV.run(dict(globals(), __file__=__file__))
