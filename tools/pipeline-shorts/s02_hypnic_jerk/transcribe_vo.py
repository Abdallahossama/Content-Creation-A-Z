import json, subprocess, sys
from faster_whisper import WhisperModel
import soundfile as sf
src, out = sys.argv[1], sys.argv[2]; wav = out + ".16k.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
a, _ = sf.read(wav, dtype="float32")
segs, _ = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8).transcribe(a, word_timestamps=True, beam_size=5, condition_on_previous_text=False)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]})
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}")
json.dump(res, open(out, "w", encoding="utf-8"), indent=1)
