"""Count hard-clipped runs (3+ consecutive samples at full scale) per channel, and where they fall (voice on/off)."""
import subprocess, sys
import numpy as np
import soundfile as sf
B = "D:/why habibi/4th video/build/"
vt, sr = sf.read(B + "vo_timeline.wav", dtype="float32")
def runs(x, thr=0.999):
    hit = np.abs(x) >= thr; d = np.diff(np.concatenate([[0], hit.astype(np.int8), [0]]))
    s, e = np.where(d == 1)[0], np.where(d == -1)[0]; keep = (e - s) >= 3
    return s[keep], e[keep]
for name in ("mix_raw.wav", "mix_ep04.wav"):
    x, sr = sf.read(B + name, dtype="float32", always_2d=True)
    for ch in range(x.shape[1]):
        s, e = runs(x[:, ch])
        voiced = sum(1 for a in s if np.abs(vt[max(0, a - 480):a + 480]).max() > 0.05) if len(s) else 0
        print(f"{name} ch{ch}: {len(s)} clipped runs (3+ samples), {voiced} of them while the voice is speaking; "
              f"max |x| {np.abs(x[:, ch]).max():.4f}; first at {[round(a / sr, 2) for a in s[:6]]}")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "D:/why habibi/4th video/export/Ask_Habibi_Ep4_1440p.mp4", "-f", "f32le",
                      "-ac", "2", "-ar", "48000", "-"], capture_output=True).stdout
y = np.frombuffer(raw, np.float32).reshape(-1, 2)
print("export AAC decoded: max |x|", round(float(np.abs(y).max()), 4), "| samples over 0.999:", int((np.abs(y) >= 0.999).sum()))
