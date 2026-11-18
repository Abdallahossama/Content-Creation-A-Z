"""Write export/captions_en.srt from the same caption chunks the render uses (word-timed, CAPFIX applied).
  python make_srt.py <video_root>   (runs <root>/spec.py's setup without rendering)"""
import sys, importlib.util, os
root = sys.argv[1].rstrip("/") + "/"
sys.argv = [root + "spec.py", "none"]
spec = importlib.util.spec_from_file_location("spec", root + "spec.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import stickvid as BV
BV.setup(dict(vars(m), __file__=root + "spec.py")); caps = BV._caps()
def ts(t): h, r = divmod(max(t, 0), 3600); mi, s = divmod(r, 60); return f"{int(h):02d}:{int(mi):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
out = []
for i, (s, e, txt) in enumerate(caps):
    e = min(e, caps[i + 1][0]) if i + 1 < len(caps) else e
    out.append(f"{i + 1}\n{ts(s)} --> {ts(e)}\n{txt}\n")
os.makedirs(root + "export", exist_ok=True); open(root + "export/captions_en.srt", "w", encoding="utf-8").write("\n".join(out)); print(len(caps), "cues")
