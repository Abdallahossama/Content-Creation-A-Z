"""whisper each mystery-Short CTA take, keep the cleanest per line -> cta_m_<key>.wav"""
import glob, re, shutil, difflib
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
D = "D:/why habibi/_newchannel/_cta/"
REF = {"cooper": "want the full file db cooper hour by hour link below",
       "flannan": "want the full file the flannan isles hour by hour link below"}
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
for key, ref in REF.items():
    best = None
    for f in sorted(glob.glob(D + f"takes/m_{key}_*.wav")):
        a, sr = sf.read(f, dtype="float32"); a = a.mean(1) if a.ndim > 1 else a
        a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
        segs, _ = wm.transcribe(a16, beam_size=5, initial_prompt="D.B. Cooper. The Flannan Isles.")
        txt = " ".join(s.text for s in segs).lower().replace("-", " ").replace("d.b.", "db").replace("d. b.", "db").replace("flannon", "flannan")
        hyp = re.sub(r"[^a-z ]", "", txt).split()
        r = difflib.SequenceMatcher(a=ref.split(), b=hyp).ratio(); print(key, f[-12:], round(r, 3), " ".join(hyp), flush=True)
        if best is None or r > best[0]: best = (r, f)
    shutil.copy(best[1], D + f"cta_m_{key}.wav"); print("PICK", key, best, flush=True)
