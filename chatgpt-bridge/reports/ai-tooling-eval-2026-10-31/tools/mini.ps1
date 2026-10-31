param([string]$Out, [double]$Scale, [int]$Cols, [Parameter(ValueFromRemainingArguments=$true)][string[]]$Files)
Add-Type -AssemblyName System.Drawing
$im0 = [System.Drawing.Image]::FromFile($Files[0]); $w = [int]($im0.Width*$Scale); $h = [int]($im0.Height*$Scale); $im0.Dispose()
$rows = [math]::Ceiling($Files.Count / $Cols); $bmp = New-Object System.Drawing.Bitmap ($w*$Cols), ($h*$rows); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::Black); $font = New-Object System.Drawing.Font 'Arial', 11, ([System.Drawing.FontStyle]::Bold)
for ($i=0; $i -lt $Files.Count; $i++) { $im = [System.Drawing.Image]::FromFile($Files[$i]); $x = ($i % $Cols)*$w; $y = [math]::Floor($i/$Cols)*$h
  $g.DrawImage($im, $x, $y, $w, $h); $im.Dispose(); $lab = [IO.Path]::GetFileNameWithoutExtension($Files[$i])
  $sz = $g.MeasureString($lab, $font); $g.FillRectangle([System.Drawing.Brushes]::Black, $x, $y, $sz.Width+4, 18); $g.DrawString($lab, $font, [System.Drawing.Brushes]::Yellow, $x+2, $y+1) }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); "SHEET $Out"
