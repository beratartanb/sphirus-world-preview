# sheet.ps1 -Out <png> -Cols n -W cellwidth -Files "a.png|b.png|..." [-Labels "l1|l2|..."] [-Title t]: contact sheet (System.Drawing).
param([string]$Out, [int]$Cols = 2, [int]$W = 800, [string]$Files, [string]$Labels = "", [string]$Title = '')
Add-Type -AssemblyName System.Drawing
$FL = $Files -split '[|]'; $LB = if ($Labels) { $Labels -split '[|]' } else { @() }
$imgs = $FL | ForEach-Object { [System.Drawing.Image]::FromFile($_) }
$H = [int]($W * $imgs[0].Height / $imgs[0].Width); $rows = [math]::Ceiling($imgs.Count / $Cols); $top = if ($Title) { 28 } else { 0 }
$bmp = New-Object System.Drawing.Bitmap ($Cols * $W), ($rows * $H + $top); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::Black); $g.InterpolationMode = 'HighQualityBicubic'; $g.TextRenderingHint = 'AntiAlias'
$f = New-Object System.Drawing.Font 'Arial', 13, ([System.Drawing.FontStyle]::Bold)
if ($Title) { $g.DrawString($Title, $f, [System.Drawing.Brushes]::White, 6, 5) }
for ($i = 0; $i -lt $imgs.Count; $i++) {
  $x = ($i % $Cols) * $W; $y = [math]::Floor($i / $Cols) * $H + $top; $g.DrawImage($imgs[$i], $x, $y, $W, $H)
  if ($LB.Count -gt $i) { $sz = $g.MeasureString($LB[$i], $f); $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(170, 0, 0, 0))), $x + 4, $y + 4, $sz.Width + 6, $sz.Height + 2); $g.DrawString($LB[$i], $f, [System.Drawing.Brushes]::White, $x + 7, $y + 5) } }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); $imgs | ForEach-Object { $_.Dispose() }; "SHEET $Out"
