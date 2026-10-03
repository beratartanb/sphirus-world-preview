#!/bin/bash
# make_gd13_baseboards.sh : GUARDIAN-13 nose-base / perioral boards A-D. REFERENCE | CURRENT (E6) | NEW (F3), clay.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian13_20261003; O=$K/boards_base; P="$O/parts"; mkdir -p "$P"; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_F3; NW=$PV/r_new_F3
ROW a_f.png 440,640,280,520 360 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW a_c.png 470,700,500,760 360 $RC ${CU}_close_clay.png ${NW}_close_clay.png
VS stack_A.png "$P/a_f.png|x" "$P/a_c.png|x"
B A_NOSTRIL_ALAR_UPPER_FORM.jpg "A NOSTRIL / ALAR UPPER FORM: REFERENCE | CURRENT (E6) | NEW (F3) - tip-ala junction + supra-alar groove filled, alar lobule softened, alar-cheek crease filled (no deepening, no inflation of the base)" 1950 "$P/stack_A.png|rows: front / 3/4"
ROW b_f.png 400,700,240,560 330 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW b_c.png 420,760,400,794 330 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW b_p.png 520,900,880,1200 330 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_B.png "$P/b_f.png|x" "$P/b_c.png|x" "$P/b_p.png|x"
B B_NOSE_BASE_INTEGRATION.jpg "B NOSE BASE INTEGRATION: front / 3/4 (REF | CURRENT | NEW) / profile (CURRENT | NEW)" 1950 "$P/stack_B.png|rows: front / 3/4 / profile"
ROW c_f.png 540,700,300,500 330 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW c_c.png 520,760,440,794 330 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW c_p.png 640,900,880,1200 330 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_C.png "$P/c_f.png|x" "$P/c_c.png|x" "$P/c_p.png|x"
B C_PHILTRUM_UPPER_LIP.jpg "C PHILTRUM / UPPER LIP: REFERENCE | CURRENT | NEW (philtrum -> upper-lip concavity filled, white roll softened, perioral relax)" 1950 "$P/stack_C.png|rows: front / 3/4 / profile (CURRENT | NEW)"
ROW d_f.png 500,820,240,560 380 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW d_c.png 480,880,400,794 380 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW d_p.png 600,1150,700,1200 380 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_D.png "$P/d_f.png|x" "$P/d_c.png|x" "$P/d_p.png|x"
B D_FULL_LIP_REGION_INTEGRATION.jpg "D FULL LIP REGION INTEGRATION: REFERENCE | CURRENT | NEW (lower-lip bump trimmed + lateral taper into corners, sublabial groove filled, modiolus filled; mouth line untouched)" 1950 "$P/stack_D.png|rows: front / 3/4 / profile (CURRENT | NEW)"
ls "$O" | grep -c jpg
