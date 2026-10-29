"""Two suspects for the 'whoosh when I speak':
1) the peak limiter on the voice: how much gain reduction, how often (leveled vs joined * static gain)
2) the music ducking: how often and how deep the music level moves while the voice is speaking"""
import subprocess
import numpy as np, soundfile as sf
V = "D:/why habibi/4th video/vo/"; B = "D:/why habibi/4th video/build/"
def dec(p, sr=48000):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                                        capture_output=True).stdout, np.float32).astype(np.float64)
j = dec(V + "ep04_vo_joined.wav"); L = dec(V + "ep04_VO_leveled_-16LUFS.wav")
n = min(len(j), len(L)); j, L = j[:n], L[:n]
w = int(0.01 * 48000); m = n // w
pk = lambda x: np.abs(x[:m * w]).reshape(m, w).max(1)
pj, pl = pk(j), pk(L); act = pj > 0.01
k = np.median(pl[act & (pj < 0.05)] / pj[act & (pj < 0.05)])          # static gain where the limiter is idle
gr = 20 * np.log10(np.maximum(pl[act], 1e-9) / (k * pj[act]))
print(f"voice: static gain {20*np.log10(k):+.1f} dB; limiter gain reduction while speaking: "
      f"median {np.median(gr):.1f} dB, >1 dB in {np.mean(gr < -1)*100:.0f}% of 10 ms windows, >3 dB in {np.mean(gr < -3)*100:.0f}%, max {gr.min():.1f} dB")
# music level movement under the voice: 50 ms RMS of the bed, how much it moves within speech
vt, sr = sf.read(B + "vo_timeline.wav", dtype="float64"); bed = sf.read(B + "music_bed_ep04.wav", dtype="float64", always_2d=True)[0].mean(1)
q = int(0.05 * sr); M = min(len(vt), len(bed)) // q
vr = np.sqrt((vt[:M * q].reshape(M, q) ** 2).mean(1)); br = 20 * np.log10(np.sqrt((bed[:M * q].reshape(M, q) ** 2).mean(1)) + 1e-9)
sp = vr > 0.01
swing = np.abs(np.diff(br))[sp[1:] & sp[:-1]]
print(f"music under the voice: moves more than 3 dB per 50 ms in {np.mean(swing > 3)*100:.1f}% of steps, >6 dB in {np.mean(swing > 6)*100:.1f}%")
