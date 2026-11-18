"""Whisper each VO line on its own slice -> vo/vo_words.json (word times on the VO clock) + vo/qa_lines.txt (match score per line).
  uv run --no-project --with faster-whisper --with soundfile --with numpy python transcribe_lines.py <video_root> [prompt words]"""
import re, json, difflib, sys
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
ROOT = sys.argv[1].rstrip("/") + "/"; V = ROOT + "vo/"
PROMPT = sys.argv[2] if len(sys.argv) > 2 else ""
LINES = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip() and l.strip() != "##"]
full, sr = sf.read(V + "vo.wav", dtype="float32")
if full.ndim > 1: full = full.mean(1)
z = np.concatenate([[False], full == 0.0, [False]]).astype(np.int8); d = np.diff(z)
GAPS = [(a, b) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]) if b - a >= int(0.3 * sr)]
assert len(GAPS) == len(LINES), (len(GAPS), len(LINES))
STARTS = [0] + [g[1] for g in GAPS[:-1]]
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
def norm(s): return re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "").replace("-", " ")).split()
out, rep = [], []
for i, line in enumerate(LINES):
    t = STARTS[i] / sr; a = full[STARTS[i]: GAPS[i][0]]
    a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
    segs, _ = wm.transcribe(a16, word_timestamps=True, beam_size=5, condition_on_previous_text=False, initial_prompt=PROMPT or None)
    ws, txt = [], []
    for sg in segs:
        txt.append(sg.text)
        for w in sg.words: ws.append({"w": w.word, "s": round(w.start + t, 3), "e": round(w.end + t, 3), "p": round(w.probability, 3)})
    hyp = " ".join(txt).strip(); r = difflib.SequenceMatcher(a=norm(line), b=norm(hyp)).ratio()
    out.append({"line": i, "start": t, "words": ws}); rep.append((r, i, line, hyp)); print(f"{i:3d} {r:.3f} {hyp}", flush=True)
json.dump(out, open(V + "vo_words.json", "w", encoding="utf-8"), indent=1)
with open(V + "qa_lines.txt", "w", encoding="utf-8") as f:
    for r, i, line, hyp in sorted(rep): f.write(f"{i:3d} {r:.3f}\n   SCRIPT: {line}\n   HEARD:  {hyp}\n")
