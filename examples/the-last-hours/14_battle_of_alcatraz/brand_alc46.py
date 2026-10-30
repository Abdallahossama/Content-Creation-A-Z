"""File 14 (Battle of Alcatraz): build the File Keeper version INSIDE the render (owner, 30 Oct 2026; repo docs/09):
- VO: insert the like-vote TEST line after line 53 (_cta/so_like46.wav), drop the old end lines 66-68, end on the File Keeper sign-off
  (_cta/so_alcatraz46.wav); exact-zero gaps kept so the render re-times itself. Backups: *_prebrand.*
- vo_lines.txt / vo/vo_tts.txt: the same edit.
- render_alcatraz46.py: every line reference >= 54 shifted (+1; old 66-68 -> the sign-off, 67), the subscribe pill moved off the like
  line, the brand stamp / pill / end card drawn with _cta/brand_patch.py (stamp_image, pill_image, end_frame), TAIL 5 s.
  uv run --no-project --with numpy --with soundfile python brand_alc46.py"""
import re, shutil, os, json
import numpy as np, soundfile as sf
R = "D:/why habibi/_newchannel/14_battle_of_alcatraz/"; CTA = "D:/why habibi/_newchannel/_cta/"
VOF = R + "vo/alcatraz46_vo_chatterbox.wav"
for f in (VOF, R + "vo_lines.txt", R + "vo/vo_tts.txt", R + "render_alcatraz46.py"):
    b, e = os.path.splitext(f); bk = b + "_prebrand" + e
    if not os.path.exists(bk): shutil.copy(f, bk)
    shutil.copy(bk, f)                                                   # always rebuild from the pre-brand originals (re-runnable)

# ---- VO
vo, sr = sf.read(VOF, dtype="float32"); vo = vo.mean(1) if vo.ndim > 1 else vo
z = np.concatenate([[False], vo == 0.0, [False]]).astype(np.int8); d = np.diff(z)
gaps = [(a, b) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]) if b - a >= int(0.3 * sr)]
def seg(path):
    a, s = sf.read(path, dtype="float32"); a = a.mean(1) if a.ndim > 1 else a
    if s != sr: a = np.interp(np.arange(int(len(a) * sr / s)) / sr, np.arange(len(a)) / s, a).astype(np.float32)
    a = a / (np.sqrt(np.mean(a[np.abs(a) > 0.01] ** 2)) + 1e-9) * np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)); a[a == 0.0] = 1e-6; return a
like, sign = seg(CTA + "so_like46.wav"), seg(CTA + "so_alcatraz46.wav")
g53, g65 = gaps[53], gaps[65]                                            # the silences after line 53 and after line 65
new = np.concatenate([vo[:g53[1]], like, np.zeros(int(0.7 * sr), np.float32), vo[g53[1]:g65[0]], np.zeros(int(1.0 * sr), np.float32), sign])
sf.write(VOF, new, sr, subtype="FLOAT"); print("VO", round(len(vo) / sr, 2), "->", round(len(new) / sr, 2), "s")

# ---- the script text
LIKE = "Would you have hidden that key too? If you would, hit like."
src = open(CTA + "signoff_gen.py", encoding="utf-8").read(); ns = {}; exec(src[src.index("HEAD = "):src.index("if __name__")], ns)
SIGN = ns["LINES"]["alcatraz46"]
for f in (R + "vo_lines.txt", R + "vo/vo_tts.txt"):
    raw = [l.rstrip("\n") for l in open(f, encoding="utf-8")]; out = []; n = -1
    for l in raw:
        if l.strip() and l.strip() != "##": n += 1
        if l.strip() and l.strip() != "##" and n in (66, 67, 68): continue
        out.append(l)
        if l.strip() and l.strip() != "##" and n == 53: out.append(LIKE)
    while out and not out[-1].strip(): out.pop()
    out.append(SIGN); open(f, "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---- the render script
p = R + "render_alcatraz46.py"; s = open(p, encoding="utf-8").read()
def m(n): return n if n <= 53 else (n + 1 if n <= 65 else 67)
a0, a1 = s.index("SHOTS = ["), s.index("def OT(ln, off)")                    # SHOTS + OV
s = s[:a0] + re.sub(r"\((\d+), ", lambda k: f"({m(int(k.group(1)))}, ", s[a0:a1]) + s[a1:]
a0, a1 = s.index("    music(\"Thunder Dreams.mp3\""), s.index("    for ln, off, name, db in EV:")   # music beds + EV
s = s[:a0] + re.sub(r"tl\((\d+)\)", lambda k: f"tl({m(int(k.group(1)))})", re.sub(r"\((\d+), ", lambda k: f"({m(int(k.group(1)))}, ", s[a0:a1])) + s[a1:]
a0, a1 = s.index("CH = ["), s.index('if __name__ == "__main__":')
s = s[:a0] + re.sub(r"\((\d+), ", lambda k: f"({m(int(k.group(1)))}, ", s[a0:a1]) + s[a1:]
rep = [
 ('(68, "everyone"): "every one", (68, "everyone."): "every one."', '(67, "everyone"): "every one", (67, "everyone."): "every one."'),
 (' (67, KB("F13", z=(1.03, 1.12))),\n ((67, 0.0), ("end", {})),', ' (54, KB("F5", z=(1.08, 1.2), c0=(0.5, 0.42))),                       # the like-vote TEST line\n ((67, -0.7), ("end", {})),'),
 (' (53, "yard|reached", "subpop", None),', ' (56, "pages|hundred", "subpop", None),                             # off the like line'),
 (' (55, 0.2, "under", "SHOCKLEY AND THOMPSON FIRED NO SHOT"),', ' (54, 0.2, "under", "WOULD YOU HAVE HIDDEN THAT KEY?  LIKE = YES"),\n (55, 0.2, "under", "SHOCKLEY AND THOMPSON FIRED NO SHOT"),'),
 (', (67, 1.0, "typewriter_return_bell", -18)]', ', (67, -0.55, "metal_hammer_hit", -16), (67, -0.3, "hit_cinematic_deep_impact", -14)]'),
 ('LEAD = 0.8; TAIL = 20.0', 'LEAD = 0.8; TAIL = 5.0                                   # the File Keeper end card runs under the sign-off'),
]
for a, b in rep:
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
# brand drawing: the shared File Keeper pieces from _cta/brand_patch.py
s = s.replace("import mshorts as MS ", 'sys.path.insert(0, "D:/why habibi/_newchannel/_cta"); import brand_patch as BP     # The File Keeper pieces (docs/09)\nimport mshorts as MS ', 1)
s = s.replace('''            L.text(c, "FILE 14  ·  ALCATRAZ  ·  MAY 1946", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)''',
'''            L.text(c, "FILE 14  ·  ALCATRAZ  ·  MAY 1946", W / 2, H / 2 + 105, 34, STEEL, TYPE, alpha=al)
            c.alpha_composite(BP.stamp_image(u), BP.STAMP_XY)                 # the File Keeper mark beside LAST HOURS''')
a0 = s.index('    elif kind == "subpop":'); a1 = s.index("def doc_frame(")
s = s[:a0] + '''    elif kind == "subpop":                                     # the File Keeper subscribe pill, top-left, 4 s
        u = t - t0
        if u < 4.0: c.alpha_composite(BP.pill_image(u, BP.PILL["alcatraz46"]), (0, BP.PILL_Y))

''' + s[a1:]
a0 = s.index('    elif kind == "end":'); a1 = s.index("    else:\n        c = Image.new(\"RGBA\", (W, H), INK + (255,))")
s = s[:a0] + '''    elif kind == "end":                                        # the File Keeper end card (stamp, CASE CLOSED, next, boxes) under the sign-off
        if "end" not in BG:
            sh = tone("F13"); k = max(W / sh.width, H / sh.height); sh = sh.resize((int(sh.width * k) + 1, int(sh.height * k) + 1), Image.LANCZOS)
            sh = sh.crop(((sh.width - W) // 2, (sh.height - H) // 2, (sh.width - W) // 2 + W, (sh.height - H) // 2 + H)).convert("RGB")
            BG["end"] = (sh, Image.blend(sh.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62))
        c = BP.end_frame(BG["end"][0], BG["end"][1], t - t0, BP.NEXT["alcatraz46"], caps=[])
''' + s[a1:]
open(p, "w", encoding="utf-8").write(s); print("render script branded")
