"""Build render_capture26.py / render_lastday27.py from 17's render_gaddafi17.py (the File Keeper engine, post-patched: print cards, no text on faces).
Swaps the per-file blocks: docstring, paths, isdoc, tags (TB), lifts, SHOTS + OV (from shots_*.py), brand key, end bg, CAPFIX, music, SFX, name, chapters, ENDL.
  python build_render_saddam.py capture26|lastday27"""
import sys, importlib.util
KEY = sys.argv[1]
SRC = "D:/why habibi/_newchannel/17_gaddafi_last_day/render_gaddafi17.py"
spec = importlib.util.spec_from_file_location("cfg", f"D:/why habibi/_newchannel/_tools/cfg_{KEY}.py"); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
s = open(SRC, encoding="utf-8").read()
def swap(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

swap('"""The Last Hours #17', "import sys, os", C.DOC)
rep('ROOT = "D:/why habibi/_newchannel/17_gaddafi_last_day/"', f'ROOT = "{C.ROOT}"')
rep('ROOT + "vo/gaddafi_vo_chatterbox.wav"', f'ROOT + "vo/{C.VO}"')
rep('ENDL = 60 ', f'ENDL = {C.ENDL} ')
rep('def isdoc(rid): return re.fullmatch(r"A90p\\d+", rid) is not None                     # only the UN verbatim pages stay paper-toned',
    'def isdoc(rid): return re.fullmatch(r"A\\d+p\\d+", rid) is not None or rid in ' + repr(C.DOCS) + '     # document pages stay paper-toned')
swap("CROP = {}", "def KB(rid", C.TBLOCK)
swap("CROPV = {}", "def VID(rid", "CROPV = {}\nLIFT = " + repr(C.LIFT) + "                     # gamma: below 1 lifts the dark clips (LESSONS 34)\n")
swap("SIRTE, DIST2, STRIKE, PIPES", "def OT(ln, off)", open(C.SHOTS, encoding="utf-8").read() + "\n")
rep('BP.LABEL["gaddafi17"]', f'BP.LABEL["{KEY}"]', 2)
rep('BP.NEXT["gaddafi17"]', f'BP.NEXT["{KEY}"]')
rep('sh = tone("A24")', f'sh = tone("{C.ENDBG}")')
swap("CAPFIX = {", "def capfix(i, w):", "CAPFIX = " + repr(C.CAPFIX) + "\n")
swap('    music("Thunder Dreams.mp3", 0.0', "    for i, (key, (kind, a)) in enumerate(SHOTS):", C.MUSIC)
swap("    EV = [", "    EV = [e for e in EV if", "    EV = " + repr(C.EV) + "\n")
rep('name = name or "TheLastHours_17_Gaddafi_LastDay.mp4"', f'name = name or "{C.NAME}"')
swap("CH = [", 'if __name__ == "__main__":', "CH = " + repr(C.CH) + "\n\n")
DST = C.ROOT + f"render_{KEY}.py"
open(DST, "w", encoding="utf-8").write(s); print("wrote", DST, len(s.splitlines()), "lines")
