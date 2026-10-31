param([string]$Out, [int]$X, [int]$Y, [int]$W, [int]$H, [int]$Zoom, [Parameter(ValueFromRemainingArguments=$true)][string[]]$Files)
Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap ($W*$Zoom*$Files.Count), ($H*$Zoom+18); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = 'NearestNeighbor'; $g.PixelOffsetMode = 'Half'; $g.Clear([System.Drawing.Color]::Black)
$font = New-Object System.Drawing.Font 'Arial', 10, ([System.Drawing.FontStyle]::Bold)
for ($i=0; $i -lt $Files.Count; $i++) { $im = [System.Drawing.Image]::FromFile($Files[$i])
  $g.DrawImage($im, (New-Object System.Drawing.Rectangle ($i*$W*$Zoom), 18, ($W*$Zoom), ($H*$Zoom)), (New-Object System.Drawing.Rectangle $X, $Y, $W, $H), 'Pixel'); $im.Dispose()
  $g.DrawString([IO.Path]::GetFileNameWithoutExtension($Files[$i]), $font, [System.Drawing.Brushes]::Yellow, ($i*$W*$Zoom+2), 2) }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); "CROP $Out"
