"""Render vertical Shorts (1080x1920) straight from the CapCut timeline JSON we built.
Main visual sits mid-frame (graphics as a framed 16:9 card, memes large), big word-highlight captions
below, hook headline on top, midnight background behind everything, audio re-mixed from the same
VO / music / SFX segments."""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageSequence
import gfxlib as G
G.W, G.H = 1080, 1920
from gfxlib import text, pill, place, bg_at, NAVY, YEL, WHITE, B

W, H, FPS = 1080, 1920, 30
CY = 880                      # visual centre
CAP_Y = 1370                  # caption centre
OUT = B + "1st video/claude_package/shorts/"
os.makedirs(OUT, exist_ok=True)
D = json.load(open("new_draft_content.json", encoding="utf-8"))
MAT = {m["id"]: m for k, v in D["materials"].items() if isinstance(v, list) for m in v if isinstance(m, dict) and "id" in m}
TR = D["tracks"]
MAIN, OV, TXT = TR[1]["segments"], TR[2]["segments"], TR[4]["segments"]
AUDIO_TRACKS = [t for t in TR if t["type"] == "audio"]

def span(s):
    st = s["target_timerange"]["start"] / 1e6
    return st, st + s["target_timerange"]["duration"] / 1e6

def seg_at(segs, t):
    for s in segs:
        a, b = span(s)
        if a <= t < b:
            return s
    return None

def kf_ratio(s, t):
    base = s["clip"]["scale"]["x"] if s.get("clip") else 1.0
    a, _ = span(s)
    src0 = (s.get("source_timerange") or {}).get("start", 0)
    rel = src0 + (t - a) * 1e6
    for e in s.get("common_keyframes") or []:
        if e["property_type"] != "KFTypeScaleX":
            continue
        pts = sorted((p["time_offset"], p["values"][0]) for p in e["keyframe_list"])
        if rel <= pts[0][0]:
            v = pts[0][1]
        elif rel >= pts[-1][0]:
            v = pts[-1][1]
        else:
            for (o0, v0), (o1, v1) in zip(pts, pts[1:]):
                if o0 <= rel <= o1:
                    v = v0 + (v1 - v0) * (rel - o0) / max(1, o1 - o0); break
        return v / base if base else 1.0
    return 1.0

_img = {}
def still_img(path):
    if path not in _img:
        _img[path] = Image.open(path).convert("RGBA")
    return _img[path]

_gif = {}
def gif_frame(path, t):
    if path not in _gif:
        im = Image.open(path); fr = []; durs = []
        for f in ImageSequence.Iterator(im):
            fr.append(f.convert("RGBA")); durs.append(max(20, f.info.get("duration", 80)) / 1000)
        _gif[path] = (fr, np.cumsum(durs))
    fr, cum = _gif[path]
    i = int(np.searchsorted(cum, t % cum[-1], side="right"))
    return fr[min(i, len(fr) - 1)]

class VReader:
    def __init__(self, path, src_start, w, h):
        self.w, self.h = w, h
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{src_start:.3f}", "-i", path, "-f", "rawvideo",
                                   "-pix_fmt", "rgba", "-r", str(FPS), "-s", f"{w}x{h}", "-"], stdout=subprocess.PIPE)
        self.last = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    def next(self):
        buf = self.p.stdout.read(self.w * self.h * 4)
        if len(buf) == self.w * self.h * 4:
            self.last = Image.frombuffer("RGBA", (self.w, self.h), buf, "raw", "RGBA", 0, 1)
        return self.last
    def close(self):
        try: self.p.kill()
        except Exception: pass

def is_card(m):
    p = m.get("path", "")
    return "/claude_gfx/" in p or "end_screen" in p

_mask = {}
def rounded(im, r=28):
    key = im.size
    if key not in _mask:
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255); _mask[key] = m
    out = im.copy(); out.putalpha(_mask[key]); return out

def framed(im, r=28, ow=7):
    pad = 26
    c = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((pad, pad + 14, pad + im.width, pad + im.height + 14), r, fill=(0, 0, 0, 150))
    c = c.filter(ImageFilter.GaussianBlur(8)); c.alpha_composite(rounded(im, r), (pad, pad))
    ImageDraw.Draw(c).rounded_rectangle((pad, pad, pad + im.width, pad + im.height), r, outline=NAVY + (255,), width=ow)
    return c

# ---------- captions ----------
def caption_layers(s, t):
    m = MAT[s["material_id"]]
    txt = json.loads(m["content"])["text"]
    a, b = span(s)
    words = [w for w in m.get("words", {}).get("text", []) if w.strip()]
    starts = [st for st, w in zip(m["words"]["start_time"], m["words"]["text"]) if w.strip()]
    rel = (t - a) * 1000
    cur = 0
    for i, st in enumerate(starts):
        if rel >= st - 60: cur = i
    if not words:
        words = txt.split(); cur = -1
    sprs = [text(w.upper(), 96, YEL if i == cur else WHITE, stroke=11, stroke_fill=(10, 10, 30), shadow=6) for i, w in enumerate(words)]
    lines, line, lw = [], [], 0
    for sp in sprs:
        if line and lw + sp.width - 10 > 1000:
            lines.append(line); line, lw = [], 0
        line.append(sp); lw += sp.width - 10
    if line: lines.append(line)
    pop = 0.86 + 0.14 * min(1, (t - a) / 0.12)
    return lines, pop

def draw_captions(c, t):
    s = seg_at(TXT, t)
    if not s: return
    lines, pop = caption_layers(s, t)
    lh = 112; y0 = CAP_Y - (len(lines) - 1) * lh / 2
    for li, line in enumerate(lines):
        tw = sum(sp.width - 10 for sp in line); x = W / 2 - tw * pop / 2
        for sp in line:
            place(c, sp, x + sp.width * pop / 2, y0 + li * lh, pop); x += (sp.width - 10) * pop

# ---------- main visual + overlays ----------
class Visual:
    def __init__(self):
        self.reader, self.rseg = None, None
    def frame(self, c, t):
        s = seg_at(MAIN, t)
        if not s: return
        m = MAT[s["material_id"]]; path = m["path"]; a, b = span(s)
        r = kf_ratio(s, t)
        if m["type"] == "video":
            card = is_card(m)
            w0, h0 = (1920, 1080) if card else (m["width"], m["height"])
            if self.rseg is not s:
                if self.reader: self.reader.close()
                src = (s.get("source_timerange") or {}).get("start", 0) / 1e6 + (t - a)
                self.reader = VReader(path, src, w0, h0); self.rseg = s
            im = self.reader.next()
        else:
            if self.reader: self.reader.close(); self.reader, self.rseg = None, None
            card = is_card(m)
            im = gif_frame(path, t - a) if m["type"] == "gif" else still_img(path)
        if card:
            mg = 0 if ("_level" in path or "end_screen" in path) else (100 if "07_streaming" in path else 170)
            src = im.crop((mg, 0, 1920 - mg, 1080)) if mg else im
            k = 1000 / src.width
            spr = framed(src.resize((1000, int(1080 * k)), Image.BILINEAR))
            place(c, spr, W / 2, CY, r if m["type"] != "video" else 1.0)
            self.vmap = (k, 960, 540)
        else:
            w, h = im.size; fit = min(1920 / w, 1080 / h); base = s["clip"]["scale"]["x"]
            dw, dh = w * fit * base, h * fit * base
            k = min(1000 / dw, 800 / dh)
            spr = im.resize((max(1, int(dw * k)), max(1, int(dh * k))), Image.BILINEAR)
            spr = framed(spr, r=18, ow=0) if True else spr
            place(c, spr, W / 2, CY, r)
            cx16 = 960 + s["clip"]["transform"]["x"] * 960; cy16 = 540 - s["clip"]["transform"]["y"] * 540
            self.vmap = (k, cx16, cy16)
        ov = seg_at(OV, t)
        if ov:
            om = MAT[ov["material_id"]]; oi = still_img(om["path"]); w, h = oi.size
            fit = min(1920 / w, 1080 / h); sc = ov["clip"]["scale"]["x"] * kf_ratio(ov, t)
            k, cx16, cy16 = self.vmap
            k = min(k, 0.95)
            px = 960 + ov["clip"]["transform"]["x"] * 960; py = 540 - ov["clip"]["transform"]["y"] * 540
            sx = W / 2 + (px - cx16) * k; sy = CY + (py - cy16) * k
            ow_ = w * fit * sc * k
            sx = min(max(sx, ow_ / 2 + 20), W - ow_ / 2 - 20)
            place(c, oi, sx, sy, (w * fit * sc * k) / w, rot=ov["clip"].get("rotation", 0) * -1)

# ---------- header ----------
def wrap2(s):
    if len(s) <= 16: return s
    mid = len(s) // 2; sp = [i for i, ch in enumerate(s) if ch == " "]
    if not sp: return s
    i = min(sp, key=lambda k: abs(k - mid)); return s[:i] + chr(10) + s[i + 1:]

def draw_header(c, tl, hook):
    big = text(wrap2(hook), 128, YEL, stroke=13, stroke_fill=(10, 10, 30), shadow=9)
    if big.width > 1000:
        big = big.resize((1000, int(big.height * 1000 / big.width)), Image.LANCZOS)
    x = min(1, max(0, (tl - 2.3) / 0.35)); e = 1 - (1 - x) ** 3
    sc = (1 - e) * 1.0 + e * 0.5
    pop = min(1, tl / 0.25); sc *= (0.6 + 0.4 * pop) if tl < 0.25 else 1
    y = (1 - e) * 330 + e * 245
    place(c, big, W / 2, y, sc)

def draw_brand(c):
    place(c, pill("ASK HABIBI", 30, fill=NAVY, tc=YEL, shadow=0, ow=4), 150, 120)

# ---------- audio ----------
def audio_for(a, b, outwav):
    ins, filt, n = [], [], 0
    segs = []
    for tr in AUDIO_TRACKS:
        segs += tr["segments"]
    segs += [s for s in MAIN if MAT[s["material_id"]]["type"] == "video" and s.get("volume", 0) > 0.01 and MAT[s["material_id"]].get("has_audio")]
    for s in segs:
        st, en = span(s)
        o0, o1 = max(a, st), min(b, en)
        if o1 - o0 < 0.02: continue
        src = (s.get("source_timerange") or {}).get("start", 0) / 1e6 + (o0 - st)
        ins += ["-ss", f"{src:.3f}", "-t", f"{o1 - o0:.3f}", "-i", MAT[s["material_id"]]["path"]]
        dl = int((o0 - a) * 1000)
        filt.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={s.get('volume', 1.0):.3f},adelay={dl}|{dl}[a{n}]")
        n += 1
    fc = ";".join(filt) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:duration=longest,atrim=0:{b - a:.3f},apad=whole_dur={b - a:.3f},alimiter=limit=0.95[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "2", outwav], check=True)

# ---------- end card (CTA) ----------
CTA_DIR = OUT + "cta/"                       # optional episode-specific lines: cta/part1.mp3 ...
CTA_LIB = B + "_cta_library/"                 # generic lines recorded ONCE, reused by every episode
CTA_VARIANT = "A"                             # switch to "B" on alternate episodes so it doesn't get repetitive
CTA_VERB = "SUBSCRIBE"                        # on-screen verb (use "FOLLOW" for TikTok/Reels renders)
LIB = B + "_music_library/"
GENERIC_CTA = {   # file stem -> exact recorded text (shown as captions on the end card)
    "cta_to_part2_A": "Part two is already on my profile. Subscribe, so the next one finds you.",
    "cta_to_part3_A": "Part three is waiting on my profile. Go check it, then subscribe.",
    "cta_to_part4_A": "Part four is on my profile. Subscribe for the rest.",
    "cta_to_part5_A": "Part five is on my profile. Subscribe so you don't miss it.",
    "cta_full_video_A": "That's the short version. The full video is on my channel. Subscribe, and send me your next midnight question.",
    "cta_to_part2_B": "This is only part one. Part two is on my profile. Subscribe, then go watch it.",
    "cta_to_part3_B": "It gets deeper. Part three is on my profile. Subscribe.",
    "cta_to_part4_B": "Don't stop here. Part four is on my profile. Subscribe for the rest.",
    "cta_to_part5_B": "One part left. Part five is on my profile. Subscribe so you catch it.",
    "cta_full_video_B": "Want the full answer? It's on my channel. Subscribe, so the next midnight question finds you.",
}
def _find(stem, folder):
    for ext in (".mp3", ".wav", ".m4a"):
        f = folder + stem + ext
        if os.path.exists(f): return f
    return None
def cta_pick(part, last):
    """-> (audio file or None, caption text or None). Episode line wins, else the generic library line."""
    f = _find(f"part{part}", CTA_DIR)
    if f: return f, None
    stem = (f"cta_full_video_{CTA_VARIANT}" if last else f"cta_to_part{part + 1}_{CTA_VARIANT}")
    f = _find(stem, CTA_LIB)
    return (f, GENERIC_CTA.get(stem)) if f else (None, None)
def cta_file(part, last=False):
    return cta_pick(part, last)[0]

def dur_of(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip() or 0)

def endcard_audio(part, dur, outwav, last=False):
    ins = ["-ss", "0", "-t", f"{dur:.2f}", "-i", LIB + "Daily Beetle.mp3", "-i", B + "1st video/claude_sfx/sparkle.wav"]
    fc = ("[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.20,afade=t=in:d=0.15,"
          f"afade=t=out:st={max(0.1, dur - 0.9):.2f}:d=0.9[m];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.35[s]")
    mix = "[m][s]"; n = 2
    cf = cta_file(part, last)
    if cf:
        ins += ["-i", cf]; fc += ";[2:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=250|250[v]"; mix += "[v]"; n = 3
    fc += f";{mix}amix=inputs={n}:normalize=0:duration=first,atrim=0:{dur:.2f},alimiter=limit=0.95[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "2", outwav], check=True)

def draw_endcard(c, t, part, last, cta_text=None, dur=2.8):
    from gfxlib import pose
    k = min(1, t / 0.35); e = 1 - (1 - k) ** 3
    if last:
        l1, l2, l3 = "FULL VIDEO", "ON MY CHANNEL", f"{CTA_VERB} FOR MORE"
    else:
        l1, l2, l3 = f"PART {part + 1}", "IS ON MY PROFILE", f"{CTA_VERB} FOR PART {part + 2}" if part + 2 <= LAST_PART else f"{CTA_VERB} FOR MORE"
    big = text(l1, 230, YEL, stroke=16, stroke_fill=(10, 10, 30), shadow=12); fit = min(1.0, 980 / big.width)
    place(c, big, W / 2, 700, (0.4 + 0.6 * e) * fit)
    place(c, text(l2, 96, WHITE, stroke=11, stroke_fill=(10, 10, 30), shadow=8), W / 2, 900, alpha=e)
    k2 = min(1, max(0, (t - 0.45) / 0.3))
    place(c, pill(l3, 54, fill=YEL, tc=NAVY), W / 2, 1060, 0.5 + 0.5 * (1 - (1 - k2) ** 3), alpha=k2)
    # arrow + Batata pointing toward the profile avatar (bottom-left in the Shorts UI)
    bob = math.sin(t * 9) * 10
    ar = Image.new("RGBA", (260, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(ar)
    d.polygon([(200, 30), (230, 60), (95, 195), (140, 195), (140, 235), (25, 235), (25, 120), (65, 120), (65, 165)], fill=YEL + (255,), outline=(10, 10, 30, 255), width=8)
    place(c, ar, 250 + bob * 0.4, 1330 + bob * 0.4, alpha=e)
    place(c, pose("Batata", "point", 330, flip=True), 760, 1330 + math.sin(t * 3) * 6, alpha=e)
    if cta_text:
        words = cta_text.split(); n = max(1, int(len(words) * min(1, (t - 0.25) / max(0.5, dur - 0.6))))
        line = " ".join(words[max(0, n - 4):n]).upper()
        if line: place(c, text(line, 64, WHITE, stroke=8, stroke_fill=(10, 10, 30)), W / 2, 1180)

# ---------- render ----------
def render_short(name, ranges, hook, part=1, cta_text=None):
    """ranges: list of (tl_start, tl_end)."""
    wavs = []
    for i, (a, b) in enumerate(ranges):
        w = f"short_{name}_{i}.wav"; audio_for(a, b, w); wavs.append(w)
    last = part == LAST_PART
    cf, lib_text = cta_pick(part, last)
    if lib_text: cta_text = lib_text
    ec_dur = max(2.8, dur_of(cf) + 0.7) if cf else 2.8
    ew = f"short_{name}_end.wav"; endcard_audio(part, ec_dur, ew, last); wavs.append(ew)
    lst = f"short_{name}_list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(w)}'\n" for w in wavs))
    aw = f"short_{name}_audio.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af", "afade=t=out:st=%.2f:d=0.3" % (sum(b - a for a, b in ranges) + ec_dur - 0.3), aw], check=True)
    out = OUT + name + ".mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", aw, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    tl = 0.0; vis = Visual()
    for a, b in ranges:
        n = int(round((b - a) * FPS)); vis.rseg = None
        for i in range(n):
            t = a + i / FPS
            c = bg_at(t)
            vis.frame(c, t)
            draw_captions(c, t)
            draw_header(c, tl + i / FPS, hook)
            draw_brand(c)
            p.stdin.write(c.convert("RGB").tobytes())
        tl += (b - a)
    for i in range(int(round(ec_dur * FPS))):
        t = i / FPS; c = bg_at(ranges[-1][1] + t)
        draw_endcard(c, t, part, last, cta_text if cf else None, ec_dur)
        draw_header(c, tl + t, hook); draw_brand(c)
        p.stdin.write(c.convert("RGB").tobytes())
    if vis.reader: vis.reader.close()
    p.stdin.close(); p.wait()
    print("rendered", out, round(tl, 2), "s", flush=True)

OFF = 3.45
T = lambda s: s if s < 9.05 else s + OFF
SHORTS = {  # name: (ranges, hook, part, ElevenLabs CTA line)
    "part1_why_3am": ([(0.0, T(17.35)), (T(123.10), T(132.25))], "WHY DOES THIS HAPPEN?!", 1,
                      "That's just the surface. Part two is already on my profile. Follow, so part three finds you at three a.m."),
    "part2_bad_memories_stick": ([(T(40.32), T(69.75))], "WHY BAD MEMORIES STICK", 2,
                      "And your brain has a second trick. Part three is on my profile. Go check it, then follow."),
    "part3_meeting_you_cant_leave": ([(T(9.35), T(12.10)), (T(70.16), T(88.05))], "THE MEETING YOU CAN'T LEAVE", 3,
                      "So how do you end that meeting? Sleep. Part four is on my profile. Follow for the rest."),
    "part4_karaoke_cringe": ([(T(88.44), T(120.62))], "SLEEP = LESS CRINGE?", 4,
                      "There's one thing that actually helps. It's part five, on my profile. Follow so you don't miss it."),
    "part5_stuck_on_replay": ([(T(150.10), T(171.40))], "STUCK ON REPLAY? TRY THIS", 5,
                      "That's the full answer. The whole video is on my channel. Follow, and send me your next midnight question."),
}

LAST_PART = max(v[2] for v in SHORTS.values())

if __name__ == "__main__":
    want = sys.argv[1:]
    if want and want[0] == "qa":
        name = want[1]; ranges, hook = SHORTS[name][:2]
        for tt in [0.5, 3.0]:
            a = ranges[0][0] + tt; c = bg_at(a); v = Visual(); v.frame(c, a); draw_captions(c, a); draw_header(c, tt, hook); draw_brand(c)
            if v.reader: v.reader.close()
            c.convert("RGB").save(f"qa_{name}_{tt}.png")
        sys.exit()
    for name, (ranges, hook, part, line) in SHORTS.items():
        if want and not any(w in name for w in want): continue
        render_short(name, ranges, hook, part, line)
