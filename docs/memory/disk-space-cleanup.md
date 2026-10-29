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

**Why:** the user wanted the space; permanent deletion is the user's own action, so a move to one clearly named folder frees D: without me deleting.
**How to apply:** never move `_style_kit`, `_music_library`, `_pipeline` or `E:\AskHabibiAI` (Chatterbox voice); The Last Hours scripts import them.
Watch D: before big renders (the Saddam v2 master alone was 2.6 GB). Old Last Hours upload-queue versions (v1/v2 of re-uploaded files) are the next
candidates if space runs low again; ask first. Related: [[focus-last-hours]], [[local-ai-stack]].
