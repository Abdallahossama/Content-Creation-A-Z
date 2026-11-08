# Renders <dir>\html\<name>.html -> <dir>\png\<name>.png for every "name|w|h" row in <dir>\render_list.txt.
# NOTE: reconstructed after the D/E agent accidentally overwrote the original on 8 Nov 06:50.
# Accepts a folder name relative to edit_styles (e.g. B) or a full path; with no argument, uses the current folder.
param([string]$Dir = "", [string]$Only = "")
$base = "D:\codebyabdullah_assets\workspace\edit_styles"
if ($Dir -eq "") { $root = (Get-Location).Path }
elseif ([System.IO.Path]::IsPathRooted($Dir)) { $root = $Dir }
else { $root = Join-Path $base $Dir }
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$prof = "$base\edge_profile"
New-Item -ItemType Directory -Force "$root\png" | Out-Null
Get-Content "$root\render_list.txt" -Encoding UTF8 | ForEach-Object {
  $p = $_.Split("|"); $n = $p[0]; $w = $p[1]; $h = $p[2]
  if ($Only -ne "" -and $n -notlike $Only) { return }
  $uri = ([System.Uri]"$root\html\$n.html").AbsoluteUri
  $out = "$root\png\$n.png"
  & $edge --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files --user-data-dir="$prof" `
    --default-background-color=00000000 --window-size="$w,$h" --virtual-time-budget=4000 --screenshot="$out" $uri 2>$null | Out-Null
  if (Test-Path $out) { "ok $n" } else { "FAIL $n" }
}
