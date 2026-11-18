---
name: stick-figure-niche
description: 18 Nov 2026 owner dislikes The Bill, Explained; wants stick-figure story animation niche for the 2nd channel — research results + formats
metadata:
  type: project
---
18 Nov 2026: owner "don't like the idea of the new channel" (The Bill, Explained), asked to research stick-figure story animation.
Research (yt-viral, 229 recent videos, 10 channels; data D:/the-bill-explained/research/stick_niche_*):
- Survival diaries "Day 1 to Day 30/365 trapped in X" — Nobody Gets In (70K subs, MEDIAN 172K, 4.3M hit), StickDread (1K subs, 202K hit = 47x).
- "Why It Sucks to Be X (in Ancient Y)" history — Bernard (398K subs, median 377K, ~20 min).
- "Every X Explained" lists — Paint Explainer (2M subs), Stickman Explains (1.8K subs, 373K hit = 432x), EverythingProfessor.
- Self-help "how to X in 9 min explained by a stick figure" — StickFigure Explains (4.9M hit = 151x).
- "What if" (What1fy), "Your Life as <famous man>" (In Their Shoes).
Tiny channels break out (432x, 151x, 47x) → good for a new channel. Many rivals use AI art + "make stickman with AI" tutorials flood the niche; owner hates AI slop → our edge = clean hand-drawn/procedural stick style, free (no-spend), Chatterbox voice, no women in visuals (pick male roles: knight, gladiator, pirate, miner...).
**How to apply:** wait for owner's format pick + whether to rebrand the same channel again (UCJXUO3S0AtoQvmWHqpGp_ow). Related: [[second-channel-money-plan]]

**18 Nov: owner picked SURVIVAL DIARIES; "make the first video".** Project F:/stick-survival (D: full). Ep 1 "Zombie Outbreak: 30 Days Trapped in a Supermarket" (5:42, 109 lines, Chatterbox voice, characters me/Rick/Walt/Marcus/Dex, all male).
Pipeline: tools/stickkit.py (pycairo stick figures, poses, zombies, props, backgrounds, day stamps, camera) + tools/stickvid.py (billvid copy with STICK shot kind + per-shot sfx list, caption tail-word filter) + chain_vo.sh. Run with: uv run --no-project --python 3.11 --with pycairo --with numpy --with pillow --with soundfile python spec.py keys|qa|frame t|all 4.
Signature: big red "DAY N" handwritten card (Ink Free font) on black per day + corner day stamp; thumbnail = DAY 1 vs DAY 30 split (thumb.py). Music CC BY Kevin MacLeod (SCP-x5x, I Can Feel it Coming, Darkling, Shadowlands 2 - Bridge, Stay the Course, Man Down). Channel NOT rebranded yet; upload needs owner OK.
