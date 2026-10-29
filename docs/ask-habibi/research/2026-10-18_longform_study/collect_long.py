"""Long-form study 2026-10-18: public YouTube search (this year, 4-20 min) for question-type queries in both Ask Habibi lanes,
then each found channel's public /videos tab (followers + last 30 views). No login.
-> hits.json (every search hit + lane, qtype, channel subs/median, multiple, views per sub) and collected.json (swipe.py input)"""
import json, statistics, concurrent.futures as cf
import yt_dlp
SP = "EgQIBRgD"   # filters: upload date = this year, duration = 4-20 min
Q = {
 "curiosity": {
  "why": ["why do we", "why does your brain", "why do humans", "why can't you", "why do i feel", "why do people"],
  "how": ["how your brain", "how does sleep work", "how your body", "how memory works"],
  "what_happens": ["what happens to your body when", "what happens if you don't sleep", "what happens when you stop", "what happens in your brain when"],
  "real_reason": ["the real reason you", "the real reason why we"],
  "is_x": ["is it bad to", "is it normal to", "is it true that"],
  "what_if": ["what if you never slept", "what if humans"],
  "can_you": ["can you really", "can you train your brain"],
  "psychology_of": ["the psychology of", "psychology behind"],
 },
 "geo_news": {
  "why": ["why does china", "why is russia", "why nobody lives in", "why is this country", "why does america"],
  "how": ["how did a country", "how one country", "how this tiny country", "how a strait"],
  "real_reason": ["the real reason why country"],
  "what_happens": ["what happens if china", "what happens if the strait"],
  "where": ["the country where", "where is the"],
  "is_x": ["is the us", "is china losing"],
  "explained": ["explained on a map", "geopolitics explained map", "geography explained"],
  "who": ["who controls", "who owns"],
 },
}
def search(lane, qt, q):
    o = {"quiet": True, "extract_flat": True, "playlistend": 40, "skip_download": True, "ignoreerrors": True}
    with yt_dlp.YoutubeDL(o) as y:
        j = y.extract_info("https://www.youtube.com/results?search_query=" + q.replace(" ", "+") + "&sp=" + SP, download=False)
    out = []
    for e in (j or {}).get("entries", []) or []:
        if e and e.get("view_count") and e.get("duration") and e.get("channel_id"):
            out.append(dict(id=e["id"], title=e.get("title"), views=e["view_count"], duration=e["duration"], channel=e.get("channel"),
                            channel_id=e["channel_id"], lane=lane, qtype=qt, query=q))
    return out
def chan(cid):
    o = {"quiet": True, "extract_flat": True, "playlistend": 30, "skip_download": True, "ignoreerrors": True}
    try:
        with yt_dlp.YoutubeDL(o) as y: c = y.extract_info("https://www.youtube.com/channel/" + cid + "/videos", download=False)
        vids = [dict(title=e.get("title"), views=e.get("view_count"), url=e.get("url"), duration=e.get("duration") or 0) for e in c.get("entries", []) if e and e.get("view_count")]
        return cid, dict(name=c.get("channel"), subs=c.get("channel_follower_count"), vids=vids)
    except Exception as ex: return cid, None
jobs = [(l, qt, q) for l, d in Q.items() for qt, qs in d.items() for q in qs]
hits = {}
with cf.ThreadPoolExecutor(6) as ex:
    for res in ex.map(lambda a: search(*a), jobs):
        for h in res: hits.setdefault(h["id"], h)
print("search hits", len(hits), flush=True)
cids = sorted({h["channel_id"] for h in hits.values()})
chans = {}
with cf.ThreadPoolExecutor(8) as ex:
    for cid, info in ex.map(chan, cids):
        if info: chans[cid] = info
print("channels", len(chans), flush=True)
rows, collected = [], []
for h in hits.values():
    c = chans.get(h["channel_id"])
    if not c or len(c["vids"]) < 4: continue
    med = statistics.median(v["views"] for v in c["vids"])
    rows.append(dict(h, subs=c["subs"], channel_median=med, multiple=h["views"] / max(med, 1), per_sub=h["views"] / max(c["subs"] or 1, 1)))
for cid, c in chans.items():
    for v in c["vids"]: collected.append(dict(channel=c["name"], title=v["title"], views=v["views"], url=v["url"], duration=v["duration"]))
json.dump(rows, open("hits.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(collected, open("collected.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("rows", len(rows))
