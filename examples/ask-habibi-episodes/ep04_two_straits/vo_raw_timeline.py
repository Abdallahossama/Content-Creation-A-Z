"""The untouched ElevenLabs voice on the final timeline (same documentary pauses as the video), no gain, no limiter,
no de-ess - for the user to process in CapCut themselves. -> build/vo_timeline_ELEVENLABS_UNTOUCHED.wav"""
import subprocess
import numpy as np, soundfile as sf
from ep04_common import *

SR = 48000; N = int(T_END * SR)
raw = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", EP + "vo/ep04_vo_joined.wav", "-f", "f32le", "-ac", "1",
                                    "-ar", str(SR), "-"], capture_output=True).stdout, np.float32)
vt = np.zeros(N, np.float32)
edges = [0.0] + [c for c, _ in PAUSES] + [VO_LEN]
for a, b in zip(edges, edges[1:]):
    seg = raw[int(a * SR):int(b * SR)]; i = int(round(T(a + 1e-4) * SR))
    n = min(len(seg), N - i); vt[i:i + n] += seg[:n]
sf.write(BUILD + "vo_timeline_ELEVENLABS_UNTOUCHED.wav", vt, SR, subtype="PCM_24")
print("wrote", BUILD + "vo_timeline_ELEVENLABS_UNTOUCHED.wav", round(N / SR, 2), "s, peak", round(20 * np.log10(np.abs(vt).max()), 2), "dBFS")
