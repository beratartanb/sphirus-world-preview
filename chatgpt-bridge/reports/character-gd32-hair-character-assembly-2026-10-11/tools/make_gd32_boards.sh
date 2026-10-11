#!/bin/bash
# make_gd32_boards.sh <label> : GD32 evaluation boards into bd/final/ - every image is a UE capture of the SAVED BP_GD32_Character_G31 in the SAVED level
# L_GD32_Eval_G31 (hair h75c, brow c4, lashes, skin n3), no paint-over. GD31 column = the GD31 studio-harness capture of the same composition (read-only GD31/ue).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD32_Identity_20261011; W31=Saved/Codex/GD31_Identity_20261011; L=$1
O=$W/bd/final; P=$W/bd/parts; mkdir -p $O $P; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
w() { cygpath -w "$(pwd)/$1"; }; m() { cygpath -m "$(pwd)/$1"; }
"$PY" - "$(m $W/ue)" "$(m $W31/ue)" "$(m $P)" "$(m $W/bd/spec_parts.json)" "$L" "${HSR:-250,60,1350,1500}" "${BDR:-500,0,1100,1600}" <<'PYE'
import json, sys, os
U, U31, P, OUT, L, HSR, BDR = sys.argv[1:8]; HSR = [int(x) for x in HSR.split(',')]; BDR = [int(x) for x in BDR.split(',')]; S = []
FACE = {'front': [240, 260, 740, 830], 'q3_faceR': [380, 250, 880, 820], 'q3_faceL': [120, 250, 620, 820], 'prof_faceL': [60, 220, 560, 790]}
WIDE = {'front': None, 'q3_faceR': None, 'q3_faceL': None, 'prof_faceL': None}   # full 2x panel frame
for v in FACE:
    for tag, R_ in (('face', FACE[v]), ('wide', WIDE[v])):
        S.append(dict(src='REF:'+v, rect=R_, w=420, out=f'{P}/ref_{tag}_{v}.jpg'))
        for nm, f in (('g31S', f'{U31}/cg31c4S_ref_{v}.png'), ('g32S', f'{U}/{L}_refS_{v}.png'), ('g32F', f'{U}/{L}_refF_{v}.png')):
            if os.path.exists(f): S.append(dict(src=f, rect=R_, w=420, out=f'{P}/{nm}_{tag}_{v}.jpg'))
for k in ('front', 'q3_faceR', 'q3_faceL', 'prof_faceR', 'prof_faceL', 'back_q3R', 'back', 'back_q3L', 'front_high'):
    f = f'{U}/{L}_hs_{k}_custom.png'
    if os.path.exists(f): S.append(dict(src=f, rect=HSR, w=440, out=f'{P}/hs_{k}.jpg'))
for k in ('front', 'front3q', 'back'):
    f = f'{U}/{L}_body_{k}_custom.png'
    if os.path.exists(f): S.append(dict(src=f, rect=BDR, w=380, out=f'{P}/body_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print('SPEC', len(S))
PYE
"$B" -b --factory-startup --python "$(w Saved/Codex/GD13_Identity_20261009/tools/gd13_parts.py)" -- "$(w $W/bd/spec_parts.json)" 2>&1 | grep -oE "PARTS_OK.*"
board() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $O/$1)" "$2" $3 "${@:4}" | tail -c 60; echo; }
row() { local r=""; for it in "$@"; do f=${it%%|*}; [ -f $P/$f ] && r="${r:+$r, }$(w $P/$f)|${it#*|}"; done; echo "$r"; }
VN=(front q3_faceR q3_faceL prof_faceL)
rows=(); for v in ${VN[@]}; do rows+=("$(row "ref_wide_$v.jpg|REF $v" "g32S_wide_$v.jpg|GD32 birlesik BP - studyo isik")"); done
board B1_REF_ve_BIRLESIK_KARAKTER_SACLI_STUDYO.jpg "B1 REF ve birlesik karakter (GD31 yuz + h75c sac + kas c4) - studyo isigi" 420 "${rows[@]}"
rows=(); for v in ${VN[@]}; do rows+=("$(row "ref_face_$v.jpg|REF $v" "g32S_face_$v.jpg|GD32 studyo" "g32F_face_$v.jpg|GD32 on isik")"); done
board B2_YUZ_YAKIN_SACLI_STUDYO_ve_ONISIK.jpg "B2 Yuz yakin - sacli: REF / studyo / on isik" 420 "${rows[@]}"
board C1_BAS_OMUZ_DONUS_SACLI.jpg "C1 Bas-omuz donus - birlesik karakter, studyo isigi" 440 "$(row "hs_front.jpg|on" "hs_q3_faceR.jpg|3/4 (q3_faceR)" "hs_q3_faceL.jpg|3/4 (q3_faceL)")" "$(row "hs_prof_faceR.jpg|profil (faceR)" "hs_prof_faceL.jpg|profil (faceL)" "hs_front_high.jpg|ustten on")" "$(row "hs_back_q3R.jpg|arka 3/4" "hs_back.jpg|arka" "hs_back_q3L.jpg|arka 3/4")"
board C2_TAM_BOY.jpg "C2 Tam boy - birlesik karakter, studyo isigi" 380 "$(row "body_front.jpg|on" "body_front3q.jpg|on 3/4" "body_back.jpg|arka")"
rows=(); for v in ${VN[@]}; do rows+=("$(row "g31S_face_$v.jpg|GD31 cekim duzeni" "g32S_face_$v.jpg|GD32 kayitli BP+harita")"); done
board V1_DOGRULAMA_GD31_CEKIM_vs_GD32_BP.jpg "V1 Dogrulama - ayni kamera ve isik: GD31 cekim duzeni / GD32 kayitli Blueprint" 420 "${rows[@]}"
ls $O
