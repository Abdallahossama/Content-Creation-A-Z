"""Short #6 finishing: Blender frames + overlays + audio via shortkit.  python post_s06.py qa t.. | seg i n | audio | final | all"""
import sys
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
from shortkit import put, outlined, pill, popk, W, YEL, IMPACT
ROOT = "D:/why habibi/shorts/s06_midnight_snack/"
K.setup(root=ROOT, vo="vo/s06_vo_chatterbox.wav", frames=ROOT + "frames/", music="Late Night Radio.mp3", out="Ask_Habibi_Short06_MidnightSnack.mp4")
at = K.at
T = dict(nearly=at("nearly"), study=at("study"), percent=at("higher"), fatty=at("fatty"), why=at("why"), clock=at("clock"),
         night=at("night"), less=at("less"), link=at("link"), testing=at("testing"), next=at("next"))
def overlay(c, t, cam):
    if t < T["study"] - 0.1:
        put(c, outlined("YOUR LIVER HAS", 92), W / 2, 300); put(c, outlined("A BEDTIME", 92, emoji="🕛"), W / 2, 405)
        if t >= T["nearly"]: put(c, pill("~200,000 US adults studied", 40, (255, 225, 120)), W / 2, 515, popk(t, T["nearly"] + 0.3))
    if T["study"] <= t < T["fatty"] - 0.1:
        put(c, outlined("+20-30%", 150, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["percent"] - 0.3))
        put(c, pill("liver disease risk · people who ate after bedtime", 34), W / 2, 460, popk(t, T["percent"]))
    if T["fatty"] <= t < T["why"] - 0.1:
        put(c, pill("fatty liver disease + cirrhosis", 44, (255, 225, 120)), W / 2, 330, popk(t, T["fatty"] + 0.1))
    if T["clock"] - 0.2 <= t < T["night"] - 0.1:
        put(c, outlined("LIVER CLOCK", 110, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["clock"] - 0.2))
        put(c, pill("nearly every organ runs its own daily rhythm · NIH", 32), W / 2, 445, popk(t, T["clock"]))
    if T["less"] <= t < T["link"] - 0.1:
        put(c, pill("at night, food is handled less efficiently", 40), W / 2, 330, popk(t, T["less"]))
    if T["link"] <= t < T["testing"] - 0.1:
        put(c, outlined("LINKED ≠ PROVEN", 100, fill=YEL, f=IMPACT, stroke=9), W / 2, 330, popk(t, T["link"] + 0.1))
        put(c, pill("self-reported eating times", 38), W / 2, 445, popk(t, T["link"] + 0.5))
    if T["testing"] <= t < T["next"] - 0.1:
        put(c, pill("next: a trial of eating earlier · OHSU", 40, (255, 225, 120)), W / 2, 330, popk(t, T["testing"] + 0.2))
SFX = [("pop", T["nearly"] + 0.3, -20), ("pop", T["percent"] - 0.3, -16), ("pop", T["fatty"] + 0.1, -18), ("bell", T["clock"] - 0.2, -24),
       ("pop", T["less"], -20), ("pop", T["link"] + 0.1, -18), ("pop", T["testing"] + 0.2, -20), ("door", T["next"] + 2.6, -22)]
if __name__ == "__main__":
    K.main(sys.argv, overlay, SFX)
