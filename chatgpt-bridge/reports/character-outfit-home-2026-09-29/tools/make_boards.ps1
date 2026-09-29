param([string]$spec, [string]$captures, [string]$out)
# spec: JSON {title, cell, rows:[{label, images:[file,...]}]} -> one board JPG (System.Drawing)
Add-Type -AssemblyName System.Drawing
$S = Get-Content $spec -Raw | ConvertFrom-Json
$cell = if ($S.cell) { [int]$S.cell } else { 420 }
$ncol = [int]$S.ncol; $nrows = [int]$S.nrows
$title = New-Object System.Drawing.Font('Segoe UI', 17, [System.Drawing.FontStyle]::Bold); $font = New-Object System.Drawing.Font('Segoe UI', 12)
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters(1); $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]90)
$shade = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(170, 0, 0, 0))
$bmp = New-Object System.Drawing.Bitmap(($cell*$ncol), (46 + $nrows*$cell)); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::FromArgb(24, 27, 31)); $g.InterpolationMode = 'HighQualityBicubic'
$g.DrawString($S.title, $title, [System.Drawing.Brushes]::White, 8, 8)
for ($r = 0; $r -lt $nrows; $r++) {
  $row = $S.rows[$r]
  for ($i = 0; $i -lt $row.images.Count; $i++) {
    $f = Join-Path $captures $row.images[$i]; $x = $i*$cell; $y = 46 + $r*$cell
    if (Test-Path $f) {
      $im = [System.Drawing.Image]::FromFile($f)
      $crop = if ($row.crop) { $row.crop } else { $null }
      if ($crop) { $src = New-Object System.Drawing.Rectangle($crop[0], $crop[1], $crop[2], $crop[3]); $g.DrawImage($im, (New-Object System.Drawing.Rectangle($x, $y, $cell, $cell)), $src, [System.Drawing.GraphicsUnit]::Pixel) }
      else { $g.DrawImage($im, $x, $y, $cell, $cell) }
      $im.Dispose()
    }
    $lab = if ($row.labels) { $row.labels[$i] } else { $row.label }
    $g.FillRectangle($shade, $x, $y, $cell, 24); $g.DrawString($lab, $font, [System.Drawing.Brushes]::White, $x+4, $y+2)
  }
}
$g.Dispose(); $bmp.Save($out, $enc, $ep); $bmp.Dispose(); "saved $out"
