"""Download the approved Andrée visuals (assets.md sections A-F + alternates I5, I25, I26, I27) into media/ (approved by the owner
23 Oct 2026: "yes download them"). JP2 pages (Ymer plates, newspapers) are converted to JPG with ffmpeg, the TIFF blueprint to PNG.
One file at a time (Commons answers 429 to bursts). Bad files are moved to the archive, never deleted.
  uv run --no-project python dl_assets.py"""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/08_andree/"
BAD = "D:/why habibi/_archive/andree_bad_downloads/"
OK_I = {"I5", "I25", "I26", "I27"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"

def kind(p):
    if not os.path.exists(p) or os.path.getsize(p) < 8000: return None
    h = open(p, "rb").read(12)
    if h[:3] == b"\xff\xd8\xff": return "jpg"
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:4] in (b"II*\x00", b"MM\x00*"): return "tif"
    if h[4:8] == b"jP  " or h[:4] == b"\xff\x4f\xff\x51": return "jp2"
    return None
def fetch(url, out, tries=5):
    code = "?"
    for attempt in range(tries):
        r = subprocess.run(["curl", "-sL", "--max-time", "300", "-A", UA, "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200" and kind(out): return code
        print("retry", code, url[:80], flush=True); time.sleep(15 * (attempt + 1))
    return code

rows, sec = [], None
for l in open(ROOT + "research/assets.md", encoding="utf-8"):
    m = re.match(r"^## ([A-Z])\. ", l)
    if m: sec = m.group(1)
    m = re.match(r"^\| ([A-I]\d+) \|", l)
    if not (m and sec): continue
    rid = m.group(1)
    if not (sec in "ABCDEF" or rid in OK_I): continue
    c = [x.strip() for x in l.strip().strip("|").split(" | ")]
    rows.append((rid, c[1], c[3]))

os.makedirs(ROOT + "media/_raw", exist_ok=True)
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|\*\([^)]*\)\*|\*", "", what).lower())[:38].strip("_")
    base = f"{ROOT}media/{rid}_{slug}"
    have = [e for e in ("jpg", "png") if kind(f"{base}.{e}")]
    if have: print("have", rid, flush=True); continue
    tmp = f"{ROOT}media/_raw/{rid}.bin"
    if os.path.exists(tmp):
        os.makedirs(BAD, exist_ok=True); os.replace(tmp, BAD + f"{rid}.{int(time.time())}.bad")
    code = fetch(url, tmp); k = kind(tmp)
    if k in ("jpg", "png"):
        out = f"{base}.{k}"; os.replace(tmp, out)
    elif k in ("jp2", "tif"):
        src = f"{ROOT}media/_raw/{rid}.{k}"; os.replace(tmp, src)
        out = f"{base}.{'jpg' if k == 'jp2' else 'png'}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src] + (["-q:v", "2"] if k == "jp2" else []) + [out], check=False)
    else:
        print(f"{rid:4} {code} BAD (not an image)", flush=True); continue
    ok = kind(out) in ("jpg", "png")
    print(f"{rid:4} {code} {'OK ' if ok else 'BAD'} {k} {os.path.getsize(out) / 1e6 if os.path.exists(out) else 0:6.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(8 if "wikimedia" in url else 3 if "archive.org" in url else 2)
print("rows", len(rows))
