"""How much plain gain can the untouched voice take? Peaks of every 10 ms speech window; for each candidate gain, how many
windows would go over -1 dBFS (i.e. would need any limiting at all)."""
import subprocess
import numpy as np
SR = 48000
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "D:/why habibi/4th video/vo/ep04_vo_joined.wav", "-f", "f32le",
                                  "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.float32).astype(np.float64)
w = SR // 100; m = len(x) // w; pk = 20 * np.log10(np.abs(x[:m * w]).reshape(m, w).max(1) + 1e-12)
sp = pk[pk > -40]
print(f"speech windows {len(sp)} · peak percentiles: 50% {np.percentile(sp, 50):.1f}  90% {np.percentile(sp, 90):.1f}  "
      f"99% {np.percentile(sp, 99):.1f}  99.9% {np.percentile(sp, 99.9):.1f}  max {sp.max():.1f} dBFS")
for g in (0, 1, 2, 3, 4, 5, 6, 7.7):
    over = sp + g > -1.0
    print(f"  +{g:3.1f} dB -> voice about {-23.7 + g:6.1f} LUFS · windows over -1 dBFS: {over.sum():5d} ({over.mean() * 100:5.2f}%)")
