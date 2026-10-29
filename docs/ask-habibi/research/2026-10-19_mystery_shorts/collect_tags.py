"""Step 2: public hashtag /shorts listings -> Short IDs + views; then per-Short public metadata (channel, subs, date)."""
import json, subprocess, sys
TAGS = ["unsolvedmysteries", "unsolvedmystery", "unsolved", "mystery", "mysteries", "unexplained", "scarystories",
        "truescarystories", "creepy", "creepyfacts", "darkhistory", "historymystery", "bermudatriangle", "disappearance",
        "coldcase", "ghostship", "strangehistory", "creepyhistory", "mysterious", "realstory", "truestory", "halloween2026"]
ids = {}
for t in TAGS:
    p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "60",
                        f"https://www.youtube.com/hashtag/{t}/shorts"], capture_output=True, text=True, encoding="utf-8")
    if p.returncode: print("FAIL", t, p.stderr[-120:]); continue
    n = 0
    for e in json.loads(p.stdout).get("entries", []):
        if e.get("id") and e["id"] not in ids: ids[e["id"]] = {"tag": t, "views_list": e.get("view_count")}; n += 1
    print(t, n, flush=True)
json.dump(ids, open("tag_ids.json", "w"), indent=0)
print("total", len(ids))
