#!/usr/bin/env bash
# Install Content-Creation-A-Z as Claude Code skills (macOS / Linux / Git Bash).
#   bash install.sh
# Copies (never deletes): the repo -> ~/.claude/skills/content-creation-a-z, each skills/* folder -> ~/.claude/skills/<name>,
# the voice profile -> ~/.claude/youtube/voice.md (only if none exists yet).
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
SK="$HOME/.claude/skills"; mkdir -p "$SK/content-creation-a-z"
for f in "$REPO"/* "$REPO"/.gitignore; do
  n="$(basename "$f")"; [ "$n" = "_build" ] && continue; cp -R "$f" "$SK/content-creation-a-z/"
done
echo "skill: content-creation-a-z"
for d in "$REPO"/skills/*/; do
  n="$(basename "$d")"; [ "$n" = "youtube-profile" ] && continue
  mkdir -p "$SK/$n"; cp -R "$d"* "$SK/$n/"; echo "skill: $n"
done
mkdir -p "$HOME/.claude/youtube"
if [ ! -f "$HOME/.claude/youtube/voice.md" ]; then cp "$REPO/skills/youtube-profile/voice.md" "$HOME/.claude/youtube/voice.md"; echo "voice profile installed"
else echo "voice profile already exists, left as is"; fi
echo "Done. Start a new session and ask for the content-creation-a-z skill."
