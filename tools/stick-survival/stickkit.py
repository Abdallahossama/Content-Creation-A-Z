"""stickkit: hand-drawn-style stick-figure scenes with pycairo (1920x1080). No AI images.
Characters = black stick limbs + coloured shirt + white round head (zombies: grey-green head, arms forward).
Scene = background painter + actors (animated poses) + props + camera move + optional day stamp.
  from stickkit import *; img = render(scene_dict, u, dur)   -> PIL RGBA
Coordinates: canvas 1920x1080, GROUND = 905 (feet line) unless the background says otherwise."""
import math, random
import cairo, numpy as np
from PIL import Image

W, H = 1920, 1080
GROUND = 905
INK = (0.08, 0.08, 0.09)
HAND = "Ink Free"           # Windows handwriting font (day stamps, wall writing)
BOLD = "Arial Black"

def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k
def cl(x): return min(max(x, 0.0), 1.0)

# ------------------------------------------------------------------ characters
CAST = {   # shirt colour, hat, extras
    "me":     dict(shirt="#2e8b57", hat="cap", hatc="#c0392b", apron="#2e8b57", tag=True),
    "rick":   dict(shirt="#f2f2f2", tie="#1f4e8c", glasses=True, hair="#5b4636"),
    "walt":   dict(shirt="#f5efe2", hat="chef", apron="#ffffff", hair="#bdbdbd", moustache=True),
    "marcus": dict(shirt="#24324a", hat="guard", hatc="#24324a", badge=True),
    "dex":    dict(shirt="#e67e22", hood=True, hair="#2b2b2b"),
    "zombie": dict(shirt="#6b7d5c", zombie=True),
    "zombie2": dict(shirt="#7a5c5c", zombie=True),
    "zombie3": dict(shirt="#4f6a7a", zombie=True),
    "man":    dict(shirt="#8e8e8e"),
    "soldier": dict(shirt="#5b6b3a", hat="helmet", hatc="#4a5a2e"),
}
SEG = dict(torso=112, neck=6, head=56, ua=62, la=58, ul=78, ll=78)

POSES = {
    "stand":   dict(ls=8, le=-6, rs=-8, re=6, lh=4, lk=0, rh=-4, rk=0),
    "worried": dict(ls=28, le=95, rs=24, re=100, lh=4, lk=0, rh=-4, rk=0, head=6),
    "scared":  dict(ls=150, le=10, rs=140, re=20, lh=10, lk=-6, rh=-12, rk=6, lean=-8),
    "point":   dict(ls=8, le=-6, rs=95, re=0, lh=4, lk=0, rh=-4, rk=0),
    "carry":   dict(ls=60, le=50, rs=55, re=55, lh=4, lk=0, rh=-4, rk=0, lean=4),
    "push":    dict(ls=80, le=10, rs=75, re=12, lh=20, lk=-10, rh=-18, rk=12, lean=18),
    "write":   dict(ls=8, le=-6, rs=120, re=-20, lh=4, lk=0, rh=-4, rk=0),
    "radio":   dict(ls=8, le=-6, rs=30, re=140, lh=4, lk=0, rh=-4, rk=0, head=-8),
    "think":   dict(ls=8, le=-6, rs=35, re=135, lh=4, lk=0, rh=-4, rk=0, head=8),
    "sit":     dict(ls=20, le=40, rs=25, re=45, lh=85, lk=-85, rh=80, rk=-80, dy=58),
    "hug_knees": dict(ls=50, le=80, rs=45, re=85, lh=120, lk=-150, rh=115, rk=-145, dy=95, lean=20),
    "zombie":  dict(ls=88, le=4, rs=82, re=8, lh=6, lk=-4, rh=-6, rk=4, lean=10, head=18),
    "climb":   dict(ls=165, le=10, rs=120, re=30, lh=40, lk=-60, rh=-5, rk=0),
    "lie":     dict(ls=20, le=0, rs=-20, re=0, lh=6, lk=0, rh=-6, rk=0, lie=True),
    "cheer":   dict(ls=160, le=-10, rs=-160, re=10, lh=4, lk=0, rh=-4, rk=0),
    "shrug":   dict(ls=40, le=-100, rs=-40, re=100, lh=4, lk=0, rh=-4, rk=0),
    "eat":     dict(ls=20, le=40, rs=30, re=140, lh=85, lk=-85, rh=80, rk=-80, dy=58),
    "throw":   dict(ls=-30, le=0, rs=170, re=-30, lh=15, lk=0, rh=-15, rk=0, lean=-6),
    "crouch":  dict(ls=40, le=40, rs=35, re=45, lh=70, lk=-110, rh=60, rk=-100, dy=60, lean=25),
}
def walk_pose(ph, amp=1.0, run=False):
    s = math.sin(ph * 2 * math.pi); c = math.cos(ph * 2 * math.pi)
    a = (34 if run else 24) * amp
    p = dict(ls=-s * a, le=(30 if run else 12), rs=s * a, re=(30 if run else 12),
             lh=s * a, lk=-max(0, -c) * (60 if run else 35) * amp, rh=-s * a, rk=-max(0, c) * (60 if run else 35) * amp,
             lean=(14 if run else 3), dy=-abs(c) * (10 if run else 5) * amp)
    return p
def zombie_walk(ph):
    p = dict(POSES["zombie"]); s = math.sin(ph * 2 * math.pi); c = math.cos(ph * 2 * math.pi)
    p.update(lh=s * 14, rh=-s * 14, lk=-max(0, -c) * 18, rk=-max(0, c) * 18, dy=-abs(c) * 3, head=18 + s * 6, ls=88 + s * 6, rs=82 - s * 6)
    return p
def mix(p0, p1, k):
    out = dict(p0)
    for key, v in p1.items():
        if isinstance(v, bool): out[key] = v if k > 0.5 else p0.get(key, False)
        else: out[key] = lerp(p0.get(key, 0.0), v, k)
    return out

class Actor:
    """who: CAST key. path: list of (u_sec, x) keyframes. act: 'stand'|'walk'|'run'|'zwalk'|pose name|list of (u_sec, pose).
    face: expression or list of (u_sec, face). f: facing (+1 right, -1 left)."""
    def __init__(self, who, x=960, path=None, act="stand", face="neutral", f=1, s=1.3, y=None, talk=None, hold=None, flip_at=None, alpha=1.0, z=0, baggy=1.0, bandage=False):
        self.who, self.x, self.path, self.act, self.face, self.f, self.s, self.y = who, x, path, act, face, f, s, y
        self.talk, self.hold, self.flip_at, self.alpha, self.z, self.baggy, self.bandage = talk, hold, flip_at, alpha, z, baggy, bandage

    def at(self, u):
        x = self.x
        if self.path:
            pts = self.path
            if u <= pts[0][0]: x = pts[0][1]
            elif u >= pts[-1][0]: x = pts[-1][1]
            else:
                for (u0, x0), (u1, x1) in zip(pts, pts[1:]):
                    if u0 <= u <= u1: x = lerp(x0, x1, (u - u0) / max(1e-6, u1 - u0)); break
        moving = False
        if self.path:
            for (u0, x0), (u1, x1) in zip(self.path, self.path[1:]):
                if u0 <= u <= u1 and abs(x1 - x0) > 1: moving = True
        act = self.act
        if isinstance(act, list):
            cur = act[0][1]; prev = cur; k = 1.0
            for i, (ua, pa) in enumerate(act):
                if u >= ua: prev = act[i - 1][1] if i else pa; cur = pa; k = cl((u - ua) / 0.25)
            pose = mix(self._pose(prev, u, moving), self._pose(cur, u, moving), k)
        else: pose = self._pose(act, u, moving)
        face = self.face
        if isinstance(face, list):
            cur = face[0][1]
            for ua, fa in face:
                if u >= ua: cur = fa
            face = cur
        f = self.f
        if self.flip_at is not None and u >= self.flip_at: f = -f
        return x, pose, face, f

    def _pose(self, act, u, moving):
        sp = 1.6 if act == "walk" else 2.6 if act == "run" else 1.1
        if act == "walk": return walk_pose(u * sp) if moving or self.path is None else dict(POSES["stand"])
        if act == "run": return walk_pose(u * sp, run=True) if moving or self.path is None else dict(POSES["stand"])
        if act == "zwalk": return zombie_walk(u * sp)
        if act == "idle":
            p = dict(POSES["stand"]); b = math.sin(u * 2.2) * 2; p.update(ls=8 + b, rs=-8 - b, head=math.sin(u * 1.3) * 3); return p
        if act == "shiver":
            p = dict(POSES["hug_knees"]); p["lean"] = 20 + math.sin(u * 30) * 1.5; return p
        if act == "zidle":
            p = dict(POSES["zombie"]); p["head"] = 18 + math.sin(u * 1.7) * 8; p["ls"] = 88 + math.sin(u * 2) * 5; return p
        if act == "talk":
            p = dict(POSES["stand"]); p["rs"] = -8 + 30 * (0.5 + 0.5 * math.sin(u * 4)); p["re"] = 40; return p
        return dict(POSES.get(act, POSES["stand"]))

def limb(c, x, y, a1, l1, a2, l2, f, lw):
    ax, ay = x + math.sin(math.radians(a1)) * l1 * f, y + math.cos(math.radians(a1)) * l1
    bx, by = ax + math.sin(math.radians(a1 + a2)) * l2 * f, ay + math.cos(math.radians(a1 + a2)) * l2
    c.move_to(x, y); c.line_to(ax, ay); c.line_to(bx, by); c.set_line_width(lw); c.stroke()
    return (ax, ay), (bx, by)

def draw_actor(c, a, u, ground=GROUND):
    x, p, face, f = a.at(u)
    st = CAST.get(a.who, CAST["man"]); s = a.s; lw = 9 * s
    y0 = (a.y if a.y is not None else ground)
    c.save()
    if p.get("lie"):
        c.translate(x, y0 - 12 * s); c.rotate(math.radians(-90 * f)); c.translate(-x, -(y0 - 12 * s))
    lean = math.radians(p.get("lean", 0)); dy = p.get("dy", 0) * s
    hip = (x, y0 - (SEG["ul"] + SEG["ll"]) * s + dy)
    tv = (math.sin(lean) * f, -math.cos(lean))
    neck = (hip[0] + tv[0] * SEG["torso"] * s, hip[1] + tv[1] * SEG["torso"] * s)
    ht = math.radians(p.get("head", 0) + p.get("lean", 0))
    hc = (neck[0] + math.sin(ht) * f * (SEG["head"] + SEG["neck"]) * s, neck[1] - math.cos(ht) * (SEG["head"] + SEG["neck"]) * s)
    sh = (neck[0] + tv[0] * -8 * s, neck[1] + tv[1] * -8 * s)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    zomb = st.get("zombie")
    dark = tuple(v * 0.75 for v in INK)
    # back limbs
    c.set_source_rgba(*dark, a.alpha)
    limb(c, hip[0], hip[1], p.get("rh", 0) + p.get("lean", 0) * 0, SEG["ul"] * s, p.get("rk", 0), SEG["ll"] * s, f, lw)
    limb(c, sh[0], sh[1], p.get("rs", 0), SEG["ua"] * s, p.get("re", 0), SEG["la"] * s, f, lw)
    # shirt / torso
    bx, by = hip; nx, ny = sh; wt, wb = 38 * s * a.baggy, 33 * s * a.baggy * (1.25 if a.baggy > 1 else 1)
    px, py = -tv[1], tv[0]
    c.move_to(nx + px * wt, ny + py * wt); c.line_to(nx - px * wt, ny - py * wt); c.line_to(bx - px * wb, by - py * wb + 6 * s); c.line_to(bx + px * wb, by + py * wb + 6 * s); c.close_path()
    c.set_source_rgba(*rgb(st["shirt"]), a.alpha); c.fill_preserve(); c.set_source_rgba(*INK, a.alpha); c.set_line_width(4 * s); c.stroke()
    if st.get("apron"):
        c.move_to(nx + px * wt * 0.6 + tv[0] * -40 * s, ny + py * wt * 0.6 + tv[1] * -40 * s)
        c.line_to(nx - px * wt * 0.6 + tv[0] * -40 * s, ny - py * wt * 0.6 + tv[1] * -40 * s)
        c.line_to(bx - px * wb * 0.9 + tv[0] * 30 * s, by - py * wb * 0.9 + tv[1] * 30 * s + 6 * s)
        c.line_to(bx + px * wb * 0.9 + tv[0] * 30 * s, by + py * wb * 0.9 + tv[1] * 30 * s + 6 * s); c.close_path()
        col = rgb(st["apron"]); col = tuple(min(1, v * 1.15) for v in col) if a.who == "me" else col
        c.set_source_rgba(*col, a.alpha); c.fill_preserve(); c.set_source_rgba(*INK, a.alpha); c.set_line_width(3 * s); c.stroke()
    if st.get("tie"):
        c.move_to(nx, ny + 4 * s); c.line_to(nx - 6 * s, ny + 40 * s); c.line_to(nx, ny + 52 * s); c.line_to(nx + 6 * s, ny + 40 * s); c.close_path()
        c.set_source_rgba(*rgb(st["tie"]), a.alpha); c.fill()
    if st.get("badge"):
        c.arc(nx + f * 12 * s, ny + 26 * s, 6 * s, 0, 7); c.set_source_rgba(1, 0.82, 0.2, a.alpha); c.fill()
    if st.get("tag"):
        c.rectangle(nx + f * 6 * s, ny + 22 * s, 16 * s * f, 9 * s); c.set_source_rgba(1, 1, 1, a.alpha); c.fill()
    if zomb:   # torn shirt + stain
        c.arc(bx + 6 * s * f, by - 40 * s, 9 * s, 0, 7); c.set_source_rgba(0.45, 0.08, 0.08, 0.8 * a.alpha); c.fill()
    # front limbs
    c.set_source_rgba(*INK, a.alpha)
    limb(c, hip[0], hip[1], p.get("lh", 0), SEG["ul"] * s, p.get("lk", 0), SEG["ll"] * s, f, lw)
    el, hand = limb(c, sh[0], sh[1], p.get("ls", 0), SEG["ua"] * s, p.get("le", 0), SEG["la"] * s, f, lw)
    if a.bandage:
        c.set_source_rgba(1, 1, 1, a.alpha); c.set_line_width(lw * 2.2); c.move_to(lerp(sh[0], el[0], .35), lerp(sh[1], el[1], .35)); c.line_to(lerp(sh[0], el[0], .75), lerp(sh[1], el[1], .75)); c.stroke()
    if a.hold: draw_prop(c, a.hold, hand[0], hand[1], s * 0.8, f)
    # head
    r = SEG["head"] * s; hx, hy = hc
    if st.get("hood"):
        c.arc(hx, hy + 4 * s, r + 9 * s, 0, 2 * math.pi); c.set_source_rgba(*rgb(st["shirt"]), a.alpha); c.fill_preserve(); c.set_source_rgba(*INK, a.alpha); c.set_line_width(4 * s); c.stroke()
    c.arc(hx, hy, r, 0, 2 * math.pi)
    c.set_source_rgba(*(rgb("#a8b89a") if zomb else (1, 1, 1)), a.alpha); c.fill_preserve()
    c.set_source_rgba(*INK, a.alpha); c.set_line_width(5 * s); c.stroke()
    if st.get("hair"):
        c.arc(hx, hy, r, math.pi * 1.08, math.pi * 1.92); c.set_source_rgba(*rgb(st["hair"]), a.alpha); c.set_line_width(9 * s); c.stroke()
    draw_face(c, hx, hy, r, face if not zomb else "zombie", f, s, a.alpha, st, u, a.talk)
    draw_hat(c, st, hx, hy, r, f, s, a.alpha)
    c.restore()

def draw_face(c, hx, hy, r, face, f, s, al, st, u, talk):
    ex = hx + f * r * 0.22; ey = hy - r * 0.08; sp = r * 0.34
    c.set_source_rgba(*INK, al)
    if face == "zombie":
        for k in (-1, 1):
            c.arc(ex + k * sp, ey, r * 0.16, 0, 7); c.set_source_rgba(0.95, 0.95, 0.85, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.set_line_width(2.5 * s); c.stroke()
            c.arc(ex + k * sp + f * 2 * s, ey + 2 * s, r * 0.05, 0, 7); c.fill()
        c.move_to(ex - sp, hy + r * 0.45)
        for i in range(1, 6): c.line_to(ex - sp + i * sp * 0.4, hy + r * (0.38 if i % 2 else 0.5))
        c.set_line_width(3 * s); c.stroke(); return
    big = face in ("scared", "shock")
    for k in (-1, 1):
        if face in ("tired", "sleep"):
            c.move_to(ex + k * sp - r * 0.12, ey); c.line_to(ex + k * sp + r * 0.12, ey); c.set_line_width(3.5 * s); c.stroke()
        elif big:
            c.arc(ex + k * sp, ey, r * 0.16, 0, 7); c.set_source_rgba(1, 1, 1, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.set_line_width(2.5 * s); c.stroke()
            c.arc(ex + k * sp, ey, r * 0.06, 0, 7); c.fill()
        else:
            c.save(); c.translate(ex + k * sp, ey); c.scale(1, 1.35); c.arc(0, 0, r * 0.075, 0, 7); c.restore(); c.fill()
    by = ey - r * 0.27; c.set_line_width(3.5 * s)
    if face in ("worried", "sad", "scared"):
        c.move_to(ex - sp - r * 0.14, by + r * 0.02); c.line_to(ex - sp + r * 0.12, by - r * 0.08); c.stroke()
        c.move_to(ex + sp - r * 0.12, by - r * 0.08); c.line_to(ex + sp + r * 0.14, by + r * 0.02); c.stroke()
    elif face == "angry":
        c.move_to(ex - sp - r * 0.14, by - r * 0.08); c.line_to(ex - sp + r * 0.12, by + r * 0.04); c.stroke()
        c.move_to(ex + sp - r * 0.12, by + r * 0.04); c.line_to(ex + sp + r * 0.14, by - r * 0.08); c.stroke()
    my = hy + r * 0.42; mx = ex
    open_ = talk and (int(u * 7) % 2 == 0)
    if face in ("scared", "shock") or open_:
        c.save(); c.translate(mx, my); c.scale(1, 1.3 if big else 0.8); c.arc(0, 0, r * (0.14 if big else 0.1), 0, 7); c.restore(); c.fill()
    elif face in ("smile", "happy"):
        c.arc(mx, my - r * 0.12, r * 0.22, math.radians(25), math.radians(155)); c.stroke()
    elif face in ("sad", "worried"):
        c.arc(mx, my + r * 0.16, r * 0.2, math.radians(205), math.radians(335)); c.stroke()
    elif face == "smirk":
        c.move_to(mx - r * 0.18, my); c.curve_to(mx, my + r * 0.05, mx + r * 0.1, my, mx + r * 0.22, my - r * 0.12); c.stroke()
    else:
        c.move_to(mx - r * 0.15, my); c.line_to(mx + r * 0.15, my); c.stroke()
    if face == "sweat" or face == "scared":
        c.move_to(hx - f * r * 0.85, hy - r * 0.3); c.curve_to(hx - f * r * 1.0, hy, hx - f * r * 0.7, hy + r * 0.05, hx - f * r * 0.85, hy - r * 0.3)
        c.set_source_rgba(0.45, 0.75, 1, al); c.fill(); c.set_source_rgba(*INK, al)
    if st.get("moustache"):
        c.move_to(mx - r * 0.2, my - r * 0.12); c.curve_to(mx - r * 0.1, my - r * 0.2, mx + r * 0.1, my - r * 0.2, mx + r * 0.2, my - r * 0.12)
        c.set_source_rgba(0.6, 0.6, 0.6, al); c.set_line_width(5 * s); c.stroke(); c.set_source_rgba(*INK, al)
    if st.get("glasses"):
        c.set_line_width(2.5 * s)
        for k in (-1, 1): c.arc(ex + k * sp, ey, r * 0.17, 0, 7); c.stroke()
        c.move_to(ex - sp + r * 0.17, ey); c.line_to(ex + sp - r * 0.17, ey); c.stroke()

def draw_hat(c, st, hx, hy, r, f, s, al):
    h = st.get("hat")
    if not h: return
    col = rgb(st.get("hatc", "#333333"))
    c.set_line_width(3.5 * s)
    if h in ("cap", "guard"):
        c.arc(hx, hy - r * 0.15, r * 1.0, math.pi, 2 * math.pi); c.close_path()
        c.set_source_rgba(*col, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.stroke()
        c.move_to(hx + f * r * 0.2, hy - r * 0.15); c.line_to(hx + f * r * 1.55, hy - r * 0.05); c.line_to(hx + f * r * 1.5, hy - r * 0.22); c.line_to(hx + f * r * 0.2, hy - r * 0.3); c.close_path()
        c.set_source_rgba(*col, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.stroke()
        if h == "guard":
            c.arc(hx, hy - r * 0.6, r * 0.14, 0, 7); c.set_source_rgba(1, 0.82, 0.2, al); c.fill()
    elif h == "chef":
        c.rectangle(hx - r * 0.65, hy - r * 1.35, r * 1.3, r * 0.55); c.set_source_rgba(1, 1, 1, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.stroke()
        for k in (-0.45, 0, 0.45): c.arc(hx + k * r, hy - r * 1.45, r * 0.38, 0, 7)
        c.set_source_rgba(1, 1, 1, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.stroke()
    elif h == "helmet":
        c.arc(hx, hy - r * 0.1, r * 1.08, math.pi, 2 * math.pi); c.close_path(); c.set_source_rgba(*col, al); c.fill_preserve(); c.set_source_rgba(*INK, al); c.stroke()

# ------------------------------------------------------------------ props
def box(c, x, y, w, h, col, lw=3.5):
    c.rectangle(x, y, w, h); c.set_source_rgb(*rgb(col)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()

def draw_prop(c, kind, x, y, s=1.0, f=1, u=0.0, **k):
    c.save(); c.translate(x, y); c.scale(s * f, s)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    if kind == "can":
        box(c, -14, -36, 28, 36, k.get("col", "#c0392b")); c.rectangle(-14, -26, 28, 12); c.set_source_rgb(1, 1, 1); c.fill()
    elif kind == "bottle":
        box(c, -10, -44, 20, 44, "#8fd3ff"); box(c, -5, -54, 10, 10, "#2d6cdf")
    elif kind == "radio":
        box(c, -60, -70, 120, 70, "#3b3b3b"); c.arc(-28, -35, 20, 0, 7); c.set_source_rgb(0.75, 0.75, 0.75); c.fill()
        box(c, 6, -55, 42, 18, "#c8e6a0", 2.5); c.move_to(40, -70); c.line_to(70, -130); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    elif kind == "cart":
        c.set_source_rgb(*INK); c.set_line_width(5)
        c.move_to(-90, -110); c.line_to(-70, -40); c.line_to(80, -40); c.line_to(100, -110); c.close_path(); c.stroke()
        for i in range(1, 6): c.move_to(-90 + i * 32, -110); c.line_to(-70 + i * 26, -40); c.stroke()
        c.move_to(-95, -112); c.line_to(-130, -130); c.stroke()
        for wx in (-60, 70): c.arc(wx, -12, 12, 0, 7); c.stroke()
        c.move_to(-70, -40); c.line_to(-60, -24); c.move_to(80, -40); c.line_to(70, -24); c.stroke()
    elif kind == "sack":
        c.move_to(-50, 0); c.curve_to(-60, -60, -40, -90, 0, -90); c.curve_to(40, -90, 60, -60, 50, 0); c.close_path()
        c.set_source_rgb(*rgb(k.get("col", "#c9a46a"))); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()
        c.select_font_face(BOLD); c.set_font_size(18); c.move_to(-30, -40); c.show_text("DOG")
    elif kind == "ladder":
        c.set_source_rgb(*rgb("#8a8f98")); c.set_line_width(8)
        hgt = k.get("h", 520)
        c.move_to(-40, 0); c.line_to(-40, -hgt); c.move_to(40, 0); c.line_to(40, -hgt); c.stroke()
        for yy in range(-40, -hgt, -55): c.move_to(-40, yy); c.line_to(40, yy); c.stroke()
    elif kind == "grill":
        box(c, -55, -70, 110, 30, "#2b2b2b"); c.set_source_rgb(*INK); c.set_line_width(5)
        c.move_to(-40, -40); c.line_to(-55, 0); c.move_to(40, -40); c.line_to(55, 0); c.stroke()
        for i in range(3):
            c.move_to(-25 + i * 25, -80); c.curve_to(-35 + i * 25, -110, -15 + i * 25, -120, -25 + i * 25, -150)
            c.set_source_rgba(0.7, 0.7, 0.7, 0.6); c.set_line_width(5); c.stroke()
    elif kind == "pool":
        c.save(); c.scale(1, 0.35); c.arc(0, 0, 130, 0, 7); c.restore(); c.set_source_rgb(*rgb("#4fb3ff")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        c.save(); c.scale(1, 0.35); c.arc(0, 0, 100, 0, 7); c.restore(); c.set_source_rgb(*rgb("#a9dcff")); c.fill()
    elif kind == "backpack":
        box(c, -32, -70, 64, 70, k.get("col", "#34495e")); box(c, -24, -40, 48, 26, "#2c3e50", 2.5)
    elif kind == "keyfob":
        box(c, -12, -28, 24, 28, "#222222", 2.5); c.arc(0, -16, 5, 0, 7); c.set_source_rgb(0.9, 0.2, 0.2); c.fill()
    elif kind == "marker":
        box(c, -5, -40, 10, 40, "#111111", 2); box(c, -5, -46, 10, 8, "#c0392b", 2)
    elif kind == "flashlight":
        box(c, -8, -46, 16, 46, "#444444", 2)
    elif kind == "steak":
        c.save(); c.scale(1.3, 0.8); c.arc(0, -20, 22, 0, 7); c.restore(); c.set_source_rgb(*rgb("#8e3b2a")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    elif kind == "map":
        box(c, -80, -60, 160, 110, "#f3e3b5"); c.set_source_rgb(*rgb("#4aa3df")); c.set_line_width(8); c.move_to(-80, -20); c.curve_to(-20, -40, 20, 10, 80, -10); c.stroke()
    elif kind == "minivan":
        c.move_to(-200, -30); c.line_to(-200, -130); c.line_to(-110, -190); c.line_to(200, -190); c.line_to(210, -30); c.close_path()
        c.set_source_rgb(*rgb(k.get("col", "#7f8fa6"))); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        box(c, -100, -175, 120, 60, "#2c3e50"); box(c, 40, -175, 140, 60, "#2c3e50")
        for wx in (-120, 130): c.arc(wx, -30, 36, 0, 7); c.set_source_rgb(0.15, 0.15, 0.15); c.fill()
        if k.get("alarm"):
            on = int(u * 4) % 2 == 0
            for hx in (-195, 205):
                c.arc(hx, -110, 26 if on else 14, 0, 7); c.set_source_rgba(1, 0.75, 0.1, 0.9 if on else 0.4); c.fill()
    elif kind == "boat":
        c.move_to(-260, -60); c.line_to(260, -60); c.line_to(200, 10); c.line_to(-220, 10); c.close_path()
        c.set_source_rgb(*rgb("#ecf0f1")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        box(c, -120, -150, 200, 90, "#d35400"); box(c, -100, -130, 50, 40, "#85c1e9", 2.5); box(c, -30, -130, 50, 40, "#85c1e9", 2.5)
    elif kind == "door":
        op = cl(k.get("open", 0.0)); dw, dh = 230, 470
        c.rectangle(-dw / 2 - 14, -dh - 14, dw + 28, dh + 14); c.set_source_rgb(*rgb("#5d4037")); c.fill()
        c.rectangle(-dw / 2, -dh, dw, dh); c.set_source_rgb(*rgb(k.get("inside", "#141414"))); c.fill()
        pw = dw * (1 - op * 0.85)
        c.rectangle(-dw / 2, -dh, pw, dh); c.set_source_rgb(*rgb(k.get("col", "#9e9e9e"))); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        if op < 0.5: c.arc(-dw / 2 + pw - 30, -dh / 2, 10, 0, 7); c.set_source_rgb(0.85, 0.75, 0.3); c.fill()
        if k.get("sign"):
            c.select_font_face(BOLD); c.set_font_size(34); c.set_source_rgb(1, 1, 1); c.rectangle(-80, -dh - 80, 160, 52); c.fill(); c.set_source_rgb(*INK); c.move_to(-66, -dh - 42); c.show_text(k["sign"])
    elif kind == "bread":
        c.save(); c.scale(1.6, 0.8); c.arc(0, -18, 20, 0, 7); c.restore(); c.set_source_rgb(*rgb("#d4a35a")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    elif kind == "bigtext":
        c.select_font_face(BOLD); c.set_font_size(k.get("size", 90)); ext = c.text_extents(k["text"]); c.move_to(-ext.width / 2, 0); c.text_path(k["text"])
        c.set_source_rgb(0, 0, 0); c.set_line_width(14); c.stroke_preserve(); c.set_source_rgb(*rgb(k.get("col", "#ffffff"))); c.fill()
    elif kind == "crowd":
        rnd = random.Random(k.get("seed", 3)); n = k.get("n", 12); wdt = k.get("w", 500)
        for i in range(n):
            xx = rnd.uniform(-wdt / 2, wdt / 2); sc = rnd.uniform(0.45, 0.7)
            who = k.get("who", ["zombie", "zombie2", "zombie3"]); a = Actor(rnd.choice(who), x=xx, act=k.get("act", "zwalk"), f=k.get("face", 1), s=sc, face=k.get("expr", "neutral"))
            draw_actor(c, a, u + rnd.random() * 3, ground=rnd.uniform(-10, 10))
    c.restore()

# ------------------------------------------------------------------ backgrounds
def grad(c, y0, y1, c0, c1):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *rgb(c0)); g.add_color_stop_rgb(1, *rgb(c1)); c.rectangle(0, y0, W, y1 - y0); c.set_source(g); c.fill()

PROD = ["#e74c3c", "#f1c40f", "#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#ecf0f1", "#1abc9c", "#d35400"]
def shelf_unit(c, x, y, w, h, rows=5, seed=1, empty=0.0):
    rnd = random.Random(seed)
    box(c, x, y, w, h, "#d5d8dc", 4)
    for r in range(rows):
        yy = y + 18 + r * (h - 30) / rows; sh_y = yy + (h - 30) / rows - 10
        c.rectangle(x + 6, sh_y, w - 12, 10); c.set_source_rgb(*rgb("#909497")); c.fill()
        xx = x + 12
        while xx < x + w - 40:
            bw = rnd.uniform(28, 48); bh = rnd.uniform(40, (h - 30) / rows - 22)
            if rnd.random() > empty: box(c, xx, sh_y - bh, bw, bh, rnd.choice(PROD), 2.5)
            xx += bw + 4

def bg_aisle(c, u, dark=0.0, empty=0.0, **k):
    grad(c, 0, 640, "#fbfaf6", "#e9e6dc"); c.rectangle(0, 640, W, H - 640); c.set_source_rgb(*rgb("#cfd2d6")); c.fill()
    for i in range(12): c.move_to(i * 180 - 200, H); c.line_to(960 + (i * 180 - 1100) * 0.25, 640); c.set_source_rgba(0, 0, 0, 0.07); c.set_line_width(3); c.stroke()
    for i in range(5): c.rectangle(260 + i * 300, 30, 200, 18); c.set_source_rgb(1, 1, 0.92); c.fill()
    shelf_unit(c, -40, 160, 640, 760, seed=2, empty=empty); shelf_unit(c, 1320, 160, 640, 760, seed=5, empty=empty)
    shelf_unit(c, 700, 300, 520, 360, rows=3, seed=9, empty=empty)
    c.set_source_rgb(*rgb("#2e8b57")); c.rectangle(760, 240, 400, 46); c.fill(); c.set_source_rgb(1, 1, 1); c.select_font_face(BOLD); c.set_font_size(30)
    c.move_to(800, 274); c.show_text(k.get("sign", "AISLE 7 - CEREAL"))

def bg_front(c, u, shutters=0.0, night=True, **k):
    c.rectangle(0, 0, W, H); c.set_source_rgb(*rgb("#ece7da")); c.fill()
    c.rectangle(0, 760, W, H - 760); c.set_source_rgb(*rgb("#cfd2d6")); c.fill()
    gx, gy, gw, gh = 330, 120, 1260, 640
    grad(c, gy, gy + gh, "#0b1a33" if night else "#9fd3ff", "#1d3557" if night else "#d6eaf8")
    c.rectangle(gx, gy + gh - 120, gw, 120); c.set_source_rgb(*rgb("#2b2d33")); c.fill()
    for lx in (520, 1050, 1420):
        c.move_to(lx, gy + gh - 120); c.line_to(lx, gy + 260); c.set_source_rgb(0.3, 0.3, 0.3); c.set_line_width(6); c.stroke()
        c.arc(lx, gy + 260, 16, 0, 7); c.set_source_rgba(1, 0.9, 0.6, 0.9); c.fill()
    if k.get("crowd"): draw_prop(c, "crowd", 960, gy + gh - 40, 1, 1, u, n=k.get("crowd"), w=1100, seed=k.get("seed", 4))
    c.set_source_rgb(*INK); c.set_line_width(10)
    c.rectangle(gx, gy, gw, gh); c.stroke()
    for i in range(1, 4): c.move_to(gx + i * gw / 4, gy); c.line_to(gx + i * gw / 4, gy + gh); c.stroke()
    if shutters > 0:
        sh = gh * cl(shutters); c.rectangle(gx, gy, gw, sh); c.set_source_rgb(*rgb("#9aa0a6")); c.fill()
        for yy in range(int(gy), int(gy + sh), 26): c.move_to(gx, yy); c.line_to(gx + gw, yy); c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(3); c.stroke()
    c.select_font_face(BOLD); c.set_font_size(54); c.set_source_rgb(*rgb("#2e8b57")); c.move_to(700, 95); c.show_text("FRESHWAY MARKET")
    if k.get("barricade"):
        for i in range(7): draw_prop(c, "cart", 430 + i * 170, 905, 1.0)
        for i in range(8): draw_prop(c, "sack", 400 + i * 160, 905, 1.0, col="#c9a46a" if i % 2 else "#b5835a")

def bg_backroom(c, u, wall_text=None, write_u=1.0, radio=True, **k):
    c.rectangle(0, 0, W, H); c.set_source_rgb(*rgb("#d9cfb8")); c.fill()
    c.rectangle(0, 800, W, H - 800); c.set_source_rgb(*rgb("#8d7b68")); c.fill()
    for i in range(4): box(c, 1450 + i * 110, 300, 100, 500, "#7f8c8d", 3.5)
    box(c, 200, 640, 520, 30, "#8e5b3a"); c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(230, 670); c.line_to(230, 800); c.move_to(690, 670); c.line_to(690, 800); c.stroke()
    if radio: draw_prop(c, "radio", 460, 640, 1.2)
    if wall_text:
        c.select_font_face(HAND, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(k.get("size", 64)); c.set_source_rgb(*rgb("#1b1b1b"))
        y = 200
        for ln in wall_text.split("\n"):
            n = int(len(ln) * cl(write_u * 1.0)); c.move_to(k.get("wx", 820), y); c.show_text(ln[:n]); y += k.get("size", 64) * 1.25
    if k.get("tally"):
        c.set_source_rgb(0.1, 0.1, 0.1); c.set_line_width(5)
        for i in range(k["tally"]):
            gx = 820 + (i // 5) * 90 + (i % 5) * 14
            if i % 5 == 4: c.move_to(gx - 60, 640); c.line_to(gx + 4, 560)
            else: c.move_to(gx, 650); c.line_to(gx, 560)
            c.stroke()

def bg_storeroom(c, u, cans=1.0, **k):
    c.rectangle(0, 0, W, H); c.set_source_rgb(*rgb("#c9c3b5")); c.fill(); c.rectangle(0, 820, W, H - 820); c.set_source_rgb(*rgb("#a39c8c")); c.fill()
    rnd = random.Random(11)
    for p in range(4):
        x0 = 120 + p * 450; n = int(36 * cl(cans))
        for i in range(n):
            col = rnd.choice(["#c0392b", "#27ae60", "#f39c12", "#2980b9"])
            draw_prop(c, "can", x0 + (i % 9) * 32, 820 - (i // 9) * 38, 1.0, col=col)
        if k.get("water"):
            for i in range(int(18 * cl(k["water"]))): draw_prop(c, "bottle", x0 + 20 + (i % 9) * 30, 640 - (i // 9) * 56, 1.0)

def bg_roof(c, u, sky="night", **k):
    if sky == "night": grad(c, 0, 700, "#050a18", "#1b2a4a")
    elif sky == "dawn": grad(c, 0, 700, "#2c3e70", "#f5b56b")
    elif sky == "rain": grad(c, 0, 700, "#4a5560", "#7d8790")
    else: grad(c, 0, 700, "#7fb3e0", "#d6eaf8")
    if sky == "night":
        rnd = random.Random(7)
        for i in range(90): c.arc(rnd.uniform(0, W), rnd.uniform(0, 500), rnd.uniform(1, 2.6), 0, 7); c.set_source_rgba(1, 1, 1, 0.5 + 0.5 * math.sin(u * 2 + i)); c.fill()
    rnd = random.Random(3)
    x = 0
    while x < W:
        bw = rnd.uniform(80, 220); bh = rnd.uniform(60, 220); c.rectangle(x, 700 - bh, bw, bh); c.set_source_rgb(*rgb("#121826" if sky != "day" else "#5d6d7e")); c.fill(); x += bw + rnd.uniform(5, 30)
    c.rectangle(0, 700, W, H - 700); c.set_source_rgb(*rgb("#7b7d7d")); c.fill()
    rnd = random.Random(9)
    for i in range(300): c.arc(rnd.uniform(0, W), rnd.uniform(705, H), 2, 0, 7); c.set_source_rgba(0, 0, 0, 0.25); c.fill()
    box(c, 1450, 560, 300, 160, "#aab7b8"); c.arc(1600, 640, 55, 0, 7); c.set_source_rgb(0.3, 0.3, 0.3); c.fill()
    c.rectangle(0, 690, W, 14); c.set_source_rgb(*rgb("#5d6060")); c.fill()
    if sky == "rain":
        for i in range(160):
            xx = (i * 97 + u * 900) % W; yy = (i * 53 + u * 1400) % H
            c.move_to(xx, yy); c.line_to(xx - 8, yy + 26); c.set_source_rgba(0.85, 0.9, 1, 0.5); c.set_line_width(2); c.stroke()

def bg_lot(c, u, night=True, **k):
    grad(c, 0, 450, "#0b1a33" if night else "#8fc1e8", "#22385e" if night else "#d6eaf8")
    rnd = random.Random(5); x = 0
    while x < W:
        bw = rnd.uniform(160, 320); bh = rnd.uniform(90, 200); c.rectangle(x, 450 - bh, bw, bh); c.set_source_rgb(*rgb("#141b2b")); c.fill()
        c.move_to(x - 10, 450 - bh); c.line_to(x + bw / 2, 450 - bh - 70); c.line_to(x + bw + 10, 450 - bh); c.close_path(); c.fill(); x += bw + 40
    c.rectangle(0, 450, W, H - 450); c.set_source_rgb(*rgb("#30343c")); c.fill()
    for i in range(9): c.move_to(i * 240, 560); c.line_to(i * 240 - 80, H); c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(6); c.stroke()

def bg_bridge(c, u, **k):
    grad(c, 0, 620, "#3b4c7a", "#f7b267"); c.arc(1500, 560, 90, 0, 7); c.set_source_rgba(1, 0.85, 0.5, 0.9); c.fill()
    c.rectangle(0, 620, W, H - 620); c.set_source_rgb(*rgb("#2f5f8a")); c.fill()
    for i in range(14): c.move_to(i * 150, 700 + (i % 3) * 60); c.line_to(i * 150 + 90, 700 + (i % 3) * 60); c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(4); c.stroke()
    c.rectangle(0, 380, W, 40); c.set_source_rgb(*rgb("#4a4a4a")); c.fill()
    for i in range(8): box(c, 60 + i * 260, 420, 40, 200, "#555555", 3)
    box(c, 0, 860, 900, 60, "#8e5b3a");
    for i in range(6): box(c, 40 + i * 150, 920, 24, 160, "#6e4529", 3)

def bg_street(c, u, **k):
    grad(c, 0, 600, "#0d1424", "#26324d")
    for i in range(6):
        x = 80 + i * 320; box(c, x, 380, 260, 220, ["#5d6d7e", "#6c5b4e", "#4e5d6c"][i % 3], 4)
        c.move_to(x - 20, 380); c.line_to(x + 130, 280); c.line_to(x + 280, 380); c.close_path(); c.set_source_rgb(*rgb("#2c2c2c")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        box(c, x + 40, 440, 60, 60, "#1b1b1b", 3); box(c, x + 160, 440, 60, 60, "#1b1b1b", 3)
    c.rectangle(0, 600, W, H - 600); c.set_source_rgb(*rgb("#3a3d44")); c.fill()
    for i in range(10): c.rectangle(i * 210, 760, 120, 12); c.set_source_rgba(1, 0.85, 0.2, 0.7); c.fill()

def bg_map(c, u, route=1.0, **k):
    c.rectangle(0, 0, W, H); c.set_source_rgb(*rgb("#2b2118")); c.fill()
    box(c, 260, 110, 1400, 860, "#f1e2b8", 5)
    c.set_source_rgb(*rgb("#5dade2")); c.set_line_width(40); c.move_to(260, 300); c.curve_to(700, 200, 1100, 330, 1660, 240); c.stroke()
    c.set_source_rgba(0.4, 0.4, 0.4, 0.5); c.set_line_width(6)
    for i in range(8): c.move_to(260, 200 + i * 100); c.line_to(1660, 260 + i * 90); c.stroke()
    for i in range(10): c.move_to(360 + i * 140, 110); c.line_to(320 + i * 140, 970); c.stroke()
    box(c, 1240, 800, 60, 60, "#2e8b57", 3)
    c.select_font_face(HAND, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(44); c.set_source_rgb(*INK); c.move_to(1180, 900); c.show_text("STORE")
    c.move_to(760, 200); c.show_text("BRIDGE")
    if route > 0:
        pts = [(1270, 800), (1180, 650), (1000, 560), (880, 420), (820, 300)]
        n = cl(route) * (len(pts) - 1); c.set_source_rgb(*rgb("#c0392b")); c.set_line_width(12); c.set_dash([30, 18])
        c.move_to(*pts[0])
        for i in range(1, len(pts)):
            if n >= i: c.line_to(*pts[i])
            elif n > i - 1:
                kk = n - (i - 1); c.line_to(lerp(pts[i - 1][0], pts[i][0], kk), lerp(pts[i - 1][1], pts[i][1], kk))
        c.stroke(); c.set_dash([])
        c.select_font_face(BOLD); c.set_font_size(52); c.move_to(1300, 540); c.show_text("12 MILES")

def bg_black(c, u, **k):
    c.rectangle(0, 0, W, H); c.set_source_rgb(0.04, 0.04, 0.05); c.fill()

BGS = dict(aisle=bg_aisle, front=bg_front, backroom=bg_backroom, storeroom=bg_storeroom, roof=bg_roof, lot=bg_lot, bridge=bg_bridge, street=bg_street, map=bg_map, black=bg_black)

# ------------------------------------------------------------------ overlays
def day_stamp(c, text, u, big=False):
    k = ease(u / 0.35)
    if big:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.04, 0.04, 0.05, 1); c.fill()
        c.save(); c.translate(W / 2, H / 2); sc = 1.25 - 0.25 * k; c.scale(sc, sc); c.rotate(math.radians(-3))
        c.select_font_face(HAND, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(230)
        ext = c.text_extents(text); c.move_to(-ext.width / 2 - ext.x_bearing, ext.height / 2)
        c.set_source_rgba(0.85, 0.15, 0.12, k); c.show_text(text); c.restore(); return
    c.save(); c.translate(70, 60 - 30 * (1 - k)); c.rotate(math.radians(-3))
    c.select_font_face(HAND, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(86)
    ext = c.text_extents(text)
    c.rectangle(-18, -10, ext.width + 44, 112); c.set_source_rgba(0.05, 0.05, 0.06, 0.85 * k); c.fill()
    c.move_to(4, 80); c.set_source_rgba(0.95, 0.2, 0.15, k); c.show_text(text); c.restore()

def vignette(c, amt):
    g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1150); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, amt)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()

def flashlight(c, x, y, r=300):
    g = cairo.RadialGradient(x, y, r * 0.2, x, y, r); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.93)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()

# ------------------------------------------------------------------ render
def render(sc, u, dur):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    cam = sc.get("cam")
    c.save()
    if cam:
        (z0, x0, y0), (z1, x1, y1) = cam; k = ease(u / max(dur, 1e-3))
        z, cx, cy = lerp(z0, z1, k), lerp(x0, x1, k), lerp(y0, y1, k)
        c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    if sc.get("shake"):
        a0, a1, amp = sc["shake"]
        if a0 <= u <= a1: c.translate(math.sin(u * 61) * amp, math.cos(u * 47) * amp)
    bga = dict(sc.get("bgargs", {}))
    for key, v in list(bga.items()):
        if callable(v): bga[key] = v(u)
    BGS[sc.get("bg", "black")](c, u, **bga)
    items = [(p.get("z", 0), "p", p) for p in sc.get("props", [])] + [(a.z, "a", a) for a in sc.get("actors", [])]
    for _, kind, it in sorted(items, key=lambda t: t[0]):
        if kind == "a": draw_actor(c, it, u, ground=sc.get("ground", GROUND))
        else:
            p = dict(it); xx = p.pop("x"); yy = p.pop("y"); ss = p.pop("s", 1.0); ff = p.pop("f", 1); p.pop("z", None); kd = p.pop("kind")
            if "path" in p:
                pts = p.pop("path"); xx = pts[0][1]
                for (u0, x0_), (u1, x1_) in zip(pts, pts[1:]):
                    if u >= u0: xx = lerp(x0_, x1_, cl((u - u0) / max(1e-6, u1 - u0)))
            draw_prop(c, kd, xx, yy, ss, ff, u, **p)
    if sc.get("fx"): sc["fx"](c, u, dur)
    c.restore()
    if sc.get("dark"): c.rectangle(0, 0, W, H); c.set_source_rgba(0.02, 0.03, 0.08, sc["dark"]); c.fill()
    if sc.get("torch"):
        tx, ty = sc["torch"](u) if callable(sc["torch"]) else sc["torch"]; flashlight(c, tx, ty)
    vignette(c, sc.get("vig", 0.35))
    if sc.get("day"): day_stamp(c, sc["day"], u, big=sc.get("daybig", False))
    if sc.get("title"):
        c.select_font_face(BOLD); c.set_font_size(sc.get("tsize", 72)); ext = c.text_extents(sc["title"]); k = ease(u / 0.3)
        c.move_to(W / 2 - ext.width / 2, sc.get("ty", 160)); c.text_path(sc["title"]); c.set_source_rgba(0, 0, 0, k); c.set_line_width(14); c.stroke_preserve(); c.set_source_rgba(1, 1, 1, k); c.fill()
    buf = surf.get_data(); a = np.ndarray((H, W, 4), np.uint8, buf).copy()
    return Image.fromarray(a[:, :, [2, 1, 0, 3]], "RGBA")
