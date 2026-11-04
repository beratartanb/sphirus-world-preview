param([string]$Dirs, [string]$Labels, [string]$Out, [int]$W = 960, [string]$Names = '')
# compare_pairs.ps1 -Dirs "beforeDir|afterDir[|thirdDir]" -Labels "BEFORE|AFTER[|X]" -Out <folder> [-W 960] [-Names "a,b,c"]:
# per station one row JPG (same name across sets, side by side, labelled) + cmp_sheet.jpg of all rows. System.Drawing only.
Add-Type -AssemblyName System.Drawing
$D = $Dirs -split '[|]'; $L = $Labels -split '[|]'; New-Item -ItemType Directory -Force $Out | Out-Null
$files = if ($Names) { $Names -split ',' | ForEach-Object { $_ + '.png' } } else { Get-ChildItem -LiteralPath $D[0] -Filter *.png | Sort-Object Name | ForEach-Object { $_.Name } }
$font = New-Object System.Drawing.Font('Segoe UI', 12, [System.Drawing.FontStyle]::Bold); $brush = [System.Drawing.Brushes]::White; $shadow = [System.Drawing.Brushes]::Black
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters 1; $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, 86L)
$H = [int]($W * 9 / 16); $rows = @()
foreach ($f in $files) {
  $bmp = New-Object System.Drawing.Bitmap ($W * $D.Count), ($H + 22); $g = [System.Drawing.Graphics]::FromImage($bmp); $g.Clear([System.Drawing.Color]::Black); $g.InterpolationMode = 'HighQualityBicubic'
  $g.DrawString(($f -replace '\.png$', ''), $font, $brush, 4, 2)
  for ($k = 0; $k -lt $D.Count; $k++) {
    $p = Join-Path $D[$k] $f
    if (Test-Path -LiteralPath $p) { $img = [System.Drawing.Image]::FromFile($p); $g.DrawImage($img, $k * $W, 22, $W, $H); $img.Dispose() }
    $g.DrawString($L[$k], $font, $shadow, $k * $W + 7, 27); $g.DrawString($L[$k], $font, $brush, $k * $W + 6, 26)
  }
  $o = Join-Path $Out ('cmp_' + ($f -replace '\.png$', '.jpg')); $bmp.Save($o, $enc, $ep); $g.Dispose(); $bmp.Dispose(); $rows += $o
}
# combined sheet (rows stacked, scaled 0.5)
$imgs = $rows | ForEach-Object { [System.Drawing.Image]::FromFile($_) }
$sw = [int]($imgs[0].Width * 0.5); $sh = [int]($imgs[0].Height * 0.5)
$sheet = New-Object System.Drawing.Bitmap $sw, ($sh * $imgs.Count); $g = [System.Drawing.Graphics]::FromImage($sheet); $g.InterpolationMode = 'HighQualityBicubic'
for ($i = 0; $i -lt $imgs.Count; $i++) { $g.DrawImage($imgs[$i], 0, $i * $sh, $sw, $sh); $imgs[$i].Dispose() }
$sheet.Save((Join-Path $Out 'cmp_sheet.jpg'), $enc, $ep); $g.Dispose(); $sheet.Dispose()
"PAIRS $($rows.Count) rows -> $Out"
