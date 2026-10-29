"""Hiss riding on the voice: look only at clearly voiced vowel frames (loud, tonal, energy at the pitch) and measure
(a) high band 6-12 kHz relative to 0.1-4 kHz (vowels carry little up there; a hiss layer lifts it)
(b) the valleys between harmonics in 0.3-3 kHz relative to the peaks (noise fills the valleys)."""
import subprocess, sys
import numpy as np
SR = 44100
FILES = {"Ep1 (your ElevenLabs download)": "D:/why habibi/1st video/ElevenLabs_2026-10-12T10_08_03_Abdullah Osama_ivc_sp100_s50_sb75_v4.mp3",
         "Ep2 part1": "D:/why habibi/2nd video/vo/ep02_vo_part1.mp3", "Ep3 part1": "D:/why habibi/3rd video/vo/ep03_vo_part1.mp3",
         "Ep4 part1": "D:/why habibi/4th video/vo/ep04_vo_part1.mp3", "Ep4 part2": "D:/why habibi/4th video/vo/ep04_vo_part2.mp3"}
for name, p in FILES.items():
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                     capture_output=True).stdout, np.float32).astype(np.float64)
    N = 2048; H = 1024; m = (len(x) - N) // H
    S = np.abs(np.array([np.fft.rfft(x[i * H:i * H + N] * np.hanning(N)) for i in range(m)])) ** 2 + 1e-20
    fq = np.fft.rfftfreq(N, 1 / SR); lvl = 10 * np.log10(S.sum(1))
    lo = S[:, (fq > 80) & (fq < 400)].sum(1); mid = S[:, (fq > 100) & (fq < 4000)].sum(1); hi = S[:, (fq > 6000) & (fq < 12000)].sum(1)
    b = (fq > 300) & (fq < 3000); flat = np.exp(np.log(S[:, b]).mean(1)) / S[:, b].mean(1)
    vow = (lvl > np.percentile(lvl, 70)) & (lo / mid > 0.15) & (flat < 0.05)
    hf = 10 * np.log10(hi[vow] / mid[vow])
    seg = S[vow][:, b]; valley = 10 * np.log10(np.percentile(seg, 20, axis=1) / np.percentile(seg, 95, axis=1))
    print(f"{name:32s} vowels {vow.sum():5d} frames · 6-12 kHz vs body {np.median(hf):6.1f} dB · harmonic valleys {np.median(valley):6.1f} dB")
