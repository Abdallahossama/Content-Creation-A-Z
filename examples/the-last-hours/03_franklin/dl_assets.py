"""Download the approved Franklin visuals (assets.md sections A-G) one at a time into media/ (approved by the owner 20 Oct 2026)."""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/03_franklin/"
def is_img(p):
    if not os.path.exists(p) or os.path.getsize(p) < 20000: return False
    head = open(p, "rb").read(8)
    return head[:3] == b"\xff\xd8\xff" or head[:8] == b"\x89PNG\r\n\x1a\n"
lines = open(ROOT + "research/assets.md", encoding="utf-8").read().splitlines()
rows, sec = [], None
for l in lines:
    m = re.match(r"^## ([A-I])\. ", l)
    if m: sec = m.group(1)
    if sec and sec in "ABCDEFG" and re.match(r"^\| [A-G]\d+ \|", l):
        cols = [c.strip() for c in l.strip().strip("|").split(" | ")]
        rows.append((cols[0], cols[1], cols[3]))
os.makedirs(ROOT + "media", exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"
for rid, what, url in rows:
    if rid == "F5":
        url = "https://assets.science.nasa.gov/dynamicimage/assets/science/esd/eo/images/imagerecords/148000/148107/canada_oli_2014181_lrg.jpg?w=4000"
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"^(ENGRAVING|LITHOGRAPH|PHOTO[^.:]*|PORTRAIT PHOTO-PRINT[^:]*|SATELLITE)[.:]\s*", "", what).lower())[:38].strip("_")
    ext = ".png" if "FORMAT=image/png" in url else ".jpg"
    out = f"{ROOT}media/{rid}_{slug}{ext}"
    if is_img(out): print("have", rid, flush=True); continue
    if os.path.exists(out):                                   # an error page saved as .jpg: keep it aside, never delete
        os.makedirs("D:/why habibi/_archive/franklin_bad_downloads", exist_ok=True)
        os.replace(out, "D:/why habibi/_archive/franklin_bad_downloads/" + os.path.basename(out) + f".{int(time.time())}.html")
    urls = [url]
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/([0-9a-f])/([0-9a-f]{2})/(.+)$", url)
    if m: urls.append(f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{m.group(3)}/1280px-{m.group(3)}")
    code = "?"
    for attempt in range(6):
        u = urls[min(attempt // 2, len(urls) - 1)]
        r = subprocess.run(["curl", "-sL", "-A", UA, "-o", out, "-w", "%{http_code}", u], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200" and is_img(out): break
        print("retry", rid, code, flush=True); time.sleep(15 * (attempt + 1))
    print(f"{rid:4} {code} {'OK ' if is_img(out) else 'BAD'} {os.path.getsize(out) / 1e6:6.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(8 if "wikimedia" in url else 1)
print("rows", len(rows))
