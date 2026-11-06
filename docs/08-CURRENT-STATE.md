# Current state (30 Oct 2026): update this file whenever the schedule changes

## The Last Hours: long files (22:00 Cairo; Studio field = Cairo time since 29 Oct)
| Date | File | Video ID | Notes |
|---|---|---|---|
| live | Alcatraz | 16b37-3-Z-Q | title A/B running |
| live | Roanoke | EKnsZ8kI_1Q | |
| live | Franklin | bUkhghG5Hs0 | title A/B: old vs "The Franklin Expedition: …" |
| live | D.B. Cooper | 1rWdT-lGkBI | end screen 31 Oct: playlist box → Alcatraz video (end-screen CTR was 0 % vs Franklin 4 %); now Subscribe + Franklin + Alcatraz |
| **Sat 31 Oct 22:00** | **18 The Muslim Brotherhood / Banna's last hours** | 1CzBdYMw9T8 | SCHEDULED 31 Oct ~19:20; title+thumb A/B (I / I4 / I5, titles without El-Sayed); new playlist "Files: People" (created 31 Oct); end screen Cooper + Subscribe + Alcatraz (imported from Cooper); English captions PUBLISHED (after processing; publishing during upload fails, save as draft first); pin + heart at 22:00 |
| **Sun 1 Nov** | Saddam / al-Khuld Hall | 79Wix9PwPpY | MOVED from Mon 2 Nov (owner 31 Oct: 2 a week; today MB, tomorrow Saddam); owner keeps current A/B; Studio date changed 31 Oct ✅ |
| Sun 8 Nov | Andrée balloon | vyX1mYdiWGw | pair 2 title = "Andrée's Balloon: …" |
| Mon 9 Nov | Gaddafi / Benghazi stadium | kJYD15hkP48 | |
| Sun 15 Nov | Flight 19 | r0wpGQzHVJ8 | |
| Mon 16 Nov | USS Cyclops | eyc6dLMqf-U | |
| Sun 22 Nov | EgyptAir 990 | AIbcwBZsxdY | title A/B (old vs "EgyptAir 990: …") |
| **Mon 23 Nov** | Flannan Isles | Rz0qyy9-7GE | MOVED from Sun 1 Nov (owner 31 Oct; Studio date changed 31 Oct ✅); title+thumb A/B (new name title + E2); its end card still says "next: Saddam" (already out by then: fine) |
| Sun 29 Nov | **Göring's last night** (file 13) | XJYc9KLbzJ0 | scheduled 29 Oct; title+thumb A/B (mix: 1 B&W + 2 colour); English captions saved as draft, publish after processing |
| Mon 30 Nov | **Battle of Alcatraz 1946** (file 14) | MiC9JTGkWq8 | File Keeper render; title+thumb A/B (A_KEY_107 B&W + 2 colour); teasers SCHEDULED 19:00: T1 KpQ1WWaIXLg Tue 1 Dec, T2 sjP79gckYY4 Thu 3 Dec, T3 KunZPPLxYlU Sat 5 Dec (Related video → MiC9JTGkWq8 after 30 Nov 22:00) |

All 9 above = the **File Keeper re-uploads of 30 Oct** (old ids Private as "OLD COPY (delete)" for the owner; table in
`_upload_queue_last_hours/branded/REUPLOAD_PLAN.txt`). When each goes public: Shorts related links + pinned comment → new id.

## Shorts gap 23-29 Nov: FILLED 30 Oct (19:00 Cairo, teasers_more.py)
EgyptAir AdZ95n42xwI 23 · _w492FOuMUU 25 · rTYz0T8oPtk 27 (related → AIbcwBZsxdY after 22 Nov) · Cyclops ccw9IAFC6fI 24 ·
rglfPKhCUpM 26 · L0YS7Y3U2Gg 28 · vC0fLGBtvxU 29 (related → eyc6dLMqf-U after 16 Nov). Teaser tool: per-file `wfix` table for
whisper's clock times ("149 | and | 45." → "1:49:45.").

## Ask Habibi: STOPPED (30 Oct 2026)
Owner: content only for The Last Hours. Ask Habibi-only folders moved to `D:\why habibi\_ASK_HABIBI_ARCHIVE (delete me)` (1.6 GB) next to the
older `E:\why habibi OLD ask habibi (delete me)` (36 GB); the owner deletes both. Shared tools stay (see docs/06 header).

## Next long files (in production since 30 Oct: owner "yes download both and go ahead", then "go Gaddafi")
| Slot | File | State |
|---|---|---|
| Sun 6 Dec 22:00 | 15 USS Indianapolis 1945 | **YXgJ09aCfXw SCHEDULED 6 Nov** (A/B title+thumb A/B/C COLOR + 3 titles, Files: Escapes and Disappearances, end screen Subscribe + Cyclops eyc6dLMqf-U + Cole & Roe qxCLouHiLjE, captions draft -> publish after processing); 35/35 downloaded; script 91 lines (~11 min, hook 86); VO done, 4 lines re-voiced; render_indy.py (from render_alcatraz46 + shots_indy.py); 3 A/B thumbs drafted (8 PLANES / HE TESTIFIED / HE LOOKED DOWN); 4 teasers planned |
| Mon 7 Dec 22:00 | 16 Cole & Roe, Alcatraz 1937 | teasers SCHEDULED 19:00: T2 x23BFO50yLY Tue 8 Dec, T3 SI5hP4pC7C4 Thu 10 Dec, T4 6AU17rfV-04 Sat 12 Dec (T1 needs re-cut); **qxCLouHiLjE SCHEDULED 6 Nov** (A/B title+thumb A/B/C COLOR + 3 titles, Files: Escapes and Disappearances, end screen Subscribe + 1962 FBI 16b37-3-Z-Q + Alcatraz 1946 MiC9JTGkWq8, captions draft replaced the auto ones -> publish after processing); 28/28 downloaded (Utah PDFs via the browser's Download button: curl gets 418); pages cropped to the articles; script 70 lines (~8.5 min, hook 77); render_coleroe.py; thumbs drafted (WHERE DID THEY GO? / DROWNED? OR FREE? / NEVER FOUND) |
| **Sun 13 Dec 22:00** | 17 Gaddafi's last day (20 Oct 2011, Sirte) | **9kB8VIKkhJQ SCHEDULED 31 Oct** (A/B E/D/B + 3 titles, Files: People, end screen Benghazi kJYD15hkP48 + Subscribe + Alcatraz, captions draft -> publish after processing); owner 31 Oct "ok 13 Dec"; RE-RENDERED 31 Oct with the face/zoom fixes (lesson 54), in _upload_queue_last_hours/FILE17_GADDAFI_slot_tbd; thumbs E/D/B + titles APPROVED; 60 assets in (13 real CC BY/PD clips, all checked: men only); script 61 lines (~8 min; hook "king of kings of Africa"; Clinton "captured or killed soon" as narration); thumbs E (ONE AFRICA. ONE KING.) + D + B proposed; VO next (Chatterbox alone) |
| after the 3 Nov vote | 18 The Muslim Brotherhood: Banna's last hours (Sat 12 Feb 1949, Cairo) | owner "go ahead" 31 Oct. Story-first "who are they" doc, no terrorist/politics debate; 1948 events (jeep case, PM Nuqrashi shot) told straight as plot twists. Owner wants Abdul El-Sayed (Michigan Senate nominee) in it for reach: factual only (hook line + ~45 s last chapter: Jan 2026 US labels on 3 branches, the Rogers/Trump claims, the 2012 letter, his denial, fact-checks; no opinion). Thumbs: A Banna + logo + MUSLIM BROTHERHOOD; B El-Sayed + ACCUSED stamp only with a PD photo. Refused: Banna + logo + El-Sayed in one row (reads founder to member). Reference: Abdullah Elshrif ep 30 (structure only). Research agent running |
Thumbnails go to the owner before upload. People-file ideas for later: Dillinger 1934, the Bin Laden raid 2011, Che 1967.

## Shorts (daily 19:00 Cairo)
27 Oct → 22 Nov scheduled: standalone mystery Shorts (Alcatraz CTA), Cooper ×3 on 2-4 Nov, Wow/Somerton/Tunguska 5-7 Nov,
Saddam/Andrée/Gaddafi/Flight 19/Franklin teasers to 22 Nov. Re-cut 29 Oct: Cooper Short NxwUdovTFrw (31 Oct) and Flannan Short
Lr0iaGmD4kE (1 Nov) end on their own long files (old copies Private).

## Open tasks
- THUMBNAIL PLAN (owner, 30 Oct): a dedicated plan later; click-through (2.6-2.8 %) is the bottleneck, retention is fine.
- FILE KEEPER RE-BRAND (30 Oct): 8 scheduled long files patched (_cta/brand_patch.py) and re-uploaded on the same dates; Alcatraz 1946 branded in its render.
- Related-video links (picker lists PUBLIC videos only; NxwUdovTFrw → 1rWdT-lGkBI done 30 Oct): Lr0iaGmD4kE (Flannan Short, MOVED 31 Oct to Tue 24 Nov 23:00 Cairo: 19:00 that day is a Cyclops Short) → Rz0qyy9-7GE after 23 Nov 22:00;
  Saddam teasers → 79Wix9PwPpY after 1 Nov 22:00; Gaddafi → _A_Ae9ddTSI after 9 Nov; Andrée → D6AbVT_ODoM after 8 Nov; Flight 19 → Sd9q1pKG4LM after 15 Nov.
- Pin + heart each new video's comment on its day (texts in `docs/the-last-hours/PINNED_COMMENTS.txt` and each teaser sheet).
- Göring (-5GSUfE4PEY): English captions published 30 Oct; pin + heart on 29 Nov.
  3 teaser Shorts SCHEDULED 30 Oct (19:00 Cairo): T1 xoFhkNH8cN0 Mon 30 Nov, T2 Pi5wwPxSBS4 Wed 2 Dec, T3 -430uUw_W7s Fri 4 Dec.
  After 29 Nov 22:00: related video -> -5GSUfE4PEY on all 3 (the picker lists public videos only); pin + heart each on its day.
- Shorts gap: nothing scheduled 23-29 Nov.
- Check Franklin/Cooper impressions after the title tests; ideas kept: Battle of Alcatraz 1946, Cole & Roe 1937, Oswald's last 48 hours.
- 31 Oct 22:03: File 18 Muslim Brotherhood (1CzBdYMw9T8) PUBLIC; prepared comment posted as @TheLastHoursDocs, pinned + hearted.

## December 2026 slate (owner 6 Nov: "ok swap escobar for washington, go ahead")
| Slot (22:00 Cairo) | File | Folder | State |
|---|---|---|---|
| Mon 14 Dec | 19 Glenn Miller vanishes, 15 Dec 1944 | 19_glenn_miller | research agent running (research.md + assets.md) |
| Sun 20 Dec | 20 Ceausescu's last days, 21-25 Dec 1989 | 20_ceausescu_last_days | research agent running |
| Mon 21 Dec | 21 Pan Am 103 / Lockerbie, 21 Dec 1988 | 21_pan_am_103 | research agent running; accused's US trial Jan 2027: "accused/alleged" only |
| Sun 27 Dec | 22 Washington crosses the Delaware -> Trenton, 25-26 Dec 1776 (250th) | 22_washington_trenton | research agent running (replaces Escobar) |
| Mon 28 Dec | 23 Rasputin's last night, 29-30 Dec 1916 | 23_rasputin_last_night | research agent running |
Next: owner OKs the download lists -> scripts -> voice -> renders -> thumbnails (owner) -> uploads. Research summary: docs/the-last-hours/research/DECEMBER_2026_TOPICS.md
