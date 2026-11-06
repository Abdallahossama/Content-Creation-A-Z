import json, wave, numpy as np
from faster_whisper import WhisperModel

m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
with wave.open("audio16k.wav") as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
SR = 16000
# chunks split at the measured silences
cuts = [0.0, 2.05, 3.12, 6.73, 9.49, 13.0, 16.3, 21.37, 25.02, 26.75, 31.74, 36.51, 39.39]
out = []
for a, b in zip(cuts, cuts[1:]):
    segs, _ = m.transcribe(audio[int(a*SR):int(b*SR)], language="ar", word_timestamps=True,
                           beam_size=1, condition_on_previous_text=False, vad_filter=False)
    words = []
    for s in segs:
        words += [{"w": w.word.strip(), "s": round(a + w.start, 2), "e": round(a + w.end, 2)} for w in s.words]
    out.append({"s": a, "e": b, "words": words})
    print(f"[{a:5.2f}-{b:5.2f}] " + " ".join(f"{w['w']}({w['s']:.1f})" for w in words))
json.dump(out, open("chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
