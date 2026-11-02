# cropstrip242.ps1 -Lab <capture> -T0 -T1 -Step <frames> -Out <png> [-Start 1.9] [-Cols 6] [-CropW 560] [-CropH 900] [-CX 864] [-CY 540] [-Scale 0.6]
# Frame strip CROPPED around the tracked character (the side/diagonal cameras keep the pawn near the frame centre). Unedited pixels, time-stamped.
param([string]$Lab, [double]$T0, [double]$T1, [int]$Step, [string]$Out, [double]$Start = 1.9, [int]$Cols = 6, [int]$CropW = 560, [int]$CropH = 900, [int]$CX = 864, [int]$CY = 540, [double]$Scale = 0.6, [double]$Fps = 30)
Add-Type -AssemblyName System.Drawing
$V = Join-Path $PSScriptRoot "..\..\Saved\Codex\SHME_V138_20260927\Video\$Lab"
$k = [int][math]::Round(($T0 - $Start) * $Fps) + 1; $tiles = @()
while ($Start + ($k - 1) / $Fps -le $T1 + 1e-6) { $p = Join-Path $V ('f{0:D5}.jpg' -f $k); if (Test-Path $p) { $tiles += ,@($p, ($Start + ($k - 1) / $Fps)) }; $k += $Step }
$tw = [int]($CropW * $Scale); $th = [int]($CropH * $Scale); $rows = [math]::Ceiling($tiles.Count / $Cols)
$bmp = New-Object System.Drawing.Bitmap ($tw * $Cols), ($th * $rows); $g = [System.Drawing.Graphics]::FromImage($bmp); $g.Clear([System.Drawing.Color]::Black)
$font = New-Object System.Drawing.Font('Arial', 14, [System.Drawing.FontStyle]::Bold); $br = [System.Drawing.Brushes]::Yellow
for ($i = 0; $i -lt $tiles.Count; $i++) {
  $src = [System.Drawing.Image]::FromFile($tiles[$i][0]); $x0 = [math]::Max(0, $CX - [int]($CropW / 2)); $y0 = [math]::Max(0, $CY - [int]($CropH / 2))
  $cw = [math]::Min($CropW, $src.Width - $x0); $ch = [math]::Min($CropH, $src.Height - $y0)
  $dst = New-Object System.Drawing.Rectangle (($i % $Cols) * $tw), ([int][math]::Floor($i / $Cols) * $th), $tw, $th
  $srcR = New-Object System.Drawing.Rectangle $x0, $y0, $cw, $ch
  $g.DrawImage($src, $dst, $srcR, [System.Drawing.GraphicsUnit]::Pixel); $g.DrawString(('{0:0.00} s' -f $tiles[$i][1]), $font, $br, $dst.X + 4, $dst.Y + 4); $src.Dispose()
}
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); "CROPSTRIP $Out $($tiles.Count) tiles"
