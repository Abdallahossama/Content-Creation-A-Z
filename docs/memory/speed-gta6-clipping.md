---
name: speed-gta6-clipping
description: 24 Nov 2026 owner wants automated Shorts of IShowSpeed playing GTA 6 (clip channel); research on permission + YouTube rules
metadata:
  type: project
---
24 Nov 2026: owner asked for "YouTube automation for Speed viral videos playing GTA 6, upload short content".
Facts found: GTA 6 launched ~18-19 Nov 2026; IShowSpeed streamed a 52-hour GTA 6 marathon on YouTube; fan channels re-upload clips.
- No official IShowSpeed clipping program (Clyper 23 Oct, ReelShift 17 Oct 2026). Only brand-sponsored clipping campaigns (e.g. Expedia on Content Rewards, ~$1 per 1K views, paid via Whop) give explicit footage permission via their brief.
- YouTube (1 Oct 2026): Shorts recommendations downrank re-uploaded clips; reused-content policy can demonetize the WHOLE channel, even with permission, unless real commentary/edit is added.
- Unlicensed re-uploads also risk Content ID claims / copyright strikes from Speed's team.
**Why:** conflicts with [[copyright-safe-only]]; strikes could hit the 2nd channel.
**How to apply:** only build the clip pipeline for licensed footage (sponsored campaign brief) or transformative commentary; owner must sign up/handle payouts himself. Existing tools: claude-shorts skill (longform→shorts, captions, vertical).

**24 Nov: owner said "just his video, it is totally open" -> go ahead.** Built pipeline in F:/speed-gta6:
1. list VODs (yt-dlp @IShowSpeed/streams); no "most replayed" heatmap on 6-24 h streams.
2. download audio only (format 249, ~120 MB per 6 h) -> tools/peaks.py (loudness bursts vs 5-min median) -> tools/scan.py (whisper on 90 s around each peak) -> pick moments.
3. tools/grab.py: FAST cut via the DASH sidx index + HTTP ranges (7 s per 90 s clip). yt-dlp --download-sections and ffmpeg -ss on the URL crawl (10+ min). Get URLs with yt-dlp --js-runtimes node -g (no JS runtime = throttled). Trim with -copyts + trim filters (seek on partial fMP4 fails).
4. tools/words_many.py (word timestamps) -> tools/speedclip.py (facecam top 700 / gameplay 1220, hook bar, yellow word captions, curse mask, credit; SC_BLUR=1 blurs gameplay).
HARD RULE: GTA 6 has a female lead (Lucia) -> check frame sheets of every window; drop or blur clips with women. Owner's yt-dlp binary: E:/WEB DEV/web/PROJECTS/ytfdownloader/bin/yt-dlp.exe.
First batch 24 Nov: S1 wrong save, S2 almost cried (blurred), S3 UFO hunt, S4 cheat codes -> F:/speed-gta6/export. Not uploaded; channel not chosen.
