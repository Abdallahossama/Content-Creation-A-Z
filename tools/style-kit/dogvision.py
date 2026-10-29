"""'How your dog sees it' filter for real photos: dog colour vision (2 cone types, blue + yellow; simulated like human
deuteranopia with the Viénot/Brettel 1999 LMS method) + lower sharpness (~20/75 -> blur) + optional slightly brighter shadows.
    from dogvision import dog_view, split_view
    dog_view(img, blur=4.0)                    # PIL RGB -> PIL RGB
    split_view(img, x_frac=0.5, label=True)    # left: you, right: your dog
Sources for the on-screen claims: Neitz, Geist & Jacobs 1989 (dichromats); Miller 2001 (~20/75); Lind et al. 2017 (acuity)."""
import numpy as np
from PIL import Image, ImageFilter

_RGB2LMS = np.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
_LMS2RGB = np.linalg.inv(_RGB2LMS)
_DEUT = np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])        # M cone replaced from L and S

def _lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def _srgb(a): return np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(np.clip(a, 0, None), 1 / 2.4) - 0.055)

def dog_colors(img):
    a = _lin(np.asarray(img.convert("RGB"), np.float32) / 255)
    m = _LMS2RGB @ _DEUT @ _RGB2LMS; b = a @ m.T
    return Image.fromarray((np.clip(_srgb(np.clip(b, 0, 1)), 0, 1) * 255).astype(np.uint8))

def dog_view(img, blur=4.0, lift=0.06):
    out = dog_colors(img)
    if blur: out = out.filter(ImageFilter.GaussianBlur(blur))
    if lift:
        a = np.asarray(out, np.float32) / 255; a = a + lift * (1 - a) * (1 - a); out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return out

def split_view(img, x_frac=0.5, blur=4.0):
    img = img.convert("RGB"); d = dog_view(img, blur); x = int(img.width * x_frac)
    out = img.copy(); out.paste(d.crop((x, 0, img.width, img.height)), (x, 0)); return out
