"""Patch a Last Hours render script (LESSONS rule 19, 23 Oct 2026): inside frame(), every flat INK background becomes
ambient(k) - the nearest photo shot, lightly blurred and dimmed, with a soft dark band so the card text stays readable.
  python no_black_patch.py <render_script.py | part file that holds frame()> [<file that gets the ambient() helper>]"""
import sys, re

HELPER = '''
AMB = {}
def ambient(k):
    """no flat black screens (LESSONS 19): the nearest photo shot, blurred a little and dimmed, sits behind every card"""
    if k not in AMB:
        if len(AMB) > 6: AMB.clear()
        im = None
        for j in list(range(k - 1, -1, -1)) + list(range(k + 1, len(SHOTS))):
            kind_j, a_j = SHOTS[j][1]
            if kind_j in ("kb", "kbp") and a_j.get("rid"):
                src = tone(a_j["rid"], a_j.get("crop")).convert("RGB"); s = max(W / src.width, H / src.height)
                im = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.BICUBIC)
                x0, y0 = (im.width - W) // 2, (im.height - H) // 2
                im = im.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(6))
                im = Image.blend(im, Image.new("RGB", (W, H), INK), 0.52).convert("RGBA"); break
        if im is None: im = Image.new("RGBA", (W, H), INK + (255,))
        band = np.clip(1 - np.abs(np.arange(H) - H / 2) / (H * 0.34), 0, 1)[:, None] * 125
        lay = Image.new("RGBA", (W, H), INK + (0,)); lay.putalpha(Image.fromarray(np.repeat(band, W, 1).astype(np.uint8))); im.alpha_composite(lay)
        AMB[k] = im
    return AMB[k].copy()

'''
INKBG = 'Image.new("RGBA", (W, H), INK + (255,))'

def patch(frame_file, helper_file=None):
    s = open(frame_file, encoding="utf-8").read()
    i = s.index("\ndef frame(t):"); j = s.find("\ndef ", i + 10); j = len(s) if j < 0 else j
    body = s[i:j]; n = body.count(INKBG)
    body = body.replace(INKBG, "ambient(k)")
    s = s[:i] + body + s[j:]
    if helper_file is None or helper_file == frame_file:
        s = s[:i] + "\n" + HELPER + s[i:]
    else:
        h = open(helper_file, encoding="utf-8").read()
        if "def ambient(" not in h: open(helper_file, "w", encoding="utf-8").write(h.rstrip() + "\n" + HELPER)
    open(frame_file, "w", encoding="utf-8").write(s)
    print(frame_file, "flat backgrounds replaced:", n)

if __name__ == "__main__":
    patch(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
