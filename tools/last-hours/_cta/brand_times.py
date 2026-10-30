"""Print, per scheduled long file, the timeline facts the brand patch needs (from each file's own render script) and check the uploaded
MP4 has the same length (DUR = VO_END + TAIL). uv run --no-project --with pillow --with numpy --with soundfile python brand_times.py"""
import sys, os, importlib, subprocess, json
NC = "D:/why habibi/_newchannel/"; UQ = "D:/why habibi/_upload_queue_last_hours/"
FILES = {"flannan": ("06_flannan", "render_flannan", UQ + "TheLastHours_05_Flannan_v3.mp4", 128),
         "khuld": ("11_khuld_hall", "render_khuld", UQ + "TheLastHours_10_KhuldHall.mp4", 101),
         "andree": ("08_andree", "render_andree", UQ + "TheLastHours_07_Andree_Balloon_v2.mp4", 128),
         "gaddafi": ("12_gaddafi_stadium", "render_gaddafi", UQ + "TheLastHours_11_GaddafiStadium.mp4", 107),
         "flight19": ("09_flight19", "render_flight19", UQ + "TheLastHours_08_Flight19.mp4", 139),
         "cyclops": ("10_cyclops", "render_cyclops", UQ + "TheLastHours_09_Cyclops.mp4", 89),
         "egyptair": ("07_egyptair", "render_egyptair", UQ + "TheLastHours_06_EgyptAir990_COLOR_v3.mp4", 105),
         "goering": ("13_goering_last_night", "render_goering", NC + "13_goering_last_night/export/TheLastHours_13_GoeringLastNight.mp4", 80)}
MIDLINE = {"flannan": 103, "khuld": 58, "andree": 99, "gaddafi": 57, "flight19": 107, "cyclops": 68, "egyptair": 81, "goering": 53}
# owner 30 Oct: the spoken mid-video ask goes right BEFORE this line (a reveal the viewer is waiting for; never before a death)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 0)
out = {}
for key in (sys.argv[1:] or FILES):
    d, mod, src, cut = FILES[key]; sys.path.insert(0, NC + d); sys.argv = [sys.argv[0], "none"]
    R = importlib.import_module(mod)
    ovt = {k: R.OT(ln, off) for ln, off, k, a in R.OV if k in ("brand", "subpop")}
    rec = dict(src=src, dir=d, cut_line=cut, cut_t=round(R.T[cut], 3), cut_text=R.LINES[cut][:60], brand_t=round(ovt["brand"], 3),
               subpop_t=round(ovt["subpop"], 3), mid_line=MIDLINE[key], mid_t=round(R.T[MIDLINE[key]] - 0.15, 3),
               mid_after=R.LINES[MIDLINE[key] - 1][-70:], mid_before=R.LINES[MIDLINE[key]][:60], vo_end=round(R.VO_END, 3), dur_script=round(R.DUR, 3), dur_mp4=round(dur(src), 3))
    out[key] = rec; print(key, json.dumps(rec), flush=True); sys.path.pop(0)
json.dump(out, open(NC + "_cta/brand_times.json", "w"), indent=1)
