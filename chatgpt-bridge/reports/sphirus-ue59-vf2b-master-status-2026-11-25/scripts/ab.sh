#!/bin/bash
# ab.sh <dirA> <dirB> <out.jpg> [W] [name ...]: two-row BEFORE/AFTER contact sheet (same file names in both folders).
P="<PROJECT>"; cd "$P"; A=$1; B=$2; OUT=$3; W=${4:-640}; shift 4
TMP=Saved/UE59Work/vf2b/_ab; rm -rf $TMP; mkdir -p $TMP
N="$@"; [ -z "$N" ] && N=$(ls $A | sed 's/\.png$//')
c=0; for n in $N; do [ -f $A/$n.png ] && [ -f $B/$n.png ] || continue; cp $A/$n.png "$TMP/A_ONCE_$n.png"; cp $B/$n.png "$TMP/B_SONRA_$n.png"; c=$((c+1)); done
mkdir -p "$(dirname "$OUT")"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File Tools/AAAEnv_20261111/sheet.ps1 -Dir "$(cygpath -w "$P/$TMP")" -Out "$(cygpath -w "$P/$OUT")" -Cols $c -W $W -Cut 2 | tail -1
