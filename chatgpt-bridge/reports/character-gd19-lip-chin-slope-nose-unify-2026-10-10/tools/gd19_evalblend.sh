#!/bin/bash
# gd19_evalblend.sh <tag> : Blender-only candidate evaluation of data/head_<tag>.npy - geometry checks vs E and G17S, fold scan, fixed-camera measurement
# dump + nose profile lines (gd19_measnose), contour band residuals, lower-face region metrics vs G17S, clay+alpha renders in the 4 solved reference cameras
# and the GD19 overlay boards (REF | candidate | 50 % blend | red-cyan) with GD17 as the first row: full views + nose / chin zooms.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD19_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009; W=Saved/Codex/GD18_Identity_20261010
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; T=$1
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_checks.py)" -- "$(Wp $N/data/head_$T.npy)" "$(Wp $N/data/checks_$T.json)" "$(Wp $N/data/head_E.npy)" "$(Wp $N/data/head_G18S.npy)" 2>&1 | grep -E "^CHECKS|^DISP" | cut -c1-330
"$B" -b --factory-startup --python "$(Wp $N/tools/gd19_foldloc.py)" -- "$(Wp $N/data/head_$T.npy)" "$(Wp $N/data/head_E.npy)" "$(Wp $N/data/head_topo.npz)" 2>&1 | grep -E "^folds|NEW|area" | head -14
bash $N/tools/gd19_measnose.sh $T 2>&1 | grep -E "^PROFLINE $T"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd19_bands.py)" -- "$(Wp $N/meas)" "$(Wp $N/meas/bands_$T.json)" $T 2>&1 | grep "^BAND"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd19_cheekmetrics.py)" -- "$(Wp $N/data/head_G18S.npy)" "$(Wp $N/data/head_topo.npz)" "$(Wp $N/data/cm_$T.json)" "$(Wp $N/data/head_$T.npy)" 2>&1 | grep -c CHEEK >/dev/null
"C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "
import json; d=json.load(open(r'$N/data/cm_$T.json'))
for k,r in d.items(): print('CM', k, {a:b for a,b in r['s'].items()}, 'max', r['max'])"
bash $N/tools/gd19_rset.sh $N/data/head_$T.npy ${T}M $N/data/Ec_cams.json >/dev/null 2>&1; ls $N/r | grep -c "^${T}M_REF" 
declare -A RC=([front]="240 260 740 830" [q3_faceR]="380 250 880 820" [q3_faceL]="120 250 620 820" [prof_faceL]="60 220 560 790")
for v in front q3_faceR q3_faceL prof_faceL; do "$B" -b --factory-startup --python "$(Wp $N/tools/gd19_overlay.py)" -- "$(Wp $N/r/OV_${T}_$v.jpg)" $v ${RC[$v]} 420 "GD18clay=$(Wp $W/r/G18EM_REF_${v}_clayA.png)|$(Wp $W/r/G18EM_REF_${v}_alpha.png)" "${T}clay=$(Wp $N/r/${T}M_REF_${v}_clayA.png)|$(Wp $N/r/${T}M_REF_${v}_alpha.png)" 2>&1 | grep -c OVERLAY_OK | tr '\n' ' '; done
for r in "nose front 400 360 620 660" "nose q3_faceR 560 360 900 660" "nose q3_faceL 60 360 400 660" "nose prof_faceL 0 340 380 640" "chin front 360 560 640 830" "chin q3_faceR 500 540 880 820" "chin q3_faceL 120 540 520 820" "chin prof_faceL 40 500 440 790"; do set -- $r; "$B" -b --factory-startup --python "$(Wp $N/tools/gd19_overlay.py)" -- "$(Wp $N/r/OVZ_${1}_${T}_$2.jpg)" $2 $3 $4 $5 $6 440 "GD18clay=$(Wp $W/r/G18EM_REF_${2}_clayA.png)|$(Wp $W/r/G18EM_REF_${2}_alpha.png)" "${T}clay=$(Wp $N/r/${T}M_REF_${2}_clayA.png)|$(Wp $N/r/${T}M_REF_${2}_alpha.png)" 2>&1 | grep -c OVERLAY_OK | tr '\n' ' '; done; echo; echo EVAL_DONE $T
