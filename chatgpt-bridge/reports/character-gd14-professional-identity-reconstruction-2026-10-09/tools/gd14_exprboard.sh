#!/bin/bash
# gd14_exprboard.sh <label> <out board> <title> : facial-rig check board from ue/<label>_expr_<case>_<front|q3>_custom.png (RigLogic control curves)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; OUT=$2; T=$3; W=Saved/Codex/GD14_Identity_20261009; G=Saved/Codex/GD13_Identity_20261009; P=$W/bd/parts; WD=${WD:-300}
CASES=${CASES:-"neutral blink blink_left look_up look_down look_left brows_up brows_down smile frown lips_closed mouth_open jaw_open jaw_left ph_oo ph_ee ph_mbp cheek_compress extreme"}
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_$OUT.json")" "$L" "$WD" $CASES <<'PYE'
import json, sys, os
U, P, OUT, L, WD = sys.argv[1:6]; C = sys.argv[6:]; S = []
for c in C:
    for k, rc in (('front', [330, 180, 1270, 1330]), ('q3', [300, 180, 1240, 1330])):
        f = f'{U}/{L}_expr_{c}_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=int(WD), out=f'{P}/ex_{L}_{c}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python "$(cygpath -w $G/tools/gd13_parts.py)" -- "$(cygpath -w $W/bd/spec_$OUT.json)" 2>&1 | grep -c PARTS_OK >/dev/null
w() { cygpath -w "$(pwd)/$1"; }; rows=(); r=""; n=0
for c in $CASES; do for k in front q3; do [ -f $P/ex_${L}_${c}_${k}.jpg ] || continue; r="${r:+$r, }$(w $P/ex_${L}_${c}_${k}.jpg)|$c $k"; n=$((n+1)); [ $n -ge ${NCOL:-6} ] && { rows+=("$r"); r=""; n=0; }; done; done; [ -n "$r" ] && rows+=("$r")
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" Tools/CharacterLookdev_20260930/lk_board.py "$(w $W/bd/$OUT)" "$T" $WD "${rows[@]}" | tail -c 50
