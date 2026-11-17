# The Last Hours: ChatGPT / Gemini thumbnail prompt template

This is the owner's reference style (17 Nov 2026): "66 NAMES. ONE ORDER.", "NO WAY HOME", "HE DISAPPEARED", "THEY LEFT ONE WORD", "THE MISSING LINK", "NOT A REAL BODY".
You can use it in ChatGPT (free tier), Gemini or any free image generator. **Attach 1-2 REAL archive photos of the person** (from the file's `media/` folder) so the face stays faithful.

## How to use it
1. Fill in the `{…}` fields from the table below.
2. Attach the real photo(s).
3. Paste the prompt.
4. Ask for 2 more versions with "same scene, different composition: {B idea}" and "{C idea}". That gives 3 options for Test & Compare.
5. Check: no women or girls anywhere (crowds included), text spelled right, nothing important in the bottom-right 170x70 px (the timestamp covers it), readable at 320x180.
6. Save as 1280x720 JPG under 2 MB. If ChatGPT returns 1536x1024, crop it to 16:9 (`thumbls.py` → `cover()` does it).

## The prompt
```
Create a 16:9 YouTube thumbnail (1280x720) for a true-history documentary channel called "The Last Hours".

SCENE: a cinematic, photorealistic, gritty scene of {SCENE: place + moment + time of day + weather}. {STORY PROPS: e.g. a TOP SECRET folder / an old newspaper / a FBI wanted paper / a red hand-drawn circle around {THE CLUE}}.
SUBJECT: {PERSON} on the {right} side, big (head and shoulders fill ~45% of the frame), looking {sideways / at the camera}, {black-and-white / sepia} like an archive photo, half the face in shadow. Use the attached real photo for the face: keep his real likeness exactly, do not beautify or change his age.
TEXT on the {left}: two lines in a huge distressed condensed font (Anton / Bebas style, scratched worn texture, heavy dark shadow):
  line 1 "{WORDS 1}" in white,
  line 2 "{WORDS 2}" {in white on a torn red brush stroke | in yellow | in icy blue with cracks | in red}.
Small yellow block bottom-left with the date "{DATE}" in black.
LOOK: dark vignette, crushed blacks, film grain, {teal-and-orange night | icy blue | warm sunset | sepia} grade, high contrast, one strong subject, very readable at phone size.
RULES: no women or girls anywhere, no real logos, no extra text besides the words above, spell the words exactly, nothing important in the bottom-right corner.
```

## Ready fields for the older files
| File | SCENE | PERSON / props | Text (L1 / L2, colour) | DATE |
|---|---|---|---|---|
| Alcatraz 1962 | Alcatraz at night from the water, fog, searchlight, a raft made of raincoats on black waves | Frank Morris (FBI mugshot) right | NEVER / FOUND (red brush) | 11 JUNE 1962 |
| Alcatraz B | 1962 cell at night, a crude papier-mâché man's head on the pillow, guard's flashlight, bars | real dummy-head photo as a print, red circle | IT WAS / A DUMMY (yellow) | 11 JUNE 1962 |
| Franklin | two 1840s ships stuck in pack ice, line of men hauling a sledge, blizzard | (no face) | NO WAY / HOME (icy blue, cracked) | 22 APRIL 1848 |
| D.B. Cooper | night storm, the 727's rear stairs open above a black forest | FBI composite sketch right, FBI WANTED paper, parachute circled red | HE / DISAPPEARED (red brush) | 24 NOV 1971 |
| Roanoke | an old tree with CROATOAN carved in it, empty colonial village at sunset | (no face) | THEY LEFT / ONE WORD (yellow, underline) | 18 AUG 1590 |
| Andrée balloon | wrecked balloon on Arctic ice, three men with a sledge | the 3 men's studio photo as a print | THE FILM / SURVIVED (icy blue) | 14 JULY 1897 |
| Saddam (don't change) | 1979 hall, TOP SECRET folder with a redacted list, soldiers row | Saddam (archive) right | 66 NAMES. / ONE ORDER. (red brush) | 22 JULY 1979 |

## Honesty rules (channel)
- Props such as "TOP SECRET" folders and redacted lists are **visual props**. Never write a fake quote, a fake name list or a fake document number that claims to be the real record.
- A real record (FBI flyer, Victory Point note, mugshot) may appear as itself.
- Real people's faces come from real photos only. Never let AI invent the face of a real person.

## Free local alternative (no ChatGPT)
`thumbls.py` (in this folder, and `tools/last-hours/thumbls/` in the repo) builds the same look offline:
- Z-Image Turbo background, about 4 min on the Radeon 780M.
- A real-photo cutout plus Anton lettering, about 3 s.
See `make_all.py` for 15 worked examples.
