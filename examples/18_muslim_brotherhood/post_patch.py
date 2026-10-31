# exec'd by _build_render.py (owner, 31 Oct): small / upright photos are print cards (never zoomed to fill the frame), a card can sit
# off-centre (x), and quotes / lists can move to the left half (quoteL, listL) so no text ever covers a face
rep('def KBP(rid, crop=None, h=880, rot=-1.5, tag=None): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid)))',
    'def KBP(rid, crop=None, h=880, rot=-1.5, tag=None, x=0.5): return ("kbp", dict(rid=rid, crop=crop or CROP.get(rid), h=h, rot=rot, tag=tag or DT(rid), x=x))')
rep('        L.drop(c, card, W / 2, H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag"))\n',
    '        L.drop(c, card, W * a.get("x", 0.5), H / 2 - 20, t, t0, dur=0.3, dy=30); tag(c, a.get("tag"))\n')
rep('"list": "center", "quote": "center"}', '"list": "center", "quote": "center", "listL": "center", "quoteL": "center"}')
rep('k2 in ("list", "typecenter", "typecenter_red", "quote")', 'k2 in ("list", "typecenter", "typecenter_red", "quote", "listL", "quoteL")')
rep('''        elif kind == "list":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay); sz = 74 if max(len(s) for s in a) < 24 else 58
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W / 2,''',
    '''        elif kind in ("list", "listL"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 150)); c.alpha_composite(lay); sz = 74 if max(len(s) for s in a) < 24 else 58
            if kind == "listL": sz = min(sz, 52)
            for i, s in enumerate(a):
                L.typewriter(c, s, t, t0 + i * 0.8, W * (0.29 if kind == "listL" else 0.5),''')
rep('''        elif kind == "quote":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay); qs = a[0].split("\\n")
            for i, q in enumerate(qs):
                L.text(c, q, W / 2, H / 2 - 40 - (len(qs) - 1) * 42 + i * 84, 50 if NO_BOTTOM and len(q) > 44 else 60, BONE, SER, alpha=ease((t - t0 - 0.25 * i) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, W / 2,''',
    '''        elif kind in ("quote", "quoteL"):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 160)); c.alpha_composite(lay); qs = a[0].split("\\n"); qx = W * (0.30 if kind == "quoteL" else 0.5)
            for i, q in enumerate(qs):
                L.text(c, q, qx, H / 2 - 40 - (len(qs) - 1) * 42 + i * 84, 44 if kind == "quoteL" else (50 if NO_BOTTOM and len(q) > 44 else 60), BONE, SER, alpha=ease((t - t0 - 0.25 * i) / 0.4))
            L.typewriter(c, a[1], t, t0 + 0.6, qx,''')
