"""Download the approved Gaddafi visuals into media/ (owner, 30 Oct 2026: "yes download the gaddafi stuff and use the first clinton line").
research/assets.md: A1-A39 (public domain) + A47-A54 (Pexels); NATO-terms items (A40-A46, V14-V16) skipped; the real footage V1-V13
(PD, EC CC BY 4.0, Al Jazeera CC BY 3.0) is cut to the men-only seconds listed in section V and RE-ENCODED, so a keyframe never drags an
unchecked frame (Gaddafi's female guards) onto disk. Commons SVG flags come as Commons' own PNG rendering. One file at a time, Commons last.
  uv run --no-project python dl_assets.py"""
import re, time, os, subprocess
ROOT = "D:/why habibi/_newchannel/17_gaddafi_last_day/"; M = ROOT + "media/"; BAD = "D:/why habibi/_archive/bad_downloads/"
UAW = "TheLastHoursResearch/1.0 (https://www.youtube.com/@TheLastHoursDocs; documentary research, one file at a time) curl/8"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"
IDS = [f"A{i}" for i in list(range(1, 40)) + list(range(47, 55))] + [f"V{i}" for i in range(1, 14)]
W = lambda *p: [(a, b) for a, b in p]                                 # men-only windows (start s, end s), 0.3 s inside each edge below
SEG = {"A30": W((10, 145)), "A31": W((15, 210)), "A32": W((1, 35)),
       "V1": W((27, 192), (200, 328)), "V2": W((7, 60), (139, 195)), "V3": W((21, 26), (60, 82)), "V4": W((10, 236), (277, 326)),
       "V5": W((15, 68)), "V6": W((5, 34), (96, 122), (155, 195), (212, 218), (230, 232)), "V7": W((59, 66), (81, 95), (104, 121)),
       "V8": W((20, 46), (142, 150), (196, 198)), "V9": W((5, 15), (19, 23), (36, 38), (47, 62), (75, 92)),
       "V10": W((0, 4), (7, 11), (15, 18), (53, 54), (58, 59)), "V11": W((0, 192)), "V12": W((0, 132)),
       "V13": W((6, 14), (20, 30), (40, 48), (196, 258))}

def kind(p):
    if not os.path.exists(p) or os.path.getsize(p) < 100: return None
    h = open(p, "rb").read(16)
    if h[:3] == b"\xff\xd8\xff":
        with open(p, "rb") as f: f.seek(-64, 2); return "jpg" if b"\xff\xd9" in f.read() else None
    if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if h[:4] == b"%PDF": return "pdf"
    if h[4:8] == b"ftyp": return "mp4"
    if h[:4] == b"\x1a\x45\xdf\xa3": return "webm"
    if b"<html" in open(p, "rb").read(3000).lower() or b"<!doctype" in h.lower(): return "html"
    return None
def svg_png(u):
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+\.svg)$", u)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m[1]}/{m[2]}/{m[3]}/1600px-{m[3]}.png" if m else u
def fetch(url, out, tries=4):
    code = "?"; wm = "wikimedia" in url
    for attempt in range(6 if wm else tries):
        r = subprocess.run(["curl", "-sL", "--max-time", "1200", "-A", UAW if wm else UA, "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200" and kind(out) not in (None, "html"): return code
        print("retry", code, kind(out), url[:90], flush=True); time.sleep((60 if wm and code == "429" else 12) * (attempt + 1))
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
    u = re.search(r"https?://[^\s)\]]+", c[3])
    if u: rows.append((m.group(1), c[1], svg_png(u.group(0))))
print("rows", len(rows), "missing", [i for i in IDS if not any(r[0] == i for r in rows)], flush=True)
rows.sort(key=lambda r: "wikimedia" in r[2])
os.makedirs(M + "_raw", exist_ok=True)
for rid, what, url in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|\*|\([^)]*\)", "", what).lower())[:38].strip("_")
    base = f"{M}{rid}_{slug}"
    if any(kind(f"{base}.{e}") or kind(f"{base}_a.mp4") for e in ("jpg", "png", "pdf", "mp4", "webm")): print("have", rid, flush=True); continue
    if rid in SEG:
        for j, (a, b) in enumerate(SEG[rid]):
            out = f"{base}_{'abcdefgh'[j]}.mp4"; code = cut(url, out, a, b)
            print(f"{rid:4} {code} {kind(out)} {os.path.getsize(out) / 1048576 if os.path.exists(out) else 0:7.2f} MB  {os.path.basename(out)}  [{a}-{b} s]", flush=True)
        continue
    tmp = f"{M}_raw/{rid}.bin"
    if os.path.exists(tmp): os.makedirs(BAD, exist_ok=True); os.replace(tmp, BAD + f"{rid}.{int(time.time())}.bad")
    code = fetch(url, tmp); k = kind(tmp)
    if k in (None, "html"): print(f"{rid:4} {code} BAD ({k})  {url[:100]}", flush=True); continue
    out = f"{base}.{k}"; os.replace(tmp, out)
    print(f"{rid:4} {code} OK  {k} {os.path.getsize(out) / 1048576:7.2f} MB  {os.path.basename(out)}", flush=True)
    time.sleep(20 if "wikimedia" in url else 2)
print("done", flush=True)
