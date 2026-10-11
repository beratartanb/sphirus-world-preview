#!/bin/bash
# make_gd38_boards.sh : GD38 boards (brow gap + brow symmetry, under-eye / eye-region symmetry, perioral sides). UE captures of the new face t38
# with the GD35 look (calm-eye rest pose, hair, studio unless noted) against the reference and GD37 n37; Blender clay in the solved reference
# cameras (GD37 n37 post-rig vs GD38 T38 target).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD38_Identity_20261011; U=$N/ue; U37=Saved/Codex/GD37_Identity_20261011/ue; P=$N/bd/parts; O=$N/bd/final; mkdir -p $P $O
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; m() { cygpath -m "$(pwd)/$1"; }; w() { cygpath -w "$(pwd)/$1"; }
"$PY" - "$(m $U)" "$(m $U37)" "$(m $N/r)" "$(m $P)" "$(m $N/bd/spec_final.json)" <<'PYE'
import json, sys, os
U, U37, R, P, OUT = sys.argv[1:6]; S = []
NEAR = {'front': [200, 200, 780, 900], 'q3_faceR': [330, 200, 910, 900], 'q3_faceL': [80, 200, 660, 900], 'prof_faceL': [0, 160, 600, 900]}
Z = {'brows_front': ('front', [330, 300, 710, 470]), 'eyes_front': ('front', [340, 330, 700, 530]), 'brows_q3R': ('q3_faceR', [470, 290, 850, 520]),
     'brows_q3L': ('q3_faceL', [200, 290, 580, 520]), 'peri_prof': ('prof_faceL', [30, 400, 370, 740]), 'peri_q3R': ('q3_faceR', [560, 380, 900, 720]),
     'peri_front': ('front', [370, 430, 680, 740])}
for v, r in NEAR.items():
    for nm, src in (('ref', 'REF:'+v), ('g37', f'{U37}/n37e_xlid60_ref_{v}.png'), ('g38', f'{U}/t38e_xlid60_ref_{v}.png')):
        if src.startswith('REF') or os.path.exists(src): S.append(dict(src=src, rect=r, w=380, out=f'{P}/f_{nm}_{v}.jpg'))
    for nm, src in (('g37', f'{U37}/n37_refnh_{v}.png'), ('g38', f'{U}/t38_refnh_{v}.png')):
        if os.path.exists(src): S.append(dict(src=src, rect=r, w=380, out=f'{P}/n_{nm}_{v}.jpg'))
for k, (v, r) in Z.items():
    for nm, src in (('ref', 'REF:'+v), ('g37', f'{U37}/n37e_xlid60_ref_{v}.png'), ('g38', f'{U}/t38e_xlid60_ref_{v}.png'), ('g37n', f'{U37}/n37_refnh_{v}.png'), ('g38n', f'{U}/t38_refnh_{v}.png'),
                    ('g37f', f'{U37}/n37f_refnh_{v}.png'), ('g38f', f'{U}/t38f_refnh_{v}.png'), ('c37', f'{R}/N37PM_REF_{v}_clayA.png'), ('c38', f'{R}/T38PM_REF_{v}_clayA.png')):
        if src.startswith('REF') or os.path.exists(src): S.append(dict(src=src, rect=r, w=420, out=f'{P}/z_{k}_{nm}.jpg'))
json.dump(S, open(OUT, 'w')); print('SPEC', len(S))
PYE
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_parts.py)" -- "$(w $N/bd/spec_final.json)" 2>&1 | grep -oE "PARTS_OK.*"
row() { local r=""; for it in "$@"; do f=${it%%|*}; [ -f $P/$f ] && r="${r:+$r, }$(w $P/$f)|${it#*|}"; done; echo "$r"; }
BD() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $O/$1)" "$2" $3 "${@:4}" >/dev/null; }
BD K1_KASLAR_ARALIK_SIMETRI.jpg "K1 Kaslar - REF / GD37 / GD38 (on: sac gizli; on: sacli sakin goz; saga ve sola bakis sac gizli)" 420 \
  "$(row "z_brows_front_ref.jpg|REF on" "z_brows_front_g37n.jpg|GD37 sac gizli" "z_brows_front_g38n.jpg|GD38 sac gizli")" \
  "$(row "z_brows_front_ref.jpg|REF on" "z_brows_front_g37.jpg|GD37 sacli" "z_brows_front_g38.jpg|GD38 sacli")" \
  "$(row "z_brows_q3R_ref.jpg|REF saga bakis" "z_brows_q3R_g37n.jpg|GD37" "z_brows_q3R_g38n.jpg|GD38")" \
  "$(row "z_brows_q3L_ref.jpg|REF sola bakis" "z_brows_q3L_g37n.jpg|GD37" "z_brows_q3L_g38n.jpg|GD38")"
BD G1_GOZ_ALTI_SIMETRI.jpg "G1 Goz bolgesi ve goz alti - REF / GD37 / GD38 (studyo sac gizli; on isik; kil)" 420 \
  "$(row "z_eyes_front_ref.jpg|REF on" "z_eyes_front_g37n.jpg|GD37 studyo" "z_eyes_front_g38n.jpg|GD38 studyo")" \
  "$(row "z_eyes_front_ref.jpg|REF on" "z_eyes_front_g37f.jpg|GD37 on isik" "z_eyes_front_g38f.jpg|GD38 on isik")" \
  "$(row "z_eyes_front_ref.jpg|REF on" "z_eyes_front_c37.jpg|GD37 kil" "z_eyes_front_c38.jpg|GD38 kil")"
BD D1_PROFIL_DUDAK_YANLARI.jpg "D1 Profil dudak yanlari - REF / GD37 / GD38 (sacli; sac gizli; kil)" 420 \
  "$(row "z_peri_prof_ref.jpg|REF profil" "z_peri_prof_g37.jpg|GD37" "z_peri_prof_g38.jpg|GD38")" \
  "$(row "z_peri_prof_ref.jpg|REF profil" "z_peri_prof_g37n.jpg|GD37 sac gizli" "z_peri_prof_g38n.jpg|GD38 sac gizli")" \
  "$(row "z_peri_prof_ref.jpg|REF profil" "z_peri_prof_c37.jpg|GD37 kil" "z_peri_prof_c38.jpg|GD38 kil")"
BD D2_SAGA_BAKIS_DUDAK_YANLARI.jpg "D2 Saga bakis dudak yanlari - REF / GD37 / GD38 (sacli; on isik; kil)" 420 \
  "$(row "z_peri_q3R_ref.jpg|REF saga bakis" "z_peri_q3R_g37.jpg|GD37" "z_peri_q3R_g38.jpg|GD38")" \
  "$(row "z_peri_q3R_ref.jpg|REF saga bakis" "z_peri_q3R_g37f.jpg|GD37 on isik" "z_peri_q3R_g38f.jpg|GD38 on isik")" \
  "$(row "z_peri_q3R_ref.jpg|REF saga bakis" "z_peri_q3R_c37.jpg|GD37 kil" "z_peri_q3R_c38.jpg|GD38 kil")"
rows=(); for v in q3_faceR q3_faceL front prof_faceL; do rows+=("$(row "f_ref_$v.jpg|REF $v" "f_g37_$v.jpg|GD37" "f_g38_$v.jpg|GD38")"); done; BD F1_SONUC_REF_GD37_GD38_SACLI.jpg "F1 REF / GD37 / GD38 - sacli, sakin goz, studyo" 380 "${rows[@]}"
rows=(); for v in q3_faceR q3_faceL front prof_faceL; do rows+=("$(row "f_ref_$v.jpg|REF $v" "n_g37_$v.jpg|GD37 sac gizli" "n_g38_$v.jpg|GD38 sac gizli")"); done; BD F2_SACSIZ_REF_GD37_GD38.jpg "F2 Sac gizli - REF / GD37 / GD38" 380 "${rows[@]}"
ls $O
