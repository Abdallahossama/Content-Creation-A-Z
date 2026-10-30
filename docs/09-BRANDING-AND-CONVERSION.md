# 09 · Branding and conversion: "The File Keeper" (The Last Hours)

Status: **DECIDED 30 Oct 2026** (owner). Applies to every new long file AND the re-brand of the already-scheduled long files.
Update this doc whenever a brand/CTA decision changes (owner's standing order: the repo is updated by default, unasked).

## Why
Retention is excellent (Cooper 74.9 % viewed, Franklin 65.7 %) but likes/subscriptions barely move. People subscribe to a
person/character more than to a topic, and a concrete "next file" gives a reason to subscribe. Honest maths: at ~55 views,
0 subs is still normal (new documentary channels convert roughly 1 sub per 100-300 views), so we fix BOTH clicks (thumbnails) and
per-viewer conversion (this brand).

## The persona
- **Name:** The File Keeper. Speaks as "I" in the narrator's (the owner's cloned) voice.
- **Mark:** a drawn vector detective silhouette (fedora, raised coat collar, face in shadow, a case file). Drawn by us, no AI.
  Shown to the owner for approval before use. Lives in `_newchannel/brand/file_keeper/` (sources + PNG exports).
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

## Measuring
- Per file: subs per 1,000 views, likes per 100 views, end-screen click rate, and the retention dip (if any) at the like line.
- The like-vote line goes channel-wide only if the Alcatraz 1946 curve shows no extra drop there.
