#!/bin/bash
# make_gd37_boards.sh : GD37 boards (lip / nose pass). UE captures of the new face n37 with the GD35 look (calm-eye rest pose, hair, studio light
# unless noted) against the reference and GD36 k36; Blender clay renders in the solved reference cameras (GD36 K36 post-rig vs GD37 N2 target).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD37_Identity_20261011; U=$N/ue; U36=Saved/Codex/GD36_Identity_20261011/ue; P=$N/bd/parts; O=$N/bd/final; mkdir -p $P $O
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; m() { cygpath -m "$(pwd)/$1"; }; w() { cygpath -w "$(pwd)/$1"; }
"$PY" - "$(m $U)" "$(m $U36)" "$(m $N/r)" "$(m $P)" "$(m $N/bd/spec_final.json)" <<'PYE'
import json, sys, os
U, U36, R, P, OUT = sys.argv[1:6]; S = []
NEAR = {'front': [200, 200, 780, 900], 'q3_faceR': [330, 200, 910, 900], 'q3_faceL': [80, 200, 660, 900], 'prof_faceL': [0, 160, 600, 900]}
ZOOM = {'prof_faceL': [30, 400, 370, 740], 'q3_faceR': [560, 380, 900, 720], 'front': [370, 430, 680, 740], 'q3_faceL': [190, 380, 530, 720]}
for v, r in NEAR.items():
    for nm, src in (('ref', 'REF:'+v), ('g36', f'{U36}/k36e_xlid60_ref_{v}.png'), ('g37', f'{U}/n37e_xlid60_ref_{v}.png')):
        if src.startswith('REF') or os.path.exists(src): S.append(dict(src=src, rect=r, w=380, out=f'{P}/f_{nm}_{v}.jpg'))
    for nm, src in (('g36', f'{U36}/k36_refnh_{v}.png'), ('g37', f'{U}/n37_refnh_{v}.png'), ('g36f', f'{U36}/k36f_refnh_{v}.png'), ('g37f', f'{U}/n37f_refnh_{v}.png')):
        if os.path.exists(src): S.append(dict(src=src, rect=r, w=380, out=f'{P}/n_{nm}_{v}.jpg'))
for v, r in ZOOM.items():
    for nm, src in (('ref', 'REF:'+v), ('g36', f'{U36}/k36e_xlid60_ref_{v}.png'), ('g37', f'{U}/n37e_xlid60_ref_{v}.png'), ('g36n', f'{U36}/k36_refnh_{v}.png'), ('g37n', f'{U}/n37_refnh_{v}.png'),
                    ('g36f', f'{U36}/k36f_refnh_{v}.png'), ('g37f', f'{U}/n37f_refnh_{v}.png'), ('c36', f'{R}/K36PM_REF_{v}_clayA.png'), ('c37', f'{R}/N2_REF_{v}_clayA.png')):
        if src.startswith('REF') or os.path.exists(src): S.append(dict(src=src, rect=r, w=420, out=f'{P}/z_{nm}_{v}.jpg'))
json.dump(S, open(OUT, 'w')); print('SPEC', len(S))
PYE
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_parts.py)" -- "$(w $N/bd/spec_final.json)" 2>&1 | grep -oE "PARTS_OK.*"
row() { local r=""; for it in "$@"; do f=${it%%|*}; [ -f $P/$f ] && r="${r:+$r, }$(w $P/$f)|${it#*|}"; done; echo "$r"; }
BD() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $O/$1)" "$2" $3 "${@:4}" >/dev/null; }
BD L1_PROFIL_DUDAK_BURUN.jpg "L1 Profil dudak ve burun - REF / GD36 / GD37 (ust sacli studyo; orta sac gizli; alt kil)" 420 \
  "$(row "z_ref_prof_faceL.jpg|REF profil" "z_g36_prof_faceL.jpg|GD36" "z_g37_prof_faceL.jpg|GD37")" \
  "$(row "z_ref_prof_faceL.jpg|REF profil" "z_g36n_prof_faceL.jpg|GD36 sac gizli" "z_g37n_prof_faceL.jpg|GD37 sac gizli")" \
  "$(row "z_ref_prof_faceL.jpg|REF profil" "z_c36_prof_faceL.jpg|GD36 kil" "z_c37_prof_faceL.jpg|GD37 kil (hedef N2)")"
BD L2_SAGA_BAKIS_DUDAK_BURUN.jpg "L2 Saga bakis (3/4) dudak ve burun - REF / GD36 / GD37 (ust sacli; orta on isik sac gizli; alt kil)" 420 \
  "$(row "z_ref_q3_faceR.jpg|REF saga bakis" "z_g36_q3_faceR.jpg|GD36" "z_g37_q3_faceR.jpg|GD37")" \
  "$(row "z_ref_q3_faceR.jpg|REF saga bakis" "z_g36f_q3_faceR.jpg|GD36 on isik" "z_g37f_q3_faceR.jpg|GD37 on isik")" \
  "$(row "z_ref_q3_faceR.jpg|REF saga bakis" "z_c36_q3_faceR.jpg|GD36 kil" "z_c37_q3_faceR.jpg|GD37 kil (hedef N2)")"
BD L3_ON_BURUN_DUDAK.jpg "L3 Onden burun ve dudak - REF / GD36 / GD37 (ust studyo sacli; orta on isik; alt kil)" 420 \
  "$(row "z_ref_front.jpg|REF on" "z_g36_front.jpg|GD36" "z_g37_front.jpg|GD37")" \
  "$(row "z_ref_front.jpg|REF on" "z_g36f_front.jpg|GD36 on isik" "z_g37f_front.jpg|GD37 on isik")" \
  "$(row "z_ref_front.jpg|REF on" "z_c36_front.jpg|GD36 kil" "z_c37_front.jpg|GD37 kil (hedef N2)")"
rows=(); for v in q3_faceR q3_faceL front prof_faceL; do rows+=("$(row "f_ref_$v.jpg|REF $v" "f_g36_$v.jpg|GD36 (mevcut yuz)" "f_g37_$v.jpg|GD37 dudak ve burun")"); done; BD F1_SONUC_REF_GD36_GD37_SACLI.jpg "F1 REF / GD36 / GD37 - sacli, sakin goz, studyo" 380 "${rows[@]}"
rows=(); for v in q3_faceR q3_faceL front prof_faceL; do rows+=("$(row "f_ref_$v.jpg|REF $v" "n_g36_$v.jpg|GD36 sac gizli" "n_g37_$v.jpg|GD37 sac gizli")"); done; BD F2_SACSIZ_REF_GD36_GD37.jpg "F2 Sac gizli - REF / GD36 / GD37" 380 "${rows[@]}"
ls $O
