---
name: long-form-plan
description: "Next 5 long videos (from the 18 Oct 2026 study), made in reverse order Egypt first; user wants fast montage, no approvals, final results only"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-23T09:47:20.844Z
---

Study 18 Oct 2026 (`_pipeline/research/2026-10-18_longform_study/FINDINGS.md`): our long videos got impressions but ~1% CTR;
winners for small channels ask about YOU/HUMANS in an everyday moment ("psychology of people who", "why did humans",
"what happens to your body"); 8-12 min beats 4-8 min. User: "why everything about sleep" -> picked non-sleep topics.

The 5 long videos, made AND uploaded in this order (user: "reverse sorting"):
1. Why Is 95% Of Egypt Empty? (maps) -> `D:\why habibi\5th video\`, code `_pipeline/episodes/ep05_egypt/` (render_ep05.py on shortkit 1920x1080)
2. Why Did Humans Start Wearing Clothes?
3. What Did Ancient Humans Do For Fun?
4. How Your Dog Really Sees You (potato dog 3D exists)
5. What Walking Every Day Does To Your Organs (3D x-ray)

**Why:** user (18 Oct): "you do everything, I will not give approval, I just want to see the final result"; all local, no money.
**How to apply:** fast montage = a new visual every 2-3 s (camera arrives, slow push-in, quick 1.1 s move), NOT sped-up voice;
script in the user's voice (voice.md), every number sourced and dated, chapters with re-hooks; 3 thumbnails + 3 titles for A/B;
long videos Thursday 23:00 Cairo. Related: [[shorts-standalone-only]], [[local-ai-stack]], [[clean-voice-mix]].

Pipeline state (18 Oct 2026): folders `5th`-`9th video`, code `_pipeline/episodes/ep05_egypt` .. `ep09_walking` (research.md + vo_lines.txt each);
shared `_style_kit/tools/longkit.py` (big/headline/place/timeline/photo/cutout/real_map/end_screen/subscribe_nudge), `vo_insert.py`
(splice a new line into a finished VO, keeps hand-fixed words), `fix_words.py` (whisper mishears), `cutout_person.py` (no-ML backdrop cut-out).
Render gotchas: the machine runs out of COMMIT memory (Chatterbox grows to ~5 GB): never run a map build or thumbnails while
`allseg` renders; check every seg frame count with ffprobe; `render_xx.py final 6` (final defaults to 3 segments!).
Wikimedia blocks full-size originals (429) -> use the API's 1920 px thumburl. Pexels CDN downloads work with curl.

DONE 18 Oct 2026 (all rendered + QA'd, thumbnails v3, upload sheets, credits): 5th Egypt 7:27 · 6th Clothes 7:19 · 7th Ancient fun 7:10 ·
8th Dog 7:15 · 9th Walking 6:30 (all -17 LUFS, end screen + mid subscribe moment). Next: upload in order Egypt (Thu 23 Oct 23:00 Cairo),
Clothes 30 Oct, Fun 6 Nov, Dog 13 Nov, Walking 20 Nov; files >10 MB so the user drags each file into YouTube's upload dialog, I fill the rest.
PUBLISHED 18 Oct 2026 ~19:40 Cairo (user: upload now, don't schedule): Ep 5 Egypt, Public, https://youtu.be/fx4Yqjxo7Ms, thumbnail
B_PACKED_EMPTY (small EGYPT flag), playlist Habibi Explains: the news, end screen = 2 videos (Best for viewer + Most recent upload)
at the bottom + Subscribe top-centre (YouTube's subscribe circle is too big to fit under our drawn boxes - place it top-centre).
Upload flow: user drags the big file into Studio's upload box; I fill everything. Altered-content left for the user.
Playlists (user, 18 Oct 2026): ALL long videos go in 'Ask Habibi: midnight questions' (Egypt too); 'Habibi Explains: the news' is for the news Shorts.
Egypt day 1 (19 Oct, ~18 h): 43 views (best long-video start; Ep 1 total 20), #1 of last 4, avg view 2:09 of 7:27 (~29%), CTR only 2.8% -> packaging is the lever; offered a "Test & compare" thumbnail test (A_95_EMPTY, C_95_HERE vs live B_PACKED_EMPTY), awaiting user's OK.
SCHEDULED 19 Oct 2026 (all Thursdays 23:00 Cairo = 16:00 NY; the old sheet dates 30 Oct/6 Nov/13 Nov/20 Nov were FRIDAYS):
Ep 6 Clothes 22 Oct (1YfFdArdcRE) · Ep 7 Ancient fun 29 Oct (tosn2qby1r4, set as 16:00 New York because Egypt DST ends at
midnight that Thursday, so 23:00 Cairo is ambiguous) · Ep 8 Dog 5 Nov (A6e1XUlx0wc) · Ep 9 Walking 12 Nov (SWRzkE6CHH8).
Each: title+thumbnail A/B test (3 variants from its sheet), playlist midnight questions, Education, English, not for kids,
no paid promo, AI toggle untouched, end screen imported from latest video then one box = previous episode (picker accepts
scheduled videos; it shows "private, will be replaced if not public" until that ep publishes). Pinned comments: post after
publish. Upload flow that worked: hard-link the 4 MP4s into `D:\why habibi\_upload_queue_ask_habibi\`, user drags all at once
into Studio's upload box, I fill each draft from the "Uploads complete" panel (don't navigate that tab while uploading).
Next free Thursday slot: 19 Nov 2026.
RESCHEDULED 19 Oct (user: "two videos per week, Thursday + any other day" -> I picked SUNDAY, 23:00 Cairo = 16:00 NY):
Ep 6 Thu 22 Oct · Ep 7 Sun 25 Oct · Ep 8 Thu 29 Oct (set 16:00 New York, Egypt DST night) · Ep 9 Sun 1 Nov.
Correct Ep 8 id is A6e1XUIx0wc (capital I). Next free slots: Thu 5 Nov, Sun 8 Nov. Cadence from now: 2 long videos/week.

22 Oct 2026 long-video data (Ask Habibi, since published): 3 AM 432 impr / CTR 1.6% / 20 views / AVD 1:32 (47.6%);
Straits 47 / 2.1% / 16 / 1:23; Sleep 265 / 0.8% / 8 / 2:04; Egypt 232 / 1.3% / 46 (only 9 engaged) / 2:30. Impressions stop
after day 1-2 = YouTube tests then drops them. Diagnosis: every long video is a different topic (no audience YouTube can
match), CTR < 2%, and the Shorts audience (money-number news maps, ~76% viewed) gets no long video in that format.
Plan proposed: long videos = the long version of winning Shorts (money/number + map, US framing), same look as the Shorts.
Ep 1 (i3pZRQq0ukY) shows a Disney-style White Rabbit still: no claim yet, but against copyright-safe rule; offer to cut it.
23 Oct 2026: Ep 10 "Why Diesel Costs $2 More Than Gas Right Now" (long version of the best Short) DONE: 10th video/export (8:25),
renderer _pipeline/episodes/ep10_diesel/render_ep10.py (shortkit 16:9 maps + charts, pyr up to 160). Render long map videos with
<= 3 parallel segments: 6 at once ran out of RAM. Thumbnails A pump +$2 / B Hormuz ISS / C IT'S NOT TAX await user OK; schedule TBD.
Ep 10 Diesel SCHEDULED: xZa4mspQBZE, Sat 24 Oct 19:00 Cairo, A/B A+B+C. When public: pin comment + point the Diesel Short at it.
23 Oct 2026 V2 RE-UPLOADS (ident + mid-video ask cut, same slots, A/B + end screens redone): Ep 7 Ancient fun tcVCWvwggrI
(Sun 25 Oct) · Ep 8 Dog EdgBd6zBnk8 (Thu 29 Oct, set 16:00 New York) · Ep 9 Walking _k2PSjmzSuE (Sun 1 Nov). Old copies
tosn2qby1r4 / A6e1XUIx0wc / SWRzkE6CHH8 = Private "OLD COPY (delete)" for the user to delete. Ep 6 Clothes trimmed in place.
Gotchas: "Edit title" on an A/B video deletes the test and the title box renders a few seconds later (JS hit the
description first); end-screen picker DOM keeps hidden duplicate dialogs, so pick tiles by video id among visible ones.
