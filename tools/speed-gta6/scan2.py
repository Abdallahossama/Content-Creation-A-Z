import sys, json, subprocess, os
import soundfile as sf
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
picks = json.load(open(sys.argv[1]))[: int(sys.argv[2])]
for p in picks:
    a = p["t"] - 40; src = [f for f in os.listdir(".") if f.startswith(p["vid"] + ".audio")][0]; wav = "_s.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(a), "-t", "60", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
    aud, _ = sf.read(wav, dtype="float32")
    segs, _ = m.transcribe(aud, vad_filter=False, initial_prompt="IShowSpeed, GTA 6, Vice City, chat, bro")
    txt = " ".join(f"[{int(s.start)}]{s.text.strip()}" for s in segs)
    print(f"\n== {p['vid']} t={p['t']} rank {p['rank']} motion {p['motion']}\n{txt[:900]}", flush=True)
