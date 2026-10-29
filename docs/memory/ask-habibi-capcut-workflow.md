---
name: ask-habibi-capcut-workflow
description: "User's \"Ask Habibi / Why Habibi?\" YouTube explainer workflow in CapCut desktop (Windows) — paths, caption style, brand pack, meme source"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-12T15:30:29.298Z
---

User edits "Ask Habibi" explainer videos (meme-heavy + some pro graphics) in CapCut desktop 9.5 on Windows.
- Drafts: %LOCALAPPDATA%/CapCut/User Data/Projects/com.lveditor.draft/<name>/ (plain JSON; also mirrored in Timelines/<id>/draft_content.json and template-2.tmp). CapCut must be fully closed before writing; ask the user to close it.
- Look + brand (default from Ep 2): D:\why habibi\_style_kit\ (rules, brand v2 logo/avatar/banner/intro sting/end screen, real-potato Batata v2, Rubik font, tools). Palette navy #0B1050, yellow #FFC21A, red #F0402F. The old cartoon packs (WhyHabibi_Pack1-3, AskHabibi_Logo) are RETIRED but must stay in place: both Ep 1 CapCut projects link to them. Rejected/retired files go to D:\why habibi\_archive\ (moved, not deleted).
- Caption style: Rubik-Bold (CapCut cache font id 7148699606082130433), white, size 7, y=-0.73, lowercase 1–3 word chunks, "3:00am" formatting.
- Voiceover: ElevenLabs mp3s (quiet ~-23 LUFS → level to ~-16 before use). Music: Xenoblade OST at volume 0.06.
- Memes: Ep 1 used imgflip templates; from Ep 2 memes are HOME-MADE only (copyright-safe, see [[copyright-safe-only]]). Use the yt-* skills by default ([[use-yt-skills-default]]).
- First video "overthincking !" rebuilt 2026-10-12; backups in D:\why habibi\_draft_backups\. See [[capcut-kit-windows-notes]].
- REUSABLE PIPELINE: D:\why habibi\_pipeline\README.md (playbook) + skill `habibi-video` (~/.claude/skills). User wants every future episode run this way. Music only from D:\why habibi\_music_library (incompetech CC BY, credit required); Xenoblade OST was dropped (Content ID). Thumbnail preference: real photos (Pexels) + ≤3 Impact words, mascots tiny — NOT cartoon-mascot-main. Shorts: 5-part series with "PART N → ON MY PROFILE" end cards; Shorts end lines: user prefers GENERIC reusable lines recorded once in D:\why habibi\_cta_library (RECORD_THESE.md; shorts.py picks cta_to_partN / cta_full_video automatically). User uploads long videos themselves; Claude uploads Shorts via the user's Chrome (YouTube Studio) as Private first, public/scheduled only on explicit OK. yt-* skills installed from github.com/Jakeschincariol/youtube-agent-skill.
- YouTube: channel "Ask Habibi" (@AskHabibi, Studio id UCJXUO3S0AtoQvmWHqpGp_ow; user's browser also has a personal channel — confirm the right one). Shorts upload prefs: NO links in descriptions ("Full video on my channel." instead), music credit line, Education category, not made for kids, target audience USA → schedule at 4–6 PM ET (= 23:00–01:00 Cairo; watch DST gaps late Oct/early Nov), first 2 parts public same day then one per day (Ep1 EXPERIMENT: user chose to publish all 5 Shorts at once on 2026-10-12 ~16:30 Cairo to "see what happens" — compare its results against spaced releases on later episodes). "Related video" was locked (channel verification in review) on 2026-10-12. Ep1 long video = i3pZRQq0ukY; its own description chapters had wrong timestamps (offered fix).
- User is on CapCut FREE (Pro expired) and wants free export: avoid Pro/AI features (auto captions, smart color adjust, normalize loudness, voice filters/isolation). Clean copy lives in project "overthincking ! FINAL"; background replaced by animated navy "midnight" clip (claude_gfx/00_background_midnight.mp4).
