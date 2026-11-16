"""EP2 Short 1 (standalone): one data center = 80,000 homes. Vertical."""
import os, sys; os.environ["BV_SQUARE"] = "1"
sys.path.insert(0, "D:/the-bill-explained/tools")
import billvid as BV
from billvid import VID, BARS, BIG, RED, BLUE
ROOT = "D:/the-bill-explained/videos/02_ai_power/shorts/s1_homes/"; MEDIA = "D:/the-bill-explained/videos/02_ai_power/media/"
NAME = "Short1_AI_80000_homes.mp4"; LEAD, TAIL = 0.15, 1.6; VERT = True; NO_CAPS = True
HEAD = ["This building uses", "80,000 homes of power"]
SHOTS = [
    (0, VID("A1", at=2, z=(1.0, 1.12), c=(.55, .5))),
    (1, VID("A4", at=6, z=(1.0, 1.1))),
    ((1, "cooling"), VID("B13", at=1, z=(1.0, 1.08))),
    (2, BARS("Data centers' share of US power", [(2, "2023", 4.4, BLUE), (3, "2030 (proj.)", 11.8, RED)], fmt="{:.1f}", unit="%", maxv=15, src="LBNL")),
    (4, VID("D4", at=8, z=(1.0, 1.1))),
    (5, VID("C1", at=3, z=(1.0, 1.08))),
    (6, VID("D3", at=4, z=(1.0, 1.12))),
]
OV = []
MUSIC = [("Industrial Cinematic.mp3", 0.0, None, -15)]
EV = [((0, "eighty|80"), "impact_soft", -14)]
CAPFIX = {"Pjm": "PJM"}
if __name__ == "__main__": BV.run(dict(globals(), __file__=__file__))
