"""Shared helpers for the style tests in edit_styles/ (B, C).
NOTE: the original file here was accidentally overwritten by the D/E agent on 8 Nov 06:50; this is a
best-effort reconstruction of the names gen_B.py uses (LINES, PAPERDIR, font_css, spans, palette) plus
timing/audio helpers. D and E use their own copy in D/de_common.py and never import this file.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
WS = ROOT.parent
PAPERDIR = WS / "edit_paper"
EDITDIR = WS / "edit"
BASE = (PAPERDIR / "base.mp4").as_posix()
MASKS = "D:/codebyabdullah_assets/tmp_masks/%04d.png"
FONTS = EDITDIR / "fonts"
FONT_A = (FONTS / "Alexandria-ExtraBold.ttf").as_uri()
DUR, FPS = 23.21, 30
SFX = "D:/why habibi/_style_kit/sfx/"
CLICK = (PAPERDIR / "click.wav").as_posix()
MUSIC = ("D:/why habibi/_music_library/Late Night Radio.mp3", -18)
PAPER, INK, PIS, COB = "#F3EEE3", "#121212", "#B9DD74", "#2E5BFF"
OUTDIR = "C:/Users/ossam/Downloads/video_20261105_130210_EDIT/styles"


def t2s(t):
    h, m, s = t.split(":"); return int(h) * 3600 + int(m) * 60 + float(s)


def _lines():
    ass = (PAPERDIR / "captions.ass").read_text(encoding="utf-8")
    rows = re.findall(r"^Dialogue: 0,([^,]+),([^,]+),Cap,,0,0,0,,(.*)$", ass, re.M)
    plan = json.loads((EDITDIR / "plan.json").read_text(encoding="utf-8"))
    return [dict(s=t2s(a), e=t2s(b), text=re.sub(r"\{[^}]*\}", "", txt).strip(), kw=cap[3])
            for (a, b, txt), cap in zip(rows, plan["captions"])]


LINES = _lines()  # 21 caption lines on the base timeline: {s, e, text, kw}


def font_css():
    return f"@font-face{{font-family:A;src:url('{FONT_A}')}}"


def spans(text, kw=""):
    """HTML for a caption: keyword wrapped in .k, Latin runs isolated in .lat."""
    def lat(s):
        return re.sub(r"([A-Za-z][A-Za-z0-9 \-]*[A-Za-z0-9]|[A-Za-z])", r'<span class="lat">\1</span>', s)
    if kw and kw in text:
        a, b = text.split(kw, 1)
        return lat(a) + f'<span class="k">{lat(kw)}</span>' + lat(b)
    return lat(text)
