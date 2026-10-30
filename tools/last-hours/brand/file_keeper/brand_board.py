"""The File Keeper: channel files + the full brand board (owner, 30 Oct 2026: "go ahead with the file keeper, show me the full branding").
Channel files -> channel/: avatar_800.png (noir badge), watermark_150.png (FLAT badge: the noir one is too dark that small),
banner_2560x1440.jpg (title + the noir File Keeper, all text inside YouTube's 1546 x 423 safe area).
Board -> _brand_board.jpg: channel header mock, the 1.5 s stamp / the mid pill / the CASE CLOSED end card on real Flannan frames,
a thumbnail with the corner mark, the pinned-comment signature.
  uv run --no-project --with pillow --with numpy --with soundfile python brand_board.py"""
import sys, os, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
NC = "D:/why habibi/_newchannel/"; sys.path.insert(0, NC); sys.path.insert(0, NC + "_cta")
import lastkit as L
from lastkit import W, H, INK, BONE, RED, STEEL, COND, TYPE, SER
import brand_patch as BP
MK = NC + "brand/file_keeper/"; CH = MK + "channel/"; os.makedirs(CH, exist_ok=True)

def grab(src, t):
    p = MK + "_grab.png"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGBA").resize((W, H))

def channel_files():
    noir = Image.open(MK + "mark_noir_badge.png").convert("RGBA")
    av = Image.new("RGBA", (800, 800), (12, 13, 15, 255)); av.alpha_composite(noir.resize((800, 800), Image.LANCZOS)); av.convert("RGB").save(CH + "avatar_800.png")
    Image.open(MK + "mark_v1_badge.png").convert("RGBA").resize((150, 150), Image.LANCZOS).save(CH + "watermark_150.png")
    bw, bh = 2560, 1440; hero = Image.open(MK + "noir_hero.png").convert("RGB")
    yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32); u = (xx / bw * 0.55 * bw / bh + yy / bh * 0.83)
    light = np.clip(1.1 - np.hypot(xx / bw - 0.25, yy / bh - 0.2) * 1.6, 0, 1) ** 2
    st = (np.sin(u * 2 * np.pi * 7) > 0.35).astype(np.float32) * light
    st = np.asarray(Image.fromarray((st * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18)), np.float32) / 255 * 0.5
    bg = np.zeros((bh, bw, 3), np.float32) + np.array([12, 13, 15]) + st[..., None] * np.array([150, 112, 70])
    ban = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")
    h = hero.resize((900, 900), Image.LANCZOS).convert("RGBA"); a = np.ones((900, 900), np.float32)
    xs = np.linspace(0, 1, 900); a *= np.clip(xs / 0.22, 0, 1)[None, :] * np.clip((1 - xs) / 0.22, 0, 1)[None, :]
    a *= np.clip(np.linspace(0, 1, 900) / 0.15, 0, 1)[:, None] * np.clip((1 - np.linspace(0, 1, 900)) / 0.25, 0, 1)[:, None]
    h.putalpha(Image.fromarray((a * 255).astype(np.uint8))); ban.alpha_composite(h, (1520, 330))                 # the File Keeper, right of centre
    L.text(ban, "THE LAST HOURS", 1060, 640, 150, BONE, COND); L.rule(ban, 700, 1420, 735, 99, 0, width=8)
    L.text(ban, "Famous cases, told hour by hour, from the real files.", 1060, 795, 46, BONE, SER)
    L.text(ban, "WITH THE FILE KEEPER  ·  NEW FILES SUN + MON", 1060, 870, 34, STEEL, TYPE)
    ban.convert("RGB").save(CH + "banner_2560x1440.jpg", quality=92)
    return av, ban

def board():
    av, ban = channel_files()
    R = json.load(open(NC + "_cta/brand_times.json", encoding="utf-8"))["flannan"]; src = R["src"]
    f1 = grab(src, R["brand_t"] + 1.0); f1.alpha_composite(BP.stamp_image(1.0), BP.STAMP_XY)
    f2 = grab(src, R["subpop_t"] + 2.0); f2.alpha_composite(BP.pill_image(2.0, BP.PILL["flannan"]), (0, BP.pill_y("flannan")))
    bgs = grab(src, R["cut_t"] - 0.2).convert("RGB"); bgb = Image.blend(bgs.filter(ImageFilter.GaussianBlur(44)), Image.new("RGB", (W, H), INK), 0.62)
    g = (np.clip((np.arange(H) - 700) / 300, 0, 1) ** 1.2 * 0.85)[:, None, None]; bgb = Image.fromarray((np.asarray(bgb, np.float32) * (1 - g)).astype(np.uint8))
    caps = None
    if os.path.exists(NC + "_cta/so_flannan.json"):
        caps = BP.caption_chunks([(a + 0.7, b + 0.7, w) for a, b, w in json.load(open(NC + "_cta/so_flannan.json", encoding="utf-8"))])
    f3 = BP.end_frame(bgs, bgb, 4.2, BP.NEXT["flannan"], caps)
    th = Image.open(NC + "14_battle_of_alcatraz/export/thumbnails/A_KEY_107_upload.jpg").convert("RGBA").resize((1280, 720))
    fm = Image.open(MK + "mark_noir_folder.png").convert("RGBA").resize((130, 130), Image.LANCZOS); th.alpha_composite(fm, (24, 720 - 130 - 18))
    # the board
    BW = 2400; S = Image.new("RGB", (BW, 2700), (24, 24, 26)); d = ImageDraw.Draw(S)
    def head(y, s): d.text((40, y), s, font=L.font(COND, 54), fill=(236, 230, 214))
    head(30, "THE FILE KEEPER  ·  THE LAST HOURS  ·  FULL BRANDING")
    d.text((40, 100), "Noir set. No first name. The flat badge only where it must read at 48 px (the Studio watermark).", font=L.font(TYPE, 28), fill=STEEL)
    head(170, "1  CHANNEL PAGE: banner + avatar + watermark")
    S.paste(ban.convert("RGB").resize((1600, 900)), (40, 240))
    m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 299, 299), fill=255); S.paste(av.resize((300, 300)).convert("RGB"), (1700, 260), m)
    d.text((1700, 580), "AVATAR (YouTube crops a circle)", font=L.font(TYPE, 24), fill=STEEL)
    wm = Image.open(CH + "watermark_150.png"); S.paste(wm, (1700, 650), wm); d.text((1870, 700), "WATERMARK 150 px\n(flat: reads small)", font=L.font(TYPE, 24), fill=STEEL)
    d.text((40, 1150), "BANNER 2560 x 1440: all text inside the 1546 x 423 safe area (desktop/phone); TV shows the whole picture.", font=L.font(TYPE, 24), fill=STEEL)
    head(1210, "2  INSIDE EVERY LONG FILE (real Flannan frames)")
    for i, (im, cap) in enumerate(((f1, "1.5 s STAMP: mark beside LAST HOURS"), (f2, "~75 % SILENT PILL: SUBSCRIBE · NEXT FILE"),
                                   (f3, "END: CASE CLOSED + NEXT FILE + sign-off"))):
        x = 40 + i * 790; S.paste(im.convert("RGB").resize((760, 428)), (x, 1290)); d.text((x, 1730), cap, font=L.font(TYPE, 24), fill=STEEL)
    head(1810, "3  THUMBNAILS: the case-file mark, bottom-left (clear of the timestamp)")
    S.paste(th.convert("RGB").resize((1067, 600)), (40, 1890))
    head(1810, "")
    d.text((1160, 1890), "4  PINNED COMMENT + REPLIES (signed)", font=L.font(COND, 54), fill=(236, 230, 214))
    msg = ("They had two guns and nine hostages, but never key 107.\nIf they had found it, could they have made it off the Rock?\n"
           "And whose file should I open next? I read every one.\n\n— The File Keeper 🕵\n\nReplies: short, in the same voice, signed\n\"— The File Keeper\". Pin + heart every new video.")
    d.multiline_text((1160, 1980), msg.replace("🕵", ""), font=L.font(SER, 34), fill=(230, 224, 210), spacing=14)
    d.text((1160, 2450), "SPOKEN SIGN-OFF (end of every long file):", font=L.font(TYPE, 24), fill=STEEL)
    d.multiline_text((1160, 2490), "\"I'm the File Keeper. Every week, I open one file the history books\nleft half-told. Next: <the next file>. Subscribe, and it'll be waiting\nfor you. And if this one was worth your time, a like really helps\na small channel get seen.\"", font=L.font(SER, 28), fill=(230, 224, 210), spacing=10)
    S.save(MK + "_brand_board.jpg", quality=90); print(MK + "_brand_board.jpg")

if __name__ == "__main__":
    board()
