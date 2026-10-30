# 09 · Branding and conversion: "The File Keeper" (The Last Hours)

Status: **APPROVED 30 Oct 2026** (owner: "this is goated", esp. the spoken mid ask at the cliffhanger). DEFAULT for every long file. Final look: the NOIR set (below). Applies to every new long file AND the re-brand of the already-scheduled long files.
Update this doc whenever a brand/CTA decision changes (owner's standing order: the repo is updated by default, unasked).

## Why
Retention is excellent (Cooper 74.9 % viewed, Franklin 65.7 %) but likes/subscriptions barely move. People subscribe to a
person/character more than to a topic, and a concrete "next file" gives a reason to subscribe. Honest maths: at ~55 views,
0 subs is still normal (new documentary channels convert roughly 1 sub per 100-300 views), so we fix BOTH clicks (thumbnails) and
per-viewer conversion (this brand).

## The persona
- **Name:** The File Keeper. Speaks as "I" in the narrator's (the owner's cloned) voice.
- **Mark (APPROVED 30 Oct):** a drawn vector detective silhouette (fedora with a red band, head under the brim in shadow, trench-coat
  collar turned up, red tie). Drawn in code by us (`brand/file_keeper/draw_mark.py`), no AI, no photo. Three treatments:
  `mark_v1_badge` (bone on ink, round: avatar, watermark, the 1.5 s video stamp), `mark_v2_stamp` (red rubber stamp "THE FILE KEEPER ·
  THE LAST HOURS": the "CASE CLOSED" end card), `mark_v3_folder` (manila case file with a "FILE KEEPER" tab: thumbnail corner, the
  mid-video badge). A "more realistic" code-drawn noir version was tried and REJECTED (looked like a mannequin); the owner chose to keep
  the drawn mark everywhere rather than use a photo.
- **Name check (30 Oct):** "The File Keeper" and "The Hour Keeper" (backup) are free on YouTube; "The Last Witness", "Mr. Midnight",
  "The Archivist", "The Night Clerk" clash with films/shows. Changing the name later = folder tab + stamp ring + spoken sign-off only.
- **Never:** a spoken channel ident, a backstory block, a pause for branding (LESSONS: viewers leave at the ident).

## Where it appears (timeline of one long file)
| When | What | Length |
|---|---|---|
| 0:00-0:40 | nothing: the hook runs clean | - |
| ~0:40 (the old "brand" stamp) | mark + "FILE NN · PLACE · DATE", over moving footage, voice keeps going | 1.5 s |
| ~75 %, right after a payoff | silent badge: mark + "SUBSCRIBE · NEXT FILE: <topic>" (runs across shot cuts) | 4 s |
| the payoff moment | TEST ONLY (Alcatraz 1946): spoken "vote with a like" ("If you think ..., hit like. If not, tell me why.") | 3-4 s |
| end | "CASE CLOSED" stamp + File Keeper sign-off naming the next file + like + "whose file next? I read every one" | <= 12 s |
| always | Studio watermark = the mark (subscribe on hover); avatar + banner; small mark in a thumbnail corner | - |
| comments | pinned comment + replies signed "— The File Keeper 🕵️"; pin + heart every new video | - |

Sign-off template (end of narration):
> "I'm the File Keeper. Every week I open one file the history books left half-told. File NN+1 is <topic>. Subscribe, and it'll be
> waiting for you. And if this one was worth your time, a like helps more than you'd think. Whose file should I open next?"

## Re-brand of scheduled files (decided 30 Oct)
- All 9 scheduled long files (Flannan 1 Nov -> Göring 29 Nov) are re-branded, re-uploaded and keep their dates.
- Method: patch the finished MP4 (stamp overlay at the brand time, the 75 % badge, new end card + re-voiced sign-off) with
  `_newchannel/_cta/` tools; no full re-render unless a patch can't reach a spot.
- Old copies -> Private, renamed "OLD COPY (delete)"; only the owner deletes. Redo A/B tests, end screens, captions, playlists.
- Shorts keep their current end cards.

## FINAL (30 Oct, later): the noir set + where each piece lives
The owner liked the noir (backlit, venetian-blind) rendering and asked for variants of it. Adopted:
| File (`_newchannel/brand/file_keeper/`) | Use |
|---|---|
| `mark_noir_badge.png` | channel avatar (`channel/avatar_800.png`) and the 1.5 s in-video stamp |
| `mark_noir_seal.png` | the "CASE CLOSED" end card (rim text THE FILE KEEPER · THE LAST HOURS) |
| `mark_noir_folder.png` | the ~75 % subscribe pill (thumbnail corner: ON HOLD, see below) |
| `mark_v1_badge.png` (flat) | ONLY the Studio watermark (`channel/watermark_150.png`): noir is too dark at 48 px |
| `channel/banner_2560x1440.jpg` | channel banner: THE LAST HOURS + tagline + "WITH THE FILE KEEPER · NEW FILES SUN + MON" (text inside 1546 x 423) |
Sources: `draw_mark.py` (geometry, flat set), `draw_mark_real.py` (noir set), `brand_board.py` (channel files + `_brand_board.jpg`).
Name: **The File Keeper**, no first name ("Noah"/"Noir" were considered: common/ungoogleable).

**Thumbnails: ON HOLD (owner, 30 Oct).** No brand mark on thumbnails for now. Thumbnails get their own plan later: the
analytics say they are the real bottleneck (click-through 2.6-2.8 % while retention is 65-75 %).

## Tools (`_newchannel/_cta/`)
- `signoff_gen.py` (Chatterbox, 3 takes per file) -> `signoff_pick.py` (whisper; numbers compared as words; writes `so_<key>.wav` +
  `so_<key>.json` word timings, "File Keeper" capitalised) .
- `brand_times.py` -> `brand_times.json`: per file, from its OWN render script: stamp time, pill time, the cut line (the first old end
  line), and a check that the uploaded MP4 length equals the script's DUR.
- `brand_patch.py <key> [--qa]`: re-encodes the uploaded MP4 up to the cut with the stamp mark + the File Keeper pill (covers the old red
  pill: y 40 for Flannan/Andrée/EgyptAir renders, y 120 for the rest), then appends the end card (blurred last frame, seal, CASE CLOSED,
  NEXT FILE, end-screen boxes, word-synced captions of the sign-off) -> `_upload_queue_last_hours/branded/*_FILEKEEPER.mp4`.
- New files (from Alcatraz 1946 on) draw the same pieces INSIDE their renderer (`import brand_patch as BP`: `stamp_image`, `pill_image`,
  `end_frame`), with the sign-off as the last VO line and TAIL 5 s.
- The cut also removes STALE end lines: after schedule reshuffles several files said "Next, I'm opening the file on <wrong video>".
  The sign-off always names the real next file in the current schedule.

## THE REFERENCE MOMENT (owner, 30 Oct: "this is goated", copy it in every file)
Flannan, 8:47: the narration asks the cliffhanger question, *"Why did all three go? And why did McArthur go without his coat?"*,
then the frame freezes and blurs, the File Keeper asks (brand new channel, like, subscribe, comment) while LIKE, SUBSCRIBE and
COMMENT pop on the words, then *"Now, back to the file"*, and the reveal (the two-waves theory) starts.
**Rule:** every long file gets exactly this, placed right after ITS cliffhanger question and right before ITS reveal (~55-75 %),
never right before a death. Pick the line with `_cta/mid_candidates.py`; set it in `brand_times.py` MIDLINE (patched files) or insert
the ask as a VO line in the renderer (new files, like `14_battle_of_alcatraz/brand_alc46.py`).

## UPDATE 30 Oct (owner review): spoken mid ask at a cliffhanger + animations
- **Why:** "most people close the video when the case is finished": the end ask reaches the fewest viewers. The ask must ALSO come
  inside the video, where the viewer most wants to continue: right before a reveal (~55-75 %), never right before a death.
- **Spoken mid ask** (same line in every file, `_cta/so_midcta.wav`): "Before I turn the next page: this channel is brand new, so if
  this file has you hooked, a like and a subscribe really help. And tell me in the comments what you think happens next. Now, back to
  the file." Visual: the frame freezes, dims and blurs; the noir badge drops in; LIKE / SUBSCRIBE / COMMENT pop on the spoken words
  (click, ding, paper SFX); de-blur back into the story. It REPLACES the like-vote test and the 24 Oct "no spoken mid ask" rule.
  Insert points (`brand_times.py` MIDLINE): Flannan 103, Saddam 58, Andrée 99, Gaddafi 57, Flight 19 107, Cyclops 68, EgyptAir 81,
  Göring 53, Alcatraz 1946 before line 42.
- **The old red pill** is covered by a silent case tab ("FILE 05 · FLANNAN ISLES · DECEMBER 1900"): one spoken ask per video, no
  second silent ask.
- **The stamp is animated** (`brand_anim.stamp_frame`, 2.9 s): the dark band sweeps in, the mark slides, turns and lands, "the"
  drops, LAST HOURS builds letter by letter, the file line types out, all fade together; a different SFX for each step, quiet under
  the voice.
- **End card:** LIKE / SUBSCRIBE pop exactly on the spoken "like" / "Subscribe" (the cursor presses SUBSCRIBE -> SUBSCRIBED).
- **Glitch fixed:** the cut into the end card is 0.25 s before the old end line (the old end card starts 0.12 s before it; one
  frame of it was flashing through).
- **Stamp band is fully opaque (255):** on patched files the OLD "the LAST HOURS" stamp is still in the picture underneath; at 248
  it ghosted through for ~0.3 s before our letters built (seen in QA).

## QA before any bulk upload (`_cta/brand_qa.py [key ...]`)
One contact sheet per file (`branded/qa_<key>.jpg`) + length + loudness (target about -16 LUFS). Tiles: stamp 0.3 / 1.0 / 1.8
(no old-stamp ghost at 0.3), case tab, the frame before the ask, ask 1.0 / buttons / out, the reveal, the end junction -0.4 /
+0.05 (must NOT show the old end card), +0.5 / +6 / +14 and the last frame. Look at every sheet before telling the owner it is ready.
New renders (Alcatraz on): `render_<file>.py keys` + a frame grab at the ask, the stamp and the end card.
Captions for re-uploads: `branded/captions_<key>_FILEKEEPER.txt` (the old text + the ask + the sign-off); new renders: the
branded `vo_lines.txt` without `##`. Chapters after the ask move by the ask's length (+13 s patched, `render chapters` for new).

## Measuring
- Per file: subs per 1,000 views, likes per 100 views, end-screen click rate, and the retention dip (if any) at the like line.
- The like-vote line goes channel-wide only if the Alcatraz 1946 curve shows no extra drop there.
