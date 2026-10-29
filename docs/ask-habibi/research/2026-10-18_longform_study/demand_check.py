"""Demand check for candidate long-video topics: public search (this year, 4-20 min), top 15 results."""
import json, statistics as st, concurrent.futures as cf
import yt_dlp
C = {
 "How Did Ancient Humans Sleep?": "how did ancient humans sleep",
 "What Happens To Your Body When You Sleep 4 Hours": "what happens to your body when you sleep 4 hours",
 "The Psychology of People Who Stay Up Late": "psychology of people who stay up late",
 "What Happens To Your Body When You Don't Sleep For 3 Days": "what happens to your body when you don't sleep",
 "The Psychology of People Who Overthink At Night": "psychology of people who overthink",
 "Why Do Humans Need Sleep At All?": "why do humans need sleep",
 "What Happens To Your Body When You Eat Before Bed": "what happens to your body when you eat before bed",
 "Why Did Humans Start Sleeping In Beds?": "why did humans start sleeping in beds",
 "The Psychology of People Who Talk To Themselves": "psychology of people who talk to themselves",
 "What Happens In Your Brain When You Dream": "what happens in your brain when you dream",
 "Why Do We Wake Up At 3 AM?": "why do we wake up at 3am",
 "The Psychology of People Who Sleep With The TV On": "people who sleep with tv on",
}
def run(item):
    title, q = item
    o = {"quiet": True, "extract_flat": True, "playlistend": 15, "skip_download": True, "ignoreerrors": True}
    with yt_dlp.YoutubeDL(o) as y:
        j = y.extract_info("https://www.youtube.com/results?search_query=" + q.replace(" ", "+") + "&sp=EgQIBRgD", download=False)
    es = [e for e in (j or {}).get("entries", []) or [] if e and e.get("view_count")]
    v = sorted([e["view_count"] for e in es], reverse=True)
    return title, dict(n=len(v), top=v[0] if v else 0, median=st.median(v) if v else 0, over100k=sum(1 for x in v if x >= 100000),
                       best=[(e.get("title")[:60], e["view_count"], e.get("channel")) for e in sorted(es, key=lambda e: -e["view_count"])[:2]])
with cf.ThreadPoolExecutor(6) as ex: res = dict(ex.map(run, C.items()))
json.dump(res, open("demand_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t, r in sorted(res.items(), key=lambda kv: -kv[1]["median"]):
    print(f"{r['median']:>10,.0f} median | {r['over100k']:2d}/15 over 100K | top {r['top']:>10,} | {t}")
    for b in r["best"]: print(f"            {b[1]:>10,}  {b[2][:20]:20s}  {b[0]}")
