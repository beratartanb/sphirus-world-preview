# stick236.ps1 -Json <stick json> -Out <png> [-Step 2] [-Cols 12] [-Scale 1.6] [-T0 0] [-T1 9]
# Source review of a generated clip WITHOUT the game: the clip's own bone positions (component space incl. root motion) drawn per frame as
# a side view (forward to the right, up) over a front view (lateral, up). Left limbs blue, right orange, trunk / head dark; floor line;
# the vertical tick = the root (capsule) position; contact markers (green dot) when a ball is within 1.5 cm of its lowest height.
param([string]$Json, [string]$Out, [int]$Step = 2, [int]$Cols = 12, [double]$Scale = 1.6, [double]$T0 = 0.0, [double]$T1 = 9.0)
Add-Type -AssemblyName System.Drawing
$j = Get-Content $Json -Raw | ConvertFrom-Json
$B = @{}; for ($i = 0; $i -lt $j.bones.Count; $i++) { $B[$j.bones[$i]] = $i }
$chains = @(@('pelvis','spine_03','spine_05','neck_01','head', 'k'), @('spine_05','clavicle_l','upperarm_l','lowerarm_l','hand_l','l'), @('spine_05','clavicle_r','upperarm_r','lowerarm_r','hand_r','r'),
            @('pelvis','thigh_l','calf_l','foot_l','ball_l','l'), @('pelvis','thigh_r','calf_r','foot_r','ball_r','r'))
$fr = $j.frames; $n = $fr.Count
$idx = @(); for ($f = 0; $f -lt $n; $f += $Step) { $t = $f * $j.dt; if ($t -ge $T0 - 1e-6 -and $t -le $T1 + 1e-6) { $idx += $f } }
$zmin = [double]::MaxValue; foreach ($f in 0..($n-1)) { foreach ($s in 'ball_l','ball_r') { $z = $fr[$f][$B[$s]][2]; if ($z -lt $zmin) { $zmin = $z } } }
$W = [int](120 * $Scale / 1.6 * 1.0); $Hs = [int](125 * $Scale); $Hf = [int](125 * $Scale); $tileW = [int](70 * $Scale); $tileH = $Hs + $Hf + 18
$rows = [math]::Ceiling($idx.Count / $Cols); $bmp = New-Object System.Drawing.Bitmap ([int]($tileW * $Cols)), ([int]($tileH * $rows))
$g = [System.Drawing.Graphics]::FromImage($bmp); $g.SmoothingMode = 'AntiAlias'; $g.Clear([System.Drawing.Color]::White)
$pen = @{ 'k' = (New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(40,40,40)), 2.2); 'l' = (New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(30,90,220)), 2.0); 'r' = (New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(230,120,20)), 2.0) }
$grey = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(170,170,170)), 1; $font = New-Object System.Drawing.Font 'Arial', ([single](7 * $Scale / 1.6)); $green = [System.Drawing.Brushes]::ForestGreen
$k = 0
foreach ($f in $idx) {
  $cx = ($k % $Cols) * $tileW; $cy = [math]::Floor($k / $Cols) * $tileH; $p = $fr[$f]
  $py = $p[$B['pelvis']][1]; $px = $p[$B['pelvis']][0]; $s = $Scale * 0.5
  $g.DrawString(('{0:N2}s' -f ($f * $j.dt)), $font, [System.Drawing.Brushes]::Black, $cx + 2, $cy + 1)
  foreach ($view in 0, 1) {
    $oy = $cy + 14 + $view * $Hs; $floor = $oy + $Hs - 6
    $g.DrawLine($grey, $cx + 2, $floor, $cx + $tileW - 2, $floor)
    foreach ($c in $chains) {
      $pn = $pen[$c[5]]; $prev = $null
      for ($i = 0; $i -lt 5; $i++) {
        $v = $p[$B[$c[$i]]]
        if ($view -eq 0) { $X = $cx + $tileW / 2 + ($v[1] - $py) * $s } else { $X = $cx + $tileW / 2 - ($v[0] - $px) * $s }
        $Y = $floor - ($v[2] - $zmin) * $s
        if ($prev) { $g.DrawLine($pn, [single]$prev[0], [single]$prev[1], [single]$X, [single]$Y) }
        $prev = @($X, $Y)
      }
    }
    foreach ($bn in 'ball_l', 'ball_r') { $v = $p[$B[$bn]]; if ($v[2] - $zmin -lt 1.5) { if ($view -eq 0) { $X = $cx + $tileW / 2 + ($v[1] - $py) * $s } else { $X = $cx + $tileW / 2 - ($v[0] - $px) * $s }; $g.FillEllipse($green, [single]($X - 2.5), [single]($floor - 2.5), 5, 5) } }
    $hv = $p[$B['head']]; if ($view -eq 0) { $X = $cx + $tileW / 2 + ($hv[1] - $py) * $s } else { $X = $cx + $tileW / 2 - ($hv[0] - $px) * $s }; $Y = $floor - ($hv[2] - $zmin) * $s
    $g.DrawEllipse($pen['k'], [single]($X - 4 * $s), [single]($Y - 4 * $s), [single](8 * $s), [single](8 * $s))
  }
  $k++
}
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); Write-Output "STICK $Out $($idx.Count) frames"
