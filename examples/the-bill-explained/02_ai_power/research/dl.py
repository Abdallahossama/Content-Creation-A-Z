import re, subprocess, os, time, sys
md = open("research/assets.md", encoding="utf-8").read()
WANT = "A1 A2 A4 A5 A7 A8 A9 A10 B1 B2 B6 B9 B11 B13 C1 C2 C3 C5 C8 D1 D3 D4 D6 D8 D11 D13 D14 E4 E6 E8 E11 E12 P1 P3 P5 P6 P9 P11 P13 P14".split()
rows = {}
for line in md.splitlines():
    m = re.match(r"\|\s*\**([A-Z]\d+)\s*★?\**\s*\|", line)
    if not m: continue
    urls = re.findall(r"https://(?:videos\.pexels\.com|cdn\.pixabay\.com|images\.pexels\.com|upload\.wikimedia\.org)/\S+?\.(?:mp4|jpeg|jpg|webm)", line)
    if urls: rows[m.group(1)] = (urls[0], line.split("|")[2].strip()[:40])
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
for rid in WANT:
    if rid not in rows: print("NO URL", rid); continue
    u, what = rows[rid]; ext = os.path.splitext(u)[1]
    name = rid + "_" + re.sub(r"[^a-z0-9]+", "_", what.lower())[:28].strip("_") + ext
    out = "media/" + name
    if os.path.exists(out) and os.path.getsize(out) > 50000: continue
    if "images.pexels.com" in u: u += "?auto=compress&cs=tinysrgb&w=3840"
    subprocess.run(["curl", "-sL", "-A", UA, "-o", out, u])
    print(rid, os.path.getsize(out), name, flush=True)
    if "wikimedia" in u: time.sleep(2)
