---
name: last-hours-next-files
description: "Last Hours files 15-17 in production (30 Oct 2026): USS Indianapolis (Sun 6 Dec), Cole & Roe 1937 (Mon 7 Dec), Gaddafi's last day (first \"Files: People\" file)"
metadata:
  node_type: memory
  type: project
  originSessionId: eff32ef8-e3b2-4b1b-abb9-4566220676dd
  modified: 2026-10-30T14:05:28.411Z
---

Owner approved on 30 Oct 2026: download both safe sets, then "go ahead" (scripts, voice, renders); later "go Gaddafi".

- **15_uss_indianapolis**: slot Sun 6 Dec 2026, 22:00 Cairo. Script vo_lines.txt (91 lines, ~11 min); render_indy.py is built by _build_render.py from 14's render_alcatraz46.py plus shots_indy.py. Doc pages are rendered from the NHHC PDFs into media/A*p*_page.jpg, and OCR lives in build/ocr. Titles: "Nobody Reported the USS Indianapolis Missing for 4 Days" / "They Asked the Man Who Sank the USS Indianapolis 1 Question" / "The USS Indianapolis Survivors Waited 4 Days. Nobody Looked." Thumbs: 8 PLANES / HE TESTIFIED / HE LOOKED DOWN.
- **16_cole_roe_1937**: slot Mon 7 Dec 2026, 22:00 Cairo. 70 lines, ~8.5 min. The Utah newspaper PDFs come only through the browser's Download button (curl gets 418). Pages are cropped to the articles (no women), and DOC boxes come from the PDF text layer. The NARA cards are COLORDOC, so the red stamp stays visible. Titles: "Counted at 1:00. Gone From Alcatraz at 1:30. Never Found." etc.
- **17_gaddafi_last_day**: the owner asked for files about PEOPLE, not only cases. Last day 20 Oct 2011 Sirte, framed by "King of Kings of Africa" (2008) and his African army idea. New playlist "Files: People". Next people ideas: Dillinger 1934 (FBI Vault), the Bin Laden raid 2011, Che 1967 (CIA cables).
- Packaging: the brand_patch LABEL/NEXT keys are "indy" and "coleroe". The teaser configs are in _tools/teasers_more.py (4 each). The CTA lines are in _cta/cta_teasers.py.

**Why:** two long files a week; the owner wants finished results.
**How to apply:** check thumbnails with the owner before upload. Never run Chatterbox beside OCR or renders: on 30 Oct it segfaulted and hit "paging file too small" while WSL held ~6 GB. See [[last-hours-file-keeper-brand]] and [[studio-timezone]].
