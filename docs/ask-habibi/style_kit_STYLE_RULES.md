# Ask Habibi: editing style rules ("cut & marker")

Ep 2's first look ("Midnight Noir": dot wordmark, tracked ALL-CAPS labels, bordered cards, mono `//` tags, amber glow,
grain) was rejected because it looked like AI-made design. That look is generic: every AI tool produces it.
**The fix:** everything on screen is either REAL (a page, a photo, a meme, footage) or HAND-MADE on top of it
(highlighter, marker, a sticker). Nothing should look like an app, a dashboard or a pitch deck.
We keep the brand: navy / yellow / red, Batata, Rubik captions, the deadpan voice.

Everything lives in `D:\why habibi\_style_kit\` (start with its README): examples in `examples\`, code in `tools\`
(`marker.py` = the kit, `receipt.py` = real-page capture), brand assets in `brand\`, Batata in `mascot\`.

## The 3-second test (run it on every frame)
1. **Is something real on screen?** A page, a photo, a meme, footage. If it's only shapes and text, rethink.
2. **Could it be a SaaS landing page or a slide deck?** Then kill it.
3. **Could a human editor make it in CapCut in ~10 minutes?** If not, it's over-designed.

## Banned (the AI-slop tells)
- Cards, boxes or panels with thin borders or rounded corners; "glass"; pills, badges, chips, tags.
- Wordmarks with a coloured dot; tracked-out ALL-CAPS micro labels; mono labels (`// LEVEL 01`, `01 —`, `FIG. 2`);
  fake UI chrome (status bars, progress bars, toggles, browser frames we drew ourselves).
- Glows, light leaks, lens flares, grain "for mood", gradient meshes, bokeh blobs, duotone posters.
- Icons used as illustrations (ear icon, brain icon, tick icons). Use a real photo or a meme.
- Charts styled like dashboards. One number? Write it by hand on the real source.
- Everything centred and symmetric; things floating or bobbing; slow fade-ins.
- A logo or watermark sitting in the corner. The brand is the voice, Batata and the captions.

## Copyright-safe only (user rule, from Ep 2)
Nothing goes in a video, thumbnail or Short unless we're allowed to use it. Keep `CREDITS.md` in every episode folder:
one line per asset, with its source and licence.
| Material | Allowed | Not allowed |
|---|---|---|
| Photos / B-roll | Pexels (free licence, no attribution needed; never show a recognisable person in a bad or offensive light) | Google Images, film/TV stills, other channels' footage |
| Memes | **home-made only**: meme *formats* rebuilt with Batata, Pexels photos and marker (formats and jokes aren't copyrighted; the images are) | imgflip templates, film/TV/celebrity/cartoon stills, viral photos of real people |
| Music | `_music_library` (Kevin MacLeod, CC BY 4.0, credit line) or YouTube Audio Library | anything commercial, game/film OSTs, "no copyright" uploads on YouTube |
| SFX | made by our scripts, recorded by you, or CC0 | sounds ripped from videos or films |
| Studies / articles | a screenshot of the real page showing the **title + 1–2 key lines**, highlighted and cited (short quotation for commentary) | full pages, figures or long passages copied |
| Fonts | Rubik (OFL), Windows' Ink Free and Impact | random "free" fonts without a licence |
| Voice | your ElevenLabs clone on a paid plan (commercial use included) | other people's voices |
| Brand | our own: Batata v2 (Pexels photo, our marker face), logo, end screen | the retired cartoon packs |

## Building blocks (use these instead)
1. **Receipts.** Real screenshot of the actual study or article (`receipt.py` captures at 2x and returns where each
   key phrase sits). Show it full-bleed, cropped off the frame edges and tilted 1–2°. The rest of the page dims, and
   the key line stays bright. A yellow highlighter swipe goes across the key phrase.
   Two beats per study: **title + year** ("it's real"), then **the finding** (highlight, circle, note).
2. **Marker.** Hand-drawn circles, underlines and arrows, never perfect ellipses. They write on in 0.3–0.4 s.
   Use red on light pages and yellow on dark images. One annotation idea per beat.
3. **Hand notes.** Ink Free, short, funny and honest ("+10 min to fall asleep (ish)"). Put them in empty space,
   never across faces or over the key words.
4. **Real photos / footage.** Pexels (free licence), with a night grade (shadows sink into navy). People reacting
   are better than objects, and objects are better than abstract shapes.
5. **Memes (home-made).** Rebuild the meme format with Batata expressions, Pexels photos and marker (e.g. Batata
   sleepy / Batata panic as a two-panel; a 4-panel "plan" with a Batata double take). Big and unframed; one hand note at most.
6. **Batata = a real potato with a marker face** (`mascot\batata\`, 9 expressions; `cool` with marker sunglasses is
   the brand face). On screen it's a reaction sticker: white edge, small hard shadow, tilted 5–10°. It pops on a beat
   (5-frame pop) at no more than ~30% of the frame height, in a corner, about once every 20–30 s. Never the narrator,
   never the centred hero. The cartoon mascots (old Batata, Tamatem, Dorra) are retired.
7. **Level / chapter changes.** A real photo, huge lowercase Rubik words and a handwritten "level n" with a scribbled
   underline. No title-card template.
8. **Captions.** Rubik Bold, white, lowercase, 1–3 words, y = -0.73, with a **black outline** now that they sit on
   real images (CapCut text stroke, black, ~0.08).

## Motion
- Hard cuts. Punch-in (instant 100% → 115–130%) on the stressed word, with a 3-frame shake on impacts.
- Slow push (≤ 2%/s) only while the viewer is reading a page.
- Things land on the beat: the highlighter wipes left→right in ~0.4 s, the marker writes on, the sticker pops.
- No crossfades except into and out of the CTA. No ease-in-out drifting. Nothing floats.
- Every pop, cut and annotation gets a sound (marker squeak, paper, whoosh, thud).

## Colour and type
- **Navy** = the night (photo grade, shadows). **Yellow** = highlighter and notes on dark. **Red** = marker on paper,
  plus one alarm per scene. **White** = captions and big words. No other colours, no gradients.
- **Rubik Bold** (captions, big words) + **Ink Free** (hand notes). **Impact** on thumbnails only. Nothing else.

## Beat recipe (the VO line decides the visual)
| The VO says… | The screen shows… |
|---|---|
| a study, a number, a date | receipt: page → highlight → marker → note |
| a claim with a joke in it | meme, full frame |
| a feeling or a situation | real photo / footage + one arrow or note |
| a new level or chapter | photo + big words + "level n" scribble |
| a punchline | Batata reaction pop, or a meme |
| tips or steps | one real photo per tip + a handwritten tick, no icon list |
| the CTA | `brand\intro_sting.mp4` / `intro_card`, and `brand\end_screen` for the last 20 s |

## Thumbnails (v3, the default from 2026-10-12; the user: "the potato thumbnails is fire")
**Batata is the hero.** One bright flat brand colour per episode (red, blue, yellow; no dark bedroom photos as the
whole thumbnail, they sink into YouTube's dark feed), a giant Batata (60–100% of the height) with a clear expression,
ONE prop (LED clock, glowing phone, timer, index card) and 0–2 Impact words that don't repeat the title.
"Mix" version = the same + a real photo pasted as a tilted print (the scene or the study) and a marker ✗ / circle.
Every video gets a Test & compare set: Batata only · Batata + photo mix · the best photo-only version.
Judge them at real feed size: `_thumbs_v2\feed_mock_v3.png` (built by `_thumbs_v2\thumbs_v3.py`, the template).
Never AI-generated people or images (YouTube's suggestions are ideas only).

## Shorts
Same rules, vertical. End cards come from `tools\endcard.py` (highlighter "part 2", handwritten line, marker
arrow to the profile picture, Batata side-eyeing it).

## Caption zone (user rule: captions never cover our text)
The burned-in captions live in a fixed band: **x 420–1500, y 860–1010** (1080p frame). Nothing we write goes there:
hand notes, big words, ticks, underlines and stickers sit **above y 850** or out in the corners (Batata bottom-right is fine).
Plan layouts with the bottom row at y ≤ 800. The render engine enforces it: `caption_safe()` (in the episode's `*_fx.py`)
lifts any note row that lands in the band (pairs move together, anything they bump into moves too), and
`check_caption_zone.py` lists what's left. Run it before every full render; it must say 0.
