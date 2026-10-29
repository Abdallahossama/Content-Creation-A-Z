---
name: caption-zone-rule
description: On-screen text/notes must never sit under the burned-in captions; keep them above the caption band or in corners
metadata:
  type: feedback
---

The user noticed captions covering our handwritten notes in Ep 2 (2026-10-12) and asked that text we write is always
placed where captions can't cover it. Caption band = x 420-1500, y 860-1010 on a 1080p frame.

**Why:** a note under a caption is unreadable and looks careless.

**How to apply:** lay out notes/big words/stickers with the bottom row at y <= 800 (corners are free); run the render
engine's `caption_safe()` + `check_caption_zone.py` before any full render (must report 0). Rule is in
`D:\why habibi\_style_kit\STYLE_RULES.md`. See [[no-ai-slop-design]].
