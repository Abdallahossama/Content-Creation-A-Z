"""Extract the exact ElevenLabs text from script_ep04.md: no [ON SCREEN], no CTA blocks, no headings,
wrapped lines joined so the voice never pauses mid-sentence; one paragraph per beat.
Usage: vo_text.py [out_full.txt]  -> also writes vo_ep04_part1..N.txt (each <= 2,500 chars, split at paragraphs)."""
import re, sys
ROOT = "D:/why habibi/4th video/"
s = open(ROOT + "script_ep04.md", encoding="utf-8").read()
body = s.split("\n---\n")[1]
body = re.sub(r"`\[ON SCREEN:.*?\]`", "", body, flags=re.S)
body = re.sub(r"## \[CTA[^\n]*\n\*.*?\*\n", "", body, flags=re.S)
body = body.replace("`(R)`", "")
paras = []
for block in re.split(r"\n\s*\n", body):
    lines = [l.strip() for l in block.splitlines() if l.strip() and not l.strip().startswith("#")]
    if lines: paras.append(" ".join(lines))
paras = [re.sub(r"\s+", " ", p).strip() for p in paras]
txt = "\n\n".join(paras)
print(f"{len(txt)} chars, {len(txt.split())} words, {len(paras)} paragraphs")
if len(sys.argv) > 1:
    open(sys.argv[1], "w", encoding="utf-8").write(txt)
    # split into parts <= 2,500 chars, as even as possible, at paragraph boundaries
    n = -(-len(txt) // 2400); target = len(txt) / n; parts, cur = [], []
    for p in paras:
        if cur and len("\n\n".join(cur + [p])) > 2500 or (cur and len("\n\n".join(cur)) >= target and len(parts) < n - 1):
            parts.append(cur); cur = []
        cur.append(p)
    parts.append(cur)
    for i, ps in enumerate(parts, 1):
        t = "\n\n".join(ps); open(f"{ROOT}vo_ep04_part{i}.txt", "w", encoding="utf-8").write(t)
        print(f"part{i}: {len(t)} chars | starts: {ps[0][:60]!r}")
