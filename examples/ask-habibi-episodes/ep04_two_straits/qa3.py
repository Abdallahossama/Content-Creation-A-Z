"""QA: 3 stills per beat (25 / 55 / 88 %) -> build/qa3_sheet.png"""
import sys
from beats_ep04 import *
sel = {int(x) for x in sys.argv[1].split(",")} if len(sys.argv) > 1 else None
tiles = []
for i, b in enumerate(BEATS):
    if sel and i not in sel: continue
    for f in (0.25, 0.55, 0.88):
        tl = b.t0 + (b.t1 - b.t0) * f; c = b.frame(tl).convert("RGB").resize((480, 270))
        ImageDraw.Draw(c).rectangle((0, 0, 230, 18), fill=(0, 0, 0)); ImageDraw.Draw(c).text((4, 3), f"{i:02d} {b.name} {tl:.1f}s", fill=(255, 255, 0))
        k = 480 / 1920; ImageDraw.Draw(c).rectangle((420 * k, 860 * k, 1500 * k, 1010 * k), outline=(255, 40, 40))
        tiles.append(c)
    b.close(); print("qa", i, b.name, flush=True)
cols = 6; rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 480, rows * 270), (20, 20, 20))
for k, t in enumerate(tiles): sheet.paste(t, ((k % cols) * 480, (k // cols) * 270))
sheet.save(BUILD + "qa3_sheet.png"); print("sheet", BUILD + "qa3_sheet.png")
