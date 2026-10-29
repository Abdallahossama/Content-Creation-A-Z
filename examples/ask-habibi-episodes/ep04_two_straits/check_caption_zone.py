"""Find every on-screen note / word / sticker that lands in the caption zone (captions cover it).
Caption zone = where the burned-in captions sit (Rubik 72, MarginV 108): x 420-1500, y 860-1010. Corners stay free."""
from beats_ep04 import *
from ep04_fx import Note, Big, Sticker, Pasted, Tick, Arrow, Circle, Underline, Strike, Bar, Censor

CAP = (420, 860, 1500, 1010)

def bbox(o):
    k = type(o).__name__
    if k == "Note":
        text, x, y, size, color, rot, anchor = o.a; im = hand(text, size, color, rot=rot)
        return (x - im.width / 2, y - im.height / 2, x + im.width / 2, y + im.height / 2) if anchor == "c" else (x, y, x + im.width, y + im.height)
    if k == "Big":
        w, h = o.img.size
        return (o.x - w / 2, o.y - h / 2, o.x + w / 2, o.y + h / 2) if o.anchor == "c" else (o.x, o.y, o.x + w, o.y + h)
    if k == "Sticker":
        path, h, x, y, rot, mirror = o.a; w = h * 0.75
        return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if k == "Pasted":
        return (o.x - o.img.width / 2, o.y - o.img.height / 2, o.x + o.img.width / 2, o.y + o.img.height / 2)
    if k == "Tick":
        x, y, s = o.a[:3]; return (x - s * 0.5, y - s * 0.6, x + s * 0.6, y + s * 0.4)
    if k in ("Underline", "Strike"):
        x0, x1, y = o.a[:3]; return (x0, y - 25, x1, y + 25)
    if k == "Bar":
        x, base, w, h = o.a[:4]; return (x, base - h - 110, x + w, base + 75)
    if k == "Circle":
        cx, cy, rx, ry = o.a[:4]; return (cx - rx, cy - ry, cx + rx, cy + ry)
    if k == "Arrow":
        (x0, y0), (x1, y1) = o.a[:2]; return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
    return None

def hits():
    out = []
    for i, b in enumerate(BEATS):
        if b.name in ("end_screen",): continue
        for o in b.ovs:
            bb = bbox(o)
            if not bb: continue
            ix = min(bb[2], CAP[2]) - max(bb[0], CAP[0]); iy = min(bb[3], CAP[3]) - max(bb[1], CAP[1])
            if ix > 20 and iy > 12:
                label = o.a[0] if type(o).__name__ == "Note" else (getattr(o, "text", "") or type(o).__name__)
                out.append((i, b.name, type(o).__name__, str(label).replace("\n", " ")[:40], [int(v) for v in bb]))
    return out

if __name__ == "__main__":
    h = hits(); print(len(h), "overlays in the caption zone")
    for r in h: print(f"  {r[0]:02d} {r[1]:14s} {r[2]:9s} {r[3]:40s} {r[4]}")
