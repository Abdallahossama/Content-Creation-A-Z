# 11 · Third-party video tools (git submodules)

Added 6 Nov 2026 at the owner's request. They live in `third_party/` as **pinned git
submodules**: links to the original projects at a fixed commit, not copies. After cloning this repo run:

```
git submodule update --init --recursive
```

Update one later: `cd third_party/<name> && git pull && cd ../.. && git add third_party/<name> && git commit`.

| Folder | Project | Licence | What it is | Use it for |
|---|---|---|---|---|
| `third_party/claude-shorts` | [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) | MIT | `/shorts` skill: long video → scored clip candidates → Remotion animated captions → TikTok/Reels/Shorts exports | Cutting Shorts out of a long video (Last Hours teasers, long personal-brand videos) |
| `third_party/ffmpeg-skill` | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | MIT | 42 local FFmpeg tools + MCP server: cut, captions, reframe, silence removal, loudness, platform exports and checks | Fast single edits and delivery checks instead of hand-written ffmpeg |
| `third_party/OpenMontage` | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | **AGPL-3.0** | Full agentic production studio: 12 pipelines, 100+ tools, 92 agent skills in `.agents/skills` | Ideas and pipelines for bigger productions; read its `AGENTS.md` first |
| `third_party/VibeVoice` | [microsoft/VibeVoice](https://github.com/microsoft/VibeVoice) | MIT | Microsoft open-source voice AI: long-form TTS and VibeVoice-ASR (50+ languages, who/when/what, hotwords) | Candidate replacement for Whisper on Arabic captions; TTS alternative to Chatterbox |

## Rules before using them

- **Read before running.** None of their install/setup scripts has been run on this machine yet. Read
  `install.sh` / `setup.sh` / requirements first, install into its own venv (uv, Python 3.12), never globally.
- **C: is nearly full.** Put models and caches on D:/E: (`HF_HOME=E:/AskHabibiAI/hf`); VibeVoice models are
  several GB. Ask the owner before any large download.
- **OpenMontage is AGPL-3.0**: fine for private use; if code from it ever ships inside a public product or
  a hosted service, that product's source must be released too. Don't copy its code into Razqora or client work.
- Our own rules still win: copyright-safe assets only, two audio versions (music + halal) for personal-brand
  reels, captions in Alexandria with `shaping=complex`, the approved grade (`docs/10-PERSONAL-BRAND-PLAYBOOK.md`).
- To use a skill in Claude Code, copy or link its folder into `~/.claude/skills/<name>/` (claude-shorts: repo
  root; ffmpeg-skill: repo root, its `.claude/skills/*` are the authors' own dev skills, don't install those).
