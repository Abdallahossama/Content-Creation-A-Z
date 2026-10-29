"""Download the approved Göring visuals (assets.md sections A-F minus D2/D3/D4) into media/
(approved by the owner 29 Oct 2026: "Safe set, ~417 MB"). Images as JPG/PNG, documents as PDF, video as MP4/WEBM/OGV.
Skipped: D2, D3, D4 (NARA "Restricted - Possibly (copyright)" Signal Corps reels, Content ID risk). Newsreels cut to the usable seconds:
D1 15-141 s only (the rest is other stories); D5 5-20, 80-100, 180-245 s only (women and a noose elsewhere: never fetched).
One file at a time (Commons answers 429 to bursts). Bad files are moved to the archive, never deleted.
  uv run --no-project python dl_assets.py"""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/13_goering_last_night/"
BAD = "D:/why habibi/_archive/goering_bad_downloads/"
UAW = "TheLastHoursResearch/1.0 (https://www.youtube.com/@TheLastHoursDocs; documentary research, one file at a time) curl/8"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"
SEG = {"D1": [("15", "126")], "D5": [("5", "15"), ("80", "20"), ("180", "65")]}   # start s, length s
SKIP = {"D2", "D3", "D4"}
EXTRA = []

def kind(p):
    if not os.path.exists(p) or os.path.getsize(p) < 3000: return None
    h = open(p, "rb").read(16)
    if h[:3] == b"\xff\xd8\xff": return "jpg"
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:4] == b"%PDF": return "pdf"
    if h[4:8] == b"ftyp": return "mp4"
    if h[:4] == b"\x1a\x45\xdf\xa3": return "webm"
    if h[:4] == b"OggS": return "ogv"
    if h[:4] in (b"II*\x00", b"MM\x00*"): return "tif"
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
    m = re.match(r"^\| ([A-I]\d+[a-z]?) \|", l)
    if not (m and sec and sec in "ABCDEF"): continue
    c = [x.strip() for x in l.strip().strip("|").split(" | ")]
    u = re.search(r"https?://[^\s)\]]+", c[3])
    if u and m.group(1) not in SKIP: rows.append((m.group(1), c[1], u.group(0)))
rows += EXTRA
rows.sort(key=lambda r: "wikimedia" in r[2])                    # Commons last (it rate-limits); sort is stable

os.makedirs(ROOT + "media/_raw", exist_ok=True)
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|\*\([^)]*\)\*|\*", "", what).lower())[:38].strip("_")
    base = f"{ROOT}media/{rid}_{slug}"
    have = [e for e in ("jpg", "png", "pdf", "mp4", "webm", "ogv", "tif", "html") if kind(f"{base}.{e}") or kind(f"{base}_a.{e}")]
    if have: print("have", rid, flush=True); continue
    tmp = f"{ROOT}media/_raw/{rid}.bin"
    if os.path.exists(tmp):
        os.makedirs(BAD, exist_ok=True); os.replace(tmp, BAD + f"{rid}.{int(time.time())}.bad")
    if rid in SEG:
        for j, (ss, t) in enumerate(SEG[rid]):
            out = f"{base}_{'abcd'[j]}.mp4"; code = ff(url, out, ss, t); k = kind(out)
            print(f"{rid:4} {code} {'OK ' if k else 'BAD'} {k} {os.path.getsize(out) / 1e6 if os.path.exists(out) else 0:7.2f} MB  {os.path.basename(out)}", flush=True)
        continue
    if url.endswith(".m3u8"):
        out = f"{base}.mp4"; code = ff(url, out); k = kind(out)
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
