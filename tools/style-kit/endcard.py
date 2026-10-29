"""Shorts end card (1080x1920) in the cut & marker style: 'part 2' on a highlighter swipe, a handwritten line,
a marker arrow to the profile picture (bottom-left in the Shorts UI) and Batata side-eyeing it.
_pipeline/core/shorts.py calls draw_endcard_v2() for every end card.   python endcard.py  -> preview PNGs"""
from PIL import ImageOps
from marker import *
from brand_v2 import texture

SW, SH = 1080, 1920

def highlighted(s, size, progress=1.0, seed=0):
    """navy Rubik words on a yellow highlighter swipe; the words appear as the swipe passes"""
    tx = bold(s, size, NAVY); bh = tx.height * 1.1
    band = swipe_band(tx.width + size * 0.3, bh, YEL, seed, progress)
    im = Image.new("RGBA", band.size, (0, 0, 0, 0)); im.alpha_composite(band)
    if progress > 0:
        m = Image.new("L", tx.size, 0); ImageDraw.Draw(m).rectangle((0, 0, int((tx.width + size * 0.1) * progress), tx.height), fill=255)
        t2 = tx.copy(); t2.putalpha(Image.composite(tx.getchannel("A"), Image.new("L", tx.size, 0), m))
        im.alpha_composite(t2, (int(size * 0.17), int(bh * 0.19)))
    im = im.rotate(-2, Image.BICUBIC, expand=True); return im.crop(im.getbbox()) if im.getbbox() else im

def draw_endcard_v2(t, part, last, cta_text=None, dur=2.8, seed=0):
    c = texture(SW, SH)
    l1, l2 = ("full video", "is on my channel") if last else (f"part {part + 1}", "is on my profile")
    hl = highlighted(l1, 200, 1.0, seed=part + seed); size = 200 if hl.width <= 960 else int(200 * 960 / hl.width)
    place(c, highlighted(l1, size, min(1, t / 0.3), seed=part + seed), SW / 2, 560)
    if t > 0.3: place(c, hand(l2, 96, WHITE, rot=-3, reveal=min(1, (t - 0.3) / 0.3)), SW / 2, 770)
    if t > 0.55:
        strokes(c, arrow_path((520, 1190), (170, 1640), bend=-0.35, head=64, seed=3), YEL, 17, min(1, (t - 0.55) / 0.3), seed=3)
    k = int(round((t - 0.2) * 30))
    if k >= 0:
        b = sticker(BATATA + "Batata_sideeye.png", 440, rot=0, scale=pop(k))
        place(c, ImageOps.mirror(b).rotate(-8, Image.BICUBIC, expand=True), 790, 1380)   # mirrored: eyes on the arrow
    if cta_text:                                     # the spoken CTA as captions, 1-3 words, channel caption style
        words = cta_text.split(); n = max(1, int(len(words) * min(1, (t - 0.25) / max(0.5, dur - 0.6))))
        line = " ".join(words[max(0, n - 3):n]).lower()
        if line: place(c, outlined(line, 84, WHITE, stroke=8), SW / 2, 960)
    return c

if __name__ == "__main__":
    draw_endcard_v2(2.0, 1, False, "part two is already on my profile").convert("RGB").save(KIT + "examples/shorts_endcard_part2.png")
    draw_endcard_v2(2.0, 5, True, "the full video is on my channel").convert("RGB").save(KIT + "examples/shorts_endcard_last.png")
    print("ok")
