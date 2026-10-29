"""Short #7 finishing: Blender frames + overlays (logo, question title, number pops, captions) + audio via shortkit.
  python post_s07.py qa t.. | seg i n | audio | final | all"""
import sys
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, W, YEL, IMPACT
ROOT = "D:/why habibi/shorts/s07_dog_bed/"
K.setup(root=ROOT, vo="vo/s07_vo_chatterbox.wav", frames=ROOT + "frames/", music="Dream Culture.mp3", out="Ask_Habibi_Short07_DogInBed.mp4")
at = K.at
T = dict(trackers=at("trackers"), scientists=at("scientists"), sharing=at("sharing"), dogs=at("dogs", 3), most=at("most"),
         first=at("first"), human=at("human"), twist=at("twist"), half=at("half"), didnt=at("didn't"), small=at("small"), tired=at("tired"))
def overlay(c, t, cam):
    if t < T["scientists"] - 0.1:
        put(c, outlined("IS YOUR DOG RUINING", 82), W / 2, 300); put(c, outlined("YOUR SLEEP?", 82, emoji="🐶"), W / 2, 400)
    if T["scientists"] <= t < T["sharing"] - 0.1:
        put(c, outlined("25 PEOPLE · 38 DOGS", 90, fill=YEL, f=IMPACT, stroke=8), W / 2, 330, popk(t, T["scientists"] + 0.3))
        put(c, pill("motion trackers on both · ~4 weeks", 38), W / 2, 440, popk(t, T["scientists"] + 0.6))
    if T["sharing"] <= t < T["most"] - 0.1:
        put(c, outlined("NO DIFFERENCE", 120, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["sharing"] + 0.6))
        put(c, pill("how long + how well people slept", 38), W / 2, 450, popk(t, T["sharing"] + 0.8))
        if t >= T["dogs"]: put(c, pill("dogs: no more restless either", 38), W / 2, 540, popk(t, T["dogs"] + 0.2))
    if T["most"] <= t < T["twist"] - 0.1:
        put(c, outlined("22 OF 36 PAIRS", 100, fill=YEL, f=IMPACT, stroke=8), W / 2, 330, popk(t, T["most"] + 0.2))
        put(c, pill("moved within 5 minutes of each other", 38), W / 2, 445, popk(t, T["most"] + 0.4))
        if t >= T["human"] - 0.2:
            put(c, pill("human moved first: 10 pairs", 44, (255, 225, 120), (150, 40, 30, 235)), W / 2, 560, popk(t, T["human"] - 0.2))
            put(c, pill("dog moved first: 4 pairs", 40, (230, 240, 255), (40, 70, 130, 235)), W / 2, 660, popk(t, T["human"] + 0.2))
    if T["half"] <= t < T["small"] - 0.1:
        put(c, outlined("50%", 170, fill=YEL, f=IMPACT, stroke=10), W / 2, 330, popk(t, T["half"]))
        put(c, pill("of owners: \"my dog disturbs my sleep\"", 38), W / 2, 470, popk(t, T["half"] + 0.3))
        if t >= T["didnt"]: put(c, outlined("TRACKERS: NOPE", 96, fill=(255, 255, 255)), W / 2, 590, popk(t, T["didnt"] + 0.2))
    if T["small"] <= t < T["tired"] - 0.1:
        put(c, pill("small study · huskies + malamutes · PLOS One, Oct 2026", 34), W / 2, 330, popk(t, T["small"] + 0.2))
SFX = [("pop", T["trackers"], -18), ("pop", T["scientists"] + 0.3, -18), ("pop", T["sharing"] + 0.6, -18), ("pop", T["most"] + 0.2, -18),
       ("pop", T["human"] - 0.2, -18), ("pop", T["half"], -16), ("record_scratch", T["didnt"] + 0.2, -24), ("pop", T["small"] + 0.2, -20)]
if __name__ == "__main__":
    K.main(sys.argv, overlay, SFX)
