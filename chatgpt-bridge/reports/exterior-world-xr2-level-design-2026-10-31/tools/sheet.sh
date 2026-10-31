#!/bin/bash
# sheet.sh <out.png> <cols> <width> <title> <file:label> ... : contact sheet via sheet.ps1 (paths may be POSIX)
O=$(cygpath -w "$1"); C=$2; W=$3; TT=$4; shift 4; F=""; L=""
for a in "$@"; do f=${a%%:*}; l=${a#*:}; F="$F|$(cygpath -w "$f")"; L="$L|$l"; done
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/ExteriorWorld_XR2_20261031/sheet.ps1")" -Out "$O" -Cols $C -W $W -Files "${F:1}" -Labels "${L:1}" -Title "$TT"
