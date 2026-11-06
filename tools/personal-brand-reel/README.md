# personal-brand-reel

Edit engine for Abdullah's on-camera reels (see docs/10-PERSONAL-BRAND-PLAYBOOK.md).

1. `ffmpeg -i raw.mp4 -af "highpass=f=80,afftdn=nr=10,loudnorm=I=-16" -ac 1 -ar 16000 audio16k.wav`
2. `HF_HOME=E:/AskHabibiAI/hf uv run --no-project --python 3.12 --with faster-whisper python chunks.py`
   (edit the `cuts` list to the silencedetect pauses) → pick the last full take of each line.
3. Write `plan.json` (src, keep [start,end,zoom], captions [start,end,text,orange word]).
4. `python build.py plan.json` with `"captions": []` and `"out": "base.mp4"` → graded, cut, clean voice.
   Then run build.py's caption part to write `captions.ass` (see build4 header).
5. Cards: edit `card.html`, render each card with headless Edge (900×640, transparent) into `broll/`;
   site screenshots 1280×800 into `broll/site_*.png`.
6. `python build4.py music <out.mp4>` and `python build4.py halal <out.mp4>`.
Fonts: put Alexandria-ExtraBold.ttf (full Google Fonts TTF) in `fonts/`.
