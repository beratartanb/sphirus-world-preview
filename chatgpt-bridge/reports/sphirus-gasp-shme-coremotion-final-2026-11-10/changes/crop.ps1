param($Pairs)
# crop.ps1 -Pairs "src,dst;src,dst": game-viewport crop (x5,y168 1510x922) of raw editor window screenshots.
Add-Type -AssemblyName System.Drawing
foreach($p in $Pairs -split ';'){ $a=$p -split ','; $src=$a[0]; $dst=$a[1]
  $img=[System.Drawing.Image]::FromFile($src); $bmp=New-Object System.Drawing.Bitmap(1510,922); $g=[System.Drawing.Graphics]::FromImage($bmp)
  $g.DrawImage($img,(New-Object System.Drawing.Rectangle(0,0,1510,922)),(New-Object System.Drawing.Rectangle(5,168,1510,922)),[System.Drawing.GraphicsUnit]::Pixel); $g.Dispose(); $img.Dispose()
  $bmp.Save($dst,[System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose(); Write-Output "CROP $dst" }
