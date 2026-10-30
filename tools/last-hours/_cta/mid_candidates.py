"""List each scheduled file's narration lines between 50 % and 78 % of the voice (index, time, text) to pick the mid-CTA cliffhanger."""
import sys, importlib, json
NC = "D:/why habibi/_newchannel/"
FILES = json.load(open(NC + "_cta/brand_times.json", encoding="utf-8"))
MODS = {"flannan": "render_flannan", "khuld": "render_khuld", "andree": "render_andree", "gaddafi": "render_gaddafi", "flight19": "render_flight19",
        "cyclops": "render_cyclops", "egyptair": "render_egyptair", "goering": "render_goering"}
for key in (sys.argv[1:] or MODS):
    d = FILES[key]["dir"]; sys.path.insert(0, NC + d); sys.argv = [sys.argv[0], "none"]; R = importlib.import_module(MODS[key])
    print(f"=== {key} (VO {R.VO_END:.0f}s, old pill {FILES[key]['subpop_t']:.0f}s)")
    for i, t in enumerate(R.T):
        if 0.5 <= t / R.VO_END <= 0.78: print(f"{i:3d} {t:6.1f} {R.LINES[i][:92]}")
    sys.path.pop(0)
