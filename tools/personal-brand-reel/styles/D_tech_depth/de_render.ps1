param([string]$Root)
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$prof = "D:\codebyabdullah_assets\workspace\edit_styles\D\edge_profile_de"
New-Item -ItemType Directory -Force "$Root\png" | Out-Null
Get-Content "$Root\render_list.txt" -Encoding UTF8 | ForEach-Object {
  $p = $_.Split("|"); $n = $p[0]; $w = $p[1]; $h = $p[2]
  $uri = ([System.Uri]"$Root\html\$n.html").AbsoluteUri
  $out = "$Root\png\$n.png"
  if (Test-Path $out) { Remove-Item $out -Force }
  & $edge --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files --user-data-dir="$prof" `
    --default-background-color=00000000 --window-size="$w,$h" --virtual-time-budget=4000 --screenshot="$out" $uri 2>$null | Out-Null
  if (-not (Test-Path $out)) { "FAIL $n" }
}
"rendered"
