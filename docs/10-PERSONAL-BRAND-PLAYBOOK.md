# 10 · Personal brand playbook (codebyabdullah)

Started 6 Nov 2026. On-camera Arabic short videos that turn viewers into client leads for the
owner's software services. **Separate from The Last Hours** (that channel stays anonymous; never
link the two). Scripting skill: `skills/brand-funnel-shorts/`. Edit tools: `tools/personal-brand-reel/`.

## Brand facts

| | |
|---|---|
| Name on screen | عبدالله أسامة (Abdullah Osama) |
| Handle | @codebyabdullah everywhere (YouTube + GitHub already his); backup @abdullahosama.dev |
| Site | https://codebyabdullah.com (5 yrs, 8 live projects: Cetus Design, CoachMind, Next Automation, Qsah, Hayyiz, Athar, Layan, Rakeeza) |
| Clients | Gulf SMEs (KSA/UAE), Arab founders, agencies (white-label) |
| Services | automation, AI for business, custom systems / SaaS MVP, websites and landing pages |
| Prices (from, SAR) | landing 1,900 · UI/UX site 2,500 · automation sprint 2,600 · AI 2,900 · custom/MVP 5,900 · free 20-min check-up |
| Dialect | light "white" Egyptian (understood in the Gulf); never fake Gulf dialect |
| Sign-off / keyword | «خلّيها شغّالة» · comment keyword «شغّال» |
| Look | HIS WEBSITE: bg #151515 + faint grid, cards #1D1D1D, text #F2F0EC, muted #9D9A92, border #2A2A2A, ONE orange #FF4F2B; Alexandria (Arabic), Bricolage Grotesque (Latin display), JetBrains Mono |
| Brand kit page | https://claude.ai/artifact/HkjjtyMwpxyLZLvpAxMo58 (private) |

Rejected on 6 Nov: an invented pine/saffron palette ("I like the branding on my website").

## Weekly content: the funnel trio

3 videos a week = REACH (viral), TRUST (value), CONVERT (lead). Sun/Tue/Thu 21:00 KSA.
Full rules, hooks and the LinkedIn version: `skills/brand-funnel-shorts/SKILL.md`.

## Edit pipeline (what the owner approved, 6 Nov)

Reference look: @AbdaalWebdeveloper Short "ازاي عملت موبايل ابلكيشن" (copy style only).

1. **Transcribe**: phone clip is 1920×1080 + rotation (ffmpeg autorotates to 1080×1920). Raw audio is
   very quiet (≈ −29 dB) → loudnorm a 16 kHz copy first. Whisper `medium` from
   `HF_HOME=E:/AskHabibiAI/hf` (C: is nearly full; big downloads and beam>1 fail with mkl_malloc).
   Transcribe in pause-split chunks (`chunks.py`), otherwise Whisper merges the retakes.
2. **Retakes**: he repeats a line several times; keep the LAST complete take, cut false starts,
   trim pauses, alternate 1.0 / 1.08 punch-in per cut (`plan.json` keep list).
3. **Grade** (`grade.txt`): nlmeans denoise + bright neutral grade + unsharp. He rejected the
   teal-orange grade ("very yellow, face very dark").
4. **Orange wall glow** (`glow.txt`): warm only the brightest background (luma mask 0.77→0.92,
   blur 40). Do the maskedmerge in **gbrp** (RGB). In YUV the gray mask's chroma = 0.5 and it
   tints the whole frame orange (shipped once by mistake; the owner hated it).
5. **Voice**: highpass 85, afftdn, EQ −2 dB @200 / +3 dB @3.2k, compressor 3:1, loudnorm −14 LUFS.
6. **Captions**: Alexandria ExtraBold full TTF (from Google Fonts CSS; fontsource subsets lose
   glyphs), `ass=...:shaping=complex` (simple shaping shows boxes), 2–3 words, one orange word.
7. **B-roll (old v2 style)**: tilted pop-up cards (`card.html` rendered with headless Edge; add
   `[hidden]{display:none!important}`) and his own website screenshots. Cards sit on the **chest**
   (centre y≈1280, 600 px; sites 470 px side by side), **never on the face, no face dimming**;
   captions switch to a lower style while a card shows (`build4.py`). He rejected: cards over the
   face; full-screen cutaway slides ("before was better").
7b. **DEFAULT since 6 Nov: UI depth (v3)** (`tools/personal-brand-reel/depth/`): MediaPipe person mask per frame;
    real-content panels (code files that type line by line, client/own site in a browser frame) BEHIND the head,
    hair overlapping a corner; small mono tags (`01 / scope`, `02 / comment`, inbox) IN FRONT on the chest with a
    hand-drawn orange circle or letter-by-letter typing; one panel at a time, synced to the spoken word; captions drop
    under front tags. Anti-AI-look: no glass blur, gradients, glow or fake buttons. Owner picked it over v2 on 6 Nov.
    The brighter colour test was rejected: keep the current grade.
8. **SFX**: soft whoosh/pop from `D:\why habibi\_style_kit\sfx`.
9. **Two audio versions every time**: chill music (Incompetech "Late Night Radio", CC BY → credit in
   description, −18 dB, sidechain duck) and **halal** = vocal nasheed beat
   (`D:\codebyabdullah_assets\music\halal_nasheed_60.mp3`, Pixabay licence, −21 dB, ducked).
   Silence + room tone was not accepted as "halal".
10. Output folder next to the raw clip: `<clip>_EDIT\` with `v2_music.mp4`, `v2_halal.mp4`,
    `captions.srt`, `CREDITS.txt`.

## Filming checklist (fixes "bad camera quality" at the source)

- Face the window or put a soft light in front of the face, 45° up; keep the orange lamp behind.
- Back camera, 4K 30 fps, lock exposure/focus (long-press), clean the lens, phone at eye level.
- Record the HOOK line first, then the rest; leave 1 s of silence between retakes.
- Lavalier or phone close to the mouth; no fan/AC noise.

## Services and products (owner, 6 Nov)

**Services (sold):** automation · landing pages · UI/UX design · custom solutions (AI integration included).
**Products (shown AS PRODUCTS, not services)** in profiles ("صانع Razqora وAtmaal") and in TRUST/CONVERT videos:

- **Razqora (رازكورا, spelled with kaf)**: AI knowledge base for contact centers, HR/onboarding, compliance/government and
  operations. Bilingual hybrid search (cross-language, typo tolerant), AI assistant that answers ONLY from approved articles
  and shows sources, decision trees (best demo), approval + verified badges, content-gap insights, embeddable website
  assistant, assessments, tasks, announcements, live agent mode (speech → suggested procedure). Cloud or on-prem.
  Tagline «كل إجابة، على بُعد بحث واحد». Demo kbs.nxtaut.com (sample data) · razqora.vercel.app. Pillars: Find · Answer ·
  Guide · Trust · Improve · Fit. Never show old names (KQuires, KBS, Terhab, AROYA).
- **Atmaal (أتمال)**: on-prem bilingual survey platform: AI writes the survey from a prompt or a PDF/Word, refines and
  auto-translates it, 12 question types with logic and piping, omnichannel distribution (link, QR, email, SMS, social,
  live agent) with per-channel attribution, real-time analytics, cross-tab, "ask your results", themes, 4-role RBAC.

**Never claim** for either product: customer counts, accuracy or speed percentages, awards, certifications (ISO/SOC2),
uptime SLAs, named third-party integrations, "the AI is always right", prices. Demo numbers only, labelled «بيانات تجريبية».
Product content ideas live in the Notion Content Pipeline (titles starting "Razqora:" / "Atmaal:").
