# The Bill, Explained - production lessons

## The pipeline (episode #1, 15 Nov 2026)
1. **Research:** two background agents. Facts go to `research/research.md` (tags RECORD/REPORTED/COMPUTED/CLAIM, plus SAFE LINES and DO-NOT-SAY). Visuals go to `research/assets.md` (a download list: Pexels/PD/CC0, women check, logos).
2. **Hook:** `skills/yt-script/hookscore.py`. The winning shape put the viewer at the pump: "You fill up for $4... the truck pays $6.13...". Title + thumbnail are checked with `yt-package/title.py` (the thumbnail must not repeat the title, max 3 words).
3. **Script:** `vo_lines.txt`, numbers spelled out, `##` = chapter pause. 1,290 words came out at about 7:30 of VO.
4. **Voice:** `tools/vo_chatterbox.py` with the owner's ref voice (about 12 s per line on CPU, 97 lines in about 20 min). Then `tools/transcribe_lines.py` (whisper medium.en) and `tools/fix_lines.py <root> gen|pick <ids>` for misread lines.
5. **Media:** `research/dl_list.txt` + curl (Pexels `?w=3840`, Commons). Then a contact sheet: look at every photo for women, foreign prices and old price signs.
6. **Render:** `spec.py` (SHOTS/OV/MUSIC/EV/CH) on `tools/billvid.py`. Run `keys` → `qa` → `frame t` → `all 4`. 7.7 min renders in about 4 min.
7. **Shorts:** the same engine in vertical mode (`VERT=True`, `BV_SQUARE=1`): a 2-line question header, a 1080x1080 panel, captions, footer. Each Short is standalone and answers its own question.
8. **Package:** `export/UPLOAD_COPY_PASTE.txt`, `captions_en.txt`, `CREDITS.md`, thumbnails A/B (`tools/thumbkit.py`).

## Lessons
1. **C: drive full = random crashes** ("paging file too small", segfaults). Before any voice job, check that C: has more than 3 GB free and route temp to D: (`TMP=D:/tmp`, `UV_CACHE_DIR=D:/tmp/uvcache`).
2. **Never run Chatterbox beside a render or QA sheet.** One heavy job at a time. The render processes need the image cache capped (`billvid` keeps at most 9 photos + 7 blurred backgrounds per process).
3. **Whisper writes digits** ("four" → "$4", "two thirteen" → "213"). Shot keys use alternatives (`(0, "$4|four")`). `CAPFIX` maps "213" → "$2.13". Captions re-join split numbers ("$2" + ".13").
4. **Whisper invents trailing sentences** on short lines ("If you liked this video..."). `billvid` drops zero-length words, words after the line's audio ends, and near-zero-confidence blips.
5. **Cached backgrounds must be copied before drawing on them**, or old text bleeds into later shots.
6. **Contact-sheet blotches are just the downscale.** Check one `frame t` at full size before blaming the render.
7. **Photo checks:**
   - Grocery aisles can hide a shopper at the edge (crop N3 by 12%).
   - Drop foreign-currency shelves (N1).
   - Drop price signs that show an old, wrong price (A2).
8. **Studio launch (15 Nov):** rebranded the old Ask Habibi channel; big file uploaded in 9.5 MB parts; captions = timed SRT from `tools/make_srt.py` (untimed fails while YouTube processes). Details: docs/03-YOUTUBE-STUDIO-PLAYBOOK.md.
