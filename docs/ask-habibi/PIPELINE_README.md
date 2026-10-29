# Ask Habibi — video pipeline (playbook)

Everything we built for Episode 1 ("overthincking !"), saved so every next episode runs the same way.
Claude reads this file (the `habibi-video` skill points here). You can follow it by hand too.

## Folder map

```
D:\why habibi\
├─ _pipeline\
│  ├─ README.md                  ← this playbook
│  ├─ core\                      ← reusable tools (copy into a new episode folder)
│  │  ├─ (the Ep 2+ look and its tools live in _style_kit\tools)
│  │  ├─ gfxlib.py               (Ep 1 look) motion-graphics engine + animated "midnight" background
│  │  ├─ transcribe.py           word-level transcript of the ElevenLabs VO (faster-whisper medium.en)
│  │  ├─ sfx.py / fire_sfx.py    generates the SFX kit (whoosh, pop, ding, impact, riser, glitch, fire…)
│  │  ├─ music_bed.py            sectioned music bed: one track per chapter, crossfades, auto-ducking under the VO
│  │  ├─ shorts.py               renders vertical Shorts straight from the timeline + "PART N → ON MY PROFILE" end cards
│  │  ├─ thumbs_real.py          real-photo thumbnails (Impact text, LED 3:00 clock, night grade, tiny Batata)
│  │  ├─ cutouts.py / crop.py    background removal (rembg/u2net) and meme cropping
│  │  ├─ create_project.py       creates a FRESH CapCut project from a built timeline (no Pro/AI history)
│  │  ├─ update_project.py       writes a rebuilt timeline into an existing CapCut project (backs it up first)
│  │  ├─ write_draft.py          (older) in-place writer for the original project
│  │  ├─ inspect_draft.py        prints every track/segment of a CapCut draft
│  │  └─ sheet2.py               contact sheet of a folder of images (for reviewing memes/photos)
│  └─ episodes\ep01_overthinking\  ← complete, re-runnable snapshot of Episode 1 (scripts + data + package)
├─ _style_kit\                   ← THE LOOK (default from Ep 2): rules, brand v2, real Batata, fonts, tools. Read its README.
├─ _archive\                     ← retired / rejected stuff (moved there, never deleted)
├─ _cta_library\                 ← Shorts end lines recorded ONCE (see RECORD_THESE.md), reused by every episode
├─ _music_library\               ← Content-ID-safe music (Kevin MacLeod / incompetech, CC BY 4.0) + full catalog JSON
├─ _draft_backups\               ← automatic backups before every CapCut write
├─ 1st video\claude_sfx\         ← SFX kit (WAV)
├─ 1st video\claude_memes\       ← imgflip memes (raw + cropped)
├─ 1st video\claude_gfx\         ← rendered graphics MP4s + background clip
└─ 1st video\claude_package\     ← thumbnails, Shorts, upload package (title/description/chapters/tags)
```

## One-time setup (already done on this PC)
- `uv` and `ffmpeg` installed (winget). Run scripts with `uv run --no-project --with pillow --with numpy python <script>`.
  The `python` in WindowsApps is a Store stub — always go through `uv`.
- Whisper model `faster-whisper medium.en` is cached in `~/.cache/huggingface`. Cutout model `~/.u2net/u2net.onnx`.
- YouTube skills installed in `~/.claude/skills/yt-*` (package, chapters, shorts, seo, script, retention…), voice profile in
  `~/.claude/youtube/voice.md`.
- Work in a SHORT folder path (Python on Windows fails on paths > 260 chars).

## The episode workflow

**ElevenLabs is connected to Claude** (connector "ElevenLabs", cloned voice "Abdullah Osama"): Claude can generate the
VO and any extra lines directly (always ask before spending ElevenLabs characters). One-take recordings with many
lines are split automatically by `core/split_cta.py` (finds lines by their words, levels to -16 LUFS).

**0. You (in CapCut + ElevenLabs):** make the cold-open meme hook by hand if you want (like Ep 1), generate the
ElevenLabs voiceover (voice "Abdullah Osama", speed 100, stability 50, similarity 75) and import it into the project.

**1. New episode folder:** copy `episodes\ep01_overthinking` → `episodes\epNN_<name>`. Update the paths/constants at the
top of `build_draft.py`, `scenes.py`, `music_bed.py`, `shorts.py` (media folder, VO file, project name).

**2. Snapshot the draft (CapCut CLOSED):** copy
`%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\<project>\draft_content.json` → `cur_draft_content.json`.

**3. Level the VO** (ElevenLabs exports are ~-23 LUFS; we want ~-16):
two-pass `ffmpeg loudnorm=I=-15:TP=-1.5:LRA=11` (see Ep 1) → `<name>_VO_leveled_-15LUFS.wav`. Timing is unchanged.

**4. Transcribe:** `ffmpeg -i VO -ac 1 -ar 16000 vo16k.wav`, then
`uv run --no-project --with faster-whisper --with soundfile python -I transcribe.py vo16k.wav vo_words.json`.

**5. Plan the beats** from the transcript with the beat recipe in `_style_kit\STYLE_RULES.md`: a study/number → a
receipt (`_style_kit\tools\receipt.py <url> out.png "phrase"…`), a joke → a meme, a feeling → a real photo + hand note, a punchline → Batata pop. Rule of thumb from Ep 1: ~25 graphics, ~15 memes,
~10 stickers, ~130 SFX hits for a 3-minute video. Write graphics as scenes in `scenes.py`, the main/overlay/SFX
lists in `build_draft.py`.

**6. Render graphics:** `python scenes.py qa` (stills to review) → `python scenes.py bg` (background clip) →
`python scenes.py` (all MP4s). Graphics bake in the same animated background at the same timeline time, so cuts are seamless.

**7. Music bed:** edit `PLAN` in `music_bed.py` (track / start / end per chapter) → `python music_bed.py`.
Target: bed ≈ -31 LUFS integrated, ~15 dB under the voice; dips 9 dB under speech automatically.

**8. Build the timeline:** `python build_draft.py` → validates refs/overlaps/files and writes `new_draft_content.json`.

**9. Write to CapCut (CapCut CLOSED):** `python create_project.py` (new clean project) or
`python update_project.py "<project name>"` (existing project; backs up first). Check for edits you made in CapCut
before overwriting (Ep 1 diff check: compare segments ignoring IDs).

**10. Package:** run `/yt-package` (10 titles → `title.py`), `/yt-chapters` (≥3 chapters, first 0:00, each ≥10 s),
`/yt-seo` (description + 3 target searches). Thumbnails: `python thumbs_real.py` with Pexels photos.

**11. Shorts:** `/yt-shorts` picks 20–55 s self-contained moments → `SHORTS` dict in `shorts.py` → `python shorts.py`.
End lines come from the permanent **`D:\why habibi\_cta_library\`** (recorded once, generic: "Part two is on my
profile…", "The full video is on my channel…"): see `RECORD_THESE.md` there. They're added to every end card
automatically (card stretches to fit, captions shown). Optional episode-specific override: `shorts\cta\partN.mp3`.
Switch `CTA_VARIANT` A/B between episodes; `CTA_VERB` = "SUBSCRIBE" (YouTube) or "FOLLOW" (TikTok/Reels).

## Rules we learned (don't relearn these)
- **Copyright-safe only** (user rule): Pexels, our own Batata/brand, home-made memes, `_music_library`, our own SFX.
  No imgflip/film/TV images. Every episode keeps `CREDITS.md` (asset, source, licence). Table in `_style_kit\STYLE_RULES.md`.
- **Use the YouTube skills by default** (github.com/Jakeschincariol/youtube-agent-skill, installed in `~/.claude/skills/yt-*`):
  topic `/yt-viral` · script + hook `/yt-script` · pauses `/yt-edit` · title + thumbnail `/yt-package` · description `/yt-seo`
  · chapters `/yt-chapters` · Shorts `/yt-shorts` · after publishing: `/yt-retention` (2–3 days in, Studio export) and
  `/yt-comment` · weekly plan `/yt-plan` · channel check `/yt-audit`. Every run ends with "ship it, or change it?".
- **The look:** `_style_kit\STYLE_RULES.md` (+ the kit's README). Real things on screen + an editor's hand on top. No cards, borders, pills, dot
  wordmarks, tracked caps labels, mono `//` tags, glow or light leaks: the user calls that "AI slop".
- **CapCut must be fully closed** before any draft write (it rewrites drafts on quit). Always back up first.
- **Free export = no Pro/AI features:** no auto-captions (use our plain-text captions), no smart color adjust,
  no normalize loudness, no AI voice filters / vocal isolation. If CapCut still asks for Pro, move the timeline into a
  fresh project (`create_project.py`) — the old project keeps an encrypted record of AI use.
- **Captions style:** Rubik Bold (CapCut cache font id 7148699606082130433), white, size 7, y = -0.73, lowercase,
  1–3 word chunks, "3:00am" style, captions never cross the hook gag.
- **Keyframe time_offset** is on the SOURCE media timeline (source start + offset), not segment-relative.
- **Music must be Content-ID safe.** Game/film OSTs (e.g. Xenoblade) get claimed. Pixabay tracks are often
  "Content ID registered" (check the track page) and Pixabay blocks automated browsing. Use `_music_library`
  (incompetech, needs the credit lines below) or YouTube Audio Library.
- **Downloads:** photos and B-roll from Pexels (free licence); memes are home-made (no imgflip from Ep 2). Ask before
  downloading, keep the file list in the episode's `CREDITS.md`.
- **Thumbnails:** real emotional subject + ≤3 huge words, words must not repeat the title, brand mascots small only.
- **Facts:** every study named in the VO gets a source in the description; anything unsourced is flagged.
- **Long videos follow the Shorts that win (23 Oct 2026 data):** money-number news-map Shorts hold ~76%; long videos on
  random topics got 47-432 impressions and YouTube stopped testing them after 1-2 days (CTR 0.8-2.1%). Make the long
  version of a winning Short, same map look, a money number on the thumbnail, and point the Short's related video at it.
- **No copyrighted stills, ever:** Ep 1 had a Disney White Rabbit (imgflip) at 0:00 and 0:17; it was blurred in the Studio
  editor on 22 Oct. Check every old meme folder before reusing anything.
- **Render memory:** map-heavy 16:9 renders (shortkit, pyramid up to 160) run out of RAM at 6 parallel segments; use 2-3,
  and check every `seg_*.mp4` duration + the final duration before uploading.
- **Captions from whisper:** numbers come back as digits ("$427" for "four twenty-seven"); fix them with `cap_fix` in
  `K.setup` and re-check the caption frames.

## Publishing & timing (target audience: USA)
- **Post time:** weekdays **4–6 PM US Eastern** (people are home, near dinner — fits "midnight questions").
  That is **11 PM–1 AM Cairo** most of the year. Use YouTube Studio → Schedule, so you never stay up for it.
- **Daylight-saving trap:** Cairo is UTC+3 in summer / UTC+2 in winter (Egypt switches back on the last
  Thursday of October); US Eastern is UTC-4 / UTC-5 (switches on the first Sunday of November).
  So Cairo = ET +7 h most of the year, but **ET +6 h in the few days between those two dates**. Check a converter
  before scheduling around late Oct / early Nov and late Mar / late Apr. Pacific (PT) = Cairo − 10 h.
- **Shorts cadence:** a linked "Part 1–5" series can all go out, but spaced: 1–2 on the long video's day, then
  one per day. Stand-alone (unlinked) Shorts: pick the 2–3 that make sense without the long video.
- **Shorts descriptions:** no links (user preference). "Part N is on my profile. Full video on my channel." +
  music credit + hashtags. Connect them to the long video with Studio's **Related video** setting instead.
- **After 1–2 months:** Studio → Analytics → Audience → "When your viewers are on YouTube" — replace this
  guess with the channel's real hours. The first 3 seconds of each Short and a consistent schedule matter
  more than the exact hour.

## Brand constants
Navy `#0B1050` · Blue `#1E2A8A` / `#2734A1` · Yellow `#FFC21A` · Red `#F0402F` / `#FF5A4E` · Green `#3CC47C` · Sky `#7CC8FF`.
Mascot (from Ep 2): **Batata v2, a real potato with a marker face**: `_style_kit\mascot\batata\` (`cool` = brand face).
Brand v2 (logo, avatar, banner, watermark, intro sting, end screen): `_style_kit\brand\`.
Retired (Ep 1 only; kept in place so Ep 1's CapCut projects still open): cartoon Batata/Tamatem/Dorra,
`WhyHabibi_Pack1-3`, `AskHabibi_Logo`.
Ep 1 background: animated navy "midnight" from `gfxlib.bg_at()`. From Ep 2: real photos with a navy night grade
(`marker.night()`) or the real navy paper texture (`brand_v2.texture()`), no abstract backgrounds. Hand notes: Ink Free.

## Music credits (paste in every description that uses them)
```
Music by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0
http://creativecommons.org/licenses/by/4.0/
"Marty Gots a Plan" · "Daily Beetle" · "Easy Lemon" · "Dream Culture" · "Thunder Dreams" · "Promises to Keep"
```
Pick new tracks from `_music_library\incompetech_catalog.json` (filter by "feel"), download, add to the bed PLAN.

## Ep 2+ build: the Cut & Marker render pipeline (reference: `episodes\ep03_two_minute_sleep\`, the newest copy)
Every frame is drawn by our code (style kit), so the finished video exports without CapCut; a CapCut project is
still created for hand edits. Run from the episode folder with `uv run --no-project --with pillow --with numpy python …`.
**New episode = copy the newest episode folder**, rename the `epNN` files, then change only `epNN_common.py` (paths,
VO length, the cold-open end phrase) and write the new `beats_epNN.py`. Ep 3 adds: `Card` (our hand-written index card,
never a book cover), the notebook list helper, `qa_caption_zone.py` over the whole export, and the music drop-out trick
in `mix_ep03.py`. Every note's bottom edge stays at y ≤ 800 (caption zone rule); `check_caption_zone.py` must print 0.
1. `vo_text.py` → the exact ElevenLabs text (one paragraph per beat). Generate the VO in parts **≤ 2,500 characters**
   (a 6,000-character request failed), 1 take each (`generations_count=1`!), join with 0.7 s seams, level to −16 LUFS.
2. `transcribe_parts.py` (Whisper in slices; the full file ran out of RAM) → `build\vo_words.json`.
3. `receipt.py` for every study (in the kit), then `prep_receipts.py` (crops the huge pages).
4. `ep02_common.py` = timeline (CTA inserts, phrase → time). `beats_ep02.py` = one visual per line, every overlay keyed
   to a word; sound cues come from the overlays automatically.
5. `render_beats.py qa` (one still per beat → `build\qa_sheet.png`, fix layouts) → `render_beats.py all k 3` ×3 in parallel.
6. `mix_ep02.py` (VO + ducked music bed + SFX → −14 LUFS) · `captions_ep02.py` (ASS + SRT + JSON, keyword in yellow,
   skips words already on screen) · `assemble_ep02.py` → `export\…_1440p.mp4`.
7. `capcut_ep02.py` + `create_project_ep02.py` (CapCut closed) → editable project. `thumbs_ep02.py` (kit `thumbkit.py`).
8. Package: `/yt-package`, `/yt-chapters`, `/yt-seo` → `export\YouTube_package.md`; `/yt-shorts` for the series.

## Every episode's `export\` folder (default, user rule)
`export\` must hold everything needed to upload, so the user only copies and pastes:
- `<Show>_EpN_1440p.mp4` · `<Show>_EpN_captions_EN.srt` · `thumbnails\` (3 for Test & compare)
- **`UPLOAD_COPY_PASTE.txt`**: plain text, in YouTube Studio's order: title · description (chapters, sources, disclaimer,
  music credit, hashtags) · thumbnail to upload + A/B set · playlist · audience · Show more (altered content = **Yes**
  because the narration is an AI voice clone, tags, language, category Education, licence) · subtitles file · end screen
  layout · cards · pinned comment · when to publish (US Eastern, Cairo time, DST note) · after-publishing steps.
- `YouTube_package.md`: the reasoning (scores, alternates, query test). Copy the Ep 2 files as the template.
