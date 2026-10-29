import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:1] + ["--", "still", "x.png"]
import scene as S
from mathutils import Vector
S.build()
def wb(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [round(min(c[i] for c in cs), 3) for i in range(3)], [round(max(c[i] for c in cs), 3) for i in range(3)]
for o in bpy.data.objects:
    if o.type == "MESH" and o.name not in ("Floor", "WallBack", "WallLeft", "Window", "Duvet", "Batata", "Mattress", "BedFrame", "Headboard", "Pillow"):
        print("OBJ", o.name, "parent", o.parent.name if o.parent else None, "rot", [round(v, 2) for v in o.rotation_euler], "bbox", wb(o))
for o in bpy.data.objects:
    if o.parent is None and o.type == "EMPTY": print("ROOT", o.name, [round(v, 2) for v in o.rotation_euler], [round(v, 2) for v in o.location])
