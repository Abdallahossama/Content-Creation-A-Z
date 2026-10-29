"""Ask Habibi Short #6 "What Midnight Snacks Do To Your Liver 🍕" (Blender 5.2, kit: _style_kit/mascot/batata3d).
Shot from INSIDE the fridge: the door opens on frame 1 and the fridge light hits Batata's face; x-ray shows his liver with
a little clock; fat droplets pop; the microwave clock flips 12:00 -> 7:00 for "eating earlier"; the door closes at the
end so the loop restarts on the opening. Beats from the local VO's word timestamps.
  blender -b --factory-startup --python anim_s06.py -- preview|stills|final <outdir> [args]"""
import bpy, sys, os, json, math
sys.path.insert(0, "D:/why habibi/_style_kit/mascot/batata3d")
import batata3d as B3
from batata3d import key, pop, shot, face, F, key_value, emission_input
from mathutils import Vector

ROOT = "D:/why habibi/shorts/s06_midnight_snack/"
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
T = dict(nearly=at("nearly"), study=at("study"), percent=at("higher"), fatty=at("fatty"), cirrhosis=at("cirrhosis"), why=at("why"),
         clock=at("clock"), tune=at("tune"), night=at("night"), less=at("less"), link=at("link"), testing=at("testing"),
         earlier=at("earlier"), next=at("next"), clocked=at("off"))

sc = B3.render_setup(32, world=(0.003, 0.004, 0.012))
P = B3.kitchen(); hinge, FL = P["hinge"], P["fridge_light"]
body_parts = [bpy.data.objects[n] for n in ("FridgeBody", "FridgeInside")]
B3.box("Milk", (0.10, 0.10, 0.24), (0.15, 0.50, 0.83), B3.mat("milk", (0.95, 0.95, 0.97), 0.4), bevel=0.01)
B3.box("Jar", (0.11, 0.11, 0.13), (0.57, 0.52, 0.78), B3.mat("jar", (0.9, 0.3, 0.2), 0.2), bevel=0.03)
b, H, W = B3.potato(height=0.95, faces=("sideeye", "shocked", "sleepy", "fine", "smug")); B3.nightcap(b, H, W)
b.location = (0.35, -0.35, 0.50); b.rotation_euler = (0, 0, math.radians(155))
BL, BR = Vector(b.location), Vector(b.rotation_euler)
sl = B3.pizza_slice((0.0, 0.0, 0.0), 0.17); SL = Vector((0.14, -0.06, 0.40)); sl.location = SL; sl.rotation_euler = (math.radians(-80), math.radians(35), math.radians(160))

# liver (inside Batata, local space; front = local -y = toward the fridge camera), with a clock face and fat droplets
lv_m = B3.mat("liver", (0.30, 0.03, 0.02), 0.45, emit=(0.45, 0.02, 0.01), strength=0.0)
liver = B3.sphere("Liver", 0.5, (0, 0, 0), lv_m, scale=(0.30 * W, 0.16 * W, 0.15 * H)); liver.parent = b; liver.location = (0.04 * W, 0.0, -0.10 * H)
lobe = B3.sphere("LiverLobe", 0.5, (0, 0, 0), lv_m, scale=(0.36, 0.9, 0.75)); lobe.parent = liver; lobe.location = (0.32, 0.0, -0.12)
cface = B3.mat("clockface", (1, 1, 1), 0.3, emit=(1, 0.98, 0.9), strength=1.5); hand_m = B3.mat("hand", (0.05, 0.05, 0.05), 0.4)
bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.006, rotation=(math.radians(90), 0, 0)); clk = bpy.context.object; clk.name = "LiverClock"
clk.data.materials.append(cface); clk.parent = b; clk.location = (0.02 * W, -0.10 * W, -0.06 * H)
hands = []
for k, (ln, wd) in enumerate(((0.040, 0.007), (0.028, 0.009))):
    piv = bpy.data.objects.new(f"HandPivot{k}", None); sc.collection.objects.link(piv); piv.parent = clk; piv.location = (0, 0, 0)
    piv.rotation_euler = (0, 0, 0)
    hb = B3.box(f"Hand{k}", (wd, ln, 0.004), (0, 0, 0), hand_m, bevel=0); hb.parent = piv; hb.location = (0, ln / 2, 0.006)
    hands.append(piv)
drops = []
for k, (x, z) in enumerate(((-0.08, 0.03), (0.06, -0.02), (0.12, 0.05), (-0.02, -0.06), (0.15, -0.05), (0.0, 0.07))):
    d = B3.sphere(f"Fat{k}", 0.018 + 0.006 * (k % 3), (0, 0, 0), B3.mat(f"fat{k}", (1.0, 0.85, 0.25), 0.3, emit=(1.0, 0.8, 0.2), strength=2.0))
    d.parent = b; d.location = (x * W + 0.04 * W, -0.085 * W, (-0.10 + z) * H); drops.append(d)
inner = [liver, lobe, clk] + drops
for o in inner: o.hide_render = True

# microwave clock: 12:00 and a hidden 7:00 for "eating earlier"
c12 = P["clock"]; c7 = B3.text3d("7:00", (-1.38, 0.815, 1.16), 0.055, c12.data.materials[0], extrude=0.002)
cam, tgt = B3.camera_rig(); cam.data.dof.use_dof = False
B3.key_light(b, loc=(1.6, -1.6, 1.8), energy=25, color=(0.7, 0.8, 1.0))

# ------------------------------------------------------------------ helpers
def vis(objs, t, on):
    for o in objs:
        o.hide_render = not on; o.keyframe_insert("hide_render", frame=max(1, F(t)))
def door(t0, t1, a0, a1, e0, e1):
    key(hinge, "rotation_euler", t0, (0, 0, math.radians(a0)), "BEZIER"); key(hinge, "rotation_euler", t1, (0, 0, math.radians(a1)), "BEZIER")
    FL.data.energy = e0; FL.data.keyframe_insert("energy", frame=F(t0)); FL.data.energy = e1; FL.data.keyframe_insert("energy", frame=F(t1))
FRIDGE = ((0.36, 0.80, 0.86), (0.31, -0.35, 0.58), 30)
SIDE = ((1.70, 0.40, 1.25), (-0.05, -0.32, 0.70), 24)
XRAY = ((0.30, 0.75, 0.60), (0.36, -0.35, 0.47), 38)
LIVER = ((0.33, 0.20, 0.50), (0.37, -0.35, 0.42), 48)

# ------------------------------------------------------------------ timeline
# B1 frame 1: door already swinging open, light flooding Batata's side-eye face with the slice at his mouth
door(-0.25, 0.10, -95, -105, 45, 60); face(b, 0.0, 0)
vis(inner, 0.0, False); vis([c12], 0.0, True)
slice_parts = [sl] + list(sl.children); shelves = [bpy.data.objects[f"Shelf{k}"] for k in range(3)]
vis(slice_parts + shelves, 0.0, True)
vis(body_parts, 0.0, False)
shot(cam, tgt, 0.0, T["nearly"], FRIDGE, ((0.36, 0.66, 0.82), (0.31, -0.35, 0.58), 32))
# B2 nearly 200,000 people: wide kitchen, microwave clock glowing 12:00
vis(body_parts, T["nearly"], True); shot(cam, tgt, T["nearly"], T["percent"] - 0.4, SIDE, push=0.20)
# B3 20-30% higher risk: x-ray, the liver glows
vis(body_parts + slice_parts + shelves, T["percent"] - 0.4, False); shot(cam, tgt, T["percent"] - 0.4, T["fatty"], XRAY, push=0.10)
key(b, '["xray"]', T["percent"] - 0.47, 0.0, "CONSTANT"); key(b, '["xray"]', T["percent"] - 0.4, 1.0, "CONSTANT")
vis([liver, lobe], T["percent"] - 0.4, True); face(b, T["percent"], 1)
key_value(emission_input(lv_m), T["percent"] - 0.4, 0.0); key_value(emission_input(lv_m), T["percent"] + 0.3, 1.5)
# B4 fatty liver + cirrhosis: liver close-up, fat droplets pop
shot(cam, tgt, T["fatty"], T["why"], LIVER, push=0.05)
for k, d in enumerate(drops): vis([d], T["fatty"] + 0.1 * k, True); pop(d, T["fatty"] + 0.1 * k)
for k, d in enumerate(drops): vis([d], T["why"] - 0.05, False)
key_value(emission_input(lv_m), T["cirrhosis"], 1.5); key_value(emission_input(lv_m), T["cirrhosis"] + 0.3, 3.0); key_value(emission_input(lv_m), T["why"], 1.0)
# B5 every organ has a clock: the clock pops on the liver, hands at day
shot(cam, tgt, T["why"], T["night"], XRAY, push=0.08); vis([clk], T["clock"] - 0.2, True); pop(clk, T["clock"] - 0.2)
key(hands[0], "rotation_euler", T["clock"], (0, 0, math.radians(0)), "LINEAR"); key(hands[1], "rotation_euler", T["clock"], (0, 0, math.radians(-90)), "LINEAR")
# B6 in tune -> at night: the hands spin to midnight, the liver dims (slows down)
key(hands[0], "rotation_euler", T["tune"] + 1.2, (0, 0, math.radians(-720)), "BEZIER"); key(hands[1], "rotation_euler", T["tune"] + 1.2, (0, 0, math.radians(-360)), "BEZIER")
shot(cam, tgt, T["night"], T["link"], LIVER, push=0.05)
key_value(emission_input(lv_m), T["night"], 1.0); key_value(emission_input(lv_m), T["less"], 0.1)
for k, d in enumerate(drops[:4]): vis([d], T["less"] + 0.12 * k, True); pop(d, T["less"] + 0.12 * k)
# B7 a link, not proof: back to normal, side-eye; wide
key(b, '["xray"]', T["link"] - 0.07, 1.0, "CONSTANT"); key(b, '["xray"]', T["link"], 0.0, "CONSTANT"); vis(inner, T["link"], False)
vis(body_parts + slice_parts + shelves, T["link"], True); shot(cam, tgt, T["link"], T["testing"], SIDE, push=0.15); face(b, T["link"], 0)
# B8 testing eating earlier: microwave clock flips 12:00 -> 7:00 (close on the microwave)
MW = ((-0.95, -0.35, 1.25), (-1.45, 0.8, 1.12), 40)
shot(cam, tgt, T["testing"], T["next"], MW, push=0.10)
vis([c7], 0.0, False); vis([c7], T["earlier"], True); vis([c12], T["earlier"], False); vis([c12], T["next"], True); vis([c7], T["next"], False)
# B9 the loop: back inside the fridge, smug, the slice goes back and the door closes to black on "clocked out"
vis(body_parts, T["next"], False); shot(cam, tgt, T["next"], END, ((0.36, 0.70, 0.84), (0.31, -0.35, 0.58), 31), FRIDGE); face(b, T["next"], 4)
key(sl, "location", T["clocked"] - 0.8, tuple(SL), "BEZIER"); key(sl, "location", T["clocked"] - 0.2, tuple(SL + Vector((0.10, 0.55, 0.12))), "BEZIER")
door(T["clocked"] + 0.2, END - 0.05, -105, -55, 60, 18)

B3.render(sc, MODE, OUT, ARGS[2:], END)
