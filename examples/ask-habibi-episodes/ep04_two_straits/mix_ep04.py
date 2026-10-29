"""Ep 4 (documentary) audio: the VO split at the documentary pauses · one cinematic track per chapter (incompetech,
CC BY 4.0), ducked under the voice and swelling in the pauses · quiet SFX from the beat cues
-> build/vo_timeline.wav, music_bed_ep04.wav, sfx_ep04.wav (CapCut stems) and mix_ep04.wav (-14 LUFS, TP -1)."""
import subprocess, json
import numpy as np, soundfile as sf
from beats_ep04 import BEATS, CUES
from ep04_common import *

SR = 48000
N = int(T_END * SR) + SR
LIB = "D:/why habibi/_music_library/"
SFX = "D:/why habibi/_style_kit/sfx/"

def dec(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32); return a.reshape(-1, ch).copy() if ch > 1 else a.copy()

# ---------------------------------------------------------------- VO timeline (split at the pauses)
# The voice is the UNTOUCHED ElevenLabs file: no limiter, no de-ess, no leveling (user, 2026-10-12: every squashed
# version had "a whoosh when I speak"; the untouched track in CapCut was clean). The whole mix below is computed at the
# old working level (+6.3 dB, float, detection and balance only) and scaled down at the end, so the balance is unchanged.
import os
S = os.environ.get("STEM_SUFFIX", "")                            # new file names while CapCut holds the old ones
VO_GAIN_DB, WORK_DB = 0.0, 6.3                                   # 0 dB: exactly the ElevenLabs file, peaks -1.1 dBFS
vo = vo_untouched(SR)[0] * np.float32(10 ** (WORK_DB / 20)); vt = np.zeros(N, np.float32)   # straight from the 2 MP3s
edges = [0.0] + [c for c, _ in PAUSES] + [VO_LEN]
for a, b in zip(edges, edges[1:]):
    seg = vo[int(a * SR):int(b * SR)]; i = int(round(T(a + 1e-4) * SR))
    n = min(len(seg), N - i); vt[i:i + n] += seg[:n]

# ---------------------------------------------------------------- music: one track per chapter
t_of = {b.name: b.t0 for b in BEATS}
PLAN = [("Stay the Course", 0.0, t_of["ch2_closing"], 0.0, 1.5, 1.2),
        ("Rising Tide", t_of["ch2_closing"], t_of["ch3_pipeline"], 0.0, 1.0, 1.2),
        ("Industrial Cinematic", t_of["ch3_pipeline"], t_of["ch4_bab"], 0.0, 1.0, 1.2),
        ("Man Down", t_of["ch4_bab"], t_of["ch5_doors"], 0.0, 1.0, 1.4),
        ("Floating Cities", t_of["ch5_doors"], T_END, 0.0, 1.2, 4.0)]
TARGET, LUFS = -16.0, {}
TRIM = {"Stay the Course": 0.0, "Rising Tide": -1.0, "Industrial Cinematic": -1.5, "Man Down": 0.0, "Floating Cities": 0.0}
def track(name):
    p = LIB + name + ".mp3"; a = dec(p)
    if name not in LUFS:
        o = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
        LUFS[name] = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    return a * (10 ** ((TARGET - LUFS[name] + TRIM.get(name, 0)) / 20))
def eqp(n, out=False):
    x = np.linspace(0, 1, max(n, 1)); return np.cos(x * np.pi / 2) if out else np.sin(x * np.pi / 2)
bed = np.zeros((N, 2), np.float32)
for name, t0, t1, off, fi, fo in PLAN:
    a = track(name)
    s0, s1 = max(0.0, t0 - fi / 2), min(T_END, t1 + (fo / 2 if t1 < T_END else 0))
    n = int((s1 - s0) * SR); src0 = max(0, int((off - (t0 - s0)) * SR)); seg = a[src0:src0 + n]
    if len(seg) < n: seg = np.concatenate([a[src0:]] + [a] * (int(np.ceil(n / max(len(a), 1))) + 1))[:n]
    g = np.ones(n, np.float32); ni, no = int(fi * SR), int(fo * SR); g[:ni] *= eqp(ni); g[n - no:] *= eqp(no, True)
    i0 = int(s0 * SR); bed[i0:i0 + n] += seg * g[:, None]
# Music NEVER moves while the voice speaks (user, 2026-10-12: a duck that drops and swells around every phrase reads as
# a "whoosh when I speak"). Spoken passages = voiced stretches joined across gaps shorter than 1.0 s; the music sits at
# one fixed level for the whole passage and only ramps (1.2 s, raised cosine) inside the real pauses. The sub-bass of
# these cinematic tracks is cut by a fixed 6 dB everywhere (static, so it never sweeps).
from scipy.signal import butter, sosfiltfilt
FR = 480                                                         # 10 ms frames
nf = N // FR; fr = np.abs(vt[:nf * FR]).reshape(nf, FR).max(1) > 0.02
k = np.flatnonzero(fr); blk = np.zeros(nf, bool)
if len(k):
    starts = [k[0]]; ends = []
    for a, b in zip(k[:-1], k[1:]):
        if b - a > 100: ends.append(a); starts.append(b)          # a gap of 1.0 s or more ends the passage
    ends.append(k[-1])
    for a, b in zip(starts, ends): blk[max(0, a - 40):b + 25] = True   # fully down 0.4 s before the first word
from scipy.ndimage import binary_dilation
ext = binary_dilation(blk, np.ones(121, bool))                   # +-0.6 s, so the 1.2 s ramp ends before the passage
ramp = np.hanning(120); ramp /= ramp.sum()
d = np.clip(np.convolve(np.pad(ext.astype(np.float64), 60, mode="edge"), ramp, "same")[60:-60], 0, 1)
assert np.all(d[blk] > 0.999), "the music would still be moving under the voice"
env = np.repeat(d, FR); env = np.concatenate([env, np.full(N - len(env), env[-1] if len(env) else 0)]).astype(np.float32)
print(f"music: {int(blk.sum() / 100)} s of speech passages, flat under the voice; it moves only in "
      f"{int(((d > 0.001) & (d < 0.999)).sum() / 100)} s of pauses")
lo = sosfiltfilt(butter(4, 150, "lowpass", fs=SR, output="sos"), bed, axis=0).astype(np.float32); hi = bed - lo
bed = (hi + lo * 10 ** (-6 / 20)) * (10 ** (-12.0 * env / 20))[:, None] * 10 ** (-3.5 / 20)

# ---------------------------------------------------------------- SFX (quiet)
# Under the voice only tiny tonal clicks (pop, sticker_slap). Whooshes, risers, impacts, paper and highlighter are
# noise-based and the user hears them as "noise while I speak" (2026-10-12), so they play only in the pauses.
UNDER_VOICE_OK = {"pop", "sticker_slap"}
voiced = np.convolve(np.abs(vt) > 0.02, np.ones(int(0.2 * SR), np.float32), "same") > 0
sfx = np.zeros((N, 2), np.float32); sounds = {}; last = {}; dropped = []
for t, name, g in CUES:
    if name == "room_tone": continue                             # a recorded noise bed: it sat under the opening lines
    if t - last.get(name, -9) < 0.12: continue
    last[name] = t
    if name not in sounds: sounds[name] = sf.read(SFX + name + ".wav", dtype="float32")[0]
    s = sounds[name]; s = s if s.ndim == 2 else np.stack([s, s], 1)
    i = int(t * SR); n = min(len(s), N - i)
    if n > 0 and name not in UNDER_VOICE_OK and voiced[i:i + n].any(): dropped.append((round(t, 1), name)); continue
    if n > 0: sfx[i:i + n] += s[:n] * g * 0.45
print(f"SFX: {len(dropped)} noise-type cues dropped because they overlap the voice:", dropped)

k = np.float32(10 ** ((VO_GAIN_DB - WORK_DB) / 20)); vt, bed, sfx = vt * k, bed * k, sfx * k   # back to the clean level
assert np.abs(vt).max() < 10 ** (-1 / 20) + 1e-3, "the voice would need limiting"
def w(name, x): sf.write(BUILD + name, x[:int(T_END * SR)], SR, subtype="PCM_24")
w(f"vo_timeline{S}.wav", vt); w(f"music_bed_ep04{S}.wav", bed); w(f"sfx_ep04{S}.wav", sfx)
mix = np.stack([vt, vt], 1) + bed + sfx
# raw mix as FLOAT, then PLAIN gain only (no limiter, nothing squashes the voice); loudness is whatever the peaks allow
sf.write(BUILD + f"mix_raw{S}.wav", mix[:int(T_END * SR)], SR, subtype="FLOAT")
import sys; sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master
audio_master.gain_only(BUILD + f"mix_raw{S}.wav", BUILD + f"mix_ep04{S}.wav", target=-14.0, tp=-1.0)
print("voice peak", round(20 * np.log10(np.abs(vt).max()), 2), "dBFS · track LUFS:", LUFS)

