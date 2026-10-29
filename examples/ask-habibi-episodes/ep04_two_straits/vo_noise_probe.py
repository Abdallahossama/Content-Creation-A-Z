"""Where does the hiss under the voice come from? Measure every stage of the Ep 4 audio chain:
noise floor in the gaps between words, HF energy, clipped samples, and what loudnorm actually did."""
import subprocess, json, sys
import numpy as np

SR = 48000
EP = "D:/why habibi/4th video/"
def dec(p, ch=1, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(t)] if t else []) + \
          ["-i", p, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
    return a.reshape(-1, ch) if ch > 1 else a

def stats(name, x):
    x = x.astype(np.float64); win = int(0.03 * SR); n = len(x) // win
    r = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12); db = 20 * np.log10(r)
    loud = np.percentile(db, 90)
    gaps = db[(db < loud - 25)]                       # short gaps between words (not silence padding at 0)
    floor = np.percentile(gaps[gaps > -120], 50) if (gaps > -120).any() else -999
    spec = np.abs(np.fft.rfft(x[: SR * 60])) ** 2; fq = np.fft.rfftfreq(min(len(x), SR * 60), 1 / SR)
    hf = 10 * np.log10(spec[fq > 9000].sum() / spec[(fq > 200) & (fq < 4000)].sum())
    clip = int((np.abs(x) >= 0.999).sum())
    print(f"{name:34s} loud90={loud:6.1f}  gap-floor={floor:6.1f} dBFS  (gap vs speech {floor - loud:6.1f} dB)  "
          f"HF/mid={hf:6.1f} dB  clipped={clip}  peak={20*np.log10(np.abs(x).max()+1e-12):5.2f}")

stats("ElevenLabs part1.mp3", dec(EP + "vo/ep04_vo_part1.mp3"))
stats("ElevenLabs part2.mp3", dec(EP + "vo/ep04_vo_part2.mp3"))
stats("VO leveled -16 LUFS wav", dec(EP + "vo/ep04_VO_leveled_-16LUFS.wav"))
stats("build/vo_timeline.wav", dec(EP + "build/vo_timeline.wav"))
stats("build/music_bed_ep04.wav", dec(EP + "build/music_bed_ep04.wav"))
stats("build/sfx_ep04.wav", dec(EP + "build/sfx_ep04.wav"))
stats("build/mix_raw.wav", dec(EP + "build/mix_raw.wav"))
stats("build/mix_ep04.wav (loudnorm)", dec(EP + "build/mix_ep04.wav"))
stats("export mp4 audio", dec(EP + "export/Ask_Habibi_Ep4_1440p.mp4"))

# what did loudnorm's second pass actually do: linear or dynamic?
src = EP + "build/mix_raw.wav"
j = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
m = json.loads(j[j.rindex("{"):j.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
j2 = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
m2 = json.loads(j2[j2.rindex("{"):j2.rindex("}") + 1])
print("pass1:", {k: m[k] for k in ("input_i", "input_tp", "input_lra")}, "-> pass2 normalization_type:", m2.get("normalization_type"))
