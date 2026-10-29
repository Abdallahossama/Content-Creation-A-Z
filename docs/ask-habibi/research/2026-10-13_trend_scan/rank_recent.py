"""Recent outliers: swipe.py's method (views / that channel's median, long-form only) applied to the newest 15
uploads per channel; formula labels taken from swipe.py's own text output."""
import json, subprocess, sys, statistics, re
SW = r"C:\Users\ossam\.claude\skills\yt-viral\swipe.py"
rows = json.load(open("longform.json", encoding="utf-8")); recent = set(json.load(open("recent.json")))
lane = {r["url"]: r["lane"] for r in json.load(open("collected.json", encoding="utf-8"))}
med = {}
for r in rows: med.setdefault(r["channel"], []).append(r["views"])
med = {k: statistics.median(v) for k, v in med.items() if len(v) >= 4}
txt = subprocess.run([sys.executable, SW, "longform.json", "--min", "1.0"], capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
formula = {}
for i, l in enumerate(txt):
    m = re.match(r"\s+[\d.]+x\s+[\d,]+\s+vs\s+[\d,]+ median\s+(.{22})\s+(.*)$", l)
    if m and i + 1 < len(txt): formula[m.group(2).strip()] = txt[i + 1].strip()
out = []
for r in rows:
    if r["url"] in recent and r["channel"] in med:
        out.append(dict(r, multiple=r["views"] / med[r["channel"]], formula=formula.get(r["title"].strip(), "?")))
json.dump(out, open("recent_ranked.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for ln in ("explainers", "news_maps"):
    print(f"\n=== {ln}: newest 15 per channel, long-form, multiple over channel median ===")
    for x in sorted([x for x in out if lane.get(x["url"]) == ln], key=lambda x: -x["multiple"])[:12]:
        print(f"{x['multiple']:5.1f}x {x['views']:>11,}  {x['channel'][:20]:20s}  {x['title'][:80]}  | {x['formula']}")
