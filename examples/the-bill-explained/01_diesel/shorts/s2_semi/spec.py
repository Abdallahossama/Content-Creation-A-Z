"""Short 2 (standalone): one semi pays $32,800 more. Vertical 1080x1920."""
import os, sys; os.environ["BV_SQUARE"] = "1"
sys.path.insert(0, "D:/the-bill-explained/tools")
import billvid as BV
from billvid import KB, RECEIPT, BIG, RED
ROOT = "D:/the-bill-explained/videos/01_diesel/shorts/s2_semi/"; MEDIA = "D:/the-bill-explained/videos/01_diesel/media/"
NAME = "Short2_Semi_32800.mp4"; LEAD, TAIL = 0.15, 1.6; VERT = True; NO_CAPS = True
HEAD = ["This truck pays", "+$32,800 a year"]
SHOTS = [
    (0, KB("C1", crop=(.25, 0, 1, 1), z=(1.0, 1.12), c0=(.6, .55), tags=(((0, 0.2), "+$32,800", 600, 830),))),
    (1, RECEIPT("One semi, one year", [(1, "MILES", "100,000"), ((1, "six"), "MILES PER GALLON", "6.5")], bg=("C3", None))),
    (2, BIG("15,385", "gallons of diesel", count=(0, 15385, 1.0), fmt="{:,.0f}")),
    (3, BIG("+$2.13", "per gallon vs. gas", col=RED, bg=("A3", None))),
    (4, RECEIPT("The math", [(4, "15,385 GAL", "x $2.13")], total=((4, "$32|thirty"), "EXTRA", "$32,800"), bg=("C1", None), src="EIA prices, our math")),
    (5, KB("O2", z=(1.0, 1.12))),
    (6, KB("N3", crop=(.12, 0, 1, 1), z=(1.0, 1.12))),
]
OV = [((5, "surcharge"), "label", dict(text="Fuel surcharge", x=60, y=60, dur=4.0))]
MUSIC = [("Stay the Course.mp3", 0.0, None, -15)]
EV = [((4, "$32|thirty"), "cash_register", -16)]
CAPFIX = {"613": "$6.13", "214,": "$2.14,", "213.": "$2.13.", "213": "$2.13", "$790": "$7.90", "Lime": "Line", "wand,": "one."}
if __name__ == "__main__": BV.run(dict(globals(), __file__=__file__))
