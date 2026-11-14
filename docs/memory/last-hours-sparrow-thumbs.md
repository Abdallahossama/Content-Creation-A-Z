---
name: last-hours-sparrow-thumbs
description: "14 Nov 2026: the owner asked to copy the @sparrow0y0 thumbnail look for The Last Hours re-thumbs. 8 options for Alcatraz/Franklin/Cooper/Roanoke are WAITING for approval. Keep Saddam as is."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0deccdd2-4bb6-4df6-90bc-0ed43495fcc4
  modified: 2026-11-14T04:58:05.905Z
---

On 14 Nov 2026 the owner sent https://www.youtube.com/@sparrow0y0/videos (an Arabic tech-story channel with 58.5K subs; top videos 140-490K views). The ask: analyse its popular videos and make "very unique" thumbnails in that style for older Last Hours videos that stalled.

**Owner's conditions:**
- Do NOT change anything until the new thumbnails are approved.
- Keep Saddam as it is ("it's working good"), so don't touch the Saddam thumbnail. Ask before applying the title-test winner.
- Recent uploads (Andrée, Gaddafi Benghazi, Mallory) need normal time; leave them.

**What the sparrow look is:**
- One big famous face or object, high-contrast black and white, on a dark grainy navy background with a soft spotlight.
- One accent colour per thumbnail.
- A HUGE 1-2 word headline: one word in the accent colour, partly behind the subject's head, and one white word in front.
- A "slice" through the letters.
- A thin accent frame and a small channel tag in the corner.
- (Sparrow's 3D cartoon props are not copied: [[real-not-cartoon]].)

**Our version:** `D:\why habibi\_newchannel\_rethumb_nov14\thumbs_sparrow.py`, output in `out/` (sheet.jpg). It uses Impact and Arial Black, real archival images only, the date in an accent block ([[last-hours-thumbnail-style]] date rule), and `#THELASTHOURS` top right.
- The slice is a gap low in the letters (80% height) with the bottom part nudged right and an accent stripe inside the glyphs only. A mid-height line read as strikethrough, so it was rejected by me.
- Cutouts use a PIL floodfill matte (no MediaPipe/rembg/cv2 on the machine). It works for mugshots and sketches; for plates and engravings, fade the left edge instead.
- Fragile setup: run it with `E:\AskHabibiAI\venv-chatterbox\Scripts\python.exe`. uv Pythons are broken, and MaxFilter(1) crashes Pillow with a silent exit 127.

**Options (A/B each):**
- Alcatraz: NEVER/FOUND + Morris mugshot; IT WAS A DUMMY + dummy head.
- Franklin: 129/MEN. GONE. + daguerreotype; ALL WELL? + 1848 note.
- Cooper: WHO/WAS HE? + sketch; $200,000/HE JUMPED. + sunglasses sketch.
- Roanoke: 115/GONE. + 1876 Croatoan engraving; ONE WORD./CROATOAN + Raleigh.

**Why:** the old videos have stalled (Alcatraz 4 views in 48 h, Roanoke 1.6% CTR); see [[last-hours-analytics-nov14]].

**How to apply:** after approval, add the picks to Test & Compare against the current thumbnail (don't replace blindly). Re-check CTR after 7-14 days.

**v2, same day.** The owner said: "make it colorful and make it that same cut the same font same everything". Built `thumbs_sparrow_v2.py`, with output in `out_v2/`.
- **The real sparrow recipe:** each line is a left word + a long baseline BAR (the Arabic kashida) + a right word. The bar runs BEHIND the subject in the middle, and the words are sized to fit beside it.
- **Lettering:** Lalezar (OFL, sparrow-like heavy face, `_rethumb_nov14/fonts/`). Letters are a white-to-grey gradient with a 7-px multicolour 3D offset and a soft shadow.
- **Background:** navy with a faint 64-px grid, 3 colour blobs, grain, and a giant faint ghost word.
- **Subjects:** cut out with a coloured sticker outline. Where flood-fill fails (Franklin plate, Raleigh, the colour dummy photo, the engraving), I used a tilted rounded photo card with a coloured border. A true cutout would need rembg/MediaPipe (not installed; ask before downloading).
- **Still waiting for approval.**
