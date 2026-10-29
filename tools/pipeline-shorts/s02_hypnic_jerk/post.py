"""Short #2 finishing: Blender frames + overlays (logo top-left, question title for the first seconds, 7 IN 10 and
HYPNIC JERK pops, 1-3 word white captions) + audio (local Chatterbox VO as float, quiet CC-BY music, soft pops/creaks,
limiter master to -16 LUFS like Short #1's LOUDER version).
  python post.py test t1 t2 ...     overlay stills -> build/post_test.png
  python post.py audio              -> build/mix.wav
  python post.py final              -> export/Ask_Habibi_Short02_HypnicJerk.mp4"""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "D:/why habibi/shorts/s02_hypnic_jerk/"; FR = ROOT + "frames/"; B = ROOT + "build/"; E = ROOT + "export/"
os.makedirs(B, exist_ok=True); os.makedirs(E, exist_ok=True)
W, H, FPS = 1080, 1920, 30
RUBIK = "D:/why habibi/_style_kit/fonts/Rubik-Bold.ttf"; IMPACT = "C:/Windows/Fonts/impact.ttf"; EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
BEATS = json.load(open("D:/why habibi/_pipeline/shorts/s02_hypnic_jerk/beats.json")); T = BEATS["t"]; END = BEATS["end"]
WORDS = [w for s in json.load(open(ROOT + "vo/vo_words.json", encoding="utf-8")) for w in s["words"]]
NF = int(round(END * FPS))
YEL = (255, 196, 26)

def font(p, s): return ImageFont.truetype(p, int(s))
def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
POP = [0.0, 0.55, 1.14, 1.05, 0.98, 1.0]
def popk(t, t0):
    f = int((t - t0) * FPS); return 0.0 if f < 0 else (POP[f] if f < len(POP) else 1.0)

def outlined(text, size, fill=(255, 255, 255), f=RUBIK, stroke=9, emoji=None):
    fo = font(f, size); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); bb = d0.textbbox((0, 0), text, font=fo, stroke_width=stroke)
    ew = 0; em = None
    if emoji:
        fe = font(EMOJI, 109); em = Image.new("RGBA", (160, 140), (0, 0, 0, 0)); ImageDraw.Draw(em).text((5, 5), emoji, font=fe, embedded_color=True)
        em = em.crop(em.getbbox()); k = size * 1.05 / em.height; em = em.resize((int(em.width * k), int(em.height * k)), Image.LANCZOS); ew = em.width + 18
    im = Image.new("RGBA", (bb[2] - bb[0] + ew + 30, max(bb[3] - bb[1], em.height if em else 0) + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((15 - bb[0] + 5, 15 - bb[1] + 7), text, font=fo, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    d.text((15 - bb[0], 15 - bb[1]), text, font=fo, fill=fill + (255,), stroke_width=stroke, stroke_fill=(12, 10, 10, 255))
    if em: im.alpha_composite(em, (im.width - em.width - 10, (im.height - em.height) // 2))
    return im

def put(c, spr, cx, cy, k=1.0):
    if k <= 0.01: return
    s = spr if abs(k - 1) < 0.01 else spr.resize((max(1, int(spr.width * k)), max(1, int(spr.height * k))), Image.BILINEAR)
    c.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def make_logo():
    lg = Image.open("D:/why habibi/_style_kit/brand/logo_horizontal.png").convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((300, int(300 * lg.height / lg.width)), Image.LANCZOS)
    out = Image.new("RGBA", (lg.width + 30, lg.height + 30), (0, 0, 0, 0)); s = Image.new("RGBA", lg.size, (0, 0, 0, 0)); s.putalpha(lg.split()[3].point(lambda v: int(v * 0.45)))
    out.alpha_composite(s, (12, 14)); out = out.filter(ImageFilter.GaussianBlur(6)); out.alpha_composite(lg, (8, 8)); return out
LOGO = make_logo()
TITLE = [outlined("WHY YOU", 104), outlined("JOLT AWAKE", 104, emoji="😨")]
SEVEN = outlined("7 IN 10", 210, fill=YEL, f=IMPACT, stroke=12)
SEVEN2 = outlined("people get it", 64)
HYPNIC = outlined("HYPNIC JERK", 120, fill=YEL, f=IMPACT, stroke=11)

def caption_chunks():
    out, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w); s = w["w"].strip()
        if len(cur) >= 3 or s.endswith((",", ".", "?", "!")): out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        t1 = out[i + 1][0]["s"] if i + 1 < len(out) else c[-1]["e"] + 0.5
        txt = " ".join(w["w"].strip() for w in c).replace("Seven in 10", "7 in 10").replace("10", "10")
        res.append((c[0]["s"] - 0.05, min(t1, c[-1]["e"] + 0.5), txt.strip(",.")))
    return res
CAPS = caption_chunks(); CAP_IMG = {}

def frame(t, img):
    c = img.convert("RGBA")
    if t < T["seven"] - 0.05:                                                    # the question, frame 1 -> "seven"
        put(c, TITLE[0], W / 2, 330); put(c, TITLE[1], W / 2, 450)
    if T["seven"] <= t < T["hypnic"] - 0.1:
        put(c, SEVEN, W / 2, 400, popk(t, T["seven"])); put(c, SEVEN2, W / 2, 545, popk(t, T["seven"] + 0.15))
    if T["hypnic"] <= t < T["drift"] - 0.1:
        put(c, HYPNIC, W / 2, 420, popk(t, T["hypnic"] + 0.25))
    c.alpha_composite(LOGO, (26, 92))
    for t0, t1, s in CAPS:
        if t0 <= t < t1:
            if s not in CAP_IMG: CAP_IMG[s] = outlined(s, 82, stroke=9)
            put(c, CAP_IMG[s], W / 2, 1390); break
    return c.convert("RGB")

def frame_path(i):
    p = FR + f"f_{i + 1:05d}.png"
    return p if os.path.exists(p) else None

# ------------------------------------------------------------------------------------------- audio
SFXD = "D:/why habibi/_style_kit/sfx/"
SFX = [("creak", 0.0, -16), ("pop", T["seven"], -18), ("pop", T["hypnic"] + 0.25, -18), ("creak", T["jumpword"], -14)] + \
      [("pop", T["theory"] + 0.35 + k * 0.25, -20) for k in range(3)] + [("pop", T["stress"], -18), ("pop", T["caffeine"], -18)]
def audio():
    import soundfile as sf
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    SR = 48000
    def dec(path):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).copy()
    vo = dec(ROOT + "vo/s02_vo_chatterbox.wav"); n = int((END + 0.3) * SR); out = np.zeros(n, np.float32); out[:min(n, len(vo))] += vo[:n]
    vrms = np.sqrt(np.mean(vo[np.abs(vo) > 1e-3] ** 2) + 1e-12)
    mus = dec("D:/why habibi/_music_library/Dream Culture.mp3")[:n]; mus = np.pad(mus, (0, max(0, n - len(mus))))
    fade = np.ones(n, np.float32); fl = int(0.5 * SR); fade[:fl] = np.linspace(0.3, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
    out += mus * fade * (vrms / (np.sqrt(np.mean(mus ** 2)) + 1e-12)) * 10 ** (-20 / 20)
    for name, t0, db in SFX:
        s = dec(SFXD + name + ".wav")[: int(1.2 * SR)]; srms = np.sqrt(np.mean(s[np.abs(s) > 1e-4] ** 2)) + 1e-12
        i0 = int(max(t0, 0) * SR); j = min(n, i0 + len(s)); out[i0:j] += s[: j - i0] * (vrms / srms) * 10 ** (db / 20)
    k = 0.89 / max(1e-6, np.abs(out).max()); sf.write(B + "mix_raw.wav", out * k, SR, subtype="FLOAT")
    AM.master(B + "mix_raw.wav", B + "mix.wav", target=-16.0, tp=-1.0); print("audio", AM.measure(B + "mix.wav"))

def final():
    out = E + "Ask_Habibi_Short02_HypnicJerk.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    last = None; missing = 0
    for i in range(NF):
        fp = frame_path(i)
        if fp: last = Image.open(fp).convert("RGB")
        else: missing += 1
        p.stdin.write(frame(i / FPS, last).tobytes())
    p.stdin.close(); p.wait(); print("WROTE", out, "missing frames:", missing)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "test":
        ims = []
        for t in sys.argv[2:]:
            i = int(float(t) * FPS); fp = frame_path(i) or frame_path(0); ims.append(frame(float(t), Image.open(fp)).resize((270, 480)))
        sheet = Image.new("RGB", (len(ims) * 276, 486), (20, 20, 20))
        for k, im in enumerate(ims): sheet.paste(im, (3 + k * 276, 3))
        sheet.save(B + "post_test.png"); print(B + "post_test.png")
    elif m == "audio": audio()
    elif m == "final": final()
