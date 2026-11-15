# The Bill, Explained - brand kit (15 Nov 2026)

Channel: **The Bill, Explained** · handle **@TheBillExplained** · faceless, everyday-America economics.
Promise: "Why everyday things cost what they cost." New long video ("new bill") every Wednesday, 12 PM ET (19:00 Cairo).

## Idea
Every video is a **bill/receipt** for something people pay for. Each item on the receipt shows a price of "$?.??", which is the
question; the TOTAL row is highlighted in yellow, and that is the answer the video explains.

## Files (`brand/`, rebuilt by code; no AI images)
| File | Use |
|---|---|
| `logo_800.png` | Profile picture (YouTube crops it to a circle; `logo_98_preview.png` shows the small size) |
| `banner_2560x1440.png` | Channel banner. Text sits inside the 1546x423 all-device safe area. `banner_safe_check.png` is a check only, never upload it |
| `watermark_150.png` | Video watermark (Studio > Customisation > Branding) |
| `thumb_demo_diesel.png` | Thumbnail template demo (old fuel-pump photo from the Ask Habibi archive, cropped; re-check its licence before any real upload) |

Rebuild everything: `E:/AskHabibiAI/venv-chatterbox/Scripts/python.exe tools/brandkit.py`. Thumbnails come from `tools/thumbkit.py` (`thumb(photo, crop, tag, strip_text, out)`).

## Colours
| Name | Hex | Use |
|---|---|---|
| Ink | #121212 | text, banner background |
| Paper | #F4F0E7 | receipts (with light grain) |
| Price red | #D62820 | price tag, logo background |
| Highlighter | #FFD400 | marker swipe under the key word or row, nothing else |
| Grey | #807A70 | dotted leaders, secondary rows |

## Fonts (Windows system fonts, used as rendered images)
- Wordmark: Arial Black.
- Money numbers on thumbnails: Impact.
- Receipt print: Consolas / Consolas Bold.

## Thumbnail rules
1. One REAL object photo (Pexels / public domain), big, filling the frame. No faces unless men only; no women ever; no AI images; no potato.
2. One red price tag holding the money number (`+$2.00`, `$65,000`, `$13B`). It is placed automatically clear of the bottom-right timestamp.
3. Optional torn receipt strip at the top-left with 2-4 mono words and a highlighter swipe. It must never repeat the title.
4. Check the 320x180 `_small.png` before uploading: the number must read at phone size.
5. Avoid brand logos on products where possible (crop them out, as the demo does with the Coke ad).

## Don'ts (carried over from our design rules)
No glow, no bordered "cards", no dot wordmarks, no stock-template look, no cartoon stand-ins for real things.
