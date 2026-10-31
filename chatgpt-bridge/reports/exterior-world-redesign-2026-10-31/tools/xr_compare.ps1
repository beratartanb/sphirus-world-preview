# xr_compare.ps1 -Cap <dir with before_clay_st, after_clay_st, before_lit_st, after_lit_st> -Out <dir> [-Tag r2]
# Per station+direction a 2x2 sheet: CLAY BEFORE | CLAY AFTER (top) / LIT BEFORE | LIT AFTER (bottom), same player-camera pose.
# Plus overview sheets of all forward views (clay row pair and lit row pair). Stills are copied with set-prefixed names (mini.ps1 labels
# each tile with its file name). Unedited pixels, scaled only.
param([string]$Cap, [string]$Out, [string]$Tag = 'r2')
$mini = Join-Path $PSScriptRoot '..\AIToolingEval_20261031\mini.ps1'; $lab = Join-Path $Out 'lab'; New-Item -ItemType Directory -Force $Out, $lab | Out-Null
$sets = [ordered]@{ 'CLAY_BEFORE' = 'before_clay_st'; "CLAY_AFTER_$Tag" = 'after_clay_st'; 'LIT_BEFORE' = 'before_lit_st'; "LIT_AFTER_$Tag" = 'after_lit_st' }
$names = Get-ChildItem (Join-Path $Cap 'after_lit_st\stills') -Filter *.png | ForEach-Object { $_.BaseName }
foreach ($n in $names) {
  $f = @(); foreach ($k in $sets.Keys) { $src = Join-Path $Cap ($sets[$k] + "\stills\$n.png"); if (Test-Path $src) { $dst = Join-Path $lab "${k}__$n.png"; Copy-Item $src $dst -Force; $f += $dst } }
  if ($f.Count -eq 4) { & $mini -Out (Join-Path $Out "cmp_$n.png") -Scale 0.5 -Cols 2 @f | Out-Null } }
foreach ($m in 'CLAY', 'LIT') {
  $f = @(); foreach ($k in $sets.Keys | Where-Object { $_ -like "$m*" }) { foreach ($s in 'hub', 'gate', 'compression', 'crossing', 'climb', 'saddle') { $f += (Join-Path $lab "${k}__${s}_forward.png") } }
  & $mini -Out (Join-Path $Out "overview_forward_$m.png") -Scale 0.25 -Cols 6 @f | Out-Null }
"XR_COMPARE $($names.Count) stills -> $Out"
