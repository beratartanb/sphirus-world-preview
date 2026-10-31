# triptych.ps1 -Base <pilot dir> -Clip <frames folder name> -Out <dir> [-Scale 0.4] (sets: clean_before | after_g1 | after_g123) : frame-by-frame side-by-side JPGs (same frame number = same
# game time in the fixed-step captures) for an MJPEG AVI via mjpeg_avi.py. Unedited frames, scaled only.
param([string]$Base, [string]$Clip, [string]$Out, [double]$Scale = 0.4)
$Dirs = @('clean_before', 'after_g1', 'after_g123') | ForEach-Object { Join-Path (Join-Path $Base $_) $Clip }
$Labels = @('BEFORE', 'G1', 'G1+G2+G3')
Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force $Out | Out-Null
$n = (Get-ChildItem $Dirs[0] -Filter *.jpg).Count
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters 1; $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 85L
$font = New-Object System.Drawing.Font 'Arial', 13, ([System.Drawing.FontStyle]::Bold)
for ($i = 1; $i -le $n; $i++) {
  $name = 'f{0:D5}.jpg' -f $i; $ims = @()
  foreach ($d in $Dirs) { $p = Join-Path $d $name; if (Test-Path $p) { $ims += [System.Drawing.Image]::FromFile($p) } else { $ims += $null } }
  if ($null -eq $ims[0]) { continue }
  $w = [int]($ims[0].Width * $Scale); $h = [int]($ims[0].Height * $Scale); $w -= $w % 2
  $bmp = New-Object System.Drawing.Bitmap ($w * $Dirs.Count), ($h + 24); $g = [System.Drawing.Graphics]::FromImage($bmp); $g.Clear([System.Drawing.Color]::Black)
  for ($k = 0; $k -lt $Dirs.Count; $k++) {
    if ($ims[$k]) { $g.DrawImage($ims[$k], $k * $w, 24, $w, $h); $ims[$k].Dispose() }
    $g.DrawString(('{0}  t={1:F2}s' -f $Labels[$k], (($i - 1) / 30.0)), $font, [System.Drawing.Brushes]::Yellow, ($k * $w + 4), 3)
  }
  $bmp.Save((Join-Path $Out $name), $enc, $ep); $g.Dispose(); $bmp.Dispose()
}
"TRIPTYCH $n frames -> $Out"
