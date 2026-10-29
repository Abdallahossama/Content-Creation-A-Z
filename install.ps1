# Install Content-Creation-A-Z as Claude Code skills (Windows).
#   powershell -ExecutionPolicy Bypass -File install.ps1
# Copies (never deletes): the repo -> ~/.claude/skills/content-creation-a-z, each skills/* folder -> ~/.claude/skills/<name>,
# the voice profile -> ~/.claude/youtube/voice.md (only if none exists yet).
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$skills = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force $skills | Out-Null

$main = Join-Path $skills "content-creation-a-z"
New-Item -ItemType Directory -Force $main | Out-Null
Get-ChildItem $repo -Force | Where-Object { $_.Name -notin @(".git", "_build") } | ForEach-Object { Copy-Item $_.FullName -Destination $main -Recurse -Force }
Write-Host "skill: content-creation-a-z"

Get-ChildItem (Join-Path $repo "skills") -Directory | Where-Object { $_.Name -ne "youtube-profile" } | ForEach-Object {
    $dst = Join-Path $skills $_.Name
    New-Item -ItemType Directory -Force $dst | Out-Null
    Copy-Item (Join-Path $_.FullName "*") -Destination $dst -Recurse -Force
    Write-Host "skill: $($_.Name)"
}

$yt = Join-Path $HOME ".claude\youtube"
New-Item -ItemType Directory -Force $yt | Out-Null
$voice = Join-Path $yt "voice.md"
if (-not (Test-Path $voice)) { Copy-Item (Join-Path $repo "skills\youtube-profile\voice.md") $voice; Write-Host "voice profile installed" }
else { Write-Host "voice profile already exists, left as is: $voice" }
Write-Host "Done. Start a new session and ask for the content-creation-a-z skill."
