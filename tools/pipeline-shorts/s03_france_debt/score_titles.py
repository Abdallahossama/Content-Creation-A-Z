import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/yt-package"))
from title import check
for r in sorted((check(t, None) for t in open(sys.argv[1], encoding="utf-8").read().splitlines() if t.strip()), key=lambda r: -r["score"]):
    print(f'{r["score"]:3} {r["chars"]:2}ch  {r["title"]}' + "".join(f"\n        x {k}: {m}" for k, m in r["issues"]))
