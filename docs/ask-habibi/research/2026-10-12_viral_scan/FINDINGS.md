# Viral scan, 2026-10-12 (yt-viral / swipe.py, last ~150 uploads per channel, public listings only)
Channels: Life Noggin, AsapSCIENCE, SciShow, Psych2Go, MinuteEarth, The Infographics Show, TED-Ed, أسئلة نص الليل (@noselleel)

In-lane outliers (multiple over the channel's own median):
- 35.4x  AsapSCIENCE: How To Fall Asleep In 2 Minutes (32M)
- 18.6x  TED-Ed: What happens to your brain without any social contact? (7.5M)
- 12.6x  Life Noggin: Staying Up vs Sleeping In - Which Is Worse? (746K)
-  5.8x  AsapSCIENCE: Why You're Always Tired (and how to fix it) (5.2M)
-  4.4x  أسئلة نص الليل: ليه بقينا مانعرفش ننام غير وفي صوت شغال جنبنا؟ ("Why can't we sleep without a sound playing?") (827K)
-  3.9x  AsapSCIENCE: What Happens To Your Brain When You Mindlessly Scroll? (3.5M)
Shared shape: the viewer's OWN night-time behaviour + what is happening in their body/brain right now.
Formula (title only, not proof of why it worked): The Question dominates (72 of the outliers).
Re-run: yt-dlp --flat-playlist -J --playlist-end 150 "https://www.youtube.com/@CHANNEL/videos" → collected.json → swipe.py
