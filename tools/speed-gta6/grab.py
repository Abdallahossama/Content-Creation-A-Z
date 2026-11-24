"""grab: fast cut of a window from a long YouTube DASH stream (fragmented MP4) using the sidx index.
Fetches init (ftyp+moov) + only the fragments covering [t0, t1] with HTTP range requests, for video and audio,
then muxes them. Needs the direct URLs from `yt-dlp --js-runtimes node -g -f "bv*[ext=mp4]+ba[ext=m4a]"`.
  python grab.py <urls file> <t0> <t1> <out.mp4>"""
import sys, struct, subprocess, urllib.request, os, tempfile

def rng(url, a, b):
    req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()

def boxes(buf, off=0):
    i = 0
    while i + 8 <= len(buf):
        size, typ = struct.unpack(">I4s", buf[i:i + 8]); hdr = 8
        if size == 1: size = struct.unpack(">Q", buf[i + 8:i + 16])[0]; hdr = 16
        yield typ.decode("latin1"), off + i, size, hdr
        if size == 0: break
        i += size

def cut(url, t0, t1, path):
    head = rng(url, 0, 400_000)
    init_end = None; sidx = None
    for typ, pos, size, hdr in boxes(head):
        if typ == "moov": init_end = pos + size
        if typ == "sidx": sidx = (pos, size, hdr); break
        if pos + size > len(head) and typ in ("moov", "free", "uuid", "styp"):     # box runs past what we read: fetch more
            head += rng(url, len(head), pos + size + 400_000)
    if sidx is None:
        for typ, pos, size, hdr in boxes(head):
            if typ == "moov": init_end = pos + size
            if typ == "sidx": sidx = (pos, size, hdr); break
    if sidx is None: raise RuntimeError("no sidx in header")
    pos, size, hdr = sidx
    if pos + size > len(head): head += rng(url, len(head), pos + size)
    b = head[pos + hdr: pos + size]; ver = b[0]
    timescale = struct.unpack(">I", b[8:12])[0]
    if ver == 0: ept, foff = struct.unpack(">II", b[12:20]); p = 20
    else: ept, foff = struct.unpack(">QQ", b[12:28]); p = 28
    count = struct.unpack(">H", b[p + 2:p + 4])[0]; p += 4
    off = pos + size + foff; t = ept / timescale; a = bb = None
    for _ in range(count):
        ref, dur = struct.unpack(">II", b[p:p + 8]); p += 12
        rsize = ref & 0x7FFFFFFF; d = dur / timescale
        if a is None and t + d > t0: a = off; start_t = t
        if t < t1: bb = off + rsize - 1
        off += rsize; t += d
    data = head[:init_end] + rng(url, a, bb)
    open(path, "wb").write(data); return start_t

urls = [l.strip() for l in open(sys.argv[1]) if l.strip()]
t0, t1, out = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(out)))
sv = cut(urls[0], t0, t1, f"{tmp}/v.mp4"); sa = cut(urls[1], t0, t1, f"{tmp}/a.m4a")
# both pieces keep their original timestamps; trim to the exact window
def st(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=start_time", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
    try: return float(r)
    except ValueError: return 0.0
subprocess.run(["ffmpeg", "-v", "error", "-y", "-copyts", "-i", f"{tmp}/v.mp4", "-i", f"{tmp}/a.m4a",
                "-vf", f"trim=start={t0}:end={t1},setpts=PTS-STARTPTS", "-af", f"atrim=start={t0}:end={t1},asetpts=PTS-STARTPTS",
                "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out], check=True)
for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
os.rmdir(tmp); print(out, round(sv, 1), round(sa, 1))
