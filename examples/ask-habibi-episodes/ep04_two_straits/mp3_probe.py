"""Is the ElevenLabs MP3 itself the source? Lossy-codec 'swish' shows up as: a hard lowpass, and in the high band (6-15 kHz)
many spectral bins switching on/off from frame to frame (holes), most of all on s-sounds and breaths."""
import subprocess, json
import numpy as np
V = "D:/why habibi/4th video/vo/"
for f in ("ep04_vo_part1.mp3", "ep04_vo_part2.mp3"):
    print(f, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate:format=bit_rate",
                             "-of", "compact", V + f], capture_output=True, text=True).stdout.strip().replace("\n", " | "))
SR = 44100
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", V + "ep04_vo_part1.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                 capture_output=True).stdout, np.float32).astype(np.float64)
N = 1024; H = 512; m = (len(x) - N) // H
S = np.abs(np.array([np.fft.rfft(x[i * H:i * H + N] * np.hanning(N)) for i in range(m)])) ** 2
fq = np.fft.rfftfreq(N, 1 / SR); lvl = 10 * np.log10(S.sum(1) + 1e-14); act = lvl > np.percentile(lvl, 50)
spec = 10 * np.log10(S[act].mean(0) + 1e-20)
cut = fq[np.max(np.flatnonzero(spec > spec[(fq > 1000) & (fq < 4000)].mean() - 60))]
print(f"effective bandwidth (lowpass) ~{cut / 1000:.1f} kHz")
band = (fq > 6000) & (fq < 15000); Sb = S[act][:, band]; ref = Sb.max(1, keepdims=True)
holes = (Sb < ref * 1e-6)                                           # bins 60 dB under the frame's loudest = switched off
flip = np.mean(holes[1:] != holes[:-1])
print(f"6-15 kHz while speaking: {holes.mean() * 100:.1f}% of bins switched off, {flip * 100:.1f}% flip on/off frame to frame")
