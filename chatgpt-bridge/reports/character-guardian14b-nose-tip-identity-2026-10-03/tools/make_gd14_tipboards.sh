#!/bin/bash
# make_gd14_tipboards.sh : GUARDIAN-14 nose-tip identity boards A-E. HS3 = GD13c (old tip, broken base), K2 = GD14 rigged, NEW = K5 (K2 base + HS3 low-frequency tip + fleshy lobule). Clay, no rig.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian14_20261003; O=$K/boards_tip; P="$O/parts"; mkdir -p "$P"; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; TP=$K/tip; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png
ROW a.png 380,680,280,520 520 $RF $PV/r_cur_FIN_front_clay.png $PV/r_cur_TIP_front_clay.png $PV/r_new_TIP5_front_clay.png
B A_NOSE_FRONT.jpg "A NOSE FRONT: REFERENCE | GD13c HS3 | GD14 K2 | NEW (K5)" 1950 "$P/a.png|x"
ROW b.png 400,720,460,780 520 $RC $PV/r_cur_FIN_close_clay.png $PV/r_cur_TIP_close_clay.png $PV/r_new_TIP5_close_clay.png
B B_NOSE_3Q.jpg "B NOSE 3/4 (verified ~33 deg): REFERENCE | GD13c HS3 | GD14 K2 | NEW (K5)" 1950 "$P/b.png|x"
ROW c.png 250,1000,600,1200 460 $PV/r_cur_FIN_side_clay.png $PV/r_cur_TIP_side_clay.png $PV/r_new_TIP5_side_clay.png
B C_NOSE_PROFILE.jpg "C NOSE PROFILE: GD13c HS3 | GD14 K2 | NEW (Tier B profile = low-weight aid)" 520 "$P/c.png|HS3 | K2 | NEW" "$TP/cu_nose_side_0.png|HS3 close, $TP/cu_nose_side_1.png|K2 close, $TP/cu6_nose_side_0.png|NEW close, $RP|Tier B (aid)"
B D_NOSE_BASE_BELOW.jpg "D NOSE BASE FROM BELOW: GD14 K2 | NEW (base preserved: open nostrils, unrolled rim, columella / sill unchanged)" 560 "$TP/cu_nostril_1.png|GD14 K2, $TP/cu6_nostril_0.png|NEW"
ROW e_r.png 400,640,300,500 520 $RF; ROW e_r3.png 420,700,520,740 520 $RC
B E_TIP_SUPRATIP_CLOSEUP.jpg "E TIP / SUPRATIP CLOSE-UP: REFERENCE | GD14 K2 | NEW (front, 3/4)" 420 "$P/e_r.png|REFERENCE front, $TP/cu_nose_front_1.png|K2 front, $TP/cu6_nose_front_0.png|NEW front" "$P/e_r3.png|REFERENCE 3/4, $TP/cu_nose_3q_1.png|K2 3/4, $TP/cu6_nose_3q_0.png|NEW 3/4"
ls "$O" | grep -c jpg
