---
name: shorts-standalone-only
description: "User dislikes clipped Shorts with \"follow for part 2\"; wants standalone Shorts, one small idea each"
metadata:
  node_type: memory
  type: feedback
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-14T06:43:04.847Z
---

The user (2026-10-14) said the Shorts already uploaded to the channel are "kind of bad" and they dislike the
"follow for part two" idea. They want Shorts made as their own content: one small midnight question, fully
answered inside the Short.

**Why:** clips cut from long episodes need context and lean on cliffhanger CTAs; the user finds that cheap.
**How to apply:** never end a Short on "part 2" or "follow for more". Write each one vertical-first (30-45 s,
one question, one receipt, ends on the answer or a loop line). New VO costs ElevenLabs credits, so ask before
generating. Supersedes the "Shorts are paused" note in [[episode-status]] once the user approves a batch.
Related: [[use-yt-skills-default]], [[copyright-safe-only]].

Style the user wants (2026-10-14, reference: GeoGlobeTales map Shorts, e.g. youtube.com/shorts/BmNSUb8HxCA "the better one"):
old-paper maps with flat-coloured countries + serif italic names, small costumed characters standing on the map, one
plain centred caption, 60-100 s. Ours: a POTATO CAST built from our real potato (`_style_kit/tools/potato_cast.py`:
skins russet/red/gold/pale, squash/stretch, any face, suit, captain/hardhat/bicorne hats), our Natural Earth maps.
Style test: `_thumbs_v2/ideas/shorts_style_frame.png` + `potato_cast_sheet.png`.
Short #1 built 2026-10-14: "21 Miles Wide, But Ships Only Get 2" (Hormuz lanes), code `_pipeline/shorts/s01_hormuz_two_mile_lane/`
(render_s01.py: map canvases L0/L1/L2 x 3 colour states, geo camera, word-timed overlays, plain captions y=1360),
output `D:\why habibi\shorts\s01_hormuz\export\` (gain-only -23 LUFS + LOUDER -17 LUFS limiter version; user to choose).
VO 825 credits. YouTube: LOUDER v3 scheduled PUBLIC 14 Oct 2026 19:00 Cairo, https://youtube.com/shorts/RBqw1-3BSic (playlist Habibi Explains: the news, related video Ep 4, AI-use question left for the user). TikTok (user has an account, TikTok Studio web): filled + set to 14 Oct 19:00, user presses Schedule. Facebook reel: not yet. Use roles (captain, worker, diplomat),
not ethnic costumes; no cute characters for war casualties.
User notes on Short #1 v1 (2026-10-14) -> rules for every map Short: fixed Ask Habibi logo top-left (logo_horizontal,
300 px); NO blur/bloom on zooms (map pyramid 40..1280 px/deg sized from the camera path, levels blended, paper texture
in SCREEN space, constant halo); characters/ships move on ONE continuous path (never jump), kept mid-channel because
sprites are drawn above their anchor; labels in open water; constant motion for retention (circle on frame 1, moving
lane arrows, wakes, reactions, rolling numbers, quiet pop/marker SFX).
No idle bobbing on characters (user found the bobbing captain annoying, 2026-10-14): they stand still, move only with their ship/anchor, pop in, swap faces; one short hop at most. Ship wakes = a soft trail along the sailed path, not a detached chevron.
Short #1 first-day result (YouTube, 15 Oct): 333 views but only 20.3% stayed to watch (79.7% swiped), 74 engaged views, avg 0:30 of 0:57; growth stopped after ~1.5 h. Cause = a quiet first frame (zoomed-out beige map, small tanker, vague line "You've never seen it"). Rule for every next Short: frame 1 = the payoff already on screen, close and colourful, big question text at the top for the first ~3 s, and the spoken first line states the surprising fact within 1.5 s.
Confirmed by the old cringe Short retention export (15 Oct, ~38 viewers, 35.6 s): curve fell 137%->50% before the question was spoken at 12.4 s (9 s anecdote + 3.6 s wordless meme clip), then stayed nearly flat to the end. Rule: the question/fact in the first second, no wordless gaps. Analysis: _pipeline/research/2026-10-15_retention_cringe_short/.
Short #1 at 24 h (15 Oct): 752 views, +1 subscriber, 96% from the Shorts feed; most views in the first 4 h. Best video on the channel so far. Published 19:00 Cairo (12:00 ET); recommended keeping Shorts at that slot and long videos at Thu 23:00 Cairo (16:00 ET).
Two Shorts series (user, 18 Oct 2026, later the same day; replaces the "News with Habibi" rename idea): (1) "Habibi Explains the News" = the MAIN series, existing playlist "Habibi Explains: the news", no rename; (2) "Ask Habibi" midnight questions. One Short a day, alternating, all free (local voice clone, our own edits). A news reel the user sends is only the idea prompt: re-check facts, correct the angle, never reuse its footage. Short #3 France debt (`_pipeline/shorts/s03_france_debt/render_s03.py`, beats keyed from vo_words.json, local Chatterbox VO); a live "interest since you started watching" counter replaced weak coin dots, and the France zoom stays at ~62 px/deg so the screen isn't a flat red wall.
Daily plan (user, 18 Oct 2026): ONE Short every day at 19:00 Cairo, alternating the two series, all free (local Chatterbox clone + our edits; user: "the voice cloning is very great", "your edits is very great"). User does not read long messages: keep replies short, tables over paragraphs. Map Shorts now use `_style_kit/tools/shortkit.py` (setup/at/set_camera/overlay/main: build|qa|caps|seg|audio|final|all; custom polygons for provinces since we only have admin-0 data). Calendar + research: `_pipeline/research/2026-10-18_daily_shorts_scan/FINDINGS.md`.

TikTok (18 Oct 2026, side agent via Claude in Chrome, user asked): Shorts 03 France (18 Oct), 04 Alberta (19), 02 hypnic v2 (20),
05 diesel (21), 06 snack (22), 08 El Niño (23), 07 dog (24) scheduled in TikTok Studio at 19:00 Cairo with short captions + hashtags,
using the <10 MB HEVC upload copies in `shorts/_upload_copies/`. AI-content toggle left for the user. TikTok shows "Video published"
even when scheduled; the clock badge in the posts list confirms it. No "Scheduled" filter exists in TikTok Studio.

Results (18 Oct 2026): France debt news-map Short = 115 views in its first ~20 min (fastest start so far; 96.6% from the Shorts feed),
vs the old clipped "Part 1/2/3" Shorts at 164-520 total. Same-day news topic + moving map + numbers is the winning Short format so far.
Update 19 Oct: France YT Short stalled at 217 after its first ~1 h test push (flat for 18 h; retention data not ready yet); TikTok copy 155 views / 4 likes (Hormuz TikTok had 0). Pattern: YouTube gives one test batch, then stops if swipe-away is high -> tighten hook + shorter (35-45 s).
Short #9 France marches (19 Oct): doc mode, real Pexels photos (flag cutout, classroom, euro notes, Palais Bourbon), shortkit `render_s09.py`; scheduled YouTube 19 Oct 21:00 Cairo (extra slot, before the 20 Oct budget vote) https://youtube.com/shorts/igOu9e3ryI0; TikTok + FB via side agent.
Format research 19 Oct (small-channel 10x outliers): single-map story, true-size drag, "find your country", X-vs-Y scale stack, "facts that sound fake"; techniques: payoff in frame 1, a beat every 2-3 s, loop ending, info captions, SFX on every move. Daily news recaps flop.
