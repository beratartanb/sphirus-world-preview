# vmp_compare.ps1 -Vmp <scratchpad\vmp> -Out <dir> [-A V0] [-B TRIAL2] : BEFORE | AFTER station comparisons of the Environment Visual
# Master Pass. Per station+direction a 2-column sheet (A | B, scale 0.5) and one overview (A row over B row, forward views, scale 0.25).
# Stills are copied to <Out>\lab\<set>_<still>.png first because mini.ps1 labels each tile with its file name.
param([string]$Vmp, [string]$Out, [string]$A = 'V0', [string]$B = 'TRIAL2')
$mini = Join-Path $PSScriptRoot 'mini.ps1'; $lab = Join-Path $Out 'lab'; New-Item -ItemType Directory -Force $Out, $lab | Out-Null
$st = @('house_front', 'pond_shore', 'trail_house_side', 'trail_rear_entry', 'trail_compression', 'trail_release', 'uphill_lookback')
$dirs = @('forward', 'left90', 'right90')
foreach ($s in $st) { foreach ($d in $dirs) {
  $f = @(); foreach ($k in $A, $B) { $src = Join-Path $Vmp "$k\stills\${s}_$d.png"; if (Test-Path $src) { $dst = Join-Path $lab "${k}_${s}_$d.png"; Copy-Item $src $dst -Force; $f += $dst } }
  if ($f.Count -eq 2) { & $mini -Out (Join-Path $Out "cmp_${s}_$d.png") -Scale 0.5 -Cols 2 @f | Out-Null } } }
$f = @(); foreach ($k in $A, $B) { foreach ($s in $st) { $f += (Join-Path $lab "${k}_${s}_forward.png") } }
& $mini -Out (Join-Path $Out "overview_forward_${A}_vs_$B.png") -Scale 0.25 -Cols 7 @f | Out-Null
"VMP_COMPARE done $Out"
