#!/bin/bash
# lum.sh <dir> [box]: luminance / clipping stats of every png in <dir> (sorted by leading number) -> <dir>/lum.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; W=$(cygpath -m "$PWD"); D=$1
ls $D/*.png | sort -t/ -k4 -V | while read f; do echo "$W/$f"; done > $D/lum_list.txt
BLWAIT=${BLWAIT:-600} bash Tools/Bio_20261115/bl.sh "$PWD/$D/lum.txt" --background --factory-startup --python "$W/Tools/UE59_20261118/lum_stats.py" -- "$W/$D/lum.txt" "${2:-0.35,0.1,0.65,0.6}" "@$W/$D/lum_list.txt" | tail -1
cat $D/lum.txt 2>/dev/null
