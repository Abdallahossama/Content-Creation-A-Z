"""Franklin thumbnail C v2 (24 Oct 2026, user: keep TRAPPED FOR 588 DAYS from _v1 "with some edits"): the _v1 image + a red
circle on the two small ships + a zoom bubble of D10 (lithograph 1850: a ship frozen in, men on the ice, Port Leopold 1849,
an Arctic search ship = illustrative) + the dates, big. The date block also covers the engraving's penguins (D4 is a fanciful
1860 print; there are no penguins in the Arctic). 588 days = 12 Sep 1846 (beset) to 22 Apr 1848 (abandoned), research.md.
  uv run --no-project --with pillow --with numpy python thumbs_trapped_v2.py"""
import sys
sys.path.insert(0, "D:/why habibi/_newchannel"); sys.path.insert(0, "D:/why habibi/_newchannel/03_franklin")
from PIL import Image
import thumbs_franklin_v3 as V
from thumbs_hakawi import src, grade, block, WHITE, RED
D = "D:/why habibi/_newchannel/03_franklin/export/thumbnails_colour/"
c = Image.open(D + "_v1/C_TRAPPED_588_DAYS.png").convert("RGBA")
V.ring(c, (868, 432, 978, 508), w=9)                                             # the two ships in the engraving
z = grade(src("03_franklin", "D10_").crop((1080, 540, 1760, 1220)), sat=1.1, contrast=1.3, teal=0.12, warm=0.06)
V.bubble(c, z, 300, 578, 132, src_xy=(870, 470), src_r=40)
block(c, "SEPT 1846 - APRIL 1848", 700, 606, 46, fill=WHITE, bg=RED + (255,))
c = c.convert("RGB"); c.save(D + "_options_v3/C_TRAPPED_588_DAYS_v2.png"); c.save(D + "_options_v3/C_TRAPPED_588_DAYS_v2_upload.jpg", quality=90)
print("ok")
