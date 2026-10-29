"""Subtract the voice from the final audio (per-window gain fit) and look at what is left while the voice speaks vs in
the gaps. Real background (music/SFX) should be QUIETER under the voice (ducking); anything that gets LOUDER when the
voice speaks is a processing artifact riding on the voice. Also checks the VO split points for clicks."""
import subprocess
import numpy as np, soundfile as sf
from ep04_common import PAUSES, T
B = "D:/why habibi/4th video/build/"
vt, sr = sf.read(B + "vo_timeline.wav", dtype="float64")
bed = sf.read(B + "music_bed_ep04.wav", dtype="float64", always_2d=True)[0].mean(1)
sfx = sf.read(B + "sfx_ep04.wav", dtype="float64", always_2d=True)[0].mean(1)
fin = sf.read(B + "mix_ep04.wav", dtype="float64", always_2d=True)[0].mean(1)
raw = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "D:/why habibi/4th video/export/Ask_Habibi_Ep4_1440p.mp4",
                    "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"], capture_output=True).stdout, np.float32).reshape(-1, 2).mean(1).astype(np.float64)
n = min(len(vt), len(fin), len(raw), len(bed)); vt, fin, raw, bed, sfx = vt[:n], fin[:n], raw[:n], bed[:n], sfx[:n]
bg = bed + sfx
W = int(0.25 * sr)
def analyse(name, y):
    rows = []
    for i in range(0, n - W, W):
        v, b, o = vt[i:i + W], bg[i:i + W], y[i:i + W]
        A = np.stack([v, b], 1); coef, *_ = np.linalg.lstsq(A, o, rcond=None)
        res = o - A @ coef                                     # what is neither the voice nor the music/SFX
        rows.append((np.sqrt((v ** 2).mean()), np.sqrt((res ** 2).mean()), np.sqrt((o ** 2).mean())))
    r = np.array(rows); sp = r[:, 0] > 0.03; gp = r[:, 0] < 0.002
    to_db = lambda x: 20 * np.log10(np.median(x) + 1e-12)
    print(f"{name:22s} leftover artifact under SPEECH {to_db(r[sp, 1]):6.1f} dBFS ({to_db(r[sp, 1]) - to_db(r[sp, 2]):+5.1f} dB vs the audio) | in GAPS {to_db(r[gp, 1]):6.1f} dBFS")
analyse("mix_ep04.wav (master)", fin)
analyse("export mp4 (AAC)", raw)
# clicks at the VO split points: sample jump at each segment boundary on the timeline
print("\nVO split points (pause starts): level of the voice at the cut, should be ~silence")
for c, p in PAUSES:
    i = int(round(T(c - 1e-4) * sr)); seg = vt[max(0, i - 240):i]; j = int(round(T(c + 1e-4) * sr)); nxt = vt[j:j + 240]
    print(f"  cut at VO {c:7.2f}s: last 5 ms {20*np.log10(np.abs(seg).max()+1e-9):6.1f} dBFS · next 5 ms {20*np.log10(np.abs(nxt).max()+1e-9):6.1f} dBFS")
