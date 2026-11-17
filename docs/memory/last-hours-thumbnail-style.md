---
name: last-hours-thumbnail-style
description: "Last Hours thumbnails: since 17 Nov 2026 = owner's ChatGPT-ref look (AI cinematic scene + REAL archive face + distressed Anton 2-4 words on red brush/colour word + date); thumbls.py pipeline. Older Hakawi notes below."
metadata:
  node_type: memory
  type: feedback
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-21T04:23:20.066Z
---

From 21 Oct 2026 (Roanoke, file 04) the user wants The Last Hours thumbnails "with the same style of this channel" = @7akawi-AA (Hakawi, 1.06M subs).

What their thumbnails do (studied 21 Oct): one FULL-COLOUR cinematic scene filling the frame (teal/blue night or golden misty forest, strong vignette); real portraits sometimes ghosted (semi-transparent) into the landscape (Flannan: the 3 keepers over the island); 1-2 lines of HUGE heavy text, usually a question ("Where did they vanish?"), white or yellow, on a solid black block or with a heavy dark shadow; one key word/number in a contrasting box (white box + black "990"; small red box for a connector word); subtitle line in yellow on a dark band. Their Roanoke thumb: misty forest + abandoned cabins, "WHERE DID THEY VANISH?" white top-right, yellow "Roanoke's Lost Colony" bottom.

**Why:** the user benchmarks the channel against Hakawi (its topics scored 1.3-2.6x there). Our Alcatraz CTR was 1.4% with B&W case-file thumbs.

**How to apply:** colour-grade real images (no AI, no cartoons, no women - [[no-women-in-visuals]], [[real-not-cartoon]]); ghost real men's portraits where it fits; question text <= 4 words in heavy condensed type (Impact-like) on black/yellow blocks; keep the A/B test with all 3 thumbs. Related: [[new-channel-last-hours]].

22 Oct 2026: user stopped me mid-upload: "i must give u the approval 1st". RULE: always show new/replacement thumbnails (contact sheet) and
WAIT for an explicit OK before uploading them or touching an A/B test in Studio, even when the redesign itself was approved.
Colour versions for Alcatraz/Franklin/Cooper are built by _newchannel/thumbs_hakawi.py (ghosting cut-free mugshots looks like floating
discs -> use print cards for faces).
22 Oct: user verdict on the colour set: the B thumbnails (ONE strong real image filling the frame: dummy head photo, the real note, the
real money) were good; collages/ghosted faces/cards were not. A/C were redone as single full-frame real images and approved; all three
videos' A/B tests replaced (Alcatraz live; Franklin + Cooper scheduled). Lesson: one hero image, big subject, 2 short lines of text.

22 Oct 2026 (Roanoke v2): user wants the subject CLEARLY visible (faint ghosted people/ships = rejected; ghosted engraving ->
full sepia print with a feathered edge was approved), "more details" (a real map with a circle + zoom bubble on the evidence,
small date tags), and one unique attention-grabber (red zoom bubble on the key clue, like EgyptAir M1). Rejected: plain
landscape backgrounds (foggy marsh, ghost forest).

24 Oct 2026 (user): EVERY thumbnail shows its date, big (red or yellow block, ~50-60 px at 1280 wide), e.g. "22 APRIL 1848",
"14 JULY 1897". Hakawi's Franklin (1.8M) = ship frozen in + a line of men beside it: show the MEN, not only the ship
(Franklin N3 bubble = D11 men hauling a sledge past a ship). User liked N3 (map + circle + bubble) and N4 (1859 cairn
engraving + note bubble); rejected N1 (note+numbers), N2 (Crozier face), N5 (reward poster).
24 Oct 2026: user showed a reference (full-colour ships in ice) and I built Franklin TRAPPED v3 (colour-graded 1849 lithograph + Pexels storm sky/snow); user said NO to swapping it in: Franklin A/B stays TRAPPED v2 + N3 + N4. v3 kept in _options_v3, unused.

25 Oct 2026 (Gaddafi file): the user called the flat colour-field thumbnails "very bad" (E: face fading into a plain red field with one
red word; F: plain Libyan-green field with spaced text). Never make plain/flat colour-background thumbnails. Keep a real photo scene filling
the frame behind the face (A-C style was approved: "the thumbnails is good"). Style research: _newchannel/research/thumb_styles/NOTES.md.

**17 Nov 2026: NEW STYLE (supersedes the Hakawi/sparrow looks above).** The owner made refs in ChatGPT and loves them: "66 NAMES. ONE ORDER." (Saddam), "NO WAY HOME", "HE DISAPPEARED", "THEY LEFT ONE WORD", "THE MISSING LINK", "NOT A REAL BODY". They think thumbnails are why the older files stall.
- **Look:**
  - A photoreal cinematic scene. AI is OK here, for places, objects and anonymous men only.
  - The REAL person, big on one side, from an archive photo (B&W or sepia).
  - 2-4 huge distressed condensed words (Anton). Line 2 is white on a torn red brush stroke, or one colour word in yellow, icy blue or red.
  - Story props: a real record as a print, a red hand-drawn circle, a FILE folder.
  - Dark vignette, grain, and the date block (24 Oct rule).
- **Free pipeline:**
  - Folder: `D:\why habibi\_newchannel\_rethumb_nov17\` with `thumbls.py`, `make_all.py` and `CHATGPT_THUMBNAIL_PROMPT.md`.
  - Run with `F:/thumbkit/venv/Scripts/python.exe` (Pillow, MediaPipe 0.10.14; fonts in `F:/thumbkit/fonts`).
  - Backgrounds: the Z-Image stack at `F:/zimage` via `D:/the-bill-explained/tools/zimage.py`, about 4 min per 1344x768 image on the 780M. Queue scripts are in `F:/thumbkit`.
  - The repo copy is `tools/last-hours/thumbls/`.
- **Rules:**
  - Never an AI face for a real person.
  - AI people come out doll-like or androgynous: re-render or drop them (no-women rule).
  - Keep the bottom-right 170x70 px clear.
  - Check every thumbnail at 320x180.
- **Re-thumb round 1 (17 Nov):** 3 variants each for Alcatraz 1962, Cooper, Franklin, Andrée and Roanoke. Leave Saddam alone. Skip Muslim Brotherhood (sensitive).
  - The sheet compares each variant with the CURRENT thumbnail.
  - **17 Nov: the owner said "use those thumbnails".** New thumbnail-only Test & Compare (A/B/C = the new set; the old thumb is out) is LIVE on Alcatraz 16b37-3-Z-Q, Cooper 1rWdT-lGkBI, Franklin bUkhghG5Hs0 and Roanoke EKnsZ8kI_1Q. The old tests had finished with no winner (Franklin's was a title test, also no winner).
  - **Andrée vyX1mYdiWGw: NOT changed.** Its title+thumbnail test was still RUNNING (about 3.5 days left), and stopping it was blocked. The plan, once the owner OKs it: a title+thumbnail test with the same 3 titles paired with the new A/B/C. The other option is to wait for it to end.
  - Check CTR after 7-14 days.
- **Why:** lifetime CTR to 15 Nov: Alcatraz 3.0%, Cooper 2.6%, Franklin 2.2%, Andrée 1.9%, Roanoke 1.6% (Saddam 3.8%).
- **How to apply:** every new and older long file gets 3 variants in this look. Show them, wait for the OK, then add them to Test & Compare against the current thumbnail.
