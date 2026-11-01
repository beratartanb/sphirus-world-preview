# png2jpg.ps1 -Dir <dir> [-Q 88] [-Recurse] : convert every PNG under Dir to JPEG (same basename) and delete the PNG. Publication size only.
param([string]$Dir, [int]$Q = 88, [switch]$Recurse)
Add-Type -AssemblyName System.Drawing
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$ep = New-Object System.Drawing.Imaging.EncoderParameters(1); $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]$Q)
$n = 0; $files = if ($Recurse) { Get-ChildItem $Dir -Filter '*.png' -Recurse } else { Get-ChildItem $Dir -Filter '*.png' }
foreach ($f in $files) { $b = New-Object System.Drawing.Bitmap $f.FullName; $o = [System.IO.Path]::ChangeExtension($f.FullName, '.jpg'); $b.Save($o, $codec, $ep); $b.Dispose(); Remove-Item $f.FullName; $n++ }
"PNG2JPG $n files q$Q $Dir"
