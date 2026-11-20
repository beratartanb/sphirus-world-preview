#!/bin/bash
# sheet.sh <out.png> <x> <y> <w> <h> <zoom> <files...>: crop strip (inline PowerShell System.Drawing; -File is blocked by execution policy)
out=$(cygpath -w "$1"); x=$2; y=$3; w=$4; h=$5; z=$6; shift 6
fl=""; for f in "$@"; do fl="$fl,'$(cygpath -w "$f")'"; done; fl="${fl:1}"
ps=$(cygpath -w "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/UE59Work/rt/crop.ps1")
powershell.exe -NoProfile -Command "\$sb=[scriptblock]::Create((Get-Content -Raw '$ps')); & \$sb -Out '$out' -X $x -Y $y -W $w -H $h -Zoom $z -Files @($fl)"
