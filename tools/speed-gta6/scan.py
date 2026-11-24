"""scan: transcribe a window around each peak (audio only) so we can pick and title the best moments."""
import sys, json, subprocess, os
import soundfile as sf
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
for vid in sys.argv[1:]:
    d = json.load(open(f"{vid}.peaks.json")); src = d["src"]; res = []
    for p in d["picks"][:8]:
        a, b = p["peak"] - 50, p["peak"] + 40; wav = f"_w_{vid}_{int(p['peak'])}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
        aud, _sr = sf.read(wav, dtype="float32"); segs, _ = m.transcribe(aud, word_timestamps=True, vad_filter=True, initial_prompt="IShowSpeed, GTA 6, Vice City, chat, bro")
        words = [dict(w=w.word, s=round(w.start + a, 2), e=round(w.end + a, 2)) for s in segs for w in (s.words or [])]
        res.append(dict(peak=p["peak"], score=p["score"], words=words)); os.remove(wav)
        print(f"\n== {vid} {p['peak']:.0f} ({p['score']})\n" + " ".join(w["w"].strip() for w in words)[:700], flush=True)
    json.dump(res, open(f"{vid}.scan.json", "w", encoding="utf-8"))
