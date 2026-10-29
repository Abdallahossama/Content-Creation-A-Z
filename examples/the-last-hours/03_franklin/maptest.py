import sys, math
sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween"); import mshorts as M
from PIL import Image
# temporarily render 16:9 panels by changing panel size
M.PW, M.PH = 1920, 1080; M._VIG.clear()
views = {"arctic": (-95.0, 72.0, 40.0), "kwi": (-97.5, 69.0, 9.0), "beechey": (-91.8, 74.7, 6.0)}
for k, v in views.items():
    b = dict(view=v, z=(1.0, 1.0), ops=[("pin", -91.9, 74.72, "BEECHEY ISLAND", 0.0), ("pin", -98.9, 69.65, "VICTORY POINT", 0.0),
                                        ("pin", -98.35, 68.95, "EREBUS (2014)", 0.0)])
    p = M.map_panel(b, 1.0, 0.0, 5.0); p.convert("RGB").save(f"maptest_{k}.png"); print(k, p.size)
