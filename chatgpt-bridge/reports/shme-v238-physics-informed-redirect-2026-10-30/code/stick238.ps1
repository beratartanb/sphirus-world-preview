# stick238.ps1 -Json <stick json> -Out <png> [-Step 2] [-Cols 12] [-Scale 1.6] [-T0 0] [-T1 9] [-Top <png>]
# Source review of a TURNING clip without the game (stick236 with a moving view): each tile is drawn in the frame of the clip's own travel
# heading at that frame (root motion over +-2 frames): upper row = side view (current travel to the right), lower row = front view (from
# ahead). Left limbs blue, right orange, trunk / head dark; green dot = ball on the floor. -Top also writes a top view of the whole clip:
# root path (grey), planted balls (blue L / orange R squares), hip-line forward (dark) and shoulder-line forward (red) every 3 frames.
param([string]$Json, [string]$Out, [int]$Step = 2, [int]$Cols = 12, [double]$Scale = 1.6, [double]$T0 = 0.0, [double]$T1 = 9.0, [string]$Top = "")
Add-Type -AssemblyName System.Drawing
$j = Get-Content $Json -Raw | ConvertFrom-Json
$B = @{}; for ($i = 0; $i -lt $j.bones.Count; $i++) { $B[$j.bones[$i]] = $i }
$chains = @(@('pelvis','spine_03','spine_05','neck_01','head', 'k'), @('spine_05','clavicle_l','upperarm_l','lowerarm_l','hand_l','l'), @('spine_05','clavicle_r','upperarm_r','lowerarm_r','hand_r','r'),
            @('pelvis','thigh_l','calf_l','foot_l','ball_l','l'), @('pelvis','thigh_r','calf_r','foot_r','ball_r','r'))
$fr = $j.frames; $n = $fr.Count; $rt = $j.root
function Hd($f) { $a = [math]::Max(0, $f - 2); $b = [math]::Min($n - 1, $f + 2); $dx = $rt[$b][0] - $rt[$a][0]; $dy = $rt[$b][1] - $rt[$a][1]; $l = [math]::Sqrt($dx*$dx + $dy*$dy); if ($l -lt 0.5) { return @($j.fwd[0], $j.fwd[1]) }; return @(($dx / $l), ($dy / $l)) }
$idx = @(); for ($f = 0; $f -lt $n; $f += $Step) { $t = $f * $j.dt; if ($t -ge $T0 - 1e-6 -and $t -le $T1 + 1e-6) { $idx += $f } }
$zmin = [double]::MaxValue; foreach ($f in 0..($n-1)) { foreach ($s in 'ball_l','ball_r') { $z = $fr[$f][$B[$s]][2]; if ($z -lt $zmin) { $zmin = $z } } }
$Hs = [int](125 * $Scale); $tileW = [int](70 * $Scale); $tileH = 2 * $Hs + 18
$rows = [math]::Ceiling($idx.Count / $Cols); $bmp = New-Object System.Drawing.Bitmap ([int]($tileW * $Cols)), ([int]($tileH * $rows))
$g = [System.Drawing.Graphics]::FromImage($bmp); $g.SmoothingMode = 'AntiAlias'; $g.Clear([System.Drawing.Color]::White)
$pen = @{ 'k' = (New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(40,40,40)), 2.2); 'l' = (New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(30,90,220)), 2.0); 'r' = (New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(230,120,20)), 2.0) }
$grey = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(170,170,170)), 1; $font = New-Object System.Drawing.Font 'Arial', ([single](7 * $Scale / 1.6)); $green = [System.Drawing.Brushes]::ForestGreen
$k = 0
foreach ($f in $idx) {
  $cx = ($k % $Cols) * $tileW; $cy = [math]::Floor($k / $Cols) * $tileH; $p = $fr[$f]; $h = Hd $f; $fx = $h[0]; $fy = $h[1]; $lx = -$fy; $ly = $fx
  $pp = $p[$B['pelvis']]; $s = $Scale * 0.5
  $g.DrawString(('{0:N2}s' -f ($f * $j.dt)), $font, [System.Drawing.Brushes]::Black, $cx + 2, $cy + 1)
  foreach ($view in 0, 1) {
    $oy = $cy + 14 + $view * $Hs; $floor = $oy + $Hs - 6
    $g.DrawLine($grey, $cx + 2, $floor, $cx + $tileW - 2, $floor)
    foreach ($c in $chains) {
      $pn = $pen[$c[5]]; $prev = $null
      for ($i = 0; $i -lt 5; $i++) {
        $v = $p[$B[$c[$i]]]; $dx = $v[0] - $pp[0]; $dy = $v[1] - $pp[1]
        if ($view -eq 0) { $X = $cx + $tileW / 2 + ($dx * $fx + $dy * $fy) * $s } else { $X = $cx + $tileW / 2 - ($dx * $lx + $dy * $ly) * $s }
        $Y = $floor - ($v[2] - $zmin) * $s
        if ($prev) { $g.DrawLine($pn, [single]$prev[0], [single]$prev[1], [single]$X, [single]$Y) }
        $prev = @($X, $Y)
      }
    }
    foreach ($bn in 'ball_l', 'ball_r') { $v = $p[$B[$bn]]; if ($v[2] - $zmin -lt 1.5) { $dx = $v[0] - $pp[0]; $dy = $v[1] - $pp[1]; if ($view -eq 0) { $X = $cx + $tileW / 2 + ($dx * $fx + $dy * $fy) * $s } else { $X = $cx + $tileW / 2 - ($dx * $lx + $dy * $ly) * $s }; $g.FillEllipse($green, [single]($X - 2.5), [single]($floor - 2.5), 5, 5) } }
    $hv = $p[$B['head']]; $dx = $hv[0] - $pp[0]; $dy = $hv[1] - $pp[1]; if ($view -eq 0) { $X = $cx + $tileW / 2 + ($dx * $fx + $dy * $fy) * $s } else { $X = $cx + $tileW / 2 - ($dx * $lx + $dy * $ly) * $s }; $Y = $floor - ($hv[2] - $zmin) * $s
    $g.DrawEllipse($pen['k'], [single]($X - 4 * $s), [single]($Y - 4 * $s), [single](8 * $s), [single](8 * $s))
  }
  $k++
}
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); Write-Output "STICK $Out $($idx.Count) frames"
if ($Top) {
  $xs = @(); $ys = @(); foreach ($f in 0..($n-1)) { foreach ($bn in 'ball_l','ball_r','pelvis') { $xs += $fr[$f][$B[$bn]][0]; $ys += $fr[$f][$B[$bn]][1] } }
  $x0 = ($xs | Measure-Object -Minimum).Minimum - 30; $x1 = ($xs | Measure-Object -Maximum).Maximum + 30; $y0 = ($ys | Measure-Object -Minimum).Minimum - 30; $y1 = ($ys | Measure-Object -Maximum).Maximum + 30
  $sc = 900.0 / [math]::Max($x1 - $x0, $y1 - $y0); $Wt = [int](($x1 - $x0) * $sc) + 20; $Ht = [int](($y1 - $y0) * $sc) + 40
  $tb = New-Object System.Drawing.Bitmap $Wt, $Ht; $tg = [System.Drawing.Graphics]::FromImage($tb); $tg.SmoothingMode = 'AntiAlias'; $tg.Clear([System.Drawing.Color]::White)
  # screen: the clip's forward axis points UP, right of the travel to the right
  $F0 = $j.fwd; $R0 = $j.right
  function TP($x, $y) { $u = ($x - $rt[0][0]) * $R0[0] + ($y - $rt[0][1]) * $R0[1]; $v = ($x - $rt[0][0]) * $F0[0] + ($y - $rt[0][1]) * $F0[1]; return @(($Wt / 2 + $u * $sc * 0.9), ($Ht - 30 - ($v + 20) * $sc * 0.9)) }
  $prev = $null; foreach ($f in 0..($n-1)) { $q = TP $rt[$f][0] $rt[$f][1]; if ($prev) { $tg.DrawLine($grey, [single]$prev[0], [single]$prev[1], [single]$q[0], [single]$q[1]) }; $prev = $q }
  $bl = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(30,90,220)); $br = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(230,120,20))
  foreach ($f in 0..($n-1)) { foreach ($sd in 'l','r') { if ($j.planted.$sd[$f]) { $v = $fr[$f][$B['ball_' + $sd]]; $q = TP $v[0] $v[1]; $b_ = if ($sd -eq 'l') { $bl } else { $br }; $tg.FillRectangle($b_, [single]($q[0] - 3), [single]($q[1] - 3), 6, 6) } } }
  $red = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(200,30,30)), 2; $dk = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(40,40,40)), 2
  foreach ($f in 0..($n-1)) { if ($f % 3 -ne 0) { continue }
    $pv = $fr[$f][$B['pelvis']]; $q = TP $pv[0] $pv[1]
    foreach ($pr in @(@('thigh_l','thigh_r',$dk,40), @('clavicle_l','clavicle_r',$red,30))) {
      $a = $fr[$f][$B[$pr[0]]]; $b = $fr[$f][$B[$pr[1]]]; $dx = $b[0] - $a[0]; $dy = $b[1] - $a[1]; $l = [math]::Sqrt($dx*$dx + $dy*$dy); $nx = $dy / $l; $ny = -$dx / $l   # forward = normal of the left->right line
      $e = TP ($pv[0] + $nx * $pr[3]) ($pv[1] + $ny * $pr[3]); $tg.DrawLine($pr[2], [single]$q[0], [single]$q[1], [single]$e[0], [single]$e[1]) }
    $tg.DrawString(('{0:N1}' -f ($f * $j.dt)), $font, [System.Drawing.Brushes]::Gray, [single]($q[0] + 3), [single]($q[1] - 4)) }
  $tb.Save($Top, [System.Drawing.Imaging.ImageFormat]::Png); Write-Output "TOP $Top"
}
