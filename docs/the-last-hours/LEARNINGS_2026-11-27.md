# Everything learned on 27 Nov 2026 (The Last Hours)

One long working day: Vice City finished, the Omar Qany "Full Story" format adopted (DreamWorks, Pixar, Cartoon Network), thumbnails rebuilt three times, the queue rescheduled. Each rule below came from a real mistake or an owner correction.

---

## 1. Thumbnails

### 1.1 What the owner wants: Omar Qany's look, literally
- Noah **big and centred** (30-50% of the frame), serious or shocked face.
- The studio's **famous characters around him**, all **behind** him, **no white borders**, mirrored **2 + 2** (back-outer + front-inner per side). Fill the bottom corners; empty space reads as "unfinished".
- The **studio logo in the middle** with the words split around it: `THE FULL | logo | STORY` (his "القصة | logo | الكاملة").
- **Layer order (owner):** city photo -> sky (gradient, clouds, stars, moon) -> **big explosion behind Noah's back** -> characters -> Noah -> logo + words.
- **No date tag** in the top-left (owner found "PIXAR 1986-2006" confusing).
- Bright, busy, colourful. Dark noir thumbnails with paper photo cards were rejected as "ugly, not catchy".
- **Font:** tested Anton / Luckiest Guy / Lilita One / Bangers on the same thumbnail; picked **Luckiest Guy** (Google Fonts, Apache, free commercial) for cartoon topics. Research agreed: bold, condensed, thick outline, readable at phone size; Anton/Bebas Neue for serious topics.
- Script: `brand/thumbs_pop/make_omar3.py` (+ `make_omar.py`, `make_omar2.py` helpers). Run: `TFONT=F:/thumbkit/fonts/LuckiestGuy-Regular.ttf python make_omar3.py`.

### 1.2 Copyright decision (owner, 27 Nov)
- Studio characters and logos are allowed **in thumbnails only**; the owner accepts the takedown risk (Omar takes the same risk). The **videos stay copyright-safe** (no clips, posters, characters, logos, studio signs).
- Still **no female characters**, **never anything over Noah's face**.

### 1.3 Getting character images
- Fandom wiki CDN (static.wikia.nocookie.net) answers scripts with a Cloudflare "Just a moment" page. **Do not bypass it.** Downloading through the owner's Chrome via JS was **denied by the permission classifier**: stop there and ask the owner to save big renders by hand.
- en.wikipedia infobox images work through the API (`tools/last-hours/thumbs/wikiimg.py`), but:
  - `prop=pageimages` skips non-free images: parse the infobox `image =` field instead.
  - Many pages give **posters, logos or title cards** (Johnny Bravo, Ed Edd n Eddy, Ratatouille, Megamind): check every file by eye before use.
  - Character lists hold the good SVGs (e.g. "List of The Amazing World of Gumball characters" -> `Gumball Watterson.svg`, rendered at 1000 px through `iiurlwidth`).
  - **429 rate limits** after a busy day: sleep 15-20 s between files, retry 429s after 60 s.
- **Never** use real-life statue photos of characters (the Toy Story park statues looked "very bad").
- Real explosion: Commons "Fireball pretty - Flickr - Focal Intent" (CC BY 2.0) on black, **screen-blended** so the black disappears. A drawn (procedural) fireball looked like a flat orange blob.

### 1.4 Cut-outs and lighting ("pop")
- Noah from a ChatGPT scene melts into it and reads as AI: cut him out (`rembg`, `isnet-general-use`), blur (3 px) + darken (0.62) the scene, enlarge him 1.14x, warm back-glow behind the head, blue->orange rim light (`brand/thumbs_pop/make_pop.py`).
- The avatar PNGs carry a faint alpha haze: threshold alpha (<40 -> 0) and **pad the image before any glow/MaxFilter**, or the glow is clipped into a visible rectangle.
- A thin logo (Pixar's serif wordmark) vanishes: crop to the letters (drop "ANIMATION STUDIOS"), thicken with `MaxFilter(9)`, white fill + dark outline.
- Collage panels from ChatGPT are ~830x310 and cut the hat: ask for **full-size single images**.

### 1.5 A/B tests vs. what the owner sees
- While a Test & Compare runs, Studio and the owner's own view keep **option 1 (the old thumbnail)**. The owner thought our update "didn't stick". If the owner wants a change **visible**, set it directly (end the test: report -> New test -> Continue deletes it, close the dialog, upload the thumbnail, Save). Done for 9 videos on 27 Nov.

---

## 2. YouTube Studio operations (Chrome)
- **Schedule date:** the date field is a calendar. Open the visibility panel (`Edit video visibility status`), click the date field, then click the day cell inside `div.calendar-month` for the right month (JS), `Done`, `Save`. Typing the date into the input does not stick. Verify in the content list.
- **Captions:** publishing fails while the video is processing; retry ~40 min later from Languages -> Edit subtitles -> Publish.
- **End screen:** the "Search your videos" list may never load. Paste the video URL into **"Search videos from other channels"**, which finds your own video. Drag elements onto the drawn slots of the Noah end card; set each element's start to when the card fades in (24:36:15 on Vice City), not the default.
- Big video files (5+ GB) cannot go through `file_upload` (<10 MB): the owner drags them into Studio.

---

## 3. Research and scripts (Qany "Full Story" format)
- Workflow: analyse his video in full (transcript + frames) -> research agent fact-checks every date/number and writes `research.md` (with a SCRIPT FIXES table + DO-NOT-SAY list) and `assets.md` -> script -> voice.
- His videos had 6-9 factual errors each (helicopter, not plane; Shrek 2001, not 2002; first **Best Animated Feature** Oscar, not first animation Oscar; "Disney refused to buy DreamWorks" unsupported). Never copy his claims unchecked.
- Swap Middle-East asides for US ones (Smash Mouth "All Star" named not played, Nickelodeon penguins show, Seinfeld's bee suit at Cannes).
- LESSONS 6 again: **no backstory block after the cold open**; drop context one line at a time inside a countdown.
- **Mid-video ask** (rule 29 Oct) must be in every script at a cliffhanger, 60-80% in, as its own line: "Before I open the next page: this channel is still new, so if this file has you hooked, a like and a subscribe really help. And tell me in the comments, [question]. Now, back to the file." If the file is already voiced, **append** it to an existing line so no line index shifts, and add a `midask` shot keyed on `(line, "before|open")`.
- Length: 3,400 words ~ 22 min at the Chatterbox pace (~2.6 words/s incl. pauses). Owner wants 20+ minutes.
- Research agents can be stopped by a session end: resume with SendMessage, ask them to **save research.md first**.

## 4. Voice (Chatterbox)
- Never beside a render (out of memory). Queue the next VO to start when the render prints its exit line.
- Fixing lines after voicing: keep a copy of `vo_tts.txt`, edit, **delete only the changed `lines/l####.wav`**, re-run `vo_chatterbox.py` (it re-voices missing lines and re-joins). `fix_lines.py gen` segfaulted on model load: the resumable runner is the reliable path.
- Respell hard names in `vo_tts.txt` only (Meledandri -> Mel-eh-dan-dree, Farquaad -> Far-kwahd, Quibi -> Kwib-ee, Catmull -> Cat-mull, Iger -> Eye-ger); map them back in `CAPFIX`.
- Whisper: strip hallucinated tails ("Bye", "you", "Thanks for watching") and fix brand words ("ASUMNIST TV" -> AwesomenessTV) directly in `vo_words.json`; most "low scores" are just digits vs. words.

## 5. Render
- `build_render_saddam.py <key>` + `patch_<key>.py` (Noah host, pops, end screen). End card: `ENDL` = the line where the card starts; if "subscribe" and "thanks" are on different lines use `wt(ENDL + 1, "subscrib")` and `wt(ENDL + 2, "thanks")`.
- Before rendering, contact-sheet every risky photo: **logos and signs** (Shrek and Xbox backdrops, "DreamWorks" letters on the Glendale gate, "Walt Disney Studios" wall sign, ABC tower logo) -> swap or crop. Jobs' 1984 Macintosh photo shows a **drawing of a woman on the screen**: always cover it.
- `NMAP(view)`: the third value is the **view width** (bigger = wider). 6.5-9.5 zoomed into ocean; 30 shows the California coast with both pins.
- After the render, run `render_<key>.py qa t1 t2 ...` on the risky moments and fix before the full re-render.
- **Disk:** D: hit 0 GB free and the final join failed. Masters now go to `F:/LastHours_exports/` (render `final` path patched); Vice City master moved there too. Clean D: before the next big render.

## 6. Schedule set on 27 Nov (22:00 Cairo)
Sat 28 Nov Vice City · Wed 2 Dec DreamWorks · Sat 5 Dec Pixar · Wed 9 Dec Cartoon Network · Sat 12 Dec Göring · Wed 16 Dec Alcatraz 1946 · Sat 19 Dec Indianapolis · Wed 23 Dec Cole & Roe · Sat 26 Dec Flannan.

Shorts (teasers, after their long video, one a day, original clock time kept): Göring 13-15 Dec · Alcatraz 1946 17-19 Dec · Indianapolis 20-23 Dec · Cole & Roe 24-27 Dec · Flannan 28 Dec. Cyclops Shorts 28-29 Nov unchanged. Lesson: when long videos move, move their teaser Shorts too (Studio > Content > Shorts).
