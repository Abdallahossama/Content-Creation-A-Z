"""Write the rebuilt timeline into the CapCut project. CapCut must be fully closed."""
import json, os, sys, time, uuid, subprocess, shutil, hashlib
LA = os.environ["LOCALAPPDATA"].replace("\\", "/")
ROOT = LA + "/CapCut/User Data/Projects/com.lveditor.draft"
D = ROOT + "/overthincking !"
TL = D + "/Timelines/CF60EA38-4C38-4f01-9335-2A7B1323DEDF"

if "capcut.exe" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower():
    sys.exit("CapCut is still running - close it fully first")

# guard: the on-disk draft must still be the one we built from
if open(D + "/draft_content.json", "rb").read() != open("cur_draft_content.json", "rb").read():
    sys.exit("draft changed on disk since the build snapshot - rebuild first")

new = open("new_draft_content.json", "rb").read()
d = json.loads(new)
for p in [D + "/draft_content.json", TL + "/draft_content.json", D + "/template-2.tmp", TL + "/template-2.tmp"]:
    if os.path.exists(p) or p.endswith("draft_content.json"):
        open(p, "wb").write(new)
        print("wrote", p[len(ROOT):])

now_s = int(time.time()); now_us = int(time.time() * 1e6)
# media panel: add every new asset the timeline uses
meta = json.load(open(D + "/draft_meta_info.json", encoding="utf-8"))
vals = meta["draft_materials"][0]["value"]
have = {v["file_Path"] for v in vals}
tmpl = next(v for v in vals if v.get("metetype") == "photo")
added = []
for kind, mats in (("videos", d["materials"]["videos"]), ("audios", d["materials"]["audios"])):
    for m in mats:
        p = m.get("path", "")
        if not p or p.startswith("##") or p in have:
            continue
        have.add(p)
        e = json.loads(json.dumps(tmpl))
        mt = "music" if kind == "audios" else ("photo" if m.get("type") == "photo" else "video")
        e.update(id=str(uuid.uuid4()), file_Path=p, extra_info=os.path.basename(p), metetype=mt,
                 width=m.get("width", 0) if kind == "videos" else 0, height=m.get("height", 0) if kind == "videos" else 0,
                 duration=5000000 if mt == "photo" else int(m.get("duration", 0)),
                 create_time=now_s, import_time=now_s, import_time_ms=now_us)
        vals.append(e); added.append(e["id"])
meta["tm_duration"] = d["duration"]; meta["tm_draft_modified"] = now_us
json.dump(meta, open(D + "/draft_meta_info.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
vs = json.load(open(D + "/draft_virtual_store.json", encoding="utf-8"))
for g in vs["draft_virtual_store"]:
    if g["type"] == 1:
        g["value"] += [{"child_id": i, "parent_id": ""} for i in added]
json.dump(vs, open(D + "/draft_virtual_store.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("media panel +", len(added))
# project list registry
rm = json.load(open(ROOT + "/root_meta_info.json", encoding="utf-8"))
for e in rm["all_draft_store"]:
    if e.get("draft_name") == "overthincking !":
        e["tm_duration"] = d["duration"]; e["tm_draft_modified"] = now_us
json.dump(rm, open(ROOT + "/root_meta_info.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("registry updated; duration", d["duration"] / 1e6)
