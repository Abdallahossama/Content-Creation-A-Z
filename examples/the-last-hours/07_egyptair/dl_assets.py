"""Download the approved EgyptAir 990 visuals (assets.md sections A-F + H1, H10-H12) into media/ (approved by the owner 22 Oct 2026:
"go ahead" on main list + H1 + H10-H12). Image URLs are fetched as they are; rows whose URL is a PDF (NTSB brief, docket) are
fetched once into build/_pdf/ and the named page ("PDF p. N") is rendered at 200 dpi. Bad files are moved to the archive, never deleted.
  uv run --no-project --with pymupdf python dl_assets.py"""
import re, time, os, subprocess, hashlib
ROOT = "D:/why habibi/_newchannel/07_egyptair/"
BAD = "D:/why habibi/_archive/egyptair_bad_downloads/"
PDFD = ROOT + "build/_pdf/"
OK_H = {"H1", "H10", "H11", "H12"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 TheLastHours-research"

def is_img(p):
    if not os.path.exists(p) or os.path.getsize(p) < 8000: return False
    h = open(p, "rb").read(8)
    return h[:3] == b"\xff\xd8\xff" or h[:8] == b"\x89PNG\r\n\x1a\n" or h[:4] in (b"II*\x00", b"MM\x00*")
def fetch(url, out, tries=5):
    code = "?"
    for attempt in range(tries):
        r = subprocess.run(["curl", "-sL", "--max-time", "300", "-A", UA, "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200" and os.path.exists(out) and os.path.getsize(out) > 8000: return code
        print("retry", code, url[:80], flush=True); time.sleep(15 * (attempt + 1))
    return code

rows, sec = [], None
for l in open(ROOT + "research/assets.md", encoding="utf-8"):
    m = re.match(r"^## ([A-Z])\. ", l)
    if m: sec = m.group(1)
    m = re.match(r"^\| ([A-H]\d+) \|", l)
    if not (m and sec): continue
    rid = m.group(1)
    if not (sec in "ABCDEF" or rid in OK_H): continue
    c = [x.strip() for x in l.strip().strip("|").split(" | ")]
    pg = re.findall(r"PDF p(?:age)?\.? ?(\d+)", c[1]) or re.findall(r"[Pp]age (\d+)", c[1])
    rows.append((rid, re.sub(r"\*\*[^*]+\*\*\s*", "", c[1]) if rid.startswith("H") else c[1], c[3], int(pg[0]) if pg else 1))

os.makedirs(ROOT + "media", exist_ok=True); os.makedirs(PDFD, exist_ok=True)
for rid, what, url, page in rows:
    slug = re.sub(r"[^a-z0-9]+", "_", re.sub(r"\*\*|^(SATELLITE[^:]*|Pexels \d+)[:.]?\s*", "", what).lower())[:38].strip("_")
    is_pdf = (".pdf" in url.lower() or "FileExtension=pdf" in url) and "/thumb/" not in url
    out = f"{ROOT}media/{rid}_{slug}.png" if is_pdf else f"{ROOT}media/{rid}_{slug}.jpg"
    if is_img(out): print("have", rid, flush=True); continue
    if os.path.exists(out):
        os.makedirs(BAD, exist_ok=True); os.replace(out, BAD + os.path.basename(out) + f".{int(time.time())}.bad")
    if is_pdf:
        pdf = PDFD + hashlib.md5(url.encode()).hexdigest()[:12] + ".pdf"
        if not (os.path.exists(pdf) and open(pdf, "rb").read(4) == b"%PDF"):
            code = fetch(url, pdf)
            if open(pdf, "rb").read(4) != b"%PDF": print(f"{rid:4} {code} BAD (not a PDF)", flush=True); continue
        import fitz
        doc = fitz.open(pdf); p = doc[min(page, doc.page_count) - 1]
        p.get_pixmap(dpi=200).save(out); doc.close()
        print(f"{rid:4} PDF p.{page} {'OK ' if is_img(out) else 'BAD'} {os.path.getsize(out) / 1e6:6.2f} MB  {os.path.basename(out)}", flush=True)
        time.sleep(2)
    else:
        code = fetch(url, out)
        print(f"{rid:4} {code} {'OK ' if is_img(out) else 'BAD'} {os.path.getsize(out) / 1e6 if os.path.exists(out) else 0:6.2f} MB  {os.path.basename(out)}", flush=True)
        time.sleep(8 if "wikimedia" in url else 2)
print("rows", len(rows))
