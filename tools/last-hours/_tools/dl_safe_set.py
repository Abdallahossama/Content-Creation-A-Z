"""Download an approved visuals safe set listed in <episode>/research/assets.md into <episode>/media/.
Owner approved 30 Oct 2026 ("yes download both and go ahead"): 15_uss_indianapolis A1-A35 (249.86 MB),
16_cole_roe_1937 A1-A14, A17, C1-C5, D1, F1-F7 (157.99 MB). Same rules as 14's dl_assets.py: one file at a time,
Commons last (it answers 429 to bursts), HABS TIFFs as Commons' 3840 px JPEG, bad files moved to the archive, never deleted.
Film segments: only the seconds checked as safe in assets.md.
  uv run --no-project python dl_safe_set.py indy|coleroe"""
import re, time, os, subprocess, sys
EP = {"indy": ("D:/why habibi/_newchannel/15_uss_indianapolis/", [f"A{i}" for i in range(1, 36)],
               {"A34": [("172", "82"), ("298", "64")]}),                       # 428-NPC-12522: 172-254 s raft/plane; 298-362 s pickups (caution)
      "coleroe": ("D:/why habibi/_newchannel/16_cole_roe_1937/",
                  [f"A{i}" for i in range(1, 15)] + ["A17"] + [f"C{i}" for i in range(1, 6)] + ["D1"] + [f"F{i}" for i in range(1, 8)], {})}
ROOT, IDS, SEG = EP[sys.argv[1]]
BAD = "D:/why habibi/_archive/bad_downloads/"
UAW = "TheLastHoursResearch/1.0 (https://www.youtube.com/@TheLastHoursDocs; documentary research, one file at a time) curl/8"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"

def kind(p):
    if not os.path.exists(p) or os.path.getsize(p) < 3000: return None
    h = open(p, "rb").read(16)
    if h[:3] == b"\xff\xd8\xff":
        with open(p, "rb") as f: f.seek(-64, 2); return "jpg" if b"\xff\xd9" in f.read() else None
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:4] == b"%PDF": return "pdf"
    if h[4:8] == b"ftyp": return "mp4"
    if h[:4] in (b"II*\x00", b"MM\x00*"): return "tif"
    if b"<html" in open(p, "rb").read(3000).lower() or b"<!doctype" in h.lower(): return "html"
    return None
def fetch(url, out, tries=4):
    code = "?"; wm = "wikimedia" in url
    for attempt in range(6 if wm else tries):
        r = subprocess.run(["curl", "-sL", "--max-time", "1200", "-A", UAW if wm else UA, "-o", out, "-w", "%{http_code}", url],
                           capture_output=True, text=True); code = r.stdout.strip()
        if code == "200" and kind(out) not in (None, "html"): return code
        print("retry", code, kind(out), url[:90], flush=True); time.sleep((60 if wm and code == "429" else 12) * (attempt + 1))
    return code
def ff(url, out, ss, t):
    for attempt in range(3):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-user_agent", UA, "-ss", ss, "-i", url, "-t", t, "-c", "copy", "-movflags", "+faststart", out])
        if kind(out) == "mp4": return "200"
        print("retry ffmpeg", url[:90], flush=True); time.sleep(15)
    return "ERR"

rows = []
for l in open(ROOT + "research/assets.md", encoding="utf-8"):
    m = re.match(r"^\| ([A-I]\d+) \|", l)
    if not m or m.group(1) not in IDS or any(r[0] == m.group(1) for r in rows): continue
    c = [x.strip() for x in l.strip().strip("|").split(" | ")]
    u = re.search(r"https?://\S+", c[3])                          # plain URL cell; NHHC file names carry "(Findings)"
    if u and "newspapers.lib.utah.edu" in u.group(0): print("browser only (curl gets 418):", m.group(1), u.group(0), flush=True); continue
    if u: rows.append((m.group(1), c[1], re.sub(r"(archive\.org/download/[^/]+/page/n\d+)\.jpg$", r"\1_w2400.jpg", u.group(0))))
missing = [i for i in IDS if not any(r[0] == i for r in rows)]
print("rows", len(rows), "missing", missing, flush=True)
rows.sort(key=lambda r: "wikimedia" in r[2])

os.makedirs(ROOT + "media/_raw", exist_ok=True)
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|\*", "", what).lower())[:38].strip("_")
    base = f"{ROOT}media/{rid}_{slug}"
    if any(kind(f"{base}.{e}") or kind(f"{base}_a.{e}") for e in ("jpg", "png", "pdf", "mp4", "tif")): print("have", rid, flush=True); continue
    tmp = f"{ROOT}media/_raw/{rid}.bin"
    if os.path.exists(tmp):
        os.makedirs(BAD, exist_ok=True); os.replace(tmp, BAD + f"{rid}.{int(time.time())}.bad")
    if rid in SEG:
        for j, (ss, t) in enumerate(SEG[rid]):
            out = f"{base}_{'abcdef'[j]}.mp4"; code = ff(url, out, ss, t)
            print(f"{rid:4} {code} {kind(out)} {os.path.getsize(out) / 1048576 if os.path.exists(out) else 0:7.2f} MB  {os.path.basename(out)}", flush=True)
        continue
    code = fetch(url, tmp); k = kind(tmp)
    if k in (None, "html"):
        print(f"{rid:4} {code} BAD ({k})  {url[:100]}", flush=True); continue
    out = f"{base}.{k}"; os.replace(tmp, out)
    print(f"{rid:4} {code} OK  {k} {os.path.getsize(out) / 1048576:7.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(20 if "wikimedia" in url else 3 if "archive.org" in url else 2)
print("done", flush=True)
