# compare_sheets.ps1 -Pilot <dir> -Out <dir> : side-by-side BEFORE | AFTER G1 | AFTER G1+G2+G3 sheets for the 13 stations, walk frames every
# 1 s and pan frames every 1 s (same frame numbers = same game time, fixed-step capture). Uses mini.ps1 (labels = file names).
param([string]$Pilot, [string]$Out)
$mini = Join-Path $PSScriptRoot 'mini.ps1'; New-Item -ItemType Directory -Force $Out | Out-Null
$sets = @('clean_before', 'after_g1', 'after_g123')
$stills = @('approach_forward','approach_left90','approach_right90','approach_lookback','compression_forward','compression_left90','compression_right90','compression_lookback','release_forward','release_left90','release_right90','release_lookback','release_house')
foreach ($s in $stills) { $f = @(); foreach ($k in $sets) { $f += (Join-Path $Pilot "$k\stills\$s.png") }; & $mini -Out (Join-Path $Out "station_$s.png") -Scale 0.33 -Cols 3 @f | Out-Null }
foreach ($k in $sets) { $f = @(); foreach ($n in 1, 31, 61, 91, 121, 151, 181, 211, 241, 271, 301, 331, 361) { $f += (Join-Path $Pilot ("$k\frames\f{0:D5}.jpg" -f $n)) }; & $mini -Out (Join-Path $Out "walk_1fps_$k.png") -Scale 0.25 -Cols 13 @f | Out-Null }
foreach ($p in 'compression', 'release') { foreach ($k in $sets) { $f = @(); foreach ($n in 1, 31, 61, 91, 121, 151, 181) { $f += (Join-Path $Pilot ("$k\frames_pan_$p\f{0:D5}.jpg" -f $n)) }; & $mini -Out (Join-Path $Out "pan_${p}_$k.png") -Scale 0.25 -Cols 7 @f | Out-Null } }
"COMPARE_SHEETS done $Out"
