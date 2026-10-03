#!/bin/bash
# make_gd12c_boards.sh : GUARDIAN-12C correction boards -> Saved/Codex/CharacterGuardian12C_20261003/boards
# REFERENCE (Tier A front / ~33 deg 3/4 = authority; Tier B profile = aid) | CURRENT = GD12 F (k11, h23) | NEW = GD12C G (k11, h24).
# Clay: pv/r_cur_L5_* (F) / pv/r_new_L5_* (G), temple: pv/r_cur_n3_* / r_new_n3_* (skull identical in n3 and G). UE: z12f_* (F) / z12cf_* (G).
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian12C_20261003; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F12=Saved/Codex/CharacterGuardian12_20261003/frames; FG=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_L5; NW=$PV/r_new_L5; CT=$PV/r_cur_n3; NT=$PV/r_new_n3
# 01 nose form
ROW n_c.png 380,760,400,794 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW n_f.png 380,700,260,540 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png
ROW n_p.png 350,950,650,1200 300 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_01.png "$P/n_c.png|x" "$P/n_f.png|x" "$P/n_p.png|x"
B 01_NOSE_FORM.jpg "01 NOSE FORM: REFERENCE | CURRENT (GD12 F) | CORRECTED (GD12C G) - rows 3/4 / front / profile (profile: CURRENT | CORRECTED)" 1950 "$P/stack_01.png|one profile curve: radix -> 21 deg dorsum -> supratip -> rounded tip; alar bulb flattened, alar crease filled, columella lifted"
# 02 nose consistency (G only: real + clay in front / 3/4 / profile)
ROW c_r.png 380,700,260,540 360 $RF $F12/z12f_real_F.png $FG/z12cf_real_F.png; ROW c_r3.png 380,760,400,794 360 $RC $F12/z12f_real_C.png $FG/z12cf_real_C.png
ROW c_pr.png 150,330,282,482 360 $RP; ROW c_p.png 520,1150,1000,1600 360 $C/z12f_real_side_custom.png $C/z12cf_real_side_custom.png
VS stack_02.png "$P/c_r.png|x" "$P/c_r3.png|x"
B 02_NOSE_FRONT_3Q_PROFILE_CONSISTENCY.jpg "02 NOSE FRONT / 3Q / PROFILE CONSISTENCY (real skin): REFERENCE | GD12 F | GD12C G" 700 "$P/stack_02.png|rows: front / 3/4 (REF | F | G)" "$P/c_pr.png|REF profile (Tier B aid), $P/c_p.png|profile GD12 F | GD12C G"
# 03 lip form
ROW l_f.png 500,800,300,500 420 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW l_c.png 480,840,420,794 420 $RC ${CU}_close_clay.png ${NW}_close_clay.png
ROW l_r.png 500,800,300,500 420 $RF $F12/z12f_real_F.png $FG/z12cf_real_F.png
VS stack_03.png "$P/l_f.png|x" "$P/l_c.png|x" "$P/l_r.png|x"
B 03_LIP_FORM.jpg "03 LIP FORM: REFERENCE | CURRENT (GD12 F) | CORRECTED (GD12C G) - rows front clay / 3/4 clay / front real" 1950 "$P/stack_03.png|lower-lip tube and overhang reduced (-2 mm), upper lip +1 mm ahead, white roll + lower border softened, sublabial fill, corners embedded; width unchanged"
# 04 lip profile / 3/4 relation
ROW lp.png 600,1150,700,1200 330 ${CU}_side_clay.png ${NW}_side_clay.png; ROW lr3.png 480,840,420,794 330 $RC $F12/z12f_real_C.png $FG/z12cf_real_C.png
VS stack_04.png "$P/lp.png|x" "$P/lr3.png|x"
B 04_LIP_PROFILE_3Q_RELATION.jpg "04 LIP PROFILE / 3Q RELATION: profile clay CURRENT | CORRECTED; 3/4 real REF | CURRENT | CORRECTED" 1950 "$P/stack_04.png|upper lip now ~1 mm ahead of lower; lower lip -> labiomental -> chin one soft S"
# 05 hair colour
B 05_HAIR_COLOUR.jpg "05 HAIR COLOUR: REFERENCE | CURRENT h23 | NEW h24 (brown-first auburn: melanin 0.53, redness 0.45 (h23 0.50 / 0.50), red variation 0.12, highlights 0.015, loose 0.62)" 520 "$RF|REFERENCE, $C/z12f_hair_reffront_custom.png|CURRENT h23, $C/z12cf_hair_reffront_custom.png|NEW h24" "$RC|REFERENCE, $C/z12f_hair_refclose2_custom.png|CURRENT h23, $C/z12cf_hair_refclose2_custom.png|NEW h24"
# 06 hair form / bun / rear mass
B 06_HAIR_FORM_BUN_REAR.jpg "06 HAIR FORM / BUN / REAR MASS: CURRENT h23 | NEW h24 (looser breakup, irregular bun + escapes, airier rear, lower side lift; bun height / side-hair start kept)" 360 "$RP|REF profile (aid), $C/z12f_hair_side_custom.png|h23 side, $C/z12cf_hair_side_custom.png|h24 side" "$C/z12f_hair_back_custom.png|h23 rear, $C/z12cf_hair_back_custom.png|h24 rear, $C/z12f_hair_back3q_custom.png|h23 rear 3/4, $C/z12cf_hair_back3q_custom.png|h24 rear 3/4" "$C/z12f_hair_top_custom.png|h23 top, $C/z12cf_hair_top_custom.png|h24 top, $C/z12f_hair_front3q_custom.png|h23 3/4, $C/z12cf_hair_front3q_custom.png|h24 3/4"
# 07 upper temple / side width
B 07_UPPER_TEMPLE_SIDE_WIDTH.jpg "07 UPPER TEMPLE / SIDE WIDTH: CURRENT | NEW (-1.8 mm per side max at z 166-168, top arc z>=171 untouched)" 360 "${CT}_frontstd_clay.png|CURRENT front, ${NT}_frontstd_clay.png|NEW front, ${CT}_rear_clay.png|CURRENT rear, ${NT}_rear_clay.png|NEW rear, ${CT}_top_clay.png|CURRENT top, ${NT}_top_clay.png|NEW top" "$C/z12f_hair_front_custom.png|CURRENT hair front, $C/z12cf_hair_front_custom.png|NEW hair front"
# 08 overall
B 08_OVERALL_FRONT_3Q_PROFILE.jpg "08 OVERALL: REFERENCE | GD12 F | GD12C G" 440 "$RF|REF, $F12/z12f_hair_F.png|GD12 F, $FG/z12cf_hair_F.png|GD12C G" "$RC|REF 3/4, $F12/z12f_hair_C.png|GD12 F, $FG/z12cf_hair_C.png|GD12C G"
# 09 rig / 10 LOD / 11 after restart
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z12cf_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z12cf_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z12cf_rig_${c}_3q_custom.png|$c 3/4"; done
r4=""; for c in neutral ref_expr ref_expr_firm squint_half squint; do r4="$r4, $FG/z12cf_expr_${c}_F.png|$c F, $FG/z12cf_expr_${c}_C.png|$c 3/4"; done
B 09_RIG_TEST.jpg "09 RIG TEST (one fresh auto-rig on G; row 4 = eyelid / squint checks)" 170 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z12c_lod_${l}_front_custom.png|face $l"; done
B 10_LOD.jpg "10 LOD (GD12C face 8 LODs + h24)" 330 "${r#, }"
B 11_AFTER_RESTART.jpg "11 AFTER FRESH RESTART (GD12C assets from disk)" 320 "$FG/rr14f_real_F.png|real front, $FG/rr14f_real_C.png|real 3/4, $FG/rr14f_hair_F.png|hair, $C/rr14f_rig_blink_front_custom.png|blink, $C/rr14f_rig_jaw_open_front_custom.png|jaw open"
ls "$O" | grep -c jpg
