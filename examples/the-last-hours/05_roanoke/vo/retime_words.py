"""After fix_lines.py splices new takes: re-base every line's start to the new vo.log durations and re-transcribe the given lines."""
import re, sys, json
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
ROOT = "D:/why habibi/_newchannel/05_roanoke/"; V = ROOT + "vo/"
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES, PAUSE = [], []
for l in RAW:
    if l == "##":
        if PAUSE: PAUSE[-1] = 0.9
    else: LINES.append(l); PAUSE.append(0.35)
durs = {int(m.group(1)) - 1: float(m.group(3)) for m in re.finditer(r"^(\d+)/(\d+)\s+([\d.]+)s audio", open(V + "vo.log", encoding="utf-8", errors="ignore").read(), re.M)}
starts = []; t = 0.0
for i in range(len(LINES)): starts.append(t); t += durs[i] + PAUSE[i]
data = json.load(open(V + "vo_words.json", encoding="utf-8")); redo = [int(x) for x in sys.argv[1:]]
full, sr = sf.read(V + "roanoke_vo_chatterbox.wav", dtype="float32")
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8) if redo else None
for sg in data:
    i = sg["line"]; t0 = starts[i]
    if i in redo:
        a = full[int(t0 * sr): int((t0 + durs[i]) * sr)]; a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
        segs, _ = wm.transcribe(a16, word_timestamps=True, beam_size=5, condition_on_previous_text=False)
        sg["words"] = [{"w": w.word, "s": round(w.start + t0, 3), "e": round(w.end + t0, 3), "p": round(w.probability, 3)} for x in segs for w in x.words]
        print(i, " ".join(w["w"] for w in sg["words"]))
    else:
        d = t0 - sg["start"]
        for w in sg["words"]: w["s"] = round(w["s"] + d, 3); w["e"] = round(w["e"] + d, 3)
    sg["start"] = t0
json.dump(data, open(V + "vo_words.json", "w", encoding="utf-8"), indent=1); print("retimed, total", round(t, 2))
