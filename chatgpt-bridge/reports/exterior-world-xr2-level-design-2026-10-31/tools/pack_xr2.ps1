# pack_xr2.ps1 -Cap <scratch xr2> -Xr <Saved/Codex/ExteriorWorld_XR2_20261031> -Dst <pub dir> : XR2 evidence for publication.
# Player-camera sheets / navigation strips / stills -> JPEG q88 (re-encoded only, no edits); maps stay PNG; AVIs; JSON/TXT data; tools.
param([string]$Cap, [string]$Xr, [string]$Dst)
Add-Type -AssemblyName System.Drawing
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters 1; $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 88L
function Jpg($src, $dstDir, $name = $null) { New-Item -ItemType Directory -Force $dstDir | Out-Null; $im = [System.Drawing.Image]::FromFile($src)
  if (-not $name) { $name = [IO.Path]::GetFileNameWithoutExtension($src) }; $im.Save((Join-Path $dstDir ($name + '.jpg')), $enc, $ep); $im.Dispose() }
foreach ($p in 'cmp_clay8_', 'cmp_lit_', 'cmp_look_') { Get-ChildItem $Cap -Filter "$p*.png" | ForEach-Object { Jpg $_.FullName (Join-Path $Dst 'compare') } }
Jpg (Join-Path $Cap 'cmp_x7x8_D06_glade.png') (Join-Path $Dst 'compare\iterations') 'x7_vs_x8_D06_glade_clay'
Jpg (Join-Path $Cap 'x7lit_a.png') (Join-Path $Dst 'compare\iterations') 'x7_lit_glade_eastbank_backyard'
Get-ChildItem (Join-Path $Cap 'nav_clayA') -Filter 'strip_*.png' | ForEach-Object { Jpg $_.FullName (Join-Path $Dst 'navigation_clay') }
foreach ($s in 'views_before_clay', 'views_before_lit', 'views_after_clay', 'views_after_lit', 'views_dress', 'views_cine') {
  Get-ChildItem (Join-Path $Cap $s) -Filter '*_fwd.png' | ForEach-Object { Jpg $_.FullName (Join-Path $Dst "stills\$s") }
  Get-ChildItem (Join-Path $Cap $s) -Filter '*_back.png' | ForEach-Object { Jpg $_.FullName (Join-Path $Dst "stills\$s") } }
New-Item -ItemType Directory -Force (Join-Path $Dst 'maps'), (Join-Path $Dst 'video'), (Join-Path $Dst 'data'), (Join-Path $Dst 'tools') | Out-Null
foreach ($f in 'XR2_x8_MASTERPLAN.png', 'CMP_probes_before_vs_x8.png', 'CMP_walk_before_vs_x8.png', 'CMP_geo_before_vs_x8.png', 'CMP_clay_before_vs_x8.png',
               'AFTER_x7_probes.png', 'alt_r6A.png', 'alt_r6B.png', 'alt_r6C.png', 'wide_plan_grid.png', 'x1_plan.png', 'x5_geo_crop.png') {
  $p = Join-Path $Xr "maps\$f"; if (Test-Path $p) { Copy-Item $p (Join-Path $Dst 'maps') -Force } }
Copy-Item (Join-Path $Xr 'video\*.avi') (Join-Path $Dst 'video') -Force
foreach ($f in 'data\*.json', 'data\*.txt', 'perf\*.json', 'design\plan_x8.json', 'design\spawn_x8.json', 'design\overlay_x8.json', 'design\apply_*_x8.json', 'design\apply_*_x7.json',
               'maps\BEFORE_walk.json', 'maps\x7_walk.json', 'maps\x8_walk.json', 'maps\BEFORE_geodesic.json', 'maps\x8_geodesic.json', 'recon\probe_assets.json', 'recon\probe_landscape.json') {
  Copy-Item (Join-Path $Xr $f) (Join-Path $Dst 'data') -Force -ErrorAction SilentlyContinue }
foreach ($t in 'probe_before', 'probe_after_x7', 'probe_after') { Copy-Item (Join-Path $Xr "cap\$t\probe_log.json") (Join-Path $Dst "data\${t}_log.json") -Force }
foreach ($w in 'views_before_clay', 'views_after_clay', 'views_after_lit') { Copy-Item (Join-Path $Cap "$w\views_log.json") (Join-Path $Dst "data\${w}_log.json") -Force }
Copy-Item (Join-Path $PSScriptRoot '*.py'), (Join-Path $PSScriptRoot '*.ps1'), (Join-Path $PSScriptRoot '*.sh') (Join-Path $Dst 'tools') -Force
"PACK_XR2 done $Dst"
