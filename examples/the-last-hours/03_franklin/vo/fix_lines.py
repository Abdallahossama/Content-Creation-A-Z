"""Re-voice selected narration lines (Chatterbox, 3 takes each), keep the take whisper hears correctly, splice it into
the full VO, and rewrite vo.log durations so the edit re-times itself.
  venv-chatterbox python fix_lines.py gen 56 69 78 81 182        -> takes/line_<i>_<k>.wav
  uv python fix_lines.py pick 56 69 78 81 182                     -> choose + splice (needs faster-whisper)"""
import os, sys, re, json
import numpy as np, soundfile as sf
ROOT = "D:/why habibi/_newchannel/03_franklin/"; V = ROOT + "vo/"; os.makedirs(V + "takes", exist_ok=True)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES, PAUSE = [], []
for l in RAW:
    if l == "##":
        if PAUSE: PAUSE[-1] = 0.9
    else: LINES.append(l); PAUSE.append(0.35)
FIX = {33: "North, up a channel, as far as latitude seventy-seven. Then back down again.",
       98: "A few winters before, they say, about forty white men were seen walking south over the ice, dragging a boat.",
       109: "Inside, the paper. All well. And the margins.",
       127: "Were they turning back? McClintock thought so. Nobody knows."}   # TTS hints (same words)

def gen(ids):
    os.environ.setdefault("HF_HOME", "E:/AskHabibiAI/hf"); os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    import torch; torch.set_num_threads(max(1, os.cpu_count() - 2))
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    m = ChatterboxTurboTTS.from_pretrained(device="cpu"); m.prepare_conditionals("E:/AskHabibiAI/voice/ref_s01_12s.wav"); sr = m.sr
    for i in ids:
        text = FIX.get(i, LINES[i])
        for k in range(4):
            w = m.generate(text).squeeze(0).numpy().astype(np.float32); nz = np.where(np.abs(w) > 0.01)[0]
            if len(nz): w = w[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
            w[w == 0.0] = 1e-6; sf.write(V + f"takes/line_{i}_{k}.wav", w, sr, subtype="FLOAT"); print("take", i, k, round(len(w) / sr, 2), flush=True)

def norm(s): return re.sub(r"[^a-z ]", " ", s.lower().replace("'", "")).split()
def pick(ids):
    from faster_whisper import WhisperModel
    wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
    full, sr = sf.read(V + "franklin_vo_chatterbox.wav", dtype="float32")
    durs = {int(m.group(1)) - 1: float(m.group(3)) for m in re.finditer(r"^(\d+)/(\d+)\s+([\d.]+)s audio", open(V + "vo.log", encoding="utf-8", errors="ignore").read(), re.M)}
    if full.ndim > 1: full = full.mean(1)
    z = np.concatenate([[False], full == 0.0, [False]]).astype(np.int8); d = np.diff(z)
    zs, ze = np.where(d == 1)[0], np.where(d == -1)[0]; gaps = [(a_, b_) for a_, b_ in zip(zs, ze) if b_ - a_ >= int(0.3 * sr)]
    assert len(gaps) == len(LINES), (len(gaps), len(LINES))           # one exact-zero pause after every line
    starts = [0.0] + [g[1] / sr for g in gaps[:-1]]; durs = {i: gaps[i][0] / sr - starts[i] for i in range(len(LINES))}
    best = {}
    for i in ids:
        ref = norm(LINES[i]); scored = []
        for k in range(4):
            p = V + f"takes/line_{i}_{k}.wav"
            a, s = sf.read(p, dtype="float32"); a16 = np.interp(np.arange(int(len(a) * 16000 / s)) / 16000, np.arange(len(a)) / s, a).astype(np.float32)
            segs, _ = wm.transcribe(a16, beam_size=5, condition_on_previous_text=False); hyp = norm(" ".join(x.text for x in segs))
            import difflib; r = difflib.SequenceMatcher(a=ref, b=hyp).ratio(); scored.append((r, k, " ".join(hyp))); print(i, k, round(r, 3), " ".join(hyp), flush=True)
        r, k, h = max(scored); best[i] = k; print("PICK", i, k, r)
    # rebuild the full VO line by line (original audio for untouched lines)
    out = []; newd = dict(durs)
    for i in range(len(LINES)):
        if i in best:
            a, s = sf.read(V + f"takes/line_{i}_{best[i]}.wav", dtype="float32"); assert s == sr; newd[i] = len(a) / sr
        else:
            a = full[int(round(starts[i] * sr)): int(round((starts[i] + durs[i]) * sr))]
        out += [a, np.zeros(int(PAUSE[i] * sr), np.float32)]
    os.replace(V + "franklin_vo_chatterbox.wav", V + "franklin_vo_chatterbox_v1.wav")
    sf.write(V + "franklin_vo_chatterbox.wav", np.concatenate(out), sr, subtype="FLOAT")
    log = open(V + "vo.log", encoding="utf-8", errors="ignore").read(); os.replace(V + "vo.log", V + "vo_v1.log")
    log = re.sub(r"^(\d+)/(\d+)\s+([\d.]+)s audio", lambda m: f"{m.group(1)}/{m.group(2)} {newd[int(m.group(1)) - 1]:6.3f}s audio", log, flags=re.M)
    open(V + "vo.log", "w", encoding="utf-8").write(log); print("spliced", {i: round(newd[i] - durs[i], 2) for i in best})

if __name__ == "__main__":
    ids = [int(x) for x in sys.argv[2:]]
    gen(ids) if sys.argv[1] == "gen" else pick(ids)
