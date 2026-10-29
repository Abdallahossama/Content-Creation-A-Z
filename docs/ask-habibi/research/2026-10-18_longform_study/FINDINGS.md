# Long-form study, 18 Oct 2026 (yt-viral): which questions make a LONG video break out for a small channel

## 1. Our own numbers (YouTube Studio, Reach tab, since publish)
| Video | Impressions | CTR | Views | Avg viewed | Main traffic |
|---|---|---|---|---|---|
| Ep 1 Why Do Embarrassing Memories Attack You at 3 AM? | 431 | 1.6% | 20 | 47.6% | 98% recommended (next to unrelated videos) |
| Ep 2 Why Can't You Sleep Without a Video On? | 245 | 0.8% | 8 | 27.4% | 91% recommended |
| Ep 4 The 2 Tiny Straits Behind Your Gas Price | 42 | 2.4% | 15 | 24.5% | barely tested |
Shorts for comparison: Hormuz map Short 850 views, "cringe at 3 a.m." Part 1 520 views.

**Diagnosis:** YouTube did show the long videos (431 and 245 times), but ~1 in 100 people clicked, so it stopped. Ep 1 even
holds viewers well (47.6%). The problem is the click: topic + title + thumbnail, not the edit.

## 2. Market scan (public search, videos from 2026, 4-20 min; 45 question-type queries in both lanes)
1,620 search hits -> 1,529 long-form with channel data; **831 from small channels (<100k subs), 740 channels.**
Multiple = the video's views over that channel's median of its last 30 uploads. Search returns videos that already rank,
so absolute "breakout rates" are inflated; compare the question types to each other, not to zero.

### Curiosity lane (body / brain / sleep / psychology), small channels
| Question type | n | Median multiple | Share >= 3x | Views per subscriber |
|---|---|---|---|---|
| **The psychology of people who...** | 25 | **91x** | 84% | 21 |
| **Why do/did humans... / Why does your brain...** | 103 | **18x** | 81% | 9.6 |
| The real reason you... | 19 | 10x | 63% | 7.4 |
| **What happens to your body when/if you...** | 62 | 8x | 63% | 4.0 |
| How your brain/body... | 56 | 5x | 54% | 3.0 |
| Can you really... | 28 | 2.4x | 43% | 0.5 |
| Is it bad/normal to... | 60 | 1.9x | 42% | 0.7 |
| What if... | 40 | 1.3x | 32% | 3.0 |

### Geo/news lane, small channels (much weaker for small channels)
| Question type | n | Median multiple | Share >= 3x |
|---|---|---|---|
| Where... (mystery places) | 39 | 3.3x | 54% |
| Who controls/owns... | 45 | 2.7x | 47% |
| How did [city/tiny country] become... | 86 | 2.1x | 44% |
| Explained on a map | 84 | 1.7x | 35% |
| Why does [country]... | 80 | 1.7x | 31% |
| What happens if [country]... | 52 | 1.1x | 25% |

### Length and channel size (small channels)
- 4-8 min: median 2.2x; **8-12 min: 3.1x; 12-20 min: 3.0x.** Our long videos are 5-8 min.
- 1k-10k subs channels break out most (median 7.2x).

### Top breakouts (small channels)
| x | Views | Subs | Title (type) |
|---|---|---|---|
| 13,789x | 2.1M | 7.7K | What Happens If You Eat Only Once a Day — Inside Your Body (what happens, 3D) |
| 2,849x | 1.1M | 1.2K | Why Are Humans So Much Weaker Than Other Animals? (why humans) |
| 2,612x | 635K | 7.4K | Psychology of People who Imagine FAKE Scenarios (psychology of) |
| 1,950x | 915K | 3.1K | What Did Ancient Humans Do For Pleasure? (ancient humans) |
| 1,665x | 482K | 4.7K | Your Body EATS ITSELF When You Exercise Hungry (3D animation) |
| 1,088x / 453x / 393x | 147K / 326K / 483K | 461 / 1.9K / 2.4K | "Why Did Humans Start Wearing Clothes?" (three different tiny channels) |
| 572x | 859K | 25K | Every Type Of Sleep Explained |
| 460x | 6.2M | 83K | How Did Tokyo Become The Largest City On Earth? (geo, how did X become) |
Formula labels (swipe.py) among outliers: mostly "The Question" or unclassified; a judgement about the title only.

**The one shared thing:** the question is about **YOU / HUMANS in an everyday situation** (your body when you eat, sleep,
exercise; people who do a relatable thing; how ancient humans did a normal thing), not about a topic or a place.
Our long titles were about a feeling or a news topic ("embarrassing memories", "can't sleep without a video",
"2 tiny straits"), which reads niche in a recommendation feed.

## 3. What to make next (long form, 8-12 min, curiosity lane; keep news for Shorts)
| # | Title (title.py) | Type | Why it fits us |
|---|---|---|---|
| 1 | How Did Ancient Humans Sleep? (94) | why/how ancient humans | proven demand (ancient-humans titles break out on tiny channels), midnight lane, strong history receipts (segmented "first and second sleep") |
| 2 | What Happens To Your Body When You Sleep 4 Hours (94) | what happens to your body | 3D Batata body format = the 3D-animation breakouts; sleep lane; clear stakes |
| 3 | The Psychology of People Who Stay Up Late (76, longer title) | psychology of people who | the strongest type in the scan; identity hook; night lane |
Also: re-test Ep 1/Ep 2 titles in this shape when the current A/B tests end, e.g. "The Psychology of People Who Replay
Conversations at Night" and "The Psychology of People Who Need a Video On to Sleep".

Files: `collect_long.py`, `hits.json`, `analyze.py`, `top_breakouts.json`, `collected.json`.

## 4. Next 5 long videos (demand check 18 Oct: public search, this year, 4-20 min, top 15 results; `demand_check.json`)
| # | Title (title.py) | Type | Demand evidence | Thumbnail (<=3 words) |
|---|---|---|---|---|
| 1 | Why You Keep Waking Up At 3 AM (100) | why + you | median 78K views, 7/15 over 100K, top 3.8M | "EVERY NIGHT?" + 3:00 clock, wide-eyed Batata |
| 2 | How Did Ancient Humans Sleep? (94) | ancient humans | median 45K, 6/15 over 100K; "What Did Ancient Humans Do at Night?" 8.1M | "FIRST SLEEP" + firelit cave Batata |
| 3 | The Psychology of People Who Overthink At Night (76; long title but the strongest format) | psychology of | 7/15 over 100K, top 2.8M | "REPLAY. AGAIN." + thought bubbles |
| 4 | The Psychology of People Who Stay Up Late (76) | psychology of | 3/15 over 100K, top 765K ("...Who Always Stay Up Late") | "NIGHT OWL?" |
| 5 | What 72 Hours Without Sleep Does To Your Body (94) | what happens to your body (3D) | format median 8x in the scan; TED-Ed lack-of-sleep 2M; exact phrase thin | "HOUR 72" timeline |
Weak in the check (skip): eating before bed, beds history, "sleep with TV on".
Rules for all five: 8-12 min; first 30 s = the payoff question + one surprising fact; 3D Batata body/brain visuals;
title about YOU/HUMANS + an everyday moment; target CTR >= 4% (A/B test 3 thumbnails each).

## 5. Non-sleep picks (user: "why everything about sleep"; wide check of 40 topics, `demand_wide.json`, 18 Oct)
| # | Title | Format | Evidence (top 15 search results) | Our edge |
|---|---|---|---|---|
| 1 | What Walking Every Day Does To Your Organs | what happens to your body | median 184K-288K, 7-9/15 over 100K, top 9-10M ("Your Organs When You Walk 10,000 Steps a Day") | 3D Batata x-ray organs |
| 2 | How Your Dog Really Sees You | animal brain | median 248K, 10/15 over 100K, top 4.7M | potato dog 3D already built |
| 3 | What Did Ancient Humans Do For Fun? | ancient humans | 7/15 over 100K, top 14.6M ("...Actually Do All Day?") | Batata caveman 3D / drawn |
| 4 | Why Did Humans Start Wearing Clothes? | why did humans start | median 92K, 7/15 over 100K, top 3.4M (crowded: many tiny channels did it) | 3D + receipts (lice DNA study) |
| 5 | Why Is 95% Of Egypt Empty? | why nobody lives in (maps) | "Why is Egypt 97% Empty?" 2.6M; format top 7.9M | our map engine + Egypt angle |
Weak (skip): supermarket tricks, prices ending in .99, shaking hands, toothbrush history, telling time before clocks.
Pet-vlog topics (cats) have demand but winners are filmed pets, not explainers.
