#!/bin/bash
# strip.sh <out.jpg> <x> <y> <w> <h> <scale> <labels a|b|c or ''> <pngdir> <frame numbers...>: crop strip (inline PowerShell)
out=$(cygpath -w "$1"); x=$2; y=$3; w=$4; h=$5; z=$6; lb="$7"; d=$(cygpath -w "$8"); shift 8
fl=""; for n in "$@"; do fl="$fl,'$d\ScreenShot$(printf %05d $n).png'"; done; fl="${fl:1}"
ps=$(cygpath -w "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/UE59Work/rt/strip.ps1")
powershell.exe -NoProfile -Command "\$sb=[scriptblock]::Create((Get-Content -Raw '$ps')); & \$sb -Out '$out' -X $x -Y $y -W $w -H $h -Scale $z -Labels '$lb' -Files @($fl)" 2>&1 | tail -1 | cut -c1-200
