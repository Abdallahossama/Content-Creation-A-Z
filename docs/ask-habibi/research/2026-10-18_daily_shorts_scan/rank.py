"""Newest 20 Shorts per channel ranked by views / that channel's median Shorts views (swipe.py method)."""
import json, statistics
rows = json.load(open("collected.json", encoding="utf-8")); rec = set(json.load(open("recent.json")))
med = {}
for r in rows: med.setdefault(r["channel"], []).append(r["views"])
med = {k: statistics.median(v) for k, v in med.items() if len(v) >= 4}
out = [dict(r, multiple=r["views"] / med[r["channel"]], median=med[r["channel"]]) for r in rows if r["url"] in rec and r["channel"] in med]
json.dump(out, open("recent_ranked.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for ln in ("curiosity", "news_maps"):
    print(f"\n=== {ln}: newest 20 Shorts per channel, multiple over channel median ===")
    for x in sorted([x for x in out if x["lane"] == ln], key=lambda x: -x["multiple"])[:22]:
        print(f"{x['multiple']:5.1f}x {x['views']:>11,} (med {int(x['median']):>9,}) #{x['rank']:<2} {x['channel'][:18]:18s} {x['title'][:85]}  {x['url'][-11:]}")
