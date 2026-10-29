"""Fix whisper mishears in a vo_words.json, phrase by phrase (multi-token aware, timings merged).
  python fix_words.py <vo_words.json> "Hollifell's=>Hohle Fels" "Geisen Klästerle=>Geissenklösterle" ...
Punctuation stuck to the last old token is kept on the last new token."""
import json, sys

def norm(s): return s.strip(" ,.?!:;\"'").lower()

def fix(path, pairs):
    S = json.load(open(path, encoding="utf-8")); n = 0
    for old, new in pairs:
        ow, nw = old.split(), new.split()
        for s in S:
            W = s["words"]; i = 0
            while i <= len(W) - len(ow):
                if all(norm(W[i + k]["w"]) == norm(ow[k]) for k in range(len(ow))):
                    lead = W[i]["w"][: len(W[i]["w"]) - len(W[i]["w"].lstrip())] or " "
                    last = W[i + len(ow) - 1]["w"].rstrip(); tail = last[len(last.rstrip(",.?!:;")):]
                    t0, t1 = W[i]["s"], W[i + len(ow) - 1]["e"]; step = (t1 - t0) / len(nw)
                    W[i:i + len(ow)] = [{"w": lead + w + (tail if k == len(nw) - 1 else ""), "s": t0 + k * step, "e": t0 + (k + 1) * step, "p": 1.0} for k, w in enumerate(nw)]
                    n += 1; i += len(nw)
                else: i += 1
            s["text"] = "".join(w["w"] for w in W)
    json.dump(S, open(path, "w", encoding="utf-8"), indent=1); return n

if __name__ == "__main__":
    pairs = [a.split("=>") for a in sys.argv[2:]]
    print("fixed", fix(sys.argv[1], pairs))
