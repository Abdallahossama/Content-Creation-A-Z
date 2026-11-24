"""motion: confirm 'crazy' candidates by facecam movement (Speed jumping, running out of frame).
For each candidate: grab 24 s of 240p video around the peak (sidx range fetch), measure mean absolute
frame difference inside the facecam box. Writes motion + combined rank.
  python motion.py <crazy.json> <out.json> [top=30]
needs <vid>.low.urls (yt-dlp --js-runtimes node -g -f "bv*[height<=240][ext=mp4]+ba[ext=m4a]") in cwd."""
import sys, json, subprocess, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FACE = {"OIeLbmyraRQ": (0, .40, .24, .30), "izXcd-bU72k": (0, .34, .25, .32), "qSyo5d-dVzA": (0, .34, .25, .40), "hwSg39yIBGU": (0, .34, .25, .40)}
cands = json.load(open(sys.argv[1])); top = int(sys.argv[3]) if len(sys.argv) > 3 else 30
src_grab = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grab.py"), encoding="utf-8").read().split("urls = [l.strip()")[0]
G = {}; exec(src_grab, G)
out = []
for c in cands[:top]:
    vid, t = c["vid"], c["t"]; urls = [l.strip() for l in open(f"{vid}.low.urls") if l.strip()]
    tmp = f"_m_{vid}_{int(t)}.mp4"
    try:
        G["cut"](urls[0], t - 12, t + 12, tmp)
        fx, fy, fw, fh = FACE.get(vid, (0, .34, .25, .36))
        p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", tmp, "-vf", f"fps=6,crop=iw*{fw}:ih*{fh}:iw*{fx}:ih*{fy},scale=64:48,format=gray", "-f", "rawvideo", "-"], capture_output=True)
        fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, 48, 64).astype(np.float32)
        d = np.abs(np.diff(fr, axis=0)).mean((1, 2)) if len(fr) > 1 else np.zeros(1)
        mot = float(np.percentile(d, 90))
    except (Exception, SystemExit) as e:
        mot = 0.0; print("skip", vid, t, e)
    finally:
        if os.path.exists(tmp): os.remove(tmp)
    c = dict(c, motion=round(mot, 2)); out.append(c)
    print(f"{vid} {int(t // 3600)}:{int(t % 3600 // 60):02d}:{int(t % 60):02d} scream {c['score']:6.1f} motion {mot:5.1f}", flush=True)
ms = np.array([o["motion"] for o in out]); ss = np.array([o["score"] for o in out])
z = lambda a: (a - a.mean()) / (a.std() + 1e-6)
for o, r in zip(out, z(ss) + 1.3 * z(ms)): o["rank"] = round(float(r), 2)
out.sort(key=lambda o: -o["rank"]); json.dump(out, open(sys.argv[2], "w"), indent=1)
print("\nTOP"); [print(o["vid"], o["t"], o["rank"], o["score"], o["motion"]) for o in out[:15]]
