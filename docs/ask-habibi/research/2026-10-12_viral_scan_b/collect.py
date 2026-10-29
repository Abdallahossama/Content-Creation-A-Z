"""Public channel listings -> swipe.py input. yt-dlp --flat-playlist on each channel's /videos tab (no login)."""
import json, subprocess, sys
CH = ["braincraft", "SciShowPsych", "besmart", "kurzgesagt", "answerswithjoe", "BrainStuff", "theschooloflifetv", "SproutsSchools", "DoctorMike"]
out = json.load(open("../2026-10-12_viral_scan/collected.json", encoding="utf-8"))
have = {r["channel"] for r in out}
for h in CH:
    p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "150", f"https://www.youtube.com/@{h}/videos"],
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode: print("FAIL", h, p.stderr[-200:]); continue
    j = json.loads(p.stdout); name = j.get("channel") or j.get("uploader") or h
    rows = [{"channel": name, "title": e.get("title"), "views": e.get("view_count") or 0, "url": e.get("url"), "duration": e.get("duration") or 0}
            for e in j.get("entries", []) if e.get("view_count")]
    out += rows; print(f"{name}: {len(rows)} videos")
json.dump(out, open("collected.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("total rows", len(out), "channels", len({r['channel'] for r in out}))
