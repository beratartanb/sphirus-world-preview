# pack_v7.ps1 -Vmp <scratchpad\vmp> -Dst <report folder>\v7 : collects the Environment Visual Master Pass evidence for publication.
# PNG stills / sheets -> JPEG q90 (System.Drawing; unedited pixels, only re-encoded), AVIs, perf / camera / spec / look / manifest JSON.
param([string]$Vmp, [string]$Dst, [string]$Manifest)
Add-Type -AssemblyName System.Drawing
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters 1; $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 90L
function Jpg($src, $dstDir) { New-Item -ItemType Directory -Force $dstDir | Out-Null; $im = [System.Drawing.Image]::FromFile($src)
  $im.Save((Join-Path $dstDir ([IO.Path]::GetFileNameWithoutExtension($src) + '.jpg')), $enc, $ep); $im.Dispose() }
foreach ($set in 'V0', 'V1', 'V2', 'V3', 'TRIAL', 'TRIAL2', 'TRIAL3') { Get-ChildItem (Join-Path $Vmp "$set\stills") -Filter *.png | ForEach-Object { Jpg $_.FullName (Join-Path $Dst "stills\$set") } }
foreach ($w in 'walk_vmp_before', 'walk_vmp_trial3') { Get-ChildItem (Join-Path $Vmp "$w\stills") -Filter *.png | ForEach-Object { Jpg $_.FullName (Join-Path $Dst "stills\$w") } }
Get-ChildItem (Join-Path $Vmp 'cmp3') -Filter *.png | ForEach-Object { Jpg $_.FullName (Join-Path $Dst 'compare\V0_vs_TRIAL3') }
foreach ($f in 'cmp2\overview_forward_V0_vs_TRIAL2.png', 'cmp2\release_3way.png', 'cmp2\rear_disc_crop.png', 'cmp2\release_crop.png', 'variants_compare.png', 'trial_vs_v0_trail.png',
               'zoom_check.png', 'video\walk_sheet_4s.png', 'lookat\lookat_sheet.png', 'lookat\lookat_sheet2.png') { Jpg (Join-Path $Vmp $f) (Join-Path $Dst 'compare\iteration') }
New-Item -ItemType Directory -Force (Join-Path $Dst 'video'), (Join-Path $Dst 'data') | Out-Null
Copy-Item (Join-Path $Vmp 'video\*.avi') (Join-Path $Dst 'video') -Force
foreach ($f in 'perf\*.json', 'perf\*.txt', 'trial_spec.json', 'trial_spec2.json', 'build_build.json', 'build_remove.json', 'look_original.json', 'look_applied_*.json', 'area_probe.json',
               'chain1.out', 'chain2.out', 'chain3.out', 'vmpcol.json') { Copy-Item (Join-Path $Vmp $f) (Join-Path $Dst 'data') -Force }
foreach ($s in 'V0', 'V1', 'V2', 'V3', 'TRIAL', 'TRIAL2', 'TRIAL3') { Copy-Item (Join-Path $Vmp "$s\stations_log.json") (Join-Path $Dst "data\stations_log_$s.json") -Force }
foreach ($w in 'walk_vmp_before', 'walk_vmp_trial2', 'walk_vmp_trial3') { Copy-Item (Join-Path $Vmp "$w\trailwalk_log.json") (Join-Path $Dst "data\trailwalk_log_$w.json") -Force }
if ($Manifest) { Copy-Item $Manifest (Join-Path $Dst 'data\manifest_vmp_map.json') -Force }
"PACK_V7 done $Dst"
