# label_map.ps1 -In <png> -Labels <json [[text,[x,y],[r,g,b]],...]> -Out <png> -X0 -Y0 -Ppm [-Title text] : draws world-space text labels
# (Unreal cm, +y down in the image, same frame as xr_maps.py) and a legend title onto a plan render. System.Drawing only.
param([string]$In, [string]$Labels, [string]$Out, [double]$X0, [double]$Y0, [double]$Ppm, [string]$Title = '')
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile($In); $bmp = New-Object System.Drawing.Bitmap $src.Width, ($src.Height + 26); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::White); $g.DrawImage($src, 0, 26, $src.Width, $src.Height); $src.Dispose()
$g.TextRenderingHint = 'AntiAlias'; $font = New-Object System.Drawing.Font 'Arial', 9, ([System.Drawing.FontStyle]::Bold)
$g.DrawString($Title, (New-Object System.Drawing.Font 'Arial', 11, ([System.Drawing.FontStyle]::Bold)), [System.Drawing.Brushes]::Black, 4, 4)
foreach ($l in (Get-Content $Labels -Raw | ConvertFrom-Json)) {
  $t = [string]$l[0]; $px = ($l[1][0] - $X0) / 100 * $Ppm; $py = ($l[1][1] - $Y0) / 100 * $Ppm + 26
  $c = [System.Drawing.Color]::FromArgb(255, [int]$l[2][0], [int]$l[2][1], [int]$l[2][2]); $sz = $g.MeasureString($t, $font)
  $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(200, 255, 255, 255))), $px, $py, $sz.Width, $sz.Height)
  $g.DrawString($t, $font, (New-Object System.Drawing.SolidBrush $c), $px, $py) }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); "LABELED $Out"
