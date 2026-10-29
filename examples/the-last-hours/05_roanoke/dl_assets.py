"""Download the approved D.B. Cooper visuals (assets.md sections A-F) one at a time into media/ (approved by the owner 20 Oct 2026).
Wayback / Wikimedia rate limits: slow pacing, retries with backoff, bad files (HTML error pages) moved to the archive, never deleted."""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/05_roanoke/"
BAD = "D:/why habibi/_archive/roanoke_bad_downloads/"
def is_img(p):
    if not os.path.exists(p) or os.path.getsize(p) < 8000: return False
    h = open(p, "rb").read(8)
    return h[:3] == b"\xff\xd8\xff" or h[:8] == b"\x89PNG\r\n\x1a\n" or h[:4] in (b"II*\x00", b"MM\x00*")
rows, sec = [], None
for l in open(ROOT + "research/assets.md", encoding="utf-8"):
    m = re.match(r"^## ([A-Z])\. ", l)
    if m: sec = m.group(1)
    if sec and sec in "ABCDEF" and re.match(r"^\| [A-F]\d+ \|", l):
        c = [x.strip() for x in l.strip().strip("|").split(" | ")]
        rows.append((c[0], c[1], c[3]))
rows.sort(key=lambda r: "web.archive.org" in r[2])          # Wayback items last (rate-limited)
os.makedirs(ROOT + "media", exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|^(SATELLITE[^:]*|Pexels \d+)[:.]?\s*", "", what).lower())[:38].strip("_")
    ext = ".tif" if url.lower().endswith(".tif") else ".png" if "FORMAT=image/png" in url else ".jpg"
    out = f"{ROOT}media/{rid}_{slug}{ext}"
    if is_img(out): print("have", rid, flush=True); continue
    if os.path.exists(out):
        os.makedirs(BAD, exist_ok=True); os.replace(out, BAD + os.path.basename(out) + f".{int(time.time())}.bad")
    urls = [url]
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/([0-9a-f])/([0-9a-f]{2})/(.+)$", url)
    if m: urls.append(f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{m.group(3)}/1280px-{m.group(3)}")
    code = "?"
    for attempt in range(6):
        u = urls[min(attempt // 3, len(urls) - 1)]
        r = subprocess.run(["curl", "-sL", "--max-time", "300", "-A", UA, "-o", out, "-w", "%{http_code}", u], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200" and is_img(out): break
        print("retry", rid, code, flush=True); time.sleep((60 if "web.archive.org" in u else 20) * (attempt + 1))
    print(f"{rid:4} {code} {'OK ' if is_img(out) else 'BAD'} {os.path.getsize(out) / 1e6 if os.path.exists(out) else 0:6.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(45 if "web.archive.org" in url else 8 if "wikimedia" in url else 2)
print("rows", len(rows))
