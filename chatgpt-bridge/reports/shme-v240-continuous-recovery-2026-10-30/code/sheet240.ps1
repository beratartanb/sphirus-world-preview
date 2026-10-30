# sheet240.ps1 -Lab <capture label> -T0 <s> -T1 <s> -Step <frames> -Out <png> [-Start 3.8] [-Cols 8] [-Scale 0.3]
# Time-stamped frame strip from an unedited 30 fps capture (Saved/Codex/SHME_V138_20260927/Video/<label>/fNNNNN.jpg, frame 1 = -Start s).
# Every tile carries its game time; nothing is interpolated or re-timed. (PIL-free copy of sheet235.py.)
param([string]$Lab, [double]$T0, [double]$T1, [int]$Step, [string]$Out, [double]$Start = 3.8, [int]$Cols = 8, [double]$Scale = 0.3)
Add-Type -AssemblyName System.Drawing
$V = Join-Path $PSScriptRoot "..\..\Saved\Codex\SHME_V138_20260927\Video\$Lab"
$k = [int][math]::Round(($T0 - $Start) * 30) + 1; $tiles = @()
while ($Start + ($k - 1) / 30.0 -le $T1 + 1e-6) {
  $p = Join-Path $V ('f{0:D5}.jpg' -f $k)
  if (Test-Path $p) { $tiles += ,@($p, ($Start + ($k - 1) / 30.0)) }
  $k += $Step
}
if ($tiles.Count -eq 0) { Write-Output "NO_FRAMES $V"; exit 1 }
$im0 = [System.Drawing.Image]::FromFile($tiles[0][0]); $w = [int]($im0.Width * $Scale); $h = [int]($im0.Height * $Scale); $im0.Dispose()
$rows = [math]::Ceiling($tiles.Count / $Cols)
$bmp = New-Object System.Drawing.Bitmap ($w * $Cols), ($h * $rows); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::Black); $font = New-Object System.Drawing.Font 'Arial', 14, ([System.Drawing.FontStyle]::Bold)
for ($i = 0; $i -lt $tiles.Count; $i++) {
  $im = [System.Drawing.Image]::FromFile($tiles[$i][0]); $x = ($i % $Cols) * $w; $y = [math]::Floor($i / $Cols) * $h
  $g.DrawImage($im, $x, $y, $w, $h); $im.Dispose()
  $g.FillRectangle([System.Drawing.Brushes]::Black, $x, $y, 78, 22); $g.DrawString(('{0:F2} s' -f $tiles[$i][1]), $font, [System.Drawing.Brushes]::Yellow, ($x + 2), ($y + 1))
}
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose()
Write-Output "SHEET $Out $($tiles.Count) tiles"
