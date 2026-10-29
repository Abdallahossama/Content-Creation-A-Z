# Ask Habibi: style kit (the default look from Ep 2 on)

Everything needed to edit an Ask Habibi video in the "cut & marker" style lives in this folder.
**Claude: read this file and `STYLE_RULES.md` before designing or rendering anything for the channel.**
The episode workflow (VO, transcript, CapCut build, music, packaging, upload) is in `..\_pipeline\README.md`.

## What's here
```
_style_kit\
├─ README.md            ← you are here
├─ STYLE_RULES.md       ← THE LOOK: what's banned, building blocks, motion, colour, type, beat recipe
├─ brand\               ← channel identity v2 (real Batata + marker)
│   BRAND_GUIDE.md      ← the brand reference: identity, colours, type, Batata, voice, sound, formats, where everything is
│   brand_board.png     ← the same on one visual page
│   logo_horizontal.png (transparent) · logo_horizontal_on_navy.png · avatar_800.png · watermark_150.png
│   channel_banner_2560x1440.png · intro_card_1920x1080.png · intro_sting.mp4 (2.4 s, use with the CTA)
│   end_screen_1920x1080.png (YouTube end screen: video elements on the 2 marker frames, subscribe on the circle)
├─ mascot\
│   batata\Batata_<expression>.png   cool (brand face) · shocked · deadpan · sleepy · sideeye · smug · sad · panic · fine
│   batata_sheet.png                  all expressions at a glance
│   source\pexels-33948200.jpg        the real potato (Pexels, photo by Nikolaos Kofidis, free licence) + potato_cut.png
├─ fonts\Rubik-Bold.ttf  ← caption + big-word font (= CapCut font id 7148699606082130433). Hand notes use Windows'
│                          Ink Free (C:\Windows\Fonts\Inkfree.ttf). Thumbnails use Impact.
├─ tools\
│   marker.py           the kit: highlighter, marker circles/arrows/underlines, Ink Free notes, stickers + pop,
│                       Rubik captions with outline, night grade, page_view (real page, tilted, focus-dim), shake
│   receipt.py          screenshot of a real study/article at 2x + where each key phrase sits (Edge via Playwright)
│   batata2.py          draws Batata's faces on the real potato (add a new expression in face())
│   brand_v2.py         rebuilds everything in brand\ (python brand_v2.py, then python brand_v2.py sting)
│   endcard.py          Shorts end card ("part 2 / is on my profile" + arrow + Batata); used by _pipeline\core\shorts.py
│   example_frames.py   the reference frames in examples\ (receipt, meme, level change, photo note, motion test)
└─ examples\            what "right" looks like: stills, Shorts end cards, motion_test_receipt.mp4
```

## How to use it (Claude)
- Run tools from `tools\` with `uv run --no-project --with pillow --with numpy python <tool>.py`
  (`receipt.py` also needs `--with playwright`; it uses the installed Edge, no browser download).
- In an episode script: `sys.path.insert(0, "D:/why habibi/_style_kit/tools")` then `from marker import *`.
  `BATATA` = mascot folder, `RUBIK` = caption font, `KIT` = this folder.
- Receipts: `python receipt.py <url> "D:/why habibi/<episode>/receipts/<name>.png" "key phrase" "another phrase"`
  → feed the PNG + JSON boxes to `page_view(..., marks=[...], focus=[...], dim=1)` and draw marker on top.
- Batata is a reaction sticker: `sticker(BATATA + "Batata_shocked.png", 300, rot=8, scale=pop(frames_since_hit))`.
  `cool` is the brand face (logo, avatar, intro). One Batata every 20–30 s, in a corner, never the narrator.
- New expression: add a branch in `batata2.face()`, run `python batata2.py` (re-renders all + the sheet).

## Retired (kept only so Episode 1 still opens in CapCut)
- The cartoon mascots and brand pack: `WhyHabibi_Pack1…`, `WhyHabibi_Pack2…`, `WhyHabibi_Pack3…`, `AskHabibi_Logo\`.
  Both Ep 1 CapCut projects link to files in them, so **don't move or delete them**; just never use them again.
- The Ep 1 motion-graphics look (`_pipeline\core\gfxlib.py`, animated "midnight" background, pills, cards).
- The rejected "Midnight Noir" test: `_archive\2026-10-12_rejected_midnight_noir\`.
