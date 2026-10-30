"""Re-brand a Last Hours long file that is already rendered/uploaded with "The File Keeper" (owner, 30 Oct 2026; repo docs/09):
  1. the 2.2 s channel stamp (~0:40-3:00) gets the round File Keeper mark (mark_v1_badge) left of "LAST HOURS"
  2. the silent ~75 % subscribe pill is covered by a File Keeper pill naming the NEXT file (mark_v3_folder + text), same slide
  3. the narration is cut right before its old end lines (stale "Next, I'm opening..." / "If you want the next file, subscribe.")
     and a new end card follows: blurred last frame, the red "THE FILE KEEPER" stamp (mark_v2_stamp), a "CASE CLOSED" slam,
     "NEXT FILE: <topic>", the end-screen boxes, and the File Keeper sign-off in the cloned voice (so_<key>.wav) over a music bed.
Times come from brand_times.json (each file's own render script: brand, subpop, the cut line). Output: _upload_queue_last_hours/branded/.
  uv run --no-project --with pillow --with numpy --with soundfile python brand_patch.py <key> [--qa]"""
import sys, os, json, subprocess, tempfile, shutil
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
NC = "D:/why habibi/_newchannel/"; sys.path.insert(0, NC)
import lastkit as L
from lastkit import W, H, FPS, INK, BONE, RED, STEEL, COND, TYPE, SER, ease
CTA = NC + "_cta/"; MK = NC + "brand/file_keeper/"; MUS = "D:/why habibi/_music_library/"; SFX = NC + "sfx/"
OUTD = "D:/why habibi/_upload_queue_last_hours/branded/"; os.makedirs(OUTD, exist_ok=True)
SR = 48000
NEXT = {"flannan": "SADDAM'S MEETING · 1979", "khuld": "THE ANDRÉE BALLOON · 1897", "andree": "GADDAFI'S STADIUM · 1984",
        "gaddafi": "FLIGHT 19 · 1945", "flight19": "USS CYCLOPS · 1918", "cyclops": "EGYPTAIR 990 · 1999",
        "egyptair": "GÖRING'S LAST NIGHT · 1946", "goering": "THE BATTLE OF ALCATRAZ · 1946", "alcatraz46": "A NEW FILE EVERY WEEK"}
PILL = {k: "NEXT FILE: " + v.split(" · ")[0] for k, v in NEXT.items()}; PILL["alcatraz46"] = "A NEW FILE EVERY WEEK"
END_MUSIC = "Promises to Keep.mp3"
STAMP_MARK, PILL_MARK, END_MARK = "noir_badge", "noir_folder", "noir_seal"     # owner 30 Oct: the noir set (flat v1 = tiny watermark only)

def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def load(p, ch=2, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", p] + (["-t", str(t)] if t else []) + ["-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, ch).copy()
def rms(a): v = a[np.abs(a).max(1) > 1e-4] if a.ndim > 1 else a; return float(np.sqrt(np.mean(v ** 2))) if len(v) else 1e-6

MARK = {}
def mark(name, size):
    k = (name, size)
    if k not in MARK: MARK[k] = Image.open(MK + f"mark_{name}.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    return MARK[k]

# ---------------------------------------------------------------- 1 + 2: overlay frame sequences
def stamp_image(u):
    """the round mark for the 2.2 s brand stamp at time u (same envelope as the renderers' stamp), on a 300 x 300 canvas"""
    m = mark(STAMP_MARK, 250); al = ease(u / 0.35) * ease((2.2 - u) / 0.35); s = 0.92 + 0.08 * ease(u / 0.35)
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); mm = m.resize((int(250 * s), int(250 * s)), Image.LANCZOS)
    a = np.asarray(mm, np.float32); a[..., 3] *= al; mm = Image.fromarray(a.astype(np.uint8))
    im.alpha_composite(mm, ((300 - mm.width) // 2, (300 - mm.height) // 2)); return im
STAMP_XY = (int(W / 2 - 560 - 150), int(H / 2 - 150))                      # left of the centred "LAST HOURS"
def stamp_frames(folder):
    for i in range(int(2.2 * FPS)): stamp_image(i / FPS).save(os.path.join(folder, f"s{i:03d}.png"))

def pill_image(u, text):
    """the File Keeper subscribe pill at time u of its 4 s (ink pill, case-file mark, 'SUBSCRIBE · <text>'), covers the old red pill"""
    fs = L.font(COND, 46); w = max(760, int(120 + fs.getlength("SUBSCRIBE  ·  " + text) + 40)); m = mark(PILL_MARK, 84)
    k = ease(u / 0.4) * ease((4.0 - u) / 0.4); x = 30 - (1 - k) * (w + 40); al = min(1.0, 2.2 * k)
    im = Image.new("RGBA", (w + 80, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, 8, x + w, 104), 26, fill=(14, 14, 16, int(250 * al)), outline=RED + (int(255 * al),), width=4)
    mm = m.copy(); a = np.asarray(mm, np.float32); a[..., 3] *= al; im.alpha_composite(Image.fromarray(a.astype(np.uint8)), (int(x + 18), 14))
    d.text((x + 118, 56), "SUBSCRIBE", font=fs, fill=RED + (int(255 * al),), anchor="lm")
    d.text((x + 118 + fs.getlength("SUBSCRIBE "), 56), "·", font=fs, fill=STEEL + (int(255 * al),), anchor="lm")
    d.text((x + 118 + fs.getlength("SUBSCRIBE  ·  "), 56), text, font=fs, fill=BONE + (int(255 * al),), anchor="lm")
    return im
PILL_Y = 104
PILL_Y_OLD40 = {"flannan", "andree", "egyptair"}                             # these renders drew the old pill at y 40-112, the rest at 120-192
def pill_y(key): return 32 if key in PILL_Y_OLD40 else PILL_Y
def pill_frames(folder, text):
    for i in range(120): pill_image(i / 30.0, text).save(os.path.join(folder, f"p{i:03d}.png"))

# ---------------------------------------------------------------- 3: the new end card
BOXES = [(110, 600, 750, 960), (1170, 600, 1810, 960)]; CIRCLE = (835, 655, 1085, 905)
CAPF = {}
def caption_chunks(words):
    """[(start, end, word)] -> chunks of <= 6 words / 30 chars, broken at punctuation (the renderers' rule)"""
    out, ch = [], []
    for k, (s0, s1, w) in enumerate(words):
        ch.append((s0, w)); txt = " ".join(x for _, x in ch)
        if len(ch) >= 6 or len(txt) >= 30 or w[-1] in ".,?!;:" or k == len(words) - 1: out.append(ch); ch = []
    return [(c[0][0] - 0.05, (out[j + 1][0][0] - 0.05) if j + 1 < len(out) else c[-1][0] + 2.2, c) for j, c in enumerate(out)]
def draw_caps(c, t, chunks):
    cur = next((chk for t0, t1, chk in chunks if t0 <= t < t1), None)
    if not cur: return
    if "f" not in CAPF: CAPF["f"] = L.font(COND, 62)
    f = CAPF["f"]; words = [w for _, w in cur]; sp = f.getlength(" "); ws = [f.getlength(w) for w in words]; tw = sum(ws) + sp * (len(ws) - 1)
    x = W / 2 - tw / 2; lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); y = 996
    d.rounded_rectangle((x - 26, y - 44, x + tw + 26, y + 42), 14, fill=(0, 0, 0, 120))
    for k, ((tm, w), wl) in enumerate(zip(cur, ws)):
        nxt = cur[k + 1][0] if k + 1 < len(cur) else tm + 0.6
        d.text((x, y), w, font=f, fill=((255, 204, 0) if tm <= t < nxt else (255, 255, 255)) + (255,), anchor="lm", stroke_width=5, stroke_fill=(0, 0, 0, 255)); x += wl + sp
    c.alpha_composite(lay)

def end_frame(bg_sharp, bg_blur, t, topic, caps=None):
    c = Image.blend(bg_sharp, bg_blur, ease(t / 0.6)).convert("RGBA")
    if t >= 0.15:                                                        # the red File Keeper stamp slams in
        u = ease((t - 0.15) / 0.18); s = 1.45 - 0.45 * u; st = mark(END_MARK, int(330 * s)).rotate(-4, resample=Image.BICUBIC)
        a = np.asarray(st, np.float32); a[..., 3] *= min(1.0, u * 1.5); st = Image.fromarray(a.astype(np.uint8))
        c.alpha_composite(st, (int(W / 2 - st.width / 2), int(245 - st.height / 2)))
    if t >= 0.4:                                                         # CASE CLOSED
        u = ease((t - 0.4) / 0.15); f = L.font(COND, 70); tw = f.getlength("CASE CLOSED")
        blk = Image.new("RGBA", (int(tw + 60), 104), (0, 0, 0, 0)); bd = ImageDraw.Draw(blk)
        bd.rectangle((0, 0, blk.width, blk.height), fill=RED + (int(235 * u),)); bd.text((blk.width / 2, 52), "CASE CLOSED", font=f, fill=BONE + (int(255 * u),), anchor="mm")
        blk = blk.rotate(7, expand=True, resample=Image.BICUBIC); sc = 1.3 - 0.3 * u; blk = blk.resize((int(blk.width * sc), int(blk.height * sc)), Image.BICUBIC)
        c.alpha_composite(blk, (int(W / 2 + 120 - blk.width / 2), int(345 - blk.height / 2)))
    if t >= 0.9:
        L.text(c, "NEXT FILE", W / 2, 462, 34, STEEL, TYPE, alpha=ease((t - 0.9) / 0.3))
        L.typewriter(c, topic, t, 1.0, W / 2, 522, size=72 if len(topic) < 28 else 60, fill=BONE, cps=24, anchor="mm", cursor=False)
    if t >= 1.4:
        al = int(255 * ease((t - 1.4) / 0.4)); d = ImageDraw.Draw(c)
        for b in BOXES: d.rectangle(b, outline=STEEL + (al,), width=3)
        d.ellipse(CIRCLE, outline=STEEL + (al,), width=3)
    if caps: draw_caps(c, t, caps)                                       # the sign-off, word by word (sound-off viewers)
    elif caps is None: L.text(c, "the LAST HOURS  ·  @TheLastHoursDocs", W / 2, 1030, 30, STEEL, TYPE, alpha=ease((t - 1.6) / 0.4))
    # caps == []: the caller (a renderer) draws its own captions there
    return c

def end_audio(n, ref, so):
    """music bed (fades in, dips 7 dB under the sign-off), the stamp thuds, the sign-off at 0.7 s"""
    y = np.zeros((n, 2), np.float32)
    mus = load(MUS + END_MUSIC, ss=20.0, t=n / SR + 0.1)[:n]; mus = mus / max(rms(mus), 1e-6) * ref * 10 ** (-15 / 20)
    g = np.ones(n, np.float32); fi = int(1.0 * SR); g[:fi] = np.linspace(0, 1, fi); fo = int(2.5 * SR); g[-fo:] = np.linspace(1, 0, fo)
    i0 = int(0.7 * SR); L_ = len(so); lo = 10 ** (-7 / 20); r = int(0.3 * SR)
    d = np.ones(n, np.float32); a0, a1 = max(0, i0 - r), min(n, i0 + L_ + r); d[a0:a1] = lo; d[a0:a0 + r] = np.linspace(1, lo, r); d[a1 - r:a1] = np.linspace(lo, 1, r)
    y[: len(mus)] += mus * (g * d)[: len(mus), None]
    for name, t, db in (("metal_hammer_hit", 0.15, -16), ("hit_cinematic_deep_impact", 0.4, -14)):
        s = load(SFX + name + ".mp3"); s = s / (np.abs(s).max() + 1e-9) * ref * 3.2 * 10 ** (db / 20); j = int(t * SR); y[j:j + len(s)] += s[: n - j]
    y[i0:i0 + L_] += so[: n - i0]
    return y

def main():
    key = sys.argv[1]; qa = "--qa" in sys.argv
    if key == "alcatraz46": raise SystemExit("alcatraz46 is branded inside its own render (render_alcatraz46.py), not patched")
    R = json.load(open(CTA + "brand_times.json", encoding="utf-8"))[key]; src = R["src"]; cut = R["cut_t"] - 0.08
    sop = CTA + f"so_{key}.wav"
    if os.path.exists(sop): so, ssr = sf.read(sop, dtype="float32", always_2d=True); so = so.mean(1)
    elif qa: so, ssr = np.zeros(int(15 * SR), np.float32), SR                      # QA before the sign-off is voiced
    else: raise SystemExit("missing " + sop + " (run signoff_gen.py + signoff_pick.py)")
    if ssr != SR: so = np.interp(np.arange(int(len(so) * SR / ssr)) / SR, np.arange(len(so)) / ssr, so).astype(np.float32)
    caps = None
    if os.path.exists(CTA + f"so_{key}.json"):
        caps = caption_chunks([(w0 + 0.7, w1 + 0.7, w) for w0, w1, w in json.load(open(CTA + f"so_{key}.json", encoding="utf-8"))])
    a_tail = load(src, ss=max(0, cut - 4.0), t=3.6); ref = rms(a_tail)                          # voice + music level of the last spoken line
    so = so / max(rms(so[:, None].repeat(2, 1)), 1e-6) * ref * 0.95; so2 = np.stack([so, so], 1)
    end_len = round(max(20.0, 0.7 + len(so) / SR + 4.5), 2); n_end = int(end_len * FPS)
    tmp = tempfile.mkdtemp(); bgp = os.path.join(tmp, "bg.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(cut - 0.1), "-i", src, "-frames:v", "1", bgp], check=True)
    bg_sharp = Image.open(bgp).convert("RGB").resize((W, H)); bg_blur = Image.blend(bg_sharp.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62)
    g = (np.clip((np.arange(H) - 700) / 300, 0, 1) ** 1.2 * 0.85)[:, None, None]                         # the burned-in caption band: darkened away
    bg_blur = Image.fromarray((np.asarray(bg_blur, np.float32) * (1 - g)).astype(np.uint8))
    if qa:
        ts = [0.3, 0.5, 1.2, 3.0, end_len - 1]; tiles = [end_frame(bg_sharp, bg_blur, t, NEXT[key], caps).convert("RGB").resize((480, 270)) for t in ts]
        S = Image.new("RGB", (480 * len(tiles), 270)); [S.paste(t, (i * 480, 0)) for i, t in enumerate(tiles)]; S.save(OUTD + f"qa_end_{key}.jpg"); print(OUTD + f"qa_end_{key}.jpg"); return
    # A: the original up to the cut, with the stamp mark and the new pill; its audio fades over the last 0.5 s
    sf_dir = os.path.join(tmp, "s"); pf_dir = os.path.join(tmp, "p"); os.makedirs(sf_dir); os.makedirs(pf_dir)
    stamp_frames(sf_dir); pill_frames(pf_dir, PILL[key])
    A = os.path.join(tmp, "A.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-framerate", str(FPS), "-i", os.path.join(sf_dir, "s%03d.png"), "-framerate", "30", "-i", os.path.join(pf_dir, "p%03d.png"),
                    "-filter_complex", f"[1:v]setpts=PTS+{R['brand_t']}/TB[s];[2:v]setpts=PTS+{R['subpop_t']}/TB[p];[0:v][s]overlay={int(W / 2 - 560 - 150)}:{int(H / 2 - 150)}:eof_action=pass[v1];[v1][p]overlay=0:{pill_y(key)}:eof_action=pass[v];"
                    f"[0:a]afade=t=out:st={cut - 0.5:.3f}:d=0.5[a]", "-map", "[v]", "-map", "[a]", "-t", f"{cut:.3f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", A], check=True)
    # B: the end card
    wav = os.path.join(tmp, "B.wav"); sf.write(wav, end_audio(int(end_len * SR), ref, so2), SR, subtype="FLOAT")
    B = os.path.join(tmp, "B.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                          "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", "-shortest", B], stdin=subprocess.PIPE)
    for f in range(n_end): p.stdin.write(end_frame(bg_sharp, bg_blur, f / FPS, NEXT[key], caps).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    lst = os.path.join(tmp, "l.txt"); open(lst, "w").write(f"file '{A}'\nfile '{B}'\n")
    out = OUTD + os.path.basename(src).replace(".mp4", "_FILEKEEPER.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{key}: {out}  cut {cut:.2f}s + end card {end_len}s = {dur(out):.2f}s (was {dur(src):.2f}s); stamp {R['brand_t']}s, pill {R['subpop_t']}s", flush=True)

if __name__ == "__main__":
    main()
