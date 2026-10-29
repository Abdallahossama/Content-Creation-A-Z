"""Download the approved al-Khuld Hall visuals (assets.md sections A-F, 94 items, + H1 segment only) into media/
(approved by the owner 24 Oct 2026: "yes to all, go ahead"). Images as JPG/PNG, AAD cables as PDF, FRUS pages as HTML,
video as MP4/WEBM. HLS streams are copied with ffmpeg. Long reels are cut to the seconds we use, so nothing else is ever on disk:
D2 6:45-7:35 only; H1 51:00-54:05 only (the NARA reel's girls are at 39:30-46:30, its IED wreckage from 54:20: never fetched).
One file at a time (Commons answers 429 to bursts). Bad files are moved to the archive, never deleted.
  uv run --no-project python dl_assets.py"""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/11_khuld_hall/"
BAD = "D:/why habibi/_archive/khuld_bad_downloads/"
UAW = "TheLastHoursResearch/1.0 (https://www.youtube.com/@TheLastHoursDocs; documentary research, one file at a time) curl/8"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"
SEG = {"D2": ("6:45", "50"), "H1": ("51:00", "185")}           # start, seconds
EXTRA = [("H1", "NARA reel: capture of most wanted, spider hole, medical exam (51:00-54:05 only)",
          "https://catalog.archives.gov/medialz/mopix/330/DIMOC/330-dimoc-6594.mp4")]

def kind(p):
    if not os.path.exists(p) or os.path.getsize(p) < 3000: return None
    h = open(p, "rb").read(16)
    if h[:3] == b"\xff\xd8\xff": return "jpg"
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:4] == b"%PDF": return "pdf"
    if h[4:8] == b"ftyp": return "mp4"
    if h[:4] == b"\x1a\x45\xdf\xa3": return "webm"
    if b"<html" in open(p, "rb").read(3000).lower() or b"<!doctype" in h.lower(): return "html"
    return None
def fetch(url, out, tries=4, ref=None):
    code = "?"; wm = "wikimedia" in url
    for attempt in range(6 if wm else tries):
        cmd = ["curl", "-sL", "--max-time", "900", "-A", UAW if wm else UA, "-o", out, "-w", "%{http_code}", url]
        if ref: cmd[1:1] = ["-e", ref]
        r = subprocess.run(cmd, capture_output=True, text=True); code = r.stdout.strip()
        if code == "200" and kind(out): return code
        print("retry", code, url[:90], flush=True); time.sleep((60 if wm and code == "429" else 12) * (attempt + 1))
    return code
def ff(url, out, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error", "-y", "-user_agent", UA]
    if ss: cmd += ["-ss", ss]
    cmd += ["-i", url]
    if t: cmd += ["-t", t]
    cmd += ["-c", "copy", "-movflags", "+faststart", out]
    for attempt in range(3):
        subprocess.run(cmd, check=False)
        if kind(out) == "mp4": return "200"
        print("retry ffmpeg", url[:90], flush=True); time.sleep(15)
    return "ERR"

rows, sec = [], None
for l in open(ROOT + "research/assets.md", encoding="utf-8"):
    m = re.match(r"^## ([A-Z])\. ", l)
    if m: sec = m.group(1)
    m = re.match(r"^\| ([A-I]\d+) \|", l)
    if not (m and sec and sec in "ABCDEF"): continue
    c = [x.strip() for x in l.strip().strip("|").split(" | ")]
    u = re.search(r"https?://[^\s)\]]+", c[3])
    if u: rows.append((m.group(1), c[1], u.group(0)))
rows += EXTRA
rows.sort(key=lambda r: "wikimedia" in r[2])                    # Commons last (it rate-limits); sort is stable

os.makedirs(ROOT + "media/_raw", exist_ok=True)
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|\*\([^)]*\)\*|\*", "", what).lower())[:38].strip("_")
    base = f"{ROOT}media/{rid}_{slug}"
    have = [e for e in ("jpg", "png", "pdf", "mp4", "webm", "html") if kind(f"{base}.{e}")]
    if have: print("have", rid, flush=True); continue
    tmp = f"{ROOT}media/_raw/{rid}.bin"
    if os.path.exists(tmp):
        os.makedirs(BAD, exist_ok=True); os.replace(tmp, BAD + f"{rid}.{int(time.time())}.bad")
    if url.endswith(".m3u8") or rid in SEG:
        ss, t = SEG.get(rid, (None, None)); out = f"{base}.mp4"; code = ff(url, out, ss, t); k = kind(out)
    else:
        ref = "https://aad.archives.gov/aad/fielded-search.jsp?dt=2776&cat=WR43&tf=X&bc=,sl" if "aad.archives" in url else None
        code = fetch(url, tmp, ref=ref); k = kind(tmp)
        if k is None:
            print(f"{rid:4} {code} BAD (unknown type)", flush=True); continue
        out = f"{base}.{k}"; os.replace(tmp, out)
    ok = k is not None
    print(f"{rid:4} {code} {'OK ' if ok else 'BAD'} {k} {os.path.getsize(out) / 1e6 if os.path.exists(out) else 0:7.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(20 if "wikimedia" in url else 3 if "archive.org" in url else 2)
print("rows", len(rows))
