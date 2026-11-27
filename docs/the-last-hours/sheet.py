"""Review sheet: current thumbnail + title + lifetime numbers vs the new Noah thumbnail + 2 new titles (27 Nov 2026).
  uv run --no-project --with pillow python sheet.py"""
from PIL import Image, ImageDraw, ImageFont
D = "D:/why habibi/_newchannel/_rethumb_nov27/"
COND = "C:/Windows/Fonts/FRAMDCN.TTF"
ROWS = [
 ("alcatraz", "What the FBI Found When 3 Men Vanished From Alcatraz", "2,473 impr · CTR 3.0% · 56% watched",
  ["3 Men Escaped Alcatraz With Spoons. The FBI Never Found Them.", "They Left Fake Heads in Their Beds. 3 Men Were Never Found."]),
 ("roanoke", "115 People Vanished From Roanoke. One Word Was Left.", "2,751 impr · CTR 1.6% (lowest) · 36% watched",
  ["115 Colonists Vanished. The Only Clue Was One Word Carved on a Post.", "The Lost Colony of Roanoke: 115 People Gone, 1 Word Left."]),
 ("franklin", "129 Men Vanished in the Arctic. This Is Their Last Note.", "2,265 impr · CTR 2.2% · 60% watched",
  ["129 Men Sailed Into the Arctic. None Came Back. 1 Note Was Found.", "The Franklin Expedition: 2 Ships, 129 Men, 0 Survivors."]),
 ("cooper", "D.B. Cooper Jumped at 8:10 PM. Here's Every Hour Before It.", "3,177 impr · CTR 2.7% · 46% watched",
  ["D.B. Cooper Jumped With $200,000. 9 Years Later, a Kid Found $5,800.", "He Hijacked a Plane, Took $200,000 and Jumped. Nobody Knows Who He Was."]),
 ("andree", "3 Men Vanished in a Balloon. Their Film Waited 33 Years.", "684 impr · CTR 3.1% · 43% watched",
  ["3 Men Flew a Balloon to the North Pole. Their Film Was Found 33 Years Later.", "They Tried to Fly Over the North Pole in 1897. Their Photos Came Back in 1930."]),
 ("flight19", "14 Men Vanished Off Florida. Their Last Call Got No Answer.", "398 impr · CTR 2.5% · 29% watched",
  ["5 Navy Bombers Vanished. This Is How the Bermuda Triangle Began.", "Flight 19: 5 Planes, 14 Men, Gone. The Navy Knew Where They Were."]),
 ("gaddafi_bb", "Gaddafi's Basketball Court Gallows: 8 Hangings in 8 Days", "296 impr · CTR 4.4% · 22% watched",
  ["Gaddafi Hanged 8 Men in 8 Days. Libya Watched It on TV.", "Students Were Bussed In to Watch a 'Trial'. Gaddafi Turned It Into Gallows."]),
 ("gaddafi_last", "Gaddafi's Last Convoy Left at 8 AM. By 11 He Was Captured.", "137 impr · CTR 6.6% · 36% watched",
  ["Gaddafi's Last Morning: 50 Cars, 2 Drain Pipes, 3 Hours.", "NATO Hit Gaddafi's Convoy at 8:30. By 11, He Was Caught by a Drain Pipe."]),
 ("brotherhood", "The Muslim Brotherhood, From 1928 to the Michigan Race", "243 impr · CTR 1.7% · 56% watched",
  ["Hassan al-Banna Was Shot in a Cairo Street. The Car Was Rented for a Police Chief.", "Who Shot the Founder of the Muslim Brotherhood? The Record, Hour by Hour."]),
]
CUR = {"gaddafi_last": "D:/why habibi/_newchannel/17_gaddafi_last_day/export/thumbnails/A_KING_OF_KINGS_COLOR_upload.jpg"}
TW, TH = 480, 270
S = Image.new("RGB", (40 + TW * 2 + 60 + 720, 70 + len(ROWS) * (TH + 40)), (24, 24, 26)); d = ImageDraw.Draw(S)
f1, f2, f3 = ImageFont.truetype(COND, 26), ImageFont.truetype(COND, 22), ImageFont.truetype(COND, 20)
d.text((20, 18), "NOW (title + thumbnail + lifetime numbers)", font=f1, fill=(170, 170, 170)); d.text((40 + TW + 30, 18), "NEW: Noah thumbnail + 2 title options", font=f1, fill=(255, 214, 64))
for i, (k, cur, num, new) in enumerate(ROWS):
    y = 60 + i * (TH + 40)
    S.paste(Image.open(CUR.get(k, D + f"cur/{k}.jpg")).convert("RGB").resize((TW, TH)), (20, y))
    S.paste(Image.open(D + f"out/{k}_N.jpg").convert("RGB").resize((TW, TH)), (40 + TW + 30, y))
    x = 40 + TW * 2 + 60
    d.text((x, y + 4), "NOW: " + cur, font=f2, fill=(200, 200, 200)); d.text((x, y + 34), num, font=f3, fill=(255, 120, 110))
    for j, t in enumerate(new):
        d.text((x, y + 90 + j * 60), f"T{j + 1}: ", font=f2, fill=(255, 214, 64)); d.text((x + 40, y + 90 + j * 60), t, font=f2, fill=(240, 240, 240))
    sm = Image.open(D + f"out/{k}_N.jpg").convert("RGB").resize((320, 180)); S.paste(sm.resize((176, 99)), (x, y + TH - 99))
    d.text((x + 186, y + TH - 30), "phone size", font=f3, fill=(120, 120, 120))
S.save(D + "REPACKAGE_SHEET_27nov.jpg", quality=86); print(D + "REPACKAGE_SHEET_27nov.jpg")
