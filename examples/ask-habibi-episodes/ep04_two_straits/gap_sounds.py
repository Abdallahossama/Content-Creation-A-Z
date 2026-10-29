"""What are the noisy sounds in the gaps between words? For every gap: the noisy runs inside it, with length, spectral
centroid (s/sh ~ 5-8 kHz, inhale ~ 1.5-3.5 kHz), level vs words, and distance to the previous / next word."""
import subprocess
import numpy as np
SR = 48000
import sys; SRC = sys.argv[1] if len(sys.argv) > 1 else "D:/why habibi/4th video/vo/ep04_vo_joined.wav"
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-f", "f32le",
                                  "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.float32).astype(np.float64)
w = 480; m = len(x) // w; f = x[:m * w].reshape(m, w)                # 10 ms frames
rms = 10 * np.log10((f ** 2).mean(1) + 1e-14)
P = np.abs(np.fft.rfft(f * np.hanning(w), axis=1)) ** 2 + 1e-18; fq = np.fft.rfftfreq(w, 1 / SR); b = (fq > 300) & (fq < 12000)
flat = np.exp(np.log(P[:, b]).mean(1)) / P[:, b].mean(1); cen = (P[:, b] * fq[b]).sum(1) / P[:, b].sum(1)
lowr = P[:, (fq > 80) & (fq < 400)].sum(1) / P[:, b].sum(1)            # voicing: energy at the pitch
sp = np.median(rms[rms > np.percentile(rms, 60)]); voiced = (rms > sp - 14) & (lowr > 0.02)
noisy = (~voiced) & (rms > sp - 45) & (flat > 0.05)
runs = []; i = 0
while i < m:
    if not noisy[i]: i += 1; continue
    j = i
    while j < m and noisy[j]: j += 1
    if j - i >= 5:
        pv = i - 1
        while pv >= 0 and not voiced[pv]: pv -= 1
        nv = j
        while nv < m and not voiced[nv]: nv += 1
        runs.append(dict(t=i / 100, dur=(j - i) * 10, lvl=rms[i:j].max() - sp, cen=np.median(cen[i:j]), after=(i - pv) * 10, before=(nv - j) * 10))
    i = j
R = runs
print(f"{len(R)} noisy runs >= 50 ms outside voiced speech")
cen = np.array([r["cen"] for r in R]); dur = np.array([r["dur"] for r in R]); lvl = np.array([r["lvl"] for r in R])
bef = np.array([r["before"] for r in R]); aft = np.array([r["after"] for r in R])
for lo, hi in ((0, 2500), (2500, 4000), (4000, 6000), (6000, 20000)):
    s = (cen >= lo) & (cen < hi)
    if s.any(): print(f" centroid {lo:5d}-{hi:5d} Hz: {s.sum():3d} runs · length median {np.median(dur[s]):4.0f} ms · level {np.median(lvl[s]):6.1f} dB vs words · "
                      f"gap to next word {np.median(bef[s]):4.0f} ms · after previous word {np.median(aft[s]):4.0f} ms")
print("examples (t s, ms, dB, Hz, after-prev ms, before-next ms):")
for r in R[:14]: print(f"  {r['t']:6.2f} {r['dur']:4.0f} {r['lvl']:6.1f} {r['cen']:6.0f} {r['after']:5.0f} {r['before']:5.0f}")

