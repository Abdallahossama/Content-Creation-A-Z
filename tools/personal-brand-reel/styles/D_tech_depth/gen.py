"""Style D 'Tech Depth': dark ink UI panels (pistachio hairline, mono labels, subtle grid) that sit
BEHIND the speaker's head, chest tags, and an ASS caption file. Writes html/, renders png/ with Edge."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from de_common import *

H = HERE / "html"; H.mkdir(exist_ok=True)
JOBS = []

CSS = f"""@font-face{{font-family:A;src:url('{FONT_A}')}}
html,body{{margin:0;background:transparent;overflow:hidden}}*{{box-sizing:border-box}}
.pn{{position:absolute;inset:0;background-color:{INK};border:2px solid {PIS};border-radius:10px;overflow:hidden;
 background-image:linear-gradient(rgba(243,238,227,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(243,238,227,.05) 1px,transparent 1px);
 background-size:24px 24px;background-position:-1px 39px}}
.hd{{height:42px;border-bottom:1px solid rgba(185,221,116,.5);display:flex;align-items:center;gap:7px;padding:0 14px;
 font-family:Consolas,monospace;font-size:17px;color:{PIS};letter-spacing:1px;background:{INK};direction:ltr}}
.hd i{{width:10px;height:10px;border:1.5px solid rgba(243,238,227,.45);display:block}}
.hd span{{margin-left:8px}}
.hd b{{margin-left:auto;font-weight:400;color:{INK};background:{PIS};padding:1px 8px}}
.hd u{{text-decoration:none;color:{COB};font-size:14px;margin-left:10px}}
.code{{padding:12px 14px;font-family:Consolas,monospace;font-size:20px;line-height:34px;color:{PAPER};white-space:pre;direction:ltr}}
.n{{color:rgba(243,238,227,.25);display:inline-block;width:30px}}
.k{{color:{PIS}}} .c{{color:rgba(243,238,227,.42)}} .m{{color:rgba(243,238,227,.62)}}
.cur{{display:inline-block;width:11px;height:22px;background:{PIS};vertical-align:-4px;margin-left:2px}}
.ok{{background:{PIS};color:{INK};padding:0 6px}}
.ar{{font-family:A,sans-serif;direction:rtl}}
"""

def page(name, w, h, body):
    (H / f"{name}.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}'
        f'body{{width:{w}px;height:{h}px;position:relative}}</style></head><body>{body}</body></html>', encoding="utf-8")
    JOBS.append((name, w, h))

def hd(fn, tag):
    return f'<div class="hd"><i></i><i></i><i></i><span>{fn}</span><u>&#9679;</u><b>{tag}</b></div>'

PW, PH = 500, 350
def typed(prefix, fn, tag, rows, w=PW):
    """one png per state; state k shows rows[:k] with a block cursor on the last row"""
    names = []
    for k in range(1, len(rows) + 1):
        body = "".join(f'<div><span class="n">{i+1}</span>{r}{"<span class=cur></span>" if i == k-1 else ""}</div>'
                       for i, r in enumerate(rows[:k]))
        page(f"{prefix}{k}", w, PH, f'<div class="pn">{hd(fn, tag)}<div class="code">{body}</div></div>')
        names.append(f"{prefix}{k}")
    return names

typed("an", "analysis.ts", "01", [
    '<span class="c">// client brief, A to Z</span>',
    '<span class="k">const</span> brief = <span class="k">await</span> client.read();',
    '<span class="k">const</span> goals = brief.goals();',
    '<span class="k">const</span> users = brief.users();',
    '<span class="k">const</span> flow  = trace(<span class="m">"A-Z"</span>);',
    '<span class="k">const</span> pains = flow.gaps();',
    '<span class="k">export</span> { goals, flow };'])

typed("prd", "PRD_v1.md", "02", [
    '<span class="k"># Business Requirement</span>',
    '<span class="k">  Description</span>',
    '<span class="m">##</span> 01  Goals',
    '<span class="m">##</span> 02  Users',
    '<span class="m">##</span> 03  Features',
    '<span class="m">##</span> 04  Delivery',
    '<span class="c">status:</span> <span class="ok">approved</span>'], w=470)

typed("tst", "requirements.test.ts", "03", [
    '<span class="c">$</span> npm test requirements',
    '<span class="ok">PASS</span> goals.match(client)',
    '<span class="ok">PASS</span> users.flow()',
    '<span class="ok">PASS</span> process("A-Z")',
    '<span class="ok">PASS</span> prd.approved',
    '<span class="m">Tests: 4 passed, 4 total</span>'])

# comment panel (Arabic text in Alexandria)
CM = lambda posted: f"""<div class="pn">{hd("post / comments", "04")}<div class="code" style="white-space:normal">
<div><span class="n">1</span><span class="c">@you</span></div>
<div style="display:flex;gap:10px;align-items:center;margin:6px 0 0 30px">
<div class="ar" style="flex:1;border:1.5px solid {'rgba(243,238,227,.3)' if not posted else PIS};padding:4px 14px 8px;font-size:26px;color:{PAPER}">
عايز البروسيس{'' if posted else '<span class="cur"></span>'}</div>
<div style="background:{PIS};color:{INK};padding:2px 12px;font-size:18px">{'sent' if posted else 'send'}</div></div>
<div style="margin-top:14px"><span class="n">2</span><span class="c">{'// queued: inbox' if posted else ''}</span></div></div></div>"""
page("cm1", 470, PH, CM(False)); page("cm2", 470, PH, CM(True))

typed("ib", "inbox", "05", [
    '<span class="c">from:</span> codebyabdullah',
    '<span class="c">subj:</span> <span class="k">process_A-Z.pdf</span>',
    '<span class="m">|-</span> 01 analysis.md',
    '<span class="m">|-</span> 02 PRD_v1.md',
    '<span class="m">|-</span> 03 delivery.md',
    '<span class="ok">1 new</span> <span class="c">just now</span>'])

typed("ho", "client_handoff.md", "06", [
    '<span class="k">## client handoff</span>',
    '<span class="m">[x]</span> analysis',
    '<span class="m">[x]</span> PRD',
    '<span class="m">[x]</span> delivery',
    '<span class="c">quality:</span> <span class="ok">professional</span>'], w=470)

# chest tags
TAGS = ["01 / ANALYSIS", "02 / PRD", "03 / BUILD", "04 / COMMENT", "05 / INBOX", "06 / CLIENT"]
for i, t in enumerate(TAGS, 1):
    page(f"tag{i}", 440, 70, f'<div style="position:absolute;inset:0;display:grid;place-items:center">'
         f'<span style="font-family:Consolas,monospace;font-size:24px;letter-spacing:4px;color:{PIS};background:rgba(18,18,18,.88);'
         f'border:1.5px solid {PIS};padding:6px 16px 7px">{t}</span></div>')

edge_render(HERE, JOBS)
print(len(JOBS), "pngs")

# ---------------------------------------------------------------- captions (libass, complex shaping)
KW = "&H0074DDB9&"   # pistachio (BGR)
WH = "&H00FFFFFF&"
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Alexandria ExtraBold,80,&H00FFFFFF,&H00FFFFFF,&H00121212,&H78000000,-1,0,0,0,100,100,0,0,1,0,3,2,80,80,520,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
def ts(x):
    return f"0:{int(x//60):02d}:{x%60:05.2f}"
for s, e, g, kw in groups_D():
    txt = " ".join(w.replace(kw, f"{{\\c{KW}}}{kw}{{\\c{WH}}}") if kw and kw in w else w for w in g)
    ass.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\fad(70,0)}}{txt}")
(HERE / "captions_D.ass").write_text("\n".join(ass) + "\n", encoding="utf-8")
print("ass ok")
