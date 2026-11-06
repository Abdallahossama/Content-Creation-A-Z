import pathlib
here = pathlib.Path(".").resolve()
css = open("v2_css.txt", encoding="utf-8").read() + """
.win{position:absolute;background:#1D1D1D;border:1.5px solid #2A2A2A;border-radius:14px;overflow:hidden;
 box-shadow:34px 44px 60px rgba(0,0,0,.55), inset 3px 0 0 rgba(255,140,60,.55)}
.win img{display:block;width:100%}
.bub{display:inline-block;margin-top:10px;padding:12px 20px;border-radius:16px;background:#FF4F2B;color:#fff;font-family:A,sans-serif;font-size:34px;direction:rtl}
.chip{display:inline-block;margin-top:10px;padding:8px 14px;border-radius:10px;background:#151515;border:1px solid #2A2A2A;color:#F2F0EC;font-size:22px}
.lt{direction:ltr;text-align:left;padding-left:8px;padding-right:0}
"""
BEHIND = 'left:610px;top:215px;width:420px;transform:rotateY(-10deg) rotateZ(1.5deg)'
FRONT = 'left:105px;top:1215px;transform:rotateY(10deg) rotateZ(-2deg)'
def page(name, body):
    (here / "p" / f"{name}.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>', encoding="utf-8")
def editor(fname, lines, k):
    rows = []
    for i, (txt, cls) in enumerate(lines[:k], 1):
        cur = '<span class="cur"></span>' if i == k else ''
        rows.append(f'<div class="ln"><i>{i}</i><span class="{cls}">{txt}{cur}</span></div>')
    for i in range(k + 1, len(lines) + 1):
        rows.append(f'<div class="ln"><i>{i}</i><span></span></div>')
    return f'<div class="ed" style="{BEHIND}"><div class="tb"><s>●</s><b>{fname}</b></div><div class="code">{"".join(rows)}</div></div>'
ok = ' <span class="ok">✓</span>'
A = [("# تحليل المشروع", "h"), ("أهداف العميل" + ok, ""), ("المستخدمين" + ok, ""), ("البروسيس الحالية" + ok, ""), ("نقط الوجع", "dim")]
for k in range(1, 6): page(f"a{k}", editor("analysis.md", A, k))
P = [("PRD", "h"), ("01 · الهدف", ""), ("02 · المستخدمين", ""), ("03 · المميزات", ""), ("04 · التسليم", "dim")]
for k in range(1, 6): page(f"prd{k}", editor("PRD_v1.md", P, k))
circ = '<svg width="225" height="100" viewBox="0 0 250 110" style="position:absolute;left:-12px;top:-14px;overflow:visible"><path pathLength="100" stroke-dasharray="{d} 100" d="M34 58 C 30 22, 130 6, 200 16 C 248 24, 246 84, 182 96 C 120 106, 30 100, 20 72 C 14 54, 44 38, 78 32" fill="none" stroke="#FF4F2B" stroke-width="5" stroke-linecap="round"/></svg>'
for j, d in enumerate([0, 30, 60, 85, 100]):
    svg = circ.format(d=d) if d else ''
    page(f"scope{j}", f'<div class="tag" style="{FRONT}">01 / scope<span class="big">من <span style="position:relative;display:inline-block;direction:ltr">A to Z{svg}</span></span></div>')
def win(img, host): return f'<div class="win" style="{BEHIND};width:440px"><div class="tb"><s>●</s><b>{host}</b></div><img src="{(here.parent / img).as_uri()}"></div>'
page("client", win("broll/site_rakeeza.png", "rakeeza-contracting.vercel.app"))
page("home", win("broll/site_home.png", "codebyabdullah.com"))
for j, w in enumerate(["ش", "شغ", "شغّا", "شغّال"]):
    page(f"cm{j}", f'<div class="tag" style="{FRONT}">02 / comment<span class="big" style="margin-top:14px;line-height:1.2">{w}<span class="cur" style="height:52px;vertical-align:-8px"></span></span></div>')
page("inbox", f'<div class="tag" style="{FRONT}">inbox · codebyabdullah<br><span class="bub">البروسيس كاملة</span><br><span class="chip">Analysis → PRD → Build</span></div>')
print("ok")
