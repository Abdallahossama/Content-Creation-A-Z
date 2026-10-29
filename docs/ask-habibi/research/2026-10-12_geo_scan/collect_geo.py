"""Public channel listings (no login) for geopolitics explainer channels -> swipe.py input, newest first."""
import json, subprocess, sys
CH = ["RealLifeLore", "johnnyharris", "CaspianReport", "Wendoverproductions", "TLDRnewsGLOBAL", "TheInfographicsShow",
      "Vox", "PolyMatter", "visualpolitikEN", "AlJazeeraEnglish"]
out = []
for h in CH:
    p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "120", f"https://www.youtube.com/@{h}/videos"],
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode: print("FAIL", h, p.stderr[-160:]); continue
    j = json.loads(p.stdout); name = j.get("channel") or j.get("uploader") or h
    rows = [{"channel": name, "title": e.get("title"), "views": e.get("view_count") or 0, "url": e.get("url"), "duration": e.get("duration") or 0}
            for e in j.get("entries", []) if e.get("view_count")]
    out += rows; print(f"{name}: {len(rows)} videos", flush=True)
json.dump(out, open("collected_geo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("total", len(out))
