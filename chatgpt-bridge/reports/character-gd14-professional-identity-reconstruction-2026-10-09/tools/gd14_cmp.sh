#!/bin/bash
# gd14_cmp.sh <out board name> <title> <label1> [label2 ...] : REF + each label's renders (GD13 r/ folder, <label>_REF_<view>_<variant>.png) in 4 views (skin A) + clay B rows
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD13_Identity_20261009; N=Saved/Codex/GD14_Identity_20261009; OUT=$1; TITLE=$2; shift 2; LABS="$*"
R="$(cygpath -m "$(pwd)/$O/r")"; P="$(cygpath -m "$(pwd)/$N/bd/parts")"; SP=$N/bd/spec_$OUT.json
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$R" "$P" "$(cygpath -m "$(pwd)/$SP")" $LABS <<'PYE'
import json, sys, os
R, P, OUT = sys.argv[1:4]; L = sys.argv[4:]; S = []
FACE = {'front': [240, 260, 740, 830], 'q3_faceR': [380, 250, 880, 820], 'q3_faceL': [120, 250, 620, 820], 'prof_faceL': [60, 220, 560, 790]}
for v, rc in FACE.items():
    S.append(dict(src='REF:'+v, rect=rc, w=420, out=f'{P}/ref_{v}_420.jpg'))
    for l in L:
        for var in ('skinA', 'clayB', 'clayA'):
            f = f'{R}/{l}_REF_{v}_{var}.png'
            if os.path.exists(f): S.append(dict(src=f, rect=rc, w=420, out=f'{P}/{l}_{v}_{var}_420.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python "$(cygpath -w $O/tools/gd13_parts.py)" -- "$(cygpath -w $SP)" 2>&1 | grep -cE "PARTS_OK"
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; w() { cygpath -w "$(pwd)/$1"; }; PP=$N/bd/parts; rows=()
for v in front q3_faceR q3_faceL prof_faceL; do r="$(w $PP/ref_${v}_420.jpg)|REF $v"; for l in $LABS; do [ -f $PP/${l}_${v}_skinA_420.jpg ] && r="$r, $(w $PP/${l}_${v}_skinA_420.jpg)|$l ten"; done; rows+=("$r"); done
for v in front q3_faceL; do r="$(w $PP/ref_${v}_420.jpg)|REF $v"; for l in $LABS; do [ -f $PP/${l}_${v}_clayB_420.jpg ] && r="$r, $(w $PP/${l}_${v}_clayB_420.jpg)|$l clay B"; done; rows+=("$r"); done
"$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $N/bd/$OUT)" "$TITLE" 420 "${rows[@]}" | tail -c 50
