# imgconv.ps1 -Mode png2raw|raw2png -In <dir> : lossless PNG <-> raw converter for the numpy metrics (no PIL in any local Python).
# raw format: int32 width, int32 height, then top-down rows of B,G,R bytes (no padding). System.Drawing only; nothing is installed.
param([string]$Mode, [string]$In)
Add-Type -AssemblyName System.Drawing
$fmt = [System.Drawing.Imaging.PixelFormat]::Format24bppRgb
if ($Mode -eq 'png2raw') {
  foreach ($f in Get-ChildItem $In -Filter *.png) {
    $out = [IO.Path]::ChangeExtension($f.FullName, '.raw')
    if ((Test-Path $out) -and ((Get-Item $out).LastWriteTime -ge $f.LastWriteTime)) { continue }
    $bmp = New-Object System.Drawing.Bitmap $f.FullName   # LockBits converts the pixel format directly (no DrawImage scaling)
    $r = New-Object System.Drawing.Rectangle 0, 0, $bmp.Width, $bmp.Height
    $d = $bmp.LockBits($r, 'ReadOnly', $fmt); $row = $bmp.Width * 3
    $buf = New-Object byte[] ($row * $bmp.Height); $tmp = New-Object byte[] $d.Stride
    for ($y = 0; $y -lt $bmp.Height; $y++) {
      [Runtime.InteropServices.Marshal]::Copy([IntPtr]($d.Scan0.ToInt64() + $y * $d.Stride), $tmp, 0, $d.Stride)
      [Array]::Copy($tmp, 0, $buf, $y * $row, $row)
    }
    $bmp.UnlockBits($d)
    $fs = [IO.File]::Create($out); $bw = New-Object IO.BinaryWriter $fs
    $bw.Write([int32]$bmp.Width); $bw.Write([int32]$bmp.Height); $bw.Write($buf); $bw.Close(); $bmp.Dispose()
    Write-Output "RAW $($f.Name)"
  }
} elseif ($Mode -eq 'raw2png') {
  foreach ($f in Get-ChildItem $In -Filter *.raw) {
    $out = [IO.Path]::ChangeExtension($f.FullName, '.png')
    $all = [IO.File]::ReadAllBytes($f.FullName); $w = [BitConverter]::ToInt32($all, 0); $h = [BitConverter]::ToInt32($all, 4)
    $bmp = New-Object System.Drawing.Bitmap $w, $h, $fmt
    $r = New-Object System.Drawing.Rectangle 0, 0, $w, $h
    $d = $bmp.LockBits($r, 'WriteOnly', $fmt); $row = $w * 3
    for ($y = 0; $y -lt $h; $y++) { [Runtime.InteropServices.Marshal]::Copy($all, 8 + $y * $row, [IntPtr]($d.Scan0.ToInt64() + $y * $d.Stride), $row) }
    $bmp.UnlockBits($d); $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose(); Remove-Item $f.FullName
    Write-Output "PNG $([IO.Path]::GetFileName($out))"
  }
}
