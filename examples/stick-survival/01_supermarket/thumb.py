import sys; sys.path.insert(0, "F:/stick-survival/tools")
from stickkit import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
O = "F:/stick-survival/videos/01_supermarket/export/"
L = render(dict(bg="aisle", actors=[Actor("me", 900, act="cheer", face="happy", s=1.55)], props=[dict(kind="cart", x=1260, y=905, s=1.2)], vig=0.2), 1, 2)
R = render(dict(bg="aisle", bgargs=dict(empty=0.85), actors=[Actor("zombie", 1330, act="zwalk", f=-1, s=1.35), Actor("zombie2", 600, act="zwalk", f=1, s=1.25, z=-1), Actor("me", 980, act="scared", face="scared", s=1.55, baggy=1.6, z=1)],
            dark=0.5, vig=0.6), 1, 2)
def fit(im): return im.convert("RGB").crop((480, 0, 1440, 1080)).resize((640, 720))
T = Image.new("RGB", (1280, 720)); T.paste(fit(L), (0, 0)); T.paste(ImageEnhance.Color(fit(R)).enhance(0.8), (640, 0))
d = ImageDraw.Draw(T); d.rectangle((634, 0, 646, 720), fill=(255, 255, 255))
f = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 120)
for txt, x, col in (("DAY 1", 320, (255, 255, 255)), ("DAY 30", 960, (255, 70, 50))):
    d.text((x, 90), txt, font=f, fill=col, anchor="mm", stroke_width=12, stroke_fill=(0, 0, 0))
T.save(O + "thumb_A_day1_day30.png"); T.save(O + "thumb_A_day1_day30_upload.jpg", quality=90); T.resize((320, 180)).save(O + "thumb_A_small.png"); print("ok")
