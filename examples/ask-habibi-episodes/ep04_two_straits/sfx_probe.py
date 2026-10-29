"""Which layer is the 'noise when I speak'? Per second: VO level, SFX level, music level, and how much of the
non-voice layers is broadband hiss (energy above 6 kHz). Lists cues that play under the voice."""
import numpy as np, soundfile as sf
from beats_ep04 import CUES
B = "D:/why habibi/4th video/build/"
vt, sr = sf.read(B + "vo_timeline.wav", dtype="float32")
sfx = sf.read(B + "sfx_ep04.wav", dtype="float32", always_2d=True)[0].mean(1)
bed = sf.read(B + "music_bed_ep04.wav", dtype="float32", always_2d=True)[0].mean(1)
def db(x): return 20 * np.log10(np.sqrt((x.astype(np.float64) ** 2).mean()) + 1e-9)
print("room_tone cues:", [(round(t, 2), g) for t, n, g in CUES if n == "room_tone"])
rt, rsr = sf.read("D:/why habibi/_style_kit/sfx/room_tone.wav", dtype="float32", always_2d=True)
print(f"room_tone.wav: {len(rt) / rsr:.1f} s, {db(rt.mean(1)):.1f} dBFS raw")
print("\ncue            t      VO dB   SFX dB (that second)  SFX-VO")
for t, n, g in CUES:
    i = int(t * sr); w = slice(i, i + sr)
    v, s = db(vt[w]), db(sfx[w])
    if v > -40 and s - v > -22: print(f"{n:14s} {t:6.2f}  {v:6.1f}  {s:6.1f}               {s - v:+5.1f}")
def hf_ratio(x):
    X = np.abs(np.fft.rfft(x[: sr * 30] if len(x) > sr * 30 else x)) ** 2; f = np.fft.rfftfreq(min(len(x), sr * 30), 1 / sr)
    return 10 * np.log10(X[f > 6000].sum() / (X[(f > 100) & (f < 6000)].sum() + 1e-12) + 1e-12)
print("\nHF share (>6 kHz vs 0.1-6 kHz): VO", round(hf_ratio(vt), 1), "dB · music", round(hf_ratio(bed), 1), "dB · room_tone", round(hf_ratio(rt.mean(1)), 1), "dB")
# music under the voice, per chapter-ish window
voiced = np.convolve(np.abs(vt) > 0.02, np.ones(int(0.2 * sr)), "same") > 0
print(f"music level under the voice {db(bed[voiced]):.1f} dBFS vs voice {db(vt[voiced]):.1f} dBFS ({db(bed[voiced]) - db(vt[voiced]):+.1f} dB)")
