"""Whisper each narration line on its own slice: word timings on the VO clock (vo_words.json) + a per-line match score
against the script (qa_lines.txt), so misread lines can be re-voiced with fix_lines.py."""
import re, json, difflib
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
ROOT = "D:/why habibi/_newchannel/03_franklin/"; V = ROOT + "vo/"
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES, PAUSE = [], []
for l in RAW:
    if l == "##":
        if PAUSE: PAUSE[-1] = 0.9
    else: LINES.append(l); PAUSE.append(0.35)
durs = {int(m.group(1)) - 1: float(m.group(3)) for m in re.finditer(r"^(\d+)/(\d+)\s+([\d.]+)s audio", open(V + "vo.log", encoding="utf-8", errors="ignore").read(), re.M)}
full, sr = sf.read(V + "franklin_vo_chatterbox.wav", dtype="float32")
if full.ndim > 1: full = full.mean(1)
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
NUM = {"1845": "eighteen forty five", "1846": "eighteen forty six", "1847": "eighteen forty seven", "1848": "eighteen forty eight", "1859": "eighteen fifty nine",
       "1854": "eighteen fifty four", "2014": "twenty fourteen", "2016": "twenty sixteen", "2019": "twenty nineteen", "2021": "twenty twenty one"}
def norm(s):
    s = s.lower().replace("'", "").replace("-", " ")
    for k, v in NUM.items(): s = s.replace(k, v)
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
out, rep = [], []; t = 0.0
for i, line in enumerate(LINES):
    a = full[int(t * sr): int((t + durs[i]) * sr)]; a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
    segs, _ = wm.transcribe(a16, word_timestamps=True, beam_size=5, condition_on_previous_text=False, initial_prompt="Franklin, Erebus, Terror, Crozier, Fitzjames, Beechey, Peglar, Hobson, McClintock, Kogvik, Inuit, Inuk.")
    ws, txt = [], []
    for sg in segs:
        txt.append(sg.text)
        for w in sg.words: ws.append({"w": w.word, "s": round(w.start + t, 3), "e": round(w.end + t, 3), "p": round(w.probability, 3)})
    hyp = " ".join(txt).strip(); r = difflib.SequenceMatcher(a=norm(line), b=norm(hyp)).ratio()
    out.append({"line": i, "start": t, "words": ws}); rep.append((r, i, line, hyp)); print(f"{i:3d} {r:.3f} {hyp}", flush=True)
    t += durs[i] + PAUSE[i]
json.dump(out, open(V + "vo_words.json", "w", encoding="utf-8"), indent=1)
with open(V + "qa_lines.txt", "w", encoding="utf-8") as f:
    for r, i, line, hyp in sorted(rep):
        f.write(f"{i:3d} {r:.3f}\n   SCRIPT: {line}\n   HEARD:  {hyp}\n")
print("low:", [(i, round(r, 2)) for r, i, _, _ in sorted(rep) if r < 0.9])
