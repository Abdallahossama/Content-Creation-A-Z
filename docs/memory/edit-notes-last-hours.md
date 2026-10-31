---
name: edit-notes-last-hours
description: "User's edit feedback on The Last Hours #1 (19 Oct 2026): no text over text, no wobbly red ellipses, highlights synced to words, hero image in frame 1, teaser Shorts that point to the long video"
metadata:
  node_type: memory
  type: feedback
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-31T16:10:03.530Z
---

User watched Alcatraz v1 and said "the rest of the video is insane wow", but:
1. **Text over text is unacceptable**: two labels/captions in the same screen spot at once. Rule: one text per screen slot
   (bottom / center / side); the next one replaces the previous (render_alcatraz.py SLOT + ov_end).
2. **Red hand-drawn ellipses looked ugly** (thin, flat, same size, overlapping) and the pencil-scratch SFX with them felt fake.
   Use instead: spotlight (dim the page except the phrase, soft edges) + a clean red underline that slides in, camera
   easing toward the quote; map marks = clean perfect circles that settle in. No pencil sound.
3. **Timing**: marks must land on the exact spoken word (whisper word times: wt(line, word)), not line offsets.
4. **First second**: combine the hero evidence image with the document (e.g. dummy head print on top of the FBI page +
   typed time) so frame 1 hooks.
5. **Shorts for a long video** must make people curious about the rest, then send them to the long video (end card
   "THE FULL FILE" + one spoken line + YouTube related-video link). This differs from Ask Habibi's "no part 2" rule
   ([[shorts-standalone-only]]), which still applies to Ask Habibi curiosity Shorts.

**Why:** the user wants a professional documentary feel; sloppy overlaps/marks undercut the real-files credibility.
**How to apply:** every Last Hours video and Short; consider the same for Ask Habibi long videos. Related: [[new-channel-last-hours]].

21 Oct 2026 (Roanoke): user found the first seconds boring (plain sea photo, no text until ~4 s). RULE: frame 1 = hero image + text
already typing (place/date lower band) + a hit SFX, then kinetic hook words synced to the voice ("3 YEARS", "7 MEN LOST"). In the
render scripts set SHOT_T[0] = 0.0 so the first shot and its overlays own frame 1 (draw_ov skips overlays that start before the shot).

22 Oct 2026 (EgyptAir 990): user: "the music can be higher in the video". The Last Hours music beds now sit about 19-22 dB under
the voice RMS (was 25-28), i.e. +6 dB; voice level unchanged (-16 LUFS after audio_master). Use this level for every new file.
(The older "music <= -22 dB" rule in clean-voice-mix is for Ask Habibi long videos.)

22 Oct 2026: user asked for a COLOUR version of EgyptAir "like the thumbnail", keeping the B&W render as main. Built as
LH_COLOR=1 mode in 07_egyptair/build/_e_body.py (photos teal/warm graded, DOCS set stays paper-toned; own cseg_ segments,
reuses mix.wav, writes *_COLOR.mp4). Also fixed ov_end: it must take the EARLIEST later overlay in a slot, not the first in
list order (an out-of-order OV entry caused text over text at 7:25). Check new OV lists with build/_ovchk.py.

24 Oct 2026 (Saddam / al-Khuld Hall v1): user: "a lot of repetitive images with no proper filter, the 1st minute very boring with no
mention of Saddam Hussein or any known figure", and "why there is no captions". RULES from now on (renderer: 11_khuld_hall/render_khuld.py):
- The famous name in the FIRST sentence of the hook and on screen from frame 1 (ghost portrait composite = thumbnail A); other known
  figures (with nameplates) inside the first minute; real footage of the person early.
- BURNED-IN captions on every long video: bold white, current word yellow, word-synced from whisper (draw_caps + CAPFIX name spellings);
  the bottom band/nameplates sit above the caption zone (y 796-900). Still upload the CC file for search.
- One archive-film finish on every frame (film(): S-curve, warm highs/teal lows, light desaturation, fine grain) under the text layers.
- No photo/clip more than twice; documents may repeat (different lines). Count repeats before rendering.
- Thumbnails must show the famous person (user rejected a microphone-only thumbnail; a document-only one too).
- User asked why the real 1979 film wasn't used: explained copyright/Content ID/reused-content risk; user moved on to other fixes (no explicit yes).

31 Oct 2026 (Muslim Brotherhood, frame 1): user: "you zoom in a really bad way ... the text is covering the main person's face". He says it
happened "a lot of times". RULES:
- Never fill the frame (KB) with a SMALL (< ~1400 px wide) or UPRIGHT photo. Show it as a print card (KBP) at its true proportions.
- A face is never under text. The hook text sits beside the card (card x≈0.79, short hook lines), and quotes/lists move left ("quoteL"/"listL").
- Check frame 1 at full size before rendering. Build: 18_muslim_brotherhood/build/post_patch.py.
