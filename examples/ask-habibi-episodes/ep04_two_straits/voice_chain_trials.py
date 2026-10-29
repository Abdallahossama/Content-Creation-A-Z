"""Try gentler voice chains on the ElevenLabs file and keep the most transparent one. For each: integrated loudness, true
peak, and how much is left after removing the (slow) gain per 0.25 s window: what the ear hears as artifacts."""
import subprocess, sys, os
import numpy as np
sys.path.insert(0, "D:/why habibi/_style_kit/tools"); import audio_master as am
SR = 48000; V = "D:/why habibi/4th video/vo/"; SRC = V + "ep04_vo_joined.wav"; TMP = "D:/why habibi/4th video/build/voice_trials/"
os.makedirs(TMP, exist_ok=True)
def dec(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                        capture_output=True).stdout, np.float32).astype(np.float64)
O = dec(SRC)
def artifacts(path):
    L = dec(path); n = min(len(O), len(L)); o, y = O[:n], L[:n]
    a, b = y[10 * SR:30 * SR], o[10 * SR:30 * SR]
    F = np.fft.rfft(a, 2 * len(a)) * np.conj(np.fft.rfft(b, 2 * len(a))); cc = np.fft.irfft(F)
    cc = np.concatenate([cc[-300:], cc[:301]]); i = int(np.argmax(cc)); y0, y1, y2 = cc[i - 1], cc[i], cc[i + 1]
    lag = (i - 300) + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    f = np.fft.rfftfreq(n, 1 / SR); o = np.fft.irfft(np.fft.rfft(o) * np.exp(-2j * np.pi * f * lag / SR), n)
    db = lambda x: 10 * np.log10((x ** 2).mean() + 1e-20); w = SR // 4; res = []
    for k in range(n // w):
        s = slice(k * w, (k + 1) * w); x, z = o[s], y[s]
        if db(z) < -40: continue
        g = np.dot(x, z) / np.dot(x, x); res.append(db(z - g * x) - db(z))
    res = np.array(res); return np.median(res), np.percentile(res, 95), res.max()
I0, P0 = am.measure(SRC)
CH = {
    "now: fast limiter (0.5/60 ms)": lambda g: f"volume={g}dB,aresample=192000,alimiter=limit=0.84140:attack=0.5:release=60:level=disabled,aresample=48000",
    "slow limiter (5/400 ms)": lambda g: f"volume={g}dB,aresample=192000,alimiter=limit=0.84140:attack=5:release=400:level=disabled,aresample=48000",
    "gentle comp 2:1 + slow limiter": lambda g: (f"acompressor=threshold=-24dB:ratio=2:attack=15:release=300:knee=6:makeup=1,volume={g}dB,"
                                                 f"aresample=192000,alimiter=limit=0.84140:attack=5:release=400:level=disabled,aresample=48000"),
    "slow limiter, 2 dB quieter (-18)": lambda g: f"volume={g - 2}dB,aresample=192000,alimiter=limit=0.84140:attack=5:release=400:level=disabled,aresample=48000",
}
print(f"ElevenLabs file: {I0:.1f} LUFS / {P0:.1f} dBTP")
for k, (name, chain) in enumerate(CH.items()):
    out = TMP + f"trial_{k}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-af", chain(round(-16 - I0, 2)), "-ar", str(SR), "-c:a", "pcm_s24le", out], check=True)
    I, P = am.measure(out); med, p95, worst = artifacts(out)
    print(f"{k} {name:34s} {I:6.1f} LUFS {P:5.1f} dBTP | artifacts median {med:6.1f}  worst 5% {p95:6.1f}  worst {worst:6.1f} dB")
