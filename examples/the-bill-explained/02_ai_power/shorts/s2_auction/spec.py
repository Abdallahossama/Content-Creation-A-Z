"""EP2 Short 2 (standalone): the PJM auction behind New Jersey's +$26 bills. Vertical."""
import os, sys; os.environ["BV_SQUARE"] = "1"
sys.path.insert(0, "D:/the-bill-explained/tools")
import billvid as BV
from billvid import VID, BARS, BIG, MAP, RECEIPT, RED, BLUE
ROOT = "D:/the-bill-explained/videos/02_ai_power/shorts/s2_auction/"; MEDIA = "D:/the-bill-explained/videos/02_ai_power/media/"
NAME = "Short2_PJM_auction.mp4"; LEAD, TAIL = 0.15, 1.6; VERT = True; NO_CAPS = True
HEAD = ["New Jersey bills:", "+$26 a month. Why?"]
PJM = ["Delaware", "Illinois", "Indiana", "Kentucky", "Maryland", "Michigan", "New Jersey", "North Carolina", "Ohio", "Pennsylvania", "Tennessee", "Virginia", "West Virginia", "District of Columbia"]
SHOTS = [
    (0, BIG("+$26", "a month, one big NJ utility (2025)", col=RED, bg=("D8", None))),
    (1, MAP((-82, 39, 22), [("states", PJM, (1, "PJM|grid"))], title="PJM: 13 states + D.C.")),
    (2, VID("B2", at=8, z=(1.0, 1.1))),
    (3, BARS("Standby auction cost", [(3, "2024/25", 2.2, BLUE), ((3, "$16|sixteen|16"), "2026/27", 16.1, RED)], fmt="${:.1f}", unit="B", maxv=19, src="PJM")),
    (4, RECEIPT("Why it jumped", [((4, "data"), "DATA CENTERS", "63%")], bg=("A2", None), src="PJM market monitor")),
    (5, VID("D8", at=4, z=(1.0, 1.1))),
    (6, VID("A1", at=4, z=(1.0, 1.12))),
]
OV = []
MUSIC = [("Industrial Cinematic.mp3", 0.0, None, -15)]
EV = [((3, "$16|sixteen|16"), "impact_soft", -14)]
CAPFIX = {"Pjm": "PJM"}
if __name__ == "__main__": BV.run(dict(globals(), __file__=__file__))
