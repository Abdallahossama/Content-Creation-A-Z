# 14 · @abdaal.dev TikTok teardown (19 Nov 2026)

This is a deep dive into the TikTok channel of **@abdaal.dev** ("عبدال", Egyptian freelance programmer). The owner asked for it: open the channel, watch every video above 10K views, and write down what we learn for codebyabdullah.

He is the closest reference to the owner: an Egyptian programmer filming his desk, selling builds to business owners, with a WhatsApp CTA. The YouTube Shorts analysis of the same creator is in memory: `reference-creators-abdaal-mostfa`.

**Raw material in this repo:**
- `research/abdaal-dev/videos.csv`: all 103 public posts with views, likes, saves, comments, duration and scene cuts.
- `research/abdaal-dev/transcripts.md`: full timestamped transcripts of the 42 videos above 10K.

**Method:**
- `yt-dlp` pulled the channel listing and the videos.
- Whisper large-v3-turbo (int8, CPU) made the Arabic transcripts.
- `ffmpeg scdet` (threshold 12) counted scene cuts.
- A frame contact sheet for each video (dense in the first 4 s, then every 4 s) was read by eye.
- The top post (a photo carousel yt-dlp can't fetch) was opened in Chrome.

Ranking is by **multiple of his own median (8,547 views)**, not raw views. Working files are in `E:\abdaal_analysis\`.

---

## 1. The numbers that matter

| | |
|---|---|
| Posts | 103 (Sep 2025 → Nov 2026) |
| Median views | 8,547 |
| Posts above 10K | 44 (43 %) |
| Biggest | 282K, a 3-photo carousel (33×) |

**By topic** (median views · median save rate · posts above 10K):

| Topic | Posts | Median views | Save rate | Above 10K |
|---|---|---|---|---|
| "How to learn / which language / jobs" (LEARNER) | 26 | **17,900** | 1.42 % | 19 |
| Client business: contracts, servers, deals, pricing (CLIENT-BIZ) | 11 | **15,600** | 1.20 % | 8 |
| "How I built X for a client" (BUILD) | 27 | 5,608 | 0.93 % | 8 |
| Other (vlogs, trends, product teases) | 39 | 7,121 | 0.75 % | 9 |

**Account age matters more than anything else.** The month medians fell from 25–55K (Sep–Nov 2025) to 2–6K (Mar–Jun 2026), then went back up to 9–15K. The early burst was new-account and new-face reach, not a formula. Don't expect his first-month numbers.

### What this means for us
- **His views come from students, not buyers.** LEARNER is his best category, but those viewers will never pay for a clinic system. The owner sells to business owners, so ignore that column ([[positioning-growth-consultant]]).
- **For a seller, CLIENT-BIZ is the gold.** It earns nearly learner-level reach (median 15.6K) and talks about clients. Contracts, servers, a $3,000 deal, pricing and the first client all beat his median 1.6–5.6×.
- **BUILD videos sit below his median on average**, but they have the highest ceiling of any category that brings leads: the CRM got 66.9K (7.8×) and the clinic 42.7K (5.0×). A build only wins when it is a specific business plus a specific pain plus real screens (§3).

---

## 2. Top videos, one line each (why it worked)

| × | Views | Video | What carried it |
|---|---|---|---|
| 33 | 282K | «مسك التراب وخلاه الماس مش دهب» (3 photos) | **Before/after carousel**: slide 1 «أدي الي قلتله عليه مش عاجبه العجب» (the client's old site), slide 3 «مسك التراب بين أيديه» + the new site on a laptop. 1,218 saves and 170 comments. A transformation shown in 3 swipes beats every talking video he has. |
| 11.5 | 98K | «ازاي تتعلم برمجة؟» | A learner roadmap: course names, 31 s, 12 cuts. Saved 3.1 %. |
| 10.5 | 89K | "Programming" | **12 s, no words**, just music + an on-screen line «عملت اكتر من 6 ارقام الشهر الي فات من البرمجه» over desk B-roll. A money claim plus a lifestyle shot. |
| 9.9 | 84K | «ليه خريجين حاسبات مش بيلاقوا شغل؟» | "3 types of students" list; standing next to a printer while talking. |
| 9.6 | 82K | «ليه رفضت 4 جوب أوفر» | A status flex («اتنين في السعودية… الصين… ليبيا»), then «قولولي رأيكم… هتعمل إيه؟» to start a debate. |
| **7.8** | **67K** | **«ازاي عملت أقوى سيستم CRM» (medical reps)** | **Best BUILD.** Open loop in s3 («في آخر الفيديو هقولكم كلف كام»), Excel chaos origin, meetings, a dashboard per role (8 roles), deploy, WhatsApp CTA. |
| 5.6 | 48K | «ازاي بشتري سيرفر للعميل» | **104 s, highest save rate among business topics (3.85 %).** A real task in progress plus FAQs (who pays, buy it on the client's email, a separate card for online payments). Drawn explainer cards on cream paper with a progress bar. |
| 5.0 | 43K | «ازاي عملت سيستم ذكي لعياده دكتور!» | «من ورقة وقلم لسيستم ذكي بضغطة واحدة». Pain by pain: bookings → medical file → **pharmacy stock (“الصداع الحقيقي”)** → finance report. CTA: **«ابعتلي كلمة دكتور على الواتساب وهبعتلك نسخة تجريبية»**. |
| 4.9 | 42K | «ازاي قفلت ديل ب 3000 دولار» | One take on a sofa, 0 cuts: the deal plus faith and motivation (Goethe quote + Quran). A money number in the title does the work. |
| 4.1 | 35K | «ازاي بعمل عقد مع عميل؟» | Starts mid-task «حاليا بعمل عقد… عميل في استراليا». Three clauses: speak business not tech; 3–6 months of maintenance; **15–35 % discount if I'm late**. |
| 3.7 | 31K | «ازاي جبت اول عميل!» | Q&A format (3 questions). His first client **came from a TikTok video with 10K views**, after 2 years of failing on Upwork/Fiverr. |
| 2.1 | 18K | «ازاي عملت موقع لشركه تسويق» | Hook = the buyer's two questions («الموضوع بيمشي ازاي؟ والتكلفة كام؟»), process steps, «تفتكر كلف كام؟ اكتبولي». |
| 1.5 | 13K | «قلدت منصة زد السعودية… وبنيت نسخة احسن» | A famous product name plus side-by-side screens (Zid vs ours), «مين الأحسن؟». |

Duds worth knowing: his 2-minute talking-head opinion pieces («العصر الذهبي انتهى»), the earthquake explainer (11K, but 17 saves: off-niche) and the German-learning platform tease.

---

## 3. The BUILD formula that works (from the CRM, clinic, real-estate and car-app videos)

Every winning build uses the same 6 beats in **45–60 s** with **9–16 cuts**:

1. **Hook = «ازاي عملت/قدرت…» + a specific business + a transformation.** For example «ازاي حوّلت عيادة الدكتور من ورقة وقلم لسيستم ذكي بضغطة واحدة». Standing at the desk, burned-in title for 3–4 s.
2. **Origin in one line: who asked and what they used before.** «العميل كان شغال على إكسيل… لما حجم الداتا كبر كل حاجة بقت فوضى». «كان بيبيع أوفلاين وحب يتوسع».
3. **One process line.** «دخلنا أكتر من ميتنج عشان أفهم السيستم ماشي إزاي». This is where expertise shows, not in tech names.
4. **Screen tour, pain by pain.** Real UI on an iPad/laptop mockup with a fake cursor dot. Each screen gets one sentence tying it to a pain. **Name the pain the owner feels** («الصداع الحقيقي للدكاترة كان المخازن»; «تعرف آخر الشهر كسبت كام بالظبط»).
5. **One "wow" detail.** A quick-search shortcut («الحركة دي عجبت العميل»), a stock alert, an ad-campaign ROI page.
6. **CTA to WhatsApp with his number on screen.** The best version is a **keyword + a free demo** («ابعت كلمة دكتور… وهبعتلك نسخة تجريبية»).

**What separates the 43–67K builds from the 11–13K ones:**
- An **owner pain** (paper, Excel chaos, stock) beats a **feature list** (the car app: «أضاف عربيته… حساب البنزين… متجر», 10.8K).
- An **open loop** («هقولكم كلف كام في الآخر») plus a **cost question** pull comments.
- A **known reference point** (Zid, Shopify ROI) helps, but not more than a clear pain.

---

## 4. Style and production (what the frames show)

- **Setting:** always his home desk: standing desk, 2–3 monitors with code, acoustic foam panels, softbox, headset on. Same room in every video, so the brand is the room.
- **Camera:** handheld or tripod phone at desk height, wide or medium. Many angles per video (over-shoulder typing, front talking, hands on keyboard, screen close-up). No studio look; daylight plus a softbox.
- **Captions:** word-by-word pop captions, white bold with a black stroke, centre-low, with key words in yellow/orange. On the clinic video every caption line is two words with one highlighted in yellow.
- **Logo pops:** PHP, JS, Laravel, Next.js logos pop next to him when he names tech. *(For us: no tech names spoken; a tech card is allowed small and silent, per [[script-feedback-value-and-proof]].)*
- **Screens:** UI shown inside an **iPad frame** on a white or black background, with a grey dot as cursor, screen recording at 1–2× speed.
- **The 104 s server video** is his most designed one: cream-paper explainer cards with a numbered progress stepper (المواقع → مين بيدفع → الكارت → VPS → الجاي), his face in a circle, a hand-drawn diagram. It has the highest business save rate. Explainer cards work for "how it works" topics.
- **Cuts:** learner/list videos run 10–18 cuts (one per item). Opinion/money videos run 0–4 (one take, sitting). Both work. **Dense cuts are not the reason a video wins.**
- **Length:** the winners are 26–63 s. Only the server FAQ (104 s) wins long; the 107–129 s talks are average or below.
- **CTA:** a WhatsApp number in white text with the WhatsApp icon, in the **top half**, on the last 3–5 s. Or "اكتب لينك/كلمة في الكومنتات".

---

## 5. What we take for codebyabdullah (and what we don't)

### Take
1. **A before/after transformation carousel** (his #1 post, 33×). This fits the «ريفيو موقع» series ([[series-website-review]]) perfectly: slide 1 the bad site with a frank line, slide 2 the problem marked, slide 3 the fixed site on a real laptop at the desk. Post the photo version alongside the reel. It costs 20 minutes.
2. **CLIENT-BIZ topics as Trust videos.** These get learner-level reach and speak to buyers: "who pays for the server and why it's on your email", "what's in my contract (late-delivery discount)", "how I price a project". Our week 6 and week 8 Trust scripts and the week 8 pricing Convert are already in this family.
3. **Start mid-task.** «حاليا بعمل عقد…», «حاليا بشتري سيرفر للعميل…». Real work in progress makes it a vlog, not a lecture, and it's instant proof.
4. **Keyword plus a free demo CTA.** «ابعت كلمة دكتور وهبعتلك نسخة تجريبية». We already run the comment-keyword assistant; add a **demo link per niche** (Qyas demo account, Rafiq demo).
5. **Name one owner pain per screen,** and give one of them the line «الصداع الحقيقي كان…».
6. **The cost question / open loop.** «في الآخر هقولك المشروع ده كلف كام» or «تفتكر كلف كام؟ اكتبلي». We don't say prices, so use the loop for something else: «في الآخر هوريك الشكل قبل وبعد» (already in our Reach scripts).
7. **An iPad frame plus a cursor dot for screens.** It's clean and readable on a phone, and easy to batch.
8. **The same room in every video.** The owner's desk setup should become the recognisable set.

### Don't take
- **Learner content** (roadmaps, which language, 6 months). It's his reach engine, but it brings students, not clients.
- **Money and status flexes** («6 أرقام», «رفضت 4 أوفرز», «مليون جنيه»). They get views but go against our rule against borrowed authority and underdog or flex framing ([[content-tone-expert-not-underdog]]), and they attract the wrong audience.
- **Tech names spoken** (React, Laravel, Contabo, Hostinger). The owner's audience doesn't know them.
- **Faith-motivation monologues** as content. That's personal brand for learners, not for clinic owners.
- **Opinion videos over 100 s with no visuals.**

### Open question for the owner
His first client came from a 10K-view video, but most of his reach is learners. Do we want a small learner lane later (one video in ten) for raw reach, or stay 100 % business? The current plan stays 100 % business.
