"""Transcribe the leveled VO in 3 slices (RAM limit), stitch word timestamps back onto the full timeline.
Run from D:/why habibi/3rd video/build."""
import json, subprocess, sys
from faster_whisper import WhisperModel
import soundfile as sf
SRC = "../vo/ep03_VO_leveled_-16LUFS.wav"
CUTS = [(0.0, 153.36), (154.06, 305.26), (305.96, 414.28)]       # part boundaries incl. the 0.7 s seams
m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=4)
res = []
for i, (a, b) in enumerate(CUTS):
    wav = f"slice{i + 1}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", SRC, "-ac", "1", "-ar", "16000", wav], check=True)
    audio, _ = sf.read(wav, dtype="float32")
    segs, _ = m.transcribe(audio, word_timestamps=True, beam_size=5, vad_filter=False, condition_on_previous_text=True)
    for s in segs:
        res.append({"start": s.start + a, "end": s.end + a, "text": s.text,
                    "words": [{"w": w.word, "s": w.start + a, "e": w.end + a, "p": w.probability} for w in s.words]})
        print(f"{s.start + a:7.2f}-{s.end + a:7.2f} {s.text}", flush=True)
json.dump(res, open("vo_words.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("DONE")
