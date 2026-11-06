import json, sys
from faster_whisper import WhisperModel

model_name = sys.argv[1] if len(sys.argv) > 1 else "small"
m = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4)
import wave, numpy as np
with wave.open("audio16k.wav") as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segs, info = m.transcribe(audio, language="ar", word_timestamps=True,
                          vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300), beam_size=1, condition_on_previous_text=False,
                          )
out = []
for s in segs:
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for w in s.words]
    out.append({"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip(), "words": words})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
json.dump(out, open(f"words_{model_name}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
