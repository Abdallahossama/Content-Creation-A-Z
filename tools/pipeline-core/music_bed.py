"""Build a sectioned, VO-ducked music bed for the whole timeline.
Each section plays one track (level-matched), sections crossfade, and the bed dips under the voice."""
import json, subprocess, sys
import numpy as np, soundfile as sf

SR = 48000
LIB = "D:/why habibi/_music_library/"
OUTF = "D:/why habibi/1st video/claude_music/music_bed_ep01.wav"
VO = "D:/why habibi/1st video/ElevenLabs_VO_leveled_-15LUFS.wav"
END = 193.0333
A_END, GAG_END, B_SRC = 269 / 30, 381 / 30, 9.25   # VO part A end, gag end, VO part B source in-point

# (track, timeline start, timeline end, source offset, fade_in, fade_out)
PLAN = [
    ("Marty Gots a Plan", 0.00, 7.24, 0.0, 0.05, 0.08),     # hook - drops dead on the punchline (user's original idea)
    ("Marty Gots a Plan", 12.05, 28.41, 7.24, 0.35, 0.6),   # resumes after hen + throat gag
    ("Daily Beetle", 28.41, 37.37, 0.0, 0.6, 0.6),           # brand reveal: "That's why Ask Habibi exists"
    ("Easy Lemon", 37.37, 91.89, 0.0, 0.6, 0.6),             # the plan + Level 1 + Level 2
    ("Dream Culture", 91.89, 124.61, 0.0, 0.6, 0.6),         # Level 3: sleep
    ("Thunder Dreams", 124.61, 136.37, 6.0, 0.6, 0.6),       # Level 4: bottom of the iceberg
    ("Easy Lemon", 136.37, 153.55, 58.0, 0.6, 0.6),          # the t-shirt study (lighter again)
    ("Promises to Keep", 153.55, 178.71, 0.0, 0.6, 0.6),     # what helps / when to get help
    ("Daily Beetle", 178.71, END, 0.0, 0.6, 2.6),            # outro (brand theme returns)
]
TARGET_LUFS = -16.0
LUFS = {}

def load(name):
    p = LIB + name + ".mp3"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    if name not in LUFS:
        o = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
        LUFS[name] = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    TRIM = {"Easy Lemon": -3.5, "Dream Culture": -2.5, "Daily Beetle": -1.5, "Promises to Keep": +2.0, "Marty Gots a Plan": +1.0, "Thunder Dreams": +1.0}
    return a * (10 ** ((TARGET_LUFS - LUFS[name] + TRIM.get(name, 0)) / 20))

def eqp(n, out=False):
    x = np.linspace(0, 1, max(n, 1))
    return np.cos(x * np.pi / 2) if out else np.sin(x * np.pi / 2)

N = int(END * SR) + SR
bed = np.zeros((N, 2), np.float32)
cache = {}
for name, t0, t1, off, fi, fo in PLAN:
    a = cache.setdefault(name, load(name))
    xf_in = fi if fi <= 0.1 else fi           # crossfade straddles the boundary
    s0 = max(0.0, t0 - (fi / 2 if fi > 0.1 else 0)); s1 = min(END, t1 + (fo / 2 if fo > 0.1 and t1 < END else 0))
    n = int((s1 - s0) * SR); src0 = int((off - (t0 - s0)) * SR); src0 = max(0, src0)
    seg = a[src0:src0 + n]
    if len(seg) < n:
        seg = np.concatenate([seg, np.zeros((n - len(seg), 2), np.float32)])
    g = np.ones(n, np.float32)
    ni, no = int(fi * SR), int(fo * SR)
    g[:ni] *= eqp(ni); g[n - no:] *= eqp(no, out=True)
    i0 = int(s0 * SR)
    bed[i0:i0 + n] += seg * g[:, None]

# --- VO on the timeline (for ducking) ---
vo, sr = sf.read(VO, dtype="float32")
if vo.ndim > 1: vo = vo.mean(axis=1)
vt = np.zeros(N, np.float32)
na = int(A_END * SR); vt[:na] = vo[:na]
b0 = int(B_SRC * SR); g0 = int(GAG_END * SR); nb = min(len(vo) - b0, N - g0); vt[g0:g0 + nb] = vo[b0:b0 + nb]

# envelope -> gain (dip ~9 dB under speech, attack 60 ms, release 450 ms, 120 ms look-ahead)
win = int(0.02 * SR)
rms = np.sqrt(np.convolve(vt ** 2, np.ones(win) / win, mode="same") + 1e-12)
db = 20 * np.log10(rms + 1e-9)
speech = np.clip((db + 46) / 10, 0, 1)                    # 0 = silence, 1 = clear speech
look = int(0.12 * SR); speech = np.concatenate([speech[look:], np.zeros(look)])
env = np.zeros_like(speech); a_c = np.exp(-1 / (0.06 * SR)); r_c = np.exp(-1 / (0.45 * SR))
# fast smoothing on a decimated signal
dec = 48; sp = speech[::dec]; e = np.zeros_like(sp); acc = 0.0
ac, rc = np.exp(-dec / (0.06 * SR)), np.exp(-dec / (0.45 * SR))
for i, v in enumerate(sp):
    acc = ac * acc + (1 - ac) * v if v > acc else rc * acc + (1 - rc) * v
    e[i] = acc
env = np.repeat(e, dec)[:N]
duck_db = -9.0 * env
gain = (10 ** (duck_db / 20)).astype(np.float32)
BED_LEVEL = 10 ** (-6.0 / 20)                             # bed level before ducking
out = bed * gain[:, None] * BED_LEVEL
out = out[: int(END * SR)]
peak = np.max(np.abs(out)); out = out / peak * 0.89 if peak > 0.89 else out
import os; os.makedirs(os.path.dirname(OUTF), exist_ok=True)
sf.write(OUTF, out, SR, subtype="PCM_16")
print("wrote", OUTF, round(len(out) / SR, 2), "s  track LUFS:", LUFS)
