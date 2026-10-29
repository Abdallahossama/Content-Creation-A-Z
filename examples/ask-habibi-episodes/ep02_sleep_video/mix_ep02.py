"""Ep 2 audio: VO timeline (+ Ep 1 CTA inserts) · sectioned, VO-ducked music bed · SFX from the beat cues
-> build/vo_timeline.wav, music_bed_ep02.wav, sfx_ep02.wav (stems for CapCut) and mix_ep02.wav (-14 LUFS, TP -1)."""
import subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from beats_ep02 import P, CUES, BEATS
from ep02_common import *

SR = 48000
N = int(T_END * SR) + SR
LIB = "D:/why habibi/_music_library/"
SFX = "D:/why habibi/_style_kit/sfx/"

def dec(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32); return a.reshape(-1, ch).copy() if ch > 1 else a.copy()

# ---------------------------------------------------------------- VO timeline
vo2, vo1 = dec(VO2, 1), dec(VO1, 1)
vt = np.zeros(N, np.float32)
def put(dst, src, t):
    i = int(round(t * SR)); n = min(len(src), len(dst) - i); dst[i:i + n] += src[:n]
cut = int(S_CUT * SR)
put(vt, vo2[:cut], 0.0)
put(vt, vo1[int(CTA_IN[0] * SR):int(CTA_IN[1] * SR)], T_CTA_IN)
put(vt, vo2[cut:], S_CUT + O1)
put(vt, vo1[int(CTA_OUT[0] * SR):int(CTA_OUT[1] * SR)], T_CTA_OUT)

# ---------------------------------------------------------------- music bed
CTA_OUT_START = [b.t0 for b in BEATS if b.name == "cta_out"][0]
PLAN = [  # (track, t0, t1, source offset, fade_in, fade_out)
    ("Late Night Radio", 0.0, S_CUT, 0.0, 0.8, 0.6),
    ("Marty Gots a Plan", S_CUT, T_CTA_IN + 24.96 - CTA_IN[0], 0.0, 0.5, 0.6),       # CTA: same music as Ep 1
    ("Daily Beetle", T_CTA_IN + 24.96 - CTA_IN[0], P("Here's the plan."), 0.0, 0.6, 0.6),
    ("Late Night Radio", P("Here's the plan."), P("Level two."), 29.0, 0.6, 0.6),
    ("Vibing Over Venus", P("Level two."), P("Level three."), 0.0, 0.6, 0.6),
    ("Dream Culture", P("Level three."), P("Level four."), 0.0, 0.6, 0.6),
    ("Vibing Over Venus", P("Level four."), P("And now, the verdict"), 150.0, 0.6, 0.6),
    ("Late Night Radio", P("And now, the verdict"), P("So, what actually helps?"), 120.0, 0.6, 0.6),
    ("Easy Lemon", P("So, what actually helps?"), CTA_OUT_START, 0.0, 0.6, 0.6),
    ("Daily Beetle", CTA_OUT_START, T_END, 0.0, 0.6, 3.0),
]
TARGET, LUFS = -16.0, {}
TRIM = {"Easy Lemon": -3.5, "Dream Culture": -2.5, "Daily Beetle": -1.5, "Marty Gots a Plan": +1.0, "Late Night Radio": -1.0,
        "Vibing Over Venus": -2.0}
def track(name):
    p = LIB + name + ".mp3"; a = dec(p)
    if name not in LUFS:
        o = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
        LUFS[name] = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    return a * (10 ** ((TARGET - LUFS[name] + TRIM.get(name, 0)) / 20))
def eqp(n, out=False):
    x = np.linspace(0, 1, max(n, 1)); return np.cos(x * np.pi / 2) if out else np.sin(x * np.pi / 2)
bed = np.zeros((N, 2), np.float32); cache = {}
for name, t0, t1, off, fi, fo in PLAN:
    a = cache.setdefault(name, track(name))
    s0, s1 = max(0.0, t0 - fi / 2), min(T_END, t1 + (fo / 2 if t1 < T_END else 0))
    n = int((s1 - s0) * SR); src0 = max(0, int((off - (t0 - s0)) * SR))
    seg = a[src0:src0 + n]
    if len(seg) < n:                                            # loop the track if a section outlasts it
        reps = int(np.ceil(n / max(len(a), 1))) + 1; seg = np.concatenate([a[src0:]] + [a] * reps)[:n]
    g = np.ones(n, np.float32); ni, no = int(fi * SR), int(fo * SR); g[:ni] *= eqp(ni); g[n - no:] *= eqp(no, True)
    i0 = int(s0 * SR); bed[i0:i0 + n] += seg * g[:, None]
# duck ~9 dB under the voice (attack 60 ms, release 450 ms, 120 ms look-ahead)
win = int(0.02 * SR); rms = np.sqrt(np.convolve(vt ** 2, np.ones(win) / win, mode="same") + 1e-12)
speech = np.clip((20 * np.log10(rms + 1e-9) + 46) / 10, 0, 1); look = int(0.12 * SR)
speech = np.concatenate([speech[look:], np.zeros(look)])
D = 48; sp = speech[::D]; e = np.zeros_like(sp); acc = 0.0; ac, rc = np.exp(-D / (0.06 * SR)), np.exp(-D / (0.45 * SR))
for i, v in enumerate(sp):
    acc = ac * acc + (1 - ac) * v if v > acc else rc * acc + (1 - rc) * v; e[i] = acc
gain = (10 ** (-9.0 * np.repeat(e, D)[:N] / 20)).astype(np.float32)
bed = bed * gain[:, None] * 10 ** (-6.0 / 20)

# ---------------------------------------------------------------- SFX
sfx = np.zeros((N, 2), np.float32); sounds = {}; last = {}
def lp(x, f): return sosfilt(butter(4, f, "lowpass", fs=SR, output="sos"), x, axis=0)
for t, name, g in CUES:
    if name == "muffled_doc":                     # "the stranger explaining Rome": our own VO, through a wall
        src = vo2[int(find("Bath.") * SR):int(find_end("fall of Rome.") * SR)]
        m = lp(np.stack([src, src], 1), 380) * 0.9; m = np.concatenate([m, m])[:int(8.2 * SR)]
        fade = np.ones(len(m)); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
        put2 = (m * fade[:, None] * g * 0.5).astype(np.float32); i = int(t * SR); sfx[i:i + len(put2)] += put2; continue
    if t - last.get(name, -9) < 0.09: continue    # don't stack identical hits
    last[name] = t
    if name not in sounds: sounds[name] = sf.read(SFX + name + ".wav", dtype="float32")[0]
    s = sounds[name]; s = s if s.ndim == 2 else np.stack([s, s], 1)
    i = int(t * SR); n = min(len(s), N - i); sfx[i:i + n] += s[:n] * g * 0.5

# ---------------------------------------------------------------- write stems + mix, then -14 LUFS
def w(name, x): sf.write(BUILD + name, x[:int(T_END * SR)], SR, subtype="PCM_24")
w("vo_timeline.wav", vt); w("music_bed_ep02.wav", bed); w("sfx_ep02.wav", sfx)
mix = np.stack([vt, vt], 1) + bed + sfx
w("mix_raw.wav", mix)
src = BUILD + "mix_raw.wav"
j = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
import json, re
m = json.loads(j[j.rindex("{"):j.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-c:a", "pcm_s24le", BUILD + "mix_ep02.wav"], check=True)
o = subprocess.run(["ffmpeg", "-hide_banner", "-i", BUILD + "mix_ep02.wav", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("mix:", [l.strip() for l in o.splitlines() if l.strip().startswith(("I:", "Peak:"))][-2:], " track LUFS:", LUFS)
for name in ("vo_timeline.wav", "music_bed_ep02.wav", "sfx_ep02.wav"):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", BUILD + name, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    print(name, [l.strip() for l in o.splitlines() if l.strip().startswith("I:")][-1])
