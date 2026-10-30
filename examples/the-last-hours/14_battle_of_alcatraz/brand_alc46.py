"""File 14 (Battle of Alcatraz): the File Keeper version built INSIDE the render (owner, 30 Oct 2026; repo docs/09). Re-runnable: always
rebuilds from the *_prebrand originals.
- VO: the spoken mid-video ask (_cta/so_midcta.wav) goes in right before line 42 (the cliffhanger: "The Marine who did the firing
  described something else." -> Buckner), the old end lines 66-68 go, the File Keeper sign-off (_cta/so_alcatraz46.wav) ends the VO.
  Exact-zero gaps kept so the render re-times itself. (The like-vote test line is dropped: the spoken mid ask replaced it.)
- vo_lines.txt / vo/vo_tts.txt: the same edit.
- render_alcatraz46.py: line references >= 42 shifted (+1; old 66-68 -> the sign-off, 67); a "midask" shot (blurred C17 + the
  File Keeper overlay, buttons on the spoken words); the animated stamp (runs across cuts), the case tab instead of the red pill,
  the CASE CLOSED end card with LIKE / SUBSCRIBE on the words; all their SFX; TAIL 5 s.
Then: transcribe_lines.py (new word times) and the render.   uv run --no-project --with numpy --with soundfile python brand_alc46.py"""
import re, shutil, os
import numpy as np, soundfile as sf
R = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"; CTA = "D:/why habibi/_newchannel/_cta/"
VOF = R + "vo/alcatraz46_vo_chatterbox.wav"
for f in (VOF, R + "vo_lines.txt", R + "vo/vo_tts.txt", R + "render_alcatraz46.py"):
    b, e = os.path.splitext(f); bk = b + "_prebrand" + e
    if not os.path.exists(bk): shutil.copy(f, bk)
    shutil.copy(bk, f)
INS = 42                                                                 # the mid ask goes in before this (old) line

# ---- VO
vo, sr = sf.read(VOF, dtype="float32"); vo = vo.mean(1) if vo.ndim > 1 else vo
z = np.concatenate([[False], vo == 0.0, [False]]).astype(np.int8); d = np.diff(z)
gaps = [(a, b) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]) if b - a >= int(0.3 * sr)]
def seg(path):
    a, s = sf.read(path, dtype="float32"); a = a.mean(1) if a.ndim > 1 else a
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    a = a / (np.sqrt(np.mean(a[np.abs(a) > 0.01] ** 2)) + 1e-9) * np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)); a[a == 0.0] = 1e-6; return a
mid, sign = seg(CTA + "so_midcta.wav"), seg(CTA + "so_alcatraz46.wav")
gi, g65 = gaps[INS - 1], gaps[65]
new = np.concatenate([vo[:gi[1]], mid, np.zeros(int(0.7 * sr), np.float32), vo[gi[1]:g65[0]], np.zeros(int(1.0 * sr), np.float32), sign, np.zeros(int(0.6 * sr), np.float32)])   # every line keeps its trailing gap
sf.write(VOF, new, sr, subtype="FLOAT"); print("VO", round(len(vo) / sr, 2), "->", round(len(new) / sr, 2), "s")

# ---- the script text
src = open(CTA + "signoff_gen.py", encoding="utf-8").read(); ns = {}; exec(src[src.index("HEAD = "):src.index("if __name__")], ns)
MID, SIGN = ns["LINES"]["midcta"], ns["LINES"]["alcatraz46"]
for f in (R + "vo_lines.txt", R + "vo/vo_tts.txt"):
    raw = [l.rstrip("\n") for l in open(f, encoding="utf-8")]; out = []; n = -1
    for l in raw:
        real = l.strip() and l.strip() != "##"
        if real: n += 1
        if real and n == INS: out.append(MID)
        if real and n in (66, 67, 68): continue
        out.append(l)
    while out and not out[-1].strip(): out.pop()
    out.append(SIGN); open(f, "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---- the render script
p = R + "render_alcatraz46.py"; s = open(p, encoding="utf-8").read()
def m(n): return n if n < INS else (n + 1 if n <= 65 else 67)
def shift(txt): return re.sub(r"\((\d+), ", lambda k: f"({m(int(k.group(1)))}, ", txt)
a0, a1 = s.index("SHOTS = ["), s.index("def OT(ln, off)"); s = s[:a0] + shift(s[a0:a1]) + s[a1:]
a0, a1 = s.index('    music("Thunder Dreams.mp3"'), s.index("    for ln, off, name, db in EV:")
s = s[:a0] + re.sub(r"tl\((\d+)\)", lambda k: f"tl({m(int(k.group(1)))})", shift(s[a0:a1])) + s[a1:]
a0, a1 = s.index("CH = ["), s.index('if __name__ == "__main__":'); s = s[:a0] + shift(s[a0:a1]) + s[a1:]
rep = [
 ('(68, "everyone"): "every one", (68, "everyone."): "every one."', '(67, "everyone"): "every one", (67, "everyone."): "every one."'),
 (' (67, KB("F13", z=(1.03, 1.12))),\n ((67, 0.0), ("end", {})),', ' ((67, -0.7), ("end", {})),                                     # the File Keeper end card under the sign-off'),
 (' ((41, "marine|firing"), KB("C17", z=(1.04, 1.14), dim=0.15)),', ' ((41, "marine|firing"), KB("C17", z=(1.04, 1.14), dim=0.15)),\n (42, ("midask", dict(bg="C17", ln=42))),                          # the spoken mid-video ask (cliffhanger)'),
 (', (67, 1.0, "typewriter_return_bell", -18)]', ', (67, -0.55, "metal_hammer_hit", -16), (67, -0.3, "hit_cinematic_deep_impact", -14)]'),
 ('LEAD = 0.8; TAIL = 20.0', 'LEAD = 0.8; TAIL = 5.0                                   # the File Keeper end card runs under the sign-off'),
 ('        if kind == "brand": sfx("hit_cinematic_deep_impact", OVT[j], -16)\n        if kind == "subpop": sfx("whoosh_fast_transition", OVT[j], -24)',
  '        if kind == "brand":\n            for tt, nm, db, ml in BA.STAMP_SFX: sfx(nm, OVT[j] + tt, db, maxlen=ml)\n'
  '        if kind == "subpop":\n            for tt, nm, db, ml in BA.CHIP_SFX: sfx(nm, OVT[j] + tt, db, maxlen=ml)'),
]
for a, b in rep:
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
s = s.replace("import mshorts as MS ", 'sys.path.insert(0, "D:/why habibi/_newchannel/_cta"); import brand_patch as BP; import brand_anim as BA     # The File Keeper (docs/09)\nimport mshorts as MS ', 1)
# the stamp: the animated File Keeper version, across shot cuts
a0 = s.index('    elif kind == "brand":'); a1 = s.index('    elif kind == "hookleft":')
s = s[:a0] + '''    elif kind == "brand":                                      # the animated File Keeper stamp (band sweep, mark, letters, file line)
        if t - t0 < BA.STAMP_LEN: c.alpha_composite(BA.stamp_frame(t - t0, BP.LABEL["alcatraz46"]))
''' + s[a1:]
s = s.replace('''        if kind == "subpop":                                           # the silent subscribe ask runs its full 4 s across shot cuts
            if t0 <= t < t0 + 4.0: ov_extra(c, kind, a, t, t0)
            continue''', '''        if kind == "subpop":                                           # the case tab runs its full length across shot cuts
            if t0 <= t < t0 + BA.PILL_LEN: ov_extra(c, kind, a, t, t0)
            continue
        if kind == "brand":                                            # so does the stamp
            if t0 <= t < t0 + BA.STAMP_LEN: ov_extra(c, kind, a, t, t0)
            continue''')
a0 = s.index('    elif kind == "subpop":'); a1 = s.index("def doc_frame(")
s = s[:a0] + '''    elif kind == "subpop":                                     # the File Keeper case tab (no ask: the spoken mid ask does that)
        if t - t0 < BA.PILL_LEN: c.alpha_composite(BA.chip_frame(t - t0, BP.LABEL["alcatraz46"]), (0, BP.PILL_Y))

''' + s[a1:]
# frame(): the mid ask shot + the File Keeper end card (LIKE / SUBSCRIBE on the spoken words)
a0 = s.index('    elif kind == "end":'); a1 = s.index("    else:\n        c = Image.new(\"RGBA\", (W, H), INK + (255,))")
s = s[:a0] + '''    elif kind == "midask":                                     # frozen-feel blurred photo + the File Keeper ask, buttons on the words
        ln = a["ln"]; c = blur_bg(a["bg"], CROP.get(a["bg"])).copy(); wk = lambda w: (wt(ln, w) - t0) if wt(ln, w) is not None else None
        BA.mid_overlay(c, t - t0, t1 - t0, wk("like"), wk("subscrib"), wk("comment"))
    elif kind == "end":                                        # the File Keeper end card under the sign-off
        if "end" not in BG:
            sh = tone("F13"); k = max(W / sh.width, H / sh.height); sh = sh.resize((int(sh.width * k) + 1, int(sh.height * k) + 1), Image.LANCZOS)
            sh = sh.crop(((sh.width - W) // 2, (sh.height - H) // 2, (sh.width - W) // 2 + W, (sh.height - H) // 2 + H)).convert("RGB")
            BG["end"] = (sh, Image.blend(sh.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62))
        wl, wsb = wt(67, "like"), wt(67, "subscrib")
        c = BP.end_frame(BG["end"][0], BG["end"][1], t - t0, BP.NEXT["alcatraz46"], caps=[], t_like=(wl - t0) if wl else None, t_sub=(wsb - t0) if wsb else None)
''' + s[a1:]
# audio(): the mid-ask and end-card SFX, timed from the shots
s = s.replace('''        elif kind in ("kb", "vid", "vidp"): sfx("whoosh_fast_transition", t0 - 0.1, -32)''', '''        elif kind in ("kb", "vid", "vidp"): sfx("whoosh_fast_transition", t0 - 0.1, -32)
        elif kind == "midask":
            t1 = SHOT_T[i + 1]; wk = lambda w: (wt(a["ln"], w) - t0) if wt(a["ln"], w) is not None else None
            for tt, nm, db, ml in BA.mid_sfx(t1 - t0, wk("like"), wk("subscrib"), wk("comment")): sfx(nm, t0 + tt, db, maxlen=ml)
        elif kind == "end":
            wl, wsb = wt(67, "like"), wt(67, "subscrib")
            for tt, nm, db, ml in BA.end_sfx((wl - t0) if wl else None, (wsb - t0) if wsb else None): sfx(nm, t0 + tt, db, maxlen=ml)''')
open(p, "w", encoding="utf-8").write(s); print("render script branded")
