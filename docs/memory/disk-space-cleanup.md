---
name: disk-space-cleanup
description: "25 Oct 2026 D: was full (1.9 GB); old Ask Habibi media moved to an E: \"delete me\" folder; what must never be moved"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-25T08:39:42.810Z
---

25 Oct 2026: D: (why habibi) had 1.9 GB free; user asked "free space and delete unneeded old stuff related to ask habibi".
I moved 36 GB of Ask Habibi videos, frame sequences and WAVs (episode folders, shorts/, _upload_queue_ask_habibi, Ask Habibi parts of _archive)
to `E:\why habibi OLD ask habibi (delete me)\` with `_pipeline/move_ask_habibi_media.py` (same relative paths, hard links kept). D: went to 38 GB free.
The user deletes that E: folder; I don't hard-delete.
30 Oct 2026: user "I will stop making content for Ask Habibi, only The Last Hours": the last Ask Habibi-only folders (episodes 1-10,
shorts, packs, logo, _cta_library, _draft_backups, _media, _thumbs_v2, _upload_queue_ask_habibi; 1.6 GB) moved to
`D:\why habibi\_ASK_HABIBI_ARCHIVE (delete me)\`. Left in D:\why habibi: _newchannel, _upload_queue_last_hours, _music_library,
_style_kit, _pipeline (mshorts BANK = _pipeline/shorts/bank), _archive, TODO.md. CapCut's Ask Habibi drafts (246 MB) and cache (2.2 GB)
stay on C: (C: had 2.1 GB free): the user clears the cache in CapCut.

**Why:** the user wanted the space; permanent deletion is the user's own action, so a move to one clearly named folder frees D: without me deleting.
**How to apply:** never move `_style_kit`, `_music_library`, `_pipeline` or `E:\AskHabibiAI` (Chatterbox voice); The Last Hours scripts import them.
Watch D: before big renders (the Saddam v2 master alone was 2.6 GB). Old Last Hours upload-queue versions (v1/v2 of re-uploaded files) are the next
candidates if space runs low again; ask first. Related: [[focus-last-hours]], [[local-ai-stack]].

C: fills fast (0 MB free on 6 and 8 Nov). Main culprits: other sessions' scratchpads in %TEMP%\claude\*\*\scratchpad (8 Nov: ~7 GB of throwaway edge-profile-* browser profiles), uv/npm caches, CapCut User Data\Cache. Safe routine: delete scratchpad edge-profile-* not touched in 60 min, %TEMP% items older than 6 h (skip %TEMP%\claude), `npm cache clean --force`, `uv cache clean` (then see [[uv-after-disk-cleanup]]). Use Bash rm; PowerShell Remove-Item on these paths is blocked.
