---
name: second-channel-money-plan
description: "Ask Habibi channel REBRANDED 15 Nov 2026 to The Bill, Explained (@TheBill.Explained, same channel ID); everyday-America economics; EP1 Diesel + 2 Shorts scheduled 18-20 Nov"
metadata:
  node_type: memory
  type: project
  originSessionId: dd4ea468-cfe1-4e18-822b-fae3d192e994
  modified: 2026-11-15T14:28:57.487Z
---

15 Nov 2026: owner wants the second channel (Ask Habibi, stopped 30 Oct) to make money from US viewers, maybe "YouTube automation"/faceless. The Last Hours stays unchanged.

Recommendation given (full doc: `docs/12-SECOND-CHANNEL-PLAN.md` in [[content-creation-repo]]):
- Niche #1 = everyday-America economics ("Why X Costs $Y", "How X Really Makes Money"), with series "Follow the Money" (maps) and "The Price of Power" (PD military/space photos). Est. US RPM $8-25.
- Runner-ups: money-number world maps, personal finance (YMYL risk), corporate collapses, big-money machines.
- NEW channel, not a rebrand; leave Ask Habibi online.
- Long-form first: 1 long/week Wed 19:00 Cairo + 2 money-number Shorts. US Shorts RPM ~$0.33 vs long ~$2.3+, and Shorts watch time doesn't count for the 4,000 h.
- Policy guard: YPP "inauthentic content" (Jul 2025) + Jul 2026 ban on AI "expert" personas for finance, so every video needs original research, 5+ sources on screen, varied structure, and a storyteller narrator. Own cloned voice needs no AI label.
- Outliers (Modern MBA, How Money Works): 13/15 use "The Question" title formula.

**Why:** money-number Shorts were Ask Habibi's only wins ([[shorts-title-money-hook]]); the long videos failed from topic spread and brand mismatch.
**How to apply:** don't create/rename channels or touch YouTube Studio until the owner OKs. Once the owner approves, script with yt-script and reuse the s01/s03 map engine + Chatterbox ([[local-ai-stack]]). Keep [[no-women-in-visuals]] (shopper photos are risky, so use objects, buildings, men only), [[real-not-cartoon]], [[copyright-safe-only]]. The Last Hours keeps priority ([[focus-last-hours]]).

**15 Nov 2026, owner: "Yes, new channel"** -> APPROVED: niche #1 + a NEW channel (Ask Habibi stays online, untouched). Name still open.
Name shortlist (handles that returned 404 on youtube.com on 15 Nov, so probably free; confirm in YouTube's handle field):
The Bill, Explained (@TheBillExplained, my pick) / The Real Price Of (@RealPriceOf) / Paid For (@PaidForChannel). Owner creates the channel in their own account; I don't.
**NAME CHOSEN 15 Nov 2026** (owner: "u pick"): **The Bill, Explained**, handle @TheBillExplained. Owner creates the channel in their own Google account.
**Brand kit built 15 Nov 2026** in `D:\the-bill-explained\` (BRAND.md; tools/brandkit.py renders logo/banner/watermark, tools/thumbkit.py renders thumbnails). Look: a torn receipt priced "$?.??", TOTAL row in yellow highlighter, price red #D62820, ink, paper; thumbnails = real object + red price tag + optional 2-4-word receipt strip. Fonts: Arial Black, Impact, Consolas. Awaiting the owner's look verdict.

**Episode #1 RENDERED 15 Nov 2026** (owner: "make the first video... finish the whole thing"):
- Long: `D:\the-bill-explained\videos\01_diesel\export\TheBillExplained_01_Diesel.mp4`, 7:41, 1080p, -16 LUFS.
- Shorts: `shorts\s1_gap` ($2.13, 0:41) and `shorts\s2_semi` ($32,800, 0:37).
- Thumbnails A (nozzles) and C (night station). Upload sheets are in `export\` and `shorts\`.
- Planned slots: long Wed 18 Nov 19:00 Cairo; Shorts Thu 19 + Fri 20 Nov 19:00. They need the owner to create the channel first and to upload in Studio.
- Engine: `tools/billvid.py` (+ `vo_chatterbox`, `transcribe_lines`, `fix_lines`, `thumbkit`).
- Process + lessons: `D:\the-bill-explained\LESSONS.md`.
- Hard lesson: C: at 0 GB crashed Chatterbox. Route `TMP` to D:, and run one heavy job at a time.

**15 Nov 2026 evening: REBRANDED the Ask Habibi channel instead of opening a new one.** The owner said new channels keep asking for a phone number, and they have only a few.
- Channel ID `UCJXUO3S0AtoQvmWHqpGp_ow`, now named **The Bill, Explained**, handle **@TheBill.Explained**. @TheBillExplained was taken.
- New description, receipt logo, banner and watermark are published.
- All 24 old Ask Habibi videos (12 long + 12 Shorts) set to **Private**: owner OK, reversible, nothing deleted.
- Playlist "The Bill, Explained" created.
- Scheduled (19:00 Cairo):

  | Date | Video | ID | Notes |
  |---|---|---|---|
  | Wed 18 Nov | Long "Why Diesel Costs $2 More Than Gas Right Now" | mJuihLRaZnI | thumbnail A/B test A nozzles vs C station; end screen subscribe + best-for-viewer; timed SRT captions uploaded |
  | Thu 19 Nov | Short 1 | zT7Uc-yy54s | |
  | Fri 20 Nov | Short 2 | cDs8LfpRhHM | |

- Still to do after the long video goes public: set each Short's Related video to mJuihLRaZnI, post/pin/heart the comments, and check the captions show as Published.

**15 Nov 2026 ~19:30 Cairo: owner said "lets upload today". New publish status:**
- **LIVE now:** EP1 long mJuihLRaZnI. Our timed English (US) captions are confirmed on the watch page; the thumbnail A/B test runs from now. Comment posted, pinned and hearted.
- **LIVE now:** Short 1 zT7Uc-yy54s. Related video = EP1; comment pinned and hearted.
- **Scheduled Mon 16 Nov 19:00 Cairo:** Short 2 cDs8LfpRhHM, related video = EP1. Its comment still has to be posted, pinned and hearted after it goes live: "Truckers: does your fuel surcharge cover it? Tell us below."
- **Next checks:** impressions/CTR/retention on day 2-4. Retitle flat Shorts after ~1 day. Next long episode = Wednesday slot.

**16 Nov 2026: EP2 "Why Your Power Bill Jumped $43 (It's Partly AI)".** Owner asked for "video inside the video, not only images" and a trending/viral idea, so EP2 = AI data centers on your electric bill, built mostly from stock video clips (billclip.py `VID` shots). Folder: D:/the-bill-explained/videos/02_ai_power (export/ has the upload sheet, thumbs A servers "+$43" / B meters "$157", SRT; CREDITS.md). 2 Shorts: s1_homes (80,000 homes), s2_auction (NJ +$26). Proposed slot Wed 18 Nov 19:00 Cairo; upload/schedule needs the owner's OK.
- **16 Nov: EP2 uploaded as hSjrHI-tGLk, scheduled PUBLIC Mon 16 Nov 22:00 Cairo** (owner: "upload today at 10 pm"). Thumbnail A servers "+$43"; playlist The Bill, Explained; timed SRT published; end screen = subscribe + EP1. After 22:00: post/pin/heart the EP2 comment (upload sheet). EP2 Shorts not uploaded yet.
- Owner asked for a "Hexfield" (= Higgsfield AI) thumbnail. The Higgsfield connector works but the account has 0.01 credits / free plan, no unlimited gens; 1 image = 1.5 credits. Needs credits (owner's call; no-spend rule) or a free alternative.
- 16 Nov: EP2 thumbnail swapped to R1 real Ashburn aerial (thumbs_real). EP2 Shorts uploaded: Short 1 nv2T6IpWzs4 (public Tue 17 Nov 19:00), Short 2 yMcm-lEQ-eA (public Wed 18 Nov 19:00). TODO after EP2 is public: set both Shorts' Related video = hSjrHI-tGLk (picker is empty while EP2 is private); post/pin/heart comments from the CHANNEL account (Chrome YouTube is signed in as the owner's personal account; a 16 Nov comment went out from it by mistake and vanished).
