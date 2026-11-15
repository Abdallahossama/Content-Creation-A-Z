---
name: uv-after-disk-cleanup
description: "Owner's C: cleanups break uv (managed Pythons + half-deleted cache envs); how to repair fast"
metadata:
  node_type: memory
  type: reference
  originSessionId: a5a6ba92-8a89-4ec5-a2f2-29545669dedf
  modified: 2026-11-06T14:13:02.598Z
---

6 Nov 2026: after the owner freed C:, `uv run --with pillow --with numpy --with soundfile` gave "No module named numpy" and renders also died with MemoryError while C: was full (page file can't grow; renders leave SHORT files).
Fix: `uv python install 3.12 3.11 --reinstall`; then `uv run -v ...` shows the cached env path (under AppData\Local\Packages\Claude_*\LocalCache\Local\uv\cache\archive-v0\<id>, the Claude app's virtualized LocalAppData); delete only that half-empty folder and rerun. Fallback python with numpy/Pillow/soundfile: E:\AskHabibiAI\venv-chatterbox\Scripts\python.exe.
Related: [[disk-space-cleanup]], [[local-ai-stack]].
