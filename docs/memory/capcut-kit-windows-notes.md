---
name: capcut-kit-windows-notes
description: Gotchas when driving CapCut drafts from this Windows machine (kit at D:\capcut\capcut-kit-main is macOS-only)
metadata:
  node_type: memory
  type: reference
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-12T11:03:59.133Z
---

- D:\capcut\capcut-kit-main\capcut-kit-main\capcut-bridge.py is macOS-only; on Windows edit the draft JSON directly with Python (run via `uv run --no-project python`; the WindowsApps `python` is a Store stub).
- The session scratchpad path is >260 chars → Python file ops fail there; work in the scratch workspace instead.
- Keyframe time_offset is on the SOURCE media timeline (source_timerange.start + offset), not segment-relative.
- Give text segments a real source_timerange (null wedges export, per kit README).
- faster-whisper medium.en is cached; decode audio with ffmpeg to 16 kHz WAV first (PyAV version mismatch breaks direct mp3 input).
- Rubik-Bold lacks the "→" glyph. Related: [[ask-habibi-capcut-workflow]]
