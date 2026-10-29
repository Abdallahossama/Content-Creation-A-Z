"""Vertical teaser Shorts cut from the long Alcatraz edit (1080x1920). Each one: hook text on top, the Case File frame in the
middle (blur fill behind), word-by-word captions, then an end card pointing to the full video + one spoken CTA line.
  python teasers.py qa <name> <t..>  |  python teasers.py render <name>  |  python teasers.py all"""
import sys, os, json, subprocess, re
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
exec(open("D:/why habibi/_newchannel/01_alcatraz/render_alcatraz.py", encoding="utf-8").read().split("if __name__")[0])
VW, VH = 1080, 1920
TZ = ROOT + "teasers/"; os.makedirs(TZ + "build", exist_ok=True)
CTA_WAV = ROOT + "vo/cta/vo_chatterbox.wav"; END_LEN = round(0.5 + sf.info(CTA_WAV).duration + 1.0, 2)      # whole CTA line + a beat
TEASERS = {
 "T1_dummy": dict(a=0.0, b=T[9] - 0.15, hook=("IT WASN'T", "A MAN."), sub="ALCATRAZ  ·  JUNE 12, 1962  ·  7:20 AM"),
 "T2_noise": dict(a=T[95] - 0.08, b=T[105] - 0.25, hook=("THE 10:30", "NOISE"), sub="ALCATRAZ  ·  JUNE 11, 1962"),
 "T3_letter": dict(a=T[167] - 0.08, b=T[175] - 0.25, hook=("51 YEARS", "LATER..."), sub="A LETTER SIGNED JOHN ANGLIN"),
}
TITLE = "What the FBI Found When 3 Men Vanished From Alcatraz"

def chunks(a, b):
    ws = [w for w in WORDS if a <= w["s"] + LEAD < b]; out = []; cur = []
    for w in ws:
        cur.append(w)
        if len(cur) == 3 or w["w"].strip().endswith((",", ".", "?", "!")): out.append(cur); cur = []
    if cur: out.append(cur)
    return [(c[0]["s"] + LEAD, c[-1]["e"] + LEAD + 0.15, " ".join(x["w"].strip() for x in c).strip(",.")) for c in out]

def vframe(name, t):
    cfg = TEASERS[name]; dur = cfg["b"] - cfg["a"]
    c = Image.new("RGBA", (VW, VH), INK + (255,))
    if t < dur:
        big = frame(cfg["a"] + t).convert("RGB")
        bg = big.resize((int(1920 * VH / 1080), VH), Image.BILINEAR).crop(((int(1920 * VH / 1080) - VW) // 2, 0, (int(1920 * VH / 1080) - VW) // 2 + VW, VH))
        bg = bg.filter(ImageFilter.GaussianBlur(28)); bg = Image.fromarray((np.asarray(bg, np.float32) * 0.35).astype(np.uint8))
        c.paste(bg, (0, 0))
        fg = big.resize((1440, 810), Image.LANCZOS).crop((180, 0, 1260, 810)); c.paste(fg, (0, 560))
        d = ImageDraw.Draw(c); d.rectangle((0, 556, VW, 560), fill=RED); d.rectangle((0, 1370, VW, 1374), fill=RED)
        L.text(c, cfg["hook"][0], VW / 2, 215, 150, BONE, COND); L.text(c, cfg["hook"][1], VW / 2, 365, 150, RED if cfg["hook"][1] != "NOISE" else BONE, COND)
        L.typewriter(c, cfg["sub"], t, 0.0, VW / 2, 490, size=34, fill=STEEL, cps=60, anchor="mm", cursor=False)
        for s0, s1, txt in CAPS[name]:
            tt = cfg["a"] + t
            if s0 <= tt < s1:
                d.text((VW / 2, 1540), txt, font=L.font(COND, 92), fill=BONE, anchor="mm", stroke_width=8, stroke_fill=(8, 8, 8)); break
        L.text(c, "the LAST HOURS", VW / 2, 1830, 40, STEEL, COND)
    else:
        te = t - dur; u = ease(te / 0.4)
        L.typewriter(c, "THE FULL FILE", te, 0.0, VW / 2, 640, size=96, cps=18, anchor="mm", cursor=False)
        if te > 0.6:
            d = ImageDraw.Draw(c); y = 760 + 12 * np.sin(te * 4); d.polygon([(VW / 2 - 40, y), (VW / 2 + 40, y), (VW / 2, y + 50)], fill=RED)
        for i, ln in enumerate(["What the FBI Found When", "3 Men Vanished From Alcatraz"]):
            L.text(c, ln, VW / 2, 930 + i * 80, 62, BONE, SER, alpha=ease((te - 0.5) / 0.4))
        L.rule(c, VW / 2 - 300, VW / 2 + 300, 1060, te, 0.9, width=6)
        L.text(c, "the", VW / 2, 1300, 54, STEEL, SER, alpha=u); L.text(c, "LAST HOURS", VW / 2, 1400, 130, BONE, COND, alpha=u)
        L.text(c, "Link below  ·  @TheLastHoursDocs", VW / 2, 1520, 40, STEEL, TYPE, alpha=ease((te - 1.0) / 0.4))
    return c
CAPS = {n: chunks(c["a"], c["b"]) for n, c in TEASERS.items()}

def audio(name):
    cfg = TEASERS[name]; sr = 48000
    mix, s = sf.read(B + "mix.wav", dtype="float32", always_2d=True); mix = mix.mean(1)
    seg = mix[int(cfg["a"] * s): int(cfg["b"] * s)].copy(); f = int(0.25 * s); seg[-f:] *= np.linspace(1, 0, f)
    if s != sr: seg = np.interp(np.arange(int(len(seg) * sr / s)) / sr, np.arange(len(seg)) / s, seg).astype(np.float32)
    cta, cs = sf.read(CTA_WAV, dtype="float32", always_2d=True); cta = cta.mean(1)
    if cs != sr: cta = np.interp(np.arange(int(len(cta) * sr / cs)) / sr, np.arange(len(cta)) / cs, cta).astype(np.float32)
    vr = np.sqrt(np.mean(seg[np.abs(seg) > 0.02] ** 2)) if np.any(np.abs(seg) > 0.02) else 0.1
    cta = cta / (np.sqrt(np.mean(cta[np.abs(cta) > 0.01] ** 2)) + 1e-9) * vr
    end = np.zeros(int(END_LEN * sr), np.float32); end[int(0.5 * sr): int(0.5 * sr) + len(cta)] += cta[: len(end) - int(0.5 * sr)]
    m, ms = sf.read(MUS + "Thunder Dreams.mp3", dtype="float32", always_2d=True); m = m.mean(1)[int(30 * ms): int((30 + END_LEN) * ms)]
    m = np.interp(np.arange(len(end)) / sr, np.arange(len(m)) / ms, m).astype(np.float32); m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9) * vr * 10 ** (-20 / 20)
    m *= np.minimum(1, np.minimum(np.arange(len(m)) / (0.3 * sr), (len(m) - np.arange(len(m))) / (0.8 * sr))); end += m
    hit = sf.read(SFXD + "hit_cinematic_deep_impact.mp3", dtype="float32", always_2d=True)[0].mean(1); hit = hit / (np.max(np.abs(hit)) + 1e-9) * vr * 1.5
    end[: min(len(hit), len(end))] += np.interp(np.arange(min(len(hit), len(end))), np.arange(len(hit)), hit)[: len(end)] * 0.6
    y = np.concatenate([seg, end]); y = y / (np.max(np.abs(y)) + 1e-9) * 0.9
    sf.write(TZ + f"build/{name}_raw.wav", y, sr, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(TZ + f"build/{name}_raw.wav", TZ + f"build/{name}.wav", target=-14, tp=-1)
    return len(y) / sr

def render(name):
    total = audio(name); n = int(total * FPS); out = TZ + f"TheLastHours_Short_{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-", "-i", TZ + f"build/{name}.wav",
                          "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                          "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(n): p.stdin.write(vframe(name, f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("wrote", out, round(total, 1), "s", flush=True)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "qa":
        name = sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]; tiles = [vframe(name, t).convert("RGB").resize((270, 480)) for t in ts]
        S = Image.new("RGB", (len(tiles) * 280, 500), (20, 20, 20))
        for i, im in enumerate(tiles): S.paste(im, (i * 280, 0))
        S.save(TZ + f"build/qa_{name}.png"); print(TZ + f"build/qa_{name}.png")
    elif m == "render": render(sys.argv[2])
    elif m == "all":
        for n in TEASERS: render(n)
