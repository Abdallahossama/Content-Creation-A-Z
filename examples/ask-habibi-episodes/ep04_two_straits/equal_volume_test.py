"""Equal-loudness A/B, lossless: ElevenLabs untouched (plain volume only) vs the voice after my processing, same words
(VO 14-44 s), both at the same integrated loudness. The only difference left is the processing itself."""
import subprocess
import numpy as np, soundfile as sf
SR = 48000; V = "D:/why habibi/4th video/vo/"; X = "D:/why habibi/4th video/export/"
def dec(p, ss=14, t=30):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", p, "-f", "f32le", "-ac", "1",
                                         "-ar", str(SR), "-"], capture_output=True).stdout, np.float32).astype(np.float64)
def lufs(x):
    sf.write(X + "_tmp.wav", x, SR, subtype="FLOAT")
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", X + "_tmp.wav", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr.splitlines()
    return float([l for l in o if l.strip().startswith("I:")][-1].split()[1])
a = dec(V + "ep04_vo_joined.wav"); b = dec(V + "ep04_VO_leveled_-16LUFS.wav")
la, lb = lufs(a), lufs(b); target = la
a = a * 10 ** ((target - la) / 20); b = b * 10 ** ((target - lb) / 20)
print(f"untouched {la:.1f} -> {lufs(a):.1f} LUFS (peak {20*np.log10(np.abs(a).max()):.1f} dBFS) | processed {lb:.1f} -> {lufs(b):.1f} LUFS (peak {20*np.log10(np.abs(b).max()):.1f} dBFS)")
beep = 0.12 * np.sin(2 * np.pi * 880 * np.arange(int(0.25 * SR)) / SR); gap = np.zeros(SR)
sf.write(X + "TEST_same_volume_1_ElevenLabs_untouched_beep_2_my_processing.wav", np.concatenate([a, gap, beep, gap, b]), SR, subtype="PCM_24")
import os; os.remove(X + "_tmp.wav"); print("written")

