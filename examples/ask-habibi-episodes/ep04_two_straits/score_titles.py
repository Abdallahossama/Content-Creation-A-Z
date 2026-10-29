import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/yt-package"))
from title import check
ts = [l for l in open(sys.argv[1], encoding="utf-8").read().splitlines() if l.strip()]
for thumb in ("CLOSED TAKEN",):
    rows = sorted((check(t, thumb) for t in ts), key=lambda r: -r["score"])
    for r in rows:
        print(f'{r["score"]:3}  {r["chars"]:2}ch  {r["title"]}')
        for k, m in r["issues"]: print(f"          x {k}: {m}")
