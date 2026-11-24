---
name: speed-clip-edit-style
description: Owner's required edit style for Speed clip Shorts (24 Nov 2026): hype edit for IRL, TikTok karaoke style for GTA; captions must not lag
metadata:
  type: feedback
---
Owner (24 Nov): plain clip edits were "very boring", wants refs: YT Shorts B4Xh4PzRtJM (53M, hype edit) + 7dlo2jQXK6s (Speed backflip) and for GTA clips TikTok @krazydafe/video/7709606773191101702 (475K). Also complained captions were DELAYED.
Tool: F:/speed-gta6/tools/speededit.py job.json (60 fps PIL renderer) + phonk.py (original synthesized phonk beat + boom = no copyright).
- IRL / non-GTA clips = HYPE style: subject-tracking 9:16 crop (srcbox drops Twitch burned captions), warm saturated grade, slow push-in, punch-zoom + shake + green/white flash on scream peaks, 1-3 word Segoe UI Black captions colour-cycling green/white/mint/yellow with glow + pop, hook card first 2 s, phonk bed ducked under speech, whoosh/bass hits, ending = zoom-blur freeze + sepia + 💀 (Segoe UI Emoji) + boom.
- GTA clips = "style":"tt": facecam top 520 px / gameplay 1400 px full-bleed, Arial Bold white captions with black stroke at the seam, current word on purple (124,58,237) rounded box, no music/FX.
- Caption fix: whisper word starts are ~0.3 s late on Speed audio -> snap each word to the real audio onset (8 dB jump), else shift -0.28 s.
**Why:** owner wants the look of million-view clip channels, not plain cuts.
**How to apply:** every Speed clip goes through speededit.py with the matching style; check frames for women (rule) before rendering. Related: [[speed-gta6-clipping]]
