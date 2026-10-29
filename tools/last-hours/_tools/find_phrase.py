import json, sys
S = json.load(open(sys.argv[1], encoding="utf-8")); W = [w for s in S for w in s["words"]]
norm = lambda s: s.strip(" ,.?!:;\"'").lower()
for ph in sys.argv[2:]:
    p = ph.lower().split(); n = len(p)
    for i in range(len(W) - n + 1):
        if all(norm(W[i + k]["w"]) == p[k] for k in range(n)):
            print(f"{ph!r}: {W[i]['s']:.2f} (prev ends {W[i-1]['e']:.2f} '{W[i-1]['w'].strip()}')")
