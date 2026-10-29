"""al-Khuld Hall (file 10) thumbnails, Hakawi colour style: ONE strong real image filling the frame + short text blocks + the date BIG.
Titles (A/B): 1 "Saddam Hussein Called a Meeting. 66 Names Were Read Out." + A, 2 "Saddam Hussein's 1979 Purge: 66 Names, One by One" + B,
3 "66 Names Were Read Out. 21 Men Were Gone in 17 Days." + C. The thumbnails never repeat the title's words.
Real images only: DoD photo of an empty palace hall (C4), Pexels still (smoke), Iraq's own list of the 21 executed (FBIS, 9 Aug 1979) on a palace room (C3), USAF photo of Saddam in court, 1 Jul 2004 (B7) and DoD photo after
his capture, Dec 2003 (B5) (the years are said in the description). No footage of the 1979 meeting (copyright). Men only.
  uv run --no-project --with pillow --with numpy python thumbs_khuld.py"""
import sys, os
from PIL import Image
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, tint, vign, block, paste_faded, TW, TH, YEL, WHITE, RED
EP = "11_khuld_hall"; OUT = "D:/why habibi/_newchannel/11_khuld_hall/export/thumbnails/"
Image.MAX_IMAGE_PIXELS = None

def saddam(h, k=0.3):
    m = src(EP, "B7_"); m = m.crop((int(m.width * 0.10), int(m.height * 0.34), int(m.width * 0.44), int(m.height * 0.88)))
    m = tint(m, col=(150, 120, 100), k=k, contrast=1.2); s = h / m.height; return m.resize((int(m.width * s), h), Image.LANCZOS)

def A():   # an empty Saddam-era palace hall (DoD, Apr 2003) + Saddam ghosted on the right: WHO'S NEXT?
    c = grade(cover(src(EP, "C4_"), TW, TH, cx=0.42, cy=0.5, z=1.0), sat=1.25, contrast=1.12, teal=0.08, warm=0.14); c = vign(c, 0.5).convert("RGBA")
    m = saddam(700); paste_faded(c, m, TW - m.width + 40, 20, left=300, bottom=220, top=60)
    block(c, "WHO'S", 34, 96, 132)
    block(c, "NEXT?", 34, 248, 132, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "22 JULY 1979", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c
def B():   # Saddam (DoD, Dec 2003) + Iraq's own list of the 21 executed (FBIS, 9 Aug 1979), red marker through the names, palace room: HIS OWN MEN
    from PIL import ImageDraw
    sys.path.insert(0, "D:/why habibi/_newchannel"); import lastkit as LK
    c = grade(cover(src(EP, "C3_"), TW, TH, cx=0.5, cy=0.45, z=1.05), sat=1.3, contrast=1.1, teal=0.05, warm=0.18); c = vign(c, 0.55).convert("RGBA")
    pg = src(EP, "A6_"); W0, H0 = pg.size; y0 = int(H0 * 0.255)
    m = pg.crop((int(W0 * 0.08), y0, int(W0 * 0.93), int(H0 * 0.392))).convert("RGB")
    d = ImageDraw.Draw(m)
    for yy in (1127, 1180, 1232, 1285, 1338, 1390, 1443, 1495):          # one stroke per line of names (all 21 were shot)
        y = yy - y0; d.line((m.width * 0.02, y + 6, m.width * 0.98, y - 4), fill=(200, 20, 20), width=14)
    from PIL import ImageEnhance
    f = src(EP, "B4_"); f = f.crop((int(f.width * 0.02), int(f.height * 0.03), int(f.width * 0.99), int(f.height * 0.74)))   # Saddam after his capture (DoD, Dec 2003)
    f = grade(f, sat=1.1, contrast=1.18, teal=0.02, warm=0.06); f = ImageEnhance.Brightness(f).enhance(1.08)
    k = TH / f.height; f = f.resize((int(f.width * k), TH), Image.LANCZOS)
    paste_faded(c, f, TW - f.width + 10, 0, left=120)
    card = LK.print_card(m, 500, border=12, rot=-4)                                   # the list sits left, under the text, off his face
    c.alpha_composite(card, (18, 318))
    block(c, "HIS OWN", 34, 96, 132)
    block(c, "MEN.", 34, 248, 132, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "22 JULY 1979", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c
def C():   # Saddam's face after his capture (DoD, Dec 2003) large on the right, smoke on the left: HE CRIED.
    c = grade(cover(src(EP, "ZE6"), TW, TH, cx=0.5, cy=0.5, z=1.0), sat=1.1, contrast=1.2, teal=0.06, warm=0.10); c = vign(c, 0.45).convert("RGBA")
    m = src(EP, "B5_"); m = m.crop((0, int(m.height * 0.05), m.width, int(m.height * 0.80)))
    m = tint(m, col=(150, 120, 100), k=0.12, contrast=1.15); s = 760 / m.height; m = m.resize((int(m.width * s), 760), Image.LANCZOS)
    paste_faded(c, m, TW - m.width + 30, -20, left=240, bottom=140)
    block(c, "HE", 34, 110, 150)
    block(c, "CRIED.", 34, 276, 150, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "22 JULY 1979", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); tiles = []
    for name, fn in (("A_WHOS_NEXT", A), ("B_HIS_OWN_MEN", B), ("C_HE_CRIED", C)):
        im = fn().convert("RGB"); im.save(OUT + name + ".png"); im.save(OUT + name + "_upload.jpg", quality=90); tiles.append(im)
    S = Image.new("RGB", (TW * 3 // 2 + 20, TH + TH // 2 + 20), (25, 25, 25))
    S.paste(tiles[0], (0, 0)); S.paste(tiles[1].resize((TW // 2, TH // 2)), (TW + 20, 0)); S.paste(tiles[2].resize((TW // 2, TH // 2)), (TW + 20, TH // 2 + 20))
    S.paste(tiles[0].resize((TW // 3, TH // 3)), (0, TH + 20)); S.paste(tiles[1].resize((TW // 3, TH // 3)), (TW // 3 + 10, TH + 20)); S.paste(tiles[2].resize((TW // 3, TH // 3)), (2 * TW // 3 + 20, TH + 20))
    S.save(OUT + "_sheet.png"); print(OUT + "_sheet.png")
