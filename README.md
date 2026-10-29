# Content-Creation-A-Z

The full playbook, tools and learned rules of a two-channel faceless YouTube operation, packaged so any AI session
(Claude Code or similar) can pick it up and keep working the same way.

- **The Last Hours**: hour-by-hour true-history documentaries built only from public records.
- **Ask Habibi**: curiosity explainers edited in CapCut.

## Use it as a skill
```bash
git clone https://github.com/Abdallahossama/Content-Creation-A-Z.git
cd Content-Creation-A-Z
powershell -ExecutionPolicy Bypass -File install.ps1     # Windows
bash install.sh                                          # macOS / Linux
```
Then in a new session: *"Use the content-creation-a-z skill"* (or just ask for the next video). The AI should read
`SKILL.md` → `docs/00-START-HERE.md` → `docs/01-OWNER-RULES.md` → the playbook for the job.

## What's inside
| Folder | Contents |
|---|---|
| `SKILL.md` | Entry point for the AI |
| `docs/` | Start-here map, owner rules, Last Hours playbook, YouTube Studio playbook, growth & analytics, tools index, Ask Habibi playbook, setup; `memory/` = every learned rule with its date and reason; `the-last-hours/LESSONS.md` |
| `skills/` | The yt-* YouTube skills (MIT, Jake Schincariol: github.com/Jakeschincariol/youtube-agent-skill), the `habibi-video` skill, the voice profile |
| `tools/` | Render engines and helpers (Last Hours engine, CTA voice, mystery Shorts, Ask Habibi style kit and CapCut pipeline, local-AI setup) |
| `examples/` | Real research files, download lists, hooks, scripts, plans, credits and upload sheets for 13 Last Hours files and the Ask Habibi episodes |

## Keeping it updated
After each video: update `docs/the-last-hours/LESSONS.md` and the relevant `docs/memory/` files, then run
`powershell -File _build/sync.ps1` (re-stages everything from the working folders and pushes a commit).

Text and code only: no media, renders, voices or model weights (see `docs/07-SETUP-NEW-MACHINE.md`).
