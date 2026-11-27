"""Split the owner's full-body waving drawing (raw/wave_full.webp -> cut/wave_full.png) into the body and the raised hand, so the hand
can rock around the wrist (a wave) while the body stays put.  uv run --no-project --with pillow --with numpy python make_wave.py"""
from PIL import Image
import numpy as np
A = "D:/why habibi/_newchannel/brand/avatar/"
PIVOT = (112, 236)                                    # the wrist, in cut/wave_full.png pixels
im = Image.open(A + "cut/wave_full.png").convert("RGBA"); a = np.asarray(im).copy()
yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
mask = (((yy < 200) & (xx < 196)) | ((yy < 230) & (xx < 168))) & (yy > 60) & (xx > 40) & (a[..., 3] > 0)   # hand incl. the thumb
lum = a[..., :3].astype(np.float32).mean(2); mask &= ~((xx >= 166) & (lum < 95))       # the dark collar tip next to the thumb stays
hand = np.zeros_like(a); hand[mask] = a[mask]; base = a.copy()
base[mask & (yy < 212)] = 0                           # the heel of the palm stays under the rotating hand: no gap at the wrist
Image.fromarray(base).save(A + "cut/wave_base.png"); Image.fromarray(hand).save(A + "cut/wave_hand.png")
frames = []
for ang in (-7, 0, 7):
    f = Image.fromarray(base); f.alpha_composite(Image.fromarray(hand).rotate(ang, Image.BICUBIC, center=PIVOT))
    bg = Image.new("RGBA", f.size, (60, 60, 70, 255)); bg.alpha_composite(f); frames.append(bg.crop((0, 40, 300, 300)).resize((450, 390)))
S = Image.new("RGB", (3 * 450, 390)); [S.paste(fr, (i * 450, 0)) for i, fr in enumerate(frames)]; S.save(A + "_wave_test.png"); print("ok")
