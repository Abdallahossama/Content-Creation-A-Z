import bpy, sys, math
sys.path.insert(0, "D:/why habibi/_style_kit/mascot/batata3d")
import batata3d as B3
sc = B3.render_setup(16)
P = B3.kitchen(); P["hinge"].rotation_euler = (0, 0, math.radians(-105)); P["fridge_light"].data.energy = 60
for n in ("FridgeBody", "FridgeInside"): bpy.data.objects[n].hide_render = True
# fridge contents in the foreground
B3.box("Milk", (0.10, 0.10, 0.24), (0.12, 0.66, 1.07), B3.mat("milk", (0.95, 0.95, 0.97), 0.4), bevel=0.01)
B3.box("Jar", (0.11, 0.11, 0.13), (0.58, 0.68, 1.02), B3.mat("jar", (0.9, 0.3, 0.2), 0.2), bevel=0.03)
b, H, W = B3.potato(height=0.95, faces=("sideeye", "shocked", "sleepy", "fine")); B3.nightcap(b, H, W)
b.location = (0.35, -0.35, 0.50); b.rotation_euler = (0, 0, math.radians(180)); b["face"] = 0.0
sl = B3.pizza_slice((0.30, -0.08, 0.80), 0.20); sl.rotation_euler = (math.radians(-90), 0, math.radians(180))
cam, tgt = B3.camera_rig((0.36, 0.80, 1.12), (0.35, -0.35, 0.92), 30)
sc.render.resolution_percentage = 50; sc.render.filepath = sys.argv[-1]; bpy.ops.render.render(write_still=True); print("RENDERED")
