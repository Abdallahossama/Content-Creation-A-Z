"""Ep 2 beat list: one visual per line of the script, every overlay keyed to a word in the voiceover.
BEATS (ordered, contiguous) + CUES (sound effects) are imported by render_beats.py and mix_audio.py."""
from ep02_fx import *

def P(phrase, after=0.0):
    """final-timeline time of `phrase` (first occurrence at/after timeline second `after`)"""
    return T(find(phrase, after if after <= S_CUT else after - O1))
def PE(phrase, after=0.0):
    return T(find_end(phrase, after if after <= S_CUT else after - O1))
def C1(t): return T_CTA_IN + t - CTA_IN[0]          # Ep 1 VO time inside the CTA intro -> timeline
def C2(t): return T_CTA_OUT + t - CTA_OUT[0]

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

FAN_GRADE = "eq=saturation=0.45:contrast=1.15,colorlevels=romax=0.36:gomax=0.42:bomax=0.62"
BEATS, CUES = [], []          # CUES: (timeline_s, sfx_name, gain)
def beat(t0, bg, ovs=(), punch=(), shakes=(), name=""):
    BEATS.append(Beat(t0, bg, ovs, punch, shakes, name))
def cue(t, name, g=1.0): CUES.append((t, name, g))

def level(n, title, photo, t_n, t_title, focus=(0.5, 0.5), x=760, amt=0.3, dark=0.8, mirror=False, video=None):
    bg = video or PhotoBG(photo, focus=focus, amt=amt, z=(1.0, 1.04), dark=dark, mirror=mirror)
    beat(t_n, bg, [Note(f"level {n}", x + 140, 270, t_n + 0.05, size=88), Underline(x + 20, x + 260, 322, t_n + 0.25),
                   Big(title, x, 360, t_title, size=180, anchor="lt")], shakes=[t_title], name=f"level{n}")
    cue(t_n, "riser_short", 0.6); cue(t_title, "impact_soft", 0.8)

# ---------------------------------------------------------------- COLD OPEN
beat(0.0, VideoBG(VID + "pexels-6943545-hd_2048_1080_25fps.mp4", z=1.04),
     [Note("1:07 a.m.", 330, 200, P("1 a.m.") + 0.15, size=100, rot=-4),
      Arrow((360, 300), (1060, 840), P("1 a.m.") + 0.5, bend=0.42, seed=3),          # bows under the face to the phone
      Note("vol. 4", 380, 560, P("volume") + 0.1, size=84, rot=3), Circle(385, 560, 150, 82, P("volume") + 0.4, color=YEL)],
     punch=[(P("You're barely listening."), 1.12)], name="cold_open")
cue(0.0, "room_tone", 0.5); cue(0.05, "muffled_doc", 0.55)

t0 = P("But turn him off,")
t_off = PE("him off,") - 0.15
beat(t0, TextureBG(), [Line([(960, 70), (966, 850)], t0), Note("video on", 480, 150, t0, size=92),
                       Sticker("sleepy", 560, 480, 560, t0 + 0.05, rot=-4), Note("z z z", 740, 330, t0 + 0.35, size=70, color=WHITE, rot=-10),
                       Note("video off", 1440, 150, t_off, size=92, rot=2), Sticker("panic", 560, 1440, 560, t_off + 0.05, rot=5)],
     shakes=[t_off], name="meme_on_off")
cue(t_off, "record_scratch", 0.7)

t0 = P("So why can't you"); t_why = P("why", t0 - 0.1)
beat(t0, PhotoBG(PH + "pexels-6943425.jpg", focus=(0.5, 0.42), amt=0.5, z=(1.0, 1.07)),
     [Big("why?", W / 2, H / 2 - 40, t_why, size=330)], shakes=[t_why], name="why")
cue(t_why, "impact_soft", 0.9)

t0 = P("Short answer:")
beat(t0, TextureBG(), [Note("you're not broken.", 960, 260, P("you're not broken.") + 0.1, size=92, color=WHITE, rot=-2),
                       Big("the deal.", 960, 540, P("made a deal."), size=210),
                       Note("*fine print", 1240, 770, P("fine print."), size=86, rot=-4), Underline(1040, 1440, 830, P("fine print.") + 0.3),
                       Sticker("smug", 300, 1680, 800, PE("fine print.") - 0.1, rot=8)], name="deal")

t0 = P("And at the end,")
beat(t0, PhotoBG(PH + "pexels-6944002.jpg", focus=(0.6, 0.5), amt=0.55, z=(1.0, 1.05)),
     [Note("the verdict →", 470, 230, P("sleep doctors", t0) + 0.1, size=92), Underline(250, 700, 300, P("sleep doctors", t0) + 0.45),
      Sticker("sideeye", 330, 1660, 790, P("You won't love it."), rot=-6, mirror=True)], name="verdict_tease")

# ---------------------------------------------------------------- CTA intro (Ep 1 audio)
beat(S_CUT, PhotoBG(PH + "pexels-6327595.jpg", focus=(0.5, 0.5), amt=0.25, z=(1.0, 1.08)),
     [Note("20 min of scrolling", 1420, 230, C1(19.70), size=84, color=WHITE, rot=-3),
      Note("cold.", 520, 820, C1(23.80), size=130, color=WHITE, rot=-7)], name="cta_food")
beat(C1(24.96), VideoHold(KIT + "brand/intro_sting.mp4"), [Note("midnight questions, answered.", 1300, 860, C1(26.68), size=60, color=WHITE, rot=-2),
                                                         Note("press play. eat.", 520, 900, C1(29.58), size=70, rot=-4)], name="cta_sting")
beat(C1(31.30), TextureBG(), [Sticker("cool", 560, 640, 560, C1(31.30), rot=-4),
                              Note("subscribe", 1300, 430, C1(31.35), size=120), Circle(1300, 430, 270, 95, C1(31.65), color=YEL),
                              Note("so you don't have to search next time", 1300, 640, C1(32.0), size=46, color=WHITE)], name="cta_sub")
cue(C1(24.96), "whoosh_long", 0.6)

# ---------------------------------------------------------------- THE PLAN
t0 = P("Here's the plan."); t4 = P("Four levels."); t_last = P("turns on you.")
cells = [(480, 250), (1440, 250), (480, 630), (1440, 630)]          # grid kept above the caption zone
labels = ["silence", "noise", "the ritual", "the fine print"]
ovs = [Line([(960, 50), (962, 830)], t0), Line([(60, 440), (1860, 445)], t0 + 0.1)]
for i, ((x, y), lab) in enumerate(zip(cells, labels)):
    ti = t4 + 0.25 * i if i < 3 else t_last
    ovs += [Note(str(i + 1), x - 330, y - 130, ti, size=96, rot=-5), Note(lab, x + 160, y + 110, ti + 0.1, size=58, color=WHITE),
            Sticker("cool" if i < 3 else "panic", 260, x - 60, y, ti, rot=[-6, 4, -3, 7][i])]
ovs += [Circle(1440, 640, 400, 185, t_last + 0.3, color=RED, width=12)]
beat(t0, TextureBG(), ovs, shakes=[t_last], name="plan")

# ---------------------------------------------------------------- LEVEL 1
level(1, "silence\nis loud.", STOCK1 + "pexels-460918.jpg", P("Level one."), P("Silence is loud."), amt=0.22, dark=1.0)

t0 = P("In a quiet room,")
beat(t0, VideoBG(VID + "pexels-6944078-hd_2048_1080_25fps.mp4", z=1.0),
     [Note("that email from 2019", 1460, 230, P("Except think about you."), size=78, rot=-3),
      Arrow((1380, 320), (1170, 560), P("Except think about you.") + 0.4, bend=0.3)], name="quiet_room")

t0 = P("In psychologist Allison"); t_thr = P("scanning for threats.")
beat(t0, Receipt("harvey2002_pubmed",
                 [dict(t=t0, at="A cognitive model of insomnia", s=1.30, dy=60), dict(t=t_thr, at="sleep-related threat cues", s=1.35)],
                 [dict(phrase="A cognitive model of insomnia", t=P("model of insomnia,") - 0.2),
                  dict(phrase="2002 Aug", t=P("Harvey's") + 0.1, kind="circle"),
                  dict(phrase="sleep-related threat cues", t=t_thr + 0.3)], tag="Harvey, 2002 · Behaviour Research and Therapy"),
     [Note("worry → alert → scanning", 1350, 880, t_thr + 0.9, size=60, rot=-3)], name="r_harvey")
cue(t0, "paper_slide", 0.8); cue(t_thr, "whoosh_fast", 0.4)

t0 = P("Every creak."); t_fs = P("Every footstep."); t_hb = P("Your own heartbeat,")
beat(t0, PhotoBG(PH + "pexels-147634.jpg", focus=(0.6, 0.5), amt=0.4, z=(1.0, 1.1)),
     [Note("creak?", 520, 300, t0 + 0.1, size=100, rot=-6), Note("footsteps??", 600, 560, t_fs + 0.1, size=100, rot=4),
      Note("ba-dum.", 640, 820, t_hb + 0.1, size=110, color=RED, rot=-3)], punch=[(t_hb, 1.1)], name="creak")
cue(t0, "creak", 0.9); cue(t_fs, "footsteps", 0.9); cue(t_hb, "heartbeat", 1.0)

t0 = P("So is \"just think"); t_t = P("Harvey tested that too.")
beat(t0, TextureBG(), [Note("\"just think about\nsomething else\"", 820, 420, t0 + 0.2, size=100, color=WHITE, rot=-2),
                       Note("?", 1500, 380, P("enough?") , size=260, color=RED, rot=8),
                       Sticker("deadpan", 330, 1690, 760, t_t, rot=6)], name="just_think")

t0 = P("In a 2002 Oxford study,")
beat(t0, Receipt("harvey_payne2002_pubmed",
                 [dict(t=t0, at="distraction with imagery versus general distraction", s=1.25, dy=40),
                  dict(t=P("41 people"), at="Forty one people with insomnia", s=1.35)],
                 [dict(phrase="2002 Mar", t=P("2002 Oxford") + 0.1, kind="circle"),
                  dict(phrase="distraction with imagery versus general distraction", t=t0 + 0.6),
                  dict(phrase="Forty one people with insomnia", t=P("41 people") + 0.2)], tag="Harvey & Payne, 2002 · Oxford"), name="r_payne")
cue(t0, "paper_slide", 0.8)

t0 = P("Some got no instructions."); t2 = P("Some were told"); t3 = P("And some were trained"); t_f = P("fell asleep faster")
beat(t0, TextureBG(), [Note("no\ninstructions", 340, 330, t0 + 0.1, size=84, color=WHITE),
                       Note("\"distract\nyourself\"", 960, 330, t2 + 0.1, size=84, color=WHITE),
                       Note("picture one\nspecific scene", 1580, 330, t3 + 0.1, size=84, color=YEL),
                       Line([(650, 160), (655, 760)], t0), Line([(1270, 160), (1272, 760)], t0 + 0.1),
                       Tick(1600, 640, t_f, size=110), Note("fell asleep faster", 1580, 850, t_f + 0.2, size=64, rot=-3)],
     shakes=[t_f], name="three_groups")

t0 = P("The researchers' explanation:")
beat(t0, Receipt("harvey_payne2002_pubmed", [dict(t=t0, at="cognitive space", s=1.45)],
                 [dict(phrase="cognitive space", t=P("cognitive space\"") - 0.1)], tag="Harvey & Payne, 2002 · Oxford"),
     [Note("worries can't\nget back in", 1450, 860, P("worries can't") + 0.1, size=64, rot=-3)], name="r_space")
cue(t0, "paper_slide", 0.6)

t0 = P("My guess?")
beat(t0, VideoBG(VID + "pexels-6943545-hd_2048_1080_25fps.mp4", start=3.0, z=1.0),
     [Note("my guess:", 260, 160, t0 + 0.05, size=70, color=WHITE, rot=-4),
      Note("one specific,\nmildly interesting\nthing", 380, 470, P("One specific, mildly") + 0.2, size=76, rot=-3),
      Arrow((560, 640), (1050, 790), P("thing to follow.") , bend=-0.2)], name="my_guess")

t0 = P("It's not entertainment.")
beat(t0, PhotoBG(PH + "pexels-2990765.jpg", focus=(0.55, 0.5), amt=0.3, z=(1.0, 1.06)),
     [Note("the video", 1190, 250, P("It's a bouncer") + 0.1, size=96, rot=-4), Arrow((1190, 320), (1180, 520), P("bouncer") + 0.2, bend=0.1),
      Note("your thoughts", 380, 760, P("for your thoughts.") + 0.05, size=84, color=WHITE, rot=3),
      Strike(160, 600, 830, P("for your thoughts.") + 0.5, color=RED)], name="bouncer")

t0 = P("If you saw our last episode,")
beat(t0, TextureBG(), [Pasted("D:/why habibi/1st video/claude_package/thumbnails/real_1_NOT_AGAIN.png", 900, 820, 500, t0 + 0.1, rot=-3),
                       Note("ep 1", 1480, 230, t0 + 0.4, size=110, rot=6), Arrow((1460, 320), (1270, 420), t0 + 0.6),
                       Note("3 a.m. cringe: outside.", 1460, 900, P("cringe outside.") , size=64, color=WHITE, rot=-3)], name="ep1_callback")

# ---------------------------------------------------------------- LEVEL 2
level(2, "the noise\nblanket.", PH + "pexels-6000684.jpg", P("Level two."), P("The noise blanket."), focus=(0.6, 0.5), amt=0.55, dark=0.62)

t0 = P("A steady sound hides")
beat(t0, VideoBG(VID + "pexels-5090504-hd_1280_720_30fps.mp4", z=1.0, grade=False), [], name="fan_video")
BEATS[-1].bg.GRADE = FAN_GRADE; BEATS[-1].bg.grade = True
BEATS[-1].ovs += [Note("steady sound", 420, 900, t0 + 0.3, size=80, color=WHITE, rot=-2)]

t0 = P("A door."); beat(t0, PhotoBG(PH + "pexels-147634.jpg", focus=(0.75, 0.5), amt=0.4, z=(1.08, 1.12)),
                       [Note("door.", 560, 540, t0 + 0.05, size=120, color=WHITE, rot=-5)], name="door")
cue(t0, "door", 0.9)
t0 = P("A car."); beat(t0, VideoBG(VID + "pexels-7628845-hd_1920_1080_25fps.mp4", z=1.0),
                      [Note("car.", 960, 300, t0 + 0.05, size=120, color=WHITE, rot=4)], name="car")
cue(t0, "car_pass", 0.8)
t0 = P("Your neighbor's very important")
beat(t0, PhotoBG(PH + "pexels-7793122.jpg", focus=(0.5, 0.4), amt=0.3, z=(1.0, 1.06), dark=0.72),
     [Note("very important", 520, 200, P("very important") + 0.1, size=84, rot=-4), Underline(300, 760, 270, P("phone call.")),
      Note("(it's 1 a.m.)", 1500, 900, P("phone call.") + 0.3, size=60, color=WHITE, rot=-3)], name="neighbor")
cue(t0, "phone_ring", 0.6)

t0 = P("There's a study that shows"); t_h = P("Unfortunately,")
beat(t0, Receipt("stanchina2005_pubmed", [dict(t=t0, at="The influence of white noise on sleep in subjects exposed to ICU noise", s=1.2, dy=80)],
                 [dict(phrase="The influence of white noise on sleep in subjects exposed to ICU noise", t=t0 + 0.6),
                  dict(phrase="2005 Sep", t=P("In 2005,"), kind="circle")], tag="Stanchina et al., 2005 · Sleep Medicine"),
     [Note("a handful = 4-5 people", 1350, 880, t_h + 0.5, size=66, rot=-3), Sticker("deadpan", 300, 1720, 640, t_h + 0.2, rot=6)], name="r_stanchina")
cue(t0, "paper_slide", 0.8)

t0 = P("Their sleep got interrupted"); t48 = P("about 48"); t13 = P("about 13"); t16 = P("about 16.")
beat(t0, TextureBG(), [Note("sleep interruptions per hour", 960, 120, t0 + 0.1, size=66, color=WHITE),
                       Bar(380, 740, 260, 120, t13, color=WHITE, num="13", label="normal night"),
                       Bar(830, 740, 260, 440, t48, color=RED, num="48", label="hospital noise"),
                       Bar(1280, 740, 260, 150, t16, color=YEL, num="16", label="+ white noise"),
                       Note("(5 people. 1 lab.)", 1640, 300, t16 + 0.6, size=50, color=WHITE, rot=-2)],
     shakes=[t48], name="bars")
cue(t48, "impact_soft", 0.6)

t0 = P("The surprise?"); t_jump = P("It was the jump."); t_raise = P("White noise raises")
beat(t0, TextureBG(), [Line([(160, 760), (700, 765), (760, 300), (820, 762), (1760, 760)], t0 + 0.3, color=WHITE, width=10),
                       Note("not how loud…", 1250, 260, P("It wasn't how loud") + 0.1, size=76, color=WHITE, rot=-3),
                       Note("the JUMP", 980, 430, t_jump + 0.1, size=110, rot=-5), Arrow((790, 740), (790, 330), t_jump + 0.3, color=RED, width=12, bend=0.0),
                       Line([(160, 640), (1760, 645)], t_raise + 0.2, color=YEL, width=26),
                       Note("background ↑   jump ↓", 1220, 900, t_raise + 0.6, size=70, rot=-2)], name="jump")

t0 = P("That's the whole idea behind")
beat(t0, PhotoBG(PH + "pexels-6000684.jpg", focus=(0.65, 0.5), amt=0.5, z=(1.0, 1.06), dark=0.7),
     [Note("white noise machine\n(basically)", 560, 300, t0 + 0.3, size=80, rot=-3)], name="wn_machine")

t0 = P("So it works?")
beat(t0, TextureBG(), [Sticker("sideeye", 480, 600, 560, P("Well.") , rot=-5),
                       Note("tiny lab study", 1380, 380, P("A tiny lab study") + 0.1, size=84, color=WHITE, rot=-3),
                       Note("≠", 1380, 520, P("is not your bedroom.") , size=120, color=RED),
                       Note("your bedroom", 1380, 660, P("your bedroom.") , size=84, color=WHITE, rot=2)], name="tiny_lab")

t0 = P("A 2021 review looked at")
beat(t0, Receipt("riedy2021_pubmed",
                 [dict(t=t0, at="Noise as a sleep aid", s=1.3, dy=80), dict(t=P("38 studies"), at="38 included articles", s=1.3),
                  dict(t=P("very low quality."), at="continuous noise improving sleep was very low", s=1.3)],
                 [dict(phrase="Noise as a sleep aid", t=t0 + 0.4), dict(phrase="2021 Feb", t=P("2021 review") + 0.1, kind="circle"),
                  dict(phrase="38 included articles", t=P("38 studies") + 0.1, kind="circle"),
                  dict(phrase="continuous noise improving sleep was very low", t=P("very low quality.") + 0.1),
                  dict(phrase="improves or disrupts sleep", t=P("Some studies said it helped.") + 0.3)],
                 tag="Riedy et al., 2021 · Sleep Medicine Reviews"),
     [Note("so... a vibe?", 1460, 900, P("made sleep worse.") + 0.2, size=70, rot=-3)], name="r_riedy")
cue(t0, "paper_slide", 0.8)

t0 = P("The reviewers also flagged")
beat(t0, Receipt("riedy2021_pubmed", [dict(t=t0, at="may also negatively affect sleep and hearing", s=1.4)],
                 [dict(phrase="may also negatively affect sleep and hearing", t=P("great for your hearing.") - 0.3)],
                 tag="Riedy et al., 2021 · Sleep Medicine Reviews"),
     [Sticker("deadpan", 300, 1700, 800, P("your hearing.") , rot=7)], name="r_hearing")

t0 = P("So white noise isn't"); t_v = P("It's a vibe.")
beat(t0, TextureBG(), [Note("proven sleep aid", 960, 330, t0 + 0.3, size=96, color=WHITE, rot=-2), Strike(600, 1320, 340, t_v - 0.2),
                       Big("it's a vibe.", 960, 620, t_v, size=200), Sticker("cool", 300, 1650, 860, t_v + 0.2, rot=-6)],
     shakes=[t_v], name="vibe")

# ---------------------------------------------------------------- LEVEL 3
level(3, "the ritual.", PH + "pexels-16219497.jpg", P("Level three."), P("The ritual."), amt=0.6, dark=0.5)

t0 = P("In 1972, psychologist"); t_l = P("something you learn.")
beat(t0, TextureBG(), [Note("Richard Bootzin,", 780, 300, t0 + 0.2, size=96, color=WHITE, rot=-2), Note("1972", 1290, 290, P("In 1972,") + 0.1, size=110, rot=-2),
                       Circle(1290, 295, 150, 85, P("In 1972,") + 0.4, color=YEL),
                       Note("falling asleep = something you LEARN", 960, 600, t_l, size=78, rot=-3)], name="bootzin")
t0 = P("The things around you")
beat(t0, PhotoBG(PH + "pexels-6468223.jpg", focus=(0.6, 0.5), amt=0.4, z=(1.0, 1.05)),
     [Pasted(PH + "pexels-20720714.jpg", 380, 330, 380, t0 + 0.1, rot=-6, grade=True),
      Note("ding →", 640, 220, t0 + 0.4, size=96, rot=-4), Note("cue", 1500, 220, P("become cues") , size=100, rot=3),
      Note("it's time.", 1420, 880, P("it's time.", t0) , size=96, color=WHITE, rot=-3)], name="pavlov")
cue(t0 + 0.4, "bell", 0.7)

t0 = P("That idea is still part")
beat(t0, Receipt("edinger2021_aasm_guideline", [dict(t=t0, at="stimulus control", s=1.35)],
                 [dict(phrase="stimulus control", t=t0 + 0.5)], tag="AASM clinical practice guideline, 2021"),
     [Note("50 years later. still used.", 1380, 880, P("therapy today.") , size=66, rot=-3)], name="r_aasm_sc")
cue(t0, "paper_slide", 0.8)

t0 = P("You know who runs"); t_k = P("Toddlers.")
beat(t0, PhotoBG(PH + "pexels-5867248.jpg", focus=(0.5, 0.45), amt=0.35, z=(1.0, 1.06)),
     [Note("toddlers.", 400, 230, t_k, size=120, rot=-6)], name="toddlers")

t0 = P("In a 2015 study of more")
beat(t0, Receipt("mindell2015_pubmed",
                 [dict(t=t0, at="Bedtime routines for young children", s=1.25, dy=80), dict(t=P("10,000"), at="10,085 children", s=1.3)],
                 [dict(phrase="Bedtime routines for young children", t=t0 + 0.4), dict(phrase="10,085 children", t=P("10,000") + 0.1, kind="circle"),
                  dict(phrase="shorter sleep onset latency, reduced night wakings", t=P("falling asleep faster,", t0) + 0.1),
                  dict(phrase="dose-dependent relationship", t=P("And the more nights") + 0.2)],
                 tag="Mindell et al., 2015 · Sleep"),
     [Note("more nights = better", 1420, 900, P("the better.") , size=66, rot=-3)], name="r_mindell")
cue(t0, "paper_slide", 0.8)

t0 = P("Bath."); t_y = P("Yours is:")
bed = PH + "pexels-16219497.jpg"
beat(t0, PhotoBG(bed, amt=0.6, dark=0.45, z=(1.0, 1.04)),
     [Note("bath →", 330, 230, t0, size=90, color=WHITE), Note("book →", 700, 230, P("Book."), size=90, color=WHITE),
      Note("lights out", 1120, 230, P("Lights out."), size=90, color=WHITE), Note("= cue chain", 1600, 230, P("That's a cue chain."), size=80, rot=-4),
      Note("lights off →", 360, 560, P("lights off."), size=84), Note("phone on →", 820, 560, P("Phone on."), size=84),
      Note("a man explains\nthe fall of Rome", 1380, 600, P("A man explains"), size=78),
      Note("same system.", 560, 880, P("Same system."), size=84, color=WHITE, rot=-3),
      Note("worse book.", 1300, 880, P("Worse book."), size=84, color=RED, rot=3), Underline(1100, 1500, 940, P("Worse book.") + 0.3, color=RED)],
     name="cue_chain")
t0 = P("So if a video is there"); t_away = P("Take it away,"); t_sig = P("waits for a signal")
beat(t0, PhotoBG(bed, amt=0.6, dark=0.45, z=(1.04, 1.08)),
     [Note("lights off →", 360, 400, t0 - 0.01, size=84), Note("video →", 800, 400, t0 - 0.01, size=84), Note("sleep", 1180, 400, t0 - 0.01, size=84),
      Strike(660, 940, 410, t_away + 0.1, color=RED, h=50), Note("→ ???", 1180, 640, t_away + 0.6, size=96, color=WHITE)], name="chain_broken")
beat(t_sig - 0.1, PhotoBG(PH + "pexels-16018842.jpg", focus=(0.5, 0.5), amt=0.5, z=(1.0, 1.06), dark=0.78),
     [Note("you, 1 a.m., video off", 960, 960, t_sig + 0.2, size=84, rot=-3)], name="skeletons")

t0 = P("You're not addicted to the video."); t_r = P("You're addicted to the routine.")
beat(t0, TextureBG(), [Big("the video.", 960, 360, t0 + 0.5, size=150, color=WHITE), Strike(620, 1300, 370, P("the video.", t0) + 0.4, h=60),
                       Big("the routine.", 960, 680, PE("addicted to the", t_r - 0.1), size=190, color=YEL),
                       Sticker("sideeye", 300, 1660, 860, t_r + 0.6, rot=6)], name="routine")

# ---------------------------------------------------------------- LEVEL 4
level(4, "the fine\nprint.", PH + "pexels-6943990.jpg", P("Level four."), P("The fine print.", 261), focus=(0.5, 0.5), amt=0.4, dark=0.7, x=700)
t_scr = P("First, the screen.")
BEATS[-1].ovs.append(Note("1. the screen", 1450, 880, t_scr + 0.1, size=76, color=WHITE, rot=-3))

t0 = P("In a 2015 Harvard study,"); t_long = P("took about 10 minutes")
beat(t0, Receipt("chang2015_pubmed",
                 [dict(t=t0, at="Evening use of light-emitting eReaders", s=1.22, dy=80), dict(t=t_long - 0.3, at="took longer to fall asleep", s=1.3, dx=-250)],
                 [dict(phrase="Evening use of light-emitting eReaders", t=t0 + 0.4), dict(phrase="2015 Jan 27", t=P("2015 Harvard") + 0.1, kind="circle"),
                  dict(phrase="took longer to fall asleep", t=t_long + 0.1), dict(phrase="took longer to fall asleep", t=t_long + 0.5, kind="circle"),
                  dict(phrase="reduced next-morning alertness", t=P("felt more tired") + 0.1)], tag="Chang et al., 2015 · PNAS (Harvard)"),
     [Note("+10 min to fall asleep\n(ish)", 640, 220, t_long + 0.8, size=68, t_out=None),
      Sticker("shocked", 300, 1710, 800, P("felt more tired") + 0.3, rot=8)], punch=[(t_long - 0.3, 1.0)], name="r_chang")
cue(t0, "paper_slide", 0.8)

t0 = P("\"Fine.", 276)
beat(t0, PhotoBG(PH + "pexels-6943444.jpg", focus=(0.5, 0.5), amt=0.2, z=(1.0, 1.06), dark=1.4),
     [Note("night mode: ON", 1400, 240, P("night mode.\"") - 0.3, size=90, rot=-4), Tick(1780, 230, P("night mode.\"") + 0.1)], name="night_mode")

t0 = P("In a 2021 study, 167"); t_nd = P("Night Shift made no difference.")
beat(t0, Receipt("duraccio2021_pubmed",
                 [dict(t=t0, at="Does iPhone night shift mitigate", s=1.25, dy=80), dict(t=t_nd - 0.2, at="no differences in sleep outcomes attributable to Night Shift", s=1.3)],
                 [dict(phrase="Does iPhone night shift mitigate", t=t0 + 0.4), dict(phrase="167 emerging adults", t=P("167") + 0.1, kind="circle"),
                  dict(phrase="no differences in sleep outcomes attributable to Night Shift", t=t_nd + 0.1)], tag="Duraccio et al., 2021 · Sleep Health"),
     [Sticker("deadpan", 300, 1700, 800, t_nd + 0.5, rot=7),
      Note("already slept enough?\nno phone won.", 600, 880, P("the no-phone group") , size=62, rot=-3)], name="r_duraccio")
cue(t0, "paper_slide", 0.8)

t0 = P("Second, the light.")
beat(t0, PhotoBG(PH + "pexels-10969601.jpg", focus=(0.5, 0.5), amt=0.25, z=(1.0, 1.05)),
     [Note("2. the light", 480, 220, t0 + 0.1, size=90, rot=-4)], name="light")
t0 = P("In a 2022 Northwestern study,")
beat(t0, Receipt("mason2022_pubmed",
                 [dict(t=t0, at="Light exposure during sleep impairs cardiometabolic function", s=1.22, dy=80),
                  dict(t=P("raised heart rates") - 0.2, at="increases nighttime heart rate", s=1.3)],
                 [dict(phrase="Light exposure during sleep impairs cardiometabolic function", t=t0 + 0.5),
                  dict(phrase="increases nighttime heart rate", t=P("raised heart rates") + 0.1),
                  dict(phrase="next-morning insulin resistance", t=P("handled sugar worse") + 0.1)], tag="Mason et al., 2022 · PNAS (Northwestern)"),
     [Note("1 night. lights on.", 620, 880, P("one night of sleeping") + 0.3, size=66, rot=-3)], name="r_mason")
cue(t0, "paper_slide", 0.8)
t0 = P("A phone isn't a ceiling light.")
beat(t0, PhotoBG(PH + "pexels-10969601.jpg", focus=(0.5, 0.5), amt=0.25, z=(1.05, 1.1)),
     [Note("heart rate ↑", 520, 260, t0 + 0.2, size=90, color=RED, rot=-4), Note("not free.", 1400, 860, P("isn't free.") , size=110, color=WHITE, rot=3)],
     name="not_free")

t0 = P("Third, your ears")
beat(t0, PhotoBG(PH + "pexels-6944002.jpg", focus=(0.4, 0.5), amt=0.55, z=(1.04, 1.1)),
     [Note("3. your ears", 480, 220, t0 + 0.1, size=90, rot=-4), Note("(still on duty)", 520, 330, P("never fully clock out.") , size=64, color=WHITE)], name="ears")
t0 = P("A 2022 study found")
beat(t0, Receipt("ameen2022_pubmed",
                 [dict(t=t0, at="The Brain Selectively Tunes to Unfamiliar Voices during Sleep", s=1.2, dy=80),
                  dict(t=P("unfamiliar voices") - 0.1, at="UFVs elicited more K-complexes and microarousals", s=1.35)],
                 [dict(phrase="The Brain Selectively Tunes to Unfamiliar Voices during Sleep", t=t0 + 0.5),
                  dict(phrase="UFVs elicited more K-complexes and microarousals", t=P("unfamiliar voices") + 0.2)],
                 tag="Ameen et al., 2022 · J Neurosci"),
     [Note("new voice = mini wake-ups", 1380, 880, P("familiar ones.") , size=66, rot=-3)], name="r_ameen")
cue(t0, "paper_slide", 0.8)

t0 = P("So when autoplay swaps")
beat(t0, PhotoBG(STOCK1 + "pexels-11645171.jpg", focus=(0.5, 0.45), amt=0.4, z=(1.0, 1.06)),
     [Circle(560, 590, 120, 170, P("stranger yelling") , color=YEL, tilt=8),
      Note("autoplay just\nswitched to\ncrypto guy", 300, 200, P("autoplay swaps") + 0.2, size=70),
      Arrow((300, 330), (430, 500), P("stranger yelling") + 0.2, bend=0.3)], shakes=[P("your brain notices.")], name="autoplay")
cue(P("stranger yelling"), "glitch_error", 0.5)

t0 = P("Translation?"); t_ch = P("quietly charges you")
lines = ["10 min to fall asleep", "heart rate", "1 a.m. crypto guy"]
ovs = [Note("THE BILL", 1260, 200, t0 + 0.3, size=70, color=NAVY, rot=-2)]
for i, l in enumerate(lines):
    ovs.append(Note(l, 1260, 330 + i * 110, P("The video gets you to sleep,") + 0.4 * i, size=60, color=NAVY, rot=-2))
ovs += [Note("TOTAL: your morning", 1260, 720, t_ch + 0.2, size=70, color=RED, rot=-3), Underline(1000, 1520, 780, t_ch + 0.6, color=RED)]
beat(t0, PhotoBG(PH + "pexels-4959907.jpg", focus=(0.5, 0.5), amt=0.15, z=(1.0, 1.04)), ovs, name="the_bill")
cue(t_ch, "cash_register", 0.6)

t0 = P("And now, the verdict"); t_q = P("What do sleep doctors")
beat(t0, TextureBG(), [Big("the verdict.", 960, 420, t0 + 0.3, size=200), Sticker("cool", 320, 1650, 820, t_q, rot=-6),
                       Note("your Roman Empire guy", 820, 760, P("Roman Empire guy?", t_q) , size=80, rot=-3)], shakes=[t0 + 0.3], name="verdict")
cue(t0 + 0.3, "impact_soft", 0.8)

t0 = P("The American Academy"); t_r1 = P("Go to bed only"); t_r2 = P("If you can't sleep, get out"); t_r3 = P("Use the bed for sleep")
t_tv = P("no reading, no watching TV")
beat(t0, Receipt("edinger2021_aasm_fulltext",
                 [dict(t=t0, at="Behavioral and psychological treatments for chronic insomnia disorder in adults", s=1.15, dy=80),
                  dict(t=t_r1 - 0.2, at="get out of bed when unable to sleep", s=1.35)],
                 [dict(phrase="Behavioral and psychological treatments for chronic insomnia disorder in adults", t=t0 + 0.6),
                  dict(phrase="go to bed only when sleepy", t=t_r1 + 0.1), dict(phrase="get out of bed when unable to sleep", t=t_r2 + 0.3),
                  dict(phrase="no reading, watching TV, etc. in bed", t=t_tv), dict(phrase="no reading, watching TV, etc. in bed", t=t_tv + 0.5, kind="circle")],
                 tag="AASM insomnia guideline, 2021 (full text)"),
     [], name="r_rules")
BEATS[-1].ovs.append(Censor(BEATS[-1].bg, "sex only (no reading", P("and one other thing.") + 0.2, expr="smug", h=170))
cue(t0, "paper_slide", 0.8)

t0 = P("So yes."); t_bed = P("You're probably watching this in bed.")
beat(t0, TextureBG(), [Sticker("sideeye", 760, W / 2, 440, t_bed, rot=0, mirror=False), Note("hi.", 1560, 260, t_bed + 0.5, size=140, rot=8),
                       Note("the guideline\nwould like a word.", 330, 720, P("would like a word.") - 0.6, size=58, color=WHITE)],
     shakes=[t_bed], name="hi")

t0 = P("To be fair,"); t_j = P("If you fall asleep fast")
beat(t0, TextureBG(), [Note("treatment", 620, 380, P("a treatment for chronic") , size=110, color=WHITE, rot=-3),
                       Note("≠", 960, 380, P("Not a law.") - 0.1, size=140, color=RED), Note("law", 1250, 380, P("Not a law."), size=110, color=WHITE, rot=3),
                       Sticker("cool", 340, 960, 640, t_j + 0.2, rot=-4), Note("video: doing its job ✓", 1480, 900, P("doing its job.") , size=60, rot=-3)],
     name="not_a_law")

# ---------------------------------------------------------------- WHAT ACTUALLY HELPS
t0 = P("So, what actually helps?"); t_c = P("make it cheaper.")
beat(t0, TextureBG(), [Note("what actually helps?", 960, 340, t0 + 0.1, size=96, color=WHITE, rot=-2),
                       Big("make it cheaper.", 960, 640, t_c, size=170, color=YEL)], shakes=[t_c], name="helps")
t0 = P("Keep the sound."); beat(t0, PhotoBG(PH + "pexels-16857540.jpg", amt=0.4, z=(1.0, 1.06)),
                               [Note("keep the sound", 600, 240, t0 + 0.05, size=92, rot=-3), Tick(980, 230, t0 + 0.4)], name="tip_sound")
t0 = P("Lose the light."); beat(t0, PhotoBG(PH + "pexels-6940357.jpg", focus=(0.5, 0.55), amt=0.4, dark=0.55, z=(1.0, 1.06)),
                               [Note("lose the light", 600, 240, t0 + 0.05, size=92, rot=-3), Tick(980, 230, t0 + 0.4)], name="tip_light")
t0 = P("Flip the phone over,"); beat(t0, PhotoBG(PH + "pexels-215582.jpg", amt=0.35, z=(1.0, 1.06)),
                                    [Note("flip it", 600, 240, t0 + 0.1, size=100, rot=-3), Tick(860, 230, t0 + 0.5),
                                     Note("or audio only", 1380, 880, P("switch to audio only.") , size=76, color=WHITE), Tick(1720, 870, P("audio only.") )], name="tip_flip")
t0 = P("Keep the volume low."); beat(t0, VideoBG(VID + "pexels-7924639-hd_1920_1080_25fps.mp4", z=1.0),
                                    [Note("vol. 4 → vol. 2", 1450, 250, t0 + 0.1, size=88, rot=-3), Tick(1830, 250, t0 + 0.6),
                                     Note("(your ears. fine print.)", 1450, 380, P("Your ears were") + 0.2, size=60, color=WHITE)], name="tip_volume")
t0 = P("Pick something boring"); beat(t0, PhotoBG(PH + "pexels-6943444.jpg", amt=0.45, z=(1.04, 1.1)),
                                     [Note("a documentary you've\nseen 6 times", 600, 260, t0 + 0.2, size=76, rot=-3), Tick(1010, 300, P("and familiar.") ),
                                      Note("no cliffhangers", 1380, 760, P("No cliffhangers.") , size=72, color=WHITE), Tick(1720, 750, P("No cliffhangers.") + 0.4),
                                      Note("no new voices", 1380, 880, P("No new voices.") , size=72, color=WHITE), Tick(1720, 870, P("No new voices.") + 0.4)],
                                     name="tip_boring")
t0 = P("Turn off autoplay."); beat(t0, PhotoBG(PH + "pexels-6943418.jpg", focus=(0.5, 0.6), amt=0.35, z=(1.0, 1.06)),
                                   [Note("autoplay: OFF", 560, 240, t0 + 0.1, size=92, rot=-3), Tick(900, 230, t0 + 0.5),
                                    Note("sleep timer: 30 min", 1380, 880, P("Set a sleep timer.") , size=80, color=WHITE), Tick(1790, 870, P("sleep timer.") + 0.3)],
                                   name="tip_autoplay")

t0 = P("One honest twist.")
beat(t0, Receipt("edinger2021_aasm_guideline", [dict(t=t0, at="not use sleep hygiene as a single-component therapy", s=1.35)],
                 [dict(phrase="not use sleep hygiene as a single-component therapy", t=P("are not a treatment") )],
                 tag="AASM clinical practice guideline, 2021"),
     [Note("...including mine.", 1450, 880, P("for real insomnia.") , size=70, rot=-3)], name="r_hygiene")
cue(t0, "paper_slide", 0.8)
t0 = P("So if you can't sleep for weeks,"); t_cbt = P("has a name:")
beat(t0, Receipt("edinger2021_aasm_guideline", [dict(t=t0, at="multicomponent cognitive behavioral therapy for insomnia", s=1.3)],
                 [dict(phrase="multicomponent cognitive behavioral therapy for insomnia", t=t_cbt + 0.2), dict(phrase="(STRONG)", t=t_cbt + 0.8, kind="circle")],
                 tag="AASM clinical practice guideline, 2021"),
     [Note("talk to a doctor.", 600, 880, P("talk to a doctor.") , size=80, rot=-3), Note("CBT-I", 1500, 880, P("CBT-I.") , size=110, color=YEL, rot=4)], name="r_cbti")
t0 = P("It's not a better playlist.")
beat(t0, TextureBG(), [Big("not a better\nplaylist.", 960, 480, t0 + 0.2, size=170), Sticker("deadpan", 300, 1680, 840, t0 + 0.6, rot=6),
                       Note("general information, not medical advice.", 960, 960, P("This is general information,") , size=50, color=WHITE)],
     name="playlist")

# ---------------------------------------------------------------- CTA outro (Ep 1 audio) + end screen
beat(T_VO_END + 0.25, TextureBG(), [Sticker("cool", 520, 620, 560, C2(175.26), rot=-4),
                                    Note("subscribe", 1320, 380, C2(177.0), size=110), Circle(1320, 380, 250, 90, C2(177.3), color=YEL),
                                    Note("next midnight question?\n→ comments", 1320, 640, C2(181.66), size=66, color=WHITE),
                                    Note("(before your food gets cold)", 1320, 860, C2(184.66), size=52, color=WHITE)], name="cta_out")
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
        elif k in ("Sticker", "Pasted"): cue(o.t_in, "sticker_slap", 0.6)
        elif k == "Big": cue(o.t_in, "impact_soft", 0.55)
    if isinstance(b.bg, Receipt):
        for m in b.bg.marks:
            cue(m["t"], "highlighter" if m.get("kind", "hl") == "hl" else "marker_squeak", 0.45)
CUES.sort()

if __name__ == "__main__":
    print(len(BEATS), "beats,", len(CUES), "sfx cues, ends", round(T_END, 2))
    for i, b in enumerate(BEATS):
        print(f"{i:02d} {b.t0:7.2f}-{b.t1:7.2f} ({b.t1 - b.t0:5.2f}s) {b.name:14s} {type(b.bg).__name__:9s} {len(b.ovs)} ov")
    assert all(b.t1 > b.t0 for b in BEATS), "non-positive beat"
