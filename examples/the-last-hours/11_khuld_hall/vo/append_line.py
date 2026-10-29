"""Append one new narration line (a take from takes/) to the end of the full VO, with its 0.35 s exact-zero pause, and log its duration,
so fix_lines.py pick (which needs one gap per line) can then choose the best take for it like any other line.
  uv run --no-project --with numpy --with soundfile python append_line.py 139 0"""
import os, sys
import numpy as np, soundfile as sf
V = "D:/why habibi/_newchannel/11_khuld_hall/vo/"
i, k = int(sys.argv[1]), int(sys.argv[2])
full, sr = sf.read(V + "khuld_vo_chatterbox.wav", dtype="float32")
a, s = sf.read(V + f"takes/line_{i}_{k}.wav", dtype="float32"); assert s == sr
out = np.concatenate([full, a, np.zeros(int(0.35 * sr), np.float32)])
os.replace(V + "khuld_vo_chatterbox.wav", V + "khuld_vo_chatterbox_pre_append.wav")
sf.write(V + "khuld_vo_chatterbox.wav", out, sr, subtype="FLOAT")
with open(V + "vo.log", "a", encoding="utf-8") as f: f.write(f"{i + 1}/{i + 1} {len(a) / sr:6.3f}s audio in 0.0s  | (appended line {i})\n")
print("appended", i, round(len(a) / sr, 2), "s ->", round(len(out) / sr, 2), "s")
