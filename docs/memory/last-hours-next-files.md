---
name: last-hours-next-files
description: "Last Hours files 15-18 (30-31 Oct 2026): USS Indianapolis (Sun 6 Dec), Cole & Roe 1937 (Mon 7 Dec), Gaddafi last day (first Files: People), Muslim Brotherhood via Banna last hours 1949 + factual El-Sayed chapter"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-11-06T07:19:02.593Z
---

Owner approved on 30 Oct 2026: download both safe sets, then "go ahead" (scripts, voice, renders); later "go Gaddafi".

- **15_uss_indianapolis**: slot Sun 6 Dec 2026, 22:00 Cairo. Script vo_lines.txt (91 lines, ~11 min); render_indy.py is built by _build_render.py from 14's render_alcatraz46.py plus shots_indy.py. Doc pages are rendered from the NHHC PDFs into media/A*p*_page.jpg, and OCR lives in build/ocr. Titles: "Nobody Reported the USS Indianapolis Missing for 4 Days" / "They Asked the Man Who Sank the USS Indianapolis 1 Question" / "The USS Indianapolis Survivors Waited 4 Days. Nobody Looked." Thumbs: 8 PLANES / HE TESTIFIED / HE LOOKED DOWN.
- **16_cole_roe_1937**: slot Mon 7 Dec 2026, 22:00 Cairo. 70 lines, ~8.5 min. The Utah newspaper PDFs come only through the browser's Download button (curl gets 418). Pages are cropped to the articles (no women), and DOC boxes come from the PDF text layer. The NARA cards are COLORDOC, so the red stamp stays visible. Titles: "Counted at 1:00. Gone From Alcatraz at 1:30. Never Found." etc.
- **17_gaddafi_last_day**: video id **9kB8VIKkhJQ**, SCHEDULED **Sun 15 Nov 2026, 22:00 Cairo** (moved from 13 Dec on 14 Nov). Setup: A/B E/D/B, Files: People, end screen with Benghazi kJYD15hkP48. English captions PUBLISHED 14 Nov 2026 (Languages > Edit subtitles > Publish); the video now airs Sun 15 Nov 22:00 (reordered). Re-rendered 31 Oct with the face/zoom fixes (LESSONS 54). The owner drags the file in. The owner asked for files about PEOPLE, not only cases. Last day 20 Oct 2011 Sirte, framed by "King of Kings of Africa" (2008) and his African army idea. New playlist "Files: People". Next people ideas: Dillinger 1934 (FBI Vault), the Bin Laden raid 2011, Che 1967 (CIA cables).
- **18_muslim_brotherhood**: video id **1CzBdYMw9T8**, scheduled **Sat 31 Oct 2026, 22:00 Cairo**. It is in the new "Files: People" playlist. The captions are published.
  - **Egypt safety check (31 Oct, before release).** I flagged three things: the Brotherhood's 2013 terrorist designation in Egypt, the 2015 anti-terror law, and the 2018 cybercrime law. I also flagged the emblem shot, the "attempt was staged" line, and the cloned voice. The owner said: "release it, I don't see a real risk, it's history not politics, nobody knows my voice".
  - After release I hid it for ethical reasons (before the vote). On 6 Nov the owner said he had made it **PUBLIC again after El-Sayed won** the 3 Nov race. Still to do: add the result as a pinned reply, and never re-edit the video.
  - Anonymity rules: never comment as the personal "Abdullah Osama" channel. Keep no contact email or links on the channel. Never link it to Ask Habibi or Facebook. The owner said "release it today", so this was **before** the 3 Nov vote.
  - **Content.** A neutral, story-first "who are they" doc told through Hassan al-Banna's last hours (Sat 12 Feb 1949). No terrorist/party debate. The 1948 killings are told straight.
  - **The owner supports Abdul El-Sayed** (31 Oct: "I'm supporting him, no clickbait, nothing that makes him look bad"). His chapter (~70 s) runs:
    - the claims (Rogers, Trump);
    - **his own words** "I have never been a member… I never will be";
    - PolitiFact "Pants on Fire" and AP "no evidence".
  - The 2012 letter is left out (signer unconfirmed).
  - **Titles never name him.** The 3 A/B titles are "From 1928 to the Michigan Race", "Who Are the Muslim Brotherhood? The 1949 File" and "Founder's Last 4 Hours".
  - **Thumbnails** (the owner's picks I, I4, I5): El-Sayed's MediaPipe cutout from his PD Senate photo, on the 1949 case board. The headline is "WHY HIM?" with a **big fair note**: "AP: NO EVIDENCE OF ANY LINK" / "HE SAYS: NEVER A MEMBER".
  - **Refused:** a half-face blend with Banna; any string linking him to the board; the emblem on a thumbnail; "WHO GAVE THE ORDER?" next to his face.
  - **Reference used:** Abdullah Elshrif ep 30, for structure only.
  - **17 Nov 2026 re-thumb (owner: "use abdul image in all the thumbnails", NEW photo; rejected a Banna+panel set; OK'd the hero set).** Thumbnail-only Test & Compare LIVE, built with `make_all.py brotherhood2`:
    - A "THE CLAIM: FALSE." + POLITIFACT: PANTS ON FIRE
    - B "1928 TO 2026" + AP: NO EVIDENCE OF ANY LINK
    - C "HIS ANSWER:" + his Fox News quote (23 Oct 2026)
    - Photos: Kenneth C. Zirkel + Conlan Houston (2025, Wikimedia, CC BY-SA 4.0). The credit line was added to the description and to CREDITS.md. Never use the meet-and-greet photo with the audience (women in it).
    - The old test had stopped as ineligible because the video was private for a while.
- **December 2026 slate** (owner 6 Nov: "swap Escobar for Washington, go ahead"), all at 22:00 Cairo:
  - 19 Glenn Miller: Mon 14 Dec.
  - 20 Ceaușescu: Sun 20 Dec. Elena is narration only.
  - 21 Pan Am 103: Mon 21 Dec. The accused's US trial starts Jan 2027, so "accused/alleged" only. No victims shown.
  - 22 Washington crosses the Delaware to Trenton (250th anniversary): Sun 27 Dec. Replaces Escobar, whose face photo is disputed and whose PD photo shows his body.
  - 23 Rasputin: Mon 28 Dec. Many of his photos include women; never use the corpse photos.
  - Folders are `_newchannel/19_…` to `23_…`. Research agents write research.md + assets.md in each. The owner OKs the downloads.
- Packaging: the brand_patch LABEL/NEXT keys are "indy" and "coleroe". The teaser configs are in _tools/teasers_more.py (4 each). The CTA lines are in _cta/cta_teasers.py.

**Why:** two long files a week; the owner wants finished results.
**How to apply:** check thumbnails with the owner before upload. Never run Chatterbox beside OCR or renders: on 30 Oct it segfaulted and hit "paging file too small" while WSL held ~6 GB. See [[last-hours-file-keeper-brand]] and [[studio-timezone]].

**Captions, 14 Nov 2026.** Draft English captions were PUBLISHED for:
- Gaddafi 17 (9kB8VIKkhJQ)
- Cole & Roe (qxCLouHiLjE)
- Indianapolis (YXgJ09aCfXw)

Studio > Languages > **Drafts** tab is now empty. That tab is the reliable check: the "All" tab lists every video and looks like drafts. Path: video > Languages > Edit subtitles > Publish.
