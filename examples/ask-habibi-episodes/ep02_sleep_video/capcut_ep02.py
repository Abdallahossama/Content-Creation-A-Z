"""Ep 2 CapCut timeline (built from the clean Ep 1 FINAL draft as the template, so no Pro/AI history):
track 1 = the 70 rendered beat clips · captions (Rubik, white, black stroke, keyword yellow, y -0.73) ·
VO timeline · music bed · SFX stem.  -> build/new_draft_content_ep02.json  (then create_project_ep02.py)"""
import json, copy, uuid, os, subprocess
from ep02_common import *
from beats_ep02 import BEATS

TPL = "D:/why habibi/_pipeline/episodes/ep01_overthinking/new_draft_content.json"
OUT = BUILD + "new_draft_content_ep02.json"
FR = lambda t: int(round(t * FPS))
def F(sec): return FR(sec) * 1000000 // FPS
def uid(): return str(uuid.uuid4()).upper()

d = json.load(open(TPL, encoding="utf-8")); M = d["materials"]
IDX = {m["id"]: (k, m) for k, v in M.items() if isinstance(v, list) for m in v if isinstance(m, dict) and "id" in m}
tr = d["tracks"]
vtracks = [t for t in tr if t["type"] == "video"]; ttracks = [t for t in tr if t["type"] == "text"]; atracks = [t for t in tr if t["type"] == "audio"]
T_VIDEO = copy.deepcopy(next(s for t in vtracks for s in t["segments"] if IDX[s["material_id"]][1].get("type") == "video"))
T_TEXT = copy.deepcopy(ttracks[-1]["segments"][0]); T_AUDIO = copy.deepcopy(atracks[0]["segments"][0])
M_VIDEO = copy.deepcopy(IDX[T_VIDEO["material_id"]][1]); M_TEXT = copy.deepcopy(IDX[T_TEXT["material_id"]][1])
M_AUDIO = copy.deepcopy(IDX[T_AUDIO["material_id"]][1])

def clone_refs(seg):
    new = []
    for r in seg["extra_material_refs"]:
        if r not in IDX: continue
        k, m = IDX[r]
        if k == "time_marks": continue
        m2 = copy.deepcopy(m); m2["id"] = uid()
        if k == "material_animations": m2["animations"] = []
        M[k].append(m2); IDX[m2["id"]] = (k, m2); new.append(m2["id"])
    seg["extra_material_refs"] = new

def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,codec_type:format=duration", "-of", "json", p],
                                  capture_output=True, text=True).stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    return v.get("width", 0), v.get("height", 0), float(j["format"]["duration"]), any(s["codec_type"] == "audio" for s in j["streams"])

def vseg(path, t0, t1):
    w, h, dur, aud = probe(path)
    m = copy.deepcopy(M_VIDEO); m.update(id=uid(), path=path, width=w, height=h, material_name=os.path.basename(path), type="video",
                                         duration=int(dur * 1e6), has_audio=aud)
    M["videos"].append(m); IDX[m["id"]] = ("videos", m)
    s = copy.deepcopy(T_VIDEO); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    st, en = F(t0), F(t1)
    s["target_timerange"] = {"start": st, "duration": en - st}; s["source_timerange"] = {"start": 0, "duration": en - st}
    s["clip"] = {"scale": {"x": 1.0, "y": 1.0}, "rotation": 0.0, "transform": {"x": 0.0, "y": 0.0},
                 "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0}
    s["uniform_scale"] = {"on": True, "value": 1.0}; s["volume"] = 0.0; s["common_keyframes"] = []; s["keyframe_refs"] = []
    return s

def aseg(path, t0, vol=1.0):
    _, _, dur, _ = probe(path)
    m = copy.deepcopy(M_AUDIO); m.update(id=uid(), path=path, name=os.path.basename(path), duration=int(dur * 1e6), type="extract_music",
                                         category_name="local")
    M["audios"].append(m); IDX[m["id"]] = ("audios", m)
    s = copy.deepcopy(T_AUDIO); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    du = int(dur * 1e6); s["target_timerange"] = {"start": F(t0), "duration": du}; s["source_timerange"] = {"start": 0, "duration": du}
    s["volume"] = vol; return s

YEL = [1.0, 194 / 255, 26 / 255]
def tseg(t0, t1, words, key):
    txt = " ".join(words)
    m = copy.deepcopy(M_TEXT); m["id"] = uid()
    for field in ("content", "base_content"):
        if not m.get(field): continue
        c = json.loads(m[field]); c["text"] = txt; base = c["styles"][0]; styles = []
        pos = 0; spans = []
        for j, w in enumerate(words):
            spans.append((pos, pos + len(w), j == key)); pos += len(w) + (1 if j < len(words) - 1 else 0)
        runs, cur = [], None                              # merge into white / yellow ranges covering the whole string
        for j, (a, b, k) in enumerate(spans):
            a2, b2 = a, (spans[j + 1][0] if j + 1 < len(spans) else len(txt))
            if cur and cur[2] == k: cur[1] = b2
            else:
                cur = [a2, b2, k]; runs.append(cur)
        for a, b, k in runs:
            st = copy.deepcopy(base); st["range"] = [a, b]
            st["fill"]["content"]["solid"]["color"] = YEL if k else [1.0, 1.0, 1.0]
            st["strokes"] = [{"content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}}, "width": 0.08}]
            styles.append(st)
        c["styles"] = styles; m[field] = json.dumps(c, ensure_ascii=False, separators=(",", ":"))
    m["recognize_text"] = txt; m["border_color"] = "#000000"; m["border_width"] = 0.08; m["border_alpha"] = 1.0
    m["words"] = {"start_time": [], "end_time": [], "text": []}
    M["texts"].append(m); IDX[m["id"]] = ("texts", m)
    s = copy.deepcopy(T_TEXT); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    st, en = F(t0), F(t1); s["target_timerange"] = {"start": st, "duration": max(en - st, 100000)}
    s["source_timerange"] = {"start": 0, "duration": s["target_timerange"]["duration"]}
    return s

# ---------------------------------------------------------------- tracks
beats_dir = BUILD + "beats/"
files = sorted(f for f in os.listdir(beats_dir) if f.endswith(".mp4") and not f.endswith(".tmp.mp4"))
assert len(files) == len(BEATS), f"{len(files)} rendered clips for {len(BEATS)} beats - render first"
video = [vseg(beats_dir + f, b.t0, b.t1) for f, b in zip(files, BEATS)]
caps = json.load(open(BUILD + "captions_ep02.json", encoding="utf-8"))
texts = []
for c in caps:
    s = tseg(c["t0"], c["t1"], c["words"], c["key"])
    if texts:
        pe = texts[-1]["target_timerange"]["start"] + texts[-1]["target_timerange"]["duration"]
        if s["target_timerange"]["start"] < pe:
            texts[-1]["target_timerange"]["duration"] = s["target_timerange"]["start"] - texts[-1]["target_timerange"]["start"]
            texts[-1]["source_timerange"]["duration"] = texts[-1]["target_timerange"]["duration"]
    texts.append(s)
def track(kind, segs): return {"id": uid(), "type": kind, "flag": 0, "attribute": 0, "name": "", "is_default_name": True, "segments": segs}
d["tracks"] = [track("video", video), track("text", texts), track("audio", [aseg(BUILD + "vo_timeline.wav", 0.0)]),
               track("audio", [aseg(BUILD + "music_bed_ep02.wav", 0.0)]), track("audio", [aseg(BUILD + "sfx_ep02.wav", 0.0)])]
for i, t in enumerate(d["tracks"]):
    for k, s in enumerate(t["segments"]):
        s["track_render_index"] = i; s["render_index"] = (14001 + k) if t["type"] == "text" else i

# ---------------------------------------------------------------- clean: drop every unused material, Pro flags off
used = {s["material_id"] for t in d["tracks"] for s in t["segments"]} | {r for t in d["tracks"] for s in t["segments"] for r in s["extra_material_refs"]}
for k, v in M.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
        M[k] = [m for m in v if m["id"] in used]
for m in M.get("loudnesses", []): m["enable"] = False
for m in M["texts"]:
    m["type"] = "text"; m["recognize_task_id"] = ""; m["recognize_model"] = ""; m["add_type"] = 0; m["recognize_type"] = 0
d["config"]["subtitle_taskinfo"] = []; d["config"]["subtitle_recognition_id"] = ""
d["duration"] = F(T_END)
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("wrote", OUT, "| video", len(video), "| captions", len(texts), "| duration", round(d["duration"] / 1e6, 2), "s")
print({k: len(v) for k, v in M.items() if isinstance(v, list) and v})
