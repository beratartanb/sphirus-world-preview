# pack_xr.ps1 -Cap <scratch xrcap> -Xr <Saved/Codex/ExteriorRedesign_20261031> -Dst <short output dir> : Exterior World Redesign evidence for
# publication. PNG stills/sheets -> JPEG q90 (re-encoded only), plan maps stay PNG, AVIs, design/plan/apply/perf JSON, walk logs, tools.
param([string]$Cap, [string]$Xr, [string]$Dst)
Add-Type -AssemblyName System.Drawing
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters 1; $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 90L
function Jpg($src, $dstDir, $name = $null) { New-Item -ItemType Directory -Force $dstDir | Out-Null; $im = [System.Drawing.Image]::FromFile($src)
  if (-not $name) { $name = [IO.Path]::GetFileNameWithoutExtension($src) }; $im.Save((Join-Path $dstDir ($name + '.jpg')), $enc, $ep); $im.Dispose() }
foreach ($s in 'before_clay_st', 'before_lit_st', 'after_clay_st', 'after_lit_st') {
  $n = $s -replace '^after', 'after_r5'; Get-ChildItem (Join-Path $Cap "$s\stills") -Filter *.png | ForEach-Object { Jpg $_.FullName (Join-Path $Dst "stills\$n") } }
Get-ChildItem (Join-Path $Cap 'after_lit_walk\stills') -Filter *.png | ForEach-Object { Jpg $_.FullName (Join-Path $Dst 'stills\after_r5_lit_walk_stations') }
Get-ChildItem (Join-Path $Cap 'cmp_r5') -Filter *.png | ForEach-Object { Jpg $_.FullName (Join-Path $Dst 'compare\final_r5_2x2') }
foreach ($r in 'r2', 'r3', 'r4') { foreach ($m in 'CLAY', 'LIT') { Jpg (Join-Path $Cap "cmp_$r\overview_forward_$m.png") (Join-Path $Dst 'compare\iterations') "${r}_overview_forward_$m" }
  foreach ($v in 'climb_forward', 'compression_forward', 'saddle_house') { Jpg (Join-Path $Cap "cmp_$r\cmp_$v.png") (Join-Path $Dst 'compare\iterations') "${r}_cmp_$v" } }
New-Item -ItemType Directory -Force (Join-Path $Dst 'maps'), (Join-Path $Dst 'video'), (Join-Path $Dst 'data'), (Join-Path $Dst 'tools') | Out-Null
foreach ($f in 'MASTERPLAN.png', 'masterplan_base.png', 'before_plan.png', 'before_clay.png', 'before_mass.png', 'R1_FINAL_before_vs_r5.png', 'R1_after5_plan.png', 'R1_after5_clay.png',
               'R1_after5_mass.png', 'R1_sections_r4_labeled.png', 'R1_compare_maps.png', 'R1_compare_r2.png', 'R1_mass_before_vs_r3.png') { Copy-Item (Join-Path $Xr "maps\$f") (Join-Path $Dst 'maps') -Force }
Rename-Item (Join-Path $Dst 'maps\R1_sections_r4_labeled.png') 'R1_sections_before_vs_final.png' -Force
Copy-Item (Join-Path $Cap 'video\*.avi') (Join-Path $Dst 'video') -Force
foreach ($f in 'design\plan_r*.json', 'design\apply_*.json', 'design\foliage_r5.json', 'design\height_before.png', 'design\height_r5.png', 'design\overlay_r5.json',
               'perf\*.json', 'perf\*.txt', 'recon\landscape.json', 'maps\overlay_master.json', 'maps\labels_master.json') { Copy-Item (Join-Path $Xr $f) (Join-Path $Dst 'data') -Force }
foreach ($w in 'before_lit_walk', 'before_clay_walk', 'after_lit_walk', 'after_clay_walk', 'before_lit_st', 'after_lit_st') { Copy-Item (Join-Path $Cap "$w\trailwalk_log.json") (Join-Path $Dst "data\log_$($w -replace '^after', 'after_r5').json") -Force }
Copy-Item (Join-Path $PSScriptRoot '*.py'), (Join-Path $PSScriptRoot '*.ps1') (Join-Path $Dst 'tools') -Force
Copy-Item (Join-Path $PSScriptRoot '..\AIToolingEval_20261031\triptych.ps1') (Join-Path $Dst 'tools') -Force
"PACK_XR done $Dst"
