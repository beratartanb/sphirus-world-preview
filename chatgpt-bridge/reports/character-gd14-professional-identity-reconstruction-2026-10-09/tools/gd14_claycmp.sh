#!/bin/bash
# gd14_claycmp.sh <out board> <title> <variant e.g. clayB> <label1> [label2 ...] : REF + Blender renders (r/<label>_REF_<view>_<variant>.png) per reference view
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD13_Identity_20261009; N=Saved/Codex/GD14_Identity_20261009; OUT=$1; TITLE=$2; VAR=$3; shift 3; LABS="$*"; WD=${WD:-360}
R="$(cygpath -m "$(pwd)/$N/r")"; P="$(cygpath -m "$(pwd)/$N/bd/parts")"; SP=$N/bd/spec_$(basename $OUT).json
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$R" "$P" "$(cygpath -m "$(pwd)/$SP")" "$VAR" "$WD" $LABS <<'PYE'
import json, sys, os
R, P, OUT, VAR, WD = sys.argv[1:6]; L = sys.argv[6:]; S = []; WD = int(WD)
FACE = {'front': [240, 260, 740, 830], 'q3_faceR': [380, 250, 880, 820], 'q3_faceL': [120, 250, 620, 820], 'prof_faceL': [60, 220, 560, 790]}
for v, rc in FACE.items():
    S.append(dict(src='REF:'+v, rect=rc, w=WD, out=f'{P}/ref_{v}_{WD}.jpg'))
    for l in L:
        f = f'{R}/{l}_REF_{v}_{VAR}.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=WD, out=f'{P}/bl_{l}_{v}_{VAR}_{WD}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python "$(cygpath -w $O/tools/gd13_parts.py)" -- "$(cygpath -w $SP)" 2>&1 | grep -cE "PARTS_OK" >/dev/null
declare -A LN=([w0F]="E taban" [w0]="E taban" [cgd12F]="GD12" [cgd12S]="GD12" [cgd13F]="GD13" [cgd13S]="GD13" [w8F]="W8 (ters firca, atildi)" [w8S]="W8 (atildi)" [w9F]="GD14 (W9)" [w9S]="GD14 (W9)" [W9M]="GD14 (W9)" [E]="E taban" [W8M]="GD14 (W8)" [GD12]="GD12" [GD13]="GD13"); nm() { echo "${LN[$1]:-$1}"; }
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; w() { cygpath -w "$(pwd)/$1"; }; PP=$N/bd/parts; rows=()
for v in ${VIEWS:-front q3_faceR q3_faceL prof_faceL}; do r="$(w $PP/ref_${v}_$WD.jpg)|REF $v"; for l in $LABS; do [ -f $PP/bl_${l}_${v}_${VAR}_$WD.jpg ] && r="$r, $(w $PP/bl_${l}_${v}_${VAR}_$WD.jpg)|$(nm $l) $VAR"; done; rows+=("$r"); done
"$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $N/bd/$OUT)" "$TITLE" $WD "${rows[@]}" | tail -c 60
