#!/bin/bash
# gd30_rimgrid.sh <SRC tag> <a1 list> <a2 list> : grid over the nostril-margin lift (a1 = posterior y 12.9-13.9, a2 = anterior y 14.0-15.0, mm) on top of
# data/head_<SRC>.npy (narrow bell at the rim margin |x-MX| 1.0 +- 0.22, inner nostril / columella excluded, rim shell 3 mm, sill floor 157.5).
# For each candidate: flips + min area ratio and the nostril-opening IoU vs the reference in 4 views (gd30_cavity.py), one line per candidate.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; V=Saved/Codex/GD30_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; H() { echo "$(Wp $V/data/head_$1.npy)"; }
REF=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel; SRC=$1
for a1 in $2; do for a2 in $3; do T=GR_${a1}_${a2}; T=${T//./p}
P=$("C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -I -c "
import json; a1=$a1; a2=$a2; ys=[12.6,12.9,13.2,13.5,13.8,14.1,14.4,14.7,15.0,15.2]
f=lambda y: (a1*{12.6:0,12.9:.5,13.2:1,13.5:1,13.8:.6,14.1:0}.get(y,0))+(a2*{13.8:0,14.1:.6,14.4:1,14.7:1,15.0:.5,15.2:0}.get(y,0))
print(json.dumps([[y, round(f(y),3)] for y in ys]))")
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_alabell.py)" -- "$(H $SRC)" "$(Wp $V/data/head_topo.npz)" "$(H $T)" "$P" "[0,0,1]" 1.0 0.22 0.55 0.75 0.3 157.5 0.2 159.4 3 2>&1 | grep -E "rror"
FL=$("$B" -b --factory-startup --python "$(Wp $V/tools/_flips.py)" -- "$(Wp $V/data/head_topo.npz)" "$(H E)" "$(H $T)" 2>&1 | grep FLIPS | cut -c1-9)
AR=$("$B" -b --factory-startup --python "$(Wp $V/tools/gd30_foldloc.py)" -- "$(H $T)" "$(H E)" "$(Wp $V/data/head_topo.npz)" 2>&1 | grep -m1 "area ratio" | awk '{print $3}')
S=""; for spec in "q3_faceL|110,150,258,284|10" "q3_faceR|348,398,260,286|10" "prof_faceL|45,95,240,266|8" "front|236,262,262,284|9"; do IFS='|' read v roi pct <<< "$spec"
I=$("$B" -b --factory-startup --python "$(Wp $V/tools/gd30_cavity.py)" -- cmp "$(Wp $V/r/_cg_$v.jpg)" "$(Wp $V/data/cavity_idx.npy)" "$(Wp $V/data/Ec_cams.json)" $v "$(Wp ${REF}_$v.png)" $roi 4 $pct "c=$(H $T)" 2>&1 | grep -oE "IoU [0-9.]+|centre d\(col,row\) [-+0-9. ]+" | paste -sd' '); S="$S | $v $I"; done
echo "a1 $a1 a2 $a2 | $FL area_min $AR $S"; done; done
