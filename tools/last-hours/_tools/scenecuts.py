"""Frame-difference shot boundaries in a window: python scenecuts.py <video> <t0> <t1>"""
import sys, subprocess, numpy as np
p, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); fps = 30
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", p, "-t", str(t1 - t0), "-vf", "scale=96:54,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2)); m = a.mean(axis=(1, 2))
for i, v in enumerate(d):
    if v > 6: print(f"cut at {t0 + (i + 1) / fps:.2f}  diff {v:.1f}  mean {m[i]:.0f}->{m[i+1]:.0f}")
