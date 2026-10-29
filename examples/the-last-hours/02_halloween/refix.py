"""Re-voice single lines of a bank Short (Chatterbox, N takes), keep the take whisper hears best, splice it into
vo_chatterbox.wav between the exact-zero gaps (backup: vo_chatterbox_v1.wav).
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe refix.py gen      (all jobs in JOBS)
  uv run --no-project --with faster-whisper --with soundfile --with numpy python refix.py pick"""
import os, sys, re, difflib, json
import numpy as np, soundfile as sf
BANK = "D:/why habibi/_pipeline/shorts/bank/"; TK = "D:/why habibi/_newchannel/02_halloween/takes/"; os.makedirs(TK, exist_ok=True)
# (folder, line index 0-based, text to speak, expected words for scoring, takes)
JOBS = [
 ("38_centralia_fire", 1, "Centralia, May nineteen sixty-two. The town dump, in an old strip-mine pit, catches fire.", "centralia may 1962 the town dump in an old strip mine pit catches fire", 4),
 ("38_centralia_fire", 4, "In nineteen eighty-three, putting it out was priced at six hundred and sixty-three million dollars.", "in 1983 putting it out was priced at 663 million dollars", 3),
 ("35_flannan_isles_keepers", 3, "The last notes, chalked on a slate, are from December fifteenth.", "the last notes chalked on a slate are from december 15th", 4),
 ("37_wow_signal", 6, "Some astronomers now think a hydrogen cloud flared, hit by a burst from a dead star.", "some astronomers now think a hydrogen cloud flared hit by a burst from a dead star", 4),
 ("39_somerton_man", 8, "It is ended. Except it isn't.", "it is ended except it isnt", 4),
 ("40_tunguska_no_crater", 2, "At a trading post, a man on his porch feels the heat. Then the blast throws him off.", "at a trading post a man on his porch feels the heat then the blast throws him off", 3),
]

def gen():
    os.environ.setdefault("HF_HOME", "E:/AskHabibiAI/hf"); os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    import torch; torch.set_num_threads(max(1, os.cpu_count() - 2))
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    m = ChatterboxTurboTTS.from_pretrained(device="cpu"); m.prepare_conditionals("E:/AskHabibiAI/voice/ref_s01_12s.wav"); sr = m.sr
    for folder, li, text, _, n in JOBS:
        for k in range(n):
            w = m.generate(text).squeeze(0).numpy().astype(np.float32); nz = np.where(np.abs(w) > 0.01)[0]
            if len(nz): w = w[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
            w[np.abs(w) < 1e-7] = 1e-6                     # never leave exact zeros inside a line (they mark line gaps)
            sf.write(TK + f"{folder[:2]}_{li}_{k}.wav", w, sr, subtype="FLOAT"); print("take", folder, li, k, round(len(w) / sr, 2), flush=True)

def norm(s): return re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split()

def pick():
    sys.path.insert(0, "D:/why habibi/_newchannel/02_halloween"); import mshorts as M
    from faster_whisper import WhisperModel
    wm = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=8); best = {}
    for folder, li, text, ref, n in JOBS:
        sc = []
        for k in range(n):
            a, s = sf.read(TK + f"{folder[:2]}_{li}_{k}.wav", dtype="float32")
            a16 = np.interp(np.arange(int(len(a) * 16000 / s)) / 16000, np.arange(len(a)) / s, a).astype(np.float32)
            segs, _ = wm.transcribe(a16, beam_size=5, condition_on_previous_text=False); hyp = " ".join(x.text for x in segs)
            r = difflib.SequenceMatcher(a=norm(ref), b=norm(hyp)).ratio(); sc.append((r, -abs(len(a) / s - 4), k, hyp)); print(folder, li, k, round(r, 3), hyp, flush=True)
        r, _, k, h = max(sc); best[(folder, li)] = (k, r, h); print("PICK", folder, li, k, round(r, 3), flush=True)
    for folder in sorted({j[0] for j in JOBS}):
        d = BANK + folder + "/"; src = d + "vo_chatterbox.wav"; bak = d + "vo_chatterbox_v1.wav"
        if not os.path.exists(bak): os.replace(src, bak)
        n_lines = len([l for l in open(d + "vo_lines.txt", encoding="utf-8") if l.strip()])
        y, sr = sf.read(bak, dtype="float32"); LT, _ = M.line_times(bak, n_lines); parts = []
        for i, (a, e) in enumerate(LT):
            if (folder, i) in best:
                w, s2 = sf.read(TK + f"{folder[:2]}_{i}_{best[(folder, i)][0]}.wav", dtype="float32"); assert s2 == sr; parts.append(w)
            else: parts.append(y[int(round(a * sr)): int(round(e * sr))])
            parts.append(np.zeros(int(0.35 * sr), np.float32))
        sf.write(src, np.concatenate(parts), sr, subtype="FLOAT"); print("spliced", folder, flush=True)
    json.dump({f"{k[0]}:{k[1]}": v for k, v in best.items()}, open(TK + "picks.json", "w"), indent=1)

if __name__ == "__main__":
    gen() if sys.argv[1] == "gen" else pick()
