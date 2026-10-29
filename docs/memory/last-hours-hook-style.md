---
name: last-hours-hook-style
description: "The Last Hours intros must open with a punchy \"imagine\"/shock hook in the first 2 seconds, then the date + clock time (Cooper-style)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-25T13:56:04.901Z
---

User (21 Oct 2026, Roanoke script): change the intro so the first couple of seconds are a hook — "imagine something" or a shocking count ("13 girls dead, found in...") — and THEN the date and clock ("like 1995", "they mention the clock and everything", as in Cooper's "Wednesday, November 24, 1971. Ten minutes past eight at night.").

**Why:** they want the strongest possible first seconds; a scene-setting opening alone was not enough.

**How to apply:** line 1-2 = hook (score it with yt-script hookscore.py; aim 70+; "you" early, a number, a stakes word, a curiosity gap like "but nobody..."), line 3 = weekday, date, year + clock time (use "about" for computed times), then the scene. Facts in the hook must still be exact (Roanoke: "Imagine you wait three years, and lose seven men, to reach your family. But nobody is there. Just one word, carved on a post." = 71). Also: user said "when you want me to download anything, let me know, and just go ahead and do your job" - only stop for download approvals. Related: [[new-channel-last-hours]], [[last-hours-thumbnail-style]].

22 Oct 2026 (Flannan): user asked for the REAL faces of the missing people in the first 3 seconds, then an edit showing
"they are not here". Done as: real photo on frame 1, red dashed outline round each man on the spoken number, then each one
flickers out (numpy fill, no AI) with a red "GONE" tag (render_flannan.py vanish_frame). Reuse this opening when a real photo
of the missing exists. User: no permission emails; use old anonymous photos (out of copyright by age) directly.

25 Oct 2026 Studio: the Alcatraz teaser Short "He Touched the Sleeping Man's Head. It Rolled Off." = 139 views, 51.4% viewed within hours,
the channel's top item; long files keep viewers (Alcatraz 47.2% avg) but get few impressions. Teaser titles: two short sentences, one
person's concrete action, then the shock; no dates or logistics (LESSONS 41).
Same evening (first 14 h 54 min): that Short = 288 views, 61.1% viewed (formula confirmed). Long files: CTR is the bottleneck,
not retention — Roanoke 1.8% CTR / 3:34 AVD (93 views), Alcatraz 1.5% CTR / 7:26 AVD (76 views). Next lever = long-video
titles/thumbnails in the teaser formula, and every teaser Short linked to its long video.
