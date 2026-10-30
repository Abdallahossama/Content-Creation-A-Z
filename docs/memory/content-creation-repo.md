---
name: content-creation-repo
description: Private GitHub repo Abdallahossama/Content-Creation-A-Z = the whole system packaged as a skill; local copy D:\Content-Creation-A-Z; sync with _build\sync.ps1 after each video
metadata:
  node_type: memory
  type: reference
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-30T05:53:25.163Z
---

29 Oct 2026: the owner asked to package everything (rules, playbooks, tools, skills, memories, example files) into a
private repo so another account/session can use it as a skill: https://github.com/Abdallahossama/Content-Creation-A-Z
(private: the public API returns 404). Local clone: `D:\Content-Creation-A-Z\` (SKILL.md entry point, docs/00-08, docs/memory = copies
of these memories, skills/ (yt-* MIT + habibi-video), tools/, examples/). Text and code only, no media.

**Owner, 30 Oct (standing order):** every decision that changes how we edit/brand/upload (agreed or rejected) goes into the
repo skill BY DEFAULT, without asking and without being reminded: "keep it updated by yourself... do your job".
Write it into the right doc (01-OWNER-RULES, 02-LAST-HOURS-PLAYBOOK, 09-BRANDING-AND-CONVERSION...) the same day and push.

**How to apply:** after each video or rule change, update LESSONS.md / memories / docs/08-CURRENT-STATE.md, then run
`_build/stage.py` (copies from the working folders, redacts private emails, refuses secret-like text) and commit + push
(`_build/sync.ps1`). Git on this machine: run git with the sandbox disabled and retry `git add -A` in a loop
(new .git objects hit transient "Permission denied", 46 retries the first time). Push uses the cached Git Credential Manager login.
Related: [[new-channel-last-hours]], [[last-hours-lessons]].
