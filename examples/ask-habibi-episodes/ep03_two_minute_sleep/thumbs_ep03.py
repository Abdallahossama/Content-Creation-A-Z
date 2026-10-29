"""Ep 3 thumbnails (3 variants for YouTube Test & compare). Title: "Can You Really Fall Asleep in 2 Minutes?"
Thumb words (all 100/100 with the title in /yt-package title.py, different words from the title): 96%? · 2:00 · TRY LESS"""
import os, sys
import numpy as np
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
from thumbkit import *

PH = "D:/why habibi/3rd video/media/photos/"
OUT = "D:/why habibi/3rd video/export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
def save(c, n): p = OUT + n + ".png"; c.convert("RGB").save(p, optimize=True); print(p)
def strike(c, x0, y0, x1, y1, width=22, seed=3):
    pts = np.linspace([x0, y0], [x1, y1], 40) + np.random.default_rng(seed).normal(0, 1.5, (40, 2))
    MK.strokes(c, [pts], RED, width, seed=seed)

# 1) 96%? - the WWII plane (the "pilots"), a huge yellow 96%? with a red marker circle
c = photo(PH + "pexels-27057738.jpg", focus=(0.62, 0.5), zoom=1.15, dx=200, bright=0.75, blue=1.18, red=0.85, contrast=1.25)
side_fade(c, 300, 720, 240); vignette(c, 0.5)
w96 = word("96%?", 230, YEL, stroke=16); put(c, w96, 60, 190)
circle(c, 60 + w96.width / 2, 190 + w96.height / 2, w96.width / 2 + 40, w96.height / 2 + 55, RED, 12, seed=7)
batata_peek(c, x=1110, size=110, expr="sideeye"); save(c, "thumb_1_96")

# 2) 2:00 - the phone stopwatch; a red LED 2:00 struck out in marker
c = photo(PH + "pexels-4114789.jpg", focus=(0.42, 0.5), zoom=1.05, dx=260, bright=0.7, blue=1.15, red=0.85, contrast=1.2)
side_fade(c, 380, 820, 245); vignette(c, 0.5)
put(c, led("2:00", 220), 40, 170)
strike(c, 50, 520, 640, 230, width=26)
batata_peek(c, x=1110, size=110, expr="sleepy"); save(c, "thumb_2_200")

# 3) TRY LESS - the man asleep, calm; the advice in two words
c = photo(PH + "pexels-3771069.jpg", focus=(0.55, 0.42), zoom=1.1, dx=220, bright=0.8, blue=1.12, red=0.9, contrast=1.15)
side_fade(c, 330, 760, 245); vignette(c, 0.45)
put(c, word("TRY", 210, WHITE), 40, 90)
put(c, word("LESS", 260, YEL, stroke=16), 34, 320)
batata_peek(c, x=1110, size=110, expr="deadpan"); save(c, "thumb_3_TRY_LESS")

ims = [Image.open(OUT + n + ".png").resize((640, 360)) for n in ("thumb_1_96", "thumb_2_200", "thumb_3_TRY_LESS")]
sheet = Image.new("RGB", (1280, 720), (20, 20, 20))
for k, im in enumerate(ims): sheet.paste(im, ((k % 2) * 640, (k // 2) * 360))
sheet.save(OUT + "_sheet.png"); print("sheet")
