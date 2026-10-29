"""Daily-Shorts scan 2026-10-18: public /shorts tab listings (yt-dlp --flat-playlist, no login) for both Ask Habibi lanes.
Per channel: up to 80 newest Shorts -> median; the newest 20 are 'recent' (~last 1-3 weeks).
-> collected.json (swipe.py input) + recent.json"""
import json, subprocess, sys
LANES = {
    "curiosity": ["zackdfilms", "InstituteofHumanAnatomy", "DoctorMike", "AsapSCIENCE", "SciShow", "TEDEd", "Psych2Go",
                  "braincraft", "veritasium", "TheInfographicsShow", "MinuteEarth", "WhatIveLearned"],
    "news_maps": ["RealLifeLore", "johnnyharris", "Vox", "TLDRnewsGLOBAL", "CaspianReport", "VisualPolitikEN", "PolyMatter",
                  "geoglobetales", "Wendover", "aljazeeraenglish", "CNBC", "BBCNews"],
}
rows, recent = [], []
for lane, chans in LANES.items():
    for h in chans:
        p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "80",
                            f"https://www.youtube.com/@{h}/shorts"], capture_output=True, text=True, encoding="utf-8")
        if p.returncode: print("FAIL", h, p.stderr[-160:].strip(), flush=True); continue
        j = json.loads(p.stdout); name = j.get("channel") or j.get("uploader") or h
        es = [e for e in j.get("entries", []) if e.get("view_count")]
        for k, e in enumerate(es):
            rows.append({"channel": name, "title": e.get("title"), "views": e["view_count"], "url": e.get("url"),
                         "duration": e.get("duration") or 45, "lane": lane, "rank": k})
            if k < 20: recent.append(e.get("url"))
        print(f"{lane:10s} {name}: {len(es)}", flush=True)
json.dump(rows, open("collected.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(recent, open("recent.json", "w", encoding="utf-8"))
print("rows", len(rows), "channels", len({r["channel"] for r in rows}))
