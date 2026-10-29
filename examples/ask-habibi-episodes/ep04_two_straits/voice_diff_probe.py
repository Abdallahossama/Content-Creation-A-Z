"""How different is the voice in the video from the ElevenLabs file? Sub-sample alignment (FFT phase shift), then per
0.25 s window: the gain my processing applied there, and what is left after removing that gain (= distortion /
anything added). Transparent processing leaves < -40 dB."""
import subprocess
import numpy as np
SR = 48000
def dec(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                        capture_output=True).stdout, np.float32).astype(np.float64)
o = dec("D:/why habibi/4th video/vo/ep04_vo_joined.wav")
L = dec("D:/why habibi/4th video/vo/ep04_VO_leveled_-16LUFS.wav")
n = min(len(o), len(L)); o, L = o[:n], L[:n]
# integer + fractional lag from the cross-correlation peak (parabolic), over 20 s of speech
a, b = L[10 * SR:30 * SR], o[10 * SR:30 * SR]
F = np.fft.rfft(a, 2 * len(a)) * np.conj(np.fft.rfft(b, 2 * len(a))); cc = np.fft.irfft(F)
cc = np.concatenate([cc[-300:], cc[:301]]); i = int(np.argmax(cc)); y0, y1, y2 = cc[i - 1], cc[i], cc[i + 1]
lag = (i - 300) + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
f = np.fft.rfftfreq(n, 1 / SR); o = np.fft.irfft(np.fft.rfft(o) * np.exp(-2j * np.pi * f * lag / SR), n)
db = lambda x: 10 * np.log10((x ** 2).mean() + 1e-20)
w = SR // 4; rows = []
for k in range(n // w):
    s = slice(k * w, (k + 1) * w); x, y = o[s], L[s]
    if db(y) < -40: continue
    g = np.dot(x, y) / np.dot(x, x); r = y - g * x
    rows.append((20 * np.log10(abs(g)), db(r) - db(y)))
r = np.array(rows); g0 = np.median(r[:, 0])
print(f"lag {lag:.2f} samples · typical gain {g0:+.2f} dB")
print(f"limiter: windows pulled down >1 dB below the typical gain {np.mean(r[:, 0] < g0 - 1) * 100:.1f}%, >3 dB {np.mean(r[:, 0] < g0 - 3) * 100:.1f}%")
print(f"left after removing the gain (distortion/added sound): median {np.median(r[:, 1]):.1f} dB, worst 5% {np.percentile(r[:, 1], 95):.1f} dB, worst {r[:, 1].max():.1f} dB under the voice")
