"""Textures for the 3D Batata: the real potato photo with its transparent outside filled by blurred skin (so a front
projection never samples black), plus face-only ink layers (transparent) for each expression."""
import sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
from batata_boss import POT, v2_layer, confident
OUT = "D:/why habibi/shorts/s02_hypnic_jerk/tex/"
pot = POT.convert("RGBA"); a = pot.split()[3]
skin = Image.new("RGB", pot.size, (150, 110, 70)); base = pot.convert("RGB")
for r in (4, 12, 30, 70, 150):                                  # grow the skin outward in passes
    blur = base.filter(ImageFilter.GaussianBlur(r)); m = a.filter(ImageFilter.GaussianBlur(r)).point(lambda v: 255 if v > 3 else 0)
    w = Image.composite(blur, skin, m); skin = w
skin = Image.composite(base, skin, a.point(lambda v: 255 if v > 200 else 0))
skin.save(OUT + "potato_skin.png"); print("skin", skin.size)
for face in ("sleepy", "shocked", "panic", "fine"):
    lay = confident() if face == "confident" else v2_layer(face)
    lay.save(OUT + f"face_{face}.png"); print(face, lay.getbbox())
