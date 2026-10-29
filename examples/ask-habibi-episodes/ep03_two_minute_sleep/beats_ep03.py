"""Ep 3 beat list: one visual per line of the script, every overlay keyed to a word in the voiceover.
BEATS (ordered, contiguous) + CUES (sound effects) are imported by render_beats.py and mix_ep03.py.
Layout rule: every note sits above the caption band (bottom edge y <= 800); only small Batata stickers use the
bottom corners (x > 1520). check_caption_zone.py must print 0."""
from ep03_fx import *

def P(phrase, after=0.0):
    """final-timeline time of `phrase` (first occurrence at/after timeline second `after`)"""
    return T(find(phrase, after if after <= S_CUT else after - O1))
def PE(phrase, after=0.0):
    return T(find_end(phrase, after if after <= S_CUT else after - O1))
def C1(t): return T_CTA_IN + t - CTA_IN[0]          # Ep 1 VO time inside the CTA intro -> timeline
def C2(t): return T_CTA_OUT + t - CTA_OUT[0]

INK = (28, 36, 105)                                  # ballpoint blue for writing on the notebook page

class Line(Static):
    def __init__(self, pts, t_in, color=WHITE, width=8, seed=2, t_out=None):
        super().__init__(t_in, 0.25, t_out); self.a = (np.array(pts, float), color, width, seed)
    def paint(self, layer, prog):
        pts, color, width, seed = self.a
        strokes(layer, [np.concatenate([np.linspace(pts[i], pts[i + 1], 40) for i in range(len(pts) - 1)])], color, width, prog, seed=seed)

class VideoHold(VideoBG):
    """plays at normal speed and holds the last frame (for the brand sting)"""
    def _open(self, d):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", self.path, "-vf", f"fps=30,scale={W}:{H}", "-f", "rawvideo",
                                   "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)

class Card(Ov):
    """our own hand-written index card (never a book cover): pops in, each line writes on at its own cue"""
    def __init__(self, x, y, t_in, lines, w=900, h=540, rot=-3):
        self.x, self.y, self.t_in, self.t_out, self.lines, self.w, self.h, self.rot = x, y, t_in, None, lines, w, h, rot
        self._base = self._done = None
    def base(self):
        if self._base is None:
            im = Image.new("RGBA", (self.w, self.h), (248, 246, 236, 255)); d = ImageDraw.Draw(im)
            d.line([(0, 100), (self.w, 100)], fill=(226, 92, 92, 255), width=3)
            for yy in range(152, self.h, 52): d.line([(0, yy), (self.w, yy)], fill=(160, 190, 232, 255), width=2)
            self._base = im
        return self._base
    def draw(self, c, tl):
        if not self.on(tl): return
        done = all(tl >= t + 0.4 for _, t, *_ in self.lines)
        if done and self._done is not None: card = self._done
        else:
            card = self.base().copy()
            for text, t, size, color, dx, dy in self.lines:
                if tl >= t: place(card, hand(text, size, color, rot=0, reveal=min(1.0, (tl - t) / 0.35)), dx, dy, "lt")
            sh = Image.new("RGBA", (self.w + 40, self.h + 40), (0, 0, 0, 0)); sh.alpha_composite(Image.new("RGBA", (self.w, self.h), (0, 0, 0, 140)), (14, 18))
            sh = sh.filter(ImageFilter.GaussianBlur(8)); sh.alpha_composite(card, (0, 0))
            card = sh.rotate(self.rot, Image.BICUBIC, expand=True)
            if done: self._done = card
        k = int((tl - self.t_in) * FPS); sc = pop(k)
        im = card if sc == 1.0 else card.resize((max(1, int(card.width * sc)), max(1, int(card.height * sc))), Image.BILINEAR)
        place(c, im, self.x, self.y)

BEATS, CUES = [], []          # CUES: (timeline_s, sfx_name, gain)
def beat(t0, bg, ovs=(), punch=(), shakes=(), name=""):
    BEATS.append(Beat(t0, bg, ovs, punch, shakes, name))
def cue(t, name, g=1.0): CUES.append((t, name, g))

def level(n, title, photo, t_n, t_title, focus=(0.5, 0.5), x=760, amt=0.3, dark=0.8, mirror=False, video=None):
    bg = video or PhotoBG(photo, focus=focus, amt=amt, z=(1.0, 1.04), dark=dark, mirror=mirror)
    beat(t_n, bg, [Note(f"level {n}", x + 140, 270, t_n + 0.05, size=88), Underline(x + 20, x + 260, 322, t_n + 0.25),
                   Big(title, x, 360, t_title, size=180, anchor="lt")], shakes=[t_title], name=f"level{n}")
    cue(t_n, "riser_short", 0.6); cue(t_title, "impact_soft", 0.8)

# the notebook list (Level 1, step six, the Level 3 verdict)
NOTEBOOK = PH + "pexels-315791.jpg"
STEPS = ["1. relax your face", "2. drop your shoulders", "3. breathe out slowly", "4. let your legs go heavy",
         "5. picture something calm", "6. \"don't think\" (10 sec)"]
SX, SY0, SDY, SSIZE = 800, 150, 105, 64
def step_y(i): return SY0 + i * SDY
def step_w(i): return hand(STEPS[i], SSIZE, INK, rot=-1).width
def steps(times):
    return [Note(STEPS[i], SX, step_y(i), t, size=SSIZE, color=INK, rot=-1, anchor="lt") for i, t in enumerate(times) if t is not None]
def notebook_bg(): return PhotoBG(NOTEBOOK, focus=(0.5, 0.5), grade=False, dark=0.93, z=(1.0, 1.03))

# ---------------------------------------------------------------- COLD OPEN
t96 = P("the 96%.")
beat(0.0, VideoBG(VID2 + "pexels-6943545-hd_2048_1080_25fps.mp4", z=1.04),
     [Note("the 2-minute trick", 1440, 190, P("2-minute") + 0.1, size=92, rot=-3),
      Note("nobody tested →", 560, 300, P("nobody tested") + 0.1, size=80, color=WHITE, rot=-2),
      Big("96%", 960, 520, t96, size=300, color=YEL), Circle(960, 520, 300, 170, t96 + 0.3, color=RED, width=12)],
     shakes=[t96], name="cold_open")
cue(0.0, "room_tone", 0.5); cue(t96, "impact_soft", 0.9)

t0 = P("96% of pilots.")
beat(t0, PhotoBG(PH + "pexels-27057738.jpg", focus=(0.55, 0.5), amt=0.25, z=(1.0, 1.06)),
     [Note("96% of pilots", 90, 110, t0 + 0.1, size=86, anchor="lt"),
      Note("asleep in 2 min ✓", 90, 240, P("Asleep in two minutes.") + 0.1, size=72, color=WHITE, anchor="lt"),
      Note("after coffee ✓", 90, 350, P("After coffee.") + 0.1, size=72, color=WHITE, anchor="lt"),
      Note("with gunfire ✓", 90, 460, P("With gunfire") + 0.1, size=72, color=WHITE, anchor="lt")], name="pilots")
cue(t0, "whoosh_fast", 0.5)

t0 = P("And you.")
beat(t0, PhotoBG(PH2 + "pexels-6943990.jpg", focus=(0.5, 0.5), amt=0.5, z=(1.0, 1.06)),
     [Note("and you.", 480, 220, t0 + 0.05, size=100, color=WHITE, rot=-3),
      Note("silent bedroom", 480, 350, P("In a silent bedroom.") + 0.1, size=76, color=WHITE),
      Note("40:00", 1450, 230, P("40 minutes"), size=150, color=RED, rot=3),
      Note("and counting…", 1450, 380, P("and counting."), size=70, color=WHITE),
      Sticker("sleepy", 300, 1730, 880, P("and counting.") + 0.3, rot=-6)], name="bedroom")

t0 = P("So can you really"); t_q = P("two minutes?", t0)
beat(t0, PhotoBG(PH2 + "pexels-6943425.jpg", focus=(0.5, 0.42), amt=0.5, z=(1.0, 1.07)),
     [Big("2 minutes?", 960, 470, t_q, size=250)], shakes=[t_q], name="question")
cue(t_q, "impact_soft", 0.9)

t0 = P("Short answer:")
beat(t0, TextureBG(), [Line([(960, 140), (964, 600)], t0 + 0.1),
                       Note("advice", 560, 360, P("good advice") + 0.1, size=120, color=WHITE, rot=-3),
                       Note("story", 1360, 360, P("half a story.") + 0.1, size=120, rot=3),
                       Note("the number at the end →", 1000, 720, P("And the number at the end") + 0.2, size=70),
                       Sticker("smug", 300, 1730, 880, P("best news") , rot=8)], name="short_answer")

# ---------------------------------------------------------------- CTA intro (Ep 1 audio)
beat(S_CUT, PhotoBG(PH2 + "pexels-6327595.jpg", focus=(0.5, 0.5), amt=0.25, z=(1.0, 1.08)),
     [Note("20 min of scrolling", 1420, 230, C1(19.70), size=84, color=WHITE, rot=-3),
      Note("cold.", 520, 720, C1(23.80), size=130, color=WHITE, rot=-7)], name="cta_food")
beat(C1(24.96), VideoHold(KIT + "brand/intro_sting.mp4"), [Note("midnight questions, answered.", 1300, 770, C1(26.68), size=60, color=WHITE, rot=-2),
                                                         Note("press play. eat.", 520, 760, C1(29.58), size=70, rot=-4)], name="cta_sting")
beat(C1(31.30), TextureBG(), [Sticker("cool", 560, 640, 500, C1(31.30), rot=-4),
                              Note("subscribe", 1300, 400, C1(31.35), size=120), Circle(1300, 400, 270, 95, C1(31.65), color=YEL),
                              Note("so you don't have to search next time", 1300, 600, C1(32.0), size=46, color=WHITE)], name="cta_sub")
cue(C1(24.96), "whoosh_long", 0.6)

# ---------------------------------------------------------------- THE PLAN
t0 = P("Here's the plan."); t4 = P("Four levels.")
tl_lab = [P("The trick.", t4), P("The receipt.", t4), P("The part that holds up."), P("And the part where")]
cells = [(480, 250), (1440, 250), (480, 630), (1440, 630)]          # grid kept above the caption zone
labels = ["the trick", "the receipt", "what holds up", "the fine print"]
ovs = [Line([(960, 50), (962, 800)], t0), Line([(60, 440), (1860, 445)], t0 + 0.1)]
for i, ((x, y), lab) in enumerate(zip(cells, labels)):
    ti = tl_lab[i]
    ovs += [Note(str(i + 1), x - 330, y - 130, ti, size=96, rot=-5), Note(lab, x + 160, y + 110, ti + 0.1, size=58, color=WHITE),
            Sticker("cool" if i < 3 else "shocked", 260, x - 60, y, ti, rot=[-6, 4, -3, 7][i])]
t_bad = P("stops being good news.")
ovs += [Circle(1440, 640, 400, 185, t_bad, color=RED, width=12)]
beat(t0, TextureBG(), ovs, shakes=[t_bad], name="plan")

# ---------------------------------------------------------------- LEVEL 1: the trick
t1 = P("Level one.")
level(1, "the trick.", NOTEBOOK, t1, P("The trick.", t1), amt=0.45, dark=0.55)

t0 = P("It's called the military method.")
tr = [P("Relax your face."), P("Drop your shoulders."), P("Breathe out slowly,"), P("Then your legs.")]
beat(t0, notebook_bg(),
     [Note("\"the military method\"", 1250, 70, t0 + 0.2, size=62, color=RED, rot=-2)] + steps(tr + [None, None]) +
     [Note("jaw: relaxed.\ntongue: ???", 1150, 680, P("You didn't know") , size=54, color=RED, rot=4),
      Sticker("cool", 280, 1720, 700, P("Your tongue.") + 0.1, rot=6)] +
     [Tick(1780, step_y(i) + 30, tr[i] + 1.0, size=56, color=RED) for i in (1, 2, 3)],
     punch=[(P("Your tongue."), 1.08), (P("Drop your shoulders."), 1.0)], name="steps_1to4")
cue(t0, "paper_slide", 0.7)

t0 = P("Then, for 10 seconds,")
beat(t0, PhotoBG(PH + "pexels-12119226.jpg", focus=(0.5, 0.5), amt=0.45, dark=0.7, z=(1.0, 1.06)),
     [Note("5. picture something calm", 960, 160, t0 + 0.1, size=80, color=WHITE, rot=-2),
      Note("10 sec", 960, 280, P("10 seconds,", t0 - 0.1) + 0.2, size=70),
      Note("(a canoe on a still lake)", 960, 400, P("lying in a canoe"), size=64, color=WHITE)], name="canoe")

t0 = P("And if that doesn't work,"); t6 = P("step six.")
w6 = step_w(5)
beat(t0, notebook_bg(), steps([t0] * 5 + [t6]) +
     [Circle(SX + w6 / 2, step_y(5) + 38, w6 / 2 + 50, 62, P("Repeat the words") + 0.8, color=RED, width=10),
      Note("?", 1760, 560, P("As instructions go,"), size=200, color=RED, rot=8),
      Sticker("sideeye", 300, 1730, 880, P("don't look down."), rot=-6)], name="step6")

t0 = P("The promise:")
beat(t0, PhotoBG(PH + "pexels-27057738.jpg", focus=(0.6, 0.5), amt=0.25, z=(1.04, 1.1)),
     [Note("practise 6 weeks", 560, 200, P("practise for six weeks,"), size=84, color=WHITE, rot=-3),
      Note("→ out in 2 minutes", 560, 340, P("you'll be out in two minutes."), size=84, rot=-2),
      Note("(like the pilots)", 560, 480, P("Like the pilots."), size=64, color=WHITE)], name="promise")

# ---------------------------------------------------------------- LEVEL 2: the receipt
t2 = P("Level two.")
level(2, "the receipt.", PH2 + "pexels-4959907.jpg", t2, P("The receipt.", t2), x=560, amt=0.45, dark=0.55)

t0 = P("So where does")
beat(t0, TextureBG(), [Big("96%", 680, 420, t0 + 0.2, size=260, color=YEL),
                       Note("← from where?", 1320, 420, P("come from?"), size=90, color=WHITE),
                       Note("I followed it back.", 960, 700, P("I followed it back."), size=70, color=WHITE)], name="where_from")

t0 = P("The articles all point")
beat(t0, TextureBG(), [Note("every article points here ↓", 900, 80, t0 + 0.2, size=62, color=WHITE, rot=-1),
                       Card(880, 490, P("A 1981 book"), [("1981", P("A 1981 book") + 0.1, 64, RED, 700, 30),
                                                          ("Relax and Win", P("Relax and Win,"), 96, INK, 50, 120),
                                                          ("by Lloyd \"Bud\" Winter", P("by Lloyd"), 64, INK, 50, 250),
                                                          ("(a college track coach)", P("a college track coach."), 58, INK, 50, 345)]),
                       Note("the story goes…", 1580, 260, P("The story goes"), size=70, rot=3),
                       Note("WWII · navy pilots", 1580, 390, P("navy pilots"), size=58, color=WHITE, rot=2)],
     name="the_book")
cue(P("A 1981 book"), "paper_slide", 0.8)

t0 = P("A book. Not a journal.")
beat(t0, TextureBG(), [Big("a book.", 640, 360, t0 + 0.05, size=180), Note("not a journal.", 1320, 400, P("Not a journal."), size=90, color=RED, rot=4)],
     name="a_book")

t0 = P("I searched PubMed")
beat(t0, TextureBG(), [Pasted(RCROP + "pubmed_search_top.png", 1760, 960, 290, t0 + 0.1, rot=-1.5),
                       Note("trials of this exact method: none found", 960, 560, P("I didn't find one."), size=64),
                       Note("no control group. no data anyone can check.", 960, 700, P("No control group."), size=54, color=WHITE)],
     name="pubmed_search")
cue(t0, "paper_slide", 0.7)

t0 = P("96% is a very confident"); t_fn = P("no footnotes.")
beat(t0, TextureBG(), [Note("96% (very confident)", 960, 220, t0 + 0.1, size=90, color=WHITE),
                       Big("no footnotes.", 960, 500, t_fn, size=200, color=YEL),
                       Sticker("sideeye", 300, 1730, 880, t_fn + 0.3, rot=-6)], shakes=[t_fn], name="no_footnotes")

t0 = P("To be fair,")
beat(t0, TextureBG(), [Note("no study ≠ doesn't work", 960, 200, P("no study doesn't mean"), size=84, color=WHITE),
                       Note("= nobody checked.", 960, 330, P("It means nobody checked."), size=84),
                       Big("let's check.", 960, 540, P("So let's check it ourselves,"), size=170),
                       Note("each step: studied ✓   together: never", 960, 730, P("Because each step has been studied."), size=54, color=WHITE)],
     name="fair")

# ---------------------------------------------------------------- LEVEL 3: what holds up
t3 = P("Level three.")
level(3, "what\nholds up.", PH + "pexels-12119226.jpg", t3, P("What holds up.", t3), amt=0.3, dark=0.8)

t0 = P("Steps one to four")
beat(t0, PhotoBG(PH + "pexels-3771069.jpg", focus=(0.5, 0.45), amt=0.5, dark=0.6, z=(1.0, 1.05)),
     [Note("steps 1–4 = relaxation therapy", 960, 150, t0 + 0.3, size=76, rot=-2),
      Note("tense less", 330, 330, P("Tense less."), size=66, color=WHITE),
      Note("breathe slower", 330, 450, P("Breathe slower."), size=66, color=WHITE),
      Note("go heavy", 330, 570, P("Let the body go heavy."), size=66, color=WHITE)], name="relax_therapy")

REL = ("We suggest that clinicians use relaxation therapy as a single-component therapy for the treatment of chronic insomnia "
       "disorder in adults. (CONDITIONAL)")
t0 = P("The American Academy")
beat(t0, Receipt("edinger2021_aasm_guideline", [dict(t=t0, at=REL, s=1.15)],
                 [dict(phrase=REL, t=P("does suggest relaxation therapy.") - 0.1, dur=1.2)], tag="AASM clinical practice guideline, 2021"),
     [Note("conditional = a maybe.", 1450, 180, P("It's a maybe,"), size=70)], name="r_aasm_relax")
cue(t0, "paper_slide", 0.8)

t0 = P("Step five, the calm picture,")
beat(t0, PhotoBG(PH + "pexels-12119226.jpg", focus=(0.5, 0.5), amt=0.45, dark=0.7, z=(1.04, 1.09)),
     [Note("5. the calm picture", 560, 200, t0 + 0.1, size=84, color=WHITE, rot=-2),
      Note("the best part ✓", 560, 330, P("is the best part."), size=70),
      Pasted("D:/why habibi/2nd video/export/thumbnails/thumb_1_STILL_AWAKE.png", 600, 1450, 420, P("last week's episode,"), rot=3),
      Note("ep 2", 1450, 700, P("last week's episode,") + 0.3, size=70)], name="calm_picture")

t0 = P("In 2002,")
beat(t0, Receipt("harvey_payne2002_pubmed",
                 [dict(t=t0, at="distraction with imagery versus general distraction", s=1.25, dy=40),
                  dict(t=P("41 people"), at="Forty one people with insomnia", s=1.35),
                  dict(t=P("The picture takes up"), at="cognitive space", s=1.45)],
                 [dict(phrase="2002 Mar", t=t0 + 0.1, kind="circle"),
                  dict(phrase="distraction with imagery versus general distraction", t=t0 + 0.6),
                  dict(phrase="Forty one people with insomnia", t=P("41 people") + 0.2),
                  dict(phrase="cognitive space", t=P("the room your worries need.") - 0.3)],
                 tag="Harvey & Payne, 2002 · Behaviour Research and Therapy"),
     [Note("one picture > no instructions", 1430, 190, P("fell asleep faster than people"), size=62)], name="r_payne")
cue(t0, "paper_slide", 0.8)

t0 = P("And step six?")
beat(t0, TextureBG(), [Note("6. \"don't think.\"", 960, 330, t0 + 0.1, size=120, color=WHITE),
                       Note("tested ✓", 960, 520, P("Psychologists tested that one too."), size=80)], name="step6_tested")

t0 = P("Try it.")
beat(t0, PhotoBG(PH + "pexels-29645467.jpg", focus=(0.6, 0.45), amt=0.35, dark=0.7, z=(1.0, 1.12)),
     [Note("5 sec", 300, 300, P("For the next five seconds,"), size=90, rot=-4),
      Note("don't think about a white bear.", 960, 130, P("don't think about a white bear."), size=76, color=WHITE),
      Sticker("panic", 300, 1730, 880, PE("white bear.") + 0.3, rot=6)], name="white_bear")

t0 = P("Yeah.")
beat(t0, PhotoBG(PH + "pexels-29645467.jpg", focus=(0.62, 0.42), amt=0.35, dark=0.7, z=(1.3, 1.36)),
     [Note("…yeah.", 1500, 220, t0 + 0.05, size=130, rot=-4)], name="yeah")

t0 = P("In 1987,")
td = P("The bell kept ringing.")
beat(t0, Receipt("wegner1987_pubmed",
                 [dict(t=t0, at="Paradoxical effects of thought suppression", s=1.25, dy=60),
                  dict(t=P("asked people to do exactly that,"), at="try not to think of a white bear", s=1.35),
                  dict(t=P("And later,"), at="significantly more tokens of thought about the bear", s=1.35)],
                 [dict(phrase="1987 Jul", t=t0 + 0.1, kind="circle"),
                  dict(phrase="Paradoxical effects of thought suppression", t=P("Daniel Wegner") + 0.2),
                  dict(phrase="try not to think of a white bear", t=P("exactly that,")),
                  dict(phrase="ring a bell", t=P("ring a bell") + 0.1),
                  dict(phrase="unable to suppress the thought", t=td + 0.3),
                  dict(phrase="significantly more tokens of thought about the bear", t=P("even more than") - 0.2)],
                 tag="Wegner et al., 1987 · J. Personality and Social Psychology"),
     [Note("ding.", 1500, 170, td, size=80, rot=-6), Note("ding.", 1660, 270, td + 0.35, size=80, rot=5),
      Note("ding.", 1530, 370, td + 0.7, size=80, rot=-3)], name="r_wegner")
cue(t0, "paper_slide", 0.8)
for k in range(3): cue(td + 0.35 * k, "bell", 0.5)

t0 = P("Telling your brain"); t_bear = P("get the bear.")
beat(t0, TextureBG(), [Note("\"don't think\"", 560, 360, t0 + 0.1, size=110, color=WHITE),
                       Arrow((840, 360), (1150, 380), t_bear - 0.4, bend=0.2),
                       Pasted(PH + "pexels-29645467.jpg", 560, 1450, 380, t_bear, rot=4, grade=True),
                       Note("= the bear.", 1450, 680, t_bear + 0.3, size=80)], name="get_the_bear")

t0 = P("But in a second experiment,")
beat(t0, Receipt("wegner1987_pubmed", [dict(t=t0, at="a specific thought to use as a distracter", s=1.35)],
                 [dict(phrase="a specific thought to use as a distracter", t=P("one specific thing") + 0.1)],
                 tag="Wegner et al., 1987 · J. Personality and Social Psychology"),
     [Note("= the calm picture, again", 1420, 180, P("That's the calm picture again."), size=66)], name="r_wegner2")

t0 = P("So, level three's verdict.")
tk1, tk2, tk3 = P("Keep the relaxing."), P("Keep the picture."), P("Drop the")
beat(t0, notebook_bg(), steps([t0] * 6) +
     [Note("verdict:", 1300, 60, t0 + 0.2, size=62, color=RED, rot=-2)] +
     [Tick(1780, step_y(i) + 30, tk1 + 0.15 * i, size=56, color=RED) for i in range(4)] +
     [Tick(1780, step_y(4) + 30, tk2 + 0.1, size=56, color=RED),
      Strike(SX - 10, SX + w6 + 10, step_y(5) + 38, P("don't think.\"", tk3) - 0.2, color=RED, width=10)], name="verdict3")

# ---------------------------------------------------------------- LEVEL 4: the fine print
t4l = P("Level four.")
level(4, "the fine\nprint.", PH + "pexels-4114789.jpg", t4l, P("The fine print.", t4l), focus=(0.4, 0.5), amt=0.3, dark=0.8)
BEATS[-1].ovs.append(Sticker("shocked", 300, 1730, 880, P("turns on you."), rot=6))

t0 = P("First, the deadline.")
beat(t0, TextureBG(), [Note("1. the deadline", 960, 330, t0 + 0.1, size=110, color=WHITE), Note("(2:00)", 960, 500, t0 + 0.5, size=90, color=RED)],
     name="deadline")

t0 = P("In 1996,")
beat(t0, Receipt("ansfield1996_pubmed",
                 [dict(t=t0, at="Ironic effects of sleep urgency", s=1.3, dy=60),
                  dict(t=P("One group of normal sleepers"), at="fall asleep as quickly as they could", s=1.35)],
                 [dict(phrase="1996 Jul", t=t0 + 0.1, kind="circle"),
                  dict(phrase="Ironic effects of sleep urgency", t=P("Wegner's lab") + 0.1),
                  dict(phrase="fall asleep as quickly as they could", t=P("fall asleep as fast as you can.") - 0.2)],
                 tag="Ansfield, Wegner & Bowser, 1996 · Behaviour Research and Therapy"),
     [Note("something mean", 1450, 180, P("tried something mean."), size=70),
      Sticker("smug", 300, 1730, 880, P("tried something mean.") + 0.2, rot=8)], name="r_ansfield")
cue(t0, "paper_slide", 0.8)

t0 = P("With calm music on,"); t_loud = P("With loud marching music on,")
beat(t0, TextureBG(), [Pasted(PH + "pexels-2563040.jpg", 700, 520, 360, t0 + 0.05, rot=-3),
                       Note("calm music", 520, 650, t0 + 0.2, size=70, color=WHITE),
                       Note("trying → faster ✓", 520, 760, P("The racers fell asleep faster."), size=64),
                       Pasted(PH + "pexels-14611706.jpg", 700, 1400, 360, t_loud, rot=3),
                       Note("loud marching music", 1400, 650, t_loud + 0.3, size=70, color=WHITE),
                       Note("trying → slower ✗", 1400, 760, P("it flipped.") + 0.2, size=64, color=RED)],
     shakes=[P("it flipped.")], name="music_split")

t0 = P("The ones racing took longer")
beat(t0, Receipt("ansfield1996_pubmed", [dict(t=t0, at="sleep onset latency was greater", s=1.35)],
                 [dict(phrase="John Philip Sousa marches", t=t0 + 0.1),
                  dict(phrase="sleep onset latency was greater", t=P("took longer", t0) + 0.2)],
                 tag="Ansfield, Wegner & Bowser, 1996 · Behaviour Research and Therapy"),
     [Note("racing = slower", 1450, 190, P("weren't trying."), size=70, color=RED)], name="r_ansfield2")

t0 = P("Translation?", P("weren't trying."))
beat(t0, TextureBG(), [Note("quiet head + effort = fine", 960, 230, P("effort is fine."), size=76, color=WHITE),
                       Note("busy head + effort = slower", 960, 380, P("effort backfires."), size=76, color=RED),
                       Note("(at 1 a.m., your head is busy)", 960, 560, P("you wouldn't be timing yourself"), size=60),
                       Sticker("deadpan", 300, 1730, 880, P("timing yourself") + 0.4, rot=6)], name="translation4")

t0 = P("Speaking of timing.")
beat(t0, PhotoBG(PH2 + "pexels-6943418.jpg", focus=(0.5, 0.6), amt=0.35, z=(1.0, 1.06)),
     [Note("speaking of timing…", 600, 220, t0 + 0.1, size=80, color=WHITE, rot=-3)], name="timing")

t0 = P("In a 2007 study,")
beat(t0, Receipt("tang2007_pubmed",
                 [dict(t=t0, at="Sleeping with the enemy", s=1.3, dy=60),
                  dict(t=P("keep an eye on a clock"), at="monitor or not to monitor a clock", s=1.35),
                  dict(t=P("worried more,"), at="reported more pre-sleep worry", s=1.35)],
                 [dict(phrase="2007 Mar", t=t0 + 0.1, kind="circle"),
                  dict(phrase="Sleeping with the enemy", t=t0 + 0.5),
                  dict(phrase="monitor or not to monitor a clock", t=P("keep an eye on a clock") + 0.2),
                  dict(phrase="reported more pre-sleep worry", t=P("worried more,")),
                  dict(phrase="longer sleep onset latency", t=P("took longer to fall asleep.")),
                  dict(phrase="both good and poor sleepers", t=P("Good sleepers too."))],
                 tag="Tang, Schmidt & Harvey, 2007 · J. Behav. Ther. Exp. Psychiatry"),
     [Note("the enemy = the clock", 1450, 180, P("keep an eye on a clock") + 0.4, size=64)], name="r_tang")
cue(t0, "paper_slide", 0.8)

t0 = P("A two-minute timer")
beat(t0, PhotoBG(PH + "pexels-4114789.jpg", focus=(0.4, 0.5), amt=0.3, z=(1.0, 1.08)),
     [Note("2:00 = an exam", 470, 200, P("turns sleep into an exam."), size=96, rot=-3),
      Note("nobody relaxes\nduring an exam.", 470, 380, P("Nobody relaxes"), size=66, color=WHITE),
      Sticker("panic", 300, 1730, 880, P("Nobody relaxes") + 0.4, rot=6)], name="exam")

t0 = P("Second, relaxation")
beat(t0, TextureBG(), [Note("2. relaxation isn't the star", 960, 330, t0 + 0.1, size=96, color=WHITE),
                       Sticker("sad", 300, 960, 600, P("the star of the show.") , rot=-5)], name="not_the_star")

t0 = P("A 2024 analysis")
beat(t0, Receipt("furukawa2024_pubmed",
                 [dict(t=t0, at="Components and Delivery Formats of Cognitive Behavioral Therapy", s=1.15, dy=60),
                  dict(t=P("241 trials"), at="241 trials were identified", s=1.3),
                  dict(t=P("Relaxation? Adding it"), at="relaxation procedures were found to be potentially counterproductive", s=1.3)],
                 [dict(phrase="2024 Apr", t=t0 + 0.1, kind="circle"),
                  dict(phrase="Components and Delivery Formats of Cognitive Behavioral Therapy", t=t0 + 0.5),
                  dict(phrase="241 trials were identified", t=P("241 trials") + 0.1),
                  dict(phrase="cognitive restructuring", t=P("changing the thoughts")),
                  dict(phrase="stimulus control", t=P("and stimulus control,")),
                  dict(phrase="relaxation procedures were found to be potentially counterproductive", t=P("Adding it didn't help"))],
                 tag="Furukawa et al., 2024 · JAMA Psychiatry"),
     [Note("31,000+ people", 1450, 180, P("31,000 people"), size=64, t_out=P("Relaxation? Adding it")),
      Note("didn't help (on average)", 1430, 180, P("didn't help on average."), size=64, color=RED),
      Note("(not certain)", 1430, 290, P("couldn't be sure."), size=56, color=WHITE)], name="r_furukawa")
cue(t0, "paper_slide", 0.8)

t0 = P("Third, the good news.")
beat(t0, TextureBG(), [Note("3. the good news", 960, 230, t0 + 0.1, size=96),
                       Big("2 minutes was\nnever the goal.", 960, 540, P("Two minutes was never the goal."), size=150)], name="good_news")

t0 = P("A National Sleep Foundation")
beat(t0, Receipt("ohayon2017_pubmed",
                 [dict(t=t0, at="sleep quality recommendations", s=1.3, dy=60),
                  dict(t=P("looked at what good sleep"), at="appropriate indicators of good sleep quality", s=1.35)],
                 [dict(phrase="2017 Feb", t=t0 + 0.1, kind="circle"),
                  dict(phrase="sleep quality recommendations", t=t0 + 0.6),
                  dict(phrase="appropriate indicators of good sleep quality", t=P("good sleep looks like.") - 0.2)],
                 tag="Ohayon et al., 2017 · Sleep Health (National Sleep Foundation)"), name="r_ohayon")
cue(t0, "paper_slide", 0.8)

t0 = P("For adults,"); t30 = P("30. You've been"); t2s = P("trying to score 2.")
beat(t0, TextureBG(), [Note("adults:", 960, 150, t0 + 0.05, size=70, color=WHITE),
                       Note("good sleep: asleep within 30 min ✓", 960, 280, P("within 30 minutes"), size=76),
                       Note("poor: 45+ min", 960, 410, P("45 minutes or more"), size=76, color=RED),
                       Big("30", 720, 640, t30, size=240, color=YEL),
                       Note("2", 1250, 640, t2s, size=200, color=WHITE), Strike(1190, 1310, 640, t2s + 0.35, color=RED, width=11)],
     punch=[(t30, 1.06)], shakes=[t30], name="thirty")

t0 = P("And if you do fall asleep")
beat(t0, PhotoBG(PH2 + "pexels-6944002.jpg", focus=(0.5, 0.5), amt=0.5, z=(1.0, 1.05)),
     [Note("2 min, every single night?", 960, 200, t0 + 0.3, size=80, color=WHITE)], name="every_night")

t0 = P("In sleep labs,")
beat(t0, Receipt("arand2005_pubmed",
                 [dict(t=t0, at="The clinical use of the MSLT and MWT", s=1.3, dy=60),
                  dict(t=P("And people fall asleep faster"), at="MSL are generally lower following sleep loss", s=1.4)],
                 [dict(phrase="2005 Jan", t=t0 + 0.1, kind="circle"),
                  dict(phrase="The clinical use of the MSLT and MWT", t=P("one way they measure sleepiness.") - 0.3),
                  dict(phrase="MSL are generally lower following sleep loss", t=P("after losing sleep.") - 0.4)],
                 tag="Arand et al., 2005 · Sleep"),
     [Note("MSL = average minutes to fall asleep", 1380, 180, P("how fast you fall asleep"), size=56),
      Note("fast = tired?", 1450, 300, P("after losing sleep."), size=80, color=RED)], name="r_arand")
cue(t0, "paper_slide", 0.8)

t0 = P("So instant sleep"); t_debt = P("It might be sleep debt.")
sw = hand("superpower?", 110, WHITE, rot=-2).width
beat(t0, TextureBG(), [Note("superpower?", 960, 300, t0 + 0.1, size=110, color=WHITE, rot=-2),
                       Strike(960 - sw / 2, 960 + sw / 2, 300, t_debt - 0.25, color=RED, width=11),
                       Big("sleep debt.", 960, 560, t_debt, size=190, color=YEL)], shakes=[t_debt], name="sleep_debt")

t0 = P("Which brings us back")
rw = hand("relaxed?", 100, WHITE, rot=-3).width
beat(t0, PhotoBG(PH + "pexels-27057738.jpg", focus=(0.6, 0.5), amt=0.25, z=(1.05, 1.1)),
     [Note("my guess:", 1500, 160, P("My guess?"), size=64),
      Note("relaxed?", 520, 230, P("They weren't relaxed."), size=100, color=WHITE, rot=-3),
      Strike(520 - rw / 2, 520 + rw / 2, 230, P("They were exhausted.") - 0.2, color=RED, width=11),
      Note("exhausted.", 560, 400, P("They were exhausted."), size=130, color=RED, rot=-2),
      Note("(there was a war on)", 560, 560, P("There was a war on."), size=64, color=WHITE),
      Sticker("deadpan", 300, 1730, 880, P("There was a war on.") + 0.3, rot=6)], name="pilots_exhausted")

# ---------------------------------------------------------------- WHAT ACTUALLY HELPS
t0 = P("So, can you really", P("There was a war on."))
beat(t0, TextureBG(), [Note("2 minutes, on command, every night?", 960, 220, P("On command,"), size=72, color=WHITE),
                       Note("probably not.", 960, 380, P("Probably not."), size=120, rot=-2),
                       Note("(and you don't need to)", 960, 530, P("And you don't need to."), size=70, color=WHITE)], name="answer")

t0 = P("That's the answer."); t_n = P("The number to remember")
beat(t0, TextureBG(), [Note("that's the answer.", 960, 160, t0 + 0.05, size=70, color=WHITE),
                       Big("the number\nis 30.", 960, 480, t_n, size=190, color=YEL)], shakes=[t_n], name="number30")

t0 = P("Here's what to keep.")
beat(t0, TextureBG(), [Note("what to keep:", 960, 420, t0 + 0.05, size=120, color=WHITE)], name="keep")

t0 = P("Do the relaxing part.")
beat(t0, PhotoBG(PH + "pexels-3771069.jpg", focus=(0.5, 0.45), amt=0.5, dark=0.6, z=(1.0, 1.06)),
     [Note("do the relaxing part", 620, 180, t0 + 0.05, size=84, rot=-3),
      Note("face · shoulders · breath · legs", 620, 300, P("Face, shoulders,"), size=56, color=WHITE),
      Note("relaxation, not a race ✓", 620, 420, P("not a race."), size=66)], name="tip_relax")

t0 = P("Hide the clock.")
beat(t0, PhotoBG(PH2 + "pexels-6943418.jpg", focus=(0.5, 0.6), amt=0.35, z=(1.0, 1.06)),
     [Note("hide the clock ✓", 600, 240, t0 + 0.05, size=92, rot=-3)], name="tip_clock")

t0 = P("Swap")
dw = hand("\"don't think\"", 80, WHITE, rot=-2).width
beat(t0, PhotoBG(PH2 + "pexels-6046594.jpg", focus=(0.5, 0.5), amt=0.3, z=(1.0, 1.06)),
     [Note("\"don't think\"", 520, 200, t0 + 0.1, size=80, color=WHITE, rot=-2),
      Strike(520 - dw / 2, 520 + dw / 2, 200, t0 + 0.6, color=RED, width=10),
      Note("→ one detailed picture", 700, 330, P("one specific, detailed picture."), size=80),
      Note("a walk you know well", 1400, 520, P("A walk you know well."), size=64, color=WHITE),
      Note("a room you could draw", 1400, 640, P("A room you could draw"), size=64, color=WHITE)], name="tip_picture")

t0 = P("And if you're lying there")
beat(t0, PhotoBG(PH2 + "pexels-10969601.jpg", focus=(0.5, 0.5), amt=0.35, z=(1.0, 1.06)),
     [Note("wide awake for ages?", 640, 170, t0 + 0.2, size=76, color=WHITE, rot=-2),
      Note("get up.", 640, 290, P("get up."), size=110, rot=-3),
      Note("something boring · dim light", 640, 430, P("Something boring,"), size=60, color=WHITE),
      Note("back when sleepy", 640, 540, P("back to bed when you're sleepy."), size=66, color=WHITE),
      Note("stimulus control (ep 2)", 640, 670, P("That's stimulus control,"), size=60)], name="tip_get_up")

STRONG = ("We recommend that clinicians use multicomponent cognitive behavioral therapy for insomnia for the treatment of "
          "chronic insomnia disorder in adults. (STRONG)")
t0 = P("If this keeps happening")
beat(t0, Receipt("edinger2021_aasm_guideline", [dict(t=t0, at=STRONG, s=1.15)],
                 [dict(phrase=STRONG, t=P("strongest recommendation") - 0.1, dur=1.0)], tag="AASM clinical practice guideline, 2021"),
     [Note("talk to a doctor.", 1450, 180, P("talk to a doctor."), size=76),
      Note("CBT-I", 1450, 310, P("CBT-I."), size=120, rot=4)], name="r_cbti")
cue(t0, "paper_slide", 0.8)

t0 = P("Not a better trick.")
beat(t0, TextureBG(), [Big("not a better\ntrick.", 960, 440, t0 + 0.15, size=170), Sticker("deadpan", 300, 1730, 880, t0 + 0.6, rot=6),
                       Note("general information, not medical advice.", 960, 760, P("This is general information,"), size=50, color=WHITE)],
     name="not_a_trick")

# ---------------------------------------------------------------- CTA outro (Ep 1 audio) + end screen
beat(T_VO_END + 0.25, TextureBG(), [Sticker("cool", 520, 620, 520, C2(175.26), rot=-4),
                                    Note("subscribe", 1320, 330, C2(177.0), size=110), Circle(1320, 330, 250, 90, C2(177.3), color=YEL),
                                    Note("next midnight question?\n→ comments", 1320, 560, C2(181.66), size=66, color=WHITE),
                                    Note("(before your food gets cold)", 1320, 740, C2(184.66), size=52, color=WHITE)], name="cta_out")
beat(T_END_SCREEN, PhotoBG(KIT + "brand/end_screen_1920x1080.png", grade=False, z=(1.0, 1.0)), name="end_screen")

# ---------------------------------------------------------------- captions never cover our text (lift the bottom row)
STILL_IN_CAPTION_ZONE = caption_safe(BEATS)

# ---------------------------------------------------------------- close the beats + auto SFX from overlays
for a, b in zip(BEATS, BEATS[1:]): a.t1 = b.t0
BEATS[-1].t1 = T_END
for b in BEATS:
    for o in b.ovs:
        k = type(o).__name__
        if k in ("Note",): cue(o.t_in, "marker_write", 0.35)
        elif k in ("Circle", "Underline", "Strike", "Tick", "Arrow", "Bar", "Line"): cue(o.t_in, "marker_squeak", 0.4)
        elif k in ("Sticker", "Pasted", "Card"): cue(o.t_in, "sticker_slap", 0.6)
        elif k == "Big": cue(o.t_in, "impact_soft", 0.55)
    if isinstance(b.bg, Receipt):
        for m in b.bg.marks:
            cue(m["t"], "highlighter" if m.get("kind", "hl") == "hl" else "marker_squeak", 0.45)
CUES.sort()

if __name__ == "__main__":
    print(len(BEATS), "beats,", len(CUES), "sfx cues, ends", round(T_END, 2), "| still in caption zone:", STILL_IN_CAPTION_ZONE)
    for i, b in enumerate(BEATS):
        print(f"{i:02d} {b.t0:7.2f}-{b.t1:7.2f} ({b.t1 - b.t0:5.2f}s) {b.name:16s} {type(b.bg).__name__:9s} {len(b.ovs)} ov")
    bad = [(i, b.name) for i, b in enumerate(BEATS) if b.t1 <= b.t0]
    assert not bad, f"non-positive beats: {bad}"
