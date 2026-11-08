"""Generate HTML for every paper/pistachio graphic, plus render_list.txt for Edge.
Palette: paper #F3EEE3, ink #121212, pistachio #B9DD74, cobalt #2E5BFF. No orange anywhere.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
H, P = HERE / "html", HERE / "png"
F = lambda n: (HERE / "fonts" / n).as_uri()
IMG = lambda n: (HERE / n).as_uri()

PAPER, INK, PIS, COB = "#F3EEE3", "#121212", "#B9DD74", "#2E5BFF"

BASE_CSS = f"""
@font-face{{font-family:A;src:url('{F("Alexandria-ExtraBold.ttf")}')}}
@font-face{{font-family:PX;src:url('{F("visitor1.ttf")}')}}
@font-face{{font-family:HW;src:url('{F("Inkfree.ttf")}')}}
@font-face{{font-family:SR;src:url('{F("majallab.ttf")}')}}
@font-face{{font-family:GI;src:url('{F("georgiaz.ttf")}')}}
html,body{{margin:0;background:transparent;overflow:hidden}}
*{{box-sizing:border-box}}
body{{font-family:A,sans-serif;color:{INK}}}
.hl{{background:{PIS};color:{INK};padding:0 .22em;border-radius:2px;display:inline-block}}
.px{{font-family:PX,monospace;letter-spacing:2px}}
.tape{{position:absolute;width:150px;height:44px;background:rgba(243,238,227,.72);
  border:1px solid rgba(18,18,18,.12);box-shadow:0 2px 4px rgba(0,0,0,.15)}}
"""

# hand-drawn wobble filter + doodle shapes
WOBBLE = """<svg width="0" height="0" style="position:absolute"><filter id="wob"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="7"/></filter></svg>"""
CHECK = f'<svg viewBox="0 0 24 24" width="30" height="30"><path d="M4 12.5l5 5L20 6" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def star(size, fill, stroke=INK, sw=5):
    pts = "50,6 61,38 95,38 67,58 78,92 50,71 22,92 33,58 5,38 39,38"
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="filter:url(#wob);overflow:visible"><polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/></svg>'

def arrow(w, h, d, color, sw=9):
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="filter:url(#wob);overflow:visible">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>')

JOBS = []  # (name, w, h)

def page(name, w, h, body, css=""):
    html = (f'<!doctype html><html lang="ar"><head><meta charset="utf-8"><style>{BASE_CSS}'
            f'body{{width:{w}px;height:{h}px;position:relative}}{css}</style></head><body>{WOBBLE}{body}</body></html>')
    (H / f"{name}.html").write_text(html, encoding="utf-8")
    JOBS.append((name, w, h))

# ---------------------------------------------------------------- captions
# token kinds: t=plain white, b=pistachio box (ink text), s=white serif contrast, p=pixel inside box
CAPS = [
    [("b", "وقدرنا نحلل ده")],
    [("t", "عن طريق إننا")],
    [("t", "حللنا"), ("b", "الأناليسيس")],
    [("t", "من"), ("p", "A to Z")],
    [("t", "والبروسيس بتاعته")],
    None,  # paper interlude carries "كاملة"
    [("t", "وقدرنا نطلّع")],
    [("t", "الـ"), ("b", "PRD")],
    [("g", "Business")],
    [("g2", "Requirement Description")],
    None,  # collage beat carries the line
    [("t", "قدرنا نحقق")],
    [("t", "المتطلبات بتاعة"), ("b", "الكلاينت")],
    [("t", "اكتب"), ("b", "كومنت"), ("t", "تحت البوست")],
    [("t", "عشان نبعتلك")],
    [("t", "كل"), ("s", "البروسيس")],
    [("t", "في"), ("b", "الإنبوكس")],
    [("t", "عشان تقدر تتعامل")],
    [("t", "مع الكلاينت بتاعك")],
    [("t", "بشكل"), ("b", "بروفيشنال")],
    [("t", "يليق بالكلاينت"), ("s", "بتاعك")],
]
CAP_CSS = f"""
.cap{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:22px;
  direction:rtl;font-size:74px;line-height:1.25;padding:0 40px;flex-wrap:nowrap;white-space:nowrap}}
.t{{color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.65),0 0 3px rgba(0,0,0,.55)}}
.b{{background:{PIS};color:{INK};padding:2px 26px 10px;border-radius:2px;box-shadow:0 6px 14px rgba(0,0,0,.30)}}
.p{{background:{PIS};color:{INK};padding:10px 26px 4px;border-radius:2px;
  font-family:PX,monospace;font-size:92px;letter-spacing:4px;direction:ltr;box-shadow:0 8px 18px rgba(0,0,0,.35)}}
.s{{font-family:SR,serif;font-size:118px;color:#fff;line-height:1;transform:skewX(-9deg) translateY(4px);
  text-shadow:0 4px 14px rgba(0,0,0,.65)}}
.g2{{font-family:GI,serif;font-size:66px;color:#fff;direction:ltr;text-shadow:0 4px 14px rgba(0,0,0,.65)}}
.g{{font-family:GI,serif;font-size:84px;color:#fff;direction:ltr;text-shadow:0 4px 14px rgba(0,0,0,.65)}}
"""
for i, line in enumerate(CAPS):
    if line is None:
        continue
    spans = "".join(f'<span class="{k}">{txt}</span>' for k, txt in line)
    fit = "<script>document.fonts.ready.then(()=>{const c=document.querySelector('.cap');const w=()=>{let a=1e9,b=-1e9;c.querySelectorAll('span').forEach(e=>{const r=e.getBoundingClientRect();a=Math.min(a,r.left);b=Math.max(b,r.right)});return b-a};let f=74,k=1;while(w()>950&&f>48){f-=2;k=f/74;c.style.fontSize=f+'px';c.style.gap=(22*k)+'px';c.querySelectorAll('.p,.s,.g,.g2').forEach(e=>{e.style.fontSize=''})}})</script>"
    page(f"cap_{i:02d}", 1080, 300, f'<div class="cap" style="padding:0 70px">{spans}</div>{fit}', CAP_CSS)

# ---------------------------------------------------------------- UI cards (paper / ink / pistachio)
CARD_CSS = f"""
.wrap{{position:absolute;inset:0;display:grid;place-items:center}}
.c{{position:relative;width:600px;background:{PAPER};border:3px solid {INK};border-radius:6px;
  box-shadow:8px 8px 0 {INK};padding:30px 34px 34px;direction:rtl;display:flex;flex-direction:column;gap:16px}}
.head{{display:flex;justify-content:space-between;align-items:center;direction:ltr}}
.head .px{{font-size:44px;color:{INK}}}
.head .fn{{font-family:Consolas,monospace;font-size:22px;color:#5b5850}}
.ttl{{font-size:44px;line-height:1.35}}
.row{{display:flex;align-items:center;gap:16px;font-size:30px}}
.ck{{width:44px;height:44px;border-radius:3px;background:{PIS};border:3px solid {INK};display:grid;place-items:center;flex:none}}
.flow{{display:flex;flex-direction:row;align-items:center;justify-content:space-between;direction:rtl;margin-top:6px}}
.st{{background:{INK};color:{PAPER};border-radius:3px;padding:12px 12px 16px;font-size:24px;min-width:84px;text-align:center}}
.st.on{{background:{PIS};color:{INK};border:3px solid {INK}}}
.ar{{font-size:28px;color:{INK}}}
.ln{{height:14px;border-radius:7px;background:rgba(18,18,18,.14)}}
.bar{{margin:-30px -34px 6px;padding:14px 20px;background:{INK};border-radius:3px 3px 0 0;display:flex;gap:10px;align-items:center;direction:ltr}}
.bar i{{width:16px;height:16px;border-radius:50%;display:block}}
.bar span{{margin-left:12px;font-family:Consolas,monospace;font-size:22px;color:{PAPER}}}
.u{{display:flex;gap:14px;align-items:center}}
.av{{width:52px;height:52px;border-radius:50%;background:{PAPER};border:3px solid {INK};flex:none;display:grid;place-items:center;font-size:22px}}
.bub{{background:#fff;border:2px solid {INK};border-radius:6px;padding:10px 24px 14px;font-size:32px}}
.bub.me{{background:{PIS}}}
.pill{{background:{COB};color:#fff;border-radius:3px;padding:4px 16px 8px;font-size:20px}}
"""
def card(name, inner, rot, tape=(250, -26, -4)):
    tx, ty, tr = tape
    t = ""
    page(name, 760, 640, f'<div class="wrap"><div class="c" style="transform:rotate({rot}deg)">{inner}{t}</div></div>', CARD_CSS)

card("card_analysis", f"""
<div class="head"><span class="px">01</span><span class="fn">analysis.md</span></div>
<div class="ttl">تحليل <span class="hl">المشروع</span></div>
<div class="row"><span class="ck">{CHECK}</span>أهداف العميل</div>
<div class="row"><span class="ck">{CHECK}</span>مين المستخدمين</div>
<div class="row"><span class="ck">{CHECK}</span>البروسيس الحالية</div>
<div class="row"><span class="ck">{CHECK}</span>نقط الوجع</div>""", -1)

card("card_process", f"""
<div class="head"><span class="px">A-Z</span><span class="fn">process.flow</span></div>
<div class="ttl">البروسيس <span class="hl">كاملة</span></div>
<div class="flow"><span class="st on">تحليل</span><span class="ar">&larr;</span><span class="st">PRD</span><span class="ar">&larr;</span>
<span class="st">تصميم</span><span class="ar">&larr;</span><span class="st">تطوير</span><span class="ar">&larr;</span><span class="st">إطلاق</span></div>""", 1, (90, -24, 5))

card("card_prd", f"""
<div class="bar"><i style="background:{PAPER}"></i><i style="background:{PIS}"></i><i style="background:{COB}"></i><span>PRD_v1.pdf</span></div>
<div class="head"><span class="px">02</span><span class="pill">v1</span></div>
<div style="font-family:GI,serif;font-size:46px;direction:ltr;text-align:left;line-height:1.25">Business Requirement <span class="hl" style="font-family:GI,serif">Description</span></div>
<div class="ln" style="width:94%"></div><div class="ln" style="width:80%"></div><div class="ln" style="width:88%"></div><div class="ln" style="width:58%"></div>""", 1, (380, -24, 4))

card("card_comment", f"""
<div class="head"><span class="px">+3</span><span class="fn">comments</span></div>
<div class="u"><span class="av">م</span><div class="bub">شغّال</div></div>
<div class="u"><span class="av">س</span><div class="bub me">شغّال</div></div>
<div class="u"><span class="av">ك</span><div class="bub">شغّال</div></div>""", -1)

card("card_inbox", f"""
<div class="head"><span class="px" style="background:{COB};color:#fff;border-radius:3px;padding:2px 12px 0">1 new</span><span class="fn">inbox</span></div>
<div class="bub me" style="align-self:flex-start">أهلًا! دي البروسيس كاملة</div>
<div class="bub me" style="align-self:flex-start;direction:ltr;font-size:28px">Analysis &rarr; PRD &rarr; Build</div>
<div class="bub" style="align-self:flex-end">تسلم يا هندسة</div>""", -1, (300, -24, -3))

# site screenshots as taped B&W photocopies (no source colours survive)
POL_CSS = f"""
.wrap{{position:absolute;inset:0;display:grid;place-items:center}}
.pol{{position:relative;width:480px;background:{PAPER};border:4px solid {INK};padding:12px 12px 16px;box-shadow:8px 8px 0 {INK}}}
.pol img{{display:block;width:100%;filter:grayscale(1) contrast(1.15) brightness(1.04);border:2px solid {INK}}}
.pol .px{{font-size:30px;margin-top:8px;direction:ltr}}
"""
for nm, src, rot, lbl in [("pol_rakeeza", "broll/site_rakeeza.png", -1, "01 / live"),
                          ("pol_athar", "broll/site_athar.png", 1, "02 / live"),
                          ]:
    page(nm, 580, 460, f'<div class="wrap"><div class="pol" style="transform:rotate({rot}deg)"><img src="{IMG(src)}">'
         f'<div class="px">{lbl}</div></div></div>', POL_CSS)

page("pol_home_top", 860, 520, f'<div class="wrap"><div class="pol" style="width:740px;transform:rotate(0deg)"><img src="{IMG("broll/site_home_top.png")}">'
     f'<div class="px">03 / live</div></div></div>', POL_CSS)

# ---------------------------------------------------------------- frames, pills, notes
page("frame_solid", 1080, 1920, f'<div style="position:absolute;inset:0;border:34px solid {PIS}"></div>'
     f'<div style="position:absolute;inset:34px;border:4px solid {INK}"></div>')
page("frame_dash", 1080, 1920, f'<div style="position:absolute;inset:26px;border:10px dashed {PIS};border-radius:28px"></div>')

PILL_CSS = f""".pill{{position:absolute;inset:0;display:grid;place-items:center}}
.pill > span{{background:{COB};color:#fff;font-family:Consolas,monospace;font-weight:700;font-size:30px;letter-spacing:3px;
 border-radius:4px;padding:10px 22px;direction:ltr;box-shadow:0 4px 10px rgba(0,0,0,.30)}}"""
for i, lbl in enumerate(["STEP 01 / ANALYSIS", "STEP 02 / PRD", "STEP 03 / DELIVERY"], 1):
    page(f"pill_{i}", 520, 120, f'<div class="pill"><span>{lbl}</span></div>', PILL_CSS)

# ---------------------------------------------------------------- paper backgrounds (procedural)
GRAPH = f"""<svg width="1080" height="1920" style="position:absolute;inset:0">
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/><feColorMatrix type="saturate" values="0"/>
<feComponentTransfer><feFuncA type="table" tableValues="0 0.09"/></feComponentTransfer></filter>
<filter id="blot"><feTurbulence type="fractalNoise" baseFrequency="0.004" numOctaves="3" seed="11"/><feColorMatrix type="saturate" values="0"/>
<feComponentTransfer><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer></filter>
<rect width="100%" height="100%" filter="url(#blot)"/><rect width="100%" height="100%" filter="url(#grain)"/></svg>"""
GRAPH_CSS = f"""body{{background-color:{PAPER};
 background-image:linear-gradient(rgba(46,91,255,.16) 2px,transparent 2px),linear-gradient(90deg,rgba(46,91,255,.16) 2px,transparent 2px),
 linear-gradient(rgba(46,91,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(46,91,255,.07) 1px,transparent 1px);
 background-size:180px 180px,180px 180px,36px 36px,36px 36px;background-position:-6px -6px}}
.vig{{position:absolute;inset:0;box-shadow:inset 0 0 200px rgba(40,40,30,.16)}}"""
CRUMPLE = f"""<svg width="1080" height="1920" style="position:absolute;inset:0">
<filter id="cr" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="5" seed="23" result="n"/>
<feDiffuseLighting in="n" surfaceScale="5" lighting-color="#F3EEE3" result="l"><feDistantLight azimuth="235" elevation="52"/></feDiffuseLighting>
<feComposite in="l" in2="SourceGraphic" operator="in"/></filter>
<filter id="grain2"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/>
<feComponentTransfer><feFuncA type="table" tableValues="0 0.07"/></feComponentTransfer></filter>
<rect width="100%" height="100%" fill="#fff" filter="url(#cr)"/><rect width="100%" height="100%" filter="url(#grain2)"/></svg>"""

BOX_CSS = f""".kbox{{position:absolute;background:{INK};color:{PIS};font-size:118px;line-height:1.2;padding:24px 54px 44px;
 direction:rtl;box-shadow:12px 12px 0 {PIS};white-space:nowrap}}
.sticky{{position:absolute;width:300px;height:300px;background:{PIS};box-shadow:6px 10px 18px rgba(0,0,0,.25);
 color:{INK};font-size:38px;line-height:1.6;padding:34px 30px;direction:rtl}}
.hw{{position:absolute;font-family:HW,cursive;font-weight:700;color:{INK};font-size:70px;white-space:nowrap}}"""

STRAIGHT_ARROW = f'<svg width="340" height="40" viewBox="0 0 340 40"><path d="M330 20H14M14 20l18-14M14 20l18 14" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="square"/></svg>'
LABEL_CSS = f""".lab{{position:absolute;font-family:Consolas,monospace;font-weight:700;font-size:30px;letter-spacing:4px;color:{INK};direction:ltr}}"""

# interlude 1: plain graph paper, straight box, one straight arrow
page("paper1_bg", 1080, 1920, f"""{GRAPH}<div class="vig"></div>
<div class="lab" style="left:110px;top:700px">02 / PROCESS</div>
<div style="position:absolute;left:370px;top:1080px">{STRAIGHT_ARROW}</div>""", GRAPH_CSS + BOX_CSS + LABEL_CSS)
page("paper1_box", 1080, 1920, f"""<div class="kbox" style="left:0;right:0;margin:auto;width:fit-content;top:780px;font-size:100px">
البروسيس <span style="background:{PIS};color:{INK};padding:0 18px 8px;border-radius:2px">كاملة</span></div>""", BOX_CSS)

# cut-out beat: clean cut-out on graph paper, line in an ink box
page("paper2_bg", 1080, 1920, f"""{GRAPH}<div class="vig"></div>
<div class="lab" style="left:110px;top:190px">03 / DELIVERY</div>""", GRAPH_CSS + LABEL_CSS)
page("paper2_box", 1080, 1920, f"""<div class="kbox" style="left:0;right:0;margin:auto;width:fit-content;top:300px;font-size:100px">
وبناءً على <span style="background:{PIS};color:{INK};padding:0 16px 6px;border-radius:2px">كل ده</span></div>""", BOX_CSS)

(HERE / "render_list.txt").write_text("\n".join(f"{n}|{w}|{h}" for n, w, h in JOBS), encoding="utf-8")
print(len(JOBS), "pages")
