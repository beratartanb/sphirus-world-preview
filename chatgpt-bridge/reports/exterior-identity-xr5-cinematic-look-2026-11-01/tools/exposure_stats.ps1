# exposure_stats.ps1 -Dirs "d1|d2|..." -Out stats.json : per PNG (sampled every 4th pixel): mean luminance (0-255), % near-white (>=245),
# % near-black (<=10), mean saturation (max-min of RGB / max), mean R/G/B. System.Drawing only.
param([string]$Dirs, [string]$Out)
Add-Type -AssemblyName System.Drawing
$res = @{}
foreach ($d in ($Dirs -split '[|]')) {
  $name = Split-Path $d -Leaf; $res[$name] = @{}
  foreach ($f in Get-ChildItem $d -Filter '*.png') {
    $bmp = New-Object System.Drawing.Bitmap $f.FullName
    $n = 0; $sum = 0.0; $white = 0; $black = 0; $sat = 0.0; $r = 0.0; $g = 0.0; $b = 0.0
    for ($y = 0; $y -lt $bmp.Height; $y += 4) { for ($x = 0; $x -lt $bmp.Width; $x += 4) {
      $c = $bmp.GetPixel($x, $y); $l = 0.2126 * $c.R + 0.7152 * $c.G + 0.0722 * $c.B; $sum += $l; $n++
      if ($l -ge 245) { $white++ }; if ($l -le 10) { $black++ }
      $mx = [math]::Max($c.R, [math]::Max($c.G, $c.B)); $mn = [math]::Min($c.R, [math]::Min($c.G, $c.B)); if ($mx -gt 0) { $sat += ($mx - $mn) / $mx }
      $r += $c.R; $g += $c.G; $b += $c.B } }
    $bmp.Dispose()
    $res[$name][$f.BaseName] = @{ mean = [math]::Round($sum / $n, 1); white_pct = [math]::Round(100.0 * $white / $n, 2); black_pct = [math]::Round(100.0 * $black / $n, 2); sat = [math]::Round($sat / $n, 3); rgb = @([math]::Round($r / $n), [math]::Round($g / $n), [math]::Round($b / $n)) }
  }
}
$res | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 $Out; "STATS $Out"
