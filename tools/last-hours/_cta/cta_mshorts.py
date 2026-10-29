"""Spoken end line for the standalone mystery Shorts that now point at their own long video (owner OK, 29 Oct):
same shape as the Alcatraz line ("Want the full file? Alcatraz, hour by hour. Link below."), Chatterbox, 4 takes per line
-> takes/m_<key>_<k>.wav. Pick with pick_mshorts.py (whisper) -> cta_m_<key>.wav.
  E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe cta_mshorts.py"""
import os
os.environ.setdefault("HF_HOME", "E:/AskHabibiAI/hf"); os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import numpy as np, soundfile as sf, torch
torch.set_num_threads(max(1, os.cpu_count() - 2))
from chatterbox.tts_turbo import ChatterboxTurboTTS
D = "D:/why habibi/_newchannel/_cta/"; os.makedirs(D + "takes", exist_ok=True)
LINES = {"cooper": "Want the full file? D.B. Cooper, hour by hour. Link below.",
         "flannan": "Want the full file? The Flannan Isles, hour by hour. Link below."}
m = ChatterboxTurboTTS.from_pretrained(device="cpu"); m.prepare_conditionals("E:/AskHabibiAI/voice/ref_s01_12s.wav"); sr = m.sr
for key, text in LINES.items():
    for k in range(4):
        w = m.generate(text).squeeze(0).numpy().astype(np.float32); nz = np.where(np.abs(w) > 0.01)[0]
        if len(nz): w = w[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
        sf.write(D + f"takes/m_{key}_{k}.wav", w, sr, subtype="FLOAT"); print("take", key, k, round(len(w) / sr, 2), flush=True)
