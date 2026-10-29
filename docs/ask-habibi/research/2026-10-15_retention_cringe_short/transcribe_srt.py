import sys, subprocess
from faster_whisper import WhisperModel
import soundfile as sf
src, out = sys.argv[1], sys.argv[2]; wav = out + ".16k.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
a, _ = sf.read(wav, dtype="float32")
segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(a, word_timestamps=True)
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02d}:{m:02d}:{int(s):02d},{int((s%1)*1000):03d}"
n = 0; lines = []
for s in segs:
    for w in s.words:
        pass
    n += 1; lines.append(f"{n}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n"); print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}")
open(out, "w", encoding="utf-8").write("\n".join(lines))
