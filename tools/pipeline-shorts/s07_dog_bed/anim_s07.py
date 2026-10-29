"""Ask Habibi Short #7 "What Happens When Your Dog Sleeps In Your Bed 🐶" (Blender 5.2, kit: _style_kit/mascot/batata3d).
Beats keyed from the local VO's word timestamps (vo_words.json). Zack-style: in the action on frame 1, close-ups, hard cuts,
characters move only on story beats (no idle bobbing).
  blender -b --factory-startup --python anim_s07.py -- preview|stills|final <outdir> [args]"""
import bpy, sys, os, json, math
sys.path.insert(0, "D:/why habibi/_style_kit/mascot/batata3d")
import batata3d as B3
from batata3d import key, pop, shot, face, F
from mathutils import Vector

ROOT = "D:/why habibi/shorts/s07_dog_bed/"
ARGS = sys.argv[sys.argv.index("--") + 1:]; MODE, OUT = ARGS[0], ARGS[1]
WORDS = [w for s in json.load(open(ROOT + "vo/vo_words.json", encoding="utf-8")) for w in s["words"]]
END = WORDS[-1]["e"] + 0.8
def at(word, n=1):
    k = 0
    for w in WORDS:
        if w["w"].strip(" ,.?!:").lower() == word.lower():
            k += 1
            if k == n: return w["s"]
    raise KeyError(f"{word} #{n}")
T = dict(trackers=at("trackers"), scientists=at("scientists"), sharing=at("sharing"), dogs=at("dogs", 3), most=at("most"),
         first=at("first"), human=at("human"), twist=at("twist"), half=at("half"), didnt=at("didn't"), small=at("small"),
         tired=at("tired"), blame=at("blame", 2))

sc = B3.render_setup(32)
B3.bedroom(duvet_body=(-0.28, 0.42), duvet_width=0.38)
b, H, W = B3.potato(height=0.95, faces=("sleepy", "shocked", "sideeye", "fine")); B3.nightcap(b, H, W)
b.location = (-0.30, 0.78, 0.98); b.rotation_euler = (math.radians(-52), 0, math.radians(-8))
BL, BR = Vector(b.location), Vector(b.rotation_euler)
dog, head = B3.potato_dog((0.28, 0.52, 0.80), rot_z=math.radians(10), size=0.62)
DR = Vector(head.rotation_euler); DL = Vector(head.location)
tail = bpy.data.objects[dog["tail"]]; TR0 = Vector(tail.rotation_euler)
cam, tgt = B3.camera_rig(); cam.data.dof.use_dof = False
B3.key_light(tgt, energy=80)

# trackers: a band with a glowing green LED on Batata's side, a red collar with a tracker on the dog
led = B3.mat("led", (0.2, 1.0, 0.4), 0.2, emit=(0.2, 1.0, 0.45), strength=25.0); blk = B3.mat("tracker", (0.05, 0.05, 0.06), 0.3)
tb = B3.box("TrackerB", (0.10, 0.04, 0.07), (0, 0, 0), blk, bevel=0.012); tb.parent = b; tb.location = (0.31 * W, -0.10 * W, -0.10 * H); tb.rotation_euler = (0, 0, math.radians(35))
l1 = B3.sphere("LedB", 0.012, (0, 0, 0), led); l1.parent = tb; l1.location = (0, -0.022, 0.012)
bpy.ops.mesh.primitive_torus_add(major_radius=0.62 * 0.19, minor_radius=0.012, location=(0, 0, 0)); col = bpy.context.object; col.name = "Collar"
col.data.materials.append(B3.mat("collar", (0.8, 0.12, 0.1), 0.5)); col.parent = dog; col.location = (0, -0.06 * 0.62, 0.30 * 0.62); col.rotation_euler = (math.radians(70), 0, 0)
td = B3.box("TrackerD", (0.06, 0.03, 0.05), (0, 0, 0), blk, bevel=0.01); td.parent = dog; td.location = (0, -0.20 * 0.62, 0.18 * 0.62)
l2 = B3.sphere("LedD", 0.01, (0, 0, 0), led); l2.parent = td; l2.location = (0, -0.016, 0.01)

# ------------------------------------------------------------------ shots
DUO = ((0.02, -1.55, 1.62), (0.0, 0.62, 0.95), 31)
WIDE = ((0.9, -1.9, 2.3), (0.05, 0.6, 0.8), 30)
TOP = ((0.0, 0.10, 3.05), (0.0, 0.62, 0.80), 26)
DOGCU = ((0.48, -0.55, 1.18), (0.28, 0.40, 1.0), 40)
BATCU = ((-0.18, -0.50, 1.50), (-0.30, 0.78, 1.08), 40)

def roll(t, big=1.0):
    """Batata turns over: a lift + twist, settles in ~0.7 s (duvet bounces)"""
    for tt, a in ((t - 0.07, 0), (t + 0.15, 1.0), (t + 0.35, 0.8), (t + 0.7, 0.0)):
        key(b, "location", tt, tuple(BL + Vector((0.02 * a * big, 0, 0.05 * a * big))), "BEZIER")
        key(b, "rotation_euler", tt, (BR.x, BR.y + math.radians(16) * a * big, BR.z - math.radians(10) * a * big), "BEZIER")
    duv = bpy.data.objects["Duvet"]; z0 = duv.location.z
    for tt, a in ((t - 0.07, 0), (t + 0.15, 0.03 * big), (t + 0.4, -0.006), (t + 0.6, 0)):
        key(duv, "location", tt, (duv.location.x, duv.location.y, z0 + a), "BEZIER")
def dog_up(t, hold=1.0, look=0.0):
    """the dog lifts its head (and turns toward Batata by `look` radians), then lies back down"""
    for tt, a in ((t - 0.07, 0), (t + 0.18, 1.0), (t + 0.18 + hold, 1.0), (t + 0.5 + hold, 0)):
        key(head, "location", tt, tuple(DL + Vector((0, 0, 0.05 * a))), "BEZIER")
        key(head, "rotation_euler", tt, (DR.x - math.radians(14) * a, DR.y, DR.z + look * a), "BEZIER")

# ------------------------------------------------------------------ timeline
# B1 hook: frame 1 = Batata mid-roll, the dog wakes and side-eyes him; trackers pop on "trackers"
roll(-0.2, 1.2); face(b, 0.0, 0); face(head, 0.0, 1); face(head, 0.9, 2); dog_up(-0.1, hold=2.2, look=math.radians(-25))
face(b, 1.4, 2)
shot(cam, tgt, 0.0, T["scientists"], DUO, ((0.02, -1.30, 1.55), (0.0, 0.62, 0.97), 32))
pop(tb, T["trackers"]); pop(td, T["trackers"] + 0.15)
# B2 the study: top-down view of the bed, both asleep
face(b, T["scientists"], 0); face(head, T["scientists"], 0)
shot(cam, tgt, T["scientists"], T["sharing"], TOP, push=0.25)
# B3 no difference for people: wide, calm
shot(cam, tgt, T["sharing"], T["dogs"], WIDE, push=0.20)
# B4 dogs weren't more restless: dog close-up, peaceful
shot(cam, tgt, T["dogs"], T["most"], DOGCU, push=0.06)
# B5 pairs moved within 5 minutes: top view, Batata rolls and the dog shifts 0.6 s later
shot(cam, tgt, T["most"], T["first"] - 0.3, TOP, push=0.15); roll(T["most"] + 0.3, 0.8); dog_up(T["most"] + 0.9, hold=0.4)
# B6 the human usually moved first: Batata rolls, then the dog's eyes snap open (shocked) and it looks at him
shot(cam, tgt, T["first"] - 0.3, T["twist"], DUO, push=0.10); roll(T["first"], 1.0)
face(head, T["human"] - 0.1, 1); dog_up(T["human"] - 0.1, hold=1.2, look=math.radians(-25)); face(head, T["human"] + 0.8, 2)
# B7 the twist: Batata side-eyes the dog (blame)
shot(cam, tgt, T["twist"], T["didnt"], BATCU, push=0.08); face(b, T["twist"], 2); face(head, T["twist"], 0)
# B8 trackers didn't show it: the dog side-eyes back
shot(cam, tgt, T["didnt"], T["small"], DOGCU, push=0.05); face(head, T["didnt"] + 0.1, 2); dog_up(T["didnt"] + 0.1, hold=1.0, look=math.radians(-25))
# B9 small study: wide; then the loop shot, both asleep
shot(cam, tgt, T["small"], T["tired"], WIDE, push=0.15); face(b, T["small"], 0); face(head, T["small"] + 0.5, 0)
shot(cam, tgt, T["tired"], END, ((0.02, -1.30, 1.55), (0.0, 0.62, 0.97), 32), DUO); face(b, T["blame"] + 0.2, 2)

B3.render(sc, MODE, OUT, ARGS[2:], END)
