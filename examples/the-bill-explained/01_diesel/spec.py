"""The Bill, Explained #1 - Why Diesel Costs $2 More Than Gas.
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe spec.py times|keys|qa|all 6"""
import sys, json, datetime
sys.path.insert(0, "D:/the-bill-explained/tools")
import billvid as BV
from billvid import KB, RECEIPT, BARS, LINE, BIG, CHAPTER, MAP, END, RED, BLUE, INK

ROOT = "D:/the-bill-explained/videos/01_diesel/"
NAME = "TheBillExplained_01_Diesel.mp4"
LEAD, TAIL = 0.6, 13.0
import os; VOF = os.environ.get("BV_VOF", "vo/vo.wav")
EIA = "EIA, week of Nov 9, 2026"

# ---- EIA weekly data (research/eia_weekly.json, from eia.gov/dnav hist_xls)
_d = json.load(open(ROOT + "research/eia_weekly.json"))
gas, die = dict(_d["gas"]), dict(_d["diesel"])
yrs = list(range(2005, 2027))
def yavg(y): k = [d for d in die if d.startswith(str(y)) and d in gas]; return sum(die[d] - gas[d] for d in k) / len(k)
GAP_Y = [round(yavg(y), 2) for y in yrs]
wk = sorted(d for d in die if d >= "2025-01-01" and d in gas)
WK_X = [datetime.date.fromisoformat(d).strftime("%b %y") for d in wk]
WK_G = [gas[d] for d in wk]; WK_D = [die[d] for d in wk]
WAR_I = min(range(len(wk)), key=lambda i: abs((datetime.date.fromisoformat(wk[i]) - datetime.date(2026, 2, 28)).days))

def S(key, shot): return (key, shot)
SHOTS = [
    S(0, KB("B1", z=(1.0, 1.18), c0=(.5, .55), tags=(((0, "$4|four"), "$4.00", 1500, 300),))),
    S(1, KB("C4", z=(1.04, 1.12), c0=(.6, .5), tags=(((1, "6|six"), "$6.13", 520, 320),))),
    S(2, KB("A3", crop=(0, .1, 1, .75), z=(1.02, 1.14), tags=(((2, "extra"), "+$2.13", 1450, 760),))),
    S(3, KB("N3", crop=(.12, 0, 1, 1), z=(1.03, 1.12), c0=(.55, .5))),
    S(4, CHAPTER("THE BILL, EXPLAINED  #1", "Why diesel costs $2 more", bg=("B1", None))),
    S(5, RECEIPT("Diesel vs. gas", [(6, "REGULAR GAS, 1 GAL", "$3.99"), (7, "DIESEL, 1 GAL", "$6.13")], total=(8, "THE GAP", "+$2.13"), sub=EIA, bg=("A1", None), src=EIA)),
    S(9, LINE("Diesel minus gas, yearly average", yrs, [("Gap", GAP_Y, RED)], src="EIA weekly retail prices (our math)", ymin=-0.25, ymax=1.75, fmt="${:.2f}")),
    S(11, BIG("$0.33", "the normal gap, 2010-2021")),
    S(12, BIG("6x", "today's gap vs. normal", bg=("A3", None))),
    S(13, BIG("$2.14", "record gap, early Nov 2026", count=(0.0, 2.14, 1.0), fmt="${:.2f}", col=RED)),
    S(14, BARS("Price change in one year", [(14, "Diesel", 59.7, RED), ((14, "gas"), "Gas", 30.7, BLUE)], fmt="+{:.0f}", unit="%", maxv=80, src=EIA)),
    S(15, LINE("Weekly price per gallon", WK_X, [("Diesel", WK_D, RED), ("Gas", WK_G, BLUE)], src="EIA weekly retail prices", ymin=2.5, ymax=7.0, gap=(0, 1), marks=[(WAR_I, "Feb 28, 2026")])),
    S(16, RECEIPT("Diesel's bill", [((16, 0.5), "LINE 1  THE BARREL", "$?.??"), ((16, 0.9), "LINE 2  THE REFINER", "$?.??"), ((16, 1.3), "LINE 3  THE WORLD", "$?.??"),
                                   ((16, 1.7), "LINE 4  THE TANKS", "$?.??"), ((16, 2.1), "LINE 5  TAX + WINTER", "$?.??")], total=((16, "one"), "TOTAL", "$2.13"), bg=("U1", None))),
    S(17, CHAPTER("LINE 1", "The barrel", bg=("E4", None))),
    S(18, KB("P2", z=(1.0, 1.1), c0=(.5, .45))),
    S(19, BARS("One 42-gallon barrel of crude makes...", [(19, "Gasoline", 19.5, BLUE), ((20, "11|eleven"), "Diesel + heating oil", 12.0, RED)], fmt="~{:.0f}", unit=" gal", maxv=26, src="EIA Energy Explained: Refining crude oil")),
    S(21, KB("E3", z=(1.04, 1.12))),
    S(22, KB("E1", z=(1.02, 1.12), c0=(.4, .5), c1=(.6, .5))),
    S(23, KB("C1", z=(1.0, 1.1), c0=(.75, .6))),
    S((24, "trucks"), KB("C3", z=(1.05, 1.1))),
    S((24, "tractors"), KB("K1", z=(1.06, 1.12), c0=(.65, .65))),
    S((24, "trains"), KB("I1", z=(1.04, 1.1))),
    S((24, "ships"), KB("J1", z=(1.04, 1.1))),
    S((24, "almost"), KB("D1", z=(1.02, 1.1))),
    S(25, KB("C2", z=(1.02, 1.12))),
    S(26, CHAPTER("LINE 2", "The refiner's cut", bg=("E2", None))),
    S(27, KB("E3", z=(1.12, 1.02), c0=(.5, .5))),
    S(28, BIG("Crack spread", "the refiner's margin on each barrel", col=INK)),
    S(29, BARS("Diesel crack spread, U.S. Gulf Coast", [(29, "January 2026", 28.62, BLUE), (30, "Late Sept 2026", 110.97, RED)], fmt="${:.0f}", unit=" / barrel", maxv=140, src="Crux Investor (ULSD crack, week to Sep 25, 2026)")),
    S(31, RECEIPT("$100 a barrel / 42 gallons", [(31, "REFINER MARGIN PER GALLON", "$2.38")], total=((32, "almost"), "GAP AT THE PUMP", "$2.13"), bg=("E1", None), src="Our math: $100 / 42 gal")),
    S(33, KB("E4", z=(1.02, 1.12), c0=(.4, .5))),
    S(34, KB("U3", z=(1.0, 1.12))),
    S(35, CHAPTER("LINE 3", "The world wants the same gallon", bg=("J1", None))),
    S(36, KB("F2", z=(1.0, 1.12))),
    S(37, MAP((25, 34, 75), [("pin", 10, 50, "Europe", (37, "europe")), ("pin", 50, 25.5, "Middle East", (38, "middle")),
                            ("route", [(56.3, 26.3), (58.5, 22.5), (52, 14.5), (43.4, 12.6), (38.5, 19), (33.5, 27.5), (32.4, 31.3), (25, 34), (14, 36.5), (5, 43)], (38, "imports"), 3.0)],
                title="Diesel into Europe", src="OGJ / IEA")),
    S(39, KB("G1", z=(1.0, 1.1), credit="NASA (public domain)")),
    S(40, MAP((56.4, 26.3, 9), [("pin", 56.35, 26.55, "Strait of Hormuz", (40, "strait"))], z=(1.0, 1.12), title="Strait of Hormuz")),
    S(41, BIG("-70%", "Hormuz shipping vs. normal, late Oct", count=(0, -70, 1.0), fmt="{:.0f}%", col=RED, bg=("G3", None))),
    S(42, KB("H1", z=(1.0, 1.1), credit="Moscow refinery, Jun 18, 2026 · CC0")),
    S(43, MAP((75, 56, 150), [("country", "Russia", (43, "russia"))], title="Russia limits fuel exports")),
    S(44, BIG("-60%", "Russia + Middle East diesel exports, Sept (World Bank est.)", count=(0, -60, 1.0), fmt="{:.0f}%", col=RED)),
    S(45, MAP((-40, 38, 125), [("pin", -94.5, 29.5, "U.S. Gulf Coast", (45, "barrels")), ("pin", -3, 46.5, "Europe", (45, "europe")),
                             ("route", [(-94, 28.5), (-85, 24.5), (-79, 26), (-60, 34), (-35, 42), (-15, 46), (-5, 47.5)], (46, "sails"), 2.2)], title="Where U.S. diesel goes")),
    S(47, CHAPTER("LINE 4", "Fewer refineries, emptier tanks", bg=("R2", None))),
    S(48, MAP((-105, 36, 50), [("x", -95.4, 29.8, (49, "houston")), ("x", -118.25, 33.9, (49, "angeles|los")), ("x", -122.16, 38.05, (49, "benicia"))],
              title="3 refineries stopped since 2025", src="EIA Refinery Capacity Report 2026")),
    S(50, BIG("547,000", "barrels a day of refining, gone", count=(0, 547000, 1.2), fmt="{:,.0f}")),
    S(51, KB("E2", z=(1.0, 1.1))),
    S(52, KB("R3", z=(1.0, 1.14))),
    S(53, BARS("U.S. diesel + heating oil in storage, early Nov", [(53, "2026", 103.3, RED), ((54, "average"), "2021-2025 average", 112.8, BLUE)], fmt="{:.1f}", unit="M barrels", maxv=135, src="EIA weekly distillate stocks, week ending Nov 6, 2026")),
    S((54, "lowest"), BIG("Record low", "for early November, in data back to 1982", col=RED)),
    S(55, KB("R1", z=(1.0, 1.12))),
    S(56, KB("F1", z=(1.02, 1.12))),
    S(57, KB("T1", z=(1.0, 1.1))),
    S(58, KB("D1", z=(1.1, 1.0))),
    S(59, CHAPTER("LINE 5", "Taxes and winter", bg=("P1", None))),
    S(60, KB("A1", z=(1.02, 1.12))),
    S(61, RECEIPT("Fuel taxes, per gallon", [(61, "FEDERAL, DIESEL", "24.4c"), ((61, "18|eighteen"), "FEDERAL, GAS", "18.4c"), (62, "STATES, DIESEL VS GAS", "+2.2c")],
                  total=(63, "TAXES' SHARE OF THE GAP", "~8c"), bg=("A1", None), src="EIA; state averages Jan 2026")),
    S(64, KB("P1", z=(1.02, 1.1))),
    S(65, KB("P2", z=(1.1, 1.0))),
    S(66, KB("V1", z=(1.3, 1.6), c0=(.8, .35), credit="NASA (public domain)")),
    S(67, KB("S1", z=(1.0, 1.1))),
    S(68, BIG("73%", "of U.S. freight moves by truck (by weight)", count=(0, 73, 1.0), fmt="{:.0f}%", bg=("C3", None))),
    S(69, RECEIPT("One long-haul semi, one year", [(69, "MILES", "100,000"), ((69, "6|six"), "MILES PER GALLON", "6.5"), ((69, "burns"), "DIESEL BURNED", "15,385 gal")],
                  total=(70, "EXTRA VS. GAS PRICE", "$32,800"), bg=("C1", None), src="Our math from EIA prices")),
    S(71, KB("C2", z=(1.0, 1.1))),
    S(72, KB("S2", z=(1.02, 1.1), c0=(.45, .5))),
    S(73, KB("O2", z=(1.0, 1.1))),
    S(74, KB("C3", z=(1.12, 1.02))),
    S(75, KB("K1", z=(1.0, 1.1))),
    S(76, BARS("Extra harvest diesel cost, per acre", [(76, "Corn", 7.98, RED), ((77, "apples"), "Apples", 57.59, RED)], fmt="${:.2f}", maxv=70, src="American Farm Bureau, Oct 1, 2026")),
    S(78, KB("L1", z=(1.0, 1.1))),
    S((79, "grocery"), KB("N3", crop=(.12, 0, 1, 1), z=(1.1, 1.0), c0=(.6, .5))),
    S((79, "box"), KB("O4", z=(1.0, 1.08))),
    S(80, MAP((-96, 37.5, 62), [("pin", -119.5, 37.0, "California $7.90", (81, "california")), ("pin", -81.0, 32.5, "Southeast $5.69", (82, "cheapest"))], title="Diesel, week of Nov 9, 2026", src=EIA)),
    S(83, BIG("$1.84", "the smallest gap anywhere in the U.S.", col=RED)),
    S(84, KB("T2", z=(1.0, 1.12))),
    S(85, LINE("EIA forecast, per gallon", ["Q4 26", "Q1 27", "Q2 27", "Q3 27", "Q4 27"], [("Diesel", [6.05, 5.37, 5.03, 4.91, 4.80], RED), ("Gas", [4.06, 3.69, 3.99, 3.91, 3.33], BLUE)],
               src="EIA Short-Term Energy Outlook, Nov 2026", ymin=2.5, ymax=7.0, gap=(0, 1))),
    S(87, BIG("4x", "normal, even in EIA's 2027 forecast", bg=("T2", None))),
    S(88, RECEIPT("Diesel's bill, explained", [(89, "1  THE BARREL", "LESS DIESEL"), (90, "2  THE REFINER", "RECORD MARGIN"), (91, "3  THE WORLD", "SUPPLY LOST"),
                                              (92, "4  THE TANKS", "RECORD LOW"), (93, "5  TAX + WINTER", "A LITTLE")], total=(94, "TOTAL PER GALLON", "$2.13"), bg=("B1", None), src=EIA)),
    S(95, END()),
]

OV = [
    ((33, "expects"), "label", dict(text="EIA: high margins through most of 2027", x=110, y=90, dur=4.5)),
    ((39, "february"), "label", dict(text="Feb 28, 2026", x=110, y=90, dur=4.0)),
    ((56, "treasury"), "label", dict(text="OFAC license: Russian diesel until Apr 7, 2027", x=110, y=90, dur=5.0)),
    ((57, "senators"), "label", dict(text="7 senators, both parties: conflicts with 2022 law", x=110, y=90, dur=5.5)),
    ((71, "27|$27|twenty"), "tag", dict(text="+$27,700 vs. normal", x=1380, y=900, h=120, dur=4.0)),
    ((73, "surcharge"), "label", dict(text="Fuel surcharge = weekly EIA diesel price", x=110, y=90, dur=5.0)),
    ((78, "7|seven"), "label", dict(text="Transport, storage + energy: 7%+ of food costs (USDA ERS)", x=110, y=90, dur=5.0)),
]

MUSIC = [("Stay the Course.mp3", 0.0, 5, -12), ("Floating Cities.mp3", 5, 35, -18), ("Industrial Cinematic.mp3", 35, 59, -18),
         ("Daily Beetle.mp3", 59, 80, -19), ("Floating Cities.mp3", 80, 95, -18), ("Stay the Course.mp3", 95, None, -14)]
EV = [((2, "extra"), "cash_register", -16), ((13, "record"), "impact_soft", -14)]
CH = [(0, "Diesel vs. gas: the $2.13 gap"), (5, "The bill as it stands"), (17, "Line 1: the barrel"), (26, "Line 2: the refiner's cut"),
      (35, "Line 3: the world wants the same gallon"), (47, "Line 4: fewer refineries, emptier tanks"), (59, "Line 5: taxes and winter"),
      (67, "Where the bill lands on you"), (80, "Diesel prices by region"), (84, "Will it come down?"), (88, "The full bill")]

CAPFIX = {"613": "$6.13", "214,": "$2.14,", "213.": "$2.13.", "213": "$2.13", "$790": "$7.90", "Lime": "Line", "wand,": "one."}
if __name__ == "__main__":
    BV.run(dict(globals(), __file__=__file__))
