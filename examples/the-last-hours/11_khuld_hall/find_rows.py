"""print the page + row indices where each phrase sits in the cable/FRUS line boxes (build/ocr/A*p*.json)
  uv run --no-project python find_rows.py "phrase one" "phrase two" ..."""
import glob, json, os, re, sys
def n(s): return re.sub(r"[^a-z0-9]", "", s.lower())
pages = {os.path.basename(f)[:-5]: json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob("D:/why habibi/_newchannel/11_khuld_hall/build/ocr/A*p*.json"))}
for q in sys.argv[1:]:
    hits = []
    for rid, rows in pages.items():
        flat = ""; idx = []
        for i, r in enumerate(rows): t = n(r["text"]); flat += t; idx += [i] * len(t)
        k = flat.find(n(q))
        if k >= 0: hits.append(f"{rid}:{idx[k]}-{idx[k + len(n(q)) - 1]}")
    print(f"{q[:50]:50} -> {', '.join(hits) or 'NOT FOUND'}")
