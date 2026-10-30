"""The File Keeper sign-off (owner, 30 Oct 2026; repo docs/09): one line per long file, in the creator's cloned voice (same reference clip
as every file), naming the NEXT file. Replaces the old end lines ("Next, I'm opening..." / "If you want the next file, subscribe.").
3 takes per file -> takes/so_<key>_<k>.wav; pick with signoff_pick.py -> so_<key>.wav.
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe signoff_gen.py [key ...]"""
import os, sys
os.environ.setdefault("HF_HOME", "E:/AskHabibiAI/hf"); os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import numpy as np, soundfile as sf, torch
torch.set_num_threads(max(1, os.cpu_count() - 2))
from chatterbox.tts_turbo import ChatterboxTurboTTS
D = "D:/why habibi/_newchannel/_cta/"; os.makedirs(D + "takes", exist_ok=True)
HEAD = "I'm the File Keeper. Every week, I open one file the history books left half-told. "
TAIL = "Subscribe, and it'll be waiting for you. And if this one was worth your time, a like really helps a small channel get seen."
ASK = " Whose file should I open after that? Tell me below. I read every one."
NEXT = {"flannan": "Saddam Hussein calls a meeting, and sixty-six names are read out.",
        "khuld": "three men vanish in a balloon, and their film waits thirty-three years.",
        "andree": "Gaddafi's basketball court gallows. Eight hangings in eight days.",
        "gaddafi": "fourteen men vanish off Florida, and their last call gets no answer.",
        "flight19": "three hundred and six men vanish at sea, and their last message is about coal.",
        "cyclops": "a pilot leaves the cockpit for a hundred and seven seconds. Then the dive begins.",
        "egyptair": "Hermann Goering is watched twenty-four seven. So how does he get cyanide?",
        "goering": "six convicts, two guns, and the one key they never found."}
LINES = {k: HEAD + "Next: " + v + " " + TAIL for k, v in NEXT.items()}
LINES["goering"] += ASK
LINES["like46"] = "Would you have hidden that key too? If you would, hit like."      # the like-vote TEST line (Alcatraz 1946 only)
LINES["alcatraz46"] = HEAD + "Subscribe, and the next one will be waiting for you. And if this one was worth your time, a like really helps a small channel get seen. Whose file should I open next? Tell me below. I read every one."
if __name__ == "__main__":
    keys = sys.argv[1:] or list(LINES)
    m = ChatterboxTurboTTS.from_pretrained(device="cpu"); m.prepare_conditionals("E:/AskHabibiAI/voice/ref_s01_12s.wav"); sr = m.sr
    for key in keys:
        for k in range(3):
            w = m.generate(LINES[key]).squeeze(0).numpy().astype(np.float32); nz = np.where(np.abs(w) > 0.01)[0]
            if len(nz): w = w[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
            sf.write(D + f"takes/so_{key}_{k}.wav", w, sr, subtype="FLOAT"); print("take", key, k, round(len(w) / sr, 2), flush=True)
