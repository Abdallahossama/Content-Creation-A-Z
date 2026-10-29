---
name: habibi-video
description: >-
  Produce an Ask Habibi / Why Habibi explainer episode end to end in CapCut desktop (Windows): ElevenLabs VO,
  captions in the channel style, the "Cut & Marker" look (real study pages, Pexels photos, home-made copyright-safe
  memes, Batata v2), SFX, a Content-ID-safe music bed, Batata-hero thumbnails (bright colour + mix), vertical Shorts with "part 2" end
  cards, and the upload package, using the yt-* skills at every step. Use for "next episode",
  "edit my new video", "make the shorts", "thumbnails for the new video", or any Ask Habibi editing request.
---

# habibi-video

The full playbook lives in **`D:\why habibi\_pipeline\README.md`**. Read it first, every time; it has the folder map,
the 11-step workflow, the exact commands and the rules we learned the hard way. Episode 1 is a complete, re-runnable
example in `D:\why habibi\_pipeline\episodes\ep01_overthinking\` (scenes.py = graphics, build_draft.py = timeline).

**The look lives in `D:\why habibi\_style_kit\` (README + STYLE_RULES.md, "cut & marker"). It is the default.**
Read both before designing any frame. The user rejected the generic AI-design look (dot wordmarks, tracked caps labels, bordered cards, glow).
Everything on screen must be real (study page, photo, meme) with an editor's hand on top (highlighter, marker,
sticker). Tools: `_style_kit\tools\` (marker, receipt, batata2, brand_v2, endcard). Mascot = Batata v2 (a real potato
with a marker face, `_style_kit\mascot\batata\`). The cartoon mascots/brand packs are retired but must NOT be moved
(Ep 1's CapCut projects link to them).

**Use the YouTube skills by default** (`~/.claude/skills/yt-*`, from github.com/Jakeschincariol/youtube-agent-skill):
`/yt-viral` topic · `/yt-script` script + scored hooks · `/yt-edit` pauses · `/yt-package` title + thumbnail ·
`/yt-seo` description · `/yt-chapters` · `/yt-shorts` · `/yt-retention` + `/yt-comment` after publishing ·
`/yt-plan` · `/yt-audit`.

**Copyright-safe only:** Pexels, our own Batata/brand, home-made memes (no imgflip/film/TV images),
`_music_library`, our own SFX; study pages = title + 1–2 cited lines. Every episode keeps `CREDITS.md`.

**Every episode ends with a complete `export\` folder:** the 1440p video, the captions `.srt`, `thumbnails\`, and
**`UPLOAD_COPY_PASTE.txt`** (plain text, in YouTube Studio's order: title, description, tags, settings, end screen,
cards, pinned comment, publish time) so the user only copies and pastes. Template: `D:\why habibi\2nd video\export\`.

Non-negotiables (details in the README):
- CapCut fully closed before writing any draft; back up to `D:\why habibi\_draft_backups\` first; diff for the
  user's own CapCut edits before overwriting a project they opened.
- Free export: no auto-captions, smart color, normalize loudness, AI voice filters. Fresh project via
  `create_project.py` if CapCut still asks for Pro.
- Music only from `D:\why habibi\_music_library\` (incompetech, credit lines in README) or YouTube Audio Library —
  never game/film OSTs, never Pixabay tracks marked "Content ID registered".
- Ask before downloading anything (photos, B-roll, music, SFX): list file, source, size, licence.
- Captions: Rubik Bold, white, size 7, y = -0.73, black outline (from Ep 2). Thumbnails (v3 default): Batata is the hero, giant, on a bright flat brand colour, one prop, 0–2 Impact words; a "mix" adds a real photo print. Test & compare = Batata · mix · best photo. Template `D:\why habibi\_thumbs_v2\thumbs_v3.py`.
- Run the yt-* skills (`/yt-package`, `/yt-chapters`, `/yt-shorts`, `/yt-seo`) for packaging; end with
  **ship it, or change it?**
