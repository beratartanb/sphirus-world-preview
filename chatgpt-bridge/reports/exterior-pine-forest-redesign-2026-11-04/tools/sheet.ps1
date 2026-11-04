param([string]$Dir, [string]$Out, [int]$Cols = 4, [int]$W = 480, [string]$Filter = '*.png', [string[]]$Names)
# sheet.ps1 -Dir <folder> -Out <file.jpg> [-Cols 4] [-W 480] [-Filter *.png] [-Names a,b,c] : labelled contact sheet (16:9 thumbs)
Add-Type -AssemblyName System.Drawing
$files = if ($Names) { $Names | ForEach-Object { Get-Item -LiteralPath (Join-Path $Dir $_) } } else { Get-ChildItem -LiteralPath $Dir -File -Filter $Filter | Sort-Object Name }
$H = [int]($W * 9 / 16); $lab = 18; $rows = [math]::Ceiling($files.Count / $Cols)
$bmp = New-Object System.Drawing.Bitmap ($Cols * $W), ($rows * ($H + $lab))
$g = [System.Drawing.Graphics]::FromImage($bmp); $g.Clear([System.Drawing.Color]::Black); $g.InterpolationMode = 'HighQualityBicubic'
$font = New-Object System.Drawing.Font('Segoe UI', 9); $brush = [System.Drawing.Brushes]::White
$i = 0
foreach ($f in $files) {
  $img = [System.Drawing.Image]::FromFile($f.FullName)
  $x = ($i % $Cols) * $W; $y = [math]::Floor($i / $Cols) * ($H + $lab)
  $g.DrawImage($img, $x, $y + $lab, $W, $H); $img.Dispose()
  $g.DrawString($f.BaseName, $font, $brush, $x + 3, $y + 1); $i++
}
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters 1; $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, 88L)
$bmp.Save($Out, $enc, $ep); $g.Dispose(); $bmp.Dispose(); "SHEET $Out $($files.Count) files $($Cols)x$rows"
