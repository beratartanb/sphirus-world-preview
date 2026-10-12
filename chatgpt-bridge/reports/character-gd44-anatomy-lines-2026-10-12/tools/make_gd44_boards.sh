#!/bin/bash
# make_gd44_boards.sh : GD44 body boards from the UE captures (lookdev harness, garment-free; BEFORE = GD44_Body morph zeroed on the same mesh)
# + the Guardian concept comparison. The EVE base-mesh reference sheet is third-party artwork: it goes ONLY into the private board
# (references_private/), never into bd/final or the public report.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD44_Lines_20261012; U=$N/ue; P=$N/bd/parts; O=$N/bd/final; mkdir -p $P $O
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; m() { cygpath -m "$(pwd)/$1"; }; w() { cygpath -w "$(pwd)/$1"; }
"$PY" - "$(m $U)" "$(m $P)" "$(m $N/bd/spec_final.json)" "$(m $N/references_concept)" <<'PYE'
import json, sys, os, glob
U, P, OUT, RC = sys.argv[1:5]; S = []; PFX = os.environ.get('PFX', 'g44')
def first(pat):
    f = sorted(glob.glob(f'{U}/{pat}')); return f[0] if f else None
FULLR = [50, 60, 1550, 1560]
for v in ('front', 'side', 'back', 'front3q', 'rear3q'):
    for mat in ('clay', 'real'):
        for ba in ('before', 'after'):
            f = first(f'{PFX}_{mat}_{v}_{ba}*.png')
            if f: S.append(dict(src=f, rect=FULLR, w=340, out=f'{P}/f_{mat}_{v}_{ba}.jpg'))
for f in sorted(glob.glob(f'{U}/{PFX}_cu_*.png')):
    b = os.path.basename(f).split('_custom')[0].replace(PFX+'_', ''); S.append(dict(src=f, rect=None, w=360, out=f'{P}/{b}.jpg'))
for f in sorted(glob.glob(f'{U}/{PFX}_dfm_*.png')):
    b = os.path.basename(f)[:-4].replace(PFX+'_', ''); S.append(dict(src=f, rect=None, w=300, out=f'{P}/{b}.jpg'))
for k in ('A', 'B'):
    f = f'{RC}/guardian_concept_sheet_{k}.png'
    if os.path.exists(f): S.append(dict(src=f, rect=None, w=700, out=f'{P}/concept_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print('SPEC', len(S))
PYE
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_parts.py)" -- "$(w $N/bd/spec_final.json)" 2>&1 | grep -oE "PARTS_OK.*"
row() { local r=""; for it in "$@"; do f=${it%%|*}; [ -f $P/$f ] && r="${r:+$r, }$(w $P/$f)|${it#*|}"; done; echo "$r"; }
BD() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(w $O/$1)" "$2" $3 "${@:4}" >/dev/null; }
V="front side back front3q rear3q"
for mat in clay real; do rows=(); for ba in before after; do it=(); for v in $V; do it+=("f_${mat}_${v}_${ba}.jpg|$( [ $ba = before ] && echo onceki vucut || echo GD44 vucut ) $v"); done; rows+=("$(row "${it[@]}")"); done
  T=$( [ $mat = clay ] && echo "kil" || echo "ten" ); BD V1_TAM_BOY_${mat^^}_ONCE_SONRA.jpg "V1 Tam boy $T - ust once (onceki vucut) / alt sonra (GD44 vucut), giysisiz" 340 "${rows[@]}"; done
rows=(); for k in chest_front chest_side waist_front3q hip_side glute_rear glute_rear3q back_upper thigh_knee_front3q calf_rear3q shoulder_arm_front3q chest_3q chest_low3q; do rows+=("$(row "cu_clay_${k}_before.jpg|once $k" "cu_clay_${k}_after.jpg|sonra $k" "cu_real_${k}_before.jpg|ten once" "cu_real_${k}_after.jpg|ten sonra")"); done
BD V2_YAKIN_PLAN_ONCE_SONRA_1.jpg "V2 Yakin plan kil ve ten - once / sonra (1)" 360 "${rows[@]:0:5}"; BD V2_YAKIN_PLAN_ONCE_SONRA_2.jpg "V2 Yakin plan kil ve ten - once / sonra (2)" 360 "${rows[@]:5:7}"
rows=(); for p in armsfwd backext crouch elbow elev150 elev180 hipflex squat twist; do rows+=("$(row "dfm_${p}_front3q_before_front3q.jpg|$p once" "dfm_${p}_front3q_after_front3q.jpg|$p sonra" "dfm_${p}_rear3q_before_rear3q.jpg|arka once" "dfm_${p}_rear3q_after_rear3q.jpg|arka sonra")"); done
BD V3_DEFORMASYON_1.jpg "V3 Deformasyon pozlari kil - once / sonra (1)" 300 "${rows[@]:0:5}"; BD V3_DEFORMASYON_2.jpg "V3 Deformasyon pozlari kil - once / sonra (2)" 300 "${rows[@]:5:4}"
BD V4_GUARDIAN_KONSEPT.jpg "V4 Guardian konsepti ve GD44 vucut (ten, giysisiz) - bacak, kol, omuz okumasi" 700 "$(row "concept_B.jpg|Guardian konsept" "f_real_front_after.jpg|GD44 on" "f_real_front3q_after.jpg|GD44 3/4")"
rows=(); for k in chest_front chest_side waist_front3q hip_side glute_rear glute_rear3q back_upper thigh_knee_front3q calf_rear3q shoulder_arm_front3q chest_3q chest_low3q; do rows+=("$(row "cu_clay_${k}_before.jpg|once $k" "cu_clay_${k}_after.jpg|sonra $k")"); done
BD V2K_YAKIN_PLAN_KIL_1.jpg "V2K Yakin plan kil - once / sonra (1)" 360 "${rows[@]:0:5}"; BD V2K_YAKIN_PLAN_KIL_2.jpg "V2K Yakin plan kil - once / sonra (2)" 360 "${rows[@]:5:7}"
ls $O
