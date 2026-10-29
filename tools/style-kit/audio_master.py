"""Clean loudness for Ask Habibi audio: STATIC gain + a peak limiter, never ffmpeg loudnorm on its own.

Why: loudnorm with linear=true silently falls back to DYNAMIC mode when the gain it needs would push the true peak over
its TP target. ElevenLabs files peak around -1 dBFS, so that fallback happened on every VO we leveled: dynamic mode is a
slow compressor that lifted the hiss/breaths between words by ~20 dB ("noise when I speak", Ep 4, 2026-10-12).

  level(src, dst, target=-16, tp=-1.5)   VO: measure, one gain, limiter (4x oversampled) on the few peaks over tp
  master(src, dst, target=-14, tp=-1)    final mix, same method; write the raw mix as FLOAT so nothing clips before this
  gap_floor(path)                        QA: median level of the gaps between words relative to speech (dB, lower = cleaner)

CLI:  python audio_master.py level in.wav out.wav [-16]   |   python audio_master.py master in.wav out.wav [-14]
      python audio_master.py check file.wav"""
import subprocess, sys
import numpy as np

SR = 48000

def measure(path):
    """integrated loudness (LUFS) and true peak (dBTP) via ebur128"""
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr.splitlines()
    i = [l for l in o if l.strip().startswith("I:")][-1].split()[1]
    p = [l for l in o if l.strip().startswith("Peak:")][-1].split()[1]
    return float(i), float(p)

def _apply(src, dst, target, tp, codec):
    I, P = measure(src); g = target - I
    lim = 10 ** (tp / 20)
    af = (f"volume={g:.3f}dB,aresample=192000,alimiter=limit={lim:.5f}:attack=0.5:release=60:level=disabled,"
          f"aresample={SR}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ar", str(SR), "-c:a", codec, dst], check=True)
    I2, P2 = measure(dst)
    print(f"{dst}: in {I:.2f} LUFS / {P:.2f} dBTP  ->  gain {g:+.2f} dB  ->  {I2:.2f} LUFS / {P2:.2f} dBTP")
    return I2, P2

def gain_only(src, dst, target=-14.0, tp=-1.0):
    """plain volume, NO limiter: as close to target as the true peak allows. Use when the voice must not be squashed
    (Ep 4: a limiter on the cloned voice made 'a whoosh when I speak', 2026-10-12)."""
    I, P = measure(src); g = min(target - I, tp - P)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"volume={g:.3f}dB", "-ar", str(SR), "-c:a", "pcm_s24le", dst], check=True)
    I2, P2 = measure(dst)
    print(f"{dst}: in {I:.2f} LUFS / {P:.2f} dBTP  ->  plain gain {g:+.2f} dB, no limiter  ->  {I2:.2f} LUFS / {P2:.2f} dBTP")
    return I2, P2

def level(src, dst, target=-16.0, tp=-1.5): return _apply(src, dst, target, tp, "pcm_s24le")
def master(src, dst, target=-14.0, tp=-1.0): return _apply(src, dst, target, tp, "pcm_s24le")

def dec(path, ch=1):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"],
                                     capture_output=True).stdout, np.float32)
    return a.reshape(-1, ch) if ch > 1 else a

def gap_floor(path):
    """median RMS of the 30 ms windows more than 25 dB under the loud speech, relative to that speech (dB)"""
    x = dec(path).astype(np.float64); w = int(0.03 * SR); n = len(x) // w
    db = 20 * np.log10(np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1) + 1e-12))
    loud = np.percentile(db, 90); g = db[(db < loud - 25) & (db > -110)]
    return float(np.median(g) - loud) if len(g) else -99.0

def peak_dbfs(path):
    x = dec(path, 2); return float(20 * np.log10(np.abs(x).max() + 1e-12))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "level": level(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else -16.0)
    elif cmd == "master": master(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else -14.0)
    elif cmd == "check":
        for p in sys.argv[2:]: print(f"{p}: gap floor {gap_floor(p):6.1f} dB under speech · sample peak {peak_dbfs(p):5.2f} dBFS · {measure(p)}")
