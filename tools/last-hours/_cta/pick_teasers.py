"""whisper each teaser CTA take, keep the cleanest per line -> cta_t_<key>.wav"""
import glob, re, shutil, difflib
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
D = "D:/why habibi/_newchannel/_cta/"
REF = {"khuld": "the full file saddam hussein called a meeting sixty six names were read out link below",
       "gaddafi": "the full file gaddafis basketball court gallows link below",
       "franklin": "the full file one hundred and twenty nine men vanished in the arctic this is their last note link below",
       "goering": "the full file hermann goering was watched twenty four seven so how did he get cyanide link below"}
import sys
if len(sys.argv) > 1: REF = {k: v for k, v in REF.items() if k in sys.argv[1:]}
wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
for key, ref in REF.items():
    best = None
    for f in sorted(glob.glob(D + f"takes/t_{key}_*.wav")):
        a, sr = sf.read(f, dtype="float32"); a = a.mean(1) if a.ndim > 1 else a
        a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) / 16000, np.arange(len(a)) / sr, a).astype(np.float32)
        segs, _ = wm.transcribe(a16, beam_size=5)
        txt = " ".join(s.text for s in segs).lower().replace("-", " ").replace("129", "one hundred and twenty nine").replace("66", "sixty six").replace("24/7", "twenty four seven").replace("24x7", "twenty four seven").replace("24 7", "twenty four seven").replace("göring", "goering").replace("goring", "goering")
        hyp = re.sub(r"[^a-z ]", "", txt).split()
        r = difflib.SequenceMatcher(a=ref.split(), b=hyp).ratio(); print(key, f[-12:], round(r, 3), " ".join(hyp), flush=True)
        if best is None or r > best[0]: best = (r, f)
    shutil.copy(best[1], D + f"cta_t_{key}.wav"); print("PICK", key, best, flush=True)
