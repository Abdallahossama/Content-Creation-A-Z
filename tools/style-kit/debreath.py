"""De-breath an ElevenLabs VO: turn the inhales / air bursts between phrases down (default 15 dB), never the words.

Why: ElevenLabs voices put a breath before most phrases, only ~16 dB under the words. At YouTube loudness each one reads
as "a whoosh when I speak" (Ep 4, 2026-10-12: 141 breaths in 5 minutes).
How: 20 ms frames. Words = frames within 14 dB of the typical word level. In each gap of 0.25-1.5 s between words, the
frames that are noisy (spectral flatness > 0.06, i.e. air, not voice) are turned down. 100 ms at both ends of every gap
are protected, so word onsets and endings (s, f, h, t) are never touched. 15 ms raised-cosine fades. Length unchanged.

  python debreath.py in.wav out.wav [depth_db]"""
import subprocess, sys
import numpy as np
import soundfile as sf

W = 960   # 20 ms at 48 kHz

def analyse(x, sr):
    w = int(0.02 * sr); m = len(x) // w; f = x[:m * w].reshape(m, w)
    rms = 10 * np.log10((f ** 2).mean(1) + 1e-14)
    P = np.abs(np.fft.rfft(f * np.hanning(w), axis=1)) ** 2 + 1e-18; fq = np.fft.rfftfreq(w, 1 / sr); b = (fq > 300) & (fq < 8000)
    flat = np.exp(np.log(P[:, b]).mean(1)) / P[:, b].mean(1)
    return w, rms, flat

def breath_frames(x, sr, min_gap=0.25, max_gap=1.5, protect=0.10):
    w, rms, flat = analyse(x, sr); sp = np.median(rms[rms > np.percentile(rms, 60)])
    voiced = rms > sp - 14; n = len(rms); hit = np.zeros(n, bool); pr = int(round(protect / 0.02)); events = 0
    i = 0
    while i < n:
        if voiced[i]: i += 1; continue
        j = i
        while j < n and not voiced[j]: j += 1
        if min_gap / 0.02 <= j - i <= max_gap / 0.02 and i > 0 and j < n:
            a, b = i + pr, j - pr
            if b > a:
                m = (flat[a:b] > 0.06) & (rms[a:b] > sp - 45) & (rms[a:b] < sp - 8)
                if m.any(): hit[a:b] |= m; events += 1
        i = j
    return w, hit, voiced, events, sp

def debreath(src, dst, depth_db=15.0):
    x, sr = sf.read(src, dtype="float64"); mono = x if x.ndim == 1 else x.mean(1)
    w, hit, voiced, events, sp = breath_frames(mono, sr)
    g = np.ones(len(hit)); g[hit] = 10 ** (-depth_db / 20)
    gs = np.repeat(g, w); gs = np.concatenate([gs, np.ones(len(mono) - len(gs))])
    k = np.hanning(int(0.03 * sr)); k /= k.sum(); gs = np.convolve(gs, k, "same")
    vs = np.repeat(voiced, w); vs = np.concatenate([vs, np.zeros(len(mono) - len(vs), bool)])
    assert np.all(gs[vs] > 0.999), "a word would be touched"
    y = x * (gs if x.ndim == 1 else gs[:, None])
    sf.write(dst, y, sr, subtype="PCM_24")
    print(f"{dst}: {events} breaths turned down {depth_db:.0f} dB ({hit.sum() * 0.02:.1f} s of air); words untouched")
    return events

if __name__ == "__main__":
    debreath(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 15.0)
