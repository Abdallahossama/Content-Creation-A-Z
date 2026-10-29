"""Add the subscribe asks to a Last Hours file that is already rendered (user, 25 Oct 2026; LESSONS 37):
- END: one spoken line ("If you want the next file, subscribe." / "If you want that file, subscribe.") in the creator's cloned voice,
  0.7 s into the 20 s end card, after the comment question; matched to the voice level of the last spoken line; the music dips 7 dB under it.
- MID (optional --badge SECONDS): the silent 4 s "SUBSCRIBE FOR THE NEXT FILE" pill, top-left (same look as the renderers' subpop),
  with its soft whoosh. Without --badge the video stream is copied untouched (only the audio changes).
  uv run --no-project --with numpy --with soundfile --with pillow python cta_patch.py IN.mp4 OUT.mp4 next|that [--badge 602]"""
import sys, os, subprocess, tempfile, shutil
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
D = "D:/why habibi/_newchannel/_cta/"; SFX = "D:/why habibi/_newchannel/sfx/"; SR = 48000; TAIL = 20.0
RED, BONE = (178, 34, 34), (236, 230, 214)

def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def load(p, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()
def rms(a): v = a[np.abs(a).max(1) > 1e-4] if a.ndim > 1 else a; return float(np.sqrt(np.mean(v ** 2))) if len(v) else 1e-6

def badge_frames(folder):
    """4 s at 30 fps: the red pill slides in from the left, holds, slides out (renderers' subpop, 640 x 110 crop at y 110)"""
    f = ImageFont.truetype("C:/Windows/Fonts/courbd.ttf", 34)
    for i in range(120):
        u = i / 30.0; e = lambda x: max(0.0, min(1.0, x)) ** 2 * (3 - 2 * max(0.0, min(1.0, x)))
        k = e(u / 0.4) * e((4.0 - u) / 0.4); x = 40 - (1 - k) * 640
        im = Image.new("RGBA", (700, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((x, 10, x + 600, 82), 36, fill=RED + (int(235 * k),))
        d.text((x + 300, 47), "SUBSCRIBE FOR THE NEXT FILE", font=f, fill=BONE + (int(255 * k),), anchor="mm")
        im.save(os.path.join(folder, f"b{i:03d}.png"))

def main():
    src, out, which = sys.argv[1], sys.argv[2], sys.argv[3]
    badge = float(sys.argv[sys.argv.index("--badge") + 1]) if "--badge" in sys.argv else None
    T = dur(src); vo_end = T - TAIL; t_cta = vo_end + 0.7
    a = load(src); n = len(a)
    ref = rms(a[int((vo_end - 3.5) * SR): int((vo_end - 0.3) * SR)])                 # the last spoken line (voice over the music bed)
    cta = load(D + f"cta_{which}.wav"); cta = cta / max(rms(cta), 1e-6) * ref * 0.95
    i0 = int(t_cta * SR); L = len(cta)
    g = np.ones(n, np.float32); r = int(0.3 * SR); lo = 10 ** (-7 / 20)              # music dips 7 dB under the line, 0.3 s ramps
    a0, a1 = max(0, i0 - r), min(n, i0 + L + r)
    g[a0:a1] = lo; g[a0:a0 + r] = np.linspace(1, lo, r); g[a1 - r:a1] = np.linspace(lo, 1, r)
    a = a * g[:, None]; seg = a[i0:i0 + L] + cta[: n - i0]
    m = np.abs(seg); T0 = 0.85; over = m > T0                                          # soft-limit ONLY the line (never the whole file)
    seg[over] = np.sign(seg[over]) * (T0 + 0.12 * np.tanh((m[over] - T0) / 0.12)); a[i0:i0 + L] = seg
    if badge is not None:
        w = load(SFX + "whoosh_fast_transition.mp3"); w = w / (np.abs(w).max() + 1e-9) * ref * 3.2 * 10 ** (-24 / 20)
        j = int((badge - 0.05) * SR); a[j:j + len(w)] += w[: n - j]
    pk = np.abs(a).max(); print("peak after", round(float(pk), 3))
    tmp = tempfile.mkdtemp(); wav = os.path.join(tmp, "a.wav"); sf.write(wav, a, SR, subtype="FLOAT")
    if badge is None:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out]
    else:
        fr = os.path.join(tmp, "b"); os.makedirs(fr); badge_frames(fr)
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-framerate", "30", "-i", os.path.join(fr, "b%03d.png"), "-i", wav,
               "-filter_complex", f"[1:v]setpts=PTS+{badge}/TB[b];[0:v][b]overlay=0:110:eof_action=pass[v]",
               "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); shutil.rmtree(tmp, ignore_errors=True)
    print(f"{os.path.basename(out)}: CTA '{which}' at {t_cta:.2f}s (end card {vo_end:.2f}s), badge {badge}, length {dur(out):.2f}s")

if __name__ == "__main__":
    main()
