"""#25 render driver: frames -> ffmpeg segments, audio mix (voice + ducked music + SFX), final mux.
  uv run --no-project --with pillow --with numpy --with soundfile --with arabic-reshaper --with python-bidi python pz_main.py qa t.. | seg i n | audio | final n"""
import sys, subprocess, os
from mi_shots import *
MUS = "D:/why habibi/_music_library/"

SH = sorted(SHOTS, key=lambda s: AT(s["at"]))
STARTS = [AT(s["at"]) for s in SH]
def frame(t):
    i = max(0, sum(1 for x in STARTS if x <= t) - 1); s = SH[i]
    t0 = STARTS[i]; t1 = STARTS[i + 1] if i + 1 < len(SH) else DUR
    c = Image.new("RGB", (W, H), PAPER); s["fn"](c, t, s, t0, t1)
    if t > VO_END + 0.3: c = Image.blend(c, Image.new("RGB", (W, H), (0, 0, 0)), clamp01((t - VO_END - 0.3) / (TAIL - 0.8)))
    if t < 0.4: c = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), c, clamp01(t / 0.4))
    return c

def seg(i, n):
    a, b = NF * i // n, NF * (i + 1) // n; out = B + f"seg_{i:02d}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(frame(f / FPS).tobytes())
        if f % 300 == 0: print(f"seg {i}: {f - a}/{b - a}", flush=True)
    p.stdin.close(); p.wait(); print("seg done", i, flush=True)

def load(path, sr=48000):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy()
def audio():
    SR = 48000; n = int(DUR * SR) + SR; mix = np.zeros(n, np.float32)
    vo = load(ROOT + "vo/mi_vo.wav"); a = int(LEAD * SR); mix[a:a + len(vo)] += vo * 1.0
    env = np.zeros(n, np.float32); env[a:a + len(vo)] = (np.abs(vo) > 0.02).astype(np.float32)
    k = int(0.35 * SR); env = np.convolve(env, np.ones(k, np.float32) / k, "same"); env = np.clip(env * 3, 0, 1)
    mus = np.zeros(n, np.float32); pos = 0
    for f in MUSIC:
        m = load(MUS + f); m = m[: n - pos]; mus[pos:pos + len(m)] = m; pos += len(m)
        if pos >= n: break
    body = np.where(np.arange(n) < T[11] * SR, -11.0, -17.0)                # owner rule (clean-voice-mix): cold open -11 dB, body -17 dB
    g = 10 ** ((body + 4) / 20) * (1 - env) + 10 ** (body / 20) * env       # +4 dB lift in the gaps between lines
    fade = np.clip(np.arange(n) / (2.0 * SR), 0, 1) * np.clip((DUR * SR - np.arange(n)) / (4.0 * SR), 0, 1)
    mix += mus * g * fade
    for s in SH:
        fx = s.get("sfx")
        if not fx: continue
        x = load(SFXF[fx]); x = x[: int(2.5 * SR)] * SFXG.get(fx, 0.25); p = int(AT(s["at"]) * SR); mix[p:p + len(x)] += x[: n - p]
    pk = np.abs(mix).max(); mix = mix / max(pk, 1e-6) * 0.89 if pk > 0.89 else mix
    sf.write(B + "mix.wav", mix[: int(DUR * SR)], SR, subtype="PCM_16"); print("audio", round(DUR, 1), "s", flush=True)

def final(n):
    open(B + "segs.txt", "w").write("".join(f"file 'seg_{i:02d}.mp4'\n" for i in range(n)))
    out = ROOT + "export/" + OUTNAME
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "segs.txt", "-i", B + "mix.wav", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", out], check=True)
    print("WROTE", out, flush=True)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "qa":
        ims = [frame(float(x)).resize((640, 360)) for x in sys.argv[2:]]; sh = Image.new("RGB", (640 * 4, 360 * ((len(ims) + 3) // 4)))
        for i, im in enumerate(ims): sh.paste(im, ((i % 4) * 640, (i // 4) * 360))
        sh.save(B + "_qa.jpg", quality=85); print("qa", B + "_qa.jpg")
    elif cmd == "seg": seg(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "audio": audio()
    elif cmd == "final": final(int(sys.argv[2]))
    elif cmd == "info": print("lines", len(LINES), "dur", round(DUR, 1), "shots", len(SH))
