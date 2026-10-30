---
name: content-creation-a-z
description: The complete, battle-tested system for producing faceless YouTube channels end to end — "The Last Hours" (hour-by-hour true-history documentaries from public records) and "Ask Habibi" (curiosity explainers in CapCut) — research with sub-agents, scored hooks, scripts from verified sources, a local cloned voice (Chatterbox), Python render engines, thumbnails, YouTube Studio scheduling/A/B tests/comments via browser automation, teaser Shorts, and analytics-driven growth. Use it for any request about making, packaging, uploading, scheduling or analysing videos for these channels, or when starting a new channel the same way.
---

# Content Creation A-Z

This repo is the memory of a working two-channel YouTube operation. Everything here was learned by doing it:
what the owner approved, what they rejected, what the numbers said, and the exact tools that made the videos.

**Read in this order, every new session:**
1. `docs/00-START-HERE.md`: the map (channels, folders, what lives where).
2. `docs/01-OWNER-RULES.md`: the hard rules. They override every default you have.
3. The playbook for the job:
   - a Last Hours long video, Shorts, packaging or upload → `docs/02-LAST-HOURS-PLAYBOOK.md`
   - anything in YouTube Studio (upload, schedule, A/B, comments, related video) → `docs/03-YOUTUBE-STUDIO-PLAYBOOK.md`
   - "why is this video not growing / what should we make" → `docs/04-GROWTH-AND-ANALYTICS.md`
   - brand, persona, calls to action, likes/subscriber conversion (The File Keeper) → `docs/09-BRANDING-AND-CONVERSION.md`
   - an Ask Habibi episode or Short in CapCut → `docs/06-ASK-HABIBI-PLAYBOOK.md` (+ `skills/habibi-video/`)
4. `docs/05-TOOLS-INDEX.md` before writing new code: the engine you need probably exists.
5. `docs/memory/`: the raw learned memories (owner feedback with dates and reasons). Search them when a detail is unclear.
6. `docs/08-CURRENT-STATE.md`: the live schedule, video IDs and open tasks (keep it updated).

**Keep this skill current by default (owner's standing order, 30 Oct 2026):** every decision that changes how we research, edit,
brand, package or upload (agreed or rejected) is written into the right doc here the same day and pushed, without being asked.

**The YouTube skills** in `skills/yt-*` (MIT, Jake Schincariol) are used at every step: `/yt-viral` topics, `/yt-script` +
`hookscore.py` hooks, `/yt-package` + `title.py` titles, `/yt-seo`, `/yt-chapters`, `/yt-shorts`, `/yt-retention`,
`/yt-comment`. Install them with `install.ps1` / `install.sh`.

**Working style the owner expects:** short replies with tables (they skim); finish the job end to end without asking for
approval at every step; STOP only for (a) downloads (list file, source, size), (b) new or replacement thumbnails, (c) anything
published, sent or deleted that they did not ask for. Report honestly when something failed.

**New machine?** `docs/07-SETUP-NEW-MACHINE.md` (paths, dependencies, the voice model).
