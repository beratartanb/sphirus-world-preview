#!/bin/bash
# make_gd13_handboards.sh : GUARDIAN-13 hand-sculpt (topology-aware) boards A-E. REFERENCE | F3 | HAND-SCULPT (HS3), clay.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian13_20261003; O=$K/boards_hand; P="$O/parts"; mkdir -p "$P"; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; HS=$K/hs; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; CU=$PV/r_cur_HS3; NW=$PV/r_new_HS3
ROW a_r.png 470,640,300,500 360 $RF; ROW a_c.png 0,0,0,0 360 $HS/cu_nostril_0.png $HS/hs3_nostril_0.png
ROW a_f.png 0,0,0,0 360 $HS/cu_nose_front_0.png $HS/hs3_nose_front_0.png
VS stack_A.png "$P/a_c.png|x" "$P/a_f.png|x"
B A_NOSTRIL_CLOSEUP.jpg "A NOSTRIL CLOSE-UP: F3 | HAND-SCULPT (rows: from below / front close-up). Alar rim unrolled (lower rim only), lower alar edge joined to the tip line, soft triangle lowered, alar bulge reduced; geodesic (surface-connected) brushes" 1950 "$P/a_r.png|REFERENCE nose base (front photo)" "$P/stack_A.png|F3 | HAND-SCULPT"
ROW b.png 380,700,260,540 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B B_NOSE_BASE_FRONT.jpg "B NOSE BASE FRONT: REFERENCE | F3 | HAND-SCULPT" 1950 "$P/b.png|x"
ROW c.png 380,760,400,794 460 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW c2.png 0,0,0,0 420 $HS/cu_nose_3q_0.png $HS/hs3_nose_3q_0.png $HS/cu_nose_side_0.png $HS/hs3_nose_side_0.png
VS stack_C.png "$P/c.png|x" "$P/c2.png|x"
B C_NOSE_BASE_3Q.jpg "C NOSE BASE 3/4: REFERENCE | F3 | HAND-SCULPT (row 2: close-ups 3/4 F3 | HS, profile F3 | HS)" 1950 "$P/stack_C.png|rows: verified 33 deg 3/4 / close-ups"
ROW d.png 520,780,240,560 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW d3.png 500,820,440,794 460 $RC ${CU}_close_clay.png ${NW}_close_clay.png
VS stack_D.png "$P/d.png|x" "$P/d3.png|x"
B D_LIP_CORNER_MODIOLUS.jpg "D LIP CORNER / MODIOLUS: REFERENCE | F3 | HAND-SCULPT (lower lip tapered into the corner, lateral border trimmed, modiolus mound, upper-lip lateral taper; mouth width and lip seam untouched)" 1950 "$P/stack_D.png|rows: front / 3/4"
ROW e_f.png 380,860,200,600 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW e_c.png 380,880,380,794 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW e_p.png 520,1150,700,1200 400 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_E.png "$P/e_f.png|x" "$P/e_c.png|x" "$P/e_p.png|x"
B E_FULL_PERIORAL.jpg "E FULL PERIORAL REGION: REFERENCE | F3 | HAND-SCULPT (profile row: F3 | HAND-SCULPT)" 1950 "$P/stack_E.png|rows: front / 3/4 / profile"
ls "$O" | grep -c jpg
