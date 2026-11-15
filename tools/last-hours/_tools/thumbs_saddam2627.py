"""Files 26 (capture, 13 Dec 2003) + 27 (last day, 30 Dec 2006) thumbnails in the CURRENT channel style (owner 14 Nov: keep the
channel's look; file 11's WHO'S NEXT? = model): one real colour image filling the frame, Saddam ghosted / big on the right,
1-3 words on black + yellow blocks, the date on a red tab. Real DoD / US Army photos only. No execution image, no women.
Preview only: never uploaded until the owner approves.
  uv run --no-project --with pillow --with numpy python thumbs_saddam2627.py"""
import sys, os
from PIL import Image, ImageDraw, ImageEnhance
sys.path.insert(0, "D:/why habibi/_newchannel")
from thumbs_hakawi import src, cover, grade, tint, vign, block, ellipse, card, paste_faded, TW, TH, YEL, WHITE, RED
Image.MAX_IMAGE_PIXELS = None
NC = "D:/why habibi/_newchannel/"; E26, E27 = "26_saddam_capture", "27_saddam_last_day"

def face(ep, key, box, h, colour=True):
    m = src(ep, key); W0, H0 = m.size; m = m.crop((int(W0 * box[0]), int(H0 * box[1]), int(W0 * box[2]), int(H0 * box[3])))
    m = ImageEnhance.Contrast(m).enhance(1.15).convert("RGBA") if colour else tint(m, col=(150, 120, 100), k=0.3, contrast=1.2)
    s = h / m.height; return m.resize((int(m.width * s), h), Image.LANCZOS)

def left_dark(c, w=900, k=210):
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x in range(w): d.line((x, 0, x, TH), fill=(0, 0, 0, int(k * (1 - x / w) ** 1.3)))
    c.alpha_composite(lay); return c

# ---------------------------------------------------------------- FILE 26
def c26_A():   # the lid over the hole (US Army, 17 Dec 2003), red ring on the foam block: HE WAS / UNDER HERE.
    c = grade(cover(src(E26, "B1_"), TW, TH, cx=0.55, cy=0.55, z=1.0), sat=1.2, contrast=1.15, teal=0.06, warm=0.12); c = vign(c, 0.5).convert("RGBA")
    c = left_dark(c, 760, 190)
    ellipse(c, (720, 330, 1110, 700), width=13)
    block(c, "HE WAS", 34, 96, 120)
    block(c, "UNDER HERE.", 34, 240, 120, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "13 DEC 2003", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

def c26_B():   # the hut's kitchen (US Army) + his face just after capture (DoD), big on the right: HIS FIRST / WORDS?
    c = grade(cover(src(E26, "B2_"), TW, TH, cx=0.45, cy=0.5, z=1.05), sat=1.15, contrast=1.1, teal=0.06, warm=0.14)
    c = ImageEnhance.Brightness(c).enhance(0.7).convert("RGBA"); c = vign(c, 0.5).convert("RGBA")
    f = face(E26, "B3_", (0.0, 0.0, 1.0, 0.92), 760); paste_faded(c, f, TW - f.width + 60, -20, left=260, bottom=120)
    c = left_dark(c, 700, 200)
    block(c, "HIS FIRST", 34, 110, 128)
    block(c, "WORDS?", 34, 270, 128, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "13 DEC 2003", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

def c26_C():   # the most-wanted deck's ace (DoD) on the hut kitchen + the face after capture: THE ACE / IN A HOLE.
    c = grade(cover(src(E26, "B2_"), TW, TH, cx=0.4, cy=0.5, z=1.1), sat=1.1, contrast=1.1, teal=0.1, warm=0.05)
    c = ImageEnhance.Brightness(c).enhance(0.55).convert("RGBA")
    f = face(E26, "B3_", (0.0, 0.0, 1.0, 0.92), 760); paste_faded(c, f, TW - f.width + 60, -20, left=260, bottom=120)
    ace = src(E26, "B10_"); W0, H0 = ace.size; ace = ace.crop((int(W0 * 0.27), int(H0 * 0.07), int(W0 * 0.76), int(H0 * 0.92)))
    k = card(ace, 300, rot=-7); c.alpha_composite(k, (420, 300))
    block(c, "THE ACE", 34, 110, 128)
    block(c, "IN A HOLE.", 34, 270, 128, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "13 DEC 2003", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

# ---------------------------------------------------------------- FILE 27
def c27_A():   # a Black Hawk over Baghdad at sunset (US Army) + his face at the 2004 hearing (DoD), ghosted: HIS LAST / MORNING.
    c = grade(cover(src(E27, "C8_"), TW, TH, cx=0.5, cy=0.5, z=1.0), sat=1.25, contrast=1.12, teal=0.05, warm=0.12); c = vign(c, 0.45).convert("RGBA")
    f = face(E27, "B1_", (0.0, 0.0, 1.0, 0.75), 720, colour=False); paste_faded(c, f, TW - f.width + 40, 20, left=300, bottom=200, top=60)
    block(c, "HIS LAST", 34, 96, 132)
    block(c, "MORNING.", 34, 248, 132, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "30 DEC 2006", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

def c27_B():   # Kadhimiya from the air (DoD), dark + his face big: 1:30 AM / THE PHONES RANG
    k13 = src(E27, "C13_"); k13 = k13.crop((0, 0, k13.width, int(k13.height * 0.55)))   # city + domes only: never the pilgrims on the bridge
    c = grade(cover(k13, TW, TH, cx=0.5, cy=0.5, z=1.0), sat=0.9, contrast=1.15, teal=0.18, warm=0.0)
    c = ImageEnhance.Brightness(c).enhance(0.5).convert("RGBA")
    f = face(E27, "B1_", (0.0, 0.0, 1.0, 0.78), 760); paste_faded(c, f, TW - f.width + 40, -10, left=280, bottom=140)
    c = left_dark(c, 720, 200)
    block(c, "1:30 AM", 34, 120, 150, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "THE PHONES RANG", 34, 290, 76)
    block(c, "30 DEC 2006", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

def c27_C():   # an empty palace dining room, Baghdad (DoD, 2003; the C25 mural is CC BY-SA: never in thumbnails) + the shaved face (DoD): HIS LAST / NIGHT.
    c = grade(cover(src(E27, "R16_"), TW, TH, cx=0.42, cy=0.5, z=1.0), sat=1.2, contrast=1.12, teal=0.05, warm=0.12)
    c = ImageEnhance.Brightness(c).enhance(0.8).convert("RGBA"); c = vign(c, 0.5).convert("RGBA")
    f = face(E27, "B5_", (0.0, 0.0, 1.0, 1.0), 720); paste_faded(c, f, TW - f.width + 20, 0, left=240, bottom=100)
    c = left_dark(c, 720, 190)
    block(c, "HIS LAST", 34, 110, 128)
    block(c, "NIGHT.", 34, 270, 128, fill=(0, 0, 0), bg=YEL + (255,))
    block(c, "30 DEC 2006", 34, 662, 58, fill=WHITE, bg=RED + (255,))
    return c

if __name__ == "__main__":
    for ep, sets in ((E26, (("A_UNDER_HERE", c26_A), ("B_FIRST_WORDS", c26_B), ("C_ACE_IN_A_HOLE", c26_C))),
                     (E27, (("A_LAST_MORNING", c27_A), ("B_PHONES_RANG", c27_B), ("C_LAST_NIGHT", c27_C)))):
        out = NC + ep + "/export/thumbnails/"; os.makedirs(out, exist_ok=True); tiles = []
        for name, fn in sets:
            im = fn().convert("RGB"); im.save(out + name + ".png"); im.save(out + name + "_upload.jpg", quality=90); tiles.append(im)
        S = Image.new("RGB", (3 * TW // 2 + 40, TH // 2 + TH // 4 + 40), (25, 25, 25))
        for i, t in enumerate(tiles):
            S.paste(t.resize((TW // 2, TH // 2)), (i * (TW // 2 + 20), 0)); S.paste(t.resize((TW // 4, TH // 4)), (i * (TW // 2 + 20), TH // 2 + 20))
        S.save(out + "_sheet.jpg", quality=88); print(out + "_sheet.jpg")
