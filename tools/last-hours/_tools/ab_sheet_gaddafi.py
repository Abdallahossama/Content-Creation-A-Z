import sys
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]
items = [("B_AGENT_OF_AMERICA_upload.jpg", "1  MAIN", "Gaddafi's Basketball Court Gallows: 8 Hangings in 8 Days"),
         ("A_8_MEN_upload.jpg", "2", "The Engineer Gaddafi Hanged in a Basketball Stadium (1984)"),
         ("C_SHOW_TRIAL_upload.jpg", "3", "Gaddafi's 1984 Purge: 8 Men Hanged in Public in 8 Days")]
W, H, P = 640, 360, 20
big = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 34); small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
sheet = Image.new("RGB", (W * 3 + P * 4, H + 110), (22, 22, 22)); dr = ImageDraw.Draw(sheet)
for i, (f, tag, title) in enumerate(items):
    x = P + i * (W + P); im = Image.open(d + "/" + f).convert("RGB").resize((W, H), Image.LANCZOS); sheet.paste(im, (x, 20))
    if i == 0: dr.rectangle((x - 5, 15, x + W + 4, 20 + H + 4), outline=(255, 204, 0), width=5)
    dr.text((x, H + 32), tag, font=big, fill=(255, 204, 0) if i == 0 else (230, 230, 230)); dr.text((x, H + 75), title, font=small, fill=(210, 210, 210))
sheet.save(out, quality=92)
