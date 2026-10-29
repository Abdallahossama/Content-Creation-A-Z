"""vidclip: moving archive footage for the Last Hours renderers.
A clip is decoded through ffmpeg in order (one reader per clip per render process), cover-fit to 1920x1080 and toned like
the stills (lastkit.bw: bone-white mono) or kept in colour, gently. Frames are asked for in order inside a segment, so the
reader only reopens (with -ss) on a jump back or a long jump forward. Past the clip's end it holds the last frame.
No grain, no glitch, no CRT frame (lastkit rules); the source label comes from the renderer's tag().
  clip = Clip(path, src_in=12.0, speed=0.8, crop=(0, 0.1, 1, 0.9), look="bw"); img = clip.at(u)   # u = s into the shot"""
import subprocess, json, numpy as np
from PIL import Image, ImageEnhance

W, H, FPS = 1920, 1080, 30
BONE = np.array([236, 230, 214], np.float32)

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", path], capture_output=True, text=True)
    j = json.loads(r.stdout); s = j["streams"][0]
    return s["width"], s["height"], float(j["format"]["duration"])

class Clip:
    def __init__(self, path, src_in=0.0, speed=1.0, crop=None, look="bw", z0=1.0, z1=1.06, c=(0.5, 0.5), dur=None, grade=None):
        self.grade = grade                                                     # look="grade": the renderer's own photo grade (PIL RGB -> RGB)
        if look == "grade" and grade is None: look = "col"
        self.path, self.src_in, self.speed, self.crop, self.look = path, src_in, speed, crop, look
        self.z0, self.z1, self.c, self.dur = z0, z1, c, dur
        self.sw, self.sh, self.len = probe(path)
        self.p, self.next, self.buf, self.lut = None, 0, None, None
        self.ch = 1 if look == "bw" else 3
        cw, ch = (self.sw, self.sh) if not crop else (self.sw * (crop[2] - crop[0]), self.sh * (crop[3] - crop[1]))
        zm = max(z0, z1) * 1.02; s = max(W * zm / cw, H * zm / ch)      # decode just larger than the push-in needs, so it stays sharp
        self.dw, self.dh = int(cw * s) // 2 * 2, int(ch * s) // 2 * 2

    def _open(self, idx):
        if self.p: self.p.kill(); self.p.wait()
        ss = self.src_in + idx / FPS * self.speed
        vf = []
        if self.crop:
            x0, y0, x1, y1 = self.crop
            vf.append(f"crop=iw*{x1 - x0:.4f}:ih*{y1 - y0:.4f}:iw*{x0:.4f}:ih*{y0:.4f}")
        vf += [f"setpts=PTS/{self.speed}", f"fps={FPS}", f"scale={self.dw}:{self.dh}:flags=bicubic"]
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", self.path, "-an", "-vf", ",".join(vf),
                                   "-f", "rawvideo", "-pix_fmt", "gray" if self.ch == 1 else "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.dw * self.dh * self.ch * 4)
        self.next = idx

    def _read(self):
        n = self.dw * self.dh * self.ch; b = self.p.stdout.read(n)
        if len(b) < n: return self.buf                                          # clip ended: hold the last frame
        return np.frombuffer(b, np.uint8).reshape((self.dh, self.dw) if self.ch == 1 else (self.dh, self.dw, 3))

    def raw(self, u):
        idx = max(0, int(round(u * FPS)))
        if self.p is None or idx < self.next - 1 or idx > self.next + 45: self._open(idx)
        while self.next <= idx:
            self.buf = self._read(); self.next += 1
        return self.buf

    def at(self, u):
        a = self.raw(u)
        if a is None: return Image.new("RGBA", (W, H), (13, 13, 14, 255))
        k = 0.0 if not self.dur else min(max(u / self.dur, 0.0), 1.0)
        z = self.z0 + (self.z1 - self.z0) * k                                # slow push over the shot, like kenburns
        s = max(W / self.dw, H / self.dh) * z; w, h = W / s, H / s
        x0 = min(max(self.c[0] * self.dw - w / 2, 0), self.dw - w); y0 = min(max(self.c[1] * self.dh - h / 2, 0), self.dh - h)
        im = Image.fromarray(a).resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
        if self.lut is None:                                                    # levels fixed from the first frame: no flicker
            if self.ch == 1:
                lo, hi = np.percentile(a[::8, ::8], (0.5, 99.5)); r = np.clip((np.arange(256) - lo) / max(hi - lo, 1.0), 0, 1)
                self.lut = [list((r * v).astype(np.uint8)) for v in BONE]
            else:
                self.lut = [[min(255, int(i * v / 236.0)) for i in range(256)] for v in BONE]
        if self.ch == 1:
            im = Image.merge("RGB", [im.point(l) for l in self.lut])
        elif self.look == "grade":
            im = self.grade(im)
        else:                                                                   # colour footage: a little desaturated, warm white point
            im = ImageEnhance.Color(im).enhance(0.72); im = Image.merge("RGB", [b.point(l) for b, l in zip(im.split(), self.lut)])
        return im.convert("RGBA")

    def close(self):
        if self.p: self.p.kill(); self.p.wait(); self.p = None
