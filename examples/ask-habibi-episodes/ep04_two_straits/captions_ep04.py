"""Ep 4 captions (copied from Ep 3): 1-3 word chunks (Ep 1 rules), lowercase, Rubik Bold white + black outline, one keyword per chunk in
brand yellow. Chunks already on screen as big words are skipped. -> build/captions_ep04.ass (burned into the final
render) + captions_ep04.srt (CapCut import) + captions_ep04.json (for the CapCut text track)."""
import re, json
from ep04_common import *
from beats_ep04 import BEATS
from ep04_fx import Big

KEEP_CAPS = {"iran": "Iran", "oman": "Oman", "arabia": "Arabia", "hormuz": "Hormuz", "gulf": "Gulf", "iraq": "Iraq", "kuwait": "Kuwait", "saudi": "Saudi", "qatar": "Qatar", "emirates": "Emirates", "asia": "Asia", "uae": "UAE", "united": "United", "states": "States", "israel": "Israel", "february": "February", "april": "April", "october": "October", "september": "September", "march": "March", "november": "November", "lloyd's": "Lloyd's", "list": "List", "yanbu": "Yanbu", "red": "Red", "sea": "Sea", "bab": "Bab", "el-mandeb": "el-Mandeb", "houthis": "Houthis", "yemeni": "Yemeni", "africa": "Africa", "mayun": "Mayun", "perim": "Perim", "hanish": "Hanish", "al": "Al", "jazeera": "Jazeera", "riyadh's": "Riyadh's", "riyadh": "Riyadh", "american": "American", "us": "US", "america": "America", "csis": "CSIS", "europe": "Europe", "habibi": "Habibi", "yemen": "Yemen", "arabian": "Arabian", "iranian": "Iranian", "saudi-backed": "Saudi-backed", "strait": "Strait", "i": "I", "ask": "ask"}
KEY = {"gas", "strip", "island", "war", "serious", "door", "chokepoint", "hormuz", "fifth", "qatar", "asia", "pipelines", "blocked",
       "blockade", "ceasefire", "open", "tankers", "struck", "stopped", "transponders", "shuttle", "sustainable", "plan", "yanbu", "seven",
       "drone", "street", "bab", "el-mandeb", "lanes", "houthis", "africa", "mayun", "perim", "withdrew", "hanish", "safe", "saudi",
       "capability", "riyadh's", "airport", "killed", "counteroffensive", "join", "doors", "price", "worldwide", "heating", "electricity",
       "watch", "mayun", "change", "subscribe", "question"}
FUNC = {"a", "an", "the", "to", "of", "your", "at", "in", "and", "for", "with", "is", "that", "my", "i", "on", "as", "it"}
SKIP = {"level one", "level two", "level three", "level four"}
norm = lambda s: re.sub(r"[^a-z0-9'\-]", "", s.lower())

def disp(w):
    core = w.strip("\"“”") if w.lower().rstrip(",") == "a.m." else re.sub(r"[.,;:!\"“”]+$", "", w).strip("\"“”")
    q = "?" if core.endswith("?") else ""
    core = core.rstrip("?")
    low = core.lower()
    return KEEP_CAPS.get(low, low) + q

toks = [{"w": w, "s": s, "e": e} for w, s, e, _ in timeline_tokens() if w.strip()]
chunks, cur = [], []
for tk in toks:
    if cur:
        prev = cur[-1]; txt_len = len(" ".join(disp(x["w"]) for x in cur + [tk]))
        hard = re.search(r"[.,?!:]\"?$", prev["w"]) and not prev["w"].lower().endswith("a.m.") or tk["s"] - prev["e"] > 0.35
        soft = len(cur) >= 3 or txt_len > 18
        if hard or soft:
            carry = [cur.pop()] if soft and not hard and len(cur) >= 2 and norm(cur[-1]["w"]) in FUNC else []
            chunks.append(cur); cur = carry
    cur.append(tk)
if cur: chunks.append(cur)

def on_screen_big(t0, t1, words):
    for b in BEATS:
        if b.t1 <= t0 or b.t0 >= t1: continue
        for o in b.ovs:
            if isinstance(o, Big) and getattr(o, "text", None) and o.t_in <= t1 + 0.1:
                bw = {norm(x) for x in o.text.split()}
                if words and words <= bw: return True
    return False

caps = []
for i, c in enumerate(chunks):
    words = [disp(x["w"]) for x in c]
    txt = " ".join(words)
    s = c[0]["s"]; e = c[-1]["e"] + 0.25
    if i + 1 < len(chunks): e = min(e if chunks[i + 1][0]["s"] - c[-1]["e"] >= 0.6 else chunks[i + 1][0]["s"], chunks[i + 1][0]["s"])
    if e - s < 0.2: e = s + 0.2
    wset = {norm(w) for w in words}
    if txt.lower() in SKIP or on_screen_big(s, e, wset): continue
    k = next((j for j, w in enumerate(words) if re.search(r"\d", w)), None)
    if k is None: k = next((j for j, w in enumerate(words) if norm(w) in KEY), None)
    caps.append({"t0": s, "t1": e, "words": words, "key": k})

def ts_ass(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h}:{m:02d}:{s:05.2f}"
def ts_srt(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
       "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Cap,Rubik,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,1.5,0,1,5.5,0,2,80,80,108,1", "",
       "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
srt = []
for n, c in enumerate(caps, 1):
    parts = [("{\\c&H1AC2FF&}" + w + "{\\c&HFFFFFF&}") if j == c["key"] else w for j, w in enumerate(c["words"])]
    ass.append(f"Dialogue: 0,{ts_ass(c['t0'])},{ts_ass(c['t1'])},Cap,,0,0,0,,{' '.join(parts)}")
    srt += [str(n), f"{ts_srt(c['t0'])} --> {ts_srt(c['t1'])}", " ".join(c["words"]), ""]
open(BUILD + "captions_ep04.ass", "w", encoding="utf-8").write("\n".join(ass) + "\n")
open(BUILD + "captions_ep04.srt", "w", encoding="utf-8").write("\n".join(srt))
json.dump(caps, open(BUILD + "captions_ep04.json", "w", encoding="utf-8"), indent=0)
print(len(caps), "captions,", sum(c["key"] is not None for c in caps), "with a yellow keyword")
for c in caps[:12] + caps[60:66] + caps[-6:]:
    print(f"  {c['t0']:7.2f}-{c['t1']:7.2f}  " + " ".join(f"[{w}]" if j == c["key"] else w for j, w in enumerate(c["words"])))
