"""crazy: rank 'Speed goes crazy' moments in long streams by SCREAM energy, not just loudness.
Per 0.5 s: absolute level (dBFS) and brightness (share of energy above 1.2 kHz - screams/yells are bright).
scream = max(0, dB - floor) * brightness, summed over ~6 s; floor = stream's 90th-percentile level, so only
peaks well above his normal shouting count. Top N moments across all streams, >= GAP s apart.
  python crazy.py <out.json> <audio1> [audio2 ...]"""
import sys, json, subprocess
import numpy as np

SR, HOP, GAP, N = 8000, 0.5, 120, 40
out = sys.argv[1]; res = []
for src in sys.argv[2:]:
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], stdout=subprocess.PIPE)
    h = int(SR * HOP); db, br = [], []
    win = np.hanning(h).astype(np.float32); freqs = np.fft.rfftfreq(h, 1 / SR); hi = freqs > 1200
    while True:
        b = p.stdout.read(h * 2 * 2400)
        if not b: break
        a = np.frombuffer(b, np.int16).astype(np.float32) / 32768; n = len(a) // h
        if n == 0: break
        fr = a[: n * h].reshape(n, h)
        db.append(10 * np.log10((fr ** 2).mean(1) + 1e-10))
        sp = np.abs(np.fft.rfft(fr * win, axis=1)) ** 2
        br.append(sp[:, hi].sum(1) / (sp.sum(1) + 1e-10))
    db, br = np.concatenate(db), np.concatenate(br)
    floor = np.percentile(db, 90)
    s = np.maximum(db - floor, 0) * br
    k = int(6 / HOP); s = np.convolve(s, np.ones(k), "same")
    vid = src.split("/")[-1].split("\\")[-1].split(".")[0]
    for _ in range(N):
        i = int(np.argmax(s))
        if s[i] <= 0: break
        res.append(dict(vid=vid, t=round(i * HOP, 1), score=round(float(s[i]), 2), peak_db=round(float(db[max(0, i - k):i + k].max()), 1)))
        lo, hi2 = max(0, i - int(GAP / HOP)), min(len(s), i + int(GAP / HOP)); s[lo:hi2] = 0
    print(vid, "frames", len(db), "floor dB", round(float(floor), 1), flush=True)
res.sort(key=lambda r: -r["score"])
json.dump(res, open(out, "w"), indent=1)
for r in res[:40]: print(f"{r['vid']} {int(r['t'] // 3600)}:{int(r['t'] % 3600 // 60):02d}:{int(r['t'] % 60):02d}  {r['score']:7.1f}  peak {r['peak_db']}")
