#!/bin/bash
# make_gd11_boards.sh : GUARDIAN-11 boards 01-18 -> Saved/Codex/CharacterGuardian12_20261003/boards
# REFERENCE (Tier A front / ~33 deg 3/4 = authority; Tier B profile = low-weight aid) | GD11 (S5 + k7) | GD12 (E + k9). Blender clay pv/r_cur_r2_* (GD11) / pv/r_new_r2_* (GD12);
# UE captures z11f_* (GD11) / z12f_* (GD12); identical cameras / lights.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian12_20261003; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F10=Saved/Codex/CharacterGuardian11_20261002/frames; F11=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_r2; NW=$PV/r_new_r2
B 01_FRONT_CLAY.jpg "01 FRONT CLAY: REFERENCE | GD11 | GD12" 520 "$RF|REFERENCE, ${CU}_front_clay.png|GD11, ${NW}_front_clay.png|GD12"
B 02_3Q_CLAY.jpg "02 3/4 CLAY (verified ~33 deg): REFERENCE | GD11 | GD12" 520 "$RC|REFERENCE, ${CU}_close_clay.png|GD11, ${NW}_close_clay.png|GD12"
B 03_PROFILE_CLAY.jpg "03 PROFILE CLAY: Tier B (low-weight aid) | GD11 | GD12" 520 "$RP|REF profile (aid), ${CU}_side_clay.png|GD11, ${NW}_side_clay.png|GD12"
ROW n_p.png 350,950,650,1200 280 ${CU}_side_clay.png ${NW}_side_clay.png; ROW n_c.png 380,720,420,780 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW n_f.png 380,640,280,540 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png
VS stack_04.png "$P/n_p.png|x" "$P/n_c.png|x" "$P/n_f.png|x"
B 07_PROFILE_NOSE.jpg "07 PROFILE NOSE (lobule fullness restored slightly, radix-bridge flow; no further de-bulbing): profile GD11 / GD12; 3/4 + front REF / GD11 / GD12" 1950 "$P/stack_04.png|rows: profile / 3/4 / front"
ROW m_c.png 360,860,250,794 420 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW m_r.png 360,860,250,794 420 $RC $F10/z11f_real_C.png $F11/z12f_real_C.png
VS stack_05.png "$P/m_c.png|x" "$P/m_r.png|x"
B 05_MIDFACE_SOFT_TISSUE.jpg "05 MIDFACE / SOFT TISSUE (malar + mid-cheek + nasolabial-side + lower-cheek / prejowl support ~0.35-0.4 mm, no hollows, jaw not widened): REF / GD11 / GD12" 1500 "$P/stack_05.png|rows: 3/4 clay / 3/4 real"
ROW l_c.png 560,860,430,780 380 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW l_f.png 560,720,280,540 380 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW l_p.png 600,1150,700,1200 260 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_06.png "$P/l_c.png|x" "$P/l_f.png|x" "$P/l_p.png|x"
B 08_PROFILE_LIPS_MOUTH.jpg "08 LIPS / MOUTH (width unchanged; lips moved down with the lower-face rhythm, no added volume): 3/4 / front REF / GD11 / GD12; profile GD11 / GD12" 1950 "$P/stack_06.png|rows: 3/4 / front / profile"
B 06_LOWER_FACE_RHYTHM.jpg "06 LOWER-FACE RHYTHM (length distributed: philtrum -0.4, lower lip -0.5, chin pad -0.6 mm, symmetric; chin centred, jaw contour identical): REF | GD11 | GD12" 440 "$RP|REF (aid), $C/z11f_real_side_custom.png|GD11, $C/z12f_real_side_custom.png|GD12" "$RC|REF 3/4, $F10/z11f_real_C.png|GD11, $F11/z12f_real_C.png|GD12"
ROW e_f.png 330,500,200,620 320 $RF $F10/z11f_real_F.png $F11/z12f_real_F.png; ROW e_c.png 430,620,380,740 320 $RC $F10/z11f_real_C.png $F11/z12f_real_C.png; ROW e_cl.png 330,500,200,620 320 $RF ${CU}_front_clay.png ${NW}_front_clay.png
VS stack_08.png "$P/e_f.png|x" "$P/e_c.png|x" "$P/e_cl.png|x"
B 04_EYE_BROW_ORBIT.jpg "04 EYE / BROW / ORBIT (upper-lid hood weight 0.9 mm + lateral hood, brow shelter forward, lower-orbit rim support; lid margins <= 0.56 mm, eye joints unchanged, no bags): REF / GD11 / GD12" 1500 "$P/stack_08.png|rows: front real / 3/4 real / front clay"
ROW a_f.png 280,820,160,640 420 $RF $F10/z11f_real_F.png $F11/z12f_real_F.png
VS stack_09.png "$P/a_f.png|x"
B 11_SKIN_REGIONAL_VARIATION.jpg "11 SKIN REGIONAL VARIATION (k11: k9 maps + low-frequency redness excess reduced (nose / cheeks / blotches), lips capped; no new lines): REF / GD11 k9 / GD12 k11 front" 1500 "$P/stack_09.png|rows: front real" "Saved/Codex/CharacterGuardian12_20261003/skin/_redness_k11.png|k11 redness reduction on the UV (red = where red was lowered)"
B 10_SKIN_TONE.jpg "10 SKIN TONE (k11: neutral olive-beige factor 0.78/0.83/0.935, less peach / orange): REFERENCE | GD11 k9 | GD12 k11" 520 "$RF|REFERENCE, $F10/z11f_real_F.png|GD11 k9, $F11/z12f_real_F.png|GD12 k11" "$RC|REFERENCE, $F10/z11f_real_C.png|GD11 k9, $F11/z12f_real_C.png|GD12 k11"
ROW s_cl.png 640,1040,430,830 420 $C/z11f_rig_neutral_front_custom.png $C/z12f_rig_neutral_front_custom.png; ROW s_n.png 380,640,200,600 420 $RF $F10/z11f_real_F.png $F11/z12f_real_F.png
VS stack_11.png "$P/s_cl.png|x" "$P/s_n.png|x"
B 12_SKIN_MICRO_MATERIAL.jpg "12 SKIN MICRO / MATERIAL (normal / SRMF maps unchanged = no added lines; pores / roughness from k9; close cam GD11 / GD12; normal distance REF / GD11 / GD12)" 1500 "$P/stack_11.png|rows: close / normal distance"
B 09_FULL_PROFILE_RHYTHM.jpg "09 FULL PROFILE RHYTHM: Tier B (aid) | GD11 | GD12 clay | GD12 real" 460 "$RP|REF (aid), ${CU}_side_clay.png|GD11, ${NW}_side_clay.png|GD12, $C/z12f_real_side_custom.png|GD12 real"
B 13_FRONT_OVERLAY.jpg "13 FRONT OVERLAY (50% clay over Tier A front): GD11 | GD12" 560 "$PV/rb_cur_r2_front.png|GD11, $PV/rb_new_r2_front.png|GD12"
B 14_3Q_OVERLAY.jpg "14 3/4 OVERLAY (50% clay over Tier A 3/4): GD11 | GD12" 560 "$PV/rb_cur_r2_close.png|GD11, $PV/rb_new_r2_close.png|GD12"
B 16_HAIR_PRESERVATION.jpg "16 HAIR PRESERVATION (h23 unchanged, rebound): GD11 | GD12" 400 "$C/z11f_hair_side_custom.png|GD11 side, $C/z12f_hair_side_custom.png|GD12 side, $C/z11f_hair_back_custom.png|GD11 rear, $C/z12f_hair_back_custom.png|GD12 rear, $F10/z11f_hair_F.png|GD11 front, $F11/z12f_hair_F.png|GD12 front"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z12f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z12f_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z12f_rig_${c}_3q_custom.png|$c 3/4"; done
r4=""; for c in neutral ref_expr_soft ref_expr ref_expr_firm squint_half squint; do r4="$r4, $F11/z12f_expr_${c}_F.png|$c F, $F11/z12f_expr_${c}_C.png|$c 3/4"; done
B 17_RIG_TEST.jpg "17 RIG TEST (one fresh auto-rig on r2; row 4 = squint / reference-expression eyelid checks)" 170 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z12_lod_${l}_front_custom.png|face $l"; done
B 18_LOD.jpg "18 LOD (GD12 face 8 LODs)" 330 "${r#, }"
B 19_AFTER_RESTART.jpg "19 AFTER FRESH RESTART (GD12 assets from disk)" 320 "$F11/rr13f_real_F.png|real front, $F11/rr13f_real_C.png|real 3/4, $F11/rr13f_hair_F.png|hair, $C/rr13f_rig_blink_front_custom.png|blink, $C/rr13f_rig_jaw_open_front_custom.png|jaw open"
B 15_PROFILE_OVERLAY_IF_RELIABLE.jpg "15 PROFILE OVERLAY (Tier B profile fit - LOW reliability: the two generated profile sheets disagree by up to 1.6 cm at the chin): GD11 | GD12" 600 "$PV/profov.png|GD11 left / GD12 right vs Tier B turnaround profile"
ls "$O" | grep -c jpg
