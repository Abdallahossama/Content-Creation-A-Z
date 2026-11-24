"""words: word timestamps for a clip (faster-whisper medium.en, CPU).
  uv run --no-project --with faster-whisper python words.py <media> <out.json>"""
import sys, json, subprocess
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
aud = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout, np.float32); segs, _ = m.transcribe(aud, word_timestamps=True, vad_filter=True, initial_prompt="IShowSpeed, GTA 6, Vice City, Lucia, Jason, chat, bro")
out = [dict(w=w.word, s=round(w.start, 2), e=round(w.end, 2), p=round(w.probability, 3)) for s in segs for w in (s.words or [])]
json.dump(out, open(sys.argv[2], "w", encoding="utf-8")); print(len(out), "words", " ".join(w["w"].strip() for w in out)[:400])
