"""Crop each full-page receipt down to the regions around its key phrases (the full pages are up to 2800x45000 px,
too big to keep in RAM while rendering). Writes build/receipts/<name>__<k>.png + <name>.json with boxes per crop."""
import json, glob, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SRC = "D:/why habibi/3rd video/receipts/"
OUT = "D:/why habibi/3rd video/build/receipts/"
os.makedirs(OUT, exist_ok=True)
for jp in sorted(glob.glob(SRC + "*.json")):
    name = os.path.basename(jp)[:-5]
    J = json.load(open(jp, encoding="utf-8"))
    boxes = [(ph, b) for ph, bl in J["phrases"].items() if bl for b in bl]
    ys = sorted(b[1] for _, b in boxes)
    clusters = []                                     # phrases closer than 3000 px share one crop
    for y in ys:
        if clusters and y - clusters[-1][-1] < 3000: clusters[-1].append(y)
        else: clusters.append([y])
    im = Image.open(SRC + name + ".png").convert("RGB")
    meta = {"crops": []}
    for k, cl in enumerate(clusters):
        y0, y1 = max(0, cl[0] - 1100), min(im.height, cl[-1] + 1300)
        im.crop((0, y0, im.width, y1)).save(OUT + f"{name}__{k}.png")
        ph = {}
        for p, b in boxes:
            if y0 <= b[1] < y1: ph.setdefault(p, []).append([b[0], b[1] - y0, b[2], b[3] - y0])
        meta["crops"].append({"file": f"{name}__{k}.png", "y0": y0, "size": [im.width, y1 - y0], "phrases": ph})
    json.dump(meta, open(OUT + name + ".json", "w", encoding="utf-8"), indent=1)
    print(name, im.size, "->", [(c["file"], c["size"][1]) for c in meta["crops"]])
    im.close()
