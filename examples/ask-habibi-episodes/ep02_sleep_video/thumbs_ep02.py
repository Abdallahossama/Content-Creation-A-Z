"""Ep 2 thumbnails (3 variants for YouTube Test & compare). Title: "Why Can't You Sleep Without a Video On?"
Thumb words (all scored 98/100 with the title by /yt-package title.py): STILL AWAKE? · VOLUME 4 · JUST ONE MORE"""
import os, sys
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
from thumbkit import *

PH = "D:/why habibi/2nd video/media/photos/"; S1 = "D:/why habibi/1st video/claude_package/stock/"
OUT = "D:/why habibi/2nd video/export/thumbnails/"; os.makedirs(OUT, exist_ok=True)
def save(c, n): p = OUT + n + ".png"; c.convert("RGB").save(p, optimize=True); print(p)

# 1) STILL AWAKE? - the man staring at his phone, pushed right; words + red LED on the dark left
c = photo(S1 + "pexels-11645171.jpg", focus=(0.5, 0.45), zoom=1.05, dx=230, bright=0.8, blue=1.15, red=0.85, contrast=1.2)
side_fade(c, 260, 640, 250); vignette(c, 0.5)
put(c, word("STILL", 150, WHITE), 36, 34)
put(c, word("AWAKE?", 190, YEL, stroke=14), 28, 178)
put(c, led("1:07", 100), 40, 470)
batata_peek(c, x=1110, size=110, expr="sideeye"); save(c, "thumb_1_STILL_AWAKE")

# 2) VOLUME 4 - man in bed lit by his phone; a huge yellow 4 with a marker circle
c = photo(PH + "frame_6943545_5s.png", focus=(0.42, 0.5), zoom=1.1, bright=1.25, blue=1.1, red=0.9, contrast=1.2)
side_fade(c, 760, 1150, 235, right=True); vignette(c, 0.45)
put(c, word("VOLUME", 140, WHITE), W - 36, 40, anchor="rt")
put(c, word("4", 330, YEL, stroke=16), 1050, 180)
circle(c, 1120, 380, 150, 175, RED, 11, seed=7)
batata_peek(c, x=40, size=110, expr="sleepy"); save(c, "thumb_2_VOLUME_4")

# 3) JUST ONE MORE - dark bedroom, giant red 1:07
c = photo(PH + "pexels-6943990.jpg", focus=(0.6, 0.5), bright=0.55, blue=1.18, red=0.85)
vignette(c, 0.55)
put(c, word("JUST ONE", 130, WHITE), 40, 34)
put(c, word("MORE", 220, YEL, stroke=14), 34, 160)
put(c, led("1:07", 150), 690, 420)
batata_peek(c, x=1110, size=110, expr="panic"); save(c, "thumb_3_JUST_ONE_MORE")

sheet = Image.new("RGB", (1280, 720 * 3 // 2 + 0), (0, 0, 0))
ims = [Image.open(OUT + n + ".png").resize((640, 360)) for n in ("thumb_1_STILL_AWAKE", "thumb_2_VOLUME_4", "thumb_3_JUST_ONE_MORE")]
sheet = Image.new("RGB", (1280, 720), (20, 20, 20))
for k, im in enumerate(ims): sheet.paste(im, ((k % 2) * 640, (k // 2) * 360))
sheet.save(OUT + "_sheet.png"); print("sheet")
