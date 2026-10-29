"""Step 1b: YouTube search URLs sorted by view count, uploaded this month / this year (public, no login)."""
import json, subprocess, sys, collections, urllib.parse
Q = ["unsolved mystery", "true scary story", "unsolved mysteries shorts", "creepy true story", "unexplained disappearance",
     "real mystery never solved", "mysterious disappearance history", "creepy history", "scary true story shorts",
     "unsolved case", "strange disappearance", "creepy unsolved mystery", "historical mystery", "ghost ship",
     "vanished without a trace", "unexplained mystery", "dark history mystery", "lighthouse keepers", "creepiest mystery"]
SP = {"month_views": "CAMSAggE", "year_views": "CAMSAggF"}
hits = collections.defaultdict(list)
for q in Q:
    for tag, sp in SP.items():
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q) + "&sp=" + urllib.parse.quote(sp)
        p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "60", url],
                           capture_output=True, text=True, encoding="utf-8")
        if p.returncode: print("FAIL", q, tag, p.stderr[-150:]); continue
        for e in json.loads(p.stdout).get("entries", []):
            d = e.get("duration") or 0
            sh = "/shorts/" in (e.get("url") or "")
            if (sh or (d and d <= 180)) and e.get("channel_id"):
                hits[(e["channel_id"], e.get("channel"))].append({"q": q, "tag": tag, "title": e.get("title"), "views": e.get("view_count"), "url": e.get("url")})
    print("done", q, len(hits), flush=True)
out = sorted(([cid, ch, len(v), max((x["views"] or 0) for x in v), v[:4]] for (cid, ch), v in hits.items()), key=lambda r: -r[3])
json.dump(out, open("candidates2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
