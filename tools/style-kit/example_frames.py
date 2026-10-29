"""Reference frames for the style kit (built for Ep. 2) ('cut & marker', anti-AI-slop). Stills: python example_frames.py  |  motion test: python example_frames.py clip"""
import sys, json, subprocess
from PIL import Image
from marker import *

OUT = "D:/why habibi/_style_kit/examples/"
RC = "D:/why habibi/2nd video/receipts/"
STOCK = "D:/why habibi/1st video/claude_package/stock/"
MEMES = "D:/why habibi/1st video/claude_memes/"
BAT = BATATA
import os; os.makedirs(OUT, exist_ok=True)

PAGE = Image.open(RC + "chang2015_pubmed.png").convert("RGBA")
BX = json.load(open(RC + "chang2015_pubmed.json", encoding="utf-8"))["phrases"]
TITLE, DATE = BX["Evening use of light-emitting eReaders"][0], BX["2015 Jan 27"][0]
TITLE_BLOCK = (TITLE[0], TITLE[1] - 6, 1790, TITLE[1] + 216)           # all 3 title lines
JOURNAL = (BX["Clinical Trial"][0][0], DATE[1], DATE[2] + 260, DATE[3])
LONGER, TIRED = BX["took longer to fall asleep"][0], BX["reduced next-morning alertness"][0]

def save(c, name):
    p = OUT + name + ".png"; c.convert("RGB").save(p); print(p)

# ---- beat A: the receipt (title). "In a 2015 Harvard study..."
def receipt_title(t=9.0, s=1.22):
    c, tf = page_view(PAGE, (1010, 860), s, -1.4, marks=[(TITLE, min(1, t / 0.45), 3)],
                      focus=[TITLE_BLOCK, JOURNAL], dim=min(1, t / 0.2))
    c = vignette(c, 0.30)
    d0 = box_to_frame(DATE, tf)
    if t > 0.6:
        strokes(c, circle_path((d0[0] + d0[2]) / 2, (d0[1] + d0[3]) / 2, (d0[2] - d0[0]) / 2 + 26, (d0[3] - d0[1]) / 2 + 22, seed=5),
                RED, 9, min(1, (t - 0.6) / 0.35), seed=5)
    if t > 1.0:
        place(c, hand("harvard. real study.", 58, RED, rot=-3, reveal=min(1, (t - 1.0) / 0.3)), d0[2] + 230, d0[1] - 64)
    return caption(c, "in a 2015 harvard study")

# ---- beat B: the receipt (the finding) + Batata reaction
def receipt_finding(t=9.0, s=1.30):
    c, tf = page_view(PAGE, (1150, 1975), s, -1.4,
                      marks=[(LONGER, min(1, max(0, t / 0.4)), 7), (TIRED, min(1, max(0, (t - 2.6) / 0.4)), 9)],
                      focus=[LONGER] + ([TIRED] if t > 2.6 else []), dim=min(1, t / 0.2))
    c = vignette(c, 0.30)
    b = box_to_frame(LONGER, tf); cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    if t > 0.55:
        strokes(c, circle_path(cx, cy, (b[2] - b[0]) / 2 + 40, (b[3] - b[1]) / 2 + 34, seed=11), RED, 10, min(1, (t - 0.55) / 0.4), seed=11)
    if t > 1.0:
        strokes(c, arrow_path((cx - 170, cy - 215), (cx - 70, cy - 80), bend=0.3, seed=2), YEL, 9, min(1, (t - 1.0) / 0.25), seed=2)
    if t > 1.25:
        place(c, hand("+10 min to fall asleep\n(ish)", 68, YEL, rot=-4, reveal=min(1, (t - 1.25) / 0.3)), cx - 360, cy - 300)
    k = int(round((t - 1.9) * 30))
    if k >= 0:
        place(c, sticker(BAT + "Batata_shocked.png", 300, rot=8, scale=pop(k)), 1710, 770)
    if t < 2.6: return caption(c, "ten minutes longer")
    return caption(c, "more tired the next morning")

# ---- a meme beat, HOME-MADE (copyright-safe): the meme format rebuilt with Batata + marker, one hand note per panel
def meme_beat():
    from brand_v2 import texture
    c = texture(W, H)
    strokes(c, [np.stack([np.full(40, 960.0) + np.linspace(-6, 8, 40), np.linspace(70, 850, 40)], 1)], WHITE, 8, seed=2)
    place(c, hand("video on", 92, YEL, rot=-3), 480, 150); place(c, hand("video off", 92, YEL, rot=2), 1440, 150)
    place(c, sticker(BATATA + "Batata_sleepy.png", 560, rot=-4), 480, 560)
    place(c, sticker(BATATA + "Batata_panic.png", 560, rot=5), 1440, 560)
    place(c, hand("z z z", 70, WHITE, rot=-10), 720, 330)
    return caption(c, "turn him off")

# ---- level change: real photo, big words, an editor's scribble. No card, no frame, no label system.
def level_beat():
    c = night(fill(Image.open(STOCK + "pexels-460918.jpg"), (0.5, 0.5)), 0.22)
    t = bold("silence\nis loud.", 190, WHITE); place(c, t, 760, 360, "lt")
    place(c, hand("level 1", 84, YEL, rot=-4), 900, 270)
    strokes(c, underline_path(780, 1010, 318, seed=8), YEL, 9, seed=8)
    return c

# ---- annotate a real photo
def photo_beat():
    c = night(fill(Image.open(STOCK + "pexels-11645171.jpg"), (0.5, 0.45)), 0.4)
    strokes(c, circle_path(560, 590, 120, 170, seed=21, tilt=8), YEL, 11, seed=21)
    place(c, hand("autoplay just\nswitched to\ncrypto guy", 70, YEL, rot=-4), 300, 200)
    strokes(c, arrow_path((300, 330), (430, 500), bend=0.3, seed=6), YEL, 10, seed=6)
    return caption(c, "a stranger yelling about crypto")

def clip():
    """5.6 s motion test: hard cuts, punch-in on the beat, marker writes on, sticker pops with a shake"""
    fps = 30; N = int(5.6 * fps); p = OUT + "motion_test_receipt.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", p], stdin=subprocess.PIPE)
    for i in range(N):
        t = i / fps
        if t < 2.0:
            s = 1.12 if t < 0.9 else 1.30                      # hard punch-in on "Harvard", no easing
            c = receipt_title(t, s); c = shake(c, i - int(0.9 * fps), 10, seed=1)
        else:
            tt = t - 2.0; c = receipt_finding(tt, 1.30 + 0.02 * tt)   # slow push only while reading
            c = shake(c, i - int(3.9 * fps), 12, seed=2)
        ff.stdin.write(c.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait(); print(p)

if __name__ == "__main__":
    if sys.argv[1:] == ["clip"]: clip()
    else:
        save(receipt_title(), "1_receipt_title"); save(receipt_finding(2.0), "2_receipt_finding")
        save(meme_beat(), "3_meme_beat"); save(level_beat(), "4_level_change"); save(photo_beat(), "5_photo_note")
