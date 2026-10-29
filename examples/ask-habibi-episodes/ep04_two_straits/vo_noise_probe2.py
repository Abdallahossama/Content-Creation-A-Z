"""Direct comparison: is the joined/leveled VO the same signal as the ElevenLabs mp3 (just louder)?
Also: noise floor in absolute terms inside the natural word gaps, per file, using the SAME gap windows for all."""
import subprocess
import numpy as np
SR = 44100
V = "D:/why habibi/4th video/vo/"
def dec(p, ch=1):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"],
                                     capture_output=True).stdout, np.float32).astype(np.float64)
    return a
info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=channels,sample_rate,bit_rate,codec_name", "-of", "compact",
                       V + "ep04_vo_part1.mp3"], capture_output=True, text=True).stdout.strip()
print("part1:", info)
p1 = dec(V + "ep04_vo_part1.mp3"); j = dec(V + "ep04_vo_joined.wav"); L = dec(V + "ep04_VO_leveled_-16LUFS.wav")
n = min(len(p1), len(j)); k = np.dot(p1[:n], j[:n]) / np.dot(p1[:n], p1[:n])
res = j[:n] - k * p1[:n]
print(f"joined vs part1: scale {k:.4f} ({20*np.log10(abs(k)):+.2f} dB), residual {20*np.log10(np.sqrt((res**2).mean())/np.sqrt((j[:n]**2).mean())):.1f} dB rel. signal")
w = int(0.03 * SR); m = n // w
def rms_db(x): return 20 * np.log10(np.sqrt((x[:m * w].reshape(m, w) ** 2).mean(1) + 1e-14))
ref = rms_db(p1[:n]); loud = np.percentile(ref, 90)
gaps = (ref < loud - 30) & (ref > -100)                      # windows that are quiet in the ORIGINAL
print(f"{gaps.sum()} gap windows (of {m}); original speech loud90 {loud:.1f} dBFS")
for name, x in (("part1.mp3", p1[:n]), ("joined.wav", j[:n]), ("leveled.wav (new)", L[:n])):
    d = rms_db(x); print(f"  {name:20s} speech {np.percentile(d, 90):6.1f}  gaps median {np.median(d[gaps]):6.1f}  -> gap {np.median(d[gaps]) - np.percentile(d, 90):6.1f} dB under speech")
