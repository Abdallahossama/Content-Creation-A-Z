"""Short #2 animation (Blender 5.2): builds scene.py's bedroom, then keys every beat of the script from beats.json
(times in seconds, taken from the voice-over's word timestamps). Zack-style: in the action from frame 1, close-ups,
glow on the point of contact, hard cuts, constant motion (no idle bobbing; characters move only on story beats).
  blender -b --factory-startup --python anim.py -- preview <beats.json> <outdir> [step]     half-res, 8 samples, every Nth frame
  blender -b --factory-startup --python anim.py -- final   <beats.json> <outdir> <f0> <f1>  full res frame range
  blender -b --factory-startup --python anim.py -- stills  <beats.json> <outdir> t1 t2 ...  full-res stills at times"""
import bpy, math, sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene as S
from mathutils import Vector

FPS = 30
ARGS = sys.argv[sys.argv.index("--") + 1:]
MODE, BEATS, OUT = ARGS[0], json.load(open(ARGS[1], encoding="utf-8")), ARGS[2]
T = BEATS["t"]; END = BEATS["end"]
def F(t): return int(round(t * FPS)) + 1

def key(o, path, t, value, interp="BEZIER", index=-1):
    if path.startswith('["'): o[path[2:-2]] = value
    else:
        attr = getattr(o, path)
        if index >= 0: attr[index] = value
        elif hasattr(attr, "__len__"): setattr(o, path, value)
        else: setattr(o, path, value)
    o.keyframe_insert(path, frame=F(t), index=index)
    ad = o.animation_data
    if ad and ad.action:
        for fc in _fcurves(ad.action):
            if fc.data_path == path:
                for kp in fc.keyframe_points:
                    if abs(kp.co.x - F(t)) < 0.5: kp.interpolation = interp

def _fcurves(action):
    try: return list(action.fcurves)
    except AttributeError:                                           # Blender 5 layered actions
        out = []
        for layer in action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags: out += list(cb.fcurves)
        return out

def mat(*a, **k): return S.mat(*a, **k)

# ------------------------------------------------------------------------------------------- scene + extras
sc = S.build(); b = bpy.data.objects["Batata"]; cam = sc.camera; tgt = bpy.data.objects["CamTarget"]
cam.constraints[0].target = tgt; cam.data.dof.use_dof = False
H, W = 0.95, 1068 / 1508 * 0.95
BASE_LOC, BASE_ROT = Vector(b.location), Vector(b.rotation_euler)
rig = bpy.data.objects.new("Rig", None); sc.collection.objects.link(rig)            # everything that falls together
for n in ("Headboard", "BedFrame", "Mattress", "Pillow", "Duvet", "Batata"):
    o = bpy.data.objects[n]; o.parent = rig
room = [bpy.data.objects[n] for n in ("Floor", "WallBack", "WallLeft", "Window")]
def _top(o):
    while o.parent: o = o.parent
    return o
props = [o for o in bpy.data.objects if o.type == "MESH" and _top(o).name.endswith("_root")]       # nightstand + clock parts

# brain + nerves + pulse inside the potato (only visible in x-ray)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0.02, 0.18 * H)); brain = bpy.context.object; brain.name = "Brain"
brain.scale = (0.17 * W, 0.12 * W, 0.12 * H); bm_tex = bpy.data.textures.new("gyri", "MUSGRAVE") if hasattr(bpy.types, "MusgraveTexture") else bpy.data.textures.new("gyri", "CLOUDS")
dsp = brain.modifiers.new("gyri", "DISPLACE"); dsp.texture = bm_tex; dsp.strength = 0.012; sub = brain.modifiers.new("s", "SUBSURF"); sub.levels = 2
bpy.ops.object.shade_smooth()
brain_m = mat("brain", (0.95, 0.55, 0.62), 0.5, emit=(1.0, 0.15, 0.10), strength=0.0); brain.data.materials.append(brain_m)
brain.parent = b
nerve_m = mat("nerve", (1.0, 0.85, 0.3), 0.4, emit=(1.0, 0.78, 0.25), strength=0.0)
nerves = []
for k, (dx, dz) in enumerate([(-0.20, -0.42), (0.20, -0.42), (-0.10, -0.46), (0.10, -0.46), (0.0, -0.47), (-0.28, -0.25), (0.28, -0.25)]):
    cu = bpy.data.curves.new(f"nerve{k}", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.006; cu.bevel_resolution = 2
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(2)
    pts = [(0, 0.02, 0.12 * H), (dx * W * 0.6, 0.0, (0.12 + dz) * H * 0.6), (dx * W, -0.01, dz * H)]
    for i, p in enumerate(pts):
        bp = sp.bezier_points[i]; bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(f"Nerve{k}", cu); sc.collection.objects.link(o); o.data.materials.append(nerve_m); o.parent = b; nerves.append(o)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0, 0.0, 0.12 * H)); pulse = bpy.context.object; pulse.name = "Pulse"
pulse.data.materials.append(mat("pulse", (1, 1, 1), 0.2, emit=(1.0, 0.95, 0.7), strength=40.0)); pulse.parent = b
bpy.ops.object.light_add(type="POINT", location=(0, 0, 0)); pl = bpy.context.object; pl.data.energy = 0; pl.data.color = (1.0, 0.85, 0.5); pl.parent = pulse

# question marks
qs = []                                                                       # world space, above the head, facing the camera
for k, (x, y, z, r) in enumerate([(-0.34, 0.80, 1.62, 14), (0.0, 0.86, 1.76, -4), (0.34, 0.80, 1.62, -12)]):
    bpy.ops.object.text_add(location=(x, y, z)); t = bpy.context.object; t.data.body = "?"; t.data.extrude = 0.03; t.data.bevel_depth = 0.008
    t.data.align_x = "CENTER"; t.scale = (0.28,) * 3; t.rotation_euler = (math.radians(72), 0, math.radians(r))
    t.data.materials.append(mat("q", (1.0, 0.76, 0.1), 0.35, emit=(1.0, 0.7, 0.1), strength=1.5)); qs.append(t)

# nightstand props: mug (with steam), phone glowing, the existing alarm clock
ns = [o for o in props if "Nightstand" in o.name or "nightstand" in o.name.lower()]
top_z = 0.70
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.10, location=(1.12, 0.95, top_z + 0.05)); mug = bpy.context.object; mug.name = "Mug"
mug.data.materials.append(mat("mug", (0.80, 0.22, 0.16), 0.35)); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_torus_add(major_radius=0.028, minor_radius=0.008, location=(1.165, 0.95, top_z + 0.05), rotation=(math.radians(90), 0, 0))
hd = bpy.context.object; hd.data.materials.append(mug.data.materials[0]); hd.parent = mug; hd.location = (0.045, 0, 0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.004, location=(1.12, 0.95, top_z + 0.095)); cof = bpy.context.object
cof.data.materials.append(mat("coffee", (0.12, 0.06, 0.03), 0.2)); cof.parent = mug; cof.location = (0, 0, 0.045)
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.38, 0.97, top_z + 0.006)); phone = bpy.context.object; phone.name = "Phone"
phone.scale = (0.075, 0.15, 0.008); phone.rotation_euler = (0, 0, math.radians(-18)); phone.data.materials.append(mat("phonebody", (0.05, 0.05, 0.06), 0.3))
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.51)); scr = bpy.context.object; scr.parent = phone; scr.scale = (0.9, 0.92, 1)
scr.data.materials.append(mat("screen", (0.6, 0.8, 1.0), 0.2, emit=(0.55, 0.75, 1.0), strength=6.0))

# ------------------------------------------------------------------------------------------- shots (hard cuts)
FACE_CU = ((0.15, -1.10, 1.74), (0.0, 0.82, 1.05), 40)      # close-up on the face
WIDE = ((0.9, -1.9, 2.3), (0.0, 0.6, 0.8), 32)
SIDE = ((0.95, -0.75, 1.42), (0.0, 0.80, 1.02), 38)
XRAY = ((0.08, -0.90, 1.66), (0.0, 0.82, 1.02), 46)
NIGHT = ((1.00, 0.30, 1.06), (1.24, 1.0, 0.80), 40)          # nightstand
def shot(t0, t1, a, bshot=None, push=0.12):
    loc0, tg0, lens = a; loc1, tg1, lens1 = bshot or (tuple(Vector(loc0) + (Vector(tg0) - Vector(loc0)).normalized() * push), tg0, lens)
    for t, l, g, ln in ((t0, loc0, tg0, lens), (t1 - 1 / FPS, loc1, tg1, lens1)):
        key(cam, "location", t, l, "LINEAR"); key(tgt, "location", t, g, "LINEAR"); key(cam.data, "lens", t, ln, "LINEAR")

# ------------------------------------------------------------------------------------------- the jolt
def jolt(t, big=1.0):
    """a 0.12 s kick up + tilt, overshoot, settle in ~0.6 s; face shocked for 1.1 s; duvet bounces with it"""
    up = Vector((0, -0.03, 0.13 * big)); rr = math.radians(9 * big)
    seq = [(t - 0.07, 0, 0), (t + 0.10, 1.0, 1.0), (t + 0.22, 0.55, 0.6), (t + 0.34, 0.12, 0.2), (t + 0.46, 0.04, -0.05), (t + 0.62, 0, 0)]
    for tt, a, r in seq:
        key(b, "location", tt, tuple(BASE_LOC + up * a), "BEZIER"); key(b, "rotation_euler", tt, (BASE_ROT.x + rr * r, BASE_ROT.y, BASE_ROT.z), "BEZIER")
    duv = bpy.data.objects["Duvet"]; z0 = duv.location.z
    for tt, a in ((t - 0.07, 0), (t + 0.10, 0.05 * big), (t + 0.26, -0.01), (t + 0.45, 0)):
        key(duv, "location", tt, (duv.location.x, duv.location.y, z0 + a), "BEZIER")
    key(b, '["shock"]', t - 0.07, 0.0, "CONSTANT"); key(b, '["shock"]', t, 1.0, "CONSTANT"); key(b, '["shock"]', t + 1.1, 0.0, "CONSTANT")

def rest(t):
    key(b, "location", t, tuple(BASE_LOC), "BEZIER"); key(b, "rotation_euler", t, tuple(BASE_ROT), "BEZIER")

# ------------------------------------------------------------------------------------------- the timeline
rest(0.0)
# B1 0 -> seven: in the action on frame 1 (the jolt has already started)
jolt(-0.10, 1.15); shot(0.0, T["seven"], FACE_CU, ((0.12, -0.92, 1.70), (0.0, 0.82, 1.05), 42))
# B2 seven -> hypnic: wide; second jolt so the "7 in 10" line is still moving
shot(T["seven"], T["hypnic"], WIDE, push=0.25); jolt(T["seven"] + 0.5, 0.8)
# B3 hypnic -> drift: side close-up, label added in post
shot(T["hypnic"], T["drift"], SIDE, push=0.10)
# B4 drift -> misreads: x-ray, nerves glow then dim (muscles go slack)
shot(T["drift"], T["misreads"], XRAY, push=0.08)
key(b, '["xray"]', T["drift"] - 0.07, 0.0, "CONSTANT"); key(b, '["xray"]', T["drift"], 1.0, "LINEAR"); key(b, '["xray"]', T["jumps"] - 0.07, 1.0, "CONSTANT"); key(b, '["xray"]', T["jumps"], 0.0, "CONSTANT")
for k, n in enumerate(nerves):
    nm = n.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
nm = nerve_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for tt, v in ((T["drift"] - 0.07, 0.0), (T["drift"], 6.0), (T["slack"], 6.0), (T["misreads"], 0.6)):
    nm.default_value = v; nm.keyframe_insert("default_value", frame=F(tt))
# B5 misreads -> fires: everything falls into the dark, the brain glows red
shot(T["misreads"], T["fires"], ((0.10, -0.60, 1.55), (0.0, 0.80, 0.95), 48), ((0.10, -0.60, 1.10), (0.0, 0.80, 0.50), 48))
for o in room:
    o.hide_render = False; o.keyframe_insert("hide_render", frame=F(T["misreads"]) - 1); o.hide_render = True; o.keyframe_insert("hide_render", frame=F(T["misreads"]))
    o.keyframe_insert("hide_render", frame=F(T["fires"]) - 1); o.hide_render = False; o.keyframe_insert("hide_render", frame=F(T["jumps"]) - 2)
for o in props:
    for fr, v in ((F(T["misreads"]) - 1, False), (F(T["misreads"]), True), (F(T["jumps"]) - 2, False)):
        o.hide_render = v; o.keyframe_insert("hide_render", frame=fr)
for tt, z in ((T["misreads"], 0.0), (T["fires"], -0.55)):
    key(rig, "location", tt, (0, 0, z), "BEZIER" if z == 0 else "LINEAR")
key(rig, "location", T["fires"] + 0.04, (0, 0, 0), "CONSTANT")
bm_s = brain_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for tt, v in ((T["misreads"] + 0.2, 0.0), (T["falling1"], 8.0), (T["fires"] + 0.4, 8.0), (T["jumps"], 0.0)):
    bm_s.default_value = v; bm_s.keyframe_insert("default_value", frame=F(tt))
# B6 fires -> jumps: the pulse races from the brain down the body (x-ray close-up)
shot(T["fires"], T["jumps"], XRAY, push=0.06)
for tt, z, e in ((T["fires"] + 0.05, 0.12 * H, 0), (T["fires"] + 0.15, 0.10 * H, 60), (T["jumps"] - 0.12, -0.40 * H, 60), (T["jumps"], -0.42 * H, 0)):
    key(pulse, "location", tt, (0, -0.02, z), "LINEAR"); pl.data.energy = e; pl.data.keyframe_insert("energy", frame=F(tt))
pulse.hide_render = True; pulse.keyframe_insert("hide_render", frame=1); pulse.hide_render = False; pulse.keyframe_insert("hide_render", frame=F(T["fires"]))
pulse.hide_render = True; pulse.keyframe_insert("hide_render", frame=F(T["jumps"]) + 1)
# B7 jumps -> theory: the big jolt from the side
shot(T["jumps"], T["theory"], SIDE, push=0.05); jolt(T.get("jumpword", T["jumps"] + 0.05), 1.3)
# B8 theory -> normal: question marks pop above the head
shot(T["theory"], T["normal"], ((0.0, -1.05, 2.05), (0.0, 0.8, 1.35), 40), push=0.10)
for k, q in enumerate(qs):
    t0 = T["theory"] + 0.35 + k * 0.25
    for tt, s in ((t0 - 0.07, 0.0), (t0 + 0.13, 0.34), (t0 + 0.26, 0.28)):
        key(q, "scale", tt, (s, s, s), "BEZIER")
    key(q, "scale", T["normal"] - 0.07, (0.28,) * 3, "CONSTANT"); key(q, "scale", T["normal"], (0, 0, 0), "CONSTANT")
for q in qs: key(q, "scale", 0.0, (0, 0, 0), "CONSTANT")
# B9 normal -> next: nightstand; mug, phone, clock pop on "stress / caffeine / sleep"
shot(T["normal"], T["next"], NIGHT, push=0.12)
for o, t0 in ((phone, T["stress"]), (mug, T["caffeine"])):
    s0 = tuple(o.scale) if o is not phone else (0.075, 0.15, 0.008)
    key(o, "scale", 0.0, (0, 0, 0), "CONSTANT")
    for tt, k in ((t0 - 0.07, 0.0), (t0 + 0.13, 1.15), (t0 + 0.26, 1.0)):
        key(o, "scale", tt, tuple(v * k for v in s0), "BEZIER")
# B10 next -> end: back to the opening close-up, calm; ends where frame 1 begins (loop)
shot(T["next"], END, ((0.12, -0.92, 1.70), (0.0, 0.82, 1.05), 42), FACE_CU)
rest(T["next"]); key(b, '["shock"]', T["next"], 0.0, "CONSTANT")
sc.frame_start, sc.frame_end = 1, F(END)

# ------------------------------------------------------------------------------------------- render
if MODE == "visible":
    sys.path.insert(0, "D:/why habibi/_style_kit/mascot/batata3d"); import batata3d as B3
    B3.visible_frames(sc, lambda o: any(k in o.name.lower() for k in ("nightstand", "alarm_clock", "_hand", "mug", "phone")) or o.name in ("Mug", "Phone"), END, OUT)
    raise SystemExit
os.makedirs(OUT, exist_ok=True)
if MODE == "preview":
    step = int(ARGS[3]) if len(ARGS) > 3 else 3
    sc.render.resolution_percentage = 50; sc.eevee.taa_render_samples = 8
    t0 = time.time()
    for fr in range(1, F(END) + 1, step):
        sc.frame_set(fr); sc.render.filepath = os.path.join(OUT, f"p_{fr:05d}.png"); bpy.ops.render.render(write_still=True)
    print("PREVIEW", (F(END) + step - 1) // step, "frames", round(time.time() - t0, 1), "s")
elif MODE == "stills":
    for t in ARGS[3:]:
        fr = F(float(t)); sc.frame_set(fr); sc.render.filepath = os.path.join(OUT, f"s_{float(t):06.2f}.png"); bpy.ops.render.render(write_still=True)
    print("STILLS done")
elif MODE == "final":
    f0, f1 = int(ARGS[3]), int(ARGS[4]); sc.eevee.taa_render_samples = 16; t0 = time.time()
    for fr in range(f0, min(f1, F(END)) + 1):
        sc.frame_set(fr); sc.render.filepath = os.path.join(OUT, f"f_{fr:05d}.png")
        if not os.path.exists(sc.render.filepath): bpy.ops.render.render(write_still=True)
    print("FINAL", f0, f1, round(time.time() - t0, 1), "s")
