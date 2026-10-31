# draw_plan.ps1 -Pilot <dir> -Out <png> : top-down map of the rear-trail pilot (UE X = up/north, Y = right/east), 1 px = 2 cm.
# Grey circles = existing instances (crown radius; dark = collision trees/rocks/trunks, green = tall soft, light = low/mid soft),
# blue line = authored TRAIL segment, white dots = pass-A pawn track, coloured arrows = planned moves (G1 red, G2 orange, G3 yellow,
# G4 magenta), cyan = house sight line from the release station, squares = stations.
param([string]$Pilot, [string]$Out)
Add-Type -AssemblyName System.Drawing
$env_ = Get-Content (Join-Path $Pilot 'env_probe.json') -Raw | ConvertFrom-Json
$plan = Get-Content (Join-Path $Pilot 'plan_p1_resolved.json') -Raw | ConvertFrom-Json
$walk = Get-Content (Join-Path $Pilot 'before\trailwalk_log.json') -Raw | ConvertFrom-Json
$cl = $env_.centreline
$xs = @($cl | ForEach-Object { $_.x }); $ys = @($cl | ForEach-Object { $_.y })
$X0 = ($xs | Measure-Object -Minimum).Minimum - 1100; $X1 = ($xs | Measure-Object -Maximum).Maximum + 1100
$Y0 = ($ys | Measure-Object -Minimum).Minimum - 1100; $Y1 = ($ys | Measure-Object -Maximum).Maximum + 1100
$k = 0.5; $W = [int](($Y1 - $Y0) * $k); $H = [int](($X1 - $X0) * $k)
function P($x, $y) { New-Object System.Drawing.PointF ([float](($y - $Y0) * $k)), ([float](($X1 - $x) * $k)) }
$bmp = New-Object System.Drawing.Bitmap $W, ($H + 60); $g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = 'AntiAlias'; $g.Clear([System.Drawing.Color]::FromArgb(255, 28, 32, 28))
foreach ($i in $env_.instances) {
  $p = P $i.x $i.y; $r = [math]::Max(2, $i.crown_r_cm * $k)
  if ($i.collision.camera -like 'ECR_BLOCK*') { $c = [System.Drawing.Color]::FromArgb(150, 120, 110, 100) }
  elseif ($i.height_cm -ge 150) { $c = [System.Drawing.Color]::FromArgb(110, 60, 150, 70) }
  else { $c = [System.Drawing.Color]::FromArgb(70, 150, 170, 120) }
  $b = New-Object System.Drawing.SolidBrush $c; $g.FillEllipse($b, $p.X - $r, $p.Y - $r, 2 * $r, 2 * $r); $b.Dispose()
}
$pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255, 80, 160, 255)), 3
for ($j = 0; $j -lt $cl.Count - 1; $j++) { $g.DrawLine($pen, (P $cl[$j].x $cl[$j].y), (P $cl[$j + 1].x $cl[$j + 1].y)) }
foreach ($t in $walk.passA.ticks) { $p = P $t.pawn[0] $t.pawn[1]; $g.FillEllipse([System.Drawing.Brushes]::White, $p.X - 1, $p.Y - 1, 2, 2) }
$cols = @{ 'G1_nearfield' = [System.Drawing.Color]::Red; 'G2_compression' = [System.Drawing.Color]::Orange; 'G3_tread_edge' = [System.Drawing.Color]::Yellow; 'G4_lookback_window' = [System.Drawing.Color]::Magenta }
foreach ($m in $plan.moves) {
  $pn = New-Object System.Drawing.Pen $cols[$m.group], 2; $pn.CustomEndCap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap 5, 5
  $a = P $m.original.loc[0] $m.original.loc[1]; $b2 = P $m.target.loc[0] $m.target.loc[1]
  $g.DrawLine($pn, $a, $b2); $r = [math]::Max(3, $m.crown_r_cm * $k); $g.DrawEllipse((New-Object System.Drawing.Pen $cols[$m.group], 1), $b2.X - $r, $b2.Y - $r, 2 * $r, 2 * $r)
}
$st = P $plan.moves[0].target.loc[0] $plan.moves[0].target.loc[1]
$rel = $null
foreach ($e in $walk.events) { if ($e.tp_s_cm -in 200, 800, 1400) { $p = P $e.xy[0] $e.xy[1]; $g.FillRectangle([System.Drawing.Brushes]::Cyan, $p.X - 5, $p.Y - 5, 10, 10); if ($e.tp_s_cm -eq 1400) { $rel = $e } } }
if ($rel) { $hp = P 760 695.5; $p = P $rel.xy[0] $rel.xy[1]; $g.DrawLine((New-Object System.Drawing.Pen ([System.Drawing.Color]::Cyan), 1), $p, $hp) }
$font = New-Object System.Drawing.Font 'Arial', 11, ([System.Drawing.FontStyle]::Bold)
$g.DrawString('rear-trail pilot P1 (plan, NOT applied) | N up | 1 px = 2 cm | blue trail, white pawn track, squares stations s 2/8/14 m, cyan = house sight line', $font, [System.Drawing.Brushes]::White, 4, $H + 4)
$g.DrawString('moves: red G1 near-field  orange G2 compression  yellow G3 tread edge  magenta G4 lookback window | dark = collision trees/rocks/trunks, green = tall soft', $font, [System.Drawing.Brushes]::White, 4, $H + 28)
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose(); "PLANMAP $Out ${W}x$H"
