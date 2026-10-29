"""Rebuild the 'overthincking !' CapCut timeline around the ElevenLabs voiceover.

Keeps the user's hand-made hook (memes, keyframes, hen/throat gag) re-timed to the new VO,
then lays the rest of the video: rendered graphics, imgflip memes, brand characters,
stickers, SFX, captions in the user's caption style (Rubik-Bold, white, size 7, y=-0.73)."""
import json, copy, uuid, re, subprocess, sys, os, time

ORIG = "cur_draft_content.json"
OUT = "new_draft_content.json"
FPS = 30
V1 = "D:/why habibi/1st video/"
MEME = V1 + "claude_memes/"
GFX = V1 + "claude_gfx/"
SFX = V1 + "claude_sfx/"
PK = "D:/why habibi/WhyHabibi_Pack1_characters_rig_brand (1)/"
VO_FILE = V1 + "ElevenLabs_VO_leveled_-15LUFS.wav"

# ---------------- time model ----------------
def F(sec):            # seconds -> frame-snapped microseconds
    return int(round(sec * FPS)) * 1000000 // FPS

A_END = 269 / FPS                       # VO part A ends (after "...waving at you.")
HEN_DUR = 85 / FPS                      # user's hen clip length (2.833s)
THROAT_DUR = 27 / FPS                   # user's clear-throat beat (0.9s)
GAG_END = A_END + HEN_DUR + THROAT_DUR  # 12.70s
B_SRC = 9.25                            # VO part B source in-point ("Why do embarrassing...")
OFFSET = GAG_END - B_SRC                # every VO time >= B_SRC shifts by this
VO_LEN = 186.82775
END = VO_LEN + OFFSET + 2.75            # hold the end screen ~2.75s after the last word

def T(src):
    """VO-source seconds -> timeline seconds."""
    return src if src < B_SRC - 0.2 else src + OFFSET

def uid():
    return str(uuid.uuid4()).upper()

# ---------------- load ----------------
d = json.load(open(ORIG, encoding="utf-8"))
M = d["materials"]
IDX = {}
for k, v in M.items():
    if isinstance(v, list):
        for m in v:
            if isinstance(m, dict) and "id" in m:
                IDX[m["id"]] = (k, m)

tr = d["tracks"]
bg_track, meme_track, logo_track, text3, text4, vo_track, music_track = tr
T_PHOTO = copy.deepcopy(meme_track["segments"][1])     # sleep.jpg
T_VIDEO = copy.deepcopy(meme_track["segments"][8])     # hen video
T_TEXT = copy.deepcopy(text4["segments"][0])
T_AUDIO = copy.deepcopy(vo_track["segments"][4])       # clear-throat (extract_music)
M_PHOTO = copy.deepcopy(IDX[T_PHOTO["material_id"]][1])
M_VIDEO = copy.deepcopy(IDX[T_VIDEO["material_id"]][1])
M_TEXT = copy.deepcopy(IDX[T_TEXT["material_id"]][1])
M_AUDIO = copy.deepcopy(IDX[T_AUDIO["material_id"]][1])

def clone_refs(seg, drop_anims=True):
    new = []
    for r in seg["extra_material_refs"]:
        k, m = IDX[r]
        if k in ("time_marks",):
            continue
        m2 = copy.deepcopy(m); m2["id"] = uid()
        if k == "material_animations" and drop_anims:
            m2["animations"] = []
        M[k].append(m2); IDX[m2["id"]] = (k, m2); new.append(m2["id"])
    seg["extra_material_refs"] = new

def ffprobe(path):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,codec_type:format=duration",
                        "-of", "json", path], capture_output=True, text=True).stdout
    j = json.loads(o)
    w = h = 0; aud = False
    for s in j.get("streams", []):
        if s.get("codec_type") == "video" and not w:
            w, h = s.get("width", 0), s.get("height", 0)
        if s.get("codec_type") == "audio":
            aud = True
    return w, h, float(j.get("format", {}).get("duration", 0) or 0), aud

_mat_cache = {}
def material(path, kind):
    key = (path, kind)
    if key in _mat_cache:
        return _mat_cache[key]
    w, h, dur, aud = ffprobe(path)
    name = os.path.basename(path)
    if kind == "photo":
        m = copy.deepcopy(M_PHOTO); m.update(path=path, width=w, height=h, material_name=name, type="photo")
        M["videos"].append(m)
    elif kind == "video":
        m = copy.deepcopy(M_VIDEO); m.update(path=path, width=w, height=h, material_name=name, type="video",
                                             duration=int(dur * 1e6), has_audio=aud)
        M["videos"].append(m)
    else:
        m = copy.deepcopy(M_AUDIO); m.update(path=path, name=name, duration=int(dur * 1e6), type="extract_music",
                                             category_name="local")
        M["audios"].append(m)
    m["id"] = uid(); IDX[m["id"]] = (kind, m)
    m["_w"], m["_h"], m["_dur"] = w, h, dur
    _mat_cache[key] = m
    return m

def kf(prop, pts):
    return {"id": uid(), "material_id": "", "property_type": prop,
            "keyframe_list": [{"id": uid(), "curveType": "Line", "time_offset": int(o), "left_control": {"x": 0.0, "y": 0.0},
                               "right_control": {"x": 0.0, "y": 0.0}, "values": [float(v)], "string_value": "", "graphID": ""}
                              for o, v in pts]}

def fit_scale(m, target_h=680, max_w=1350):
    w, h = m["_w"], m["_h"]
    fit = min(1920 / w, 1080 / h)
    return min(target_h / (h * fit), max_w / (w * fit))

def vseg(path, kind, t0, t1, scale=1.0, x=0.0, y=0.0, rot=0.0, src=0.0, motion="pop_zoom", volume=1.0, ri=1):
    """t0/t1 timeline seconds."""
    m = material(path, kind)
    s = copy.deepcopy(T_VIDEO if kind == "video" else T_PHOTO)
    s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    st, en = F(t0), F(t1); dur = en - st
    s["target_timerange"] = {"start": st, "duration": dur}
    s["source_timerange"] = {"start": int(src * 1e6), "duration": dur}
    s["clip"] = {"scale": {"x": scale, "y": scale}, "rotation": rot, "transform": {"x": x, "y": y},
                 "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0}
    s["uniform_scale"] = {"on": True, "value": 1.0}
    s["volume"] = volume; s["last_nonzero_volume"] = 1.0
    s["render_index"] = ri; s["track_render_index"] = ri
    s["common_keyframes"] = []; s["keyframe_refs"] = []
    o0 = int(src * 1e6)
    D = dur
    if motion == "pop_zoom" and D > 400000:
        s["common_keyframes"] = [kf("KFTypeScaleX", [(o0, scale * 0.82), (o0 + 100000, scale * 1.05), (o0 + 170000, scale),
                                                     (o0 + D, scale * 1.07)])]
    elif motion == "pop_zoom":
        s["common_keyframes"] = [kf("KFTypeScaleX", [(o0, scale * 0.88), (o0 + 80000, scale * 1.02), (o0 + D, scale * 1.04)])]
    elif motion == "pop":
        s["common_keyframes"] = [kf("KFTypeScaleX", [(o0, scale * 0.3), (o0 + 120000, scale * 1.12), (o0 + 200000, scale),
                                                     (o0 + D, scale * 1.02)])]
    elif motion == "pop_out":   # pop in, shrink out at the end
        s["common_keyframes"] = [kf("KFTypeScaleX", [(o0, scale * 0.3), (o0 + 120000, scale * 1.12), (o0 + 200000, scale),
                                                     (o0 + D - 150000, scale * 1.03), (o0 + D, scale * 0.2)])]
    elif motion == "zoom":
        s["common_keyframes"] = [kf("KFTypeScaleX", [(o0, scale), (o0 + D, scale * 1.06)])]
    return s

def aseg(path, t0, dur=None, volume=1.0, src=0.0, fade_out=0, ri=0):
    m = material(path, "audio")
    s = copy.deepcopy(T_AUDIO); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    if dur is None:
        dur = m["_dur"] - src
    st = F(t0); du = int(round(dur * 1e6))
    s["target_timerange"] = {"start": st, "duration": du}
    s["source_timerange"] = {"start": int(round(src * 1e6)), "duration": du}
    s["volume"] = volume; s["render_index"] = 0; s["track_render_index"] = ri
    if fade_out:
        for r in s["extra_material_refs"]:
            if IDX[r][0] == "audio_fades":
                IDX[r][1]["fade_out_duration"] = int(fade_out * 1e6)
                break
        else:
            fm = copy.deepcopy(M["audio_fades"][0]); fm["id"] = uid(); fm["fade_in_duration"] = 0
            fm["fade_out_duration"] = int(fade_out * 1e6); M["audio_fades"].append(fm); IDX[fm["id"]] = ("audio_fades", fm)
            s["extra_material_refs"].append(fm["id"])
    return s

# =====================================================================
# 1) HOOK: re-time the user's own 16 meme segments to the new VO
# =====================================================================
hook_times = [  # (t0, t1) in timeline seconds, same order as the user's track
    (0.00, 1.46), (1.46, 3.54), (3.54, 4.42), (4.42, 4.78), (4.78, 6.02), (6.02, 6.48), (6.48, 7.24), (7.24, A_END),
    (A_END, A_END + HEN_DUR), (A_END + HEN_DUR, GAG_END),
    (T(9.25), T(12.68)), (T(12.68), T(14.06)), (T(14.06), T(14.52)), (T(14.52), T(16.46)), (T(16.46), T(16.84)),
    (T(16.84), T(17.98)),
]
old_segs = meme_track["segments"]
assert len(old_segs) == 16
hook = []
for s, (a, b) in zip(old_segs, hook_times):
    s = copy.deepcopy(s)
    old_dur = s["target_timerange"]["duration"]
    st, en = F(a), F(b); dur = en - st
    s["target_timerange"] = {"start": st, "duration": dur}
    if s.get("source_timerange"):
        s["source_timerange"]["duration"] = dur
    src0 = (s.get("source_timerange") or {}).get("start", 0)
    for e in s.get("common_keyframes") or []:
        for p in e["keyframe_list"]:
            rel = p["time_offset"] - src0
            p["time_offset"] = int(src0 + rel * dur / old_dur)
    s["render_index"] = 1; s["track_render_index"] = 1
    hook.append(s)

# =====================================================================
# 2) MAIN VISUAL TRACK after the hook (src times from the VO)
# =====================================================================
def meme(name):
    return MEME + name

def ch(name, mood):
    return f"{PK}01_Characters_Plain/{name}/{name}_{mood}.png"

def ps(name, p):
    return f"{PK}03_Poses/{name}/{name}_pose_{p}.png"

G = lambda n: GFX + n + ".mp4"
main = [  # (kind, path, src0, src1, opts)
    ("photo", ch("Batata", "love"), 17.98, 19.56, dict(h=640)),
    ("photo", meme("waiting_skeleton.png"), 19.56, 23.00, {}),
    ("photo", meme("sad_pablo.png"), 23.00, 24.96, {}),
    ("gfx", G("01_brand_reveal"), 24.96, 33.92, {}),
    ("photo", meme("grus_plan_4levels.png"), 33.92, 35.98, {}),
    ("gfx", G("02_iceberg_overview"), 35.98, 38.80, {}),
    ("photo", meme("harold_smile.png"), 38.80, 40.32, {}),
    ("gfx", G("03_level1"), 40.32, 42.10, {}),
    ("gfx", G("04_study_2007"), 42.10, 46.88, {}),
    ("gfx", G("05_three_days_bars"), 46.88, 54.68, {}),
    ("photo", meme("leo_cheers.png"), 54.68, 56.34, {}),
    ("gfx", G("06_not_the_same"), 56.34, 62.08, {}),
    ("photo", meme("megamind_peeking.png"), 62.08, 65.56, {}),
    ("gfx", G("07_streaming"), 65.56, 70.16, {}),
    ("gfx", G("08_level2"), 70.16, 72.84, {}),
    ("gfx", G("09_term_post_event"), 72.84, 75.72, {}),
    ("gfx", G("10_chat_stranger"), 75.72, 78.28, {}),
    ("gfx", G("11_rating"), 78.28, 84.02, {}),
    ("gfx", G("12_calendar_postmortem"), 84.02, 88.44, {}),
    ("gfx", G("13_level3"), 88.44, 90.06, {}),
    ("gfx", G("14_karaoke_steps"), 90.06, 94.20, {}),
    ("photo", meme("sleeping_shaq.png"), 94.20, 97.54, {}),
    ("gfx", G("15_sensitivity_gauge"), 97.54, 102.20, {}),
    ("photo", meme("scientist_myself.png"), 102.20, 104.40, {}),
    ("gfx", G("16_rem_proposal"), 104.40, 115.52, {}),
    ("gfx", G("17_cringe_volume"), 115.52, 121.16, {}),
    ("gfx", G("18_level4"), 121.16, 123.14, {}),
    ("gfx", G("19_search_no_study"), 123.14, 126.70, {}),
    ("gfx", G("20_my_guess"), 126.70, 130.90, {}),
    ("photo", meme("this_is_fine.png"), 130.90, 132.92, {}),
    ("photo", ch("Dorra", "happy"), 132.92, 134.28, dict(h=620)),
    ("gfx", G("21_cornell_tshirt"), 134.28, 141.32, {}),
    ("photo", meme("surprised_pikachu.png"), 141.32, 142.74, {}),
    ("gfx", G("22_noticing_remembering"), 142.74, 145.84, {}),
    ("photo", meme("monkey_puppet.png"), 145.84, 148.50, {}),
    ("photo", meme("pawn_stars.png"), 148.50, 150.10, {}),
    ("gfx", G("23_strategy_title"), 150.10, 152.70, {}),
    ("gfx", G("24_steps_notice_move"), 152.70, 161.34, {}),
    ("photo", meme("squidward_window.png"), 161.34, 163.96, {}),
    ("photo", V1 + "Absolute Cinema.jpg", 163.96, 165.78, {}),
    ("gfx", G("25_doctor_disclaimer"), 165.78, 175.26, {}),
    ("photo", ps("Batata", "thumbs"), 175.26, 176.34, dict(h=640)),
    ("endscreen", PK + "07_Brand/end_screen_1920x1080.png", 176.34, None, {}),
]
main_segs = list(hook)
for kind, path, s0, s1, o in main:
    t0 = T(s0); t1 = END if s1 is None else T(s1)
    if kind == "gfx":
        main_segs.append(vseg(path, "video", t0, t1, 1.0, 0, 0, motion=None, volume=0.0))
    elif kind == "endscreen":
        main_segs.append(vseg(path, "photo", t0, t1, 1.0, 0, 0, motion="zoom"))
    else:
        m = material(path, "photo")
        sc = fit_scale(m, o.get("h", 680))
        main_segs.append(vseg(path, "photo", t0, t1, sc, 0.0, 0.09))
# sanity: contiguous, no overlap
for a, b in zip(main_segs, main_segs[1:]):
    ea = a["target_timerange"]["start"] + a["target_timerange"]["duration"]
    assert ea == b["target_timerange"]["start"], (ea, b["target_timerange"]["start"], IDX[b["material_id"]][1].get("path"))
meme_track["segments"] = main_segs

# background: extend to the end
bg_track["segments"] = [vseg(GFX + "00_background_midnight.mp4", "video", 0.0, END, 1.0, 0, 0, motion=None, volume=0.0, ri=0)]

# =====================================================================
# 3) OVERLAY TRACK (stickers / reaction pop-ins / end-screen extras)
# =====================================================================
STK = PK + "07_Brand/stickers/"
def sticker_scale(path, width_px):
    m = material(path, "photo"); fit = min(1920 / m["_w"], 1080 / m["_h"])
    return width_px / (m["_w"] * fit)

ov = []
def overlay(path, s0, s1, width_px, x, y, rot=0.0, src_is_tl=False, motion="pop_out"):
    t0 = s0 if src_is_tl else T(s0); t1 = s1 if src_is_tl else T(s1)
    ov.append(vseg(path, "photo", t0, t1, sticker_scale(path, width_px), x, y, rot, motion=motion, ri=2))

overlay(STK + "sticker_huh.png", 9.40, 11.40, 430, 0.52, 0.62, -7)             # "why do embarrassing memories..."
overlay(STK + "sticker_zzz.png", 94.30, 96.90, 400, 0.55, 0.62, 8)             # Shaq sleeping
overlay(meme("laughing_leo.png"), 91.50, 92.72, 560, 0.42, 0.06, 4)            # recordings played back
overlay(STK + "sticker_mind.png", 68.72, 70.10, 470, 0.50, -0.42, -6)          # worst content
overlay(STK + "sticker_actually.png", 56.34, 58.00, 470, -0.55, 0.70, -6)      # sleepless night != bad evening
overlay(STK + "sticker_wrong.png", 141.88, 142.70, 430, 0.52, 0.60, 8)         # the bad news?
overlay(STK + "sticker_fact.png", 52.44, 53.80, 380, 0.70, 0.52, 7)           # held up
overlay(PK + "07_Brand/subscribe_button.png", 177.24, 180.70, 560, 0.0, -0.52, 0.0)
overlay(GFX + "comment_bubble.png", 181.66, 184.66, 600, -0.33, -0.26, 0.0)
ov = [s for s in ov if s]
ov.sort(key=lambda s: s["target_timerange"]["start"])
for a, b in zip(ov, ov[1:]):
    assert a["target_timerange"]["start"] + a["target_timerange"]["duration"] <= b["target_timerange"]["start"]
ov_track = {"id": uid(), "type": "video", "flag": 2, "attribute": 0, "name": "", "is_default_name": True, "segments": ov}

# =====================================================================
# 4) LOGO watermark: whole video except brand reveal + end screen
# =====================================================================
logo = logo_track["segments"][0]
l1 = copy.deepcopy(logo); l2 = copy.deepcopy(logo); l2["id"] = uid(); clone_refs(l2, drop_anims=False)
l1["target_timerange"] = {"start": 0, "duration": F(T(24.96))}
l1["source_timerange"] = {"start": 0, "duration": F(T(24.96))}
l2["target_timerange"] = {"start": F(T(33.92)), "duration": F(T(176.34)) - F(T(33.92))}
l2["source_timerange"] = {"start": 0, "duration": l2["target_timerange"]["duration"]}
for s in (l1, l2):
    s["render_index"] = 3; s["track_render_index"] = 3
logo_track["segments"] = [l1, l2]

# =====================================================================
# 5) CAPTIONS (user's style: Rubik-Bold white size 7 at y=-0.73, short chunks)
# =====================================================================
words = json.load(open("words_flat.json", encoding="utf-8"))
toks = []
for w in words:
    tx = w["w"].strip()
    if tx.startswith("-") and toks:              # post -event, t -shirt
        toks[-1]["w"] += tx; toks[-1]["e"] = w["e"]; continue
    if tx == ".m." and len(toks) >= 2 and toks[-1]["w"] == "a" and toks[-2]["w"] == "3":
        toks.pop(); toks[-1]["w"] = "3am"; toks[-1]["e"] = w["e"]; continue
    toks.append({"w": tx, "s": w["s"], "e": w["e"]})

CAPS = {"i": "I", "habibi": "Habibi", "cornell": "Cornell", "rem": "REM", "i'm": "I'm", "i'd": "I'd"}
def disp(tok, prev):
    core = re.sub(r"[.,;:]+$", "", tok)
    q = "?" if core.endswith("?") else ("!" if core.endswith("!") else "")
    core = core.rstrip("?!")
    low = core.lower()
    low = re.sub(r"^3am$", "3:00am", low)
    if low in CAPS: low = CAPS[low]
    if low == "ask" and prev is not None and False: pass
    return low + q

FUNC = {"a", "an", "the", "to", "of", "your", "at", "in", "and", "for", "with", "is", "that", "my", "i", "on", "as"}
chunks = []; cur = []
for i, tk in enumerate(toks):
    if cur:
        prev = cur[-1]
        text_len = len(" ".join(disp(x["w"], None) for x in cur + [tk]))
        hard = re.search(r"[.,?!]$", prev["w"]) or tk["s"] - prev["e"] > 0.35
        soft = len(cur) >= 3 or text_len > 18
        if prev["w"].lower() == "ask" and tk["w"].lower().startswith("habibi") and text_len <= 24:
            soft = False
        if hard or soft:
            carry = []
            if soft and not hard and len(cur) >= 2 and cur[-1]["w"].lower() in FUNC:
                carry = [cur.pop()]
            chunks.append(cur); cur = carry
    cur.append(tk)
if cur: chunks.append(cur)

caps = []
for i, c in enumerate(chunks):
    words_d = []
    for j, x in enumerate(c):
        dd = disp(x["w"], c[j - 1]["w"] if j else None)
        if dd == "habibi".capitalize() and j and words_d and words_d[-1] == "ask":
            words_d[-1] = "Ask"
        words_d.append(dd)
    txt = " ".join(words_d)
    s = c[0]["s"]; e = c[-1]["e"] + 0.25
    if len(c) >= 2 and c[1]["s"] - c[0]["s"] > 0.45 and len(c[0]["w"]) <= 3:
        s = c[1]["s"] - 0.2
    if i + 1 < len(chunks):
        nc = chunks[i + 1]
        ns = nc[0]["s"]
        if len(nc) >= 2 and nc[1]["s"] - nc[0]["s"] > 0.45 and len(nc[0]["w"]) <= 3:
            ns = nc[1]["s"] - 0.2
        if ns - c[-1]["e"] < 0.6:
            e = ns
        e = min(e, ns)
    t0, t1 = T(s), T(e)
    if s < B_SRC - 0.2:
        t1 = min(t1, A_END)
    if t1 - t0 < 0.2:
        t1 = t0 + 0.2
    caps.append((t0, t1, txt, [(x["s"], x["e"], disp(x["w"], None)) for x in c]))

text_segs = []
for k, (t0, t1, txt, ws) in enumerate(caps):
    m = copy.deepcopy(M_TEXT); m["id"] = uid()
    content = json.loads(m["content"]); content["text"] = txt
    for st in content["styles"]: st["range"] = [0, len(txt)]
    m["content"] = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
    bc = json.loads(m["base_content"]); bc["text"] = txt
    for st in bc["styles"]: st["range"] = [0, len(txt)]
    m["base_content"] = json.dumps(bc, ensure_ascii=False, separators=(",", ":"))
    m["recognize_text"] = txt
    st_, et_, tx_ = [], [], []
    base = ws[0][0]
    for j, (a, b, w) in enumerate(ws):
        if j:
            st_.append(int((a - base) * 1000)); et_.append(int((a - base) * 1000)); tx_.append(" ")
        st_.append(int((a - base) * 1000)); et_.append(int((b - base) * 1000)); tx_.append(w)
    m["words"] = {"start_time": st_, "end_time": et_, "text": tx_}
    M["texts"].append(m); IDX[m["id"]] = ("texts", m)
    s = copy.deepcopy(T_TEXT); s["id"] = uid(); s["material_id"] = m["id"]; clone_refs(s)
    st, en = F(t0), F(t1)
    if text_segs:
        prev_end = text_segs[-1]["target_timerange"]["start"] + text_segs[-1]["target_timerange"]["duration"]
        st = max(st, prev_end)
    s["target_timerange"] = {"start": st, "duration": max(en - st, 100000)}
    s["source_timerange"] = {"start": 0, "duration": s["target_timerange"]["duration"]}
    s["render_index"] = 14001 + k; s["track_render_index"] = 5
    text_segs.append(s)
text4["segments"] = text_segs

# =====================================================================
# 6) AUDIO: VO (A + B), clear throat, music, SFX
# =====================================================================
throat = copy.deepcopy(vo_track["segments"][4])
throat["target_timerange"]["start"] = F(A_END + HEN_DUR)
vo_a = aseg(VO_FILE, 0.0, A_END, 1.0, 0.0, ri=6)
vo_b = aseg(VO_FILE, GAG_END, VO_LEN - B_SRC, 1.0, B_SRC, ri=6)
vo_b["target_timerange"]["start"] = F(GAG_END)
vo_track["segments"] = [vo_a, throat, vo_b]

# music: one sectioned, VO-ducked bed (built by music_bed.py) replaces the old game-OST track
MUSIC_BED = V1 + "claude_music/music_bed_ep01.wav"
music_track["segments"] = [aseg(MUSIC_BED, 0.0, END - 0.01, 1.0, 0.0, ri=7)]

# SFX cue sheet: (name, src_time, volume)  — times < 9 are timeline (hook), else VO-source
SV = dict(whoosh_fast=0.2, whoosh_long=0.2, swoosh_in=0.22, pop=0.3, pop_high=0.28, ding=0.22, sparkle=0.25,
          impact_boom=0.3, riser=0.16, clock_ticks=0.3, heartbeat=0.45, glitch_error=0.16, boing=0.25, click=0.4,
          typing=0.3, shutter=0.3, dramatic_sting=0.25, record_scratch=0.3, fire_crackle=0.55)
cues = [
    ("clock_ticks", 0.0), ("pop", 3.54), ("pop_high", 4.42), ("shutter", 4.78), ("whoosh_fast", 6.02), ("pop", 6.48),
    ("dramatic_sting", 11.40), ("heartbeat", 12.68), ("pop", 14.06), ("whoosh_fast", 14.52), ("pop_high", 16.46), ("ding", 16.90),
    ("pop", 17.98), ("clock_ticks", 19.70), ("record_scratch", 22.95),
    ("whoosh_long", 24.80), ("sparkle", 25.40), ("pop", 26.68), ("impact_boom", 28.06), ("click", 29.58), ("pop", 29.76),
    ("whoosh_fast", 31.20), ("pop", 31.30), ("click", 32.05), ("ding", 32.15),
    ("swoosh_in", 33.40), ("pop", 35.02), ("whoosh_long", 35.90),
    ("click", 36.03), ("click", 36.35), ("click", 36.67), ("click", 36.99), ("glitch_error", 37.86), ("record_scratch", 38.80),
    ("whoosh_long", 40.20), ("impact_boom", 40.60), ("pop", 42.10), ("pop", 43.26), ("pop", 44.80), ("boing", 45.10),
    ("whoosh_fast", 46.85), ("swoosh_in", 47.40), ("whoosh_fast", 50.14), ("impact_boom", 52.44), ("impact_boom", 53.80),
    ("ding", 55.08), ("whoosh_fast", 56.30), ("pop", 58.04), ("pop", 59.22), ("whoosh_fast", 60.18), ("pop", 60.86),
    ("pop_high", 62.62), ("whoosh_long", 65.50), ("whoosh_fast", 66.68), ("click", 67.94), ("glitch_error", 68.72),
    ("whoosh_long", 70.05), ("impact_boom", 70.45), ("typing", 72.95), ("whoosh_fast", 75.70), ("pop", 76.58), ("pop_high", 77.32),
    ("pop", 78.58), ("click", 79.80), ("click", 80.10), ("click", 80.40), ("pop", 81.42), ("sparkle", 83.38),
    ("whoosh_fast", 84.00), ("click", 87.03), ("glitch_error", 87.15),
    ("whoosh_long", 88.35), ("impact_boom", 88.75), ("pop", 90.06), ("pop", 91.42), ("pop", 92.80),
    ("whoosh_fast", 94.18), ("whoosh_fast", 97.50), ("riser", 98.30), ("pop", 102.20), ("pop", 104.55), ("click", 105.74),
    ("whoosh_fast", 107.76), ("boing", 109.80), ("impact_boom", 113.80),
    ("whoosh_fast", 115.48), ("click", 116.56), ("whoosh_fast", 117.92), ("riser", 118.40), ("glitch_error", 120.30),
    ("whoosh_long", 121.05), ("dramatic_sting", 121.40), ("typing", 123.40), ("glitch_error", 125.55),
    ("pop", 126.70), ("click", 127.45), ("click", 128.85), ("click", 130.05), ("whoosh_fast", 130.88),
    ("fire_crackle", 130.85), ("sparkle", 132.92), ("whoosh_fast", 134.25), ("pop", 136.30), ("whoosh_fast", 138.12), ("pop", 138.80), ("pop_high", 140.70),
    ("record_scratch", 141.30), ("pop", 141.88), ("click", 143.72), ("pop", 144.70), ("whoosh_fast", 145.84), ("pop", 148.50),
    ("whoosh_long", 150.00), ("ding", 150.25), ("pop", 152.70), ("pop", 154.62), ("click", 158.36), ("click", 159.28),
    ("click", 159.92), ("whoosh_fast", 161.34), ("pop", 161.50), ("dramatic_sting", 163.96), ("whoosh_long", 165.70),
    ("ding", 169.70), ("pop", 175.26), ("whoosh_long", 176.25), ("pop", 177.24), ("click", 177.70), ("ding", 177.80),
    ("pop", 181.66),
]
sfx_tracks = [[], []]
for name, s0 in cues:
    t0 = s0 if s0 < 9.0 else T(s0)
    dur, fo = {"fire_crackle": (2.35, 0.4)}.get(name, (None, 0))
    seg = aseg(SFX + name + ".wav", t0, dur, SV[name], fade_out=fo)
    st = seg["target_timerange"]["start"]; en = st + seg["target_timerange"]["duration"]
    for k, lane in enumerate(sfx_tracks):
        if not lane or lane[-1]["target_timerange"]["start"] + lane[-1]["target_timerange"]["duration"] <= st:
            seg["track_render_index"] = 8 + k; lane.append(seg); break
    else:
        # third lane needed: trim the earlier one in lane 0
        last = sfx_tracks[0][-1]
        last["target_timerange"]["duration"] = st - last["target_timerange"]["start"]
        last["source_timerange"]["duration"] = last["target_timerange"]["duration"]
        sfx_tracks[0].append(seg)
sfx_track_objs = [{"id": uid(), "type": "audio", "flag": 0, "attribute": 0, "name": "", "is_default_name": True, "segments": lane}
                  for lane in sfx_tracks if lane]

# =====================================================================
# 6b) STRIP PRO / AI FEATURES so the project exports on a free plan
# =====================================================================
pro_effects = {m["id"] for m in M.get("effects", []) if m.get("type") == "smart_color_adjust"}
for seg in meme_track["segments"]:
    if any(r in pro_effects for r in seg["extra_material_refs"]):
        seg["extra_material_refs"] = [r for r in seg["extra_material_refs"] if r not in pro_effects]
    seg["enable_smart_color_adjust"] = False
M["effects"] = [m for m in M.get("effects", []) if m["id"] not in pro_effects]
M["audio_effects"] = []                       # unused "Divine Echo" voice filter
for m in M.get("loudnesses", []):
    m["enable"] = False                       # normalize-loudness off
for m in M.get("vocal_separations", []):
    m["choice"] = 0; m["removed_sounds"] = []; m["production_path"] = ""
for m in M["texts"]:                          # auto-caption origin -> plain text
    m["type"] = "text"; m["recognize_task_id"] = ""; m["recognize_model"] = ""; m["add_type"] = 0
    m["recognize_type"] = 0
d["config"]["subtitle_taskinfo"] = []
d["config"]["subtitle_recognition_id"] = ""

# =====================================================================
# 7) ASSEMBLE + garbage-collect materials from removed segments
# =====================================================================
d["tracks"] = [bg_track, meme_track, ov_track, logo_track, text4, vo_track, music_track] + sfx_track_objs
for i, t in enumerate(d["tracks"]):
    for s in t["segments"]:
        if t["type"] == "video":
            s["render_index"] = s.get("render_index", i); s["track_render_index"] = i
        elif t["type"] == "text":
            s["track_render_index"] = i
        else:
            s["track_render_index"] = i
used = set()
for t in d["tracks"]:
    for s in t["segments"]:
        used.add(s["material_id"]); used.update(s["extra_material_refs"])
GC_KINDS = {"videos", "audios", "texts", "speeds", "placeholder_infos", "canvases", "material_animations",
            "sound_channel_mappings", "material_colors", "loudnesses", "vocal_separations", "beats", "audio_fades",
            "realtime_denoises", "vocal_beautifys"}
removed = 0
for k in GC_KINDS:
    if k in M:
        before = len(M[k]); M[k] = [m for m in M[k] if m.get("id") in used]; removed += before - len(M[k])
for k, v in M.items():
    if isinstance(v, list):
        for m in v:
            if isinstance(m, dict):
                for kk in ("_w", "_h", "_dur"):
                    m.pop(kk, None)
d["duration"] = F(END)
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

# report
print("END", round(END, 3), "OFFSET", round(OFFSET, 3), "removed mats", removed)
for i, t in enumerate(d["tracks"]):
    print(i, t["type"], t["flag"], len(t["segments"]))
print("captions:", len(caps))
for c in caps[:14] + caps[-6:]:
    print(f"  {c[0]:7.2f}-{c[1]:7.2f} {c[2]}")
json.dump({"assets": sorted({m["path"] for m in M["videos"]} | {m["path"] for m in M["audios"]})}, open("assets_used.json", "w"), indent=1)
