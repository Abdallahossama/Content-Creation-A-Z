from PIL import Image, ImageDraw, ImageFont
E = "D:/why habibi/2nd video/export/thumbnails/"
items = [("thumb_X_H_BEDTIME_STORY.png", "H bedtime story (LIVE now)"), ("thumb_X_I_NEW_LULLABY.png", "I new lullaby"), ("thumb_X_J_SPLIT_SILENCE.png", "J split silence")]
TW, TH = 480, 270; F = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
sheet = Image.new("RGB", (3 * (TW + 20) + 20, TH + 80), (15, 15, 15)); d = ImageDraw.Draw(sheet)
for k, (f, n) in enumerate(items):
    x = 20 + k * (TW + 20); y = 20
    im = Image.open(E + f).convert("RGB").resize((TW, TH), Image.LANCZOS)
    mk = Image.new("L", (TW, TH), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, TW - 1, TH - 1), 12, fill=255); sheet.paste(im, (x, y), mk)
    d.text((x, y + TH + 10), n, font=F, fill=(255, 194, 26) if k == 0 else (241, 241, 241))
out = E + "ab_test_candidates_sheet.png"; sheet.save(out); print(out)
