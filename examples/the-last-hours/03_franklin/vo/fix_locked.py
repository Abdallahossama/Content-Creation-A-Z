"""Second pass for words the clone says oddly ('cairn' heard as 'can'): spoken-form hints, 4 takes each, whisper pick,
and a LENGTH-LOCKED splice: the new take goes into the old line's slot (line + its pause), so the edit's timing never moves.
  venv-chatterbox python fix_locked.py gen        -> takes2/line_<i>_<k>.wav
  uv python fix_locked.py pick                     -> choose + splice into franklin_vo_chatterbox.wav (backup _v2)"""
import os, sys, re, difflib
import numpy as np, soundfile as sf
ROOT = "D:/why habibi/_newchannel/03_franklin/"; V = ROOT + "vo/"; TK = V + "takes2/"; os.makedirs(TK, exist_ok=True)
RAW = [l.strip() for l in open(ROOT + "vo_lines.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
SAY = {55: "Gore signs it. Des Voeux signs it. They leave the tin inside a stone kern.",           # cairn = 'kern' (US)
       108: "Among the loose stones that have fallen from the kern, there's a small tin cylinder.",
       173: "Thanks for staying, for the last hours."}
N = 4

def gen():
    os.environ.setdefault("HF_HOME", "E:/AskHabibiAI/hf"); os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    import torch; torch.set_num_threads(max(1, os.cpu_count() - 2))
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    m = ChatterboxTurboTTS.from_pretrained(device="cpu"); m.prepare_conditionals("E:/AskHabibiAI/voice/ref_s01_12s.wav"); sr = m.sr
    for i, text in SAY.items():
        for k in range(N):
            w = m.generate(text).squeeze(0).numpy().astype(np.float32); nz = np.where(np.abs(w) > 0.01)[0]
            if len(nz): w = w[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
            w[w == 0.0] = 1e-6; sf.write(TK + f"line_{i}_{k}.wav", w, sr, subtype="FLOAT"); print("take", i, k, round(len(w) / sr, 2), flush=True)

def norm(s):
    s = re.sub(r"\b(kern|karn|kerne|carn|care in|cairns?)\b", "cairn", s.lower().replace("'", ""))
    return re.sub(r"[^a-z ]", " ", s).split()

def pick():
    from faster_whisper import WhisperModel
    wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8)
    full, sr = sf.read(V + "franklin_vo_chatterbox.wav", dtype="float32")
    full = np.concatenate([full, np.zeros(sr, np.float32)])            # the last line may run into the 20 s end screen
    z = np.concatenate([[False], full == 0.0, [False]]).astype(np.int8); d = np.diff(z)
    gaps = [(a, b) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0]) if b - a >= int(0.3 * sr)]
    assert len(gaps) == len(LINES), (len(gaps), len(LINES))
    starts = [0] + [g[1] for g in gaps[:-1]]; out = full.copy(); done = {}
    for i in SAY:
        slot = (starts[i + 1] if i + 1 < len(LINES) else len(full)) - starts[i]; old = gaps[i][0] - starts[i]; scored = []
        for k in range(N):
            a, s = sf.read(TK + f"line_{i}_{k}.wav", dtype="float32"); assert s == sr
            if len(a) > slot - int(0.12 * sr): print(i, k, "too long", round(len(a) / sr, 2), "slot", round(slot / sr, 2)); continue
            a16 = np.interp(np.arange(int(len(a) * 16000 / s)) / 16000, np.arange(len(a)) / s, a).astype(np.float32)
            hyps = []
            for wt in (False, True):                                   # both decoders must agree (the 'last'/'lost' trap)
                segs, _ = wm.transcribe(a16, beam_size=5, condition_on_previous_text=False, word_timestamps=wt); hyps.append(" ".join(x.text for x in segs))
            r = min(difflib.SequenceMatcher(a=norm(LINES[i]), b=norm(h)).ratio() for h in hyps)
            scored.append((r, -abs(len(a) - old), k, hyps)); print(i, k, round(r, 3), hyps, flush=True)
        if not scored: print("NO TAKE FITS", i); continue
        r, _, k, h = max(scored); print("PICK", i, k, round(r, 3))
        if r < 0.95: print("  kept the old take (best new take not clean)"); continue
        a, _ = sf.read(TK + f"line_{i}_{k}.wav", dtype="float32")
        out[starts[i]: starts[i] + slot] = 0.0; out[starts[i]: starts[i] + len(a)] = a; done[i] = k
    if done:
        os.replace(V + "franklin_vo_chatterbox.wav", V + "franklin_vo_chatterbox_v2.wav")
        sf.write(V + "franklin_vo_chatterbox.wav", out, sr, subtype="FLOAT"); print("spliced (length-locked)", done)

if __name__ == "__main__":
    gen() if sys.argv[1] == "gen" else pick()
