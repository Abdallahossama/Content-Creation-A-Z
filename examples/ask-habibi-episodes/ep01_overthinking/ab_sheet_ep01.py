from PIL import Image, ImageDraw, ImageFont
E = "D:/why habibi/1st video/thumbnails/"
items = [("thumb_PHOTO_C_BRAIN_PLATE.png", "PHOTO C brain plate (LIVE now)"), ("thumb_PHOTO_D_PHONE_NIGHT.png", "PHOTO D phone at night"),
         ("thumb_MAP_A_RED_LOBE.png", "MAP A red lobe"), ("thumb_MAP_B_LAND.png", "MAP B land")]
TW, TH = 480, 270; F = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
sheet = Image.new("RGB", (2 * (TW + 20) + 20, 2 * (TH + 60) + 20), (15, 15, 15)); d = ImageDraw.Draw(sheet)
for k, (f, n) in enumerate(items):
    x = 20 + (k % 2) * (TW + 20); y = 20 + (k // 2) * (TH + 60)
    im = Image.open(E + f).convert("RGB"); print(f, im.size)
    im = im.resize((TW, TH), Image.LANCZOS)
    mk = Image.new("L", (TW, TH), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, TW - 1, TH - 1), 12, fill=255); sheet.paste(im, (x, y), mk)
    d.text((x, y + TH + 10), n, font=F, fill=(255, 194, 26) if k == 0 else (241, 241, 241))
out = E + "ab_test_candidates_sheet.png"; sheet.save(out); print(out)
