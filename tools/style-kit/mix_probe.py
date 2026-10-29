"""QA for any episode mix: music and SFX level under the voice, sub-bass share of the music under the voice, and whether
the final loudnorm pass would have gone dynamic.  python mix_probe.py <build dir> <ep tag>   (e.g. ".../3rd video/build" ep03)
Targets (doc mode and cut & marker alike): music <= -20 dB under the voice, sub<120 Hz <= 0 dB, master static gain."""
import sys, subprocess, json
import numpy as np, soundfile as sf
B, tag = sys.argv[1].rstrip("/\\") + "/", sys.argv[2]
vt, sr = sf.read(B + "vo_timeline.wav", dtype="float64")
vt = vt.mean(1) if vt.ndim == 2 else vt
bed = sf.read(B + f"music_bed_{tag}.wav", dtype="float64", always_2d=True)[0].mean(1)
sfx = sf.read(B + f"sfx_{tag}.wav", dtype="float64", always_2d=True)[0].mean(1)
n = min(len(vt), len(bed), len(sfx)); vt, bed, sfx = vt[:n], bed[:n], sfx[:n]
db = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
on = np.convolve(np.abs(vt) > 0.02, np.ones(int(0.2 * sr)), "same") > 0
def sub(x):
    F = 4096; P = np.mean([np.abs(np.fft.rfft(x[i:i + F] * np.hanning(F))) ** 2 for i in range(0, len(x) - F, F * 4)], 0)
    f = np.fft.rfftfreq(F, 1 / sr); return 10 * np.log10(P[f < 120].sum() / P[(f >= 120) & (f < 8000)].sum())
print(f"{tag}: music under voice {db(bed[on]) - db(vt[on]):+.1f} dB · sub<120Hz {sub(bed[on]):+.1f} dB · SFX under voice {db(sfx[on]) - db(vt[on]):+.1f} dB")
for k in range(0, n // sr - 30, 60):                       # per minute, to find the loud stretches
    w = slice(k * sr, (k + 60) * sr); o = on[w]
    if o.any(): print(f"   {k // 60}:00  music {db(bed[w][o]) - db(vt[w][o]):+5.1f} dB")
src = B + "mix_raw.wav"
j = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(j[j.rindex("{"):j.rindex("}") + 1])
print(f"   raw mix {m['input_i']} LUFS / TP {m['input_tp']} -> loudnorm would run {'DYNAMIC' if float(m['input_tp']) + (-14 - float(m['input_i'])) > -1 else 'linear'}")
