# sheet233.ps1 -Rows "dirA,dirB" -Frames "60,105,150,210,270" -Out <png> [-Scale 0.3] : contact sheet (rows = capture folders, columns = frames)
param([string]$Rows, [string]$Frames, [string]$Out, [double]$Scale = 0.3)
Add-Type -AssemblyName System.Drawing
$V = "C:\Users\berat\OneDrive\Documents\Unreal Projects\ActionAdventureMovementS\Saved\Codex\SHME_V138_20260927\Video"
$rowList = $Rows.Split(','); $frList = $Frames.Split(',') | ForEach-Object { [int]$_ }
$probe = [System.Drawing.Image]::FromFile((Join-Path (Join-Path $V $rowList[0]) ('f{0:D5}.jpg' -f $frList[0])))
$w = [int]($probe.Width * $Scale); $h = [int]($probe.Height * $Scale); $probe.Dispose()
$bmp = New-Object System.Drawing.Bitmap ($w * $frList.Count), ($h * $rowList.Count)
$g = [System.Drawing.Graphics]::FromImage($bmp); $font = New-Object System.Drawing.Font 'Arial', 11
for ($r = 0; $r -lt $rowList.Count; $r++) { for ($c = 0; $c -lt $frList.Count; $c++) {
  $p = Join-Path (Join-Path $V $rowList[$r]) ('f{0:D5}.jpg' -f $frList[$c])
  if (Test-Path $p) { $im = [System.Drawing.Image]::FromFile($p); $g.DrawImage($im, $c * $w, $r * $h, $w, $h); $im.Dispose() }
  $g.DrawString(("{0} f{1}" -f $rowList[$r].Replace('v233cap_',''), $frList[$c]), $font, [System.Drawing.Brushes]::Yellow, $c * $w + 4, $r * $h + 4) } }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); "OK $Out"
