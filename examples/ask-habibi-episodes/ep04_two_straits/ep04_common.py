"""Ep 4 (documentary) shared timeline: aligned words (script spelling, Whisper timing) + documentary pauses.
There are no Ep 1 CTA inserts here. Instead the voice is split at PAUSES and silence (music only) is inserted, so the
title card, the chapter cards and the big map reveals can breathe. `T(src)` turns VO seconds into timeline seconds."""
import json, re, difflib, sys
sys.path.insert(0, "D:/why habibi/_style_kit/tools")

EP = "D:/why habibi/4th video/"
BUILD = EP + "build/"
MEDIA = EP + "media/"
RC = EP + "receipts/"
VO = EP + "vo/ep04_VO_leveled_-16LUFS.wav"          # old processed voice (limited -> "whoosh"), kept only for reference
FPS = 30
VO_LEN = 303.82

# THE voice (user, 2026-10-13): the two ElevenLabs MP3s exactly as delivered, from this folder. VO time = part 1, then
# 0.7 s of silence, then part 2 (the layout every timing in this episode was measured on).
UNTOUCHED = EP + "export/ElevenLabs_original_untouched/"
VO_PARTS = [UNTOUCHED + "ep04_vo_part1.mp3", UNTOUCHED + "ep04_vo_part2.mp3"]
JOIN_GAP = 0.7
def vo_untouched(sr=48000):
    """the untouched voice on VO time (float32 mono) and the length of part 1 in seconds"""
    import subprocess, numpy as np
    dec = lambda p: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
                                                 capture_output=True).stdout, np.float32)
    p1, p2 = dec(VO_PARTS[0]), dec(VO_PARTS[1])
    return np.concatenate([p1, np.zeros(int(round(JOIN_GAP * sr)), np.float32), p2]), len(p1) / sr

_norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("\u2019", "'"))

def _align():
    script = open(EP + "vo_ep04_tts.txt", encoding="utf-8").read().split()
    words = [x for s in json.load(open(BUILD + "vo_words.json", encoding="utf-8")) for x in s["words"]]
    A, B = [_norm(w) for w in script], [_norm(w["w"]) for w in words]
    out = []
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(a=A, b=B, autojunk=False).get_opcodes():
        if op == "equal":
            out += [{"w": script[a0 + i], "s": words[b0 + i]["s"], "e": words[b0 + i]["e"]} for i in range(a1 - a0)]
        elif op == "replace":
            heard = [w["w"].strip() for w in words[b0:b1]]
            numeric = all(re.search(r"\d", h) or h in (",000", "%") for h in heard)
            if numeric:            # keep Whisper's digits for captions ("$1.27", "20%")
                txt = " ".join(heard).replace(" ,000", ",000").replace(" %", "%").replace(" .", ".")
                parts = txt.split()
                for k, piece in enumerate(parts):
                    w = words[min(b0 + k, b1 - 1)]
                    out.append({"w": piece, "s": w["s"], "e": words[b1 - 1]["e"] if k == len(parts) - 1 else w["e"]})
            else:                  # names / spellings: script spelling, times spread over the heard span
                s0, e0, n = words[b0]["s"], words[b1 - 1]["e"], a1 - a0
                for k in range(n):
                    out.append({"w": script[a0 + k], "s": s0 + (e0 - s0) * k / n, "e": s0 + (e0 - s0) * (k + 1) / n})
        elif op == "delete":
            t = out[-1]["e"] if out else 0.0
            out += [{"w": script[a0 + k], "s": t, "e": t + 0.05} for k in range(a1 - a0)]
    return out

TOK = _align()

def find(phrase, after=0.0):
    p = [_norm(x) for x in phrase.split()]; ws = [_norm(t["w"]) for t in TOK]
    for i in range(len(TOK) - len(p) + 1):
        if TOK[i]["s"] + 1e-6 >= after and ws[i:i + len(p)] == p: return TOK[i]["s"]
    raise KeyError(f"phrase not found after {after:.2f}s: {phrase!r}")

def find_end(phrase, after=0.0):
    p = [_norm(x) for x in phrase.split()]; ws = [_norm(t["w"]) for t in TOK]
    for i in range(len(TOK) - len(p) + 1):
        if TOK[i]["s"] + 1e-6 >= after and ws[i:i + len(p)] == p: return TOK[i + len(p) - 1]["e"]
    raise KeyError(phrase)

# documentary pauses: (phrase that starts after the pause, seconds of music-only space before it)
PAUSE_SPEC = [("This is Ask Habibi.", 1.5), ("Oil, it turns out", 3.6), ("In 2024, about", 1.0),
              ("On February 28th", 2.4), ("In September, Lloyd's", 1.3), ("Saudi Arabia had a plan", 2.4),
              ("This is Bab el-Mandeb.", 2.4), ("The Houthis say ships", 1.5), ("So, why do two tiny", 2.4),
              ("Here's what to watch next.", 1.4), ("If this helped you", 1.4)]
PAUSES = []                                    # (VO-source cut point, seconds)
for ph, sec in PAUSE_SPEC:
    s = find(ph)
    prev = max([t["e"] for t in TOK if t["e"] <= s + 1e-6] or [0.0])
    PAUSES.append(((prev + s) / 2, sec))
PAUSES.sort()

def T(src):
    """VO-source seconds -> final timeline seconds"""
    return src + sum(sec for cut, sec in PAUSES if src >= cut)

LEAD = 0.0
T_VO_END = T(VO_LEN)
END_SCREEN_LEN = 20.0
T_END_SCREEN = T_VO_END + 0.6
T_END = T_END_SCREEN + END_SCREEN_LEN

def timeline_tokens():
    return sorted([(t["w"], T(t["s"]), T(t["e"]), "vo") for t in TOK], key=lambda r: r[1])

if __name__ == "__main__":
    print(f"VO {VO_LEN:.2f}s + pauses {sum(s for _, s in PAUSES):.1f}s -> VO ends {T_VO_END:.2f}, end screen {T_END_SCREEN:.2f}-{T_END:.2f} ({T_END / 60:.2f} min)")
    print(len(TOK), "aligned words;", " ".join(t["w"] for t in TOK[:24]))
    print([t["w"] for t in TOK if re.search(r"\d", t["w"])])
