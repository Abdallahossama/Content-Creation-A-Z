"""Wide demand check (non-sleep): public search, this year, 4-20 min, top 15 results per topic."""
import json, statistics as st, concurrent.futures as cf
import yt_dlp
C = {
 # body / food
 "body: what happens if you eat only once a day": "what happens if you eat only once a day",
 "body: what happens to your body when you stop eating sugar": "what happens when you stop eating sugar",
 "body: what happens when you drink only water": "what happens when you drink only water",
 "body: what coffee does to your body": "what coffee does to your body",
 "body: what happens to your body when you walk every day": "what happens when you walk every day",
 "body: why humans are so weak compared to animals": "why are humans so weak",
 "body: what happens to your body after you die": "what happens to your body after you die",
 "body: what happens to your body in a cold shower": "what happens to your body cold shower",
 # brain / psychology
 "psych: the psychology of people who don't use social media": "psychology of people who don't use social media",
 "psych: the psychology of people who walk fast": "psychology of people who walk fast",
 "psych: why you remember useless things": "why do we remember useless things",
 "psych: why your brain loves bad news": "why your brain loves bad news",
 "psych: the psychology of lonely people": "psychology of lonely people",
 "psych: why you procrastinate": "why do we procrastinate",
 "psych: what deja vu really is": "what is deja vu",
 "psych: why time feels faster as you get older": "why time goes faster as you get older",
 # history of everyday life
 "hist: what did ancient humans do for fun": "what did ancient humans do for fun",
 "hist: why did humans start wearing clothes": "why did humans start wearing clothes",
 "hist: how did people brush their teeth before toothpaste": "how did people brush teeth before toothbrush",
 "hist: what ancient humans ate": "what did ancient humans eat",
 "hist: how did people tell time before clocks": "how did people tell time before clocks",
 "hist: why do we shake hands": "why do we shake hands",
 # money / modern life
 "money: why is everything so expensive": "why is everything so expensive",
 "money: how supermarkets trick you": "how supermarkets trick you",
 "money: why prices end in 99": "why prices end in 99",
 "money: how casinos make money": "how casinos make money",
 "money: why your phone is designed to be addictive": "why is your phone so addictive",
 # animals / nature / space
 "animal: why do cats": "why do cats",
 "animal: what dogs actually see": "what do dogs see",
 "space: what if the sun disappeared": "what if the sun disappeared",
 "space: what's at the bottom of the ocean": "what is at the bottom of the ocean",
 "space: why can't we go back to the moon": "why haven't we gone back to the moon",
 # geography / countries (long-form)
 "geo: how did tokyo become the largest city": "how did tokyo become the largest city",
 "geo: why nobody lives in": "why nobody lives in",
 "geo: how a tiny country got so rich": "how did a tiny country get so rich",
 "geo: the country with no": "the country with no",
 "geo: why does this country drive on the left": "why do some countries drive on the left",
 # morbid / weird
 "weird: what happens if you fall into a black hole": "what happens if you fall into a black hole",
 "weird: what happens if you get lost at sea": "what happens if you get lost at sea",
 "weird: why do we have fingerprints": "why do we have fingerprints",
}
def run(item):
    k, q = item
    o = {"quiet": True, "extract_flat": True, "playlistend": 15, "skip_download": True, "ignoreerrors": True}
    try:
        with yt_dlp.YoutubeDL(o) as y:
            j = y.extract_info("https://www.youtube.com/results?search_query=" + q.replace(" ", "+") + "&sp=EgQIBRgD", download=False)
    except Exception: return k, None
    es = [e for e in (j or {}).get("entries", []) or [] if e and e.get("view_count")]
    v = sorted([e["view_count"] for e in es], reverse=True)
    return k, dict(n=len(v), median=st.median(v) if v else 0, over100k=sum(1 for x in v if x >= 100000), top=v[0] if v else 0,
                   best=[(e.get("title")[:70], e["view_count"], e.get("channel")) for e in sorted(es, key=lambda e: -e["view_count"])[:2]])
with cf.ThreadPoolExecutor(6) as ex: res = {k: r for k, r in ex.map(run, C.items()) if r}
json.dump(res, open("demand_wide.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, r in sorted(res.items(), key=lambda kv: (-kv[1]["over100k"], -kv[1]["median"])):
    print(f"{r['over100k']:2d}/15 >100K  median {r['median']:>9,.0f}  top {r['top']:>10,}  | {k}")
    print(f"        best: {r['best'][0][1]:>10,} {r['best'][0][2][:18]:18s} {r['best'][0][0]}" if r["best"] else "")
