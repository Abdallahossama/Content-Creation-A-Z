"""Re-score whisper lines with numbers spelled out (24 -> twenty four), list the ones that really differ."""
import re, difflib, sys
from num2words import num2words
RAW = [l.strip() for l in open("vo_tts.txt", encoding="utf-8") if l.strip()]
LINES = [l for l in RAW if l != "##"]
def yearish(n):
    n = int(n)
    if 1100 <= n <= 1999: return num2words(n // 100) + " " + (num2words(n % 100) if n % 100 else "hundred")
    if 2010 <= n <= 2099: return "twenty " + num2words(n % 100)
    return num2words(n)
def norm(s):
    s = s.lower().replace("£", "").replace("'", "").replace("-", " ").replace(",000", " thousand")
    s = re.sub(r"(\d+)(st|nd|rd|th)\b", lambda m: num2words(int(m.group(1)), to="ordinal"), s)
    s = re.sub(r"\d+", lambda m: " " + yearish(m.group(0)) + " ", s)
    s = s.replace("-", " ").replace(",", " ")
    return [w for w in re.sub(r"[^a-z ]", " ", s).split() if w not in ("and", "the", "a", "of")]
out = []
for l in open("transcribe.log", encoding="utf-8", errors="ignore"):
    m = re.match(r"^\s*(\d+) ([\d.]+) (.*)$", l.rstrip("\n"))
    if not m: continue
    i, hyp = int(m.group(1)), m.group(3)
    r = difflib.SequenceMatcher(a=norm(LINES[i]), b=norm(hyp)).ratio()
    if r < float(sys.argv[1] if len(sys.argv) > 1 else 0.97): out.append((r, i, LINES[i], hyp))
for r, i, a, b in sorted(out):
    sm = difflib.SequenceMatcher(a=norm(a), b=norm(b)); diffs = [(" ".join(norm(a)[x1:x2]), " ".join(norm(b)[y1:y2])) for tag, x1, x2, y1, y2 in sm.get_opcodes() if tag != "equal"]
    print(f"{i:3d} {r:.2f}  {diffs}")
