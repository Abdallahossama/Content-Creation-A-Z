"""Word timestamps for the Short VO (56 s, one slice). Writes build/vo_words.json."""
import json, subprocess
from faster_whisper import WhisperModel
import soundfile as sf
B = "D:/why habibi/shorts/s01_hormuz/build/"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "D:/why habibi/shorts/s01_hormuz/vo/s01_vo.mp3", "-ac", "1", "-ar", "16000", B + "vo16k.wav"], check=True)
audio, _ = sf.read(B + "vo16k.wav", dtype="float32")
m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(audio, word_timestamps=True, beam_size=5, vad_filter=False)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]})
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}", flush=True)
json.dump(res, open(B + "vo_words.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("DONE")
