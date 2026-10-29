"""Step 3: per-Short public metadata via yt-dlp --print (no download), 6 parallel batches."""
import json, subprocess, sys, concurrent.futures as cf
KEEP = {"unsolvedmysteries", "unsolvedmystery", "unsolved", "mysteries", "unexplained", "truescarystories", "creepyfacts",
        "darkhistory", "historymystery", "disappearance", "ghostship", "strangehistory", "creepyhistory", "mysterious"}
ids = [k for k, v in json.load(open("tag_ids.json")).items() if v["tag"] in KEEP]
chunks = [ids[i::6] for i in range(6)]
FMT = "%(id)s\t%(channel)s\t%(channel_id)s\t%(channel_follower_count)s\t%(upload_date)s\t%(view_count)s\t%(duration)s\t%(title)s"
def run(ch):
    args = [sys.executable, "-m", "yt_dlp", "--skip-download", "--ignore-errors", "--no-warnings", "-O", FMT] + \
           [f"https://www.youtube.com/shorts/{i}" for i in ch]
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    return p.stdout
with cf.ThreadPoolExecutor(6) as ex:
    outs = list(ex.map(run, chunks))
rows = []
for o in outs:
    for line in o.splitlines():
        f = line.split("\t")
        if len(f) >= 8:
            rows.append(dict(zip(["id", "channel", "channel_id", "subs", "date", "views", "dur", "title"], f[:7] + ["\t".join(f[7:])])))
json.dump(rows, open("meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("ids", len(ids), "rows", len(rows))
