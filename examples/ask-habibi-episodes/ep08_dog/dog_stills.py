"""Potato-dog stickers for Ep 8 (transparent PNGs, our real-potato 3D dog from batata3d).
  blender -b --factory-startup --python dog_stills.py
-> D:/why habibi/_media/cutouts/potato_dog_{sleepy,shocked,sideeye,fine}.png"""
import sys, math
sys.path.insert(0, "D:/why habibi/_style_kit/mascot/batata3d")
import bpy
import batata3d as B3

OUT = "D:/why habibi/_media/cutouts/potato_dog_{}.png"
sc = B3.render_setup(samples=64, world=(0.05, 0.05, 0.05))
sc.render.resolution_x, sc.render.resolution_y = 1400, 1100; sc.render.film_transparent = True
root, head = B3.potato_dog((0, 0, 0), rot_z=math.radians(-28), size=1.0)
cam, tgt = B3.camera_rig(loc=(-0.55, -2.55, 1.05), target=(0.05, 0.05, 0.40), lens=50)
B3.key_light(tgt, loc=(1.6, -1.6, 2.4), energy=420, color=(1.0, 0.86, 0.70), size=50)
bpy.ops.object.light_add(type="AREA", location=(-2.0, -1.0, 1.6)); fill = bpy.context.object; fill.data.energy = 160; fill.data.size = 3.0
fill.rotation_euler = (math.radians(60), 0, math.radians(-60)); fill.data.color = (0.75, 0.85, 1.0)
bpy.ops.object.light_add(type="AREA", location=(0.0, 2.2, 1.8)); rim = bpy.context.object; rim.data.energy = 220; rim.data.size = 2.0
rim.rotation_euler = (math.radians(-55), 0, 0)
for idx, name in enumerate(("sleepy", "shocked", "sideeye", "fine")):
    head["face"] = float(idx); head.update_tag(); bpy.context.view_layer.update()
    sc.render.filepath = OUT.format(name); bpy.ops.render.render(write_still=True); print("wrote", sc.render.filepath, flush=True)
