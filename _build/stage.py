"""Stage the Content-Creation-A-Z repo from the live working folders (copies only; originals untouched).
Text and code only: no media, renders, voice files, venvs, logs or anything over 1 MB.
  uv run --no-project python _build/stage.py"""
import os, re, shutil, glob

REPO = "D:/Content-Creation-A-Z/"
MEM = ("C:/Users/ossam/.claude/projects/C--Users-ossam-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-"
       "cbe7bc10-d625-4434-82c4-f8967c032c9f-13580dea-f3a7-4ecb-93ff-59148270826e-scratch-2026-10-12-1ceecf/memory/")
SK = "C:/Users/ossam/.claude/skills/"
WH = "D:/why habibi/"
OK_EXT = {".py", ".md", ".txt", ".json", ".sh", ".ps1", ".bat", ".toml", ".csv", ".srt"}
SKIP_DIRS = {"media", "build", "export", "takes", "__pycache__", "venv", "venv-chatterbox", "venv-qwen", "hf", "uv-cache", "site-packages",
             "node_modules", "_raw", "_orig", "upload", "upload_v2", "out", "bank", "voice", "assets", "blender", "fonts", "mascot", "maps",
             "sfx", "brand", "examples", "_v1_alcatraz_endcard", "_options_v3", "preview", "teasers_media"}
SKIP_NAME = re.compile(r"(\.log$|_backup\.py$|_v1\.py$|^qa_lines\.txt$|^dl\d?\.log$|^gen.*\.err$|^exp_lines\.txt$|^transcribe\d?\.log$)", re.I)
MAX = 1_000_000
copied = []

def want(path):
    n = os.path.basename(path); ext = os.path.splitext(n)[1].lower()
    if ext not in OK_EXT or SKIP_NAME.search(n): return False
    try: return os.path.getsize(path) <= MAX
    except OSError: return False

def tree(src, dst, keep_dirs=None):
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".") and (keep_dirs is None or d in keep_dirs or root != src)]
        for f in files:
            p = os.path.join(root, f)
            if not want(p): continue
            out = os.path.join(dst, os.path.relpath(p, src)); os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy2(p, out); copied.append(out)

def one(src, dst):
    if os.path.isfile(src) and want(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst); copied.append(dst)

# 1. learned rules and preferences (the auto-memory)
tree(MEM, REPO + "docs/memory/")
# 2. skills: the yt-* set (MIT, Jakeschincariol/youtube-agent-skill) + our habibi-video skill + the voice profile
for s in sorted(glob.glob(SK + "yt-*")) + [SK + "habibi-video"]:
    tree(s, REPO + "skills/" + os.path.basename(s) + "/")
one("C:/Users/ossam/.claude/youtube/voice.md", REPO + "skills/youtube-profile/voice.md")
# 3. Ask Habibi: pipeline + style kit (docs + code, no media)
tree(WH + "_pipeline/core", REPO + "tools/pipeline-core/")
tree(WH + "_pipeline/shorts", REPO + "tools/pipeline-shorts/")
tree(WH + "_pipeline/episodes", REPO + "examples/ask-habibi-episodes/")
tree(WH + "_pipeline/research", REPO + "docs/ask-habibi/research/")
one(WH + "_pipeline/README.md", REPO + "docs/ask-habibi/PIPELINE_README.md")
for f in ("README.md", "STYLE_RULES.md", "DOC_MODE.md"): one(WH + "_style_kit/" + f, REPO + "docs/ask-habibi/style_kit_" + f)
tree(WH + "_style_kit/tools", REPO + "tools/style-kit/")
one(WH + "TODO.md", REPO + "docs/ask-habibi/TODO_snapshot.md")
# 4. The Last Hours: shared engine, tools, CTA voice scripts, mystery-Shorts engine, lessons, every episode's text files
NC = WH + "_newchannel/"
for f in ("lastkit.py", "vidclip.py", "thumbs_hakawi.py"): one(NC + f, REPO + "tools/last-hours/" + f)
tree(NC + "_tools", REPO + "tools/last-hours/_tools/")
tree(NC + "_cta", REPO + "tools/last-hours/_cta/")
tree(NC + "brand/file_keeper", REPO + "tools/last-hours/brand/file_keeper/")   # The File Keeper mark (drawn in code, docs/09)
for f in ("mshorts.py", "specs.py", "refix.py"): one(NC + "02_halloween/" + f, REPO + "tools/last-hours/mystery-shorts/" + f)
for f in ("LESSONS.md", "PINNED_COMMENTS.txt"): one(NC + f, REPO + "docs/the-last-hours/" + f)
tree(NC + "research", REPO + "docs/the-last-hours/research/")
for ep in sorted(glob.glob(NC + "[0-9][0-9]_*")):
    name = os.path.basename(ep); dst = REPO + "examples/the-last-hours/" + name + "/"
    for f in glob.glob(ep + "/*"):
        if os.path.isfile(f): one(f, dst + os.path.basename(f))
    for sub in ("research", "vo", "teasers"):
        if os.path.isdir(ep + "/" + sub):
            for f in glob.glob(ep + "/" + sub + "/*"):
                if os.path.isfile(f): one(f, dst + sub + "/" + os.path.basename(f))
    for f in glob.glob(ep + "/export/*.txt") + glob.glob(ep + "/export/*.md"): one(f, dst + "export/" + os.path.basename(f))
    for f in glob.glob(ep + "/teasers/*.txt"): one(f, dst + "teasers/" + os.path.basename(f))
# 5. local AI stack: setup scripts only
for f in ("setup_local_ai.sh", "setup_voice.sh"): one("E:/AskHabibiAI/" + f, REPO + "tools/local-ai/" + f)
# 6. CapCut kit: notes only (third-party, no licence file): the README is linked from the docs, not copied
print(len(copied), "files", round(sum(os.path.getsize(p) for p in copied) / 1048576, 2), "MB")

# 7. redact private email addresses (scraped channel pages) and refuse to stage secrets
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|icloud)\.com", re.I)
SECRET = re.compile(r"xi-api-key|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}|SAPISID|refresh_token|client_secret", re.I)
bad = []
for p in copied:
    try: s = open(p, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError): continue
    s2 = EMAIL.sub("[email removed]", s)
    if s2 != s: open(p, "w", encoding="utf-8").write(s2)
    if SECRET.search(s2): bad.append(p)
if bad:
    raise SystemExit("SECRET-LIKE TEXT FOUND, not staged for commit: " + ", ".join(bad))
print("redaction + secret scan ok")
