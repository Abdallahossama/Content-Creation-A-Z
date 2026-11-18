"""1st video (A to Z) -> CapCut draft_content: face cuts (graded) / B-roll / brand PNG overlays / captions (editable text) /
voice / music / SFX stems. Template = the clean Ask Habibi Ep1 FINAL draft (no Pro/AI history). Output: capcut/draft_content_1st.json"""
import json, copy, uuid, os, subprocess
W = "D:/personal brand/07_workspace/1st_video/"
TPL = "D:/why habibi/_pipeline/episodes/ep01_overthinking/new_draft_content.json"
OUT = W + "capcut/draft_content_1st.json"
FONT = "D:/codebyabdullah_assets/workspace/edit/fonts/Alexandria-ExtraBold.ttf"
CW, CH = 1080, 1920
def uid(): return str(uuid.uuid4()).upper()
def us(t): return int(round(t * 1e6))

d = json.load(open(TPL, encoding="utf-8")); M = d["materials"]
IDX = {m["id"]: (k, m) for k, v in M.items() if isinstance(v, list) for m in v if isinstance(m, dict) and "id" in m}
vtr = [t for t in d["tracks"] if t["type"] == "video"]
T_VIDEO = copy.deepcopy(next(s for t in vtr for s in t["segments"] if IDX[s["material_id"]][1].get("type") == "video"))
T_PHOTO = copy.deepcopy(next(s for t in vtr for s in t["segments"] if IDX[s["material_id"]][1].get("type") == "photo"))
T_TEXT = copy.deepcopy(next(t for t in d["tracks"] if t["type"] == "text")["segments"][0])
T_AUDIO = copy.deepcopy(next(t for t in d["tracks"] if t["type"] == "audio")["segments"][0])
M_VIDEO, M_PHOTO = copy.deepcopy(IDX[T_VIDEO["material_id"]][1]), copy.deepcopy(IDX[T_PHOTO["material_id"]][1])
M_TEXT, M_AUDIO = copy.deepcopy(IDX[T_TEXT["material_id"]][1]), copy.deepcopy(IDX[T_AUDIO["material_id"]][1])

def clone_refs(seg):
    new = []
    for r in seg["extra_material_refs"]:
        if r not in IDX: continue
        k, m = IDX[r]
        if k in ("time_marks", "beats"): continue
        m2 = copy.deepcopy(m); m2["id"] = uid()
        if k == "material_animations": m2["animations"] = []
        M[k].append(m2); IDX[m2["id"]] = (k, m2); new.append(m2["id"])
    seg["extra_material_refs"] = new

def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,codec_type:format=duration", "-of", "json", p],
                                  capture_output=True, text=True).stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    return v.get("width", 0), v.get("height", 0), float(j["format"].get("duration", 0) or 0), any(s["codec_type"] == "audio" for s in j["streams"])

MAT = {}
def material(path, kind):
    if path in MAT: return MAT[path]
    w, h, dur, aud = probe(path)
    if kind == "photo":
        m = copy.deepcopy(M_PHOTO); m.update(id=uid(), path=path, width=w, height=h, material_name=os.path.basename(path), type="photo")
    else:
        m = copy.deepcopy(M_VIDEO); m.update(id=uid(), path=path, width=w, height=h, material_name=os.path.basename(path), type="video",
                                             duration=us(dur), has_audio=aud)
    M["videos"].append(m); IDX[m["id"]] = ("videos", m); MAT[path] = m; return m

def place(seg, x, y, w, h, dw):
    """top-left x,y + displayed width dw (px on the 1080x1920 canvas) -> CapCut clip (contain-fit base, centre-normalised)"""
    fit = min(CW / w, CH / h); sc = dw / (w * fit); dh = h * dw / w
    cx, cy = x + dw / 2, y + dh / 2
    seg["clip"] = {"scale": {"x": sc, "y": sc}, "rotation": 0.0, "transform": {"x": (cx - CW / 2) / (CW / 2), "y": (CH / 2 - cy) / (CH / 2)},
                   "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0}
    seg["uniform_scale"] = {"on": True, "value": 1.0}

def vseg(path, t0, dur, src0=0.0, kind="video", geo=None):
    m = material(path, kind)
    s = copy.deepcopy(T_PHOTO if kind == "photo" else T_VIDEO); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    s["target_timerange"] = {"start": us(t0), "duration": us(dur)}; s["source_timerange"] = {"start": us(src0), "duration": us(dur)}
    if geo: place(s, *geo)
    else: place(s, 0, 0, m["width"] or CW, m["height"] or CH, CW)
    s["volume"] = 0.0; s["common_keyframes"] = []; s["keyframe_refs"] = []
    return s

def aseg(path, t0=0.0, vol=1.0, name=None):
    _, _, dur, _ = probe(path)
    m = copy.deepcopy(M_AUDIO); m.update(id=uid(), path=path, name=name or os.path.basename(path), duration=us(dur), type="extract_music", category_name="local")
    M["audios"].append(m); IDX[m["id"]] = ("audios", m)
    s = copy.deepcopy(T_AUDIO); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    s["target_timerange"] = {"start": us(t0), "duration": us(dur)}; s["source_timerange"] = {"start": 0, "duration": us(dur)}; s["volume"] = vol
    return s

def tseg(t0, t1, txt):
    m = copy.deepcopy(M_TEXT); m["id"] = uid()
    for field in ("content", "base_content"):
        if not m.get(field): continue
        c = json.loads(m[field]); base = c["styles"][0]; st = copy.deepcopy(base)
        st["range"] = [0, len(txt)]; st["fill"]["content"]["solid"]["color"] = [1.0, 1.0, 1.0]; st["size"] = 9
        st["font"] = {"path": FONT, "id": ""}; st.pop("strokes", None)
        c["text"] = txt; c["styles"] = [st]; m[field] = json.dumps(c, ensure_ascii=False, separators=(",", ":"))
    m.update(recognize_text=txt, font_path=FONT, font_resource_id="", font_id="", fonts=[], font_title="Alexandria ExtraBold", font_size=9,
             border_width=0.0, border_color="", background_color="#121212", background_alpha=0.92, background_style=1,
             background_round_radius=0.18, background_width=0.16, background_height=0.18, alignment=1, has_shadow=False)
    m["words"] = {"start_time": [], "end_time": [], "text": []}
    M["texts"].append(m); IDX[m["id"]] = ("texts", m)
    s = copy.deepcopy(T_TEXT); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    s["target_timerange"] = {"start": us(t0), "duration": max(us(t1 - t0), 100000)}
    s["source_timerange"] = {"start": 0, "duration": s["target_timerange"]["duration"]}
    s["clip"] = {"scale": {"x": 1.0, "y": 1.0}, "rotation": 0.0, "transform": {"x": 0.0, "y": -0.54},
                 "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0}
    return s

# ---------------------------------------------------------------- build
E = json.load(open(W + "edl2_segs.json", encoding="utf-8")); MAN = json.load(open(W + "manifest2.json", encoding="utf-8"))
face, t, k = [], 0.0, 0
for c in E:
    for p, n in c["segs"]:
        dur = n / 30; face.append(vseg(W + f"seg2/s{k:03d}.mov", t, dur)); t += dur; k += 1
broll = [vseg(b["file"], b["a"], b["b"] - b["a"], src0=b["ss"]) for b in MAN["brolls"]]
def ovl(o):
    f = W + o["file"]; w, h, _, _ = probe(f)
    dw = int(o["scale"].split(":")[0]) if o.get("scale") else w
    y = o["y"] if isinstance(o["y"], (int, float)) else float(str(o["y"]).split("+")[0].strip("'"))
    return vseg(f, o["s"], o["e"] - o["s"], kind="photo", geo=(o["x"], y, w, h, dw))
paper = [ovl(o) for o in MAN["overlays"] if "paper_" in o["file"]]
cards = [ovl(o) for o in MAN["overlays"] if any(x in o["file"] for x in ("/bf", "/an", "/prd", "/bd", "/ho", "/af", "cta.png"))]
steps = [ovl(o) for o in MAN["overlays"] if "/step" in o["file"]]
pills = [ovl(o) for o in MAN["overlays"] if "/p_" in o["file"]]
wm = [ovl(o) for o in MAN["overlays"] if "wm.png" in o["file"]]
caps = [tseg(c["s"], c["e"], c["txt"]) for c in MAN["caps"]]

def track(kind, segs, name, flag=0):
    return {"id": uid(), "type": kind, "flag": flag, "attribute": 0, "name": name, "is_default_name": False, "segments": segs}
d["tracks"] = [track("video", face, "Face (graded, tight cuts)"), track("video", broll, "B-roll", 2), track("video", paper, "Paper cutaway", 2),
               track("video", cards, "Cards + CTA", 2), track("video", steps, "Step bar", 2), track("video", pills, "Pop-ups", 2),
               track("video", wm, "Watermark", 2), track("text", caps, "Captions"),
               track("audio", [aseg(W + "capcut/voice_clean.wav", name="Voice (DeepFilterNet + EQ)")], "Voice"),
               track("audio", [aseg(W + "capcut/music_bed.wav", name="Eternity bed (Incompetech, CC BY)")], "Music"),
               track("audio", [aseg(W + "capcut/sfx_stem.wav", name="SFX stem")], "SFX")]
for i, tr in enumerate(d["tracks"]):
    for j, s in enumerate(tr["segments"]):
        s["track_render_index"] = i; s["render_index"] = (14001 + j) if tr["type"] == "text" else i

used = {s["material_id"] for t in d["tracks"] for s in t["segments"]} | {r for t in d["tracks"] for s in t["segments"] for r in s["extra_material_refs"]}
for kk, v in M.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
        M[kk] = [m for m in v if m["id"] in used]
for m in M.get("loudnesses", []): m["enable"] = False
for m in M["texts"]:
    m["type"] = "text"; m["recognize_task_id"] = ""; m["recognize_model"] = ""; m["add_type"] = 0; m["recognize_type"] = 0
d["config"]["subtitle_taskinfo"] = []; d["config"]["subtitle_recognition_id"] = ""
d["canvas_config"] = {"ratio": "9:16", "width": CW, "height": CH, "background": None}
d["duration"] = us(MAN["T"])
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("wrote", OUT, {tr["name"]: len(tr["segments"]) for tr in d["tracks"]}, round(d["duration"] / 1e6, 2), "s")
