# Setting up on a new machine or account

## 1. Install the skills
- Windows: `powershell -ExecutionPolicy Bypass -File install.ps1`   ·   macOS/Linux: `bash install.sh`
- This copies the repo as the `content-creation-a-z` skill and each `skills/*` folder (yt-*, habibi-video) into `~/.claude/skills/`,
  and the YouTube voice profile into `~/.claude/youtube/voice.md`.
- Optional: copy `docs/memory/*.md` into the new account's Claude memory folder so the learned rules load automatically
  (or just let the skill point at them).

## 2. Tools the scripts expect
| Tool | Used for | Notes |
|---|---|---|
| `uv` | runs every script: `uv run --no-project --with pillow --with numpy --with soundfile python <script>` | The Windows Store `python` is a stub; use uv. uv's Python 3.11 link broke once → use 3.12. |
| `ffmpeg` / `ffprobe` | render pipes, audio decode, 2-pass Shorts copies | on PATH |
| `faster-whisper` (medium.en) | per-line VO QA, word timings | `HF_HOME=E:/AskHabibiAI/hf HF_HUB_OFFLINE=1` once cached |
| `rapidocr_onnxruntime` | document line boxes (`ocr_docs.py`) | run alone, not beside Chatterbox |
| Chatterbox Turbo (MIT) | the cloned narrator | `tools/local-ai/setup_voice.sh`; venv Python 3.12; `HF_HUB_DISABLE_XET=1`; `setuptools<80`; reference clip of the owner's voice (not in this repo) |
| Fonts | Impact-like condensed, a typewriter face, a serif, Rubik Bold | from `_style_kit/fonts` (not in repo: licences vary) |
| Music | Kevin MacLeod (incompetech.com), CC BY 4.0 | re-download into `_music_library/` |
| SFX | Mixkit | re-download into `_newchannel/sfx/` (names in the scripts) |
| Claude in Chrome | YouTube Studio automation | see 03-YOUTUBE-STUDIO-PLAYBOOK |

## 3. Paths
Scripts hard-code the owner's layout: `D:/why habibi/_newchannel/...`, `D:/why habibi/_style_kit/...`, `D:/why habibi/_music_library/`,
`E:/AskHabibiAI/...`. On a new machine either recreate that layout or search-replace the `ROOT` / `M` / `MUS` / `SFXD` constants
at the top of each script.

## 4. What is NOT in this repo (on purpose)
Media (photos, film, maps, music, SFX), rendered videos, thumbnails, voice recordings and the voice reference clip, model weights,
venvs, logs, draft backups. Everything text/code is here; assets are re-fetched from each episode's `research/assets.md` (URLs + licences).
