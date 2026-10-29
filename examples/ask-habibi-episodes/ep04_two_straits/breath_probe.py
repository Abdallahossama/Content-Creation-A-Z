"""Breaths (inhales) between phrases: noisy, unvoiced bursts in the gaps. How loud are they relative to the words, in the
ElevenLabs file vs the voice in the video?"""
import subprocess
import numpy as np
SR = 48000; V = "D:/why habibi/4th video/vo/"
def dec(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                        capture_output=True).stdout, np.float32).astype(np.float64)
def frames(x, w=960):
    m = len(x) // w; f = x[:m * w].reshape(m, w)
    rms = 10 * np.log10((f ** 2).mean(1) + 1e-14)
    P = np.abs(np.fft.rfft(f * np.hanning(w), axis=1)) ** 2 + 1e-18; fq = np.fft.rfftfreq(w, 1 / SR); b = (fq > 300) & (fq < 8000)
    flat = np.exp(np.log(P[:, b]).mean(1)) / P[:, b].mean(1)
    return rms, flat
def breaths(path):
    rms, flat = frames(dec(path)); sp = np.median(rms[rms > np.percentile(rms, 60)])     # typical word level
    voiced = rms > sp - 14
    ev = []; i = 0; n = len(rms)
    while i < n:
        if voiced[i]: i += 1; continue
        j = i
        while j < n and not voiced[j]: j += 1
        if 7 <= j - i <= 60 and i > 0 and j < n:                 # gaps of 0.14-1.2 s between voiced frames
            seg = slice(i, j); k = i + int(np.argmax(rms[seg]))
            if rms[k] > sp - 40 and flat[k] > 0.08: ev.append((k * 0.02, rms[k] - sp))   # noisy burst = breath / air
        i = j
    return sp, ev
for name, p in (("ElevenLabs file", V + "ep04_vo_joined.wav"), ("voice in the video", V + "ep04_VO_leveled_-16LUFS.wav"), ("before de-breath", "D:/why habibi/_archive/ep04_dynamic_loudnorm_audio/ep04_VO_leveled_static_limiter_with_breaths.wav")):
    sp, ev = breaths(p); r = np.array([e[1] for e in ev])
    print(f"{name:20s} words at {sp:6.1f} dBFS · {len(ev)} breaths · breath vs words: median {np.median(r):6.1f} dB, loudest 10% {np.percentile(r, 90):6.1f} dB")
    print("   first few at (s):", [round(e[0], 1) for e in ev[:10]])
