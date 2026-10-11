#!/bin/bash
# make_gd36_boards.sh : GD36 boards (UE captures of the new face with the GD35 look, calm-eye rest pose, hair, studio light unless noted).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD36_Identity_20261011; U=$N/ue; U35=Saved/Codex/GD35_Identity_20261011/ue; P=$N/bd/parts; O=$N/bd/final; mkdir -p $P $O
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; m() { cygpath -m "$(pwd)/$1"; }; w() { cygpath -w "$(pwd)/$1"; }
for f in $U/k36_common_q3_faceL_custom.png $U/g35b_common_q3_faceL_custom.png $U/k36_common_prof_faceL_custom.png $U/g35b_common_prof_faceL_custom.png; do [ -f $f ] && "$B" -b --factory-startup --python "$(cygpath -w $N/tools/gd36_flip.py)" -- "$(m $f)" "$(m ${f%.png}_flip.png)" 2>&1 | grep -c FLIP_OK >/dev/null; done
"$PY" - "$(m $U)" "$(m $U35)" "$(m $P)" "$(m $N/bd/spec_final.json)" <<'PYE'
import json, sys, os
U, U35, P, OUT = sys.argv[1:5]; S = []
NEAR = {'front': [200, 200, 780, 900], 'q3_faceR': [330, 200, 910, 900], 'q3_faceL': [80, 200, 660, 900], 'prof_faceL': [0, 160, 600, 900]}
for v, r in NEAR.items():
    for nm, src in (('ref', 'REF:'+v), ('g35', f'{U35}/e11_xlid60_ref_{v}.png'), ('g36', f'{U}/k36e_xlid60_ref_{v}.png')):
        if src.startswith('REF') or os.path.exists(src): S.append(dict(src=src, rect=r, w=380, out=f'{P}/f_{nm}_{v}.jpg'))
    for nm, src in (('g35', f'{U35}/bds7n4_refnh_{v}.png'), ('g36', f'{U}/k36_refnh_{v}.png')):
        if os.path.exists(src): S.append(dict(src=src, rect=r, w=380, out=f'{P}/n_{nm}_{v}.jpg'))
CR = [330, 180, 1270, 1300]
for nm in ('g35b', 'k36'):
    for v in ('q3_faceR', 'q3_faceL_custom_flip', 'prof_faceR', 'prof_faceL_custom_flip', 'front'):
        f = f'{U}/{nm}_common_{v}.png' if v.endswith('flip') else f'{U}/{nm}_common_{v}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=CR, w=360, out=f'{P}/c_{nm}_{v}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_parts.py)" -- "$(w $N/bd/spec_final.json)" 2>&1 | grep -oE "PARTS_OK.*"
row() { local r=""; for it in "$@"; do f=${it%%|*}; [ -f $P/$f ] && r="${r:+$r, }$(w $P/$f)|${it#*|}"; done; echo "$r"; }
BD() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $O/$1)" "$2" $3 "${@:4}" >/dev/null; }
rows=(); for v in q3_faceR q3_faceL front prof_faceL; do rows+=("$(row "f_ref_$v.jpg|REF $v" "f_g35_$v.jpg|GD35 (mevcut yuz)" "f_g36_$v.jpg|GD36 simetrik yuz")"); done; BD F1_SONUC_REF_GD35_GD36_SACLI.jpg "F1 REF / GD35 / GD36 (sag yari sol yarinin aynasi) - sacli, sakin goz, studyo" 380 "${rows[@]}"
rows=(); for v in q3_faceR q3_faceL front; do rows+=("$(row "f_ref_$v.jpg|REF $v" "n_g35_$v.jpg|GD35 sac gizli" "n_g36_$v.jpg|GD36 sac gizli")"); done; BD F2_SACSIZ_REF_GD35_GD36.jpg "F2 Sac gizli - REF / GD35 / GD36" 380 "${rows[@]}"
BD S3_SAG_SOL_KARSILASTIRMA.jpg "S3 Saga bakis / sola bakisin aynasi (sabit kameralar) - ust GD35, alt GD36" 360 "$(row "c_g35b_q3_faceR.jpg|GD35 saga bakis (3/4)" "c_g35b_q3_faceL_custom_flip.jpg|GD35 sola bakis yatay cevrik" "c_g35b_prof_faceR.jpg|GD35 sag profil" "c_g35b_prof_faceL_custom_flip.jpg|GD35 sol profil cevrik")" "$(row "c_k36_q3_faceR.jpg|GD36 saga bakis (3/4)" "c_k36_q3_faceL_custom_flip.jpg|GD36 sola bakis yatay cevrik" "c_k36_prof_faceR.jpg|GD36 sag profil" "c_k36_prof_faceL_custom_flip.jpg|GD36 sol profil cevrik")"
ls $O
