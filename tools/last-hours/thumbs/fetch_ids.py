import re, sys, os, subprocess
root, ids = sys.argv[1], sys.argv[2].split(",")
M = root + "media/"; os.makedirs(M, exist_ok=True)
UA = "TheLastHoursResearch/1.0 (documentary research) curl/8"
for l in open(root + "research/assets.md", encoding="utf-8"):
    m = re.match(r"\|\s*([A-Z]\d+)\s*\|(.*)", l)
    if not m or m.group(1) not in ids: continue
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    urls = re.findall(r"https?://[^\s|)\]]+", l)
    urls = [u for u in urls if "upload.wikimedia.org" in u or "pexels.com" in u or "loc.gov" in u or u.endswith((".jpg",".png",".tif",".mp4"))] or urls
    desc = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*", "", cells[1]).lower())[:40].strip("_")
    u = urls[0]; ext = os.path.splitext(u.split("?")[0])[1] or ".jpg"
    out = M + m.group(1) + "_" + desc + ext
    r = subprocess.run(["curl", "-sL", "-A", UA, "-o", out, "-w", "%{http_code}", u], capture_output=True, text=True)
    print(m.group(1), r.stdout, os.path.getsize(out) if os.path.exists(out) else 0, u[:90])
