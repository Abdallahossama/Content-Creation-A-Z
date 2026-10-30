"""Vertical teaser Shorts (1080x1920) for Saddam / Gaddafi / Franklin, cut from each long edit, same layout as the Flight 19 and
Andree teasers: hook text on top, the Case File frame in the middle (blur fill behind), word-by-word captions, then an end card with
the long video's title + a spoken line that NAMES the long video (owner, 26 Oct: the Short -> long CTA must say which video).
  uv run --no-project --with pillow --with numpy --with soundfile python teasers_more.py qa <file> <name> <t..> | render <file> <name> | all <file>
  <file> = khuld | gaddafi | franklin | goering"""
import sys, os, re, json, subprocess, importlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
NC = "D:/why habibi/_newchannel/"
FILES = {
 "khuld": dict(dir="11_khuld_hall", mod="render_khuld", title=("Saddam Hussein Called a Meeting.", "66 Names Were Read Out."), teasers={
   "T1_the_hall": dict(a=(1, 0), b=(5, 0), hook=("66 NAMES", "READ OUT"), sub="AL-KHULD HALL  \u00b7  BAGHDAD  \u00b7  22 JUL 1979"),
   "T2_he_cried": dict(a=(32, 0), b=(37, 0), hook=("THE FBI", "WATCHED IT"), sub="THE 1979 TAPE  \u00b7  FBI REPORT, 2004"),
   "T3_all_scared": dict(a=(87, 0), b=(93, 0), hook=("\u201cWE WERE", "ALL SCARED\u201d"), sub="SADDAM TO THE FBI  \u00b7  BAGHDAD  \u00b7  20 FEB 2004")}),
 "gaddafi": dict(dir="12_gaddafi_stadium", mod="render_gaddafi", title=("Gaddafi's Basketball", "Court Gallows:", "8 Hangings in 8 Days"), teasers={
   "T1_terror_council": dict(a=(1, 0), b=(3, 0), hook=("TERROR", "COUNCIL"), sub="GADDAFI  \u00b7  UN, NEW YORK  \u00b7  23 SEP 2009"),
   "T2_heart_of_america": dict(a=(78, 0), b=(81, 0), hook=("\u201cTHE HEART", "OF AMERICA\u201d"), sub="GADDAFI ON LIBYAN RADIO  \u00b7  11 JUN 1984"),
   "T3_stadium": dict(a=(61, 0), b=(66, 0), hook=("THE", "STADIUM"), sub="BENGHAZI  \u00b7  5 JUN 1984  \u00b7  RAMADAN")}),
 "franklin": dict(dir="03_franklin", mod="render_franklin", title=("129 Men Vanished in the Arctic.", "This Is Their Last Note."), teasers={
   "T1_all_well": dict(a=(0, 0), b=(7, 0), hook=("\u201cALL", "WELL\u201d"), sub="VICTORY POINT  \u00b7  25 APR 1848"),
   "T2_the_boat": dict(a=(119, 0), b=(127, 0), hook=("THE BOAT", "POINTED BACK"), sub="KING WILLIAM ISLAND  \u00b7  MAY 1859"),
   "T3_closed_door": dict(a=(140, 0), b=(151, 0), hook=("ONE DOOR", "STILL CLOSED"), sub="HMS TERROR  \u00b7  CAMERA INSIDE, 2019")}),
 "goering": dict(dir="13_goering_last_night", mod="render_goering", title=("Hermann G\u00f6ring Was Watched 24/7.", "So How Did He Get Cyanide?"), teasers={
   "T1_hundred_searches": dict(a=(0, 0), b=(4, 0), hook=("100 SEARCHES.", "DEAD ANYWAY."), sub="NUREMBERG PRISON  \u00b7  TUE 15 OCT 1946"),
   "T2_his_own_note": dict(a=(44, 0), b=(48, 0), hook=("HIS OWN", "NOTE"), sub="G\u00d6RING TO THE COMMANDANT  \u00b7  11 OCT 1946"),
   "T3_four_answers": dict(a=(53, 0), b=(60, 0), hook=("4 MEN.", "4 ANSWERS."), sub="HOW DID G\u00d6RING GET THE CYANIDE?  \u00b7  1951-2026")}),
 "alcatraz46": dict(dir="14_battle_of_alcatraz", mod="render_alcatraz46", title=("Alcatraz, 1946: Marines Dropped", "Grenades Through the Roof"), teasers={
   "T1_gun_cage": dict(a=(13, 0), b=(16, 0), hook=("THE GUN", "CAGE"), sub="ALCATRAZ  \u00b7  THU 2 MAY 1946  \u00b7  2:00 PM"),
   "T2_key_107": dict(a=(18, 0), b=(22, 0), hook=("KEY", "107"), sub="ALCATRAZ  \u00b7  CELLS 403 AND 402  \u00b7  2 MAY 1946"),
   "T3_grenades_roof": dict(a=(41, 0), b=(44, 0), hook=("GRENADES", "THROUGH THE ROOF"), sub="ALCATRAZ  \u00b7  FRI 3 MAY 1946")}),
}
KEY = sys.argv[2] if len(sys.argv) > 2 else "khuld"; F = FILES[KEY]
sys.path.insert(0, NC + F["dir"]); R = importlib.import_module(F["mod"])
L = R.L; ease = getattr(R, "ease", None) or L.ease
INK, BONE, RED, STEEL, COND, TYPE, SER, FPS, T = R.INK, R.BONE, R.RED, R.STEEL, R.COND, R.TYPE, R.SER, R.FPS, R.T
if hasattr(R, "NO_BOTTOM"): R.NO_BOTTOM = True
if hasattr(R, "OV"): R.OV[:] = [(ln, off, "none" if k == "hookleft" else k, a) for ln, off, k, a in R.OV]   # the teaser's own hook replaces the frame-1 blocks (cut off in 9:16)
LE = R.LE if hasattr(R, "LE") else [T[i] + R.DURS.get(i, 0) for i in range(len(T))]   # Franklin: line end = start + spoken length
VW, VH = 1080, 1920
FIT_KINDS = {"tcard", "coldopen"}                          # shots with left-aligned date text: never centre-crop them
TZ =NC + F["dir"] + "/teasers/"; os.makedirs(TZ + "build", exist_ok=True)
CTA_WAV = NC + f"_cta/cta_t_{KEY}.wav"
END_LEN = round(0.5 + sf.info(CTA_WAV).duration + 1.2, 2) if os.path.exists(CTA_WAV) else 6.0     # 6.0 only for QA before the CTA exists
TEASERS = {n: dict(c, a=T[c["a"][0]] - 0.08, b=LE[c["b"][0]] + 0.3) for n, c in F["teasers"].items()}
TITLE = F["title"]

WD = []                                                    # absolute words on the video clock
for sg in json.load(open(NC + F["dir"] + "/vo/vo_words.json", encoding="utf-8")):
    for w in sg["words"]:
        txt = R.capfix(sg["line"], w["w"].strip()) if hasattr(R, "capfix") else w["w"]          # the long edit's spelling fixes (Göring, Andrus...)
        if not txt.strip(): continue
        if WD and len(txt) > 1 and txt[0] in ".," and txt[1].isalnum():                       # "2" + ".15" -> "2:15", as in the long edit
            WD[-1]["w"] = re.sub(r"^(\d{1,2})\.(\d\d)", r"\1:\2", WD[-1]["w"] + txt); WD[-1]["e"] = T[sg["line"]] + w["e"] - sg["start"]; continue
        WD.append(dict(w=txt, s=T[sg["line"]] + w["s"] - sg["start"], e=T[sg["line"]] + w["e"] - sg["start"]))
def chunks(a, b):
    ws = [w for w in WD if a <= w["s"] < b]; out = []; cur = []
    for w in ws:
        cur.append(w)
        if len(cur) == 3 or w["w"].strip().endswith((",", ".", "?", "!")): out.append(cur); cur = []
    if cur: out.append(cur)
    return [(c[0]["s"], c[-1]["e"] + 0.15, " ".join(x["w"].strip() for x in c).strip(",.")) for c in out]
CAPS = {n: chunks(c["a"], c["b"]) for n, c in TEASERS.items()}
def fit(txt, font, size, maxw):
    while size > 30 and L.font(font, size).getlength(txt) > maxw: size -= 2
    return size

def vframe(name, t):
    cfg = TEASERS[name]; dur = cfg["b"] - cfg["a"]
    c = Image.new("RGBA", (VW, VH), INK + (255,))
    if t < dur:
        big = R.frame(cfg["a"] + t).convert("RGB")
        bg = big.resize((int(1920 * VH / 1080), VH), Image.BILINEAR).crop(((int(1920 * VH / 1080) - VW) // 2, 0, (int(1920 * VH / 1080) - VW) // 2 + VW, VH))
        bg = bg.filter(ImageFilter.GaussianBlur(28)); bg = Image.fromarray((np.asarray(bg, np.float32) * 0.25).astype(np.uint8))
        c.paste(bg, (0, 0))
        kind, a = R.shot_at(cfg["a"] + t)[1][1]
        wide = kind == "kbp" and a.get("crop") and (a["crop"][2] - a["crop"][0]) * 16 > (a["crop"][3] - a["crop"][1]) * 9 * 2.5   # a headline strip
        if kind in FIT_KINDS or wide: c.paste(big.resize((VW, 608), Image.LANCZOS), (0, 661))   # left-set date text / wide strip: whole frame
        else: c.paste(big.resize((1440, 810), Image.LANCZOS).crop((180, 0, 1260, 810)), (0, 560))
        d = ImageDraw.Draw(c); d.rectangle((0, 556, VW, 560), fill=RED); d.rectangle((0, 1370, VW, 1374), fill=RED)
        for i, (hk, col, y) in enumerate(((cfg["hook"][0], BONE, 215), (cfg["hook"][1], RED, 365))):
            L.text(c, hk, VW / 2, y, fit(hk, COND, 150, 1000), col, COND)
        L.typewriter(c, cfg["sub"], t, 0.0, VW / 2, 490, size=fit(cfg["sub"], TYPE, 34, 1020), fill=STEEL, cps=60, anchor="mm", cursor=False)
        tt = cfg["a"] + t
        for s0, s1, txt in CAPS[name]:
            if s0 <= tt < s1:
                d.text((VW / 2, 1540), txt, font=L.font(COND, fit(txt, COND, 92 if len(txt) < 20 else 78, 1000)), fill=BONE, anchor="mm", stroke_width=8, stroke_fill=(8, 8, 8)); break
        L.text(c, "the LAST HOURS", VW / 2, 1830, 40, STEEL, COND)
    else:
        te = t - dur; u = ease(te / 0.4)
        L.typewriter(c, "THE FULL FILE", te, 0.0, VW / 2, 640, size=96, cps=18, anchor="mm", cursor=False)
        if te > 0.6:
            d = ImageDraw.Draw(c); y = 760 + 12 * np.sin(te * 4); d.polygon([(VW / 2 - 40, y), (VW / 2 + 40, y), (VW / 2, y + 50)], fill=RED)
        size = min(fit(ln, SER, 62, 980) for ln in TITLE)
        for i, ln in enumerate(TITLE):
            L.text(c, ln, VW / 2, 930 + i * 80, size, BONE, SER, alpha=ease((te - 0.5) / 0.4))
        L.rule(c, VW / 2 - 300, VW / 2 + 300, 930 + len(TITLE) * 80 - 30, te, 0.9, width=6)
        L.text(c, "the", VW / 2, 1300, 54, STEEL, SER, alpha=u); L.text(c, "LAST HOURS", VW / 2, 1400, 130, BONE, COND, alpha=u)
        L.text(c, "Link below  \u00b7  @TheLastHoursDocs", VW / 2, 1520, 40, STEEL, TYPE, alpha=ease((te - 1.0) / 0.4))
    return c

def audio(name):
    cfg = TEASERS[name]; sr = 48000
    mix, s = sf.read(R.B + "mix.wav", dtype="float32", always_2d=True); mix = mix.mean(1)
    seg = mix[int(cfg["a"] * s): int(cfg["b"] * s)].copy(); f = int(0.25 * s); seg[-f:] *= np.linspace(1, 0, f)
    if s != sr: seg = np.interp(np.arange(int(len(seg) * sr / s)) / sr, np.arange(len(seg)) / s, seg).astype(np.float32)
    cta, cs = sf.read(CTA_WAV, dtype="float32", always_2d=True); cta = cta.mean(1)
    if cs != sr: cta = np.interp(np.arange(int(len(cta) * sr / cs)) / sr, np.arange(len(cta)) / cs, cta).astype(np.float32)
    vr = np.sqrt(np.mean(seg[np.abs(seg) > 0.02] ** 2)) if np.any(np.abs(seg) > 0.02) else 0.1
    cta = cta / (np.sqrt(np.mean(cta[np.abs(cta) > 0.01] ** 2)) + 1e-9) * vr
    end = np.zeros(int(END_LEN * sr), np.float32); end[int(0.5 * sr): int(0.5 * sr) + len(cta)] += cta[: len(end) - int(0.5 * sr)]
    m, ms = sf.read(R.MUS + "Thunder Dreams.mp3", dtype="float32", always_2d=True); m = m.mean(1)[int(30 * ms): int((30 + END_LEN) * ms)]
    m = np.interp(np.arange(len(end)) / sr, np.arange(len(m)) / ms, m).astype(np.float32); m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9) * vr * 10 ** (-20 / 20)
    m *= np.minimum(1, np.minimum(np.arange(len(m)) / (0.3 * sr), (len(m) - np.arange(len(m))) / (0.8 * sr))); end += m
    hit = sf.read(R.SFXD + "hit_cinematic_deep_impact.mp3", dtype="float32", always_2d=True)[0].mean(1); hit = hit / (np.max(np.abs(hit)) + 1e-9) * vr * 1.5
    end[: min(len(hit), len(end))] += np.interp(np.arange(min(len(hit), len(end))), np.arange(len(hit)), hit)[: len(end)] * 0.6
    y = np.concatenate([seg, end]); y = y / (np.max(np.abs(y)) + 1e-9) * 0.9
    sf.write(TZ + f"build/{name}_raw.wav", y, sr, subtype="FLOAT")
    sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as AM
    AM.master(TZ + f"build/{name}_raw.wav", TZ + f"build/{name}.wav", target=-14, tp=-1)
    return len(y) / sr

def render(name):
    total = audio(name); n = int(total * FPS); out = TZ + f"TheLastHours_Short_{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-", "-i", TZ + f"build/{name}.wav",
                          "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                          "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(n): p.stdin.write(vframe(name, f / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("wrote", out, round(total, 1), "s", flush=True)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "qa":
        name = sys.argv[3]; ts = [float(x) for x in sys.argv[4:]]; tiles = [vframe(name, t).convert("RGB").resize((270, 480)) for t in ts]
        S = Image.new("RGB", (len(tiles) * 280, 500), (20, 20, 20))
        for i, im in enumerate(tiles): S.paste(im, (i * 280, 0))
        S.save(TZ + f"build/qa_{name}.png"); print(TZ + f"build/qa_{name}.png")
    elif m == "times":
        for n, c in TEASERS.items(): print(KEY, n, round(c["b"] - c["a"], 1), "s +", END_LEN, "=", round(c["b"] - c["a"] + END_LEN, 1))
    elif m == "render": render(sys.argv[3])
    elif m == "all":
        for n in TEASERS: render(n)
