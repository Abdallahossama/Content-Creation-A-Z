"""Per chapter: how noise-like is the music under the voice (spectral flatness, 0 = tonal, 1 = white noise),
how much sub-bass rumble (<120 Hz) it has, and its level relative to the voice."""
import numpy as np, soundfile as sf
from beats_ep04 import BEATS
B = "D:/why habibi/4th video/build/"
vt, sr = sf.read(B + "vo_timeline.wav", dtype="float64")
bed = sf.read(B + "music_bed_ep04.wav", dtype="float64", always_2d=True)[0].mean(1)
sfx = sf.read(B + "sfx_ep04.wav", dtype="float64", always_2d=True)[0].mean(1)
t_of = {b.name: b.t0 for b in BEATS}
CH = [("Stay the Course (0:00 open)", 0, t_of["ch2_closing"]), ("Rising Tide (ch2)", t_of["ch2_closing"], t_of["ch3_pipeline"]),
      ("Industrial Cinematic (ch3)", t_of["ch3_pipeline"], t_of["ch4_bab"]), ("Man Down (ch4)", t_of["ch4_bab"], t_of["ch5_doors"]),
      ("Floating Cities (ch5)", t_of["ch5_doors"], len(vt) / sr)]
def flat_and_sub(x):
    F = 4096; fr = [x[i:i + F] * np.hanning(F) for i in range(0, len(x) - F, F)]
    P = np.mean([np.abs(np.fft.rfft(f)) ** 2 for f in fr], 0) + 1e-18; f = np.fft.rfftfreq(F, 1 / sr)
    band = (f > 150) & (f < 8000); fl = np.exp(np.log(P[band]).mean()) / P[band].mean()
    sub = 10 * np.log10(P[f < 120].sum() / P[(f >= 120) & (f < 8000)].sum())
    return fl, sub
db = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
for name, a, b in CH:
    i, j = int(a * sr), int(b * sr); v, m, s = vt[i:j], bed[i:j], sfx[i:j]
    on = np.convolve(np.abs(v) > 0.02, np.ones(int(0.2 * sr)), "same") > 0
    fl, sub = flat_and_sub(m[on]) if on.any() else (0, 0)
    print(f"{name:30s} {a:6.1f}-{b:6.1f}s  music under voice {db(m[on]) - db(v[on]):+5.1f} dB  flatness {fl:.3f}  sub<120Hz {sub:+5.1f} dB  sfx under voice {db(s[on]) - db(v[on]):+5.1f} dB")
fl, sub = flat_and_sub(sf.read("D:/why habibi/_style_kit/sfx/room_tone.wav", dtype="float64", always_2d=True)[0].mean(1))
print(f"room_tone.wav (first 9 s)  flatness {fl:.3f}  sub<120Hz {sub:+5.1f} dB")
