"""phonk: original drift-phonk style beat synthesised from scratch (no samples -> no copyright claims).
808 bass with glide + distortion, cowbell melody (two detuned square tones through a band-pass), kick,
clap on 2 & 4, trap hats with rolls. Also boom() = the 'vine boom' style ending hit.
  from phonk import beat, boom; y = beat(seconds=30, bpm=140, seed=1)   # float32 mono 48 kHz"""
import numpy as np

SR = 48000
NOTES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
def hz(name, octv): return 440.0 * 2 ** ((NOTES[name] + 12 * (octv + 1) - 69) / 12)

def env(n, a=0.002, d=0.2, curve=4.0):
    t = np.arange(n) / SR; e = np.minimum(t / a, 1.0) * np.exp(-t * curve / max(d, 1e-4))
    return e.astype(np.float32)

def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] *= 0.05
    return np.fft.irfft(X, len(x)).astype(np.float32)

def kick(n=int(0.35 * SR)):
    t = np.arange(n) / SR; f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * env(n, 0.001, 0.25, 5) * 1.1).astype(np.float32)

def clap(rng, n=int(0.25 * SR)):
    x = rng.standard_normal(n).astype(np.float32); x = bandpass(x, 900, 5000)
    e = env(n, 0.001, 0.12, 6)
    for k in (0.008, 0.016): s = int(k * SR); e[s:] = np.maximum(e[s:], env(n - s, 0.001, 0.1, 6))
    return x * e * 0.6

def hat(rng, n=int(0.05 * SR), open_=False):
    if open_: n = int(0.2 * SR)
    x = rng.standard_normal(n).astype(np.float32); x = bandpass(x, 7000, 16000)
    return x * env(n, 0.0005, 0.03 if not open_ else 0.15, 8) * 0.35

def cowbell(freq, n=int(0.32 * SR)):
    t = np.arange(n) / SR
    sq = lambda f: np.sign(np.sin(2 * np.pi * f * t))
    x = (sq(freq) + sq(freq * 1.48)) * 0.5
    x = bandpass(x.astype(np.float32), freq * 0.8, freq * 4)
    return x * env(n, 0.001, 0.18, 4) * 0.5

def bass808(f0, f1, n):
    t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t * 18)        # glide into the note
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env(n, 0.003, max(0.3, n / SR), 1.6)
    return np.tanh(x * 2.4).astype(np.float32) * 0.8                    # warm distortion

def beat(seconds=30.0, bpm=140, seed=1, key="F#"):
    rng = np.random.default_rng(seed); n = int(seconds * SR); y = np.zeros(n + SR, np.float32)
    step = 60 / bpm / 4                                                  # 16th note
    def put(x, t, g=1.0):
        i = int(t * SR)
        if i < 0 or i >= n: return
        m = min(len(x), len(y) - i); y[i:i + m] += x[:m] * g
    root = NOTES[key]
    scale = [0, 2, 3, 5, 7, 8, 10]                                       # natural minor
    names = list(NOTES)
    def note(deg, octv):
        s = root + scale[deg % 7] + 12 * (deg // 7); return hz(names[s % 12], octv + s // 12)
    mel = rng.choice([[0, 0, 3, 0, 4, 3, 0, 2], [0, 3, 4, 3, 0, 0, 5, 4], [4, 4, 3, 0, 3, 2, 0, 0]])
    rhythm = [0, 3, 6, 8, 10, 11, 13, 14]                                # classic phonk cowbell syncopation
    bass_pat = [(0, 0), (6, 0), (10, -2), (14, 0)]
    K = kick(); bars = int(seconds / (16 * step)) + 1
    for b in range(bars):
        t0 = b * 16 * step
        for s in (0, 6, 10): put(K, t0 + s * step, 1.0)
        for s in (4, 12): put(clap(rng), t0 + s * step, 0.9)
        for s in range(16):
            roll = (b % 4 == 3 and s >= 12)
            put(hat(rng), t0 + s * step, 0.8 if s % 2 == 0 else 0.5)
            if roll: put(hat(rng), t0 + (s + 0.5) * step, 0.4)
        put(hat(rng, open_=True), t0 + 14 * step, 0.4)
        for i, s in enumerate(rhythm):
            put(cowbell(note(int(mel[i]), 5)), t0 + s * step, 0.55)
        for s, deg in bass_pat:
            dur = 4 * step if s != 14 else 2 * step
            f = note(deg if deg >= 0 else 7 + deg, 1); put(bass808(f * 1.5, f, int(dur * SR)), t0 + s * step, 0.9)
    y = y[:n]
    y = np.tanh(y * 1.3) / np.tanh(1.3)                                  # glue
    return (y / (np.abs(y).max() + 1e-9) * 0.9).astype(np.float32)

def boom(seconds=2.2):
    n = int(seconds * SR); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 1.8) + 0.3 * np.sin(ph * 2) * np.exp(-t * 4)
    nz = np.random.default_rng(3).standard_normal(n) * np.exp(-t * 30) * 0.4
    x = np.tanh((x + nz) * 2.0)
    for d, g in ((0.09, 0.35), (0.21, 0.22), (0.37, 0.12)):               # cheap room tail
        s = int(d * SR); x[s:] += x[:-s] * g
    return (x / np.abs(x).max() * 0.95).astype(np.float32)

if __name__ == "__main__":
    import soundfile as sf
    sf.write("F:/speed-gta6/tools/_phonk_test.wav", beat(20, 140, 1), SR); sf.write("F:/speed-gta6/tools/_boom_test.wav", boom(), SR); print("ok")
