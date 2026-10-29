---
name: use-yt-skills-default
description: Always use the installed yt-* skills (github.com/Jakeschincariol/youtube-agent-skill) for Ask Habibi video work
metadata:
  node_type: memory
  type: feedback
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-12T15:30:25.767Z
---

The user wants the YouTube agent skills (github.com/Jakeschincariol/youtube-agent-skill, installed in
`~/.claude/skills/yt-*`) used by default whenever they fit (2026-10-12): /yt-viral (topic), /yt-script (script +
scored hooks via hookscore.py), /yt-edit (pauses), /yt-package (title + thumbnail via title.py), /yt-seo (description),
/yt-chapters, /yt-shorts, /yt-retention + /yt-comment after publishing, /yt-plan, /yt-audit.

**Why:** they make the writing and packaging measurable (scored hooks, linted titles) instead of guesswork.

**How to apply:** invoke the matching skill at each step of the `_pipeline\README.md` workflow, run its Python tool,
show the scores, and end each run with "ship it, or change it?". Voice profile: `~/.claude/youtube/voice.md`.
See [[ask-habibi-capcut-workflow]].
