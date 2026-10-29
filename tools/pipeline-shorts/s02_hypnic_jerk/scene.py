"""Short #2 (hypnic jerk) 3D scene for Blender 5.2 (run: blender -b --factory-startup --python scene.py -- <mode> ...).
Everything procedural + CC0: night bedroom, bed/duvet/pillow, a REAL-potato 3D Batata (photo skin + marker faces
front-projected), nightcap, Poly Haven nightstand + alarm clock, warm lamp + cold moonlight. Eevee, 1080x1920.
modes:  still <out.png> [face]     one look-test frame"""
import bpy, bmesh, math, sys, os, time
from mathutils import Vector

TEX = "D:/why habibi/shorts/s02_hypnic_jerk/tex/"
PH = "E:/AskHabibiAI/assets/polyhaven/"
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["still", "D:/why habibi/shorts/s02_hypnic_jerk/look_test.png"]

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, color, rough=0.6, emit=None, strength=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m

def box(name, size, loc, material, bevel=0.02, subdiv=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel: m = o.modifiers.new("bev", "BEVEL"); m.width = bevel; m.segments = 3
    if subdiv: s = o.modifiers.new("sub", "SUBSURF"); s.levels = subdiv; s.render_levels = subdiv
    o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o

def image_node(nt, path, alpha=True):
    n = nt.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(path); n.interpolation = "Cubic"
    n.extension = "EXTEND"; return n

def potato(loc=(0, 0, 0), rot=(0, 0, 0), height=1.0, faces=("sleepy", "shocked"), lod=2, name="Batata"):
    """UV sphere shaped like the photo silhouette; UVs = front projection of the photo; faces mixed on the front only"""
    W, H = 1068 / 1508 * height, height
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96 if lod > 1 else 48, ring_count=48 if lod > 1 else 24, radius=0.5)
    o = bpy.context.object; o.name = name; o.scale = (W, 0.58 * W, H); bpy.ops.object.transform_apply(scale=True)
    me = o.data; bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts:                                              # slightly flatter bottom, fuller top like the photo
        z = v.co.z / (H / 2); v.co.x *= 1 + 0.06 * z; v.co.y *= 1 + 0.04 * z
    uv = bm.loops.layers.uv.verify()                                 # overwrite the sphere's own UVs (the active map)
    xs = [v.co.x for v in bm.verts]; zs = [v.co.z for v in bm.verts]; x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    for f in bm.faces:
        for l in f.loops:
            l[uv].uv = ((l.vert.co.x - x0) / (x1 - x0), (l.vert.co.z - z0) / (z1 - z0))
    bm.to_mesh(me); bm.free()
    # front mask as a vertex attribute (1 on the front, fading at the sides)
    attr = me.attributes.new("front", "FLOAT", "POINT")
    for i, v in enumerate(me.vertices): attr.data[i].value = max(0.0, min(1.0, (-v.co.y / (0.29 * W) - 0.15) * 1.6))
    tx = bpy.data.textures.new("lumps", "CLOUDS"); tx.noise_scale = 0.22
    d = o.modifiers.new("lumps", "DISPLACE"); d.texture = tx; d.strength = 0.025; d.texture_coords = "LOCAL"
    s = o.modifiers.new("sub", "SUBSURF"); s.levels = 1; s.render_levels = lod
    bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new("batata"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    skin = image_node(nt, TEX + "potato_skin.png"); b.inputs["Roughness"].default_value = 0.55
    out_col = skin.outputs["Color"]
    att = nt.nodes.new("ShaderNodeAttribute"); att.attribute_name = "front"
    face_nodes = []
    for k, fname in enumerate(faces):
        f = image_node(nt, TEX + f"face_{fname}.png"); f.name = f"face_{fname}"
        mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; nt.links.new(f.outputs["Alpha"], mul.inputs[0]); nt.links.new(att.outputs["Fac"], mul.inputs[1])
        sel = nt.nodes.new("ShaderNodeMath"); sel.operation = "MULTIPLY"; sel.name = f"sel_{fname}"; sel.inputs[1].default_value = 1.0 if k == 0 else 0.0
        nt.links.new(mul.outputs[0], sel.inputs[0])
        if len(faces) == 2:                                          # face chosen by the object property "shock" (0 sleepy, 1 shocked)
            if k == 0:
                shock = nt.nodes.new("ShaderNodeAttribute"); shock.attribute_type = "OBJECT"; shock.attribute_name = "shock"
                inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
                nt.links.new(shock.outputs["Fac"], inv.inputs[1]); nt.links.new(inv.outputs[0], sel.inputs[1])
            else: nt.links.new(shock.outputs["Fac"], sel.inputs[1])
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; nt.links.new(sel.outputs[0], mix.inputs["Factor"])
        nt.links.new(out_col, mix.inputs["A"]); mix.inputs["B"].default_value = (0.03, 0.025, 0.02, 1); out_col = mix.outputs["Result"]
        face_nodes.append(sel)
    nt.links.new(out_col, b.inputs["Base Color"])
    xr = nt.nodes.new("ShaderNodeAttribute"); xr.attribute_type = "OBJECT"; xr.attribute_name = "xray"   # 1 = see-through
    al = nt.nodes.new("ShaderNodeMath"); al.operation = "MULTIPLY_ADD"; al.inputs[1].default_value = -0.82; al.inputs[2].default_value = 1.0
    nt.links.new(xr.outputs["Fac"], al.inputs[0]); nt.links.new(al.outputs[0], b.inputs["Alpha"])
    o["shock"] = 0.0; o["xray"] = 0.0
    b.inputs["Subsurface Weight"].default_value = 0.08; b.inputs["Subsurface Radius"].default_value = (0.4, 0.25, 0.15)
    me.materials.append(m)
    return o, H, W

def nightcap(parent, H, W, tilt=22):
    """built in the potato's local space (potato at the origin), then parented without an inverse"""
    zb = 0.30 * H; d = 0.52 * H                                             # band height on the head, cap length
    r = 0.5 * W * math.sqrt(max(0.0, 1 - (zb / (0.5 * H)) ** 2)) * 0.97
    bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=r * 1.03, radius2=0.012, depth=d, location=(0, 0, d / 2))
    c = bpy.context.object; c.name = "Nightcap"
    for v in c.data.vertices: v.co.y *= 0.68; v.co.z += d / 2              # oval like the head; base at the origin
    c.location = (0, 0, zb - 0.02 * H); c.rotation_euler = (0, math.radians(tilt), 0)
    sub = c.modifiers.new("sub", "SUBSURF"); sub.levels = 1; sub.render_levels = 2; bpy.ops.object.shade_smooth()
    c.data.materials.append(mat("cap", (1.0, 0.62, 0.05), 0.8))
    bpy.ops.mesh.primitive_torus_add(major_radius=r * 1.0, minor_radius=0.038 * W, location=(0, 0, zb), major_segments=96)
    t = bpy.context.object; t.name = "CapBand"
    for v in t.data.vertices: v.co.y *= 0.68
    t.data.materials.append(mat("capband", (0.95, 0.95, 0.97), 0.9)); bpy.ops.object.shade_smooth()
    a = math.radians(tilt)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08 * W, location=(d * math.sin(a), 0, zb - 0.02 * H + d * math.cos(a)))
    p = bpy.context.object; p.name = "Pompom"; p.data.materials.append(mat("pompom", (0.97, 0.97, 0.99), 0.9)); bpy.ops.object.shade_smooth()
    for o in (c, t, p): o.parent = parent
    return c, t, p

def duvet(color, body=(0.0, 0.42), size=(1.86, 1.62), z=0.70):
    """a thick quilt: a subdivided grid raised over the body (an ellipsoid bump) and draped over the bed edges, + folds"""
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=90, y_subdivisions=80, size=1, location=(0, -0.08, z))
    o = bpy.context.object; o.name = "Duvet"
    for v in o.data.vertices:
        x, y = v.co.x * size[0], v.co.y * size[1]; v.co.x, v.co.y = x, y
        bx, by = (x - body[0]) / 0.42, (y - (body[1] - 0.08 - 0.62)) / 0.75     # the body lump under the quilt
        lump = max(0.0, 1 - bx * bx - by * by) ** 0.6 * 0.22
        edge = max(0.0, abs(x) - 0.80) * 2.2                                    # drape down over the bed sides
        v.co.z = lump - min(edge, 0.58) + 0.018 * math.sin(x * 7 + y * 3) * (1 - min(1, edge))
    sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.07
    tx = bpy.data.textures.new("folds", "CLOUDS"); tx.noise_scale = 0.28
    dd = o.modifiers.new("folds", "DISPLACE"); dd.texture = tx; dd.strength = 0.035
    sub = o.modifiers.new("sub", "SUBSURF"); sub.levels = 1; sub.render_levels = 1
    o.data.materials.append(mat("duvet", color, 0.9)); bpy.ops.object.shade_smooth(); return o

def clear_glass():
    """Poly Haven glass (BLENDED, textured) renders as a black disc in Eevee here: make it a faint clear glass"""
    for m in bpy.data.materials:
        if m.name.endswith("_Glass") and m.use_nodes:
            b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
            if not b: continue
            for k in ("Alpha", "Base Color"):
                for l in list(b.inputs[k].links): m.node_tree.links.remove(l)
            b.inputs["Base Color"].default_value = (1, 1, 1, 1); b.inputs["Alpha"].default_value = 0.06; b.inputs["Roughness"].default_value = 0.05

def import_gltf(asset, loc, rot_z=0.0, scale=1.0, surface=None):
    """import a Poly Haven glTF under ONE parent empty (keeps the parts' relative positions, e.g. clock hands), then
    place it: rotate/scale the parent, put it at loc (x, y) and, if `surface` is given, sit its lowest point on that z"""
    path = PH + asset + "/" + [f for f in os.listdir(PH + asset) if f.endswith(".gltf")][0]
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=path); new = [o for o in bpy.data.objects if o not in before]
    root = bpy.data.objects.new(asset + "_root", None); bpy.context.scene.collection.objects.link(root)
    for o in new:
        if o.parent is None: o.parent = root
    root.rotation_euler = (0, 0, rot_z); root.scale = (scale,) * 3; root.location = loc
    if surface is not None:
        bpy.context.view_layer.update()
        zs = [(o.matrix_world @ Vector(c)).z for o in new if o.type == "MESH" for c in o.bound_box]
        root.location.z += surface - min(zs)
    return [root]

def build():
    clear(); sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"; sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.fps = 30
    sc.eevee.taa_render_samples = 32
    try: sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception: pass
    w = bpy.data.worlds.new("night"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.006, 0.016, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    # room
    box("Floor", (6, 6, 0.1), (0, 0, -0.05), mat("floor", (0.16, 0.10, 0.07), 0.45), bevel=0)
    box("WallBack", (6, 0.1, 4), (0, 1.6, 2), mat("wall", (0.05, 0.07, 0.15), 0.9), bevel=0)
    box("WallLeft", (0.1, 6, 4), (-2.6, 0, 2), mat("wall2", (0.05, 0.065, 0.14), 0.9), bevel=0)
    box("Window", (0.02, 1.0, 1.3), (-2.54, 0.2, 2.2), mat("window", (0.1, 0.15, 0.3), 0.3, emit=(0.45, 0.6, 1.0), strength=4.0), bevel=0)
    # bed
    wood = mat("bedwood", (0.32, 0.18, 0.10), 0.45)
    box("Headboard", (1.8, 0.12, 1.2), (0, 1.45, 0.6), wood, bevel=0.04)
    box("BedFrame", (1.8, 2.4, 0.35), (0, 0.3, 0.2), wood, bevel=0.03)
    box("Mattress", (1.7, 2.3, 0.25), (0, 0.3, 0.5), mat("sheet", (0.92, 0.92, 0.95), 0.8), bevel=0.06)
    pil = box("Pillow", (0.95, 0.42, 0.22), (0, 1.12, 0.74), mat("pillow", (0.95, 0.95, 0.98), 0.85), bevel=0.0, subdiv=3)
    duv = duvet((0.06, 0.10, 0.32))
    # batata, reclined on the pillow, under the duvet to the chest
    b, H, W = potato(height=0.95); nightcap(b, H, W)
    b.location = (0, 0.78, 0.98); b.rotation_euler = (math.radians(-52), 0, 0)
    # props
    import_gltf("ClassicNightstand_01", (1.3, 1.1, 0), rot_z=math.radians(180), scale=1.0)
    import_gltf("alarm_clock_01", (1.25, 1.08, 0.0), rot_z=math.radians(20), scale=1.6, surface=0.70); clear_glass()
    # lights
    bpy.ops.object.light_add(type="AREA", location=(1.6, 0.4, 2.2)); L = bpy.context.object; L.data.energy = 70; L.data.size = 0.6
    L.data.color = (1.0, 0.72, 0.42); L.rotation_euler = (math.radians(30), math.radians(40), 0)
    bpy.ops.object.light_add(type="AREA", location=(-2.2, 0.2, 2.4)); M = bpy.context.object; M.data.energy = 120; M.data.size = 1.0
    M.data.color = (0.55, 0.7, 1.0); M.rotation_euler = (0, math.radians(-60), 0)
    bpy.ops.object.light_add(type="POINT", location=(1.25, 1.05, 1.05)); P = bpy.context.object; P.data.energy = 18; P.data.color = (1.0, 0.62, 0.30)
    # camera: close-up of the face from the foot of the bed, slightly above
    bpy.ops.object.camera_add(location=(0.15, -1.15, 1.75)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 40
    tgt = bpy.data.objects.new("CamTarget", None); sc.collection.objects.link(tgt); tgt.location = (0, 0.82, 1.05)
    tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    bpy.ops.object.light_add(type="SPOT", location=(0.9, -0.6, 2.1)); K = bpy.context.object; K.data.energy = 90; K.data.spot_size = math.radians(35)
    K.data.spot_blend = 0.8; K.data.color = (1.0, 0.80, 0.60); kc = K.constraints.new("TRACK_TO"); kc.target = b; kc.track_axis = "TRACK_NEGATIVE_Z"; kc.up_axis = "UP_Y"
    cam.data.dof.use_dof = True; cam.data.dof.focus_object = b; cam.data.dof.aperture_fstop = 2.8
    return sc

def facetest(out, face="sleepy"):
    clear(); sc = bpy.context.scene; sc.render.engine = "BLENDER_EEVEE"; sc.render.resolution_x, sc.render.resolution_y = 720, 1080
    sc.eevee.taa_render_samples = 16; sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.4, 0.45, 0.55, 1)
    b, H, W = potato(height=1.0); nightcap(b, H, W)
    nt = b.active_material.node_tree
    for n in nt.nodes:
        if n.name.startswith("sel_"): n.inputs[1].default_value = 1.0 if n.name == "sel_" + face else 0.0
    bpy.ops.object.light_add(type="AREA", location=(1.5, -2.5, 2.0)); L = bpy.context.object; L.data.energy = 300; L.data.size = 2
    L.rotation_euler = (math.radians(55), 0, math.radians(30))
    bpy.ops.object.camera_add(location=(0, -3.2, 0.1)); cam = bpy.context.object; sc.camera = cam; cam.rotation_euler = (math.radians(90), 0, 0); cam.data.lens = 50
    sc.render.filepath = out; bpy.ops.render.render(write_still=True); print("RENDERED", out)


if __name__ == "__main__":
    mode = ARGS[0]
    if mode == "facetest": facetest(ARGS[1], ARGS[2] if len(ARGS) > 2 else "sleepy")
    if mode == "still":
        sc = build(); out = ARGS[1]
        if len(ARGS) > 2:
            bpy.data.objects["Batata"]["shock"] = 1.0 if ARGS[2] == "shocked" else 0.0
        sc.render.filepath = out; t0 = time.time(); bpy.ops.render.render(write_still=True)
        print("RENDERED", out, round(time.time() - t0, 1), "s")
        bpy.ops.wm.save_as_mainfile(filepath=out.replace(".png", ".blend"))
