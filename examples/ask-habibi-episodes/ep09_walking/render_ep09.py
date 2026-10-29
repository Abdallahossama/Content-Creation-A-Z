"""Ask Habibi Ep 9 "What Walking Every Day Does To Your Organs" — 16:9 long form on shortkit (paper background, no map) + longkit.
A walk clock (minute 1 -> years -> the number) stays on screen; organs are Gray's Anatomy plates (PD) turned into x-ray cards.
  python render_ep09.py qa t.. | anchors | allseg [n] | audio | final n"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep09_walking")
import shortkit as K
from shortkit import put, outlined, pill, popk, ease, font, YEL, SANS, IMPACT
import longkit as L
import ep09_draw as D
sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep07_ancient_fun"); from ep07_draw import stamp

ROOT = "D:/why habibi/9th video/"
K.setup(root=ROOT, vo="vo/ep09_vo_chatterbox.wav", size=(1920, 1080), cap_size=64, tail=21.5, out="Ask_Habibi_Ep09_What_Walking_Does_To_Your_Organs.mp4",
        cap_fix=[("GLUT4", "GLUT4")])
W, H = K.W, K.H
A = L.Anchors(); a = A.a
# ------------------------------------------------------------------ anchors
a("lab", "lab"); a("pedometer", "pedometer"); a("y1965", "1965"); a("inside", "inside"); a("lower", "lower"); a("habibi", "habibi"); a("advice", "advice")
a("minute1", "minute", 1, "advice"); a("muscles", "muscles"); a("insulin", "insulin"); a("x50", "50"); a("pumps", "pumps"); a("lymph", "lymph")
a("thigh", "thigh"); a("knees", "knees"); a("standing", "standing", 1, "knees"); a("lying", "lying")
a("minute10", "minute", 1, "lying"); a("brain", "brain"); a("stanford", "stanford"); a("stuck", "stuck")
a("ate", "ate"); a("diabetes", "diabetes"); a("dinner", "dinner"); a("older", "older"); a("tiny", "tiny"); a("stomach", "stomach"); a("brandy", "brandy")
a("stop", "stop"); a("spikes", "spikes"); a("threedays", "three", 1, "spikes")
a("sub_mid", "quick", 1, "threedays"); a("sub_word", "subscribe", 1, "sub_mid"); a("sub_more", "more", 1, "sub_mid")
a("weeks", "weeks"); a("population", "population"); a("immune", "immune", 1, "weeks"); a("colds", "colds"); a("p43", "43"); a("fat", "fat", 1, "p43"); a("scale", "scale")
a("year", "year", 1, "scale"); a("hippocampus", "hippocampus"); a("stretched", "stretched"); a("aging", "aging")
a("bigger", "bigger"); a("depression", "depression"); a("dementia", "dementia"); a("hip", "hip"); a("wear", "wear"); a("park", "park", 1, "wear")
a("shopping", "shopping"); a("links", "links", 1, "shopping"); a("pattern", "pattern")
a("number", "number", 1, "pattern"); a("y2025", "2025"); a("women", "women", 1, "y2025"); a("short", "short", 1, "women"); a("guidelines", "guidelines")
a("so_end", "so", 1, "guidelines"); a("drink", "drink"); a("lifts", "lifts"); a("relaxes", "relaxes"); a("sharper", "sharper"); a("name", "name", 1, "sharper")
a("start", "start", 1, "name"); a("subscribe", "subscribe", 1, "start")
A["endscreen"] = K.WORDS[-1]["e"] + 0.6
END = K.DUR
STAGE_T = [A["minute1"], A["minute10"], A["ate"] - 0.3, A["stop"] - 0.3, A["weeks"] - 0.6, A["year"] - 0.4, A["bigger"] - 0.6, A["number"] - 0.5]
CH = [("MINUTE 1", STAGE_T[0] - 0.3), ("MINUTE 10", STAGE_T[1] - 0.3), ("AFTER YOU EAT", STAGE_T[2]), ("WHEN YOU STOP", STAGE_T[3]), ("AFTER A FEW WEEKS", STAGE_T[4]),
      ("AFTER A YEAR", STAGE_T[5]), ("AFTER YEARS", STAGE_T[6]), ("THE NUMBER", STAGE_T[7]), ("SO...", A["so_end"] - 0.4)]
K.CFG["music"] = [("Easy Lemon.mp3", 0.0), ("Daily Beetle.mp3", A["ate"] - 1.0), ("Rising Tide.mp3", A["weeks"] - 1.5), ("Stay the Course.mp3", A["number"] - 1.0)]

# ------------------------------------------------------------------ background: fresh green/teal paper, tint per chapter
TINTS = [(206, 230, 206), (214, 232, 222), (232, 226, 200), (226, 214, 206), (210, 226, 236), (222, 216, 236), (214, 230, 214), (236, 226, 196), (220, 232, 214), (210, 228, 214)]
BG = {}
def bg(t):
    k = sum(1 for _, t0 in CH if t >= t0)
    if k not in BG:
        base = np.array(TINTS[k % len(TINTS)], np.float32); yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.45) / H) ** 2); BG[k] = K.papered(Image.fromarray((base * (1.05 - 0.45 * r[..., None])).clip(0, 255).astype(np.uint8)))
    return BG[k]
K.CFG["bgfn"] = bg

P9 = "D:/why habibi/_media/photos_ep09/"
def ph(n): return P9 + n if os.path.exists(P9 + n) and os.path.getsize(P9 + n) > 20000 else None
XR = {}
def xr(name, w, label):
    if (name, w) not in XR: XR[(name, w)] = D.xray_card(P9 + name, w, label)
    return XR[(name, w)]
def S(im, k): return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
ST = {k: stamp(k, 60, c) for k, c in (("NOT FROM A LAB", (210, 40, 40)), ("NO HELP", (210, 40, 40)), ("JUST 3 DAYS", (210, 40, 40)),
                                      ("LINKS, NOT GUARANTEES", (40, 90, 180)), ("SHORT WALKS COUNT", (30, 140, 60)), ("1-2 YEARS BACK", (30, 140, 60)))}
def card(c, img, t, t0, t1, x, y):
    if t0 <= t < t1: put(c, img, x, y, popk(t, t0) if t < t1 - 0.25 else ease((t1 - t) / 0.25))

# ------------------------------------------------------------------ the montage
def overlay(c, t, cam):
    # walk clock (top, after the hook)
    if STAGE_T[0] <= t < A["so_end"] - 0.4:
        k = sum(1 for s in STAGE_T if t >= s) - 1; put(c, D.walk_clock(k), W / 2 + 120, 62, 1.0)
    # ---- HOOK
    if t < A["pedometer"]:
        if ph("f9_feet.jpg"): L.photo(c, ph("f9_feet.jpg"), t, 0.0, x=560, y=560, w=760, rot=-2, credit="Pexels · MART Production")
        put(c, S(D.step_counter(min(10000, t / 2.2 * 10000)), 1.4), 1450, 470, popk(t, 0.2))
        if t >= A["lab"]: put(c, ST["NOT FROM A LAB"], 1450, 720, popk(t, A["lab"]))
    if A["pedometer"] <= t < A["inside"]:
        if ph("f9_pedometer.jpg"): L.photo(c, ph("f9_pedometer.jpg"), t, A["pedometer"], x=560, y=580, w=520, rot=-3, credit="a mechanical pedometer, ~1970 (similar) · Sarang, public domain")
        L.big(c, "1965: 'MANPO-KEI'", t, A["y1965"] - 0.4, x=1350, y=420, size=96)
        if t >= A["y1965"]: L.sub(c, "= '10,000-step meter', a Japanese pedometer's name · Lee et al. 2019", t, A["y1965"], y=820)
    if A["inside"] <= t < A["habibi"]:
        L.headline(c, "MINUTE BY MINUTE. ORGAN BY ORGAN.", t, A["inside"] + 0.4, size=84)
        for k, (f, lab) in enumerate((("f9_gray_heart.png", "HEART"), ("f9_gray_hippocampus.png", "BRAIN"), ("f9_gray_knee.png", "KNEE"))):
            put(c, xr(f, 300 if f != "f9_gray_knee.png" else 160, lab), 520 + k * 440, 600, popk(t, A["inside"] + 0.6 + k * 0.4))
        if t >= A["lower"]: put(c, pill("the real number is LOWER than 10,000", 48, YEL), W / 2, 880 - 70, popk(t, A["lower"]))
    if A["habibi"] <= t < STAGE_T[0] - 0.3:
        L.character(c, "host_cool", t, A["habibi"], 1560, h=500); L.headline(c, "I'M HABIBI, NOT YOUR DOCTOR", t, A["habibi"], size=84)
        L.sub(c, "these are studies, not medical advice", t, A["advice"] - 0.5, y=270)
    # ---- MINUTE 1
    if A["muscles"] <= t < A["pumps"]:
        if ph("f9_feet.jpg"): L.photo(c, ph("f9_feet.jpg"), t, A["muscles"], x=540, y=600, w=700, rot=-2, credit="Pexels · MART Production")
        L.big(c, "MUSCLES PULL SUGAR IN", t, A["muscles"] + 1.0, x=1340, y=330, size=80, sub="the 'GLUT4 door' opens without insulin · Sylow 2017", sub_y=410)
        if t >= A["x50"] - 0.3: L.big(c, "UP TO 50x", t, A["x50"] - 0.3, x=1340, y=600, size=130, sub="in HARD exercise; a walk is much gentler", sub_y=700)
    card(c, xr("f9_gray_lymph.png", 260, "LYMPH"), t, A["pumps"] + 1.0, A["knees"] - 0.2, 520, 580)
    if A["lymph"] <= t < A["knees"] - 0.2:
        L.big(c, "3-6x FASTER", t, A["thigh"] - 0.6, x=1300, y=420, size=120, sub="lymph flow with thigh-muscle contractions · Havas et al. 1997", sub_y=530)
        L.sub(c, "your lymph system has no heart of its own", t, A["lymph"] + 1.0, y=700, col=(255, 255, 255))
    card(c, xr("f9_gray_knee.png", 240, "KNEE"), t, A["knees"], STAGE_T[1] - 0.3, 420, 600)
    if A["standing"] <= t < STAGE_T[1] - 0.3:
        put(c, S(D.bars([("30 min standing", 5, 6, (230, 90, 70), "-5%"), ("10-min walk refills it", 3, 3.3, (90, 200, 110), "~3x faster")], w=900,
            u=ease((t - A["standing"]) / 1.0), title="knee cartilage, a small study · Kust et al. 2024"), 1.1), 1220, 560, popk(t, A["standing"]))
    # ---- MINUTE 10
    if A["brain"] <= t < A["stanford"] - 0.2:
        card(c, xr("f9_gray_hippocampus.png", 520, "BRAIN"), t, A["brain"], A["stanford"] - 0.2, 560, 600)
        L.big(c, "MOOD UP, FATIGUE DOWN", t, A["brain"] + 1.5, x=1340, y=420, size=78, sub="66 young adults, 10-min brisk walk · Edwards & Loprinzi 2018", sub_y=510)
    if A["stanford"] - 0.2 <= t < STAGE_T[2]:
        if ph("f9_park.jpg"): L.photo(c, ph("f9_park.jpg"), t, A["stanford"] - 0.2, x=560, y=600, w=700, rot=-2, credit="Pexels · Orkhan Sweden")
        L.big(c, "81%", t, A["stanford"] + 3.0, x=1360, y=420, size=200, sub="had more creative ideas walking · Oppezzo & Schwartz, Stanford 2014", sub_y=560)
        if t >= A["stuck"]: put(c, pill("stuck on a problem? take it for a walk", 44, YEL), 1360, 700, popk(t, A["stuck"]))
    # ---- AFTER A MEAL
    if A["ate"] - 0.3 <= t < A["stomach"] - 0.3:
        u = ease((t - A["diabetes"]) / 2.0)
        lab = "10-min walk after each meal: ~12% lower · Reynolds et al. 2016" if t < A["older"] else "3 x 15-min walks after meals = 1 x 45-min walk · DiPietro 2013"
        put(c, S(D.glucose(u, label=lab), 1.25), W / 2, 500, popk(t, A["ate"]))
        if t >= A["dinner"] and t < A["older"]: L.big(c, "~22% AFTER DINNER", t, A["dinner"], y=830, size=70)
        if t >= A["tiny"]: put(c, pill("even 2 minutes every 20 helps · Buffey et al. 2022", 44, YEL), W / 2, 880 - 60, popk(t, A["tiny"]))
    if A["stomach"] - 0.3 <= t < STAGE_T[3]:
        card(c, xr("f9_gray_stomach.png", 560, "STOMACH"), t, A["stomach"] - 0.3, STAGE_T[3], 560, 600)
        L.big(c, "EMPTIES FASTER", t, A["stomach"] + 1.5, x=1360, y=420, size=96, sub="half-emptying 123 -> 107 min, 10 men · Franke 2008", sub_y=520)
        if t >= A["brandy"]: put(c, ST["NO HELP"], 1360, 700, popk(t, A["brandy"] + 1.2)); L.sub(c, "brandy, liqueur, espresso:", t, A["brandy"], y=640, col=(255, 255, 255)) if t < A["brandy"] + 1.2 else None
    # ---- WHEN YOU STOP
    if STAGE_T[3] <= t < A["sub_mid"] - 0.2:
        if ph("f9_desk.jpg"): L.photo(c, ph("f9_desk.jpg"), t, A["stop"], x=560, y=600, w=720, rot=-2, credit="Pexels · Vitaly Gariev")
        n = 13000 - (13000 - 4300) * ease((t - A["stop"] - 4.0) / 2.5); put(c, S(D.step_counter(n), 1.4), 1380, 380, popk(t, A["stop"] + 1.0))
        if t >= A["spikes"]: L.big(c, "+42-97%", t, A["spikes"], x=1380, y=620, size=130); L.sub(c, "sugar spikes after meals · 12 young adults · Mikus 2012", t, A["spikes"] + 0.2, y=820)
        if t >= A["threedays"]: put(c, ST["JUST 3 DAYS"], 1380, 860 - 40, popk(t, A["threedays"]))
    L.subscribe_nudge(c, t, A["sub_mid"], A["sub_more"] + 1.4, x=1200, y=470, t_click=A["sub_word"])
    # ---- WEEKS
    if A["weeks"] <= t < A["immune"] - 0.2:
        card(c, xr("f9_gray_heart.png", 460, "HEART"), t, A["weeks"], A["immune"] - 0.2, 520, 600)
        put(c, S(D.bars([("blood pressure (top)", 3.7, 4, (230, 90, 70), "-3.7"), ("blood pressure (bottom)", 3.1, 4, (230, 140, 70), "-3.1"), ("resting heart rate", 2.9, 4, (90, 200, 110), "-2.9 bpm")],
            w=880, u=ease((t - A["weeks"] - 2.0) / 1.0), title="42 walking-group studies · Hanson & Jones 2015"), 1.05), 1380, 560, popk(t, A["weeks"] + 1.5))
        if t >= A["population"]: put(c, pill("small for you, big for a whole population", 42, YEL), 1380, 860 - 40, popk(t, A["population"]))
    if A["immune"] - 0.2 <= t < A["fat"] - 0.3:
        L.big(c, "COLDS: ~HALF AS LONG", t, A["immune"] + 0.5, y=300, size=100, sub="brisk walking 45 min x5/week · Nieman 1990", sub_y=400)
        if t >= A["p43"] - 0.3: L.big(c, "43% FEWER DAYS WITH COLDS", t, A["p43"] - 0.3, y=620, size=84, col=(120, 220, 140), sub="1,002 adults, aerobic exercise 5+ days/week · Nieman 2011", sub_y=710)
    if A["fat"] - 0.3 <= t < STAGE_T[5]:
        L.big(c, "-6% DEEP BELLY FAT", t, A["fat"], y=380, size=110, sub="even without weight loss · 117 studies, all exercise · Verheggen 2016", sub_y=490)
    # ---- YEAR
    if STAGE_T[5] <= t < STAGE_T[6]:
        card(c, xr("f9_gray_hippocampus.png", 560, "HIPPOCAMPUS"), t, STAGE_T[5] + 0.8, STAGE_T[6], 560, 600)
        put(c, S(D.bars([("walked 40 min, 3x/week", 2.0, 2.2, (90, 200, 110), "+2%"), ("only stretched", 1.4, 2.2, (230, 90, 70), "-1.4%")], w=860,
            u=ease((t - A["hippocampus"] - 1.0) / 1.0), title="120 older adults, 1 year · Erickson et al., PNAS 2011"), 1.05), 1380, 520, popk(t, A["hippocampus"]))
        if t >= A["aging"] - 1.2: put(c, ST["1-2 YEARS BACK"], 1380, 800, popk(t, A["aging"] - 1.2))
    # ---- YEARS
    if STAGE_T[6] <= t < A["park"] - 0.3:
        if ph("f9_park.jpg"): L.photo(c, ph("f9_park.jpg"), t, STAGE_T[6] + 0.3, x=520, y=620, w=640, rot=-2, credit="Pexels · Orkhan Sweden")
        rows = [("depression risk (~1.25 h/week)", 18, 60, (120, 170, 255), "-18%")]
        if t >= A["dementia"]: rows.append(("dementia risk (~9,800 steps/day)", 51, 60, (190, 130, 255), "-51%"))
        if t >= A["hip"]: rows.append(("hip fractures (4+ h/week, older women)", 41, 60, (255, 160, 60), "-41%"))
        put(c, S(D.bars(rows, w=900, u=1.0, title="LINKED TO (observational studies)"), 1.05), 1380, 520, popk(t, A["depression"] - 0.4))
        if t >= A["wear"]: put(c, pill("and walking doesn't wear out your knees (Lo et al. 2022)", 40, YEL), 1380, 860 - 40, popk(t, A["wear"]))
    if A["park"] - 0.3 <= t < A["number"] - 0.5:
        if t < A["links"] - 0.2:
            if ph("f9_leafy.jpg"): L.photo(c, ph("f9_leafy.jpg"), t, A["park"] - 0.3, x=520, y=560, w=640, rot=-3, credit="a park · Pexels / Felipe Balduino")
            if ph("f9_traffic.jpg") and t >= A["shopping"] - 0.3: L.photo(c, ph("f9_traffic.jpg"), t, A["shopping"] - 0.3, x=1400, y=560, w=640, rot=3, credit="a busy street · Pexels / Jimmy Liao")
            L.sub(c, "park walk: lungs better · busy street: mostly cancelled · Sinharay et al., Lancet 2018", t, A["park"], y=820)
        else:
            put(c, ST["LINKS, NOT GUARANTEES"], W / 2, 420, popk(t, A["links"] - 0.2))
            if t >= A["pattern"]: L.sub(c, "...but the pattern keeps showing up", t, A["pattern"], y=560)
    # ---- THE NUMBER
    if A["number"] - 0.5 <= t < A["y2025"] - 0.3:
        L.big(c, "WHERE THE BENEFIT LEVELS OFF", t, A["number"], y=230, size=84, sub="15 studies, 47,471 adults · Paluch et al., Lancet Public Health 2022", sub_y=320)
        put(c, S(D.bars([("60 and older", 7000, 10000, (90, 200, 110), "6-8K"), ("younger than 60", 9000, 10000, (120, 170, 255), "8-10K")], w=1000, u=ease((t - A["number"] - 1.5) / 1.0)), 1.1), W / 2, 600, popk(t, A["number"] + 1.0))
    if A["y2025"] - 0.3 <= t < A["short"] - 0.3:
        L.big(c, "7,000 vs 2,000 STEPS", t, A["y2025"] - 0.3, y=200, size=100, sub="57 studies · Ding et al., Lancet Public Health 2025", sub_y=300)
        done = sum(1 for tt in (A["y2025"] + 5.0, A["y2025"] + 8.5, A["y2025"] + 11.0) if t >= tt)
        put(c, S(D.checklist([("47% lower risk of dying early"), ("38% lower dementia risk"), ("28% fewer falls")], done) if hasattr(D, "checklist") else D.checkmark_list(["47% lower risk of dying early", "38% lower dementia risk", "28% fewer falls"], done), 1.1), 640, 620, popk(t, A["y2025"] + 2.0))
        if t >= A["women"]: put(c, pill("older women: ~4,400 steps -> 41% lower risk vs ~2,700 · Lee 2019", 38, YEL), W / 2, 820, popk(t, A["women"]))
    if A["short"] - 0.3 <= t < A["so_end"] - 0.4:
        if ph("f9_leafy.jpg"): L.photo(c, ph("f9_leafy.jpg"), t, A["short"] - 0.3, x=560, y=600, w=700, rot=-2, credit="Pexels · Felipe Balduino")
        put(c, ST["SHORT WALKS COUNT"], 1360, 460, popk(t, A["short"]))
        if t >= A["guidelines"]: L.sub(c, "US guidelines dropped the '10 minutes or it doesn't count' rule (2018)", t, A["guidelines"], y=830)
    # ---- END
    if A["so_end"] <= t < A["name"] - 0.3:
        items = ["muscles drink sugar", "lymph moves", "knees refill", "mood lifts", "ideas get better", "heart relaxes", "sharper brain, longer life (linked)"]
        done = sum(1 for tt in [A["drink"]] + [A["drink"] + 1.6 * k for k in range(1, 5)] + [A["relaxes"], A["sharper"]] if t >= tt)
        put(c, D.checkmark_list(items, done, w=900), W / 2 - 280, 560, popk(t, A["so_end"]))
        L.character(c, "host_cool", t, A["so_end"] + 0.5, 1560, h=500)
    if A["name"] - 0.3 <= t < A["subscribe"]:
        put(c, S(D.step_counter(10000 if t < A["name"] + 1.0 else 7000), 1.6), W / 2, 460, popk(t, A["name"]))
        if t >= A["name"] + 1.0: put(c, outlined("A GOOD PLACE TO START", 90, fill=YEL), W / 2, 720, popk(t, A["start"] - 0.6))
    if A["subscribe"] <= t < A["endscreen"]:
        L.character(c, "host_cool", t, A["subscribe"], 1560, h=520)
        put(c, pill("SUBSCRIBE · and maybe watch the next one standing up", 48, (255, 255, 255), (200, 30, 30, 240)), W / 2 - 160, 300, popk(t, A["subscribe"] + 0.3))
    L.end_screen(c, t, A["endscreen"], "keep walking?")
    L.chapter_card(c, t, CH)

SFX = [("pop", A[n] + 0.3, -20) for n in ("lab", "pedometer", "muscles", "x50", "pumps", "thigh", "knees", "standing", "brain", "stanford", "ate", "dinner",
                                          "tiny", "stomach", "brandy", "stop", "spikes", "threedays", "weeks", "immune", "p43", "fat", "hippocampus", "aging",
                                          "depression", "dementia", "hip", "park", "shopping", "links", "number", "y2025", "short", "name", "start")]
SFX += [("paper_slide", t0, -20) for _, t0 in CH]
SFX += [("pop", A["sub_word"] + 0.25, -18), ("paper_slide", A["endscreen"], -18), ("pop", A["endscreen"] + 2.3, -20)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END)
    else: K.main(sys.argv, overlay, SFX)
