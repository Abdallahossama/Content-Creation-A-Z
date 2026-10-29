import bpy, sys, math
sys.path.insert(0, "D:/why habibi/_style_kit/mascot/batata3d")
import batata3d as B3
sc = B3.render_setup(16)
B3.bedroom(duvet_body=(-0.25, 0.42), duvet_width=0.38)
b, H, W = B3.potato(height=0.95, faces=("sleepy", "shocked", "sideeye", "fine")); B3.nightcap(b, H, W)
b.location = (-0.30, 0.78, 0.98); b.rotation_euler = (math.radians(-52), 0, math.radians(-8))
dog, head = B3.potato_dog((0.45, 0.45, 0.80), rot_z=math.radians(12), size=0.62)
cam, tgt = B3.camera_rig((0.10, -1.55, 1.95), (0.05, 0.7, 0.95), 34); B3.key_light(tgt)
sc.render.resolution_percentage = 50; sc.render.filepath = sys.argv[-1]; bpy.ops.render.render(write_still=True); print("RENDERED")
