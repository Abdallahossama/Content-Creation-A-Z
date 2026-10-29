"""The Cut & Marker sound set, synthesized from scratch (100% ours, copyright-safe). Writes _style_kit/sfx/<name>.wav
(48 kHz, peak -3 dBFS).   uv run --no-project --with numpy --with scipy --with soundfile python sfx_kit.py"""
import os, shutil
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
OUT = "D:/why habibi/_style_kit/sfx/"
EP1 = "D:/why habibi/1st video/claude_sfx/"          # our own generated Ep 1 kit (re-used, also ours)
rng = np.random.default_rng(7)

def t(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def bp(x, lo, hi, o=4): return sosfilt(butter(o, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f, o=4): return sosfilt(butter(o, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, "highpass", fs=SR, output="sos"), x)
def env(n, a, r, shape=1.0):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na) ** shape
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** shape
    return e
def bumps(d, k, width=0.05, seed=0):
    r = np.random.default_rng(seed); tt = t(d); e = np.zeros_like(tt)
    for c in np.sort(r.uniform(0.02, d - 0.05, k)):
        e += np.exp(-0.5 * ((tt - c) / (width * r.uniform(0.6, 1.4))) ** 2) * r.uniform(0.6, 1.0)
    return e / max(e.max(), 1e-6)
def thump(f, d, drop=0.5):
    tt = t(d); ph = 2 * np.pi * np.cumsum(f * (1 - drop * tt / d)) / SR
    return np.sin(ph) * np.exp(-tt / (d / 4))
def save(name, x, stereo_w=0.0):
    x = x / (np.max(np.abs(x)) + 1e-9) * 10 ** (-3 / 20)
    st = np.stack([x, x], 1)
    if stereo_w:                                 # tiny decorrelation so it isn't dead-centre mono
        d = int(0.0007 * SR); st[d:, 1] = x[:-d] * (1 - stereo_w) + x[d:] * stereo_w
    sf.write(OUT + name + ".wav", st.astype(np.float32), SR, subtype="PCM_16"); print(name, round(len(x) / SR, 2), "s")

os.makedirs(OUT, exist_ok=True)
# marker: writing (scratchy strokes) and a squeak (circles, arrows, ticks)
d = 0.55; save("marker_write", bp(noise(d), 2200, 7000) * bumps(d, 6, 0.03, 1) * env(int(d * SR), 0.01, 0.08) * 0.6)
d = 0.32; tt = t(d)
sq = bp(noise(d), 2600, 4200, 6) * 0.7 + np.sin(2 * np.pi * np.cumsum(2300 + 400 * np.sin(tt * 18)) / SR) * 0.12
save("marker_squeak", sq * bumps(d, 2, 0.06, 2) * env(len(tt), 0.01, 0.06))
d = 0.45; save("highlighter", bp(noise(d), 900, 4200) * env(int(d * SR), 0.12, 0.2, 1.5) * 0.7)
# paper: the signature "receipt" sound = slide + soft stamp
d = 0.62; tt = t(d); sweep = np.zeros_like(tt); x = noise(d)
for k, (lo, hi) in enumerate([(300, 1200), (600, 2400), (1000, 4000)]):
    seg = slice(int(k * len(tt) / 3), int((k + 1) * len(tt) / 3)); sweep[seg] = bp(x, lo, hi)[seg]
slide = sweep * env(len(tt), 0.08, 0.15) * 0.8
stamp = np.zeros_like(tt); st = thump(95, 0.14, 0.3); stamp[-len(st) - 1000:-1000] = st * 0.9
save("paper_slide", slide + stamp, 0.3)
d = 0.16; x = hp(noise(d), 1500) * env(int(d * SR), 0.0, 0.14, 3) * 0.6; x[:len(thump(150, 0.08))] += thump(150, 0.08) * 0.9
save("sticker_slap", x)
d = 0.9; x = thump(58, d, 0.4) * 1.0 + lp(noise(d), 1500) * env(int(d * SR), 0.0, 0.85, 4) * 0.35; save("impact_soft", lp(x, 3000), 0.2)
d = 1.0; tt = t(d); x = noise(d); y = np.zeros_like(tt)
for k in range(10):
    seg = slice(int(k * len(tt) / 10), int((k + 1) * len(tt) / 10)); lo = 300 * 1.45 ** k; y[seg] = bp(x, lo, min(lo * 2.2, 20000))[seg]
save("riser_short", y * np.linspace(0.05, 1, len(tt)) ** 2 * env(len(tt), 0.0, 0.03), 0.3)
# night room
d = 9.0; save("room_tone", lp(noise(d), 700) * 0.4 + np.sin(2 * np.pi * 60 * t(d)) * 0.02, 0.4)
# creak: stick-slip impulses through wood resonances
d = 0.95; tt = t(d); imp = np.zeros_like(tt); pos = 0.0
while pos < d - 0.02:
    rate = 35 + 70 * (pos / d); imp[int(pos * SR)] = 1.0; pos += 1 / rate * rng.uniform(0.8, 1.2)
cr = sum(bp(imp, f * 0.85, f * 1.15, 2) * g for f, g in [(420, 1.0), (930, 0.7), (1700, 0.4)])
save("creak", cr * env(len(tt), 0.1, 0.25))
d = 1.2; x = np.zeros(int(d * SR))
for c in (0.05, 0.6):
    s = lp(noise(0.12), 600) * env(int(0.12 * SR), 0.005, 0.1, 2) * 0.8 + thump(75, 0.12) * 0.7; i = int(c * SR); x[i:i + len(s)] += s
save("footsteps", x, 0.2)
d = 0.7; x = np.zeros(int(d * SR)); cl = hp(noise(0.03), 2500) * env(int(0.03 * SR), 0, 0.025); x[:len(cl)] += cl * 0.7
th = thump(105, 0.25) + lp(noise(0.25), 900) * env(int(0.25 * SR), 0, 0.2, 2) * 0.4; x[int(0.08 * SR):int(0.08 * SR) + len(th)] += th
save("door", x, 0.2)
d = 2.3; tt = t(d); x = noise(d); y = np.zeros_like(tt)
for k in range(12):
    seg = slice(int(k * len(tt) / 12), int((k + 1) * len(tt) / 12)); c = 1300 - 800 * k / 11; y[seg] = bp(x, c * 0.5, c * 1.6)[seg]
save("car_pass", lp(y, 2500) * np.exp(-((tt - d * 0.55) / 0.45) ** 2), 0.6)
d = 1.7; tt = t(d); trill = np.sign(np.sin(2 * np.pi * 18 * tt))
ring = np.where(trill > 0, np.sin(2 * np.pi * 1250 * tt), np.sin(2 * np.pi * 1550 * tt)) * 0.5
gate = ((tt % 0.85) < 0.6).astype(float); save("phone_ring", lp(ring * gate * env(len(tt), 0.01, 0.1), 2200))   # muffled, "through the wall"
d = 1.4; tt = t(d); save("bell", sum(np.sin(2 * np.pi * 1180 * r * tt) * np.exp(-tt * (2.2 + 1.6 * i)) * g
                                   for i, (r, g) in enumerate([(1, 1), (2.76, 0.5), (5.4, 0.3), (8.93, 0.15)])), 0.3)
d = 0.9; tt = t(d); kc = sum(np.sin(2 * np.pi * 2100 * r * tt) * np.exp(-tt * (4 + 2 * i)) * g for i, (r, g) in enumerate([(1, 1), (2.4, 0.4), (3.9, 0.2)]))
kc[:int(0.04 * SR)] += hp(noise(0.04), 2000) * 0.8; save("cash_register", kc, 0.3)
for n in ("heartbeat", "record_scratch", "whoosh_long", "whoosh_fast", "glitch_error", "pop", "swoosh_in", "riser"):
    if os.path.exists(EP1 + n + ".wav"): shutil.copy(EP1 + n + ".wav", OUT + n + ".wav"); print(n, "(Ep 1 kit)")
