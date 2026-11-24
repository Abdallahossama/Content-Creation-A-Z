import sys, json, subprocess
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    aud = np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    segs, _ = m.transcribe(aud, word_timestamps=True, vad_filter=True, initial_prompt="IShowSpeed, GTA 6, Vice City, chat, bro")
    out = [dict(w=w.word, s=round(w.start, 2), e=round(w.end, 2), p=round(w.probability, 3)) for s in segs for w in (s.words or [])]
    json.dump(out, open(f.replace(".mp4", ".words.json"), "w", encoding="utf-8"))
    print("\n==", f); print(" ".join(f"[{w['s']:.0f}]{w['w'].strip()}" if i % 8 == 0 else w["w"].strip() for i, w in enumerate(out)))
