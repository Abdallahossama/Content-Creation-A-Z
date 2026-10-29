# Doc mode: Ask Habibi documentaries (serious topics, news, war, money)

The serious sibling of Cut & Marker. Same brand (navy, highlighter yellow, red; Rubik + Ink Free; Batata), different
temperature. Reference episode: `_pipeline\episodes\ep04_two_straits\` ("Why Do 2 Tiny Straits Control the World's Oil?").

## When to use it
Real conflicts, disasters, deaths, money and policy: anything where a meme would be disrespectful. The everyday
"midnight question" episodes stay in Cut & Marker.

## Tone
- No jokes about violence or victims, no memes, no reaction stickers during the story. Dry lines only about money and
  logistics ("Oil, it turns out, needs a door.").
- Batata appears twice: small and calm on the title card, and at the closing ask. Never next to casualties.
- Every number on screen is dated and sourced. Nothing from one side's state media alone. Say "reportedly" when the
  source does. Close with an "as of <date>" stamp; pin updates in the comments instead of editing the video.

## The look
| Element | Tool | Rule |
|---|---|---|
| Moving real maps | `tools\mapkit.py` (Natural Earth, public domain) + `tools\mapcam.py` | Day palette: sand land, navy sea, shallow-water halo, faint graticule, film grain. Bases at several zooms so close-ups stay sharp. Eased camera, "fly" moves pull back mid-way. |
| Map overlays | `mapcam`: Route (draws itself), Flow (oil chevrons), Pulse (a place that matters), Ship (moving; ghosted = transponder off), Barrier (closed), Area (an island), HandCircle / HandArrow (our marker, white-outlined), Label (Rubik, sentence case) | Base-map labels follow the zoom (`smin/smax`). Our marker stays the brand's signature on top of clean cartography. |
| Title card | `tools\docfx.TitleCard` | The world map, dimmed, slow push; Rubik title in sentence case + a hand line "Ask Habibi · a documentary"; Batata small. |
| Chapter cards | `docfx.ChapterCard` | Over the moving map: dim, big yellow hand number, Rubik title, marker underline. 2-2.5 s of music-only pause before the chapter's first line. |
| Dated facts | `docfx.LowerThird` | Bottom-left, ABOVE the caption band: Rubik line on a highlighter swipe + a hand source line, soft dark patch behind. |
| Numbers | `docfx.Counter` | Rolls to its value; hand label says what and whose number. |
| Quotes | `docfx.PullQuote` | Marker quote marks, Rubik, hand attribution with outlet + date. |
| Sources | `docfx.SourceTag`, receipts (`receipt.py`) | Same receipt engine as Cut & Marker; tag = outlet · date. |
| Photos | `DocPhotoBG` (docfx.grade) | Cooler, a touch desaturated, slow push. Real, licensed, never war footage. |
| Date stamp | `docfx.Stamp` | Red hand "as of <date>" at the end. |

No bordered cards, no glows, no tracked caps (same bans as Cut & Marker): darkness comes from soft scrims and vignette.

## Sound
One cinematic incompetech track per chapter (CC BY, credited): tense pulse for the setup, steadier drive for the
escalation, somber for loss of life, calm for the close. The music NEVER moves while the voice speaks: one fixed level
(12 dB down, about 21 dB under the voice) for each spoken passage, ramps of 1.2 s only inside pauses of 2.5 s or more, and
sub-bass cut by a fixed 6 dB. A per-phrase duck (and above all a two-band one) reads as "a whoosh when I speak" (Ep 4).
SFX: under the voice only tiny pops. Whooshes, risers, impacts, paper and highlighter play only in the pauses (the
user hears them as "noise while I speak"). No `room_tone`.
Voice: EXACTLY as ElevenLabs made it. No limiter, no compressor, no loudnorm, no de-ess. Squashing the cloned voice's
peaks is what made "a whoosh when I speak" in Ep 4; the user proved it in CapCut by muting tracks.
Master: raw mix written as FLOAT, then `tools/audio_master.py gain_only` (plain volume up to -1 dBTP; Ep 4 = -21 LUFS).
Never ffmpeg loudnorm or `audio_master.master/level` on anything containing the voice. QA: `tools/mix_probe.py`.

## Pacing
Documentary pauses are inserted into the voice timeline (`PAUSE_SPEC` in `ep04_common.py`): ~3.5 s for the title +
first chapter, ~2.4 s per chapter, 1-1.5 s after big reveals. Captions stay on (Rubik, the usual style).

## Thumbnails
Real map (Natural Earth) + giant Batata + bold white-outlined marker arrows + 1-2 Impact words (V1 "CLOSED / TAKEN" is
the reference: `D:\why habibi\_thumbs_v2\ideas\ep4_map_variants.py`).
