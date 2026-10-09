#!/bin/bash
# gd14_uecmp.sh <out board> <title> <set: ref|refnh|refclay> <label1> [label2 ...] : UE real-material board - per reference view a row REF panel + each
# label's capture warped onto that panel frame (ue/<label>_<set>_<view>.png, same solved camera for every candidate). COMMON=1 adds rows of the fixed
# common cameras (ue/<label>_common[nh]_<view>_custom.png, same lens for all) without a reference.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD13_Identity_20261009; N=Saved/Codex/GD14_Identity_20261009; OUT=$1; TITLE=$2; SET=$3; shift 3; LABS="$*"
U="$(cygpath -m "$(pwd)/$N/ue")"; P="$(cygpath -m "$(pwd)/$N/bd/parts")"; SP=$N/bd/spec_$(basename $OUT).json; CS=${CSET:-common}; WD=${WD:-400}
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$U" "$P" "$(cygpath -m "$(pwd)/$SP")" "$SET" "$CS" "$WD" $LABS <<'PYE'
import json, sys, os
U, P, OUT, SET, CS, WD = sys.argv[1:7]; L = sys.argv[7:]; S = []; WD = int(WD)
FACE = {'front': [240, 260, 740, 830], 'q3_faceR': [380, 250, 880, 820], 'q3_faceL': [120, 250, 620, 820], 'prof_faceL': [60, 220, 560, 790]}
for v, rc in FACE.items():
    S.append(dict(src='REF:'+v, rect=rc, w=WD, out=f'{P}/ref_{v}_{WD}.jpg'))
    for l in L:
        f = f'{U}/{l}_{SET}_{v}.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=WD, out=f'{P}/ue_{l}_{SET}_{v}_{WD}.jpg'))
CR = {'front': [400, 260, 1200, 1300], 'q3_faceR': [420, 260, 1220, 1300], 'q3_faceL': [380, 260, 1180, 1300], 'prof_faceL': [330, 260, 1130, 1300], 'prof_faceR': [470, 260, 1270, 1300]}
for l in L:
    for v, rc in CR.items():
        f = f'{U}/{l}_{CS}_{v}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=WD, out=f'{P}/ue_{l}_{CS}_{v}_{WD}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python "$(cygpath -w $O/tools/gd13_parts.py)" -- "$(cygpath -w $SP)" 2>&1 | grep -cE "PARTS_OK" >/dev/null
declare -A LN=([w0F]="E taban" [w0]="E taban" [cgd12F]="GD12" [cgd12S]="GD12" [cgd13F]="GD13" [cgd13S]="GD13" [w8F]="W8 (ters firca, atildi)" [w8S]="W8 (atildi)" [w9F]="GD14 (W9)" [w9S]="GD14 (W9)" [W9M]="GD14 (W9)" [E]="E taban" [W8M]="GD14 (W8)" [GD12]="GD12" [GD13]="GD13"); nm() { echo "${LN[$1]:-$1}"; }
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; w() { cygpath -w "$(pwd)/$1"; }; PP=$N/bd/parts; rows=()
for v in ${VIEWS:-front q3_faceR q3_faceL prof_faceL}; do r="$(w $PP/ref_${v}_$WD.jpg)|REF $v"; for l in $LABS; do [ -f $PP/ue_${l}_${SET}_${v}_$WD.jpg ] && r="$r, $(w $PP/ue_${l}_${SET}_${v}_$WD.jpg)|$(nm $l) UE"; done; rows+=("$r"); done
if [ -n "${COMMON:-}" ]; then for v in front q3_faceR q3_faceL prof_faceL; do r=""; for l in $LABS; do [ -f $PP/ue_${l}_${CS}_${v}_$WD.jpg ] && r="${r:+$r, }$(w $PP/ue_${l}_${CS}_${v}_$WD.jpg)|$(nm $l) ortak $v"; done; [ -n "$r" ] && rows+=("$r"); done; fi
"$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $N/bd/$OUT)" "$TITLE" $WD "${rows[@]}" | tail -c 60
