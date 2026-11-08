"""Shared bits for the style tests (D, E): caption timing, word groups, Edge rendering, audio chain.
Caption times come from the approved Paper Pro captions.ass (already mapped to the base timeline
through plan.json's keep list), so speech and timing stay identical across styles.
"""
import json, os, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
WS = ROOT.parent
BASE = (WS / "edit_paper" / "base.mp4").as_posix()
MASKS = "D:/codebyabdullah_assets/tmp_masks/%04d.png"
FONT_A = (WS / "edit" / "fonts" / "Alexandria-ExtraBold.ttf").as_uri()
FONTS_DIR = (WS / "edit" / "fonts").as_posix()
DUR, FPS, NFR = 23.21, 30, 698
SFX = "D:/why habibi/_style_kit/sfx/"
CLICK = (WS / "edit_paper" / "click.wav").as_posix()
MUSIC = ("D:/why habibi/_music_library/Late Night Radio.mp3", -18)
PAPER, INK, PIS, COB = "#F3EEE3", "#121212", "#B9DD74", "#2E5BFF"
OUTDIR = "C:/Users/ossam/Downloads/video_20261105_130210_EDIT/styles"


def t2s(t):
    h, m, s = t.split(":"); return int(h) * 3600 + int(m) * 60 + float(s)


def lines():
    """[(start, end, text, keyword)] on the base timeline, 21 lines."""
    ass = (WS / "edit_paper" / "captions.ass").read_text(encoding="utf-8")
    rows = re.findall(r"^Dialogue: 0,([^,]+),([^,]+),Cap,,0,0,0,,(.*)$", ass, re.M)
    plan = json.loads((WS / "edit" / "plan.json").read_text(encoding="utf-8"))
    out = []
    for (a, b, txt), cap in zip(rows, plan["captions"]):
        out.append((t2s(a), t2s(b), re.sub(r"\{[^}]*\}", "", txt).strip(), cap[3]))
    assert len(out) == 21
    return out


def tokens(text, kw):
    """Split into words, keeping a multi-word keyword and 'الـ X' together."""
    if kw and " " in kw and kw in text:
        text = text.replace(kw, kw.replace(" ", "\u00a0"))
    toks = text.split(" ")
    out = []
    for t in toks:
        if out and out[-1] == "الـ":
            out[-1] = out[-1] + "\u00a0" + t
        else:
            out.append(t)
    return [t.replace("\u00a0", " ") for t in out]


def split_time(s, e, groups):
    w = [sum(len(t) + 1 for t in g) for g in groups]
    tot, acc, res = sum(w), s, []
    for g, wi in zip(groups, w):
        d = (e - s) * wi / tot
        res.append((round(acc, 3), round(acc + d, 3), g))
        acc += d
    return res


def groups_D():
    """2-3 words per caption (4-word lines become 2+2)."""
    res = []
    for s, e, txt, kw in lines():
        t = tokens(txt, kw)
        gs = [t] if len(t) <= 3 else [t[:2], t[2:]]
        res += [(a, b, g, kw) for a, b, g in split_time(s, e, gs)]
    return res


def groups_E():
    """1-3 words per pop; the keyword starts its own pop so it can land on the beat."""
    res = []
    for s, e, txt, kw in lines():
        t = tokens(txt, kw)
        if len(t) >= 4:
            gs = [t[:2], t[2:]]
        elif kw and kw in t and len(t) > 1:
            i = t.index(kw)
            pre, post = t[:i], t[i:]
            if len(pre) == 1 and len(pre[0]) <= 3:      # tiny particle stays with the keyword
                gs = [t]
            else:
                gs = ([pre[:2], pre[2:]] if len(pre) > 2 else [pre] if pre else []) + [post[:2]] + ([post[2:]] if len(post) > 2 else [])
        elif len(t) >= 4:
            gs = [t[:2], t[2:]]
        else:
            gs = [t]
        res += [(a, b, g, kw) for a, b, g in split_time(s, e, [g for g in gs if g])]
    return res


def edge_render(root, jobs):
    """jobs: [(name, w, h)] with html/<name>.html -> png/<name>.png (transparent background)."""
    root = pathlib.Path(root)
    (root / "render_list.txt").write_text("\n".join(f"{n}|{w}|{h}" for n, w, h in jobs), encoding="utf-8")
    ps = pathlib.Path(__file__).resolve().parent / "de_render.ps1"
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps), "-Root", str(root)], check=True)
    missing = [n for n, *_ in jobs if not (root / "png" / f"{n}.png").exists()]
    assert not missing, missing


def audio_chain(k, fx):
    """Input args + filter lines for voice + sfx + ducked music bed, loudnorm -14 LUFS (same chain as Paper Pro).
    k = index of the next ffmpeg input; fx = [(file, at_seconds, gain_db)]."""
    args, mix, labels = [], ["[0:a]asplit=2[voice][key]"], ["[voice]"]
    for j, (f, at, g) in enumerate(fx):
        args += ["-i", f if ":" in f else SFX + f]
        mix.append(f"[{k+j}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={int(at*1000)}:all=1[fx{j}]")
        labels.append(f"[fx{j}]")
    b = k + len(fx)
    args += ["-stream_loop", "-1", "-i", MUSIC[0]]
    mix.append(f"[{b}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR},volume={MUSIC[1]}dB,"
               f"afade=t=in:d=0.8,afade=t=out:st={DUR-1.8}:d=1.8[bedraw]")
    mix.append("[bedraw][key]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=300[bed]")
    labels.append("[bed]")
    mix.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.89,"
               "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
    return args, mix


ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-color_range", "tv", "-r", "30",
       "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k"]


def link_track(dst, frames, blank):
    """Write an image-sequence track: frames = list of png paths (or None) per output frame, hard-linked."""
    dst = pathlib.Path(dst); dst.mkdir(parents=True, exist_ok=True)
    for f in dst.glob("*.png"):
        f.unlink()
    for n, src in enumerate(frames):
        os.link(src or blank, dst / f"{n:04d}.png")
