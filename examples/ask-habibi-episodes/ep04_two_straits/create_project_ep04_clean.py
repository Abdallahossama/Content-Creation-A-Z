"""Create the CapCut project "Ask Habibi Ep4 - two straits" from build/new_draft_content_ep04_clean.json, using the clean
"overthincking ! FINAL" project only as a folder skeleton (no Pro/AI history, empty media panel). CapCut must be closed."""
import json, os, sys, time, uuid, shutil, subprocess

LA = os.environ["LOCALAPPDATA"].replace("\\", "/")
ROOT = LA + "/CapCut/User Data/Projects/com.lveditor.draft"
SRC = ROOT + "/overthincking ! FINAL"
NAME = "Ask Habibi Ep4 - CLEAN voice"
DST = ROOT + "/" + NAME
CONTENT = "D:/why habibi/4th video/build/new_draft_content_ep04_clean.json"

if "capcut.exe" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower():
    sys.exit("CapCut is still running - close it fully first")
if os.path.exists(DST): sys.exit("target project folder already exists: " + DST)

def U(): return str(uuid.uuid4()).upper()
def jload(p): return json.load(open(p, encoding="utf-8"))
def jsave(p, obj, pretty=False):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, **({"indent": 4} if pretty else {"separators": (",", ":")}))

now_s = int(time.time()); now_us = int(time.time() * 1e6); TL, PJ, DID = U(), U(), U()
for sub in ["adjust_mask", "audio_record", "common_attachment", "loudness", "matting", "qr_upload", "smart_crop", "subdraft",
            "Resources/audioAlg", "Resources/combination", "Resources/videoAlg", "Resources/digitalHuman/audio",
            "Resources/digitalHuman/bsinfo", "Resources/digitalHuman/video", f"Timelines/{TL}/common_attachment"]:
    os.makedirs(f"{DST}/{sub}", exist_ok=True)
for f in ["key_value.json", "draft_agency_config.json", "performance_opt_info.json", "attachment_pc_common.json"]:
    if os.path.exists(f"{SRC}/{f}"): shutil.copy2(f"{SRC}/{f}", f"{DST}/{f}")
from PIL import Image                                                # cover = the Ep 4 flag thumbnail, so it is easy to spot
Image.open("D:/why habibi/4th video/export/thumbnails/thumb_4_V5_FLAGS.png").convert("RGB").save(f"{DST}/draft_cover.jpg", quality=90)
for f in os.listdir(SRC + "/common_attachment"):
    for base in (DST, f"{DST}/Timelines/{TL}"): shutil.copy2(f"{SRC}/common_attachment/{f}", f"{base}/common_attachment/{f}")
if os.path.exists(f"{SRC}/attachment_pc_common.json"): shutil.copy2(f"{SRC}/attachment_pc_common.json", f"{DST}/Timelines/{TL}/attachment_pc_common.json")
ae = jload(SRC + "/attachment_editing.json")
for k, v in list(ae["editing_draft"].items()):
    if k.startswith("is_use_") and v is True: ae["editing_draft"][k] = False
ae["editing_draft"]["paste_segment_list"] = []
jsave(DST + "/attachment_editing.json", ae); jsave(f"{DST}/Timelines/{TL}/attachment_editing.json", ae)

d = jload(CONTENT); d["id"] = TL
for p in (DST + "/draft_content.json", f"{DST}/Timelines/{TL}/draft_content.json"): jsave(p, d)
jsave(DST + "/Timelines/project.json", {
    "config": {"color_space": -1, "hdr_vivid": False, "mixed_track_mode_on": False, "render_index_track_mode_on": False, "use_float_render": False},
    "create_time": now_us, "id": PJ, "main_timeline_id": TL,
    "timelines": [{"create_time": now_us, "id": TL, "is_marked_delete": False, "name": "Timeline 01", "update_time": now_us}],
    "update_time": now_us, "version": 0})
jsave(DST + "/timeline_layout.json", {"dockItems": [{"dockIndex": 0, "ratio": 1, "timelineIds": [TL], "timelineNames": ["Timeline 01"]}], "layoutOrientation": 1})
jsave(DST + "/draft_biz_config.json", {"timeline_settings": {TL: {"linkage_enabled": False}}}, pretty=True)
with open(DST + "/draft_settings", "w", encoding="utf-8") as f:
    f.write(f"[General]\ndraft_create_time={now_s}\ndraft_last_edit_time={now_s}\nreal_edit_seconds=0\nreal_edit_keys=0\n"
            f"audio_record_index=0\ncloud_last_modify_platform=windows\n")

meta = jload(SRC + "/draft_meta_info.json")
tmpl = next(v for v in meta["draft_materials"][0]["value"] if v.get("metetype") == "photo")
vals, added, have = [], [], set()
for kind in ("videos", "audios"):
    for m in d["materials"][kind]:
        p = m.get("path", "")
        if not p or p in have: continue
        have.add(p); e = json.loads(json.dumps(tmpl)); mt = "music" if kind == "audios" else "video"
        e.update(id=str(uuid.uuid4()), file_Path=p, extra_info=os.path.basename(p), metetype=mt,
                 width=m.get("width", 0) if kind == "videos" else 0, height=m.get("height", 0) if kind == "videos" else 0,
                 duration=int(m.get("duration", 0)), create_time=now_s, import_time=now_s, import_time_ms=now_us)
        vals.append(e); added.append(e["id"])
meta["draft_materials"][0]["value"] = vals
meta.update(draft_id=DID, draft_name=NAME, draft_fold_path=DST, draft_root_path=ROOT, draft_cover="draft_cover.jpg",
            tm_draft_create=now_us, tm_draft_modified=now_us, tm_duration=d["duration"], draft_is_ai_shorts=False,
            draft_is_ai_packaging_used=False, draft_is_ai_translate=False)
jsave(DST + "/draft_meta_info.json", meta)
vs = jload(SRC + "/draft_virtual_store.json")
for g in vs["draft_virtual_store"]:
    if g["type"] == 1: g["value"] = [{"child_id": i, "parent_id": ""} for i in added]
jsave(DST + "/draft_virtual_store.json", vs)

rm = jload(ROOT + "/root_meta_info.json")
shutil.copy2(ROOT + "/root_meta_info.json", ROOT + "/root_meta_info.json.before_ep04_clean_project")
src_e = next(e for e in rm["all_draft_store"] if e["draft_name"] == "overthincking ! FINAL")
e = json.loads(json.dumps(src_e))
e.update(draft_cover=DST + "\\draft_cover.jpg", draft_fold_path=DST, draft_id=DID, draft_json_file=DST + "\\draft_content.json",
         draft_name=NAME, tm_draft_create=now_us, tm_draft_modified=now_us, tm_duration=d["duration"])
rm["all_draft_store"].insert(0, e); rm["draft_ids"] = len(rm["all_draft_store"])
jsave(ROOT + "/root_meta_info.json", rm)
print("created", NAME, "| media", len(added), "| duration", round(d["duration"] / 1e6, 2), "s")
