# sheet235.ps1 -Label <capture label> -T0 <s> -T1 <s> -Step <frames> -Out <png> [-Start 3.0] [-Cols 8] [-Crop x0,y0,x1,y1] [-Scale 0.5]
# Time-stamped frame strip from an unedited 30 fps capture (Saved/Codex/SHME_V138_20260927/Video/<label>/fNNNNN.jpg, frame 1 = capture
# start). Every tile carries its game time; nothing is interpolated or re-timed. (System.Drawing: no PIL in the project interpreters.)
param([string]$Label, [double]$T0, [double]$T1, [int]$Step = 2, [string]$Out, [double]$Start = 3.0, [int]$Cols = 8, [string]$Crop = "0,0,0,0", [double]$Scale = 0.5, [string]$Root = "")
Add-Type -AssemblyName System.Drawing
if (-not $Root) { $Root = Join-Path $PSScriptRoot "..\..\Saved\Codex\SHME_V138_20260927\Video" }
$V = Join-Path $Root $Label
$c = $Crop.Split(',') | ForEach-Object { [int]$_ }
$tiles = @(); $k = [int][math]::Round(($T0 - $Start) * 30) + 1
while ($Start + ($k - 1) / 30.0 -le $T1 + 1e-6) {
  $p = Join-Path $V ("f{0:D5}.jpg" -f $k)
  if (Test-Path $p) { $tiles += ,@($p, ($Start + ($k - 1) / 30.0)) }
  $k += $Step
}
if ($tiles.Count -eq 0) { Write-Output "no frames"; exit 1 }
$im0 = [System.Drawing.Image]::FromFile($tiles[0][0])
if ($c[2] -gt $c[0]) { $sw = $c[2] - $c[0]; $sh = $c[3] - $c[1] } else { $c = @(0, 0, $im0.Width, $im0.Height); $sw = $im0.Width; $sh = $im0.Height }
$im0.Dispose()
$w = [int]($sw * $Scale); $h = [int]($sh * $Scale); $rows = [math]::Ceiling($tiles.Count / $Cols)
$S = New-Object System.Drawing.Bitmap ($w * $Cols), ($h * $rows)
$g = [System.Drawing.Graphics]::FromImage($S); $g.Clear([System.Drawing.Color]::FromArgb(20, 20, 20))
$font = New-Object System.Drawing.Font "Arial", 11; $bk = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::Black); $ye = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::Yellow)
for ($i = 0; $i -lt $tiles.Count; $i++) {
  $im = [System.Drawing.Image]::FromFile($tiles[$i][0]); $x = ($i % $Cols) * $w; $y = [math]::Floor($i / $Cols) * $h
  $g.DrawImage($im, (New-Object System.Drawing.Rectangle $x, $y, $w, $h), (New-Object System.Drawing.Rectangle $c[0], $c[1], $sw, $sh), [System.Drawing.GraphicsUnit]::Pixel)
  $g.FillRectangle($bk, $x, $y, 62, 18); $g.DrawString(("{0:F2} s" -f $tiles[$i][1]), $font, $ye, ($x + 2), ($y + 1)); $im.Dispose()
}
$S.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $S.Dispose()
Write-Output ("SHEET {0} {1} tiles {2}x{3}" -f $Out, $tiles.Count, ($w * $Cols), ($h * $rows))
