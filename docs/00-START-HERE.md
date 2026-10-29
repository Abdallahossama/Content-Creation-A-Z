# Start here: the map

## The channels

| Channel | What it is | Status (Oct-Nov 2026) |
|---|---|---|
| **The Last Hours** (@TheLastHoursDocs, Studio `UC-BYTy_ucM8VC30PaOglijg`) | Hour-by-hour true stories (mysteries, disappearances, purges, last nights) told **only from the record**: FBI/Army/State files, court records, 1940s-80s newspapers. Faceless, cloned narrator voice, "Case File" look, burned-in captions. | **The main focus.** 2 long videos a week (Sun + Mon 22:00 Cairo), 1 Short a day (19:00 Cairo). |
| **Ask Habibi** (@AskHabibi, `UCJXUO3S0AtoQvmWHqpGp_ow`) | Midnight-curiosity explainers (sleep, body, news on maps) in a "Cut & Marker" style with a real-potato mascot (Batata), edited in CapCut. | Paused after its scheduled videos (owner, 24 Oct). |

Audience target for both: USA first, then Canada, UK/Europe (high-pay viewers). Use US units and dollars.

## The working folders (Windows, on the owner's machine)

| Path | What |
|---|---|
| `D:\why habibi\_newchannel\` | The Last Hours: one folder per file (`01_alcatraz` … `13_goering_last_night`), shared engine `lastkit.py`, `vidclip.py`, `thumbs_hakawi.py`, `_tools\`, `_cta\`, `LESSONS.md`, `PINNED_COMMENTS.txt` |
| `D:\why habibi\_pipeline\` | Ask Habibi pipeline (README = playbook), `core\` CapCut draft writers, `episodes\`, `shorts\` |
| `D:\why habibi\_style_kit\` | Ask Habibi look: README, STYLE_RULES, DOC_MODE, `tools\` (audio_master, mapkit, shortkit, cinekit, endcard…) |
| `D:\why habibi\_music_library\` | Kevin MacLeod (incompetech, CC BY 4.0) tracks: the only music we use |
| `D:\why habibi\_newchannel\sfx\` | Our SFX library (Mixkit) |
| `E:\AskHabibiAI\` | Local AI: Chatterbox voice clone (`venv-chatterbox`, `voice\ref_s01_12s.wav`), Qwen3-TTS backup, Blender |
| `C:\Users\<you>\.claude\skills\` | The yt-* skills + habibi-video skill |

In this repo the same material is under `tools/`, `examples/`, `docs/` (code and text only: no media, renders or voices).

## The system in one picture

```
topic (yt-viral, breakout formulas, owner)
  → research sub-agents: facts (research.md: safe lines + do-not-say) ‖ visuals (assets.md: PD download list)
  → owner approves downloads → dl_assets.py
  → hooks (hookscore ≥ 70) → script vo_lines.txt (every claim from safe lines)
  → voice: vo_chatterbox.py (cloned voice) → transcribe_lines.py (whisper QA) → fix_lines.py (re-take bad lines)
  → render_<file>.py (SHOTS + OV lists; docs spotlighted on the spoken word; captions; film finish) → QA sheet → full render
  → thumbnails (owner approves) + titles (title.py) → UPLOAD_COPY_PASTE.txt
  → Studio: upload, schedule, A/B test, captions, end screen, playlist
  → teaser Shorts (teasers_more.py) naming the long video → related-video link
  → on publish: pinned + hearted comment → analytics review → LESSONS.md
```

## Where the knowledge lives

- `docs/01-OWNER-RULES.md`: every standing rule, in one place.
- `docs/the-last-hours/LESSONS.md`: the channel's lessons from real Studio data (read before every new file).
- `docs/memory/*.md`: the dated feedback memories behind those rules (search them).
- `examples/the-last-hours/<file>/`: real research, scripts, plans, credits and upload sheets for 13 files.
- `examples/the-last-hours/13_goering_last_night/` is the newest, cleanest reference build.
