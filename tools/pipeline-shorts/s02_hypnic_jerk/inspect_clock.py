import bpy, os
PH = "E:/AskHabibiAI/assets/polyhaven/alarm_clock_01/"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=PH + [f for f in os.listdir(PH) if f.endswith(".gltf")][0])
for o in bpy.data.objects:
    print("OBJ", o.name, o.type, [s.material.name if s.material else None for s in o.material_slots])
for m in bpy.data.materials:
    if not m.use_nodes: continue
    b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if b: print("MAT", m.name, "transmission", round(b.inputs["Transmission Weight"].default_value, 2), "alpha", round(b.inputs["Alpha"].default_value, 2), "linked base", b.inputs["Base Color"].is_linked, "blend", getattr(m, "surface_render_method", "?"))
