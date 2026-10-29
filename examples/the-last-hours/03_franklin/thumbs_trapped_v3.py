"""Franklin TRAPPED v3: the look of the user's reference (two ships frozen in, big, full colour, storm sky), built only from REAL images:
D10 = "Noon in mid-winter", HMS Enterprise and Investigator frozen in, 1849 (lithograph, PD) colour-graded; G4 = Pexels storm sky over pack ice
(multiplied into the flat engraved sky, so the masts stay); G8 = Pexels falling snow (screen). No AI.
  uv run --no-project --with pillow --with numpy python thumbs_trapped_v3.py"""
import sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, vign, block, ellipse, TW, TH, YEL, WHITE, RED
D = "D:/why habibi/_newchannel/03_franklin/export/thumbnails_colour/_options_v3/"

def gradient_map(im, stops):
    """B&W -> colour through luminance stops [(lum, (r,g,b)), ...]"""
    g = np.asarray(im.convert("L"), np.float32) / 255; out = np.zeros(g.shape + (3,), np.float32)
    xs = [s[0] for s in stops]
    for ch in range(3): out[..., ch] = np.interp(g, xs, [s[1][ch] for s in stops])
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def make(cx=0.66, cy=0.60, z=1.04, name="C_TRAPPED_588_DAYS_v3"):
    eng = src("03_franklin", "D10_"); eng = eng.crop((int(eng.width * 0.04), int(eng.height * 0.04), int(eng.width * 0.94), int(eng.height * 0.80)))
    base = cover(eng, TW, TH, cx=cx, cy=cy, z=z).convert("L")
    base = Image.fromarray(np.clip((np.asarray(base, np.float32) - 40) * 1.25, 0, 255).astype(np.uint8))      # deeper blacks, whiter snow
    col = gradient_map(base, [(0.0, (10, 18, 28)), (0.28, (42, 66, 84)), (0.52, (110, 146, 166)), (0.75, (200, 220, 230)), (1.0, (255, 250, 240))])
    a = np.asarray(col, np.float32)
    sky = np.asarray(cover(src("03_franklin", "G4_"), TW, TH, cx=0.5, cy=0.18, z=1.25).convert("RGB"), np.float32)
    sky = sky * np.array([0.92, 1.0, 1.08])                                                              # cold storm tint
    yy = np.linspace(0, 1, TH)[:, None, None]; m = np.clip((0.50 - yy) / 0.20, 0, 1)                  # sky only: top ~60%, soft edge
    a = a * (1 - m) + (a * sky / 255 * 1.7) * m                                                       # multiply keeps rigging and masts
    xx = np.linspace(0, 1, TW)[None, :, None]; glow = np.exp(-(((xx - 0.30) / 0.30) ** 2 + ((yy - 0.52) / 0.16) ** 2))   # low winter sun on the horizon
    a = a + glow * np.array([120, 70, 20]) * 0.55
    snow = np.asarray(cover(src("03_franklin", "G8_"), TW, TH, cx=0.5, cy=0.3, z=1.1).convert("L"), np.float32)
    flakes = np.clip((snow - np.asarray(Image.fromarray(snow.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32)) * 3.0, 0, 255)[..., None]
    a = 255 - (255 - a) * (255 - flakes * 0.8) / 255                                                    # screen in the real snowflakes
    c = grade(Image.fromarray(a.clip(0, 255).astype(np.uint8)), sat=1.15, contrast=1.08, teal=0.10, warm=0.08); c = vign(c, 0.55)
    block(c, "TRAPPED", 34, 92, 140)
    block(c, "FOR 588 DAYS", 34, 240, 112, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "SEPT 1846 - APRIL 1848", 34, 662, 54, fill=WHITE, bg=RED + (255,))
    c = c.convert("RGB"); c.save(D + name + ".png"); c.save(D + name + "_upload.jpg", quality=90); return c

if __name__ == "__main__":
    make(); print(D + "C_TRAPPED_588_DAYS_v3.png")
