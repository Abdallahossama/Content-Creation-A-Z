# UI depth (default reel style since 6 Nov 2026)

Panels with real content sit BEHIND the speaker (hair overlaps a corner) and small tags sit IN FRONT.

1. `uv run --python 3.12 --with mediapipe==0.10.14 --with opencv-python-headless python masks.py ../base.mp4 D:/codebyabdullah_assets/tmp_masks`
   (MediaPipe selfie mask per frame, smoothed over time).
2. Edit `make_panels.py` (panel text, file names, timings live in compose.py), run it, then render each `p/*.html`
   to a transparent 1080x1920 PNG with headless Edge (`--default-background-color=00000000`).
   `v2_css.txt` holds the look: solid #1D1D1D, #2A2A2A border, 14px radius, shadow to bottom-right (lamp on the left),
   orange rim on the lamp side, Alexandria + JetBrains Mono. Fix the font path in it for your machine.
3. `python compose.py` → `depth_video.mp4` (glow grade + behind panels + person + front panels + captions).
   Needs `../base.mp4`, `../glow.txt` (gbrp maskedmerge) and `../captions.ass` with Dialogue lines.
4. Mux audio from the music and halal mixes: `ffmpeg -i depth_video.mp4 -i v2_music.mp4 -map 0:v -map 1:a -c copy out.mp4`.

Anti-AI-look rules: max 1–2 panels on screen, real content only, no glass blur / gradients / glow / fake buttons,
one hand-made touch (marker circle, typing), every panel synced to the spoken word.
