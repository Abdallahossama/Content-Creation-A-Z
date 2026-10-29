"""Extract the exact ElevenLabs text from script_ep02.md: no [ON SCREEN], no CTA blocks, no headings,
wrapped lines joined so the voice never pauses mid-sentence; one paragraph per beat."""
import re, sys
s = open("D:/why habibi/2nd video/script_ep02.md", encoding="utf-8").read()
body = s.split("\n---\n")[1]
body = re.sub(r"`\[ON SCREEN:.*?\]`", "", body, flags=re.S)
body = re.sub(r"## \[CTA[^\n]*\n\*.*?\*\n", "", body, flags=re.S)
body = body.replace("`(R)`", "")
paras = []
for block in re.split(r"\n\s*\n", body):
    lines = [l.strip() for l in block.splitlines() if l.strip() and not l.strip().startswith("#")]
    if lines: paras.append(" ".join(lines))
txt = "\n\n".join(re.sub(r"\s+", " ", p).strip() for p in paras)
w = len(txt.split())
print(f"{len(txt)} chars, {w} words, {len(paras)} paragraphs")
if len(sys.argv) > 1: open(sys.argv[1], "w", encoding="utf-8").write(txt)
