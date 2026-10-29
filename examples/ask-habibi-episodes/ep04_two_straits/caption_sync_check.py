"""Do the captions start when the untouched voice starts? For every caption that begins a phrase (>= 0.25 s of silence
before it in the voice), find the real voice onset near it and report the offset."""
import json
import numpy as np, soundfile as sf
B = "D:/why habibi/4th video/build/"
v, sr = sf.read(B + "vo_timeline_ELEVENLABS_UNTOUCHED.wav", dtype="float64")
w = sr // 100; m = len(v) // w; db = 20 * np.log10(np.sqrt((v[:m * w].reshape(m, w) ** 2).mean(1)) + 1e-9)
on = db > np.percentile(db[db > -80], 30) - 6                    # voice present (10 ms frames)
caps = json.load(open(B + "captions_ep04.json", encoding="utf-8"))
off = []
for c in caps:
    i = int(round(c["t0"] * 100))
    if i < 30 or on[i - 25:i - 5].any(): continue               # only captions that start after a real pause
    k = np.flatnonzero(on[i - 25:i + 40])
    if len(k):
        off.append((k[0] - 25) * 10)
        if abs((k[0] - 25) * 10) > 120:
            seg = db[i - 25 + k[0]:i + 5]; print(f"  {c['t0']:7.2f}s  {(k[0] - 25) * 10:+5d} ms  '{' '.join(c['words'])}'  onset level {db[i - 25 + k[0]]:.0f} dB, at caption {db[i]:.0f} dB")
off = np.array(off)
print(f"{len(off)} phrase-start captions checked · caption vs voice onset: median {np.median(off):+.0f} ms, "
      f"90% within {np.percentile(np.abs(off), 90):.0f} ms, worst {np.abs(off).max():.0f} ms (1 frame = 33 ms)")

