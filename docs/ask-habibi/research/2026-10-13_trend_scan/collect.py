"""Trend scan 2026-10-13: public channel listings (yt-dlp --flat-playlist, no login) for the two Ask Habibi lanes.
Each channel: up to 120 long-form uploads -> median views; the newest 15 are flagged recent.
-> collected.json (swipe.py input, all rows) + recent.json (urls of the newest 15 per channel)"""
import json, subprocess, sys
LANES = {
    "explainers": ["TED-Ed", "Psych2Go", "MinuteEarth", "DoctorMike", "SciShowPsych", "braincraft", "kurzgesagt",
                   "veritasium", "AsapSCIENCE", "WhatIveLearned", "answerswithjoe", "besmart"],
    "news_maps": ["Vox", "johnnyharris", "TLDRnewsGLOBAL", "CaspianReport", "VisualPolitikEN", "Wendover", "PolyMatter",
                  "aljazeeraenglish"],
}
rows, recent = [], []
for lane, chans in LANES.items():
    for h in chans:
        p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "120",
                            f"https://www.youtube.com/@{h}/videos"], capture_output=True, text=True, encoding="utf-8")
        if p.returncode: print("FAIL", h, p.stderr[-160:].strip()); continue
        j = json.loads(p.stdout); name = j.get("channel") or j.get("uploader") or h
        es = [e for e in j.get("entries", []) if e.get("view_count")]
        for k, e in enumerate(es):
            rows.append({"channel": name, "title": e.get("title"), "views": e["view_count"], "url": e.get("url"),
                         "duration": e.get("duration") or 0, "lane": lane})
            if k < 15: recent.append(e.get("url"))
        print(f"{lane:10s} {name}: {len(es)}")
json.dump(rows, open("collected.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(recent, open("recent.json", "w", encoding="utf-8"))
print("rows", len(rows), "channels", len({r["channel"] for r in rows}))
