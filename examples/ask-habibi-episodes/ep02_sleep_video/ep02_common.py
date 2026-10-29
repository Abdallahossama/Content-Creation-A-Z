"""Ep 2 shared timeline: aligned words, the CTA inserts, phrase lookup. Imported by every Ep 2 build script.

Timeline =  cold open (Ep 2 VO) · CTA intro (Ep 1 VO) · rest of Ep 2 VO · CTA outro (Ep 1 VO) · end screen.
Times called `src` are Ep 2 voiceover seconds; `T(src)` turns them into final-timeline seconds."""
import json, re, difflib, sys
sys.path.insert(0, "D:/why habibi/_style_kit/tools")

EP = "D:/why habibi/2nd video/"
BUILD = EP + "build/"
MEDIA = EP + "media/"
RC = EP + "receipts/"
VO2 = EP + "vo/ep02_VO_leveled_-15LUFS.wav"
VO1 = "D:/why habibi/1st video/ElevenLabs_VO_leveled_-15LUFS.wav"
EP1_WORDS = "D:/why habibi/_pipeline/episodes/ep01_overthinking/vo_words.json"
FPS = 30
VO2_LEN = 406.68

# ---------------------------------------------------------------- aligned words (script spelling, whisper timing)
_norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'"))
NUMWORDS = {"one": "1", "four": "4", "forty-one": "41", "forty-eight": "48", "thirteen": "13", "sixteen.": "16.",
            "thirty-eight": "38", "ten": "10"}

def _align():
    script = open(EP + "vo_ep02_tts.txt", encoding="utf-8").read().split()
    words = [x for s in json.load(open(BUILD + "vo_words.json", encoding="utf-8")) for x in s["words"]]
    A, B = [_norm(w) for w in script], [_norm(w["w"]) for w in words]
    out = []
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(a=A, b=B, autojunk=False).get_opcodes():
        if op == "equal":
            out += [{"w": script[a0 + i], "s": words[b0 + i]["s"], "e": words[b0 + i]["e"]} for i in range(a1 - a0)]
        elif op == "replace":
            heard = [w["w"].strip() for w in words[b0:b1]]
            numeric = all(re.search(r"\d", h) or h in (",000",) for h in heard)
            if numeric:            # keep whisper's digits for captions ("41", "48"), fix the odd split "10 ,000"
                txt = " ".join(heard).replace(" ,000", ",000").replace("3am", "3 a.m.")
                for k, piece in enumerate(txt.split()):
                    w = words[min(b0 + k, b1 - 1)]
                    out.append({"w": piece, "s": w["s"], "e": words[b1 - 1]["e"] if k == len(txt.split()) - 1 else w["e"]})
            else:                  # names / apostrophes: script spelling, times spread over the heard span
                s0, e0, n = words[b0]["s"], words[b1 - 1]["e"], a1 - a0
                for k in range(n):
                    out.append({"w": script[a0 + k], "s": s0 + (e0 - s0) * k / n, "e": s0 + (e0 - s0) * (k + 1) / n})
        elif op == "delete":       # script words the ASR missed: squeeze them next to the previous word
            t = out[-1]["e"] if out else 0.0
            out += [{"w": script[a0 + k], "s": t, "e": t + 0.05} for k in range(a1 - a0)]
    return out

TOK = _align()

def find(phrase, after=0.0):
    """VO-source start time of the first occurrence of `phrase` starting at/after `after`."""
    p = [_norm(x) for x in phrase.split()]
    ws = [_norm(t["w"]) for t in TOK]
    for i in range(len(TOK) - len(p) + 1):
        if TOK[i]["s"] + 1e-6 >= after and ws[i:i + len(p)] == p:
            return TOK[i]["s"]
    raise KeyError(f"phrase not found after {after:.2f}s: {phrase!r}")

def find_end(phrase, after=0.0):
    p = [_norm(x) for x in phrase.split()]
    ws = [_norm(t["w"]) for t in TOK]
    for i in range(len(TOK) - len(p) + 1):
        if TOK[i]["s"] + 1e-6 >= after and ws[i:i + len(p)] == p:
            return TOK[i + len(p) - 1]["e"]
    raise KeyError(phrase)

# ---------------------------------------------------------------- the CTA inserts
CTA_IN = (17.90, 33.60)          # Ep 1 VO: "The food is hot… won't have to search next time."
CTA_OUT = (175.15, 186.83)       # Ep 1 VO: "That's the answer… before your food gets cold."
S_CUT = find_end("You won't love it.") + 0.30         # Ep 2 cold open ends here
GAP = 0.35
T_CTA_IN = S_CUT + GAP
O1 = T_CTA_IN + (CTA_IN[1] - CTA_IN[0]) + GAP - S_CUT  # offset added to Ep 2 VO after the cut
T_VO_END = VO2_LEN + O1
T_CTA_OUT = T_VO_END + 0.5
T_END_SCREEN = T_CTA_OUT + (CTA_OUT[1] - CTA_OUT[0]) + 0.4
END_SCREEN_LEN = 18.0
T_END = T_END_SCREEN + END_SCREEN_LEN

def T(src):
    """Ep 2 VO-source seconds -> final timeline seconds."""
    return src if src <= S_CUT else src + O1

def ep1_words(span):
    w = [x for s in json.load(open(EP1_WORDS, encoding="utf-8")) for x in s["words"]]
    return [{"w": x["w"].strip(), "s": x["s"], "e": x["e"]} for x in w if span[0] <= x["s"] < span[1]]

def timeline_tokens():
    """every spoken word on the final timeline (for captions): (word, t0, t1, source)"""
    out = [(t["w"], T(t["s"]), T(t["e"]), "ep2") for t in TOK]
    for span, t0 in ((CTA_IN, T_CTA_IN), (CTA_OUT, T_CTA_OUT)):
        out += [(x["w"], t0 + x["s"] - span[0], t0 + x["e"] - span[0], "cta") for x in ep1_words(span)]
    return sorted(out, key=lambda r: r[1])

if __name__ == "__main__":
    print(f"S_CUT {S_CUT:.2f}  CTA in at {T_CTA_IN:.2f}  O1 {O1:.2f}  VO ends {T_VO_END:.2f}  "
          f"CTA out {T_CTA_OUT:.2f}  end screen {T_END_SCREEN:.2f}-{T_END:.2f}  ({T_END / 60:.2f} min)")
    print(len(TOK), "aligned words;", " ".join(t["w"] for t in TOK[:30]))
    for ph in ["Here's the plan.", "Level two.", "Level three.", "Level four.", "So, what actually helps?"]:
        print(f"  {ph!r:30s} src {find(ph):7.2f}  timeline {T(find(ph)):7.2f}")
