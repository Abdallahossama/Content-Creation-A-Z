"""Whisper each narration line on its own slice: word timings on the VO clock (vo_words.json) + a per-line match score
against the script (qa_lines.txt), so misread lines can be re-voiced with fix_lines.py."""
import re, json, difflib
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
ROOT = "D:/why habibi/_newchannel/08_andree/"; V = ROOT + "vo/"
RAW = [l.strip() for l in open(V + "vo_tts.txt", encoding="utf-8") if l.strip()]
LINES, PAUSE = [], []
for l in RAW:
    if l == "##":
        if PAUSE: PAUSE[-1] = 0.9
    else: LINES.append(l); PAUSE.append(0.35)
durs = {int(m.group(1)) - 1: float(m.group(3)) for m in re.finditer(r"^(\d+)/(\d+)\s+([\d.]+)s audio", open(V + "vo.log", encoding="utf-8", errors="ignore").read(), re.M)}
full, sr = sf.read(V + "andree_vo_chatterbox.wav", dtype="float32")
if full.ndim > 1: full = full.mean(1)
z = np.concatenate([[False], full == 0.0, [False]]).astype(np.int8); d = np.diff(z)      # exact-zero line gaps (no rounding drift)
GAPS = [(a, b) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]) if b - a >= int(0.3 * sr)]
assert len(GAPS) == len(LINES), (len(GAPS), len(LINES))
STARTS = [0] + [g[1] for g in GAPS[:-1]]
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
NUM = {"1897": "eighteen ninety seven", "1898": "eighteen ninety eight", "1930": "nineteen thirty", "1952": "nineteen fifty two",
       "1945": "nineteen forty five", "2024": "twenty twenty four"}
def norm(s):
    s = s.lower().replace("'", "").replace("-", " ")
    for k, v in NUM.items(): s = s.replace(k, v)
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
out, rep = [], []; t = 0.0
for i, line in enumerate(LINES):
    t = STARTS[i] / sr; a = full[STARTS[i]: GAPS[i][0]]; a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
    segs, _ = wm.transcribe(a16, word_timestamps=True, beam_size=5, condition_on_previous_text=False, initial_prompt="Andray, Strindberg, Frenkel, the Eagle balloon, Danes Island, Svalbard, Vogelsang, Cape Flora, Franz Josef Land, Alken, Bratvaag, Greely, Hertzberg, Uusma, White Island, Chateaubriand, trichinosis.")
    ws, txt = [], []
    for sg in segs:
        txt.append(sg.text)
        for w in sg.words: ws.append({"w": w.word, "s": round(w.start + t, 3), "e": round(w.end + t, 3), "p": round(w.probability, 3)})
    hyp = " ".join(txt).strip(); r = difflib.SequenceMatcher(a=norm(line), b=norm(hyp)).ratio()
    out.append({"line": i, "start": t, "words": ws}); rep.append((r, i, line, hyp)); print(f"{i:3d} {r:.3f} {hyp}", flush=True)
json.dump(out, open(V + "vo_words.json", "w", encoding="utf-8"), indent=1)
with open(V + "qa_lines.txt", "w", encoding="utf-8") as f:
    for r, i, line, hyp in sorted(rep):
        f.write(f"{i:3d} {r:.3f}\n   SCRIPT: {line}\n   HEARD:  {hyp}\n")
print("low:", [(i, round(r, 2)) for r, i, _, _ in sorted(rep) if r < 0.9])
