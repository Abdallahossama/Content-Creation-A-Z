# Re-stage everything from the working folders, scan for secrets, commit and push.
#   powershell -ExecutionPolicy Bypass -File _build\sync.ps1 "what changed"
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $repo
uv run --no-project python _build/stage.py
if ($LASTEXITCODE -ne 0) { throw "staging stopped (see the message above): nothing committed" }
$msg = if ($args.Count -gt 0) { $args[0] } else { "Sync working folders $(Get-Date -Format 'yyyy-MM-dd HH:mm')" }
git add -A
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host "Nothing changed."; exit 0 }
git commit -m $msg
git push
