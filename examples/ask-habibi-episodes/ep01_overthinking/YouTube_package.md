# Ask Habibi, Ep. 1: upload package

Video: CapCut project **"overthincking ! FINAL"** (3:13) — new sectioned music bed (Content-ID safe), Pro features removed. Everything below was written with the yt-package /
yt-chapters / yt-seo / yt-shorts skills and their linters. Nothing here is published: copy, paste, upload.

---

## 1. Title (scored with `title.py`)

| # | Title | Chars | Score | Issue |
|---|---|---|---|---|
| **1 (use this)** | **Why Do Embarrassing Memories Hit at 3 a.m.?** | 43 | 100 | Mobile feed cuts at "…Hit at 3…", but the subject survives |
| 2 | Your Brain at 3 a.m.: 4 Levels of Cringe | 40 | 100 | None; mobile-safe. Best alternate for an A/B test |
| 3 | Why Embarrassing Memories Attack You at 3 a.m. | 46 | 98 | Mobile cut drops "3 a.m." |

Title #1 matches the channel's "WHY DO…?" format and is the exact question people type.

## 2. Thumbnails (folder `thumbnails/`)

Real-photo set (recommended). Each thumbnail's words were linted against title #1: no repeated words, three words max.

| File | Words | Idea |
|---|---|---|
| `real_2_BRAIN_STOP.png` | BRAIN, STOP. | Man staring at his phone; "NOW REPLAYING: that time you waved back at a stranger" |
| `real_1_NOT_AGAIN.png` | NOT AGAIN | Hands over mouth, wide eyes, red LED 3:00 |
| `real_4_CRINGE_ATTACK.png` | CRINGE ATTACK | Real brain + screaming seagull (your D–G reference style) |
| `real_3_CRINGE_OCLOCK.png` | CRINGE O'CLOCK | Shocked man + giant LED 3:00 |
| `real_5_THEY_BARELY_NOTICED.png` | THEY BARELY NOTICED | Lone man in a spotlight (the t-shirt study) |

**A/B test:** YouTube Studio → Test & compare takes 3 thumbnails. Run **BRAIN, STOP.** vs **NOT AGAIN** vs **CRINGE ATTACK**.

**Brief for the lead (BRAIN, STOP.):** stunned open-mouth expression aimed at a phone; subject in the right half,
face in the top third, phone glow as the only light; the words white + red, stacked on pure black on the left.
That black is what keeps it readable at feed size. Batata only peeks in small at the bottom (brand hint, not the hero).

(The cartoon set `thumb_1…5` is still there if you ever want a mascot-first version.)

Photos: Pexels (free licence, no credit required): 8276884, 11645171, 3779453, 15410078, 460918. Seagull: imgflip "Inhaling Seagull".

## 3. Description (paste as-is, then fill the two [links])

```
Why do embarrassing memories hit at 3 a.m. and replay at night when you just want to sleep? Here's what sleep research says, in four levels, plus one thing psychologists say actually helps.

▶ Next midnight question: [link to next video / playlist]

0:00 The 3 a.m. cringe attack
0:37 Level 1: The sleepless night
1:13 Level 2: The replay
1:31 Level 3: Sleep vs. cringe
2:04 Level 4: Why 3 a.m.?
2:16 The t-shirt study
2:33 What actually helps
2:49 When to get help

You're almost asleep, and your brain decides to show you the time you waved back at a stranger who wasn't waving at you. This video walks through why that happens: what one sleepless night does to bad vs. good memories, why your brain "reviews" social moments (post-event processing), what a karaoke experiment showed about sleep and embarrassment, and why 3 a.m. itself probably isn't special. Then one simple strategy for when the replay starts.

Sources:
• Sterpenich et al. (2007), PLoS Biology: sleep deprivation the first night after learning; negative items held up 3 days later, neutral & positive faded.
• Dannahy & Stopa (2007), Behaviour Research and Therapy: post-event processing after a conversation with a stranger.
• Wassing, Van Someren et al. (2019), Current Biology: "Restless REM sleep impedes overnight amygdala adaptation" (the karaoke study).
• Gilovich, Medvec & Savitsky (2000), Journal of Personality and Social Psychology: the spotlight effect (the embarrassing t-shirt study).

This video is general information, not medical advice. If intrusive memories happen constantly or affect your daily life, talk to a doctor or a therapist.

Ask Habibi: midnight questions, answered. Subscribe so the next one finds you before you start scrolling.

Music by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0
http://creativecommons.org/licenses/by/4.0/
"Marty Gots a Plan" · "Daily Beetle" · "Easy Lemon" · "Dream Culture" · "Thunder Dreams" · "Promises to Keep"

#psychology #sleep #overthinking
```

**Fact check before upload:** the line "memories that pop up on their own tend to be more negative" has no source in
this list. I couldn't verify one, so either add your source or keep it out of the description (it's fine spoken as-is).

## 4. Chapters (validated: starts 0:00, 8 entries, every one ≥10 s)

Already inside the description above. `chapters.py` found boundaries at 2:00 / 2:18 / 2:33 / 2:46. They were
snapped to the exact level-card cuts in the edit and retitled. "When to get help" absorbs the outro, because a separate
2:58 chapter would make the one before it 9 s long, and YouTube would then drop all chapters.

## 5. Tags (they barely matter; these are for disambiguation)

```
embarrassing memories, why do embarrassing memories come back, cringe memories, 3am thoughts, can't sleep, overthinking at night, post-event processing, spotlight effect, REM sleep, sleep and memory, social anxiety, insomnia, ask habibi, why habibi
```

**The three searches this should win:** "why do embarrassing memories come back at night", "why do I remember
embarrassing moments at 3am", "why does my brain replay embarrassing memories". Title + first description line
contain *embarrassing memories, 3 a.m., at night, replay*. ✔

## 6. Pinned comment

```
What's your 3 a.m. question? Drop it below. The best one might be the next Ask Habibi.
```

## 7. Shorts (folder `shorts/`, 1080×1920, ready to upload — post in this order)

Each Short ends on a **"PART N → ON MY PROFILE"** end card (Batata pointing at your profile icon + brand music sting),
so it never just stops. Generate each line below in ElevenLabs (same voice + settings as the main VO), save as
`shorts\cta\part1.mp3 … part5.mp3`, and re-run `shorts.py` — the voice is added to the end card automatically.
On YouTube say "Subscribe"; keep "Follow" for TikTok/Reels.

| Post | File | From the long video | On-screen hook | ElevenLabs end line |
|---|---|---|---|---|
| Part 1 | `part1_why_3am.mp4` | 0:00–0:21 + 2:06–2:16 | WHY DOES THIS HAPPEN?! | "That's just the surface. Part two is already on my profile. Follow, so part three finds you at three a.m." |
| Part 2 | `part2_bad_memories_stick.mp4` | 0:43–1:13 | WHY BAD MEMORIES STICK | "And your brain has a second trick. Part three is on my profile. Go check it, then follow." |
| Part 3 | `part3_meeting_you_cant_leave.mp4` | 0:12–0:15 + 1:13–1:31 | THE MEETING YOU CAN'T LEAVE | "So how do you end that meeting? Sleep. Part four is on my profile. Follow for the rest." |
| Part 4 | `part4_karaoke_cringe.mp4` | 1:31–2:04 | SLEEP = LESS CRINGE? | "There's one thing that actually helps. It's part five, on my profile. Follow so you don't miss it." |
| Part 5 | `part5_stuck_on_replay.mp4` | 2:33–2:55 | STUCK ON REPLAY? TRY THIS | "That's the full answer. The whole video is on my channel. Follow, and send me your next midnight question." |

Optional stronger cold opens (spoken, scored with `hookscore.py`): P1 "Why does your brain replay your most
embarrassing moment at 3 a.m., right when you need sleep?" (57) · P2 "Why do your bad memories survive a sleepless
night when the good ones fade?" (44) · P3 "Why do you replay one awkward conversation for hours after it ends?" (44) ·
P4 "Why does a bad night's sleep make you cringe harder the next day?" (40) · P5 "What do you do when your brain
won't stop replaying something embarrassing at night?" (54).

**Shorts titles & descriptions** (add the music credit line to each description too):

```
Part 1  Why does cringe hit at 3 a.m.? (Part 1)          | Part 2 is on my profile. #shorts #psychology
Part 2  Why bad memories survive a sleepless night (Part 2) | From a 2007 study. #shorts #psychology
Part 3  The meeting your brain won't let you leave (Part 3) | It's called post-event processing. #shorts
Part 4  Sleep vs. cringe: the karaoke study (Part 4)       | #shorts #sleep
Part 5  Can't stop replaying it at night? (Part 5)         | Not medical advice. Full video on my channel. #shorts
```

Post Part 1 the same day as the long video, then one every day or two.

---

**Ship it, or change it?**

---

## A/B test (running since 14 Oct 2026)

Studio > A/B Testing > Title and thumbnail, up to ~2 weeks, winner = watch-time share. Thumbnails in `1st video\thumbnails\`.

| # | Title (title.py score) | Thumbnail |
|---|---|---|
| 1 | Why Do Embarrassing Memories Attack You at 3 AM? (100, live title) | thumb_PHOTO_C_BRAIN_PLATE.png (live) |
| 2 | Your Brain at 3 AM: 4 Levels of Cringe (100) | thumb_MAP_A_RED_LOBE.png |
| 3 | The Science of 3 AM Cringe Attacks (100) | thumb_PHOTO_D_PHONE_NIGHT.png |

No title uses "replay" (every thumbnail says REPLAYING). All 10 scored titles: `ab_titles.txt` in this folder.
