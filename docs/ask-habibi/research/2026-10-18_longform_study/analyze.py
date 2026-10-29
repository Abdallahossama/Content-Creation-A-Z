"""Long-form study analysis: question types x lanes, small channels (<100k subs), breakout = multiple over channel median."""
import json, statistics as st, collections
rows = [r for r in json.load(open("hits.json", encoding="utf-8")) if r["duration"] >= 240]
small = [r for r in rows if r["subs"] and r["subs"] < 100000]
print(f"long-form hits: {len(rows)}  small-channel (<100k subs): {len(small)}  channels: {len({r['channel_id'] for r in small})}")
def summ(rs):
    if not rs: return "-"
    m = [r["multiple"] for r in rs]; ps = [r["per_sub"] for r in rs]
    hit = sum(1 for x in m if x >= 3) / len(m)
    return f"n={len(rs):3d}  median multiple {st.median(m):5.2f}x  breakout rate (>=3x) {hit*100:4.0f}%  median views/sub {st.median(ps):5.2f}"
for lane in ("curiosity", "geo_news"):
    print(f"\n=== {lane}: question types, small channels ===")
    by = collections.defaultdict(list)
    for r in small:
        if r["lane"] == lane: by[r["qtype"]].append(r)
    for qt, rs in sorted(by.items(), key=lambda kv: -st.median([r["multiple"] for r in kv[1]])):
        print(f"  {qt:14s} {summ(rs)}")
# length buckets
print("\n=== length (small channels, both lanes) ===")
for lo, hi in ((240, 480), (480, 720), (720, 1200)):
    rs = [r for r in small if lo <= r["duration"] < hi]; print(f"  {lo//60}-{hi//60} min  {summ(rs)}")
# subscriber buckets
print("\n=== channel size ===")
for lo, hi in ((0, 1000), (1000, 10000), (10000, 100000)):
    rs = [r for r in small if lo <= r["subs"] < hi]; print(f"  {lo:>6}-{hi:<6} subs  {summ(rs)}")
print("\n=== top breakouts, small channels (multiple >= 3x, views >= 20k) ===")
top = sorted([r for r in small if r["multiple"] >= 3 and r["views"] >= 20000], key=lambda r: -r["multiple"])
for r in top[:40]:
    print(f"{r['multiple']:6.1f}x {r['views']:>9,} views  {r['subs']:>7,} subs  {r['duration']//60:2d}m  {r['lane'][:4]} {r['qtype']:12s} | {r['channel'][:22]:22s} | {r['title'][:90]}")
json.dump(top, open("top_breakouts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
