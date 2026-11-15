"""Short 1 (standalone): why diesel costs $2.13 more. Vertical 1080x1920."""
import os, sys; os.environ["BV_SQUARE"] = "1"
sys.path.insert(0, "D:/the-bill-explained/tools")
import billvid as BV
from billvid import KB, RECEIPT, BARS, BIG, MAP, RED, BLUE
ROOT = "D:/the-bill-explained/videos/01_diesel/shorts/s1_gap/"; MEDIA = "D:/the-bill-explained/videos/01_diesel/media/"
NAME = "Short1_Diesel_2_13_more.mp4"; LEAD, TAIL = 0.15, 1.6; VERT = True; NO_CAPS = True
HEAD = ["Diesel costs", "$2.13 more. Why?"]
SHOTS = [
    (0, BIG("+$2.13", "per gallon vs. gas: a record", col=RED, bg=("A3", None))),
    (1, BIG("$0.33", "the normal gap, 2010-2021")),
    (2, BARS("1 barrel of crude makes", [(2, "Gas", 19.5, BLUE), ((2, "11|eleven"), "Diesel", 12.0, RED)], fmt="~{:.0f}", unit=" gal", maxv=27, src="EIA")),
    (3, BIG("$2.38", "refiner's margin per gallon", bg=("E1", None))),
    (4, MAP((45, 42, 80), [("country", "Russia", (4, "russia")), ("pin", 50, 25.5, "Middle East", (4, "middle"))], title="-60% diesel exports")),
    (5, KB("R3", z=(1.0, 1.15), tags=(((5, "lowest"), "Record low", 560, 820),))),
    (6, BIG("8c", "of the gap is taxes")),
    (7, RECEIPT("Diesel's bill", [((7, 0.1), "BARREL", "LESS DIESEL"), ((7, 0.4), "REFINERS", "$2.38/GAL"), ((7, 0.7), "WORLD", "-60%")], total=((7, "213|$2|2|thirteen"), "TOTAL", "+$2.13"), bg=("N3", (.12, 0, 1, 1)), src="EIA, week of Nov 9, 2026")),
]
OV = []
MUSIC = [("Stay the Course.mp3", 0.0, None, -15)]
EV = [((0, "$2|thirteen"), "cash_register", -16)]
CAPFIX = {"613": "$6.13", "214,": "$2.14,", "213.": "$2.13.", "213": "$2.13", "$790": "$7.90", "Lime": "Line", "wand,": "one.", "1.": "One.", "2.": "Two.", "3.": "Three.", ".33": "33 cents", "-13": "to 13", (1, "sentence."): ""}
if __name__ == "__main__": BV.run(dict(globals(), __file__=__file__))
