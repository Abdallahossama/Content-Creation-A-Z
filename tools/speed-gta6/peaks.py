"""peaks: find the hype moments in a long stream from its audio alone.
Score = short loudness (2 s) over the local norm (rolling 5-min median), smoothed. Picks the top N windows,
at least GAP seconds apart. Prints start/end (seconds) of each candidate clip.
  python peaks.py <audio file> [N=20] [clip_len=45] > peaks.json"""
import sys, json, subprocess
import numpy as np

src = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 20; L = float(sys.argv[3]) if len(sys.argv) > 3 else 45
SR = 8000; HOP = 0.5; GAP = 150
p = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True)
a = np.frombuffer(p.stdout, np.int16).astype(np.float32) / 32768
h = int(SR * HOP); n = len(a) // h
rms = np.sqrt((a[: n * h].reshape(n, h) ** 2).mean(1) + 1e-9)
db = 20 * np.log10(rms)
def roll(x, w, fn):
    w = max(1, int(w)); pad = np.pad(x, (w // 2, w - w // 2 - 1), mode="edge")
    from numpy.lib.stride_tricks import sliding_window_view as sw
    return fn(sw(pad, w), axis=1)
short = roll(db, 2 / HOP, np.mean)                 # 2 s loudness
norm = roll(db[::20], 300 / HOP / 20, np.median)   # 5-min median (downsampled for speed)
norm = np.interp(np.arange(n), np.arange(0, n, 20)[: len(norm)], norm)
burst = roll(np.maximum(short - norm, 0), 8 / HOP, np.mean)   # sustained excitement over ~8 s
score = burst.copy(); picks = []
for _ in range(N):
    i = int(np.argmax(score))
    if score[i] <= 0: break
    t = i * HOP; picks.append(dict(peak=round(t, 1), start=round(max(0, t - L * 0.55), 1), end=round(t + L * 0.45, 1), score=round(float(score[i]), 2)))
    lo, hi = max(0, i - int(GAP / HOP)), min(n, i + int(GAP / HOP)); score[lo:hi] = 0
picks.sort(key=lambda d: -d["score"])
print(json.dumps(dict(src=src, duration=round(n * HOP, 1), picks=picks), indent=1))
