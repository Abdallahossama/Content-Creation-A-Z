"""Write new_draft_content.json into an EXISTING CapCut project (keeps its ids/registry). CapCut must be closed.
usage: python update_project.py "<project name>" [expected_sha1_of_current_draft]"""
import json, os, sys, time, uuid, shutil, subprocess, hashlib
LA = os.environ["LOCALAPPDATA"].replace("\\", "/")
ROOT = LA + "/CapCut/User Data/Projects/com.lveditor.draft"
NAME = sys.argv[1]; P = f"{ROOT}/{NAME}"
if "capcut.exe" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower():
    sys.exit("CapCut is running - close it fully first")
cur = open(P + "/draft_content.json", "rb").read()
if len(sys.argv) > 2 and hashlib.sha1(cur).hexdigest() != sys.argv[2]:
    sys.exit("project changed since it was checked - re-check before writing")
stamp = time.strftime("%Y%m%d-%H%M%S")
bk = f"D:/why habibi/_draft_backups/{NAME} ({stamp})"; shutil.copytree(P, bk); print("backup:", bk)
TL = json.load(open(P + "/Timelines/project.json", encoding="utf-8"))["main_timeline_id"]
d = json.load(open("new_draft_content.json", encoding="utf-8")); d["id"] = TL
data = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
for f in (P + "/draft_content.json", f"{P}/Timelines/{TL}/draft_content.json", P + "/template-2.tmp", f"{P}/Timelines/{TL}/template-2.tmp"):
    if f.endswith("draft_content.json") or os.path.exists(f):
        open(f, "wb").write(data)
now_s, now_us = int(time.time()), int(time.time() * 1e6)
meta = json.load(open(P + "/draft_meta_info.json", encoding="utf-8"))
vals = meta["draft_materials"][0]["value"]; have = {v["file_Path"] for v in vals}
tmpl = next(v for v in vals if v.get("metetype") == "photo"); added = []
for kind in ("videos", "audios"):
    for m in d["materials"][kind]:
        p = m.get("path", "")
        if not p or p.startswith("##") or p in have: continue
        have.add(p); e = json.loads(json.dumps(tmpl))
        mt = "music" if kind == "audios" else ("photo" if m.get("type") == "photo" else "video")
        e.update(id=str(uuid.uuid4()), file_Path=p, extra_info=os.path.basename(p), metetype=mt,
                 width=m.get("width", 0) if kind == "videos" else 0, height=m.get("height", 0) if kind == "videos" else 0,
                 duration=5000000 if mt == "photo" else int(m.get("duration", 0)), create_time=now_s, import_time=now_s, import_time_ms=now_us)
        vals.append(e); added.append(e["id"])
meta["tm_duration"] = d["duration"]; meta["tm_draft_modified"] = now_us
json.dump(meta, open(P + "/draft_meta_info.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
vs = json.load(open(P + "/draft_virtual_store.json", encoding="utf-8"))
for g in vs["draft_virtual_store"]:
    if g["type"] == 1: g["value"] += [{"child_id": i, "parent_id": ""} for i in added]
json.dump(vs, open(P + "/draft_virtual_store.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
rm = json.load(open(ROOT + "/root_meta_info.json", encoding="utf-8"))
for e in rm["all_draft_store"]:
    if e.get("draft_name") == NAME: e["tm_duration"] = d["duration"]; e["tm_draft_modified"] = now_us
json.dump(rm, open(ROOT + "/root_meta_info.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"updated '{NAME}' (timeline {TL}), media +{len(added)}, duration {d['duration'] / 1e6:.2f}s")
