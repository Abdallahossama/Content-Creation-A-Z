"""Mystery-Shorts scan 2026-10-19 step 1: public YouTube search listings (yt-dlp flat, no login) -> candidate channels."""
import json, subprocess, sys, collections
Q = ["unsolved mystery shorts", "true scary story shorts", "real unsolved mysteries", "unexplained disappearance shorts",
     "creepy true story shorts", "mystery that was never solved", "bermuda triangle shorts", "db cooper shorts",
     "lighthouse keepers vanished", "somerton man shorts", "ghost ship mystery shorts", "creepiest unsolved case shorts",
     "strange historical mystery shorts", "unexplained events history shorts", "creepy facts history shorts",
     "dark history shorts", "unsolved mysteries 2026", "mysterious disappearances history", "tunguska event shorts",
     "wow signal shorts", "centralia fire shorts", "flight 19 shorts", "mary celeste shorts", "dyatlov pass shorts"]
hits = collections.defaultdict(list)
for q in Q:
    for mode in ("ytsearch40", "ytsearchdate40"):
        p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", f"{mode}:{q}"],
                           capture_output=True, text=True, encoding="utf-8")
        if p.returncode: print("FAIL", q, p.stderr[-120:]); continue
        for e in json.loads(p.stdout).get("entries", []):
            d = e.get("duration") or 0
            if d and d <= 180 and e.get("channel_id"):
                hits[(e["channel_id"], e.get("channel"))].append({"q": q, "title": e.get("title"), "views": e.get("view_count"), "url": e.get("url")})
    print("done", q, len(hits), flush=True)
out = sorted(([cid, ch, len(v), v[:3]] for (cid, ch), v in hits.items()), key=lambda r: -r[2])
json.dump(out, open("candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for cid, ch, n, v in out[:80]: print(n, ch, cid, "|", (v[0]["title"] or "")[:60], v[0]["views"])
