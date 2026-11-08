# Edit styles (owner approved A, D and E, 8 Nov 2026)

Three edit styles, all in the Pistachio palette: paper #F3EEE3, ink #121212, pistachio #B9DD74 with ink text on it, and cobalt #2E5BFF in small doses.

Rules for every style:
- No orange anywhere.
- No stars, hearts, doodles or handwriting.
- Never cover the face.
- Arabic captions in Alexandria, using `shaping=complex` or HTML rendered by Edge.
- Render two audio versions every time: music and halal.

We tested five styles on the same 23 s test clip. B (Minimal Keynote) and C (Editorial Magazine) were not chosen. Reference renders are in
`C:/Users/ossam/Downloads/video_20261105_130210_EDIT/styles/`, including `compare_all_styles.jpg`.

## Which style for which video

| Video | Style | Why |
|---|---|---|
| Reach, Sunday («رأيي كخبير», hot takes, money numbers) | **E · Bold Kinetic** | Highest energy: it stops the scroll and holds the first 3 seconds |
| Value, Tuesday (step-by-step answers, «سؤال صاحب شركة») | **A · Paper Pro** | Clear numbered paper cards and keyword boxes, so steps are easy to follow and save |
| Sales, Thursday (case studies «من الكواليس», product demos «في 60 ثانية») | **D · Tech Depth** | Engineer credibility: real code, documents and product panels behind his head |

When in doubt, use A. E's full-screen title cards can also be borrowed for a single beat inside A or D.

## The three styles

**A · Paper Pro** (`A_paper_pro/`)
- Pistachio frame on the hook, the CTA and the ending; a dashed frame on detail parts.
- Straight keyword boxes with ink text.
- Graph-paper interludes with a mono label (e.g. "02 / PROCESS") and one straight arrow.
- Straight paper UI cards on the chest. The caption drops below the card while it shows.
- Cobalt mono step pills, e.g. "STEP 01 / ANALYSIS".
- Soft whoosh and click sound effects.

**D · Tech Depth** (`D_tech_depth/`)
- The background is darkened and desaturated with the person mask; the person stays naturally graded.
- Dark ink panels sit behind the head, with thin pistachio outlines, a subtle grid and mono labels (Consolas). They show code typing line by line, a PRD doc, an inbox and checklists. Hair overlaps a panel corner.
- Captions are 2–3 words in white, with the keyword in pistachio text.
- Small mono chest tags ("01 / ANALYSIS"). Soft clicks per typed line.

**E · Bold Kinetic** (`E_bold_kinetic/`)
- Big Alexandria ExtraBold captions, 1–3 words, with a scale pop. The keyword sits in a pistachio box.
- Punch-in zoom on every cut (1.00 / 1.06) and on every keyword (up to 1.12).
- Full-screen ink title cards, about 0.6 s each, in giant pistachio type (e.g. «تحليل», «PRD», «تسليم»).
- Paper cards slam in with motion blur, with a whoosh or hit. No frame.

## How to build one

Each folder has `gen.py`, which renders the graphics (HTML to PNG through headless Edge, launched from PowerShell), and `build.py`, which composites everything in FFmpeg with captions, SFX, music ducking and -14 LUFS.

The inputs are the jump-cut `base.mp4` and `plan.json` (keep list plus word-timed captions with one keyword per line).

The scripts were written against the test clip. Absolute paths point into `D:/codebyabdullah_assets/workspace/` and the person masks live in `D:/codebyabdullah_assets/tmp_masks/`, so update the paths and the caption, card and keyword lists for each new video.

Run Python with `uv run --no-project python`. Shared helpers are in `_shared/` and `D_tech_depth/de_common.py`.
