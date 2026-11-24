p = 'F:/speed-gta6/tools/speededit.py'; s = open(p, encoding='utf-8').read()
s = s.replace('FB, FBI, EMO = F + "seguibl.ttf", F + "seguibli.ttf", F + "seguiemj.ttf"',
              'FB, FBI, EMO = F + "seguibl.ttf", F + "seguibli.ttf", F + "seguiemj.ttf"\nMX, MXB = "F:/speed-gta6/fonts/Montserrat-ExtraBold.ttf", "F:/speed-gta6/fonts/Montserrat-Black.ttf"')
s = s.replace('END = 0.0 if TT else 1.6; TOTAL = L + END; NF = int(TOTAL * FPS)',
              'END = job.get("outro_len", 2.6); TOTAL = L + END; NF = int(TOTAL * FPS)\nCAPSTYLE = job.get("caps", "frayzz" if TT else "pop")')

old = 'def draw_text(c, t):\n    if TT: return tt_caps(c, t)'
new = '''FZ_PAL = [(57, 255, 57), (255, 52, 52), (255, 214, 0), (0, 229, 255), (255, 80, 220)]
def spaced(d, x, y, txt, f, fill, track):
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    return x
def spaced_w(txt, f, track):
    d = ImageDraw.Draw(Image.new("L", (1, 1))); return sum(d.textlength(ch, font=f) + track for ch in txt) - track
FZ = []
cur = []
for w in words:
    if cur and (len(cur) >= 6 or w["s"] - cur[-1]["e"] > 0.45): FZ.append(cur); cur = []
    cur.append(w)
    if w["w"].endswith((".", "!", "?")): FZ.append(cur); cur = []
if cur: FZ.append(cur)
def fz_caps(c, t, y_mid):
    for k, p in enumerate(FZ):
        s0 = p[0]["s"]; e0 = (FZ[k + 1][0]["s"] if k + 1 < len(FZ) else p[-1]["e"] + 0.5); e0 = min(e0, p[-1]["e"] + 0.7)
        if not (s0 <= t < e0): continue
        ws = [x["w"].strip(",") for x in p]
        key = next((j for j, x in enumerate(ws) if HYPE.match(x)), max(range(len(ws)), key=lambda j: len(ws[j].strip("?!."))))
        col = FZ_PAL[k % len(FZ_PAL)]
        lines, ln = [], []
        for j, w in enumerate(ws):
            if ln and len(" ".join(ws[i] for i in ln + [j])) > 16: lines.append(ln); ln = []
            ln.append(j)
        if ln: lines.append(ln)
        f = font(MX, 66); tr = 5; lh = 84
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d, g = ImageDraw.Draw(lay), ImageDraw.Draw(glow)
        y = y_mid - lh * len(lines) / 2
        for ln in lines:
            full = " ".join(ws[j] for j in ln); x = W / 2 - spaced_w(full, f, tr) / 2
            for j in ln:
                if p[j]["s"] <= t:
                    fill = col if j == key else (255, 255, 255)
                    g.text((x, y + 4), ws[j], font=f, fill=(0, 0, 0, 200))
                    if j == key: g.text((x, y), ws[j], font=f, fill=col + (255,))
                    spaced(d, x, y, ws[j], f, fill + (255,), tr)
                x += spaced_w(ws[j] + " ", f, tr) + tr
            y += lh
        c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9))); c.alpha_composite(lay); return

def draw_text(c, t):
    if CAPSTYLE == "frayzz": return fz_caps(c, t, job.get("top_h", 520) if TT else int(H * job.get("cap_y", 0.55)))
    if TT: return tt_caps(c, t)'''
assert old in s; s = s.replace(old, new)

i = s.index('SKULL = None'); j = s.index('# ---------------------------------------------------------------- render video')
outro = '''def emoji_img(ch, size):
    f = font(EMO, size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t_, r, b = d.textbbox((0, 0), ch, font=f, embedded_color=True); pad = 30
    im = Image.new("RGBA", (r - l + 2 * pad, b - t_ + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t_), ch, font=f, embedded_color=True); return im
_OUT = {}
def outro_layers():
    if _OUT: return _OUT
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.45) / 0.6, 0, 1) ** 1.4
    vig = np.zeros((H, W, 4), np.uint8); vig[..., 0] = 235; vig[..., 1] = 60; vig[..., 2] = 20; vig[..., 3] = (a * 190).astype(np.uint8)
    _OUT["vig"] = Image.fromarray(vig, "RGBA")
    txt = job.get("outro", "*BRO REALLY DID THAT*").upper(); f = font(MXB, 66); tr = 4
    lines, ln = [], ""
    for w in txt.split():
        if ln and len(ln + " " + w) > 18: lines.append(ln); ln = w
        else: ln = (ln + " " + w).strip()
    lines.append(ln)
    lay = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); glow = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    for k, l2 in enumerate(lines):
        x = W / 2 - spaced_w(l2, f, tr) / 2; y = 20 + k * 82
        ImageDraw.Draw(glow).text((x, y), l2, font=f, fill=(255, 40, 20, 255))
        spaced(ImageDraw.Draw(lay), x, y, l2, f, (255, 38, 38, 255), tr)
    g = glow.filter(ImageFilter.GaussianBlur(16)); g.alpha_composite(lay); _OUT["txt"] = g; _OUT["nl"] = len(lines)
    _OUT["emo"] = emoji_img(job.get("emoji", "\\U0001F602"), 150)
    return _OUT
def ring_pos():
    if job.get("ring") is not None: return job["ring"]
    if TT: return (W // 2, job.get("top_h", 520) // 2, 230)
    return None
def ending(last, u):
    o = outro_layers()
    if u < 0.35:
        c = zoom_blur(last.convert("RGB"), 0.25 * ease(u / 0.35))
    else:
        z = 1.0 + 0.04 * ease((u - 0.35) / (END - 0.35)); im = last.convert("RGB")
        c = im.resize((int(W * z), int(H * z)), Image.BICUBIC).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
        if u < 0.5: c = zoom_blur(c, 0.25 * (1 - ease((u - 0.35) / 0.15)))
    c = grade(c, warm=1.3).convert("RGBA")
    if u >= 0.35:
        k = ease((u - 0.35) / 0.25); v = o["vig"].copy(); v.putalpha(Image.eval(v.getchannel("A"), lambda a: int(a * k))); c.alpha_composite(v)
        rp = ring_pos()
        if rp and u > 0.4:
            x, y, r = rp; rr = r * (1.25 - 0.25 * ease((u - 0.4) / 0.2))
            gl = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((x - rr, y - rr, x + rr, y + rr), outline=(57, 255, 57, 255), width=22)
            c.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10))); ImageDraw.Draw(c).ellipse((x - rr, y - rr, x + rr, y + rr), outline=(70, 255, 70, 255), width=10)
        ty = int(H * job.get("outro_y", 0.36))
        if u > 0.45:
            a = ease((u - 0.45) / 0.15); tx = o["txt"].copy(); tx.putalpha(Image.eval(tx.getchannel("A"), lambda v2: int(v2 * a))); c.alpha_composite(tx, (0, ty - 40))
        if u > 0.6:
            d2 = u - 0.6; s = 0.4 + 0.75 * ease(d2 / 0.12) - 0.15 * ease((d2 - 0.12) / 0.1); e = o["emo"]
            e2 = e.resize((max(1, int(e.width * s)), max(1, int(e.height * s))), Image.BICUBIC)
            c.alpha_composite(e2, (W // 2 - e2.width // 2, ty + 20 + 82 * o["nl"]))
    return c

'''
s = s[:i] + outro + s[j:]
s = s.replace('if not TT: mix[: len(m)] += (m * lvl)[:, None]', 'if job.get("music", True): mix[: len(m)] += (m * lvl)[:, None]')
s = s.replace('m = phonk.beat(TOTAL + 1, job.get("bpm", 140), job.get("seed", 1))[: int(L * SR)]', 'm = phonk.beat(TOTAL + 1, job.get("bpm", 140), job.get("seed", 1))[: int(TOTAL * SR)]')
s = s.replace('env_s = np.interp(np.arange(len(m)) / SR, np.arange(nfr) / 100, np.clip((sm - (base - 3)) / 15, 0, 1))',
              'env_s = np.interp(np.arange(len(m)) / SR, np.arange(nfr) / 100, np.clip((sm - (base - 3)) / 15, 0, 1), right=0.0)')
s = s.replace('lvl = np.where(np.arange(len(m)) / SR < drop, 0.035, 0.085) * (1 - 0.55 * env_s)',
              'tt_ = np.arange(len(m)) / SR; lvl = np.where(tt_ < drop, 0.045, 0.085) * (1 - 0.55 * env_s); lvl = np.where(tt_ >= L, 0.11, lvl)')
s = s.replace('if not TT: bm = phonk.boom(); i = int(L * SR); n = min(len(bm), N - i); mix[i:i + n] += (bm[:n] * 0.6)[:, None]',
              'bm = phonk.boom(); i = int((L + 0.35) * SR); n = min(len(bm), N - i); mix[i:i + n] += (bm[:n] * 0.45)[:, None]')
open(p, 'w', encoding='utf-8').write(s); print('patched')
