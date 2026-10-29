"""Builds the Ask Habibi potato cast pack (brand asset): every character as a transparent PNG + one cast sheet.
-> _style_kit/brand/potato_cast/<name>.png (900 px tall body) and _cast_sheet.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from potato_cast import cast

OUT = "D:/why habibi/_style_kit/brand/potato_cast/"; os.makedirs(OUT, exist_ok=True)
CAST = [  # name, skin, face, outfit, headwear, extra, flip, lean, label
    ("host", "russet", "confident", "suit", "none", "none", False, 0, "the host"),
    ("host_cool", "russet", "cool", "suit", "none", "none", False, 0, "host, cool"),
    ("gulf_shemagh", "russet", "fine", "thobe", "shemagh", "none", False, 0, "thobe + shemagh"),
    ("gulf_ghutra", "pale", "confident", "thobe", "ghutra", "none", True, 0, "thobe + ghutra"),
    ("egyptian_galabeya", "gold", "fine", "galabeya", "taqiyah", "none", False, 0, "galabeya + taqiyah"),
    ("ship_captain", "russet", "shocked", "suit", "captain", "none", True, 0, "ship captain"),
    ("pilot", "pale", "smug", "pilot", "pilot", "aviators", False, 0, "pilot"),
    ("oil_worker", "red", "panic", "hivis", "hardhat", "none", False, 0, "oil worker"),
    ("doctor", "pale", "deadpan", "doctor", "none", "none", True, 0, "doctor"),
    ("scientist", "gold", "shocked", "labcoat", "none", "none", False, 0, "scientist"),
    ("sleepy", "russet", "sleepy", "pajamas", "nightcap", "none", False, -3, "can't sleep"),
    ("general", "gold", "smug", "general", "bicorne", "none", True, 0, "history general"),
    ("student", "red", "sideeye", "hoodie", "none", "none", False, 0, "student"),
    ("diplomat", "pale", "sideeye", "suit", "none", "none", True, 0, "diplomat"),
    ("viewer", "russet", "sad", "none", "none", "none", False, 2, "the viewer"),
    ("ice_age_naked", "russet", "panic", "none", "none", "none", False, 0, "naked (no clothes)"),
    ("ice_age_cape", "gold", "deadpan", "fur_cape", "none", "none", True, 0, "draped fur cape"),
    ("ice_age_parka", "red", "fine", "fur_parka", "none", "none", False, 0, "sewn fur parka"),
]
if __name__ == "__main__":
    only = sys.argv[1:]
    sheet = Image.new("RGBA", (8 * 300 + 40, 2 * 560 + 40), (222, 204, 160, 255)); F = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 30)
    for k, (name, sk, face, outfit, head, extra, flip, lean, label) in enumerate(CAST):
        if only and name not in only: continue
        big = cast(sk, face, outfit, head, extra, height=900, flip=flip, lean=lean); big.save(OUT + f"{name}.png")
        p = cast(sk, face, outfit, head, extra, height=330, flip=flip, lean=lean)
        x = 20 + (k % 8) * 300; y = 20 + (k // 8) * 560
        sheet.alpha_composite(p, (x + (300 - p.width) // 2, y + 480 - p.height))
        ImageDraw.Draw(sheet).text((x + 150, y + 515), label, font=F, fill=(60, 44, 26, 255), anchor="mm"); print(name)
    sheet.convert("RGB").save(OUT + "_cast_sheet.png"); print(OUT + "_cast_sheet.png")
