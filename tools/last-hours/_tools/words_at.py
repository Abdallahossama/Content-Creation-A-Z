"""Word-level timings in a window of a finished video: python words_at.py <video> <t0> <t1>"""
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
path, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", path, "-t", str(t1 - t0), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.float32)
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=8)
segs, _ = m.transcribe(a, beam_size=3, word_timestamps=True)
for s in segs:
    print(" ".join(f"{w.word.strip()}@{w.start + t0:.2f}-{w.end + t0:.2f}" for w in s.words))
