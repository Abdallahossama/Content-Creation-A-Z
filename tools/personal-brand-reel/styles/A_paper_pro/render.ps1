param([string]$Only = "")
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$root = "D:\codebyabdullah_assets\workspace\edit_paper"
$prof = "$root\edge_profile"
Get-Content "$root\render_list.txt" -Encoding UTF8 | ForEach-Object {
  $p = $_.Split("|"); $n = $p[0]; $w = $p[1]; $h = $p[2]
  if ($Only -ne "" -and $n -notlike $Only) { return }
  $uri = ([System.Uri]"$root\html\$n.html").AbsoluteUri
  $out = "$root\png\$n.png"
  & $edge --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files --user-data-dir="$prof" `
    --default-background-color=00000000 --window-size="$w,$h" --virtual-time-budget=4000 --screenshot="$out" $uri 2>$null | Out-Null
  if (Test-Path $out) { "ok $n" } else { "FAIL $n" }
}
