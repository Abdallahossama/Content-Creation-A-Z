"""Whisper every File Keeper sign-off take and keep the cleanest per file -> so_<key>.wav (numbers are compared as words, so "66" or
"24/7" in the transcript don't count as misses). Prints each take's text so a human can check the names.
  uv run --no-project --with faster-whisper --with soundfile --with numpy python signoff_pick.py [key ...]"""
import glob, re, shutil, difflib, sys, json
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
sys.path.insert(0, "D:/why habibi/_newchannel/_cta")
D = "D:/why habibi/_newchannel/_cta/"
src = open(D + "signoff_gen.py", encoding="utf-8").read(); ns = {}                                # HEAD/TAIL/NEXT/LINES without loading torch
exec(src[src.index('HEAD = '):src.index('if __name__')], ns); LINES = ns["LINES"]
NUM = {"66": "sixty six", "33": "thirty three", "8": "eight", "306": "three hundred and six", "107": "a hundred and seven", "24/7": "twenty four seven",
       "24x7": "twenty four seven", "24 7": "twenty four seven", "14": "fourteen", "19": "nineteen"}
def norm(s):
    s = s.lower().replace("-", " ").replace("göring", "goering").replace("goring", "goering")
    for k, v in NUM.items(): s = re.sub(r"\b" + re.escape(k) + r"\b", v, s)
    return re.sub(r"[^a-z ]", "", s).split()
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
for key in (sys.argv[1:] or list(LINES)):
    ref = norm(LINES[key]); best = None
    for f in sorted(glob.glob(D + f"takes/so_{key}_*.wav")):
        a, sr = sf.read(f, dtype="float32"); a = a.mean(1) if a.ndim > 1 else a
        a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
        segs = list(wm.transcribe(a16, beam_size=5, word_timestamps=True)[0]); txt = " ".join(s.text for s in segs)
        words = [(round(w.start, 3), round(w.end, 3), w.word.strip()) for sg in segs for w in sg.words if w.word.strip()]
        r = difflib.SequenceMatcher(a=ref, b=norm(txt)).ratio(); dur = len(a) / sr
        print(key, f[-10:], round(r, 3), round(dur, 1), "s |", txt.strip(), flush=True)
        if best is None or (r, -dur) > (best[0], -best[2]): best = (r, f, dur, words)
    shutil.copy(best[1], D + f"so_{key}.wav"); print("PICK", key, best[:3], flush=True)
    FIX = {"Goering": "Göring", "Goring": "Göring", "Gowering": "Göring", "24-7": "24/7", "24x7": "24/7"}       # whisper spelling -> ours
    def fix(w): core = w.rstrip(".,?!"); return FIX.get(core, core) + w[len(core):]
    ws = [[a, b, fix(w)] for a, b, w in best[3]]
    for i in range(len(ws) - 1):                                                              # "file keeper" -> "File Keeper"
        if ws[i][2].lower() == "file" and ws[i + 1][2].lower().startswith("keeper"): ws[i][2] = "File"; ws[i + 1][2] = "K" + ws[i + 1][2][1:]
    json.dump(ws, open(D + f"so_{key}.json", "w", encoding="utf-8"), ensure_ascii=False)                       # word timings for the end-card captions
