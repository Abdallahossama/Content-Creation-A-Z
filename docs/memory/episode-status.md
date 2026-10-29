---
name: episode-status
description: "Ask Habibi episode pipeline status and weekly publish slot (Ep 2 schedule pending, Ep 3 planned)"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-14T04:37:37.894Z
---

Weekly slot: Thursdays 4:00 PM US Eastern = 11:00 PM Cairo (from 2026-10-15). NOW 2 long videos a week: Thursday + Sunday, 23:00 Cairo (user, 19 Oct). Scheduled through Sun 1 Nov (Ep 6-9), see [[long-form-plan]].

- Ep 2 "Why Can't You Sleep Without a Video On?": target Thu 2026-10-15. A private upload (WccIJ7cyZmY) has the OLD
  version with captions over notes; the fixed file was re-assembled 2026-10-12. Schedule only after an explicit "yes".
  The user deletes the old private copy themselves.
- Ep 3 "Can You Really Fall Asleep in 2 Minutes?": plan at `D:\why habibi\3rd video\PLAN_ep03.md`, target Thu 2026-10-22.
  Angle: the 96%-of-pilots claim comes from Bud Winter's 1981 book *Relax and Win*, not a study.
  Script v1 at `D:\why habibi\3rd video\script_ep03.md`, approved ("go ahead") 2026-10-12. Built the same day:
  VO 6,205 credits, 62 beats, export `3rd video\export\` (1440p, 7:41, -14 LUFS, upload sheet, 3 thumbnails),
  CapCut project "Ask Habibi Ep3 - 2 minute sleep". Pipeline: `_pipeline\episodes\ep03_two_minute_sleep\`.
  Not uploaded yet; needs the user's review first.
- Ep 4 documentary special "Why Do 2 Tiny Straits Control the World's Oil?" (Hormuz + Houthis/Mayun), built
  2026-10-12 in doc mode (`4th video\`, `_pipeline\episodes\ep04_two_straits\`), 5:46. User: "more than perfect".
  Re-exported the same night: map labels kept out of the caption band, and the audio fixed (whooshes/impacts off the voice,
  music -23 dB under the VO, see [[clean-voice-mix]]). Thumbnails V1 (pick) / V5 flags / V6 flags + effects.
  The user still heard a "whoosh while I speak, stops when I stop" and chose to fix the voice THEMSELVES in CapCut
  ("forget about spending more with ElevenLabs"). CapCut project "Ask Habibi Ep4 - two straits" was created for that
  (`capcut_ep04.py` + `create_project_ep04.py`). Its tracks: scenes, captions, voice as exported, untouched ElevenLabs
  voice (muted), music, SFX. An unused ElevenLabs flow "Ask Habibi Ep 4 - voice isolator" was left with nothing charged.
  The user then found the whoosh was in my limited `vo_timeline.wav`. Fresh render the same night uses the UNTOUCHED
  voice: -21.1 LUFS, no limiter, captions verified in sync (median 0 ms). See [[clean-voice-mix]].
  Proposed
  publish: Tue 2026-10-13 11 PM Cairo (time-sensitive news); needs the user's yes to upload/schedule.
- 2026-10-13: Ep 3 re-mixed from its 3 ElevenLabs MP3s (the old joined WAV was 8-bit = whoosh), no limiter, whoosh SFX
  off the voice, -20.8 LUFS. Re-rendered `3rd video\export\Ask_Habibi_Ep3_1440p.mp4` (7:41); the old one is in
  `_archive\ep03_8bit_voice`.
- Facebook plan (user, 2026-10-13), Thursdays 11 PM Cairo: Ep 4 now, Ep 1 15 Oct, Ep 2 22 Oct, Ep 3 29 Oct. Posted via
  Meta Business Suite. Ep 1 file: `D:\why habibi\export\overthincking ! FINAL.mp4`. Instagram: the user creates it
  themselves later, for Reels.
- 2026-10-13: full-length VERTICAL 1080x1920 versions of Ep 1-4 for FB Reels/TikTok, made with
  `_style_kit/tools/vertical.py` (run by `_pipeline/make_verticals.ps1`). Layout: question header + logo, the full 16:9
  picture at full width, big Rubik captions with a yellow keyword, a blurred dark background. Files:
  `1st video\export_vertical\` and `<ep>\export\vertical\`. Ep 1 crops CapCut's burned captions (bottom 20%) and redraws
  them from final_timeline.srt.
- 2026-10-14: Ep 4 YouTube (KFiy4Rabb9s) A/B test #2 RUNNING (Title and thumbnail, ~2 weeks; test #1 had no data and was
  replaced at the user's request): Trump+MBS + "The 2 Tiny Straits Behind Your Gas Price" / cine_6_STUCK (boss Batata,
  tankers photo) + original title / cine_7b_CHOKEPOINT ($8.44 = AAA California diesel record, 22 Sep 2026, source line added
  to the description) + "Why Gas Got Expensive: 2 Straits on a Map". Check the report before yt-retention.
  Tip: the scratchpad path is past Windows MAX_PATH; uv/python scripts there fail. Put them in the pipeline folder.
  Same day, Ep 1 (i3pZRQq0ukY) got the same kind of test: brain plate + current title / MAP A red lobe + "Your Brain at
  3 AM: 4 Levels of Cringe" / PHOTO D phone + "The Science of 3 AM Cringe Attacks" (logged in ep01 YouTube_package.md).
  Ep 2 (WccIJ7cyZmY, scheduled 15 Oct, file Ask_Habibi_Ep2_1440p.mp4) test saved too: BEDTIME STORY + current title /
  NEW LULLABY + "Why You Fall Asleep to YouTube: 4 Levels" / SPLIT SILENCE + "Why You Need a Video On to Fall Asleep".
  Studio says "Ineligible: video is not public" until it premieres; confirm it shows "Running" after 15 Oct.
  Tip: the scratchpad path is past Windows MAX_PATH; uv/python scripts there fail. Put them in the pipeline folder.
- **Shorts are paused** (user, 2026-10-12: "forget about shorts now, let's focus on long videos"). Don't offer
  or build Shorts until the user brings them back; the Ep 2 Shorts (and their ~470 ElevenLabs credits) are on hold.

**Why:** the user works across many sessions; this is the quickest way to know what is live, pending or planned.
**How to apply:** check this before suggesting dates or next steps; update it when an episode ships. Related:
[[upload-copy-paste-sheet]], [[caption-zone-rule]], [[use-yt-skills-default]].
