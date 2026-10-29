"""Remove time ranges from a finished video (spoken ident, mid-video ask), frame-accurate, with 30 ms audio fades at every seam.
  python cut_ranges.py <in.mp4> <out.mp4> a1:b1 [a2:b2 ...]      (seconds; [a, b) is removed)"""
import sys, subprocess

def cut(src, out, ranges):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    keep, t = [], 0.0
    for a, b in sorted(ranges):
        if a > t: keep.append((t, a))
        t = b
    if t < dur: keep.append((t, dur))
    f, n = [], len(keep)
    for i, (a, b) in enumerate(keep):
        fade = (f",afade=t=in:st=0:d=0.03" if i else "") + (f",afade=t=out:st={b - a - 0.03:.3f}:d=0.03" if i < n - 1 else "")
        f.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS{fade}[a{i}]")
    f.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                    "-movflags", "+faststart", out], check=True)
    removed = sum(b - a for a, b in ranges)
    print(out, f"removed {removed:.2f} s:", ", ".join(f"{a:.2f}-{b:.2f}" for a, b in sorted(ranges)))

if __name__ == "__main__":
    cut(sys.argv[1], sys.argv[2], [tuple(map(float, r.split(":"))) for r in sys.argv[3:]])
