"""Download the approved Muslim Brotherhood visuals into media/ (owner, 31 Oct 2026: "Yes + extras").
research/assets.md: A1-A55 (PD / CC0 / CC BY) + V1, V2 (Universal Newsreel, PD) cut to the checked seconds and RE-ENCODED (V2 has women
at 0:10.5-0:12.5 and 0:26.5-0:28) + V5 (1954 speech audio) + N1, N2 (1948-49 front pages, archive.org page images) + H1 (the emblem,
in-video only). Unchecked reels V3, V4 skipped. Commons images wider than 4000 px come as Commons' 3840 px rendering; SVG as 1920 px PNG.
  uv run --no-project python dl_assets.py"""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/18_muslim_brotherhood/"; M = ROOT + "media/"; BAD = "D:/why habibi/_archive/bad_downloads/"
UAW = "TheLastHoursResearch/1.0 (https://www.youtube.com/@TheLastHoursDocs; documentary research, one file at a time) curl/8"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"
IDS = [f"A{i}" for i in range(1, 56)] + ["V1", "V2", "V5"]
SEG = {"V1": [(12, 50)], "V2": [(13, 16), (21, 26), (28, 40)]}       # checked seconds (assets.md section V), 0.3 s inside each edge
EXTRA = [("N1", "wilmington news journal 28 dec 1948 p1", "https://archive.org/download/wilmington-news-journal-1948-12-28/page/n0.jpg"),
         ("N2", "monroe morning world 13 feb 1949", "https://archive.org/download/monroe-morning-world-1949-02-13/page/n12.jpg"),
         ("H1", "muslim brotherhood emblem", "https://upload.wikimedia.org/wikipedia/commons/1/1b/Muslim_Brotherhood_Emblem.svg")]

def kind(p):
    if not os.path.exists(p) or os.path.getsize(p) < 100: return None
    h = open(p, "rb").read(16)
    if h[:3] == b"\xff\xd8\xff": return "jpg"
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:4] == b"%PDF": return "pdf"
    if h[4:8] == b"ftyp": return "mp4"
    if h[:4] == b"OggS": return "oga"
    if h[:4] == b"\x1a\x45\xdf\xa3": return "webm"
    if h[:4] == b"II*\x00" or h[:4] == b"MM\x00*": return "tif"
    if b"<html" in open(p, "rb").read(3000).lower() or b"<!doctype" in h.lower(): return "html"
    return None
def commons(u, px):
    """SVG -> 1920 px PNG; a raster wider than 4000 px -> Commons' 3840 px JPEG (saves ~80 MB on the Highsmith files)"""
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", u)
    if not m: return u
    if m[3].lower().endswith(".svg"): return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m[1]}/{m[2]}/{m[3]}/1920px-{m[3]}.png"
    w = re.match(r"(\d+)\s*[×x]", px or "")
    if w and int(w.group(1)) > 4000 and re.search(r"\.(jpe?g|tiff?|png)$", m[3], re.I):
        name = m[3] + (".jpg" if re.search(r"\.tiff?$", m[3], re.I) else "")
        return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m[1]}/{m[2]}/{m[3]}/3840px-{name}"
    return u
def fetch(url, out, tries=4):
    code = "?"; wm = "wikimedia" in url
    for attempt in range(6 if wm else tries):
        r = subprocess.run(["curl", "-sL", "--max-time", "1200", "-A", UAW if wm else UA, "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200" and kind(out) not in (None, "html"): return code
        print("retry", code, kind(out), url[:90], flush=True); time.sleep((60 if wm and code == "429" else 10) * (attempt + 1))
    return code
def cut(url, out, a, b):
    """exact window [a+0.3, b-0.3], re-encoded (no keyframe spill), audio kept"""
    s, t = a + 0.3, max(0.4, b - a - 0.6)
    for attempt in range(3):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-user_agent", UA, "-ss", f"{s:.2f}", "-i", url, "-t", f"{t:.2f}", "-c:v", "libx264", "-crf", "16",
                        "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
        if kind(out) == "mp4": return "200"
        print("retry ffmpeg", url[:90], flush=True); time.sleep(15)
    return "ERR"

rows = []
for l in open(ROOT + "research/assets.md", encoding="utf-8"):
    m = re.match(r"^\| ([AV]\d+) \|", l)
    if not m or m.group(1) not in IDS or any(r[0] == m.group(1) for r in rows): continue
    c = [x.strip() for x in l.strip().strip("|").split(" | ")]
    u = re.search(r"https?://\S+?(?=[\s)\]|]|$)", c[3])
    if u: rows.append((m.group(1), c[1], commons(u.group(0), c[4] if len(c) > 4 else "")))
print("rows", len(rows), "missing", [i for i in IDS if not any(r[0] == i for r in rows)], flush=True)
rows = sorted(rows, key=lambda r: "wikimedia" in r[2]) + [(i, w, commons(u, "")) for i, w, u in EXTRA]
os.makedirs(M + "_raw", exist_ok=True)
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|\*|\([^)]*\)", "", what).lower())[:38].strip("_")
    base = f"{M}{rid}_{slug}"
    if any(kind(f"{base}.{e}") for e in ("jpg", "png", "pdf", "mp4", "oga", "tif")) or kind(f"{M}{rid}a_{slug}.mp4"): print("have", rid, flush=True); continue
    if rid in SEG:
        for j, (a, b) in enumerate(SEG[rid]):
            out = f"{M}{rid}{'abcdefgh'[j]}_{slug}.mp4"; code = cut(url, out, a, b)
            print(f"{rid:4} {code} {kind(out)} {os.path.getsize(out) / 1048576 if os.path.exists(out) else 0:7.2f} MB  {os.path.basename(out)}  [{a}-{b} s]", flush=True)
        continue
    tmp = f"{M}_raw/{rid}.bin"
    if os.path.exists(tmp): os.makedirs(BAD, exist_ok=True); os.replace(tmp, BAD + f"{rid}.{int(time.time())}.bad")
    code = fetch(url, tmp); k = kind(tmp)
    if k in (None, "html"): print(f"{rid:4} {code} BAD ({k})  {url[:110]}", flush=True); continue
    out = f"{base}.{k}"; os.replace(tmp, out)
    print(f"{rid:4} {code} OK  {k} {os.path.getsize(out) / 1048576:7.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(6 if "wikimedia" in url else 2)
print("done", flush=True)
