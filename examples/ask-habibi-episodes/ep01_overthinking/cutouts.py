from rembg import remove, new_session
from PIL import Image, ImageOps
S = "D:/why habibi/1st video/claude_package/stock/"
sess = new_session("u2net")
def cut(src, dst, crop=None, gray=False):
    im = Image.open(S + src).convert("RGB")
    if crop: im = im.crop(crop)
    if gray:
        g = ImageOps.grayscale(im); im = Image.merge("RGB", (g, g, g))
    out = remove(im, session=sess, post_process_mask=True)
    bb = out.getbbox(); out = out.crop(bb); out.save(S + dst); print(dst, out.size)
cut("pexels-15410078.jpg", "cut_brain.png", crop=(500, 150, 1450, 900))
sg = Image.open(S + "inhaling_seagull_imgflip.jpg"); w, h = sg.size
cut("inhaling_seagull_imgflip.jpg", "cut_seagull.png", crop=(0, int(h * 0.755), w, h), gray=True)
cut("pexels-8276884.jpg", "cut_hands_face.png")
cut("pexels-3779453.jpg", "cut_shocked.png")
