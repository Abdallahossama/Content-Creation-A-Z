---
name: last-hours-next-files
description: "Last Hours files 15-18 (30-31 Oct 2026): USS Indianapolis (Sun 6 Dec), Cole & Roe 1937 (Mon 7 Dec), Gaddafi last day (first Files: People), Muslim Brotherhood via Banna last hours 1949 + factual El-Sayed chapter"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-31T12:08:16.123Z
---

Owner approved on 30 Oct 2026: download both safe sets, then "go ahead" (scripts, voice, renders); later "go Gaddafi".

- **15_uss_indianapolis**: slot Sun 6 Dec 2026, 22:00 Cairo. Script vo_lines.txt (91 lines, ~11 min); render_indy.py is built by _build_render.py from 14's render_alcatraz46.py plus shots_indy.py. Doc pages are rendered from the NHHC PDFs into media/A*p*_page.jpg, and OCR lives in build/ocr. Titles: "Nobody Reported the USS Indianapolis Missing for 4 Days" / "They Asked the Man Who Sank the USS Indianapolis 1 Question" / "The USS Indianapolis Survivors Waited 4 Days. Nobody Looked." Thumbs: 8 PLANES / HE TESTIFIED / HE LOOKED DOWN.
- **16_cole_roe_1937**: slot Mon 7 Dec 2026, 22:00 Cairo. 70 lines, ~8.5 min. The Utah newspaper PDFs come only through the browser's Download button (curl gets 418). Pages are cropped to the articles (no women), and DOC boxes come from the PDF text layer. The NARA cards are COLORDOC, so the red stamp stays visible. Titles: "Counted at 1:00. Gone From Alcatraz at 1:30. Never Found." etc.
- **17_gaddafi_last_day**: the owner asked for files about PEOPLE, not only cases. Last day 20 Oct 2011 Sirte, framed by "King of Kings of Africa" (2008) and his African army idea. New playlist "Files: People". Next people ideas: Dillinger 1934 (FBI Vault), the Bin Laden raid 2011, Che 1967 (CIA cables).
- **18_muslim_brotherhood**: released **Sat 31 Oct 2026, 22:00 Cairo**. The owner said "release it today", so this was **before** the 3 Nov vote.
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
- Packaging: the brand_patch LABEL/NEXT keys are "indy" and "coleroe". The teaser configs are in _tools/teasers_more.py (4 each). The CTA lines are in _cta/cta_teasers.py.

**Why:** two long files a week; the owner wants finished results.
**How to apply:** check thumbnails with the owner before upload. Never run Chatterbox beside OCR or renders: on 30 Oct it segfaulted and hit "paging file too small" while WSL held ~6 GB. See [[last-hours-file-keeper-brand]] and [[studio-timezone]].
