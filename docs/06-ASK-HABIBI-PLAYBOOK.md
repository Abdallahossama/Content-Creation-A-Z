# Ask Habibi playbook (CapCut explainers + Shorts)

> **STOPPED 30 Oct 2026 (owner): no more Ask Habibi content; The Last Hours only.** Ask Habibi-only files are archived in
> `D:\why habibi\_ASK_HABIBI_ARCHIVE (delete me)` and `E:\why habibi OLD ask habibi (delete me)` (the owner deletes them). Kept because The Last Hours
> uses them: `_style_kit` (tools, maps), `_music_library`, `_pipeline` (Shorts bank), `E:\AskHabibiAI` (the voice clone).


Full playbook: `docs/ask-habibi/PIPELINE_README.md` (folder map, 11-step workflow, commands) and the `habibi-video` skill
(`skills/habibi-video/SKILL.md`). Look: `docs/ask-habibi/style_kit_README.md`, `style_kit_STYLE_RULES.md`, `style_kit_DOC_MODE.md`.
Reference episodes: `examples/ask-habibi-episodes/` (ep01 is the complete re-runnable example: `scenes.py` graphics, `build_draft.py` timeline).

Key rules (details in `docs/memory/`):
- **Cut & Marker look:** real study pages, Pexels photos, home-made copyright-safe memes, marker/highlighter hand on top. No AI-slop
  design (dot wordmarks, tracked caps labels, bordered cards, glow). Mascot = Batata v2 (a real potato with a marker face), small.
- **Doc mode** for news/conflict/money topics: moving real maps (Natural Earth, `mapkit.py` + `mapcam.py`), chapter cards, dated
  lower-thirds, sourced counters, no memes.
- **CapCut (Windows, FREE tier):** write the draft JSON directly (CapCut fully closed, back up first); no Pro features (auto captions,
  smart colour, loudness normalise, AI voice). Captions Rubik Bold, white, size 7, y = -0.73, black outline; never under the caption
  band (x 420-1500, y 860-1010).
- **Voice:** ElevenLabs credits are used up → local Chatterbox clone (`E:\AskHabibiAI`). Decode to float; never 8-bit joins.
- **Shorts:** standalone (one question fully answered, no "part 2"), daily 19:00 Cairo, `shortkit.py`; money-number titles win.
- **Thumbnails:** Batata-hero cinematic (`cinekit.py`), real potato, glowing prop, gradient words; no AI images.
- **Upload:** `UPLOAD_COPY_PASTE.txt` in every export folder; target US/Canada/Europe framing (US units, $).
- The CapCut Bridge kit (`D:\capcut\capcut-kit-main`) is third-party, macOS UI automation; on Windows we only edit draft JSON
  (notes: `docs/memory/capcut-kit-windows-notes.md`).
