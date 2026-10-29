# Tools index (generated from each script's own docstring)

Paths in the scripts point at the owner's machine (`D:/why habibi/...`, `E:/AskHabibiAI/...`); change the ROOT constants on a new machine (see 07-SETUP-NEW-MACHINE).


## The Last Hours engine (shared)  (`tools/last-hours/`)

| File | What it does |
|---|---|
| `lastkit.py` | lastkit: The Last Hours editing kit (16:9 documentary). Black / bone / evidence-red, typewriter timestamps, real archive photos in black and white with slow push-ins, case-file prints, red evidence marks, hard cuts. |
| `thumbs_hakawi.py` | Hakawi-style (@7akawi-AA) colour thumbnails for The Last Hours (1280x720), 3 per video for the A/B test. One full-colour cinematic real scene (only colour-graded), a real period photo ghosted in, 1-2 huge lines on solid  |
| `vidclip.py` | vidclip: moving archive footage for the Last Hours renderers. A clip is decoded through ffmpeg in order (one reader per clip per render process), cover-fit to 1920x1080 and toned like |

## The Last Hours helpers  (`tools/last-hours/_tools/`)

| File | What it does |
|---|---|
| `ab_sheet_gaddafi.py` | — |
| `cut_ranges.py` | Remove time ranges from a finished video (spoken ident, mid-video ask), frame-accurate, with 30 ms audio fades at every seam. python cut_ranges.py <in.mp4> <out.mp4> a1:b1 [a2:b2 ...]      (seconds; [a, b) is removed) |
| `find_phrase.py` | — |
| `fix_chain.sh` | 23 Oct 2026: re-render the scheduled Last Hours files without flat black screens, cut the spoken ident + mid-video ask. |
| `fix_chain2.sh` | — |
| `no_black_patch.py` | Patch a Last Hours render script (LESSONS rule 19, 23 Oct 2026): inside frame(), every flat INK background becomes ambient(k) - the nearest photo shot, lightly blurred and dimmed, with a soft dark band so the card text s |
| `scenecuts.py` | Frame-difference shot boundaries in a window: python scenecuts.py <video> <t0> <t1> |
| `teasers_more.py` | Vertical teaser Shorts (1080x1920) for Saddam / Gaddafi / Franklin, cut from each long edit, same layout as the Flight 19 and Andree teasers: hook text on top, the Case File frame in the middle (blur fill behind), word-b |
| `words_at.py` | Word-level timings in a window of a finished video: python words_at.py <video> <t0> <t1> |

## Spoken CTAs (cloned voice)  (`tools/last-hours/_cta/`)

| File | What it does |
|---|---|
| `cta_mshorts.py` | Spoken end line for the standalone mystery Shorts that now point at their own long video (owner OK, 29 Oct): same shape as the Alcatraz line ("Want the full file? Alcatraz, hour by hour. Link below."), Chatterbox, 4 take |
| `cta_patch.py` | Add the subscribe asks to a Last Hours file that is already rendered (user, 25 Oct 2026; LESSONS 37): - END: one spoken line ("If you want the next file, subscribe." / "If you want that file, subscribe.") in the creator' |
| `cta_teasers.py` | The spoken end line for teaser Shorts that names the long video (owner, 26 Oct: Short -> long CTA must say which video): Chatterbox, the creator's cloned voice (same reference clip as every file), 4 takes per line -> tak |
| `cta_voice.py` | The spoken subscribe line for files that are already uploaded (Franklin, Flannan, Cooper, EgyptAir, Andree): Chatterbox, the creator's cloned voice (same reference clip as every file), 4 takes per line -> takes/<key>_<k> |
| `pick_cta.py` | whisper each take, keep the cleanest per line -> cta_next.wav / cta_that.wav |
| `pick_mshorts.py` | whisper each mystery-Short CTA take, keep the cleanest per line -> cta_m_<key>.wav |
| `pick_teasers.py` | whisper each teaser CTA take, keep the cleanest per line -> cta_t_<key>.wav |

## Standalone mystery Shorts engine  (`tools/last-hours/mystery-shorts/`)

| File | What it does |
|---|---|
| `mshorts.py` | mshorts: The Last Hours vertical mystery Shorts (1080x1920, Case File look). Every Short ends on the Alcatraz file unless its spec has "end" (own long video: img, label, title, cta).   cd "D:/why habibi/_newchannel/02_ha |
| `refix.py` | Re-voice single lines of a bank Short (Chatterbox, N takes), keep the take whisper hears best, splice it into vo_chatterbox.wav between the exact-zero gaps (backup: vo_chatterbox_v1.wav). |
| `specs.py` | Beat specs for the Halloween mystery Shorts (The Last Hours). One beat per VO line unless 'at' splits a line. Times inside a beat (ops / ov) are seconds from the beat start. Images live in media/ (see CREDITS.md). |

## Newest long-file template (Göring)  (`examples/the-last-hours/13_goering_last_night/`)

| File | What it does |
|---|---|
| `dl_assets.py` | Download the approved Göring visuals (assets.md sections A-F minus D2/D3/D4) into media/ (approved by the owner 29 Oct 2026: "Safe set, ~417 MB"). Images as JPG/PNG, documents as PDF, video as MP4/WEBM/OGV. |
| `ocr_docs.py` | OCR the scanned document pages once (FBIS, State, LoC, CIA: the A* page images): line boxes -> build/ocr/<rid>.json, so DOC spotlights land on the right words. The UN record (A90p*) gets exact boxes from un_pages.py inst |
| `render_goering.py` | The Last Hours #13: Hermann Göring's last night, Nuremberg prison, Tuesday 15 October 1946 (10:45 p.m.), and the hangings of Wednesday 16 October (1:11-2:57 a.m.). Case File style, colour grade, 1920x1080, burned-in capt |
| `thumbs_goering.py` | File 13 (Göring's last night) thumbnails, BREAKOUT style: one real image filling the frame, 1-3 words on a red block, the date BIG. YouTube safety (research.md section 13): no swastika, no rope/noose/gallows/body; the te |

## Voice pipeline (Chatterbox + whisper QA)  (`examples/the-last-hours/13_goering_last_night/vo/`)

| File | What it does |
|---|---|
| `fix_lines.py` | Re-voice selected narration lines (Chatterbox, 3 takes each), keep the take whisper hears correctly, splice it into the full VO, and rewrite vo.log durations so the edit re-times itself. |
| `retime_words.py` | After fix_lines.py splices new takes: re-base every line's start to the new vo.log durations and re-transcribe the given lines. |
| `transcribe_lines.py` | Whisper each narration line on its own slice: word timings on the VO clock (vo_words.json) + a per-line match score against the script (qa_lines.txt), so misread lines can be re-voiced with fix_lines.py. |
| `vo_chatterbox.py` | Local voice-over with Chatterbox Turbo (MIT, CPU): the user's own cloned voice, conditioned on a clean 13 s clip of his existing ElevenLabs narration (Short #1). One sentence per call (stable), joined with short pauses,  |

## Ask Habibi style kit tools  (`tools/style-kit/`)

| File | What it does |
|---|---|
| `audio_master.py` | Clean loudness for Ask Habibi audio: STATIC gain + a peak limiter, never ffmpeg loudnorm on its own.  |
| `batata2.py` | Batata v2: a REAL potato (Pexels 33948200, Nikolaos Kofidis) with a face drawn on in black marker. Writes D:/why habibi/_style_kit/mascot/batata/Batata_<expression>.png (transparent, full res; marker.sticker() adds the |
| `batata_boss.py` | Batata "boss" trial (2026-10-14, user: "make the potato more handsome, like the reference"). The same REAL potato (potato_cut.png, Pexels 33948200) with a grown-up marker face and a painted navy suit + brand-yellow tie,  |
| `brand_v2.py` | Ask Habibi brand v2 (real Batata + marker). Writes everything into _style_kit/brand/: logo_horizontal(.png / _on_navy), avatar_800, watermark_150, channel_banner_2560x1440, intro_card_1920x1080, |
| `cinekit.py` | Cinematic Batata thumbnail kit (the default from 2026-10-14; the user picked it over the flat Batata-hero look). Still the REAL potato with its marker face, no AI images. What changed: |
| `cutout_person.py` | Cut a person (or object) out of a plain studio backdrop without any ML model: fit a smooth quadratic to the backdrop (top, left and right borders), mark pixels that differ from it, keep the component touching the bottom  |
| `debreath.py` | De-breath an ElevenLabs VO: turn the inhales / air bursts between phrases down (default 15 dB), never the words.  |
| `deess.py` | De-esser for the ElevenLabs voice: turns down only the hiss of s / sh / f (above 4.5 kHz) when it pokes out, never the vowels. Why: the cloned voice is very bright, its "s" sounds sit ~4 dB under the vowels (a normal VO: |
| `docfx.py` | Doc mode (Ask Habibi documentaries): the serious sibling of Cut & Marker. Same brand colours and fonts, no memes. Screen-space overlays for the beat engine (each has t_in / t_out / on(tl) / draw(c, tl)): |
| `dogvision.py` | 'How your dog sees it' filter for real photos: dog colour vision (2 cone types, blue + yellow; simulated like human deuteranopia with the Viénot/Brettel 1999 LMS method) + lower sharpness (~20/75 -> blur) + optional slig |
| `endcard.py` | Shorts end card (1080x1920) in the cut & marker style: 'part 2' on a highlighter swipe, a handwritten line, a marker arrow to the profile picture (bottom-left in the Shorts UI) and Batata side-eyeing it. |
| `example_frames.py` | Reference frames for the style kit (built for Ep. 2) ('cut & marker', anti-AI-slop). Stills: python example_frames.py  /  motion test: python example_frames.py clip |
| `fix_words.py` | Fix whisper mishears in a vo_words.json, phrase by phrase (multi-token aware, timings merged).   python fix_words.py <vo_words.json> "Hollifell's=>Hohle Fels" "Geisen Klästerle=>Geissenklösterle" ... |
| `longkit.py` | longkit: shared helpers for the 16:9 long-form Ask Habibi explainers built on shortkit (from Ep 5 Egypt). Use after K.setup(..., size=(1920, 1080)). |
| `make_cast_pack.py` | Builds the Ask Habibi potato cast pack (brand asset): every character as a transparent PNG + one cast sheet. -> _style_kit/brand/potato_cast/<name>.png (900 px tall body) and _cast_sheet.png |
| `mapcam.py` | Moving maps for documentaries (doc mode): Natural Earth bases pre-rendered at several zoom levels (cached PNGs), an eased camera (centre lon/lat + view height in degrees of latitude), and geo overlays drawn per frame in  |
| `mapkit.py` | Real maps from Natural Earth (public domain, _style_kit/maps/*.geojson) in the Cut & Marker look: deep navy sea with a soft shallow-water halo, warm paper land, thin borders, Rubik labels. Reusable for any episode. |
| `marker.py` | Ask Habibi 'cut & marker' kit (from Ep. 2): the anti-AI-slop look, see _style_kit/STYLE_RULES.md. Real sources on screen + an editor's hand on top: yellow highlighter, red/yellow marker circles, arrows and notes |
| `mix_probe.py` | QA for any episode mix: music and SFX level under the voice, sub-bass share of the music under the voice, and whether the final loudnorm pass would have gone dynamic.  python mix_probe.py <build dir> <ep tag>   (e.g. ".. |
| `potato_cast.py` | Potato cast v2 (2026-10-14). Many characters from our one real potato photo (no AI), drawn costumes only. User notes on v1: squashing/stretching looked like broken perspective; some hats floated above the head. |
| `receipt.py` | Real 'receipt' capture: screenshot a source page (study, article) at 2x in the installed Edge and record where each key phrase sits, so the editor can drop highlighter / marker circles exactly on the words. |
| `sfx_kit.py` | The Cut & Marker sound set, synthesized from scratch (100% ours, copyright-safe). Writes _style_kit/sfx/<name>.wav (48 kHz, peak -3 dBFS).   uv run --no-project --with numpy --with scipy --with soundfile python sfx_kit.p |
| `shortkit.py` | shortkit: the Ask Habibi map-Short engine (from Short #1 v3 / Short #3), reusable for every "Habibi Explains the News" Short. Rules baked in: logo top-left, map pyramid (no blur on zoom), paper texture in screen space, p |
| `thumbkit.py` | Thumbnail kit (1280x720): real emotional photo, <=3 huge Impact words, night grade, LED clock, marker circle, Batata v2 peeking small. Same recipe as Ep 1's thumbs_real.py, without the glow, importable by any episode. |
| `truesize.py` | truesize: a Web-Mercator world map + "drag a country to its true size" for map Shorts (Greenland, Alaska, Africa...). Same old-paper palette as shortkit (OLD). A country is moved on the SPHERE (rotation along a great cir |
| `vertical.py` | — |
| `vo_insert.py` | Insert a freshly generated voice line (e.g. the smooth mid-video subscribe line) into a finished long-video VO, without re-generating or re-transcribing the rest: the hand-fixed vo_words.json is kept, later words are shi |

## Ask Habibi CapCut pipeline core  (`tools/pipeline-core/`)

| File | What it does |
|---|---|
| `create_project.py` | Create a fresh CapCut project "overthincking ! FINAL" holding the cleaned timeline. Leaves the original project untouched. CapCut must be fully closed. |
| `crop.py` | — |
| `cutouts.py` | — |
| `fire_sfx.py` | — |
| `gfxlib.py` | Tiny PIL motion-graphics engine for the Ask Habibi edit (1920x1080 @30fps -> H.264). |
| `inspect_draft.py` | — |
| `music_bed.py` | Build a sectioned, VO-ducked music bed for the whole timeline. Each section plays one track (level-matched), sections crossfade, and the bed dips under the voice. |
| `sfx.py` | — |
| `sheet2.py` | — |
| `shorts.py` | Render vertical Shorts (1080x1920) straight from the CapCut timeline JSON we built. Main visual sits mid-frame (graphics as a framed 16:9 card, memes large), big word-highlight captions |
| `split_cta.py` | Split ONE ElevenLabs recording that contains many lines into separate, levelled clips. Lines are found by their words (Whisper word timestamps + fuzzy match), so pause length doesn't matter. |
| `thumbs_real.py` | Real-photo thumbnails (1280x720), 'famous YouTube' style: emotional real subject, 2-3 huge condensed words, night grade, LED 3:00 clock, tiny Batata as the only brand hint. |
| `transcribe.py` | — |
| `update_project.py` | Write new_draft_content.json into an EXISTING CapCut project (keeps its ids/registry). CapCut must be closed. usage: python update_project.py "<project name>" [expected_sha1_of_current_draft] |
| `write_draft.py` | Write the rebuilt timeline into the CapCut project. CapCut must be fully closed. |

## Ask Habibi Shorts  (`tools/pipeline-shorts/`)

| File | What it does |
|---|---|
| `remix_music.py` | Re-mix finished Shorts with the louder, ducked music bed (shortkit.mix) and swap the audio into the exports. |

## Local AI setup  (`tools/local-ai/`)

| File | What it does |
|---|---|
| `setup_local_ai.sh` | Ask Habibi local AI setup (approved by the user 18 Oct 2026). Everything lives on E:\AskHabibiAI. |
| `setup_voice.sh` | Ask Habibi local AI setup (approved by the user 18 Oct 2026). Everything lives on E:\AskHabibiAI. |
