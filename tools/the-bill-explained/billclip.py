"""billclip: stock-video shots for billvid (colour, cover-fit, slow push-in), adapted from The Last Hours' vidclip.
Frames are read in order through one ffmpeg pipe per clip; the reader reopens with -ss only on a jump.
Past the clip's end it holds the last frame. If the clip is shorter than the shot, the renderer slows it down (never below 0.4x).
  c = Clip(path, out=(1920, 1080), src_in=3.0, speed=1.0, crop=None, z0=1.0, z1=1.06, c=(.5, .5), dur=5.2); img = c.at(u)"""
import subprocess, json, numpy as np
from PIL import Image, ImageEnhance

FPS = 30

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", path], capture_output=True, text=True)
    j = json.loads(r.stdout); s = j["streams"][0]
    return s["width"], s["height"], float(j["format"]["duration"])

class Clip:
    def __init__(self, path, out=(1920, 1080), src_in=0.0, speed=1.0, crop=None, z0=1.0, z1=1.06, c=(0.5, 0.5), dur=None):
        self.W, self.H = out
        self.path, self.src_in, self.speed, self.crop = path, src_in, speed, crop
        self.z0, self.z1, self.c, self.dur = z0, z1, c, dur
        self.sw, self.sh, self.len = probe(path)
        self.p, self.next, self.buf = None, 0, None
        cw, ch = (self.sw, self.sh) if not crop else (self.sw * (crop[2] - crop[0]), self.sh * (crop[3] - crop[1]))
        zm = max(z0, z1) * 1.02; s = max(self.W * zm / cw, self.H * zm / ch)
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
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.dw * self.dh * 12)
        self.next = idx

    def _read(self):
        n = self.dw * self.dh * 3; b = self.p.stdout.read(n)
        if len(b) < n: return self.buf
        return np.frombuffer(b, np.uint8).reshape((self.dh, self.dw, 3))

    def at(self, u):
        idx = max(0, int(round(u * FPS)))
        if self.p is None or idx < self.next - 1 or idx > self.next + 45: self._open(idx)
        while self.next <= idx:
            self.buf = self._read(); self.next += 1
        a = self.buf
        if a is None: return Image.new("RGBA", (self.W, self.H), (18, 18, 18, 255))
        k = 0.0 if not self.dur else min(max(u / self.dur, 0.0), 1.0)
        z = self.z0 + (self.z1 - self.z0) * k
        s = max(self.W / self.dw, self.H / self.dh) * z; w, h = min(self.W / s, self.dw), min(self.H / s, self.dh)
        x0 = max(0.0, min(max(self.c[0] * self.dw - w / 2, 0), self.dw - w)); y0 = max(0.0, min(max(self.c[1] * self.dh - h / 2, 0), self.dh - h))
        im = Image.fromarray(a).resize((self.W, self.H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
        im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.05)        # same light grade as the photos
        return im.convert("RGBA")

    def close(self):
        if self.p: self.p.kill(); self.p.wait(); self.p = None
