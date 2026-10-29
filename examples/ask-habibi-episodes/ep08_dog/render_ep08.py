"""Ask Habibi Ep 8 "How Your Dog Really Sees You" — 16:9 long form on shortkit (no map: paper background) + longkit.
Real dog photos (Pexels) with a live 'how your dog sees it' wipe (dogvision.py), drawings (ep08_draw.py), 3D potato dog stickers.
  python render_ep08.py qa t.. | anchors | allseg [n] | audio | final n"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep08_dog")
import shortkit as K
from shortkit import put, outlined, pill, popk, ease, font, YEL, SANS, IMPACT
import longkit as L
import ep08_draw as D
import dogvision as DV
sys.path.insert(0, "D:/why habibi/_pipeline/episodes/ep07_ancient_fun"); from ep07_draw import stamp

ROOT = "D:/why habibi/8th video/"
K.setup(root=ROOT, vo="vo/ep08_vo_chatterbox.wav", size=(1920, 1080), cap_size=64, tail=21.5, out="Ask_Habibi_Ep08_How_Your_Dog_Sees_You.mp4")
W, H = K.W, K.H
A = L.Anchors(); a = A.a
# ------------------------------------------------------------------ anchors
a("scanner", "scanner"); a("didnt", "didn't"); a("stares", "stares"); a("blurry", "blurry"); a("smelly", "smelly"); a("recognizes", "recognizes")
a("habibi", "habibi"); a("eyes", "eyes")
a("colors", "colors"); a("three", "three"); a("two", "two"); a("blues", "blues"); a("black", "black"); a("test", "test"); a("reds", "reds")
a("toy", "toy"); a("dumb", "dumb"); a("sharpness", "sharpness"); a("vets", "vets"); a("detail", "detail"); a("park", "park"); a("moving", "moving")
a("police", "police"); a("motion", "motion"); a("flicker", "flicker"); a("wider", "wider"); a("dim", "dim"); a("shine", "shine")
a("face2", "face", 1, "shine"); a("inner", "inner"); a("happy", "happy"); a("never", "never", 1, "happy"); a("right", "right", 1, "never")
a("brain2", "brain", 1, "right"); a("cared", "cared"); a("matters", "matters")
a("smell", "smell", 1, "matters"); a("m300", "300"); a("genes", "genes"); a("broken", "broken"); a("trillion", "trillion"); a("horowitz", "horowitz")
a("fades", "fades"); a("tested", "tested"); a("greeted", "greeted"); a("brain3", "brain", 1, "greeted"); a("feeling", "feeling"); a("stressed", "stressed")
a("sub_mid", "quick"); a("sub_word", "subscribe", 1, "sub_mid"); a("sub_more", "more", 1, "sub_mid")
a("voice", "voice", 1, "sub_more"); a("happy2", "happy", 1, "voice"); a("tones", "tones"); a("left", "left"); a("flat", "flat"); a("y2024", "2024")
a("match", "match"); a("stand", "stand")
a("bond", "bond"); a("eyebrows", "eyebrows"); a("five", "five", 1, "eyebrows"); a("shelter", "shelter"); a("adopted", "adopted"); a("evolve", "evolve")
a("oxytocin", "oxytocin"); a("questioned", "questioned"); a("toddlers", "toddlers"); a("puzzle", "puzzle"); a("stranger", "stranger"); a("n13", "13")
a("food", "food"); a("alpha", "alpha"); a("y1970", "1970"); a("wild", "wild"); a("parents", "parents"); a("print", "print"); a("boss", "boss"); a("safe", "safe")
a("really", "really", 1, "safe"); a("shape", "shape"); a("smell_end", "smell", 1, "shape"); a("voice_end", "voice", 1, "smell_end"); a("home", "home")
a("tears", "tears"); a("withyou", "with", 2, "tears"); a("subscribe", "subscribe", 1, "tears")
A["endscreen"] = K.WORDS[-1]["e"] + 0.6
END = K.DUR
CH = [("WHAT YOUR DOG SEES", A["colors"] - 0.5), ("YOUR FACE", A["face2"] - 0.8), ("YOUR SMELL", A["smell"] - 0.8), ("YOUR VOICE", A["voice"] - 0.6),
      ("THE BOND", A["bond"] - 0.6), ("ARE YOU THE ALPHA?", A["alpha"] - 0.5), ("SO... HOW DOES YOUR DOG SEE YOU?", A["really"] - 1.2)]
K.CFG["music"] = [("Easy Lemon.mp3", 0.0), ("Daily Beetle.mp3", A["smell"] - 1.0), ("Vibing Over Venus.mp3", A["bond"] - 1.0), ("Dream Culture.mp3", A["really"] - 1.5)]

# ------------------------------------------------------------------ background: warm paper, a different tint per chapter
TINTS = [(236, 214, 178), (214, 226, 236), (236, 220, 206), (226, 236, 214), (238, 214, 214), (222, 216, 238), (232, 222, 196), (226, 214, 236)]
BG = {}
def bg(t):
    k = sum(1 for _, t0 in CH if t >= t0)
    if k not in BG:
        base = np.array(TINTS[k % len(TINTS)], np.float32); yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.45) / H) ** 2); im = base * (1.05 - 0.45 * r[..., None])
        BG[k] = K.papered(Image.fromarray(im.clip(0, 255).astype(np.uint8)))
    return BG[k]
K.CFG["bgfn"] = bg

# ------------------------------------------------------------------ photos + dog-vision splits
P8 = "D:/why habibi/_media/photos_ep08/"; CUT = "D:/why habibi/_media/cutouts/"
def ph(n): return P8 + n if os.path.exists(P8 + n) and os.path.getsize(P8 + n) > 50000 else None
def dogpng(face): return None          # the 3D potato dog is retired (user: real things only, no cartoons)
PC = {}
def pcard(name, w, rot=0):
    if not ph(name): return None
    if (name, w, rot) not in PC:
        iw, ih = Image.open(ph(name)).size; w2 = min(w, int(500 * iw / ih))          # cap the card height (portrait photos)
        PC[(name, w, rot)] = L._photo_card(ph(name), w2, rot, None)
    return PC[(name, w, rot)]
def real(c, name, t, t0, x, y, w, rot=0, t1=None):
    if t >= t0 and (t1 is None or t < t1) and pcard(name, w, rot):
        im = pcard(name, w, rot); y = min(y, 870 - im.height / 2); put(c, im, x, y, popk(t, t0))          # keep clear of the caption band
SPL = {}
def split_frame(name, w, h, frac, blur=4.0):
    """photo `name` cropped to w x h; right of frac shows the dog view (cached), with a white wipe line + labels"""
    if name not in SPL:
        im = Image.open(P8 + name).convert("RGB"); s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        x0, y0 = (im.width - w) // 2, (im.height - h) // 2; im = im.crop((x0, y0, x0 + w, y0 + h)); SPL[name] = (im, DV.dog_view(im, blur))
    a_, b_ = SPL[name]; x = int(w * frac); out = a_.copy(); out.paste(b_.crop((x, 0, w, h)), (x, 0)); d = ImageDraw.Draw(out)
    d.line((x, 0, x, h), fill=(255, 255, 255), width=6)
    if frac < 0.97: d.text((x + 24, 24), "YOUR DOG", font=font(SANS, 40), fill=(255, 255, 255), stroke_width=4, stroke_fill=(10, 10, 10))
    if frac > 0.03: d.text((x - 24, 24), "YOU", font=font(SANS, 40), fill=(255, 255, 255), anchor="ra", stroke_width=4, stroke_fill=(10, 10, 10))
    card = Image.new("RGBA", (w + 24, h + 24), (250, 247, 240, 255)); card.paste(out, (12, 12)); return card
def split(c, name, t, t0, t1, x=W / 2, y=520, w=1000, h=600, wipe=(0.5, 1.6)):
    if not (t0 <= t < t1) or not ph(name): return
    frac = 1.0 - ease((t - t0 - wipe[0]) / wipe[1]) * 0.5
    put(c, split_frame(name, w, h, frac), x, y, popk(t, t0))


def S(im, k): return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
EMO = {}
def emoji(ch, size=220):
    if (ch, size) not in EMO:
        from PIL import ImageFont
        im = Image.new("RGBA", (180, 160), (0, 0, 0, 0)); ImageDraw.Draw(im).text((8, 8), ch, font=ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 109), embedded_color=True)
        im = im.crop(im.getbbox()); EMO[(ch, size)] = im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)
    return EMO[(ch, size)]

# ------------------------------------------------------------------ cached drawings
CONES_H, CONES_D = D.cones(False), D.cones(True); CH20, CH75 = D.eye_chart(), D.eye_chart(5, label="DOG · ~20/75")
FOV_D, FOV_H = D.fov(True), D.fov(False); STAMPS = {k: stamp(k, 64, c) for k, c in (("NO FACE AREA", (210, 40, 40)), ("BUILT FOR MOTION", (40, 90, 180)),
    ("UNTESTED IDEA", (210, 40, 40)), ("DISPUTED", (210, 40, 40)), ("SECURE BASE", (30, 140, 60)), ("NOT BLACK & WHITE", (40, 90, 180)))}

# ------------------------------------------------------------------ the montage
def overlay(c, t, cam):
    # ---- HOOK
    if t < A["stares"]:
        L.big(c, "20 DOG BRAINS SCANNED", t, 0.0, y=170, size=110, sub="looking for a 'face area' like ours · Bunford et al., J Neuroscience 2020")
        real(c, "f8_brain.jpg", t, 0.3, W / 2, 600, 560, -2)
        if t >= A["didnt"]: put(c, STAMPS["NO FACE AREA"], 1340, 640, popk(t, A["didnt"]))
    if A["stares"] <= t < A["blurry"]:
        L.headline(c, "SO WHAT IS YOUR DOG LOOKING AT?", t, A["stares"], size=84)
        if ph("f8_dog_eyes.jpg"): L.photo(c, ph("f8_dog_eyes.jpg"), t, A["stares"] + 0.2, x=W / 2, y=600, w=760, rot=-2, credit="Pexels · Rajesh S Balouria")
    if A["blurry"] <= t < A["recognizes"]:
        split(c, "f8_man.jpg", t, A["blurry"] - 0.3, A["recognizes"], y=560, w=1040, h=585, wipe=(0.3, 1.2))
        for k, (txt, tt) in enumerate((("BLURRY", A["blurry"]), ("BLUE + YELLOW", A["blurry"] + 1.2), ("VERY SMELLY", A["smelly"] - 0.3))):
            if t >= tt: put(c, pill(txt, 44, YEL), W / 2 - 420 + k * 420, 150, popk(t, tt))
    if A["recognizes"] <= t < A["habibi"]:
        L.big(c, "IT'S NOT (MOSTLY) YOUR FACE", t, A["recognizes"], y=260, size=100)
        real(c, "f8_brows.jpg", t, A["recognizes"] + 0.5, W / 2, 640, 640, 2)
    if A["habibi"] <= t < CH[0][1]:
        L.character(c, "host_cool", t, A["habibi"], 1560, h=520); L.headline(c, "THE WORLD THROUGH A DOG'S EYES", t, A["habibi"] + 0.5, size=84)
        real(c, "f8_dog_eyes.jpg", t, A["habibi"] + 0.6, 600, 620, 620, -3)
    # ---- CH1 what your dog sees
    if A["three"] <= t < A["blues"] + 1.0:
        put(c, CONES_H, W / 2 - 480, 520, popk(t, A["three"]))
        if t >= A["two"]: put(c, CONES_D, W / 2 + 480, 520, popk(t, A["two"]))
        if t >= A["blues"]: L.big(c, "MOSTLY BLUES + YELLOWS", t, A["blues"], y=170, size=96, sub="Neitz, Geist & Jacobs 1989")
    if A["black"] <= t < A["toy"] - 0.3:
        put(c, STAMPS["NOT BLACK & WHITE"], W / 2, 300, popk(t, A["black"]))
        if t >= A["test"]: L.sub(c, "in one test, 6 of 8 dogs chose by colour, not brightness · Kasparson et al. 2013", t, A["test"], y=470)
        if t >= A["reds"]: L.big(c, "REDS + GREENS -> DULL BROWNS", t, A["reds"], y=640, size=90, col=(200, 170, 110))
    if A["toy"] - 0.3 <= t < A["sharpness"]:
        split(c, "f8_red_ball.jpg", t, A["toy"] - 0.3, A["sharpness"], y=540, w=1180, h=690, wipe=(1.2, 2.2))
        if t >= A["dumb"]: put(c, pill("it's not dumb. it just can't see it.", 46, YEL), W / 2, 950 - 120, popk(t, A["dumb"]))
    if A["sharpness"] <= t < A["park"]:
        L.headline(c, "SHARPNESS", t, A["sharpness"], size=100); put(c, CH20, W / 2 - 300, 590, popk(t, A["sharpness"] + 0.3))
        if t >= A["vets"]: put(c, CH75, W / 2 + 300, 590, popk(t, A["vets"] + 0.8)); L.sub(c, "vet estimate (Miller 2001) · people see ~3x more detail (Lind et al. 2017)", t, A["vets"] + 1.0, y=270)
    if A["park"] <= t < A["police"] - 0.2:
        split(c, "f8_park_dog.jpg", t, A["park"] - 0.2, A["police"] - 0.2, y=540, w=1100, h=640, wipe=(0.2, 1.0))
        if t >= A["moving"]: put(c, pill("...but a MOVING blur is different", 46, YEL), W / 2, 950 - 120, popk(t, A["moving"]))
    if A["police"] - 0.2 <= t < A["flicker"]:
        if ph("f8_police.jpg"): L.photo(c, ph("f8_police.jpg"), t, A["police"] - 0.2, x=520, y=560, w=720, rot=-3, credit="Pexels · maxed. RAW")
        put(c, S(D.bars([("spotted MOVING", 900, 900, (255, 160, 60), "~900 m"), ("recognized STILL", 585, 900, (120, 190, 255), "~580 m")], w=820, u=ease((t - A["police"] - 0.8) / 1.0), title="14 police dogs, a 1936 study (via Miller 2001)"), 1.15), 1420, 520, popk(t, A["police"] + 0.5))
        if t >= A["motion"]: put(c, STAMPS["BUILT FOR MOTION"], 1420, 840, popk(t, A["motion"]))
    if A["flicker"] <= t < A["wider"]:
        L.big(c, "70-80 FLASHES A SECOND", t, A["flicker"] + 0.6, y=170, size=96, sub="humans: ~60 · Coile et al. 1989 (via Healy 2013)")
        real(c, "f8_tv.jpg", t, A["flicker"] + 1.0, W / 2, 600, 600, 2)
        if t >= A["flicker"] + 5.0: put(c, pill("old TVs may have looked flickery to dogs", 42, (255, 255, 255)), W / 2, 870 - 60, popk(t, A["flicker"] + 5.0))
    if A["wider"] <= t < A["shine"] + 3.5:
        if t < A["dim"]:
            put(c, FOV_H, W / 2 - 420, 560, popk(t, A["wider"])); put(c, FOV_D, W / 2 + 420, 560, popk(t, A["wider"] + 0.6))
            L.headline(c, "DOGS SEE WIDER", t, A["wider"], size=96); L.sub(c, "yellow = both eyes overlap · Miller 2001", t, A["wider"] + 1.0, y=270)
        else:
            L.big(c, "~5x LESS LIGHT NEEDED", t, A["dim"], y=170, size=100, sub="probably · tapetum lucidum + more rods · Miller 2007")
            real(c, "f8_dog_eyes.jpg", t, A["dim"] + 0.4, W / 2, 600, 620, -2)
            if t >= A["shine"]: put(c, pill("eye shine = a mirror layer behind the eye", 44, YEL), W / 2, 870 - 60, popk(t, A["shine"]))
    # ---- CH2 your face
    if A["face2"] <= t < A["happy"] - 0.3:
        L.headline(c, "CAN DOGS TELL FACES APART?", t, A["face2"], size=90)
        if ph("f8_man.jpg"): L.photo(c, ph("f8_man.jpg"), t, A["face2"] + 0.6, x=W / 2, y=600, w=760, rot=2, credit="Pexels · Andrea Piacquadio")
        if t >= A["inner"]: L.sub(c, "yes, from photos... but many struggled with the INNER face only · Racca 2010, Huber 2013", t, A["inner"], y=270)
    if A["happy"] - 0.3 <= t < A["right"] - 0.4:
        L.big(c, "HAPPY vs ANGRY", t, A["happy"] - 0.3, y=180, size=120, sub="20 dogs, trained on HALF a face · Müller et al., Current Biology 2015")
        real(c, "f8_man.jpg", t, A["happy"], W / 2, 600, 640, -2)
        if t >= A["never"]: put(c, pill("...then got NEW faces right", 46, YEL), W / 2, 820, popk(t, A["never"]))
    if A["right"] - 0.4 <= t < A["brain2"] - 0.3:
        L.headline(c, "THEY LOOK AT YOUR RIGHT SIDE FIRST", t, A["right"] - 0.4, size=80)
        L.sub(c, "like we do, and only with human faces · Guo et al. 2009", t, A["right"], y=270)
        if ph("f8_man.jpg"): L.photo(c, ph("f8_man.jpg"), t, A["right"] - 0.2, x=W / 2 + 120, y=620, w=700, rot=-2)
        if t >= A["right"] + 0.6: put(c, pill("their RIGHT side = YOUR left as you look", 40, YEL), 470, 860 - 60, popk(t, A["right"] + 0.6))
    if A["brain2"] - 0.3 <= t < CH[2][1]:
        L.big(c, "HUMAN OR DOG?", t, A["cared"] - 0.4, y=180, size=120, sub="that's what their brains cared about · Bunford et al. 2020") if t >= A["cared"] - 0.4 else L.headline(c, "THAT BRAIN SCAN AGAIN", t, A["brain2"] - 0.3, size=96)
        real(c, "f8_brain.jpg", t, A["brain2"], W / 2, 600, 560, 2)
        if t >= A["matters"]: put(c, pill("your face matters... it's just not the main clue", 44, YEL), W / 2, 830, popk(t, A["matters"]))
    # ---- CH3 your smell
    if A["smell"] <= t < A["genes"] - 0.2:
        if ph("f8_nose.jpg"): L.photo(c, ph("f8_nose.jpg"), t, A["smell"], x=520, y=560, w=680, rot=-3, credit="Pexels · Denisha Sandoval")
        put(c, S(D.bars([("dogs (estimated)", 300, 300, (255, 160, 60), "300M"), ("humans", 6, 300, (120, 190, 255), "6M")], w=820, u=ease((t - A["m300"]) / 1.0), title="smell receptors · NOVA/PBS"), 1.15), 1420, 560, popk(t, A["m300"] - 0.4))
    if A["genes"] - 0.2 <= t < A["trillion"] - 0.4:
        put(c, S(D.bars([("dog smell genes that look broken", 18, 100, (255, 160, 60), "18%"), ("human", 63, 100, (120, 190, 255), "63%")], w=1100, u=ease((t - A["broken"]) / 1.0), title="~1,100 smell genes · Quignon et al. 2003/2005"), 1.15), W / 2, 560, popk(t, A["genes"] - 0.2))
    if A["trillion"] - 0.4 <= t < A["horowitz"] - 0.3:
        L.big(c, "~1 PART PER TRILLION", t, A["trillion"] - 0.4, y=170, size=110, sub="2 dogs, one chemical (amyl acetate) · via Concha et al. 2019")
        real(c, "f8_pool.jpg", t, A["trillion"] + 0.3, W / 2, 600, 760, -2)
        if t >= A["trillion"] + 1.0: put(c, pill("about 1 drop in 20 Olympic pools", 48, YEL), W / 2, 880 - 60, popk(t, A["trillion"] + 1.0))
    if A["horowitz"] - 0.3 <= t < A["greeted"] - 0.2:
        L.headline(c, "CAN DOGS SMELL TIME?", t, A["horowitz"] - 0.3, size=96); L.sub(c, "an idea from Alexandra Horowitz", t, A["horowitz"], y=270)
        real(c, "f8_door.jpg", t, A["horowitz"] + 0.3, W / 2, 610, 620, -2)
        if t >= A["tested"]: put(c, STAMPS["UNTESTED IDEA"], 1460, 760, popk(t, A["tested"]))
    if A["greeted"] - 0.2 <= t < A["brain3"] - 0.2:
        if ph("f8_dog_eyes.jpg"): L.photo(c, ph("f8_dog_eyes.jpg"), t, A["greeted"] - 0.2, x=W / 2, y=600, w=700, rot=2, credit="Pexels · Rajesh S Balouria")
        L.big(c, "2 HOURS > 30 MINUTES", t, A["greeted"] + 0.6, y=170, size=100, sub="12 dogs greeted owners more intensely · Rehn & Keeling 2011")
    if A["brain3"] - 0.2 <= t < A["stressed"] - 0.3:
        L.big(c, "YOUR SCENT = REWARD", t, A["brain3"] + 2.0, y=170, size=110, sub="12 dogs, 5 scents: familiar human won · Berns et al. 2015")
        real(c, "f8_brain.jpg", t, A["brain3"], W / 2, 600, 560, -2)
        if t >= A["feeling"]: put(c, pill("a good feeling, not just information", 44, YEL), W / 2, 830, popk(t, A["feeling"]))
    if A["stressed"] - 0.3 <= t < A["sub_mid"] - 0.2:
        L.big(c, "~94%", t, A["stressed"] + 1.0, y=300, size=200, sub="4 trained dogs told stressed vs relaxed breath + sweat apart · Wilson et al. 2022", sub_y=440)
        real(c, "f8_nose.jpg", t, A["stressed"], 1560, 760, 420, 3)
    L.subscribe_nudge(c, t, A["sub_mid"], A["sub_more"] + 1.4, x=1200, y=470, t_click=A["sub_word"])
    # ---- CH4 your voice
    if A["voice"] <= t < A["flat"] - 0.3:
        L.headline(c, "DOGS HAVE VOICE AREAS TOO", t, A["voice"], size=90); L.sub(c, "11 dogs scanned · Andics et al. 2014", t, A["voice"] + 0.6, y=270)
        put(c, S(D.waves(t, happy=t >= A["happy2"]), 1.9), W / 2, 560, popk(t, A["voice"] + 0.3))
        if t >= A["left"]: L.sub(c, "left brain: the WORD · reward: only praise word + praising tone · Andics 2016", t, A["left"], y=780, col=(255, 255, 255))
    if A["flat"] - 0.3 <= t < A["y2024"] - 0.2:
        put(c, outlined("good boy.", 90, fill=(170, 170, 170)), W / 2 - 400, 420, popk(t, A["flat"] - 0.3)); put(c, S(D.waves(t, False), 1.4), W / 2 - 400, 620, popk(t, A["flat"]))
        put(c, outlined("GOOD BOY!", 110, fill=YEL), W / 2 + 400, 420, popk(t, A["flat"] + 0.6)); put(c, S(D.waves(t, True), 1.4), W / 2 + 400, 620, popk(t, A["flat"] + 0.6))
    if A["y2024"] - 0.2 <= t < CH[4][1]:
        L.big(c, "2024: DO DOGS KNOW WORDS?", t, A["y2024"] - 0.2, y=170, size=96, sub="18 dogs, brainwaves (EEG) · Boros et al., Current Biology 2024")
        put(c, S(D.waves(t * 0.5, True), 1.9), W / 2, 540, popk(t, A["y2024"] + 0.6))
        if t >= A["match"]: put(c, pill("the brain reacted when the toy DIDN'T match the word", 42, YEL), W / 2, 760, popk(t, A["match"]))
    # ---- CH5 the bond
    if A["bond"] <= t < A["evolve"] - 0.3:
        if ph("f8_puppy_eyes.jpg"): L.photo(c, ph("f8_puppy_eyes.jpg"), t, A["bond"] + 0.3, x=560, y=560, w=760, rot=-2, credit="Pexels · MJ Rahnama")
        L.headline(c, "THE PUPPY-EYES MUSCLE", t, A["eyebrows"] - 0.4, size=90)
        if t >= A["five"]: put(c, S(D.bars([("dogs (dissected)", 5, 6, (255, 160, 60), "5 of 6"), ("wolves", 0, 4, (120, 190, 255), "0 of 4")], w=760, u=ease((t - A["five"]) / 1.0), title="Kaminski et al., PNAS 2019"), 1.15), 1420, 520, popk(t, A["five"]))
        if t >= A["adopted"]: put(c, pill("shelter dogs that used it more: adopted faster (Waller 2013)", 38, YEL), 1420, 820, popk(t, A["adopted"]))
    if A["evolve"] - 0.3 <= t < A["toddlers"] - 0.3:
        L.big(c, "DID DOGS EVOLVE TO WORK ON US?", t, A["evolve"] - 0.3, y=170, size=90, sub="maybe", sub_y=270)
        real(c, "f8_eye_contact.jpg", t, A["evolve"] + 0.4, 1380, 700, 560, 3)
        if t >= A["oxytocin"]: L.sub(c, "mutual gaze: oxytocin up in dogs + owners · Nagasawa et al., Science 2015", t, A["oxytocin"], y=360)
        if t >= A["questioned"]: put(c, STAMPS["DISPUTED"], W / 2, 520, popk(t, A["questioned"]))
    if A["toddlers"] - 0.3 <= t < CH[5][1]:
        L.headline(c, "ATTACHED, LIKE TODDLERS", t, A["toddlers"] - 0.3, size=90); L.sub(c, "Topál 1998 · Horn, Huber & Range 2013", t, A["toddlers"], y=270)
        real(c, "f8_park_dog.jpg", t, A["toddlers"] + 0.4, 760, 700, 460, -2)
        if t >= A["puzzle"]: put(c, STAMPS["SECURE BASE"], 1450, 420, popk(t, A["puzzle"]))
        if t >= A["n13"]: put(c, S(D.bars([("praise from owner ≥ food", 13, 15, (255, 160, 60), "13 of 15")], w=760, u=ease((t - A["n13"]) / 0.8), title="Cook et al. 2016"), 1.15), 1460, 700, popk(t, A["n13"]))
    # ---- CH6 alpha
    if A["alpha"] <= t < A["safe"] - 0.3:
        if ph("f8_wolf.jpg"): L.photo(c, ph("f8_wolf.jpg"), t, A["alpha"], x=540, y=580, w=760, rot=-2, credit="Pexels · Daniel Lengies")
        if t >= A["y1970"]: L.big(c, "1970: 'ALPHA' WOLVES", t, A["y1970"], y=180, size=90, x=1400, sub="from a book by L. David Mech")
        if t >= A["parents"] - 0.6: put(c, D.crossed_word("ALPHA", "parents"), 1400, 560, popk(t, A["parents"] - 0.6))
        if t >= A["print"]: put(c, pill("Mech later had his own book taken out of print", 38, YEL), 1400, 820, popk(t, A["print"]))
    if A["safe"] - 0.3 <= t < CH[6][1]:
        L.big(c, "YOU'RE A SAFE BASE", t, A["safe"] - 0.3, y=200, size=120)
        real(c, "f8_shoes.jpg", t, A["safe"], W / 2, 620, 360, 2)
    # ---- CH7 so how does your dog see you
    if A["shape"] - 0.6 <= t < A["smell_end"] - 0.3: split(c, "f8_man.jpg", t, A["shape"] - 0.6, A["smell_end"] - 0.3, y=560, w=1000, h=560, wipe=(0.2, 0.8))
    if A["smell_end"] - 0.3 <= t < A["voice_end"] - 0.3:
        if ph("f8_shoes.jpg"): L.photo(c, ph("f8_shoes.jpg"), t, A["smell_end"] - 0.3, x=W / 2, y=560, w=420, rot=2, credit="Pexels · Sameer Singh")
        put(c, pill("a smell that may tell time + carries your mood", 42, YEL), W / 2, 140, popk(t, A["smell_end"]))
    if A["voice_end"] - 0.3 <= t < A["home"] - 0.3:
        put(c, outlined("GOOD BOY!", 120, fill=YEL), W / 2, 380, popk(t, A["voice_end"])); put(c, S(D.waves(t, True), 1.9), W / 2, 620, popk(t, A["voice_end"] + 0.3))
    if A["home"] - 0.3 <= t < A["subscribe"]:
        if ph("f8_park_dog.jpg"): L.photo(c, ph("f8_park_dog.jpg"), t, A["home"] - 0.3, x=600, y=560, w=720, rot=-2, credit="Pexels · Omar Ramadan")
        if t >= A["tears"]: L.big(c, "MORE TEARS", t, A["tears"], y=200, size=120, x=1400, sub="when reunited with their owner · Murata et al. 2022")
        if t >= A["withyou"]: put(c, outlined("WITH YOU.", 150, fill=YEL, f=IMPACT, stroke=10), 1400, 560, popk(t, A["withyou"]))
    if A["subscribe"] <= t < A["endscreen"]:
        L.character(c, "host_cool", t, A["subscribe"], 1560, h=520)
        put(c, pill("SUBSCRIBE · next: what walking does to your organs", 50, (255, 255, 255), (200, 30, 30, 240)), W / 2 - 160, 300, popk(t, A["subscribe"] + 0.3))
    L.end_screen(c, t, A["endscreen"], "still curious?")
    L.chapter_card(c, t, CH)

SFX = [("pop", A[n] + 0.3, -20) for n in ("didnt", "stares", "blurry", "two", "black", "toy", "vets", "park", "police", "motion", "flicker", "wider", "dim",
                                          "face2", "happy", "right", "cared", "smell", "genes", "trillion", "horowitz", "tested", "greeted", "stressed", "voice",
                                          "flat", "y2024", "bond", "five", "questioned", "toddlers", "n13", "alpha", "parents", "safe", "shape", "home", "withyou")]
SFX += [("paper_slide", t0, -20) for _, t0 in CH]
SFX += [("pop", A["sub_word"] + 0.25, -18), ("paper_slide", A["endscreen"], -18), ("pop", A["endscreen"] + 2.3, -20)]

if __name__ == "__main__":
    if sys.argv[1] == "anchors":
        for k, v in A.items(): print(f"{v:7.2f}  {k}")
        print("END", END)
    else: K.main(sys.argv, overlay, SFX)
