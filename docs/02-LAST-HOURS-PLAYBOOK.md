# The Last Hours: one long file, start to finish

Reference build: `examples/the-last-hours/13_goering_last_night/` (research, assets list, hooks, script, PLAN, credits, upload sheet)
and its engine `templates`-equivalent files: `render_goering.py`, `vo/*.py`, `dl_assets.py`, `ocr_docs.py`, `thumbs_goering.py`.
Read `docs/the-last-hours/LESSONS.md` first.

## 0. Pick the topic
- Famous name in the title is what makes YouTube suggest it (Alcatraz, Roanoke, D.B. Cooper got impressions; "129 men vanished" without "Franklin" did not).
- Proven breakout formula (Oct 2026): **"They Asked [famous name] [question]. He [answer held back]."** on WWII interrogation records,
  ~10 min, B&W face + 1-3 words on a red block. Our version: famous person + their last hours + the primary record.
- Use `/yt-viral` (multiples over channel median) and the owner's ideas list (`docs/memory/last-hours-alcatraz-analytics.md`).

## 1. Research with two parallel sub-agents (background)
- **Facts agent** → `research/research.md`: spine line, clock note (time zone + DST of that place/date), people, day-by-day and
  hour-by-hour tables with "who recorded the time", myths vs record, **safe lines** (word-for-word usable), **do-not-say** list,
  YouTube safety notes, copyright of each quote source, 5 hooks. Every claim tagged RECORD / REPORTED / COMPUTED / CLAIM.
- **Visuals agent** → `research/assets.md`: a DOWNLOAD LIST (nothing downloaded): ID, what it shows, beat, exact file URL,
  px, MB, licence link, credit, content check (women / bodies / symbols). Best-15 shortlist + 6 thumbnail picks + exclusions.
- Brief them with the exact output format (point them at a previous research.md / assets.md) and the hard rules.

## 2. Owner approves the download → `dl_assets.py`
Parses assets.md tables; one file at a time (Commons rate-limits); cuts long reels to the usable seconds (SEG dict) so frames with
women never reach disk; skips flagged items (SKIP set). Then contact sheets of every image to eyeball content and set crops.

## 3. Hook + script
- `hookscore.py` (skills/yt-script): write digits in the scored text; aim 70+ (our Göring hook: 85).
- `vo_lines.txt`: one sentence group per line, `##` = chapter pause; numbers spelled out; ~150 words/min (8-12 min target).
- Loops every 60-90 s ("Remember that date. It matters later."), myth-vs-record beat, payoff summary, end ask (rule).
- `vo/vo_tts.txt` = a speech-friendly copy (e.g. "p.m." → "at night", "Ley" → "Lye", "SS" → "S.S.").
- Verify primary documents once downloaded (OCR / read them): they often correct the press (Göring file: the Army copy of his
  note, the Andrus delivery-time memo).

## 4. Voice (local, free)
`E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe vo/vo_chatterbox.py <ref.wav> <out.wav> vo/vo_tts.txt > vo/vo.log`
(one line per call, exact-zero gaps mark line boundaries; ~20 min for 80 lines on CPU) →
`uv run --with faster-whisper ... vo/transcribe_lines.py` (per-line match score + `vo_words.json`) →
`fix_lines.py gen <ids>` (4 takes each) → `fix_lines.py pick <ids>` (whisper picks + splices). Check picks by ear-like
transcription when digits matter (the scorer ignores digits). Known misreads: "guard" → "god", name variants.

## 5. Render
`render_<file>.py` (built on the previous file's engine):
- `SHOTS` = (line or (line, "word|alt") key, KB/KBP/DOC/VID/VIDP/TCARD/COUNTER/NMAP/end); `OV` = overlays (badge date/clock,
  under, nameplate, quote, typecenter, stamp, list, subpop, brand). Keys snap to whisper word times.
- `ocr_docs.py` (rapidocr) gives line boxes so DOC spotlights + red underlines land on the spoken words; typewritten pages may need
  hand boxes in page pixels.
- Modes: `times`, `keys` (missing word cues + shot lengths), `boxes`, `qa` (one frame per shot → contact sheet), `seg i n`,
  `audio`, `final n`, `all n` (parallel segments + mix + mux), `chapters`.
- Rules: visual change every 4-6 s, nothing static > 8 s; CAPFIX maps whisper spellings to the record's; frame 1 owns the hook;
  check the QA sheet for blank maps, cut headlines, text over text.
- Output ~1-2 GB 1080p; audio mastered by `_style_kit/tools/audio_master.py`.

## 6. Package
- `thumbs_<file>.py`: breakout or channel-colour variants; contact sheet at full + phone size → owner approval.
- `title.py` (skills/yt-package): ≤ 60 chars, a number/name, no repetition between title and its thumbnail; 3 title+thumbnail pairs for the A/B test.
- `export/UPLOAD_COPY_PASTE.txt`, `export/captions_en.txt` (plain text, "Without timing"), `CREDITS.md`, chapters from `render … chapters`.

## 7. Studio (see 03-YOUTUBE-STUDIO-PLAYBOOK)
Owner drags files > 10 MB into Studio; fill details, playlist, not-for-kids, tags, language, category Education, captions,
end screen (2 videos + subscribe), A/B test, schedule (Sun/Mon 22:00 Cairo).

## 8. Teaser Shorts (3 per long file)
`_tools/teasers_more.py` cuts 30-55 s vertical teasers from the long edit (hook title, captions, end card naming the long video,
spoken CTA from `_cta/cta_teasers.py` in the cloned voice). Titles: two short sentences, one person's concrete action, then the
shock. Files > 10 MB → 2-pass x264 copies under 10 MB for upload. Schedule 19:00 Cairo; related video = the long file once public.

## 9. After publishing
Pin + heart the prepared comment; check reach (impressions, CTR) and retention after 2-5 days; retitle with the famous name or
A/B test if impressions stay low; write the lesson into LESSONS.md and memory.
