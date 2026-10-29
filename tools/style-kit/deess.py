"""De-esser for the ElevenLabs voice: turns down only the hiss of s / sh / f (above 4.5 kHz) when it pokes out, never
the vowels. Why: the cloned voice is very bright, its "s" sounds sit ~4 dB under the vowels (a normal VO: 10-15 dB).
At YouTube loudness that is a hiss on nearly every word, heard as "a whoosh when I speak" (Ep 4, 2026-10-12).

How: split at 4.5 kHz (zero-phase, perfect reconstruction). The high band's 5 ms level is held at least `under` dB below
the typical word level; reduction is at most `max_db`, smoothed 3 ms attack / 60 ms release. Length unchanged.
  python deess.py in.wav out.wav [under_db=11] [max_db=10]"""
import sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt

def deess(src, dst, under=11.0, max_db=10.0, fc=4500):
    x, sr = sf.read(src, dtype="float64"); mono = x if x.ndim == 1 else x.mean(1)
    sos = butter(4, fc, "highpass", fs=sr, output="sos")
    hi = sosfiltfilt(sos, x, axis=0); lo = x - hi
    hm = hi if hi.ndim == 1 else hi.mean(1)
    w = int(0.005 * sr); k = np.ones(w) / w
    lv = 10 * np.log10(np.convolve(mono ** 2, np.ones(int(0.02 * sr)) / int(0.02 * sr), "same") + 1e-14)
    sp = np.median(lv[lv > np.percentile(lv, 60)])                       # typical word level (20 ms)
    hl = 10 * np.log10(np.convolve(hm ** 2, k, "same") + 1e-14)
    red = np.clip(hl - (sp - under), 0, max_db)                         # dB to take off the high band
    a, r = np.exp(-1 / (0.003 * sr)), np.exp(-1 / (0.060 * sr))
    D = 16; rd = red[::D]; e = np.zeros_like(rd); acc = 0.0; aD, rD = a ** D, r ** D
    for i, v in enumerate(rd):
        acc = aD * acc + (1 - aD) * v if v > acc else rD * acc + (1 - rD) * v; e[i] = acc
    g = 10 ** (-np.repeat(e, D)[:len(mono)] / 20)
    y = lo + hi * (g if x.ndim == 1 else g[:, None])
    sf.write(dst, y, sr, subtype="PCM_24")
    act = np.repeat(e, D)[:len(mono)]
    print(f"{dst}: de-essed {np.mean(act > 1) * 100:.1f}% of the time, median reduction there {np.median(act[act > 1]):.1f} dB, max {act.max():.1f} dB")

if __name__ == "__main__":
    a = sys.argv; deess(a[1], a[2], float(a[3]) if len(a) > 3 else 11.0, float(a[4]) if len(a) > 4 else 10.0)
