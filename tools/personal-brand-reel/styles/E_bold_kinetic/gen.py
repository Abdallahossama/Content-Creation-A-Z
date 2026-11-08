"""Style E 'Bold Kinetic': big pop captions (keyword in a pistachio box), full-screen ink title cards,
paper b-roll cards that slam in with motion blur. Renders html -> png with Edge, then builds three
frame-exact overlay tracks (tracks/cap, tracks/broll, tracks/title) with ffmpeg + hard links."""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "D"))
from de_common import *

H = HERE / "html"; H.mkdir(exist_ok=True)
P = HERE / "png"; FR = HERE / "frames"; FR.mkdir(exist_ok=True)
JOBS = []
SKIP_RENDER = "--norender" in sys.argv

BASE_CSS = f"""@font-face{{font-family:A;src:url('{FONT_A}')}}
html,body{{margin:0;background:transparent;overflow:hidden}}*{{box-sizing:border-box}}body{{font-family:A,sans-serif}}"""

def page(name, w, h, body, css=""):
    (H / f"{name}.html").write_text(f'<!doctype html><html lang="ar"><head><meta charset="utf-8"><style>{BASE_CSS}'
        f'body{{width:{w}px;height:{h}px;position:relative}}{css}</style></head><body>{body}</body></html>', encoding="utf-8")
    JOBS.append((name, w, h))

# ------------------------------------------------------------------ captions
CW, CH = 1080, 420
CAP_CSS = f"""
.cap{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;direction:rtl;gap:26px;
 font-size:118px;line-height:1.15;color:#fff;white-space:nowrap}}
.w{{text-shadow:0 6px 22px rgba(0,0,0,.55),0 2px 4px rgba(0,0,0,.45)}}
.kb{{background:{PIS};color:{INK};padding:4px 30px 18px;border-radius:16px;box-shadow:0 10px 26px rgba(0,0,0,.35)}}
.lat{{direction:ltr;unicode-bidi:isolate}}
"""
FIT = ("<script>document.fonts.ready.then(()=>{const c=document.querySelector('.cap');const w=()=>{let a=1e9,b=-1e9;"
       "c.querySelectorAll(':scope>span').forEach(e=>{const r=e.getBoundingClientRect();a=Math.min(a,r.left);b=Math.max(b,r.right)});return b-a};"
       "let f=118;while(w()>840&&f>60){f-=3;c.style.fontSize=f+'px';c.style.gap=(26*f/118)+'px'}})</script>")
import re
def lat(s):
    return f'<span class="lat">{s}</span>' if re.search(r"[A-Za-z]", s) else s
GROUPS = groups_E()
for i, (s, e, g, kw) in enumerate(GROUPS):
    parts = []
    for w in g:
        if kw and kw in w:
            pre = w.replace(kw, "").strip()
            if pre:
                parts.append(f'<span class="w">{pre}</span>')
            parts.append(f'<span class="kb">{lat(kw)}</span>')
        else:
            parts.append(f'<span class="w">{lat(w)}</span>')
    page(f"cap{i:02d}", CW, CH, f'<div class="cap">{"".join(parts)}</div>{FIT}', CAP_CSS)

# ------------------------------------------------------------------ title cards (3 key beats)
TITLES = [("تحليل", "01 / ANALYSIS", 1.41, 2.02), ("PRD", "02 / PRD", 5.79, 6.40), ("تسليم", "03 / DELIVERY", 8.09, 8.72)]
for i, (word, lab, *_ ) in enumerate(TITLES, 1):
    page(f"tbg{i}", 1080, 1920, f"""<div style="position:absolute;inset:0;background:{INK}"></div>
<div style="position:absolute;left:96px;top:640px;font-family:Consolas,monospace;font-size:34px;letter-spacing:6px;color:{PAPER};opacity:.75">{lab}</div>
<div style="position:absolute;left:96px;right:96px;top:1300px;height:6px;background:{PIS}"></div>
<div style="position:absolute;right:96px;top:1336px;font-family:Consolas,monospace;font-size:28px;letter-spacing:5px;color:{PAPER};opacity:.45">CODEBYABDULLAH</div>""")
    fs = 330 if word != "PRD" else 360
    page(f"tw{i}", 1080, 1920, f"""<div style="position:absolute;left:0;right:0;top:0;height:1920px;display:flex;align-items:center;justify-content:center">
<div style="font-size:{fs}px;line-height:1;color:{PIS};direction:rtl;margin-top:30px;{'direction:ltr;letter-spacing:6px' if word=='PRD' else ''}">{word}</div></div>""")

# ------------------------------------------------------------------ b-roll cards (paper, clean, big type)
BW, BH = 1080, 660
CARD_CSS = f"""
.wrap{{position:absolute;inset:0;display:grid;place-items:center}}
.c{{width:900px;background:{PAPER};border-radius:30px;padding:40px 48px 46px;direction:rtl;color:{INK};
 box-shadow:0 24px 50px rgba(0,0,0,.40),0 4px 10px rgba(0,0,0,.25);display:flex;flex-direction:column;gap:22px}}
.lab{{font-family:Consolas,monospace;font-size:24px;letter-spacing:4px;color:rgba(18,18,18,.55);direction:ltr;text-align:left;display:flex;justify-content:space-between}}
.lab b{{font-weight:400;color:{INK};background:{PIS};padding:2px 12px;border-radius:6px}}
.ttl{{font-size:66px;line-height:1.2}}
.hl{{background:{PIS};padding:0 16px 8px;border-radius:12px}}
.flow{{display:flex;align-items:center;justify-content:space-between}}
.st{{background:{INK};color:{PAPER};border-radius:16px;padding:12px 22px 18px;font-size:34px}}
.st.on{{background:{PIS};color:{INK}}}
.ar{{font-size:34px;color:rgba(18,18,18,.4)}}
.ln{{height:16px;border-radius:8px;background:rgba(18,18,18,.12)}}
.row{{display:flex;align-items:center;gap:22px;font-size:44px}}
.ck{{width:58px;height:58px;border-radius:14px;background:{PIS};display:grid;place-items:center;flex:none}}
.shot{{border-radius:18px;overflow:hidden;height:330px}}
.shot img{{width:100%;display:block;filter:grayscale(1) contrast(1.1)}}
"""
CHECK = f'<svg viewBox="0 0 24 24" width="34" height="34"><path d="M5 12.5l4.5 4.5L19 7" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def card(name, inner):
    page(name, BW, BH, f'<div class="wrap"><div class="c">{inner}</div></div>', CARD_CSS)

card("b_flow", f"""<div class="lab"><span>process.flow</span><b>A-Z</b></div>
<div class="ttl">البروسيس <span class="hl">كاملة</span></div>
<div class="flow"><span class="st on">تحليل</span><span class="ar">&larr;</span><span class="st">PRD</span><span class="ar">&larr;</span>
<span class="st">تصميم</span><span class="ar">&larr;</span><span class="st">تسليم</span></div>""")
card("b_prd", f"""<div class="lab"><span>PRD_v1.pdf</span><b>02</b></div>
<div class="ttl" style="direction:ltr;text-align:left;font-size:60px">Business Requirement <span class="hl">Description</span></div>
<div class="ln" style="width:92%"></div><div class="ln" style="width:76%"></div><div class="ln" style="width:84%"></div>""")
card("b_site", f"""<div class="lab"><span>client / live</span><b>03</b></div>
<div class="shot"><img src="{(WS / 'edit_paper' / 'broll' / 'site_athar.png').as_uri()}"></div>""")
card("b_comment", f"""<div class="lab"><span>comments</span><b>+1</b></div>
<div style="display:flex;gap:18px;align-items:center">
<div style="flex:1;border:3px solid {INK};border-radius:18px;padding:10px 26px 18px;font-size:46px">اكتب كومنت...</div>
<div style="background:{PIS};border-radius:18px;padding:12px 30px 20px;font-size:42px">ابعت</div></div>""")
card("b_inbox", f"""<div class="lab"><span>inbox</span><b>1 new</b></div>
<div style="display:flex;gap:24px;align-items:center">
<div style="width:96px;height:96px;border-radius:50%;background:{INK};color:{PIS};display:grid;place-items:center;font-family:Consolas,monospace;font-size:34px;flex:none">CA</div>
<div style="display:flex;flex-direction:column;gap:6px"><div style="font-size:30px;font-family:Consolas,monospace;direction:ltr;text-align:right;color:rgba(18,18,18,.6)">codebyabdullah</div>
<div style="font-size:50px">البروسيس <span class="hl">كاملة</span></div></div></div>
<div class="ln" style="width:88%"></div>""")
card("b_pro", f"""<div class="lab"><span>client_handoff</span><b>06</b></div>
<div class="row"><span class="ck">{CHECK}</span>تحليل</div>
<div class="row"><span class="ck">{CHECK}</span>PRD</div>
<div class="row"><span class="ck">{CHECK}</span>تسليم <span class="hl" style="font-size:40px">بروفيشنال</span></div>""")

if not SKIP_RENDER:
    edge_render(HERE, JOBS)
print(len(JOBS), "pngs")

# ------------------------------------------------------------------ derived frames (ffmpeg)
def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)

def blank(w, h):
    p = FR / f"blank_{w}x{h}.png"
    if not p.exists():
        ff("-f", "lavfi", "-i", f"color=c=black@0.0:s={w}x{h},format=rgba", "-frames:v", "1", str(p))
    return str(p)

def scaled(src, dst, sc, w, h):
    """scale about the centre, keep canvas size (pop frames)"""
    ff("-i", src, "-filter_complex",
       f"color=c=black@0:s={w}x{h},format=rgba[c];[0]format=rgba,scale=iw*{sc}:-1:flags=lanczos[k];[c][k]overlay=(W-w)/2:(H-h)/2:format=auto",
       "-frames:v", "1", dst)

def slammed(src, dst, dx, sigma, w, h):
    blur = f",gblur=sigma={sigma}:sigmaV=0.01" if sigma > 0 else ""
    ff("-i", src, "-filter_complex",
       f"color=c=0xF3EEE3@0:s={w}x{h},format=rgba[c];[0]format=rgba[k];[c][k]overlay=x={int(dx)}:y=0:format=auto{blur}",
       "-frames:v", "1", dst)

NF = NFR
fi = lambda t: int(round(t * FPS))

# captions: pop 1.22 -> 1.08 -> 1.0
cap = [None] * NF
POP = [1.22, 1.08]
for i, (s, e, g, kw) in enumerate(GROUPS):
    src = str(P / f"cap{i:02d}.png")
    pops = []
    for j, sc in enumerate(POP):
        d = FR / f"cap{i:02d}_p{j}.png"; scaled(src, str(d), sc, CW, CH); pops.append(str(d))
    a, b = fi(s), min(fi(e), NF)
    for n in range(a, b):
        cap[n] = pops[n - a] if n - a < len(pops) else src

# title cards: word pop 1.35 -> 1.12 -> 1.03 -> 1.0 over the ink background
title = [None] * NF
for i, (word, lab, s, e) in enumerate(TITLES, 1):
    seq = []
    for j, sc in enumerate([1.35, 1.12, 1.03, 1.0]):
        d = FR / f"title{i}_{j}.png"
        ff("-i", str(P / f"tbg{i}.png"), "-i", str(P / f"tw{i}.png"), "-filter_complex",
           f"[1]format=rgba,scale=iw*{sc}:-1:flags=lanczos,crop=1080:1920[w];[0]format=rgba[b];[b][w]overlay=0:0:format=auto",
           "-frames:v", "1", str(d))
        seq.append(str(d))
    a, b = fi(s), fi(e)
    for n in range(a, b):
        title[n] = seq[min(n - a, 3)]

# b-roll: slam in (5 frames, motion blur), hold, slam out (3 frames)
BROLL = [("b_flow", 2.40, 4.00, 1), ("b_prd", 6.66, 8.06, -1), ("b_site", 9.86, 11.30, 1),
         ("b_comment", 11.40, 12.66, -1), ("b_inbox", 14.30, 17.25, 1), ("b_pro", 19.12, 21.58, -1)]
IN = [(1.00, 46), (0.52, 30), (0.22, 14), (0.06, 4), (-0.015, 0)]
OUTF = [(-0.10, 8), (-0.42, 28), (-1.0, 46)]
broll = [None] * NF
for name, s, e, side in BROLL:
    src = str(P / f"{name}.png")
    a, b = fi(s), fi(e)
    frames_in, frames_out = [], []
    for j, (m, sg) in enumerate(IN):
        d = FR / f"{name}_in{j}.png"; slammed(src, str(d), side * m * 1080, sg, BW, BH); frames_in.append(str(d))
    for j, (m, sg) in enumerate(OUTF):
        d = FR / f"{name}_out{j}.png"; slammed(src, str(d), side * m * 1080, sg, BW, BH); frames_out.append(str(d))
    for n in range(a, b):
        r, q = n - a, b - 1 - n
        broll[n] = frames_in[r] if r < len(frames_in) else frames_out[len(frames_out) - 1 - q] if q < len(frames_out) else src

link_track(HERE / "tracks" / "cap", cap, blank(CW, CH))
link_track(HERE / "tracks" / "broll", broll, blank(BW, BH))
link_track(HERE / "tracks" / "title", title, blank(1080, 1920))
json.dump(dict(groups=[(s, e, " ".join(g), kw) for s, e, g, kw in GROUPS], titles=TITLES, broll=BROLL),
          open(HERE / "timeline_E.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("tracks ok")
