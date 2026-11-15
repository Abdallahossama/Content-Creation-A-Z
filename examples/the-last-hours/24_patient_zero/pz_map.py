"""#24 map shots: a light basemap with a slow push-in, routes that draw on, and pinned place labels."""
from pz_scenes import *

def sc_map(c, t, s, t0, t1):
    view = s["view"]; base = basemap(view, s.get("hi"))
    c.paste(K.kenburns(base, t, t0, t1 + 0.6, 1.0, 1.06)); d = ImageDraw.Draw(c)
    z = 1.0 + 0.06 * ease((t - t0) / max(t1 + 0.6 - t0, 0.01))          # keep overlays on the zoomed map
    def zp(ll):
        x, y = proj(view, *ll); return W / 2 + (x - W / 2) * z, H / 2 + (y - H / 2) * z
    for r in s.get("routes", []):
        pts, at = r[0], r[1]; dur = r[2] if len(r) > 2 else 2.0; col = r[3] if len(r) > 3 else RED
        k = ease((t - AT(at)) / dur)
        if k <= 0: continue
        xy = [zp(p) for p in pts]
        if r[4:5] == ["arc"]: xy = arc_pts(xy[0], xy[-1])
        L = [math.dist(xy[i], xy[i + 1]) for i in range(len(xy) - 1)]; tot = sum(L) * k; out = [xy[0]]
        for i, l in enumerate(L):
            if tot >= l: out.append(xy[i + 1]); tot -= l
            else: f = tot / l; out.append((xy[i][0] + (xy[i + 1][0] - xy[i][0]) * f, xy[i][1] + (xy[i + 1][1] - xy[i][1]) * f)); break
        d.line(out, fill=col, width=8, joint="curve"); x, y = out[-1]; d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=col)
    for p in s.get("pins", []):
        ll, name, at = p[:3]; st = p[3] if len(p) > 3 else "yel"; te = AT(at)
        if t < te: continue
        x, y = zp(ll); r = 11 * eout((t - te) / 0.3); d.ellipse((x - r, y - r, x + r, y + r), fill=INK, outline=(255, 255, 255), width=3)
        K.pop(c, lab(name, p[4] if len(p) > 4 else 40, st), x, y - 50, t, te + 0.1, t1=t1 - 0.25)
    if s.get("top"): K.pop(c, lab(s["top"], 54, "ink"), W / 2, 90, t, t0 + 0.2)
    put_labels(c, t, s.get("labels", []), t1)
