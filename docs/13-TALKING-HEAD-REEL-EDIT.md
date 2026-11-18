# 13 · Talking-head reel edit (codebyabdullah), approved 18 Nov 2026

The recipe for editing a raw on-camera Arabic reel (many retakes in one long phone clip) into a sales/convert Short.
It took 5 rounds with the owner, all on 18 Nov 2026, and the final round was "the whole video is very good".
First video: "إزاي حوّلنا فكرة عميل لنظام كامل من A to Z" (47.7 s, `D:\personal brand\02_videos\1st_video_A-to-Z_v5.mp4`).
Scripts: `tools/personal-brand-reel/talking-head/`. The workspace was `D:\personal brand\07_workspace\1st_video\`.

## What the owner rejected in v1 ("super horrible"), and the fix for each

| Rejected | Fix that was approved |
|---|---|
| Takes where he looks down reading the phone, or low-energy takes | Pick takes **visually + by energy**, never by "last take": contact sheet per line (3 mirrored face crops per candidate, `cands.js`) + loudness and words per second per take (`score.py`). Eyes on the camera and the loudest, most confident delivery win. One full take beats stitched halves (the CTA was one take). |
| "A millisecond of silence between each clip", "a lot of empty spaces" | Cut on **speech islands, not word timestamps**: 10 ms RMS frames, speech = above (take max − 32 dB), merge gaps < 0.16 s, pad 50 ms before / 70 ms after, frame-quantise every piece to 1/30 s (`segs.py`). Voice pieces get 12–15 ms fades; video pieces get the same frame counts, so A/V never drifts. |
| The same phrase said twice ("أول حاجة… أول حاجة") | After cutting, **transcribe every piece on its own WITHOUT an initial prompt** (`rep.py`): a script prompt makes Whisper hide repeats. Keep only the second (complete) attempt. Whisper's first-word start is unreliable; trust the energy islands. |
| "The sound is very horrible… a lot of noise" | DeepFilterNet3 on the cut voice only (fast: 1.2 s for 48 s), then highpass 75 · EQ −2.5 dB @280 / +2.5 dB @4.2k / +1.5 dB shelf @10k · de-esser 0.35 · compressor 2.5:1, −22 dB, knee 6 · limiter · loudnorm −16 (master +2 dB = −14). Install: `uv run --python 3.11 --with deepfilternet --with soundfile --with torch==2.1.2 --with torchaudio==2.1.2 --with "numpy<2" deepFilter in.wav -o outdir`. Run it from a path **without spaces** (the scratchpad), or soundfile fails with "System error". |
| Music that feels like "cooking" (Late Night Radio), then "anxious/addictive" (Rising Tide's synth pulse) | Calm, classy, **non-busy** bed: **Eternity** (Incompetech, e-piano + guitar, 100 bpm, CC BY → credit). "Inspired" was OK as a step. Level: **about 16 dB under the voice** (bed ≈ −30 LUFS with voice −14). Flat, **no sidechain ducking** (he hates pumping). "Not that loud" came after an 11 dB gap. |
| Zoom "punch" at the start of every cut ("very ugly") | No animated punch. Each piece alternates framing 1.0 / 1.10 (hard cut) and gets a **slow linear push-in of 2.5 %** across the piece. Do it with `perspective` (sub-pixel, cubic) on a **2× supersampled** frame (`scale=2160:3840:lanczos → perspective → scale=1080:1920:lanczos`). `scale` with `eval=frame` jitters (whole-pixel steps). The same push is used on the B-roll. |
| The first clip darker than the rest ("fix the colour") | **Shot-match every piece to the hook**: measure YLOW / YAVG / YHIGH (`signalstats`), build a per-piece `curves` mapping its 3 points onto the hook's, then re-measure and correct twice (RGB curves do not move luma 1:1). Converges within about 2 levels (`match.json`, `segs3.js`). Camera auto-exposure drifts between takes, so always check this. |
| Stickers on his beard | Pop-up stickers go in the **empty space above the head** (y ≈ 215 of 1920, below the step bar), never on the face or beard. |
| B-roll where he looks at the camera | B-roll must not have him looking at the lens. Use looking-down or hands shots (`01_phone_scroll_face`, `12_phone_at_desk`, notebook, blurred-screen writing). |
| A coding B-roll shown for about 1.6 s ("looks like a glitch") | **B-roll ≥ 2.2 s** or don't use it. |
| No CapCut project | Always deliver an editable CapCut project too (see below). |

## The approved layer stack (Sales style, D Tech Depth in Pistachio)

1. Face pieces (graded, Raw+ grade + beard/brow darken mask, mirrored if asked, shot-matched, smooth push).
2. B-roll every 2–4 s from `D:\my\BEST_BROLL` (the owner likes these), with a whoosh at entry.
3. **Step progress bar** at the top: `01 التحليل · 02 المستند · 03 التنفيذ · 04 التسليم`. Active = pistachio fill, done = outline + ✓, future = dim.
4. **Typed step cards** (ink panel, pistachio border, 4 states that tick in), 650 px wide, top of frame. Non-technical client language («مستند واحد واضح», not "PRD spec").
5. **Pistachio stickers** (ink text, 4 px ink border, hard ink shadow, −2° tilt) with **new** info, never repeating the caption. Example: caption «طلب بيضيع» → sticker «فلوس بتضيع».
6. A **full-screen paper card** for the turn («والفرق؟»), 0.6 s, with paper-slide + soft impact.
7. CTA card «احجز استشارة مجانية · 20 دقيقة · اللينك في البايو · codebyabdullah.com». The owner: "really good, keep it".
8. Captions: Alexandria ExtraBold 66, white on an ink box, 2–5 words, RLM prefix, small scale-in.
9. Small «● codebyabdullah» watermark at the bottom.

SFX (from `D:\why habibi\_style_kit\sfx`, levels before the +2 dB master): impact_soft on the hook −18 · whoosh_fast at B-roll entry −21 ·
swoosh_in + clicks on cards −20 / −21 / −24 · click on step change −18 · sticker_slap −19 + pop −22 on stickers · paper_slide −18 ·
riser_short −27 into the CTA, pop −18 + bell −24 on the CTA card. When mixing SFX into a stem, force `aformat=sample_fmts=fltp`
on every input, including anullsrc (the 8-bit trap from `memory/clean-voice-mix.md`).

## CapCut project (Windows)

`capcut_build.py` clones segment templates from the clean Ask Habibi Ep1 FINAL draft and builds 11 tracks: face pieces · B-roll ·
paper · cards+CTA · step bar · stickers · watermark (PNG photos) · captions (CapCut text, Alexandria, ink background) · voice ·
music · SFX stems. `capcut_create.py` registers it (CapCut must be **fully closed**; it backs up `root_meta_info.json`).
Photo placement: CapCut contain-fits the image, then applies `scale = displayed_w / (w × fit)`. The transform is centre-normalised
(x right, y **up**). Canvas `9:16 1080×1920`. Each new version is a new project name; re-rendering the shared `seg2/` pieces
breaks older projects, so tell the owner to delete them.

## Practical notes

- Source clip: 1920×1080 + rotation 90 → ffmpeg autorotates. Python only via `uv`. Whisper medium from `HF_HOME=E:/AskHabibiAI/hf`.
- ffmpeg `drawtext` on Windows: copy the font next to the script (`fontfile=arialbd.ttf`); a `C:` path breaks the filter parser.
- D: fills up. Clean your own intermediates (old pieces, base.mov) before a render; never write to C:.
- Always send a phone copy under 30 MB (crf 25, maxrate 4M).
- Mirror: footage filmed with this phone is not actually mirrored, so flipping it makes monitor text read backwards. Flip only on request.

## Round 6 (18 Nov 2026): skin not orange + animated phone-call CTA

- **"Don't make the colours super saturated, I look orange."** The contrast S-curve + shot-match curves pushed skin to orange
  (hands worst). Fix appended after the shot-match curves in `segs3.js`:
  `huesaturation=saturation=-0.4:colors=r+y:strength=1, huesaturation=hue=-4:colors=r+y, eq=saturation=0.88`.
  It only pulls reds/yellows (skin, warm wall light) and leaves the blue monitor alone. Always check hands, not just the face.
- **Animated CTA, "phone call" style, two variants** (`cta_anim/call_a.html`, `call_b.html`), timed to the CTA captions
  (0 / 1.54 / 3.14 / 5.43 s after the CTA cut):
  - **A, incoming call:** a dynamic-island pill morphs into an ink call card (pistachio avatar with pulsing rings, «استشارة مجانية»,
    decline + accept buttons, ring wiggle) → a fingertip taps accept on «تقدر تحجز» → "● connected" + running 00:0x timer,
    "FREE · 20 MIN" → «20 دقيقة · على الويبسايت» line → «اللينك في البايو ↓» sticker tab + codebyabdullah.com bounce in.
  - **B, approved card + ringing phone:** the v5 CTA card enters the same way; a pistachio sticker phone badge rings (wiggle + rings)
    with an "incoming call…" tag → on the tap it flips to ✓ and "connected 00:0x" → «مكالمة 20 دقيقة · مجاناً» sticker slaps in
    at «20 دقيقة» → underline sweep on «اللينك في البايو» + bouncing ↓.
  - SFX: phone_ring −22 · click on the tap −16/−17 · pop −20 + bell −24 on "link in bio" · riser_short −27 into the CTA.
- **Rendering HTML animations to frames:** `cta_anim/frames.js` drives headless Edge over CDP (Node 24 global `WebSocket`):
  transparent background override, `render(t)` per frame, `Page.captureScreenshot` → PNG sequence (198 frames in about 1 min).
  The compositor overlays the sequence directly (`CTA=a|b node comp2.js out.mp4`); CapCut gets a ProRes 4444 alpha `.mov`
  of the same frames (`CTA_MOV`, `SFX_STEM`, `OUT` env vars on `capcut_build.py`; `NAME`, `CONTENT`, `COVER` on `capcut_create.py`).
