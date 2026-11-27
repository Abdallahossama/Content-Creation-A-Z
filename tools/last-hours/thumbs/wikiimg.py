import json, re, sys, time, urllib.request, urllib.parse, urllib.error
UA = {"User-Agent": "TheLastHoursThumbs/1.0 (thumbnail research) python-urllib"}
def api(**p):
    for k in range(5):
        try: return api0(**p)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(60)
    return api0(**p)
def api0(**p):
    p["format"] = "json"; r = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA)
    return json.load(urllib.request.urlopen(r, timeout=30))
def infobox_file(page):
    wt = api(action="parse", prop="wikitext", section=0, redirects=1, page=page)["parse"]["wikitext"]["*"]
    m = re.search(r"\|\s*(?:image|logo)\s*=\s*(?:\[\[)?(?:File:|Image:)?([^|\]\n]+\.(?:png|jpg|jpeg|svg|webp))", wt, re.I)
    return m.group(1).strip() if m else None
jobs = [l.split("\t") for l in sys.stdin.read().strip().splitlines()]
for name, page in jobs:
    try:
        f = infobox_file(page)
        if not f: print(name, "NOFILE"); continue
        ii = api(action="query", prop="imageinfo", iiprop="url", iiurlwidth=1200, titles="File:" + f)
        info = list(ii["query"]["pages"].values())[0]["imageinfo"][0]; u = info.get("thumburl") or info["url"]
        ext = u.split("?")[0].rsplit(".", 1)[-1]; data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
        open(f"{name}.{ext}", "wb").write(data); print(name, len(data), f)
    except Exception as e: print(name, "ERR", repr(e)[:100])
    time.sleep(20)
