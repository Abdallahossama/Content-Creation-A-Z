"""Post-patch render_vice28.py (after build_render_saddam.py vice28): the NOAH host rebrand (owner 27 Nov 2026).
host cutaway shots, corner pops (POPS), Noah end screen, their sounds.  python patch_vice28.py"""
P = "D:/why habibi/_newchannel/28_vice_city_real/render_vice28.py"
s = open(P, encoding="utf-8").read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:60], s.count(a)); s = s.replace(a, b)
rep('import mshorts as MS ', 'sys.path.insert(0, "D:/why habibi/_newchannel/_tools"); import hostkit as HK      # Noah, the File Keeper (host avatar)\n'
    'BP.LABEL["vice28"] = "FILE 28  ·  VICE CITY WAS REAL  ·  MIAMI 1979-1986"; BP.NEXT["vice28"] = "A NEW FILE EVERY WEEK"\nimport mshorts as MS ')
rep('    elif kind == "midask":                                     # frozen-feel',
    '    elif kind == "host": c = HK.cutaway(t, t0, t1, a["expr"], name=a.get("name"))\n    elif kind == "midask":                                     # frozen-feel')
i = s.index('    elif kind == "end":                                        # the File Keeper end card'); j = s.index("    else:\n        c = Image.new(\"RGBA\", (W, H), INK + (255,))", i)
s = s[:i] + ('    elif kind == "end":                                        # Noah end screen (subscribe on the sign-off line)\n'
             '        wsb = wt(ENDL + 1, "subscrib"); ww = wt(ENDL + 1, "thanks"); c = HK.end_screen(t - t0, sub_at=(wsb - t0) if wsb else None, wave_at=(ww - t0) if ww else None)\n') + s[j:]
rep('    draw_ov(c, t, t0, t1)\n    if kind not in ("tcard", "end"): draw_badge(c, t)',
    '    draw_ov(c, t, t0, t1)\n    if kind not in ("tcard", "end", "host"): draw_badge(c, t)\n'
    '    if kind not in ("host", "end"):\n        for pk, pd, pe in POPS:\n            tp = AT(pk) - 0.1; HK.corner(c, t, tp, tp + pd, pe)')
rep('            wl, wsb = wt(ENDL, "like"), wt(ENDL, "subscrib")\n            for tt, nm, db, ml in BA.end_sfx(',
    '            wl, wsb = wt(ENDL + 1, "like"), wt(ENDL + 1, "subscrib")\n            for tt, nm, db, ml in BA.end_sfx(')
i = s.index("BA.end_sfx("); j = s.index('    for j, (ln, off, kind, a) in enumerate(OV):', i)
s = s[:j] + ('    for i, (key, (kind, a)) in enumerate(SHOTS):\n        if kind == "host": sfx("whoosh_fast_transition", SHOT_T[i] - 0.05, -21)\n'
             '    for pk, pd, pe in POPS: sfx("whoosh_ghostly", AT(pk) - 0.15, -24, maxlen=0.8)\n') + s[j:]
open(P, "w", encoding="utf-8").write(s); print("patched", P)
