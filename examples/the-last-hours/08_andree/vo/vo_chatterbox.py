"""Local voice-over with Chatterbox Turbo (MIT, CPU): the user's own cloned voice, conditioned on a clean 13 s clip of
his existing ElevenLabs narration (Short #1). One sentence per call (stable), joined with short pauses, float WAV.
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe vo_chatterbox.py <ref.wav> <out.wav> [lines.txt]"""
import os, sys, time
os.environ.setdefault("HF_HOME", "E:/AskHabibiAI/hf"); os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import numpy as np, soundfile as sf, torch
torch.set_num_threads(max(1, os.cpu_count() - 2))
from chatterbox.tts_turbo import ChatterboxTurboTTS

LINES = [  # (sentence, pause after in seconds)
    ("You're seconds from sleep, and your body jumps.", 0.25),
    ("Seven in ten people get this, and your brain is the reason.", 0.45),
    ("It's called a hypnic jerk.", 0.40),
    ("As you drift off, your nervous system winds down, and your muscles go slack.", 0.30),
    ("But sometimes, your brain misreads that sudden slack as falling.", 0.30),
    ("So it fires one quick, powerful signal to catch you.", 0.15),
    ("And your whole body jumps.", 0.50),
    ("That's the leading theory. Scientists still don't know for sure.", 0.45),
    ("It's normal, and harmless. But stress, caffeine, and too little sleep are linked to more of them.", 0.50),
    ("So next time it happens, your brain wasn't broken.", 0.25),
    ("It just thought you were falling.", 0.60),
]

def main():
    ref, out = sys.argv[1], sys.argv[2]
    lines = LINES
    if len(sys.argv) > 3:                                              # one sentence per line; a line "##" = chapter pause (0.9 s)
        lines = []
        for l in open(sys.argv[3], encoding="utf-8"):
            l = l.strip()
            if not l: continue
            if l == "##":
                if lines: lines[-1] = (lines[-1][0], 0.9)
            else: lines.append((l, 0.35))
    t0 = time.time(); model = ChatterboxTurboTTS.from_pretrained(device="cpu"); print("loaded", round(time.time() - t0, 1), "s", flush=True)
    model.prepare_conditionals(ref)
    sr = model.sr; parts = []
    for i, (text, pause) in enumerate(lines):
        t1 = time.time(); wav = model.generate(text).squeeze(0).numpy().astype(np.float32)
        nz = np.where(np.abs(wav) > 0.01)[0]                                     # trim the model's leading/trailing silence
        if len(nz): wav = wav[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
        wav[wav == 0.0] = 1e-6                                                   # exact zeros only in the gaps (line timing)
        parts += [wav, np.zeros(int(pause * sr), np.float32)]
        print(f"{i + 1}/{len(lines)} {len(wav) / sr:5.2f}s audio in {time.time() - t1:5.1f}s  | {text}", flush=True)
    y = np.concatenate(parts); sf.write(out, y, sr, subtype="FLOAT")
    print("WROTE", out, round(len(y) / sr, 2), "s total,", round(time.time() - t0, 1), "s wall", flush=True)

if __name__ == "__main__":
    main()
